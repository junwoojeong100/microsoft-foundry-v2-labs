import json
import unittest

from . import ROOT

ASSETS = ROOT / "docs/assets/live-20260913-swc"


class VideoLinkTests(unittest.TestCase):
    def test_live_guides_embed_the_verified_recording_attachments(self):
        uploads = json.loads((ASSETS / "github-playback.json").read_text())
        media = json.loads((ASSETS / "media.json").read_text())
        active = {item["filename"]: item for item in media["videos"]}
        self.assertEqual(uploads["repository"], "junwoojeong100/microsoft-foundry-v2-labs")
        self.assertTrue(uploads["private_repository"])
        self.assertTrue(uploads["edited_recordings_published"])
        self.assertEqual(len(uploads["videos"]), 2)
        for item in uploads["videos"]:
            original = active[item["filename"]]
            self.assertEqual(item["source_sha256"], original["sha256"])
            self.assertEqual(item["bytes"], original["bytes"])
            self.assertRegex(
                item["url"], r"^https://github\.com/user-attachments/assets/[0-9a-f-]+$"
            )
            for document in ("live-run.md", "video-summary.md"):
                text = (ROOT / "docs" / document).read_text()
                self.assertIn(item["url"], text.splitlines())
                self.assertNotIn("private-user-images.githubusercontent.com", text)
                if document == "video-summary.md":
                    self.assertEqual(text.count(item["url"]), 1)

    def test_edits_preserve_source_order_and_declared_frame_counts(self):
        timeline = json.loads((ASSETS / "edit-timeline.json").read_text())
        self.assertTrue(timeline["waiting_time_removed"])
        self.assertFalse(timeline["new_recording"])
        self.assertEqual(timeline["playback_speed"], 1)
        media = {
            item["filename"]: item
            for item in json.loads((ASSETS / "media.json").read_text())["videos"]
        }
        for video in timeline["videos"]:
            previous = -1
            frames = 0
            for segment in video["segments"]:
                self.assertGreater(segment["first_frame"], previous)
                self.assertGreaterEqual(segment["last_frame"], segment["first_frame"])
                frames += segment["last_frame"] - segment["first_frame"] + 1
                previous = segment["last_frame"]
            self.assertEqual(frames, video["expected_frames"])
            self.assertAlmostEqual(
                frames / video["fps"], media[video["filename"]]["duration_seconds"], places=3
            )
            self.assertLess(
                media[video["filename"]]["duration_seconds"],
                media[video["filename"]]["source_duration_seconds"] * 0.2,
            )
            self.assertGreaterEqual(
                video["source_frame_verification"]["minimum_source_frame_ssim"], 0.95
            )

    def test_all_cli_results_and_verified_portal_screens_are_retained(self):
        videos = json.loads((ASSETS / "edit-timeline.json").read_text())["videos"]
        cli = next(item for item in videos if item["filename"].startswith("cli-"))
        stages = {
            reason["stage"]
            for segment in cli["segments"]
            for reason in segment["reasons"]
            if reason["kind"] == "result"
        }
        self.assertEqual(len(stages), 72)
        self.assertEqual(cli["retained_stage_count"], 72)
        self.assertIn("055-native-luna-judge", stages)
        self.assertIn("076-hosted-monitor", stages)
        portal = next(item for item in videos if item["filename"].startswith("portal-"))
        self.assertEqual(len(portal["retained_verified_screens"]), 17)
        self.assertIn("P12-native-evaluation-report.png", portal["retained_verified_screens"])

    def test_originals_remain_identifiable_without_duplicate_large_files(self):
        media = json.loads((ASSETS / "media.json").read_text())
        self.assertEqual(len(media["original_recordings"]), 2)
        for original in media["original_recordings"]:
            self.assertRegex(original["sha256"], r"^[0-9a-f]{64}$")
            self.assertTrue(
                original["github_url"].startswith("https://github.com/user-attachments/assets/")
            )
            self.assertFalse((ASSETS / original["filename"]).exists())
        self.assertEqual(len(media["images"]), media["screenshot_count"])
        self.assertEqual(
            {item["filename"] for item in media["images"]},
            {path.name for path in ASSETS.glob("*.png")},
        )
