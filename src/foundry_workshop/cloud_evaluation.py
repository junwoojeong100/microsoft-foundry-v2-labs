import json
import math
import time
from pathlib import Path
from typing import Any

from .cloud import project_clients
from .contracts import digest, read_json, safe_label, write_json
from .evaluation import load_run
from .settings import Settings, owned_prefix, require_env

EVALUATORS = ("groundedness", "relevance")


def normalize_results(items: list[dict[str, Any]], row_ids: list[str]) -> list[dict[str, Any]]:
    if len(items) != len(row_ids):
        raise ValueError("Cloud evaluation must return exactly one result per submitted response.")
    normalized = []
    seen = set()
    for item in items:
        if item.get("status") in {"failed", "error", "errored"}:
            raise ValueError("A cloud evaluation output item failed.")
        source = item.get("datasource_item")
        row_id = source.get("case_id") if isinstance(source, dict) else None
        if row_id is None:
            position = str(item.get("datasource_item_id", ""))
            if not position.isdigit() or not 0 <= int(position) < len(row_ids):
                raise ValueError("Cannot map an evaluation output to its source case.")
            row_id = row_ids[int(position)]
        if row_id not in row_ids or row_id in seen:
            raise ValueError("Unknown or duplicate cloud evaluation case ID.")
        seen.add(row_id)
        results = item.get("results")
        if not isinstance(results, list) or len(results) != len(EVALUATORS):
            raise ValueError("Missing evaluator results.")
        if {result.get("name") for result in results} != set(EVALUATORS):
            raise ValueError("Unexpected evaluator names.")
        for result in results:
            score = result.get("score")
            if (
                result.get("error")
                or type(result.get("passed")) is not bool
                or type(score) not in {int, float}
                or not math.isfinite(score)
            ):
                raise ValueError(
                    "Evaluator returned an error or incomplete native score/pass result."
                )
        normalized.append({"case_id": row_id, "results": results})
    return normalized


def evaluate_cloud(
    root: Path, settings: Settings, label: str, *, timeout: int, confirmed: bool
) -> dict[str, Any]:
    from azure.ai.projects.models import TestingCriterionAzureAIEvaluator

    if not confirmed:
        raise ValueError("Cloud judges are billable. Explicitly pass --confirm-cost.")
    if not 5 <= timeout <= 900:
        raise ValueError("Evaluation timeout must be 5-900 seconds.")
    manifest, rows, cases = load_run(root, safe_label(label))
    if manifest["mode"] != "live" or any(row["status"] != "ok" for row in rows):
        raise ValueError("Cloud evaluation requires a complete real run with no collection errors.")
    judge = require_env("AZURE_AI_EVALUATION_MODEL_DEPLOYMENT_NAME")
    if judge == manifest["deployment"]:
        raise ValueError(
            "Use an explicitly separate judge deployment to make judge selection visible."
        )
    by_id = {case["case_id"]: case for case in cases}
    items = [
        {
            "case_id": row["case_id"],
            "query": row["question"],
            "response": row["answer"]["answer"],
            "context": json.dumps(row["documents"], ensure_ascii=False),
            "ground_truth": json.dumps(
                {
                    key: by_id[row["case_id"]][key]
                    for key in ("expected_decision", "expected_limit_krw", "required_citations")
                },
                ensure_ascii=False,
            ),
        }
        for row in rows
    ]
    directory = root / "outputs" / label
    state_path = directory / "cloud-evaluation.json"
    state = (
        read_json(state_path)
        if state_path.exists()
        else {
            "source_run_id": manifest["run_id"],
            "input_hash": digest(items),
            "judge_deployment": judge,
            "project_endpoint": settings.project_endpoint,
        }
    )
    for key, value in (
        ("input_hash", digest(items)),
        ("judge_deployment", judge),
        ("project_endpoint", settings.project_endpoint),
    ):
        if state.get(key) != value:
            raise ValueError(f"Saved evaluation has a different {key}; do not reuse it.")
    with project_clients(settings, preview=True) as (project, client):
        if "evaluation_id" not in state:
            criteria = []
            catalog = []
            for name in EVALUATORS:
                definition = project.beta.evaluators.get_version(
                    f"builtin.{name}", "latest"
                ).as_dict()
                properties = definition["definition"]["init_parameters"]["properties"]
                model_keys = [key for key in ("model", "deployment_name") if key in properties]
                if len(model_keys) != 1:
                    raise ValueError(
                        f"Unsupported {name} judge initialization schema; inspect the evaluator catalog."
                    )
                parameters = {model_keys[0]: judge}
                if "threshold" in properties:
                    parameters["threshold"] = 4
                catalog.append({"name": name, "definition": definition, "parameters": parameters})
                criteria.append(
                    TestingCriterionAzureAIEvaluator(
                        type="azure_ai_evaluator",
                        name=name,
                        evaluator_name=f"builtin.{name}",
                        evaluator_version=definition["version"],
                        initialization_parameters=parameters,
                        data_mapping={
                            "query": "{{item.query}}",
                            "response": "{{item.response}}",
                            **({"context": "{{item.context}}"} if name == "groundedness" else {}),
                        },
                    )
                )
            write_json(directory / "evaluator-catalog.json", catalog)
            evaluation = client.evals.create(
                name=f"{owned_prefix()}-{label}"[:63],
                data_source_config={
                    "type": "custom",
                    "item_schema": {
                        "type": "object",
                        "properties": {key: {"type": "string"} for key in items[0]},
                        "required": list(items[0]),
                    },
                },
                testing_criteria=criteria,
                metadata={
                    "source_run_id": manifest["run_id"],
                    "dataset_hash": manifest["dataset_hash"],
                },
            )
            state["evaluation_id"] = evaluation.id
            state["evaluator_hash"] = digest(catalog)
            write_json(state_path, state)
        if "run_id" not in state:
            run = client.evals.runs.create(
                eval_id=state["evaluation_id"],
                name=label,
                data_source={
                    "type": "jsonl",
                    "source": {
                        "type": "file_content",
                        "content": [{"item": item} for item in items],
                    },
                },
            )
            state["run_id"] = run.id
            write_json(state_path, state)
        deadline = time.monotonic() + timeout
        while True:
            run = client.evals.runs.retrieve(run_id=state["run_id"], eval_id=state["evaluation_id"])
            state.update(
                status=run.status, report_url=run.report_url, run=run.model_dump(mode="json")
            )
            write_json(state_path, state)
            if run.status in {"completed", "failed", "canceled", "cancelled"}:
                break
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    "Evaluation is still running. Repeat the same command/label to resume without resubmitting."
                )
            time.sleep(5)
        if run.status != "completed":
            raise ValueError(
                f"Cloud evaluation ended with {run.status}; inspect cloud-evaluation.json."
            )
        raw_items = [
            item.model_dump(mode="json")
            for item in client.evals.runs.output_items.list(
                run_id=state["run_id"], eval_id=state["evaluation_id"]
            )
        ]
        write_json(directory / "cloud-evaluation-raw.json", raw_items)
        normalized = normalize_results(raw_items, [row["case_id"] for row in rows])
        write_json(directory / "cloud-evaluation-results.json", normalized)
    return {
        "mode": "live",
        "label": label,
        "evaluation_id": state["evaluation_id"],
        "run_id": state["run_id"],
        "report_url": state["report_url"],
        "rows": len(normalized),
        "note": "Native judge results are saved separately from deterministic business checks.",
    }
