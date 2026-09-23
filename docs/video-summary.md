# gpt-6-sol workshop recordings — September 23, 2026

**English** | [한국어](ko/video-summary.md)

**New English recording — September 23, 2026.** The main A (portal) and B (CLI) steps of Labs 00–09 and 11 were executed in a new Sweden Central training project with `gpt-6-sol` / `2026-09-22`; the optional cloud judge used the separate `gpt-6-sol-judge` deployment. English prompts, policies, evaluation data and browser sessions are independent of the Korean recording.

| Video | Duration | File |
|---|---:|---|
| Labs 00–11 in guide order | 04:36 | [guide-ordered.mp4](assets/g6sol-20260923-en/guide-ordered.mp4) |
| B · CLI execution | 02:30 | [cli-edited.mp4](assets/g6sol-20260923-en/cli-edited.mp4) |
| A · Foundry portal | 01:43 | [portal-edited.mp4](assets/g6sol-20260923-en/portal-edited.mp4) |

**69 actions and 207 lossless captures.** Videos join actual source intervals at 1× speed with only waits shortened; chapter cards are labeled and are not application screens. Every one of the 175 joined segments was compared with its source frame (minimum SSIM 0.9925).

**Local playback and chapter seeks are verified; the videos were not uploaded to GitHub.** After downloading the repository, play only the verified files on localhost:

```bash
python scripts/play_recordings.py --edition en
```

## What was recorded

- **Lab 00:** offline doctor, v1/v2 fixtures (not model responses), virtual environment, `.env` from the setup card, read-only preflight.
- **Lab 01–02:** project versus account endpoint, deployment inventory, two Playground answers with Web search removed, the first SDK request and a validated structured answer.
- **Lab 03:** portal agent (saved version 2) answering D01/D02/D03/D05; optional SDK prompt agent version 1.
- **Lab 04–06:** MAF without tools, function tool and local MCP; sequential, concurrent and bounded Group Chat workflows; local retrieval, an owned Search index, a GA Foundry IQ knowledge base and an IQ-grounded answer.
- **Lab 07:** dev baseline v1 6/6, candidate v2 6/6, the frozen candidate once on holdout 4/4, acceptance `ready-for-human-review`, optional cloud judge groundedness 6/6 and relevance 5/6 (D05); portal D01–D06.
- **Lab 08–11:** Hosted bundle packaging only, agent Details/Traces/Monitor tabs, the owned-asset cleanup inventory (deletes nothing) and the handoff summary.

## Not recorded in this edition

Lab 10, the optional IQ Chat preset (`gpt-5.6-luna`; Search did not accept a GPT-6 model), Lab 03 portal File Search, Lab 06 hybrid RAG, Lab 08 local/remote Hosted runs, Lab 09 server-side tracing and continuous evaluation, the advanced C paths and the extension modules were **not re-run with `gpt-6-sol`**. The earlier `gpt-5.6-luna` recordings were removed and are not evidence for this preset.

Authentication, password and MFA entry are not recorded. A recorded exit code is not a quality score, and none of these results is a production approval. Use your own resource names, versions and results.

[Videos](video-summary.md) · [Actions and captures](action-captures.md) · [Chapters](video-chapters.md) · [Actual results](live-run.md) · [Model choice](reference/model-choice.md)
