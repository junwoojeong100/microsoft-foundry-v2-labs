import argparse
import asyncio
import json
import subprocess
import sys
import traceback
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .contracts import load_cases, load_documents, read_json, validate_question
from .evaluation import acceptance_report, compare_runs, evaluate_run, record_feedback
from .experiments import collect, offline_demo
from .knowledge import local_retrieve
from .profiles import INFERENCE_APIS, PATTERNS, RETRIEVALS, RuntimeProfile

DEFAULT_QUESTION = "2026년 9월 국내 출장 숙박비는 1박 얼마까지인가요?"
DEFAULT_QUESTION_EN = (
    "What is the domestic business-trip lodging limit per night for September 2026?"
)


def runtime_arguments(command: argparse.ArgumentParser, *, default_kind: str = "policy") -> None:
    command.add_argument("--kind", choices=("policy", "workflow"), default=default_kind)
    command.add_argument("--pattern", choices=PATTERNS, default="sequential")
    command.add_argument("--retrieval", choices=RETRIEVALS, default="local")
    command.add_argument("--prompt", choices=("v1", "v2"), default="v2")
    command.add_argument("--api", choices=INFERENCE_APIS, default="project-responses")
    command.add_argument("--protocol", choices=("responses", "invocations"), default="responses")


def runtime_profile(args: argparse.Namespace) -> RuntimeProfile:
    return RuntimeProfile(
        **{key: getattr(args, key) for key in RuntimeProfile.__dataclass_fields__}
    )


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Microsoft Foundry v2 workshop (separate Korean/English synthetic assets)."
    )
    result.add_argument("--language", choices=("ko", "en"), default="ko")
    result.add_argument(
        "--debug", action="store_true", help="Print the error stack for local diagnosis."
    )
    commands = result.add_subparsers(dest="command", required=True)
    doctor = commands.add_parser(
        "doctor", help="Read-only prerequisite checks; offline by default."
    )
    doctor.add_argument("--cloud", action="store_true")
    demo = commands.add_parser(
        "demo", help="OFFLINE teaching fixtures; never calls an LLM or Azure."
    )
    demo.add_argument("--label", default="demo-" + datetime.now(UTC).strftime("%Y%m%d-%H%M%S"))
    demo.add_argument("--prompt", choices=("v1", "v2"), default="v2")
    retrieve = commands.add_parser(
        "retrieve", help="Read evidence; local keyword search by default."
    )
    retrieve.add_argument("--provider", choices=RETRIEVALS, default="local")
    retrieve.add_argument("--question")
    for name in ("model", "answer", "maf", "workflow"):
        command = commands.add_parser(
            name, help="LIVE: calls your configured billable Azure model."
        )
        command.add_argument("--question")
        if name == "answer":
            command.add_argument("--prompt", choices=("v1", "v2"), default="v2")
            command.add_argument("--retrieval", choices=RETRIEVALS, default="local")
        if name == "maf":
            group = command.add_mutually_exclusive_group()
            group.add_argument("--tools", action="store_true")
            group.add_argument("--mcp", action="store_true")
        if name == "workflow":
            command.add_argument(
                "--pattern",
                choices=("sequential", "concurrent", "group-chat"),
                default="sequential",
            )
    wrapped = commands.add_parser(
        "workflow-agent",
        help="LIVE: run a case-isolated workflow with validated answer and model-call lineage.",
    )
    wrapped.add_argument("--question")
    runtime_arguments(wrapped, default_kind="workflow")
    contract = commands.add_parser(
        "runtime-contract",
        help="Read local code/prompt/configuration hashes; no Azure request or deployment.",
    )
    runtime_arguments(contract)
    benchmark = commands.add_parser(
        "benchmark",
        help="Version-pinned Hosted model matrix, native judges, regressions and release evidence.",
    )
    benchmark_actions = benchmark.add_subparsers(dest="benchmark_action", required=True)
    for action in ("plan", "collect", "smoke"):
        operation = benchmark_actions.add_parser(action)
        runtime_arguments(operation)
        operation.set_defaults(protocol="invocations")
        if action == "collect":
            operation.add_argument("--label", required=True)
            operation.add_argument("--split", choices=("dev", "holdout"), default="dev")
            operation.add_argument("--model-key", action="append")
            operation.add_argument("--concurrency", type=int, default=1)
            operation.add_argument("--candidate")
            operation.add_argument("--unlock-holdout", action="store_true")
            operation.add_argument("--regressions")
            operation.add_argument("--confirm-cost", action="store_true")
        elif action == "smoke":
            operation.add_argument("--label", required=True)
            operation.add_argument("--local", action="store_true")
            operation.add_argument("--case", default="D01")
            operation.add_argument("--model-key")
            operation.add_argument("--confirm-cost", action="store_true")
    matrix_eval = benchmark_actions.add_parser("evaluate")
    matrix_eval.add_argument("--label", required=True)
    matrix_eval.add_argument("--reference")
    matrix_eval.add_argument("--timeout", type=int, default=300)
    matrix_eval.add_argument("--retry-failed", action="store_true")
    matrix_eval.add_argument("--confirm-cost", action="store_true")
    matrix_compare = benchmark_actions.add_parser("compare")
    matrix_compare.add_argument("--baseline", required=True)
    matrix_compare.add_argument("--candidate", required=True)
    for action in ("report", "trace-plan", "monitor", "stop-session"):
        operation = benchmark_actions.add_parser(action)
        operation.add_argument("--label", required=True)
    regression = benchmark_actions.add_parser("regression")
    regression.add_argument("--label", required=True)
    regression.add_argument("--row-id", required=True)
    regression.add_argument("--regression-label", required=True)
    regression.add_argument("--reviewer", required=True)
    regression.add_argument("--reason", required=True)
    regression.add_argument("--confirm-review", action="store_true")
    verify = benchmark_actions.add_parser("verify")
    verify.add_argument("--baseline", required=True)
    verify.add_argument("--candidate", required=True)
    verify.add_argument("--holdout", required=True)
    verify.add_argument("--require-native", action="store_true")
    verify.add_argument("--require-traces", action="store_true")
    verify.add_argument("--require-native-pass", action="store_true")
    verify.add_argument("--require-regressions", action="store_true")
    verify.add_argument("--calibration")
    calibration = commands.add_parser(
        "calibrate-judge",
        help="LIVE judge over bundled calibration fixtures; no target-agent responses.",
    )
    calibration.add_argument("--label", required=True)
    calibration.add_argument("--reference")
    calibration.add_argument("--timeout", type=int, default=300)
    calibration.add_argument("--confirm-cost", action="store_true")
    batch = commands.add_parser(
        "collect", help="LIVE: collect all cases, keeping errors in the denominator."
    )
    batch.add_argument("--label", required=True)
    batch.add_argument("--split", choices=("dev", "holdout"), default="dev")
    batch.add_argument("--prompt", choices=("v1", "v2"), default="v1")
    batch.add_argument("--retrieval", choices=RETRIEVALS, default="local")
    batch.add_argument("--unlock-holdout", action="store_true")
    batch.add_argument("--candidate", help="Frozen real dev label; required for holdout.")
    grade = commands.add_parser(
        "evaluate", help="Deterministic local business checks; no judge/model call."
    )
    grade.add_argument("--label", required=True)
    compare = commands.add_parser(
        "compare", help="Compare controlled dev experiments without deploying."
    )
    compare.add_argument("--baseline", required=True)
    compare.add_argument("--candidate", required=True)
    compare.add_argument("--variable", choices=("prompt", "model"), default="prompt")
    accept = commands.add_parser(
        "accept", help="Produce a real candidate/holdout handoff, never a deployment approval."
    )
    accept.add_argument("--candidate", required=True)
    accept.add_argument("--holdout", required=True)
    feedback = commands.add_parser(
        "feedback", help="Queue a real dev failure for human review; never auto-approve."
    )
    feedback.add_argument("--label", required=True)
    feedback.add_argument("--case", required=True)
    feedback.add_argument("--reason", required=True)
    judge = commands.add_parser(
        "cloud-evaluate", help="LIVE: billable Foundry judges over already-collected responses."
    )
    judge.add_argument("--label", required=True)
    judge.add_argument("--timeout", type=int, default=300)
    judge.add_argument("--confirm-cost", action="store_true")
    seed = commands.add_parser(
        "seed-search", help="Create namespaced Search objects in an existing service."
    )
    seed.add_argument("--iq", action="store_true")
    seed.add_argument("--hybrid", action="store_true")
    seed.add_argument("--confirm-cost", action="store_true")
    seed.add_argument("--confirm-create", action="store_true")
    iq_chat = commands.add_parser(
        "iq-chat",
        help="Fixed Luna + Search managed identity preset; separate from model-free GA retrieval.",
    )
    iq_actions = iq_chat.add_subparsers(dest="iq_chat_action", required=True)
    iq_actions.add_parser(
        "check", help="Read-only model, Search identity, role and source preflight."
    )
    iq_setup = iq_actions.add_parser(
        "setup", help="Create only the owned chat base after a successful preflight."
    )
    iq_setup.add_argument("--confirm-create", action="store_true")
    iq_ask = iq_actions.add_parser(
        "ask", help="Billable IQ planning and answer synthesis with recorded evidence."
    )
    iq_ask.add_argument("--question")
    iq_ask.add_argument("--label", required=True)
    iq_ask.add_argument("--confirm-cost", action="store_true")
    agent = commands.add_parser(
        "prompt-agent", help="Create/invoke a real, service-managed prompt agent."
    )
    agent.add_argument("action", choices=("create", "invoke"))
    agent.add_argument("--name", required=True)
    agent.add_argument("--version")
    agent.add_argument("--question")
    agent.add_argument("--confirm-create", action="store_true")
    server = commands.add_parser(
        "serve", help="Run the optional local hosted-agent server. Inference remains billable."
    )
    runtime_arguments(server)
    commands.add_parser(
        "cleanup-plan", help="List local ownership records. Does NOT delete Azure resources."
    )
    return result


def doctor_offline(root: Path, language: str = "ko") -> dict[str, Any]:
    if not (3, 13) <= sys.version_info[:2] < (3, 15):
        raise ValueError("Use Python 3.13 (recommended) or 3.14.")
    documents = load_documents(root, language)
    dev, holdout = load_cases(root, "dev", language), load_cases(root, "holdout", language)
    if {case["case_id"] for case in dev} & {case["case_id"] for case in holdout}:
        raise ValueError("Dev and holdout IDs overlap.")
    if {case["question"] for case in dev} & {case["question"] for case in holdout}:
        raise ValueError("Dev and holdout questions overlap.")
    return {
        "mode": "offline-check",
        "language": language,
        "python": sys.version.split()[0],
        "documents": len(documents),
        "dev_cases": len(dev),
        "holdout_cases": len(holdout),
        "azure_tested": False,
        "result": "PASS",
    }


def cloud_command(root: Path, args: argparse.Namespace) -> dict[str, Any] | None:
    if args.debug:
        print(f"Python executable: {sys.executable}; prefix: {sys.prefix}", file=sys.stderr)
    import httpx
    from azure.core.exceptions import AzureError
    from openai import OpenAIError

    from .cloud import (
        answer_with_context,
        call_model,
        create_prompt_agent,
        doctor_cloud,
        invoke_prompt_agent,
        project_clients,
        retrieve,
    )
    from .settings import Settings, load_environment

    load_environment(root)
    settings = Settings.from_env(language=args.language)
    if hasattr(args, "question"):
        validate_question(args.question)
    try:
        if args.command == "iq-chat":
            from .iq_chat import ask, check, setup

            if args.iq_chat_action == "check":
                return check(root, settings)
            if args.iq_chat_action == "setup":
                return setup(root, settings, confirmed=args.confirm_create)
            return ask(root, settings, args.question, args.label, confirmed=args.confirm_cost)
        if args.command == "runtime-contract":
            from .contracts import digest
            from .profiles import runtime_contract

            contract = runtime_contract(root, settings, runtime_profile(args))
            return {
                "runtime_contract": contract,
                "contract_hash": digest(contract),
                "azure_verified": False,
            }
        if args.command == "calibrate-judge":
            from .benchmark import directory
            from .calibration import calibrate

            return calibrate(
                root,
                settings,
                args.label,
                confirmed=args.confirm_cost,
                timeout=args.timeout,
                reference_catalog=directory(root, args.reference) / "evaluator-catalog.json"
                if args.reference
                else None,
            )
        if args.command == "workflow-agent":
            from .runtime import run_pipeline

            async def execute_workflow():
                return await asyncio.wait_for(
                    run_pipeline(settings, root, args.question, runtime_profile(args)), timeout=240
                )

            return asyncio.run(execute_workflow())
        if args.command == "doctor":
            return doctor_cloud(settings)
        if args.command == "retrieve":
            return retrieve(root, settings, args.question, args.provider)
        if args.command == "seed-search":
            from .search import SearchGateway

            with SearchGateway(settings) as gateway:
                return gateway.seed(
                    root,
                    include_iq=args.iq,
                    confirmed=args.confirm_create,
                    hybrid=args.hybrid,
                    confirm_embedding_cost=args.confirm_cost,
                )
        if args.command == "cloud-evaluate":
            from .cloud_evaluation import evaluate_cloud

            return evaluate_cloud(
                root, settings, args.label, timeout=args.timeout, confirmed=args.confirm_cost
            )
        if args.command in {"maf", "workflow", "serve"}:
            from .agents import run_agent, run_workflow, serve

            if args.command == "maf":
                return asyncio.run(
                    run_agent(settings, root, args.question, tools=args.tools, mcp=args.mcp)
                )
            if args.command == "workflow":
                return asyncio.run(run_workflow(settings, root, args.question, args.pattern))
            serve(settings, root, runtime_profile(args))
            return None
        if args.command == "collect" and args.split == "holdout" and not args.unlock_holdout:
            raise ValueError("Freeze the candidate first, then explicitly pass --unlock-holdout.")
        with project_clients(settings) as (project, client):
            if args.command == "model":
                return call_model(client, settings, args.question)
            if args.command == "prompt-agent":
                if args.action == "create":
                    return create_prompt_agent(
                        project, settings, root, args.name, confirmed=args.confirm_create
                    )
                if not args.version:
                    raise ValueError(
                        "Invoke requires an explicit --version from the created agent."
                    )
                return invoke_prompt_agent(client, args.name, args.version, args.question)
            if args.command == "answer":
                context = retrieve(root, settings, args.question, args.retrieval)
                return answer_with_context(
                    client, settings, root, args.question, args.prompt, context
                )
            if args.command == "collect":
                from .profiles import retrieval_configuration

                def answer_case(case: dict[str, Any]) -> dict[str, Any]:
                    context = retrieve(root, settings, case["question"], args.retrieval)
                    return answer_with_context(
                        client, settings, root, case["question"], args.prompt, context
                    )

                return collect(
                    root,
                    label=args.label,
                    split=args.split,
                    prompt_version=args.prompt,
                    retrieval=args.retrieval,
                    mode="live",
                    deployment=settings.deployment,
                    answer_case=answer_case,
                    recoverable_errors=(ValueError, AzureError, OpenAIError, httpx.HTTPError),
                    inference={
                        "project_endpoint": settings.project_endpoint,
                        "api": "project-responses",
                        "max_output_tokens": settings.max_output_tokens,
                        "retrieval_configuration": retrieval_configuration(
                            RuntimeProfile(retrieval=args.retrieval, language=args.language)
                        ),
                    },
                    candidate=args.candidate,
                    language=args.language,
                )
    except (AzureError, OpenAIError, httpx.HTTPError) as exc:
        status = (
            exc.response.status_code
            if isinstance(exc, httpx.HTTPStatusError)
            else getattr(exc, "status_code", None)
        )
        if args.debug and isinstance(exc, httpx.HTTPStatusError):
            print(f"Service error: {exc.response.text[:2000]}", file=sys.stderr)
        raise ValueError(
            f"Azure request failed: {type(exc).__name__}, HTTP {status}. "
            "See docs/reference/troubleshooting.md. No provider/model fallback was used."
        ) from exc
    raise ValueError("Unsupported cloud command.")


def main(root: Path, argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if hasattr(args, "question") and args.question is None:
        args.question = DEFAULT_QUESTION_EN if args.language == "en" else DEFAULT_QUESTION
    try:
        if args.command == "doctor" and not args.cloud:
            result = doctor_offline(root, args.language)
        elif args.command == "benchmark":
            from .benchmark_cli import execute

            result = execute(root, args)
        elif args.command == "demo":
            result = offline_demo(root, args.label, args.prompt, language=args.language)
        elif args.command == "retrieve" and args.provider == "local":
            result = local_retrieve(root, args.question, language=args.language)
        elif args.command == "evaluate":
            result = evaluate_run(root, args.label)
        elif args.command == "compare":
            result = compare_runs(root, args.baseline, args.candidate, args.variable)
        elif args.command == "accept":
            result = acceptance_report(root, args.candidate, args.holdout)
        elif args.command == "feedback":
            result = {
                "review_record": str(record_feedback(root, args.label, args.case, args.reason))
            }
        elif args.command == "cleanup-plan":
            ledger_path = root / "outputs/azure-objects.json"
            result = {
                "deletes_resources": False,
                "search_ownership": read_json(ledger_path) if ledger_path.exists() else None,
                "required_manual_inventory": [
                    "prompt/hosted agent versions and active sessions",
                    "Foundry model deployments",
                    "Search service and owned index/source/base",
                    "Application Insights / Log Analytics / storage",
                    "separately created Fabric / Work IQ assets, if any",
                ],
                "guide": "docs/reference/cleanup.md",
            }
        else:
            result = cloud_command(root, args)
        if result is not None:
            print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        if args.command in {"evaluate", "accept"} and not result["business_gate_passed"]:
            return 1
        if args.command == "collect" and result["errors"]:
            return 1
        if isinstance(result, dict) and result.get("gate_passed") is False:
            return 1
        return 0
    except (OSError, ValueError, ImportError, TimeoutError, subprocess.SubprocessError) as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        if args.debug:
            traceback.print_exc()
        if isinstance(exc, ImportError):
            print(
                'Install the matching optional dependencies: python -m pip install -e ".[cloud]" or ".[agents,hosted]".',
                file=sys.stderr,
            )
        return 2
