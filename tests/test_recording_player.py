import hashlib
import http.client
import json
import tempfile
import threading
import unittest
from pathlib import Path

from .test_packaging import load_script

PLAYER = load_script("play_recordings")


class RecordingPlayerTests(unittest.TestCase):
    def test_byte_ranges_cover_full_partial_open_and_suffix_requests(self):
        for value, expected in (
            (None, (0, 9)),
            ("bytes=2-5", (2, 5)),
            ("bytes=3-", (3, 9)),
            ("bytes=-4", (6, 9)),
            ("bytes=-40", (0, 9)),
            ("bytes=8-99", (8, 9)),
        ):
            with self.subTest(value=value):
                self.assertEqual(PLAYER.byte_range(value, 10), expected)

    def test_invalid_ranges_are_rejected(self):
        for value in (
            "bytes=-",
            "bytes=-0",
            "bytes=10-",
            "bytes=5-2",
            "bytes=0-1,4-5",
            "items=0-1",
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                PLAYER.byte_range(value, 10)
        with self.assertRaises(ValueError):
            PLAYER.byte_range(None, 0)

    def test_server_exposes_only_verified_media_and_supports_seeking(self):
        with tempfile.TemporaryDirectory(prefix="recording-player-test-") as directory:
            root = Path(directory)
            assets = root / "docs/assets" / PLAYER.ASSET_RUN
            assets.mkdir(parents=True)
            (root / "recording").mkdir()
            (root / "recording/player.html").write_text("<video controls></video>")
            content = b"0123456789"
            media = assets / "cli-full-run.mp4"
            media.write_bytes(content)
            manifest = {
                "videos": [
                    {
                        "filename": media.name,
                        "bytes": len(content),
                        "sha256": hashlib.sha256(content).hexdigest(),
                    }
                ]
            }
            (assets / "media.json").write_text(json.dumps(manifest))
            server = PLAYER.create_server(root, 0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            connection = http.client.HTTPConnection("127.0.0.1", server.server_port)
            try:
                connection.request("GET", "/video/cli-full-run.mp4", headers={"Range": "bytes=2-5"})
                response = connection.getresponse()
                self.assertEqual(response.status, 206)
                self.assertEqual(response.getheader("Content-Range"), "bytes 2-5/10")
                self.assertEqual(response.read(), b"2345")
                connection.request("HEAD", "/video/cli-full-run.mp4")
                response = connection.getresponse()
                self.assertEqual(response.getheader("Content-Length"), "10")
                self.assertEqual(response.read(), b"")
                connection.request("GET", "/video/cli-full-run.mp4", headers={"Range": "bytes=99-"})
                response = connection.getresponse()
                self.assertEqual(response.status, 416)
                self.assertEqual(response.getheader("Content-Range"), "bytes */10")
                response.read()
                for path in ("/.env", "/video/../.env", "/outputs/azure-objects.json"):
                    connection.request("GET", path)
                    response = connection.getresponse()
                    self.assertEqual(response.status, 404)
                    response.read()
            finally:
                connection.close()
                server.shutdown()
                server.server_close()
                thread.join()
            media.write_bytes(b"modified")
            with self.assertRaises(ValueError):
                PLAYER.media_catalog(root)

    def test_manifest_cannot_publish_paths_outside_media_directory(self):
        with tempfile.TemporaryDirectory(prefix="recording-path-test-") as directory:
            root = Path(directory)
            assets = root / "docs/assets" / PLAYER.ASSET_RUN
            assets.mkdir(parents=True)
            (assets / "media.json").write_text(json.dumps({"videos": [{"filename": "../../.env"}]}))
            with self.assertRaises(ValueError):
                PLAYER.media_catalog(root)
