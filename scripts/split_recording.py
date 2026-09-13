#!/usr/bin/env python3
"""Split a silent workshop recording without re-encoding or dropping frames."""

import argparse
import bisect
import csv
import json
import math
import shutil
import subprocess
import tempfile
from itertools import pairwise
from pathlib import Path


def probe(path: Path, *, packets: bool = False) -> dict:
    command = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-of", "json"]
    if packets:
        command += ["-show_packets", "-show_entries", "packet=pts_time,size,flags"]
    else:
        command += [
            "-count_packets",
            "-show_entries",
            "format=duration,size:stream=nb_read_packets,codec_name,width,height",
        ]
    return json.loads(subprocess.check_output([*command, str(path)], text=True))


def plan_parts(
    chapters: list[dict], packets: list[dict], duration: float, target_bytes: int
) -> list[dict]:
    ordered = sorted(packets, key=lambda packet: float(packet["pts_time"]))
    times = [float(packet["pts_time"]) for packet in ordered]
    keyframes = [float(packet["pts_time"]) for packet in ordered if "K" in packet["flags"]]
    if not keyframes or abs(keyframes[0]) > 0.001:
        raise ValueError("The recording must begin with an independently decodable keyframe.")
    offsets = [0]
    for packet in ordered:
        offsets.append(offsets[-1] + int(packet["size"]))

    def next_keyframe(value: float) -> float:
        index = bisect.bisect_left(keyframes, value)
        return keyframes[index] if index < len(keyframes) else duration

    boundaries = (
        [0.0]
        + [next_keyframe(float(chapter["start_seconds"])) for chapter in chapters[1:]]
        + [duration]
    )
    if any(right <= left for left, right in pairwise(boundaries)):
        raise ValueError("Chapter boundaries must be strictly increasing.")
    result = []
    for index, chapter in enumerate(chapters):
        start, end = boundaries[index : index + 2]
        lo, hi = bisect.bisect_left(times, start), bisect.bisect_left(times, end)
        total_bytes = offsets[hi] - offsets[lo]
        count = max(1, math.ceil(total_bytes / target_bytes))
        cuts = [start]
        for part in range(1, count):
            wanted = offsets[lo] + total_bytes * part / count
            packet_index = min(bisect.bisect_left(offsets, wanted), hi - 1)
            cut = next_keyframe(times[packet_index])
            if cuts[-1] < cut < end:
                cuts.append(cut)
        cuts.append(end)
        for part, (left, right) in enumerate(pairwise(cuts), 1):
            suffix = f"-part-{part:02d}" if len(cuts) > 2 else ""
            result.append(
                {
                    "chapter": index + 1,
                    "title": chapter["title"],
                    "part": part,
                    "parts_in_chapter": len(cuts) - 1,
                    "filename": f"chapter-{index + 1:02d}{suffix}.mp4",
                    "source_start_seconds": round(left, 3),
                    "source_end_seconds": round(right, 3),
                }
            )
    return result


def split(source: Path, metadata: Path, output: Path, max_bytes: int) -> dict:
    if output.exists():
        raise FileExistsError(f"Preserve the existing video output: {output}")
    if not 10_000_000 <= max_bytes <= 100_000_000:
        raise ValueError("Choose a per-file limit between 10 MB and 100 MB.")
    original = probe(source)
    duration = float(original["format"]["duration"])
    packets = probe(source, packets=True)["packets"]
    chapters = json.loads(metadata.read_text(encoding="utf-8"))["chapters"]
    output.parent.mkdir(parents=True, exist_ok=True)
    target = int(max_bytes * 0.85)
    for _attempt in range(3):
        plan = plan_parts(chapters, packets, duration, target)
        with tempfile.TemporaryDirectory(prefix="video-segments-", dir=output.parent) as working:
            temporary = Path(working)
            boundaries = ",".join(str(part["source_start_seconds"]) for part in plan[1:])
            subprocess.run(
                [
                    "ffmpeg",
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    "-i",
                    str(source),
                    "-map",
                    "0",
                    "-c",
                    "copy",
                    "-f",
                    "segment",
                    "-segment_times",
                    boundaries,
                    "-segment_time_delta",
                    "0.01",
                    "-reset_timestamps",
                    "1",
                    "-segment_format",
                    "mp4",
                    "-segment_format_options",
                    "movflags=+faststart",
                    "-segment_list",
                    str(temporary / "segments.csv"),
                    "-segment_list_type",
                    "csv",
                    str(temporary / "segment-%03d.mp4"),
                ],
                check=True,
            )
            with (temporary / "segments.csv").open(newline="", encoding="utf-8") as handle:
                actual = list(csv.reader(handle))
            if len(actual) != len(plan):
                raise ValueError(
                    "The segment muxer did not produce the planned number of chapters."
                )
            packet_total = 0
            oversized = False
            for item, row in zip(plan, actual, strict=True):
                file = temporary / Path(row[0]).name
                details = probe(file)
                size = file.stat().st_size
                oversized |= size >= max_bytes
                packet_total += int(details["streams"][0]["nb_read_packets"])
                first_packets = probe(file, packets=True)["packets"]
                if not first_packets or "K" not in first_packets[0]["flags"]:
                    raise ValueError(f"Segment does not begin at a keyframe: {file.name}")
                item.update(
                    size_bytes=size,
                    duration_seconds=float(details["format"]["duration"]),
                    mux_start_seconds=float(row[1]),
                    mux_end_seconds=float(row[2]),
                )
            if packet_total != len(packets):
                raise ValueError("Frame/packet count changed; refuse a recording with omissions.")
            if oversized:
                target = int(target * 0.7)
                continue
            output.mkdir()
            for item, row in zip(plan, actual, strict=True):
                shutil.move(temporary / Path(row[0]).name, output / item["filename"])
            report = {
                "source_duration_seconds": duration,
                "source_video_packets": len(packets),
                "output_video_packets": packet_total,
                "max_file_bytes": max_bytes,
                "reencoded": False,
                "waiting_time_removed": False,
                "parts": plan,
            }
            (output / "parts.json").write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            return report
    raise ValueError("Could not satisfy the per-file size limit.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-bytes", type=int, default=100_000_000)
    args = parser.parse_args()
    report = split(args.source, args.metadata, args.output, args.max_bytes)
    print(
        json.dumps(
            {
                "parts": len(report["parts"]),
                "largest_bytes": max(part["size_bytes"] for part in report["parts"]),
                "source_packets": report["source_video_packets"],
                "output_packets": report["output_video_packets"],
                "output": str(args.output),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
