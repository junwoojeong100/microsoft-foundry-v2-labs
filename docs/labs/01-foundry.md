# Lab 01. Understand Foundry and prepare a project

**English** | [한국어](../ko/labs/01-foundry.md)

**Goal:** Explain the relationship between Foundry, Agent Framework, model deployments, and agents.

Next: A → [Lab 02](02-models.md) · B: [skip to Lab 02](02-models.md) · [Paths](../paths.md)

## Before you start

**This pass:** A verifies the prepared project; environment owners use section 2 only if it is not prepared.

**Need:** The setup card's tenant, project, account and gpt-5.6-luna deployment.

**Continue when:** You can distinguish account, project, deployment and agent, and identify your own endpoint.

**If blocked:** Stop if the project is missing; resolve tenant/RBAC rather than following a similarly named project.

[One-time setup and learner files](../setup.md).

## Distinguish four concepts

| Concept | Plain-language meaning | Workshop example |
|---|---|---|
| Foundry resource | Azure resource operating AI services | Training Foundry account |
| Project | Workspace for agents, connections, and evaluations | Hanbit Technology training project |
| Model deployment | Configuration exposing a model/version/SKU for calls | This preset's invocation name: `gpt-5.6-luna` |
| Agent | Model plus instructions, tools, and execution behavior | Travel-policy assistant |

**Foundry is the cloud platform. Microsoft Agent Framework (MAF) is the open-source
SDK for building agents and workflows in code.** Local MAF can still make billable Azure model calls.

```mermaid
flowchart TD
    S["Azure subscription / Billing and administration"] --> R["Resource Group"]
    R --> F["Foundry resource"]
    F --> D["Model deployment / Actual invocation name"]
    F --> P["Foundry project"]
    P --> A["Agents and versions"]
    P --> C["Knowledge and tool connections"]
    P --> E["Evaluation and observability"]
    D --> A
```

## 1. Check the prepared environment

1. Open the current Foundry experience and training project at `https://ai.azure.com`.
2. Record project name, resource name, and connected model deployment.
3. Locate agents, models, and evaluation/observability within the same project.
4. Menu labels vary by language and rollout. Navigate by the **object to verify**,
   such as "the project's model deployments," rather than memorizing screen coordinates.
5. If you encounter a classic Hub project or threads/runs code, use the
   [migration map](../reference/migration.md). Do not combine incompatible APIs.



**What to check:** **View deployments** opens model deployments; **Start building**
starts agent creation. They are distinct assets even inside the same project.

## 2. No environment yet: instructor/administrator preparation

These steps are outside participant class time and require separate authorization.

1. Select a training subscription and dedicated resource group.
2. Create a Foundry resource and current project following the
   [official quickstart](https://learn.microsoft.com/azure/foundry/quickstarts/get-started-code).
3. Verify **model/SKU/quota** before choosing a region. If using Hosted, separately
   check [Hosted regions](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents);
   the region lists need not match.
4. Prepare `gpt-5.6-luna`, model version `2026-07-09`, with the exact deployment name `gpt-5.6-luna`.
   Check availability rather than copying a recording's region/SKU/capacity.
5. Assign necessary project roles and wait for propagation.
6. Verify an actual model request with a learner account.
7. Prepare Search, Application Insights, and Hosted only for selected modules.

Resource-creation permission does not imply model-invocation permission.
**Management-plane and data-plane permissions differ.** Do not give every learner subscription Owner.


The September 15 recording reused an existing approved resource group/project; it did not create them.
Use [the environment-owner checklist](../setup.md#4-environment-owner-checklist) for preparation, not commands transcribed from a recording.

## 3. Starting points for least privilege

| Actor | Starting role | Scope |
|---|---|---|
| Learner developing agents/evaluations | `Foundry User` | Training project |
| Caller of an existing agent | `Foundry Agent Consumer` | Relevant agent |
| Hosted deployer to an existing project | Deployment-guide roles such as `Foundry Project Manager` | Relevant project |
| Resource/role preparer | Creation and required role-assignment permissions | Dedicated training scope |
| Log reader | Such as `Log Analytics Reader` | Connected observability resource |

Names may still display as `Azure AI User`; renaming does not change existing role IDs.
Check additional permissions and IDs in [official RBAC guidance](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).
The user, Search managed identity, and Hosted agent identity are separate principals.

## 4. Do not confuse endpoints

| Purpose | Shape |
|---|---|
| Project SDK | `https://<account>.services.ai.azure.com/api/projects/<project>` |
| Account Azure OpenAI API | `https://<account>.openai.azure.com/openai/v1/` |
| Azure AI Search | `https://<search>.search.windows.net` |
| Browser portal | `https://ai.azure.com` — **not an SDK endpoint** |

Keep `/api/projects/<project>` in the project endpoint. The project SDK handles
authentication and endpoints for default inference. Do not silently redirect to
another endpoint or guess a different token audience.


**What to check:** Compare the deployment returned by `doctor --cloud` with your
settings. ARM read access does not establish inference permission; complete [Lab 02](02-models.md).

<details>
<summary>Recorded reference screens (optional; not steps to repeat)</summary>

These are newly recorded English actions using the separate English prompt/data bundle. Use your own returned resource IDs and record your own results.

![Inspect the real project in the English UI](../assets/refresh-20260915-en/screenshots/EP01-001-home-2.webp)

**What to check:** Check the actual project/account endpoint and your own deployment configuration; a preflight is not inference.

![Distinguish project and account endpoints](../assets/refresh-20260915-en/screenshots/EP01-002-endpoint-2.webp)

**What to check:** Check the actual project/account endpoint and your own deployment configuration; a preflight is not inference.

![Verify the approved existing project](../assets/refresh-20260915-en/screenshots/E01-002-preflight-2.webp)

**What to check:** Check the actual project/account endpoint and your own deployment configuration; a preflight is not inference.

[Full action index](../action-captures.md) · [Recordings](../video-summary.md)

</details>

## Completion

Explain whether knowledge and evaluation criteria can remain when a model is replaced.
A deployment can change, but that does not automatically revalidate knowledge,
instructions, evaluation, or permissions. Later modules deliberately reuse the same data and criteria.

Next: A → [Lab 02](02-models.md) · B: [skip to Lab 02](02-models.md)
