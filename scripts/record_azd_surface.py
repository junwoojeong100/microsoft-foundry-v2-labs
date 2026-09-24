#!/usr/bin/env python3
"""Record the local azd help surface for every azd command used in the guides.

Maintainer tool; read-only. It runs `azd <command> --help`, `azd version` and `azd ext list`
only, and writes scripts/azd-surface.json for check_docs.py. Re-record after upgrading azd or
its Foundry extensions, then review the diff before changing guide commands.
"""

import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_docs import azd_command_paths, markdown_files  # noqa: E402

OUTPUT = ROOT / "scripts/azd-surface.json"


def run(arguments: list[str]) -> str:
    result = subprocess.run(
        ["azd", *arguments], capture_output=True, text=True, timeout=60, check=True
    )
    return result.stdout


def help_flags(text: str) -> list[str]:
    flags, section = set(), False
    for line in text.splitlines():
        if line.strip().rstrip(":") in {"Flags", "Global Flags"}:
            section = True
            continue
        if section and not line.startswith(" "):
            section = False
        if section:
            match = re.match(r"\s+(?:-\w,\s+)?(--[a-z][a-z0-9-]*)", line)
            if match:
                flags.add(match.group(1))
    return sorted(flags)


def record(root: Path) -> dict:
    paths = set()
    for path in markdown_files(root):
        paths.update(azd_command_paths(path.read_text(encoding="utf-8")))
    commands = {}
    for command in sorted(paths):
        flags = help_flags(run([*command.split(), "--help"]))
        if not flags:
            raise ValueError(f"No flags parsed for azd {command}; inspect its help output.")
        commands[command] = flags
    version = json.loads(run(["version", "--output", "json"]))["azd"]["version"]
    extensions = {
        item["id"]: item.get("installedVersion") or item.get("version")
        for item in json.loads(run(["ext", "list", "--installed", "--output", "json"]))
    }
    return {
        "recorded_at": datetime.now(UTC).date().isoformat(),
        "azd_version": version,
        "extensions": dict(sorted(extensions.items())),
        "commands": commands,
        "note": "Local help snapshot; not proof that a command succeeds in Azure.",
    }


if __name__ == "__main__":
    snapshot = record(ROOT)
    OUTPUT.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    print(f"Recorded {len(snapshot['commands'])} azd commands to {OUTPUT.relative_to(ROOT)}")
