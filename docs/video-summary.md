# gpt-6-sol workshop recordings — September 24, 2026

**English** | [한국어](ko/video-summary.md)

**New English recording — September 24, 2026.** The main A (portal) and B (CLI) steps of Labs 00–09 and 11, plus the optional Foundry evaluation steps (portal evaluation, trace evaluation, cloud judges with the business rubric and **Compare runs**, MAF tool-call scoring), were executed in the Sweden Central training project with `gpt-6-sol` / `2026-09-22`; every judge used the separate `gpt-6-sol-judge` deployment. English prompts, policies, evaluation data and browser sessions are independent of the Korean recording.

| Video | Duration | File |
|---|---:|---|
| Labs 00–09 and 11 in guide order | 06:29 | [guide-ordered.mp4](assets/g6sol-20260924-en/guide-ordered.mp4) |
| B · CLI execution | 03:11 | [cli-edited.mp4](assets/g6sol-20260924-en/cli-edited.mp4) |
| A · Foundry portal | 02:55 | [portal-edited.mp4](assets/g6sol-20260924-en/portal-edited.mp4) |

**98 actions and 293 lossless captures.** Videos join actual source intervals at 1× speed with only waits shortened; chapter cards are labeled and are not application screens. Every one of the 262 joined segments was compared with its source frame (minimum SSIM 0.9922).

**Local playback and chapter seeks are verified; the videos were not uploaded to GitHub.** After downloading the repository, play only the verified files on localhost:

```bash
python scripts/play_recordings.py --edition en
```

## What was recorded

- **Lab 00:** offline doctor, v1/v2 fixtures (not model responses), virtual environment, `.env` from the setup card, read-only preflight.
- **Lab 01–02:** project versus account endpoint, deployment inventory, two Playground answers with Web search removed, the first SDK request and a validated structured answer.
- **Lab 03:** portal agent (saved version 2) answering D01/D02/D03/D05; optional SDK prompt agent version 1.
- **Lab 04–06:** MAF without tools, function tool and local MCP; optional `maf-evaluate` (tool_call_accuracy 6/6, relevance 6/6); sequential, concurrent and bounded Group Chat workflows; local retrieval, an owned Search index, a GA Foundry IQ knowledge base and an IQ-grounded answer.
- **Lab 07:** dev baseline v1 6/6, candidate v2 6/6, the frozen candidate once on holdout 4/4, acceptance `ready-for-human-review`, the no-evidence diagnostic 0/6 with 0 errors; cloud judge groundedness 6/6 and relevance 5/6 (failed: D05); business rubric agreement 6/6 and 6/6 with **Compare runs** (the first baseline attempt came back without `business_rubric` and was retried once with `--retry-failed`); portal D01–D06 and a portal evaluation (Relevance 6/6, Coherence 6/6, TaskAdherence 0/6), repeated with agent Version 2 because the first run kept the preselected Version 1.
- **Lab 08–11:** Hosted bundle packaging only, agent Details/Traces/Monitor tabs, a trace evaluation of the recorded conversations (Relevance 10/10, Coherence 10/10, TaskAdherence 10/10), the owned-asset cleanup inventory (deletes nothing) and the handoff summary.

## Not recorded in this edition

Lab 10, the optional IQ Chat preset (`gpt-5.6-luna`; Search did not accept a GPT-6 model), Lab 03 portal File Search, Lab 06 hybrid RAG, Lab 08 local/remote Hosted runs, Lab 09 recurring evaluation, the advanced C paths and the extension modules are **not in this recording**; the Lab 09 B server-side trace search is in the [September 25 supplement](#review-refresh-supplement). The conversation evaluation module, the recurring evaluation, Agent Optimizer, cloud red teaming and the CI release ran separately on September 23 ([results](live-run.md#previously-not-run-items--september-23-2026); conversation evaluation: [validation](reference/validation.md#foundry-evaluation-additions)). Earlier recordings were removed and are not evidence for this edition.

Authentication, password and MFA entry are not recorded. A recorded exit code is not a quality score, and none of these results is a production approval. Use your own resource names, versions and results.

<a id="review-refresh-supplement"></a>

## Review-refresh supplement — September 25, 2026

**Two short English clips for the core steps the 2026-09-24 review added.** Same project, `gpt-6-sol` / `2026-09-22`, source commit `f990af3`; one new agent version and one model call. The September 24 videos stay the reference for unchanged steps.

**Later guide change (2026-09-25):** [Lab 03 B's invocation block](labs/03-prompt-agent.md#sdk-invoke-recording-scope)
now asks for both the saved name and version and rejects empty values. These clips show the earlier prompt, not that offline-checked resume change.

| Clip | Duration | File |
|---|---:|---|
| B · Lab 03 create and invoke with `--output` (real zsh terminal) | 01:02 | [en-terminal.mp4](assets/review-refresh-20260925/en-terminal.mp4) |
| Lab 03 B portal check · Lab 09 B trace search by `response_id` | 01:13 | [en-portal.mp4](assets/review-refresh-20260925/en-portal.mp4) |

Both run at 1×; the terminal clip trims only idle time before and after the actions, and the portal clip is uncut. The six lossless screenshots sit in [Lab 03 B](labs/03-prompt-agent.md#path-b) and [Lab 09 B](labs/09-operations.md#path-b).
[captures.json](assets/review-refresh-20260925/captures.json) records hashes, IDs and checks. One earlier English attempt was discarded because its terminal showed a local home-directory path; nothing from it is published and its agent was deleted on September 25.

**Videos** · [Actions and captures](action-captures.md) · [Chapters](video-chapters.md) · [Actual results](live-run.md) · [Model choice](reference/model-choice.md)
