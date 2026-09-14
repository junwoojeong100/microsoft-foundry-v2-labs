import tempfile
import unittest
from pathlib import Path

from . import ROOT
from .test_packaging import load_script

DOCS = load_script("check_docs")


class DocumentationTests(unittest.TestCase):
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
