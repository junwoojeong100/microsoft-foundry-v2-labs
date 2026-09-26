#!/usr/bin/env python3
"""Check your SDK recipe copies with fixed synthetic responses, never real model inference."""

import argparse
import hashlib
import json
import os
import socket
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from foundry_workshop.contracts import digest  # noqa: E402

RECIPE_NAMES = (
    "02_responses.py",
    "03_prompt_agent.py",
    "04_maf_tool.py",
    "05_maf_sequential.py",
    "06_iq_retrieve.py",
    "08_hosted_agent.py",
)


def recipe_fingerprint(directory: Path) -> str:
    if not directory.is_dir() or directory.is_symlink():
        raise ValueError("Choose a real directory containing the six recipe copies.")
    files = {name: directory / name for name in RECIPE_NAMES}
    for name, path in files.items():
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"Missing or redirected recipe: {name}")
    return digest(
        {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in files.items()}
    )


def check(directory: Path) -> dict:
    if sys.version_info[:2] != (3, 13):
        raise ValueError("These installed-SDK exercises require Python 3.13.")
    before = recipe_fingerprint(directory)
    policies = ROOT / "data/knowledge/en/policies.json"
    environment = {
        "OTEL_SDK_DISABLED": "true",
        "WORKSHOP_POLICIES_FILE": str(policies),
    }
    network_error = RuntimeError(
        "Offline recipe exercise blocked a network connection; do not run a live main()."
    )
    with (
        patch.dict(os.environ, environment, clear=True),
        patch.object(socket, "getaddrinfo", side_effect=network_error),
        patch.object(socket.socket, "connect", side_effect=network_error),
        patch.object(socket.socket, "connect_ex", side_effect=network_error),
    ):
        from tests_sdk import test_recipes

        load_recipe = test_recipes.recipe

        def with_fixture(name):
            module = load_recipe(name)
            if hasattr(module, "POLICIES"):
                module.POLICIES = policies
            return module

        with (
            patch.object(test_recipes, "RECIPES", directory.resolve()),
            patch.object(test_recipes, "recipe", side_effect=with_fixture),
        ):
            suite = unittest.defaultTestLoader.loadTestsFromModule(test_recipes)
            expected = suite.countTestCases()
            result = unittest.TextTestRunner(stream=sys.stderr, verbosity=2).run(suite)
    after = recipe_fingerprint(directory)
    passed = (
        expected > 0
        and result.testsRun == expected
        and result.wasSuccessful()
        and not result.skipped
        and not result.expectedFailures
        and before == after
    )
    return {
        "schema_version": 1,
        "mode": "offline-sdk-practice",
        "fixture_language": "en",
        "fixture_corpus_sha256": hashlib.sha256(policies.read_bytes()).hexdigest(),
        "test_definition_sha256": hashlib.sha256(
            (ROOT / "tests_sdk/test_recipes.py").read_bytes()
        ).hexdigest(),
        "recipes_before_sha256": before,
        "recipes_after_sha256": after,
        "source_unchanged": before == after,
        "tests_expected": expected,
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "expected_failures": len(result.expectedFailures),
        "status": "passed" if passed else "failed",
        "azure_tested": False,
        "model_quality_measured": False,
        "note": "Mock-transport SDK checks, not Azure execution or a security sandbox. Run only trusted recipe copies.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--directory",
        type=Path,
        required=True,
        help="Your copied recipe directory, not a ZIP or another learner's code.",
    )
    args = parser.parse_args(argv)
    try:
        result = check(args.directory)
    except ModuleNotFoundError as exc:
        print(
            f"FAIL: missing {exc.name}. In a Python 3.13 venv install the repository lock and "
            ".[cloud,agents,hosted,dev]; nothing was installed automatically.",
            file=sys.stderr,
        )
        return 2
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
