import csv
import io
import json
import unittest
import zipfile
from unittest.mock import patch

from foundry_workshop.contracts import load_cases, load_documents
from foundry_workshop.materials import learner_files, policy_document_text

from . import ROOT, workspace
from .test_packaging import load_script

BUILDER = load_script("build_learner_materials")


class LearnerMaterialTests(unittest.TestCase):
    def test_committed_browser_materials_are_exact_generated_outputs(self):
        self.assertEqual(BUILDER.check(ROOT), [])

    def test_questions_and_blank_assessment_never_include_reference_labels_or_holdout(self):
        for language in ("ko", "en"):
            with patch("foundry_workshop.materials.load_cases", wraps=load_cases) as loader:
                files = learner_files(ROOT, language)
            self.assertEqual(loader.call_args.args, (ROOT, "dev", language))
            questions = files["dev-questions.txt"].decode()
            for case in load_cases(ROOT, "dev", language):
                self.assertIn(case["question"], questions)
            for field in ("expected_decision", "expected_limit_krw", "required_citations", "H01"):
                self.assertNotIn(field, questions)
                self.assertNotIn(field, files["instructions-with-policies.txt"].decode())
            dataset = [
                json.loads(line) for line in files["dev-questions.jsonl"].decode().splitlines()
            ]
            self.assertEqual(
                dataset,
                [
                    {"case_id": case["case_id"], "query": case["question"]}
                    for case in load_cases(ROOT, "dev", language)
                ],
            )
            rows = list(csv.DictReader(io.StringIO(files["assessment.csv"].decode("utf-8-sig"))))
            self.assertEqual(len(rows), 6)
            for row in rows:
                self.assertTrue(
                    all(
                        not row[key]
                        for key in (
                            "actual_answer",
                            "actual_document_ids",
                            "pass_or_fail",
                            "review_note",
                        )
                    )
                )

    def test_zip_is_small_safe_and_contains_exactly_the_reviewed_files(self):
        for language in ("ko", "en"):
            files = learner_files(ROOT, language)
            archive = files["learner-materials.zip"]
            self.assertLess(len(archive), 100_000)
            with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
                self.assertIsNone(bundle.testzip())
                self.assertEqual(
                    set(bundle.namelist()), set(files) - {"learner-materials.zip", "manifest.json"}
                )
                self.assertTrue(
                    all(".." not in name and not name.startswith("/") for name in bundle.namelist())
                )
                for name in bundle.namelist():
                    self.assertEqual(bundle.read(name), files[name])

    def test_policy_exports_keep_original_ids_dates_and_text(self):
        for language in ("ko", "en"):
            files = learner_files(ROOT, language)
            for document in load_documents(ROOT, language):
                rendered = policy_document_text(document)
                self.assertEqual(files[f"policies/{document['id']}.txt"].decode(), rendered)
                self.assertIn(document["content"], rendered)
                self.assertIn(document["effective_from"], rendered)
                self.assertIn(document["effective_to"], rendered)

    def test_start_file_keeps_policy_inspection_in_the_core_route(self):
        for language in ("en", "ko"):
            with self.subTest(language=language):
                start = learner_files(ROOT, language)["START-HERE.txt"].decode()
                policy_line = next(line for line in start.splitlines() if "policies/" in line)
                self.assertIn("Lab 03", policy_line)
                self.assertIn("06", policy_line)
                self.assertNotIn("File Search", policy_line)
                optional_line = next(
                    line for line in start.splitlines() if "instructions.txt" in line
                )
                self.assertIn("File Search", optional_line)
                self.assertNotIn("policies/", optional_line)

    def test_evidence_templates_are_blank_localized_and_in_the_start_sequence(self):
        for language, marker in (("en", "BLANK WORKSHEET"), ("ko", "빈 기록 양식")):
            with self.subTest(language=language):
                files = learner_files(ROOT, language)
                start = files["START-HERE.txt"].decode()
                for name in (
                    "session-notes.txt",
                    "workflow-review.txt",
                    "operations-checklist.txt",
                ):
                    text = files[name].decode()
                    self.assertTrue(text.startswith(marker))
                    self.assertIn(name, start)
                    fields = [line for line in text.splitlines() if ":" in line]
                    self.assertGreaterEqual(len(fields), 7)
                    self.assertTrue(all(line.endswith(":") for line in fields))
                    for answer_key in ("expected_limit_krw", "required_citations", "H01"):
                        self.assertNotIn(answer_key, text)
                notes = files["session-notes.txt"].decode()
                for lab in ("00", "01", "02", "03", "06", "07"):
                    self.assertIn(f"Lab {lab}", notes)
                self.assertIn("assessment-baseline.csv", start)
                self.assertIn("approval_status", files["workflow-review.txt"].decode())
                self.assertIn("external_actions_performed", files["workflow-review.txt"].decode())

    def test_setup_card_has_a_blank_search_endpoint_handoff_for_b(self):
        for language, field in (
            ("en", "Search endpoint (B only):"),
            ("ko", "Search endpoint(B 전용):"),
        ):
            with self.subTest(language=language):
                notes = learner_files(ROOT, language)["session-notes.txt"].decode()
                card = notes.split("\nLab 00 -", 1)[1].split("\n\n", 1)[0]
                self.assertIn(field, card.splitlines())
                directory = ROOT / ("docs" if language == "en" else "docs/ko")
                setup = (directory / "setup.md").read_text()
                self.assertIn(f"`{field}`", setup)
                self.assertIn("Lab 06", setup)

    def test_workflow_review_uses_saved_paths_for_b_without_requiring_a_second_json_copy(self):
        for language, fields in (
            ("en", ("Saved JSON file path (B only):", "Complete actual JSON output (A only):")),
            ("ko", ("저장된 JSON 파일 경로(B 전용):", "실제 JSON 출력 전체(A 전용):")),
        ):
            with self.subTest(language=language):
                files = learner_files(ROOT, language)
                review = files["workflow-review.txt"].decode()
                self.assertIn("--output", review)
                for field in fields:
                    self.assertIn(field + "\n", review)
                for pattern in ("sequential", "concurrent", "group-chat"):
                    self.assertIn(pattern, review)

    def test_workflow_review_supports_the_browser_question_and_hosted_profile(self):
        for language, fields in (
            (
                "en",
                (
                    "Hosted agent name / version (Playground option only):",
                    "Exact command / Playground question:",
                ),
            ),
            (
                "ko",
                (
                    "Hosted agent 이름 / 버전(Playground 방식만):",
                    "정확한 명령 / Playground 질문:",
                ),
            ),
        ):
            with self.subTest(language=language):
                review = learner_files(ROOT, language)["workflow-review.txt"].decode()
                for field in fields:
                    self.assertIn(field + "\n", review)
                self.assertIn("runtime_profile.pattern", review)

    def test_session_notes_separate_routes_and_provide_blank_b_review_fields(self):
        for language, headings in (
            ("en", ("A - browser notes only", "B - code evidence and handoff", "Pause / resume")),
            ("ko", ("A - 브라우저 전용 기록", "B - 코드 근거와 인계", "중단 / 재개")),
        ):
            with self.subTest(language=language):
                notes = learner_files(ROOT, language)["session-notes.txt"].decode()
                a_heading, b_heading, resume_heading = (f"\n{heading}\n" for heading in headings)
                for heading in (a_heading, b_heading, resume_heading):
                    self.assertTrue(heading in notes, f"{language}: missing section {heading!r}")
                self.assertLess(notes.index("\nLab 00 -"), notes.index(a_heading))
                self.assertLess(notes.index(a_heading), notes.index(b_heading))
                self.assertLess(notes.index(b_heading), notes.index(resume_heading))
                browser = notes.split(a_heading, 1)[1].split(b_heading, 1)[0]
                code = notes.split(b_heading, 1)[1].split(resume_heading, 1)[0]
                self.assertIn("Playground", browser)
                self.assertIn("assessment-baseline.csv", browser)
                self.assertNotIn("Playground", code)
                self.assertNotIn("assessment-baseline.csv", code)
                fields = [line for line in code.splitlines() if line.startswith("Lab ")]
                self.assertTrue(all(line.endswith(":") for line in fields))
                self.assertEqual(
                    [line.split()[1] for line in fields],
                    ["02", "03", "04", "05", "06", "06", "07", "07", "07", "07", "08", "11"],
                )
                architecture = next(line for line in fields if line.startswith("Lab 11 "))
                directory = ROOT / ("docs" if language == "en" else "docs/ko")
                capstone = (directory / "labs/11-capstone.md").read_text()
                handoff = capstone.split('<a id="b-architecture"></a>', 1)[1]
                self.assertIn(f"`{architecture}`", handoff.split("\n\n", 1)[1])
                for name in (
                    "model.json",
                    "answer-local.json",
                    "prompt-agent-create.json",
                    "prompt-agent-invoke.json",
                    "maf-none.json",
                    "maf-function.json",
                    "maf-mcp.json",
                    "workflow-review.txt",
                    "answer-iq.json",
                    "feedback",
                    "v1/v2",
                    "recommendation",
                    "cloud_deployed",
                ):
                    self.assertIn(name, code)

    def test_unexpected_files_stop_both_language_writes_without_deleting_them(self):
        with workspace() as root:
            BUILDER.write(root)
            stale = root / "data/learner/ko/instructions.txt"
            stale.write_text("Preserve until both directories pass preflight.")
            unexpected = root / "data/learner/en/learner-notes.txt"
            unexpected.write_text("Synthetic test notes, not generated output.")
            with self.assertRaisesRegex(ValueError, "Unexpected files"):
                BUILDER.write(root)
            self.assertEqual(stale.read_text(), "Preserve until both directories pass preflight.")
            self.assertTrue(unexpected.is_file())
            self.assertTrue(BUILDER.check(root))

    def test_generated_directories_and_files_cannot_redirect_writes_through_symlinks(self):
        for relative in (
            "data/learner",
            "data/learner/ko",
            "data/learner/ko/policies",
            "data/learner/ko/instructions.txt",
        ):
            with self.subTest(path=relative), workspace() as root:
                target = root / "untouched"
                target.mkdir()
                sentinel = target / "sentinel.txt"
                sentinel.write_text("Keep this synthetic test sentinel.")
                link = root / relative
                link.parent.mkdir(parents=True, exist_ok=True)
                if link.exists():
                    link.rename(root / "original-generated")
                is_directory = not relative.endswith(".txt")
                link.symlink_to(
                    target if is_directory else sentinel, target_is_directory=is_directory
                )
                with self.assertRaisesRegex(ValueError, "symlink"):
                    BUILDER.write(root)
                self.assertTrue(any("symlink" in failure for failure in BUILDER.check(root)))
                self.assertEqual(sentinel.read_text(), "Keep this synthetic test sentinel.")
                self.assertEqual(list(target.iterdir()), [sentinel])
