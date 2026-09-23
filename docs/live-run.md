# gpt-6-sol live execution and evaluation results — September 23, 2026

**English** | [한국어](ko/live-run.md)

**These are this English recording's actual Azure results from September 23, 2026.** They are not copied from the Korean run, from the earlier `gpt-5.6-luna` editions or from upstream repositories.

## Environment

| Item | Value |
|---|---|
| Region / project | Sweden Central / `mfv2-g6luna-20260923` |
| Answer deployment | `gpt-6-sol` → `gpt-6-sol` `2026-09-22`, DataZoneStandard 150K TPM, NoAutoUpgrade |
| Judge deployment | `gpt-6-sol-judge` → `gpt-6-sol` `2026-09-22`, DataZoneStandard 100K TPM |
| Created by the portal | `text-embedding-3-large` Standard 110K — created when the first portal agent opened; not used by these labs |
| Owned prefix | `mfv2-sol-20260923-en` |

Resource names keep the environment's original `g6luna` label; the recorded deployments are `gpt-6-sol`. Local keys are disabled; every call used Microsoft Entra ID.

## Lab 07 business evaluation

| Cohort | Split | Instructions | Rows | Errors | Business | Median latency |
|---|---|---|---:|---:|---:|---:|
| baseline | dev | v1 | 6 | 0 | 6/6 | 1.96 s |
| candidate | dev | v2 | 6 | 0 | 6/6 | 2.37 s |
| final-holdout | holdout | v2 (frozen) | 4 | 0 | 4/4 | 1.79 s |

- The feedback/regression step was **not run** because the actual baseline had no failed case. An all-pass baseline is recorded as-is, not as proof that v2 is better.
- The candidate was frozen before the single holdout run. Holdout was not used for prompt development.
- Acceptance: `ready-for-human-review`, `deployment_approved: false`. This is a small public synthetic set, not a production validation.

## Optional Foundry cloud judge

Candidate dev rows (6), judged by `gpt-6-sol-judge`. Evaluation `eval_f32ab14675784588ba27de99c3713bde`, run `evalrun_ed83f7b8ebc0413db758bc12b66f74b9`, status `completed`.

| Evaluator | Passed | Failed | Errored |
|---|---:|---:|---:|
| groundedness | 6 | 0 | 0 |
| relevance | 5 | 1 | 0 |

The failed relevance row is **D05** (score 3), the intended abstention case: no international policy exists, and the answer correctly declined to give an amount. A low relevance score on a correct abstention is a judge limitation to review; it is not a reason to invent an amount, and the score is kept unchanged. Native judge scores are not part of the acceptance decision.

## Other live results

- **Lab 02:** `response_model: gpt-6-sol` for the first SDK request; the validated structured answer cited `TRAVEL-2026`, `RECEIPT-01`, `APPROVAL-01`.
- **Lab 03:** portal agent `mfv2-sol-20260923-en-policy` saved as version 2 (answers captured as screens, not scored); SDK agent `mfv2-sol-20260923-en-policy-sdk` version 1 created and invoked.
- **Lab 04–05:** MAF runs with `tools: none`, `function` and `local-mcp`; workflow patterns sequential, concurrent and group-chat. All exited 0.
- **Lab 06:** local, Search and GA IQ retrieval against the six synthetic policies. The IQ-grounded answer retrieved `TRAVEL-2025`, `TRAVEL-2026` and cited `TRAVEL-2026` (`needs_approval`, KRW 150,000). This retrieval did not return `APPROVAL-01`, so the answer said the approval document was not provided instead of inventing the procedure. It is kept unchanged; compare it with the D03 expectation (`TRAVEL-2026` + `APPROVAL-01`).
- **Lab 08–09:** packaging only (no Hosted deployment); cleanup inventory only (nothing deleted).

## Lineage

- base commit `47f3b492d5146d8050faf303b4060db2dfc75185`, working-tree source hash `267291d92bfa9ec4d87a9a2aa750bf8abe06b0891588f270472d38a474963038`
- `baseline` run `c87dc00a-02c7-47fd-9523-26b32d0cbfc4`: dataset `1fa5362e46e027e3…`, corpus `9df56da4500a010c…`, code `466558728a75693c…`, prompt `705dc29ecb89c047…`, responses `bbe67be1f89bfc03…`
- `candidate` run `e48d902b-213f-4897-b560-d68361e63e7b`: dataset `1fa5362e46e027e3…`, corpus `9df56da4500a010c…`, code `466558728a75693c…`, prompt `05c0d23b0f56b080…`, responses `78bc9cdbd8a90d2d…`
- `final-holdout` run `a91de1c7-c613-4181-bb62-98ae32b95af3`: dataset `e276e82bbac04260…`, corpus `9df56da4500a010c…`, code `466558728a75693c…`, prompt `05c0d23b0f56b080…`, responses `e887dbf79b78584d…`
- cloud judge: input `1b5daf431e3e3f06…`, evaluator `a0e7f44a59d34f75…`, results `152165cf10c4e7c5…`

Full hashes are in [live-results.json](assets/g6sol-20260923-en/live-results.json).

## Optional evaluation additions — separate verification, September 23, 2026

These runs verified the optional evaluation steps added after the recording. They used new labels in a separate copy of the
same source (code hash `b160d84d2e0e1087…`), the same `gpt-6-sol` / `gpt-6-sol-judge` deployments and the prefix `mfv2-sol-20260923-en`.
They are not part of the edited videos; the portal steps have their own [captures](assets/eval-portal-20260923/captures.json).

| Step | Result |
|---|---|
| Lab 07 A optional portal evaluation (`eval_3f85f529…`, 6 questions from `dev-questions.jsonl`) | Coherence 6/6, Relevance 5/6 (D05), TaskAdherence (Preview) 1/6; the manual business assessment of the same agent was 6/6 |
| Lab 07 B dev collections (`baseline` `25dc8b88…`, `candidate` `c8d8e4b3…`) | Business 6/6 and 6/6, 0 errors |
| Lab 07 B no-evidence diagnostic (`diagnostic-no-evidence` `b0b17e7c…`) | Business 0/6, 0 errors; every answer withheld (`insufficient_evidence`); `feedback` rejected the run |
| Lab 07 B cloud judges with the business rubric (`eval_f231e23c…`, two runs) | baseline and candidate: groundedness 6/6, relevance 6/6, `business_rubric` 6/6; agreement with local checks 6/6 each; portal comparison relevance 4.33 → 4.83, **Too few samples** |
| Lab 04 optional `maf-evaluate` (`eval_34a0f785…`) | tool_call_accuracy 6/6, relevance 6/6; one `lookup_policy` call per question |

The custom evaluator `mfv2_sol_20260923_en_business_rubric` is version 2; version 1 was an earlier trial with the same checks before formatting.
The TaskAdherence failures state that the cited amounts cannot be verified, because only the question and the answer reach the evaluator.
The existing-traces evaluation was not run: the portal asked for a Monitoring Reader role on Application Insights, and no role was assigned.

**Re-check after the code review (code `408b1b57…`):** `maf-evaluate` ran again with the rewritten result mapping
(`eval_fd079e29…`): tool_call_accuracy 6/6 and relevance 6/6, each output item joined to its question.
Cloud judges on the no-evidence diagnostic (run `evalrun_2b495a2e…` in `eval_f231e23c…`) completed, but Groundedness skipped
3 of 6 rows because their context was empty. The service reported relevance 1/6 and `business_rubric` 0/6; the workshop marked the
result invalid and counted nothing. The final code (`67e7ac04…`) refuses such a run before any cloud call, checked on the same label.

## Not run with gpt-6-sol

- Lab 03 portal File Search
- Lab 06 IQ Chat preset (gpt-5.6-luna) and hybrid RAG
- Lab 07 feedback/regression step (no baseline failure; the separate no-evidence diagnostic is rejected by design)
- Lab 07 Hosted model matrix
- Lab 08 local server and Hosted deployment
- Lab 09 server-side tracing checks, the existing-traces evaluation and continuous evaluation
- Lab 10 external IQ extensions
- Extension modules

Earlier `gpt-5.6-luna` recordings and result pages (September 15–17, 2026) were removed from the working tree; they remain only in git history and are not results for this preset.

[Videos](video-summary.md) · [Actions and captures](action-captures.md) · [Chapters](video-chapters.md) · [Actual results](live-run.md) · [Model choice](reference/model-choice.md)
