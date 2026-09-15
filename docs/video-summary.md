# September 14 source workshop videos

**English** | [한국어](ko/video-summary.md)

**Looking for the new English-guide videos?** [Play the September 15 recordings](english-recordings.md):
13:09 combined, 5:15 CLI, and 4:45 portal. The archive below remains the Korean-content source run.

[Learning paths](paths.md) · [12 chapters](video-chapters.md) ·
[236 actions and screenshots](action-captures.md) · [Results and limits](live-run.md)

**Every September 14, 2026 source recording has a direct playback link.**
The guide-ordered version is **23:35**, CLI **14:02**, and portal **9:09**.
Long waits were removed while retaining typing, creation, configuration, saving,
questions, responses, and error inspection.

**Language:** these are the original Korean-content recordings, described in English.
They are not a newly recorded English Azure run. See [the language contract](reference/languages.md).

## Play now

**Click a link or the embedded player's play button. No download or local server is required.**
This is a private repository: **sign in with a GitHub account that can access it**.
That sign-in is separate from Azure.

**[Play combined walkthrough](https://github.com/user-attachments/assets/c005e1a6-f577-4d07-b2c3-9a4827750c81)** ·
**[Play CLI](https://github.com/user-attachments/assets/1e2eb2ac-a164-4c67-8d4f-95cec33e2a3a)** ·
**[Play portal](https://github.com/user-attachments/assets/714599fe-744d-40e2-a945-c4919d0fb0b3)**

### Combined walkthrough: 23:35

https://github.com/user-attachments/assets/c005e1a6-f577-4d07-b2c3-9a4827750c81

### CLI execution: 14:02

https://github.com/user-attachments/assets/1e2eb2ac-a164-4c67-8d4f-95cec33e2a3a

### Foundry portal: 9:09

https://github.com/user-attachments/assets/714599fe-744d-40e2-a945-c4919d0fb0b3

All three attachments match the repository's corresponding current source-video
files byte-for-byte. They do not link to older or unedited recordings.

## Guide-ordered walkthrough

CLI and portal footage is **interleaved in Lab 00–11 order**, rather than placing all
CLI footage before all portal footage. Actions and results for a lab appear together.

Time links in the [chapter table](video-chapters.md) and [action index](action-captures.md)
open the **matching position in the GitHub video**. No command is required;
press play if it opens paused.

All scenes from the two individual edits and **all 236 actions** are retained at
original speed. Twelve chapter cards add 24 seconds. This is an **educational reorder**,
not a new Azure execution or the original wall-clock sequence. It assumes an
instructor-prepared environment. File Search, SDK, and Hosted agent versions and
their evaluation criteria remain separate.

## Optional: offline local playback

Only use this if the repository is already on your computer and you want local playback.
**None of the GitHub links above require this command.**

```bash
python scripts/play_recordings.py --edition ko
```

Open the printed address. `--edition ko` explicitly selects this source set; without it,
the new English-guide set is selected. The combined source video is selected and the
chapter selector navigates among labs. Stop with `Ctrl+C`; use `--port 8766` if needed.
The local player defaults to English. Its **한국어** link switches the interface while
preserving the selected video and playback position; it does not translate the footage.
The local player performs no Azure calls, sign-in, or uploads.

## What is included?

CLI covers new-group/model preparation, installation, offline/live distinctions,
SDK/MAF/MCP, three workflows, Search/IQ, complete dev/native/Hosted evaluations,
final acceptance, and session cleanup.
Portal covers agent creation, model choice, instructions/documents, version saving,
new conversations, File Search upload/indexing, failed evaluation rows, and actual trace errors.

The edit preserves boundaries for **131 CLI actions and 105 portal actions**.
Of 1,500 original capture events, 1,065 meaningful events are retained using
**898 lossless WebP files** with shared identical images.

## Editing and interpretation

- Body footage comes from actual source-video segments. Chapter cards are identified separately.
  Answers, scores, and failures were not changed.
- Individual edits preserve each source's order. The combined edit follows the guide.
  The local Hosted terminals are interleaved in actual time within that section.
- Video duration is not model latency or deployment time. Pause to read commands/results.
- `RUN_TOOLS` is instructor recording support; execute commands in the labs instead.
- Sign-in, PIN, and MFA were not recorded. Review resource identifiers before external sharing.

[Files/hashes](assets/live-20260914-action/media.json) ·
[Source/edit frames](assets/live-20260914-action/edit-timeline.json) ·
[Combined frames/chapters](assets/live-20260914-action/combined-timeline.json) ·
[Playback publication](assets/live-20260914-action/github-playback.json)
