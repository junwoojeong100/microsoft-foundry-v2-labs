# C. Advanced: choose a capability, preserve its evidence

**English** | [한국어](../ko/paths/c-advanced.md)

**C is a module catalog, not one enormous mandatory sequence.**
The existing Hosted workflow evaluation workbook is already advanced and remains intact.
New modules must meet their own prerequisites and completion criteria before they are described as verified.

**Choose one module below.** Read its **First pass**, **Need**, and **Stop when** before running anything.
Use the [developer setup](../labs/extensions/developer-toolkit.md) only for that module's missing tools.
Keep the same language, record the last step and exact labels in `session-notes.txt`, and leave generated outputs in their original directories.
An unselected feature is **not run**; an attempted failure stays **failed/blocked**, not a successful substitute.

## Existing integration route

After B's real model, MAF and IQ results, follow the [Hosted evaluation workbook](../reference/evaluation-workbook.md).
It pins the actual Hosted version and protocol, keeps every model-by-case row and error,
calibrates the judge, preserves reviewed regression lineage, and checks real root traces.
Packaging, local invocation, remote deployment, native evaluation and human approval remain different outcomes.

## Additional capability modules

| Module | Learn | Prerequisite / first-pass boundary |
|---|---|---|
| [Managed Toolbox](../labs/extensions/toolbox.md) | Reuse a version-pinned synthetic policy tool | Lab 06 Search, approved keyless connection and Hosted/Toolbox SDK; default promotion is optional |
| [Hosted Toolbox](../labs/extensions/toolbox-hosted.md) | Run that same tool agent remotely | Verified local Toolbox; a separate azd directory, runtime permissions and deployment approval |
| [Code Interpreter / OpenAPI](../labs/extensions/additional-tools.md) | Verify a real generated CSV or read-only API call | Choose one tool; Code Interpreter first, OpenAPI needs the owned Search index |
| [Tool Search and Skills](../labs/extensions/tool-search-skills.md) | Discover selected tools; version and reuse behavioral instructions | An owned, working Toolbox; Preview opt-in |
| [Conversation evaluation](../labs/extensions/conversation-evaluation.md) | Compare individual-turn checks with full-conversation outcomes | A real multi-turn run from bundled dev questions; no holdout development |
| [Agent Optimizer](../labs/extensions/agent-optimizer.md) | Generate and review candidate configurations against a frozen dev baseline | Prepared evaluator/optimizer models, explicit cost approval; Preview |
| [Approval and recovery](../labs/extensions/approval-recovery.md) | Observe real SDK suspension/checkpoints with explicit prewritten work and simulated decisions | Local-only first pass; not real human authorization or Hosted crash proof |
| [A2A](../labs/extensions/a2a.md) | Connect independently addressed agent endpoints | Explicit A2A 1.0 and caller permissions; no 0.3 fallback |
| [Memory](../labs/extensions/memory.md) | Persist, isolate, recall and remove synthetic context | Compatible chat/embedding models; API-backed first pass, not automatic agent memory or user authorization proof |
| [Routines](../labs/extensions/routines.md) | Dispatch and inspect bounded scheduled work | Existing agent, explicit schedule/cost/cleanup ownership |
| [Agent safety](../labs/extensions/agent-safety.md) | Observe applied guardrails and controlled safety evaluation | Owned policy and non-production target; additional permissions/Preview boundaries |
| [Release operations](../labs/extensions/release-operations.md) | Connect OIDC, smoke/evaluation gates, approval and rollback | Dedicated deployment identity and manual release approval |
| [Model operations](../labs/extensions/model-operations.md) | Evaluate a replacement/router and plan retirement | Frozen workload, exact permitted model list, actual usage/latency evidence |
| [Governance/networking](../labs/extensions/governance-networking.md) | Explain actor, policy and private-network boundaries | Owner-prepared infrastructure; do not alter shared network/access settings |

The [coverage record](../coverage.md) identifies which modules have executable steps,
which have actual new Azure evidence, and which remain design-only or blocked.
An official product page or an installed SDK is not evidence that this workshop ran the feature.
Use [this edition's recorded results](../edition-results.md) to see the actual first-pass outcomes,
including baseline-only optimization and delivery-only routine verification.

## Pick a sensible next module

For reusable tooling: Toolbox first, then Tool Search/Skills **or** Hosted Toolbox.
For the learning loop: conversation evaluation first; Optimizer and recurring evaluation are separate later choices.
For local SDK mechanics without model calls: approval/recovery. A2A, memory, schedules and releases do not depend on completing that simulation.
For read-only/design work: governance/networking or specialist scope; do not create missing resources to fill their worksheets.

Do not share memory or conversation state between independent evaluation cases.
Do not let optimizer-generated changes enter a held-out evaluation until a person has reviewed and frozen the candidate.
An all-pass baseline is a valid outcome; no regression or improvement is manufactured.

## Specialist scope

Fabric/Work IQ, Autopilot/Agent 365, fine-tuning, voice/multimodal and browser/computer actions
have separate data, identity and runtime requirements. This course does not access real company/Microsoft 365 data.
Their [architecture/scope discussion](../labs/extensions/specialist-scope.md) must not be reported as executed capability coverage.

**Finish each selected module:** retain its complete evidence, undo only approved owned resources,
then add its actual outcome to [Lab 11](../labs/11-capstone.md).
