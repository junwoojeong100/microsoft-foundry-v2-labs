# Microsoft Foundry v2 Hands-on Labs

**English** | [한국어](ko/index.md)

**Build one travel-policy assistant and finish with evidence another learner can review.**

1. Choose [A. Beginner](paths/a-beginner.md) for browser steps plus a prepared Lab 05 workflow path, or
   [B. Implementation](paths/b-practitioner.md) for SDK calls, managed prompt agent, tools, workflows, Search/IQ, controlled evaluation, traces and local packaging.
2. Complete [setup](setup.md) for that route. A uses the learner ZIP; B uses the source repository.
3. Follow the route's checklist from Lab 00. Use **A done / B done** to leave each lab; do not continue into the other path.

**No Azure access yet:** stop after the [offline rehearsal](labs/00-start.md#offline-rehearsal).
**Learning alone:** prepare your own environment with [the self-study steps](setup-owner.md#self-study) first.
**Already started:** use [recovery and resume](reference/troubleshooting.md#resume-safely), not a fresh installation.

This Pre-Ignite 2026 Edition uses **synthetic data only**, with separate English/Korean inputs and recordings.
A's planned teaching budget is 4 h 30 min after setup; B's is 8 h, split into [two balanced 4-hour sessions](paths.md#b-session-budget).
These are plans, not measured learner completion times. Neither route authors workflows in the portal. Advanced sections and recordings are optional.
For A Lab 05, use the prepared terminal by default; the optional browser path needs an owner-verified Hosted Responses workflow before class.

A keeps the extracted learner ZIP as a personal evidence folder. B uses
[the source copy's notes directory](labs/00-start.md#prepare-notes), without a second ZIP.
Fill `session-notes.txt`, `workflow-review.txt` and `operations-checklist.txt` as you go;
A also fills a copy of `assessment.csv`.
Use the ready files, not reference-answer records. Keep credentials and filled worksheets out of `data/learner/`.

<details>
<summary>Reference directory — open only for the item you need</summary>

[C — Advanced](paths/c-advanced.md) adds selected modules after the core route.
[Coverage and evidence](coverage.md) records new-module status separately.

| What you need | Start here |
|---|---|
| Accounts, exact model, input files, and a self-setup route | [One-time setup](setup.md) |
| A starting point and schedule | [Learning paths](paths.md) |
| First-run instructions | [Lab 00](labs/00-start.md) |
| Classroom preparation | [Instructor guide](instructor.md) |
| September 24 `gpt-6-sol` English recordings | [Evidence hub](evidence.md) and [videos: 6:29 in guide order, 3:11 CLI, 2:55 portal](video-summary.md) |
| One video in guide order | [Lab chapters](video-chapters.md) |
| A particular screen or action | [98 actions and 293 captures](action-captures.md) |
| Actual results and limits | [Execution evidence](live-run.md) |
| Separate Korean recordings | [Korean videos](ko/video-summary.md) |
| Hosted matrices and independent gates | [Evaluation workbook](reference/evaluation-workbook.md) |
| Optional IQ, Toolbox, Fabric and Work IQ boundaries | [IQ extension workbook](reference/iq-workbook.md) |
| Final deliverables | [Capstone](labs/11-capstone.md) |
| Supported contracts and versions | [Compatibility snapshot](reference/versions.md) |
| Errors, roles, or quota | [Troubleshooting](reference/troubleshooting.md) |
| Finishing without overlooked costs | [Cleanup](reference/cleanup.md) |
| English/Korean scope and sample translations | [Language contract](reference/languages.md) |

</details>

> **Keep three things separate.** `offline-fixture` is a fixed example. Local MAF runs
> on your computer but calls a model in Azure. Hosted Agent runs your code in the cloud.
> Their completion criteria are different. English execution explicitly selects its own frozen
> English policies/prompts/datasets; Korean originals remain unchanged.

```mermaid
flowchart TD
    S["Lab 00 / Choose a starting point"] --> A["A / Portal + prepared MAF"]
    S --> B["B / Python + managed prompt agent"]
    A --> P["Project / Agent / MAF example / Source documents"]
    B --> C["SDK / managed prompt agent / MAF and tools / Workflows / Search and IQ / traces"]
    P --> E["Evaluate against the same business criteria"]
    C --> E
    E --> R["Review failures / Improve / Final check"]
    R --> O["Observability / Costs / Safe cleanup"]
    C -. "Optional" .-> H["Hosted Agent / IQ extensions"]
```

Both current and historical documents are intentional: retrieving the newest document
does not prove that the assistant applied the policy valid **on the travel date**.
Observing models, retrieval, and business checks independently is the core of these labs.
