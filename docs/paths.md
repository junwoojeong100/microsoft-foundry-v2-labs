# Learning paths and completion criteria

**English** | [한국어](ko/paths.md)

**Path A runs prepared examples without writing code. Path B works directly with code and execution records.**
Both use equivalent language-specific synthetic Hanbit Technology policies. Complete A first and extend
to B later, or follow the relevant A/B section in each lab. A is portal-first, but
its workflow exercise runs in a prepared MAF environment.

**Route pages:** [A — Beginner](paths/a-beginner.md) · [B — Implementation](paths/b-practitioner.md) ·
[C — Advanced modules](paths/c-advanced.md) · [Coverage and evidence](coverage.md).
**First visit: choose A.** Use its route page as the checklist; the tables below are schedules, not additional tasks.
Each lab has a direct `path-a` / `path-b` entry and an **A done / B done** exit.
The original times below describe the existing prepared core routes.
New capability modules add separate sessions; they are not silently squeezed into the same four/six-hour promise.

**Start with [the setup card and learner ZIP](setup.md), then follow only your path's next link.**
Read the start card, perform the action/command, and check its completion criterion.
Images and collapsed recording galleries are optional references, not your own results.
Use [the screenshot guide](labs/00-start.md#how-to-read-this-guide),
[new English recordings](video-summary.md), and [new action index](action-captures.md).
English commands select their own frozen English policy/prompt/evaluation bundle with `--language en`.
[Language and lineage rules](reference/languages.md) distinguish translation from an unchanged-dataset comparison.

## A. Complete beginner: four hours in a prepared environment

You need a browser, an Entra account, and an instructor-prepared Foundry project and
**`gpt-5.6-luna` deployment**. Lab 05 also needs a **prepared MAF environment** with SDKs installed
and the learner signed in. Copy commands and read their results; Python authoring,
installation, and subscription billing setup are preparation, not class exercises.
For self-study, complete [the environment-owner checklist](setup.md#4-environment-owner-checklist)
and [Lab 00 B setup](labs/00-start.md#b-code-one-folder-one-environment) first.

| Order | Lab | Time | Your evidence |
|---|---|---:|---|
| 1 | [00. Start](labs/00-start.md#path-a) | 20 min | Account, project, and chosen path |
| 2 | [01. Foundry](labs/01-foundry.md#path-a) | 25 min | Resource/project/model relationship diagram |
| 3 | [02. Models: A](labs/02-models.md#path-a) | 20 min | Actual Playground response and deployment name |
| 4 | [03. Agent: A](labs/03-prompt-agent.md#path-a) | 35 min | Agent using inline synthetic policies |
| 5 | [05. MAF workflow: A](labs/05-workflows.md#path-a) | 25 min | Prepared sequential run and human review record |
| 6 | [06. Knowledge: A](labs/06-knowledge.md#path-a) | 35 min | Source citation and effective-date check; IQ Chat not selected by default |
| 7 | [07. Evaluation: A](labs/07-evaluation.md#path-a) | 30 min | Manual business assessment of all six dev cases |
| 8 | [09. Operations: A](labs/09-operations.md#path-a) | 25 min | Risks, costs, and cleanup record |
| 9 | [11. Capstone: A](labs/11-capstone.md#path-a) | 15 min | Your worksheet and evidence handoff |
| — | Breaks and buffer | 10 min | **240 minutes total** |

**A is complete** when you have actual Playground/agent responses, a prepared MAF
sequential run, source checks, a dev assessment, and a Lab 11 cleanup/evidence handoff. Writing Python
or deploying a server is not required.

Distinguish observing MAF from running it yourself. Portal workflow authoring is not
a substitute. The Preview IQ Chat segment is optional: select it only when prepared,
otherwise label it **not run** and complete the source checks with the already-created agent.
This is a declared scope choice before execution, never fallback after an IQ error.

## B. Practitioner: six hours in a prepared environment

You should understand basic Python, JSON, a terminal, and `async/await`.
Region/model/permission approvals, SDK downloads, and Search service creation happen first.

| Order | Lab | Time | Your evidence |
|---|---|---:|---|
| 1 | [00. Doctor and settings](labs/00-start.md#path-b) | 15 min | Environment checks |
| 2 | [02. SDK: B](labs/02-models.md#path-b) | 20 min | Actual Responses result |
| 3 | [04. MAF, functions, MCP](labs/04-agents-tools.md#path-b) | 45 min | Differences among three execution paths |
| 4 | [05. MAF workflows: B](labs/05-workflows.md#path-b) | 40 min | Sequential, concurrent, and Group Chat code/results |
| 5 | [06. Search/IQ: B](labs/06-knowledge.md#path-b) | 45 min | GA references, activity, and context hash |
| 6 | [07. Learning loop: B](labs/07-evaluation.md#path-b) | 50 min | Local-retrieval baseline/candidate/holdout lineage with real model calls |
| 7 | [08. Hosted Agent](labs/08-hosted.md#path-b) | 40 min | Package and manifest review; serving/deployment not required |
| 8 | [09. Observability and operations](labs/09-operations.md#path-b) | 30 min | Existing run-ID lineage and read-only cleanup plan |
| 9 | [11. Capstone](labs/11-capstone.md#path-b) | 45 min | Existing acceptance report and artifact checklist |
| — | Breaks and buffer | 30 min | **360 minutes total** |

**B's core completion** requires the listed real model/tool/workflow and Search/IQ results,
comparable dev records, frozen final evaluation, package and cleanup handoff.
Hosted serving/deployment, actual telemetry and paid cloud judges have separate optional gates.
Mark them **not run** if omitted; unavailable quota is not permission to submit fixtures
as real model responses.

[10. Fabric/Work IQ extensions](labs/10-iq-extensions.md) is a separate 45–90-minute
session. Approval, licensing, and capacity preparation are additional.

## C. Advanced integration — additional 150–180 minutes

After B, continue in the [Hosted evaluation workbook](reference/evaluation-workbook.md).
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

## Return to an independent module

| Module | Minimum prerequisite | Restart at |
|---|---|---|
| Model/prompt | Project, deployment, Foundry User permission | [02 B](labs/02-models.md#path-b) |
| MAF/MCP/workflow | SDKs, successful `doctor --cloud` and `model` | [04 B](labs/04-agents-tools.md#path-b) |
| Foundry IQ | Above plus prepared Search, retrieval configuration, and roles | [06 B](labs/06-knowledge.md#path-b) |
| Evaluation | A complete real run or an explicitly labeled fixture in `outputs/<label>` | [07 B](labs/07-evaluation.md#path-b); fixtures do not unlock real acceptance |
| Hosted packaging | Repository and Python; runtime gates are separate | [08 B](labs/08-hosted.md#path-b) |
| IQ extensions | IQ basics and separate service approvals | [10](labs/10-iq-extensions.md) |

**Never silently switch paths.** A model error must not select another model. Failed
IQ must not become ordinary Search labeled as IQ. For installation failures, return to
the [version contract](reference/versions.md) or prepared environment instead of upgrading
individual SDKs at random.
