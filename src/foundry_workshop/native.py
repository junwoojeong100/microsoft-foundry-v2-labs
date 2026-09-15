import time
from pathlib import Path
from typing import Any

from .cloud import project_clients
from .contracts import digest, read_json, safe_label, write_json
from .settings import Settings, owned_prefix, require_env


def evaluate_items(
    settings: Settings,
    directory: Path,
    items: list[dict[str, str]],
    *,
    label: str,
    source_run_id: str,
    dataset_hash: str,
    forbidden_deployments: set[str],
    evaluator_names: tuple[str, ...],
    confirmed: bool,
    timeout: int,
    reference_catalog: Path | None = None,
    retry_failed: bool = False,
) -> dict[str, Any]:
    from azure.ai.projects.models import TestingCriterionAzureAIEvaluator

    from .cloud_evaluation import normalize_results

    if not confirmed:
        raise ValueError("Native judges are billable; explicitly pass --confirm-cost.")
    if not 5 <= timeout <= 900 or not items or not evaluator_names:
        raise ValueError("Provide evaluation items/evaluators and a timeout of 5-900 seconds.")
    ids = [item["case_id"] for item in items]
    if len(ids) != len(set(ids)) or any(
        not isinstance(value, str) for item in items for value in item.values()
    ):
        raise ValueError("Native evaluation items must have unique case IDs and string fields.")
    judge = require_env("AZURE_AI_EVALUATION_MODEL_DEPLOYMENT_NAME")
    if judge in forbidden_deployments:
        raise ValueError(
            "The judge deployment must be explicitly separate from every target deployment."
        )
    directory.mkdir(parents=True, exist_ok=True)
    state_path = directory / "cloud-evaluation.json"
    catalog_path = directory / "evaluator-catalog.json"
    identity = {
        "source_run_id": source_run_id,
        "input_hash": digest(items),
        "dataset_hash": dataset_hash,
        "judge_deployment": judge,
        "project_endpoint": settings.project_endpoint,
    }
    state = read_json(state_path) if state_path.exists() else dict(identity)
    if "dataset_hash" not in state and "evaluation_id" in state:
        if "evaluator_names" in state or evaluator_names != ("groundedness", "relevance"):
            raise ValueError(
                "Only the original legacy evaluation schema may derive a missing dataset hash."
            )
        state["dataset_hash"] = dataset_hash
        state["legacy_schema_checked"] = True
    for key, value in identity.items():
        if state.get(key) != value:
            raise ValueError(f"The saved native evaluation changed {key}.")
    if state.get("evaluator_names", list(evaluator_names)) != list(evaluator_names):
        raise ValueError("The saved native evaluation uses a different evaluator set.")
    if "evaluator_names" not in state and "evaluation_id" in state:
        if evaluator_names != ("groundedness", "relevance"):
            raise ValueError("A legacy evaluation can only resume its original two evaluators.")
        state["legacy_schema_checked"] = True
    state["evaluator_names"] = list(evaluator_names)
    if retry_failed:
        if (
            state.get("status") not in {"failed", "canceled", "cancelled"}
            and state.get("validation_status") != "invalid"
        ):
            raise ValueError(
                "Only a failed/invalid attempt can be retried, not a completed low score."
            )
        if not catalog_path.is_file() or state.get("evaluator_hash") != digest(
            read_json(catalog_path)
        ):
            raise ValueError(
                "A failed attempt's evaluator catalog must remain unchanged before retry."
            )
        original_evaluator_hash = state["evaluator_hash"]
        attempts = directory / "native-attempts"
        attempts.mkdir(exist_ok=True)
        attempt = attempts / f"attempt-{len(list(attempts.iterdir())) + 1}"
        attempt.mkdir()
        for name in (
            "cloud-evaluation.json",
            "cloud-evaluation-raw.json",
            "cloud-evaluation-results.json",
        ):
            path = directory / name
            if path.exists():
                path.rename(attempt / name)
        state = {
            **identity,
            "evaluator_names": list(evaluator_names),
            "evaluator_hash": original_evaluator_hash,
            "retry_of": {
                "evaluation_id": state.get("evaluation_id"),
                "run_id": state.get("run_id"),
            },
        }
    with project_clients(settings, preview=True) as (project, client):
        if catalog_path.exists():
            catalog = read_json(catalog_path)
            if reference_catalog is not None:
                reference = [
                    item for item in read_json(reference_catalog) if item["name"] in evaluator_names
                ]
                if digest(reference) != digest(catalog):
                    raise ValueError(
                        "The requested reference catalog differs from this frozen evaluation."
                    )
        elif reference_catalog is not None:
            source = read_json(reference_catalog)
            catalog = [item for item in source if item["name"] in evaluator_names]
        else:
            catalog = []
            for name in evaluator_names:
                definition = project.beta.evaluators.get_version(
                    f"builtin.{name}", "latest"
                ).as_dict()
                properties = definition["definition"]["init_parameters"]["properties"]
                fields = [field for field in ("model", "deployment_name") if field in properties]
                if len(fields) != 1:
                    raise ValueError(
                        f"Unsupported {name} initialization schema; inspect the actual catalog."
                    )
                parameters = {fields[0]: judge}
                if "threshold" in properties:
                    parameters["threshold"] = 4
                catalog.append({"name": name, "definition": definition, "parameters": parameters})
        if (
            len(catalog) != len(evaluator_names)
            or {item["name"] for item in catalog} != set(evaluator_names)
            or any(not item["definition"].get("version") for item in catalog)
        ):
            raise ValueError("The catalog must pin exactly the requested evaluator versions.")
        for item in catalog:
            parameters = item["parameters"]
            models = [parameters[key] for key in ("model", "deployment_name") if key in parameters]
            if models != [judge]:
                raise ValueError("The frozen evaluator catalog uses a different judge deployment.")
        if state.get("evaluator_hash", digest(catalog)) != digest(catalog):
            raise ValueError("The evaluator catalog changed after job creation.")
        write_json(catalog_path, catalog)
        state["evaluator_hash"] = digest(catalog)
        if "evaluation_id" not in state:
            criteria = [
                TestingCriterionAzureAIEvaluator(
                    type="azure_ai_evaluator",
                    name=item["name"],
                    evaluator_name=f"builtin.{item['name']}",
                    evaluator_version=item["definition"]["version"],
                    initialization_parameters=item["parameters"],
                    data_mapping={
                        "query": "{{item.query}}",
                        "response": "{{item.response}}",
                        **(
                            {"context": "{{item.context}}"}
                            if item["name"] == "groundedness"
                            else {}
                        ),
                    },
                )
                for item in catalog
            ]
            evaluation = client.evals.create(
                name=f"{owned_prefix()}-{safe_label(label)}"[:63],
                data_source_config={
                    "type": "custom",
                    "item_schema": {
                        "type": "object",
                        "properties": {key: {"type": "string"} for key in items[0]},
                        "required": list(items[0]),
                    },
                },
                testing_criteria=criteria,
                metadata={"source_run_id": source_run_id, "dataset_hash": dataset_hash},
            )
            state["evaluation_id"] = evaluation.id
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
                    "The native run is still running. Resume this label; do not submit another job."
                )
            time.sleep(5)
        if run.status != "completed":
            raise ValueError(f"Native evaluation ended with {run.status}; the attempt is retained.")
        raw_items = [
            item.model_dump(mode="json")
            for item in client.evals.runs.output_items.list(
                run_id=state["run_id"], eval_id=state["evaluation_id"]
            )
        ]
        write_json(directory / "cloud-evaluation-raw.json", raw_items)
        try:
            normalized = normalize_results(raw_items, ids, evaluator_names)
        except ValueError:
            state["validation_status"] = "invalid"
            write_json(state_path, state)
            raise
        state["validation_status"] = "valid"
        state["results_hash"] = digest(normalized)
        write_json(directory / "cloud-evaluation-results.json", normalized)
        write_json(state_path, state)
    return {
        "mode": "live",
        "label": label,
        "evaluation_id": state["evaluation_id"],
        "run_id": state["run_id"],
        "report_url": state["report_url"],
        "rows": len(normalized),
        "evaluator_hash": state["evaluator_hash"],
        "native_pass_counts": {
            name: {
                "passed": sum(
                    item["passed"]
                    for row in normalized
                    for item in row["results"]
                    if item["name"] == name
                ),
                "total": len(normalized),
            }
            for name in evaluator_names
        },
        "note": "Native judge scores remain separate from business checks and target-agent execution.",
    }


def verified_native(directory: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    state = read_json(directory / "cloud-evaluation.json")
    results = read_json(directory / "cloud-evaluation-results.json")
    if state.get("status") != "completed" or state.get("validation_status") != "valid":
        raise ValueError("A completed and row-validated native evaluation is required.")
    if state.get("results_hash") != digest(results):
        raise ValueError("Native evaluation results changed after validation.")
    if state["evaluator_hash"] != digest(read_json(directory / "evaluator-catalog.json")):
        raise ValueError("The native evaluator definition changed.")
    return state, results
