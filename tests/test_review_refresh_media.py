import hashlib
import re
import struct
import unittest
from datetime import datetime

from foundry_workshop.contracts import read_json

from . import ROOT

DIRECTORY = ROOT / "docs/assets/review-refresh-20260925"
GUIDES = {
    "en": ("docs/labs/03-prompt-agent.md", "docs/labs/09-operations.md"),
    "ko": ("docs/ko/labs/03-prompt-agent.md", "docs/ko/labs/09-operations.md"),
}
TERMINAL = ("03-201-sdk-create", "03-202-sdk-invoke")
PORTAL = ("P03-201-playground", "P03-202-details", "P09-201-trace-search", "P09-202-trace-detail")


def guide_blocks(path):
    text = (ROOT / path).read_text()
    section = text[text.index('<a id="path-b"></a>') :]
    return re.findall(r"```bash\n(.*?)\n```", section[: section.index("\n### 3.")], re.S)


class ReviewRefreshSupplementTests(unittest.TestCase):
    """2026-09-25 screenshots and clips of the steps added by the 2026-09-24 review refresh."""

    @classmethod
    def setUpClass(cls):
        cls.evidence = read_json(DIRECTORY / "captures.json")

    def test_capture_scope_and_side_effects_are_explicit(self):
        value = self.evidence
        self.assertEqual(value["schema_version"], 1)
        self.assertEqual(value["captured_on"], "2026-09-25")
        self.assertEqual(
            value["deployment"],
            {"name": "gpt-6-sol", "model": "gpt-6-sol", "version": "2026-09-22"},
        )
        for flag in (
            "image_edited",
            "page_dom_modified_for_capture",
            "authentication_captured",
            "role_assignments_changed",
            "model_deployments_changed",
            "default_subscription_changed",
            "connections_changed",
            "new_evaluation_results",
        ):
            self.assertIs(value[flag], False, flag)
        self.assertEqual(value["portal_chat_messages_sent"], 0)
        self.assertEqual(value["resource_writes"], 2)
        self.assertEqual(value["model_invocations"], 2)
        (discarded,) = value["discarded_attempts"]
        self.assertIs(discarded["published"], False)
        self.assertTrue(discarded["reason"])
        typed = [
            answer["text"]
            for item in value["images"]
            for answer in item.get("interactive_inputs", [])
        ]
        self.assertNotIn(discarded["agent"], typed)
        self.assertNotIn(
            discarded["agent"], {item["agent"] for item in value["languages"].values()}
        )

    def test_each_language_has_its_own_agent_response_and_trace(self):
        languages = self.evidence["languages"]
        self.assertEqual(set(languages), {"en", "ko"})
        for language, item in languages.items():
            with self.subTest(language=language):
                self.assertEqual(item["agent"], f"mfv2-sup-20260925-{language}-policy-sdk")
                self.assertEqual(item["agent_version"], "1")
                self.assertRegex(item["response_id"], r"^resp_[0-9a-f]+$")
                self.assertRegex(item["server_trace"]["operation_id"], r"^[0-9a-f]{32}$")
                self.assertEqual(
                    item["server_trace"]["spans"],
                    [f"invoke_agent {item['agent']}:1", "chat gpt-6-sol-2026-09-22"],
                )
                self.assertEqual(item["response_model"], "gpt-6-sol")
                self.assertEqual(item["answer"]["limit_krw"], 150000)
                self.assertIn("TRAVEL-2026", item["answer"]["citations"])
                self.assertEqual(item["trace_export_in_cli_output"], "not-configured")
                self.assertRegex(item["source_commit"], r"^[0-9a-f]{40}$")
        self.assertNotEqual(languages["en"]["response_id"], languages["ko"]["response_id"])

    def test_images_are_lossless_hash_bound_and_complete(self):
        images = self.evidence["images"]
        self.assertEqual(len({item["sha256"] for item in images}), len(images))
        for language in ("en", "ko"):
            letter = "E" if language == "en" else "K"
            expected = [letter + name for name in TERMINAL] + [letter + name for name in PORTAL]
            own = [item for item in images if item["guide_language"] == language]
            self.assertEqual([item["action_id"] for item in own], expected)
            stamps = [datetime.fromisoformat(item["observed_at"]) for item in own]
            self.assertEqual(stamps, sorted(stamps))
            for item in own:
                with self.subTest(file=item["file"]):
                    self.assertEqual(item["file"], f"{item['action_id']}.webp")
                    self.assertEqual(item["scenario_language"], language)
                    self.assertIs(item["pixel_exact"], True)
                    self.assertRegex(item["source_png_sha256"], "^[0-9a-f]{64}$")
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

    def test_terminal_captures_used_the_current_guide_blocks(self):
        for item in self.evidence["images"]:
            if item["channel"] != "terminal":
                continue
            with self.subTest(file=item["file"]):
                blocks = guide_blocks(GUIDES[item["guide_language"]][0])
                self.assertIn(item["recorded_command"], blocks)
                self.assertIs(item["command_matches_guide_block"], True)
                self.assertEqual(item["exit_code"], 0)
                self.assertEqual(item["mode"], "LIVE AZURE")
                (answer,) = item["interactive_inputs"]
                self.assertIn(answer["after"].strip(), item["recorded_command"])

    def test_portal_captures_record_read_only_checks(self):
        for item in self.evidence["images"]:
            if item["channel"] != "portal":
                continue
            checks = item["checks"]
            with self.subTest(file=item["file"]):
                self.assertEqual(item["mode"], "READ-ONLY PORTAL")
                self.assertEqual(item["portal_display_language"], item["guide_language"])
                if item["action_id"].endswith("P03-201-playground"):
                    self.assertIs(checks["instructions_equal_cli_definition"], True)
                    self.assertIs(checks["chat_message_sent"], False)
                elif item["action_id"].endswith("P03-202-details"):
                    self.assertRegex(checks["active_version_text"], r"\((Version|버전) 1\)")
                    self.assertIs(checks["responses_endpoint_visible"], True)
                elif item["action_id"].endswith("P09-201-trace-search"):
                    self.assertEqual(checks["rows"], 1)
                    self.assertIs(checks["matches_app_insights_operation"], True)
                else:
                    self.assertIs(checks["invoke_agent_span"], True)
                    self.assertIs(checks["chat_span"], True)

    def test_clips_are_real_time_and_hash_bound(self):
        videos = self.evidence["videos"]
        self.assertEqual(
            [item["file"] for item in videos],
            ["en-terminal.mp4", "en-portal.mp4", "ko-terminal.mp4", "ko-portal.mp4"],
        )
        for item in videos:
            with self.subTest(file=item["file"]):
                self.assertEqual(item["playback_speed"], 1)
                self.assertIs(item["full_decode_verified"], True)
                self.assertEqual(item["codec"], "h264")
                self.assertEqual(item["fps"], "25/1")
                self.assertAlmostEqual(item["frames"] / 25, item["duration_seconds"], delta=0.05)
                self.assertLessEqual(item["duration_seconds"], item["source_duration_seconds"])
                self.assertRegex(item["source_webm_sha256"], "^[0-9a-f]{64}$")
                if item["channel"] == "portal":
                    self.assertIsNone(item["source_trim_seconds"])
                offsets = list(item["action_offsets_seconds"].values())
                self.assertEqual(offsets, sorted(offsets))
                self.assertTrue(all(0 <= value < item["duration_seconds"] for value in offsets))
                path = DIRECTORY / item["file"]
                self.assertFalse(path.is_symlink())
                content = path.read_bytes()
                self.assertEqual(len(content), item["bytes"])
                self.assertEqual(hashlib.sha256(content).hexdigest(), item["sha256"])
                self.assertEqual(content[4:8], b"ftyp")

    def test_guides_place_each_image_once_in_its_own_language(self):
        for item in self.evidence["images"]:
            language = item["guide_language"]
            other = "ko" if language == "en" else "en"
            reference = f"/review-refresh-20260925/{item['file']}"
            guide = GUIDES[language][0 if "03-" in item["action_id"] else 1]
            with self.subTest(file=item["file"]):
                self.assertEqual((ROOT / guide).read_text().count(reference), 1)
                for path in GUIDES[other]:
                    self.assertNotIn(reference, (ROOT / path).read_text())

    def test_index_play_links_match_recorded_offsets(self):
        pages = {"en": ROOT / "docs/action-captures.md", "ko": ROOT / "docs/ko/action-captures.md"}
        for item in self.evidence["videos"]:
            if item["channel"] == "terminal":
                offsets = {
                    key: value
                    for key, value in item["action_offsets_seconds"].items()
                    if not key[1:].startswith("00-")
                }
            else:
                offsets = item["action_offsets_seconds"]
            text = pages[item["guide_language"]].read_text()
            for action, seconds in offsets.items():
                with self.subTest(action=action):
                    self.assertIn(f"| {action} |", text)
                    self.assertIn(f"{item['file']}#t={seconds:.2f})", text)


if __name__ == "__main__":
    unittest.main()
