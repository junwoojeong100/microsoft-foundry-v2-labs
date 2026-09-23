# Versions and feature boundaries — September 15, 2026

**English** | [한국어](../ko/reference/versions.md)

**A compatibility check date is not a release date or a future support guarantee.**
This edition does not predict Ignite announcements or universal tenant/region availability.

## Verified contracts

The workshop code edition is `2026.9.15`.
Direct Python dependency versions remain the known-compatible set below.
Installed-SDK/transport-stub checks and actual Azure execution are separate evidence.

| Area | Contract |
|---|---|
| Answer model preset | `gpt-6-sol` / `2026-09-22` from September 23, 2026, with a separate `gpt-6-sol-judge`. The checked agent paths and recorded main A/B steps passed; `gpt-6-luna` failed on the agent path that day. [Model choice](model-choice.md) |
| Current Foundry | Projects SDK 2.x and Responses, separate from classic threads/runs |
| MAF | `Agent`, provider `model=`, sequential/concurrent/group-chat builders |
| Workflow host | Actual `Workflow.as_agent()` and ResponsesHostServer |
| Evaluation host | InvocationAgentServerHost, local POST `/invocations`, four query-only fields |
| Service-call lineage | Actual ChatResponse ID/model/usage, not the workflow wrapper UUID |
| Middleware | Pinned core 1.17.0 uses `await call_next()`, not older `next(context)` examples |
| Functional workflows | Experimental; not a mandatory prerequisite |
| Keyword Search | REST `2024-07-01`; do not call it hybrid |
| Hybrid | Actual embedding dimensions and text/vector requests; explicit project/account API selection |
| IQ GA | REST `2026-04-01`, intents/minimal/extractive |
| Richer IQ | `2026-08-01-preview`, separate settings/approval |
| IQ Chat model + managed identity | Verified on 2026-09-15: Search SMI → `gpt-5.6-luna`, `low` planning + `answerSynthesis`, HTTP 200. MI itself is not the Preview feature; [exact setup and request contract](iq-model-identity.md) |
| First-pass chat preset | `iq-chat check/setup/ask`: deployment/model `gpt-5.6-luna`, version `2026-07-09`, Search SMI, `2026-08-01-preview`, separate owned chat base. Search accepted no GPT-6 model on 2026-09-23, so this preset did not follow the answer model. New command preflight was read-only; earlier temporary-base inference remains separate |
| Hosted service vs package | Service status and prerelease Python package status are independent |
| Native evaluation | Actual catalog initialization schema and pinned evaluator/version/threshold |
| Work IQ/Fabric/Toolbox | Separate service-specific access, identity, billing, and Preview conditions |

## CLI compatibility

The initial environment had azd 1.31.1 and microsoft.foundry 1.0.0-beta.2.
Installed agents 1.0.0-beta.10 and projects 1.0.0-beta.6 were marked incompatible with that CLI.
The live follow-up used a checksum-verified **session-local azd 1.34.0**;
the shared global CLI was not replaced, and the existing extensions became compatible.

Before your deployment, verify the actual installed help/schema and an approved compatible combination.
Do not blindly upgrade every package/extension after an error.
See [azd installation](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
and [Hosted quickstart](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent).

## Pinned direct dependencies

`pyproject.toml` is authoritative.

| Package | Version |
|---|---|
| `azure-ai-projects` | 2.3.0 |
| `azure-identity` | 1.25.3 |
| `openai` | 2.54.0 |
| `httpx` | 0.28.1 |
| `python-dotenv` | 1.2.3 |
| `agent-framework-core` | 1.17.0 |
| `agent-framework-foundry` | 1.12.0 |
| `agent-framework-orchestrations` | 1.1.1 |
| `mcp` | 1.28.1 |
| `agent-framework-foundry-hosting` | 1.0.0b260903 |

Use Python 3.13 for Hosted packages. Offline code is tested on 3.13–3.14.
The provider requires Projects SDK `>=2.2.0,<2.4.0`; the newest independent package versions are not necessarily compatible.
The resolved lock file describes the authoring platform, not every OS or remote build.
Record the actual remote build's resolved versions.

## Drift found during real execution

- Full project endpoints retain `/api/projects/...`.
- A full `--agent-endpoint` already identifies its protocol; do not also pass `--protocol`.
- Adding a session parameter must preserve the endpoint's API-version query.
- Project embeddings returned 404 in the live environment. The account API was selected explicitly, not used as an automatic fallback.
- Project requests use the AI audience; explicitly selected account inference uses the Cognitive Services audience.
- App Insights needs its own audience and the intended subscription/tenant credential.
- Already-idle sessions are verified without another conflicting stop request.

## Freeze before teaching

Check dependencies, offline/SDK contracts, one real model request, model/SKU/region/quota/cost,
and actual generated configuration. Reverify related commands, code, data, guides, and evaluation when versions change.
Official sources and immutable comparison points are in [sources](sources.md).
