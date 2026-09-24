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

from foundry_workshop.cli import main, parser
from foundry_workshop.contracts import load_documents, read_json, read_jsonl
from foundry_workshop.profiles import RuntimeProfile

from . import ROOT, workspace
from .test_packaging import load_script

DOCS = load_script("check_docs")

ROUTES = {
    "A": (0, 1, 2, 3, 5, 6, 7, 9, 11),
    "B": (0, 2, 4, 5, 6, 7, 8, 9, 11),
}

CORE_COMMANDS = {
    0: ("doctor", "demo", "demo", "compare", "doctor"),
    2: ("doctor", "model", "answer"),
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
            for route, following, total in (("A", "B", 240), ("B", "C", 360)):
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
                    self.assertEqual(len(minutes), 10)
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
                    self.assertEqual([int(index) for index, _ in rows], list(range(1, 10)))
                    self.assertEqual(
                        [target for _, target in rows],
                        [f"{labs[number].name}#path-{route.lower()}" for number in ROUTES[route]],
                    )
                    for number in ROUTES[route]:
                        self.core_section(language, labs[number], route)

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
                for check in (
                    "python -m ruff check .",
                    "python -m ruff format --check .",
                    "python -m compileall -q",
                    "python -m unittest discover -s tests -t . -v",
                    "python scripts/check_docs.py",
                ):
                    self.assertIn(check, visible)

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

    def test_four_object_sketch_keeps_deployments_at_account_scope(self):
        for language, _, labs in self.language_labs():
            with self.subTest(language=language):
                core = self.core_section(language, labs[1], "A")
                self.assertIn('F --> D["', core)
                self.assertIn('F --> P["', core)
                self.assertNotRegex(core, r"→ (?:deployment|배포) gpt-6-sol →")
                relation = (
                    "agent → calls → deployment" if language == "en" else "에이전트 → 호출 → 배포"
                )
                self.assertIn(relation, core)

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

    def test_editorial_rubric_is_consistent_without_forcing_a_particular_score(self):
        for language, directory, _ in self.language_labs():
            with self.subTest(language=language):
                text = (directory / "reference/validation.md").read_text()
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
                text = (directory / "reference/validation.md").read_text()
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
                text = (directory / "reference/validation.md").read_text()
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

    def test_all_twelve_b_exports_execute_in_both_languages_without_overwriting(self):
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
                for number in (2, 4, 5, 6):
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
                self.assertEqual(len(saved), 12)

    def test_b_handoff_lists_all_printed_results_and_review_files(self):
        filenames = (
            "model.json",
            "answer-local.json",
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
                    ["doctor", "demo", "evaluate"],
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
