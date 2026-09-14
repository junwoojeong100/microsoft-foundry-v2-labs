import hashlib
import json
import unittest

from . import ROOT

ASSETS = ROOT / "docs/assets/live-20260914-action"


class VideoLinkTests(unittest.TestCase):
    def test_new_recording_and_publication_status_are_honest(self):
        media = json.loads((ASSETS / "media.json").read_text())
        uploads = json.loads((ASSETS / "github-playback.json").read_text())
        self.assertEqual(media["recorded_on"], "2026-09-14")
        self.assertEqual(media["resource_group"], "rg-mfv2-action-swc-20260914")
        self.assertTrue(media["new_recording"])
        self.assertTrue(media["headless"])
        self.assertFalse(media["authentication_recorded"])
        self.assertFalse(media["historical_json_replay"])
        self.assertIn("Bash PTY", media["cli_surface"])
        self.assertEqual(uploads["repository"], "junwoojeong100/microsoft-foundry-v2-labs")
        self.assertTrue(uploads["private_repository"])
        active = {item["filename"]: item for item in media["videos"]}
        if uploads["edited_recordings_published"]:
            self.assertEqual(len(uploads["videos"]), 2)
            for item in uploads["videos"]:
                self.assertEqual(item["source_sha256"], active[item["filename"]]["sha256"])
                self.assertRegex(
                    item["url"], r"^https://github\.com/user-attachments/assets/[0-9a-f-]+$"
                )
                for document in ("live-run.md", "video-summary.md"):
                    self.assertIn(item["url"], (ROOT / "docs" / document).read_text().splitlines())
        else:
            self.assertEqual(uploads["status"], "not-published")
            self.assertEqual(uploads["videos"], [])
            for document in ("live-run.md", "video-summary.md"):
                text = (ROOT / "docs" / document).read_text()
                self.assertIn("아직", text)
                self.assertNotIn("github.com/user-attachments/assets/", text)
        for document in ("live-run.md", "video-summary.md"):
            self.assertNotIn(
                "private-user-images.githubusercontent.com",
                (ROOT / "docs" / document).read_text(),
            )

    def test_every_edit_preserves_source_order_frames_and_provenance(self):
        timeline = json.loads((ASSETS / "edit-timeline.json").read_text())
        media = {
            item["filename"]: item
            for item in json.loads((ASSETS / "media.json").read_text())["videos"]
        }
        sources = {item["id"]: item for item in timeline["sources"]}
        self.assertEqual(set(sources), {"cli-1", "cli-2", "local-server", "portal"})
        self.assertTrue(timeline["new_recording"])
        self.assertTrue(timeline["waiting_time_removed"])
        self.assertFalse(timeline["screenshot_slideshow"])
        self.assertEqual(timeline["playback_speed"], 1)
        for video in timeline["videos"]:
            previous = {}
            frames = 0
            for segment in video["segments"]:
                source = sources[segment["source_id"]]
                self.assertGreater(segment["first_frame"], previous.get(source["id"], -1))
                self.assertGreaterEqual(segment["last_frame"], segment["first_frame"])
                self.assertLess(segment["last_frame"], source["frames"])
                self.assertEqual(segment["output_first_frame"], frames)
                frames += segment["last_frame"] - segment["first_frame"] + 1
                self.assertEqual(segment["output_last_frame"], frames - 1)
                previous[source["id"]] = segment["last_frame"]
            self.assertEqual(frames, video["expected_frames"])
            self.assertAlmostEqual(
                frames / video["fps"], media[video["filename"]]["duration_seconds"], places=3
            )
            self.assertLess(
                media[video["filename"]]["duration_seconds"],
                media[video["filename"]]["source_duration_seconds"] * 0.25,
            )
            verification = video["source_frame_verification"]
            self.assertEqual(verification["checked_segments"], len(video["segments"]))
            self.assertEqual(
                {item["segment"] for item in verification["comparisons"]},
                set(range(len(video["segments"]))),
            )
            self.assertGreaterEqual(verification["minimum_source_frame_ssim"], 0.95)

    def test_all_declared_actions_have_capture_and_video_evidence(self):
        ledger = json.loads((ASSETS / "actions.json").read_text())
        media = json.loads((ASSETS / "media.json").read_text())
        actions = {item["id"]: item for item in ledger["actions"]}
        self.assertEqual(len(actions), len(ledger["actions"]))
        self.assertEqual(len(actions), media["action_count"])
        self.assertEqual(ledger["counts"], {"cli": 131, "portal": 105})
        required = {
            "01-008-create-group",
            "02-001-deploy-luna",
            "03-001-sdk-agent-create",
            "04-006-input-boundary-attempt-2",
            "P03-005-create-open-agent",
            "P03-013-save-evidence-version",
            "P03-F11-select-six-files",
            "P03-F14-inspect-index-files",
            "P07-001-d06-send",
            "07-010-native-judge",
            "08-027-run-hosted-eval",
            "P09-006-first-storage-miss",
            "P09-007-second-storage-miss",
            "09-033-sessions-after",
        }
        self.assertTrue(required <= actions.keys())
        self.assertEqual(actions["04-006-input-boundary-attempt-2"]["exit_code"], 2)
        images = {item["filename"] for item in media["images"]}
        for action in actions.values():
            self.assertTrue(action["video_intervals"])
            labels = {item["label"] for item in action["screenshots"]}
            self.assertIn("before", labels)
            self.assertTrue(labels & {"result", "ready", "failed", "timeout"})
            for screenshot in action["screenshots"]:
                self.assertIn(screenshot["image"], images)

    def test_current_tree_contains_only_verified_new_media(self):
        media = json.loads((ASSETS / "media.json").read_text())
        self.assertFalse((ROOT / "docs/assets/live-20260913-swc").exists())
        self.assertTrue(media["lossless_screenshots"])
        self.assertEqual(len(media["images"]), media["screenshot_count"])
        self.assertEqual(
            {item["filename"] for item in media["images"]},
            {path.relative_to(ASSETS).as_posix() for path in ASSETS.glob("shots/*.webp")},
        )
        for item in media["videos"] + media["images"]:
            path = ASSETS / item["filename"]
            self.assertEqual(path.stat().st_size, item["bytes"])
            with path.open("rb") as stream:
                self.assertEqual(hashlib.file_digest(stream, "sha256").hexdigest(), item["sha256"])
