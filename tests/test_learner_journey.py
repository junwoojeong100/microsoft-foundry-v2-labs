import re
import unittest
from itertools import pairwise

from foundry_workshop.contracts import load_documents

from . import ROOT

ROUTES = {
    "A": (0, 1, 2, 3, 5, 6, 7, 9, 11),
    "B": (0, 2, 4, 5, 6, 7, 8, 9, 11),
}


class LearnerJourneyTests(unittest.TestCase):
    def language_labs(self):
        for language, directory in (("en", ROOT / "docs"), ("ko", ROOT / "docs/ko")):
            yield (
                language,
                directory,
                {int(path.name[:2]): path for path in (directory / "labs").glob("*.md")},
            )

    def test_every_lab_has_one_start_card_completion_recovery_and_setup_link(self):
        for language, _, labs in self.language_labs():
            heading, labels = (
                ("Before you start", ("This pass", "Need", "Continue when", "If blocked"))
                if language == "en"
                else ("시작 전", ("이번 순서", "준비물", "다음으로 갈 기준", "막히면"))
            )
            self.assertEqual(set(labs), set(range(12)))
            for number, path in labs.items():
                with self.subTest(language=language, lab=number):
                    text = path.read_text()
                    self.assertEqual(len(re.findall(rf"(?m)^## {heading}$", text)), 1)
                    card = text.split(f"## {heading}\n", 1)[1].split("\n## ", 1)[0]
                    for label in labels:
                        self.assertIn(f"**{label}:**", card)
                    self.assertIn("(../setup.md)", card)

    def test_a_and_b_next_links_reach_the_capstone_without_missing_a_step(self):
        for language, _, labs in self.language_labs():
            for route, sequence in ROUTES.items():
                for current, following in pairwise(sequence):
                    with self.subTest(language=language, route=route, lab=current):
                        footer = labs[current].read_text().strip().splitlines()[-1]
                        self.assertIn(
                            f"{route} → [Lab {following:02d}]({labs[following].name})", footer
                        )
            self.assertIn(
                "(../reference/cleanup.md)", labs[11].read_text().strip().splitlines()[-1]
            )

    def test_beginner_timetable_includes_handoff_and_really_totals_four_hours(self):
        for language, directory, _ in self.language_labs():
            with self.subTest(language=language):
                section = (
                    (directory / "paths.md").read_text().split("## A.", 1)[1].split("## B.", 1)[0]
                )
                minutes = []
                for line in section.splitlines():
                    columns = [value.strip() for value in line.split("|")[1:-1]]
                    if len(columns) == 4:
                        duration = re.fullmatch(r"(\d+)\s*(?:min|분)", columns[2])
                        if duration:
                            minutes.append(int(duration[1]))
                self.assertEqual(len(minutes), 10)
                self.assertEqual(sum(minutes), 240)
                self.assertIn("(labs/11-capstone.md)", section)

    def test_browser_steps_use_ready_inputs_not_reference_answer_records(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                agent = labs[3].read_text().split("## B.", 1)[0]
                assessment = labs[7].read_text().split("## B.", 1)[0]
                self.assertIn("instructions-with-policies.txt", agent)
                self.assertIn("instructions.txt", agent)
                for document in load_documents(ROOT, language):
                    self.assertIn(document["id"], agent)
                self.assertIn("dev-questions.txt", assessment)
                self.assertIn("assessment.csv", assessment)
                self.assertNotIn("dev.jsonl", assessment)
                self.assertNotIn("holdout.jsonl", assessment)
                for number in range(1, 7):
                    self.assertIn(f"D{number:02d}", assessment)

    def test_optional_sections_and_recordings_have_balanced_details(self):
        for language, _, labs in self.language_labs():
            for number, path in labs.items():
                with self.subTest(language=language, lab=number):
                    text = re.sub(r"```.*?```", "", path.read_text(), flags=re.DOTALL)
                    depth = 0
                    for tag in re.findall(r"</?details>", text):
                        depth += 1 if tag == "<details>" else -1
                        self.assertGreaterEqual(depth, 0)
                    self.assertEqual(depth, 0)

    def test_documented_output_fields_do_not_reintroduce_invented_success_flags(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                doctor = labs[0].read_text()
                self.assertIn("deployment.state: Succeeded", doctor)
                self.assertNotIn("provisioningState: Succeeded", doctor)
                seed = labs[6].read_text()
                self.assertIn("document_count: 6", seed)
                self.assertNotIn("documents_uploaded", seed)
                self.assertNotIn("iq_created", seed)
                acceptance = labs[11].read_text()
                for field in (
                    "candidate_grade",
                    "holdout_grade",
                    "business_gate_passed",
                    "deployment_approved: false",
                ):
                    self.assertIn(field, acceptance)
                self.assertNotIn("accepted: true", acceptance)
                self.assertNotIn("human_approval", acceptance)
