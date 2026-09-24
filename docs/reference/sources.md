# Sources and integration lineage

**English** | [한국어](../ko/reference/sources.md)

**We integrated the source modules' learning structures, not their claimed execution results.**
Source check date: September 15, 2026. The commits below remain fixed even if upstream main changes.
New official-reference rows marked checked 2026-09-24 reflect this review refresh, not new workshop execution.
See [consolidation and archive gates](consolidation.md) for self-contained replacement paths and optional-feature limits.

## User-owned source workshops

| Source | Checked commit/date | Incorporated scope |
|---|---|---|
| [microsoft-foundry-labs](https://github.com/junwoojeong100/microsoft-foundry-labs/tree/23e831f367b37d41ea1ad1df47f22b076bc372ff) | `23e831f367b37d41ea1ad1df47f22b076bc372ff` / 2025-12-14 | Original seven topics and portal/code paths |
| [foundry-evaluation](https://github.com/junwoojeong100/foundry-evaluation/tree/0b91e47f88ca4d1a5e1dd961d45ea6b40afbb33b) | `0b91e47f88ca4d1a5e1dd961d45ea6b40afbb33b` / 2026-09-15 | Typed Hosted matrices, preserved failures/lineage, traces and native evaluation |
| [foundry-maf-workshop](https://github.com/junwoojeong100/foundry-maf-workshop/tree/d07c614a616446e63ee50b0b34540b5481aff5b2) | `d07c614a616446e63ee50b0b34540b5481aff5b2` / 2026-07-13 | Model SDK, MAF functions, code-deployment sequence |
| [agent-framework-labs](https://github.com/junwoojeong100/agent-framework-labs/tree/cca14163def4c88616dcd4c93fcfd6441fb08f30) | `cca14163def4c88616dcd4c93fcfd6441fb08f30` / 2026-09-15 | MAF builders, hosted adapters and MCP patterns |
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
| IQ model identity | [Portal keyless model setup](https://learn.microsoft.com/azure/search/get-started-portal-agentic-retrieval#create-a-knowledge-base) · [Model/source/API support](https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-create-knowledge-base) | Search identity, `Cognitive Services User`, source-specific LLM mode |
| IQ Preview request | [2026-08-01-preview retrieve](https://learn.microsoft.com/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true) | `messages`, planning/synthesis, tested `maxOutputSize`; retain endpoint/schema discrepancies |
| Search exercise | [Retrieval quickstart](https://learn.microsoft.com/azure/search/search-get-started-agentic-retrieval?pivots=python) | Index, semantic configuration, identity, costs |
| Evaluation inputs | [Cloud datasets](https://learn.microsoft.com/azure/foundry/observability/how-to/cloud-evaluation-datasets) | Item schema, inline `file_content` |
| Evaluation outputs | [Cloud results](https://learn.microsoft.com/azure/foundry/observability/how-to/cloud-evaluation-results) | Run state, every output page, native scores |
| Automatic trace data | [Traces to dataset](https://learn.microsoft.com/azure/foundry/observability/how-to/traces-to-dataset) | Preview, SDK/role requirements |
| Hosted start | [Quickstart](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent) | Code deployment, existing/new-project cleanup differences |
| Hosted operations | [Concepts](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents) | Service GA, regions, per-session scaling/billing |
| Traces | [Tracing setup](https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup) | App Insights, sensitive data, permissions; checked 2026-09-24 |
| Agent Insights | [Insights](https://learn.microsoft.com/azure/foundry/observability/how-to/agent-insights) | Preview trace scanning, judge model, linked traces, role requirements; checked 2026-09-24 |
| Configure and publish agents | [Configure](https://learn.microsoft.com/azure/foundry/agents/how-to/configure-agent) · [Publish to Copilot/Teams](https://learn.microsoft.com/azure/foundry/agents/how-to/publish-copilot) | Stable endpoint, active version, Agent Applications and M365 publishing boundaries; checked 2026-09-24 |
| Workflows retirement | [Workflow concepts](https://learn.microsoft.com/azure/foundry/agents/concepts/workflow) | Portal Workflows visual Preview retires 2026-12-01; use Microsoft Agent Framework; checked 2026-09-24 |
| Classic agents retirement | [Threads/runs/messages](https://learn.microsoft.com/azure/foundry-classic/agents/concepts/threads-runs-messages) | Classic agents retire 2027-03-31; checked 2026-09-24 |
| Assistants retirement | [Assistants code interpreter](https://learn.microsoft.com/azure/foundry-classic/openai/how-to/code-interpreter) | Azure OpenAI Assistants API retired 2026-08-26; checked 2026-09-24 |
| Classic agent migration | [Migration guide](https://learn.microsoft.com/azure/foundry/agents/how-to/migrate) | Migration from classic agents to current Foundry agents; checked 2026-09-24 |
| Work IQ | [Knowledge source](https://learn.microsoft.com/azure/search/agentic-knowledge-source-how-to-work-iq) | Delegated users, usage billing, user assertion, customer-owned app and federated credential; possible actions |
| Workflow as agent | [Using workflows as agents](https://learn.microsoft.com/agent-framework/workflows/as-agents) | The start executor takes `list[Message]`; use the actual `.as_agent()` and preserve builder behavior |
| Hosted adapter | [Foundry Hosted Agents](https://learn.microsoft.com/agent-framework/hosting/foundry-hosted-agent) | Service GA separate from the prerelease Python package; Responses vs. Invocations |
| Functional workflows | [Functional workflow API](https://learn.microsoft.com/agent-framework/concepts/workflows/functional) | Experimental; not a required prerequisite |
| MAF evaluation | [Foundry evaluation integration](https://learn.microsoft.com/agent-framework/integrations/by-component/evaluation/microsoft-foundry) | Existing-response and agent-target evaluation are separate |
| Agent-target evaluation | [Evaluate agents](https://learn.microsoft.com/azure/foundry/observability/how-to/evaluate-agent) | The service calls the target again; a separate path |
| Hybrid query | [Hybrid query](https://learn.microsoft.com/azure/search/hybrid-search-how-to-query) | Send text and vector together |
| Toolbox | [MAF FoundryToolbox](https://learn.microsoft.com/agent-framework/integrations/by-component/tools/foundry-toolbox) | Managed MCP lifecycle and prepared connection requirements; prerelease |
| Fabric IQ | [Tool guide](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/fabric-iq) | Asset-specific delegated/OBO identity vs. Data Agent MCP app-only identity |
| Operations and recurring evaluation | [Monitoring dashboard](https://learn.microsoft.com/azure/foundry/observability/how-to/how-to-monitor-agents-dashboard) | Batch, trace and recurring sampling have separate conditions |
| AI-103 / AI-102 | [AI-103 study guide](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103) · [AI-102 study guide](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-102) · [retirement announcement](https://learn.microsoft.com/partner-center/announcements/2026-june) | AI-103 skill weights and AI-102 retirement; checked 2026-09-24 |
| Learn path and Applied Skills | [Develop AI agents on Azure](https://learn.microsoft.com/training/paths/develop-ai-agents-on-azure/) · [APL-0302](https://learn.microsoft.com/credentials/applied-skills/resources/study-guides/apl-0302) | Next learning path and task assessment; checked 2026-09-24 |
| Foundry capability map | [Capabilities](https://learn.microsoft.com/azure/foundry/concepts/capabilities) | Specialist coverage map; checked 2026-09-24 |
| Grok Responses support | [Use Grok models](https://learn.microsoft.com/azure/foundry/foundry-models/how-to/use-foundry-models-grok) | Chat Completions and Responses support documented; Structured Outputs still deployment-verified; checked 2026-09-24 |
| Foundry Dev Pack | [Announcement](https://devblogs.microsoft.com/foundry/foundry-devpack-announcement/) · [Installer](https://aka.ms/foundrydevpack) | Installs current Foundry tooling bundle; checked 2026-09-24 |
| Microsoft Foundry skill | [Use the skill](https://learn.microsoft.com/azure/foundry/how-to/develop/use-microsoft-foundry-skill) | Coding-agent integration for Foundry workflows; checked 2026-09-24 |
| Voice-based prompt agents | [Quickstart](https://learn.microsoft.com/azure/foundry/agents/quickstarts/prompt-voice-agent) | Portal voice quickstart; Python SDK support is outside this edition's pins; checked 2026-09-24 |
| Content Understanding | [Overview](https://learn.microsoft.com/azure/ai-services/content-understanding/overview) | Specialist document/receipt extraction design boundary; checked 2026-09-24 |
| Web IQ preview tool | [azure-ai-projects release history](https://pypi.org/project/azure-ai-projects/) | `WebIQPreviewTool` arrived in 2.6.0; checked 2026-09-24 |

Package versions were compared with official PyPI release metadata. An `Unreleased`
section was not treated as an installable release. Older official `ChatAgent`/middleware examples can differ
from the installed SDK; the SDK contract checks compare the installed `Agent`, `ChatContext`, `Workflow.as_agent`
and host routes. A check date does not guarantee support in every subscription or region. [Validation](validation.md)
distinguishes illustrative URLs/IDs/scores from actual execution evidence.
