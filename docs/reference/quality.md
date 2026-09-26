# Workshop quality contract and public references

**English** | [한국어](../ko/reference/quality.md)

**Comparison checked: September 26, 2026.** This workshop aims to combine a beginner-readable journey with reproducible engineering evidence.
It does **not** claim to be GitHub's objectively best workshop. No exhaustive ranking, independent learner trial or all-feature Azure run was performed for this comparison.
Stars, feature counts and AI editorial scores do not establish those claims.

## What a complete workshop must demonstrate

| Requirement | This repository's implementation | Evidence boundary |
|---|---|---|
| One clear first route | [A's explanation, diagram and exact sequence](../paths/a-beginner.md) | A needs the prepared project and Lab 05 option; it is not entirely browser-only |
| Self-study preparation and recovery | [Setup](../setup.md), [owner preparation](../setup-owner.md), [troubleshooting](troubleshooting.md) | Account access, quota, costs and permissions cannot be assumed |
| Code that learners can understand and change | [Code-along exercises](../code-along.md), six small SDK recipes | Mock-transport checks, not model inference or a substitute for the B route |
| Executable instructions | CLI examples checked against the real parser; A/B route and output contracts tested | Syntax and fixtures do not prove current Azure availability |
| Reproducible inputs and results | Frozen language-specific data, explicit model/provider choices, saved responses and hashes | No error-triggered model, provider, language or fixture substitution |
| Meaningful evaluation | [Lab 07](../labs/07-evaluation.md), dev gates, preserved failures and final-only holdout | Six dev cases and four public teaching holdout cases are not statistical superiority |
| Operations through cleanup | [Lab 09](../labs/09-operations.md), [handoff](../labs/11-capstone.md), [cleanup](cleanup.md) | Trace status, approval authority, shared ownership and remaining costs stay explicit |
| Honest feature coverage | [Dated coverage](../coverage.md) and [actual results](../live-run.md) | Design-only, blocked, older-model and unrun features do not become current live evidence |
| Current, aligned documentation | Exact completion hashes for **every** reviewed English/Korean pair, not only the active revision | Pending translations retain warnings; a prose edit can invalidate a completed hash even when commands are unchanged |
| Repeatable maintenance | [One-command local verification](#verify-this-copy), CI, dependency-drift checks | A passing report applies to that source fingerprint and selected local checks only |

The official [Foundry agent lifecycle](https://learn.microsoft.com/azure/foundry/agents/concepts/development-lifecycle),
checked September 26, 2026, connects creation, tools, immutable versions, tracing, evaluation, publishing and monitoring.
This workshop follows those concerns without making publishing or role changes an automatic consequence of completing a lesson.
Published-agent identity permissions require their own review; company/Microsoft 365 data remains excluded here.

## Public reference sample

These are **seven representative repositories**, not every repository on GitHub.
GitHub repository search and the default-branch files were reviewed, then the observed commits were fixed below.
The dates are **commit dates**, not repository update times or proof of a successful live run.
Different languages, audiences and scopes make a single numerical ranking misleading.

| Public reference at the reviewed commit | Commit date | Observed teaching pattern | How it informs this workshop |
|---|---|---|---|
| [microsoft/ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners/tree/25b7985f3b2dc37a84f4a7387ccd3c9f0e5b1595) | 2026-09-09 | Topic lessons, code samples, videos and many translations | Keep concepts and code discoverable, while preserving independently versioned English/Korean evidence |
| [MicrosoftLearning/mslearn-ai-agents](https://github.com/MicrosoftLearning/mslearn-ai-agents/tree/7eafc3c339d31a8fd125af71ee7fd2465c083be8) | 2026-09-22 | Task-focused exercises and just-in-time explanations; the reviewed A3 client task is marked `draft` | Add predict → edit → check → explain practice rather than make every task a wrapper command |
| [Azure-Samples/foundry-hosted-agents-workshop](https://github.com/Azure-Samples/foundry-hosted-agents-workshop/tree/bf12d4e12f2a44c2251ba54b24fd1355ab1b4534) | 2026-08-18 | One growing travel assistant, step navigation, preflight and local progression | Keep one scenario and clear checkpoints, without requiring pushes or rewriting a learner's previous work |
| [Azure-Samples/microsoft-foundry-e2e-agent-observability-workshop](https://github.com/Azure-Samples/microsoft-foundry-e2e-agent-observability-workshop/tree/75eb82dfe36e5aae3375829a85433d940e422070) | 2026-04-17 | Observe → optimize → protect, with SDK and skill routes | Retain evaluation, tracing and failure review as core learning, not decorative screenshots |
| [Azure-Samples/multi-agent-orchestration-workshop](https://github.com/Azure-Samples/multi-agent-orchestration-workshop/tree/4095e86d52e644e691ee19d0076741104dd8111c) | 2026-05-27 | .NET pattern-specific starter code and architecture walkthroughs | Explain the builder and role order; demonstrate a broken participant contract in the Python practice |
| [Azure-Samples/foundry-agent-sdk-workshop-kr](https://github.com/Azure-Samples/foundry-agent-sdk-workshop-kr/tree/79d3f03e645f7189861bb09b15a40697690b644c) | 2026-08-20 | Korean SDK notebooks, staged setup and a declared validation date | Make Korean a complete executable path and keep compatibility claims dated |
| [monuminu/foundry-workshop](https://github.com/monuminu/foundry-workshop/tree/f8a810ee4e611f25a3c1bb3c4ee2d60c438b46d9) | 2026-06-19 | Readable web lessons, generated notebooks and expected outputs | Show expected results and interpretation, while distinguishing examples from the learner's actual response |

Reviewed evidence: each repository's README; additionally the
[Microsoft Learn A3 task](https://github.com/MicrosoftLearning/mslearn-ai-agents/blob/7eafc3c339d31a8fd125af71ee7fd2465c083be8/Instructions/Consolidated/A3-call-your-agent-from-a-client-app.md),
[hosted preflight](https://github.com/Azure-Samples/foundry-hosted-agents-workshop/blob/bf12d4e12f2a44c2251ba54b24fd1355ab1b4534/.workshop/scripts/preflight.py),
[sequential code-along](https://github.com/Azure-Samples/multi-agent-orchestration-workshop/blob/4095e86d52e644e691ee19d0076741104dd8111c/docs/01-sequential-pattern.md)
and [notebook workshop setup](https://github.com/monuminu/foundry-workshop/blob/f8a810ee4e611f25a3c1bb3c4ee2d60c438b46d9/docs/setup.md).
These support the stated educational patterns, **not a claim that the referenced code was executed here**.
No external code, media or lesson prose was copied into this edition; source licenses remain independent.

## Improvements made from this comparison

The core routes already cover the project-to-evaluation-to-cleanup journey, so this pass does not add unrelated services just to increase a feature count.
It adds three concrete capabilities:

1. **Executable code practice:** personal copies, fixed SDK transports and three deliberate contract mistakes, with failures retained.
2. **A source-bound quality report:** one local command records every selected gate, failures, interpreter, timestamps and before/after source fingerprints.
3. **Completion-hash enforcement:** `check_docs.py` rejects stale reviewed translations from older revisions, not only current pending work.

Codespaces, additional model families, voice and fine-tuning are not implicitly added or claimed as verified by this work.
Their availability in another curriculum does not establish a tested implementation here.

<a id="verify-this-copy"></a>

## Verify this copy locally

Run from the source repository root in an isolated Python **3.13** or **3.14** environment; use 3.13 for installed-SDK checks.
Keep an existing activated `.venv`. For a **fresh** check-only environment, this block refuses to replace an existing `.venv`:

```bash
mkdir .venv &&
python3.13 -m venv .venv &&
source .venv/bin/activate &&
python -m pip install -e ".[dev]"
```

If `.venv` already exists, skip that block, activate it with `source .venv/bin/activate`, and install `".[dev]"` only if needed.
Python 3.14 is an offline-only alternative; replace `python3.13` above explicitly. Windows uses WSL.
No Azure account, `.env`, role grant or model deployment is needed for these checks.

```bash
python scripts/verify_workshop.py --label quality-check
```

This runs Ruff lint/format, Python compilation, the offline tests, documentation checks and learner-bundle checks.
The offline tests also execute the documented fixture rehearsal and preserve overwrite/failure protections.
It writes **`outputs/verification/quality-check/report.json`**; use a new label for another attempt.
An existing directory stops before checks start. It does not remove or replace earlier evidence.

| Report field | Read it as |
|---|---|
| `mode: offline-verification` | Local engineering checks, not a live agent evaluation |
| `status: passed` | Every selected check passed and the relevant source stayed unchanged during the run |
| `checks` | Exact commands, status, exit codes and durations; failures do not disappear from the list |
| `source_before_sha256`, `source_after_sha256` | Fingerprints of relevant code, guides, synthetic data and validation configuration, excluding `.env` and personal `outputs/` |
| `sdk_checks_selected` | Whether the additional installed-SDK contract and transport tests ran |
| `azure_tested`, `learner_pilot_performed`, `global_ranking_established`, `deployment_approved` | All remain `false`; none can be inferred from a local pass |

Exit `0` means selected checks passed, `1` means a failed gate, `2` means invalid input or a setup/report error, and `130` means interrupted.
Read the terminal's actual failure message. Reports omit environment values and log bodies; they are not a credential export.
A changed source fingerprint, timeout, missing tool, unrun gate or interruption cannot yield a passing report.

For **optional installed-SDK checks**, stay in Python 3.13 and install the declared full set if it is missing:

```bash
python -m pip install -r requirements.lock.txt -e ".[cloud,agents,hosted,dev]" &&
python scripts/verify_workshop.py --sdk --label quality-sdk-check
```

`--sdk` adds `pip check`, import contracts and the SDK test suite. The tests use fixed transports, not an Azure login.
It does not turn this report into live evidence. The CI workflow uses the same local gate runner; the separate SDK job remains local/stub-only.

## What still requires real evidence

Before claiming a particular workshop delivery is ready, the owner must rehearse that selected route with participant-level access
and keep its model/version, inputs, responses, failures and cleanup records. Use [the instructor rehearsal](../instructor.md#rehearse-route).
Do not create a new deployment or run paid comparisons just to fill this page.

An independent beginner pilot is a **separate, not-yet-performed activity**, not an AI review:
give consenting learners only the frozen guide and prepared environment; record the route/revision, started/completed/blocked counts,
assistance points and elapsed time without names or credentials. Count blocked learners in the denominator and report assisted completion separately.
Do not label setup time or model latency as learner completion time.

This public comparison and the local gates establish inspectable improvements. They do not establish a global rank,
production approval, a measured learning outcome, or a fresh Azure result for every feature.

Return to [the beginner guide](../paths/a-beginner.md), [the implementation guide](../paths/b-practitioner.md) or [actual validation boundaries](validation.md).
