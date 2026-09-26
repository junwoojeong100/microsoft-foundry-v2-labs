import argparse
import csv
import io
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from itertools import pairwise
from unittest.mock import patch

from foundry_workshop.cli import DEFAULT_QUESTION, DEFAULT_QUESTION_EN, main, parser
from foundry_workshop.contracts import load_cases, load_documents, read_json, read_jsonl
from foundry_workshop.evaluation import grade
from foundry_workshop.knowledge import local_retrieve
from foundry_workshop.profiles import RuntimeProfile

from . import ROOT, workspace
from .test_packaging import load_script

DOCS = load_script("check_docs")

ROUTES = {
    "A": (0, 1, 2, 3, 5, 6, 7, 9, 11),
    "B": (0, 2, 3, 4, 5, 6, 7, 8, 9, 11),
}
TIMETABLES = {"A": (10, 270), "B": (11, 480)}

CORE_COMMANDS = {
    0: ("doctor", "demo", "demo", "compare", "doctor"),
    2: ("doctor", "model", "answer"),
    3: ("prompt-agent", "prompt-agent"),
    4: ("maf", "maf", "maf"),
    5: ("workflow", "workflow", "workflow"),
    6: ("retrieve", "seed-search", "retrieve", "seed-search", "retrieve", "answer"),
    7: (
        "collect",
        "evaluate",
        "feedback",
        "collect",
        "evaluate",
        "compare",
        "collect",
        "evaluate",
        "accept",
    ),
    8: (),
    9: ("cleanup-plan",),
    11: ("accept",),
}


def expanded_markdown(text):
    result, depth = [], 0
    for part in re.split(r"(<details>|</details>)", text):
        if part == "<details>":
            depth += 1
        elif part == "</details>":
            depth -= 1
        elif depth == 0:
            result.append(part)
    return "".join(result)


class LearnerJourneyTests(unittest.TestCase):
    def language_labs(self):
        for language, directory in (("en", ROOT / "docs"), ("ko", ROOT / "docs/ko")):
            yield (
                language,
                directory,
                {int(path.name[:2]): path for path in (directory / "labs").glob("*.md")},
            )

    def core_section(self, language, path, route):
        visible = expanded_markdown(path.read_text())
        anchor = f'<a id="path-{route.lower()}"></a>'
        self.assertEqual(visible.count(anchor), 1, f"{path}: entry must not be collapsed")
        section = visible.split(anchor, 1)[1]
        label = "done" if language == "en" else "완료"
        checkpoint = re.search(rf"\*\*{route} {label}:\*\*.*?(?=\n\n|\Z)", section, flags=re.DOTALL)
        if checkpoint is None:
            self.fail(f"{path}: missing visible {route} exit checkpoint")
        return section[: checkpoint.end()]

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
                            f"{route} → [Lab {following:02d}]({labs[following].name}#path-{route.lower()})",
                            footer,
                        )
                        core = self.core_section(language, labs[current], route)
                        self.assertIn(f"({labs[following].name}#path-{route.lower()})", core)
            self.assertIn(
                "(../reference/cleanup.md)", labs[11].read_text().strip().splitlines()[-1]
            )

    def test_both_timetables_include_handoff_and_sum_to_the_advertised_hours(self):
        for language, directory, _ in self.language_labs():
            for route, following in (("A", "B"), ("B", "C")):
                rows, total = TIMETABLES[route]
                with self.subTest(language=language, route=route):
                    section = (
                        (directory / "paths.md")
                        .read_text()
                        .split(f"## {route}.", 1)[1]
                        .split(f"## {following}.", 1)[0]
                    )
                    minutes = []
                    for line in section.splitlines():
                        columns = [value.strip() for value in line.split("|")[1:-1]]
                        if len(columns) == 4:
                            duration = re.fullmatch(r"(\d+)\s*(?:min|분)", columns[2])
                            if duration:
                                minutes.append(int(duration[1]))
                    self.assertEqual(len(minutes), rows)
                    self.assertEqual(sum(minutes), total)
                    self.assertIn(f"(labs/11-capstone.md#path-{route.lower()})", section)

    def test_route_tables_link_to_every_exact_section_in_order(self):
        for language, directory, labs in self.language_labs():
            for route, filename in (("A", "a-beginner.md"), ("B", "b-practitioner.md")):
                with self.subTest(language=language, route=route):
                    text = (directory / "paths" / filename).read_text()
                    rows = re.findall(
                        r"^\|\s*(\d+)\s*\|[^\n]*?\]\(\.\./labs/([^)]+)\)",
                        text,
                        re.MULTILINE,
                    )
                    self.assertEqual(
                        [int(index) for index, _ in rows], list(range(1, len(ROUTES[route]) + 1))
                    )
                    self.assertEqual(
                        [target for _, target in rows],
                        [f"{labs[number].name}#path-{route.lower()}" for number in ROUTES[route]],
                    )
                    for number in ROUTES[route]:
                        self.core_section(language, labs[number], route)

    def test_offline_readers_can_skip_the_live_setup_card_and_notes_copy(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                text = expanded_markdown(labs[0].read_text())
                folder = text.split('<a id="source-folder"></a>', 1)[1]
                before_notes = folder.split('<a id="prepare-notes"></a>', 1)[0]
                self.assertIn("(#offline-fixtures)", before_notes)
                self.assertIn(
                    "Skip B's personal-notes preparation"
                    if language == "en"
                    else "B의 개인 기록 폴더 준비는 건너뜁니다",
                    before_notes,
                )
                anchor = '<a id="offline-fixtures"></a>'
                self.assertIn(anchor, text)
                rehearsal = text.split(anchor, 1)[1].split("### 3.", 1)[0]
                commands = [args for _, args in DOCS.workshop_commands(rehearsal)]
                self.assertEqual(
                    [parser().parse_args(args).command for args in commands],
                    ["demo", "demo", "compare"],
                )
                self.assertIn("not run" if language == "en" else "미실행", rehearsal)

    def test_offline_rehearsal_checks_each_expected_result_before_the_next_command(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                rehearsal = (
                    expanded_markdown(labs[0].read_text())
                    .split('<a id="offline-fixtures"></a>', 1)[1]
                    .split("### 3.", 1)[0]
                )
                blocks = list(re.finditer(r"```bash\n(.*?)```", rehearsal, re.DOTALL))
                self.assertEqual(len(blocks), 3, "Inspect each fixture before the next command")
                for index, passed in enumerate((0, 6)):
                    check = rehearsal[blocks[index].end() : blocks[index + 1].start()]
                    for field in ("total: 6", f"passed: {passed}", "errors: 0"):
                        self.assertIn(f"`{field}`", check)
                    gate = "false" if passed == 0 else "true"
                    self.assertIn(f"`business_gate_passed: {gate}`", check)
                comparison = rehearsal[blocks[-1].end() :]
                self.assertIn("outputs/rehearsal-v2/comparison-vs-rehearsal-v1.json", comparison)
                self.assertIn("OFFLINE FIXTURES ONLY", comparison)

    def test_terminal_choice_is_explained_before_the_first_download_command(self):
        for language, directory, labs in self.language_labs():
            with self.subTest(language=language):
                text = labs[0].read_text()
                anchor = '<a id="terminal-check"></a>'
                self.assertIn(anchor, text)
                check = text.split(anchor, 1)[1].split("```bash", 1)[0]
                for marker in ("WSL:", "PowerShell", "Command Prompt", "`>>>`", "`exit()`"):
                    self.assertIn(marker, check)
                recovery = (directory / "reference/troubleshooting.md").read_text()
                self.assertIn("(../labs/00-start.md#terminal-check)", recovery)

    def test_source_setup_prepares_the_editor_and_opens_the_extracted_root(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                setup = self.core_section(language, labs[0], "B")
                folder = setup.split('<a id="source-folder"></a>', 1)[1].split(
                    '<a id="terminal-check"></a>', 1
                )[0]
                anchor = '<a id="editor-and-folder"></a>'
                self.assertIn(anchor, folder)
                opening = folder.split(anchor, 1)[1]
                for marker in (
                    "Visual Studio Code",
                    "https://code.visualstudio.com/docs/getstarted/overview#_install-vs-code",
                    "**File → Open Folder...**",
                    "`README.md`",
                    "`pyproject.toml`",
                    "`scripts/`",
                ):
                    self.assertIn(marker, opening)
                self.assertIn(
                    "not the ZIP file or its parent Downloads folder"
                    if language == "en"
                    else "ZIP 파일 자체나 상위 다운로드 폴더가 아닙니다",
                    opening,
                )
                self.assertEqual(DOCS.workshop_commands(opening), [])

    def test_browser_paste_replaces_instructions_and_absent_web_search_is_ready(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                model = self.core_section(language, labs[2], "A")
                tools = model.split("### 2.", 1)[1].split("### 3.", 1)[0]
                self.assertIn("already absent" if language == "en" else "처음부터 없다면", tools)
                agent = self.core_section(language, labs[3], "A")
                paste = agent.split(
                    "#### Instructions and saving" if language == "en" else "#### 지침 입력과 저장",
                    1,
                )[1].split("### 2.", 1)[0]
                for marker in ("instructions-with-policies.txt", "Ctrl+A", "Cmd+A"):
                    self.assertIn(marker, paste)
                self.assertIn("replace" if language == "en" else "교체", paste)

    def test_optional_file_search_returns_to_the_recorded_inline_agent_before_core_checks(self):
        for language, directory, labs in self.language_labs():
            with self.subTest(language=language):
                text = labs[3].read_text()
                optional = next(
                    block
                    for block in re.findall(r"<details>.*?</details>", text, re.DOTALL)
                    if "File Search" in block
                )
                self.assertIn("(#check-inline-agent)", optional)
                core = self.core_section(language, labs[3], "A")
                anchor = '<a id="check-inline-agent"></a>'
                self.assertIn(anchor, core)
                check = core.split(anchor, 1)[1].split("\n|", 1)[0]
                for field in ("session-notes.txt", "instructions-with-policies.txt", "-files"):
                    self.assertIn(field, check)
                for marker in (
                    ("**Version**", "**Save**", "unsaved")
                    if language == "en"
                    else ("**버전**", "**저장**", "미저장")
                ):
                    self.assertIn(marker, check)
                policy_check = core.split("### 2.", 1)[1].split(anchor, 1)[0]
                self.assertIn("session-notes.txt", policy_check)
                recovery = (directory / "reference/troubleshooting.md").read_text()
                self.assertIn("(../labs/03-prompt-agent.md#check-inline-agent)", recovery)

    def test_a_assessment_preserves_saved_version_and_all_csv_cells(self):
        for language, directory, labs in self.language_labs():
            with self.subTest(language=language):
                assessment = self.core_section(language, labs[7], "A")
                for anchor in ("assessment-version", "assessment-sheet"):
                    self.assertIn(f'<a id="{anchor}"></a>', assessment)
                    recovery = (directory / "reference/troubleshooting.md").read_text()
                    self.assertIn(f"(../labs/07-evaluation.md#{anchor})", recovery)
                version = assessment.split('<a id="assessment-version"></a>', 1)[1].split(
                    '<a id="assessment-sheet"></a>', 1
                )[0]
                self.assertIn("draft" if language == "en" else "초안", version)
                self.assertIn(
                    "do not select **Save**" if language == "en" else "**저장**을 누르지", version
                )
                sheet = assessment.split('<a id="assessment-sheet"></a>', 1)[1].split("### 3.", 1)[
                    0
                ]
                with (ROOT / "data/learner" / language / "assessment.csv").open(
                    encoding="utf-8-sig", newline=""
                ) as source:
                    reader = csv.DictReader(source)
                    for column in reader.fieldnames:
                        self.assertIn(f"`{column}`", sheet)
                    self.assertEqual(
                        [row["case_id"] for row in reader],
                        [f"D{index:02d}" for index in range(1, 7)],
                    )
                for marker in ("CSV UTF-8", "D01", "D06"):
                    self.assertIn(marker, sheet)
                paste = sheet.split("### 2.", 1)[1].split("\n3. ", 1)[0]
                for marker in (
                    ("edit mode", "one cell", "Undo")
                    if language == "en"
                    else ("편집 상태", "한 셀", "실행 취소")
                ):
                    self.assertIn(marker, paste)
                self.assertIn("comma" if language == "en" else "쉼표", sheet)

    def test_a_cleanup_does_not_assume_self_study_implies_resource_ownership(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                operations = self.core_section(language, labs[9], "A")
                self.assertIn("(../setup-owner.md#self-study)", operations)
                self.assertIn(
                    "only this course's resources" if language == "en" else "이 실습의 자산만",
                    operations,
                )
                self.assertNotIn(
                    "everything in your own resource group is yours"
                    if language == "en"
                    else "본인 리소스 그룹의 모든 자산이 본인 것입니다",
                    operations,
                )

    def test_self_study_cleanup_checks_log_resources_outside_the_course_group(self):
        for language, directory, _ in self.language_labs():
            with self.subTest(language=language):
                owner = (directory / "setup-owner.md").read_text()
                study = owner.split('<a id="self-study"></a>', 1)[1].split(
                    '<a id="class-owner-checklist"></a>', 1
                )[0]
                tracing = study.split("5. **", 1)[1].split("6. **", 1)[0]
                self.assertIn("Application Insights", tracing)
                self.assertIn("Log Analytics", tracing)
                self.assertIn("operations-checklist.txt", tracing)
                self.assertIn("(reference/cleanup.md#self-study-cleanup)", study)
                cleanup = expanded_markdown((directory / "reference/cleanup.md").read_text()).split(
                    "## 1.", 1
                )[0]
                self.assertIn('<a id="self-study-cleanup"></a>', cleanup)
                for marker in (
                    ("only resources in that group", "other resource groups", "Log Analytics")
                    if language == "en"
                    else ("그 그룹 안의 리소스만", "다른 리소스 그룹", "Log Analytics")
                ):
                    self.assertIn(marker, cleanup)
                self.assertIn("operations-checklist.txt", cleanup)

    def test_self_study_location_retries_retain_every_group_for_cleanup(self):
        for language, directory, labs in self.language_labs():
            with self.subTest(language=language):
                study = (
                    (directory / "setup-owner.md")
                    .read_text()
                    .split('<a id="self-study"></a>', 1)[1]
                    .split('<a id="class-owner-checklist"></a>', 1)[0]
                )
                model = study.split("3. **", 1)[1].split("4. **", 1)[0]
                self.assertIn("setup-attempts.txt", model)
                self.assertIn("(reference/cleanup.md#self-study-cleanup)", model)
                for marker in (
                    ("subscription", "resource group", "location", "project", "error")
                    if language == "en"
                    else ("구독", "리소스 그룹", "위치", "프로젝트", "오류")
                ):
                    self.assertIn(marker, model)
                files = study.split("6. **", 1)[1].split("7. **", 1)[0]
                for section in (
                    files,
                    self.core_section(language, labs[0], "B"),
                    self.core_section(language, labs[9], "A"),
                ):
                    self.assertIn("setup-attempts.txt", section)
                    self.assertIn("operations-checklist.txt", section)
                cleanup = expanded_markdown((directory / "reference/cleanup.md").read_text()).split(
                    "## 1.", 1
                )[0]
                self.assertIn("setup-attempts.txt", cleanup)
                for marker in (
                    ("before Lab 00", "each recorded group", "earlier attempts")
                    if language == "en"
                    else ("Lab 00 전에", "기록한 각 그룹", "이전 시도")
                ):
                    self.assertIn(marker, cleanup)

    def test_cleanup_preserves_incomplete_and_rejected_handoff_outcomes(self):
        for language, directory, labs in self.language_labs():
            with self.subTest(language=language):
                cleanup = expanded_markdown((directory / "reference/cleanup.md").read_text())
                anchor = '<a id="learner-finish"></a>'
                self.assertEqual(cleanup.count(anchor), 1, "Give cleanup an explicit ending")
                ending = cleanup.split(anchor, 1)[1].split("\n## ", 1)[0]
                outcomes = ("incomplete", "rejected") if language == "en" else ("미완료", "반려")
                handoff = self.core_section(language, labs[11], "B")
                for outcome in outcomes:
                    self.assertIn(f"**{outcome}**", handoff)
                    self.assertIn(f"**{outcome}**", ending)
                self.assertIn("session-notes.txt", ending)
                self.assertIn("(../labs/11-capstone.md)", ending)
                self.assertEqual(DOCS.workshop_commands(ending), [])

    def test_each_practitioner_session_fits_four_hours_including_breaks(self):
        for language, directory, _ in self.language_labs():
            with self.subTest(language=language):
                section = (
                    (directory / "paths.md").read_text().split("## B.", 1)[1].split("## C.", 1)[0]
                )
                lab_minutes = {}
                sessions = []
                for line in section.splitlines():
                    columns = [value.strip() for value in line.split("|")[1:-1]]
                    if len(columns) == 4:
                        lab = re.search(r"labs/(\d{2})-", columns[1])
                        minutes = re.fullmatch(r"(\d+)\s*(?:min|분)", columns[2])
                        if lab and minutes:
                            lab_minutes[int(lab[1])] = int(minutes[1])
                    elif len(columns) == 5 and re.fullmatch(r"Day [12]", columns[0]):
                        sessions.append(columns)
                self.assertEqual(len(sessions), 2)
                self.assertIn('<a id="b-session-budget"></a>', section)
                ordered_labs = []
                route = (directory / "paths/b-practitioner.md").read_text()
                for day, columns in enumerate(sessions, start=1):
                    self.assertEqual(columns[0], f"Day {day}")
                    labs = [int(value) for value in re.findall(r"\b\d{2}\b", columns[1])]
                    self.assertTrue(labs)
                    ordered_labs.extend(labs)
                    durations = []
                    for value in columns[2:]:
                        match = re.fullmatch(r"(\d+)\s*(?:min|분)", value)
                        self.assertIsNotNone(match)
                        durations.append(int(match[1]))
                    core, buffer, total = durations
                    self.assertEqual(core, sum(lab_minutes[lab] for lab in labs))
                    self.assertEqual(core + buffer, total)
                    self.assertGreater(buffer, 0)
                    self.assertEqual(total, 240)
                    route_day = re.search(rf"Day {day}[^`]*`([\d, ]+)`", route)
                    self.assertIsNotNone(route_day)
                    self.assertEqual(
                        [int(value.strip()) for value in route_day[1].split(",")], labs
                    )
                self.assertEqual(tuple(ordered_labs), ROUTES["B"])
                self.assertIn("(../paths.md#b-session-budget)", route)

    def test_setup_distinguishes_search_writers_from_read_only_learners(self):
        for language, directory, _ in self.language_labs():
            with self.subTest(language=language):
                owner = (directory / "setup-owner.md").read_text()
                writer_rows = [
                    line
                    for line in owner.splitlines()
                    if line.startswith("|") and "`seed-search`" in line
                ]
                self.assertEqual(len(writer_rows), 1)
                self.assertIn("B", writer_rows[0])
                self.assertIn("Search Service Contributor", writer_rows[0])
                self.assertIn("Search Index Data Contributor", writer_rows[0])
                reader_rows = [
                    line
                    for line in owner.splitlines()
                    if line.startswith("|") and "`retrieve`" in line
                ]
                self.assertEqual(len(reader_rows), 1)
                self.assertIn("Search Index Data Reader", reader_rows[0])
                self.assertNotIn("Contributor", reader_rows[0])

    def test_owner_iq_preparation_stops_before_later_commands_when_a_step_fails(self):
        stub = """
calls=0
python() {
    calls=$((calls + 1))
    printf '%s\\n' "$*"
    if [ "$calls" -eq "$FAIL_AT" ]; then return 2; fi
    return 0
}
"""
        for language, directory, _ in self.language_labs():
            owner = (directory / "setup-owner.md").read_text()
            blocks = [
                block
                for block in re.findall(r"```bash\n(.*?)```", owner, re.DOTALL)
                if "seed-search --iq" in block and "iq-chat ask" in block
            ]
            self.assertEqual(len(blocks), 1)
            for fail_at in (1, 2, 3, 0):
                with self.subTest(language=language, fail_at=fail_at):
                    result = subprocess.run(
                        ["bash", "--noprofile", "--norc", "-c", stub + blocks[0]],
                        cwd=ROOT,
                        env={"PATH": os.defpath, "FAIL_AT": str(fail_at)},
                        capture_output=True,
                        text=True,
                        timeout=10,
                        check=False,
                    )
                    self.assertEqual(result.returncode, 2 if fail_at else 0, result.stderr)
                    self.assertEqual(len(result.stdout.splitlines()), fail_at or 4)
                    if fail_at:
                        self.assertNotIn("iq-chat ask", result.stdout)

    def test_self_study_b_has_search_service_steps_before_authentication(self):
        for language, directory, _ in self.language_labs():
            with self.subTest(language=language):
                owner = expanded_markdown((directory / "setup-owner.md").read_text())
                anchor = '<a id="search-service"></a>'
                self.assertEqual(owner.count(anchor), 1, "B needs a service preparation entry")
                study, rest = owner.split('<a id="class-owner-checklist"></a>', 1)
                self.assertIn("(#search-service)", study)
                checklist, preparation = rest.split(anchor, 1)
                self.assertIn("(#search-service)", checklist)
                preparation = preparation.split('<a id="search-authentication"></a>', 1)[0]
                for marker in (
                    "**Basic**",
                    "**Default**",
                    "https://<search>.search.windows.net",
                    "Premium features",
                    "Semantic ranker",
                    "Knowledge retrieval",
                    "**Free**",
                    "**Standard**",
                    "2026-09-26",
                    "(#search-authentication)",
                    "(labs/06-knowledge.md#path-b)",
                    "(setup.md)",
                    "https://learn.microsoft.com/azure/search/search-create-service-portal",
                    "https://learn.microsoft.com/azure/search/search-region-support",
                    "https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-enable-disable",
                ):
                    self.assertIn(marker, preparation)
                self.assertEqual(DOCS.workshop_commands(preparation), [])

    def test_search_token_authentication_is_prepared_separately_from_caller_roles(self):
        for language, directory, labs in self.language_labs():
            with self.subTest(language=language):
                owner = expanded_markdown((directory / "setup-owner.md").read_text())
                anchor = '<a id="search-authentication"></a>'
                self.assertIn(anchor, owner)
                preparation = owner.split(anchor, 1)[1]
                for marker in (
                    "Microsoft Entra",
                    "Settings",
                    "Keys",
                    "API access control",
                    "Role-based access control",
                    "Both",
                    "API Key",
                    "Search Service Contributor",
                    "Search Index Data Contributor",
                    "2026-09-26",
                    "https://learn.microsoft.com/azure/search/search-security-enable-roles",
                ):
                    self.assertIn(marker, preparation)
                self.assertIn("owner only" if language == "en" else "담당자 전용", preparation)
                self.assertIn("shared" if language == "en" else "공유", preparation)
                self.assertIn("(#search-authentication)", owner.split(anchor, 1)[0])
                setup = expanded_markdown((directory / "setup.md").read_text())
                self.assertIn("(setup-owner.md#search-authentication)", setup)
                entry = self.core_section(language, labs[6], "B").split("### 2.", 1)[0]
                self.assertIn("(../setup-owner.md#search-authentication)", entry)
                self.assertIn("API access control", entry)
                recovery = (directory / "reference/troubleshooting.md").read_text()
                search_error = next(
                    line for line in recovery.splitlines() if line.startswith("| Search 401/403")
                )
                self.assertIn("(../setup-owner.md#search-authentication)", search_error)

    def test_evidence_hub_and_coverage_include_the_headless_followup(self):
        for language, directory, _ in self.language_labs():
            with self.subTest(language=language):
                for name in ("evidence.md", "coverage.md"):
                    text = (directory / name).read_text()
                    self.assertIn("(live-run.md#headless-guide-audit-20260925)", text)
                hub = (directory / "evidence.md").read_text()
                self.assertNotIn("Current workflow and evaluation curriculum", hub)
                self.assertNotIn("five guide defects", hub)

    def test_beginner_exits_before_code_except_for_one_prepared_workflow(self):
        for language, _, labs in self.language_labs():
            for number in ROUTES["A"]:
                with self.subTest(language=language, lab=number):
                    core = self.core_section(language, labs[number], "A")
                    commands = [
                        parser().parse_args(arguments)
                        for _, arguments in DOCS.workshop_commands(core)
                    ]
                    self.assertEqual(
                        [command.command for command in commands],
                        ["workflow"] if number == 5 else [],
                    )
                    if commands:
                        self.assertEqual(commands[0].pattern, "sequential")
                    self.assertNotIn("--unlock-holdout", core)
                    self.assertNotIn("azd deploy", core)

    def test_beginner_orientation_uses_the_dev_question_and_explains_work_locations(self):
        for language, directory, _ in self.language_labs():
            with self.subTest(language=language):
                route = (directory / "paths/a-beginner.md").read_text()
                question = load_cases(ROOT, "dev", language)[0]["question"]
                self.assertIn(question, route)
                self.assertIn('<a id="first-success"></a>', route)
                self.assertIn("```mermaid\n", route)
                self.assertIn(
                    "not full A completion" if language == "en" else "A 전체 완료가 아닙니다",
                    route,
                )
                work_locations = route.split('<a id="where-to-work"></a>', 1)[1]
                for marker in (
                    "ai.azure.com",
                    "Instructions",
                    "session-notes.txt",
                    "workflow-review.txt",
                    "assessment-baseline.csv",
                ):
                    self.assertIn(marker, work_locations)
                self.assertEqual(DOCS.workshop_commands(route), [])
                for page in (
                    ROOT / ("README.md" if language == "en" else "README.ko.md"),
                    directory / "index.md",
                ):
                    self.assertIn("paths/a-beginner.md#first-success)", page.read_text())

    def test_beginner_file_preparation_checks_extraction_and_persistent_plain_text(self):
        for language, directory, labs in self.language_labs():
            with self.subTest(language=language):
                setup = (directory / "setup.md").read_text()
                extraction = setup.split('<a id="extract-learner-files"></a>', 1)[1].split(
                    '<a id="local-tools"></a>', 1
                )[0]
                for marker in ("Windows", "macOS", "START-HERE.txt", "policies/"):
                    self.assertIn(marker, extraction)
                saving = setup.split('<a id="saving-notes"></a>', 1)[1].split(
                    '<a id="environment-card"></a>', 1
                )[0]
                for marker in (
                    "session-notes.txt",
                    "Ctrl+S",
                    "Cmd+S",
                    "UTF-8",
                    "instructions-baseline.txt",
                    ".rtf",
                    ".txt.txt",
                ):
                    self.assertIn(marker, saving)
                agent = self.core_section(language, labs[3], "A")
                self.assertIn("(../setup.md#saving-notes)", agent)
                self.assertIn("policies/TRAVEL-2026.txt", agent)
                policy = (ROOT / "data/learner" / language / "policies/TRAVEL-2026.txt").read_text()
                for field in ("Document ID", "Effective"):
                    self.assertIn(field, agent)
                    self.assertIn(field, policy)

    def test_worked_assessment_marks_a_correct_amount_with_the_wrong_source_as_failure(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                core = self.core_section(language, labs[7], "A")
                example = core.split('<a id="assessment-example"></a>', 1)[1].split("![", 1)[0]
                self.assertIn(
                    "not an actual model result"
                    if language == "en"
                    else "실제 모델 결과가 아닙니다",
                    example,
                )
                values = dict(re.findall(r"^\| `(\w+)` \| (.*?) \|$", example, re.MULTILINE))
                self.assertEqual(
                    set(values),
                    {"actual_answer", "actual_document_ids", "pass_or_fail", "review_note"},
                )
                case = load_cases(ROOT, "dev", language)[0]
                self.assertEqual(case["case_id"], "D01")
                self.assertIn(str(case["expected_limit_krw"]), values["actual_answer"])
                source = values["actual_document_ids"].strip("`")
                document = next(
                    doc for doc in load_documents(ROOT, language) if doc["id"] == source
                )
                self.assertIn(f"[{source}]", values["actual_answer"])
                self.assertNotIn(source, case["required_citations"])
                self.assertEqual(values["pass_or_fail"], "`fail`")
                self.assertIn(document["effective_to"], values["review_note"])
                for citation in case["required_citations"]:
                    self.assertIn(citation, values["review_note"])
                for score in ("**4/6**", "**5/6**", "4/5"):
                    self.assertIn(score, core)

    def test_practitioner_core_keeps_its_declared_commands_and_no_optional_calls(self):
        for language, _, labs in self.language_labs():
            for number, expected in CORE_COMMANDS.items():
                with self.subTest(language=language, lab=number):
                    core = self.core_section(language, labs[number], "B")
                    commands = [
                        parser().parse_args(arguments)
                        for _, arguments in DOCS.workshop_commands(core)
                    ]
                    self.assertEqual(tuple(command.command for command in commands), expected)
                    if number == 5:
                        self.assertEqual(
                            [command.pattern for command in commands],
                            ["sequential", "concurrent", "group-chat"],
                        )
                    if number == 7:
                        collections = [
                            command for command in commands if command.command == "collect"
                        ]
                        self.assertEqual(
                            [
                                (command.split, command.prompt, command.retrieval)
                                for command in collections
                            ],
                            [
                                ("dev", "v1", "local"),
                                ("dev", "v2", "local"),
                                ("holdout", "v2", "local"),
                            ],
                        )
                        self.assertEqual(
                            collections[-1].candidate,
                            collections[1].label,
                        )
                        self.assertTrue(collections[-1].unlock_holdout)
                        self.assertEqual(
                            re.findall(r"^### (\d+)\.", core, re.MULTILINE),
                            ["1", "2", "3", "4"],
                        )
                        gate = core.index("business_gate_passed: true")
                        self.assertLess(gate, core.index("--unlock-holdout"))
                    if number == 8:
                        blocks = re.findall(r"```bash\n(.*?)```", core, re.DOTALL)
                        self.assertEqual(len(blocks), 1)
                        self.assertRegex(
                            blocks[0].strip(),
                            r"^python scripts/package_hosted\.py(?: --language (en|ko))?$",
                        )
                        self.assertIn("cloud_deployed: false", core)

    def test_readme_starts_with_setup_and_owner_commands_stay_collapsed(self):
        for language, directory, _ in self.language_labs():
            with self.subTest(language=language):
                name = "README.md" if language == "en" else "README.ko.md"
                readme = expanded_markdown((ROOT / name).read_text())
                setup_link = "docs/setup.md" if language == "en" else "docs/ko/setup.md"
                self.assertIn(f"({setup_link})", readme[:600])
                self.assertNotIn("satyanadella", readme)
                setup = expanded_markdown((directory / "setup.md").read_text())
                self.assertEqual(DOCS.workshop_commands(setup), [])
                for name in (
                    "session-notes.txt",
                    "workflow-review.txt",
                    "operations-checklist.txt",
                ):
                    self.assertIn(name, setup)

    def test_entry_points_choose_route_then_setup_then_first_lab(self):
        for language, directory, _ in self.language_labs():
            readme = ROOT / ("README.md" if language == "en" else "README.ko.md")
            for path in (readme, directory / "index.md"):
                with self.subTest(language=language, page=path):
                    opening = expanded_markdown(path.read_text())
                    steps = re.findall(
                        r"^([123])\. (.*?)(?=^\d+\. |\n\n|\Z)",
                        opening,
                        re.MULTILINE | re.DOTALL,
                    )[:3]
                    self.assertEqual([number for number, _ in steps], ["1", "2", "3"])
                    self.assertRegex(steps[0][1], r"(?:\*\*A\*\*|A\. Beginner|A\. 입문)")
                    self.assertRegex(steps[0][1], r"(?:\*\*B\*\*|B\. Implementation|B\. 구현)")
                    self.assertIn("setup.md)", steps[1][1])
                    self.assertIn("Lab 00", steps[2][1])
                    self.assertIn(
                        "A done / B done" if language == "en" else "A 완료 / B 완료", steps[2][1]
                    )

    def test_setup_provides_learner_files_before_the_environment_card(self):
        for language, directory, _ in self.language_labs():
            with self.subTest(language=language):
                text = expanded_markdown((directory / "setup.md").read_text())
                self.assertEqual(
                    re.findall(r"^## (\d+)\.", text, re.MULTILINE), ["1", "2", "3", "4"]
                )
                files = text.index('<a id="learner-files"></a>')
                card = text.index('<a id="environment-card"></a>')
                self.assertLess(files, card)
                self.assertIn("learner-materials.zip)", text[files:card])
                self.assertIn("`session-notes.txt`", text[files:card])
                self.assertIn("(labs/00-start.md#source-folder)", text[files:card])
                self.assertIn(f"`outputs/learner-notes-{language}/session-notes.txt`", text[card:])
                self.assertEqual(DOCS.workshop_commands(text), [])

    def test_a_local_editors_are_checked_during_setup_before_billable_assessment(self):
        for language, directory, labs in self.language_labs():
            with self.subTest(language=language):
                setup = expanded_markdown((directory / "setup.md").read_text())
                anchor = '<a id="local-tools"></a>'
                self.assertIn(anchor, setup)
                tools = setup.split(anchor, 1)[1].split('<a id="environment-card"></a>', 1)[0]
                for marker in (
                    "session-notes.txt",
                    "assessment.csv",
                    "LibreOffice Calc",
                    "UTF-8",
                    "D01",
                    "D06",
                    "`case_id`",
                    "`review_note`",
                    "(labs/07-evaluation.md#assessment-sheet)",
                ):
                    self.assertIn(marker, tools)
                self.assertIn("six columns" if language == "en" else "6개 열", tools)
                self.assertIn("unchanged" if language == "en" else "수정하지 않고", tools)
                readiness = setup.split("## 4.", 1)[1]
                self.assertIn("(#local-tools)", readiness)
                assessment = self.core_section(language, labs[7], "A")
                before_questions = assessment.split("### 2.", 1)[0]
                self.assertIn("(../setup.md#local-tools)", before_questions)
                with (ROOT / "data/learner" / language / "assessment.csv").open(
                    encoding="utf-8-sig", newline=""
                ) as source:
                    reader = csv.DictReader(source)
                    self.assertEqual(len(reader.fieldnames), 6)
                    self.assertEqual(reader.fieldnames[0], "case_id")
                    self.assertEqual(reader.fieldnames[-1], "review_note")
                    self.assertEqual(
                        [row["case_id"] for row in reader],
                        [f"D{index:02d}" for index in range(1, 7)],
                    )

    def test_core_model_and_hosting_steps_exclude_optional_reading_and_runtime_gates(self):
        for language, directory, labs in self.language_labs():
            with self.subTest(language=language):
                model = self.core_section(language, labs[2], "B")
                self.assertEqual(re.findall(r"^### (\d+)\.", model, re.MULTILINE), ["1", "2", "3"])
                self.assertNotIn("```python", model)
                self.assertIn("```python", labs[2].read_text())
                hosted = self.core_section(language, labs[8], "B")
                self.assertNotIn("PROJECT_ARM_ID", hosted)
                self.assertNotIn("HOSTED_DIRECTORY", hosted)
                self.assertNotIn("`maf --tools`", hosted)
                self.assertIn('<a id="hosting-gates"></a>', labs[8].read_text())
                self.assertNotIn(
                    '<a id="hosting-gates"></a>', expanded_markdown(labs[8].read_text())
                )
                self.assertNotIn(
                    "| 1 | [Deployable MAF workflow]",
                    expanded_markdown((directory / "paths.md").read_text()),
                )
                self.assertNotIn(
                    "| 1 | [배포 가능한 MAF workflow]",
                    expanded_markdown((directory / "paths.md").read_text()),
                )

    def test_evaluation_overview_links_to_steps_and_keeps_each_verdict_visible(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                core = self.core_section(language, labs[7], "B")
                anchors = ("dev-baseline", "dev-review", "dev-candidate", "final-acceptance")
                for number, anchor in enumerate(anchors, 1):
                    self.assertIn(f"](#{anchor})", core.split("### 1.", 1)[0])
                    self.assertRegex(core, rf'<a id="{anchor}"></a>\s+### {number}\.')
                blocks = re.findall(r"```bash\n(.*?)```", core, re.DOTALL)
                for block in blocks:
                    commands = [
                        parser().parse_args(arguments)
                        for _, arguments in DOCS.workshop_commands(block)
                    ]
                    self.assertEqual(
                        len(commands), 1, "Inspect each verdict before the next action."
                    )
                self.assertIn("business_gate_passed: true", core)
                self.assertNotIn("--retrieval iq", core)

    def test_instructor_rehearsal_requires_core_b_but_keeps_hosted_sdk_optional(self):
        for language, directory, _ in self.language_labs():
            with self.subTest(language=language):
                text = (directory / "instructor.md").read_text()
                visible = expanded_markdown(text)
                self.assertIn('".[cloud,agents,dev]"', visible)
                self.assertNotIn('".[cloud,agents,hosted,dev]"', visible)
                self.assertNotIn("python scripts/check_sdk.py", visible)
                self.assertIn("python scripts/check_sdk.py", text)
                commands = [
                    parser().parse_args(arguments)
                    for _, arguments in DOCS.workshop_commands(visible)
                ]
                self.assertEqual(
                    [command.command for command in commands],
                    ["doctor", "doctor", "model", "answer", "workflow"],
                )
                route = visible.split('<a id="rehearse-route"></a>', 1)[1]
                required = next(
                    line for line in route.splitlines() if "(paths/b-practitioner.md)" in line
                )
                self.assertIn("Search", required)
                self.assertIn("GA IQ", required)
                self.assertIn("MCP", required)
                self.assertIn("python scripts/verify_workshop.py --label instructor-check", visible)
                self.assertIn("outputs/verification/instructor-check/report.json", visible)

    def test_command_lookup_keeps_no_evidence_diagnostic_out_of_the_core(self):
        for language, directory, _ in self.language_labs():
            with self.subTest(language=language):
                text = (directory / "reference/commands.md").read_text()
                self.assertNotIn("`collect --retrieval none`", expanded_markdown(text))
                self.assertIn("`collect --retrieval none`", text)
                self.assertIn("(../labs/07-evaluation.md#diagnostic-no-evidence)", text)
                self.assertIn(
                    "`collect --split dev --label baseline --prompt v1 --retrieval local`",
                    expanded_markdown(text),
                )

    def test_setup_and_core_lookup_distinguish_required_sdk_agent_from_browser_agent(self):
        for language, directory, labs in self.language_labs():
            with self.subTest(language=language):
                setup = self.core_section(language, labs[0], "B")
                notes = setup.split('<a id="prepare-notes"></a>', 1)[1].split("```bash", 1)[0]
                for route in ("a", "b"):
                    self.assertTrue(
                        f"(03-prompt-agent.md#path-{route})" in notes,
                        "Notes setup must distinguish the browser agent from the core SDK agent.",
                    )
                lookup = expanded_markdown((directory / "reference/commands.md").read_text())
                core = lookup.split('<a id="saving-json"></a>', 1)[0]
                for operation in ("create", "invoke"):
                    self.assertTrue(
                        f"`prompt-agent {operation} " in core,
                        f"Managed-agent {operation} belongs in the core lookup, not optional work.",
                    )

    def test_existing_sign_in_is_reused_and_optional_login_rejects_an_empty_tenant(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                text = labs[0].read_text()
                visible_blocks = re.findall(
                    r"```bash\n(.*?)```", expanded_markdown(text), re.DOTALL
                )
                self.assertFalse(
                    any(re.search(r"(?m)^\s*az login\b", block) for block in visible_blocks),
                    "An already authenticated learner must not be sent through another login.",
                )
                self.assertIn('<a id="azure-sign-in"></a>', text)
                login_blocks = [
                    block
                    for block in re.findall(r"```bash\n(.*?)```", text, re.DOTALL)
                    if re.search(r"(?m)^\s*az login\b", block)
                ]
                self.assertEqual(len(login_blocks), 1)
                for shell in ("bash", "zsh"):
                    if not shutil.which(shell):
                        continue
                    for tenant in ("", "00000000-0000-0000-0000-000000000001"):
                        with self.subTest(shell=shell, tenant=tenant):
                            result = subprocess.run(
                                [
                                    shell,
                                    "-c",
                                    'az() { printf "STUB_AZ %s\\n" "$*"; }\n' + login_blocks[0],
                                ],
                                input=tenant + "\n",
                                env={**os.environ, "AZURE_TENANT_ID": ""},
                                capture_output=True,
                                text=True,
                                timeout=10,
                                check=False,
                            )
                            if tenant:
                                self.assertEqual(result.returncode, 0, result.stderr)
                                self.assertIn(f"STUB_AZ login --tenant {tenant}", result.stdout)
                            else:
                                self.assertNotEqual(result.returncode, 0)
                                self.assertNotIn("STUB_AZ", result.stdout)

    def test_documented_env_preparation_preserves_existing_files_and_symlinks(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language), workspace() as root:
                blocks = [
                    block
                    for block in re.findall(r"```bash\n(.*?)```", labs[0].read_text(), re.DOTALL)
                    if "cp .env.example .env" in block
                ]
                self.assertEqual(len(blocks), 1)
                self.assertNotIn("az login", blocks[0])
                template = "WORKSHOP_PREFIX=mfv2-template\n"
                (root / ".env.example").write_text(template)
                for state in ("missing", "existing", "symlink"):
                    with self.subTest(state=state):
                        if state == "existing":
                            (root / ".env").write_text("WORKSHOP_PREFIX=mfv2-preserved\n")
                        elif state == "symlink":
                            (root / ".env").unlink()
                            (root / ".env").symlink_to("absent-personal-config")
                        result = subprocess.run(
                            ["bash", "-c", blocks[0]],
                            cwd=root,
                            capture_output=True,
                            text=True,
                            timeout=10,
                            check=False,
                        )
                        self.assertEqual(result.returncode, 0, result.stderr)
                        if state == "symlink":
                            self.assertTrue((root / ".env").is_symlink())
                            self.assertFalse((root / "absent-personal-config").exists())
                        else:
                            self.assertEqual(
                                (root / ".env").read_text(),
                                template
                                if state == "missing"
                                else "WORKSHOP_PREFIX=mfv2-preserved\n",
                            )

    def test_core_preflights_require_the_exact_preset_not_only_succeeded(self):
        for language, _, labs in self.language_labs():
            for number, step in ((0, 5), (2, 1)):
                with self.subTest(language=language, lab=number):
                    section = self.core_section(language, labs[number], "B")
                    section = section.split(f"### {step}.", 1)[1]
                    verification = section.split("```", 2)[2].split("![", 1)[0]
                    for value in ("`gpt-6-sol`", "`2026-09-22`", "`Succeeded`"):
                        self.assertTrue(
                            value in verification,
                            f"Preflight must require the exact preset before inference: {value}",
                        )

    def test_portal_recovery_distinguishes_tenant_identity_and_loaded_agent_content(self):
        for language, directory, labs in self.language_labs():
            with self.subTest(language=language):
                start = self.core_section(language, labs[0], "A")
                self.assertIn("(../reference/troubleshooting.md#portal-tenant)", start)
                recovery = (directory / "reference/troubleshooting.md").read_text()
                section = recovery.split('<a id="portal-tenant"></a>', 1)[1]
                section = section.split('<a id="maf-request-failure"></a>', 1)[0]
                for marker in ("`tid=`", "Loading...", "Azure CLI"):
                    self.assertTrue(marker in section, f"Missing portal recovery check: {marker}")

    def test_maf_failure_recovery_is_linked_and_covers_each_framework_entry_point(self):
        for language, directory, labs in self.language_labs():
            with self.subTest(language=language):
                start = labs[5].read_text().split('<a id="path-a"></a>', 1)[0]
                self.assertIn("(../reference/troubleshooting.md#maf-request-failure)", start)
                recovery = (directory / "reference/troubleshooting.md").read_text()
                section = recovery.split('<a id="maf-request-failure"></a>', 1)[1]
                for command in ("maf", "workflow", "workflow-agent", "maf-evaluate", "serve"):
                    self.assertIn(f"`{command}`", section)
                for marker in ("MAF request failed", "TimeoutExpired", "doctor --cloud", "`2`"):
                    self.assertIn(marker, section)
                lookup = (directory / "reference/commands.md").read_text()
                self.assertIn("MAF request failed", lookup)

    def test_prepared_source_folder_is_kept_before_offering_a_download(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                core = self.core_section(language, labs[0], "B")
                anchor = '<a id="source-folder"></a>'
                self.assertIn(anchor, core)
                choice = core.split(anchor, 1)[1].split("```bash", 1)[0]
                prepared, fresh = (
                    ("Already have a prepared source folder?", "No source folder yet?")
                    if language == "en"
                    else ("준비된 소스 폴더가 있나요?", "아직 소스 폴더가 없나요?")
                )
                self.assertLess(choice.index(prepared), choice.index(fresh))
                reuse = choice.split(fresh, 1)[0]
                for name in (".env", ".venv", "outputs/", "outputs/azure-objects.json"):
                    self.assertIn(f"`{name}`", reuse)
                self.assertNotIn("Download ZIP", reuse)

    def test_sparse_clone_enters_only_the_new_copy_and_stops_after_failure(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                blocks = [
                    block
                    for block in re.findall(r"```bash\n(.*?)```", labs[0].read_text(), re.DOTALL)
                    if "git clone" in block
                ]
                self.assertEqual(len(blocks), 1)
                block = blocks[0]
                self.assertEqual(
                    shlex.split(block),
                    [
                        "git",
                        "clone",
                        "--depth",
                        "1",
                        "--filter=blob:none",
                        "--sparse",
                        "https://github.com/junwoojeong100/microsoft-foundry-v2-labs.git",
                        "microsoft-foundry-v2-labs",
                        "&&",
                        "cd",
                        "microsoft-foundry-v2-labs",
                        "&&",
                        "git",
                        "sparse-checkout",
                        "set",
                        "--no-cone",
                        "/*",
                        "!docs/assets/",
                        "!videos/",
                    ],
                )
                for state in ("new", "clone-failed", "existing"):
                    with self.subTest(state=state), workspace() as root:
                        target = root / "microsoft-foundry-v2-labs"
                        if state == "existing":
                            target.mkdir()
                        result = subprocess.run(
                            [
                                "bash",
                                "-c",
                                "git() {\n"
                                '  if [ "$1" = clone ]; then\n'
                                '    [ "$CLONE_STATUS" = 0 ] || return "$CLONE_STATUS"\n'
                                "    mkdir microsoft-foundry-v2-labs\n"
                                "  else\n"
                                '    printf "SPARSE_CWD=%s\\n" "$PWD"\n'
                                "  fi\n"
                                "}\n" + block,
                            ],
                            cwd=root,
                            env={
                                "PATH": os.defpath,
                                "CLONE_STATUS": "19" if state == "clone-failed" else "0",
                            },
                            capture_output=True,
                            text=True,
                            timeout=10,
                            check=False,
                        )
                        if state == "new":
                            self.assertEqual(result.returncode, 0, result.stderr)
                            self.assertEqual(
                                result.stdout.strip(), f"SPARSE_CWD={target.resolve()}"
                            )
                        else:
                            self.assertNotEqual(result.returncode, 0)
                            self.assertNotIn("SPARSE_CWD", result.stdout)

    def test_sdk_install_stops_before_pip_when_venv_or_activation_fails(self):
        for language, _, labs in self.language_labs():
            core = self.core_section(language, labs[0], "B")
            block = next(
                block
                for block in re.findall(r"```bash\n(.*?)```", core, re.DOTALL)
                if "python3.13 -m venv .venv" in block
            )
            for venv_status, activation_status in ((19, None), (0, 23), (0, 0)):
                with (
                    self.subTest(language=language, venv=venv_status, activation=activation_status),
                    workspace() as root,
                ):
                    if activation_status is not None:
                        activation = root / ".venv/bin/activate"
                        activation.parent.mkdir(parents=True)
                        activation.write_text(f"return {activation_status}\n")
                    result = subprocess.run(
                        [
                            "bash",
                            "-c",
                            'python3.13() { return "$VENV_STATUS"; }\n'
                            'python() { printf "PIP_RAN\\n"; }\n' + block,
                        ],
                        cwd=root,
                        env={"PATH": os.defpath, "VENV_STATUS": str(venv_status)},
                        capture_output=True,
                        text=True,
                        timeout=10,
                        check=False,
                    )
                    expected = venv_status or activation_status
                    self.assertEqual(result.returncode, expected, result.stderr)
                    self.assertEqual("PIP_RAN" in result.stdout, expected == 0)

    def test_prompt_agent_invoke_restores_saved_name_and_version_in_a_new_terminal(self):
        for language, directory, labs in self.language_labs():
            core = self.core_section(language, labs[3], "B")
            block = next(
                block
                for block in re.findall(r"```bash\n(.*?)```", core, re.DOTALL)
                if "prompt-agent invoke" in block
            )
            for name, version in (
                ("mfv2-resumed-policy-sdk", "7"),
                ("", "7"),
                ("mfv2-resumed-policy-sdk", ""),
            ):
                with (
                    self.subTest(language=language, name=name, version=version),
                    workspace() as root,
                ):
                    result = subprocess.run(
                        ["bash", "-c", 'python() { printf "STUB_ARG=%s\\n" "$@"; }\n' + block],
                        cwd=root,
                        env={
                            "PATH": os.defpath,
                            "AGENT_NAME": "mfv2-stale-policy-sdk",
                            "AGENT_VERSION": "99",
                        },
                        input=f"{name}\n{version}\n",
                        capture_output=True,
                        text=True,
                        timeout=10,
                        check=False,
                    )
                    arguments = re.findall(r"STUB_ARG=(.*)", result.stdout)
                    if name and version:
                        self.assertEqual(result.returncode, 0, result.stderr)
                        parsed = parser().parse_args(arguments[1:])
                        self.assertEqual(parsed.name, name)
                        self.assertEqual(parsed.version, version)
                        self.assertEqual(parsed.action, "invoke")
                    else:
                        self.assertNotEqual(result.returncode, 0)
                        self.assertEqual(arguments, [])
            with self.subTest(language=language, guide="resume"):
                self.assertIn('<a id="resume-managed-agent"></a>', core)
                resume = core.split('<a id="resume-managed-agent"></a>', 1)[1].split("### 1.", 1)[0]
                for filename in ("prompt-agent-create.json", "prompt-agent-invoke.json"):
                    self.assertIn(f"`{filename}`", resume)
                recovery = (directory / "reference/troubleshooting.md").read_text()
                self.assertIn("(../labs/03-prompt-agent.md#resume-managed-agent)", recovery)

    def test_self_study_finishes_terminal_preparation_before_marking_a_ready(self):
        for language, directory, _ in self.language_labs():
            with self.subTest(language=language):
                owner = (directory / "setup-owner.md").read_text()
                section = owner.split('<a id="self-study"></a>', 1)[1].split(
                    '<a id="class-owner-checklist"></a>', 1
                )[0]
                label = "**Ready:**" if language == "en" else "**준비 완료:**"
                ready = section.split(label, 1)[1].split("\n\n", 1)[0]
                self.assertIn("**1–7**", ready)
                anchor = "5-ready-to-start" if language == "en" else "5-시작-가능-여부"
                self.assertIn(f"(setup.md#{anchor})", ready)
                deferred = "when you reach Lab 05" if language == "en" else "Lab 05에 도착했을 때"
                self.assertNotIn(deferred, section)

    def test_four_object_sketch_keeps_deployments_at_account_scope(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                core = self.core_section(language, labs[1], "A")
                self.assertIn('F --> D["', core)
                self.assertIn('F --> P["', core)
                call_label = "Calls" if language == "en" else "호출"
                self.assertIn(f'A -. "{call_label}" .-> D', core)
                self.assertNotIn("D --> A", core)
                self.assertNotRegex(core, r"→ (?:deployment|배포) gpt-6-sol →")
                relation = (
                    "agent → calls → deployment" if language == "en" else "에이전트 → 호출 → 배포"
                )
                self.assertIn(relation, core)

    def test_a_terminal_preparation_distinguishes_before_class_from_mid_route_resume(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                setup = self.core_section(language, labs[0], "B")
                self.assertIn("(02-models.md#a-terminal-ready)", setup)
                model = self.core_section(language, labs[2], "B")
                anchor = '<a id="a-terminal-ready"></a>'
                self.assertIn(anchor, model)
                return_choices = model.split(anchor, 1)[1]
                self.assertIn("(00-start.md#path-a)", return_choices)
                self.assertIn("(05-workflows.md#path-a)", return_choices)
                self.assertIn("(03-prompt-agent.md#path-b)", return_choices)
                ready = "5-ready-to-start" if language == "en" else "5-시작-가능-여부"
                field = (
                    "Prepared MAF terminal location:"
                    if language == "en"
                    else "준비된 MAF 터미널 위치:"
                )
                self.assertIn(f"`{field}`", return_choices)
                self.assertLess(
                    return_choices.index(f"(../setup.md#{ready})"),
                    return_choices.index("(00-start.md#path-a)"),
                )
                self.assertEqual(DOCS.workshop_commands(return_choices), [])

    def test_self_study_preparation_is_reachable_and_checks_every_step(self):
        for language, directory, labs in self.language_labs():
            with self.subTest(language=language):
                owner = (directory / "setup-owner.md").read_text()
                anchor = '<a id="self-study"></a>'
                self.assertEqual(owner.count(anchor), 1)
                section = owner.split(anchor, 1)[1]
                section = section.split('<a id="class-owner-checklist"></a>', 1)[0]
                self.assertEqual(
                    re.findall(r"^(\d)\. \*\*", section, re.MULTILINE),
                    [str(number) for number in range(1, 8)],
                )
                check = "**Check:**" if language == "en" else "**확인:**"
                self.assertEqual(section.count(check), 7)
                for required in (
                    "`gpt-6-sol`",
                    "`2026-09-22`",
                    "**Foundry User**",
                    "(setup.md#learner-files)",
                    "(labs/02-models.md#a-terminal-ready)",
                    "(labs/00-start.md#path-a)",
                    "(reference/cleanup.md#self-study-cleanup)",
                ):
                    self.assertIn(required, section)
                self.assertEqual(DOCS.workshop_commands(section), [])
                readme = ROOT / ("README.md" if language == "en" else "README.ko.md")
                prefix = "docs/" if language == "en" else "docs/ko/"
                self.assertIn(f"({prefix}setup-owner.md#self-study)", readme.read_text())
                for name in ("index.md", "setup.md", "paths.md"):
                    self.assertIn("(setup-owner.md#self-study)", (directory / name).read_text())
                for name in ("paths/a-beginner.md", "reference/cleanup.md"):
                    self.assertIn("(../setup-owner.md#self-study)", (directory / name).read_text())
                start = self.core_section(language, labs[0], "A")
                self.assertIn("(../setup-owner.md#self-study)", start)

    def test_retrieval_comparison_keeps_one_question_with_retrievable_policy_evidence(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                core = self.core_section(language, labs[6], "B")
                commands = [
                    parser().parse_args(arguments) for _, arguments in DOCS.workshop_commands(core)
                ]
                queries = [
                    command for command in commands if command.command in {"retrieve", "answer"}
                ]
                self.assertEqual(len(queries), 4)
                self.assertEqual(
                    [command.provider for command in queries if command.command == "retrieve"],
                    ["local", "search", "iq"],
                )
                self.assertEqual(queries[-1].retrieval, "iq")
                question = queries[0].question
                self.assertTrue(question)
                self.assertEqual([command.question for command in queries], [question] * 4)
                retrieved = local_retrieve(ROOT, question, language=language)
                self.assertEqual(retrieved["provider"], "local-keyword")
                self.assertTrue({"TRAVEL-2026", "APPROVAL-01"}.issubset(retrieved["source_ids"]))
                self.assertIn('<a id="retrieval-comparison"></a>', core)
                self.assertIn("context_hash", core)
                notes = (ROOT / "data/learner" / language / "session-notes.txt").read_text()
                for field in ("provider", "source_ids", "context_hash"):
                    self.assertIn(field, notes)

    def test_portal_evaluation_uses_the_recorded_baseline_not_a_fixed_version(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                text = labs[7].read_text()
                anchor = '<a id="portal-evaluation"></a>'
                self.assertIn(anchor, text)
                optional = text.split(anchor, 1)[1].split('<a id="path-b"></a>', 1)[0]
                target = re.search(
                    r"^2\. \*\*(?:Target|대상):\*\*.*?(?=^3\.)",
                    optional,
                    flags=re.MULTILINE | re.DOTALL,
                )
                if target is None:
                    self.fail("The optional portal evaluation needs an explicit target step.")
                self.assertIn("session-notes.txt", target[0])
                self.assertNotRegex(target[0], r"`[^`\n]+:v\d+`")

    def test_evaluation_resume_table_precedes_collection_and_is_linked_from_the_route(self):
        for language, directory, labs in self.language_labs():
            with self.subTest(language=language):
                core = self.core_section(language, labs[7], "B")
                anchor = '<a id="resume-evaluation"></a>'
                self.assertIn(anchor, core)
                self.assertLess(core.index(anchor), core.index("### 1."))
                resume = core.split(anchor, 1)[1].split("### 1.", 1)[0]
                for label in ("baseline", "candidate", "final-holdout"):
                    self.assertIn(f"`outputs/{label}/`", resume)
                self.assertEqual(DOCS.workshop_commands(resume), [])
                self.assertIn("(11-capstone.md#incomplete-handoff)", resume)
                for name in ("paths/b-practitioner.md", "reference/troubleshooting.md"):
                    text = (directory / name).read_text()
                    self.assertIn("(../labs/07-evaluation.md#resume-evaluation)", text)

    def worksheet_lines(self, language):
        return {
            name: [
                line
                for line in (ROOT / "data/learner" / language / name).read_text().splitlines()
                if line.endswith(":")
            ]
            for name in ("session-notes.txt", "workflow-review.txt", "operations-checklist.txt")
        }

    def test_core_steps_cite_only_existing_worksheet_lines(self):
        console_labels = {"Saved JSON:", "Command stderr:"}
        for language, _, labs in self.language_labs():
            lines = {line for values in self.worksheet_lines(language).values() for line in values}
            for route, sequence in ROUTES.items():
                for number in sequence:
                    with self.subTest(language=language, route=route, lab=number):
                        core = self.core_section(language, labs[number], route)
                        for cited in re.findall(r"`([^`\n]*:)`", core):
                            self.assertIn(cited, lines | console_labels)

    def test_b_review_fields_are_named_in_the_matching_lab_before_its_exit(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                fields = self.worksheet_lines(language)["session-notes.txt"]
                for number, count in ((2, 1), (3, 1), (4, 1), (5, 1), (6, 2), (7, 4), (8, 1)):
                    with self.subTest(lab=number):
                        matching = [
                            line for line in fields if line.startswith(f"Lab {number:02d} ")
                        ]
                        self.assertEqual(len(matching), count)
                        core = self.core_section(language, labs[number], "B")
                        for field in matching:
                            self.assertTrue(
                                f"`{field}`" in core, f"Missing review checkpoint: {field}"
                            )
                handoff = self.core_section(language, labs[11], "B")
                heading = (
                    "B - code evidence and handoff" if language == "en" else "B - 코드 근거와 인계"
                )
                self.assertTrue(f"**{heading}**" in handoff, f"Missing handoff section: {heading}")

    def test_cleanup_guidance_explains_missing_and_recorded_local_ownership(self):
        for language, directory, labs in self.language_labs():
            texts = (
                self.core_section(language, labs[9], "B"),
                expanded_markdown((directory / "reference/cleanup.md").read_text()),
            )
            for text in texts:
                with self.subTest(language=language, text=text[:60]):
                    for field in (
                        "search_ownership: null",
                        "search_ownership.objects",
                        "required_manual_inventory",
                        "outputs/azure-objects.json",
                    ):
                        self.assertTrue(
                            f"`{field}`" in text, f"Missing cleanup explanation: {field}"
                        )

    def test_lab00_setup_table_mirrors_the_worksheet_setup_card(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                notes = (ROOT / "data/learner" / language / "session-notes.txt").read_text()
                card = notes.split("\nLab 00 -", 1)[1].split("\n\n", 1)[0].splitlines()[1:]
                core = self.core_section(language, labs[0], "A")
                rows = re.findall(r"^\| `([^`]+:)` \|", core, re.MULTILINE)
                self.assertEqual(rows, card)

    def test_lab01_numbers_only_the_learner_steps(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                text = labs[1].read_text()
                core = self.core_section(language, labs[1], "A")
                self.assertEqual(re.findall(r"^## (\d+)\.", core, re.MULTILINE), ["1", "2", "3"])
                self.assertEqual(re.findall(r"^## (\d+)\.", text, re.MULTILINE), ["1", "2", "3"])

    def test_workflow_checks_match_the_builders_output_shapes(self):
        orchestration = (ROOT / "src/foundry_workshop/agents.py").read_text()
        orchestration = orchestration.split("def build_orchestration", 1)[1]
        self.assertIn("SequentialBuilder(participants=participants).build()", orchestration)
        self.assertEqual(orchestration.count("output_from=participants"), 2)
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                self.assertIn("`EvidenceReviewer`", self.core_section(language, labs[5], "A"))
                core = self.core_section(language, labs[5], "B")
                question = DEFAULT_QUESTION_EN if language == "en" else DEFAULT_QUESTION
                self.assertIn(f"> {question}", core.split("```bash", 1)[0])
                steps = core.split("### 1.", 1)[1]
                sequential, rest = steps.split("### 2.", 1)
                concurrent, group_chat = rest.split("### 3.", 1)
                self.assertIn("`EvidenceReviewer`", sequential.split("```", 2)[2])
                self.assertIn("aggregator", concurrent.split("```", 2)[2])
                self.assertIn("max_rounds=3", group_chat.split("```", 2)[2])

    def test_a_workflow_options_share_a_question_but_keep_distinct_output_contracts(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                text = labs[5].read_text()
                core = self.core_section(language, labs[5], "A")
                self.assertEqual(
                    re.findall(r"^### (\d+)\.", core, re.MULTILINE), ["1", "2", "3", "4"]
                )
                command = parser().parse_args(DOCS.workshop_commands(core)[0][1])
                choice, remainder = core.split("### 2.", 1)
                self.assertIn(f"> {command.question}", choice)
                self.assertIn("(#workflow-a-run)", choice)
                self.assertIn('<a id="workflow-a-run"></a>', choice)
                browser = next(
                    block
                    for block in re.findall(r"<details>.*?</details>", text, re.DOTALL)
                    if "(#workflow-a-review)" in block
                )
                self.assertLess(text.index(browser), text.index("### 2."))
                self.assertIn("Responses", browser)
                self.assertIn("Invocations", browser)
                self.assertNotIn("Invocations", choice)
                self.assertEqual(DOCS.workshop_commands(browser), [])
                self.assertIn('<a id="workflow-a-review"></a>', remainder)
                terminal_label = "Terminal" if language == "en" else "터미널"
                rows = {
                    parts[1].strip(): line
                    for line in core.splitlines()
                    if len(parts := line.split("|")) == 5
                }
                self.assertIn(terminal_label, rows)
                self.assertIn("Playground", rows)
                self.assertIn("`pattern: sequential`", rows[terminal_label])
                self.assertIn("`outputs`", rows[terminal_label])
                for field in (
                    "runtime_profile.kind: workflow",
                    "runtime_profile.pattern: sequential",
                    "answer",
                ):
                    self.assertIn(f"`{field}`", rows["Playground"])
                self.assertNotIn("`outputs`", rows["Playground"])

    def test_b_trace_resume_checks_the_request_time_range_before_declaring_it_missing(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                core = self.core_section(language, labs[9], "B")
                lookup = core.split("### 2.", 1)[1].split("### 3.", 1)[0]
                for field in ("**Last Day**", "**7D**", "prompt-agent-invoke.json", "response_id"):
                    self.assertTrue(field in lookup, f"Trace lookup must retain {field}.")
                marker = "trace unverified" if language == "en" else "추적 미확인"
                self.assertLess(lookup.index("**7D**"), lookup.index(marker))

    def test_failed_case_comes_from_the_business_evaluation_before_feedback(self):
        failed = grade({"status": "error"}, {"case_id": "D01"})
        self.assertEqual(set(failed), {"case_id", "passed", "checks"})
        self.assertIs(failed["passed"], False)
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                core = self.core_section(language, labs[7], "B")
                review = core.split('<a id="dev-review"></a>', 1)[1].split("```bash", 1)[0]
                self.assertIn("`outputs/baseline/business-evaluation.json`", review)
                self.assertIn("`passed`", review)
                self.assertLess(
                    review.index("business-evaluation.json"), review.index("responses.jsonl")
                )

    def test_iq_seed_capture_and_check_precede_the_iq_query(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                step = self.core_section(language, labs[6], "B").split("### 4.", 1)[1]
                step = step.split("### 5.", 1)[0]
                seed = re.search(r"[EK]06-004-seed-iq-2\.webp", step).start()
                query = step.index("--provider iq")
                self.assertLess(step.index("seed-search --iq"), seed)
                self.assertLess(seed, query)
                self.assertLess(query, re.search(r"[EK]06-005-iq-2\.webp", step).start())

    def test_route_names_match_across_entry_pages_schedules_and_handoff(self):
        names = {"en": ("A. Beginner", "B. Implementation"), "ko": ("A. 입문", "B. 구현")}
        for language, directory, labs in self.language_labs():
            with self.subTest(language=language):
                beginner, implementation = names[language]
                schedule = (directory / "paths.md").read_text()
                self.assertRegex(schedule, rf"(?m)^## {re.escape(beginner)}\b")
                self.assertRegex(schedule, rf"(?m)^## {re.escape(implementation)}\b")
                for route, name in (("a-beginner", beginner), ("b-practitioner", implementation)):
                    title = (directory / "paths" / f"{route}.md").read_text().splitlines()[0]
                    self.assertTrue(title.startswith(f"# {name}:"), title)
                self.assertIn(f"| {beginner} | {implementation} |", labs[11].read_text())
                instructor = (directory / "instructor.md").read_text()
                for name in (beginner, implementation):
                    self.assertIn(f"\n| {name} |", instructor)

    def test_editorial_rubric_is_consistent_without_forcing_a_particular_score(self):
        for language, directory, _ in self.language_labs():
            with self.subTest(language=language):
                text = (directory / "reference/validation-history.md").read_text()
                anchor = '<a id="guide-straightforwardness"></a>'
                self.assertIn(anchor, text)
                section = text.split(anchor, 1)[1].partition("\n## ")[2].split("\n## ", 1)[0]
                rows = re.findall(r"^\| (\d{2}) \|[^\n]+\| (\d+) \|$", section, re.MULTILINE)
                self.assertEqual([int(number) for number, _ in rows], list(range(1, 21)))
                awarded = [int(points) for _, points in rows]
                self.assertTrue(all(0 <= points <= 5 for points in awarded))
                self.assertEqual(awarded[-1], 0)
                claimed = re.search(r"\b(\d{1,3})/100\b", section)
                if claimed is None:
                    self.fail(
                        "The editorial table needs an explicit, arithmetically consistent total."
                    )
                self.assertEqual(int(claimed[1]), sum(awarded))

    def test_straightforwardness_review_v2_totals_match_its_dimension_rows(self):
        for language, directory, _ in self.language_labs():
            with self.subTest(language=language):
                text = (directory / "reference/validation-history.md").read_text()
                anchor = '<a id="guide-straightforwardness-v2"></a>'
                self.assertIn(anchor, text)
                section = text.split(anchor, 1)[1].partition("\n## ")[2].split("\n## ", 1)[0]
                rows = re.findall(
                    r"^\| D(\d{1,2}) \|[^\n]+\| (\d{1,2}(?:\.5)?) \| (\d{1,2}(?:\.5)?) \|$",
                    section,
                    re.MULTILINE,
                )
                self.assertEqual([int(number) for number, _, _ in rows], list(range(1, 11)))
                first = [float(row[1]) for row in rows]
                final = [float(row[2]) for row in rows]
                self.assertTrue(all(0 <= score <= 10 for score in first + final))
                claimed = re.findall(r"\b(\d{1,3}(?:\.5)?)/100\b", section)
                self.assertGreaterEqual(len(claimed), 2)
                self.assertEqual(float(claimed[0]), sum(final))
                self.assertEqual(float(claimed[1]), sum(first))

    def test_straightforwardness_review_v3_totals_match_both_tables(self):
        for language, directory, _ in self.language_labs():
            with self.subTest(language=language):
                text = (directory / "reference/validation-history.md").read_text()
                anchor = '<a id="straightforwardness-v3"></a>'
                self.assertIn(anchor, text)
                section = text.split(anchor, 1)[1].partition("\n## ")[2].split("\n## ", 1)[0]
                scores = {}
                for prefix in ("D", "R"):
                    rows = re.findall(
                        rf"^\| {prefix}(\d{{1,2}}) \|[^\n]+\| (\d{{1,2}}(?:\.5)?) \| (\d{{1,2}}(?:\.5)?) \|$",
                        section,
                        re.MULTILINE,
                    )
                    self.assertEqual([int(row[0]) for row in rows], list(range(1, 11)), prefix)
                    first = [float(row[1]) for row in rows]
                    final = [float(row[2]) for row in rows]
                    self.assertTrue(all(0 <= score <= 10 for score in first + final))
                    scores[prefix] = (sum(first), sum(final))
                claimed = [
                    float(value) for value in re.findall(r"\b(\d{1,3}(?:\.5)?)/100\b", section)
                ]
                self.assertGreaterEqual(len(claimed), 4)
                self.assertEqual(
                    claimed[:4], [scores["D"][1], scores["R"][1], scores["D"][0], scores["R"][0]]
                )

    def test_latest_straightforwardness_review_totals_match_every_round(self):
        for language, directory, _ in self.language_labs():
            with self.subTest(language=language):
                text = (directory / "reference/validation.md").read_text()
                anchor = '<a id="straightforwardness-95"></a>'
                self.assertIn(anchor, text)
                if "<details>" in text:
                    self.assertLess(text.index(anchor), text.index("<details>"))
                section = text.split(anchor, 1)[1].partition("\n## ")[2].split("\n## ", 1)[0]
                totals = {}
                for prefix in ("D", "R"):
                    rows = re.findall(
                        rf"^\| {prefix}(\d{{1,2}}) \| [^|\n]+ \|((?: \d{{1,2}}(?:\.5)? \|)+)$",
                        section,
                        re.MULTILINE,
                    )
                    self.assertEqual([int(row[0]) for row in rows], list(range(1, 11)), prefix)
                    columns = [[float(value) for value in row[1].split("|")[:-1]] for row in rows]
                    self.assertTrue(all(len(scores) == len(columns[0]) >= 2 for scores in columns))
                    self.assertTrue(all(0 <= score <= 10 for scores in columns for score in scores))
                    totals[prefix] = [
                        sum(scores[index] for scores in columns) for index in range(len(columns[0]))
                    ]
                self.assertEqual(len(totals["D"]), len(totals["R"]))
                claimed = [
                    float(value) for value in re.findall(r"\b(\d{1,3}(?:\.5)?)/100\b", section)
                ]
                expected = [totals["D"][-1], totals["R"][-1]]
                for guides, documents in zip(totals["D"][:-1], totals["R"][:-1], strict=True):
                    expected += [guides, documents]
                self.assertEqual(claimed[: len(expected)], expected)
                current = text.split('<a id="current-answer"></a>', 1)[1].split("\n## ", 2)[1]
                self.assertIn("#straightforwardness-95", current)
                self.assertIn(f"{totals['D'][-1]:g}/100", current)
                self.assertIn(f"{totals['R'][-1]:g}/100", current)

    def test_validation_page_answers_first_and_collapses_dated_history(self):
        for language, directory, _ in self.language_labs():
            with self.subTest(language=language):
                text = (directory / "reference/validation.md").read_text()
                headings = re.findall(r"^## (.+)$", text, re.MULTILINE)
                self.assertTrue(
                    text.split("\n## ", 1)[0].rstrip().endswith('<a id="current-answer"></a>')
                )
                visible = expanded_markdown(text)
                for anchor in (
                    "gpt-6-sol-20260924",
                    "previously-not-run-items",
                    "foundry-evaluation-additions",
                    "gpt-6-sol-20260923",
                    "straightforwardness-95",
                ):
                    self.assertIn(f'<a id="{anchor}"></a>', visible)
                history = (directory / "reference/validation-history.md").read_text()
                self.assertIn("(validation-history.md)", text)
                for anchor in (
                    "straightforwardness-v3",
                    "guide-straightforwardness-v2",
                    "guide-straightforwardness",
                ):
                    self.assertIn(f'<a id="{anchor}"></a>', history)
                    self.assertNotIn(f'<a id="{anchor}"></a>', text)
                history_headings = re.findall(r"^## (.+)$", history, re.MULTILINE)
                self.assertEqual(len(history_headings), len(set(history_headings)))
                visible_headings = re.findall(r"^## (.+)$", visible, re.MULTILINE)
                self.assertFalse([name for name in visible_headings if "15" in name.split("—")[-1]])
                self.assertEqual(len(headings), len(set(headings)))

    def test_full_error_reference_has_the_same_rows_in_both_languages(self):
        tables = []
        for _, directory, _ in self.language_labs():
            text = (directory / "reference/troubleshooting.md").read_text()
            block = text.split("<details>", 1)[1].split("</details>", 1)[0]
            rows = [line for line in block.splitlines() if line.startswith("| ")][1:]
            tables.append([row.rstrip(" |").rsplit("| ", 1)[1] for row in rows])
        self.assertGreaterEqual(len(tables[0]), 50)
        self.assertEqual(tables[0], tables[1])

    def test_saving_reference_names_every_command_that_accepts_output(self):
        subcommands = next(
            action for action in parser()._actions if isinstance(action, argparse._SubParsersAction)
        ).choices
        accepting = [
            name
            for name, subparser in subcommands.items()
            if any("--output" in action.option_strings for action in subparser._actions)
        ]
        self.assertIn("maf-evaluate", accepting)
        for _, directory, _ in self.language_labs():
            text = (directory / "reference/commands.md").read_text()
            paragraph = text.split('<a id="saving-json"></a>', 1)[1].split("\n\n", 3)[2]
            for name in accepting:
                self.assertIn(f"`{name}`", paragraph)

    def test_learner_start_file_points_to_the_guide_outside_the_zip(self):
        for language, marker in (("en", "(not in this ZIP)"), ("ko", "(이 ZIP에는 없음)")):
            with self.subTest(language=language):
                start = (ROOT / "data/learner" / language / "START-HERE.txt").read_text()
                self.assertIn(marker, start)
                for path in re.findall(r"docs/[\w/.-]+\.md", start):
                    self.assertTrue((ROOT / path).is_file(), path)

    def test_b_notes_copy_is_executable_and_never_overwrites_personal_records(self):
        names = (
            "session-notes.txt",
            "workflow-review.txt",
            "operations-checklist.txt",
            "SOURCE.json",
        )
        for language, _, labs in self.language_labs():
            with self.subTest(language=language), workspace() as root:
                section = labs[0].read_text().split('<a id="prepare-notes"></a>', 1)[1]
                block = re.findall(r"```bash\n(.*?)```", section, re.DOTALL)[0]
                directory = f"outputs/learner-notes-{language}"
                self.assertEqual(
                    shlex.split(block),
                    [
                        "mkdir",
                        "-p",
                        "outputs",
                        "&&",
                        "mkdir",
                        directory,
                        "&&",
                        "cp",
                        f"data/learner/{language}/{{{','.join(names)}}}",
                        directory + "/",
                    ],
                )
                first = subprocess.run(
                    ["bash", "-c", block],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    timeout=10,
                    check=False,
                )
                self.assertEqual(first.returncode, 0, first.stderr)
                self.assertEqual({path.name for path in (root / directory).iterdir()}, set(names))
                for name in names:
                    self.assertEqual(
                        (root / directory / name).read_bytes(),
                        (root / "data/learner" / language / name).read_bytes(),
                    )
                notes = root / directory / "session-notes.txt"
                notes.write_text("Synthetic learner observation that must survive a rerun.\n")
                before = {path.name: path.read_bytes() for path in (root / directory).iterdir()}
                repeated = subprocess.run(
                    ["bash", "-c", block],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    timeout=10,
                    check=False,
                )
                self.assertNotEqual(repeated.returncode, 0)
                self.assertEqual(
                    {path.name: path.read_bytes() for path in (root / directory).iterdir()}, before
                )

    def test_hosted_guide_has_one_preparation_route_and_explicit_guarded_azd_scope(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                text = labs[8].read_text()
                blocks = re.findall(r"```bash\n(.*?)```", text, re.DOTALL)
                lines = [
                    line.strip()
                    for block in blocks
                    for line in block.replace("\\\n", " ").splitlines()
                ]
                prepare = [
                    shlex.split(line)
                    for line in lines
                    if line.startswith("python scripts/prepare_hosted_azd.py ")
                    and "--help" not in line
                ]
                self.assertEqual(
                    prepare,
                    [
                        [
                            "python",
                            "scripts/prepare_hosted_azd.py",
                            "--language",
                            language,
                            "--kind",
                            "runtime",
                            "--package",
                            "$HOSTED_PACKAGE",
                            "--directory",
                            "$HOSTED_DIRECTORY",
                            "--agent-name",
                            "$HOSTED_AGENT_NAME",
                            "--initialize-env",
                            "--project-id",
                            "$PROJECT_ARM_ID",
                            "--location",
                            "$PROJECT_LOCATION",
                        ]
                    ],
                )
                self.assertFalse(any(line.startswith("azd ai agent init ") for line in lines))
                scoped = [
                    line.removesuffix("&&").rstrip()
                    for line in lines
                    if line.startswith(
                        ("azd deploy ", "azd ai agent show ", "azd ai agent invoke ")
                    )
                ]
                self.assertEqual(sum(line.startswith("azd deploy ") for line in scoped), 1)
                self.assertEqual(len(scoped), 5)
                values = {
                    "HOSTED_DIRECTORY": str(ROOT),
                    "HOSTED_AGENT_NAME": "mfv2-unit",
                    "HOSTED_AGENT_VERSION": "1",
                }
                for line in scoped:
                    arguments = shlex.split(line)
                    self.assertIn("--cwd", arguments)
                    self.assertTrue(
                        arguments[arguments.index("--cwd") + 1].startswith("${HOSTED_DIRECTORY:?")
                    )
                    if arguments[1] == "deploy":
                        self.assertTrue(arguments[2].startswith("${HOSTED_AGENT_NAME:?"))
                    if "--version" in arguments:
                        self.assertTrue(
                            arguments[arguments.index("--version") + 1].startswith(
                                "${HOSTED_AGENT_VERSION:?"
                            )
                        )
                    for missing in re.findall(r"\$\{(HOSTED_[A-Z_]+):\?", line):
                        for empty in (False, True):
                            with self.subTest(command=line, missing=missing, empty=empty):
                                environment = {"PATH": os.defpath, **values}
                                if empty:
                                    environment[missing] = ""
                                else:
                                    del environment[missing]
                                result = subprocess.run(
                                    [
                                        "bash",
                                        "-c",
                                        "azd() { printf 'UNEXPECTED_AZD_CALL'; }\n" + line,
                                    ],
                                    env=environment,
                                    capture_output=True,
                                    text=True,
                                    timeout=10,
                                    check=False,
                                )
                                self.assertNotEqual(result.returncode, 0)
                                self.assertNotIn("UNEXPECTED_AZD_CALL", result.stdout)
                                self.assertIn(missing, result.stderr)

    def test_incomplete_evaluation_has_a_handoff_before_any_holdout_unlock(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                evaluation = self.core_section(language, labs[7], "B")
                link = "(11-capstone.md#incomplete-handoff)"
                self.assertIn(link, evaluation)
                self.assertLess(evaluation.index(link), evaluation.index("--unlock-holdout"))
                handoff = self.core_section(language, labs[11], "B")
                incomplete = handoff.split('<a id="incomplete-handoff"></a>', 1)[1]
                self.assertIn("session-notes.txt", incomplete)
                self.assertIn("operations-checklist.txt", incomplete)
                self.assertEqual(DOCS.workshop_commands(incomplete), [])

    def test_printed_outputs_have_a_save_checkpoint_before_the_next_command(self):
        expected = {
            2: ("model.json", "answer-local.json"),
            3: ("prompt-agent-create.json", "prompt-agent-invoke.json"),
            4: ("maf-none.json", "maf-function.json", "maf-mcp.json"),
            5: (
                "workflow-sequential.json",
                "workflow-concurrent.json",
                "workflow-group-chat.json",
            ),
            6: (
                "retrieve-local.json",
                "retrieve-search.json",
                "retrieve-iq.json",
                "answer-iq.json",
            ),
        }
        for language, _, labs in self.language_labs():
            for number, filenames in expected.items():
                core = self.core_section(language, labs[number], "B").replace("\\\n", " ")
                commands = DOCS.workshop_commands(core)
                saved = []
                for index, (line, arguments) in enumerate(commands):
                    parsed = parser().parse_args(arguments)
                    if parsed.command in {"doctor", "seed-search"}:
                        continue
                    following = core.split(line, 1)[1]
                    if index + 1 < len(commands):
                        following = following.split(commands[index + 1][0], 1)[0]
                    label = "Save" if language == "en" else "저장"
                    match = re.search(rf"\*\*{label}:\*\* `([^`]+)`", following)
                    with self.subTest(language=language, lab=number, command=line):
                        self.assertIsNotNone(match, "Name the saved file before the next command.")
                        if match:
                            self.assertEqual(
                                str(parsed.output),
                                f"outputs/learner-notes-{language}/{match[1]}",
                                "The documented command must actually save the promised JSON.",
                            )
                            saved.append(match[1])
                self.assertEqual(tuple(saved), filenames)

    def test_all_fourteen_b_exports_execute_in_both_languages_without_overwriting(self):
        def explicit_offline_transport(_root, arguments):
            return {
                "mode": "explicit-offline-command-stub",
                "command": arguments.command,
                "language": arguments.language,
                "question": arguments.question,
                "response_id": "unit-test-response",
                "trace_id": None,
            }

        for language, _, labs in self.language_labs():
            with self.subTest(language=language), workspace() as root:
                notes = root / "outputs" / f"learner-notes-{language}"
                notes.mkdir(parents=True)
                saved = set()
                for number in (2, 3, 4, 5, 6):
                    for _, arguments in DOCS.workshop_commands(
                        self.core_section(language, labs[number], "B")
                    ):
                        parsed = parser().parse_args(arguments)
                        if getattr(parsed, "output", None) is None:
                            continue
                        stdout, stderr = io.StringIO(), io.StringIO()
                        with (
                            redirect_stdout(stdout),
                            redirect_stderr(stderr),
                            patch(
                                "foundry_workshop.cli.cloud_command",
                                side_effect=explicit_offline_transport,
                            ),
                        ):
                            self.assertEqual(main(root, arguments), 0, stderr.getvalue())
                        target = root / parsed.output
                        original = target.read_bytes()
                        self.assertEqual(original, stdout.getvalue().encode("utf-8"))
                        self.assertEqual(target.parent, notes)
                        saved.add(target)
                        with (
                            redirect_stdout(io.StringIO()),
                            redirect_stderr(io.StringIO()),
                            patch("foundry_workshop.cli.cloud_command") as cloud,
                        ):
                            self.assertEqual(main(root, arguments), 2)
                        cloud.assert_not_called()
                        self.assertEqual(target.read_bytes(), original)
                self.assertEqual(len(saved), 14)

    def test_b_handoff_lists_all_printed_results_and_review_files(self):
        filenames = (
            "model.json",
            "answer-local.json",
            "prompt-agent-create.json",
            "prompt-agent-invoke.json",
            "maf-none.json",
            "maf-function.json",
            "maf-mcp.json",
            "workflow-sequential.json",
            "workflow-concurrent.json",
            "workflow-group-chat.json",
            "retrieve-local.json",
            "retrieve-search.json",
            "retrieve-iq.json",
            "answer-iq.json",
            "session-notes.txt",
            "workflow-review.txt",
            "operations-checklist.txt",
            "SOURCE.json",
            "outputs/azure-objects.json",
            "outputs/baseline/",
            "outputs/candidate/",
            "outputs/final-holdout/",
        )
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                core = self.core_section(language, labs[11], "B")
                inventory = core.split('<a id="b-evidence"></a>', 1)
                self.assertEqual(len(inventory), 2)
                for filename in filenames:
                    self.assertIn(f"`{filename}`", inventory[1])
                package = "hosted-en" if language == "en" else "hosted"
                self.assertIn(f"`.build/{package}/package-manifest.json`", inventory[1])

    def test_b_handoff_points_to_the_existing_operations_trace_field(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                worksheet = (
                    ROOT / "data/learner" / language / "operations-checklist.txt"
                ).read_text()
                prefix = "Actual trace evidence" if language == "en" else "실제 추적 근거"
                field = next(line for line in worksheet.splitlines() if line.startswith(prefix))
                handoff = self.core_section(language, labs[11], "B")
                paragraphs = [text for text in handoff.split("\n\n") if f"`{field}`" in text]
                self.assertEqual(len(paragraphs), 1, "Name the trace field where Lab 09 filled it")
                self.assertIn("`operations-checklist.txt`", paragraphs[0])
                self.assertNotIn("`session-notes.txt`", paragraphs[0])
                self.assertIn(f"`{field}`", self.core_section(language, labs[9], "B"))

    def test_browser_check_tables_use_the_canonical_dev_limits_and_citations(self):
        for language, _, labs in self.language_labs():
            directory = ROOT / "data/evaluation"
            if language == "en":
                directory /= "en"
            cases = {case["case_id"]: case for case in read_jsonl(directory / "dev.jsonl")}
            for number, expected in ((3, ["D01", "D02", "D03", "D05"]), (7, list(cases))):
                core = self.core_section(language, labs[number], "A")
                rows = [
                    (match[1], line)
                    for line in core.splitlines()
                    if (match := re.match(r"^\| (D\d{2})(?: |[|·])", line))
                ]
                with self.subTest(language=language, lab=number):
                    self.assertEqual([case_id for case_id, _ in rows], expected)
                for case_id, row in rows:
                    with self.subTest(language=language, lab=number, case=case_id):
                        for source_id in cases[case_id]["required_citations"]:
                            self.assertIn(f"`{source_id}`", row)
                        if cases[case_id]["expected_limit_krw"] is not None:
                            self.assertIn(str(cases[case_id]["expected_limit_krw"]), row)

    def test_a_assessment_snapshots_are_named_at_creation_review_and_handoff(self):
        for language, directory, labs in self.language_labs():
            with self.subTest(language=language):
                materials = ROOT / "data/learner" / language
                notes = (materials / "session-notes.txt").read_text()
                start = (materials / "START-HERE.txt").read_text()
                agent = self.core_section(language, labs[3], "A")
                assessment = self.core_section(language, labs[7], "A")
                handoff = self.core_section(language, labs[11], "A")
                route = (directory / "paths/a-beginner.md").read_text()
                for text in (agent, route, start):
                    self.assertIn("instructions-baseline.txt", text)
                for filename in (
                    "instructions-baseline.txt",
                    "instructions-candidate.txt",
                    "assessment-baseline.csv",
                    "assessment-candidate.csv",
                ):
                    for text in (assessment, handoff, notes):
                        self.assertIn(filename, text)
                self.assertIn("Lab 07 A", notes)
                self.assertIn("pass_or_fail", assessment)
                self.assertIn("review_note", assessment)

    def test_model_comparison_overrides_are_scoped_and_preserve_failures(self):
        for language, directory, _ in self.language_labs():
            text = (directory / "labs/extensions/model-operations.md").read_text()
            blocks = re.findall(r"(?m)^\(\n.*?^\)", text, re.DOTALL)
            self.assertEqual(
                len(blocks), 2, "Preflight and collection each need a scoped override."
            )
            for block in blocks:
                for value in (None, "", "mfv2-approved-alternative"):
                    for status in (0, 9):
                        with (
                            self.subTest(language=language, model=value, status=status),
                            workspace() as root,
                        ):
                            env_file = root / ".env"
                            original = b"AZURE_AI_MODEL_DEPLOYMENT_NAME=mfv2-original\n"
                            env_file.write_bytes(original)
                            environment = {
                                "PATH": os.defpath,
                                "AZURE_AI_MODEL_DEPLOYMENT_NAME": "mfv2-original",
                                "STUB_STATUS": str(status),
                            }
                            if value is not None:
                                environment["MODEL_B"] = value
                            result = subprocess.run(
                                [
                                    "bash",
                                    "-c",
                                    'python() { printf "STUB_MODEL=%s\\n" "$AZURE_AI_MODEL_DEPLOYMENT_NAME"; return "$STUB_STATUS"; }\n'
                                    + block
                                    + '\nresult=$?\nprintf "PARENT_MODEL=%s\\n" "$AZURE_AI_MODEL_DEPLOYMENT_NAME"\nexit "$result"',
                                ],
                                cwd=root,
                                env=environment,
                                capture_output=True,
                                text=True,
                                timeout=10,
                                check=False,
                            )
                            self.assertEqual(env_file.read_bytes(), original)
                            self.assertIn("PARENT_MODEL=mfv2-original", result.stdout)
                            if value:
                                self.assertIn(f"STUB_MODEL={value}", result.stdout)
                                self.assertEqual(result.returncode, status)
                            else:
                                self.assertNotEqual(result.returncode, 0)
                                self.assertNotIn("STUB_MODEL", result.stdout)
                                self.assertIn("MODEL_B", result.stderr)

    def test_project_scoped_extension_commands_reject_missing_values_before_azd(self):
        names = ("tool-search-skills.md", "routines.md", "a2a.md")
        values = {
            "PROJECT_ENDPOINT": "https://mfv2-unit.services.ai.azure.com/api/projects/unit",
            "SKILL_NAME": "mfv2-unit-policy-review",
            "SKILL_VERSION": "1",
            "ROUTINE_NAME": "mfv2-unit-timer",
            "AGENT_NAME": "mfv2-unit-agent",
            "WHEN": "2099-01-01T00:00:00+00:00",
            "A2A_BASE": "https://mfv2-unit.services.ai.azure.com/unit-a2a",
            "A2A_CONNECTION": "mfv2-unit-a2a",
        }
        for language, directory, _ in self.language_labs():
            for name in names:
                text = (directory / "labs/extensions" / name).read_text()
                for block in re.findall(r"```bash\n(.*?)```", text, re.DOTALL):
                    for line in block.replace("\\\n", " ").splitlines():
                        line = line.strip().removesuffix("&&").rstrip()
                        if not line.startswith("azd ") or "--help" in shlex.split(line):
                            continue
                        with self.subTest(language=language, file=name, command=line):
                            self.assertIn(
                                '--project-endpoint "${PROJECT_ENDPOINT:?',
                                line,
                            )
                            self.assertNotRegex(line, r'"\$[A-Z_]+"')
                            for missing in set(re.findall(r"\$\{([A-Z_]+):\?", line)):
                                for empty in (False, True):
                                    environment = {"PATH": os.defpath, **values}
                                    if empty:
                                        environment[missing] = ""
                                    else:
                                        del environment[missing]
                                    result = subprocess.run(
                                        [
                                            "bash",
                                            "-c",
                                            'azd() { printf "UNEXPECTED_AZD_CALL"; }\n' + line,
                                        ],
                                        env=environment,
                                        capture_output=True,
                                        text=True,
                                        timeout=10,
                                        check=False,
                                    )
                                    self.assertNotEqual(result.returncode, 0)
                                    self.assertNotIn("UNEXPECTED_AZD_CALL", result.stdout)
                                    self.assertIn(missing, result.stderr)

    def test_routine_disable_is_not_skipped_after_enable_or_dispatch_failure(self):
        for language, directory, _ in self.language_labs():
            text = (directory / "labs/extensions/routines.md").read_text()
            blocks = [
                block
                for block in re.findall(r"```bash\n(.*?)```", text, re.DOTALL)
                if "azd ai routine enable " in block
            ]
            self.assertEqual(len(blocks), 1)
            for enable_status, dispatch_status in ((0, 0), (7, 0), (0, 9)):
                with self.subTest(
                    language=language, enable=enable_status, dispatch=dispatch_status
                ):
                    result = subprocess.run(
                        [
                            "bash",
                            "-c",
                            'azd() { printf "%s\\n" "$3"; case "$3" in enable) return "$ENABLE_STATUS";; dispatch) return "$DISPATCH_STATUS";; esac; }\n'
                            + blocks[0],
                        ],
                        env={
                            "PATH": os.defpath,
                            "PROJECT_ENDPOINT": "https://mfv2-unit.services.ai.azure.com/api/projects/unit",
                            "ROUTINE_NAME": "mfv2-unit-timer",
                            "ENABLE_STATUS": str(enable_status),
                            "DISPATCH_STATUS": str(dispatch_status),
                        },
                        capture_output=True,
                        text=True,
                        timeout=10,
                        check=False,
                    )
                    expected = ["enable"]
                    if enable_status == 0:
                        expected.append("dispatch")
                    self.assertEqual(
                        result.stdout.splitlines(), [*expected, "disable", "run", "show"]
                    )

    def test_skill_readback_preserves_original_bytes_and_stops_before_redownloading(self):
        for language, directory, _ in self.language_labs():
            text = (directory / "labs/extensions/tool-search-skills.md").read_text()
            blocks = [
                block
                for block in re.findall(r"```bash\n(.*?)```", text, re.DOTALL)
                if "azd ai skill download " in block and "--help" not in block
            ]
            self.assertEqual(len(blocks), 1)
            marker = f"mkdir outputs/skill-readback-{language}"
            self.assertIn(marker, blocks[0])
            block = blocks[0][blocks[0].index(marker) :]
            for status in (0, 9):
                with self.subTest(language=language, status=status), workspace() as root:
                    original = b"synthetic skill bytes\n"
                    source = root / f"outputs/extensions-{language}/policy-review/SKILL.md"
                    source.parent.mkdir(parents=True)
                    source.write_bytes(original)
                    environment = {
                        "PATH": os.defpath,
                        "PROJECT_ENDPOINT": "https://mfv2-unit.services.ai.azure.com/api/projects/unit",
                        "SKILL_NAME": "mfv2-unit-policy-review",
                        "SKILL_VERSION": "1",
                        "STUB_STATUS": str(status),
                    }
                    script = (
                        'azd() { printf "STUB_DOWNLOAD\\n" >&2; while [ "$#" -gt 0 ]; do if [ "$1" = "--output-dir" ]; then printf "synthetic skill bytes\\n" > "$2/SKILL.md"; break; fi; shift; done; return "$STUB_STATUS"; }\n'
                        'cmp() { printf "STUB_COMPARE\\n" >&2; command cmp "$@"; }\n' + block
                    )
                    first = subprocess.run(
                        ["bash", "-c", script],
                        cwd=root,
                        env=environment,
                        capture_output=True,
                        text=True,
                        timeout=10,
                        check=False,
                    )
                    self.assertEqual(first.returncode, status, first.stderr)
                    self.assertEqual("STUB_COMPARE" in first.stderr, status == 0)
                    readback = root / f"outputs/skill-readback-{language}/SKILL.md"
                    self.assertEqual(readback.read_bytes(), original)
                    repeated = subprocess.run(
                        ["bash", "-c", script],
                        cwd=root,
                        env={**environment, "STUB_STATUS": "0"},
                        capture_output=True,
                        text=True,
                        timeout=10,
                        check=False,
                    )
                    self.assertNotEqual(repeated.returncode, 0)
                    self.assertNotIn("STUB_DOWNLOAD", repeated.stderr)
                    self.assertNotIn("STUB_COMPARE", repeated.stderr)
                    self.assertEqual(readback.read_bytes(), original)

    def test_all_guide_bash_blocks_parse_without_executing_cloud_commands(self):
        for path in DOCS.markdown_files(ROOT):
            for index, block in enumerate(
                re.findall(r"```bash\n(.*?)```", path.read_text(), re.DOTALL)
            ):
                with self.subTest(path=path.relative_to(ROOT), block=index):
                    result = subprocess.run(
                        ["bash", "-n"], input=block, text=True, capture_output=True, check=False
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)

    def test_every_extension_has_a_first_pass_and_is_reachable_from_the_catalog(self):
        for language, directory, _ in self.language_labs():
            catalog = (directory / "paths/c-advanced.md").read_text()
            modules = sorted((directory / "labs/extensions").glob("*.md"))
            self.assertGreaterEqual(len(modules), 16)
            for path in modules:
                with self.subTest(language=language, module=path.name):
                    text = expanded_markdown(path.read_text())
                    first_pass = "**First pass:**" if language == "en" else "**첫 회차:**"
                    self.assertIn(first_pass, text.split("\n## ", 1)[0])
                    self.assertIn(f"(../labs/extensions/{path.name})", catalog)
                    self.assertTrue(
                        any(
                            f"({target})" in text
                            for target in (
                                "../../paths/c-advanced.md",
                                "../../paths/b-practitioner.md",
                                "../11-capstone.md",
                            )
                        ),
                        f"{path}: provide a visible route or handoff link",
                    )

    def test_optional_extension_mutations_and_maintainer_work_are_not_in_the_first_pass(self):
        for language, directory, _ in self.language_labs():
            extensions = directory / "labs/extensions"
            with self.subTest(language=language):
                toolbox = [
                    parser().parse_args(arguments).toolbox_action
                    for _, arguments in DOCS.workshop_commands(
                        expanded_markdown((extensions / "toolbox.md").read_text())
                    )
                ]
                self.assertEqual(
                    toolbox, ["plan", "create", "inspect", "probe", "query", "ask", "cleanup"]
                )
                skills = expanded_markdown((extensions / "tool-search-skills.md").read_text())
                self.assertNotIn("toolbox select", skills)
                tools = [
                    parser().parse_args(arguments).command
                    for _, arguments in DOCS.workshop_commands(
                        expanded_markdown((extensions / "additional-tools.md").read_text())
                    )
                ]
                self.assertEqual(tools, ["code-interpreter", "code-interpreter"])
                recovery = expanded_markdown((extensions / "approval-recovery.md").read_text())
                self.assertIn("--run-id first-pass", recovery)
                self.assertNotIn("--run-id resume-pass", recovery)
                self.assertNotIn("--crash-after-checkpoint", recovery)
                self.assertNotIn("-m unittest", recovery)
                toolkit = expanded_markdown((extensions / "developer-toolkit.md").read_text())
                self.assertNotIn("python scripts/check_sdk.py", toolkit)
                self.assertNotIn('pip install -e ".[hosted]"', toolkit)
                cleanup = expanded_markdown((directory / "reference/cleanup.md").read_text())
                self.assertEqual(DOCS.workshop_commands(cleanup), [])
                self.assertIn("operations-checklist.txt", cleanup)
                self.assertNotIn("media.json", cleanup)

    def test_matrix_first_pass_does_not_depend_on_an_uncreated_regression(self):
        for language, directory, _ in self.language_labs():
            with self.subTest(language=language):
                text = (directory / "reference/evaluation-workbook.md").read_text()
                visible = expanded_markdown(text)
                commands = [
                    parser().parse_args(arguments)
                    for _, arguments in DOCS.workshop_commands(visible)
                ]
                collections = [
                    command
                    for command in commands
                    if command.command == "benchmark" and command.benchmark_action == "collect"
                ]
                self.assertEqual(
                    [command.label for command in collections],
                    ["wf-baseline", "wf-candidate", "wf-final"],
                )
                self.assertTrue(all(command.regressions is None for command in collections))
                self.assertNotIn("benchmark regression", visible)
                verification = [
                    command
                    for command in commands
                    if command.command == "benchmark" and command.benchmark_action == "verify"
                ]
                self.assertEqual(len(verification), 1)
                self.assertFalse(verification[0].require_regressions)
                self.assertTrue(verification[0].require_native)
                self.assertTrue(verification[0].require_traces)
                local_smoke = [
                    command
                    for command in commands
                    if command.command == "benchmark"
                    and command.benchmark_action == "smoke"
                    and command.local
                ]
                self.assertEqual(len(local_smoke), 1)
                self.assertIsNotNone(local_smoke[0].azd_directory)
                self.assertLess(
                    visible.index("models.<key>.business_gate_passed: true"),
                    visible.index("--unlock-holdout"),
                )
                preparations = [
                    shlex.split(line.strip())
                    for block in re.findall(r"```bash\n(.*?)```", text, re.DOTALL)
                    for line in block.replace("\\\n", " ").splitlines()
                    if line.strip().startswith("python scripts/prepare_hosted_azd.py ")
                ]
                self.assertEqual(len(preparations), 2)
                for command in preparations:
                    self.assertEqual(command[command.index("--kind") + 1], "matrix")
                    self.assertEqual(command[command.index("--language") + 1], language)
                    self.assertIn("--initialize-env", command)
                self.assertNotRegex(text, r"(?m)^azd ai agent init ")
                self.assertNotRegex(text, r"(?m)^azd env set ")

    def test_extension_azd_commands_fail_before_execution_when_scope_values_are_missing(self):
        names = (
            "labs/extensions/toolbox-hosted.md",
            "labs/extensions/agent-safety.md",
            "reference/evaluation-workbook.md",
            "reference/cleanup.md",
        )
        values = {
            "HOSTED_DIRECTORY": str(ROOT),
            "HOSTED_AGENT_NAME": "mfv2-unit-hosted",
            "HOSTED_AGENT_VERSION": "1",
            "OWNED_SESSION_ID": "unit-session",
        }
        for language, directory, _ in self.language_labs():
            for name in names:
                blocks = re.findall(r"```bash\n(.*?)```", (directory / name).read_text(), re.DOTALL)
                for block in blocks:
                    for line in block.replace("\\\n", " ").splitlines():
                        line = line.strip()
                        if not line.startswith("azd "):
                            continue
                        line = re.split(r"\s+\|", line, maxsplit=1)[0].removesuffix("&&").rstrip()
                        arguments = shlex.split(line)
                        with self.subTest(language=language, file=name, command=line):
                            self.assertIn("--cwd", arguments)
                            self.assertTrue(
                                arguments[arguments.index("--cwd") + 1].startswith(
                                    "${HOSTED_DIRECTORY:?"
                                )
                            )
                            if arguments[1] == "deploy":
                                self.assertTrue(arguments[2].startswith("${HOSTED_AGENT_NAME:?"))
                            for flag, prefix in (
                                ("--agent-name", "${HOSTED_AGENT_NAME:?"),
                                ("--version", "${HOSTED_AGENT_VERSION:?"),
                            ):
                                if flag in arguments:
                                    self.assertTrue(
                                        arguments[arguments.index(flag) + 1].startswith(prefix)
                                    )
                            for missing in set(re.findall(r"\$\{([A-Z_]+):\?", line)):
                                for empty in (False, True):
                                    environment = {"PATH": os.defpath, **values}
                                    if empty:
                                        environment[missing] = ""
                                    else:
                                        del environment[missing]
                                    result = subprocess.run(
                                        [
                                            "bash",
                                            "-c",
                                            'azd() { printf "UNEXPECTED_AZD_CALL"; }\n' + line,
                                        ],
                                        env=environment,
                                        capture_output=True,
                                        text=True,
                                        timeout=10,
                                        check=False,
                                    )
                                    self.assertNotEqual(result.returncode, 0, (missing, empty))
                                    self.assertNotIn("UNEXPECTED_AZD_CALL", result.stdout)
                                    self.assertIn(missing, result.stderr)

                    if "azd deploy " in block:
                        deployment = block[block.index("azd deploy ") :]
                        result = subprocess.run(
                            [
                                "bash",
                                "-c",
                                'azd() { printf "%s\\n" "$1"; return 9; }\n' + deployment,
                            ],
                            env={"PATH": os.defpath, **values},
                            capture_output=True,
                            text=True,
                            timeout=10,
                            check=False,
                        )
                        self.assertEqual(result.returncode, 9)
                        self.assertEqual(result.stdout.strip(), "deploy")

    def test_toolbox_remote_block_preserves_failed_streams_and_rejects_overwrite_before_calling(
        self,
    ):
        for language, directory, _ in self.language_labs():
            text = (directory / "labs/extensions/toolbox-hosted.md").read_text()
            blocks = [
                block
                for block in re.findall(r"```bash\n(.*?)```", text, re.DOTALL)
                if "set -o pipefail" in block
            ]
            self.assertEqual(len(blocks), 1)
            for status in (0, 9):
                with self.subTest(language=language, status=status), workspace() as root:
                    environment = {
                        "PATH": os.defpath,
                        "HOSTED_PACKAGE": str(root),
                        "HOSTED_DIRECTORY": str(root),
                        "HOSTED_AGENT_NAME": "mfv2-unit-hosted",
                        "HOSTED_AGENT_VERSION": "1",
                        "STUB_STATUS": str(status),
                    }
                    script = (
                        'azd() { printf "STUB_AZD_CALL\\n" >&2; printf "synthetic test stream\\n"; return "$STUB_STATUS"; }\n'
                        'python() { printf "STUB_VERIFIER_CALLED\\n"; }\n' + blocks[0]
                    )
                    first = subprocess.run(
                        ["bash", "-c", script],
                        cwd=root,
                        env=environment,
                        capture_output=True,
                        text=True,
                        timeout=10,
                        check=False,
                    )
                    self.assertEqual(first.returncode, status, first.stderr)
                    self.assertIn("STUB_AZD_CALL", first.stderr)
                    self.assertEqual("STUB_VERIFIER_CALLED" in first.stdout, status == 0)
                    raw = root / f"outputs/toolbox-remote-{language}/response.raw"
                    self.assertEqual(raw.read_bytes(), b"synthetic test stream\n")
                    repeated = subprocess.run(
                        ["bash", "-c", script],
                        cwd=root,
                        env={**environment, "STUB_STATUS": "0"},
                        capture_output=True,
                        text=True,
                        timeout=10,
                        check=False,
                    )
                    self.assertNotEqual(repeated.returncode, 0)
                    self.assertNotIn("STUB_AZD_CALL", repeated.stderr)
                    self.assertNotIn("STUB_VERIFIER_CALLED", repeated.stdout)
                    self.assertEqual(raw.read_bytes(), b"synthetic test stream\n")

    def test_documented_offline_rehearsal_creates_real_files_and_preserves_existing_runs(self):
        def run(root, arguments, script="workshop.py"):
            return subprocess.run(
                [sys.executable, "-S", f"scripts/{script}", *arguments],
                cwd=root,
                env={
                    "PATH": os.defpath,
                    "PYTHONIOENCODING": "utf-8",
                    "PYTHONDONTWRITEBYTECODE": "1",
                },
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

        for language, _, labs in self.language_labs():
            with self.subTest(language=language), workspace() as root:
                rehearsal = (
                    labs[0]
                    .read_text()
                    .split('<a id="offline-rehearsal"></a>', 1)[1]
                    .split("### 3.", 1)[0]
                )
                commands = [arguments for _, arguments in DOCS.workshop_commands(rehearsal)]
                self.assertEqual(
                    [parser().parse_args(arguments).command for arguments in commands],
                    ["doctor", "demo", "demo", "compare"],
                )
                self.assertNotIn("--cloud", commands[0])
                (root / "scripts").mkdir()
                for script in ("workshop.py", "package_hosted.py"):
                    shutil.copy2(ROOT / "scripts" / script, root / "scripts" / script)
                results = []
                for arguments in commands:
                    process = run(root, arguments)
                    self.assertEqual(process.returncode, 0, process.stderr)
                    results.append(json.loads(process.stdout))
                self.assertFalse(results[0]["azure_tested"])
                self.assertEqual(
                    [results[0][key] for key in ("documents", "dev_cases", "holdout_cases")],
                    [6, 6, 4],
                )
                for label, passed in (("rehearsal-v1", 0), ("rehearsal-v2", 6)):
                    directory = root / "outputs" / label
                    manifest = read_json(directory / "manifest.json")
                    rows = read_jsonl(directory / "responses.jsonl")
                    grade = read_json(directory / "business-evaluation.json")
                    self.assertEqual(manifest["language"], language)
                    self.assertEqual(manifest["mode"], "offline-fixture")
                    self.assertEqual(manifest["deployment"], "not-a-model")
                    self.assertEqual(len(rows), 6)
                    self.assertEqual(len({row["case_id"] for row in rows}), 6)
                    self.assertTrue(all(row["response_id"] is None for row in rows))
                    self.assertTrue(all(row["usage"] is None for row in rows))
                    self.assertEqual(
                        (grade["total"], grade["passed"], grade["errors"]), (6, passed, 0)
                    )
                    self.assertEqual(grade["business_gate_passed"], passed == 6)
                comparison = read_json(
                    root / "outputs/rehearsal-v2/comparison-vs-rehearsal-v1.json"
                )
                self.assertEqual(comparison, results[-1])
                self.assertEqual(comparison["changed_context_cases"], [])
                self.assertIn("OFFLINE FIXTURES ONLY", comparison["note"])
                readme = ROOT / ("README.md" if language == "en" else "README.ko.md")
                preview = DOCS.workshop_commands(expanded_markdown(readme.read_text()))
                self.assertEqual(
                    [parser().parse_args(arguments).command for _, arguments in preview],
                    ["doctor", "demo"],
                )
                for _, arguments in preview:
                    process = run(root, arguments)
                    self.assertEqual(process.returncode, 0, process.stderr)
                preview_manifest = read_json(root / "outputs/first-offline/manifest.json")
                preview_grade = read_json(root / "outputs/first-offline/business-evaluation.json")
                self.assertEqual(preview_manifest["language"], language)
                self.assertEqual(preview_manifest["mode"], "offline-fixture")
                self.assertEqual(
                    (preview_grade["total"], preview_grade["passed"], preview_grade["errors"]),
                    (6, 6, 0),
                )
                failed_gate = run(root, ["evaluate", "--label", "rehearsal-v1"])
                self.assertEqual(failed_gate.returncode, 1)
                self.assertFalse(json.loads(failed_gate.stdout)["business_gate_passed"])
                before = {
                    path.relative_to(root): path.read_bytes()
                    for path in (root / "outputs").rglob("*")
                    if path.is_file()
                }
                repeated = run(root, commands[2])
                self.assertEqual(repeated.returncode, 2)
                after = {
                    path.relative_to(root): path.read_bytes()
                    for path in (root / "outputs").rglob("*")
                    if path.is_file()
                }
                self.assertEqual(after, before)
                package_core = self.core_section(language, labs[8], "B")
                package_blocks = re.findall(r"```bash\n(.*?)```", package_core, re.DOTALL)
                self.assertEqual(len(package_blocks), 1)
                package_command = shlex.split(package_blocks[0])
                self.assertEqual(package_command[:2], ["python", "scripts/package_hosted.py"])
                packaged = run(root, package_command[2:], "package_hosted.py")
                self.assertEqual(packaged.returncode, 0, packaged.stderr)
                package_name = "hosted-en" if language == "en" else "hosted"
                manifest = read_json(root / ".build" / package_name / "package-manifest.json")
                self.assertFalse(manifest["cloud_deployed"])
                self.assertEqual(
                    RuntimeProfile.from_dict(manifest["runtime_profile"]).language, language
                )
                cleanup_commands = DOCS.workshop_commands(self.core_section(language, labs[9], "B"))
                self.assertEqual(len(cleanup_commands), 1)
                self.assertEqual(
                    parser().parse_args(cleanup_commands[0][1]).command, "cleanup-plan"
                )
                cleanup = run(root, cleanup_commands[0][1])
                self.assertEqual(cleanup.returncode, 0, cleanup.stderr)
                cleanup_result = json.loads(cleanup.stdout)
                self.assertFalse(cleanup_result["deletes_resources"])
                self.assertEqual(
                    cleanup_result["guide"],
                    "docs/reference/cleanup.md"
                    if language == "en"
                    else "docs/ko/reference/cleanup.md",
                )
                self.assertTrue((root / ".build" / package_name / "package-manifest.json").exists())
                self.assertEqual(
                    {
                        path.relative_to(root): path.read_bytes()
                        for path in (root / "outputs").rglob("*")
                        if path.is_file()
                    },
                    before,
                )

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
        for path in DOCS.markdown_files(ROOT):
            with self.subTest(path=path.relative_to(ROOT)):
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
                comparison = labs[7].read_text()
                for field in ("changed_context_cases", "baseline_metrics", "candidate_metrics"):
                    self.assertIn(field, comparison)
                self.assertNotIn("changed_context_count", comparison)
                self.assertNotIn("unchanged_config", comparison)
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
