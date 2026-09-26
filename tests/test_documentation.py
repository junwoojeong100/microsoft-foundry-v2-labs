import argparse
import hashlib
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from . import ROOT
from .test_packaging import load_script

DOCS = load_script("check_docs")


class DocumentationTests(unittest.TestCase):
    def test_every_command_family_has_a_bilingual_lookup(self):
        commands = next(
            action
            for action in DOCS.parser()._actions
            if isinstance(action, argparse._SubParsersAction)
        ).choices
        for directory in ("docs", "docs/ko"):
            text = (ROOT / directory / "reference/commands.md").read_text()
            for command in commands:
                with self.subTest(directory=directory, command=command):
                    self.assertRegex(text, rf"`{re.escape(command)}(?: |`)")

    def test_configuration_templates_use_documented_environment_names(self):
        template = (ROOT / ".env.example").read_text()
        names = set(re.findall(r"^(?:# )?([A-Z][A-Z0-9_]*)=", template, re.MULTILINE))
        self.assertTrue(names)
        for directory in ("docs", "docs/ko"):
            text = (ROOT / directory / "reference/configuration.md").read_text()
            for name in names:
                with self.subTest(directory=directory, setting=name):
                    self.assertIn(f"`{name}`", text)
        for path in (ROOT / "examples/hosted").glob("*.yaml.example"):
            with self.subTest(template=path.name):
                referenced = set(re.findall(r"\$\{([A-Z][A-Z0-9_]*)\}", path.read_text()))
                self.assertEqual(referenced - names, set())

    def test_output_parity_normalizes_only_the_selected_languages_notes_directory(self):
        english = ["--language", "en", "model", "--output", "outputs/learner-notes-en/model.json"]
        korean = ["model", "--output", "outputs/learner-notes-ko/model.json"]
        self.assertEqual(DOCS.normalized_command(english, {}), DOCS.normalized_command(korean, {}))
        for wrong in (
            "outputs/learner-notes-ko/model.json",
            "outputs/learner-notes-en/answer.json",
        ):
            self.assertNotEqual(
                DOCS.normalized_command([*english[:-1], wrong], {}),
                DOCS.normalized_command(korean, {}),
            )

    def test_language_specific_extension_labels_keep_strict_command_parity(self):
        english = ["--language", "en", "prepare-extensions", "--label", "extensions-en"]
        korean = ["--language", "ko", "prepare-extensions", "--label", "extensions-ko"]
        self.assertEqual(DOCS.normalized_command(english, {}), DOCS.normalized_command(korean, {}))
        self.assertNotEqual(
            DOCS.normalized_command(english, {}),
            DOCS.normalized_command(
                ["--language", "ko", "prepare-extensions", "--label", "extensions-en"], {}
            ),
        )

    def test_readmes_do_not_present_upstream_source_columns(self):
        for name in ("README.md", "README.ko.md"):
            tables = "\n".join(
                line for line in (ROOT / name).read_text().splitlines() if line.startswith("|")
            )
            self.assertNotIn("Main source modules", tables)
            self.assertNotIn("주요 통합 원본", tables)
            self.assertNotIn("Agent Framework Labs", tables)
            self.assertNotIn("Foundry Evaluation", tables)

    def test_korean_first_exception_requires_visible_notice_and_exact_hashes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            english, korean = root / "README.md", root / "README.ko.md"
            english.write_text(
                "# Guide\n\n**English** | [한국어](README.ko.md)\n\n"
                "<!-- translation-pending: ko-revision -->\n\n"
                "> **Translation pending** — read the Korean revision.\n"
            )
            korean.write_text("# 새 가이드\n\n[English](README.md) | **한국어**\n")
            state = {
                "schema_version": 1,
                "revision": "ko-revision",
                "source_language": "ko",
                "pending_files": {
                    "README.md": {
                        "english_sha256": hashlib.sha256(english.read_bytes()).hexdigest(),
                        "korean_sha256": hashlib.sha256(korean.read_bytes()).hexdigest(),
                    }
                },
            }
            (root / "docs/localization.json").write_text(json.dumps(state))
            failures = []
            self.assertEqual(DOCS.pending_translations(root, failures), {english})
            self.assertEqual(failures, [])
            korean.write_text(korean.read_text() + "\nChanged command\n")
            failures = []
            self.assertEqual(DOCS.pending_translations(root, failures), set())
            self.assertTrue(any("hashes" in failure for failure in failures))

    def test_all_language_pairs_links_anchors_and_cli_examples_are_valid(self):
        with patch.object(DOCS, "parser", wraps=DOCS.parser) as command_parser:
            failures, counts = DOCS.check(ROOT)
        command_parser.assert_called_once()
        self.assertEqual(failures, [])
        self.assertGreaterEqual(counts["language_pairs"], 31)
        self.assertGreaterEqual(counts["cli_examples"], 108)
        self.assertGreater(counts["local_anchors"], 0)

    def test_hosted_workbook_checks_collection_and_calibration_before_paid_next_steps(self):
        for directory in ("docs", "docs/ko"):
            with self.subTest(directory=directory):
                text = (ROOT / directory / "reference/evaluation-workbook.md").read_text()
                baseline = text.split("## 5.", 1)[1].split("benchmark evaluate", 1)[0]
                for marker in (
                    "`manifest.json`",
                    "`business-evaluation.json`",
                    "`status: completed`",
                    "`actual_rows`",
                    "`expected_rows`",
                    "`errors: 0`",
                    "#incomplete-handoff",
                ):
                    self.assertIn(marker, baseline)
                calibration = text.split("## 8.", 1)[1].split("## 9.", 1)[0]
                for marker in (
                    "outputs/judge-calibration/judge-calibration/calibration.json",
                    "`total: 2`",
                    "`correct: 2`",
                    "`gate_passed: true`",
                    "1/2",
                ):
                    self.assertIn(marker, calibration)
                holdout_gate = text.split("## 9.", 1)[1].split("--unlock-holdout", 1)[0]
                self.assertIn("calibration", holdout_gate)
                self.assertIn("#incomplete-handoff", holdout_gate)

    def test_insights_sdk_preserves_results_before_separate_cleanup(self):
        for directory in ("docs", "docs/ko"):
            with self.subTest(directory=directory):
                text = (ROOT / directory / "labs/extensions/agent-insights.md").read_text()
                block = next(
                    block
                    for block in re.findall(r"```python\n(.*?)```", text, re.DOTALL)
                    if "agent_insight_monitors" in block
                )
                self.assertIn("run = monitors.begin_create_run", block)
                self.assertIn("insights = list(", block)
                self.assertNotIn("monitors.delete(", block)
                cleanup = text.split(block, 1)[1].split("</details>", 1)[0]
                self.assertLess(
                    cleanup.index("insights-review.txt"), cleanup.index("monitors.delete(")
                )

    def test_trace_setup_and_local_metadata_do_not_claim_a_verified_connection(self):
        for directory, optional, unverified, disclaimer in (
            ("docs", "step 5 is optional", "trace unverified", "not a check of"),
            ("docs/ko", "5단계는 선택", "추적 미확인", "검사한 결과가 아니며"),
        ):
            with self.subTest(directory=directory):
                owner = (ROOT / directory / "setup-owner.md").read_text()
                self.assertIn(optional, owner.split("1. **", 1)[0])
                for name in ("setup-owner.md", "instructor.md"):
                    self.assertIn(unverified, (ROOT / directory / name).read_text())
                operations = (
                    (ROOT / directory / "labs/09-operations.md")
                    .read_text()
                    .split('<a id="path-b"></a>', 1)[1]
                    .split("### 2.", 1)[0]
                )
                for marker in (
                    "trace_id: null",
                    "trace_export: not-configured",
                    "Application Insights",
                    "operations-checklist.txt",
                    disclaimer,
                ):
                    self.assertIn(marker, operations)

    def test_workflow_a_review_opens_the_actual_saved_file_not_the_example_name(self):
        for directory in ("docs", "docs/ko"):
            with self.subTest(directory=directory):
                review = (
                    (ROOT / directory / "labs/05-workflows.md")
                    .read_text()
                    .split('<a id="workflow-a-review"></a>', 1)[1]
                    .split('<a id="path-b"></a>', 1)[0]
                )
                self.assertIn("Saved JSON:", review)
                self.assertIn("workflow-review.txt", review)
                self.assertNotIn("outputs/workflow-a-sequential.json", review)

    def test_optional_evaluator_counts_follow_selection_without_ignoring_missing_results(self):
        for directory, count, unavailable, incomplete in (
            ("docs", "two or three evaluators", "TaskAdherence not available", "incomplete"),
            ("docs/ko", "평가자 2개 또는 3개", "TaskAdherence 사용 불가", "미완료"),
        ):
            with self.subTest(directory=directory):
                text = (ROOT / directory / "labs/07-evaluation.md").read_text()
                portal = next(
                    block
                    for block in re.findall(r"<details>.*?</details>", text, re.DOTALL)
                    if "Task-Adherence-Evaluator-(Preview)" in block
                )
                self.assertIn(count, portal)
                self.assertGreaterEqual(portal.count(unavailable), 2)
                self.assertIn(f"**{incomplete}**", portal)

    def test_iq_reference_reuses_core_outputs_and_requires_explicit_optional_preparation(self):
        for directory, optional, browser, new_experiment in (
            ("docs", "optional C", "Browser-only A", "separately approved new hybrid experiment"),
            ("docs/ko", "선택 C", "브라우저만 사용한 A", "별도로 승인한 새 hybrid 실험"),
        ):
            with self.subTest(directory=directory):
                reference = (
                    (ROOT / directory / "reference/iq-workbook.md")
                    .read_text()
                    .split("## 1.", 1)[1]
                    .split("## 2.", 1)[0]
                )
                self.assertEqual(DOCS.workshop_commands(reference), [])
                for marker in (
                    "../labs/06-knowledge.md#path-b",
                    "../labs/06-knowledge.md#d-",
                    "retrieve-iq.json",
                    "answer-iq.json",
                    optional,
                ):
                    self.assertIn(marker, reference)
                lab = (ROOT / directory / "labs/06-knowledge.md").read_text()
                chat_setup = lab.split('<a id="iq-chat-model"></a>', 1)[1].split("1. ", 1)[0]
                for marker in (browser, ".venv", "prefix"):
                    self.assertIn(marker, chat_setup)
                recovery = (ROOT / directory / "reference/troubleshooting.md").read_text()
                embedding = next(
                    row
                    for row in recovery.splitlines()
                    if row.startswith("|") and "WORKSHOP_EMBEDDING_API=account" in row
                )
                self.assertIn(new_experiment, embedding)

    def test_local_hosted_recipe_states_inference_cost_before_its_server_example(self):
        for directory, cost in (("docs", "inference cost approval"), ("docs/ko", "추론 비용 승인")):
            with self.subTest(directory=directory):
                text = (ROOT / directory / "labs/08-hosted.md").read_text()
                recipe = next(
                    block
                    for block in re.findall(r"<details>.*?</details>", text, re.DOTALL)
                    if "examples/recipes/08_hosted_agent.py" in block
                )
                before_code = recipe.split("```python", 1)[0]
                for marker in (cost, "Hosted SDK", "Lab 02", "(09-operations.md#path-b)"):
                    self.assertIn(marker, before_code)

    def test_insights_requires_scan_approval_and_distinguishes_empty_from_incomplete(self):
        for directory, approval, incomplete in (
            ("docs", "approval for one scan's judge cost", "review incomplete"),
            ("docs/ko", "scan 1회의 judge 비용 승인", "검토 미완료"),
        ):
            with self.subTest(directory=directory):
                text = (ROOT / directory / "labs/extensions/agent-insights.md").read_text()
                self.assertIn(approval, text.split("**Run scan now**", 1)[0])
                scan = text.split("**Run scan now**", 1)[1].split("## 3.", 1)[0]
                for marker in (
                    "scan completed; no insights returned",
                    "insights-review.txt",
                    "(#insights-cleanup)",
                    incomplete,
                ):
                    self.assertIn(marker, scan)
                self.assertIn('<a id="insights-cleanup"></a>', text)

    def test_standalone_c_handoff_is_linked_without_new_evaluation_commands(self):
        for directory, incomplete in (("docs", "incomplete"), ("docs/ko", "미완료")):
            with self.subTest(directory=directory):
                catalog = (ROOT / directory / "paths/c-advanced.md").read_text()
                self.assertIn("(../labs/11-capstone.md#path-c)", catalog)
                text = (ROOT / directory / "labs/11-capstone.md").read_text()
                self.assertIn("(#path-c)", text.split("## ", 1)[0])
                handoff = text.split('<a id="path-c"></a>', 1)[1].split(
                    '<a id="hosted-acceptance"></a>', 1
                )[0]
                for marker in (
                    "session-notes.txt",
                    "(../reference/cleanup.md)",
                    "(#hosted-acceptance)",
                    f"**{incomplete}**",
                ):
                    self.assertIn(marker, handoff)
                self.assertEqual(DOCS.workshop_commands(handoff), [])
                self.assertNotIn("--unlock-holdout", handoff)

    def test_fixture_and_live_evaluation_reentry_have_separate_destinations(self):
        for directory in ("docs", "docs/ko"):
            with self.subTest(directory=directory):
                rows = (ROOT / directory / "paths.md").read_text().splitlines()
                fixture = next(row for row in rows if "labs/00-start.md#offline-fixtures" in row)
                real = next(row for row in rows if "labs/07-evaluation.md#resume-evaluation" in row)
                self.assertIn("fixture", fixture)
                self.assertNotIn("07-evaluation.md", fixture)
                self.assertNotIn("#offline-fixtures", real)
                self.assertNotEqual(fixture, real)

    def test_hosted_comparison_and_final_handoff_name_the_actual_artifacts_and_fields(self):
        for directory in ("docs", "docs/ko"):
            with self.subTest(directory=directory):
                workbook = (ROOT / directory / "reference/evaluation-workbook.md").read_text()
                comparison = workbook.split(
                    "benchmark compare --baseline wf-baseline --candidate wf-candidate", 1
                )[1].split("benchmark evaluate --label wf-candidate", 1)[0]
                for marker in (
                    "outputs/benchmarks/wf-candidate/comparison-wf-baseline.json",
                    "changed_context_rows: []",
                    "isolated_prompt_comparison: true",
                    "`false`",
                    "session-notes.txt",
                ):
                    self.assertIn(marker, comparison)
                capstone = (ROOT / directory / "labs/11-capstone.md").read_text()
                for text in (workbook, capstone):
                    for marker in (
                        "outputs/benchmarks/wf-final/release-verification.json",
                        "`gate_passed`",
                        "`native_quality_passed`",
                        "`recommendation`",
                        "`deployment_approved: false`",
                    ):
                        self.assertIn(marker, text)
                report = "outputs/benchmarks/wf-final/release-verification.json"
                hosted = capstone.split('<a id="hosted-acceptance"></a>', 1)[1]
                self.assertLess(hosted.index(report), hosted.index("benchmark verify"))

    def test_local_only_cleanup_exits_before_remote_commands_without_ignoring_failed_deploys(self):
        for directory, markers in (
            ("docs", ("**Local-only:**", "**not run**", "attempted", "failed deployment")),
            ("docs/ko", ("**로컬만 실행한 경우:**", "**미실행**", "시도", "배포 실패")),
        ):
            with self.subTest(directory=directory):
                text = (ROOT / directory / "reference/cleanup.md").read_text()
                before_commands = text.split('<a id="hosted-sessions"></a>', 1)[1].split(
                    "```bash", 1
                )[0]
                for marker in markers:
                    self.assertIn(marker, before_commands)
                self.assertIn("Ctrl+C", before_commands)

    def test_optimizer_missing_raw_judge_inputs_cannot_become_a_completed_review(self):
        for directory, no_promotion in (
            ("docs", "**do not promote**"),
            ("docs/ko", "**승격하지 않습니다**"),
        ):
            with self.subTest(directory=directory):
                text = (ROOT / directory / "labs/extensions/agent-optimizer.md").read_text()
                review = text.split("`sample.input`", 1)[1].split("## 6.", 1)[0]
                self.assertIn("`judge inputs unavailable / review incomplete`", review)
                self.assertIn("`optimizer-review.txt`", review)
                self.assertIn(no_promotion, review)

    def test_optional_hybrid_and_iq_commands_save_distinct_results(self):
        expected = {
            ("retrieve", "hybrid"): "retrieve-hybrid.json",
            ("answer", "hybrid"): "answer-hybrid.json",
            ("workflow-agent", "iq"): "workflow-iq.json",
        }
        command_parser = DOCS.parser()
        for language, directory in (("en", "docs"), ("ko", "docs/ko")):
            with self.subTest(language=language):
                text = (ROOT / directory / "labs/06-knowledge.md").read_text()
                found = {}
                for _, arguments in DOCS.workshop_commands(text):
                    args = command_parser.parse_args(arguments)
                    key = (
                        args.command,
                        getattr(args, "provider", getattr(args, "retrieval", None)),
                    )
                    if key in expected:
                        self.assertNotIn(key, found)
                        found[key] = args.output
                self.assertEqual(
                    found,
                    {
                        key: Path(f"outputs/learner-notes-{language}/{name}")
                        for key, name in expected.items()
                    },
                )

    def test_hosted_monitor_reentry_does_not_regenerate_a_verified_query(self):
        for directory in ("docs", "docs/ko"):
            with self.subTest(directory=directory):
                text = (ROOT / directory / "labs/09-operations.md").read_text()
                operations = [
                    args[args.index("benchmark") + 1]
                    for _, args in DOCS.workshop_commands(text)
                    if "benchmark" in args
                ]
                self.assertNotIn("trace-plan", operations)
                self.assertEqual(operations.count("monitor"), 1)
                self.assertLess(operations.index("monitor"), operations.index("stop-session"))
                for marker in (
                    "trace-query.kql",
                    "trace-verification.json",
                    "query hash",
                    "cached_verified_evidence: true",
                ):
                    self.assertIn(marker, text)

    def test_iq_chat_handoff_uses_a_shared_worksheet_field(self):
        for language, directory, heading, field in (
            ("en", "docs", "**Return:**", "Optional IQ Chat selected or not selected:"),
            ("ko", "docs/ko", "**복귀:**", "선택 IQ Chat의 선택 또는 미선택:"),
        ):
            with self.subTest(language=language):
                notes = (ROOT / "data/learner" / language / "session-notes.txt").read_text()
                shared = notes.split("\nA -", 1)[0]
                self.assertIn(field, shared)
                text = (ROOT / directory / "labs/06-knowledge.md").read_text()
                handoff = text.split(heading, 1)[1].split("</details>", 1)[0]
                self.assertIn(f"`{field}`", handoff)
                self.assertIn("label", handoff)

    def test_evaluation_resume_reuses_review_and_code_changes_need_a_new_dev_pair(self):
        for directory, pair, approval, holdout in (
            ("docs", "new dev baseline/candidate pair", "cost approval", "Keep holdout closed"),
            ("docs/ko", "새 dev baseline/candidate 쌍", "비용 승인", "Holdout은 열지 않습니다"),
        ):
            with self.subTest(directory=directory):
                text = (ROOT / directory / "labs/07-evaluation.md").read_text()
                resume = text.split('<a id="resume-evaluation"></a>', 1)[1].split(
                    '<a id="dev-baseline"></a>', 1
                )[0]
                self.assertIn("`review-*.json`", resume)
                candidate = text.split('<a id="dev-candidate"></a>', 1)[1].split(
                    "collect --split dev --label candidate", 1
                )[0]
                for marker in (pair, approval, holdout):
                    self.assertIn(marker, candidate)

    def test_creation_and_optimizer_review_prerequisites_precede_paid_actions(self):
        for directory, button, authorization in (
            ("docs", "**Create agent and open playground**", "owner's authorization"),
            ("docs/ko", "**에이전트 만들기 및 플레이그라운드 열기**", "담당자 승인"),
        ):
            with self.subTest(directory=directory):
                agent = (ROOT / directory / "labs/03-prompt-agent.md").read_text()
                before_create = agent.split(button, 1)[0]
                self.assertIn("`text-embedding-3-large`", before_create)
                self.assertIn(authorization, before_create)
                optimizer = (ROOT / directory / "labs/extensions/agent-optimizer.md").read_text()
                prerequisites = optimizer.split("## 2.", 1)[0]
                for marker in (
                    "`sample.input`",
                    "evaluation ID",
                    "raw-input review unavailable",
                    "`optimizer-review.txt`",
                ):
                    self.assertIn(marker, prerequisites)

    def test_conversation_evaluation_names_status_files_and_both_result_denominators(self):
        for directory, turn_rows, conversation_rows in (
            ("docs", "**six**", "**two**"),
            ("docs/ko", "**6행**", "**2행**"),
        ):
            with self.subTest(directory=directory):
                text = (ROOT / directory / "labs/extensions/conversation-evaluation.md").read_text()
                turn = text.split("## 4.", 1)[1].split("## 5.", 1)[0]
                before_request = turn.split("conversations evaluate", 1)[0]
                for marker in (
                    "groundedness",
                    "coherence",
                    "300",
                    "native-<level>/cloud-evaluation.json",
                    "status: completed",
                    "validation_status: valid",
                ):
                    self.assertIn(marker, before_request)
                self.assertIn("native-turn/cloud-evaluation-results.json", turn)
                self.assertIn(turn_rows, turn)
                conversation = text.split("## 5.", 1)[1].split("## 6.", 1)[0]
                self.assertIn("native-conversation/cloud-evaluation-results.json", conversation)
                self.assertIn(conversation_rows, conversation)

    def test_matrix_recovery_never_recollects_an_exposed_holdout(self):
        for directory, prefix, dev_only, no_recollection in (
            ("docs", "| Matrix rows", "**Dev only:**", "do not recollect"),
            ("docs/ko", "| matrix 행", "**Dev만:**", "재수집하지 말고"),
        ):
            with self.subTest(directory=directory):
                text = (ROOT / directory / "reference/troubleshooting.md").read_text()
                row = next(line for line in text.splitlines() if line.startswith(prefix))
                for marker in (dev_only, "holdout", no_recollection, "endpoint", "provider"):
                    self.assertIn(marker, row)

    def test_optional_hosting_has_a_local_exit_and_failed_verification_evidence_path(self):
        for directory, local_only, not_run in (
            ("docs", "**Local-only:**", "**not run**"),
            ("docs/ko", "**로컬만 실행한 경우:**", "**미실행**"),
        ):
            with self.subTest(directory=directory):
                hosted = (ROOT / directory / "labs/08-hosted.md").read_text()
                handoff = hosted.split("## 5.", 1)[1].split("</details>", 1)[0]
                for marker in (
                    local_only,
                    not_run,
                    "`session-notes.txt`",
                    "(09-operations.md#path-b)",
                ):
                    self.assertIn(marker, handoff)
                toolbox = (ROOT / directory / "labs/extensions/toolbox-hosted.md").read_text()
                cleanup = toolbox.split("## 6.", 1)[1]
                for marker in (
                    "`remote_evidence_directory`",
                    "`workshop-evidence/toolbox-runs/`",
                    "`failure.json`",
                    "stopped/idle",
                ):
                    self.assertIn(marker, cleanup)

    def test_extension_inspection_paths_and_synthetic_policy_input_are_explicit(self):
        for language, directory in (("en", "docs"), ("ko", "docs/ko")):
            with self.subTest(language=language):
                extensions = ROOT / directory / "labs/extensions"
                routine = (extensions / "routines.md").read_text()
                for marker in (
                    "outputs/routine-inspections/<label>/",
                    "`routine.json`",
                    "`runs.json`",
                    "`summary.json`",
                    "`manual_delivery_verified: true`",
                ):
                    self.assertIn(marker, routine)
                memory = (extensions / "memory.md").read_text()
                for marker in (
                    "`memory inspect`",
                    "`scope`",
                    "`alpha`/`beta`",
                    "`memory-alpha-02`",
                    "`outputs/memory-runs/<new-label>/`",
                ):
                    self.assertIn(marker, memory)
                policy = "policies/RECEIPT-01.txt"
                self.assertIn(f"`{policy}`", (extensions / "specialist-scope.md").read_text())
                self.assertTrue((ROOT / "data/learner" / language / policy).is_file())

    def test_english_cli_examples_explicitly_select_the_english_bundle(self):
        for english, _ in DOCS.translation_pairs(ROOT):
            for line, arguments in DOCS.workshop_commands(english.read_text()):
                with self.subTest(page=english.relative_to(ROOT), command=line):
                    self.assertIn("--language", arguments)
                    self.assertEqual(arguments[arguments.index("--language") + 1], "en")

    def test_completed_pairs_in_the_active_revision_retain_exact_file_hashes(self):
        state = json.loads((ROOT / "docs/localization.json").read_text())
        pairs = {
            english.relative_to(ROOT).as_posix(): (english, korean)
            for english, korean in DOCS.translation_pairs(ROOT)
        }
        for name, record in state.get("completed_translations", {}).items():
            if record["revision"] != state["revision"] or name in state["pending_files"]:
                continue
            with self.subTest(pair=name):
                english, korean = pairs[name]
                self.assertEqual(
                    record["english_sha256_at_completion"],
                    hashlib.sha256(english.read_bytes()).hexdigest(),
                )
                self.assertEqual(
                    record["korean_sha256_at_completion"],
                    hashlib.sha256(korean.read_bytes()).hexdigest(),
                )
                self.assertIs(record["cli_parity_verified"], True)

    def test_english_first_revision_warns_korean_readers_and_pins_both_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            english, korean = root / "README.md", root / "README.ko.md"
            english.write_text("# Current guide\n\n**English** | [한국어](README.ko.md)\n")
            korean.write_text(
                "# 가이드\n\n[English](README.md) | **한국어**\n\n"
                "<!-- translation-pending: english-first -->\n\n"
                "> **번역 준비 중** — 영어 실행·촬영·보완 후 한국어를 갱신합니다.\n"
            )
            (root / "docs/localization.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "source_language": "en",
                        "revision": "english-first",
                        "pending_files": {
                            "README.md": {
                                "english_sha256": hashlib.sha256(english.read_bytes()).hexdigest(),
                                "korean_sha256": hashlib.sha256(korean.read_bytes()).hexdigest(),
                            }
                        },
                    }
                )
            )
            failures = []
            self.assertEqual(DOCS.pending_translations(root, failures), {english})
            self.assertEqual(failures, [])
            english.write_text(english.read_text() + "\nA new command.\n")
            failures = []
            self.assertEqual(DOCS.pending_translations(root, failures), set())
            self.assertTrue(any("hashes changed" in failure for failure in failures))

    def test_github_heading_ids_handle_both_languages_formatting_and_duplicates(self):
        headings = DOCS.heading_ids(
            "# English **guide**\n## [Linked](other.md) `code`\n"
            "## 이 가이드의 화면 읽는 법\n## Repeat\n## Repeat\n"
            "```text\n## Not a heading\n```\n"
            '<a id="stable-anchor"></a>\n'
        )
        self.assertEqual(
            headings,
            {
                "english-guide",
                "linked-code",
                "이-가이드의-화면-읽는-법",
                "repeat",
                "repeat-1",
                "stable-anchor",
            },
        )

    def test_command_parity_keeps_canonical_questions_and_joined_lines(self):
        commands = DOCS.workshop_commands(
            'python scripts/workshop.py model \\\n  --question "한국어 질문" | tee output.json\n'
        )
        self.assertEqual(commands[0][1], ["model", "--question", "한국어 질문"])
        with self.assertRaises(ValueError):
            DOCS.workshop_commands('python scripts/workshop.py model --question "unclosed')

    def test_language_parity_only_normalizes_explicit_translations(self):
        mapping = {"Approved English question": "승인된 한국어 질문"}
        english = [
            "--language",
            "en",
            "answer",
            "--question",
            "Approved English question",
            "--retrieval",
            "iq",
        ]
        korean = ["answer", "--question", "승인된 한국어 질문", "--retrieval", "iq"]
        self.assertEqual(DOCS.normalized_command(english, mapping), korean)
        changed = [*english[:-1], "local"]
        self.assertNotEqual(DOCS.normalized_command(changed, mapping), korean)
        unknown = [
            "--language",
            "en",
            "answer",
            "--question",
            "Unreviewed question",
            "--retrieval",
            "iq",
        ]
        self.assertNotEqual(DOCS.normalized_command(unknown, mapping), korean)

    def test_language_pair_discovery_keeps_orphans_visible(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs/ko/labs").mkdir(parents=True)
            (root / "docs/labs").mkdir()
            (root / "docs/labs/00-start.md").touch()
            (root / "docs/ko/labs/01-foundry.md").touch()
            pairs = DOCS.translation_pairs(root)
            self.assertIn(
                (root / "docs/labs/00-start.md", root / "docs/ko/labs/00-start.md"), pairs
            )
            self.assertIn(
                (root / "docs/labs/01-foundry.md", root / "docs/ko/labs/01-foundry.md"), pairs
            )

    def test_azd_examples_are_checked_against_the_recorded_help_surface(self):
        commands = {"ai agent invoke": ["--cwd", "--help", "--version"], "deploy": ["--cwd"]}
        text = (
            "```bash\n"
            'AZURE_DEV_USER_AGENT=x azd ai agent invoke --cwd "${DIR:?}" \\\n  --version 1\n'
            'azd deploy "$NAME" --cwd "$DIR" && azd ai agent invoke --bogus\n'
            "azd ai agent vanish\n"
            "```\n"
            "Prose mentioning azd deploy --nope is not a command.\n"
        )
        segments = DOCS.azd_segments(text)
        self.assertEqual(len(segments), 4)
        errors = [error for segment in segments for error in DOCS.azd_errors(segment, commands)]
        self.assertEqual(len(errors), 2)
        self.assertIn("unknown azd flag --bogus", errors[0])
        self.assertIn("unknown azd command", errors[1])
        self.assertEqual(
            DOCS.azd_command_paths(text), {"ai agent invoke", "deploy", "ai agent vanish"}
        )

    def test_recorded_azd_surface_is_dated_and_covers_every_guide_command(self):
        surface = json.loads((ROOT / "scripts/azd-surface.json").read_text())
        self.assertRegex(surface["recorded_at"], r"^\d{4}-\d{2}-\d{2}$")
        self.assertTrue(surface["azd_version"])
        paths = set()
        for path in DOCS.markdown_files(ROOT):
            paths |= DOCS.azd_command_paths(path.read_text(encoding="utf-8"))
        self.assertTrue(paths)
        self.assertLessEqual(paths, set(surface["commands"]))
        for flags in surface["commands"].values():
            self.assertNotIn("--cask", flags)
