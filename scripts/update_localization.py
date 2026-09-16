#!/usr/bin/env python3
import argparse
import hashlib
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from check_docs import (  # noqa: E402
    command_translations,
    normalized_command,
    translation_pairs,
    workshop_commands,
)

from foundry_workshop.contracts import read_json, write_json  # noqa: E402


def mark_pending(root: Path, names: list[str], source: str, revision: str) -> dict:
    if source not in {"en", "ko"} or not re.fullmatch(r"[a-z0-9-]+", revision):
        raise ValueError("Choose an explicit source language and lowercase revision name.")
    pairs = {
        english.relative_to(root).as_posix(): (english, korean)
        for english, korean in translation_pairs(root)
    }
    if not names or len(names) != len(set(names)) or any(name not in pairs for name in names):
        raise ValueError("List unique, existing English-path language pairs explicitly.")
    path = root / "docs/localization.json"
    state = read_json(path) if path.exists() else {"pending_files": {}}
    if state["pending_files"] and (
        state.get("source_language") != source or state.get("revision") != revision
    ):
        raise ValueError("Finish or review the current pending revision before changing direction.")
    state.update(schema_version=1, source_language=source, revision=revision)
    planned = []
    for name in names:
        english, korean = pairs[name]
        original, target = (english, korean) if source == "en" else (korean, english)
        if not original.is_file() or original.is_symlink() or target.is_symlink():
            raise ValueError(
                "The source must be a real file; do not follow documentation symlinks."
            )
        relative = os.path.relpath(original, target.parent)
        if target.exists():
            text = target.read_text(encoding="utf-8")
        else:
            navigation = (
                f"[English]({relative}) | **한국어**"
                if source == "en"
                else f"**English** | [한국어]({relative})"
            )
            title = original.read_text(encoding="utf-8").splitlines()[0]
            text = title + "\n\n" + navigation + "\n"
        if "<!-- translation-pending:" not in text:
            warning = (
                f"> **번역 준비 중** — 영어 가이드의 실행·촬영·보완 후 이 페이지를 한국어로 갱신합니다. "
                f"[현재 영어 가이드]({relative})를 확인하세요. 기존 국문 자료를 새 기능의 실행 증거로 사용하지 않습니다."
                if source == "en"
                else f"> **Translation pending** — this page will follow the Korean execution and media review. "
                f"[Read the current Korean guide]({relative}); older English evidence does not verify new features."
            )
            paragraphs = text.split("\n\n")
            paragraphs.insert(2, f"<!-- translation-pending: {revision} -->\n\n{warning}")
            text = "\n\n".join(paragraphs).rstrip() + "\n"
        elif f"<!-- translation-pending: {revision} -->" not in text:
            raise ValueError("A target contains another revision's pending marker.")
        planned.append((name, english, korean, target, text))
    for name, english, korean, target, text in planned:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        state["pending_files"][name] = {
            "english_sha256": hashlib.sha256(english.read_bytes()).hexdigest(),
            "korean_sha256": hashlib.sha256(korean.read_bytes()).hexdigest(),
        }
    write_json(path, state)
    return state


def mark_complete(root: Path, names: list[str], source: str, revision: str) -> dict:
    path = root / "docs/localization.json"
    state = read_json(path)
    if state.get("source_language") != source or state.get("revision") != revision:
        raise ValueError("Complete only the active explicit source-language revision.")
    if (
        not names
        or len(names) != len(set(names))
        or any(name not in state["pending_files"] for name in names)
    ):
        raise ValueError("List only unique pending language pairs.")
    pairs = {
        english.relative_to(root).as_posix(): (english, korean)
        for english, korean in translation_pairs(root)
    }
    errors = []
    translations = command_translations(root, errors)
    if errors:
        raise ValueError("; ".join(errors))
    completed = {}
    for name in names:
        english, korean = pairs[name]
        texts = [file.read_text() for file in (english, korean)]
        if any("<!-- translation-pending:" in text for text in texts):
            raise ValueError(f"{name}: remove the pending notice only after completing the guide.")
        commands = [
            [normalized_command(args, translations) for _, args in workshop_commands(text)]
            for text in texts
        ]
        if commands[0] != commands[1]:
            raise ValueError(f"{name}: English/Korean executable commands differ.")
        completed[name] = {
            "revision": revision,
            "pending_source_record": state["pending_files"][name],
            "english_sha256_at_completion": hashlib.sha256(english.read_bytes()).hexdigest(),
            "korean_sha256_at_completion": hashlib.sha256(korean.read_bytes()).hexdigest(),
            "cli_parity_verified": True,
        }
    state.setdefault("completed_translations", {}).update(completed)
    for name in names:
        del state["pending_files"][name]
    write_json(path, state)
    return state


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Explicitly mark source-first documentation work; no translation or Azure calls."
    )
    parser.add_argument("--source", choices=("en", "ko"), required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--complete", action="store_true")
    parser.add_argument("english_paths", nargs="+")
    args = parser.parse_args()
    try:
        operation = mark_complete if args.complete else mark_pending
        result = operation(ROOT, args.english_paths, args.source, args.revision)
        print(
            f"Recorded {len(result['pending_files'])} hash-bound pending translations from {args.source}."
        )
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
