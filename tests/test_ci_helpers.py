import os
import unittest
from unittest.mock import patch

from .test_packaging import load_script
from .test_toolbox import settings

EXPORT = load_script("export_hosted_binding")
PREPARE = load_script("prepare_ci_azd")
GRANT = load_script("grant_ci_runtime_role")

SUBSCRIPTION = "00000000-0000-0000-0000-000000000002"
ENV = {
    "WORKSHOP_PREFIX": "mfv2-unit",
    "AZURE_SUBSCRIPTION_ID": SUBSCRIPTION,
    "AZURE_RESOURCE_GROUP": "unit-group",
    "AZURE_AI_ACCOUNT_NAME": "unit",
    "AZURE_AI_PROJECT_ID": f"/subscriptions/{SUBSCRIPTION}/resourceGroups/unit-group/providers/Microsoft.CognitiveServices/accounts/unit/projects/workshop",
}


class CIHelperTests(unittest.TestCase):
    def test_runtime_role_is_bound_to_the_actual_deployed_identity(self):
        principal = "00000000-0000-0000-0000-000000000004"
        actual = {
            "name": "mfv2-unit-ci",
            "version": "2",
            "status": "active",
            "instance_identity": {"principal_id": principal},
        }
        self.assertEqual(GRANT.runtime_principal(actual, "mfv2-unit-ci", "2"), principal)
        with self.assertRaises(ValueError):
            GRANT.runtime_principal(actual, "mfv2-unit-ci", "1")
        with self.assertRaises(ValueError):
            GRANT.runtime_principal({**actual, "instance_identity": {}}, "mfv2-unit-ci", "2")

    def test_scope_is_verified_before_initialization(self):
        with patch.dict(os.environ, ENV, clear=True):
            PREPARE.validate_config(settings(), "mfv2-unit-ci")
            with self.assertRaises(ValueError):
                PREPARE.validate_config(settings(), "another-agent")
            with patch.dict(
                os.environ, {"AZURE_AI_PROJECT_ID": "/subscriptions/other/projects/workshop"}
            ):
                with self.assertRaises(ValueError):
                    PREPARE.validate_config(settings(), "mfv2-unit-ci")

    def test_binding_uses_actual_version_and_never_exports_other_env_values(self):
        values = {
            "AGENT_MFV2_UNIT_CI_NAME": "mfv2-unit-ci",
            "AGENT_MFV2_UNIT_CI_VERSION": "12",
            "AGENT_MFV2_UNIT_CI_INVOCATIONS_ENDPOINT": "https://unit.services.ai.azure.com/api/projects/workshop/agents/mfv2-unit-ci/endpoint/protocols/invocations?api-version=v1",
            "UNRELATED_PRIVATE_VALUE": "not-exported",
        }
        with patch.dict(os.environ, ENV, clear=True):
            result = EXPORT.binding(values, settings(), "mfv2-unit-ci")
            self.assertEqual(len(result), 3)
            self.assertEqual(result["WORKSHOP_HOSTED_AGENT_VERSION"], "12")
            self.assertNotIn("UNRELATED_PRIVATE_VALUE", result)
            for key, value in (
                ("AGENT_MFV2_UNIT_CI_VERSION", "latest"),
                ("AGENT_MFV2_UNIT_CI_VERSION", "12\nOTHER=bad"),
                ("AGENT_MFV2_UNIT_CI_NAME", "another-agent"),
                ("AGENT_MFV2_UNIT_CI_INVOCATIONS_ENDPOINT", "https://other.invalid/invocations"),
            ):
                with self.subTest(key=key), self.assertRaises(ValueError):
                    EXPORT.binding({**values, key: value}, settings(), "mfv2-unit-ci")
