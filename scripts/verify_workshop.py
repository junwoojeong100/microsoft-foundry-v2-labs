#!/usr/bin/env python3
"""Run the workshop's local quality gates and save a hash-bound report. No Azure calls."""

import argparse
import hashlib
import os
import platform
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from foundry_workshop.contracts import digest, safe_label, write_json  # noqa: E402

CHECKS = (
    ("ruff-lint", ("-m", "ruff", "check", ".")),
    ("ruff-format", ("-m", "ruff", "format", "--check", ".")),
    (
        "python-compile",
        ("-m", "compileall", "-q", "src", "scripts", "examples", "tests", "tests_sdk"),
    ),
    ("offline-tests", ("-m", "unittest", "discover", "-s", "tests", "-t", ".", "-q")),
    ("documentation", ("scripts/check_docs.py",)),
    ("learner-bundles", ("scripts/build_learner_materials.py",)),
)
SDK_CHECKS = (
    ("installed-dependencies", ("-m", "pip", "check")),
    ("sdk-contracts", ("scripts/check_sdk.py",)),
    ("sdk-tests", ("-m", "unittest", "discover", "-s", "tests_sdk", "-t", ".", "-q")),
)


def timestamp() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def source_fingerprint(root: Path) -> str:
    paths = set()
    for directory, suffixes in (
        ("src", {".py"}),
        ("scripts", {".py", ".json"}),
        ("examples", {".py", ".yaml", ".example"}),
        ("tests", {".py"}),
        ("tests_sdk", {".py"}),
        ("docs", {".md", ".json"}),
        ("data", {".json", ".jsonl", ".txt", ".csv", ".zip"}),
        ("prompts", {".txt"}),
        (".github/workflows", {".yml", ".yaml"}),
    ):
        paths.update(
            path
            for path in (root / directory).rglob("*")
            if path.is_file() and path.suffix in suffixes and "__pycache__" not in path.parts
        )
    paths.update(
        root / name
        for name in (
            "README.md",
            "README.ko.md",
            "AGENTS.md",
            "pyproject.toml",
            "requirements.lock.txt",
            "azure.yaml",
            ".env.example",
            ".python-version",
        )
        if (root / name).is_file()
    )
    if not paths:
        raise ValueError("No workshop source files were found.")
    for path in paths:
        if (
            path.is_symlink()
            or any(
                parent.is_symlink()
                for parent in path.parents
                if parent != root and parent.is_relative_to(root)
            )
            or not path.resolve().is_relative_to(root.resolve())
        ):
            raise ValueError(
                f"Do not fingerprint redirected source files: {path.relative_to(root)}"
            )
    return digest(
        {
            path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(paths)
        }
    )


def prepare_report(root: Path, label: str) -> Path:
    directory = root
    for index, part in enumerate(("outputs", "verification", safe_label(label))):
        directory /= part
        if directory.is_symlink():
            raise ValueError("Verification reports must not follow directory symlinks.")
        directory.mkdir(exist_ok=index < 2)
    return directory / "report.json"


def verify(root: Path, label: str, *, sdk: bool = False) -> tuple[dict, Path]:
    if sdk and sys.version_info[:2] != (3, 13):
        raise ValueError("Installed SDK checks require Python 3.13; no interpreter is substituted.")
    fingerprint = source_fingerprint(root)
    path = prepare_report(root, label)
    selected = CHECKS + SDK_CHECKS if sdk else CHECKS
    result = {
        "schema_version": 1,
        "mode": "offline-verification",
        "label": label,
        "started_at": timestamp(),
        "finished_at": None,
        "python": platform.python_version(),
        "platform": platform.system(),
        "source_before_sha256": fingerprint,
        "source_after_sha256": None,
        "source_unchanged": None,
        "status": "running",
        "sdk_checks_selected": sdk,
        "azure_tested": False,
        "learner_pilot_performed": False,
        "global_ranking_established": False,
        "deployment_approved": False,
        "checks": [
            {"name": name, "command": ["python", *arguments], "status": "not-run"}
            for name, arguments in selected
        ],
    }
    write_json(path, result, overwrite=False)
    environment = {**os.environ, "OTEL_SDK_DISABLED": "true"}
    try:
        for check, (_, arguments) in zip(result["checks"], selected, strict=True):
            check["status"] = "running"
            write_json(path, result)
            print(f"\n[{check['name']}] {' '.join(check['command'])}", flush=True)
            start = time.monotonic()
            try:
                process = subprocess.run(
                    [sys.executable, *arguments],
                    cwd=root,
                    env=environment,
                    text=True,
                    capture_output=True,
                    timeout=900,
                    check=False,
                )
                check["exit_code"] = process.returncode
                check["status"] = "passed" if process.returncode == 0 else "failed"
                for stream, destination in (
                    (process.stdout, sys.stdout),
                    (process.stderr, sys.stderr),
                ):
                    if stream:
                        print(stream, file=destination, end="" if stream.endswith("\n") else "\n")
            except (OSError, subprocess.TimeoutExpired) as exc:
                check.update(status="failed", exit_code=None, failure=type(exc).__name__)
                print(f"FAIL: {check['name']}: {exc}", file=sys.stderr)
            check["duration_seconds"] = round(time.monotonic() - start, 3)
            write_json(path, result)
        result["source_after_sha256"] = source_fingerprint(root)
        result["source_unchanged"] = result["source_after_sha256"] == fingerprint
        result["status"] = (
            "passed"
            if result["source_unchanged"]
            and all(check["status"] == "passed" for check in result["checks"])
            else "failed"
        )
        if not result["source_unchanged"]:
            print(
                "FAIL: workshop source changed during verification; use a fresh label after review.",
                file=sys.stderr,
            )
    except (OSError, ValueError) as exc:
        result.update(status="failed", evidence_error=type(exc).__name__)
        print(f"FAIL: verification evidence could not be completed: {exc}", file=sys.stderr)
    except KeyboardInterrupt:
        result["status"] = "interrupted"
        for check in result["checks"]:
            if check["status"] == "running":
                check["status"] = "interrupted"
        print("FAIL: verification interrupted; unfinished checks remain not-run.", file=sys.stderr)
    finally:
        result["finished_at"] = timestamp()
        write_json(path, result)
    return result, path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--label", required=True, help="Fresh name for outputs/verification/<label>/report.json."
    )
    parser.add_argument(
        "--sdk",
        action="store_true",
        help="Also run installed-SDK checks with mock transports; Python 3.13 only.",
    )
    args = parser.parse_args(argv)
    try:
        result, path = verify(ROOT, args.label, sdk=args.sdk)
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2
    print(f"\nOffline verification: {result['status']}. Report: {path.relative_to(ROOT)}")
    print(f"Source SHA-256: {result['source_before_sha256']}")
    print("No live Azure, learner-pilot, model-quality or global-ranking claim is established.")
    if result["status"] == "passed":
        return 0
    if result["status"] == "interrupted":
        return 130
    return 2 if "evidence_error" in result else 1


if __name__ == "__main__":
    raise SystemExit(main())
