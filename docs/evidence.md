# Execution evidence and recordings

**English** | [한국어](ko/evidence.md)

**Use this hub to find what was actually run, recorded, validated, or left unverified.** Older recordings do not prove new 2026-09-24 additions.

## Current evidence links

| Need | Link |
|---|---|
| Final corrections and post-edit, item-by-item checks | [Final closeout](reference/validation.md#final-guide-closeout-20260925) · [fresh execution](live-run.md#final-guide-closeout-20260925) |
| Actual live results and limitations | [live-run.md](live-run.md) |
| September 25 headless responses, timings and portal trace correlation | [Headless follow-up](live-run.md#headless-guide-audit-20260925) |
| Recording summary | [video-summary.md](video-summary.md) |
| Action/capture index | [action-captures.md](action-captures.md) |
| Capability and module evidence | [coverage.md](coverage.md) |
| Validation boundaries and local checks | [reference/validation.md](reference/validation.md) |

## September 15 foundation run box

**Historical foundation: September 15, 2026, with the earlier preset.** This is not current `gpt-6-sol` execution evidence.
Follow the current [beginner or practitioner guide](paths.md), not an older recording. Read [how to use the screenshots](labs/00-start.md#how-to-read-this-guide) first.

## Headless follow-up — 2026-09-25

After authentication was resolved, Playwright MCP headless verified the existing A agents and new model/smoke/dev replies,
then correlated A's new and B's original response IDs and tokens with portal traces, independently in both languages.
The 24 requests, 28 screenshots, six-row assessments and exact hashes are [separate live evidence](live-run.md#headless-guide-audit-20260925),
not a new video or a new agent-creation run. Send-to-render timings do not establish learner completion times.
File Search upload was unavailable for the selected `gpt-6-sol` model; the remote Lab 05 Hosted Responses option remains unverified.

## September 24 `gpt-6-sol` recordings

English videos: [summary](video-summary.md) · [action/capture index](action-captures.md) · [chapters](video-chapters.md) · [actual results and limitations](live-run.md).
The English set contains **98 actions, 293 lossless captures, and three videos**: **6:29 in guide order**, **3:11 CLI** and **2:55 portal**.
It covers the main A (portal) and B (CLI) steps of Labs 00–09 and 11 and the optional Foundry evaluation steps with `gpt-6-sol` / `2026-09-22` in the Sweden Central training project.
Failed attempts stay in the recording next to their retries. Local playback and chapter seeks are verified; the videos were not uploaded to GitHub.
Play them locally with `python scripts/play_recordings.py --edition en`. Earlier recordings were removed.

Korean recordings are independent: [Korean videos](ko/video-summary.md). The Korean set contains **91 actions, 272 captures, and three videos**: **6:03 in guide order**, **2:57 CLI** and **2:43 portal**. Playback and chapter seeks were verified independently.

## Run and language metadata

English uses separate English instructions, synthetic policies, dev/calibration/holdout datasets and fixtures.
Select them explicitly with `--language en`; original Korean files remain unchanged.
The [language contract](reference/languages.md) and [versioned data bundle](../data/README.md) preserve language-specific lineage.

## Additional modules and their evidence

**September 16 English-first expansion:** [A — Beginner](paths/a-beginner.md) · [B — Implementation](paths/b-practitioner.md) · [C — Advanced modules](paths/c-advanced.md).
Use the [capability/evidence record](coverage.md) to distinguish existing labs, executable modules and actual Azure verification.
The extension modules were exercised on September 16, 2026 with the earlier `gpt-5.6-luna` preset, and those recordings were removed.
With `gpt-6-sol` and without recording, conversation evaluation, Agent Optimizer, the red-team step of agent safety and release operations were re-run on September 23, A2A and one Insights scan on September 24, and conversation evaluation, memory, one routine dispatch and the Toolbox up to discovery on September 25. The [coverage record](coverage.md) shows each module's latest evidence.

## End-to-end guide run — 2026-09-25

Both core routes ran as written in English and Korean from fresh GitHub copies: route B's core blocks in one terminal, route A in the portal.
Every block exited 0 and D01–D06 met their criteria. The guide corrections, including the changed **Create an agent** dialog, are itemized in the run record.
See [the run record](live-run.md#end-to-end-20260925).

## Review refresh live verification — 2026-09-24

The refreshed SDK pins, the core B route with Lab 03 B, the Lab 09 trace lookup, the SDK recipes, A2A with typed requests and one Insights scan
were run against Azure on the evening of 2026-09-24 in the same training project; see [live results](live-run.md#review-refresh-live-verification).
The September 24 recordings above predate these additions and are not evidence for them.

**Supplement recorded 2026-09-25:** Lab 03 B create/invoke with `--output`, the Lab 03 B portal check and the Lab 09 B trace search by `response_id`, in English and Korean.
Twelve lossless screenshots and four short clips: [summary](video-summary.md#review-refresh-supplement) · [captures](action-captures.md#review-refresh-supplement) · [captures.json](assets/review-refresh-20260925/captures.json).
The other additions have no new recording. Still not run, or waiting for owner approval: a remote deployment for the browser Lab 05 option, a cross-provider model comparison, a new Agent Optimizer run (needs a supported optimizer deployment), the Toolbox query, Tool Search and Skills (need a Search role) and the Dev Pack; see [what each needs](live-run.md#not-run-feasibility).
