# Lab 10. Fabric IQ, Work IQ, and Toolbox extensions

**English** | [한국어](../ko/labs/10-iq-extensions.md)

**Optional advanced work. Complete the core labs without accessing actual Fabric or Microsoft 365 accounts.**

Next: A/B → [Lab 11](11-capstone.md) · Optional prerequisite: [Lab 06](06-knowledge.md) · [Paths](../paths.md)

## Before you start

**This pass:** Optional extension only. A/B can finish at Lab 11 without this module.

**Need:** Only the synthetic routing exercise is unconditional; external services require separate prepared assets and approval.

**Continue when:** A design-only result is labeled design-only. No Work IQ/Fabric access is implied.

**If blocked:** Stop without consent, billing or user-context requirements; never connect real company data by default.

[One-time setup and learner files](../setup.md).

## Three IQs are not one API

| Product | Main context | Default scope here |
|---|---|---|
| Foundry IQ | Enterprise knowledge, knowledge sources/bases | GA retrieval over a synthetic Search index |
| Fabric IQ | Semantic models, analytics, ontology, OneLake, data agents | Separate connection design only when synthetic assets are prepared |
| Work IQ | Microsoft 365 work/collaboration context | Disabled by default; real user connection needs separate approval |

Do not infer that similarly named products share a key, or that a Copilot license
permits unrestricted app-only backend access.

## 1. Synthetic design exercise for everyone

Without signing into services, design this routing table:

| Question | Appropriate evidence | Required verification |
|---|---|---|
| What is the lodging limit? | Versioned policies / Foundry IQ | Source, effective date, citation |
| What are quarterly travel totals by department? | Synthetic analytics model / Fabric | Aggregation definition, user data permissions |
| What did the travel-review meeting agree? | Approved work context / Work IQ | Consent, delegated permission, sensitive-data protection |

Copy the table into your own `iq-routing-design.txt` and add **source available / identity needed / run or not run** to each row.
Only the bundled policy source exists in the core workshop; no quarterly analytics or meeting dataset is supplied.
Mark Fabric and Work IQ **design-only / not run**. Do not invent their response JSON or company data.

**What to check:** This task produces your own design note. No command here prints connection-status flags or proves a service connection.
If this is your selected scope, stop here and continue to [Lab 11](11-capstone.md).

<details>
<summary>Optional preparation reference: external services need separate assets, permission and cost approval</summary>

## 2. Fabric: only with prepared synthetic assets

Record prerequisites before connecting:

1. A Fabric workspace containing only synthetic data and a currently supported capacity.
2. A published Data Agent/semantic model and source-read permissions.
3. Tenant, network, region, and processing requirements across Foundry/Search/Fabric.
4. Current supported MCP or Foundry tool/knowledge-source integration.
5. Asset-specific identity: ontology/semantic-model paths require delegated/OBO context; published Data Agent MCP may support a separately authorized service principal.
6. Capacity uptime, request costs, and shutdown/restoration plan.

If assets are absent, start with the
[official Fabric Data Agent tutorial](https://learn.microsoft.com/fabric/data-science/data-agent-end-to-end-tutorial).
Preparation is outside the 45–90-minute module.
Use the [self-contained IQ workbook](../reference/iq-workbook.md) and
[current official Fabric IQ guide](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/fabric-iq);
no source-repository clone is required.

**Evidence:** actual user question, selected agent/source, answer/evidence, and
user-context/OBO verification. An administrator's success does not establish every user's access.

## 3. Work IQ: explicit opt-in and additional billing

An administrator first reviews the current
[Work IQ knowledge-source requirements](https://learn.microsoft.com/azure/search/agentic-knowledge-source-how-to-work-iq):
tenant enablement, real user sign-in and assigned usage-based billing;
delegated `WorkIQAgent.Ask` and admin/user consent; network/tenant/support boundaries;
data movement, retention, regulation, and per-user access/deletion policy.
Preview Work IQ may **perform actions**, not merely read.

No repository script automatically enables Work IQ or creates accounts/service
principals. Do not force personal sign-in or paste Graph/M365 tokens.
Owning M365 Copilot alone does not satisfy these requirements.
The September 15 contract includes a Copilot Studio usage-based billing plan with per-user assignments,
tenant enablement, user assertions, `WorkIQAgent.Ask` delegated consent, and a customer-owned Entra app/federated credential
for the `2026-08-01-preview` path. `applicationId` is the client ID; `federatedCredentialId` is the credential object ID.
Do not generalize old same-tenant examples or replace user context with the host identity.

**Stop:** if approval, billing, tenant, delegated access, or action scope is unclear,
remain with synthetic routing. Do not make a real connection.

## 4. Toolbox, remote MCP, and the web

[Lab 04](04-agents-tools.md) uses local MCP. Begin remote-tool extensions with approved
public documentation such as Microsoft Learn.

| Addition | Decide before connecting |
|---|---|
| Microsoft Learn MCP | Trusted server URL, exposed tools, call budget |
| Web Search | Allowed domains, freshness, source URLs, query sensitivity |
| Company API | OpenAPI/MCP schema, input validation, per-user authorization |
| Mutating operation | Separate approval, idempotency, audit and compensation |

Web IQ and ordinary Web Search are not interchangeable.
Tool registration is not proof of a correct result under real permissions.
`FoundryToolbox` belongs to the prerelease hosting package; it does not create the upstream project connection.
Read the [IQ workbook](../reference/iq-workbook.md) for the actual lifecycle, credential, Fabric, and Work IQ boundaries.

## 5. Richer IQ Preview: separate from GA code

The dated compatibility snapshot uses `2026-08-01-preview` for richer experiments.
Message-based planning, reasoning effort, synthesis, and added sources have different
bodies from GA `2026-04-01`. Do not insert Preview fields into `seed-search --iq`.

Use a separate experiment copy, prefix, and configuration following
[official API migration](https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-migrate).
Install any Preview SDK in its own environment; do not upgrade all GA dependencies.
Configure the actual KB model binding rather than unused planner environment placeholders.
Managed identity is supported independently of Preview status.
The [IQ model-identity guide](../reference/iq-model-identity.md) shows the tested planning/synthesis path and its version-specific request fields.
For the bundled Search source, choose the existing **`iq-chat` Luna/SMI preset** in Lab 06 rather than designing a new model binding.
It uses the pinned HTTP client and does not require installing a Preview Search SDK.

</details>

Lab 10 is optional and was not recorded in the September 24 `gpt-6-sol` edition. [Full action index](../action-captures.md) · [Recordings](../video-summary.md)

## Finish

Design-only work created no cloud resources. Do not perform cleanup for services you did not use.
Remove/restore only approved added connections and check owned Fabric capacity,
Work IQ billing, and sessions. Check shared-agent dependencies before stopping capacity.
Never arbitrarily remove another team's connection or organization-wide consent.

Next: A: [skip to Lab 11](11-capstone.md) · B: [skip to Lab 11](11-capstone.md)
