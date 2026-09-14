import hashlib
import json
import re
import unittest

from . import ROOT

ASSETS = ROOT / "docs/assets/live-20260914-action"


class VideoLinkTests(unittest.TestCase):
    def test_merged_video_follows_guide_order_without_losing_input_frames_or_actions(self):
        timeline = json.loads((ASSETS / "combined-timeline.json").read_text())
        media = json.loads((ASSETS / "media.json").read_text())
        videos = {item["filename"]: item for item in media["videos"]}
        ledger = json.loads((ASSETS / "actions.json").read_text())["actions"]
        merged = videos["guide-walkthrough.mp4"]
        self.assertEqual(media["default_video"], merged["filename"])
        self.assertEqual([item["lab"] for item in timeline["chapters"]], list(range(12)))
        self.assertEqual(merged["chapters"], timeline["chapters"])
        self.assertFalse(timeline["new_azure_execution"])
        self.assertFalse(timeline["original_videos_modified"])
        self.assertEqual(timeline["playback_speed"], 1)
        self.assertTrue(timeline["full_decode_verified"])
        self.assertTrue(timeline["embedded_chapters_verified"])
        cursor = 0
        content_frames = 0
        cards = []
        footage = []
        for segment in timeline["segments"]:
            self.assertEqual(segment["output_first_frame"], cursor)
            cursor += segment["frames"]
            self.assertEqual(segment["output_last_frame"], cursor - 1)
            if segment["kind"] == "chapter-card":
                cards.append(segment["chapter"])
            else:
                footage.append(segment)
                content_frames += segment["frames"]
                self.assertEqual(
                    int(segment["action_id"].removeprefix("P").split("-", 1)[0]),
                    segment["chapter"],
                )
        self.assertEqual(cards, list(range(12)))
        self.assertEqual([s["chapter"] for s in footage], sorted(s["chapter"] for s in footage))
        self.assertEqual(cursor, timeline["expected_frames"])
        self.assertAlmostEqual(cursor / timeline["fps"], merged["duration_seconds"], places=3)
        self.assertEqual(content_frames, timeline["source_content_frames"])
        self.assertEqual(
            {segment["action_id"] for segment in footage}, {item["id"] for item in ledger}
        )
        for source in timeline["inputs"]:
            self.assertEqual(source["sha256"], videos[source["filename"]]["sha256"])
            ranges = sorted(
                (segment["input_first_frame"], segment["input_last_frame"])
                for segment in footage
                if segment["input_video"] == source["filename"]
            )
            position = 0
            for first, last in ranges:
                self.assertEqual(first, position)
                self.assertGreaterEqual(last, first)
                position = last + 1
            self.assertEqual(position, source["frames"])
        for action in ledger:
            self.assertTrue(action["combined_video_intervals"])
            start = next(
                item["start_seconds"]
                for item in action["combined_video_intervals"]
                if not item["context_only"]
            )
            self.assertEqual(action["combined_start_seconds"], start)
            for interval in action["combined_video_intervals"]:
                segment = timeline["segments"][interval["segment"]]
                self.assertEqual(segment["action_id"], action["id"])
                self.assertAlmostEqual(
                    interval["start_seconds"], segment["output_first_frame"] / timeline["fps"]
                )
        checks = timeline["frame_verification"]
        self.assertEqual(checks["checked_footage_segments"], len(footage))
        self.assertGreaterEqual(checks["minimum_ssim"], 0.95)

    def test_lab_images_are_current_captioned_and_placed_with_the_steps(self):
        media = json.loads((ASSETS / "media.json").read_text())
        known_images = {(ASSETS / item["filename"]).resolve() for item in media["images"]}
        minimums = {
            "00-start.md": 5,
            "01-foundry.md": 3,
            "02-models.md": 7,
            "03-prompt-agent.md": 12,
            "04-agents-tools.md": 4,
            "05-workflows.md": 5,
            "06-knowledge.md": 6,
            "07-evaluation.md": 7,
            "08-hosted.md": 7,
            "09-operations.md": 5,
            "10-iq-extensions.md": 1,
            "11-capstone.md": 1,
        }
        total = 0
        for directory, caption in (("docs", "**What to check:**"), ("docs/ko", "**화면 확인:**")):
            for filename, minimum in minimums.items():
                path = ROOT / directory / "labs" / filename
                text = path.read_text()
                images = list(re.finditer(r"!\[[^\]]+\]\(([^)\s]+)\)", text))
                with self.subTest(language=directory, lab=filename):
                    self.assertGreaterEqual(len(images), minimum)
                    for image in images:
                        self.assertIn((path.parent / image.group(1)).resolve(), known_images)
                        self.assertIn(caption, text[image.end() : image.end() + 350])
                    completion = re.search(
                        r"^## (?:완료|반드시 정리|Completion|Always finish)", text, re.MULTILINE
                    )
                    if completion:
                        self.assertGreaterEqual(
                            sum(image.start() < completion.start() for image in images),
                            max(1, minimum - 1),
                        )
                total += len(images)
        self.assertGreaterEqual(total, 140)

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
            self.assertEqual(uploads["status"], "published")
            self.assertEqual(uploads["recorded_on"], media["recorded_on"])
            self.assertEqual(uploads["repository_id"], 1367892793)
            self.assertFalse(uploads["signed_media_urls_saved"])
            self.assertEqual(len(uploads["videos"]), len(active))
            self.assertEqual(
                set(uploads.get("not_uploaded_videos", [])),
                set(active) - {item["filename"] for item in uploads["videos"]},
            )
            for item in uploads["videos"]:
                self.assertEqual(item["source_sha256"], active[item["filename"]]["sha256"])
                self.assertEqual(item["bytes"], active[item["filename"]]["bytes"])
                self.assertRegex(
                    item["url"], r"^https://github\.com/user-attachments/assets/[0-9a-f-]+$"
                )
                for directory in ("docs", "docs/ko"):
                    for document in ("live-run.md", "video-summary.md"):
                        lines = (ROOT / directory / document).read_text().splitlines()
                        self.assertEqual(lines.count(item["url"]), 1)
            summary = (ROOT / "docs/ko/video-summary.md").read_text()
            primary = summary.split("## 재생하기", 1)[1].split("## 선택:", 1)[0]
            self.assertNotIn("127.0.0.1", primary)
            self.assertNotIn("python scripts/play_recordings.py", primary)
            self.assertIn("GitHub 계정으로 로그인", primary)
            by_name = {item["filename"]: item for item in uploads["videos"]}
            for label, filename in (
                ("통합본 재생", "guide-walkthrough.mp4"),
                ("CLI 재생", "cli-edited.mp4"),
                ("포털 재생", "portal-edited.mp4"),
            ):
                self.assertIn(f"[{label}]({by_name[filename]['url']})", primary)
            english = (ROOT / "docs/video-summary.md").read_text()
            english_primary = english.split("## Play now", 1)[1].split("## Optional:", 1)[0]
            self.assertNotIn("127.0.0.1", english_primary)
            self.assertNotIn("python scripts/play_recordings.py", english_primary)
            self.assertIn("GitHub account", english_primary)
            for label, filename in (
                ("Play combined walkthrough", "guide-walkthrough.mp4"),
                ("Play CLI", "cli-edited.mp4"),
                ("Play portal", "portal-edited.mp4"),
            ):
                self.assertIn(f"[{label}]({by_name[filename]['url']})", english_primary)
            merged_url = by_name["guide-walkthrough.mp4"]["url"]
            actions = json.loads((ASSETS / "actions.json").read_text())["actions"]
            for directory, label in (("docs", "Combined"), ("docs/ko", "통합")):
                index = (ROOT / directory / "action-captures.md").read_text()
                rows = {
                    line.split("`", 2)[1]: line
                    for line in index.splitlines()
                    if line.startswith("| `")
                }
                for action in actions:
                    self.assertIn(f"▶ [{label} ", rows[action["id"]])
                    self.assertIn(
                        f"({merged_url}#t={action['combined_start_seconds']:.2f})",
                        rows[action["id"]],
                    )
                chapters = (ROOT / directory / "video-chapters.md").read_text()
                for chapter in active["guide-walkthrough.mp4"]["chapters"]:
                    self.assertIn(f"({merged_url}#t={chapter['start_seconds']:.2f})", chapters)
                self.assertEqual(len(re.findall(r"\| ▶ \[[0-9:]+\]\(", chapters)), 12)
                for document in ("video-summary.md", "video-chapters.md", "action-captures.md"):
                    text = (ROOT / directory / document).read_text()
                    self.assertNotIn("127.0.0.1:8765", text)
                    self.assertNotRegex(text, r"\]\([^)\s]*\.mp4(?:[?#][^)]*)?\)")
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
        media_extensions = {
            ".png",
            ".jpg",
            ".jpeg",
            ".webp",
            ".gif",
            ".svg",
            ".mp4",
            ".webm",
            ".mov",
            ".mkv",
            ".avi",
        }
        expected_media = {ASSETS / item["filename"] for item in media["videos"] + media["images"]}
        self.assertEqual(
            {
                path
                for path in (ROOT / "docs/assets").rglob("*")
                if path.is_file() and path.suffix.lower() in media_extensions
            },
            expected_media,
        )
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
