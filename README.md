# Microsoft Foundry v2 Hands-on Labs

**English** | [한국어](README.ko.md)

## Start here

**1. Complete [the setup card](docs/setup.md). 2. Choose one route below. 3. Follow that route page from Lab 00.**
You build one travel-policy assistant with the supplied synthetic data only.
Background reading, videos and advanced modules are optional.

| Route | Choose it if | You do | You finish with |
|---|---|---|---|
| **[A — Beginner](docs/paths/a-beginner.md)** | You are new to Azure or agents | Browser steps and one command in a prepared terminal; no Python writing | Your agent, a six-question assessment, a workflow review and a cleanup handoff |
| **[B — Implementation](docs/paths/b-practitioner.md)** | You are comfortable with Python and APIs | SDK calls, tools, workflows, Search/IQ, a controlled evaluation and local packaging | Saved run records and an acceptance report |

**Time:** 4 hours for A and 6 hours for B, after the environment is prepared.
**Files:** A uses the small learner ZIP from the setup card. B uses the source repository ZIP; no second ZIP is needed.
**A's Lab 05 needs a prepared terminal.** If none was supplied, complete [Lab 00 B](docs/labs/00-start.md#path-b) and [Lab 02 B](docs/labs/02-models.md#path-b) before class.
**No Azure access yet?** Run only the [offline rehearsal](docs/labs/00-start.md#offline-rehearsal) and mark the cloud labs **not run**.

Already completed the core route: [C. Advanced modules](docs/paths/c-advanced.md).
Preparing a class: [Instructor guide](docs/instructor.md). Returning from the old edition: [Migration map](docs/reference/migration.md).

<details>
<summary>Background and previous recordings — optional context, not prerequisites</summary>

## Background: learning loops and frontier ecosystems

In his [June 14, 2026 essay](https://x.com/satyanadella/status/2066182223213293753),
Satya Nadella argued for a **frontier ecosystem, not just a frontier model**:
organizations should build learning systems that retain their knowledge and expertise even when the underlying model changes.
He reiterated this in Microsoft's [July 29, 2026 earnings call](https://www.microsoft.com/en-us/Investor/events/FY-2026/earnings-fy-2026-q4),
emphasizing each organization's own **continuous learning loop** and control of its core IP.
The focus shifts from simply choosing the strongest model to building an ecosystem in which organizations can keep learning and creating value.

This workshop turns that perspective into a practical engineering loop:
**run → observe and evaluate → human review → improve → verify again**.
Using only bundled synthetic data, you connect Foundry and Microsoft Agent Framework (MAF) agents,
knowledge, tools, workflows, Hosted deployment, and evaluation into one system.
Here, learning means reviewed improvements to instructions, retrieval, tools, and workflows—not automatic model-weight training.
Dev data supports iteration; holdout is reserved for final acceptance.

**Start with one agent. Finish with a system whose knowledge, evaluation criteria, and operational decisions your team can reuse.**

English by default · Korean available · Synthetic data only

**Pre-Ignite 2026 Edition / Current workflow and evaluation curriculum: September 15, 2026**

Follow the **[beginner or practitioner guide](docs/paths.md)**. Each lab places reference
images and a **What to check** explanation beside the relevant action or command.
Read [how to use the screenshots](docs/labs/00-start.md#how-to-read-this-guide) first.

**September 24 `gpt-6-sol` recordings:** [English videos](docs/video-summary.md) ·
[Action/capture index](docs/action-captures.md) · [Chapters](docs/video-chapters.md) ·
[Actual results and limitations](docs/live-run.md)

The English set contains **98 actions, 293 lossless captures, and three videos**: **6:29 in guide order**,
3:11 CLI and 2:55 portal. It covers the main A (portal) and B (CLI) steps of Labs 00–09 and 11 and the optional
Foundry evaluation steps with `gpt-6-sol` / `2026-09-22` in the Sweden Central training project
([model choice](docs/reference/model-choice.md)). Failed attempts stay in the recording next to their retries
([what failed](docs/live-run.md#failures-kept-in-this-recording)).
Local playback and chapter seeks are verified; the videos were not uploaded to GitHub.
Play them with `python scripts/play_recordings.py --edition en`. Earlier recordings were removed.

English uses **separate English instructions, synthetic policies, dev/calibration/holdout datasets, and fixtures**.
Select them explicitly with `--language en`; original Korean files remain unchanged.
The [language contract](docs/reference/languages.md) and [versioned data bundle](data/README.md)
preserve language-specific lineage. [Korean recordings](docs/ko/video-summary.md) are independent.

This self-contained edition brings agents, workflows, knowledge, evaluation, and
operations into **one environment and one business scenario**. It is not a list of
repositories to visit in sequence.
The labs, Python code, synthetic policies, evaluation data, and instructor guide are here.

## Additional modules and their evidence

**September 16 English-first expansion:** [A — Beginner](docs/paths/a-beginner.md) ·
[B — Implementation](docs/paths/b-practitioner.md) · [C — Advanced modules](docs/paths/c-advanced.md).
Use the [capability/evidence record](docs/coverage.md) to distinguish existing labs, executable modules
and actual Azure verification. The extension modules were exercised on September 16, 2026 with the earlier
`gpt-5.6-luna` preset; they were not re-run or re-recorded with `gpt-6-sol`, and their recordings were removed.

</details>

## One scenario, an expanding system

Build a travel-policy assistant for the fictional **Hanbit Technology**.
It handles current and historical lodging limits, meals, advance approval, and
unsupported international-travel questions. No real company documents, personal
information, or Microsoft 365 data are used. The assistant provides guidance;
it does not approve, book, or reimburse travel.

```mermaid
flowchart LR
    U["User question"] --> A["Foundry Agent / MAF"]
    K["Six synthetic policies"] --> R["Document context / Search / Foundry IQ"]
    R --> A
    T["Read-only functions / MCP"] --> A
    A --> E["Answers / citations / execution history"]
    E --> V["Business checks + optional Foundry evaluation"]
    V --> H["Human failure review"]
    H --> P["Improved instructions + regression assets"]
    P --> A
    E --> O["Trace / Monitor / costs"]
```

| Module | Topics |
|---|---|
| [00. Getting started](docs/labs/00-start.md) | Learning paths, browser/code setup, offline/cloud boundaries |
| [01. Foundry and projects](docs/labs/01-foundry.md) | Platform vs. SDK, resources, projects, roles |
| [02. Models](docs/labs/02-models.md) | Deployment names, Playground, SDK, comparison and Router |
| [03. Your first agent](docs/labs/03-prompt-agent.md) | Instructions, synthetic documents, citations, tool/permission boundaries |
| [04. MAF and tools](docs/labs/04-agents-tools.md) | Single agent, functions, local MCP |
| [05. MAF workflows](docs/labs/05-workflows.md) | Prepared example, sequential/concurrent/Group Chat code, human review |
| [06. RAG and Foundry IQ](docs/labs/06-knowledge.md) | Search vs. IQ, GA API, source citations |
| [07. Evaluation and learning](docs/labs/07-evaluation.md) | Dev, failure analysis, instruction improvements, holdout |
| [08. Hosted Agent](docs/labs/08-hosted.md) | Safe packaging, local server, code deployment |
| [09. Operations and cleanup](docs/labs/09-operations.md) | Traces, release gates, costs, ownership-aware cleanup |
| [10. IQ extensions](docs/labs/10-iq-extensions.md) | Fabric, Work IQ, Toolbox, Preview approval boundaries |
| [11. Capstone](docs/labs/11-capstone.md) | Final handoff across knowledge, models, evaluation, and operations |

## Shortest code-path start

Run every command from **this repository's root**. Examples use Bash; use WSL on
Windows. The commands call Python 3.13, which the full code route and Hosted work need (3.14 runs only the offline checks).
Browser-path learners do not need these commands.

```bash
# Try the checker without external packages or Azure.
python3.13 scripts/workshop.py --language en doctor
python3.13 scripts/workshop.py --language en demo --label first-offline --prompt v2
python3.13 scripts/workshop.py --language en evaluate --label first-offline
```

`offline-fixture` results are **prewritten examples**, not evidence of model quality,
Foundry performance, or Azure connectivity. Continue with [Lab 00](docs/labs/00-start.md)
for SDK installation, authentication, and real calls. Use a new label for every run;
existing runs are not overwritten.

## Scope of this edition

- Current Foundry and Projects SDK **2.x**; no mixing with classic threads/runs code.
- **MAF code** owns workflow authoring and orchestration. Portal workflow creation/publishing is excluded.
- The first-pass preset is **`gpt-6-sol`**, deployed with that exact name, model version **`2026-09-22`**
  (September 23, 2026; [why this model](docs/reference/model-choice.md)).
  The optional IQ Chat path keeps its own `gpt-5.6-luna` deployment because Search knowledge bases accepted no GPT-6 model;
  other models belong to explicit comparison experiments.
- Service GA and SDK Preview are separate. The Hosted Agent service is GA, while this
  edition's Python hosting package is prerelease. Foundry IQ GA and richer Preview contracts are distinct.
- Model replacement, instruction improvement, and accumulating evaluation evidence are included.
  **Automatic weight training, fine-tuning, and RL are not.**
- Deployment, paid evaluation, and external connections are optional, separately executed steps.
  Opening the repository or running `doctor` creates no resources.
- Unannounced Ignite 2026 capabilities, future prices, regions, and quotas are not guaranteed.

**Evidence:** [Versions/status](docs/reference/versions.md) ·
[Validation scope](docs/reference/validation.md) · [Sources](docs/reference/sources.md) ·
[Troubleshooting](docs/reference/troubleshooting.md) · [Cleanup](docs/reference/cleanup.md)

New terms: [glossary](docs/reference/glossary.md). Execution options:
[command reference](docs/reference/commands.md). Environment variables:
[configuration](docs/reference/configuration.md).

## Repository layout

```text
docs/                  English labs, learning paths, instructor and reference guides
docs/ko/               Matching Korean guides
src/foundry_workshop/   Shared settings, retrieval, agents, evaluation, and lineage
scripts/               Workshop CLI, packaging, and documentation checks
data/knowledge/        Six canonical synthetic policies (Korean)
data/evaluation/       Six dev / four holdout / two judge-calibration cases
data/fixtures/         Fixed examples for the offline checker
data/learner/          Ready-to-use English/Korean browser materials and ZIPs
prompts/               Canonical v1 / v2 instructions (Korean)
examples/              Local MCP server and Hosted Agent entry point
tests/                 Offline logic and contract checks
outputs/               Personal run outputs; excluded from Git
```

Licensed under [MIT](LICENSE). Source attribution and repository-specific license
boundaries are recorded in [Sources](docs/reference/sources.md).
