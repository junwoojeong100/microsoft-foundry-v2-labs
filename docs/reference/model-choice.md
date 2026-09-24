# Model choice: why this edition uses gpt-6-sol — September 23, 2026

**English** | [한국어](../ko/reference/model-choice.md)

**The answer preset is `gpt-6-sol`, model version `2026-09-22`; the separate evaluation judge is `gpt-6-sol-judge`.**
These are dated observations from the dedicated Sweden Central training project, not a support guarantee.
Check again immediately before class.

## What was actually checked

| Lab path | `gpt-6-sol` | `gpt-6-astra` | `gpt-6-luna` |
|---|---|---|---|
| Project Responses: `model`, `answer`, `collect` (Labs 02, 06, 07) | ✅ | ✅ | ❌ HTTP 500 |
| Portal Prompt Agent chat (Labs 03, 07 A) | ✅ | ✅ | ❌ `reasoning.effort` is not supported |
| SDK Prompt Agent invocation | ✅ | ✅ | ❌ HTTP 500 |
| MAF function tool and local MCP (Lab 04) | ✅ | ✅ | ❌ HTTP 500 |
| Six dev questions, business checks (`v2`, local retrieval) | 6/6, median 2.1 s | 6/6, median 4.3 s | not run |
| Data Zone Standard in Sweden Central | ✅ | ❌ Global Standard only | ✅ |
| Published price per 1M tokens (input / output) | not yet published | USD 10 / 50 | not yet published |
| Recorded main A/B steps, Labs 00–09 and 11 ([recordings](../video-summary.md)) | ✅ English and Korean | not run | not run |

`gpt-6-luna` deployed successfully and answered in the portal model Playground, but the project agent path returned
HTTP 500 from 23:52 to 01:53 UTC in repeated checks, with Data Zone and Global Standard deployments and in a second region.
A `gpt-6-astra` deployment in the same project worked, so the failure was specific to `gpt-6-luna` on that date.
`gpt-6-astra` works but costs more, is slower in this check and is not offered as Data Zone Standard in Sweden Central.

**Choice:** `gpt-6-sol` passed every checked path above, keeps EU Data Zone processing and needs no quota-tier request.
File Search, hybrid RAG, a learner-run Hosted deployment and most extension modules were not re-run with it; the approved CI release, conversation evaluation, Agent Optimizer, the red-team step of agent safety and release operations were re-run or verified with it ([results](../live-run.md#previously-not-run-items--september-23-2026)).
Confirm its published price before class. Do not replace it with another model after an error; stop and record the error.

## Two fixed exceptions

- **IQ Chat stays on `gpt-5.6-luna` / `2026-07-09`.** Search knowledge bases accepted no GPT-6 model on September 23
  (`Unsupported model type in Knowledge Base Model Configuration`). Prepare that separate deployment only for the optional branch.
  [IQ Chat preset](iq-model-identity.md).
- **Portal side effect:** opening the first portal agent also created a `text-embedding-3-large` Standard deployment.
  The labs do not use it; list it with your owned assets in Lab 09.

`gpt-6-sol` reports reasoning tokens even for short answers; they count toward output usage.

[Setup](../setup.md) · [Troubleshooting](troubleshooting.md) · [Versions](versions.md) · [Validation](validation.md)
