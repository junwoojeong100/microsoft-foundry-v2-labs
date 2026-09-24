#!/usr/bin/env python3
"""Report drift between pinned SDK versions and the latest PyPI releases.

Read-only and advisory: it never edits pins or installs packages. Newer releases still need
installation, SDK contract checks and separately recorded live verification before adoption.
"""

import argparse
import json
import os
import re
import tomllib
import urllib.request
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRAS = ("cloud", "agents", "hosted", "dev")


def pinned_requirements(root: Path) -> dict[str, str]:
    configuration = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    project = configuration["project"]["name"]
    pins = {}
    for extra in EXTRAS:
        for requirement in configuration["project"]["optional-dependencies"][extra]:
            if requirement.startswith(project + "["):
                continue
            name, separator, version = requirement.partition("==")
            if not separator:
                raise ValueError(f"Unpinned requirement: {requirement}")
            pins[name] = version
    return pins


def release(version: str) -> tuple[int, ...]:
    match = re.match(r"(\d+(?:\.\d+)*)", version)
    if match is None:
        raise ValueError(f"Unrecognized version: {version}")
    return tuple(int(part) for part in match.group(1).split("."))


def classify(pinned: str, latest: str) -> str:
    if pinned == latest:
        return "current"
    old, new = release(pinned), release(latest)
    width = max(len(old), len(new), 3)
    old, new = old + (0,) * (width - len(old)), new + (0,) * (width - len(new))
    if new < old:
        return "pinned-newer"
    if new[0] != old[0]:
        return "major"
    if new[1] != old[1]:
        return "minor"
    return "patch" if new[:3] != old[:3] else "prerelease"


def fetch_latest(name: str) -> str:
    with urllib.request.urlopen(f"https://pypi.org/pypi/{name}/json", timeout=20) as response:
        return json.load(response)["info"]["version"]


def report(root: Path, fetch: Callable[[str], str] = fetch_latest) -> dict:
    packages = []
    for name, pinned in sorted(pinned_requirements(root).items()):
        try:
            latest = fetch(name)
            drift = classify(pinned, latest)
        except (OSError, ValueError, KeyError) as exc:
            latest, drift = None, f"unavailable: {type(exc).__name__}"
        packages.append({"name": name, "pinned": pinned, "latest": latest, "drift": drift})
    return {
        "checked_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "source": "https://pypi.org/pypi/<package>/json",
        "packages": packages,
        "major_drift": [item["name"] for item in packages if item["drift"] == "major"],
        "unavailable": [item["name"] for item in packages if item["latest"] is None],
        "pins_changed": False,
        "note": "Advisory only. Verify newer releases offline and live before changing pins.",
    }


def markdown(result: dict) -> str:
    lines = ["| Package | Pinned | Latest on PyPI | Drift |", "|---|---|---|---|"]
    for item in result["packages"]:
        lines.append(
            f"| `{item['name']}` | {item['pinned']} | {item['latest']} | {item['drift']} |"
        )
    return "\n".join(["### SDK pin drift", "", *lines, "", result["note"], ""])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fail-on-major", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Also fail when PyPI is unreachable.")
    args = parser.parse_args()
    result = report(ROOT)
    print(json.dumps(result, indent=2))
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as handle:
            handle.write(markdown(result))
    failed = (args.fail_on_major and result["major_drift"]) or (
        args.strict and result["unavailable"]
    )
    raise SystemExit(1 if failed else 0)
