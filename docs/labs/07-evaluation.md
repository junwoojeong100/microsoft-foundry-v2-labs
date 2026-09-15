# Lab 07. Evaluate, learn from failures, and verify again

**English** | [한국어](../ko/labs/07-evaluation.md)

**Goal:** Judge improvements with the same business criteria and execution lineage, not "the answer looks good."

Previous: [Lab 06](06-knowledge.md) · Next: A → [Lab 09](09-operations.md), B → [Lab 08](08-hosted.md)

## What becomes a reusable team asset?

```mermaid
flowchart LR
    K["Knowledge and business criteria"] --> B["Dev baseline"]
    B --> F["Failed response / source / request and trace links"]
    F --> H["Human review of cause and proposed improvement"]
    H --> P["New instructions"]
    P --> C["Reevaluate the same dev cases"]
    C --> T["Frozen candidate + unused holdout"]
    T --> G["Human accept/reject decision"]
    G --> O["Operational observation"]
    O --> F
```

Collecting logs does not automatically train model weights. This learning loop improves
**knowledge, instructions, evaluation, and human decisions**.
The canonical data/prompt language remains Korean in both guide editions;
[translation alone is not an English quality evaluation](../reference/languages.md).

## A. Browser: assess all six actual answers

1. Open the six questions in `data/evaluation/en/dev.jsonl`; do not open holdout yet.
2. Send each to your [Lab 03](03-prompt-agent.md) agent in a **new conversation**.
3. Record the actual decision, amount, evidence, and failure reason below.
4. If an instruction is missing a condition, fix it and ask the same six questions again.
5. Retain all before/after answers, not only successes.

If every case passes and no condition is missing, record that honestly. Do not
manufacture failures or force unnecessary edits. The fixed v1/v2 code comparison is separate.

| ID | Business criterion | Actual answer/document ID | Pass/failure reason |
|---|---|---|---|
| D01 | Current lodging KRW 150000 / current policy | Record yourself | Record yourself |
| D02 | Historical lodging KRW 120000 / historical policy | Record yourself | Record yourself |
| D03 | Over limit → advance approval / current + approval policies | Record yourself | Record yourself |
| D04 | Meals KRW 30000 per day / meal policy | Record yourself | Record yourself |
| D05 | No international policy → withhold | Record yourself | Record yourself |
| D06 | Cannot approve despite a request to ignore policy | Record yourself | Record yourself |

This is a **manual business assessment of real answers**, not a Foundry Evaluation
portal run. If using portal batch evaluation, the instructor separately verifies the
evaluator, judge, mappings, and cost before running the same data.


**What to check:** Record the actual KRW 150,000 limit, approval-before-booking condition,
and IDs. Do not fill your table by assuming your answer matches the screenshot.


**What to check:** Withholding an amount is not automatically a business failure.
Assess whether the evidence lacks that policy and the assistant explains how to confirm it.

## B. Code: reproducible run units

The following collection commands call Azure. Defaults use `--retrieval local` so
learners without Search can complete them. To evaluate IQ, change **all three
collections** to `--retrieval iq`; mixing providers is not a single-variable experiment.

Comparisons also freeze project, output limit, and Search endpoint/index/source/base.
`corpus_hash` hashes the local synthetic corpus; it does not prove an immutable remote
index. Do not modify remote documents during the experiment. Preserve actual returned
evidence and each `context_hash`.

### 1. Collect the dev baseline

```bash
python scripts/workshop.py --language en collect --split dev --label baseline --prompt v1 --retrieval local
python scripts/workshop.py --language en evaluate --label baseline
```

`evaluate` exit code `1` means the business gate failed. Inspect the files.
Errored collection rows stay in the six-case denominator; missing, duplicate, or
different questions cause evaluation rejection. **v1 is not guaranteed to fail.**
Never edit actual model responses to manufacture a result.



**What to check:** Read `completed`, `schema`, `decision`, and `required_citations`
inside `checks`. The image shows the final cases; also inspect the summary and all six rows.

### 2. Separate the cause of one failure

Find the actual failed case in `outputs/baseline/responses.jsonl`.

| Symptom | Check first |
|---|---|
| Correct document absent | Retrieval query, index, source |
| Correct document but wrong date | Travel date and instructions |
| Correct amount but no citation | Citation instruction, schema, source ID |
| Claimed approval | Business authority boundary and tools |
| JSON/request error | Model support, output limit, SDK, service |

The following assumes D03 actually failed. Use the real failed ID and reason.

```bash
python scripts/workshop.py --language en feedback --label baseline --case D03 --reason "Review the approval conditions and citations in the actual response against the original policy and investigate omissions."
```

The reason means: compare approval conditions/citations with the source and review
why something was omitted. This creates a **pending-human-review record**, not approval.
It links the original dev expected answer and source run/response/request/trace IDs.
The model's answer is not promoted to ground truth. Missing traces remain `null`;
do not invent UUIDs as Azure trace IDs.

If all dev cases pass, record that and compare an explainable change or design a
separate **new dev version**. Never open holdout to find prompt-development failures.

### 3. Apply improved instructions to the same dev set

Compare `prompts/en/v1.txt` and `prompts/en/v2.txt`. v2 clarifies effective dates,
receipts/approval, document IDs, and insufficient evidence.


**What to check:** Explain which omissions the changed rules target. A text diff is
not an evaluation score; these fixed prompts do not guarantee a performance ordering.

```bash
python scripts/workshop.py --language en collect --split dev --label candidate --prompt v2 --retrieval local
python scripts/workshop.py --language en evaluate --label candidate
python scripts/workshop.py --language en compare --baseline baseline --candidate candidate --variable prompt
```

Do not edit JSONL responses or scores. After instruction/code changes, collect under
a new label. Existing labels are protected; changed input/response hashes invalidate comparison.


**What to check:** Inspect the complete `business-evaluation.json`, using the same
criteria as baseline. The last few passing rows do not establish full success.


**What to check:** Read `variable: prompt`, `changed_context_count`, and
`unchanged_config`. Equal scores or shorter elapsed time do not establish v2 superiority.
Use this language's actual results, not the other edition's scores.

### 4. Optional: Foundry cloud judge

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


**What to check:** Read actual native pass counts and case-level reasons.
Review any low score on correct withholding without changing the score.
`RUN_TOOLS` is an instructor summary helper; learners read their own native result files.

`data/evaluation/en/calibration.jsonl` contains two explicitly correct/incorrect examples.
Use them in a separate evaluator experiment before production. They are not generated
target-model answers, and passing two examples does not establish a universally reliable judge.

### 5. Freeze the candidate, then use holdout once

Proceed only when instructions, model, and retrieval will no longer change.
`--candidate` links the frozen dev candidate.

```bash
python scripts/workshop.py --language en collect --split holdout --label final-holdout --prompt v2 --retrieval local --candidate candidate --unlock-holdout
python scripts/workshop.py --language en evaluate --label final-holdout
python scripts/workshop.py --language en accept --candidate candidate --holdout final-holdout
```

Holdout has four cases. If you change instructions after seeing failures, it is no
longer unused validation. Do not claim final acceptance without a new holdout.
Repository file separation is an educational procedure, not access control or secrecy.


**What to check:** Inspect all four cases and their candidate link, not only H03/H04.
The source 4/4 uses an already-exposed teaching set; it is not evidence from a newly
unseen holdout.

### 6. Model replacement is a separate experiment

Change only to another **verified deployment name** in `.env`, keeping code, prompt,
retrieval, and dev data fixed.

```bash
python scripts/workshop.py --language en collect --split dev --label model-b --prompt v2 --retrieval local
python scripts/workshop.py --language en compare --baseline candidate --candidate model-b --variable model
```

Changed retrieval context makes this an end-to-end result, not a model-only ranking.
Six/four cases are teaching gates, not statistical superiority or a production SLA.

## C. Verify Hosted matrices and the evaluators

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

## New English execution evidence

These are newly recorded English actions using the separate English prompt/data bundle. Use your own returned resource IDs and record your own results.

![Collect every real model-by-case response](../assets/refresh-20260915-en/screenshots/E07B-run-collect-2.webp)

**What to check:** Keep actual numerators/denominators, business checks and native findings separate. The initial 20/24, candidate 23/24 and three-model holdout selection are not hidden.

![Diagnose the actual D05 evidence miss without changing the evaluator](../assets/refresh-20260915-en/screenshots/E06-040-recall-diagnostic-2.webp)

**What to check:** Keep actual numerators/denominators, business checks and native findings separate. The initial 20/24, candidate 23/24 and three-model holdout selection are not hidden.

![Collect every real model-by-case response](../assets/refresh-20260915-en/screenshots/E07R-run-collect-2.webp)

**What to check:** Keep actual numerators/denominators, business checks and native findings separate. The initial 20/24, candidate 23/24 and three-model holdout selection are not hidden.

![Inspect the new recall-controlled English baseline with the same native evaluators](../assets/refresh-20260915-en/screenshots/EP07-031-recall-native-2.webp)

**What to check:** Keep actual numerators/denominators, business checks and native findings separate. The initial 20/24, candidate 23/24 and three-model holdout selection are not hidden.

![Inspect the actual English V2 native results; business failures remain separate](../assets/refresh-20260915-en/screenshots/EP07-040-candidate-native-2.webp)

**What to check:** Keep actual numerators/denominators, business checks and native findings separate. The initial 20/24, candidate 23/24 and three-model holdout selection are not hidden.

![Read Astra D05 and preserve the over-broad citation finding](../assets/refresh-20260915-en/screenshots/EP07-042-astra-finding-2.webp)

**What to check:** Keep actual numerators/denominators, business checks and native findings separate. The initial 20/24, candidate 23/24 and three-model holdout selection are not hidden.

![Inspect the actual English judge calibration, not target-generated answers](../assets/refresh-20260915-en/screenshots/EP07-043-calibration-2.webp)

**What to check:** Keep actual numerators/denominators, business checks and native findings separate. The initial 20/24, candidate 23/24 and three-model holdout selection are not hidden.

![Freeze the three dev-eligible models before opening English holdout](../assets/refresh-20260915-en/screenshots/E07H-select-2.webp)

**What to check:** Keep actual numerators/denominators, business checks and native findings separate. The initial 20/24, candidate 23/24 and three-model holdout selection are not hidden.

![Inspect the actual 12-row English holdout for the three dev-selected models](../assets/refresh-20260915-en/screenshots/EP07-044-holdout-2.webp)

**What to check:** Keep actual numerators/denominators, business checks and native findings separate. The initial 20/24, candidate 23/24 and three-model holdout selection are not hidden.

[Full action index](../action-captures.md) · [Recordings](../video-summary.md)


## Completion

The introductory path uses six dev/four holdout cases; the four-model Hosted path has 24/24/16 rows.
See the [actual English run](../live-run.md) for its own scores, failures, and native findings.
Do not infer superiority or unseen-set quality from this small public teaching dataset.

Retain actual baseline/candidate lineage, failure review or all-pass evidence, frozen
holdout results, and human judgment. `accept` prepares handoff evidence; it **does not
deploy or grant operational approval**. A 100% business-check score does not prove
complete semantic accuracy, security, or legal suitability.
