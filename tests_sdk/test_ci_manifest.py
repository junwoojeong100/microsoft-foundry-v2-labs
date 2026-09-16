import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from tests import ROOT
from tests.test_ci_helpers import ENV, PREPARE
from tests.test_toolbox import settings


class CIManifestTests(unittest.TestCase):
    def test_release_deployment_is_isolated_from_the_historical_repository_project(self):
        workflow = yaml.safe_load((ROOT / ".github/workflows/hosted-lab-release.yml").read_text())
        job = workflow["jobs"]["release"]
        self.assertTrue(all("${{ runner." not in str(value) for value in job["env"].values()))
        steps = {step.get("name"): step.get("run", "") for step in job["steps"]}
        initialization = steps["Initialize only the existing-project code deployment"]
        self.assertIn('AZD_PROJECT_DIR="$RUNNER_TEMP/foundry-workshop-release"', initialization)
        self.assertIn('>> "$GITHUB_ENV"', initialization)
        self.assertIn("prepare_hosted_azd.py", initialization)
        self.assertIn('--directory "$AZD_PROJECT_DIR"', initialization)
        self.assertNotIn("azd ai agent init", initialization)
        for step in (
            "Deploy only the approved service",
            "Give only the owned runtime project access",
        ):
            self.assertIn('cd "$AZD_PROJECT_DIR"', steps[step])
            self.assertIn("$GITHUB_WORKSPACE/scripts/", steps[step])
        self.assertNotIn("azd provision", "\n".join(steps.values()))

    def test_sdk_checks_install_the_declared_development_dependencies(self):
        workflow = yaml.safe_load((ROOT / ".github/workflows/check.yml").read_text())
        commands = "\n".join(
            step.get("run", "") for step in workflow["jobs"]["sdk-imports"]["steps"]
        )
        self.assertRegex(commands, r"pip install [^\n]*\.\[[^\]]*\bdev\b[^\]]*\]")

    def test_only_the_owned_agent_env_is_merged_into_the_existing_project(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, ENV, clear=True):
            path = Path(directory) / "azure.yaml"
            project = {"host": "azure.ai.project", "endpoint": settings().project_endpoint}
            manifest = {
                "name": "unit",
                "services": {
                    "existing-project": project,
                    "mfv2-unit-ci": {
                        "host": "azure.ai.agent",
                        "name": "mfv2-unit-ci",
                        "project": ".build/unit",
                        "uses": ["existing-project"],
                        "codeConfiguration": {"runtime": "python_3_13", "entryPoint": "main.py"},
                        "env": {"KEEP": "unchanged"},
                    },
                },
            }
            path.write_text(yaml.safe_dump(manifest))
            PREPARE.prepare(path, settings(), "mfv2-unit-ci")
            result = yaml.safe_load(path.read_text())
            self.assertEqual(result["services"]["existing-project"], project)
            self.assertEqual(result["services"]["mfv2-unit-ci"]["env"]["KEEP"], "unchanged")
            self.assertEqual(
                result["services"]["mfv2-unit-ci"]["env"]["WORKSHOP_AUTH_MODE"], "managed-identity"
            )
            self.assertEqual(result["services"]["mfv2-unit-ci"]["project"], ".build/unit")
            result["services"]["another-agent"] = {"host": "azure.ai.agent"}
            path.write_text(yaml.safe_dump(result))
            before = path.read_bytes()
            with self.assertRaises(ValueError):
                PREPARE.prepare(path, settings(), "mfv2-unit-ci")
            self.assertEqual(path.read_bytes(), before)
