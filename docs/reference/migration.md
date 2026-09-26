# From the 2025 integrated labs to v2

**English** | [한국어](../ko/reference/migration.md)

**The concepts continue; execution contracts and learning paths were rebuilt.**
The original integrated workshop's last checked commit is dated December 14, 2025.

| Original module | v2 location | Change |
|---|---|---|
| 01. Environment | 00–01 | Separate browser/Python paths; no learner subscription Owner requirement |
| 02. Models/Router | 02 + 07 | Pin deployment names; distinguish fixed-model comparisons and routing |
| 03. Agents/tools | 03–04 | Managed Prompt Agent vs. local MAF; synthetic read-only tools |
| 04. Foundry IQ | 06 + 10 | GA intents vs. richer Preview; reference numbers vs. document IDs |
| 05. Portal workflow | 05 + 08 | MAF code instead of portal authoring; human-review/Hosted boundaries |
| 06. Evaluation | 07 | Dev/holdout, errors in denominator, frozen candidate, evaluator lineage |
| 07. Control Plane | 09 | Operational gates for versions, roles, traces, quota, costs, cleanup |

## How the smaller workshops were integrated

| Source | Learning structure retained | Integration changes |
|---|---|---|
| foundry-maf-workshop | Portal, model SDK, agent, tool, workflow, hosted | Shared CLI/environment and synthetic-policy scenario |
| agent-framework-labs | Single/sequential/concurrent/Group Chat/MCP/RAG | Same inputs, permission boundaries, explicit termination |
| microsoft-iq-on-foundry | Sources/bases, Toolbox, IQ distinctions | GA retrieval over bundled synthetic data; optional [IQ routing design](../labs/10-iq-extensions.md), not a company-data connection |
| foundry-evaluation | Enterprise learning loop, failures, dev/holdout, review | No mandatory four-model set; small shared data/provider choices |

## What was not copied unchanged

- Portal workflow node creation/connection/publishing; learn MAF builders in Lab 05.
- Subscription-specific verified model IDs, regions, and quota as universal defaults.
- Incompatible `.env` vocabularies or Python/SDK combinations.
- Customer data, personal environments, resource IDs, tokens, or filmed environment identifiers.
- Another repository's successful runs or scores as evidence for this edition.
- 2025 notebook cells mixed with current SDK 2.x.
- Claims that portal, local MAF, Hosted, and offline fixtures are one execution path.

Before adapting classic threads/runs/Assistants or `azure-ai-inference` examples,
check the [official migration guide](https://learn.microsoft.com/azure/foundry/how-to/navigate-from-classic).
Current transition/retirement guidance does not guarantee old examples still work.

## Retirement dates that affect old tutorials

Checked 2026-09-24. Use the current
[classic-to-new agent migration guide](https://learn.microsoft.com/azure/foundry/agents/how-to/migrate)
before reviving an older sample.

| Old tutorial surface | Retirement date | What to do instead | Source |
|---|---:|---|---|
| Azure OpenAI Assistants API | 2026-08-26, already retired | Move to current Foundry agents and SDK 2.x patterns | [Assistants retirement note](https://learn.microsoft.com/azure/foundry-classic/openai/how-to/code-interpreter) |
| Foundry Agent Service classic agents using threads/runs/messages | 2027-03-31 | Migrate classic agents to the new Foundry agent service | [Classic agents deprecation](https://learn.microsoft.com/azure/foundry-classic/agents/concepts/threads-runs-messages) |
| Foundry portal Workflows visual Preview | 2026-12-01 | Build new workflow logic with Microsoft Agent Framework | [Workflows retirement](https://learn.microsoft.com/azure/foundry/agents/concepts/workflow) |

The core needs no additional repository clones or old notebooks. Return to your current lab,
or choose [A or B](../paths.md) if starting here; source links are background and attribution, not another setup sequence.
English is now the default entry point, with matching [Korean guides](../../README.ko.md).
