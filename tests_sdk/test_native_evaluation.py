import json
import os
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from foundry_workshop.contracts import read_json, write_json
from foundry_workshop.native import evaluate_items, verified_native

from .test_sdk_contracts import settings


class NativeEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.environment = patch.dict(
            os.environ,
            {
                "WORKSHOP_PREFIX": "mfv2-unit",
                "AZURE_AI_EVALUATION_MODEL_DEPLOYMENT_NAME": "unit-judge",
            },
            clear=True,
        )
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.catalog_calls = []
        self.create_calls = []
        self.run_calls = []
        self.status = "completed"
        self.result_passed = False
        self.omit_rows = False
        self.evaluator_names = ("groundedness", "relevance")
        self.supported_levels = ["turn", "conversation"]
        self.items = [
            {
                "case_id": "D01",
                "query": "합성 질문",
                "response": "합성 답",
                "context": "합성 근거",
                "ground_truth": "원본 정답",
            }
        ]

    @contextmanager
    def clients(self, *_args, **_kwargs):
        def catalog(name, version):
            self.catalog_calls.append((name, version))
            return SimpleNamespace(
                as_dict=lambda: {
                    "name": name,
                    "version": "7",
                    "supported_evaluation_levels": self.supported_levels,
                    "definition": {
                        "init_parameters": {
                            "properties": {"model": {}, "threshold": {}, "evaluation_level": {}}
                        }
                    },
                }
            )

        def create(**kwargs):
            self.create_calls.append(kwargs)
            return SimpleNamespace(id=f"eval-unit-{len(self.create_calls)}")

        def create_run(**kwargs):
            self.run_calls.append(kwargs)
            return SimpleNamespace(id=f"run-unit-{len(self.run_calls)}")

        def retrieve(**_kwargs):
            return SimpleNamespace(
                status=self.status,
                report_url="https://ai.azure.com/unit",
                model_dump=lambda **_: {"status": self.status},
            )

        def output_items(**_kwargs):
            if self.omit_rows:
                return []
            return [
                SimpleNamespace(
                    model_dump=lambda **_: {
                        "datasource_item": {"case_id": "D01"},
                        "results": [
                            {"name": name, "score": 3, "passed": self.result_passed}
                            for name in self.evaluator_names
                        ],
                    }
                )
            ]

        project = SimpleNamespace(
            beta=SimpleNamespace(evaluators=SimpleNamespace(get_version=catalog))
        )
        client = SimpleNamespace(
            evals=SimpleNamespace(
                create=create,
                runs=SimpleNamespace(
                    create=create_run,
                    retrieve=retrieve,
                    output_items=SimpleNamespace(list=output_items),
                ),
            )
        )
        yield project, client

    def evaluate(self, path, **kwargs):
        with patch("foundry_workshop.native.project_clients", self.clients):
            return evaluate_items(
                settings(),
                path,
                self.items,
                label="unit-eval",
                source_run_id="unit-source",
                dataset_hash="unit-dataset",
                forbidden_deployments={"unit-deployment"},
                evaluator_names=self.evaluator_names,
                confirmed=True,
                timeout=5,
                **kwargs,
            )

    def test_catalog_is_pinned_and_resuming_does_not_submit_again_or_hide_low_scores(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            first = self.evaluate(path)
            second = self.evaluate(path)
            self.assertEqual(first["run_id"], second["run_id"])
            self.assertEqual(len(self.create_calls), 1)
            self.assertEqual(len(self.run_calls), 1)
            self.assertEqual(len(self.catalog_calls), 2)
            criteria = self.create_calls[0]["testing_criteria"]
            self.assertTrue(all(item["evaluator_version"] == "7" for item in criteria))
            state, rows = verified_native(path)
            self.assertEqual(state["validation_status"], "valid")
            self.assertFalse(rows[0]["results"][0]["passed"])
            with self.assertRaises(ValueError):
                self.evaluate(path, retry_failed=True)

    def test_only_failed_attempts_can_retry_with_the_same_catalog_and_preserved_history(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            self.status = "failed"
            with self.assertRaises(ValueError):
                self.evaluate(path)
            self.status = "completed"
            self.evaluate(path, retry_failed=True)
            self.assertTrue((path / "native-attempts/attempt-1/cloud-evaluation.json").is_file())
            self.assertEqual(len(self.catalog_calls), 2)
            self.assertEqual(len(self.create_calls), 2)
            self.assertTrue(read_json(path / "cloud-evaluation.json")["retry_of"])

    def test_missing_rows_and_changed_input_or_catalog_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            self.omit_rows = True
            with self.assertRaises(ValueError):
                self.evaluate(path)
            self.assertEqual(
                read_json(path / "cloud-evaluation.json")["validation_status"], "invalid"
            )
            self.assertEqual(read_json(path / "cloud-evaluation-raw.json"), [])
            catalog = read_json(path / "evaluator-catalog.json")
            catalog[0]["parameters"]["threshold"] = 1
            write_json(path / "evaluator-catalog.json", catalog)
            with self.assertRaises(ValueError):
                self.evaluate(path, retry_failed=True)
            self.items[0]["response"] = "changed"
            with self.assertRaises(ValueError):
                self.evaluate(path)

    def test_only_query_response_context_enter_native_mapping(self):
        with tempfile.TemporaryDirectory() as folder:
            self.evaluate(Path(folder))
            source = self.run_calls[0]["data_source"]["source"]
            self.assertEqual(source["type"], "file_content")
            self.assertEqual(source["content"][0]["item"], self.items[0])
            criteria = self.create_calls[0]["testing_criteria"]
            self.assertIn("context", criteria[0]["data_mapping"])
            self.assertNotIn("context", criteria[1]["data_mapping"])
            self.assertNotIn("sample.output", json.dumps(criteria))

    def test_message_inputs_pin_level_and_use_array_schema_without_query_mapping(self):
        self.evaluator_names = ("groundedness", "coherence")
        self.items = [
            {
                "case_id": "D01",
                "messages": [
                    {"role": "user", "content": "Synthetic question"},
                    {"role": "assistant", "content": "Synthetic answer"},
                ],
            }
        ]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            result = self.evaluate(path, messages_input=True, evaluation_level="conversation")
            self.assertEqual(result["evaluation_level"], "conversation")
            self.assertEqual(self.run_calls[0]["extra_body"], {"evaluation_level": "conversation"})
            self.assertEqual(
                self.create_calls[0]["data_source_config"]["item_schema"]["properties"]["messages"],
                {"type": "array"},
            )
            for criterion in self.create_calls[0]["testing_criteria"]:
                self.assertEqual(criterion["data_mapping"], {"messages": "{{item.messages}}"})
                self.assertEqual(
                    criterion["initialization_parameters"]["evaluation_level"], "conversation"
                )
            with self.assertRaisesRegex(ValueError, "evaluation level"):
                self.evaluate(path, messages_input=True, evaluation_level="turn")
            self.assertEqual(len(self.run_calls), 1)

    def test_unsupported_conversation_evaluator_or_missing_answer_never_submits(self):
        self.items = [
            {
                "case_id": "D01",
                "messages": [
                    {"role": "user", "content": "Synthetic question"},
                    {"role": "assistant", "content": "Synthetic answer"},
                ],
            }
        ]
        self.supported_levels = ["turn"]
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, "advertise support"):
                self.evaluate(Path(folder), messages_input=True, evaluation_level="conversation")
            self.items[0]["messages"].pop()
            with self.assertRaisesRegex(ValueError, "complete text conversations"):
                self.evaluate(Path(folder), messages_input=True, evaluation_level="conversation")
        self.assertEqual(self.create_calls, [])
        self.assertEqual(self.run_calls, [])
