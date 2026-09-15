import json
import math
from pathlib import Path
from typing import Any

from .contracts import safe_label
from .evaluation import load_run
from .settings import Settings

EVALUATORS = ("groundedness", "relevance")


def normalize_results(
    items: list[dict[str, Any]], row_ids: list[str], evaluator_names: tuple[str, ...] = EVALUATORS
) -> list[dict[str, Any]]:
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
        if not isinstance(results, list) or len(results) != len(evaluator_names):
            raise ValueError("Missing evaluator results.")
        if {result.get("name") for result in results} != set(evaluator_names):
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
    from .native import evaluate_items

    if not confirmed:
        raise ValueError("Cloud judges are billable. Explicitly pass --confirm-cost.")
    if not 5 <= timeout <= 900:
        raise ValueError("Evaluation timeout must be 5-900 seconds.")
    manifest, rows, cases = load_run(root, safe_label(label))
    if manifest["mode"] != "live" or any(row["status"] != "ok" for row in rows):
        raise ValueError("Cloud evaluation requires a complete real run with no collection errors.")
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
    return evaluate_items(
        settings,
        root / "outputs" / label,
        items,
        label=label,
        source_run_id=manifest["run_id"],
        dataset_hash=manifest["dataset_hash"],
        forbidden_deployments={manifest["deployment"]},
        evaluator_names=EVALUATORS,
        confirmed=confirmed,
        timeout=timeout,
    )
