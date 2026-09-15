import hashlib
import json
import re
import unittest
from collections import Counter
from itertools import pairwise

from . import ROOT

ASSETS = ROOT / "docs/assets/english-20260915"


class EnglishMediaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.media = json.loads((ASSETS / "media.json").read_text())
        cls.ledger = json.loads((ASSETS / "actions.json").read_text())
        cls.timeline = json.loads((ASSETS / "edit-timeline.json").read_text())
        cls.uploads = json.loads((ASSETS / "github-playback.json").read_text())
        cls.results = json.loads((ASSETS / "live-results.json").read_text())

    def test_new_recording_scope_and_canonical_input_language_are_explicit(self):
        self.assertEqual(self.media["recorded_on"], "2026-09-15")
        self.assertEqual(self.media["guide_language"], "en")
        self.assertEqual(self.media["scenario_language"], "ko")
        self.assertTrue(self.media["new_recording"])
        for flag in (
            "authentication_recorded",
            "historical_json_replay",
            "provisioned",
            "deployed",
            "roles_changed",
            "default_subscription_changed",
            "company_or_m365_data_accessed",
        ):
            self.assertFalse(self.media[flag], flag)
        self.assertFalse(self.results["new_english_language_evaluation"])
        self.assertIn("English", (ROOT / "README.md").read_text())
        self.assertIn("docs/english-recordings.md", (ROOT / "README.md").read_text())

    def test_every_action_has_real_screens_and_a_combined_video_position(self):
        actions = self.ledger["actions"]
        self.assertEqual(len(actions), 234)
        self.assertEqual(len({action["id"] for action in actions}), len(actions))
        self.assertEqual(self.media["action_count"], len(actions))
        counts = Counter(action["surface"] for action in actions)
        self.assertEqual(counts, {"cli": 57, "portal": 88, "guide": 89})
        self.assertEqual(self.media["action_counts"], counts)
        self.assertEqual(self.ledger["counts"], counts)
        known = {image["filename"] for image in self.media["images"]}
        self.assertEqual(len(known), self.media["screenshot_count"])
        captures = 0
        for action in actions:
            with self.subTest(action=action["id"]):
                self.assertTrue(action["screenshots"])
                for shot in action["screenshots"]:
                    self.assertIn(shot["image"], known)
                    self.assertRegex(shot["original_png_sha256"], r"^[0-9a-f]{64}$")
                    captures += 1
                intervals = [
                    item
                    for item in action["video_intervals"]
                    if item["video"] == "guide-walkthrough.mp4"
                ]
                self.assertTrue(intervals)
                self.assertEqual(action["combined_start_seconds"], intervals[0]["start_seconds"])
                self.assertTrue(
                    all(item["end_seconds"] > item["start_seconds"] for item in intervals)
                )
        self.assertEqual(captures, self.media["retained_capture_events"])

    def test_all_media_bytes_match_the_published_hashes(self):
        for item in [*self.media["videos"], *self.media["images"]]:
            with self.subTest(file=item["filename"]):
                path = (ASSETS / item["filename"]).resolve()
                self.assertTrue(path.is_relative_to(ASSETS.resolve()))
                self.assertEqual(path.stat().st_size, item["bytes"])
                with path.open("rb") as stream:
                    self.assertEqual(
                        hashlib.file_digest(stream, "sha256").hexdigest(), item["sha256"]
                    )

    def test_edits_preserve_real_frames_actions_chapters_and_recovery_disclosure(self):
        self.assertFalse(self.timeline["screenshot_slideshow"])
        self.assertFalse(self.timeline["new_azure_execution_by_edit"])
        self.assertEqual(self.timeline["playback_speed"], 1)
        sources = {source["id"]: source for source in self.timeline["sources"]}
        recovery = sources["portal"]["metadata_recovery"]
        self.assertFalse(recovery["timestamps_are_original_event_ledger"])
        self.assertFalse(recovery["source_footage_replayed_or_regenerated"])
        self.assertEqual(recovery["matched_screenshots"], 250)
        self.assertTrue(sources["guide"]["superseded_document_actions"])
        media = {video["filename"]: video for video in self.media["videos"]}
        combined = None
        for video in self.timeline["videos"]:
            position = 0
            for segment in video["segments"]:
                self.assertEqual(segment["output_first_frame"], position)
                position += segment["frames"]
                self.assertEqual(segment["output_last_frame"], position - 1)
                if segment["kind"] == "footage":
                    source = sources[segment["source_id"]]
                    self.assertLess(segment["last_frame"], source["frames"])
                    self.assertGreaterEqual(segment["first_frame"], 0)
                    self.assertEqual(
                        segment["frames"], segment["last_frame"] - segment["first_frame"] + 1
                    )
            self.assertEqual(position, media[video["filename"]]["frames"])
            self.assertAlmostEqual(
                position / 25, media[video["filename"]]["duration_seconds"], places=3
            )
            self.assertTrue(media[video["filename"]]["full_decode_verified"])
            if video["filename"] == "guide-walkthrough.mp4":
                combined = video["segments"]
        self.assertIsNotNone(combined)
        self.assertEqual([s["lab"] for s in combined], sorted(s["lab"] for s in combined))
        cards = [s for s in combined if s["kind"] == "chapter-card"]
        self.assertEqual([s["lab"] for s in cards], list(range(12)))
        self.assertEqual(sum(s["frames"] for s in cards), 600)
        footage = [s for s in combined if s["kind"] == "footage"]
        self.assertEqual(len({s["clip"] for s in footage}), len(footage))
        self.assertEqual(
            {s["action_id"] for s in footage}, {a["id"] for a in self.ledger["actions"]}
        )
        checks = self.timeline["frame_verification"]
        self.assertEqual(checks["checked_segments"], len(footage))
        self.assertEqual({c["clip"] for c in checks["comparisons"]}, {s["clip"] for s in footage})
        self.assertGreaterEqual(checks["minimum_midpoint_ssim"], 0.95)
        chapters = media["guide-walkthrough.mp4"]["chapters"]
        self.assertEqual([chapter["lab"] for chapter in chapters], list(range(12)))
        self.assertEqual(chapters[0]["start_seconds"], 0)
        for before, after in pairwise(chapters):
            self.assertEqual(before["end_seconds"], after["start_seconds"])
        self.assertEqual(
            chapters[-1]["end_seconds"], media["guide-walkthrough.mp4"]["duration_seconds"]
        )

    def test_failures_remain_and_historical_judges_are_not_new_scores(self):
        actions = {action["id"]: action for action in self.ledger["actions"]}
        self.assertEqual(actions["07-002-evaluate-baseline"]["exit_code"], 1)
        self.assertEqual(actions["04-004-input-boundary"]["exit_code"], 2)
        self.assertEqual(actions["08-006-local-response"]["exit_code"], 1)
        self.assertEqual(actions["08-006b-local-response"]["exit_code"], 0)
        self.assertEqual(actions["P03-010-current-response"]["status"], "failed")
        self.assertEqual(actions["P03-010-current-response"]["service_status"], 503)
        self.assertEqual(actions["P03-010-current-retry-response"]["status"], "recorded")
        self.assertEqual(
            [(run["passed"], run["total"], run["errors"]) for run in self.results["runs"]],
            [(5, 6, 0), (6, 6, 0), (4, 4, 0)],
        )
        for run in self.results["runs"]:
            self.assertEqual(run["actual_rows"], run["expected_rows"])
            for key in (
                "prompt_hash",
                "dataset_hash",
                "corpus_hash",
                "code_hash",
                "responses_hash",
            ):
                self.assertRegex(run[key], r"^[0-9a-f]{64}$")
        historical = self.results["historical_evaluation_observations"]
        self.assertEqual(historical["executed_on"], "2026-09-14")
        self.assertEqual(historical["new_jobs_created"], 0)
        self.assertFalse(self.results["hosted"]["new_hosted_quality_evaluation"])
        self.assertEqual(self.results["hosted"]["local_readiness"], {"status": "healthy"})

    def test_both_languages_link_every_new_video_chapter_and_action(self):
        self.assertEqual(self.uploads["status"], "published")
        self.assertEqual(self.uploads["repository_id"], 1367892793)
        self.assertTrue(self.uploads["private_repository"])
        self.assertFalse(self.uploads["signed_media_urls_saved"])
        videos = {video["filename"]: video for video in self.media["videos"]}
        combined = next(
            video["url"]
            for video in self.uploads["videos"]
            if video["filename"] == "guide-walkthrough.mp4"
        )
        for directory in ("docs", "docs/ko"):
            summary = (ROOT / directory / "english-recordings.md").read_text()
            index = (ROOT / directory / "english-captures.md").read_text()
            rows = {
                line.split("`", 2)[1]: line for line in index.splitlines() if line.startswith("| `")
            }
            self.assertEqual(len(rows), len(self.ledger["actions"]))
            for uploaded in self.uploads["videos"]:
                self.assertEqual(uploaded["source_sha256"], videos[uploaded["filename"]]["sha256"])
                self.assertEqual(uploaded["bytes"], videos[uploaded["filename"]]["bytes"])
                self.assertRegex(
                    uploaded["url"], r"^https://github\.com/user-attachments/assets/[0-9a-f-]+$"
                )
                self.assertEqual(summary.splitlines().count(uploaded["url"]), 1)
            for chapter in videos["guide-walkthrough.mp4"]["chapters"]:
                self.assertIn(f"({combined}#t={chapter['start_seconds']:.2f})", summary)
            for action in self.ledger["actions"]:
                self.assertIn(
                    f"({combined}#t={action['combined_start_seconds']:.2f})", rows[action["id"]]
                )
            self.assertNotIn("private-user-images.githubusercontent.com", summary + index)
            self.assertNotRegex(summary + index, r"\]\([^)\s]*\.mp4(?:[?#][^)]*)?\)")
            self.assertEqual(len(re.findall(r"\| ▶ \[[0-9:]+\]\(", summary)), 12)
