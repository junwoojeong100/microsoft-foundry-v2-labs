import hashlib
import struct
import unittest
from datetime import datetime

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


class IQChatConfigurationCaptureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = ROOT / "docs/assets/iq-chat-20260917"
        cls.evidence = read_json(cls.directory / "captures.json")

    def test_new_screens_are_read_only_configuration_evidence_not_inference(self):
        value = self.evidence
        self.assertEqual(value["schema_version"], 1)
        self.assertEqual(value["captured_on"], "2026-09-17")
        self.assertEqual(value["pending_languages"], [])
        self.assertEqual(value["portal_language_restored"], "en")
        self.assertIs(value["existing_saved_configuration"], True)
        for flag in (
            "image_edited",
            "page_dom_modified_for_capture",
            "authentication_captured",
            "role_assignments_changed",
            "model_deployments_changed",
            "default_subscription_changed",
            "existing_ga_bases_changed",
            "new_evaluation_results",
        ):
            self.assertIs(value[flag], False, flag)
        self.assertEqual(value["resource_writes"], 0)
        self.assertEqual(value["model_invocations"], 0)
        deployment = value["deployment_verification"]
        self.assertEqual(deployment["deployment"], "gpt-5.6-luna")
        self.assertEqual(deployment["model"], "gpt-5.6-luna")
        self.assertEqual(deployment["model_version"], "2026-07-09")
        self.assertEqual(deployment["state"], "Succeeded")

    def test_both_real_language_images_match_hashes_and_complete_form_values(self):
        images = self.evidence["images"]
        self.assertEqual([item["guide_language"] for item in images], ["en", "ko"])
        self.assertEqual(len({item["sha256"] for item in images}), 2)
        self.assertLess(
            datetime.fromisoformat(images[0]["observed_at"]),
            datetime.fromisoformat(images[1]["observed_at"]),
        )
        displays = {
            "en": (["gpt-5.6-luna", "Low", "Answer synthesis"], "Active"),
            "ko": (["gpt-5.6-luna", "낮음", "응답 합성"], "활성"),
        }
        for item in images:
            language = item["guide_language"]
            with self.subTest(language=language):
                self.assertEqual(item["scenario_language"], language)
                self.assertEqual(item["document_language"], language)
                self.assertEqual(item["file"], f"{language}-configured-kb.png")
                self.assertEqual(item["knowledge_base"], f"mfv2-course-20260916-chat-{language}-kb")
                self.assertEqual(
                    item["knowledge_source"], f"mfv2-course-20260916-{language}-source"
                )
                self.assertEqual(item["selected_model"], "gpt-5.6-luna")
                self.assertEqual(item["reasoning_effort"], "low")
                self.assertEqual(item["output_mode"], "answerSynthesis")
                self.assertEqual(item["display_values"], displays[language][0])
                self.assertEqual(item["source_status"], displays[language][1])
                self.assertEqual(item["visible_invalid_controls"], 0)
                self.assertIs(item["missing_model_error_visible"], False)
                self.assertIs(item["managed_identity_notice_visible"], True)
                path = self.directory / item["file"]
                self.assertFalse(path.is_symlink())
                self.assertTrue(path.resolve().is_relative_to(self.directory.resolve()))
                content = path.read_bytes()
                self.assertEqual(len(content), item["bytes"])
                self.assertEqual(hashlib.sha256(content).hexdigest(), item["sha256"])
                self.assertEqual(content[:8], b"\x89PNG\r\n\x1a\n")
                self.assertEqual(
                    struct.unpack(">II", content[16:24]), (item["width"], item["height"])
                )
                self.assertGreaterEqual(item["width"], 1000)
                self.assertGreaterEqual(item["height"], 800)

    def test_lab_06_uses_ready_screens_without_removed_historical_images(self):
        for item in self.evidence["images"]:
            language = item["guide_language"]
            directory = ROOT / ("docs" if language == "en" else "docs/ko")
            text = (directory / "labs/06-knowledge.md").read_text()
            with self.subTest(language=language):
                self.assertIn('<a id="iq-chat-model"></a>', text)
                self.assertEqual(text.count(f"/iq-chat-20260917/{item['file']}"), 1)
                self.assertNotIn("refresh-20260915", text)
                for historical in ("EP06-041-english-kb-2.webp", "KP06-002-kb-2.webp"):
                    self.assertNotIn(historical, text)
