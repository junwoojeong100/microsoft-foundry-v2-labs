import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

from tests import workspace

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_recipes", ROOT / "scripts/check_recipes.py")
PRACTICE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PRACTICE)


class CodePracticeTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name) / "nested" / "personal-recipes"
        self.directory.mkdir(parents=True)
        for name in PRACTICE.RECIPE_NAMES:
            shutil.copy2(ROOT / "examples/recipes" / name, self.directory / name)
        self.stderr = io.StringIO()

    def check(self):
        with redirect_stderr(self.stderr):
            return PRACTICE.check(self.directory)

    def test_reference_copies_pass_outside_the_source_tree_without_azure(self):
        result = self.check()
        self.assertEqual(result["status"], "passed", self.stderr.getvalue())
        self.assertGreater(result["tests_expected"], 0)
        self.assertEqual(result["tests_run"], result["tests_expected"])
        self.assertEqual(result["errors"], 0)
        self.assertEqual(result["failures"], 0)
        self.assertEqual(result["skipped"], 0)
        self.assertTrue(result["source_unchanged"])
        self.assertFalse(result["azure_tested"])
        self.assertFalse(result["model_quality_measured"])
        self.assertEqual(result["fixture_language"], "en")

    def test_documented_store_change_fails_then_restoration_passes(self):
        path = self.directory / "02_responses.py"
        original = path.read_text()
        self.assertIn("store=False", original)
        path.write_text(original.replace("store=False", "store=True", 1))
        broken = self.check()
        self.assertEqual(broken["status"], "failed")
        self.assertGreater(broken["failures"], 0)
        path.write_text(original)
        repaired = self.check()
        self.assertEqual(repaired["status"], "passed", self.stderr.getvalue())
        self.assertNotEqual(broken["recipes_before_sha256"], repaired["recipes_before_sha256"])

    def test_documented_version_and_participant_changes_fail(self):
        for name, before, after in (
            ("03_prompt_agent.py", '"version": version', '"version": "latest"'),
            ("05_maf_sequential.py", "participants=[analyst, writer]", "participants=[writer]"),
        ):
            with self.subTest(recipe=name):
                path = self.directory / name
                original = path.read_text()
                self.assertIn(before, original)
                path.write_text(original.replace(before, after, 1))
                result = self.check()
                self.assertEqual(result["status"], "failed", self.stderr.getvalue())
                self.assertGreater(result["failures"] + result["errors"], 0)
                path.write_text(original)

    def test_network_attempt_is_an_error_not_a_fixture_fallback(self):
        path = self.directory / "02_responses.py"
        original = path.read_text()
        path.write_text(
            original.replace(
                "    response = client.responses.create(",
                "    import socket\n"
                "    socket.create_connection(('unit.invalid', 443))\n"
                "    response = client.responses.create(",
                1,
            )
        )
        result = self.check()
        self.assertEqual(result["status"], "failed")
        self.assertGreater(result["errors"], 0)
        self.assertIn("blocked a network connection", self.stderr.getvalue())

    def test_empty_test_discovery_is_not_success(self):
        with patch.object(
            unittest.defaultTestLoader, "loadTestsFromModule", return_value=unittest.TestSuite()
        ):
            result = self.check()
        self.assertEqual(result["tests_run"], 0)
        self.assertEqual(result["status"], "failed")


class CodePracticeGuideTests(unittest.TestCase):
    def test_both_written_guides_copy_break_repair_and_preserve_prior_reports(self):
        for language, directory in (("en", "docs"), ("ko", "docs/ko")):
            with self.subTest(language=language), workspace() as root:
                for folder in ("tests", "tests_sdk"):
                    shutil.copytree(
                        ROOT / folder,
                        root / folder,
                        ignore=shutil.ignore_patterns("__pycache__"),
                    )
                (root / "scripts").mkdir()
                shutil.copy2(ROOT / "scripts/check_recipes.py", root / "scripts/check_recipes.py")
                text = (ROOT / directory / "code-along.md").read_text()
                blocks = re.findall(r"```bash\n(.*?)```", text, re.DOTALL)
                copy = next(block for block in blocks if "cp examples/recipes/" in block)
                checks = [block for block in blocks if "scripts/check_recipes.py" in block]
                environment = {
                    **os.environ,
                    "PATH": str(Path(sys.executable).parent)
                    + os.pathsep
                    + os.environ.get("PATH", ""),
                    "PYTHONDONTWRITEBYTECODE": "1",
                    "OTEL_SDK_DISABLED": "true",
                }

                def run(block, cwd=root, env=environment):
                    return subprocess.run(
                        ["bash", "-c", block],
                        cwd=cwd,
                        env=env,
                        capture_output=True,
                        text=True,
                        timeout=60,
                        check=False,
                    )

                copied = run(copy)
                self.assertEqual(copied.returncode, 0, copied.stderr)
                baseline = run(checks[0])
                self.assertEqual(baseline.returncode, 0, baseline.stderr)
                personal = root / "outputs" / f"code-along-{language}"
                baseline_report = json.loads((personal / "check-baseline.json").read_text())
                self.assertEqual(baseline_report["status"], "passed")
                recipe = personal / "02_responses.py"
                original = recipe.read_text()
                recipe.write_text(original.replace("store=False", "store=True", 1))
                broken = run(checks[1])
                self.assertEqual(broken.returncode, 1, broken.stderr)
                self.assertEqual(
                    json.loads((personal / "check-store-broken.json").read_text())["status"],
                    "failed",
                )
                recipe.write_text(original)
                repaired = run(checks[2])
                self.assertEqual(repaired.returncode, 0, repaired.stderr)
                report = personal / "check-store-repaired.json"
                saved = report.read_bytes()
                self.assertEqual(json.loads(saved)["status"], "passed")
                self.assertEqual(
                    json.loads(saved)["recipes_before_sha256"],
                    baseline_report["recipes_before_sha256"],
                )
                repeated = run(checks[2])
                self.assertNotEqual(repeated.returncode, 0)
                self.assertEqual(report.read_bytes(), saved)
