import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from foundry_workshop.cli import main, parser

from . import workspace


class CliTests(unittest.TestCase):
    def run_cli(self, root, arguments):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = main(root, arguments)
        return status, stdout.getvalue(), stderr.getvalue()

    def test_help_has_short_usage_an_offline_start_and_every_command(self):
        command_parser = parser()
        self.assertLess(len(command_parser.format_usage()), 140)
        help_text = command_parser.format_help()
        self.assertIn("COMMAND", help_text)
        self.assertIn("First offline pass", help_text)
        self.assertIn("default: ko", help_text)
        self.assertIn("routines", help_text)
        self.assertIn("Fixtures are not model-quality evidence.", help_text)

    def test_invalid_questions_fail_before_cloud_configuration_or_imports(self):
        with tempfile.TemporaryDirectory() as directory:
            for question in ("", " ", "A" * 2001):
                with (
                    self.subTest(question_length=len(question)),
                    patch("foundry_workshop.cli.cloud_command") as cloud,
                ):
                    status, stdout, stderr = self.run_cli(
                        Path(directory), ["maf", "--tools", "--question", question]
                    )
                    self.assertEqual(status, 2)
                    self.assertEqual(stdout, "")
                    self.assertIn("Question must contain 1-2000 characters.", stderr)
                    cloud.assert_not_called()

    def test_local_output_matches_stdout_and_retains_language_and_evidence(self):
        with workspace() as root:
            for language in ("en", "ko"):
                with self.subTest(language=language):
                    notes = root / "outputs" / f"learner-notes-{language}"
                    notes.mkdir(parents=True)
                    target = notes / "retrieve-local.json"
                    status, stdout, stderr = self.run_cli(
                        root,
                        [
                            "--language",
                            language,
                            "retrieve",
                            "--output",
                            str(target.relative_to(root)),
                        ],
                    )
                    self.assertEqual(status, 0, stderr)
                    self.assertEqual(target.read_text(encoding="utf-8"), stdout)
                    result = json.loads(stdout)
                    self.assertEqual(result["provider"], "local-keyword")
                    self.assertIn("TRAVEL-2026", result["source_ids"])
                    self.assertIn("context_hash", result)
                    self.assertTrue(result["documents"])
                    self.assertIn(f"Saved JSON: {target.resolve()}", stderr)

    def test_without_output_the_print_only_contract_is_unchanged(self):
        with workspace() as root:
            status, stdout, stderr = self.run_cli(root, ["retrieve"])
            self.assertEqual(status, 0, stderr)
            self.assertEqual(json.loads(stdout)["provider"], "local-keyword")
            self.assertEqual(stderr, "")
            self.assertFalse((root / "outputs").exists())

    def test_live_commands_save_the_complete_unmodified_result(self):
        result = {
            "mode": "live",
            "response_id": "explicit-unit-test-response",
            "usage": None,
            "trace_id": None,
            "source_ids": ["TRAVEL-2026"],
            "approval_status": "pending-human-review",
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "outputs").mkdir()
            for command in ("model", "answer", "maf", "workflow", "workflow-agent"):
                with (
                    self.subTest(command=command),
                    patch("foundry_workshop.cli.cloud_command", return_value=result) as cloud,
                ):
                    target = root / "outputs" / f"{command}.json"
                    status, stdout, stderr = self.run_cli(
                        root, ["--language", "en", command, "--output", str(target)]
                    )
                    self.assertEqual(status, 0, stderr)
                    self.assertEqual(json.loads(stdout), result)
                    self.assertEqual(target.read_text(), stdout)
                    cloud.assert_called_once()
                    self.assertEqual(cloud.call_args.args[1].language, "en")

    def test_unsafe_existing_or_unprepared_outputs_fail_before_the_request(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notes = root / "outputs/notes"
            notes.mkdir(parents=True)
            existing = notes / "existing.json"
            existing.write_text("Preserve this earlier evidence.\n")
            folder = notes / "folder.json"
            folder.mkdir()
            dangling = notes / "dangling.json"
            dangling.symlink_to(notes / "absent.json")
            outside = root / "outside"
            outside.mkdir()
            linked = notes / "linked"
            linked.symlink_to(outside, target_is_directory=True)
            for target in (
                existing,
                folder,
                dangling,
                linked / "result.json",
                outside / "result.json",
                notes / "result.txt",
                root / "outputs/missing/result.json",
                root / "outputs/../outside/result.json",
            ):
                with (
                    self.subTest(target=target),
                    patch("foundry_workshop.cli.cloud_command") as cloud,
                ):
                    status, stdout, stderr = self.run_cli(root, ["model", "--output", str(target)])
                    self.assertEqual(status, 2)
                    self.assertEqual(stdout, "")
                    self.assertIn("FAIL:", stderr)
                    cloud.assert_not_called()
            self.assertEqual(existing.read_text(), "Preserve this earlier evidence.\n")
            self.assertEqual(list(outside.iterdir()), [])
            self.assertFalse((root / "outputs/missing").exists())
            self.assertTrue(dangling.is_symlink())

    def test_a_failed_request_does_not_create_a_success_shaped_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "outputs").mkdir()
            target = root / "outputs/failed.json"
            with patch(
                "foundry_workshop.cli.cloud_command",
                side_effect=ValueError("Explicit unit-test request failure."),
            ) as cloud:
                status, stdout, stderr = self.run_cli(root, ["model", "--output", str(target)])
            self.assertEqual(status, 2)
            self.assertEqual(stdout, "")
            self.assertIn("Explicit unit-test request failure.", stderr)
            self.assertFalse(target.exists())
            cloud.assert_called_once()

    def test_a_save_race_preserves_the_other_file_and_the_actual_stdout(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "outputs").mkdir()
            target = root / "outputs/race.json"
            result = {"response_id": "unit-response"}

            def competing_writer(*_args):
                target.write_text("Another writer's file.\n")
                return result

            with patch("foundry_workshop.cli.cloud_command", side_effect=competing_writer):
                status, stdout, stderr = self.run_cli(root, ["model", "--output", str(target)])
            self.assertEqual(status, 2)
            self.assertEqual(json.loads(stdout), result)
            self.assertIn("FileExistsError", stderr)
            self.assertNotIn("Saved JSON:", stderr)
            self.assertEqual(target.read_text(), "Another writer's file.\n")

    def test_missing_result_is_not_reported_as_a_successful_export(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "outputs").mkdir()
            target = root / "outputs/missing.json"
            with patch("foundry_workshop.cli.cloud_command", return_value=None):
                status, stdout, stderr = self.run_cli(root, ["model", "--output", str(target)])
            self.assertEqual(status, 2)
            self.assertEqual(stdout, "")
            self.assertIn("No JSON result", stderr)
            self.assertFalse(target.exists())

    def test_invalid_json_result_does_not_leave_a_partial_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "outputs").mkdir()
            target = root / "outputs/invalid.json"
            with patch("foundry_workshop.cli.cloud_command", return_value={"value": float("nan")}):
                status, stdout, stderr = self.run_cli(root, ["model", "--output", str(target)])
            self.assertEqual(status, 2)
            self.assertEqual(stdout, "")
            self.assertIn("FAIL:", stderr)
            self.assertFalse(target.exists())
