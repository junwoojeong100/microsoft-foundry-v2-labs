import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import unittest
from itertools import pairwise

from foundry_workshop.cli import parser
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

    def test_lab_bash_blocks_parse_without_executing_cloud_commands(self):
        for language, _, labs in self.language_labs():
            for number, path in labs.items():
                for index, block in enumerate(
                    re.findall(r"```bash\n(.*?)```", path.read_text(), re.DOTALL)
                ):
                    with self.subTest(language=language, lab=number, block=index):
                        result = subprocess.run(
                            ["bash", "-n"], input=block, text=True, capture_output=True, check=False
                        )
                        self.assertEqual(result.returncode, 0, result.stderr)

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
