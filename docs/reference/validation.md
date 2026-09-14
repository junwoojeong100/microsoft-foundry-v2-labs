# Validation record for this edition

**English** | [한국어](../ko/reference/validation.md)

**Source Azure run: September 14, 2026, new Sweden Central environment and action-level recording.**

[Actual execution](../live-run.md) · [Videos](../video-summary.md) ·
[236-action evidence](../action-captures.md)

The source run started from `8d094723d651d011592578a76609695c86570ba7` in an
independent folder. These are that run's direct observations, not upstream results.
**English documentation added September 15 does not reset these evidence dates
or constitute another Azure run.**

## Actual Azure evidence: September 14

| Area | Result |
|---|---|
| Environment | `rg-mfv2-action-swc-20260914`, regional resources in Sweden Central, default subscription unchanged |
| Model | Luna `2026-07-09`, target 100K / separate judge 50K, Data Zone Standard, NoAutoUpgrade |
| Portal/SDK | Browser agent v3: four intro/six dev questions; separate SDK agent v1 |
| MAF | Single/function/MCP; A's two sequential cases; B's three patterns |
| Search/IQ | Six synthetic documents and actual GA retrieval, rechecked after portal observation |
| File Search | Separate v2, all six Completed, stored bytes identical to originals |
| Dev | v1 6/6, v2 6/6; same local retrieval/model/data/output limit |
| Native | Groundedness 6/6, relevance 5/6; original D05 score 2/reason preserved |
| Teaching holdout | Final frozen-candidate procedure 4/4; not a new unseen set |
| Hosted | New code deployment v1; actual local/remote answers; model/tool success logs |
| Hosted evaluation | Six fresh remote responses, all query-only inputs checked, rubric 6/6 |
| Trace | Same ID `e72dc58132dbc461e5fa381c67da3ed9`, 20 spans, two chat/one tool, root Completed |
| Child errors | Two initial state store/item GET 404s retained; later writes/final Responses succeeded |
| Cleanup | Both owned sessions stopped and idle, local server stopped, existing Azure environments preserved |

Natural-language review, deterministic business checks, native judges, and Hosted
rubrics are different criteria. Missing/errors remain in denominators; unmeasured
latency is not zero. The actual Hosted evaluator version selector was empty despite
catalog v1 lookup. No retroactive explicit-version claim is made.
Human production approval, durable crash recovery, and real Fabric/Work IQ/M365
connections were not performed.

## Guide corrections from that run

New agents can re-add Web Search; remove it before questions.
The guide names **New agent → Build an agent**, distinguishes **Save** from **Publish**,
and documents **Leave without saving?**.
The 2001-character check uses a short generator to avoid terminal truncation.
File Search citation controls did not open sources, so the same stored bytes were
checked separately. The IQ portal's chat-model requirement did not change GA settings.
Hosted logs were read immediately, and successful roots were distinguished from child 404s.

## Source media validation

CLI is **841.52 s**, portal **549.44 s**, edited from real video segments at normal speed.
Each source's order was retained. These are not screenshot slideshows.

| Check | Evidence |
|---|---|
| Action boundaries | 131 CLI + 105 portal actions linked to images/video intervals |
| Captures | 1,500 originals → 1,065 retained events → 898 lossless WebP files |
| Image equivalence | Decoded PNG/WebP RGB pixels matched |
| Video integrity | Full-frame FFmpeg decoding |
| Source correspondence | Start/middle/end of 227 segments: **681 comparisons** |
| Minimum SSIM | CLI **0.984467**, portal **0.991442** |
| Authentication | No sign-in/PIN/MFA recording |

[Frame correspondence](../assets/live-20260914-action/edit-timeline.json) ·
[Hashes](../assets/live-20260914-action/media.json)

Repository publication and GitHub player attachment upload are separate.
All three final files were hash-checked and uploaded as attachments scoped to the same
private repository. Guides store canonical attachment URLs, not signed CDN URLs/tokens.

The source verification rendered `video-summary.md` and `live-run.md` through the
authenticated GitHub Markdown API, yielding three players each. CDN downloads matched
file lengths/SHA-256. Headless Edge checked start/50%/90% across six players:
**18 playback/seek checks**. No local or mock videos replaced remote media.
Direct links returned an authenticated redirect and ultimately HTTP 200 `video/mp4`.
Tokens were not forwarded to redirect destinations.

All **12 chapter** positions survived authenticated redirects with `#t=`.
All **236 action and 12 chapter** links retained timestamps after Markdown rendering.
The `▶` prefix prevents GitHub from replacing timestamp-table links with duplicate
players that lose their position.

## Illustrated guides

The September 14 update expanded direct image references in twelve labs from 18 to
**77**, plus two instructor references: **79 uses of 77 distinct captures**.
Every image explains controls, verification, and interpretation beside its step.
Optional File Search images remain in expandable details.

Original media/lineage and executable blocks were unchanged in that update.
A local headless Edge preview loaded all 79 images across thirteen guides and expanded
File Search. That check made no Azure calls/uploads.

## Guide-ordered video

The **1,414.96 s (23:35)** combined video rearranges existing CLI/portal edits into
Lab 00–11. It is not a new Azure execution or original wall-clock order.

- All **34,774 input frames** occur exactly once.
- All **236 actions** map to combined intervals.
- Twelve separate chapter cards add **600 frames / 24 seconds**, for **35,374 total frames**.
- Full decoding and all twelve embedded chapter times were verified.
- Start/middle/end of 387 footage segments produced **1,161 comparisons**,
  minimum SSIM **0.988877**.

[Combined lineage](../assets/live-20260914-action/combined-timeline.json) preserves
input hashes and exact frame mappings. The individual source files/URLs stayed
unchanged; the combined video was uploaded separately.
Headless Edge verified default selection, all twelve chapters, video switching,
direct timestamps, and invalid-time rejection in the local player.

## Revalidation commands

### English-default documentation: September 15, 2026

The localization check passed **63 offline tests and seven installed-SDK contract
tests**, Ruff lint/format, Python compilation, and dependency/SDK checks.
The documentation checker verified **63 Markdown files, 2,747 local links,
12 local heading anchors, 108 CLI examples, and 31 reciprocal language pairs**.
Paired executable policy inputs are identical; canonical datasets/prompts and Azure
integration code were not changed.

Headless Edge loaded **60 guide pages and all 158 image references** across both
languages. The local player defaults to English, preserves video/time on language
switch, seeks all twelve chapters, plays all three source videos, and rejects invalid
times, filenames, and languages. These were **local checks with zero Azure requests**.
The historical results below remain attributed to September 14.

The historical check reported **59 offline tests, seven installed-SDK contracts**,
Ruff/format, compilation, SDK versions/dependencies, and **31 Markdown files,
1,338 local links, 54 CLI examples**. These are the pretranslation counts, not the
English edition's current counts or a remote GitHub Actions result.
Eight source-video playback/seek checks covered start/25%/50%/90%, switching, and
invalid time/file rejection with no external or mocked video.

```bash
python -m pip check
python scripts/check_sdk.py
python -m ruff check .
python -m ruff format --check .
python -m compileall -q src scripts examples tests tests_sdk
python -m unittest discover -s tests -t . -v
python -m unittest discover -s tests_sdk -t . -v
python scripts/check_docs.py
```

SDK checks need `.[cloud,agents,hosted]`; Ruff needs `.[dev]`.
Offline contracts are not Azure quality scores. Raw run/evaluator/cleanup evidence
remains in Git-excluded `outputs/live-20260914-action/`.
Do not add `.env`, authentication material, or private raw traces to Git.
