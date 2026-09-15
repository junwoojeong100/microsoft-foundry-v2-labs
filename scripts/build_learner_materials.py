#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from foundry_workshop.materials import learner_files  # noqa: E402


def inventory(directory: Path) -> set[str]:
    if any(path.is_symlink() for path in (directory.parent.parent, directory.parent, directory)):
        raise ValueError("Do not access a generated learner directory through a symlink.")
    files = set()
    for path in directory.rglob("*"):
        if path.is_symlink():
            raise ValueError("Generated learner materials must not contain symlinks.")
        if path.is_file():
            files.add(path.relative_to(directory).as_posix())
    return files


def check(root: Path) -> list[str]:
    failures = []
    for language in ("ko", "en"):
        directory = root / "data/learner" / language
        try:
            actual = inventory(directory)
        except ValueError as exc:
            failures.append(f"{language}: {exc}")
            continue
        expected = learner_files(root, language)
        if actual != set(expected):
            failures.append(f"{language}: learner material file inventory differs.")
        for name, content in expected.items():
            path = directory / name
            if not path.is_file() or path.is_symlink() or path.read_bytes() != content:
                failures.append(
                    f"{language}/{name}: regenerate from the canonical synthetic sources."
                )
    return failures


def write(root: Path) -> None:
    planned = []
    for language in ("ko", "en"):
        directory = root / "data/learner" / language
        actual = inventory(directory)
        expected = learner_files(root, language)
        if actual - set(expected):
            raise ValueError(
                "Unexpected files in the generated learner directory; do not delete them implicitly."
            )
        planned.append((directory, expected))
    for directory, expected in planned:
        for name, content in expected.items():
            path = directory / name
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.is_symlink():
                raise ValueError("Do not write learner materials through a symlink.")
            path.write_bytes(content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check or explicitly regenerate the small browser-learner bundles; no Azure calls."
    )
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        if args.write:
            write(ROOT)
        failures = check(ROOT)
        for failure in failures:
            print("FAIL:", failure, file=sys.stderr)
        if failures:
            raise SystemExit(1)
        print(
            "Both learner bundles match their canonical prompts, synthetic policies and dev questions. No holdout or answer keys included."
        )
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
