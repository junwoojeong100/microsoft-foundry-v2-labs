# Validation boundaries and actual execution

**English** | [한국어](../ko/reference/validation.md)

**Installation, offline contracts, real Azure execution, model quality, and media validation are distinct.**
Each language uses independent execution labels and recording sources.
Earlier videos and upstream results are not relabeled as new evidence.

<a id="follow-through-review"></a>

## Follow-through review — September 17, 2026

The second review followed configuration, file handoff and optional Hosted setup from the `5cce55b` guide,
rather than treating its editorial score as proof that every learner could finish.
It found gaps the initial structural checklist did not establish:

| Gap | Correction | Evidence boundary |
|---|---|---|
| A new language/label can still conflict with the old Search ownership scope | Exact `mfv2-` grammar, one-copy/scope rules and an explicit instructor ownership handoff | Language/prefix-change refusals reproduced locally before any network request; the old ledger remains unchanged |
| B can enter from the source copy without receiving the browser worksheets | Executable, non-overwriting notes preparation; named JSON outputs and B-specific worksheet fields | Actual file copies and rejected reruns are tested, not inferred from links |
| A blocked dev gate leaves no clear end-of-session handoff | Separate complete, rejected and incomplete handoffs; no acceptance command for absent runs | Missing work stays incomplete; holdout and business thresholds are not weakened |
| Optional Hosted setup requires manual YAML merging and relies on shell state | Reuse the package-verifying helper with `--kind runtime`, a separate directory and guarded, service-scoped azd commands | Actual manifest generation plus stubbed environment/readback contracts; missing scope variables stop before azd runs |

The preparation helper supports only language-matched **local/v2/project-Responses** introductory packages.
The existing Toolbox and CI Invocations contracts remain distinct. No model or retrieval fallback was added.
`cleanup-plan` now links to the selected language's cleanup guide.
Official manifest documentation and installed azd help were reviewed on September 17; this is **not a new Azure deployment result**.

The checks verify concrete behavior, including safe copies, directory/profile rejection and missing-value guards.
The editorial-table test checks arithmetic and the unrun pilot, **not a hardcoded 95-point outcome**.
The earlier score below remains an initial self-assessment; no additional usability points or novice completion rate are claimed.
Canonical prompts, policy/evaluation/fixture data and existing media remain unchanged.
No new paid model/judge call, resource/role change, Azure deployment or novice pilot was performed for this review.

**Local acceptance of this follow-through revision:** 215 offline tests passed on each of Python 3.13 and 3.14.
Ruff 0.16.6 lint/format, Python compilation, both deterministic learner bundles and documentation checks passed
(61 language pairs, 332 workshop CLI examples, no pending translations).
The scope-guard tests use a local azd stub and cover both unset and empty values; they do not run a deployment.

<a id="guide-straightforwardness"></a>

## Initial guide straightforwardness assessment — September 17, 2026

**Self-assessed editorial acceptance: 95/100.** This is an explicit rubric for the **prepared A/B core guides**,
not an independent usability benchmark, a 95% learner-success rate, or a rating of every optional C integration.
Each criterion is worth **5 points**. Source review and the checks below support criteria 01–19.
Criterion 20 receives **0**, because no fresh novice pilot was performed; the advertised hours remain prepared-course allocations, not newly measured completion times.

| # | Acceptance criterion — 5 points each | Evidence | Awarded |
|---|---|---|---:|
| 01 | Setup is the first action; background/videos are not prerequisites | [README](../../README.md) and entry-page checks | 5 |
| 02 | One route and first-pass presets are chosen before execution | [A](../paths/a-beginner.md) / [B](../paths/b-practitioner.md) | 5 |
| 03 | Both nine-step sequences include handoff; schedules total 240/360 minutes | [Schedules](../paths.md) and route-order assertions | 5 |
| 04 | All 36 route steps across both languages have visible entry/exit links to the correct section | [Journey tests](../../tests/test_learner_journey.py) | 5 |
| 05 | Every numbered lab has scope, prerequisites, completion and recovery in one start card | All 24 language lab pages and start-card assertions | 5 |
| 06 | A contains only its one prepared workflow command, not B code or holdout | [A route](../paths/a-beginner.md) and extracted-command assertions | 5 |
| 07 | B's core commands exclude optional judges, hosting and Preview branches | [B route](../paths/b-practitioner.md) and extracted-command assertions | 5 |
| 08 | Owner preparation and optional settings do not interrupt the prepared learner route | [Setup](../setup.md); owner commands are collapsed | 5 |
| 09 | Paid model/retrieval calls, cloud writes and local-only work are distinguished before execution | Lab 02/04/05/06/07/08 scope and command notes | 5 |
| 10 | Learner ZIP and source ZIP have distinct purposes and acquisition steps | [Setup](../setup.md) / [Lab 00](../labs/00-start.md#path-b) | 5 |
| 11 | Ready instructions and questions use the frozen synthetic inputs, without answer keys or holdout | [Learner-material tests](../../tests/test_learner_materials.py) | 5 |
| 12 | Blank evidence templates supply the same filenames required at handoff | [Learner bundle](../../data/README.md) / [Lab 11 A](../labs/11-capstone.md#path-a) | 5 |
| 13 | The browser assessment requires all six real answers, citations and review reasons | [Lab 07 A](../labs/07-evaluation.md#path-a) and worksheet assertions | 5 |
| 14 | Documented output fields and filenames match actual CLI artifacts | Executed offline comparison; no invented comparison fields | 5 |
| 15 | The evaluation mainline is steps 1–4 with a six-case candidate gate before four-case holdout | [Lab 07 B](../labs/07-evaluation.md#path-b) and command/gate assertions | 5 |
| 16 | Resume instructions distinguish local reinspection, a new collection and polling an existing job | [Recovery table](troubleshooting.md#resume-safely); existing fixture bytes survive a rejected rerun | 5 |
| 17 | Package-only and cleanup-plan outputs cannot be mistaken for deployment or deletion | Executed [Lab 08 B](../labs/08-hosted.md#path-b) / [Lab 09 B](../labs/09-operations.md#path-b) CLI examples | 5 |
| 18 | English/Korean commands, links and active-revision file hashes agree | [Documentation tests](../../tests/test_documentation.py) / [localization record](../localization.json) | 5 |
| 19 | Synthetic-data lineage, errors and unverified outcomes remain explicit; older footage is not new proof | [Frozen data hashes](../../data/localization.json), offline contracts and dated records below | 5 |
| 20 | New learners independently finish the prepared routes, with intervention and elapsed-time records | **Not run — no points awarded** | 0 |

**Verification for this revision:** complete offline suites passed on Python 3.13 and 3.14, together with
Ruff 0.16.6 lint/format, Python compilation, deterministic learner bundles, and documentation checks
(61 language pairs, 332 workshop CLI examples, no pending translations).
The guide's offline commands run in temporary copies with no `.env`, inherited Azure credentials or installed SDKs.
They verify actual files, the intentional fixture 0/6 versus 6/6, comparison fields, exit codes, byte-preserving label rejection,
`cloud_deployed: false` packaging, and non-deleting cleanup. Fixture scores are **not model-quality measurements**.

Only the guide, blank learner worksheets and their checks changed. Canonical prompts, policy/evaluation/fixture data and recorded media remain unchanged.
**No new live Azure run, deployment, role assignment, paid evaluation, SDK integration run or recording is claimed for this revision.**
The historical results below retain their original scope and dates.

## Extension acceptance — September 17, 2026

The September 16 English/Korean extension source is now checked separately from the historical cohorts below:
**200 offline tests on each of Python 3.13 and 3.14, 67 installed-SDK transport tests**, Ruff check/format,
Python compilation, dependency compatibility and deterministic learner bundles passed.
Documentation checks cover **61 language pairs and 332 executable workshop examples**, with no pending translations.

The English extension has 166 actions, 496 captures and 368 retained source segments;
the independent Korean extension has 172 actions, 516 captures and 363 segments.
Minimum midpoint SSIM is **0.982302 / 0.983325** respectively.
All six extension videos played locally, and every one of the 15 chapter seeks in each combined video
waited for seek completion and a decoded frame. Korean reboot parts keep their own video epochs;
authentication transitions and source tails are explicitly excluded.

[English results](../edition-results.md) and [Korean results](../ko/edition-results.md) preserve actual failures.
The Optimizer's self-referential grounding inputs are not accepted as source verification or a promotion gate.
The separate conversation evaluations retained the original policy JSON in their actual judge inputs.
The Korean safety D06 tool-discovery failure remains a failed response despite CLI exit 0.
On September 17, all six extension attachments were also verified against their actual private GitHub bytes,
native playback and completed chapter seeks. The manually dispatched CI run remains a separate execution check,
not something inferred from local tests or published video URLs.

The first GitHub check exposed a missing SDK-test development dependency, and the initial release dispatch
was rejected because `runner.temp` was used before the runner context exists.
The SDK job now installs the declared `dev` extra, and the release initializes its path from `$RUNNER_TEMP`
inside a step and passes it through `$GITHUB_ENV`. Regression checks and actionlint 1.7.12 workflow
schema/expression validation passed; the original failed GitHub result remains in its run history.
The corrected [GitHub repository check](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35121096979)
passed all jobs. A subsequent OIDC mismatch was narrowed to the exact immutable subject emitted by this repository;
the existing federation was corrected without new credentials, broader roles or weaker GitHub settings.
The [actual OIDC release](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35121162793)
then passed on attempt 2: Korean dev 6/6, zero errors, original artifact hashes and recomputed business checks verified,
with the exact created session independently confirmed idle. This post-publication run did not execute native judging or holdout.

## Korean prerequisite run — September 15, 2026

The existing Sweden Central workshop project was reused; no default subscription or resource group was changed.
Approved Sol/Terra/Astra deployments were added at 100K TPM with minimum scoped model/Search roles.
Existing Luna, judge, and embedding deployments were reused.

| Cohort | Version | Rows | Errors | Business | Groundedness | Relevance | Root traces |
|---|---:|---:|---:|---:|---:|---:|---:|
| `ko-baseline-final` | 7 | 24 | 0 | 24/24 | 24/24 | 19/24 | 24/24 |
| `ko-candidate` | 8 | 24 | 0 | 24/24 | 22/24 | 20/24 | 24/24 |
| `ko-holdout` | 8 | 16 | 0 | 16/16 | 16/16 | 13/16 | 16/16 |

Calibration classified both prewritten correct/incorrect examples as expected.
It did not create two new target responses or certify the judge generally.
The initial version-6 diagnostic cohort remains separate.

The recommendation is `review-native-findings`, not production approval.
Correct abstentions can score poorly on generic relevance. Scores and reasons remain unchanged.
No failure or regression promotion was manufactured for an all-pass baseline.
The public holdout teaches final acceptance; it is not an unseen production test.

## Independent English run — September 15, 2026

English prompts, corpus, dev/calibration/fixtures and final holdout are separate frozen assets.
The initial version-10 baseline was **20/24**: IQ's default retrieval filter omitted the scope document.
That entire cohort remains unchanged. An explicit same-provider recall diagnostic led to a new baseline/candidate pair;
the evaluator/reference labels and frozen prompts were not weakened or tuned on holdout.

| Cohort | Version | Rows | Errors | Business | Groundedness | Relevance | Root traces |
|---|---:|---:|---:|---:|---:|---:|---:|
| `en-baseline-recall` | 11 | 24 | 0 | 24/24 | 24/24 | 20/24 | 24/24 |
| `en-candidate` | 12 | 24 | 0 | 23/24 | 24/24 | 20/24 | 24/24 |
| `en-holdout` | 12 | 12 | 0 | 12/12 | 12/12 | 9/12 | 12/12 |

Astra failed the predeclared citation-relevance check on dev D05.
Only Luna/Sol/Terra were selected **using dev results before any holdout response**; the final denominator is 12, not 16.
The original four-model candidate remains 23/24. English calibration classified both fixed examples correctly.
The D05 regression candidate remains pending human review and was not promoted/consumed without approval.
Read the [full English lineage](../live-run.md); neither language's outcomes are copied into the other.

## Corrections established by actual calls

Endpoint/protocol CLI conflicts, dropped API-version query parameters, explicit account embeddings,
App Insights credential scoping, and already-idle session cleanup were fixed while preserving original failures.
Changed runtime versions and controlled comparisons remain separately labeled.

## Media evidence

The Korean set contains 182 actions, 543 lossless screenshots, and three edited videos.
Published WebP pixels exactly match source PNGs.
All 435 retained source-video segments were compared, with minimum midpoint SSIM 0.987849.
Full MP4 decoding and frame counts were checked; chapter cards are labeled as non-application footage.

Authentication/password entry is excluded. Failures and diagnostics remain in the source ledger.
One portal trace showed 17 spans/two chat calls while the response recorded three actual model calls:
root trace verification is not proof that every child span was exported.
The six uploaded synthetic files were read back through the Files API and matched byte-for-byte.
An unconfirmed UI citation download was not reported as successful.

The English set has **172 actions, 516 lossless captures, three videos and 407 checked source-video segments**.
Its minimum midpoint SSIM is **0.985156**. Actual native playback, byte ranges and all 12 chapter jumps were verified for each language.
All six new videos were uploaded as private-repository GitHub attachments after user approval.
Their actual hosted bytes/hashes, native playback, and chapter seeks were verified.
Only canonical attachment URLs are saved; temporary signed storage URLs are not retained.
Older current-worktree media files were removed only after both replacements passed these checks.

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

SDK tests use the actual installed libraries with explicitly stubbed transports.
They are not counted as real Azure responses.
After the guide/preset revision: **126 offline tests on each of Python 3.13 and 3.14, 27 installed-SDK tests**, Ruff check/format,
Python compilation, dependency compatibility, and documentation checks passed.
Documentation checks cover **37 language pairs and 218 CLI examples**, with no pending translations.
Both deterministic learner bundles match their canonical inputs on Python 3.13 and 3.14.

## Guide and IQ preset revision — September 15, 2026

All 24 language lab pages now have scope, prerequisites, completion/recovery and next-step cards.
The A route includes its capstone and totals 240 minutes **after preparation**.
Ready browser instructions, questions-only files and blank assessments derive from canonical v2/policies/dev;
neither reference-answer columns nor holdout enter the learner ZIP. Original prompts/datasets and media were not changed.

The final **read-only Azure preflight** confirmed `gpt-5.6-luna` / `2026-07-09` in `Succeeded` state,
the actual Search system-assigned identity, its documented account role, and the intended synthetic source.
It returned `ready_for_setup: true`, **`configured: false`**, `model_inference_verified: false`, and `cloud_changes: false`.
The new permanent chat base was **not created**. No new role assignment, deployment or paid inference/evaluation was performed for this revision.

The earlier successful MI binding/response was replayed **locally**, without another Azure request.
This confirmed API-key `null` serialization and the actual `id/title/content` source projection.
Returned fields are checked against the canonical corpus; missing date fields are not invented.
Transport tests cover configuration/model drift before paid requests, explicit errors, ownership, and preserved failures.

These checks are not a new end-to-end Azure run, a novice classroom pilot, or a rerecording of the revised preparation steps.
Earlier live scores/footage retain their original versions and hashes; they do not prove execution of the newly changed code.

## Not established

Real company/Microsoft 365 data, external Work IQ/Fabric connections, operational SLAs,
statistical superiority, automatic retraining/weight changes, human production approval,
and deletion of other users' resources are outside this evidence.
Stopping sessions does not eliminate all model/Search/log/storage costs.
