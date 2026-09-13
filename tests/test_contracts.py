import os
import unittest
from unittest.mock import patch

from foundry_workshop.cli import doctor_offline, parser
from foundry_workshop.contracts import (
    Answer,
    digest,
    load_cases,
    load_documents,
    parse_json,
    safe_label,
)
from foundry_workshop.knowledge import evidence, local_retrieve
from foundry_workshop.settings import Settings, azure_endpoint

from . import ROOT


class ContractTests(unittest.TestCase):
    def valid_answer(self):
        return {
            "answer": "합성 규정의 한도입니다.",
            "decision": "answer",
            "limit_krw": 150000,
            "citations": ["TRAVEL-2026"],
        }

    def test_dataset_counts_and_partitions(self):
        result = doctor_offline(ROOT)
        self.assertEqual(
            (result["documents"], result["dev_cases"], result["holdout_cases"]), (6, 6, 4)
        )
        self.assertFalse(result["azure_tested"])
        self.assertEqual(result["result"], "PASS")

    def test_answer_roundtrip(self):
        value = self.valid_answer()
        self.assertEqual(Answer.from_dict(value).to_dict(), value)

    def test_invalid_answer_shapes(self):
        examples = [
            {**self.valid_answer(), "limit_krw": True},
            {**self.valid_answer(), "limit_krw": -1},
            {**self.valid_answer(), "limit_krw": "150000"},
            {**self.valid_answer(), "decision": "approved"},
            {**self.valid_answer(), "answer": ""},
            {**self.valid_answer(), "citations": ["TRAVEL-2026", "TRAVEL-2026"]},
            {**self.valid_answer(), "citations": "TRAVEL-2026"},
            {**self.valid_answer(), "unexpected": "field"},
        ]
        for value in examples:
            with self.subTest(value=value), self.assertRaises(ValueError):
                Answer.from_dict(value)

    def test_json_is_not_silently_repaired(self):
        for text in ('{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '```json\n{"a":1}\n```'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_json(text)

    def test_label_rejects_paths(self):
        for label in ("../outside", "/tmp/results", "UPPER", "a/b", "", "a" * 49):
            with self.subTest(label=label), self.assertRaises(ValueError):
                safe_label(label)
        self.assertEqual(safe_label("candidate-02"), "candidate-02")

    def test_endpoint_validation(self):
        endpoint = "https://unit.services.ai.azure.com/api/projects/workshop/"
        self.assertEqual(azure_endpoint(endpoint, "project"), endpoint.rstrip("/"))
        invalid = [
            "https://ai.azure.com",
            "https://unit.services.ai.azure.com",
            "http://unit.services.ai.azure.com/api/projects/workshop",
            "https://user:password@unit.services.ai.azure.com/api/projects/workshop",
            endpoint + "?token=secret",
            "https://unit.services.ai.azure.com.evil.example/api/projects/workshop",
        ]
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(ValueError):
                azure_endpoint(value, "project")

    def test_settings_have_no_model_fallback(self):
        with patch.dict(os.environ, {}, clear=True), self.assertRaises(ValueError):
            Settings.from_env()

    def test_settings_use_explicit_local_tenant(self):
        environment = {
            "AZURE_TENANT_ID": "00000000-0000-0000-0000-000000000001",
            "AZURE_AI_PROJECT_ENDPOINT": "https://unit.services.ai.azure.com/api/projects/workshop",
            "AZURE_AI_MODEL_DEPLOYMENT_NAME": "actual-deployment-name",
        }
        with patch.dict(os.environ, environment, clear=True):
            settings = Settings.from_env()
        self.assertEqual(settings.deployment, "actual-deployment-name")
        self.assertEqual(settings.auth_mode, "cli")

    def test_context_hash_is_order_independent(self):
        documents = load_documents(ROOT)
        self.assertEqual(
            evidence(documents, "unit")["context_hash"],
            evidence(list(reversed(documents)), "unit")["context_hash"],
        )

    def test_duplicate_or_incomplete_evidence_fails(self):
        document = load_documents(ROOT)[0]
        for documents in ([document, document], [{"id": "missing-fields"}]):
            with self.subTest(documents=documents), self.assertRaises(ValueError):
                evidence(documents, "unit")

    def test_local_retrieval_is_not_labeled_iq(self):
        result = local_retrieve(ROOT, "2026년 9월 국내 출장 숙박비 한도")
        self.assertEqual(result["provider"], "local-keyword")
        self.assertIn("TRAVEL-2026", result["source_ids"])
        self.assertEqual(result["context_hash"], digest(result["documents"]))

    def test_empty_search_does_not_invent_context(self):
        result = local_retrieve(ROOT, "zzzzunmatchedtoken")
        self.assertEqual(result["documents"], [])

    def test_unknown_split_fails(self):
        with self.assertRaises(ValueError):
            load_cases(ROOT, "../other")

    def test_holdout_parser_requires_explicit_flags_at_execution(self):
        args = parser().parse_args(
            [
                "collect",
                "--split",
                "holdout",
                "--label",
                "final",
                "--candidate",
                "candidate",
                "--unlock-holdout",
            ]
        )
        self.assertEqual(args.candidate, "candidate")
        self.assertTrue(args.unlock_holdout)


if __name__ == "__main__":
    unittest.main()
