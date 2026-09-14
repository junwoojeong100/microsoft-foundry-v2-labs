# Sources and integration lineage

**English** | [한국어](../ko/reference/sources.md)

**We integrated the source modules' learning structures, not their claimed execution results.**
Source check date: September 13, 2026. The commits below remain fixed even if upstream main changes.

## User-owned source workshops

| Source | Checked commit/date | Incorporated scope |
|---|---|---|
| [microsoft-foundry-labs](https://github.com/junwoojeong100/microsoft-foundry-labs/tree/23e831f367b37d41ea1ad1df47f22b076bc372ff) | `23e831f367b37d41ea1ad1df47f22b076bc372ff` / 2025-12-14 | Original seven topics and portal/code paths |
| [foundry-evaluation](https://github.com/junwoojeong100/foundry-evaluation/tree/a73c7b89169aff457b55647e4e68d1610b029860) | `a73c7b89169aff457b55647e4e68d1610b029860` / 2026-09-11 | Learning loop, dev/holdout, failure/source/evaluator lineage |
| [foundry-maf-workshop](https://github.com/junwoojeong100/foundry-maf-workshop/tree/d07c614a616446e63ee50b0b34540b5481aff5b2) | `d07c614a616446e63ee50b0b34540b5481aff5b2` / 2026-07-13 | Model SDK, MAF functions, code-deployment sequence |
| [agent-framework-labs](https://github.com/junwoojeong100/agent-framework-labs/tree/1d3e3652784a421eeeed4c7f3f6b9476208ceb07) | `1d3e3652784a421eeeed4c7f3f6b9476208ceb07` / 2026-07-11 | FoundryChatClient, workflow builders, MCP patterns |
| [microsoft-iq-on-foundry](https://github.com/junwoojeong100/microsoft-iq-on-foundry/tree/fa16c84f9800377823edd9aea1cb20d6a56a1edf) | `fa16c84f9800377823edd9aea1cb20d6a56a1edf` / 2026-07-25 | IQ/Toolbox distinctions, read-only default, approval boundaries for M365 |

This edition's scenario, synthetic data, integrated code, and guides were assembled
for this repository. Root MIT notices retain attribution for the MIT-licensed
MAF Workshop/Agent Framework sources. Whole source repositories or their media were
not indiscriminately copied/reissued. We do not claim MIT covers an entire source
repository whose separate license was not confirmed.

## Official references

Document display/edit dates are not necessarily feature-release dates.

| Topic | Official source | Important contract |
|---|---|---|
| Current Foundry vs. classic | [Migration](https://learn.microsoft.com/azure/foundry/how-to/navigate-from-classic) | SDK 2.x, Agents v2, transition/retirement boundaries |
| Prompt Agent | [Quickstart](https://learn.microsoft.com/azure/foundry/agents/quickstarts/prompt-agent) | `create_version`, project/agent clients |
| Permissions | [Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) | Role names, management/data planes |
| MAF Python | [2026 significant changes](https://learn.microsoft.com/agent-framework/support/upgrade/python-2026-significant-changes) | `FoundryChatClient`, `FoundryAgent`, `model=` |
| MAF samples | [python-1.18.0](https://github.com/microsoft/agent-framework/tree/python-1.18.0/python/samples) | Provider/function-tool API |
| Foundry IQ concepts | [What is Foundry IQ?](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq) | Product roles, portal/REST distinction |
| IQ versions | [Retrieval migration](https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-migrate) | GA `2026-04-01` vs. `2026-08-01-preview` |
| IQ GA REST | [Retrieve](https://learn.microsoft.com/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-04-01&preserve-view=true) | OData paths, intents, references/activity |
| Search exercise | [Retrieval quickstart](https://learn.microsoft.com/azure/search/search-get-started-agentic-retrieval?pivots=python) | Index, semantic configuration, identity, costs |
| Evaluation inputs | [Cloud datasets](https://learn.microsoft.com/azure/foundry/observability/how-to/cloud-evaluation-datasets) | Item schema, inline `file_content` |
| Evaluation outputs | [Cloud results](https://learn.microsoft.com/azure/foundry/observability/how-to/cloud-evaluation-results) | Run state, every output page, native scores |
| Automatic trace data | [Traces to dataset](https://learn.microsoft.com/azure/foundry/observability/how-to/traces-to-dataset) | Preview, SDK/role requirements |
| Hosted start | [Quickstart](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent) | Code deployment, existing/new-project cleanup differences |
| Hosted operations | [Concepts](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents) | Service GA, regions, per-session scaling/billing |
| Traces | [Tracing setup](https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup) | App Insights, sensitive data, permissions |
| Work IQ | [Knowledge source](https://learn.microsoft.com/azure/search/agentic-knowledge-source-how-to-work-iq) | Delegated users, usage billing, possible actions |

Package versions were compared with official PyPI release metadata. An `Unreleased`
section was not treated as an installable release. [Validation](validation.md)
distinguishes illustrative URLs/IDs/scores from actual execution evidence.
