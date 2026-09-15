# Source execution: action-level run in Sweden Central

**English** | [한국어](ko/live-run.md)

**New run:** [September 15 English-guide recording results](english-recordings.md#actual-results-and-boundaries).
The evidence below remains attributed to the September 14 source execution.

**On September 14, 2026, the guide was rerun and recorded in the new
`rg-mfv2-action-swc-20260914` environment.**
The designated training account was used without changing the default Azure CLI
subscription. Only bundled synthetic data was accessed, not company or Microsoft 365 data.

[Videos](video-summary.md) · [236-action captures](action-captures.md) ·
[Chapters](video-chapters.md) · [Media hashes](assets/live-20260914-action/media.json)

**This is an English translation of that run's evidence, not a new English-language
Azure run.** Source media remains in `docs/assets/live-20260914-action/`.

## Recording

| Surface | Recorded evidence |
|---|---|
| CLI | **131 actions** in an actual Bash PTY: typing, execution, output |
| Portal | **105 actions** in actual `ai.azure.com`: creation, editing, saving, questions, navigation |
| Captures | 1,065 meaningful action-boundary/change events from 1,500 originals, stored as **898 lossless WebP images** |
| CLI video | **14:02**, waits removed, source footage at normal speed |
| Portal video | **9:09**, waits removed, source footage at normal speed |
| Guide-ordered video | **23:35**, all scenes rearranged into Lab 00–11 with twelve title cards |
| Method | Playwright 1.62.0, headless Edge; no sign-in/PIN/MFA footage |

Agent creation via **New agent → Build an agent**, naming/model choice, removing
Web Search, entering instructions/synthetic documents, and saving versions were
captured separately. Every question started a new conversation.
File selection/upload/indexing, failed evaluation rows, and child trace errors are included.

The [combined chapters](video-chapters.md) follow the guide, not a new run.
**All three videos play directly on GitHub without a local server.**
Sign in with an account authorized for this private repository.
[Playback links](video-summary.md#play-now) point to the same current files.
`RUN_TOOLS` is instructor support; use the learner commands in each lab.

### Guide-ordered source video: 23:35

https://github.com/user-attachments/assets/c005e1a6-f577-4d07-b2c3-9a4827750c81

### CLI source video: 14:02

https://github.com/user-attachments/assets/1e2eb2ac-a164-4c67-8d4f-95cec33e2a3a

### Portal source video: 9:09

https://github.com/user-attachments/assets/714599fe-744d-40e2-a945-c4919d0fb0b3

## Environment and models

| Item | Source run |
|---|---|
| Resource group | `rg-mfv2-action-swc-20260914` |
| Foundry account/project | `ai-mfv2-action-swc-20260914` / `mfv2-action-20260914` |
| Search | `srch-mfv2-action-swc-20260914`, Basic, Entra authentication |
| Observability | Same-region Application Insights/Log Analytics, 30-day retention, 1 GB daily cap |
| Answer model | `gpt-5.6-luna`, `2026-07-09`, Data Zone Standard 100K TPM |
| Separate judge | `gpt-5.6-luna-judge`, same model version, Data Zone Standard 50K TPM |
| Version policy | `NoAutoUpgrade` on both; no model/endpoint fallback |

Data Zone Standard processes inference in the **EU data zone**.
Sweden Central resource placement is not a single-datacenter inference guarantee.
Target and judge share an underlying model, so this is not independent cross-model validation.

## Actual source-run results

| Path | Evidence |
|---|---|
| Model | SDK/portal Luna calls; unsupported lodging amount withheld before policies were supplied |
| A. Portal Prompt Agent | `mfv2-action-20260914-portal` **v3**, inline sources; four introductory and six dev questions, each in a fresh conversation |
| SDK Prompt Agent | `mfv2-action-20260914-policy` **v1**, current/historical/approval/insufficient-evidence questions |
| MAF | Single/function/local MCP; A's current/historical sequential runs; B's sequential/concurrent/Group Chat |
| Search/IQ | Six synthetic documents, new index/source/base, actual GA `2026-04-01` retrieval; rechecked after portal observation |
| File Search | `mfv2-action-20260914-files` **v2**, no inline evidence; six Completed files, stored bytes matched all six originals |
| v1/v2 dev | **6/6 / 6/6**, fixed local retrieval, no collection errors |
| Teaching holdout | Final frozen-candidate procedure **4/4**; already-exposed teaching set, not a fresh unseen set |
| Native judge | Groundedness **6/6**, relevance **5/6**; all six cases retained in each denominator |
| Hosted | `mfv2-action-20260914-hosted` **v1**, actual local/remote responses and managed identity |
| Separate Hosted evaluation | Six fresh remote responses, generative rubric **6/6**; query-only target inputs verified in all raw outputs |
| Lab 10 | Synthetic routing design; no Fabric/Work IQ/Microsoft 365 connection |

Portal dev responses were reviewed for current KRW 150,000, historical KRW 120,000,
advance approval, meals KRW 30,000, international withholding, and refusal to ignore
policy. This was assistant review, not human production approval or statistical
quality assurance. Group Chat stopped at three rounds and performed no booking/approval/payment.

## Failures and limitations retained

- **D05 native relevance = 2:** correct withholding of an unsupported international
  amount was penalized for not providing an amount. Preserve the metric and a pending
  dev review rather than rewriting the score to match business criteria.
- **File Search source UI:** citation chips/numbers did not open a preview/download.
  This was not marked successful. The same stored files were separately read via SDK
  and compared to all six originals; neither answers nor retrieval providers changed.
- **IQ portal editor:** an Active GA base still required a separate chat-completions
  model. No model was added and no Preview configuration was saved. GA retrieval still worked.
- **Hosted evaluator version:** generated YAML contained v1, but the actual run's version
  selector was empty. Catalog v1 was retained without retroactively claiming explicit pinning.
- **Small evaluation:** both prompts passed 6/6; no superiority claim.
  Holdout was not used for instruction development or regression harvesting.

Prerelease, serialization, and non-durable-execution warnings and capture-helper retries
were recorded separately. No missing/error rows were removed from denominators.

## Actual Hosted trace and logs

The CLI's Trace ID **`e72dc58132dbc461e5fa381c67da3ed9`** was located in the same agent's
Traces view. It showed **20 spans, two chat calls, one tool call, about 7.2 seconds,
root Completed**.

The displayed **two errors** were initial GET 404s for a new state store and conversation
item. Subsequent creation/update, model, and `lookup_policy` calls succeeded.
Overall completion and zero child errors are different claims.

`azd ai agent monitor` was run **immediately after invocation** on the same Running
session. Logs showed two model HTTP 200s, successful tool execution, and final
Responses HTTP 200. Resilient tasks were disabled; durable crash recovery was not verified.

## Cleanup and reproduction

Both new Hosted sessions were explicitly stopped even after automatic idle, then
reread as idle. Local server/capture processes were stopped.
The group was retained for review, so **Search, File Search storage, logs, and future
model calls can still incur costs**.

Execution used a standalone folder outside other azd projects. Personal raw responses,
evaluators, settings, and cleanup evidence remain Git-excluded.
[Validation](reference/validation.md) and the [action index](action-captures.md)
separate exactly what was verified.
