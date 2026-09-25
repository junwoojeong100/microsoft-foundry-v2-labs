import hashlib
import struct
import unittest

from foundry_workshop.contracts import read_json

from . import ROOT

DIRECTORY = ROOT / "docs/assets/e2e-check-20260925"
GUIDES = {"en": "docs/labs/03-prompt-agent.md", "ko": "docs/ko/labs/03-prompt-agent.md"}
BUTTONS = {"en": "Create agent and open playground", "ko": "에이전트 만들기 및 플레이그라운드 열기"}
DEFAULTS = {"en": "Text", "ko": "텍스트"}


class EndToEndCheckMediaTests(unittest.TestCase):
    """2026-09-25 portal screens that replaced a changed Lab 03 A dialog."""

    @classmethod
    def setUpClass(cls):
        cls.evidence = read_json(DIRECTORY / "captures.json")

    def test_capture_scope_is_explicit(self):
        value = self.evidence
        self.assertEqual(value["schema_version"], 1)
        self.assertEqual(value["captured_on"], "2026-09-25")
        for flag in ("image_edited", "page_dom_modified_for_capture", "authentication_captured"):
            self.assertIs(value[flag], False, flag)
        self.assertIs(value["captured_before_create"], True)
        self.assertEqual(value["resource_writes_in_capture"], 0)
        self.assertEqual(value["model_invocations_in_capture"], 0)
        self.assertEqual(set(value["languages"]), {"en", "ko"})

    def test_images_are_lossless_hash_bound_and_record_the_new_dialog(self):
        images = self.evidence["images"]
        self.assertEqual([item["guide_language"] for item in images], ["en", "ko"])
        for item in images:
            language = item["guide_language"]
            with self.subTest(language=language):
                self.assertEqual(item["scenario_language"], language)
                self.assertIs(item["pixel_exact"], True)
                self.assertEqual(item["checks"]["create_button"], BUTTONS[language])
                self.assertEqual(item["checks"]["default_interaction_mode"], DEFAULTS[language])
                path = DIRECTORY / item["file"]
                self.assertFalse(path.is_symlink())
                content = path.read_bytes()
                self.assertEqual(len(content), item["bytes"])
                self.assertEqual(hashlib.sha256(content).hexdigest(), item["sha256"])
                self.assertEqual(content[:4] + content[8:12], b"RIFFWEBP")
                self.assertEqual(content[12:16], b"VP8L")
                bits = struct.unpack("<I", content[21:25])[0]
                self.assertEqual(
                    ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1),
                    (item["width"], item["height"]),
                )

    def test_guides_show_the_dialog_they_describe(self):
        for item in self.evidence["images"]:
            language = item["guide_language"]
            other = "ko" if language == "en" else "en"
            reference = f"/e2e-check-20260925/{item['file']}"
            with self.subTest(language=language):
                text = (ROOT / GUIDES[language]).read_text()
                self.assertEqual(text.count(reference), 1)
                self.assertIn(BUTTONS[language], text)
                self.assertNotIn(reference, (ROOT / GUIDES[other]).read_text())


if __name__ == "__main__":
    unittest.main()
