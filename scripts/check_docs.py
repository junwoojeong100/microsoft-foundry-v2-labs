#!/usr/bin/env python3
import contextlib
import hashlib
import io
import os
import re
import shlex
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from foundry_workshop.cli import parser  # noqa: E402
from foundry_workshop.contracts import read_json  # noqa: E402

IGNORED = {
    ".git",
    ".venv",
    ".build",
    ".azure",
    ".foundry",
    "__pycache__",
    "outputs",
    "site",
    "dist",
}


def markdown_files(root: Path):
    for parent, directories, files in os.walk(root):
        directories[:] = [
            name for name in directories if name not in IGNORED and not name.endswith(".egg-info")
        ]
        for name in files:
            if name.endswith(".md"):
                yield Path(parent) / name


def heading_ids(text: str) -> set[str]:
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    result = set(re.findall(r'<(?:a|h[1-6])\b[^>]*\bid=["\']([^"\']+)', text))
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.MULTILINE):
        heading = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", heading)
        heading = re.sub(r"<[^>]+>", "", heading).replace("`", "").replace("*", "")
        slug = "".join(
            char
            for char in heading.lower()
            if char in " -_" or unicodedata.category(char)[0] in "LN"
        ).replace(" ", "-")
        unique, suffix = slug, 0
        while unique in result:
            suffix += 1
            unique = f"{slug}-{suffix}"
        result.add(unique)
    return result


def workshop_commands(text: str) -> list[tuple[str, list[str]]]:
    commands = []
    for line in text.replace("\\\n", " ").splitlines():
        line = line.strip()
        if not re.match(r"python(?:3(?:\.13)?)? scripts/workshop\.py(?: |$)", line):
            continue
        command = shlex.split(line)
        for separator in ("&&", ">", "2>", "|"):
            if separator in command:
                command = command[: command.index(separator)]
        commands.append((line, command[2:]))
    return commands


def translation_pairs(root: Path) -> list[tuple[Path, Path]]:
    english = {
        path.relative_to(root / "docs")
        for path in (root / "docs").rglob("*.md")
        if path.relative_to(root / "docs").parts[0] not in {"ko", "assets"}
    }
    korean = {path.relative_to(root / "docs/ko") for path in (root / "docs/ko").rglob("*.md")}
    return [
        (root / "README.md", root / "README.ko.md"),
        (root / "data/README.md", root / "data/README.ko.md"),
        (root / "data/fixtures/README.md", root / "data/fixtures/README.ko.md"),
        *((root / "docs" / path, root / "docs/ko" / path) for path in sorted(english | korean)),
    ]


def command_translations(root: Path, errors: list[str]) -> dict[str, str]:
    path = root / "data/guide-questions.json"
    if not path.exists():
        return {}
    try:
        value = read_json(path)
        pairs = value["pairs"]
        if value.get("schema_version") != 1 or not isinstance(pairs, list):
            raise ValueError("Expected a versioned list of explicit guide translations.")
        mapping = {}
        sources = set()
        for pair in pairs:
            if set(pair) != {"ko", "en"} or any(
                not isinstance(pair[key], str) or not pair[key].strip() for key in ("ko", "en")
            ):
                raise ValueError("Guide translations need nonempty Korean and English text.")
            if pair["en"] in mapping or pair["ko"] in sources:
                raise ValueError("Guide translation pairs must be unique.")
            sources.add(pair["ko"])
            mapping[pair["en"]] = pair["ko"]
        return mapping
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"data/guide-questions.json: invalid command translation map: {exc}")
        return {}


def normalized_command(arguments: list[str], translations: dict[str, str]) -> list[str]:
    result = list(arguments)
    language = None
    if "--language" in result:
        index = result.index("--language")
        if index + 1 < len(result) and result[index + 1] in {"ko", "en"}:
            language = result[index + 1]
            del result[index : index + 2]
    if "prepare-extensions" in result and "--label" in result and language is not None:
        index = result.index("--label") + 1
        if index < len(result) and result[index] == f"extensions-{language}":
            result[index] = "extensions-<language>"
    for option in ("--question", "--reason"):
        if option in result:
            index = result.index(option) + 1
            if index < len(result):
                result[index] = translations.get(result[index], result[index])
    return result


def pending_translations(root: Path, errors: list[str]) -> set[Path]:
    path = root / "docs/localization.json"
    if not path.exists():
        return set()
    try:
        state = read_json(path)
    except (OSError, ValueError) as exc:
        errors.append(f"docs/localization.json: invalid localization state: {exc}")
        return set()
    if (
        not isinstance(state, dict)
        or type(state.get("schema_version")) is not int
        or state["schema_version"] != 1
        or state.get("source_language") not in {"ko", "en"}
        or not isinstance(state.get("revision"), str)
        or not re.fullmatch(r"[a-z0-9-]+", state["revision"])
        or not isinstance(state.get("pending_files"), dict)
    ):
        errors.append("docs/localization.json: expected explicit, versioned localization state.")
        return set()
    pairs = {
        english.relative_to(root).as_posix(): (english, korean)
        for english, korean in translation_pairs(root)
    }
    valid = set()
    for name, record in state["pending_files"].items():
        if name not in pairs or not isinstance(record, dict):
            errors.append(f"docs/localization.json: unknown language pair {name}.")
            continue
        english, korean = pairs[name]
        if not english.is_file() or not korean.is_file():
            errors.append(f"{name}: pending translation still requires both language entry pages.")
            continue
        hashes = {
            "english_sha256": hashlib.sha256(english.read_bytes()).hexdigest(),
            "korean_sha256": hashlib.sha256(korean.read_bytes()).hexdigest(),
        }
        if record != hashes:
            errors.append(
                f"{name}: localization hashes changed; review and update the explicit pending record."
            )
            continue
        target = english if state["source_language"] == "ko" else korean
        warning = (
            "**Translation pending**" if state["source_language"] == "ko" else "**번역 준비 중**"
        )
        beginning = target.read_text(encoding="utf-8")[:1200]
        marker = f"<!-- translation-pending: {state['revision']} -->"
        if marker not in beginning or warning not in beginning:
            errors.append(
                f"{target.relative_to(root)}: readers must see the source-first revision warning."
            )
            continue
        valid.add(english)
    return valid


def check(root: Path) -> tuple[list[str], dict[str, int]]:
    errors = []
    pending = pending_translations(root, errors)
    translations = command_translations(root, errors)
    counts = {
        "markdown_files": 0,
        "local_links": 0,
        "local_anchors": 0,
        "cli_examples": 0,
        "language_pairs": 0,
        "pending_translations": len(pending),
    }
    for path in markdown_files(root):
        counts["markdown_files"] += 1
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(root)
        outside_code = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", outside_code):
            target = target.strip().split(' "')[0]
            url = urlsplit(target)
            if url.scheme:
                continue
            destination = (
                (path.parent / unquote(url.path)).resolve() if url.path else path.resolve()
            )
            counts["local_links"] += 1
            if not destination.is_relative_to(root.resolve()) or not destination.exists():
                errors.append(f"{relative}: broken/out-of-scope link {target}")
            elif url.fragment and destination.suffix == ".md":
                counts["local_anchors"] += 1
                if unquote(url.fragment) not in heading_ids(
                    destination.read_text(encoding="utf-8")
                ):
                    errors.append(f"{relative}: broken heading link {target}")
        try:
            commands = workshop_commands(text)
        except ValueError as exc:
            errors.append(f"{relative}: invalid command quoting: {exc}")
            commands = []
        for line, arguments in commands:
            counts["cli_examples"] += 1
            try:
                with (
                    contextlib.redirect_stderr(io.StringIO()),
                    contextlib.redirect_stdout(io.StringIO()),
                ):
                    parser().parse_args(arguments)
            except SystemExit as exc:
                if exc.code:
                    errors.append(f"{relative}: invalid CLI example: {line}")
    expected = [f"{index:02d}-" for index in range(12)]
    for directory in ("docs/labs", "docs/ko/labs"):
        actual = [path.name[:3] for path in (root / directory).glob("*.md")]
        if sorted(actual) != expected:
            errors.append(f"{directory}: expected exactly the twelve numbered lab modules 00-11.")
    for english, korean in translation_pairs(root):
        if not english.is_file() or not korean.is_file():
            errors.append(f"Missing language counterpart: {english.relative_to(root)}.")
            continue
        counts["language_pairs"] += 1
        if (
            any(
                "<!-- translation-pending:" in path.read_text(encoding="utf-8")[:1200]
                for path in (english, korean)
            )
            and english not in pending
        ):
            errors.append(
                f"{english.relative_to(root)}: a pending translation needs a valid hash-bound record."
            )
        for path, counterpart, language in ((english, korean, "en"), (korean, english, "ko")):
            text = path.read_text(encoding="utf-8")
            target = os.path.relpath(counterpart, path.parent)
            navigation = (
                f"**English** | [한국어]({target})"
                if language == "en"
                else f"[English]({target}) | **한국어**"
            )
            if navigation not in text.split("\n\n", 2)[1:2]:
                errors.append(f"{path.relative_to(root)}: missing reciprocal language navigation.")
        try:
            english_commands = [
                normalized_command(args, translations)
                for _, args in workshop_commands(english.read_text())
            ]
            korean_commands = [
                normalized_command(args, translations)
                for _, args in workshop_commands(korean.read_text())
            ]
        except ValueError:
            continue  # Invalid quoting was reported during the per-file check.
        if english_commands != korean_commands and english not in pending:
            errors.append(f"{english.relative_to(root)}: English/Korean CLI examples differ.")
    return errors, counts


if __name__ == "__main__":
    failures, counts = check(ROOT)
    for failure in failures:
        print("FAIL:", failure, file=sys.stderr)
    print(counts)
    raise SystemExit(1 if failures else 0)
