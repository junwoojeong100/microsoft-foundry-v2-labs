# Versions and feature status: September 13, 2026 snapshot

**English** | [한국어](../ko/reference/versions.md)

<!-- translation-pending: ko-integrated-20260915 -->

> **Translation pending** — The [Korean-first integration revision](../ko/reference/versions.md) is current for the new workflow/evaluation curriculum. This English page retains the earlier material. English expansion and new media follow Korean execution, capture, and corrections.

**The check date is neither a release date nor a guarantee of future support.**
This document translates the edition's recorded official-documentation/source
contracts; it does not predict Ignite 2026 announcements.

## Feature boundaries

| Feature | Choice in this edition | Boundary |
|---|---|---|
| Current Foundry / Agents v2 / Responses | Default | Separate from classic SDK 1.x and threads/runs |
| Prompt Agent | Model/instructions with explicit version | Record actual creation/invocation API |
| MAF | `Agent`, `FoundryChatClient`, `model=` | Provider and core package versions need not match |
| Workflow authoring | Sequential/Concurrent/GroupChat builders | No portal Workflow Designer dependency |
| Ordinary Search | REST `2024-07-01`, text index | Not vector/hybrid search |
| IQ GA | REST `2026-04-01`, `intents` | No separate planner deployment; inspect actual activity and charges |
| Richer IQ | `2026-08-01-preview` | Separate environment/configuration/approval |
| Portal IQ | Portal's own Preview contract | Not assumed identical to GA REST |
| Hosted Agent service | GA, optional deployment | Separate region/permission/session-cost gates |
| Python hosting package | Pinned prerelease | Distinct from service GA |
| Cloud evaluation | Project OpenAI `evals` | Check actual catalog schemas and features |
| Automatic trace-to-dataset | Preview | Default is manual review lineage, not automatic learning |
| Work IQ | Separate Preview, user consent, billing | Disabled by default |

## Pinned direct dependencies

`pyproject.toml` is the installation contract. The compatibility combination was
chosen by comparing release metadata, SDK contracts, and installability in the
authoring environment. Latest published versions may differ.
**Installation, SDK execution, and Azure validation are separate levels**;
[Validation](validation.md) records what was actually checked.

| Area | Package | Pinned version |
|---|---|---|
| Projects | `azure-ai-projects` | 2.3.0 |
| OpenAI interface | `openai` | 2.54.0 |
| Authentication | `azure-identity` | 1.25.3 |
| MAF core | `agent-framework-core` | 1.17.0 |
| Foundry provider | `agent-framework-foundry` | 1.12.0 |
| Orchestration | `agent-framework-orchestrations` | 1.1.1 |
| Local MCP | `mcp` | 1.28.1 |
| Hosted adapter | `agent-framework-foundry-hosting` | 1.0.0b260903 |
| HTTP/environment | `httpx` / `python-dotenv` | 0.28.1 / 1.2.3 |

The MCP table entry was aligned with the existing manifest on September 15, 2026;
this documentation correction does not claim a new Azure compatibility run.

Python 3.13 is recommended; examples use Bash. Offline code targets 3.13–3.14.
Prepare Hosted packages for 3.13. Direct pins are not a full transitive lock.
`requirements.lock.txt` records 103 resolved packages from the authoring environment
(macOS ARM64 / Python 3.13, excluding editable paths and development Ruff).
Recheck installation on other operating systems and remote builders.

Foundry provider 1.12.0 requires Projects SDK `>=2.2.0,<2.4.0`. This edition chose
2.3.0 rather than mixing in metadata's newer Projects 2.6.0, prioritizing
**a mutually installable, API-compatible combination** over "latest of everything."

Prompt-agent invocation explicitly supplies
`agent_reference: {type, name, version}` to the project OpenAI endpoint.
This matches the installed provider's non-preview request contract; it differs from
Preview `get_openai_client(agent_name=...)` binding or implicit latest-version invocation.

## Documented drift

- Keep the full `/api/projects/...` endpoint even if descriptive text abbreviates it.
- GA IQ REST uses `knowledgesources`, not `knowledge-sources`.
- Current evaluator initialization may use `model`, while older examples use
  `deployment_name`. Code inspects and records the actual catalog schema/version.
- Some azd help/troubleshooting retains old manifest/extension terms.
  Compare installed `azd ai agent ... --help` with generated `azure.yaml`.
- Do not mix `https://ai.azure.com/.default` with old Azure OpenAI audience examples;
  let the project SDK manage default inference authentication.

## Freeze immediately before class

1. Install direct/transitive dependencies in a new environment and run `pip check`.
2. Run offline/SDK contracts and a minimal real model request.
3. Verify service/API GA/Preview, regions, model features, quota, and prices.
4. Revalidate prompts, code, data, CLI, both guides, and evaluation after version changes.
5. Do not respond to failure by upgrading everything with `--upgrade --pre`.

Official links and pinned upstream sources are in [Sources](sources.md).
