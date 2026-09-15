import unittest

from foundry_workshop.contracts import load_documents, read_json

from . import ROOT


class IQModelIdentityEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = read_json(ROOT / "docs/assets/iq-mi-20260915/verification.json")

    def test_verified_model_uses_search_identity_without_an_api_key(self):
        value = self.evidence
        self.assertEqual(value["search_identity_type"], "SystemAssigned")
        self.assertTrue(value["search_and_foundry_api_key_auth_disabled"])
        self.assertEqual(value["role_name"], "Cognitive Services User")
        self.assertIn("/Microsoft.CognitiveServices/accounts/", value["role_scope"])
        self.assertEqual(value["saved_model"]["kind"], "azureOpenAI")
        self.assertFalse(value["saved_model"]["api_key_present"])
        self.assertIsNone(value["saved_model"]["authIdentity"])
        self.assertFalse(value["secrets_recorded"])

    def test_validation_failure_is_retained_separately_from_successful_model_calls(self):
        value = self.evidence
        self.assertEqual(value["retrieve_requests_sent"], 2)
        self.assertEqual(value["first_attempt"]["status_code"], 400)
        self.assertIn("maxOutputSizeInTokens", value["first_attempt"]["error"]["message"])
        self.assertFalse(value["first_attempt"]["model_activity_verified"])
        self.assertEqual(value["successful_status_code"], 200)
        request = value["successful_request"]
        self.assertEqual(value["api_version"], "2026-08-01-preview")
        self.assertIn("messages", request)
        self.assertNotIn("intents", request)
        self.assertNotIn("maxOutputSizeInTokens", request)
        self.assertEqual(request["maxOutputSize"], 6000)
        self.assertEqual(request["retrievalReasoningEffort"], {"kind": "low"})
        self.assertEqual(request["outputMode"], "answerSynthesis")

    def test_actual_activity_contains_both_planning_and_answer_synthesis(self):
        value = self.evidence
        self.assertTrue(value["model_planning_verified"])
        self.assertTrue(value["model_synthesis_verified"])
        by_type = {item["type"]: item for item in value["activity"]}
        for kind in ("modelQueryPlanning", "modelAnswerSynthesis"):
            item = by_type[kind]
            self.assertFalse(item.get("error"))
            self.assertEqual(item["model"]["deploymentId"], value["saved_model"]["deploymentId"])
            self.assertEqual(item["model"]["modelName"], value["saved_model"]["modelName"])
            self.assertGreater(item["inputTokens"], 0)
            self.assertGreater(item["outputTokens"], 0)
        known = {document["id"] for document in load_documents(ROOT)}
        self.assertTrue(set(value["reference_document_ids"]) <= known)
        self.assertTrue({"TRAVEL-2026", "APPROVAL-01"} <= set(value["reference_document_ids"]))
        text = "\n".join(
            item["text"]
            for response in value["response"]
            for item in response["content"]
            if item["type"] == "text"
        )
        self.assertIn("[ref_id:", text)

    def test_temporary_base_is_deleted_without_relabeling_existing_evaluations(self):
        value = self.evidence
        self.assertTrue(value["temporary_base_deleted"])
        self.assertEqual(value["cleanup_absence_status_code"], 404)
        self.assertTrue(value["role_retained_as_approved"])
        self.assertFalse(value["model_deployments_changed"])
        self.assertFalse(value["datasets_or_benchmark_scores_changed"])
        before = value["existing_base_models_before"]
        self.assertEqual(len(before), 2)
        self.assertTrue(all(models == [] for models in before.values()))
        after = value["existing_bases_unchanged"]
        self.assertEqual({item["name"] for item in after}, set(before))
        self.assertEqual(len(after), 4)
        for name in before:
            self.assertEqual(len({item["etag"] for item in after if item["name"] == name}), 1)
