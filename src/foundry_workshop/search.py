from pathlib import Path
from typing import Any
from urllib.parse import quote

from .contracts import digest, load_documents, read_json, validate_question, write_json
from .knowledge import evidence
from .settings import Settings, azure_endpoint, credential_for, owned_prefix, require_env

SEARCH_API = "2024-07-01"
IQ_API = "2026-04-01"
SEARCH_SCOPE = "https://search.azure.com/.default"


def asset_name(variable: str, suffix: str) -> str:
    import os
    import re

    value = os.environ.get(variable, "").strip() or f"{owned_prefix()}-{suffix}"
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value) or len(value) > 100:
        raise ValueError(f"{variable} must be a lowercase Search object name, not a URL.")
    return value


def search_configuration() -> dict[str, str]:
    return {
        "endpoint": azure_endpoint(require_env("AZURE_SEARCH_ENDPOINT"), "search"),
        "index": asset_name("AZURE_SEARCH_INDEX_NAME", "policies"),
        "source": asset_name("AZURE_SEARCH_KNOWLEDGE_SOURCE_NAME", "source"),
        "knowledge_base": asset_name("AZURE_SEARCH_KNOWLEDGE_BASE_NAME", "kb"),
        "search_api": SEARCH_API,
        "iq_api": IQ_API,
    }


class SearchGateway:
    def __init__(self, settings: Settings):
        import httpx

        self.configuration = search_configuration()
        self.endpoint = self.configuration["endpoint"]
        self.index = self.configuration["index"]
        self.source = self.configuration["source"]
        self.kb = self.configuration["knowledge_base"]
        self.credential = credential_for(settings)
        self.http = httpx.Client(timeout=90, follow_redirects=False)

    def __enter__(self) -> "SearchGateway":
        return self

    def __exit__(self, *_args: Any) -> None:
        self.http.close()
        self.credential.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        api: str,
        body: dict[str, Any] | None = None,
        create_only: bool = False,
    ):
        token = self.credential.get_token(SEARCH_SCOPE)
        headers = {"Authorization": "Bearer " + token.token}
        if create_only:
            headers["If-None-Match"] = "*"
        return self.http.request(
            method,
            f"{self.endpoint}/{path}",
            params={"api-version": api},
            headers=headers,
            json=body,
        )

    def retrieve(self, question: str, provider: str) -> dict[str, Any]:
        validate_question(question)
        if provider == "search":
            response = self.request(
                "POST",
                f"indexes/{self.index}/docs/search",
                api=SEARCH_API,
                body={
                    "search": question,
                    "top": 6,
                    "select": "id,title,content,effective_from,effective_to",
                },
            )
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload.get("value"), list):
                raise ValueError("Search response has no document list.")
            return {
                **evidence(payload["value"], "azure-ai-search-keyword"),
                "configuration": self.configuration,
            }
        if provider != "iq":
            raise ValueError("SearchGateway supports search or iq, never an automatic fallback.")
        response = self.request(
            "POST",
            f"knowledgebases('{self.kb}')/retrieve",
            api=IQ_API,
            body={
                "intents": [{"type": "semantic", "search": question}],
                "includeActivity": True,
                "maxRuntimeInSeconds": 30,
                "maxOutputSizeInTokens": 6000,
                "knowledgeSourceParams": [
                    {
                        "kind": "searchIndex",
                        "knowledgeSourceName": self.source,
                        "includeReferences": True,
                        "includeReferenceSourceData": True,
                    }
                ],
            },
        )
        response.raise_for_status()
        payload = response.json()
        references, activity = payload.get("references"), payload.get("activity")
        if not isinstance(references, list) or not isinstance(activity, list):
            raise ValueError("Foundry IQ must return references and activity arrays.")
        if any(not isinstance(item, dict) or item.get("error") for item in activity):
            raise ValueError("Foundry IQ reported an invalid/failed retrieval activity.")
        documents = {}
        for reference in references:
            if not isinstance(reference, dict):
                raise ValueError("Invalid Foundry IQ reference.")
            source = reference.get("sourceData")
            if not isinstance(source, dict):
                key = reference.get("docKey")
                if not isinstance(key, str) or not key:
                    raise ValueError("IQ reference has neither sourceData nor a document key.")
                lookup = self.request(
                    "GET", f"indexes/{self.index}/docs/{quote(key, safe='')}", api=SEARCH_API
                )
                lookup.raise_for_status()
                source = lookup.json()
            if not isinstance(source.get("id"), str):
                raise ValueError("IQ source data has no stable document ID.")
            documents[source["id"]] = source
        return {
            **evidence(
                list(documents.values()), "foundry-iq", references=references, activity=activity
            ),
            "knowledge_base": self.kb,
            "api_version": IQ_API,
            "configuration": self.configuration,
        }

    def seed(self, root: Path, *, include_iq: bool, confirmed: bool) -> dict[str, Any]:
        if not confirmed:
            raise ValueError(
                "Cloud writes require --confirm-create. Review the lab prerequisites first."
            )
        prefix = owned_prefix()
        for name in (self.index, self.source, self.kb):
            if not name.startswith(prefix + "-"):
                raise ValueError("Refusing to modify an object outside WORKSHOP_PREFIX.")
        documents = load_documents(root)
        scope = {"search_endpoint": self.endpoint, "prefix": prefix}
        ledger_path = root / "outputs/azure-objects.json"
        ledger = (
            read_json(ledger_path)
            if ledger_path.exists()
            else {
                "scope": scope,
                "corpus_hash": digest(documents),
                "objects": [],
            }
        )
        if ledger["scope"] != scope or ledger["corpus_hash"] != digest(documents):
            raise ValueError(
                "Existing ownership ledger has a different scope/corpus. Use a fresh workshop copy."
            )
        index_body = {
            "name": self.index,
            "fields": [
                {"name": "id", "type": "Edm.String", "key": True, "filterable": True},
                {"name": "title", "type": "Edm.String", "searchable": True, "retrievable": True},
                {"name": "content", "type": "Edm.String", "searchable": True, "retrievable": True},
                {
                    "name": "effective_from",
                    "type": "Edm.String",
                    "filterable": True,
                    "retrievable": True,
                },
                {
                    "name": "effective_to",
                    "type": "Edm.String",
                    "filterable": True,
                    "retrievable": True,
                },
            ],
            "semantic": {
                "defaultConfiguration": "policy-semantic",
                "configurations": [
                    {
                        "name": "policy-semantic",
                        "prioritizedFields": {
                            "titleField": {"fieldName": "title"},
                            "prioritizedContentFields": [{"fieldName": "content"}],
                        },
                    }
                ],
            },
        }
        definitions = [(f"indexes/{self.index}", SEARCH_API, index_body)]
        if include_iq:
            definitions.extend(
                [
                    (
                        f"knowledgesources('{self.source}')",
                        IQ_API,
                        {
                            "name": self.source,
                            "kind": "searchIndex",
                            "searchIndexParameters": {
                                "searchIndexName": self.index,
                                "sourceDataFields": [
                                    {"name": field} for field in ("id", "title", "content")
                                ],
                            },
                        },
                    ),
                    (
                        f"knowledgebases('{self.kb}')",
                        IQ_API,
                        {
                            "name": self.kb,
                            "description": "Synthetic workshop policies only.",
                            "knowledgeSources": [{"name": self.source}],
                        },
                    ),
                ]
            )
        for path, api, body in definitions:
            existing = self.request("GET", path, api=api)
            if existing.status_code == 404:
                response = self.request("PUT", path, api=api, body=body, create_only=True)
                response.raise_for_status()
                ledger["objects"].append({"path": path, "api_version": api})
                write_json(ledger_path, ledger)
            elif existing.status_code == 200:
                if path not in {item["path"] for item in ledger["objects"]}:
                    raise ValueError(f"Refusing to overwrite an unowned Search object: {path}")
            else:
                existing.raise_for_status()
            if path.startswith("indexes/"):
                response = self.request(
                    "POST",
                    f"{path}/docs/index",
                    api=SEARCH_API,
                    body={
                        "value": [
                            {"@search.action": "upload", **document} for document in documents
                        ]
                    },
                )
                response.raise_for_status()
                statuses = response.json().get("value")
                if (
                    not isinstance(statuses, list)
                    or len(statuses) != len(documents)
                    or any(item.get("status") is not True for item in statuses)
                    or {item.get("key") for item in statuses}
                    != {document["id"] for document in documents}
                ):
                    raise ValueError(
                        "Partial/missing Search indexing results. Inspect the owned index before retrying."
                    )
        return {
            "mode": "live",
            "index": self.index,
            "knowledge_base": self.kb if include_iq else None,
            "document_count": len(documents),
            "ledger": str(ledger_path),
            "note": "Resource creation is not retrieval verification. Run retrieve separately.",
        }
