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
