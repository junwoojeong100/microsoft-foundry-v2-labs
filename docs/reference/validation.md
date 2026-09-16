# Validation boundaries and actual execution

**English** | [한국어](../ko/reference/validation.md)

**Installation, offline contracts, real Azure execution, model quality, and media validation are distinct.**
Each language uses independent execution labels and recording sources.
Earlier videos and upstream results are not relabeled as new evidence.

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
