# Learning paths and completion criteria

**English** | [한국어](ko/paths.md)

**Path A uses the browser and one prepared Lab 05 workflow (terminal by default; an owner-verified Hosted Playground is optional), without writing Python. Path B works with code and saved run records.**
Both use the same Hanbit Technology scenario with language-specific synthetic policies.

**Choose A** if you are new to Azure or agents, and **B** if you are comfortable with Python and APIs.
Complete [the setup card](setup.md), then use your route page as the checklist:
[A — Beginner](paths/a-beginner.md) · [B — Implementation](paths/b-practitioner.md).
The tables below are schedules, not extra tasks. Each lab has a `path-a` / `path-b` entry and an **A done / B done** exit.
[C — Advanced modules](paths/c-advanced.md) are separate sessions after the core route.

**How each lab works:** read the start card, do the action or command, then compare your result with **What to check**.
Screenshots come from the September 24, 2026 recording and dated September 25 checks/supplements; your names, IDs and answers will differ
([how to read them](labs/00-start.md#how-to-read-this-guide)).
English commands use `--language en`, which selects the English input files ([language rules](reference/languages.md)).
**All times below are teaching budgets, not measured learner completion times.** Browser response timings and edited video lengths do not validate a class schedule.

## A. Beginner: four hours thirty minutes in a prepared environment

You need a browser, an Entra account, and an instructor-prepared Foundry project and
**`gpt-6-sol` deployment**. Lab 05 defaults to a **prepared MAF environment** with SDKs installed and the learner signed in.
A Hosted Responses workflow in Playground is optional, only after the owner verifies it before class. Copy commands and read their results; Python authoring,
installation, and subscription billing setup are preparation, not class exercises.
For self-study, complete [the self-study preparation](setup-owner.md#self-study) first.
Its [Lab 00 B](labs/00-start.md#b-code-one-folder-one-environment) and [Lab 02 B](labs/02-models.md#path-b) steps prepare the terminal;
then start **[Lab 00 A](labs/00-start.md#path-a)**, not Lab 03 B.

| Order | Lab | Time | Your evidence |
|---|---|---:|---|
| 1 | [00. Start](labs/00-start.md#path-a) | 20 min | Account, project, and chosen path |
| 2 | [01. Foundry](labs/01-foundry.md#path-a) | 25 min | Resource/project/model relationship diagram |
| 3 | [02. Models: A](labs/02-models.md#path-a) | 20 min | Actual Playground response and deployment name |
| 4 | [03. Agent: A](labs/03-prompt-agent.md#path-a) | 35 min | Agent using inline synthetic policies |
| 5 | [05. MAF workflow: A](labs/05-workflows.md#path-a) | 25 min | Prepared sequential run (terminal by default) and human review record |
| 6 | [06. Knowledge: A](labs/06-knowledge.md#path-a) | 35 min | Source citation and effective-date check; IQ Chat not selected by default |
| 7 | [07. Evaluation: A](labs/07-evaluation.md#path-a) | 40 min | Manual business assessment of all six dev cases |
| 8 | [09. Operations: A](labs/09-operations.md#path-a) | 30 min | Risks, trace evidence or unverified reason, costs, and cleanup record |
| 9 | [11. Capstone: A](labs/11-capstone.md#path-a) | 15 min | Your worksheet and evidence handoff |
| — | Breaks and buffer | 25 min | **270 minutes total** |

**A is complete** when you have actual Playground/agent responses, a prepared MAF or hosted workflow run, source checks,
a dev assessment, trace evidence or an unverified reason, and a Lab 11 cleanup/evidence handoff. Writing Python
or deploying a server is not required.

Run the Lab 05 option assigned on your setup card yourself; watching another person's run does not count.
IQ Chat is optional: if it was not prepared for you, mark it **not selected** before you start (a scope choice, not a fallback after an error).

## B. Implementation: eight hours in a prepared environment

You should understand basic Python, JSON, a terminal, and `async/await`.
Region/model/permission approvals, SDK downloads, and Search service creation happen first.
B includes a managed Prompt Agent, local MAF tools/workflows, Search/IQ, local evaluation, package inspection, and trace lookup.
Recommended delivery is **two 4-hour sessions**, with Lab 06 on Day 1 and evaluation beginning on Day 2.
B assumes a prepared, verified environment; failures, role changes and approvals are extra.

| Order | Lab | Time | Your evidence |
|---|---|---:|---|
| 1 | [00. Doctor and settings](labs/00-start.md#path-b) | 15 min | Environment checks |
| 2 | [02. SDK: B](labs/02-models.md#path-b) | 20 min | Actual Responses result |
| 3 | [03. Prompt Agent SDK: B](labs/03-prompt-agent.md#path-b) | 25 min | Managed agent create/invoke files and response ID |
| 4 | [04. MAF, functions, MCP](labs/04-agents-tools.md#path-b) | 45 min | Differences among three execution paths |
| 5 | [05. MAF workflows: B](labs/05-workflows.md#path-b) | 40 min | Sequential, concurrent, and Group Chat code/results |
| 6 | [06. Search/IQ: B](labs/06-knowledge.md#path-b) | 50 min | GA references, activity, and context hash |
| 7 | [07. Learning loop: B](labs/07-evaluation.md#path-b) | 70 min | Local-retrieval baseline/candidate/holdout lineage with real model calls |
| 8 | [08. Hosted Agent](labs/08-hosted.md#path-b) | 40 min | Package and manifest review; serving/deployment not required |
| 9 | [09. Observability and operations](labs/09-operations.md#path-b) | 40 min | Existing run-ID lineage, Prompt Agent trace lookup, and read-only cleanup plan |
| 10 | [11. Capstone](labs/11-capstone.md#path-b) | 45 min | Existing acceptance report and artifact checklist |
| — | Breaks and buffer | 90 min | **480 minutes total** |

<a id="b-session-budget"></a>

| Session | Labs, in order | Core work | Breaks and buffer | Total |
|---|---|---:|---:|---:|
| Day 1 | 00, 02, 03, 04, 05, 06 | 195 min | 45 min | 240 min |
| Day 2 | 07, 08, 09, 11 | 195 min | 45 min | 240 min |

At the Day 1 pause, keep the Search ownership ledger and all saved outputs. Resume at Lab 07 without reseeding Search or repeating earlier model calls.

**B's core completion** requires the listed real model/tool/workflow and Search/IQ results,
managed Prompt Agent create/invoke evidence, comparable dev records, a frozen final holdout evaluation only after
[the dev gate passes](labs/07-evaluation.md#final-acceptance), package, trace status and cleanup handoff.
Hosted serving/deployment, actual client-side telemetry and paid cloud judges have separate optional gates.
Mark them **not run** if omitted; unavailable quota is not permission to submit fixtures
as real model responses.
If a required stage stays blocked, use [the incomplete handoff](labs/11-capstone.md#incomplete-handoff)
to preserve the actual work and recovery owner. It does not satisfy the missing B completion criteria.

[10. Fabric/Work IQ extensions](labs/10-iq-extensions.md) is a separate 45–90-minute
session. Approval, licensing, and capacity preparation are additional.

## C. Advanced integration — additional 150–180 minutes

<details>
<summary>Optional Hosted integration schedule — not another requirement for A or B</summary>

This is **one optional C route**, not the prerequisite for every [C module](paths/c-advanced.md).
For a version-pinned Hosted matrix, continue in the [Hosted evaluation workbook](reference/evaluation-workbook.md).
Prepare actual model deployments, IQ/Search roles, a Hosted identity, a judge, and App Insights access first.
Environment creation, permissions, quotas, and encoding waits are outside class time.

| Order | Work | Time | Evidence |
|---|---|---:|---|
| 1 | [Deployable MAF workflow](labs/05-workflows.md#c-practitioner-extension-make-the-workflow-deployable) | 25 min | Actual final answer and model-call lineage |
| 2 | [Hosted Responses/Invocations](labs/08-hosted.md) | 30 min | Fixed profile, real local response, exact remote version |
| 3 | Model matrix and native evaluation | 40 min | Four-model 24-row dev cohorts and pinned evaluators |
| 4 | Reviewed regression/calibration | 25 min | Legitimate dev review/consumption or all-pass record; actual judge calibration |
| 5 | Frozen holdout/traces/acceptance | 30 min | Four-model 16-row final set, actual root traces, human-review evidence |

The corpus, reference answers, code, API, model list, retrieval, and evaluator stay frozen for each comparison.
Optional [IQ extensions](reference/iq-workbook.md) need separate service-specific approval.

</details>

## Return to an independent module

| Module | Minimum prerequisite | Restart at |
|---|---|---|
| Model/prompt | [Lab 00 B's prepared code environment](labs/00-start.md#path-b), project, deployment and Foundry User permission | [02 B](labs/02-models.md#path-b) |
| MAF/MCP/workflow | SDKs, successful `doctor --cloud` and `model` | [04 B](labs/04-agents-tools.md#path-b) |
| Foundry IQ | Above plus prepared Search, retrieval configuration, and roles | [06 B](labs/06-knowledge.md#path-b) |
| Offline fixture comparison | Explicitly labeled fixture results in `outputs/<label>`; no Azure preparation | [00: offline comparison and stopping point](labs/00-start.md#offline-fixtures); inspect existing results rather than rerunning them |
| Real evaluation | A saved real run from the intended experiment and B's Azure preparation | [07 B: resume from saved evidence](labs/07-evaluation.md#resume-evaluation); fixtures do not unlock real acceptance |
| Hosted packaging | Repository and Python; runtime gates are separate | [08 B](labs/08-hosted.md#path-b) |
| IQ extensions | IQ basics and separate service approvals | [10](labs/10-iq-extensions.md) |

**Never silently switch paths.** A model error must not select another model. Failed
IQ must not become ordinary Search labeled as IQ. For installation failures, return to
the [version contract](reference/versions.md) or prepared environment instead of upgrading
individual SDKs at random.
