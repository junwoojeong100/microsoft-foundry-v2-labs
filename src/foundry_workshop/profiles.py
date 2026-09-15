import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from .contracts import code_hash, digest, load_documents, load_prompt, parse_json, read_json
from .settings import Settings, azure_endpoint

PATTERNS = ("sequential", "concurrent", "group-chat")
RETRIEVALS = ("local", "search", "iq", "hybrid")
INFERENCE_APIS = ("project-responses", "account-chat")
PROFILE_FILENAME = "runtime-profile.json"


@dataclass(frozen=True)
class RuntimeProfile:
    kind: str = "policy"
    pattern: str = "sequential"
    retrieval: str = "local"
    prompt: str = "v2"
    api: str = "project-responses"
    protocol: str = "responses"

    def __post_init__(self):
        choices = {
            "kind": ("policy", "workflow"),
            "pattern": PATTERNS,
            "retrieval": RETRIEVALS,
            "prompt": ("v1", "v2"),
            "api": INFERENCE_APIS,
            "protocol": ("responses", "invocations"),
        }
        for name, allowed in choices.items():
            if getattr(self, name) not in allowed:
                raise ValueError(f"Runtime {name} must be one of {', '.join(allowed)}.")
        if self.kind == "policy" and self.pattern != "sequential":
            raise ValueError("A workflow pattern requires kind=workflow.")

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: Any) -> "RuntimeProfile":
        if not isinstance(value, dict) or set(value) != set(cls.__dataclass_fields__):
            raise ValueError("Runtime profile must contain exactly the six documented fields.")
        return cls(**value)

    @property
    def package_name(self) -> str:
        if self == RuntimeProfile():
            return "hosted"
        parts = [self.kind]
        if self.kind == "workflow":
            parts.append(self.pattern)
        return "-".join([*parts, self.retrieval, self.prompt, self.api, self.protocol])


def packaged_profile(root: Path) -> RuntimeProfile:
    value = read_json(root / PROFILE_FILENAME)
    if not isinstance(value, dict) or set(value) != {"schema_version", "profile"}:
        raise ValueError("Invalid packaged runtime profile.")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise ValueError("Unsupported packaged runtime profile version.")
    return RuntimeProfile.from_dict(value["profile"])


def model_deployments(settings: Settings) -> dict[str, str]:
    raw = os.environ.get("WORKSHOP_MODEL_DEPLOYMENTS_JSON")
    models = parse_json(raw) if raw is not None else {"primary": settings.deployment}
    if not isinstance(models, dict) or not 1 <= len(models) <= 8:
        raise ValueError("WORKSHOP_MODEL_DEPLOYMENTS_JSON must map 1-8 keys to real deployments.")
    for key, deployment in models.items():
        if not isinstance(key, str) or not re.fullmatch(r"[a-z][a-z0-9-]{0,23}", key):
            raise ValueError("Model keys must be short lowercase names, not paths.")
        if not isinstance(deployment, str) or not re.fullmatch(
            r"[a-zA-Z0-9][a-zA-Z0-9_.-]{0,127}", deployment
        ):
            raise ValueError("Every model key needs an explicit real deployment name.")
    if len(set(models.values())) != len(models):
        raise ValueError("Do not represent the same deployment as multiple model candidates.")
    if settings.deployment not in models.values():
        raise ValueError("The default model deployment must be included in the approved model map.")
    return models


def retrieval_configuration(profile: RuntimeProfile) -> dict[str, Any]:
    if profile.retrieval == "local":
        return {"provider": "local-keyword", "max_documents": 6}
    from .search import search_configuration

    configuration: dict[str, Any] = search_configuration()
    if profile.retrieval == "hybrid":
        from .search import embedding_configuration

        configuration["embedding"] = embedding_configuration()
    return configuration


def validate_inference_endpoint(settings: Settings, profile: RuntimeProfile) -> None:
    if profile.api == "account-chat" and not settings.openai_endpoint:
        raise ValueError("account-chat requires the explicitly configured AZURE_OPENAI_ENDPOINT.")
    if profile.api == "account-chat":
        project = urlsplit(azure_endpoint(settings.project_endpoint, "project")).hostname
        account = urlsplit(azure_endpoint(settings.openai_endpoint, "openai")).hostname
        if (
            not project
            or not account
            or project.removesuffix(".services.ai.azure.com")
            != account.removesuffix(".openai.azure.com")
        ):
            raise ValueError(
                "The explicitly selected account-chat endpoint must belong to the same Foundry account."
            )


def runtime_contract(root: Path, settings: Settings, profile: RuntimeProfile) -> dict[str, Any]:
    validate_inference_endpoint(settings, profile)
    _, prompt_hash = load_prompt(root, profile.prompt)
    from .runtime import instruction_snapshot

    instructions = instruction_snapshot(root, profile)
    execution_path = "case-isolated-maf-pipeline"
    if profile == RuntimeProfile():
        from .agents import policy_instructions

        instructions = {
            "HanbitPolicyGuide": policy_instructions(root)
            + "\n반드시 lookup_policy로 근거를 조회한 뒤 답하세요."
        }
        execution_path = "legacy-maf-function-agent"
    return {
        "schema_version": 1,
        "profile": profile.to_dict(),
        "models": model_deployments(settings),
        "project_endpoint": settings.project_endpoint,
        "inference_endpoint": settings.openai_endpoint
        if profile.api == "account-chat"
        else settings.project_endpoint,
        "max_output_tokens": settings.max_output_tokens,
        "prompt_hash": prompt_hash,
        "effective_prompt_hash": digest(instructions),
        "execution_path": execution_path,
        "corpus_hash": digest(load_documents(root)),
        "code_hash": code_hash(root),
        "retrieval_configuration": retrieval_configuration(profile),
        "side_effects": "read-only-synthetic-policy-guidance",
    }
