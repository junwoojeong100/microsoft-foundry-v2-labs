#!/usr/bin/env python3
import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from foundry_workshop.cli import parser as workshop_parser  # noqa: E402
from foundry_workshop.contracts import safe_label  # noqa: E402


def redact(value: str) -> str:
    value = value.replace(str(ROOT), "{workspace}")
    value = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[account redacted]", value)
    value = re.sub(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
        "[identifier redacted]",
        value,
        flags=re.IGNORECASE,
    )
    return re.sub(r"(?i)(Bearer\s+)[A-Za-z0-9._~+/-]+", r"\1[redacted]", value)


def save_state(path: Path, value: dict) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Record a real, finite workshop CLI step for the headless video."
    )
    parser.add_argument("--run", required=True)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--kind", choices=("workshop", "package", "azd"), default="workshop")
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    run = safe_label(args.run)
    stage = safe_label(args.stage)
    arguments = args.arguments[1:] if args.arguments[:1] == ["--"] else args.arguments
    if args.kind == "workshop":
        command_args = workshop_parser().parse_args(arguments)
        if command_args.command == "serve":
            raise ValueError(
                "Start long-lived servers separately; this recorder captures finite CLI commands only."
            )
    elif args.kind == "package" and arguments:
        raise ValueError("The package step does not accept additional commands.")
    elif args.kind == "azd":
        prefixes = [
            ("deploy",),
            ("ai", "agent", "init"),
            ("ai", "agent", "show"),
            ("ai", "agent", "invoke"),
            ("ai", "agent", "doctor"),
            ("ai", "agent", "sessions", "list"),
            ("ai", "agent", "sessions", "stop"),
        ]
        if not any(tuple(arguments[: len(prefix)]) == prefix for prefix in prefixes):
            raise ValueError("This azd operation is not a supported recording step.")
    if not 1 <= args.timeout <= 1800:
        raise ValueError("Timeout must be 1-1800 seconds.")
    directory = ROOT / "outputs" / run
    result_dir = directory / "results"
    viewer = directory / "viewer"
    result_dir.mkdir(parents=True, exist_ok=True)
    viewer.mkdir(parents=True, exist_ok=True)
    result_file = result_dir / f"{stage}.json"
    if result_file.exists():
        raise FileExistsError(f"Preserve the existing stage evidence: {result_file}")
    shutil.copy2(ROOT / "recording/live-console.html", viewer / "index.html")
    interpreter = ROOT / ".venv/bin/python"
    if not interpreter.is_file():
        raise FileNotFoundError("Prepare the project .venv before recording cloud steps.")
    # Keep the venv symlink path rather than invoking the base interpreter.
    if args.kind == "workshop":
        command = [str(interpreter), str(ROOT / "scripts/workshop.py"), *arguments]
        display_command = ["python", "scripts/workshop.py", *arguments]
    elif args.kind == "package":
        command = [str(interpreter), str(ROOT / "scripts/package_hosted.py")]
        display_command = ["python", "scripts/package_hosted.py"]
    else:
        command = ["azd", *arguments]
        display_command = command
    state = {
        "stage": stage,
        "title": args.title,
        "command": redact(shlex.join(display_command)),
        "started_at": datetime.now(UTC).isoformat(),
        "status": "running",
        "return_code": None,
        "output": "",
    }
    save_state(viewer / "state.json", state)
    started = time.monotonic()
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=args.timeout,
            env={**os.environ, "PYTHONUNBUFFERED": "1"},
        )
        output = result.stdout + ("\n" + result.stderr if result.stderr else "")
        state.update(
            return_code=result.returncode,
            status="completed" if result.returncode == 0 else "failed",
        )
    except subprocess.TimeoutExpired as exc:
        output = "Execution timed out; no success result was produced.\n"
        for partial in (exc.stdout, exc.stderr):
            if partial:
                output += (
                    partial.decode("utf-8", errors="replace")
                    if isinstance(partial, bytes)
                    else partial
                )
        state.update(return_code=124, status="failed")
    except OSError as exc:
        output = f"Process could not be executed: {exc}"
        state.update(return_code=2, status="failed")
    state.update(
        finished_at=datetime.now(UTC).isoformat(),
        duration_seconds=round(time.monotonic() - started, 2),
        output=redact(output),
    )
    save_state(result_file, state)
    save_state(viewer / "state.json", state)
    print(state["output"])
    print(f"Recorded stage: {stage}; exit code: {state['return_code']}")
    return state["return_code"]


if __name__ == "__main__":
    raise SystemExit(main())
