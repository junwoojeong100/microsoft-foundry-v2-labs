import hashlib
import json
import re
import unittest
from itertools import pairwise

from . import ROOT

ASSETS = {
    language: ROOT / "docs/assets" / f"refresh-20260915-{language}" for language in ("ko", "en")
}


def read(path):
    return json.loads(path.read_text())


class MediaIntegrityTests(unittest.TestCase):
    def test_language_editions_use_different_actual_source_and_output_videos(self):
        hashes = {}
        for language, directory in ASSETS.items():
            media = read(directory / "media.json")
            self.assertEqual(media["edition"], language)
            self.assertEqual(media["recorded_on"], "2026-09-15")
            self.assertFalse(media["authentication_recorded"])
            self.assertTrue(media["new_azure_execution"])
            self.assertTrue(media["all_failures_retained_in_private_source"])
            self.assertEqual(len(media["videos"]), 3)
            hashes[language] = {
                item["sha256"] for item in media["source_recordings"] + media["videos"]
            }
            for video in media["videos"]:
                self.assertEqual(video["guide_language"], language)
                self.assertEqual(video["scenario_language"], language)
                self.assertTrue(video["new_recording"])
                self.assertTrue(video["full_decode_verified"])
        self.assertFalse(hashes["ko"] & hashes["en"])

    def test_every_published_image_and_video_matches_its_recorded_hash(self):
        for language, directory in ASSETS.items():
            media = read(directory / "media.json")
            images = read(directory / "screenshots.json")
            self.assertEqual(len(images), media["screenshot_count"])
            for item in images:
                self.assertEqual(item["guide_language"], language)
                self.assertTrue(item["pixel_exact"])
                self.assertRegex(item["source_png_sha256"], "^[0-9a-f]{64}$")
            for item in media["videos"] + images:
                name = item.get("filename") or item["file"]
                path = (directory / name).resolve()
                with self.subTest(language=language, file=name):
                    self.assertTrue(path.is_relative_to(directory.resolve()))
                    self.assertFalse(path.is_symlink())
                    with path.open("rb") as handle:
                        self.assertEqual(
                            hashlib.file_digest(handle, "sha256").hexdigest(), item["sha256"]
                        )
                    if "bytes" in item:
                        self.assertEqual(path.stat().st_size, item["bytes"])

    def test_every_action_has_new_screens_and_real_video_intervals(self):
        for language, directory in ASSETS.items():
            media = read(directory / "media.json")
            actions = read(directory / "actions.json")["actions"]
            known = {item["file"] for item in read(directory / "screenshots.json")}
            self.assertEqual(len(actions), media["actions"])
            self.assertEqual(len(actions), len({item["id"] for item in actions}))
            self.assertEqual({item["lab"] for item in actions}, set(range(12)))
            self.assertEqual(
                {item["channel"] for item in actions}, {"terminal", "local-server", "portal"}
            )
            for action in actions:
                self.assertTrue(action["id"].startswith("K" if language == "ko" else "E"))
                self.assertIn(action["status"], {"recorded", "failed"})
                self.assertTrue(action["images"])
                self.assertTrue(set(action["images"]) <= known)
                intervals = [
                    item
                    for item in action["video_intervals"]
                    if item["video"] == "guide-ordered.mp4"
                ]
                self.assertTrue(intervals)
                self.assertEqual(action["combined_start_seconds"], intervals[0]["start_seconds"])
                self.assertTrue(
                    all(item["start_seconds"] < item["end_seconds"] for item in intervals)
                )

    def test_frames_chapters_and_source_comparisons_cover_every_action(self):
        for directory in ASSETS.values():
            media = read(directory / "media.json")
            sources = {item["id"]: item for item in media["source_recordings"]}
            for video in media["videos"]:
                timeline = read(directory / video["filename"].replace(".mp4", "-timeline.json"))
                position = 0
                for segment in timeline:
                    self.assertEqual(segment["output_first_frame"], position)
                    position += segment["frames"]
                    self.assertEqual(segment["output_last_frame"], position - 1)
                    if "source_id" in segment:
                        self.assertEqual(
                            segment["frames"], segment["last_frame"] - segment["first_frame"] + 1
                        )
                        self.assertGreaterEqual(segment["first_frame"], 0)
                        self.assertLess(
                            segment["last_frame"], sources[segment["source_id"]]["frames"]
                        )
                self.assertEqual(position, video["frames"])
                self.assertAlmostEqual(position / 25, video["duration_seconds"], places=3)
            combined = read(directory / "guide-ordered-timeline.json")
            footage = [item for item in combined if "source_id" in item]
            cards = [item for item in combined if item.get("kind") == "chapter-card"]
            self.assertEqual([item["lab"] for item in cards], list(range(12)))
            self.assertEqual(
                [item["lab"] for item in combined], sorted(item["lab"] for item in combined)
            )
            self.assertEqual(len(footage), len({item["clip"] for item in footage}))
            self.assertEqual(
                {item["action_id"] for item in footage},
                {item["id"] for item in read(directory / "actions.json")["actions"]},
            )
            for source_id in sources:
                segments = sorted(
                    (item for item in footage if item["source_id"] == source_id),
                    key=lambda item: item["first_frame"],
                )
                for before, after in pairwise(segments):
                    self.assertLess(before["last_frame"], after["first_frame"])
            checks = read(directory / "frame-verification.json")
            self.assertFalse(checks["screenshot_slideshow"])
            self.assertFalse(checks["source_footage_modified"])
            self.assertEqual(checks["playback_speed"], 1)
            self.assertEqual(checks["checked_segments"], len(footage))
            self.assertGreaterEqual(checks["minimum_midpoint_ssim"], 0.95)
            self.assertEqual(
                {item["clip"] for item in checks["comparisons"]}, {item["clip"] for item in footage}
            )
            video = next(
                item for item in media["videos"] if item["filename"] == "guide-ordered.mp4"
            )
            chapters = video["chapters"]
            self.assertEqual([item["lab"] for item in chapters], list(range(12)))
            self.assertEqual(chapters[0]["start_seconds"], 0)
            for before, after in pairwise(chapters):
                self.assertAlmostEqual(before["end_seconds"], after["start_seconds"])
            self.assertAlmostEqual(chapters[-1]["end_seconds"], video["duration_seconds"])

    def test_local_native_playback_and_all_chapter_links_were_checked(self):
        for language, directory in ASSETS.items():
            metadata = read(directory / "media.json")
            playback = read(directory / "local-playback.json")
            self.assertEqual(playback["language"], language)
            self.assertEqual(playback["azure_calls"], 0)
            known = {item["filename"]: item for item in metadata["videos"]}
            self.assertEqual({item["filename"] for item in playback["videos"]}, set(known))
            for item in playback["videos"]:
                self.assertTrue(item["native_playback"])
                self.assertEqual(item["range_status"], 206)
                self.assertAlmostEqual(
                    item["duration_seconds"], known[item["filename"]]["duration_seconds"], places=2
                )
                self.assertEqual(
                    item["chapters_checked"], len(known[item["filename"]].get("chapters", []))
                )

    def test_guides_reference_only_their_own_new_language_images(self):
        for language, directory in ASSETS.items():
            docs = ROOT / ("docs/ko" if language == "ko" else "docs")
            known = {
                (directory / item["file"]).resolve()
                for item in read(directory / "screenshots.json")
            }
            for path in (docs / "labs").glob("*.md"):
                images = re.findall(r"!\[[^\]]+\]\(([^)]+)\)", path.read_text())
                self.assertTrue(images, path.name)
                for image in images:
                    self.assertIn((path.parent / image).resolve(), known)
            index = (docs / "action-captures.md").read_text()
            for action in read(directory / "actions.json")["actions"]:
                self.assertIn(f"| {action['id']} |", index)
                self.assertIn(f"#t={action['combined_start_seconds']:.2f}", index)

    def test_actual_language_results_and_failures_keep_separate_lineage(self):
        results = {
            language: read(directory / "live-results.json")
            for language, directory in ASSETS.items()
        }
        for language, result in results.items():
            self.assertEqual(result["language"], language)
            self.assertFalse(result["holdout_used_for_development"])
            self.assertFalse(result["production_approval"])
            self.assertEqual([item["rows"] for item in result["cohorts"][:2]], [24, 24])
            final = result["cohorts"][-1]
            self.assertEqual(final["rows"], 4 * len(result["selected_holdout_model_keys"]))
            for item in result["cohorts"]:
                self.assertLessEqual(item["business_passed"], item["rows"])
                self.assertLessEqual(item["groundedness_passed"], item["rows"])
                self.assertLessEqual(item["relevance_passed"], item["rows"])
                self.assertEqual(item["verified_traces"], item["rows"])
                for key in (
                    "dataset_hash",
                    "corpus_hash",
                    "code_hash",
                    "responses_hash",
                    "evaluator_hash",
                ):
                    self.assertRegex(item[key], "^[0-9a-f]{64}$")
        self.assertNotEqual(
            results["ko"]["cohorts"][0]["dataset_hash"], results["en"]["cohorts"][0]["dataset_hash"]
        )
        self.assertNotEqual(
            results["ko"]["cohorts"][0]["corpus_hash"], results["en"]["cohorts"][0]["corpus_hash"]
        )
        diagnostic = results["en"]["diagnostics"][0]
        self.assertEqual((diagnostic["rows"], diagnostic["business_passed"]), (24, 20))
        self.assertEqual(results["en"]["regression_review"], "pending-human-review")
        self.assertFalse(results["en"]["regressions_consumed"])
        self.assertEqual(results["en"]["cohorts"][1]["business_passed"], 23)
        self.assertEqual(results["en"]["selected_holdout_model_keys"], ["luna", "sol", "terra"])

    def test_publication_status_is_not_inferred_from_local_file_existence(self):
        for language, directory in ASSETS.items():
            status = read(directory / "github-playback.json")
            media = {item["filename"]: item for item in read(directory / "media.json")["videos"]}
            docs = ROOT / ("docs/ko" if language == "ko" else "docs")
            summary = (docs / "video-summary.md").read_text()
            self.assertIn(status["status"], {"published", "local-verified-not-published"})
            if status["status"] == "published":
                self.assertEqual(status["repository"], "junwoojeong100/microsoft-foundry-v2-labs")
                self.assertEqual(len(status["videos"]), len(media))
                for item in status["videos"]:
                    self.assertRegex(
                        item["url"], r"^https://github\.com/user-attachments/assets/[a-zA-Z0-9-]+$"
                    )
                    self.assertEqual(item["source_sha256"], media[item["filename"]]["sha256"])
                    self.assertEqual(item["bytes"], media[item["filename"]]["bytes"])
                    self.assertEqual(summary.splitlines().count(item["url"]), 1)
            else:
                self.assertEqual(status["videos"], [])
                self.assertNotIn("https://github.com/user-attachments/assets/", summary)
