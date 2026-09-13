import importlib.util
import json
import tempfile
import unittest
from itertools import pairwise
from pathlib import Path

from . import ROOT


def script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class VideoChapterTests(unittest.TestCase):
    def test_parts_preserve_the_complete_timeline_at_keyframes(self):
        packets = [
            {"pts_time": str(index), "size": "1000", "flags": "K_" if index % 2 == 0 else "__"}
            for index in range(20)
        ]
        chapters = [
            {"title": "First", "start_seconds": 1},
            {"title": "Second", "start_seconds": 9.5},
        ]
        parts = script("split_recording").plan_parts(chapters, packets, 20.0, 6000)
        self.assertEqual(len(parts), 4)
        self.assertEqual(parts[0]["source_start_seconds"], 0)
        self.assertEqual(parts[-1]["source_end_seconds"], 20)
        self.assertEqual(len({part["filename"] for part in parts}), len(parts))
        for previous, following in pairwise(parts):
            self.assertEqual(previous["source_end_seconds"], following["source_start_seconds"])
        self.assertTrue(all(part["source_start_seconds"] % 2 == 0 for part in parts))

    def test_missing_initial_keyframe_is_rejected(self):
        with self.assertRaises(ValueError):
            script("split_recording").plan_parts(
                [{"title": "First", "start_seconds": 0}],
                [{"pts_time": "1", "size": "1000", "flags": "K_"}],
                5,
                10000,
            )

    def test_attachment_urls_are_restricted_to_github_media(self):
        builder = script("build_video_index")
        with tempfile.TemporaryDirectory(prefix="video-index-test-") as directory:
            receipt = Path(directory) / "upload.json"
            receipt.write_text(json.dumps({"url": "https://example.com/video.mp4"}))
            with self.assertRaises(ValueError):
                builder.attachment_url(receipt)
            url = "https://github.com/user-attachments/assets/unit-test"
            receipt.write_text(json.dumps({"url": url}))
            self.assertEqual(builder.attachment_url(receipt), url)
        self.assertEqual(builder.timestamp(688.8), "11:29")
        self.assertEqual(builder.timestamp(3661), "1:01:01")
