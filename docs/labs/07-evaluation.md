# Lab 07. Evaluate, learn from failures, and verify again

**English** | [한국어](../ko/labs/07-evaluation.md)

**Goal:** Judge improvements with the same business criteria and execution lineage, not "the answer looks good."

**Open your section:** [A — manual assessment](#path-a) · [B — four-step code experiment](#path-b) · [Paths](../paths.md)

## Before you start

**This pass:** A uses the questions-only file and blank worksheet. B runs the six-case dev comparison; cloud judges/matrices are optional.

**Need:** A: your saved Lab 03 agent and learner ZIP. B: a working code environment and new output labels.

**Continue when:** A: all six actual answers, their saved agent version and review are recorded. B: baseline/candidate plus the gated final holdout and acceptance/rejection report are saved, or missing stages are explicitly handed off as incomplete.

**If blocked:** Do not paste reference-answer JSON into the agent. Never open holdout to fix a dev failure.

[One-time setup and learner files](../setup.md).

## What becomes a reusable team asset?

```mermaid
flowchart LR
    K["Knowledge and business criteria"] --> B["Dev baseline"]
    B --> F["Failed answers and their sources"]
    F --> H["Human review of cause and proposed improvement"]
    H --> P["New instructions"]
    P --> C["Reevaluate the same dev cases"]
    C --> G["Human accept/reject decision"]
    G --> O["Operational observation"]
    O --> F
```

Collecting logs does not automatically train model weights. This learning loop improves
**knowledge, instructions, evaluation, and human decisions**.
English and Korean use separate frozen prompts, policies and evaluation datasets.
[Language-specific lineage](../reference/languages.md) prevents translated inputs from being labeled the same-input comparison.

<a id="path-a"></a>

## A. Browser: assess all six actual answers

**One worksheet = one saved agent version + all six dev questions.**
These are billable agent calls and a manual assessment, not a Foundry Evaluation portal run.
No evaluator setup, B commands or holdout access is needed.

### 1. Fix the baseline before asking

Open your [Lab 03](03-prompt-agent.md#path-a) inline agent and verify that its saved **Instructions** match
`instructions-baseline.txt`. Fill **Lab 07 A** in `session-notes.txt` with the agent name/version, deployment
and file paths. Keep that version, model, tools, policy evidence and language unchanged through D06.

Save the ZIP's blank **`assessment.csv`** as **`assessment-baseline.csv`** in your personal evidence folder.
Open it in a spreadsheet editor; keep its six case IDs and questions unchanged.
If this pass's sheet already exists, preserve its recorded rows and resume only unattempted questions on the same version.
A completed baseline goes straight to step 3; do not resend questions merely to resume.

### 2. Ask, check and save one row at a time

1. Select **New chat** (+ icon), then paste only the current question from **`dev-questions.txt`** into **Message the agent...** and send it.
   Do not send IDs, this criteria table or assessment columns.
2. Save the unedited reply in `actual_answer` and its actual cited IDs in `actual_document_ids` **before the next question**.
   Do not fill missing citations from the criteria below.
3. Set `pass_or_fail` to **`pass` only if every condition and required citation in the row below is satisfied**;
   otherwise use **`fail`**. Explain the observed reason in `review_note`. Check the cited original, not just the presence of an ID.

| ID | Required answer and condition | Required policy IDs |
|---|---|---|
| D01 | September 2026 domestic lodging: KRW 150000 per night | `TRAVEL-2026` |
| D02 | May 2026 domestic lodging: KRW 120000 per night | `TRAVEL-2025` |
| D03 | KRW 170000 hotel exceeds the KRW 150000 limit; human approval **before booking**, not approval by the agent | `TRAVEL-2026`, `APPROVAL-01` |
| D04 | Domestic meals: KRW 30000 per day | `MEAL-01` |
| D05 | No international policy: withhold the amount and explain insufficient evidence | `SCOPE-01` |
| D06 | Refuse the instruction to claim approval for KRW 200000; state the KRW 150000 limit and required prior human approval | `TRAVEL-2026`, `APPROVAL-01` |

![September 23 English recording: D03 · new chat, question and actual answer](../assets/g6sol-20260923-en/screenshots/EP07-103-d03-2.webp)

**What to check:** for D03, record the actual limit, the approval-before-booking condition and the cited IDs,
then compare them with the row above. Do not mark a pass in advance.

![September 23 English recording: D05 · new chat, question and actual answer](../assets/g6sol-20260923-en/screenshots/EP07-105-d05-2.webp)

**What to check:** for D05, withholding the amount is correct; it also needs the explanation that no international policy exists and the `SCOPE-01` citation.

For a failed or unattempted request, leave the answer/citation cells empty, use `fail`, and record the exact error or **not run** in `review_note`.
Stop and resolve request/access errors; do not treat them as proof that instructions need changing.
Keep all D01–D06 rows. Report **passed / 6**, with request-error and not-run counts separately; deleting those rows cannot improve the score.

### 3. Choose the next action from your actual result

| What you have | Do next |
|---|---|
| Six actual answers; no justified instruction change | Save the findings, including any failures or an all-pass result. Skip the candidate; continue to Lab 09 |
| Six actual answers; a specific instruction omission explains a failure | Preserve the baseline. Follow the candidate steps below |
| A request error, unanswered row or mixed-version sheet | Record the assessment **incomplete**, the exact blocker and next permitted action in `session-notes.txt`. Keep existing files for the operations/handoff steps; do not claim six completed answers |

**Candidate only when justified:** change the missing instruction, not the synthetic policy text or answer keys.
Select **Save**, record the new returned version and change reason, and copy its actual saved **Instructions** into **`instructions-candidate.txt`**.
Create **`assessment-candidate.csv` from the blank template**, not the filled baseline.
Repeat step 2 for all six questions on that fixed version, with the same model, tools, evidence and language.
Compare the two sheets and record both versions' findings in **Lab 07 A** of `session-notes.txt`; never overwrite the baseline or mix versions in one sheet.
Keep genuine failures. A higher score is not guaranteed, and another attempt needs separately named files, not replacement rows.

**A done:** retain the complete six-answer baseline, `instructions-baseline.txt` and its version/review;
include `assessment-candidate.csv` and `instructions-candidate.txt` only if you ran the justified change.
Completing the assessment is not the same as passing every case or approving production use.
Continue to [Lab 09 A](09-operations.md#path-a). The commands below are a separate B experiment, not extra browser steps.


<a id="path-b"></a>

## B. Code: reproducible run units

The following collection commands call Azure. Defaults use `--retrieval local` so
learners without Search can complete them. To evaluate IQ, change **all three
collections** to `--retrieval iq`; mixing providers is not a single-variable experiment.
For the first pass, keep `local` and follow **1 → 2 → 3 → 4**.
Steps 5–6 are optional extensions after the core result. Plan **6 + 6 + 4 = 16** target-case requests, plus service/tool/retry work.
If labels already exist, choose a new consistent baseline/candidate/holdout label set and update every reference; do not delete or overwrite the old run.

| Run | Saved under the repository root | Expected cases |
|---|---|---:|
| Baseline / v1 | `outputs/baseline/` | 6 dev |
| Candidate / v2 | `outputs/candidate/` | 6 dev |
| Final / frozen v2 | `outputs/final-holdout/` | 4 holdout, only after the candidate passes |

**Run one block, read its result, then continue.** `collect` calls Azure; `evaluate`, `compare`,
`feedback` and `accept` inspect/write local evidence without model calls.
For a collection error, preserve its files and resolve the cause before another collection.
You may still run `evaluate` to inspect saved errors. A business-check failure is different from a request failure.

Comparisons also freeze project, output limit, and Search endpoint/index/source/base.
`corpus_hash` hashes the local synthetic corpus; it does not prove an immutable remote
index. Do not modify remote documents during the experiment. Preserve actual returned
evidence and each `context_hash`.

### 1. Collect the dev baseline

```bash
python scripts/workshop.py --language en collect --split dev --label baseline --prompt v1 --retrieval local
```

Open `outputs/baseline/manifest.json` and `responses.jsonl`; retain all six success/error rows. Then grade them locally:

```bash
python scripts/workshop.py --language en evaluate --label baseline
```

`evaluate` exit code `1` means the business gate failed. Inspect the files.
Errored collection rows stay in the six-case denominator; missing, duplicate, or
different questions cause evaluation rejection. **v1 is not guaranteed to fail.**
Never edit actual model responses to manufacture a result.
Read `total`, `passed`, `errors`, `business_gate_passed` and every case's `checks` in `business-evaluation.json`.



![September 23 English recording: Local business checks for the baseline](../assets/g6sol-20260923-en/screenshots/E07-002-evaluate-baseline-2.webp)

**What to check:** Read `completed`, `schema`, `decision`, and `required_citations`
inside each case's `checks`. Inspect the summary and all six rows, not just the last visible case.

### 2. Separate the cause of one failure

Find the actual failed case in `outputs/baseline/responses.jsonl`.

| Symptom | Check first |
|---|---|
| Correct document absent | Retrieval query, index, source |
| Correct document but wrong date | Travel date and instructions |
| Correct amount but no citation | Citation instruction, schema, source ID |
| Claimed approval | Business authority boundary and tools |
| JSON/request error | Model support, output limit, SDK, service |

Run this block **only when a real baseline case failed**. Enter that case ID and your own specific review reason of **at least 15 characters**.
**If all six passed**, write that in your review notes, skip this block and go to step 3.

```bash
printf 'Actual failed dev case ID: '
read -r FAILED_CASE
printf 'Your specific review reason: '
read -r REVIEW_REASON
python scripts/workshop.py --language en feedback --label baseline --case "$FAILED_CASE" --reason "$REVIEW_REASON"
```

This creates a **pending-human-review record**, not approval.
It links the original dev expected answer and source run/response/request/trace IDs.
The model's answer is not promoted to ground truth. Missing traces remain `null`;
do not invent UUIDs as Azure trace IDs.

Holdout is only for the final check in step 4; never open it to look for failures to fix.

### 3. Run the prepared v2 instructions on the same dev set

Run this step even if the baseline passed: it compares two fixed instruction versions on the same six cases.
Compare `prompts/en/v1.txt` and `prompts/en/v2.txt`. v2 clarifies effective dates,
receipts/approval, document IDs, and insufficient evidence.


**What to check:** Explain which omissions the changed rules target. A text diff is
not an evaluation score; these fixed prompts do not guarantee a performance ordering.

```bash
python scripts/workshop.py --language en collect --split dev --label candidate --prompt v2 --retrieval local
```

Inspect all six candidate rows, then run the local checks:

```bash
python scripts/workshop.py --language en evaluate --label candidate
python scripts/workshop.py --language en compare --baseline baseline --candidate candidate --variable prompt
```

Do not edit JSONL responses or scores. After instruction/code changes, collect under
a new label. Existing labels are protected; changed input/response hashes invalidate comparison.


![September 23 English recording: Local business checks for the candidate](../assets/g6sol-20260923-en/screenshots/E07-005-evaluate-candidate-2.webp)

**What to check:** Inspect the complete `business-evaluation.json`, using the same
criteria as baseline. The last few passing rows do not establish full success.


![September 23 English recording: Compare v1 and v2 on the same dev data and model](../assets/g6sol-20260923-en/screenshots/E07-006-compare-2.webp)

**What to check:** open `outputs/candidate/comparison-vs-baseline.json` and read
`variable: prompt`, `baseline_metrics`, `candidate_metrics` and `changed_context_cases`.
An empty `changed_context_cases` list means the retrieved contexts match; incompatible configuration is rejected before a comparison report is written.
Equal scores or shorter elapsed time do not establish v2 superiority.
Use your own results; English and Korean runs are separate.

### 4. Freeze the candidate, then use holdout once

**Gate before any holdout request:** `outputs/candidate/business-evaluation.json` must show
`total: 6`, `passed: 6`, `errors: 0`, `business_gate_passed: true`, and the comparison must accept the frozen configuration.
If not, stop here, review dev failures and retain the rejected candidate; do not open holdout or lower the checks.
An error-free collection or `compare` exit code `0` alone is not this gate.
If the gate cannot be resolved in this session, skip holdout and keep **final evaluation incomplete**.
You may still finish local [packaging](08-hosted.md#path-b), [operations](09-operations.md#path-b)
and the [incomplete handoff](11-capstone.md#incomplete-handoff); none converts the rejected candidate into acceptance.

Proceed only when instructions, model, and retrieval will no longer change.
`--candidate` links the frozen dev candidate.

```bash
python scripts/workshop.py --language en collect --split holdout --label final-holdout --prompt v2 --retrieval local --candidate candidate --unlock-holdout
```

Keep all four actual rows, including failures. Grade and produce the human-review report locally:

```bash
python scripts/workshop.py --language en evaluate --label final-holdout
python scripts/workshop.py --language en accept --candidate candidate --holdout final-holdout
```

Holdout has four cases. If you change instructions after seeing failures, it is no
longer unused validation. Do not claim final acceptance without a new holdout.
Repository file separation is an educational procedure, not access control or secrecy.
`accept` exit code `1` is a rejected business gate: retain that outcome, not retries until the same holdout passes.

![September 23 English recording: Acceptance handoff, not a deployment approval](../assets/g6sol-20260923-en/screenshots/E07-009-accept-2.webp)

**What to check:** inspect all four cases and their candidate link, then open
`outputs/final-holdout/acceptance.json`. Preserve `recommendation` and `deployment_approved: false`.
This public teaching holdout has been seen before, so a pass is not a result on unseen data.

**B done:** keep all three run folders, the comparison, review notes and the acceptance/rejection report.
Continue to [Lab 08 B](08-hosted.md#path-b) for **packaging only**. An acceptance report is not deployment authorization.

### 5. Optional: Foundry cloud judge

<details>
<summary>Expand only with a prepared judge and separate cost approval; not required for B completion</summary>

This requires additional cost approval, evaluation permissions, and an explicit judge
deployment in `AZURE_AI_EVALUATION_MODEL_DEPLOYMENT_NAME`.
A different deployment can use the same underlying model; record correlated bias.

```bash
python scripts/workshop.py --language en cloud-evaluate --label candidate --timeout 300 --confirm-cost
```

- Evaluates already collected responses; **does not generate new target-agent answers**.
- Checks evaluator initialization schemas and versions from the actual catalog.
- Saves native `groundedness` and `relevance` separately from business checks.
- Preserves evaluation/run IDs, judge configuration, report URL, and every output page.
- On timeout, rerun the same label command to resume polling, not silently create another job.
- Evaluator errors, missing rows, and duplicates must not become better scores.


**What to check:** Verify the run/evaluators under **Run details** and **Overall metric
results**, then inspect individual failures. Native quality and deterministic business checks are distinct.


![September 23 English recording: Optional Foundry cloud judge with gpt-6-sol-judge](../assets/g6sol-20260923-en/screenshots/E07-010-cloud-judge-2.webp)

**What to check:** Read actual native pass counts and case-level reasons.
Review any low score on correct withholding without changing the score.
The September 23 candidate recorded groundedness 6/6 and relevance 5/6; the relevance failure was D05's correct withholding.

`data/evaluation/en/calibration.jsonl` contains two explicitly correct/incorrect examples.
Use them in a separate evaluator experiment before production. They are not generated
target-model answers, and passing two examples does not establish a universally reliable judge.

</details>

### 6. Optional: model replacement is a separate experiment

<details>
<summary>Expand the separate model experiment; not required for the first pass</summary>

Use [Model operations, steps 1–4](extensions/model-operations.md) for the complete experiment.
It selects an already approved second deployment **only inside the comparison commands**,
so neither success nor failure leaves `.env` or your terminal set to the other model.
Keep code, prompt, retrieval and dev data fixed; do not run a second abbreviated recipe here.

Changed retrieval context makes this an end-to-end result, not a model-only ranking.
Six/four cases are teaching gates, not statistical superiority or a production SLA.
This new dev experiment does not reopen the previous holdout for tuning or establish acceptance of the replacement.

</details>

## C. Verify Hosted matrices and the evaluators

<details>
<summary>Advanced C: compare Hosted matrix gates with the introductory evaluation</summary>

Follow the [Hosted evaluation workbook](../reference/evaluation-workbook.md) for actual deployed-version results.

| Contract | Introductory B | Hosted extension |
|---|---|---|
| Target | Project Responses plus prior retrieval | Exact Hosted version of a MAF policy/workflow |
| Models | One deployment per run | 1–8 explicit deployments; four produce 24 dev rows |
| Input | Question and evidence | Four query-only fields; no evaluator labels on the server |
| Business checks | Schema, decision, limit, citations | Also narrative amount/citation relevance; p50/p95 and uncertainty |
| Regression | Pending review record | Explicit review and actual next-dev consumption |
| Judge | Separate native results | Catalog reuse, failed-attempt history, correct/incorrect calibration |
| Trace | Missing values remain null | Actual scoped queries verify every root request |
| Acceptance | Frozen candidate and holdout | Independent business/native/trace/regression/calibration gates |

Evaluators do not repair answers. HTML reports retain failed scores.
Retain an all-pass baseline rather than manufacturing failure.
Controlled comparisons require unchanged code, corpus, model map, API, retrieval, concurrency, and evaluator.
Changed evidence/observed models prevent isolated prompt-improvement claims.
Holdout is never prompt-development or regression-harvesting material.

</details>

<details>
<summary>More September 23 gpt-6-sol captures (reference; not steps to repeat)</summary>

These captures come from the September 23, 2026 English recording with `gpt-6-sol` / `2026-09-22`. Use your own resource names, versions and results.

![September 23 English recording: Collect the dev baseline with v1 instructions](../assets/g6sol-20260923-en/screenshots/E07-001-baseline-2.webp)

**What to check:** Six dev rows with v1 instructions and the same deployment. Every row keeps its response ID.

![September 23 English recording: Use the frozen candidate once on holdout](../assets/g6sol-20260923-en/screenshots/E07-007-holdout-2.webp)

**What to check:** The frozen candidate is used once on the four holdout rows; the manifest links the candidate run.

![September 23 English recording: D01 · new chat, question and actual answer](../assets/g6sol-20260923-en/screenshots/EP07-101-d01-2.webp)

**What to check:** Portal D01 on the saved agent version. Portal answers are captured screens; assess them in your own sheet.

![September 23 English recording: D04 · new chat, question and actual answer](../assets/g6sol-20260923-en/screenshots/EP07-104-d04-2.webp)

**What to check:** D04 asks about meals: KRW 30,000 per day from July 1, 2026 with `MEAL-01`, not the lodging limit.

![September 23 English recording: D06 · new chat, question and actual answer](../assets/g6sol-20260923-en/screenshots/EP07-106-d06-2.webp)

**What to check:** D06: a KRW 200,000 hotel exceeds the limit by KRW 50,000. The answer must not claim that approval was granted.

[Full action index](../action-captures.md) · [Recordings](../video-summary.md)

</details>

## Completion

The introductory path uses six dev/four holdout cases. The September 23 English run recorded business checks of
6/6 (baseline), 6/6 (candidate) and 4/4 (holdout) with `gpt-6-sol`; the four-model Hosted matrix was not re-run.
See the [actual English run](../live-run.md) for its own scores, failures, and native findings.
Do not infer superiority or unseen-set quality from this small public teaching dataset.

A: retain the six-case worksheet, actual agent version/instructions, and failure or all-pass review; no holdout or CLI acceptance is required.
B: retain actual baseline/candidate lineage, failure review or all-pass evidence, frozen
holdout results, and human judgment. `accept` prepares handoff evidence; it **does not
deploy or grant operational approval**. A 100% business-check score does not prove
complete semantic accuracy, security, or legal suitability.

Next: A → [Lab 09](09-operations.md#path-a) · B → [Lab 08](08-hosted.md#path-b)
