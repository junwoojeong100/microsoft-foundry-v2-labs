# New English-guide recordings

**English** | [한국어](ko/english-recordings.md)

**Recorded September 15, 2026. Combined 13:09 · CLI 5:15 · portal 4:45.**

These are **new recordings**, not translated title cards over the old videos: 57 actual CLI actions, 88 actual portal actions, and 89 local English-guide views. The **234 actions** retain **819 capture events as 537 lossless screenshots**.

English documentation was published first in `26d2e80`. The new footage uses that edition and the existing Sweden Central environment. **Policy prompts, questions, and datasets remain Korean** to preserve lineage; this is not a new English-language quality evaluation.

[All new captures](english-captures.md) · [Learning paths](paths.md) · [Language contract](reference/languages.md)

## Play now

Click a link or an embedded player's play button. **No download or local command is needed.** Sign in with a GitHub account authorized for this private repository.

### Combined walkthrough — 13:09

▶ [Combined walkthrough — 13:09](https://github.com/user-attachments/assets/082ede4b-d363-474c-ad47-598b20f593e9)

https://github.com/user-attachments/assets/082ede4b-d363-474c-ad47-598b20f593e9

### Actual CLI execution — 5:15

▶ [Actual CLI execution — 5:15](https://github.com/user-attachments/assets/e29e5b98-b7c9-4e3f-825d-be56adf4c6a2)

https://github.com/user-attachments/assets/e29e5b98-b7c9-4e3f-825d-be56adf4c6a2

### Actual English-UI portal — 4:45

▶ [Actual English-UI portal — 4:45](https://github.com/user-attachments/assets/ef769e93-598a-458a-a2e3-fc21f6a788c2)

https://github.com/user-attachments/assets/ef769e93-598a-458a-a2e3-fc21f6a788c2

## Chapters

The combined video interleaves guide views, portal actions, and CLI execution by **Lab 00–11**. It is a learning-order edit, not wall-clock order or another Azure run. Chapter cards are separate; body footage remains at normal speed.

| Start | Lab | Actions |
|---|---|---:|
| ▶ [00:00](https://github.com/user-attachments/assets/082ede4b-d363-474c-ad47-598b20f593e9#t=0.00) | [Lab 00. Getting started](labs/00-start.md) | 31 |
| ▶ [01:20](https://github.com/user-attachments/assets/082ede4b-d363-474c-ad47-598b20f593e9#t=80.12) | [Lab 01. Foundry and projects](labs/01-foundry.md) | 10 |
| ▶ [01:46](https://github.com/user-attachments/assets/082ede4b-d363-474c-ad47-598b20f593e9#t=106.84) | [Lab 02. Models and actual requests](labs/02-models.md) | 21 |
| ▶ [03:00](https://github.com/user-attachments/assets/082ede4b-d363-474c-ad47-598b20f593e9#t=180.84) | [Lab 03. Agents, evidence, and File Search](labs/03-prompt-agent.md) | 44 |
| ▶ [05:21](https://github.com/user-attachments/assets/082ede4b-d363-474c-ad47-598b20f593e9#t=321.76) | [Lab 04. MAF functions and MCP](labs/04-agents-tools.md) | 10 |
| ▶ [05:59](https://github.com/user-attachments/assets/082ede4b-d363-474c-ad47-598b20f593e9#t=359.16) | [Lab 05. MAF workflows](labs/05-workflows.md) | 11 |
| ▶ [06:39](https://github.com/user-attachments/assets/082ede4b-d363-474c-ad47-598b20f593e9#t=399.92) | [Lab 06. Search and Foundry IQ](labs/06-knowledge.md) | 15 |
| ▶ [07:30](https://github.com/user-attachments/assets/082ede4b-d363-474c-ad47-598b20f593e9#t=450.52) | [Lab 07. Evaluation and failure review](labs/07-evaluation.md) | 39 |
| ▶ [09:43](https://github.com/user-attachments/assets/082ede4b-d363-474c-ad47-598b20f593e9#t=583.28) | [Lab 08. Local and Hosted agents](labs/08-hosted.md) | 19 |
| ▶ [11:22](https://github.com/user-attachments/assets/082ede4b-d363-474c-ad47-598b20f593e9#t=682.00) | [Lab 09. Traces, operations, and cleanup](labs/09-operations.md) | 20 |
| ▶ [12:36](https://github.com/user-attachments/assets/082ede4b-d363-474c-ad47-598b20f593e9#t=756.16) | [Lab 10. IQ extension boundaries](labs/10-iq-extensions.md) | 8 |
| ▶ [12:52](https://github.com/user-attachments/assets/082ede4b-d363-474c-ad47-598b20f593e9#t=772.60) | [Lab 11. Final acceptance](labs/11-capstone.md) | 6 |

## Actual results and boundaries

| Path | September 15 evidence |
|---|---|
| Canonical dev v1 / v2 | **5/6 / 6/6**, zero collection errors. v1 D06 failed the `decision` check; the original row and pending review remain. |
| Final teaching holdout | **4/4** after freezing v2. Already-exposed teaching data, not a fresh unseen set or prompt-development input. |
| Portal v3 | Four introductory questions and all six dev questions. An introductory **HTTP 503** is retained; a separate retry of the same agent/version succeeded. |
| File Search v2 | Existing six files are Completed; fresh answer has file citations. No new upload/deletion. Citation control still did not open a preview. |
| Local Hosted | Actual readiness is `{"status":"healthy"}` with HTTP 200. Initial missing-azd-context failure and corrected local invocation are both recorded. |
| Existing remote Hosted v1 | Fresh response and exact trace **94b4e5f61dc7e93016fc53a57ffa9f78**: 15 visible spans, one chat span, one tool span, root OK. A smoke call is not a Hosted quality evaluation. |
| Native / Hosted evaluation reports | **Historical September 14 reports**, viewed now; no new paid judge job. Their 6/6, 5/6, and rubric 6/6 are not September 15 scores. |
| Cleanup / scope | Owned new session stopped, local server stopped, default subscription unchanged. No resource provisioning, deployment, role changes, company/Fabric/M365 access. Existing services may still incur costs. |

The local SDK emitted an IMDS metadata-detection timeout while outside Azure; the local server and actual model response still completed. The readiness wording was corrected in both guides and its documentation segment was rerecorded. No endpoint, model, retrieval provider, or fixture was substituted.

The first portal browser context reset after its footage and 250 screenshots were saved. Those **original files were retained**, and capture positions were recovered by matching actual video frames near filesystem timestamps. They are not claimed to be the lost original event ledger. Part two persisted each event as it happened. The edit compares every retained footage segment with its source (minimum midpoint SSIM **0.988842**) and verifies full decoding; screenshots are pixel-lossless.

## Optional local playback

English-guide recordings are the default; `--edition ko` explicitly selects the older Korean source set. The UI language switch preserves video/time and does not switch the recording set.

```bash
python scripts/play_recordings.py
```

[Media hashes](assets/english-20260915/media.json) · [Edit/frame lineage](assets/english-20260915/edit-timeline.json) · [Run lineage](assets/english-20260915/live-results.json) · [GitHub playback](assets/english-20260915/github-playback.json)

[Original September 14 recordings](video-summary.md)
