# gpt-6-sol live execution and evaluation results — September 24, 2026

**English** | [한국어](ko/live-run.md)

**These are this English recording's actual Azure results from September 24, 2026.** They are not copied from the Korean run, from the earlier `gpt-5.6-luna` editions or from upstream repositories.

## Environment

| Item | Value |
|---|---|
| Region / project | Sweden Central / `mfv2-g6luna-20260923` |
| Answer deployment | `gpt-6-sol` → `gpt-6-sol` `2026-09-22`, DataZoneStandard 150K TPM, NoAutoUpgrade |
| Judge deployment | `gpt-6-sol-judge` → `gpt-6-sol` `2026-09-22`, DataZoneStandard 100K TPM |
| Created by the portal | `text-embedding-3-large` Standard 110K — created when the first portal agent opened; not used by these labs |
| Owned prefix | `mfv2-sol-20260924-en` |

Resource names keep the environment's original `g6luna` label; the recorded deployments are `gpt-6-sol`. Local keys are disabled; every call used Microsoft Entra ID.

## Lab 07 business evaluation

| Cohort | Split | Instructions | Rows | Errors | Business | Median latency |
|---|---|---|---:|---:|---:|---:|
| baseline | dev | v1 | 6 | 0 | 6/6 | 2.65 s |
| candidate | dev | v2 | 6 | 0 | 6/6 | 3.08 s |
| final-holdout | holdout | v2 (frozen) | 4 | 0 | 4/4 | 4.26 s |

- The actual baseline had no failed case, so the feedback step was skipped and the dev-only no-evidence diagnostic ran instead: 0/6 with 0 errors, every answer withheld. An all-pass baseline is recorded as-is, not as proof that v2 is better.
- The candidate was frozen before the single holdout run. Holdout was not used for prompt development.
- Acceptance: `ready-for-human-review`, `deployment_approved: false`. This is a small public synthetic set, not a production validation.

## Optional Foundry cloud judge

Candidate dev rows (6), judged by `gpt-6-sol-judge`. Evaluation `eval_30a54a5f94694d7493aa2dc5a50a6147`, run `evalrun_539e35c0a2c14f828ae99c193483c42f`, status `completed`.

| Evaluator | Passed | Failed | Errored |
|---|---:|---:|---:|
| groundedness | 6 | 0 | 0 |
| relevance | 5 | 1 | 0 |

The failed relevance row is **D05** (score 3), the intended abstention case: no international policy exists, and the answer correctly declined to give an amount. A low relevance score on a correct abstention is a judge limitation to review; it is not a reason to invent an amount, and the score is kept unchanged. Native judge scores are not part of the acceptance decision.
The same candidate responses scored relevance 6/6 in the business-rubric run below, with the same judge deployment: judge scores vary between runs, so compare runs only inside one evaluation.

## Optional Foundry evaluations in this recording

| Evaluation | Scope | Result |
|---|---|---|
| Portal evaluation (Lab 07 A) | `mfv2-sol-20260924-en-portal-dev-2`, six dev questions | Relevance 6/6, Coherence 6/6, TaskAdherence 0/6 |
| Portal evaluation, superseded | `mfv2-sol-20260924-en-portal-dev`, agent Version 1 with Web search | Relevance 5/6, Coherence 6/6, TaskAdherence 4/6 |
| Trace evaluation (Lab 09 A) | `mfv2-sol-20260924-en-traces`, the recorded conversations | Relevance 10/10, Coherence 10/10, TaskAdherence 10/10 |
| Business rubric (Lab 07 B, Preview) | `eval_649f9fc6cb224c38b66543e7493d6133` | baseline: groundedness 6/6, relevance 5/6, business_rubric 6/6, agreement 6/6; candidate: groundedness 6/6, relevance 6/6, business_rubric 6/6, agreement 6/6 |
| MAF tool calls (Lab 04, experimental API) | `eval_93954d3f64e04a54bc309b45ae2ac07e` | tool_call_accuracy 6/6, relevance 6/6 |

The first English portal evaluation kept the preselected agent Version 1, which still had Web search. It scored TaskAdherence higher than the saved Version 2 (see the table), while its D05 answer offered an external U.S. federal lodging rate instead of withholding. A higher judge score did not identify the intended agent: check the version before reading scores. The evaluators saw only the question and answer, so they could not verify Version 2's cited policy amounts.

Judge scores are not the business decision; read each row's reason. Portal evaluations were found by their recorded names; their per-row scores are in live-results.json.

## Failures kept in this recording

Failed actions stay in the videos and captures with their real output. A retry or fix is a separate, later action; it does not replace the failed one.

| ID | Exit | What happened |
|---|---:|---|
| E07-011-business-baseline | 2 | Missing evaluator results: the Foundry evaluation had three testing criteria, but its run returned only groundedness and relevance (0 errored). The CLI kept the attempt as invalid and scored nothing; the next action retried it once with --retry-failed. |
| E07-012-business-candidate | 2 | Refused before any job: the retried baseline state had no item_fields, so it could not be a --reference. This was a workshop CLI bug in the new retry path, fixed in native.py during the recording (see Lineage); the completed retry was then read back without a new job and the candidate joined the evaluation. |
| EP07-205-criteria | capture tool | The capture tool clicked TaskAdherence before the Add evaluators list had loaded (Target count 0). The judge and evaluator removals were already applied; EP07-205-criteria-resume added TaskAdherence after the list loaded. Not a Foundry failure. |
| EP07-202-target-scope | superseded | Superseded: the Target list had preselected Version 1 (the first version, which still had Web search) and the capture tool did not change it. Guide step 2 requires the saved version; EP07-211 to EP07-217 repeat the evaluation with Version 2. |
| EP07-206-submit | superseded | Superseded: this evaluation ran agent Version 1 with Web search, not the saved Version 2. |
| EP07-207-results | superseded | Superseded: results for agent Version 1 with Web search; see EP07-217-results for Version 2. |

First business-rubric attempt: evaluation `eval_2cc3faa0e2ca4db1aefe48a26dcc1961`, run `evalrun_675845e548054452b231eec373431968`, status `completed`, validation `invalid`, returned criteria groundedness, relevance. It is kept under `native-attempts/attempt-1`; the retry reused the same pinned evaluator catalog (unchanged).

## Other live results

- **Lab 02:** `response_model: gpt-6-sol` for the first SDK request; the validated structured answer cited `TRAVEL-2026`, `APPROVAL-01`.
- **Lab 03:** portal agent `mfv2-sol-20260924-en-policy` saved as version 2 (answers captured as screens; the optional Lab 09 trace evaluation later scored these conversations); SDK agent `mfv2-sol-20260924-en-policy-sdk` version 1 created and invoked.
- **Lab 04–05:** MAF runs with `tools: none`, `function` and `local-mcp`; workflow patterns sequential, concurrent and group-chat. All exited 0.
- **Lab 06:** local, Search and GA IQ retrieval against the six synthetic policies. The IQ-grounded answer retrieved `TRAVEL-2025`, `TRAVEL-2026` and cited `TRAVEL-2026` (`needs_approval`, KRW 150,000). This retrieval did not return `APPROVAL-01`, so the answer said the approval document was not provided instead of inventing the procedure. It is kept unchanged; compare it with the D03 expectation (`TRAVEL-2026` + `APPROVAL-01`).
- **Lab 08–09:** packaging only (no Hosted deployment); cleanup inventory only (nothing deleted).

## Lineage

- base commit `90b18b305721c73398c92071f3ba7f85540c4d5d`, working-tree source hash `612d9dae1000dc9716c1908bc37a22c6ac71bf336f3283ce08193ed22ed362c8`
- source update from `E07-013-business-retry`: `src/foundry_workshop/cli.py`, `src/foundry_workshop/cloud_evaluation.py` → `fa3fb5ce076c15a3a0df2ba6433021bce7e36b03125c799699c91624001f7aa7`
- source update from `E07-014-business-readback`: `src/foundry_workshop/native.py` → `b38ff5780d8fb920661e822c0ac8fafb0d3bcf0d170e572400735e952937ca4f`
- `baseline` run `52b0b4eb-856f-44bc-bbaf-c0a13ce89af4`: dataset `1fa5362e46e027e3…`, corpus `9df56da4500a010c…`, code `67e7ac041e5b1f78…`, prompt `705dc29ecb89c047…`, responses `6f2a36e4123de036…`
- `candidate` run `b6d22306-7e5a-4555-84af-ce7461824234`: dataset `1fa5362e46e027e3…`, corpus `9df56da4500a010c…`, code `67e7ac041e5b1f78…`, prompt `05c0d23b0f56b080…`, responses `7872de30fbdbe71a…`
- `final-holdout` run `95374597-1104-44e6-8e2d-f99370dd9c54`: dataset `e276e82bbac04260…`, corpus `9df56da4500a010c…`, code `67e7ac041e5b1f78…`, prompt `05c0d23b0f56b080…`, responses `21d5f21fbb834e63…`
- cloud judge: input `92b0a6be29a79f5b…`, evaluator `a0e7f44a59d34f75…`, results `2f1c580401f13193…`

Full hashes are in [live-results.json](assets/g6sol-20260924-en/live-results.json).

## Optional evaluation additions — separate verification, September 23, 2026

These runs verified the optional evaluation steps added after the recording. They used new labels in a separate copy of the
same source (code hash `b160d84d2e0e1087…`), the same `gpt-6-sol` / `gpt-6-sol-judge` deployments and the prefix `mfv2-sol-20260923-en`.
They are not part of the edited videos. Their separate portal captures were removed after the September 24 recording repeated these portal steps ([actions](action-captures.md)).

| Step | Result |
|---|---|
| Lab 07 A optional portal evaluation (`eval_3f85f529…`, 6 questions from `dev-questions.jsonl`) | Coherence 6/6, Relevance 5/6 (D05), TaskAdherence (Preview) 1/6; the manual business assessment of the same agent was 6/6 |
| Lab 07 B dev collections (`baseline` `25dc8b88…`, `candidate` `c8d8e4b3…`) | Business 6/6 and 6/6, 0 errors |
| Lab 07 B no-evidence diagnostic (`diagnostic-no-evidence` `b0b17e7c…`) | Business 0/6, 0 errors; every answer withheld (`insufficient_evidence`); `feedback` rejected the run |
| Lab 07 B cloud judges with the business rubric (`eval_f231e23c…`, two runs) | baseline and candidate: groundedness 6/6, relevance 6/6, `business_rubric` 6/6; agreement with local checks 6/6 each; portal comparison relevance 4.33 → 4.83, **Too few samples** |
| Lab 04 optional `maf-evaluate` (`eval_34a0f785…`) | tool_call_accuracy 6/6, relevance 6/6; one `lookup_policy` call per question |

The custom evaluator `mfv2_sol_20260923_en_business_rubric` is version 2; version 1 was an earlier trial with the same checks before formatting.
The TaskAdherence failures state that the cited amounts cannot be verified, because only the question and the answer reach the evaluator.
The existing-traces evaluation first stopped at the portal's Monitoring Reader request; it ran later the same day after the owner assigned that role (next section).

**Re-check after the code review (code `408b1b57…`):** `maf-evaluate` ran again with the rewritten result mapping
(`eval_fd079e29…`): tool_call_accuracy 6/6 and relevance 6/6, each output item joined to its question.
Cloud judges on the no-evidence diagnostic (run `evalrun_2b495a2e…` in `eval_f231e23c…`) completed, but Groundedness skipped
3 of 6 rows because their context was empty. The service reported relevance 1/6 and `business_rubric` 0/6; the workshop marked the
result invalid and counted nothing. The final code (`67e7ac04…`) refuses such a run before any cloud call, checked on the same label.

## Previously not-run items — September 23, 2026

The owner then asked for the items listed as not run. They ran the same evening against the same project and deployments,
under the prefix `mfv2-sol-20260923-<language>`. None of them is in the edited videos.

| Item | What ran | Result |
|---|---|---|
| Lab 09 A existing-traces evaluation | Owner assigned **Monitoring Reader** to the project identity on Application Insights; portal evaluation of 15 recorded conversations per language (`eval_a68f080f…` English, `eval_71cf2435…` Korean) | Relevance, Coherence and TaskAdherence 15/15 each in both languages; each `query` carried the agent's instructions with the policies |
| Recurring evaluation | **Make recurring** on each trace evaluation: Scheduled, hourly, live traffic, random sampling, 5 traces per run; one planned D01 request per language; then **Pause** | The first run started when the schedule was saved (5/5 in each language). The next hourly run sampled the English planned request (5/5) but not the Korean one (5/5 from older conversations): each run samples the latest seven days. Both schedules were paused and read back as disabled |
| Agent Optimizer | Temporary `gpt-5.5` optimizer deployment; isolated copies `mfv2-sol-20260923-<language>-optimize` v1; Instruction only, 2 candidates, judge `gpt-6-sol-judge` (`opt_63e8e1d5…`, `opt_607d539e…`) | Baseline only: 0.979 English, 0.938 Korean (D05 relevance 2); Groundedness compared each answer with itself; nothing promoted; the temporary deployment was deleted afterwards |
| Cloud red teaming (Preview) | SDK scans of the Lab 03 prompt agents (Prohibited actions taxonomy, Flip and Base64, one turn) and one English portal scan with a two-action taxonomy | Displayed ASR 89% (75/84) English, 57% (48/84) Korean and 100% (6/6) portal, while every row's reasoning called the response safe; no response performed a prohibited action; ASR marked invalid |
| Approved Hosted release | Existing CI identity given project-scoped roles on this project; `hosted-lab-release` runs [35856612314](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35856612314) (English) and [35857252318](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35857252318) (Korean) | Both passed on the first attempt: Hosted agent `mfv2-sol-20260923-ci-hosted` versions 1 and 2, six-case dev gate 6/6 with 0 errors, session idle |

While the temporary optimizer deployment existed, a new evaluation's **Judge model** defaulted to it, and the optimizer wizard's
**Evaluation model** defaulted to `gpt-6-sol`; both were set to `gpt-6-sol-judge` explicitly.
Red-team calls left no agent traces in Application Insights; optimizer runs left 27 per agent, which is why they used isolated copies.

## Not run with gpt-6-sol

- Lab 03 portal File Search
- Lab 06 IQ Chat preset (gpt-5.6-luna) and hybrid RAG
- Lab 07 feedback/regression step (the baseline had no failure; the no-evidence diagnostic ran instead)
- Lab 07 Hosted model matrix
- Lab 08 local server and the learner's own Hosted deployment (the approved CI release deployed a separate Hosted agent)
- Lab 09 server-side tracing checks for a Hosted agent
- Lab 10 external IQ extensions
- Extension modules other than conversation evaluation, Agent Optimizer, the red-team step of agent safety and release operations

Earlier `gpt-5.6-luna` recordings and result pages (September 15–17, 2026) were removed from the working tree; they remain only in git history and are not results for this preset.

[Videos](video-summary.md) · [Actions and captures](action-captures.md) · [Chapters](video-chapters.md) · [Actual results](live-run.md) · [Model choice](reference/model-choice.md)
