import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from . import ROOT
from .test_packaging import load_script

DOCS = load_script("check_docs")


class DocumentationTests(unittest.TestCase):
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
        failures, counts = DOCS.check(ROOT)
        self.assertEqual(failures, [])
        self.assertGreaterEqual(counts["language_pairs"], 31)
        self.assertGreaterEqual(counts["cli_examples"], 108)
        self.assertGreater(counts["local_anchors"], 0)

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
