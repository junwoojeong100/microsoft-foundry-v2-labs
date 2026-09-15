#!/usr/bin/env python3
import argparse
import hashlib
import json
import shutil
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from foundry_workshop.profiles import PROFILE_FILENAME, RuntimeProfile  # noqa: E402


def build(root: Path, profile: RuntimeProfile | None = None) -> Path:
    profile = RuntimeProfile() if profile is None else profile
    destination = root / ".build" / profile.package_name
    if destination.exists():
        raise ValueError(
            "The hosted package already exists. Preserve or remove that exact generated directory before rebuilding."
        )
    configuration = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = []
    for extra in ("cloud", "agents", "hosted"):
        for requirement in configuration["project"]["optional-dependencies"][extra]:
            if requirement.startswith(configuration["project"]["name"] + "["):
                continue
            if "==" not in requirement:
                raise ValueError(f"Direct hosted dependency is not pinned: {requirement}")
            if requirement not in dependencies:
                dependencies.append(requirement)
    destination.mkdir(parents=True)
    shutil.copytree(
        root / "src/foundry_workshop",
        destination / "foundry_workshop",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    shutil.copytree(root / "data/knowledge", destination / "data/knowledge")
    shutil.copytree(root / "prompts", destination / "prompts")
    for name in ("main.py", ".agentignore"):
        shutil.copy2(root / "examples/hosted" / name, destination / name)
    (destination / PROFILE_FILENAME).write_text(
        json.dumps({"schema_version": 1, "profile": profile.to_dict()}, indent=2) + "\n",
        encoding="utf-8",
    )
    (destination / "requirements.txt").write_text("\n".join(dependencies) + "\n", encoding="utf-8")
    files = {}
    for path in sorted(destination.rglob("*")):
        if path.is_file():
            files[path.relative_to(destination).as_posix()] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
    (destination / "package-manifest.json").write_text(
        json.dumps(
            {
                "edition": configuration["project"]["version"],
                "files": files,
                "excludes": [
                    ".env",
                    ".foundry",
                    "eval YAML configs",
                    "outputs",
                    "evaluation datasets",
                    "holdout",
                    "virtualenv",
                    "credentials",
                ],
                "dependency_policy": "Direct versions pinned; record resolved dependencies from the actual remote build.",
                "cloud_deployed": False,
                "runtime_profile": profile.to_dict(),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build a secret-free, profile-pinned Hosted package."
    )
    parser.add_argument("--kind", choices=("policy", "workflow"), default="policy")
    parser.add_argument(
        "--pattern", choices=("sequential", "concurrent", "group-chat"), default="sequential"
    )
    parser.add_argument("--retrieval", choices=("local", "search", "iq", "hybrid"), default="local")
    parser.add_argument("--prompt", choices=("v1", "v2"), default="v2")
    parser.add_argument(
        "--api", choices=("project-responses", "account-chat"), default="project-responses"
    )
    parser.add_argument("--protocol", choices=("responses", "invocations"), default="responses")
    parser.add_argument("--language", choices=("ko", "en"), default="ko")
    args = parser.parse_args()
    try:
        print(build(ROOT, RuntimeProfile(**vars(args))))
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
