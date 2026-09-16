#!/usr/bin/env python3
"""Serve only the verified workshop recordings on localhost."""

import argparse
import functools
import hashlib
import json
import math
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
ASSET_RUN = "refresh-20260915-en"
ASSET_RUNS = {"en": ASSET_RUN, "ko": "refresh-20260915-ko"}
SERIES = {
    "foundation": ASSET_RUNS,
    "extensions": {"en": "edition-20260916-en", "ko": "edition-20260916-ko"},
}


def byte_range(value: str | None, size: int) -> tuple[int, int]:
    if size <= 0:
        raise ValueError("A recording must not be empty.")
    if value is None:
        return 0, size - 1
    match = re.fullmatch(r"bytes=(\d*)-(\d*)", value)
    if not match or not any(match.groups()):
        raise ValueError("Only a single byte range is supported.")
    first, last = match.groups()
    if not first:
        length = int(last)
        if length <= 0:
            raise ValueError("A suffix range must request at least one byte.")
        return max(0, size - length), size - 1
    start, end = int(first), min(int(last) if last else size - 1, size - 1)
    if start > end:
        raise ValueError("The requested range is outside the recording.")
    return start, end


def media_catalog(
    root: Path, edition: str = "en", series: str = "foundation"
) -> tuple[dict, dict[str, Path]]:
    if edition not in ASSET_RUNS:
        raise ValueError("Choose recording edition en or ko.")
    if series not in SERIES:
        raise ValueError("Choose recording series foundation or extensions.")
    directory = root / "docs/assets" / SERIES[series][edition]
    metadata = json.loads((directory / "media.json").read_text(encoding="utf-8"))
    videos = metadata["videos"]
    if not isinstance(videos, list) or not videos:
        raise ValueError("The recording manifest has no videos.")
    files = {}
    for item in videos:
        name = item["filename"]
        if not re.fullmatch(r"[a-z0-9-]+\.mp4", name) or name in files:
            raise ValueError("The recording manifest has an invalid or duplicate filename.")
        path = directory / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Missing local recording: {name}. Download the repository first.")
        with path.open("rb") as handle:
            digest = hashlib.file_digest(handle, "sha256").hexdigest()
        if path.stat().st_size != item["bytes"] or digest != item["sha256"]:
            raise ValueError(f"Recording integrity check failed: {name}.")
        chapters = item.get("chapters", [])
        if not isinstance(chapters, list):
            raise ValueError(f"Invalid chapter list: {name}.")
        previous_end = 0
        chapter_ids = set()
        for chapter in chapters:
            start, end = chapter["start_seconds"], chapter["end_seconds"]
            duration = item["duration_seconds"]
            if (
                not isinstance(chapter["id"], str)
                or not re.fullmatch(r"[a-z0-9-]+", chapter["id"])
                or chapter["id"] in chapter_ids
                or not isinstance(chapter["title"], str)
                or not chapter["title"].strip()
                or any(
                    type(value) not in (int, float) or not math.isfinite(value)
                    for value in (start, end, duration)
                )
                or not previous_end <= start < end <= duration
            ):
                raise ValueError(f"Invalid or overlapping recording chapter: {name}.")
            previous_end = end
            chapter_ids.add(chapter["id"])
        files[name] = path
    default_video = metadata.get("default_video", videos[0]["filename"])
    if not isinstance(default_video, str) or default_video not in files:
        raise ValueError("The default recording is not in the verified media catalog.")
    return {
        "videos": videos,
        "default_video": default_video,
        "edition": edition,
        "recorded_on": metadata.get("recorded_on"),
        "series": series,
    }, files


class RecordingHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, player: bytes, catalog: bytes, files: dict[str, Path], **kwargs):
        self.player, self.catalog, self.files = player, catalog, files
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.respond(head=False)

    def do_HEAD(self):
        self.respond(head=True)

    def respond(self, *, head: bool):
        path = urlsplit(self.path).path
        documents = {
            "/": ("text/html; charset=utf-8", self.player),
            "/media.json": ("application/json", self.catalog),
        }
        if path in documents:
            content_type, body = documents[path]
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            if not head:
                self.wfile.write(body)
            return
        name = path.removeprefix("/video/") if path.startswith("/video/") else ""
        if name not in self.files:
            self.send_error(404, "Only the listed workshop recordings are served.")
            return
        source = self.files[name]
        size = source.stat().st_size
        requested = self.headers.get("Range")
        try:
            start, end = byte_range(requested, size)
        except ValueError:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        self.send_response(206 if requested else 200)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("X-Content-Type-Options", "nosniff")
        if requested:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        if head:
            return
        try:
            with source.open("rb") as handle:
                handle.seek(start)
                remaining = end - start + 1
                while remaining:
                    chunk = handle.read(min(1_048_576, remaining))
                    if not chunk:
                        raise OSError("The recording changed while streaming.")
                    self.wfile.write(chunk)
                    remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            self.log_message("Player closed or replaced a byte-range request.")


def create_server(
    root: Path, port: int, edition: str = "en", series: str = "foundation"
) -> ThreadingHTTPServer:
    catalog, files = media_catalog(root, edition, series)
    handler = functools.partial(
        RecordingHandler,
        player=(root / "recording/player.html").read_bytes(),
        catalog=json.dumps(catalog).encode(),
        files=files,
    )
    return ThreadingHTTPServer(("127.0.0.1", port), handler)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument(
        "--edition",
        choices=tuple(ASSET_RUNS),
        default="en",
        help="Recording set: English-guide recordings (default) or the Korean source recordings.",
    )
    parser.add_argument(
        "--series",
        choices=tuple(SERIES),
        default="foundation",
        help="Keep foundational recordings and the September 16 extensions as separate evidence sets.",
    )
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error("--port must be between 1024 and 65535.")
    try:
        with create_server(ROOT, args.port, args.edition, args.series) as server:
            print(f"Recording player: http://127.0.0.1:{args.port}/", flush=True)
            print("Local files only; no Azure calls or uploads. Press Ctrl+C to stop.", flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                print("\nRecording player stopped.")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
