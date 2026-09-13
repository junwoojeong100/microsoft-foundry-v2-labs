#!/usr/bin/env python3
"""Build chapter playback pages from verified split files and GitHub upload receipts."""

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit


def timestamp(seconds: float) -> str:
    value = round(seconds)
    hours, remainder = divmod(value, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes:02d}:{seconds:02d}"


def attachment_url(receipt: Path) -> str:
    url = json.loads(receipt.read_text(encoding="utf-8"))["url"]
    parsed = urlsplit(url)
    if (
        parsed.scheme != "https"
        or parsed.hostname != "github.com"
        or not parsed.path.startswith("/user-attachments/assets/")
    ):
        raise ValueError(f"Invalid repository media URL in {receipt.name}")
    return url


def build(parts_dir: Path, summary_receipt: Path, docs: Path, asset_run: str) -> dict:
    source = json.loads((parts_dir / "parts.json").read_text(encoding="utf-8"))
    if source["source_video_packets"] != source["output_video_packets"]:
        raise ValueError("The source timeline was not fully preserved.")
    summary = attachment_url(summary_receipt)
    parts = source["parts"]
    for item in parts:
        name = item["filename"]
        if Path(name).name != name or not name.endswith(".mp4"):
            raise ValueError("Unexpected segment filename.")
        path = parts_dir / name
        if path.stat().st_size != item["size_bytes"] or item["size_bytes"] >= 100_000_000:
            raise ValueError(f"Segment size changed or exceeds the limit: {name}")
        item["url"] = attachment_url(parts_dir / f"{path.stem}-upload.json")
        item["page"] = f"videos/{path.stem}.md"
        with path.open("rb") as handle:
            item["sha256"] = hashlib.file_digest(handle, "sha256").hexdigest()
    target = docs / "videos"
    if target.exists():
        raise FileExistsError("Preserve the existing chapter pages before rebuilding.")
    target.mkdir(parents=True)
    for index, item in enumerate(parts):
        suffix = (
            f" ({item['part']}/{item['parts_in_chapter']})" if item["parts_in_chapter"] > 1 else ""
        )
        title = item["title"] + suffix
        previous = parts[index - 1] if index else None
        following = parts[index + 1] if index + 1 < len(parts) else None
        navigation = ["[전체 영상 목차](../video-chapters.md)", "[실행 결과](../live-run.md)"]
        if previous:
            navigation.append(f"[이전 구간]({Path(previous['page']).name})")
        if following:
            navigation.append(f"[다음 구간]({Path(following['page']).name})")
        text = (
            f"# {item['chapter']:02d}. {title}\n\n"
            f"{' · '.join(navigation)}\n\n"
            f"**길이 {timestamp(item['duration_seconds'])} · {item['size_bytes'] / 1_000_000:.1f} MB · 원래 속도**\n\n"
            f"전체 녹화의 {timestamp(item['source_start_seconds'])}–{timestamp(item['source_end_seconds'])} 구간입니다.\n"
            "대기·진단·재시도를 포함하며, 재인코딩하거나 내용을 생략하지 않았습니다.\n\n"
            f"{item['url']}\n\n"
            "GitHub에 로그인한 상태이며 이 비공개 리포에 접근 권한이 있어야 재생할 수 있습니다.\n"
            f"플레이어를 사용할 수 없으면 [영상 파일 열기/다운로드]({item['url']})를 이용하세요.\n"
        )
        (docs / item["page"]).write_text(text, encoding="utf-8")
    rows = []
    for item in parts:
        suffix = (
            f" {item['part']}/{item['parts_in_chapter']}" if item["parts_in_chapter"] > 1 else ""
        )
        rows.append(
            f"| {item['chapter']:02d}{suffix} | {item['title']} | "
            f"{timestamp(item['source_start_seconds'])}–{timestamp(item['source_end_seconds'])} | "
            f"{timestamp(item['duration_seconds'])} | {item['size_bytes'] / 1_000_000:.1f} MB | "
            f"[재생]({item['page']}) · [다운로드]({item['url']}) |"
        )
    index = (
        "# 전체 녹화 — 실습 구간별 재생\n\n"
        f"**약 {source['source_duration_seconds'] / 60:.0f}분의 전체 과정을 {len(parts)}개 파일로 나눴습니다. 모든 파일은 100 MB 미만입니다.**\n\n"
        "[20분 배속본 재생](video-summary.md) · [실제 실행 결과](live-run.md)\n\n"
        "필요한 구간의 **재생**을 선택하면 해당 영상만 플레이어로 열립니다. "
        "영상은 같은 비공개 리포에 연결된 GitHub 동영상 첨부파일이며, 접근 권한이 있는 계정으로 로그인해야 합니다.\n\n"
        "| 구간 | 내용 | 전체본 위치 | 길이 | 파일 크기 | 링크 |\n"
        "|---|---|---|---:|---:|---|\n" + "\n".join(rows) + "\n\n## 분할 기준\n\n"
        "- 대기시간을 포함한 원래 순서를 유지했습니다. 분할은 총용량을 줄이는 압축 작업이 아닙니다.\n"
        f"- 재인코딩 없이 keyframe 경계에서 나눴으며, 원본과 분할본의 영상 packet 수는 모두 **{source['source_video_packets']:,}개**입니다.\n"
        f"- 긴 MAF/평가 구간은 두 파일로 나눴습니다. 가장 큰 파일은 약 **{max(item['size_bytes'] for item in parts) / 1_000_000:.1f} MB**입니다.\n"
        "- 영상 본문은 Git 히스토리에 추가하지 않았습니다. 기존에 커밋했던 20분 파일의 과거 이력은 재작성하지 않습니다.\n"
        "- 로그인 화면 제외와 식별정보 가림은 분할본에도 그대로 유지됩니다.\n\n"
        f"[파일별 메타데이터·SHA-256](assets/{asset_run}/video-parts.json)\n"
    )
    (docs / "video-chapters.md").write_text(index, encoding="utf-8")
    (docs / "video-summary.md").write_text(
        "# 20분 배속본 재생\n\n"
        "[구간별 원래 속도 영상](video-chapters.md) · [실제 실행 결과](live-run.md)\n\n"
        "**20분 · 67.7 MB · 약 5.55배속**입니다. 대기시간도 배속되어 있으며 제거된 것은 아닙니다.\n\n"
        f"{summary}\n\n"
        "GitHub에 로그인하고 이 비공개 리포의 접근 권한이 있는지 확인하세요.\n"
        f"필요하면 [영상 파일 열기/다운로드]({summary})를 이용할 수 있습니다.\n\n"
        "이전 MP4 blob 링크 대신 GitHub가 실제 `<video>` 플레이어로 렌더링하는 첨부 링크를 사용합니다. "
        "headless Edge에서 재생 진행과 10분 지점 탐색을 확인했습니다.\n",
        encoding="utf-8",
    )
    report = {
        "recorded_on": "2026-09-13",
        "repository": "junwoojeong100/microsoft-foundry-v2-labs",
        "hosting": "repository-scoped GitHub user attachments",
        "private_repository_authentication_required": True,
        "source_duration_seconds": source["source_duration_seconds"],
        "source_video_packets": source["source_video_packets"],
        "output_video_packets": source["output_video_packets"],
        "reencoded": False,
        "waiting_time_removed": False,
        "summary_url": summary,
        "parts": parts,
    }
    asset_dir = docs / "assets" / asset_run
    asset_dir.mkdir(parents=True, exist_ok=True)
    (asset_dir / "video-parts.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parts-dir", type=Path, required=True)
    parser.add_argument("--summary-receipt", type=Path, required=True)
    parser.add_argument("--docs", type=Path, default=Path("docs"))
    parser.add_argument("--asset-run", required=True)
    args = parser.parse_args()
    result = build(args.parts_dir, args.summary_receipt, args.docs, args.asset_run)
    print(
        f"Built {len(result['parts'])} chapter playback pages and a verified summary player page."
    )
