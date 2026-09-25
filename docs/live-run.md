# gpt-6-sol live execution and evaluation results — September 24, 2026

**English** | [한국어](ko/live-run.md)

**These are this English recording's actual Azure results from September 24, 2026.** They are not copied from the Korean run, from the earlier `gpt-5.6-luna` editions or from upstream repositories.

**Later check:** [September 25 live guide audit](#azure-guide-audit-20260925) covers the CLI routes and trace API in both languages, with one retained request failure. It is not a new portal recording.
The subsequent [headless portal follow-up](#headless-guide-audit-20260925) resolved its browser-authentication blocker and added new responses, timings and screenshots, not a new video.
**Latest:** the [final closeout](#final-guide-closeout-20260925) ran bounded core checks only after the final guide corrections and offline gates; its fresh results and remaining boundaries are separate below.

## Environment

| Item | Value |
|---|---|
| Region / project | Sweden Central / `mfv2-g6luna-20260923` |
| Answer deployment | `gpt-6-sol` → `gpt-6-sol` `2026-09-22`, DataZoneStandard 150K TPM, NoAutoUpgrade |
| Judge deployment | `gpt-6-sol-judge` → `gpt-6-sol` `2026-09-22`, DataZoneStandard 100K TPM |
| Created by the portal | `text-embedding-3-large` Standard 110K — created automatically when the recording's trainer opened the first portal agent; not used by these labs |
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

These runs verified the optional evaluation steps before the September 24 recording repeated them. They used new labels in a
separate copy of the same source (code hash `b160d84d2e0e1087…`), the same `gpt-6-sol` / `gpt-6-sol-judge` deployments and the
prefix `mfv2-sol-20260923-en`; they are not in the edited videos.

| Step | Result |
|---|---|
| Lab 07 A optional portal evaluation (`eval_3f85f529…`, 6 questions from `dev-questions.jsonl`) | Coherence 6/6, Relevance 5/6 (D05), TaskAdherence (Preview) 1/6; the manual business assessment of the same agent was 6/6 |
| Lab 07 B dev collections (`baseline` `25dc8b88…`, `candidate` `c8d8e4b3…`) | Business 6/6 and 6/6, 0 errors |
| Lab 07 B no-evidence diagnostic (`diagnostic-no-evidence` `b0b17e7c…`) | Business 0/6, 0 errors; every answer withheld (`insufficient_evidence`); `feedback` rejected the run |
| Lab 07 B cloud judges with the business rubric (`eval_f231e23c…`, two runs) | baseline and candidate: groundedness 6/6, relevance 6/6, `business_rubric` 6/6; agreement with local checks 6/6 each; portal comparison relevance 4.33 → 4.83, **Too few samples** |
| Lab 04 optional `maf-evaluate` (`eval_34a0f785…`) | tool_call_accuracy 6/6, relevance 6/6; one `lookup_policy` call per question |

Findings, the re-check after the code review and Azure changes: [validation](reference/validation.md#foundry-evaluation-additions).

## Previously not-run items — September 23, 2026

These items ran the same evening against the same project and deployments, under the prefix `mfv2-sol-20260923-<language>`;
none is in the edited videos.

| Item | What ran | Result |
|---|---|---|
| Lab 09 A existing-traces evaluation | Owner assigned **Monitoring Reader** to the project identity on Application Insights; portal evaluation of 15 recorded conversations per language (`eval_a68f080f…` English, `eval_71cf2435…` Korean) | Relevance, Coherence and TaskAdherence 15/15 each in both languages; each `query` carried the agent's instructions with the policies |
| Recurring evaluation | **Make recurring** on each trace evaluation: Scheduled, hourly, live traffic, random sampling, 5 traces per run; one planned D01 request per language; then **Pause** | The first run started when the schedule was saved (5/5 in each language). The next hourly run sampled the English planned request (5/5) but not the Korean one (5/5 from older conversations): each run samples the latest seven days. Both schedules were paused and read back as disabled |
| Agent Optimizer | Temporary `gpt-5.5` optimizer deployment; isolated copies `mfv2-sol-20260923-<language>-optimize` v1; Instruction only, 2 candidates, judge `gpt-6-sol-judge` (`opt_63e8e1d5…`, `opt_607d539e…`) | Baseline only: 0.979 English, 0.938 Korean (D05 relevance 2); Groundedness compared each answer with itself; nothing promoted; the temporary deployment was deleted afterwards |
| Cloud red teaming (Preview) | SDK scans of the Lab 03 prompt agents (Prohibited actions taxonomy, Flip and Base64, one turn) and one English portal scan with a two-action taxonomy | Displayed ASR 89% (75/84) English, 57% (48/84) Korean and 100% (6/6) portal, while every row's reasoning called the response safe; no response performed a prohibited action; ASR marked invalid |
| Approved Hosted release | Existing CI identity given project-scoped roles on this project; `hosted-lab-release` runs [35856612314](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35856612314) (English) and [35857252318](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35857252318) (Korean) | Both passed on the first attempt: Hosted agent `mfv2-sol-20260923-ci-hosted` versions 1 and 2, six-case dev gate 6/6 with 0 errors, session idle |

Findings, owner actions and Azure changes: [validation](reference/validation.md#previously-not-run-items).

<a id="review-refresh-live-verification"></a>

## Review refresh live verification — September 24, 2026 (evening)

Same project and deployments as above. Two fresh copies of commit `a9c3990` used the prefixes `mfv2-rr-20260924-en` and
`mfv2-rr-20260924-ko` and the refreshed pins (`azure-ai-projects` 2.6.1, `openai` 3.16.1, MAF core 1.18.0,
`agent-framework-foundry` 1.13.0, hosting 1.0.0b260910, `mcp` 1.30.0). Calls used Microsoft Entra ID with the lab subscription
pinned; the Azure CLI default subscription was not changed. Nothing here was recorded; the [September 25 supplement](#review-refresh-supplement) recorded Lab 03 B and the Lab 09 B trace search.

| Core B step | English | Korean |
|---|---|---|
| Lab 00 `doctor --cloud` | `gpt-6-sol` `2026-09-22`, `Succeeded` | Same |
| Lab 02 `model` / `answer` | `response_model: gpt-6-sol`; KRW 150,000 citing `TRAVEL-2026`, `APPROVAL-01` | Same model; KRW 150,000 citing `TRAVEL-2026`, `RECEIPT-01`, `APPROVAL-01` |
| Lab 03 B managed agent | `mfv2-rr-20260924-en-policy-sdk` version 1; invoke `resp_0e84a5df…` (1,124 / 101 tokens), `TRAVEL-2026` | `mfv2-rr-20260924-ko-policy-sdk` version 1; invoke `resp_0883c0c2…` (1,290 / 157 tokens), `TRAVEL-2026` |
| Lab 04 function / MCP | `needs_approval` (`TRAVEL-2026`, `APPROVAL-01`, `RECEIPT-01`) / KRW 120,000 (`TRAVEL-2025`) | Same decisions and citations |
| Lab 05 workflows | Sequential 1, concurrent 4, Group Chat 4 outputs; all `pending-human-review` | Same |
| Lab 06 retrieval | Local and Search: six sources; GA IQ: four; IQ answer `needs_approval` (`TRAVEL-2026`, `APPROVAL-01`) | Same |
| Lab 07 | baseline 6/6, candidate 6/6, holdout 4/4, 0 errors; `ready-for-human-review`, `deployment_approved: false` | Same |
| Lab 08–09 | Package `cloud_deployed: false`; `cleanup-plan` lists the three owned Search objects | Same |

Median latencies: English 2.51 / 2.67 / 3.53 s, Korean 2.46 / 3.17 / 2.56 s (baseline / candidate / holdout). Both baselines had no failed case,
so `feedback` was not run. Lab 07 runs: English `9a8d3d81…`, `9e187bee…`, `8953197f…`; Korean `bf510464…`, `4924c781…`, `ded07977…`.

**Traces (Lab 09 B):** a read-only Application Insights query by response ID found `invoke_agent <agent>:1` and `chat gpt-6-sol-2026-09-22`
spans for every managed agent call, with token counts equal to the saved `usage`, within about three minutes. The direct Responses calls
(`model`, `answer`, `maf`, `workflow`, `collect`) left no server-side spans.

| Optional or C item | Result |
|---|---|
| Lab 04 `maf-evaluate` (English) | `complete: true`, 0 errors, tool_call_accuracy 6/6, relevance 6/6; Pydantic serializer warnings printed but did not affect the run |
| Lab 07 `cloud-evaluate` candidate (English) | groundedness 6/6, relevance 5/6 (D05 score 2, the correct abstention) |
| A2A 1.0 (English) | Typed target and caller; card offered 1.0 JSONRPC plus 0.3; one delegated call (`a2a_preview_call`) completed; caller usage 676 / 228 tokens |
| Insights (English, SDK) | 22 traces analyzed, 4 insights, 227,246 judge tokens; the monitor was deleted afterwards |
| Lab 08 section 6 workflow server (English, local) | `healthy`; one Responses request completed with three model calls and `pending-human-review` (sent with curl, not `azd ai agent invoke --local`) |
| Recipes 02–06 and 08 (English) | All completed after the two fixes below |

**Found and fixed during this check:**

1. The recipes built `AzureCliCredential()` without a subscription. With several Azure CLI accounts it used another tenant's default account and the call failed with 403; the recipes now pin `AZURE_SUBSCRIPTION_ID`.
2. Recipes 05 and 08 sent no policy evidence, so the model answered that no policy was available; they now carry the synthetic policies as data.
3. `maf-evaluate` with `openai` 3.x prints Pydantic serializer warnings; the guide now says to judge `complete` and `errors`.
4. An Application Insights query through a tool bound to the default account failed with `InvalidTokenError`; the guide now asks for a lab-tenant token.

**Not run:** a remote Hosted deployment for the browser Lab 05 option (needs separate approval); a cross-provider comparison
(the project has no non-OpenAI deployment); Toolbox, Tool Search and Skills (not attempted that evening; on September 25 the keyless
connection existed but Search denied the project identity, [below](#not-run-feasibility));
Memory, Routines, conversation evaluation, Agent Optimizer and red teaming (code unchanged, not re-run); the portal steps of route A.

**Owned objects created:** agents `mfv2-rr-20260924-en-policy-sdk`, `-ko-policy-sdk`, `-en-recipe-sdk`, `-en-a2a-target-en`, `-en-a2a-caller-en`
(version 1 each); connection `mfv2-rr-20260924-en-a2a-link-en`; Search index, knowledge source and knowledge base for each prefix;
the Foundry evaluations created by `maf-evaluate` and `cloud-evaluate`. Nothing was deleted that evening except the Insights monitor;
the rest was deleted on September 25 ([cleanup record](#cleanup-20260925)).

<a id="review-refresh-supplement"></a>

## Supplement recording and not-run review — September 25, 2026

**Recording, English and Korean.** Neutral working copies of commit `f990af3`, prefixes `mfv2-sup-20260925-<language>`,
same project and deployments. The guide blocks were pasted verbatim into a real zsh terminal and the `read` prompts answered by typing.

| Step | English | Korean |
|---|---|---|
| Lab 03 B create (`--output`) | `mfv2-sup-20260925-en-policy-sdk` version 1 | `mfv2-sup-20260925-ko-policy-sdk` version 1 |
| Lab 03 B invoke (`--output`) | `resp_0ba4d3d0…`, 1,124 / 145 tokens; KRW 150,000 citing `TRAVEL-2026` | `resp_01227453…`, 1,290 / 160 tokens; KRW 150,000 citing `TRAVEL-2026`, `RECEIPT-01`, `APPROVAL-01` |
| Lab 03 B portal check | Playground: Version 1, instructions equal to the CLI definition; Details: `Latest (Version 1)`; no message sent | Same; Details shows `최신(Version 1)` |
| Lab 09 B trace search | One row; trace `0ef25bf8…` equals the Application Insights `operation_Id`; `invoke_agent …:1` and `chat gpt-6-sol-2026-09-22` | One row; trace `71804741…`; same spans |

Screens and clips: [summary](video-summary.md#review-refresh-supplement) · [captures.json](assets/review-refresh-20260925/captures.json).
An earlier English attempt (`mfv2-cap-20260925-en-policy-sdk`, one call) was discarded because its terminal showed a local home-directory path.

<a id="not-run-feasibility"></a>

### What the not-run items need

English only, prefix `mfv2-nr-20260925-en`, same project, lab subscription pinned.

| Item | Result or blocker |
|---|---|
| Conversation evaluation, refreshed pins | Six turns, business checks 6/6; turn level groundedness 6/6 and coherence 6/6 (`eval_e07e2e35…`); conversation level groundedness 2/2 and coherence 2/2 (`eval_e82b6f87…`) |
| Memory, `gpt-6-sol` + `text-embedding-3-large` | Store created; alpha item stored and recalled in a fresh request; beta recall empty; update, forget and store deletion verified absent |
| Routines, azd `azure.ai.routines` 1.0.0-beta.6 | Disabled one-shot timer; one manual dispatch `Finished`; disabled, then deleted. The SDK helper still could not retrieve the response, but a Traces search by its `response_id` found `invoke_agent …:1` and `chat` spans |
| Toolbox | Owned index seeded; Toolbox version 1 created; MCP discovery listed `policy_search`. The direct query returned **Access denied** from Search: the keyless `workshop-search` connection exists, but the project identity has only Search Index Data Reader. Toolbox deleted; no role changed |
| Tool Search and Skills | Blocked by the same Search access |
| Route A Lab 09 trace check | Read-only: under **7D** the September 24 browser agent listed 16 traces; the 12 opened each showed `invoke_agent <agent>:2` with a child `chat` span |
| Remote Hosted deployment (A Lab 05 browser option) | Needs a deployment and runtime role assignments; owner approval required |
| Cross-provider comparison | Needs one non-OpenAI deployment. Read-only check: the account catalog offers, for example, `grok-4-1-fast-reasoning` (GlobalStandard) and `Mistral-Large-3` (DataZoneStandard) with unused quota; owner approval required |
| Agent Optimizer | Needs a supported optimizer deployment such as `gpt-5.5` (quota available); owner approval required |
| Cloud red teaming | No workshop code path changed; the September 23 run stands; not re-run |
| Foundry Dev Pack | Installs or upgrades global `az`/`azd` tooling on the workstation; use a clean machine; not run |

**Owned objects created on September 25:** agents `mfv2-cap-20260925-en-policy-sdk`, `mfv2-sup-20260925-en-policy-sdk`, `mfv2-sup-20260925-ko-policy-sdk`
and `mfv2-nr-20260925-en-policy-sdk` (version 1 each); Search index `mfv2-nr-20260925-en-policies`; the two conversation evaluations.
The memory store, Toolbox and routine were deleted by their own module commands; the rest was deleted the same day.

<a id="cleanup-20260925"></a>

### Cleanup — September 25, 2026

The owned objects of the September 24 and 25 checks were deleted after their definitions and evaluation results were exported to the private record.
Each was read back afterwards and returned 404.

| Object | Deleted |
|---|---|
| Agents (version 1 each) | `mfv2-rr-20260924-en-a2a-caller-en`, `mfv2-rr-20260924-en-a2a-target-en`, `mfv2-rr-20260924-en-policy-sdk`, `mfv2-rr-20260924-ko-policy-sdk`, `mfv2-rr-20260924-en-recipe-sdk`, `mfv2-cap-20260925-en-policy-sdk`, `mfv2-sup-20260925-en-policy-sdk`, `mfv2-sup-20260925-ko-policy-sdk`, `mfv2-nr-20260925-en-policy-sdk` |
| Connection | `mfv2-rr-20260924-en-a2a-link-en`, after its caller agent and before its target |
| Evaluations | `mfv2-rr-20260924-en-maf-tools`, `mfv2-rr-20260924-en-candidate`, `mfv2-nr-20260925-en-conversations-first-turn`, `mfv2-nr-20260925-en-conversations-first-conversation` |
| Datasets | The four `eval-data-2026-09-24_…_UTC` datasets the service created with those evaluation runs, matched by time and row content |
| Search | Knowledge base → knowledge source → index for `mfv2-rr-20260924-en` and `mfv2-rr-20260924-ko`; index `mfv2-nr-20260925-en-policies` |

The Entra agent identity and blueprint of each deleted agent also returned 404, while those of a retained agent still returned 200.
The evaluation delete call returned no `deleted: true` field; only the read-back confirmed each deletion.
Kept: the September 23–24 recording agents, evaluations and datasets, and the shared connections, deployments, Search service and Application Insights.

<a id="end-to-end-20260925"></a>

## End-to-end guide run — September 25, 2026

**Both core routes ran as written, in English and Korean, against the same project and deployments.** Fresh copies of commit
`f128f0c` came from GitHub: English by the documented sparse clone, Korean by **Download ZIP**. Prefixes were `mfv2-e2e-20260925-<language>`.
Route B ran every core bash block of Labs 00–11 in order in one terminal (English zsh, Korean macOS bash 3.2), typing the answers at
each `read` prompt. Only two steps happened outside a block, as the guide describes: the already signed-in account replaced
`az login` (which would also reset this shared machine's default subscription), and `.env` was filled from the setup card.
Route A ran the portal steps of Labs 01–03, 07 and 09 in the English and Korean portal UI, plus Lab 05 A's terminal command in English.

| Check | English | Korean |
|---|---|---|
| Route B blocks | 34 exited 0; the feedback block was skipped because the baseline passed 6/6 | Same |
| Route B results | Baseline 6/6, candidate 6/6, holdout 4/4; `ready-for-human-review`, `deployment_approved: false`; Lab 03 B version 1; Search and IQ six documents; Lab 08 package only | Same |
| Route A, Labs 01–02 | Full project endpoint, `gpt-6-sol` `2026-09-22` **Succeeded**, the four **Build** menu entries; Web search listed and removed; the no-evidence answer asked for the policy | Same, in the Korean UI |
| Route A, Labs 03 and 07 | Saved version 2 with all six policy IDs; D01–D06 each met its criteria on that version | Same |
| Route A, Lab 09 | **Details** `Latest (Version 2)`; 10 traces, each opened one `invoke_agent <agent>:2` with a child `chat` span and no `web.run` | **세부 정보** `최신(Version 2)`; same traces |

**Found and fixed in the guide:**

1. The portal's **Create an agent** dialog now has a required **Interaction mode** (default **Text**, fixed after creation), and its button
   reads **Create agent and open playground**; Lab 03 A says so and shows [the new dialog](assets/e2e-check-20260925/captures.json).
2. An agent's **Details** tab shows the name and active version but not the model; Lab 09 A now checks the model on the **Playground** tab.
3. Lab 03 A named the removed September 23 recording's agent; it now names the September 24 one.
4. Lab 02 B now says the fields sit inside the top-level `answer` object, and Lab 05 B quotes the English round-limit item
   `The group chat has reached the maximum number of rounds.`, which also appears in Korean runs.
5. The Korean Lab 07 feedback block now prompts in Korean.

**Cleanup:** agents `mfv2-e2e-20260925-<language>-policy` (versions 1–2) and `mfv2-e2e-20260925-<language>-policy-sdk` (version 1),
and each language's Search knowledge base, knowledge source and index were deleted and read back as 404, as were the agents'
Entra agent identities. No evaluation or dataset was created.

<a id="azure-guide-audit-20260925"></a>

## Live guide audit — September 25, 2026 (CLI and trace API)

**Scope:** separate English and Korean copies of the current working tree after `b741473`, including the uncommitted guide fixes.
The existing project and `gpt-6-sol` / `2026-09-22` deployment above were verified read-only.
The source repository's personal `.env` still pointed to an earlier project and `gpt-5.6-luna`; it was left unchanged.
Fresh copies used the verified current-guide values and owned prefixes `mfv2-a2-0f01-en` and `mfv2-a2-0f01-ko`.
No request was sent to the older model as a substitute.

| Check | English | Korean |
|---|---|---|
| Core B terminal blocks | 33 distinct blocks completed; 34 attempts because the first Group Chat attempt failed | 33 distinct blocks, all first attempts completed |
| Saved response files | All 14 core JSON files retained | All 14 retained independently |
| Managed Prompt Agent | `mfv2-a2-0f01-en-policy-sdk`, version `1` | `mfv2-a2-0f01-ko-policy-sdk`, version `1` |
| Functions / local MCP | Prior approval for KRW 170000; historical KRW 120000 with `TRAVEL-2025` | Same criteria, independent Korean answers |
| Sequential / concurrent / Group Chat | 1 / 4 / 4 outputs; pending human review, no external actions | Same output shapes; the sequential final text omitted the date and stated the limit only through an over-limit condition, retained as a review finding |
| Search / GA IQ | Six indexed policies; local and ordinary Search returned six, IQ returned four including `TRAVEL-2026` and `APPROVAL-01` | Same counts with the Korean corpus |
| IQ-grounded answer | `needs_approval`, KRW 150000, both required citations; the second retrieval's context hash matched the prior IQ result | Same criteria and independent matching context hash |
| Lab 07 baseline / candidate / final holdout | 6/6 / 6/6 / 4/4, zero collection errors | 6/6 / 6/6 / 4/4, zero collection errors |
| Acceptance | `ready-for-human-review`, `deployment_approved: false` | Same; not copied from English |
| Lab 09 trace API | Matching `invoke_agent` and `chat` spans; input/output tokens 1124 / 123 | Matching spans; 1290 / 216 |
| A Lab 05 terminal option | Exact KRW 170000 question executed once and reviewed | Independently executed once and reviewed |
| Lab 08 / Lab 11 | Local package only; read the existing acceptance report instead of repeating `accept` | Same |

The all-pass baselines correctly skipped `feedback`. Each candidate was reviewed and frozen before its one final holdout collection.
All six evaluation runs used code hash `d105b70b726458f70c1f7820ae8f6a921f0d42a2e008e8100af083e876f59ae4`;
each language retained its own prompt, corpus, dataset and response hashes.
The public teaching holdout is not an unseen production acceptance set.

**Failure kept and code fixed:** English Group Chat's first attempt failed when `az account get-access-token` exceeded
the configured 30-second subprocess timeout. MAF wrapped the credential error in `ChatClientException`, which escaped the
CLI's existing error boundary as a traceback/exit `1`. The CLI now catches the specific Agent Framework exception family,
reports the underlying cause and returns the normal handled-failure code `2`, without writing a success file.
It adds no retry or fallback and changes no timeout, model, endpoint or prompt.
A read-only token check succeeded; one new Group Chat attempt with the same configuration completed. The first log remains retained.

**Browser boundary:** Playwright headless observations exposed an account/tenant mismatch: a project header and
**Loading...** did not establish that the SDK agent had loaded. A visible authentication-only browser was opened for the
training account. Correct-tenant portal verification remains pending authentication; neither the A portal sequence nor
the B portal agent/trace checks are claimed as newly verified. The trace results above came from the scoped read-only API,
not the portal. No new screenshot or video asset was produced.
That was this CLI audit's boundary; the separate headless follow-up below subsequently resolved the portal blocker.

**Other clarifications:** verify the exact preset, not just `Succeeded`; distinguish A's explicit workflow question from
B's default question; and keep IQ `agenticReasoning`/retrieval-token activity separate from answer-model `usage`.
The two GA IQ results reported 413 and 505 reasoning tokens respectively; that is not proof of optional model planning/synthesis.

**Owned assets retained for review:** the two SDK agents and each prefix's `-policies` index, `-source` knowledge source
and `-kb` knowledge base. Ownership ledgers and original errors/results remain in the separate working copies.
Cleanup inventory was recorded; no cloud deletion was performed. Shared models, Search and logging remain owner-managed.
No model deployment, role assignment, Hosted deployment, default-subscription change or push occurred.
The signed-in CLI account was used as configured; a least-privilege learner-only identity was not separately tested.

[Machine-readable results, hashes and trace IDs](assets/azure-guide-audit-20260925/results.json) ·
[Validation and changes](reference/validation.md#azure-guide-audit-20260925).

<a id="headless-guide-audit-20260925"></a>

## Headless portal follow-up and measured response times — September 25, 2026

**The previously blocked A/B portal checks now have new live evidence.** A visible browser was used only for authentication;
all checks ran through **Playwright MCP headless**, English first, then Korean, in the same training project.
The portal language was restored to English. The temporary authentication-transfer file was deleted.

The existing A agents `mfv2-sol-20260924-<language>-policy`, version **2**, were reused without saving a new version.
Their actual saved instructions exactly matched the current learner files, including all six synthetic policies.
The creation dialogs were inspected and cancelled: this is a resume/read-back and request check, **not a new agent-creation run**.

| Check | English | Korean |
|---|---|---|
| Lab 02 model Playground | Two new replies; the no-evidence question withheld the amount | Two independent new replies; the amount was withheld |
| Lab 03 / Lab 06 inline evidence | Four new smoke replies met the date, amount, approval and citation criteria; no external tools or knowledge connection | Same four checks with Korean questions and instructions |
| Lab 07 fixed-version dev assessment | **6/6**, no request errors or missing rows | **6/6**, no request errors or missing rows |
| Send → rendered answer, six dev rows | Median **6.75 s**, range **5.69–9.29 s** | Median **5.41 s**, range **4.11–7.01 s** |
| Lab 09 A, this run's D06 | Matching response, version 2 and `invoke_agent` → `chat`; input/output **1144/153** | Matching response, version 2 and spans; **1339/273** |
| Lab 03 B / Lab 09 B, original audit request | SDK instructions exactly match the CLI definition; version 1, trace **79b867e1985015fdd02cfe8a47fa9ee7**, **1124/123** tokens | Exact instruction match; version 1, trace **87fad9894be9e9c55f0a9b3d8b5199bc**, **1290/216** tokens |

**Measurement boundary:** 24 new requests in total: two model, four smoke and six dev requests per language.
Each question started a new chat. No B request was repeated for trace lookup, and no candidate, holdout or cloud judge ran.
The times measure the Send click to the rendered response-specific Copy action, including portal/network/rendering overhead.
They are not server-span durations, a human learner pilot, a validation of the 270-minute course, or evidence that one language is faster.
The Korean concept reply simplified a Foundry resource as a workspace; Lab 01's resource/project distinction remains the reference.

**Capture failures retained:** the initial capture helper hit VM, endpoint, response-body and stream-lifecycle limitations.
The original replies and response IDs were retained from the UI, without resending a question.
Four initial requests have no high-resolution timing; none is assigned a fabricated value. All six dev rows per language have measured times.
These capture issues do not replace the earlier CLI audit's retained Group Chat failure.

**Still not run:** File Search—the selected `gpt-6-sol` model showed **Upload files** disabled with a model-unavailability tooltip;
the remote Lab 05 Hosted **Responses** Playground option; new deployments, role changes, default-subscription changes, optional cloud judges
and C modules. A Lab 05's already completed terminal outputs remain in the earlier audit; they were not rerun or relabeled as Hosted results.
No agent definition, prompt, corpus, dataset or grading criterion was changed. No publication, push or cloud deletion occurred.
New conversation/response records and the existing shared services remain subject to the owner's cleanup and cost plan.

**Evidence:** 28 new screenshots, both six-row assessment CSVs, actual instruction snapshots, responses, token counts,
trace metadata and SHA-256 hashes are retained separately from earlier recordings.
[Results and hashes](assets/headless-guide-audit-20260925/results.json) ·
[English assessment](assets/headless-guide-audit-20260925/en/assessment-baseline.csv) ·
[Korean assessment](assets/headless-guide-audit-20260925/ko/assessment-baseline.csv) ·
[English trace](assets/headless-guide-audit-20260925/en-b-trace-detail.png) ·
[Korean trace](assets/headless-guide-audit-20260925/ko-b-trace-detail.png).

<a id="final-guide-closeout-20260925"></a>

## Final closeout: checks after the guide corrections — September 25, 2026

**Order:** English guide fixes → Korean/learner-file alignment → all offline gates → source freeze → English CLI checks →
Korean CLI checks → headless read-back and trace correlation. The freeze is `2026-09-25T07:04:32Z`,
base `b741473` plus working-tree changes, code hash `e92c1be2716a3a65608de16bd217a72439d606594ca2506910881974996b1682`.
Fresh isolated runtime copies reused the existing owned training prefixes and their original ledgers. The source `.env` and Azure CLI
default subscription were unchanged. These were prepared-environment checks, not new learner installation, resource creation or deployment.

| Item | Fresh result, English and Korean |
|---|---|
| Lab 00/02 preflight | Exact `gpt-6-sol` / `2026-09-22`, `Succeeded`; no inference claim from preflight alone |
| Lab 02 | Real model response and structured local-evidence answer; current KRW 150000 limit and actual citations |
| Lab 03 B | Existing `mfv2-a2-0f01-<language>-policy-sdk`, version 1, invoked once per language; saved instructions matched the current CLI definition. Creation was not repeated |
| Lab 04 | No-tool, function and local-MCP commands completed; over-limit approval and historical KRW 120000 results checked. A configured-tool flag alone is not a captured tool-event trace |
| Lab 05 B | Sequential/concurrent/Group Chat output counts 1/4/4; no external actions and pending human review |
| Lab 05 A default terminal | The exact KRW 170000 question ran once per language; both final texts stated KRW 150000, approval before booking and `TRAVEL-2026` + `APPROVAL-01` |
| Lab 06 | Existing local/Search/GA IQ evidence: 6/6/4 documents in each language; actual contents matched the synthetic originals. IQ's three returned fields were `id`, `title`, `content`; separate date fields were not invented |
| Lab 06 answer | New IQ-grounded answer: `needs_approval`, KRW 150000 and both required IDs. Its retrieval hash matched the preceding IQ read in each language |
| Lab 08 | Two local package commands completed; both manifests retain `cloud_deployed: false` |
| Lab 09 | The new English and Korean SDK response IDs matched portal traces and input/output tokens; cleanup inventory read the preserved local ledger and deleted nothing |
| Lab 07/10/11 boundary | No new collection, judge or acceptance; prior evaluation lineage retained, external IQ remains design-only, fresh output/package/trace artifacts checked for handoff |

**Counts:** 32 guide CLI commands, all exit 0; two additional local package commands; 28 fresh JSON outputs.
These are command counts, **not the number of underlying model calls**. MAF workflows/tools and the unchanged SDK retry policy can make
more calls. No driver retry, alternative model, endpoint/provider substitution or fixture fallback was used.
The A inline agents were read back at saved version 2 with exact instruction hashes; their earlier six-case browser assessments were not repeated.
Both agent languages were inspected in the English portal UI in this closeout, not relabeled as a new Korean UI recording.

| New managed-agent call | Response ID | Server trace ID | Input / output tokens |
|---|---|---|---|
| English version 1 | `resp_0131ce4e1fd7c0f2016ab61dcaebb88194acd3fea76cd13212` | `bd829da0e764532e45c5cc134b1585ac` | 1124 / 113 |
| Korean version 1 | `resp_07b8501455f6649a016ab61e946b588195ae3734eb853b81e1` | `4d5f22d02ca12433bbdd18c8f8203d51` | 1290 / 114 |

**Failures and review findings retained:** a separate Foundry MCP `agent_get` read returned **403** because its configured identity lacked
`agents/read`. No role was added and that probe is not marked successful; the guide's preselected subscription-bound CLI and the authenticated
headless portal were checked separately. In Korean concurrent output index 2, the amount and approval conditions are present but policy IDs are
missing. Other participants' citations in the aggregate do not repair that individual answer. Its original JSON is unchanged.
No prompts, corpus, datasets or thresholds were tuned to improve these observations.

**Not newly executed:** agent creation/Save, Search seeding, v1/v2 dev/holdout collections, cloud judges, local/remote Hosted serving,
the remote A Hosted Responses option and the separately gated extension modules. Earlier 6/6·6/6·4/4 runs are not new acceptance for this code hash.
File Search remained disabled after capability loading; an initially enabled-looking control was not counted as support.
No company/Microsoft 365 data, role/default-subscription change, publication, push or cloud deletion.
Actual participant-account readiness and learner teaching-time validation remain owner/pilot work, not claims from an operator's successful run.

[Results and byte-exact output hashes](assets/final-guide-closeout-20260925/results.json) ·
[Per-lab and per-extension status](assets/final-guide-closeout-20260925/module-checks.csv) ·
[Document-pair checks](assets/final-guide-closeout-20260925/document-checks.json) ·
[Guide corrections and local validation](reference/validation.md#final-guide-closeout-20260925).

## Not run with gpt-6-sol

- Lab 03 portal File Search (the September 25 headless check found upload disabled for the selected model)
- Lab 06 IQ Chat preset (gpt-5.6-luna) and hybrid RAG
- Lab 07 feedback/regression step (the baseline had no failure; the no-evidence diagnostic ran instead)
- Lab 07 Hosted model matrix
- Lab 08's default local server, `azd ai agent invoke --local` and the learner's own Hosted deployment (the approved CI release deployed a separate Hosted agent; section 6's workflow server answered one `curl` request in the review refresh check)
- Lab 09 server-side tracing checks for a Hosted agent
- Lab 10 external IQ extensions
- Extension modules other than conversation evaluation, Agent Optimizer, the red-team step of agent safety, release operations, the A2A and Insights checks of the review refresh, and the September 25 memory, routine and Toolbox discovery checks

Earlier `gpt-5.6-luna` recordings and result pages (September 15–17, 2026) were removed from the working tree; they remain only in git history and are not results for this preset.

[Videos](video-summary.md) · [Actions and captures](action-captures.md) · [Chapters](video-chapters.md) · **Actual results** · [Model choice](reference/model-choice.md)
