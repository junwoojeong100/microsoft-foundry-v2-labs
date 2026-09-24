# Validation boundaries and actual execution

**English** | [한국어](../ko/reference/validation.md)

**Installation, offline contracts, real Azure execution, model quality, and media validation are distinct.**
Each language uses independent execution labels and recording sources.
Earlier videos and upstream results are not relabeled as new evidence.

<a id="current-answer"></a>

## Current answer — September 25, 2026

| Question | Answer | Details |
|---|---|---|
| What is recorded? | The main A/B steps of Labs 00–09 and 11 and the optional Foundry evaluation steps, in English and Korean, with `gpt-6-sol` / `gpt-6-sol-judge` (`2026-09-22`) in the Sweden Central training project | [Re-recording](#gpt-6-sol-20260924) · [videos](../video-summary.md) |
| What did the live runs return? | In each language: business checks baseline 6/6, candidate 6/6 and holdout 4/4; acceptance `ready-for-human-review` with `deployment_approved: false`. Judge scores are kept separately and do not decide acceptance | [Actual results](../live-run.md) |
| What else ran with `gpt-6-sol`, unrecorded? | September 23: verification runs of the optional evaluation steps (recorded again on September 24), the conversation evaluation module, existing-traces and recurring evaluations, Agent Optimizer (baseline only), cloud red teaming (displayed ASR invalid) and the approved Hosted CI release | [Additions](#foundry-evaluation-additions) · [previously not-run items](#previously-not-run-items) |
| What has not run with `gpt-6-sol`? | Lab 03 portal File Search; Lab 06 IQ Chat and hybrid RAG; Lab 07 feedback/regression and the Hosted matrix; Lab 08's local server and the learner's own Hosted deployment; Hosted server-side tracing; Lab 10; the other extension modules (memory, a routine and Toolbox discovery ran on September 25) | [Not-run list](../live-run.md#not-run-with-gpt-6-sol) |
| How do I check a working copy? | Run the offline tests, Ruff, compilation, documentation and learner-bundle checks below. Each dated record states what passed for its revision | [Local checks](#local-checks-to-run) |
| What is outside this evidence? | Company/Microsoft 365 data, external Work IQ/Fabric connections, SLAs, statistical superiority, automatic retraining, production approval and other users' resources | [Not established](#not-established) |
| What changed in the September 24 review refresh? | Refreshed SDK pins, Lab 03 B managed agent in the B core, a core trace check, a browser option for A Lab 05, the Insights module, standalone SDK recipes and new CI checks. That evening the core B route ran live in both languages with the new pins, plus the trace lookup, recipes, A2A and one Insights scan; four guide or recipe defects were fixed | [Review refresh](#review-refresh-20260924) · [live check](#review-refresh-live-20260924) |
| What was added on September 25? | Screenshots and short clips of Lab 03 B and the Lab 09 B trace search in both languages; English runs of conversation evaluation, memory, a routine and the Toolbox up to discovery; the remaining items need owner approval | [Supplement and not-run review](#review-refresh-supplement-20260925) |
| How straightforward are the guides and documents? | AI editorial review, September 24: guides 100/100 and documents 98.5/100 in round 5 (the round-4 reviewers after fixes); new reviewers in rounds 1–4 scored 86.5–97.5. Not a learner pilot or timing measurement | [Latest review](#straightforwardness-95) |

<a id="review-refresh-20260924"></a>

## Review refresh, offline only — September 24, 2026

**Changed:** SDK pins (`azure-ai-projects` 2.6.1, `openai` 3.16.1, MAF core 1.18.0, `agent-framework-foundry` 1.13.0,
hosting 1.0.0b260910, `mcp` 1.30.0; [versions](versions.md)); typed A2A SDK requests; one dated
`compatibility.py` registry for raw REST API versions; `prompt-agent --output`; Lab 03 B as a core B step;
Lab 09 trace check; A Lab 05 browser option; the [Insights module](../labs/extensions/agent-insights.md);
six standalone recipes in `examples/recipes/`; azd command validation against a recorded help snapshot;
a read-only SDK drift report and a manual, cost-gated live smoke workflow.

**Verified offline:** 297 offline tests on Python 3.13 and 3.14 without site packages, 87 SDK tests with the installed pinned libraries and stubbed transports, Ruff, formatting, compilation, `check_docs.py` (127 Markdown files, 2,520 local links, 510 anchors, 328 workshop CLI examples, 84 azd examples, 63 language pairs), learner bundles, `pip check`, `check_sdk.py` and the CI offline doctor/demo/evaluate/package steps passed.

**Not run in this offline pass:** no Azure call, deployment, role change, recording or live smoke run. The live check follows below.
The recordings and live results above used the previous pins and guide revision; they are not evidence for the new steps.

<a id="review-refresh-live-20260924"></a>

## Review refresh live verification — September 24, 2026 (evening)

**Scope:** fresh copies of commit `a9c3990` with the refreshed pins, prefixes `mfv2-rr-20260924-<language>`, the same Sweden Central
project and `gpt-6-sol` / `gpt-6-sol-judge`. The lab subscription was pinned; the Azure CLI default was not changed.

- **Core B route, English and Korean:** every documented command exited 0; Lab 07 baseline 6/6, candidate 6/6, holdout 4/4 with 0 errors;
  acceptance `ready-for-human-review`, `deployment_approved: false`. Lab 03 B created version 1 in each language and invoked it by version.
- **Traces:** each managed agent call produced `invoke_agent` and `chat` spans with matching tokens within about three minutes;
  direct Responses calls produced none.
- **Optional and C items:** `maf-evaluate` 6/6 and 6/6; `cloud-evaluate` groundedness 6/6, relevance 5/6 (D05); A2A 1.0 with typed
  requests completed one delegated call; one Insights scan analyzed 22 traces and returned 4 insights; the local workflow server
  answered one Responses request; recipes 02–06 and 08 completed.
- **Fixed:** recipes now pin `AZURE_SUBSCRIPTION_ID` (an unpinned CLI credential returned 403 from another tenant's account);
  recipes 05 and 08 now carry synthetic evidence; the Pydantic warnings of `maf-evaluate` and the tenant-scoped trace query are documented.
- **Not run:** remote Hosted deployment for the browser Lab 05 option, cross-provider comparison, Toolbox/Tool Search/Skills,
  Memory, Routines, conversation evaluation, Agent Optimizer, red teaming and the route A portal steps.

[Details, IDs and owned objects](../live-run.md#review-refresh-live-verification).

<a id="review-refresh-supplement-20260925"></a>

## Supplement recording and not-run review — September 25, 2026

- **Recorded, English and Korean:** Lab 03 B create and invoke with `--output` (real zsh terminal; guide blocks pasted verbatim, `read` prompts answered by typing), the Lab 03 B portal check and the Lab 09 B trace search.
  Twelve lossless WebP screenshots decode pixel-identical to their PNG captures and four H.264 clips at 1× decode fully. The portal instructions equaled the CLI definition, and each trace ID equaled the Application Insights `operation_Id`.
- **Discarded:** one English attempt whose terminal printed a local home-directory path; it was re-recorded from a neutral working directory.
- **Ran, English:** conversation evaluation with the refreshed pins, the memory lifecycle, one routine dispatch, the Toolbox up to MCP discovery and a read-only route A trace check. Search denied the Toolbox direct query because the project identity has only Search Index Data Reader.
- **Needs owner approval:** a remote Hosted deployment with runtime roles; one non-OpenAI deployment for the cross-provider comparison; a supported optimizer deployment; the Search role for Toolbox, Tool Search and Skills. Installing the Dev Pack changes a workstation's global tools.

- **Offline checks:** 305 offline tests on Python 3.13 and 3.14, 87 SDK tests with the pinned libraries, Ruff check and format, compilation, `check_docs.py` (127 Markdown files, 2,608 local links, 552 anchors), learner bundles and the CI offline doctor, demo, evaluate and package steps passed.

[IDs, results and owned objects](../live-run.md#review-refresh-supplement).

<a id="gpt-6-sol-20260924"></a>

## Re-recording with the optional evaluation steps — September 24, 2026

**Recordings:** new English and Korean recordings, started after 00:00 KST, in the same Sweden Central project with
`gpt-6-sol` / `gpt-6-sol-judge` and the prefixes `mfv2-sol-20260924-<language>`.

- **Scope:** the main A/B steps of Labs 00–09 and 11 and the optional Foundry evaluation steps.
- **English:** 98 actions, 293 lossless captures, videos 6:29 / 3:11 / 2:55 and 262 source segments (minimum SSIM 0.9922)
  from one terminal and two portal recordings.
- **Korean:** 91 actions, 272 captures, videos 6:03 / 2:57 / 2:43 and 244 segments (minimum SSIM 0.9923).
- **Playback:** local byte-range playback and all 11 chapter seeks were verified in each language; nothing was uploaded or pushed.
- **Removed:** the `g6sol-20260923` recordings and the separate `eval-portal-20260923` captures (git history at `90b18b3`).
  `videos/` holds `gpt-6-sol-20260924-en-summary.mp4` and `-ko-summary.mp4`, copies of each guide-ordered video.

[Recordings](../video-summary.md) · [Actual results](../live-run.md).

**Failures kept in the recording and what changed:**

- `E07-011`: the business-rubric baseline run returned groundedness and relevance but no `business_rubric` (0 errored), although
  its evaluation had three testing criteria. The CLI rejected it as invalid. The Korean `K07-011` returned all three the first time.
- `cloud-evaluate` gained `--retry-failed` (the native retry already existed) and an error that names the missing evaluator.
  `E07-013` retried once and kept the first attempt under `native-attempts/attempt-1`.
- `E07-012` then refused `--reference baseline`: the rebuilt retry state had lost `item_fields`, a bug in that retry path.
  The retry now keeps `item_fields` (regression test added); `E07-014` read the completed retry back without a new job and
  `E07-015` joined the candidate. Both source updates and hashes are in `live-results.json` (`source_updates`).
  After the recording, a `--reference` run can also be retried: the retry stays in the reference's evaluation as
  `<label>-retry-N`, and the advice to use `--retry-failed` appears only in `cloud-evaluate` errors. This change has offline
  and SDK tests only; it was not run against Azure.
- Opened from the playground, the portal evaluation wizard preselected agent **Version 1**, which still had Web search. The English
  capture tool kept it (`EP07-202`), so `EP07-206`/`EP07-207` scored Version 1 (TaskAdherence 4/6; D05 answered with an external U.S.
  rate). Both languages repeated the evaluation with Version 2 (`*P07-211` to `*P07-217`): Relevance 6/6, Coherence 6/6,
  TaskAdherence 0/6. Item 2 of Lab 07 A step 4 and item 1 of the Lab 09 A trace evaluation now tell learners to keep only the saved version.
- Capture-tool timing, not Foundry failures: `EP07-205` clicked before the evaluator list loaded, `KP07-203` waited for a dataset
  row that did not refresh after a successful upload, `KP07-215` typed before the rename dialog loaded. Later, separately named
  actions completed each step.

**Results in each language:** business checks baseline 6/6, candidate 6/6 and holdout 4/4; the no-evidence diagnostic 0/6 with
0 errors; cloud judge groundedness 6/6 and relevance 5/6 (D05). Business-rubric agreement was 6/6 for both runs; **Compare runs**
showed mean relevance 3.83 → 4.83 (English) and 4.17 → 4.50 (Korean) with **Too few samples** (captures `EP07-301`, `KP07-301`). MAF tool calls: English 6/6 and
6/6; Korean tool_call_accuracy 5/6 (D03's search query named `APPROVAL-01`, which the evaluator called a fabricated parameter) and
relevance 5/6 (D05). Trace evaluation: English 10/10, Korean 15/15, including five conversations that the earlier portal evaluation created.

**Azure changes:** under the new prefixes — portal agents (versions 1–2) and SDK agents, Search indexes, IQ knowledge sources and
bases, datasets, evaluations and runs, and custom evaluator versions `mfv2_sol_20260924_en_business_rubric` 1 and
`mfv2_sol_20260924_ko_business_rubric` 1 — plus billable model and judge calls. The portal language was switched to Korean for the
Korean recording and restored to English. No deployment, role assignment or default-subscription change.

**Local verification:** 256 offline tests passed on each of Python 3.13 and 3.14; the SDK import check and 77 installed-SDK tests
passed; Ruff, formatting, compilation and documentation checks passed.

<a id="previously-not-run-items"></a>

## Previously not-run evaluation, safety and release items — September 23, 2026

The owner asked for the items the evaluation additions left unrun. They ran the same evening against the same project,
`gpt-6-sol` / `gpt-6-sol-judge` and the prefix `mfv2-sol-20260923-<language>`; none is part of the edited videos.

| Item | Owner action first | English | Korean |
|---|---|---|---|
| Existing-traces evaluation (Lab 09 A) | **Monitoring Reader** for the project identity on Application Insights | 15/15 on Relevance, Coherence and TaskAdherence | 15/15 on each |
| Recurring evaluation | none beyond that role | first run on save 5/5; next hourly run sampled the planned request, 5/5; paused | first run 5/5; next hourly run 5/5 without the planned request; paused |
| Agent Optimizer | temporary `gpt-5.5` optimizer deployment, deleted afterwards | baseline only, 0.979 | baseline only, 0.938 (D05 relevance 2) |
| Cloud red teaming (Preview) | taxonomy reviewed; only the portal run was scoped, by deleting actions (SDK `enabled` flags did not limit generated attacks) | SDK: displayed ASR 89% (75/84); portal: 100% (6/6) | SDK: displayed ASR 57% (48/84) |
| Approved Hosted release | CI identity given project-scoped **Foundry Project Manager** and account **Reader**; environment variables pointed at this project | [run 35856612314](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35856612314): 6/6, 0 errors | [run 35857252318](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35857252318): 6/6, 0 errors |

**Findings kept as findings:**

- What an evaluator receives decides what it can verify. Each trace's `query` carried the agent's instructions with the six policies,
  so TaskAdherence passed 15/15; the dataset-based run in Lab 07 A sent only the question and scored 1/6 (English) and 0/6 (Korean).
- Recurring runs sample the latest seven days, not only the last hour: the first ran as soon as the schedule was saved and
  re-scored earlier conversations, and a random 5 of 16 took the English planned request but not the Korean one.
  Schedule configuration and evaluated samples stay separate evidence; nothing was re-sent to populate a run.
- The red-team service labelled rows as attack successes (score 0 against threshold 3) whose own reasoning said the response refused;
  every response was read and none performed or claimed a prohibited action, and 3 attacks were blocked by the content filter.
  The displayed ASR is therefore marked invalid. Taxonomy `enabled` flags did not limit attack generation; deleting actions in the
  portal did. A taxonomy PATCH needs the complete object, and a read right after a change can return the previous version.
- The optimizer's generic early-stop message said all candidates were perfect while rows failed, and its Groundedness judge compared
  each answer with itself, so no candidate was promoted; `optimizer-review.txt` records `pending-human-review`.
- Default model pickers can point at the wrong deployment: while the temporary optimizer deployment existed, a new evaluation's
  **Judge model** defaulted to it, and the optimizer's **Evaluation model** defaulted to `gpt-6-sol`. Both were set to `gpt-6-sol-judge`.
- Red-team calls left no agent traces; optimizer runs left 27 per agent, so the optimizer used isolated agent copies and the recurring
  schedule's sample was not affected.
- The Korean portal names the red-team wizard **빨간색 팀 실행 만들기** and the tabs **레드 팀 미리 보기** and **최적화 미리 보기**;
  the Korean scans and optimizer run were submitted from the English UI.

**Azure changes:** role assignments (Monitoring Reader for the project identity on Application Insights; the CI identity's
project-scoped Foundry Project Manager and account Reader; Foundry User for the Hosted runtime, granted by the pipeline);
deployment `mfv2-sol-20260923-opt-gpt55` created and deleted; agents `mfv2-sol-20260923-<language>-optimize` (version 1) and
`mfv2-sol-20260923-ci-hosted` (versions 1–2); datasets `mfv2-sol-20260923-<language>-optimizer-dev`; trace, optimizer and red-team
evaluations, red-team taxonomies and two paused schedules; changed `foundry-workshop` environment variables (previous values kept
in the session record). The CI identity's roles on the September 14 project were kept. No default-subscription change.

**Still not run:** Lab 08's local server and the learner's own Hosted deployment, server-side tracing for a Hosted agent,
guardrail attachment with `gpt-6-sol`, and the **Continuous** recurring mode (unavailable for trace evaluations).

<a id="foundry-evaluation-additions"></a>

## Optional Foundry evaluation additions — September 23, 2026

This revision adds optional Foundry Evaluation practice to the existing A/B routes; the core routes, their commands and
the recorded videos are unchanged.

| Where | Addition | Status |
|---|---|---|
| Lab 07 A step 4 | Run the saved agent on `dev-questions.jsonl` (new, questions only) as a portal evaluation with Relevance, Coherence and TaskAdherence, then compare with the manual worksheet | Optional; TaskAdherence is Preview |
| Lab 07 B step 2 | If the baseline passes, `collect --retrieval none` creates a real, dev-only failure to diagnose; `feedback` and `cloud-evaluate` reject it | Optional |
| Lab 07 B step 5 | `cloud-evaluate --business-evaluator` registers or reuses an owned code-based evaluator with the local business rules; `--reference` adds candidate to baseline's evaluation for **Compare runs** | Optional Preview |
| Lab 04 section 5 | `maf-evaluate` scores the MAF function-tool agent's calls with `tool_call_accuracy` and `relevance` | Optional; experimental MAF API |
| Lab 09 A | Owner-prepared existing-traces evaluation and the **Recurring** option | Documented here; run later that day after the owner's actions ([previously not-run items](#previously-not-run-items)) |

**Live Azure checks, English and Korean separately, with `gpt-6-sol` / `gpt-6-sol-judge`:**

| Check | English | Korean |
|---|---|---|
| Portal evaluation (Relevance / Coherence / TaskAdherence) | 5/6, 6/6, 1/6 | 5/6, 6/6, 0/6 |
| Manual business assessment of the same agent | 6/6 | 6/6 |
| New dev collections, business checks (baseline / candidate) | 6/6, 6/6 | 6/6, 6/6 |
| No-evidence diagnostic | 0/6, 0 errors, `feedback` rejected | 0/6, 0 errors, `feedback` rejected |
| Cloud judges with `business_rubric` (groundedness / relevance / business, each run) | 6/6, 6/6, 6/6; agreement 6/6 | 6/6, 5/6, 6/6; agreement 6/6 |
| Portal comparison of the two runs | relevance 4.33 → 4.83, too few samples | relevance 3.83 → 4.50, too few samples |
| `maf-evaluate` (tool_call_accuracy / relevance) | 6/6, 6/6; re-run after review fixes (code `408b1b57…`, `eval_fd079e29…`) 6/6, 6/6 | 6/6, 5/6; re-run after review fixes (`eval_e330c6aa…`) 6/6, 6/6 |
| Cloud judges on the no-evidence diagnostic (before the refusal was added) | invalid (`evalrun_2b495a2e…` in `eval_f231e23c…`): Groundedness skipped 3/6 rows; nothing counted | invalid (`evalrun_1e0790d4…` in `eval_910a4729…`): Groundedness skipped 4/6 rows; nothing counted |
| Conversation evaluation module (turn; conversation groundedness) | 6/6 and 6/6; 1/2 | 6/6 and 6/6; 2/2 |

**Findings kept as findings:** TaskAdherence and Relevance disagreed with the business assessment because the evaluators receive
only the question and answer, not the policies inside **Instructions**. Relevance marked down D05's correct withholding, and its
result varied between runs (5/6 in the recording, 6/6 in the English verification; 5/6, then 6/6 in the two Korean `maf-evaluate`
runs). Groundedness returns *skipped* (`not_applicable`) for a row with empty context; the workshop never counts a skipped row, and
`cloud-evaluate` now refuses a no-evidence run before submission. In the Korean portal, the localized default
names of the Relevance and Coherence evaluators failed the evaluator-name check and kept **Next** disabled until renamed; the guide
states this workaround. Six cases are too few for the portal's statistical comparison.

**Run later the same day:** the existing-traces evaluation, recurring evaluation, Agent Optimizer, cloud red teaming and a new
release pipeline run, after the owner's actions listed in [the next section](#previously-not-run-items).

**Azure changes:** two uploaded dev-question datasets, datasets that `cloud-evaluate` creates automatically, portal and SDK
evaluations and runs (three evaluations named `...-trial-...` were scaffolding checks, one of them grading offline fixture rows; the
invalid diagnostic runs are kept), and owned custom evaluator versions (`mfv2_sol_20260923_en_business_rubric` 1–2, `mfv2_sol_20260923_ko_business_rubric` 1),
all under the `mfv2-sol-20260923-<language>` prefixes, plus billable agent and judge calls. The portal language was switched to
Korean for the Korean captures and restored to English. No deployment, role assignment or default-subscription change.
[English results](../live-run.md#optional-evaluation-additions--separate-verification-september-23-2026) · [September 24 recording of the same portal steps](../action-captures.md)

**Local verification:** 255 offline tests passed on each of Python 3.13 and 3.14, and 73 installed-SDK tests passed with stub
transports. New tests cover the grader's parity with the local rules, the diagnostic's rejection paths, skipped judge rows,
custom-evaluator criteria, shared reference runs, tool-result mapping and the new captures. Ruff 0.16.6, compilation, both learner
bundles, the CI offline commands in a clean copy and documentation checks (117 Markdown files, 58 language pairs, 340 CLI examples)
passed. Final code hash: `67e7ac04…`.

<a id="gpt-6-sol-20260923"></a>

## gpt-6-sol environment, recordings and removal of earlier media — September 23, 2026

**Environment:** a dedicated Sweden Central resource group with a Foundry account (API keys disabled) and project,
Basic Search with a system-assigned identity and key authentication disabled, Log Analytics (30 days, 1 GB/day cap),
Application Insights, keyless Search and Application Insights project connections, and resource-scoped roles only.
Resource names keep the environment's original `g6luna` label. The default Azure CLI subscription was not changed.

**Model switch:** `gpt-6-luna` deployed but failed on the project Responses, prompt-agent and MAF paths (HTTP 500; the
portal agent reported `reasoning.effort` unsupported). `gpt-6-sol` and `gpt-6-astra` passed the same agent checks and
`gpt-6-sol` was selected ([model choice](model-choice.md)). The environment now has `gpt-6-sol` (150K TPM) and
`gpt-6-sol-judge` (100K TPM), Data Zone Standard `2026-09-22` with `NoAutoUpgrade`. The `gpt-6-luna`, `gpt-6-luna-judge`
and `gpt-6-astra` deployments, probe agents and a temporary North Central US account (also purged) were deleted.
Opening the first portal agent created a `text-embedding-3-large` deployment (Standard, 110K) that the labs do not use.
Search accepted no GPT-6 model for knowledge bases, so the optional IQ Chat preset stays on `gpt-5.6-luna`.

**Recordings:** independent English and Korean runs of the main A/B steps of Labs 00–09 and 11 — 69 actions and
207 lossless captures per language, three edited videos each (English 4:36 / 2:30 / 1:43, Korean 4:32 / 2:27 / 1:43),
175 and 176 source segments with minimum midpoint SSIM 0.9925 (English) and 0.9922 (Korean), local byte-range playback
and all 11 chapter seeks verified. Not uploaded or pushed. Every recorded action exited 0; the feedback step was not run
because neither baseline had a failed case. In each language the business checks were baseline 6/6, candidate 6/6 and
holdout 4/4, and the optional cloud judge on the candidate returned groundedness 6/6 and relevance 5/6 (D05, a correct
abstention). [Recordings](../video-summary.md) · [Actual results](../live-run.md).

**Removed:** the September 15 foundation recordings, the September 16 extension recordings, the September 23
`gpt-6-luna` recordings and their pages were deleted from the working tree; they remain in git history at `47f3b49`.
Earlier GitHub attachment URLs are no longer linked; removing those hosted copies is a separate manual action.
The September 17 IQ Chat configuration captures remain because that preset is unchanged.

**Local verification:** 244 offline tests passed on each of Python 3.13 and 3.14; 67 installed-SDK tests passed with
stub transports. Ruff 0.16.6 lint/format, compilation, the CI offline commands in a clean copy and both learner bundles passed.
Documentation checks cover 117 Markdown files, 58 language pairs and 330 CLI examples, with no pending translations.
Azure changes in this revision were limited to the deployments above and the recorded agents, Search objects and
evaluation runs under each `mfv2-sol-20260923-<language>` prefix; no role or default-subscription change.

## Local checks to run

```bash
python3.13 -S -m unittest discover -s tests -t . -q
python3.14 -S -m unittest discover -s tests -t . -q
python -m unittest discover -s tests_sdk -t . -q
python -m ruff check .
python -m ruff format --check .
python -m compileall -q src scripts examples tests tests_sdk
python scripts/check_docs.py
python scripts/build_learner_materials.py
python -m pip check
python scripts/check_sdk.py
```

Maintainers can also run `python scripts/check_dependency_drift.py` (advisory, needs PyPI access; never edits pins)
and, after upgrading azd or its Foundry extensions, `python scripts/record_azd_surface.py` to refresh the help snapshot
used by `check_docs.py`. The **Approved live smoke check** workflow is manual and cost-gated.

SDK tests use the actual installed libraries with explicitly stubbed transports.
They are not counted as real Azure responses.
Each dated record on this page states what passed for its revision.

## Not established

Real company/Microsoft 365 data, external Work IQ/Fabric connections, operational SLAs,
statistical superiority, automatic retraining/weight changes, human production approval,
and deletion of other users' resources are outside this evidence.
Stopping sessions does not eliminate all model/Search/log/storage costs.

<a id="straightforwardness-95"></a>

## Straightforwardness review: guides and documents — September 24, 2026

**Round 5: guides 100/100 and documents 98.5/100.** Earlier rounds: 97/100 and 86.5/100; 97.5/100 and 94/100;
93.5/100 and 92.5/100; 96.5/100 and 92/100.
Rounds 1–4 each used seven new, independent AI cold reads: English A, English B and Korean guides (D1–D10), and two English
and two Korean document groups (R1–R10). Round 5 is the round-4 reviewers re-reading their whole scope after the fixes.
Each dimension starts at 10, loses 3, 2, 1 or 0.5 points per critical, major, moderate or minor finding and takes the lowest
reviewer score; D10 and R10 come from the Korean reviews. New reviewers kept finding a few different small issues, so rounds 2–4
moved up and down. This is an editorial assessment, not a human usability pilot, a learner-success rate or a measured completion time.

| Guides | What earns full points | Round 1 | Round 2 | Round 3 | Round 4 | Round 5 |
|---|---|---:|---:|---:|---:|---:|
| D1 | Entry and route choice reach the first action of either route | 10 | 9.5 | 10 | 10 | 10 |
| D2 | One linear core path; optional, owner and historical material collapsed or marked | 10 | 10 | 9 | 10 | 10 |
| D3 | Numbered, imperative steps with exact UI labels, file names and values | 10 | 10 | 9 | 10 | 10 |
| D4 | A visible success or failure check after every action or command | 10 | 9 | 9 | 10 | 10 |
| D5 | Commands run as written, in order, with named output files | 10 | 10 | 10 | 7 | 10 |
| D6 | Plain, lean language in the core path | 10 | 10 | 9 | 9.5 | 10 |
| D7 | Concrete recovery, including what to ask the owner for | 9 | 10 | 9 | 10 | 10 |
| D8 | Explicit done criteria, correct A/B next links and a clear handoff | 10 | 10 | 10 | 10 | 10 |
| D9 | Current, consistent model, date, screenshot and link claims | 10 | 10 | 9.5 | 10 | 10 |
| D10 | Korean pages mirror the English and read naturally | 8 | 9 | 9 | 10 | 10 |

| Documents | What earns full points | Round 1 | Round 2 | Round 3 | Round 4 | Round 5 |
|---|---|---:|---:|---:|---:|---:|
| R1 | Purpose, audience and the current answer come first | 8 | 10 | 10 | 9.5 | 10 |
| R2 | Headings, tables and anchors find an answer in seconds | 9 | 10 | 10 | 9.5 | 10 |
| R3 | Procedures are numbered, with the actor and a success check | 10 | 10 | 10 | 9 | 10 |
| R4 | Numbers, flags, links and results agree with guides, CLI and evidence | 7 | 9 | 8 | 9 | 9 |
| R5 | Each fact lives in one place; dated history stays compact | 9 | 10 | 10 | 9.5 | 10 |
| R6 | Short sentences and explained terms | 9.5 | 10 | 10 | 10 | 9.5 |
| R7 | Brief, consistent evidence boundaries, Preview status and dates | 10 | 9 | 9 | 9 | 10 |
| R8 | Paid calls, cloud writes, roles and cleanup name approver and actor | 9 | 8 | 8 | 9 | 10 |
| R9 | Every page gives a next step; no dead or removed links | 9 | 9.5 | 10 | 9.5 | 10 |
| R10 | Korean pages mirror the English and read naturally | 6 | 8.5 | 7.5 | 8 | 10 |

**Rejected after verification:** two critical findings came from errors in the reviewers' brief, not from the pages.
Round 1's R4 finding said the coverage page over-claimed the September 23 `gpt-6-sol` runs; those claims are correct, but the
README sentence denying any re-run was wrong and is fixed. Round 4's D5 finding assumed core paid commands take `--confirm-cost`;
by design they do not, and the reviewer withdrew it after the correction (Lab 07 B now states its billable calls).
Without them, round 1 documents would score 89.5 and round 4 guides 99.5. Round 1's proposal to add `--language ko` to every
Korean core command was not adopted because the Korean recordings use the default form; Lab 00 now states both Korean forms.

**What changed, English first and then Korean:**

- **Validation page:** a current-answer table comes first; current evidence, local checks and limits precede the collapsed
  review and September 15–17 history; the recording summary is a list.
- **Checks that match the code:** Lab 00's Python note and install check, Lab 02's `usage` fields, `echo $?` for the Lab 04/07
  expected failures, Lab 08's printed package path and rebuild command, `maf-evaluate --output` and the Hosted `stop-session` receipt.
- **Approver and actor at the command:** A2A writes, `routine create`, the agent-safety redeploy, the optimizer submission,
  `stop-session` and Lab 07 B's billable collections.
- **Less to read on the core path:** Lab 09 A's optional review and the cleanup rows for optional modules are collapsed;
  both learner `START-HERE.txt` files say the guide pages are outside the ZIP.
- **One fact, one wording:** the four modules re-run on September 23, conversation evaluation among the September 23 runs,
  the fixture files, the guide-ordered video's "Labs 00–09 and 11", the release deployment, version and schedules, and the
  Lab 09 A status in the September 23 table now agree across pages.
- **Navigation:** per-lab jumps in both action indexes, next or return links on coverage and developer tools, the current page
  marked in the evidence footers, and one 51-row full error reference in both languages.
- **Korean:** every extension page, Lab 10 and the flagged guide and reference sections were compared sentence by sentence,
  keeping Korean-edition results and Korean-UI steps; the A route, Lab 00's language note and several reference sentences read naturally.

**Afterward, not re-scored:** round 5's two findings, a missing verb on the model-choice page and one schedule count on the
coverage page, were corrected.

**Verification:** 287 offline tests passed on each of Python 3.13 and 3.14; five new tests cover this record's arithmetic,
the validation layout, the mirrored error reference, the `--output` command list and the learner start files.
Ruff 0.16.6 lint/format, Python compilation, documentation checks (117 Markdown files, 58 language pairs, 328 CLI examples)
and byte-for-byte learner-bundle checks passed. Changed pairs have exact completion hashes in `docs/localization.json`;
no translation is deferred.

**Boundaries:** workshop command lines, Foundry request logic, prompts, synthetic policies, evaluation datasets, fixtures and
recordings are unchanged; only one Korean `printf` prompt was translated. The learner `START-HERE.txt` text changed, so both
learner ZIPs were regenerated. No Azure call, resource or permission change, deployment, publishing or push was performed.

## Older validation history

Older guide reviews, September 17 records and September 15 media/execution history moved to [Validation history](validation-history.md). The current page keeps the current answer, recent dated evidence, local checks and boundaries.

