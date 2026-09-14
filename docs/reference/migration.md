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
| microsoft-iq-on-foundry | Sources/bases, Toolbox, IQ distinctions | GA default; explicit opt-in for real external data |
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

The core needs no additional repository clones. Source links support deeper exploration
and attribution; the executable core, data, and documentation are here.
English is now the default entry point, with matching [Korean guides](../../README.ko.md).
