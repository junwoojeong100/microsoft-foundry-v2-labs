import io
import json
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from .test_packaging import load_script

VERIFY = load_script("verify_workshop")
RECIPES = load_script("check_recipes")


class WorkshopVerificationTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / "docs").mkdir()
        (self.root / "docs/index.md").write_text("# Synthetic verification test\n")
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()

    def run_verification(self, label="unit", **kwargs):
        with redirect_stdout(self.stdout), redirect_stderr(self.stderr):
            return VERIFY.verify(self.root, label, **kwargs)

    def test_default_gates_are_local_and_report_has_no_logs_or_environment_values(self):
        process = subprocess.CompletedProcess([], 0, "synthetic-private-output\n", "")
        with patch.object(VERIFY.subprocess, "run", return_value=process) as runner:
            result, path = self.run_verification()
        self.assertEqual(result["status"], "passed")
        self.assertEqual(json.loads(path.read_text()), result)
        self.assertEqual(len(result["checks"]), len(VERIFY.CHECKS))
        self.assertEqual(
            [check["name"] for check in result["checks"]],
            [
                "ruff-lint",
                "ruff-format",
                "python-compile",
                "offline-tests",
                "documentation",
                "learner-bundles",
            ],
        )
        self.assertEqual(runner.call_count, len(VERIFY.CHECKS))
        for call in runner.call_args_list:
            self.assertEqual(call.args[0][0], VERIFY.sys.executable)
            self.assertEqual(call.kwargs["cwd"], self.root)
            self.assertEqual(call.kwargs["timeout"], 900)
        for field in (
            "azure_tested",
            "learner_pilot_performed",
            "global_ranking_established",
            "deployment_approved",
            "sdk_checks_selected",
        ):
            self.assertIs(result[field], False)
        self.assertTrue(result["source_unchanged"])
        self.assertNotIn("synthetic-private-output", path.read_text())
        self.assertNotIn(str(self.root), path.read_text())
        self.assertTrue(all(check["command"][0] == "python" for check in result["checks"]))

    def test_failures_stay_failed_while_other_local_checks_still_run(self):
        outcomes = [subprocess.CompletedProcess([], 1, "", "synthetic lint failure\n")]
        outcomes += [subprocess.CompletedProcess([], 0, "", "")] * (len(VERIFY.CHECKS) - 1)
        with patch.object(VERIFY.subprocess, "run", side_effect=outcomes):
            result, path = self.run_verification()
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["checks"][0]["exit_code"], 1)
        self.assertTrue(all(check["status"] == "passed" for check in result["checks"][1:]))
        self.assertIn("synthetic lint failure", self.stderr.getvalue())
        self.assertEqual(json.loads(path.read_text())["status"], "failed")

    def test_timeouts_and_missing_tools_are_not_successful_or_skipped_checks(self):
        for error in (
            subprocess.TimeoutExpired("unit-command", 900),
            FileNotFoundError("unit-tool"),
        ):
            with self.subTest(error=type(error).__name__):
                outcomes = [error] + [subprocess.CompletedProcess([], 0, "", "")] * (
                    len(VERIFY.CHECKS) - 1
                )
                with patch.object(VERIFY.subprocess, "run", side_effect=outcomes):
                    result, _ = self.run_verification(type(error).__name__.lower())
                self.assertEqual(result["status"], "failed")
                self.assertEqual(result["checks"][0]["status"], "failed")
                self.assertIsNone(result["checks"][0]["exit_code"])
                self.assertEqual(result["checks"][0]["failure"], type(error).__name__)

    def test_interrupted_run_keeps_an_honest_partial_report(self):
        with patch.object(VERIFY.subprocess, "run", side_effect=KeyboardInterrupt):
            result, path = self.run_verification()
        self.assertEqual(result["status"], "interrupted")
        self.assertEqual(result["checks"][0]["status"], "interrupted")
        self.assertTrue(all(check["status"] == "not-run" for check in result["checks"][1:]))
        self.assertIsNotNone(result["finished_at"])
        self.assertEqual(json.loads(path.read_text()), result)

    def test_changed_source_cannot_receive_a_passing_report(self):
        def change_source(*_args, **_kwargs):
            (self.root / "docs/index.md").write_text("# Changed during checks\n")
            return subprocess.CompletedProcess([], 0, "", "")

        with patch.object(VERIFY.subprocess, "run", side_effect=change_source):
            result, _ = self.run_verification()
        self.assertEqual(result["status"], "failed")
        self.assertFalse(result["source_unchanged"])
        self.assertNotEqual(result["source_before_sha256"], result["source_after_sha256"])

    def test_existing_run_and_invalid_labels_stop_before_any_check(self):
        process = subprocess.CompletedProcess([], 0, "", "")
        with patch.object(VERIFY.subprocess, "run", return_value=process):
            _, path = self.run_verification()
        before = path.read_bytes()
        with patch.object(VERIFY.subprocess, "run") as runner:
            with self.assertRaises(FileExistsError):
                self.run_verification()
            for label in ("../other", "UPPER", "", "x" * 49):
                with self.subTest(label=label), self.assertRaises(ValueError):
                    self.run_verification(label)
        runner.assert_not_called()
        self.assertEqual(path.read_bytes(), before)

    def test_ancestor_names_are_valid_labels_but_symlinked_outputs_are_not(self):
        for label in ("outputs", "verification"):
            with self.subTest(label=label):
                path = VERIFY.prepare_report(self.root, label)
                self.assertEqual(path, self.root / "outputs/verification" / label / "report.json")
        other = self.root / "other"
        other.mkdir()
        linked_root = self.root / "linked-root"
        linked_root.mkdir()
        (linked_root / "outputs").symlink_to(other, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlinks"):
            VERIFY.prepare_report(linked_root, "untouched")
        self.assertEqual(list(other.iterdir()), [])

    def test_private_outputs_and_env_are_not_fingerprinted(self):
        before = VERIFY.source_fingerprint(self.root)
        (self.root / ".env").write_text("SYNTHETIC_TEST_VALUE=do-not-export\n")
        (self.root / "outputs").mkdir()
        (self.root / "outputs/private.json").write_text('{"synthetic": "private"}')
        self.assertEqual(VERIFY.source_fingerprint(self.root), before)
        (self.root / "docs/index.md").write_text("# Changed guide\n")
        self.assertNotEqual(VERIFY.source_fingerprint(self.root), before)

    def test_source_directory_cannot_redirect_fingerprinting_into_private_outputs(self):
        (self.root / "outputs").mkdir()
        (self.root / "outputs/private.py").write_text("# Synthetic private test file\n")
        (self.root / "src").symlink_to(self.root / "outputs", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "redirected"):
            VERIFY.source_fingerprint(self.root)

    def test_sdk_checks_are_explicit_and_use_the_supported_interpreter(self):
        with patch.object(VERIFY.sys, "version_info", (3, 14, 0)):
            with self.assertRaisesRegex(ValueError, "3.13"):
                self.run_verification(sdk=True)
        self.assertFalse((self.root / "outputs").exists())
        with (
            patch.object(VERIFY.sys, "version_info", (3, 13, 0)),
            patch.object(
                VERIFY.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "", "")
            ),
        ):
            result, _ = self.run_verification(sdk=True)
        self.assertTrue(result["sdk_checks_selected"])
        self.assertEqual(len(result["checks"]), len(VERIFY.CHECKS + VERIFY.SDK_CHECKS))


class CodePracticeInputTests(unittest.TestCase):
    def test_missing_or_redirected_recipe_never_passes_preflight(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, "Missing"):
                RECIPES.recipe_fingerprint(root)
            for name in RECIPES.RECIPE_NAMES:
                (root / name).write_text("# Synthetic recipe test\n")
            before = RECIPES.recipe_fingerprint(root)
            (root / RECIPES.RECIPE_NAMES[0]).write_text("# Changed synthetic recipe\n")
            self.assertNotEqual(RECIPES.recipe_fingerprint(root), before)
            redirected = root / RECIPES.RECIPE_NAMES[0]
            redirected.unlink()
            redirected.symlink_to(root / RECIPES.RECIPE_NAMES[1])
            with self.assertRaisesRegex(ValueError, "redirected"):
                RECIPES.recipe_fingerprint(root)
