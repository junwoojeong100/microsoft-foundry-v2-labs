#!/usr/bin/env python3
import contextlib
import io
import os
import re
import shlex
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from foundry_workshop.cli import parser  # noqa: E402

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


def check(root: Path) -> tuple[list[str], dict[str, int]]:
    errors = []
    counts = {"markdown_files": 0, "local_links": 0, "cli_examples": 0}
    for path in markdown_files(root):
        counts["markdown_files"] += 1
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(root)
        outside_code = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", outside_code):
            target = target.strip().split(' "')[0]
            url = urlsplit(target)
            if url.scheme or target.startswith("#"):
                continue
            destination = (path.parent / unquote(url.path)).resolve()
            counts["local_links"] += 1
            if not destination.is_relative_to(root.resolve()) or not destination.exists():
                errors.append(f"{relative}: broken/out-of-scope link {target}")
        joined = text.replace("\\\n", " ")
        for line in joined.splitlines():
            line = line.strip()
            if not re.match(r"python(?:3(?:\.13)?)? scripts/workshop\.py(?: |$)", line):
                continue
            command = shlex.split(line)
            for separator in ("&&", ">", "2>", "|"):
                if separator in command:
                    command = command[: command.index(separator)]
            counts["cli_examples"] += 1
            try:
                with (
                    contextlib.redirect_stderr(io.StringIO()),
                    contextlib.redirect_stdout(io.StringIO()),
                ):
                    parser().parse_args(command[2:])
            except SystemExit as exc:
                if exc.code:
                    errors.append(f"{relative}: invalid CLI example: {line}")
    expected = [f"{index:02d}-" for index in range(12)]
    actual = [path.name[:3] for path in (root / "docs/labs").glob("*.md")]
    if sorted(actual) != expected:
        errors.append("Expected exactly the twelve numbered lab modules 00-11.")
    return errors, counts


if __name__ == "__main__":
    failures, counts = check(ROOT)
    for failure in failures:
        print("FAIL:", failure, file=sys.stderr)
    print(counts)
    raise SystemExit(1 if failures else 0)
