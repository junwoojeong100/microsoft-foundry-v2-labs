import hashlib
import json
import re
import unittest
from itertools import pairwise

from . import ROOT

ASSETS = {
    language: ROOT / "docs/assets" / f"g6sol-20260924-{language}" for language in ("ko", "en")
}
REMOVED_SERIES = ("refresh-20260915", "edition-20260916", "g6luna-20260923", "g6sol-20260923")
REMOVED_SUPPLEMENTS = ("eval-portal-20260923",)
REMOVED_PAGES = (
    "edition-results.md",
    "edition-videos.md",
    "edition-actions.md",
    "edition-chapters.md",
    "gpt-6-luna-recordings.md",
)
HASH_FIELDS = ("dataset_hash", "corpus_hash", "code_hash", "prompt_hash", "responses_hash")
# A kept failure must be followed by the recorded action that completed the same guide step.
FOLLOW_UPS = {
    "07-011-business-baseline": ("07-013-business-retry",),
    "07-012-business-candidate": ("07-014-business-readback", "07-015-business-candidate"),
}


def read(path):
    return json.loads(path.read_text())


class MediaIntegrityTests(unittest.TestCase):
    """September 24 gpt-6-sol recordings of the main A/B steps (Labs 00-09 and 11) with the optional evaluations."""

    assets = ASSETS
    recorded_on = "2026-09-24"
    lab_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11]
    unrecorded_guides = {"10-iq-extensions"}
    action_index = "action-captures.md"
    video_summary = "video-summary.md"
    supplemental_assets = ("iq-chat-20260917",)

    def test_language_editions_use_different_actual_source_and_output_videos(self):
        hashes = {}
        for language, directory in self.assets.items():
            media = read(directory / "media.json")
            self.assertEqual(media["edition"], language)
            self.assertEqual(media["recorded_on"], self.recorded_on)
            self.assertFalse(media["authentication_recorded"])
            self.assertTrue(media["new_azure_execution"])
            self.assertTrue(media["all_failures_retained_in_private_source"])
            self.assertEqual(len(media["videos"]), 3)
            self.assertEqual(media["edition_id"], "g6sol-20260924")
            self.assertEqual(
                media["model_preset"],
                {
                    "deployment": "gpt-6-sol",
                    "model": "gpt-6-sol",
                    "version": "2026-09-22",
                    "judge_deployment": "gpt-6-sol-judge",
                },
            )
            self.assertTrue(media["independent_language_capture"])
            self.assertFalse(media["translated_english_assets"])
            self.assertFalse(media["upstream_results_reused_as_this_edition"])
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
        for language, directory in self.assets.items():
            media = read(directory / "media.json")
            images = read(directory / "screenshots.json")
            self.assertEqual(len(images), media["screenshot_count"])
            for item in images:
                self.assertEqual(item["guide_language"], language)
                self.assertTrue(item["pixel_exact"])
                self.assertRegex(item["source_png_sha256"], "^[0-9a-f]{64}$")
            for item in media["videos"] + images:
                name = item.get("filename") or item["file"]
                candidate = directory / name
                path = candidate.resolve()
                with self.subTest(language=language, file=name):
                    self.assertTrue(path.is_relative_to(directory.resolve()))
                    self.assertFalse(candidate.is_symlink())
                    with path.open("rb") as handle:
                        self.assertEqual(
                            hashlib.file_digest(handle, "sha256").hexdigest(), item["sha256"]
                        )
                    if "bytes" in item:
                        self.assertEqual(path.stat().st_size, item["bytes"])

    def test_every_action_has_new_screens_and_real_video_intervals(self):
        for language, directory in self.assets.items():
            media = read(directory / "media.json")
            actions = read(directory / "actions.json")["actions"]
            known = {item["file"] for item in read(directory / "screenshots.json")}
            self.assertEqual(len(actions), media["actions"])
            self.assertEqual(len(actions), len({item["id"] for item in actions}))
            self.assertEqual({item["lab"] for item in actions}, set(self.lab_ids))
            self.assertEqual({item["channel"] for item in actions}, {"terminal", "portal"})
            summary = read(directory / "live-results.json")["actions"]
            expected_nonzero = set(summary["expected_nonzero_exit"])
            retained = {item["id"]: item for item in summary["retained_failures"]}
            identifiers = [item["id"] for item in actions]
            for identifier, item in retained.items():
                self.assertIn(identifier[1:], FOLLOW_UPS)
                self.assertTrue(item["reason"])
                for follow_up in FOLLOW_UPS[identifier[1:]]:
                    self.assertIn(identifier[0] + follow_up, identifiers)
            for action in actions:
                self.assertTrue(action["id"].startswith("K" if language == "ko" else "E"))
                if action["id"] in retained:
                    self.assertEqual(action["status"], "failed")
                    self.assertEqual(action["exit_code"], retained[action["id"]]["exit_code"])
                    self.assertNotEqual(action["exit_code"], 0)
                    continue
                self.assertEqual(action["status"], "recorded")
                self.assertEqual(action["exit_code"], 1 if action["id"] in expected_nonzero else 0)
                if action.get("capture_issue"):
                    self.assertIn("Not a Foundry failure", action["capture_issue"])
                    named = set(
                        re.findall(
                            r"\b[EK]P?\d\d-\d{3}-[a-z0-9-]*[a-z0-9]", action["capture_issue"]
                        )
                    )
                    self.assertTrue(named - {action["id"]})
                    self.assertTrue(named <= set(identifiers), named)
                self.assertTrue(action["capture_status_is_not_execution_success"])
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
        for directory in self.assets.values():
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
            self.assertEqual([item["lab"] for item in cards], self.lab_ids)
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
            self.assertEqual([item["lab"] for item in chapters], self.lab_ids)
            self.assertEqual(chapters[0]["start_seconds"], 0)
            for before, after in pairwise(chapters):
                self.assertAlmostEqual(before["end_seconds"], after["start_seconds"])
            self.assertAlmostEqual(chapters[-1]["end_seconds"], video["duration_seconds"])

    def test_local_native_playback_and_all_chapter_links_were_checked(self):
        for language, directory in self.assets.items():
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
                self.assertEqual(item["seek_validation"], "seek-complete-and-decoded-frame")

    def test_guides_reference_only_their_own_new_language_images(self):
        for language, directory in self.assets.items():
            docs = ROOT / ("docs/ko" if language == "ko" else "docs")
            known = {
                (directory / item["file"]).resolve()
                for item in read(directory / "screenshots.json")
            }
            for name in self.supplemental_assets:
                supplement = ROOT / "docs/assets" / name
                known.update(
                    (supplement / item["file"]).resolve()
                    for item in read(supplement / "captures.json")["images"]
                    if item["guide_language"] == language
                )
            used = set()
            for path in sorted((docs / "labs").glob("*.md")):
                images = re.findall(r"!\[[^\]]+\]\(([^)]+)\)", path.read_text())
                with self.subTest(language=language, guide=path.name):
                    if path.stem in self.unrecorded_guides:
                        self.assertFalse(images)
                    else:
                        self.assertTrue(images)
                    for image in images:
                        target = (path.parent / image).resolve()
                        self.assertIn(target, known)
                        used.add(target)
            self.assertGreaterEqual(len(used), 50)
            for path in sorted((docs / "labs/extensions").glob("*.md")):
                self.assertFalse(re.findall(r"!\[[^\]]+\]\(([^)]+)\)", path.read_text()), path)
            index = (docs / self.action_index).read_text()
            for action in read(directory / "actions.json")["actions"]:
                self.assertIn(f"| {action['id']} |", index)
                self.assertIn(f"#t={action['combined_start_seconds']:.2f}", index)

    def test_actual_language_results_and_failures_keep_separate_lineage(self):
        results = {
            language: read(directory / "live-results.json")
            for language, directory in self.assets.items()
        }
        for language, result in results.items():
            with self.subTest(language=language):
                actions = read(self.assets[language] / "actions.json")["actions"]
                self.assertEqual(result["language"], language)
                self.assertEqual(result["series"], "gpt-6-sol")
                self.assertEqual(result["edition_id"], "g6sol-20260924")
                self.assertFalse(result["holdout_used_for_development"])
                self.assertFalse(result["production_approval"])
                self.assertRegex(result["source_hash"], "^[0-9a-f]{64}$")
                self.assertRegex(result["base_commit"], "^[0-9a-f]{40}$")
                self.assertEqual(
                    {
                        (item["name"], item["model"], item["version"])
                        for item in result["deployments"]
                    },
                    {
                        ("gpt-6-sol", "gpt-6-sol", "2026-09-22"),
                        ("gpt-6-sol-judge", "gpt-6-sol", "2026-09-22"),
                    },
                )
                self.assertEqual(result["actions"]["total"], len(actions))
                self.assertEqual(
                    result["actions"]["failed"],
                    [item["id"] for item in actions if item["status"] == "failed"],
                )
                self.assertEqual(
                    result["actions"]["failed"],
                    [item["id"] for item in result["actions"]["retained_failures"]],
                )
                self.assertEqual(result["actions"]["nonzero_exit"], [])
                self.assertEqual(
                    [item["id"] for item in result["actions"]["capture_issues"]],
                    [item["id"] for item in actions if item.get("capture_issue")],
                )
                letter = "K" if language == "ko" else "E"
                identifiers = {item["id"] for item in actions}
                conditional = [
                    letter + suffix
                    for suffix in (
                        "07-013-business-retry",
                        "07-014-business-readback",
                        "07-015-business-candidate",
                    )
                    if letter + suffix not in identifiers
                ]
                skipped = [item["id"] for item in result["actions"]["skipped"]]
                if result["diagnostic_no_evidence"]:
                    self.assertEqual(skipped, [f"{letter}07-003-feedback", *conditional])
                    self.assertEqual(
                        result["actions"]["expected_nonzero_exit"],
                        [f"{letter}07-022-diagnostic-evaluate"],
                    )
                    self.assertEqual(result["diagnostic_no_evidence"]["business_passed"], 0)
                    self.assertEqual(result["diagnostic_no_evidence"]["errors"], 0)
                else:
                    self.assertEqual(
                        skipped,
                        [
                            f"{letter}07-021-diagnostic",
                            f"{letter}07-022-diagnostic-evaluate",
                            *conditional,
                        ],
                    )
                for update in result["source_updates"]:
                    self.assertIn(update["applies_from_action"], identifiers)
                    self.assertRegex(update["source_hash_after"], "^[0-9a-f]{64}$")
                    self.assertNotEqual(update["source_hash_before"], update["source_hash_after"])
                    self.assertTrue(update["files"])
                cohorts = result["cohorts"]
                self.assertEqual(
                    [item["label"] for item in cohorts], ["baseline", "candidate", "final-holdout"]
                )
                self.assertEqual([item["split"] for item in cohorts], ["dev", "dev", "holdout"])
                self.assertEqual([item["rows"] for item in cohorts], [6, 6, 4])
                self.assertEqual([item["prompt_version"] for item in cohorts], ["v1", "v2", "v2"])
                self.assertEqual(cohorts[2]["frozen_candidate_run_id"], cohorts[1]["run_id"])
                for item in cohorts:
                    self.assertEqual(item["rows"], item["expected_rows"])
                    self.assertEqual(item["observed_models"], ["gpt-6-sol"])
                    self.assertEqual(
                        item["business_passed"] + item["business_failed"] + item["errors"],
                        item["rows"],
                    )
                    for key in (*HASH_FIELDS, "business_report_sha256"):
                        self.assertRegex(item[key], "^[0-9a-f]{64}$")
                self.assertNotEqual(cohorts[0]["prompt_hash"], cohorts[1]["prompt_hash"])
                self.assertEqual(cohorts[1]["prompt_hash"], cohorts[2]["prompt_hash"])
                acceptance = result["acceptance"]
                self.assertFalse(acceptance["deployment_approved"])
                self.assertFalse(acceptance["cloud_judge_results_included"])
                judge = result["cloud_judge"]
                self.assertEqual(judge["judge_deployment"], "gpt-6-sol-judge")
                self.assertEqual(judge["source_run_id"], cohorts[1]["run_id"])
                self.assertEqual(judge["dataset_hash"], cohorts[1]["dataset_hash"])
                self.assertFalse(judge["included_in_acceptance"])
                self.assertEqual(set(judge["evaluators"]), {"groundedness", "relevance"})
                for name, counts in judge["evaluators"].items():
                    self.assertEqual(sum(counts.values()), judge["rows"])
                    self.assertEqual(counts["failed"], len(judge["failed_cases"].get(name, [])))
                for key in ("input_hash", "dataset_hash", "evaluator_hash", "results_hash"):
                    self.assertRegex(judge[key], "^[0-9a-f]{64}$")
                self.assertTrue(result["portal"]["portal_answers_evaluated"])
                rubric = result["business_rubric"]
                self.assertEqual(
                    rubric["baseline"]["evaluation_id"], rubric["candidate"]["evaluation_id"]
                )
                for label in ("baseline", "candidate"):
                    self.assertEqual(rubric[label]["validation_status"], "valid")
                    self.assertEqual(rubric[label]["agreement"]["total"], 6)
                    first = rubric[label].get("first_attempt")
                    if first:
                        self.assertEqual(first["validation_status"], "invalid")
                        self.assertTrue(first["evaluator_hash_unchanged"])
                        self.assertEqual(rubric[label]["retry_of"]["run_id"], first["run_id"])
                tools = result["maf_tool_evaluation"]
                self.assertTrue(tools["complete"])
                self.assertEqual(tools["errors"], 0)
                self.assertEqual(
                    set(tools["native_pass_counts"]), {"tool_call_accuracy", "relevance"}
                )
                portal = result["portal_evaluations"]
                superseded = {item["id"] for item in result["actions"]["superseded"]}
                self.assertEqual(
                    set(portal),
                    {"portal_dataset", "portal_traces"}
                    | (
                        {"portal_dataset_superseded"}
                        if f"{letter}P07-206-submit" in superseded
                        else set()
                    ),
                )
                for item in portal.values():
                    self.assertTrue(item["name"].startswith(result["prefix"] + "-"))
                    self.assertTrue(any(run["status"] == "completed" for run in item["runs"]))
                for key in ("portal_dataset", "portal_traces"):
                    self.assertEqual(
                        {run["agent_version"] for run in portal[key]["runs"]}, {"2"}, key
                    )
        for key in ("dataset_hash", "corpus_hash"):
            self.assertNotEqual(results["ko"]["cohorts"][0][key], results["en"]["cohorts"][0][key])

    def test_publication_status_is_not_inferred_from_local_file_existence(self):
        for language, directory in self.assets.items():
            status = read(directory / "github-playback.json")
            media = {item["filename"]: item for item in read(directory / "media.json")["videos"]}
            docs = ROOT / ("docs/ko" if language == "ko" else "docs")
            summary = (docs / self.video_summary).read_text()
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

    def test_removed_recordings_are_neither_kept_nor_linked(self):
        for name in REMOVED_SERIES:
            for language in ("ko", "en"):
                self.assertFalse((ROOT / "docs/assets" / f"{name}-{language}").exists())
        for name in REMOVED_SUPPLEMENTS:
            self.assertFalse((ROOT / "docs/assets" / name).exists())
        for name in REMOVED_PAGES:
            self.assertFalse((ROOT / "docs" / name).exists())
            self.assertFalse((ROOT / "docs/ko" / name).exists())
        pages = [ROOT / "README.md", ROOT / "README.ko.md", *sorted((ROOT / "docs").rglob("*.md"))]
        for path in pages:
            text = path.read_text()
            with self.subTest(page=path.relative_to(ROOT)):
                self.assertNotIn("github.com/user-attachments/assets/", text)
                for name in REMOVED_SERIES:
                    self.assertNotIn(f"{name}-en", text)
                    self.assertNotIn(f"{name}-ko", text)
                for name in REMOVED_PAGES:
                    self.assertNotIn(name, text)
                for name in REMOVED_SUPPLEMENTS:
                    self.assertNotIn(f"{name}/", text)
