# Validation boundaries and actual execution

**English** | [한국어](../ko/reference/validation.md)

**Installation, offline contracts, real Azure execution, model quality, and media validation are distinct.**
Each language uses independent execution labels and recording sources.
Earlier videos and upstream results are not relabeled as new evidence.

<a id="current-answer"></a>

## Current answer — September 26, 2026

| Question | Answer | Details |
|---|---|---|
| What changed in the latest straightforwardness pass? | Three sequential, fresh-context reviews corrected seven further beginner gaps: local editors, Search preparation/authentication, trace-record location, truthful completion status, opening the source folder and cleanup of earlier preparation attempts. Both languages are aligned; no new learner-pilot or Azure claim | [Three fresh-context passes](#fresh-context-three-pass-20260926) |
| What is the final closeout status? | Six guide/material/evidence issues corrected; all 63 language pairs checked. After the corrected revision passed offline gates, 32 bounded guide CLI commands and two local package commands completed in both languages. Two new SDK responses matched portal traces. This is not a fresh full acceptance or an all-feature Azure claim | [Final closeout](#final-guide-closeout-20260925) |
| What is recorded? | The main A/B steps of Labs 00–09 and 11 and the optional Foundry evaluation steps, in English and Korean, with `gpt-6-sol` / `gpt-6-sol-judge` (`2026-09-22`) in the Sweden Central training project | [Re-recording](#gpt-6-sol-20260924) · [videos](../video-summary.md) |
| What did the live runs return? | In each language: business checks baseline 6/6, candidate 6/6 and holdout 4/4; acceptance `ready-for-human-review` with `deployment_approved: false`. Judge scores are kept separately and do not decide acceptance | [Actual results](../live-run.md) |
| What else ran with `gpt-6-sol`, unrecorded? | September 23: verification runs of the optional evaluation steps (recorded again on September 24), the conversation evaluation module, existing-traces and recurring evaluations, Agent Optimizer (baseline only), cloud red teaming (displayed ASR invalid) and the approved Hosted CI release | [Additions](#foundry-evaluation-additions) · [previously not-run items](#previously-not-run-items) |
| What has not run with `gpt-6-sol`? | Lab 03 portal File Search; Lab 06 IQ Chat and hybrid RAG; Lab 07 feedback/regression and the Hosted matrix; Lab 08's default local server, `azd ai agent invoke --local` and the learner's own Hosted deployment (section 6's workflow server answered one `curl` request on September 24); Hosted server-side tracing; Lab 10; the extension modules that [coverage](../coverage.md) does not list as re-run | [Not-run list](../live-run.md#not-run-with-gpt-6-sol) |
| How do I check a working copy? | Run the offline tests, Ruff, compilation, documentation and learner-bundle checks below. Each dated record states what passed for its revision | [Local checks](#local-checks-to-run) |
| What is outside this evidence? | Company/Microsoft 365 data, external Work IQ/Fabric connections, SLAs, statistical superiority, automatic retraining, production approval and other users' resources | [Not established](#not-established) |
| What changed in the September 24 review refresh? | Refreshed SDK pins, Lab 03 B managed agent in the B core, a core trace check, a browser option for A Lab 05, the Insights module, standalone SDK recipes and new CI checks. That evening the core B route ran live in both languages with the new pins, plus the trace lookup, recipes, A2A and one Insights scan; four guide or recipe defects were fixed | [Review refresh](#review-refresh-20260924) · [live check](#review-refresh-live-20260924) |
| What was added on September 25? | Both core routes run end to end as written in both languages, with six guide fixes; screenshots and short clips of Lab 03 B and the Lab 09 B trace search in both languages; English runs of conversation evaluation, memory, a routine and the Toolbox up to discovery; the remaining items need owner approval | [End-to-end run](#end-to-end-20260925) · [supplement](#review-refresh-supplement-20260925) |
| What changed in the later guide audit? | Corrected the required B agent, sign-in/recovery, A workflow branches and their different JSON shapes, trace-resume filters and learner worksheets. Offline checks only; no new Azure or media evidence | [Guide audit](#guide-audit-20260925) |
| What did the subsequent Azure audit verify? | Both core CLI routes and A Lab 05 terminal commands ran against the existing `gpt-6-sol` project. Each language returned 6/6, 6/6 and 4/4 and matching managed-agent traces. One English Group Chat credential timeout was retained; its uncaught SDK error reporting was fixed. Its portal blocker was resolved in the separate follow-up below | [Live audit](#azure-guide-audit-20260925) |
| What did the headless follow-up complete? | A's model/inline-agent/dev checks and A/B portal trace correlation, English then Korean. New manual dev assessments: 6/6 each. Median Send-to-render time: 6.75 s / 5.41 s over six rows each. File Search upload was disabled for the selected model | [Headless follow-up](#headless-guide-audit-20260925) |
| How straightforward are the guides and documents? | Earlier AI editorial review scored guides 94/100 and documents 90/100 (round 6), then 99.5/100 and 98/100 (round 7). Those scores do not rate the later audit revision and are not a learner pilot or timing measurement | [Earlier review](#straightforwardness-95) |
| Can a beginner finish route A alone from the guide? | Offline editorial audit: in a prepared environment, each A step names the screen, value or worksheet line and its check. Learning alone was the gap; [self-study preparation](../setup-owner.md#self-study) now covers the project, exact model, role, tracing, terminal and final cleanup. Not a learner pilot; the new portal steps follow official docs and were not run live | [Self-study audit](#beginner-self-study-audit-20260925) |

<a id="fresh-context-three-pass-20260926"></a>

## Three fresh-context beginner reviews, offline only — September 26, 2026

**Method:** three separate agent contexts ran sequentially. Each started from the current README/setup and followed the
complete A route and B's entry/setup and route boundaries. Only the updated files carried forward: earlier conversations,
findings, scores, session history and validation reports were excluded from each review. This isolated review context;
it did not delete stored conversation history. Each pass implemented and checked its own English-first/Korean changes.

| Pass | Independently found beginner gaps | Improvement |
|---|---|---|
| 1 | A discovered its spreadsheet requirement only at assessment time; B's Search token authentication was assumed | Check local text/CSV editors during setup, including six rows and columns; separately prepare Search token authentication and user roles |
| 2 | B self-study lacked concrete Search service setup; the handoff looked for trace evidence in the wrong notes file; cleanup could call incomplete work finished | Add owner-only Search creation/readiness steps and a return to setup; reuse the trace field in `operations-checklist.txt`; preserve incomplete/rejected outcomes after cleanup |
| 3 | Opening the source assumed VS Code knowledge; earlier failed region/project attempts could disappear from cleanup | Explain the editor, installation and **File → Open Folder...**; retain each owned preparation attempt through notes, operations and per-group cleanup |

**Final verification:** 341 offline tests passed on each of Python 3.13 and 3.14, including seven new bilingual regression
tests from these passes. Ruff 0.16.6 lint/format, compilation on both versions, documentation checks for all 63 language pairs,
and both unchanged learner-bundle checks passed. Changed pairs retain exact completion hashes and command parity in
`docs/localization.json`; no translation is pending.

Two child contexts had full-suite failures because their temporary workspaces were inside this existing azd project.
The final coordinator runs used a neutral system temporary directory, without hiding `azure.yaml`, changing guards or
using sandbox exclusions:

```bash
TMPDIR=/private/tmp python3.13 -S -m unittest discover -s tests -t . -q
TMPDIR=/private/tmp python3.14 -S -m unittest discover -s tests -t . -q
```

These are macOS validation commands; other systems should use their own temporary location outside an existing azd project.
Earlier failed attempts are not presented as successful standard-suite runs.

**Evidence boundary:** application code, executable workshop commands, prompts, synthetic data, grading and learner ZIPs
are unchanged. No Azure/portal execution, resource or role change, new recording, actual beginner pilot/timing, or new
editorial score was produced. Three AI reviews improve the instructions but do not prove that every beginner will finish
unaided. Installed-SDK tests were not rerun because application code and dependencies are unchanged.

<a id="checkpoint-clarity-audit-20260926"></a>

## Checkpoint clarity audit, offline only — September 26, 2026

**Scope:** traced the core A/B reading order against the current commands and worksheets, then corrected three remaining
action/check/return gaps in English first and Korean second. Executable workshop commands, application code, model,
prompts, synthetic inputs, grading and learner ZIPs are unchanged.

| Finding | Correction |
|---|---|
| Lab 00's intentionally failing v1 fixture could look like a broken environment; three commands appeared in one block | Separate each command from its expected result: v1 0/6 and v2 6/6, both with zero request errors, then the saved fixture-only comparison. Distinguish command success from the business gate |
| A learner finishing optional File Search could run the core checks on the wrong agent; a corrective Save could leave the recorded version stale | Return to the recorded inline agent/version with no unsaved edits before the four questions and baseline snapshot. Record the new version when correcting the initial policy paste; keep File Search evidence separate |
| Self-study cleanup implied that deleting the course group removed all connected logging resources | Record Application Insights and Log Analytics separately, including their actual groups. Verify remaining/shared/managed workspace state and costs; tracing not configured stays not run |

**Verified locally:** 334 offline tests on each of Python 3.13 and 3.14 with site packages disabled, including three new bilingual
regressions that failed before the guide corrections. Existing tests execute the documented offline commands and verify
the exact fixture counts, business gates, saved files and overwrite protection. Ruff 0.16.6 lint/format, compilation on both
Python versions, all 63 documentation language pairs and both unchanged learner bundles passed.
Completed translations retain exact file hashes in `docs/localization.json`.

**Evidence boundary:** logging-resource cleanup was checked against the linked Microsoft Learn documentation on September 26, 2026.
No new Azure execution, portal/deletion check, recording, beginner pilot/timing or editorial score was produced.
Installed-SDK tests were not rerun because application code and dependencies are unchanged; older media is not proof of these guide changes.

<a id="beginner-final-audit-20260926"></a>

## Beginner final clarity audit, offline only — September 26, 2026

**Scope:** followed the core A/B reading order and corrected concrete copy, save and recovery gaps, English first and then Korean.
The route, executable workshop commands, model, prompts, synthetic inputs, grading and learner ZIPs are unchanged.

| Finding | Correction |
|---|---|
| Offline-only readers reached B's Azure setup-card and notes instructions before the fixtures | A direct jump after `doctor` skips that preparation; no `.env`, Azure sign-in or SDK installation is needed |
| Opening a Windows source folder did not ensure a Bash terminal | Show the WSL-connected VS Code entry, distinguish PowerShell/Command Prompt and Python's `>>>`, and explain root-relative output paths |
| Browser instructions assumed Web search existed and did not say to replace existing instructions | Continue when Web search is absent; select only the Instructions field and replace its whole contents |
| A's assessment did not explain unsaved-version recovery or multiline CSV pasting | Define baseline/candidate/dev, restore the recorded version without saving a draft, paste each reply into one cell, undo a misplaced paste before other edits, and retain all six original rows |
| Self-study wording implied that accessible resource-group assets were all learner-owned | Require the dedicated group to contain only course resources; otherwise inventory individual assets and the authorized owner |

**Verified locally:** 331 offline tests on each of Python 3.13 and 3.14 with site packages disabled, including five new bilingual
guide-contract regressions that failed before the corrections. Existing tests execute the documented offline commands in temporary
copies and check their saved files and overwrite protection. Ruff 0.16.6 lint/format, compilation on both Python versions,
documentation/command parity for all 63 language pairs and both learner-bundle checks passed.
Changed translations retain exact completion hashes in `docs/localization.json`.

**Evidence boundary:** the WSL opening steps were checked against the linked official VS Code guide on September 26, 2026.
Windows/WSL and spreadsheet UI execution, live Azure/portal checks, new recordings, a beginner pilot/timing and a new editorial score
were **not run**. Installed-SDK tests were not rerun because application code and dependencies are unchanged.
Older screenshots remain references, not proof of these new usability instructions.

<a id="copy-resume-audit-20260925"></a>

## Straightforwardness: copy and resume audit, offline only — September 25, 2026

**Scope:** traced the core A/B paths against their executable commands and worksheets, English first and then Korean.
The fixes remove assumptions about preparation order and terminal state; they do not change the model, prompts, policies or grading.

| Finding | Correction |
|---|---|
| Self-study said learners were ready after step 6, although A requires the step 7 terminal | Complete steps 1–7, allowing the optional trace step to be marked skipped, then use the setup ready check |
| The English lightweight-clone shortcut omitted a real URL and folder change; Korean had no matching option | Both guides have one optional, complete clone → enter folder → sparse-checkout block, with `&&` and an explicit parent-directory starting point |
| A failed virtual-environment creation or activation did not stop the SDK installation line | Chain the three commands with `&&`; keep the first error and do not run global `pip install` |
| Lab 03 B invocation inherited its name from the previous terminal; portal checks assumed the recording's version 1 | Choose a restart point from saved files; enter both `agent_name` and `agent_version`, reject blank values before the request, and compare the portal with the saved invocation |

**Verified locally:** 326 offline tests on each of Python 3.13 and 3.14 with site packages disabled, including four new regressions
that first reproduced these gaps. Shell tests use explicit stubs: failed clone/setup stops, and a new terminal uses the entered agent
name/version rather than stale variables. Ruff 0.16.6 check/format, compilation on both Python versions, documentation/command parity
for all 63 language pairs and both learner-bundle checks passed. Changed translations retain exact hashes in `docs/localization.json`.

**Media boundary:** the two Lab 03 invocation captures still show the earlier version-only prompt. Their original commands, inputs,
responses and media hashes are preserved; the capture metadata separately pins the revised blocks and marks them not live-verified.
The lab, video page and action index disclose that difference. No old recording is evidence for the new resume behavior.

**Not run:** live Azure or portal steps, new recordings, a learner pilot/timing or a new editorial score.
Installed-SDK tests were not rerun because application code and dependencies are unchanged. Learner ZIPs and evaluation inputs are unchanged.

<a id="beginner-self-study-audit-20260925"></a>

## Beginner self-study audit, offline only — September 25, 2026

**Question:** can a beginner finish route A alone, using only the guide? Every A step was traced from the README to the Lab 11 cleanup,
English first and then Korean, for two learners: one in a prepared class environment and one learning alone.

| Finding | Correction |
|---|---|
| Learning alone led to owner steps written for administrators: a code quickstart, no portal steps, no role check and no final cleanup. Many blockers said only "ask the owner" | New [self-study preparation](../setup-owner.md#self-study): portal project, exact `gpt-6-sol` deployment, **Foundry User** check, optional tracing, setup card, terminal and resource-group cleanup, each with a check. The README, index, setup, routes, Lab 00 A, Lab 09 A, instructor guide, troubleshooting and cleanup link to it |
| Preparing A's terminal ran B's notes block without saying which notes file is the learner's | Lab 00 B runs the block, because Lab 02 B saves there, but keeps A's notes in the learner ZIP. It also links the WSL installation guide |
| Several checks named a value without saying where to find it | Lab 02 names the line under the reply for time and tokens; Labs 03 and 06 name the exact worksheet lines; Lab 05 says how to copy the saved JSON |
| Lab 07 asked beginners to compare a 4.8 KB instruction text by eye | Check the recorded **Version** and a greyed-out **Save**: saved versions are immutable, while unsaved edits would be used in the chat |
| Smaller beginner gaps | A plain-text Lab 01 sketch; `assessment-baseline.csv` as a renamed copy saved as CSV UTF-8; `.venv` reactivation for a self-prepared terminal; Lab 09's trace step in reading order |

**Verified locally:** 322 offline tests on each of Python 3.13 and 3.14 with site packages disabled, including one new regression test
that keeps the self-study route reachable and checked in both languages; Ruff 0.16.6 check/format, Python compilation, documentation and
English/Korean command-parity checks for all 63 language pairs, and the learner-bundle check. Installed-SDK tests were not rerun because no
SDK code or dependency changed. Changed pairs have exact completion hashes in `docs/localization.json`.

**Not run:** live Azure calls or the new portal steps (they follow the linked Microsoft Learn pages, checked September 25, 2026),
a learner pilot or timing, new screenshots or recordings, and a new editorial score. Workshop commands, prompts, policies, datasets,
fixtures, grading and the learner ZIPs are unchanged.

<a id="guide-audit-20260925"></a>

## Guide accuracy and consistency audit, offline only — September 25, 2026

Reviewed the A/B instructions after `b741473` against the executable commands, output contracts, generated handouts
and official sign-in/tracing documentation. English was corrected first, then Korean; completed pairs retain exact hashes in `docs/localization.json`.

| Finding | Correction |
|---|---|
| Lab 00 said B did not need a Lab 03 agent, while the route required one; the command lookup also hid it under optional work | Distinguish A's browser agent from B's required SDK agent; align the core lookup, save checkpoints and route-specific completion criteria |
| `.env` preparation repeated `az login`, and 403 recovery repeated it again despite shared-subscription constraints | Separate file preparation from first/expired sign-in, preserve an existing login, reject a blank tenant before login and send permission failures to the owner |
| Lab 05's browser option led into terminal-only commands and output fields | One explicit question and one selected option; Playground skips the terminal block. Document `runtime_profile` / `answer` versus terminal `pattern` / `outputs`, the owner-prepared profile, and the matching worksheet/handoff |
| Day-2 trace lookup could search only Last Day and report older evidence missing | Include the original request's time range and agent/version before searching the saved response ID; do not make a new request to replace history |
| Smaller cross-page/language inconsistencies remained | Correct Korean Lab 05 step numbering, remove its extra B setup command, distinguish the A ZIP from B's source copy, and correct the earlier live-run fix count from five to six |

**Verified locally:** 314 offline tests on each of Python 3.13 and 3.14 with site packages disabled, including six added regression tests;
five installed-SDK workflow tests with stubbed transports, including both language Responses payloads;
Ruff check/format, Python compilation, documentation checks, generated learner-bundle checks, `pip check` and `check_sdk.py`.
The worksheet generator rebuilt both learner ZIPs and their manifests. Canonical prompts, policy corpus, evaluation datasets,
fixtures and grading criteria were not changed.

**Not run in this audit:** live Azure calls, sign-in, deployment, role/default-subscription changes, publication, push,
new screenshots/recordings or a learner pilot. The remote Lab 05 Playground option remains unverified in this edition;
the local stub-transport check is not a remote execution result. No new editorial score or model-quality claim was assigned.

<a id="azure-guide-audit-20260925"></a>

## Subsequent Azure guide audit — September 25, 2026

The user requested real Azure execution after the offline audit, with **Playwright headless** for browser work and a visible
browser only when authentication was needed. English ran first, then Korean, using separate copies/prefixes and only bundled synthetic data.

**Live evidence:** 33 distinct core B terminal blocks per language; all 14 saved response files per language;
real model, managed-agent, function/MCP, three workflow patterns, Search/IQ and controlled evaluation;
A Lab 05's terminal question in both languages; package-only output and cleanup inventory.
Each language's baseline/candidate/holdout passed 6/6, 6/6 and 4/4 with no collection errors.
Both managed-agent trace queries matched the saved response IDs and token counts.
The existing acceptance files were read at handoff; they were not recreated to count another execution.

**Corrected:** typed MAF SDK exceptions now retain their cause and use exit `2` rather than escaping the CLI error boundary;
the guides distinguish authentication/tenant/preset readiness, document the actual default B workflow question,
and separate IQ retrieval accounting from model usage. The first English Group Chat credential timeout remains in the record;
after a successful read-only token check, one explicit retry with unchanged model/prompt/provider settings completed.

**Verified locally:** 317 offline tests on each of Python 3.13 and 3.14, four new installed-SDK error-boundary tests with mocked
calls, Ruff check/format, compilation, documentation and learner-bundle checks. No model, prompt, corpus, dataset, grading threshold
or fallback behavior was changed.

**Blocked or not selected at that point:** correct training-account browser authentication, hence new A portal and B portal verification;
remote Hosted/Playground deployment, cloud judges and C modules. The portal header seen while loading was not counted as a successful
agent check. No new media, role assignment, model deployment, default-subscription change, deletion or push.
The subsequent headless follow-up resolved the browser blocker without changing this earlier run's scope or results.

[Run details and retained objects](../live-run.md#azure-guide-audit-20260925) ·
[Machine-readable evidence](../assets/azure-guide-audit-20260925/results.json).

<a id="headless-guide-audit-20260925"></a>

## Headless portal follow-up — September 25, 2026

**Completed live, in English then Korean:** the prepared project/model check; two model Playground questions; read-back of the existing
inline agent's exact saved instructions, version and empty tools/knowledge; four smoke questions and six dev questions per language;
the new A response's portal trace; and the original audit's B agent/version/instructions and response-to-trace/token correlation.
There were **24 new requests**, with no B trace-seeding call. Both six-row dev assessments passed **6/6**, with no missing/error rows.

**Measured:** over the six dev requests per language, Send-to-render median **6.75 s** (English, **5.69–9.29 s**) and
**5.41 s** (Korean, **4.11–7.01 s**). These are automated browser measurements including network/rendering, not server latency,
a learner pilot or proof of the 270-minute schedule. Initial capture-helper failures were preserved without resending questions;
four initial requests lack high-resolution timing. They are not assigned zero or included in the six-row dev timing cohort.

**New evidence, not older media:** 28 screenshots, actual responses, instruction snapshots, two assessment CSVs,
trace metadata and exact file hashes. No new video, agent creation/Save, prompt change, candidate, holdout, cloud judge or acceptance run.
The two creation forms were inspected and cancelled; the existing version-2 browser agents were reused.

**Remaining boundary:** File Search upload was disabled for the selected `gpt-6-sol` model in this project;
the remote Lab 05 Hosted Responses option remains unverified. A Lab 05's terminal runs remain the previous audit's results.
Provisioning, role/default-subscription changes, deployment, publication, push and cloud deletion were not performed.
Company/Microsoft 365 data and a separate least-privilege learner-account test remain outside this evidence.

[Actual results and measurement method](../live-run.md#headless-guide-audit-20260925) ·
[Machine-readable evidence](../assets/headless-guide-audit-20260925/results.json).

<a id="final-guide-closeout-20260925"></a>

## Final guide closeout — September 25, 2026

**The identified guide inconsistencies are corrected; owner preparation and unselected modules remain explicit.**
English was corrected first, then Korean and the generated learner ZIPs. No new editorial score or learner-time claim was assigned.

| Review angle | Correction |
|---|---|
| Accuracy | The former B Day 2 had 245 minutes before breaks. Lab 06 now ends Day 1; each session is 195 minutes of labs + 45 minutes of breaks/buffer. All advertised durations are teaching plans |
| Consistency | `policies/` is required for A's source inspection, not File Search only. Setup, generated `START-HERE.txt`, ZIPs and both languages agree |
| Alignment | Fresh B seeding participants need the named Search writer roles. Current evidence is linked with its actual scope; the English availability image is labeled as a reference, not a Korean tutorial capture |
| Straightforwardness | A Lab 05 defaults to the verified prepared terminal. Hosted Responses is an owner-verified opt-in; an error never silently changes the selected account/model/route |

**Verified before Azure:** 321 offline tests on each of Python 3.13 and 3.14, 91 installed-SDK tests with stubbed transports,
Ruff check/format, compilation, documentation/CLI parity and both generated learner bundles.
Four new regressions first reproduced the inconsistencies. The full suite also found the availability-image language/registration
problem; it was corrected without relaxing the existing media test.

**Then verified live:** the corrected source was frozen before the English and Korean checks.
Each language completed 16 current guide CLI commands: read-only preflight, model/structured answers, invocation of the existing
SDK agent, all three MAF modes and workflow patterns, local/Search/GA IQ reads, an IQ-grounded answer, A's exact terminal workflow
question and local cleanup inventory. Each language also built the package locally. Saved definitions and new response/trace/token
correlation were checked through Playwright MCP headless. No agent creation, seeding, deployment, role/default-subscription change,
cloud judge or holdout collection was performed.

**Retained findings, not hidden by successful exits:** the separate Foundry MCP `agent_get` probe returned **403** for its configured
identity; its permissions were not broadened. The already authenticated portal and explicitly subscription-bound guide CLI worked.
One Korean concurrent participant output omitted policy IDs; its original text remains. The aggregate's citations do not repair that output.
Successful command execution is not an all-pass business-quality score or human approval.

**Remaining work before a class:** the owner must check actual participant permissions, quota, Search writes and trace access.
The 270/480-minute schedules still need a learner pilot. File Search was unavailable after capabilities loaded; the remote A Hosted
Responses path and other optional C/paid/owner-write workflows are not newly verified. Earlier baseline/candidate/holdout results remain
historical evidence, not acceptance for this new code hash.

[Fresh execution details](../live-run.md#final-guide-closeout-20260925) ·
[12 labs and 17 extensions, item by item](../assets/final-guide-closeout-20260925/module-checks.csv) ·
[63 document pairs and frozen hashes](../assets/final-guide-closeout-20260925/document-checks.json) ·
[Results, original outputs and retained findings](../assets/final-guide-closeout-20260925/results.json).

<a id="review-refresh-20260924"></a>

## Review refresh, offline only — September 24, 2026

**Changed:** SDK pins (`azure-ai-projects` 2.6.1, `openai` 3.16.1, MAF core 1.18.0, `agent-framework-foundry` 1.13.0,
hosting 1.0.0b260910, `mcp` 1.30.0; [versions](versions.md)); typed A2A SDK requests; one dated
`compatibility.py` registry for raw REST API versions; `prompt-agent --output`; Lab 03 B as a core B step;
Lab 09 trace check; A Lab 05 browser option; the [Insights module](../labs/extensions/agent-insights.md);
six standalone recipes in `examples/recipes/`; azd command validation against a recorded help snapshot;
a read-only SDK drift report and a manual, cost-gated live smoke workflow.

**Verified offline:** 297 offline tests on Python 3.13 and 3.14 without site packages, 87 SDK tests with the installed pinned libraries and stubbed transports, Ruff, formatting, compilation, `check_docs.py` (127 Markdown files, 2,520 local links, 510 anchors, 328 workshop CLI examples, 84 azd examples, 63 language pairs), learner bundles, `pip check`, `check_sdk.py` and the CI offline doctor/demo/evaluate/package steps passed.

**Not run in this offline pass:** no Azure call, deployment, role change, recording or live smoke run. The live check follows below.
The recordings and live results above used the previous pins and guide revision; they are not evidence for the new steps.

<a id="review-refresh-live-20260924"></a>

## Review refresh live verification — September 24, 2026 (evening)

**Scope:** fresh copies of commit `a9c3990` with the refreshed pins, prefixes `mfv2-rr-20260924-<language>`, the same Sweden Central
project and `gpt-6-sol` / `gpt-6-sol-judge`. The lab subscription was pinned; the Azure CLI default was not changed.

- **Core B route, English and Korean:** every documented command exited 0; Lab 07 baseline 6/6, candidate 6/6, holdout 4/4 with 0 errors;
  acceptance `ready-for-human-review`, `deployment_approved: false`. Lab 03 B created version 1 in each language and invoked it by version.
- **Traces:** each managed agent call produced `invoke_agent` and `chat` spans with matching tokens within about three minutes;
  direct Responses calls produced none.
- **Optional and C items:** `maf-evaluate` 6/6 and 6/6; `cloud-evaluate` groundedness 6/6, relevance 5/6 (D05); A2A 1.0 with typed
  requests completed one delegated call; one Insights scan analyzed 22 traces and returned 4 insights; the local workflow server
  answered one Responses request; recipes 02–06 and 08 completed.
- **Fixed:** recipes now pin `AZURE_SUBSCRIPTION_ID` (an unpinned CLI credential returned 403 from another tenant's account);
  recipes 05 and 08 now carry synthetic evidence; the Pydantic warnings of `maf-evaluate` and the tenant-scoped trace query are documented.
- **Not run:** remote Hosted deployment for the browser Lab 05 option, cross-provider comparison, Toolbox/Tool Search/Skills,
  Memory, Routines, conversation evaluation, Agent Optimizer, red teaming and the route A portal steps.

[Details, IDs and owned objects](../live-run.md#review-refresh-live-verification).

<a id="review-refresh-supplement-20260925"></a>

## Supplement recording and not-run review — September 25, 2026

- **Recorded, English and Korean:** Lab 03 B create and invoke with `--output` (real zsh terminal; guide blocks pasted verbatim, `read` prompts answered by typing), the Lab 03 B portal check and the Lab 09 B trace search.
  Twelve lossless WebP screenshots decode pixel-identical to their PNG captures and four H.264 clips at 1× decode fully. The portal instructions equaled the CLI definition, and each trace ID equaled the Application Insights `operation_Id`.
- **Discarded:** one English attempt whose terminal printed a local home-directory path; it was re-recorded from a neutral working directory.
- **Ran, English:** conversation evaluation with the refreshed pins, the memory lifecycle, one routine dispatch, the Toolbox up to MCP discovery and a read-only route A trace check. Search denied the Toolbox direct query because the project identity has only Search Index Data Reader.
- **Needs owner approval:** a remote Hosted deployment with runtime roles; one non-OpenAI deployment for the cross-provider comparison; a supported optimizer deployment; the Search role for Toolbox, Tool Search and Skills. Installing the Dev Pack changes a workstation's global tools.

- **Offline checks:** 305 offline tests on Python 3.13 and 3.14, 87 SDK tests with the pinned libraries, Ruff check and format, compilation, `check_docs.py`, learner bundles and the CI offline doctor, demo, evaluate and package steps passed.

[IDs, results and owned objects](../live-run.md#review-refresh-supplement).

<a id="end-to-end-20260925"></a>

## End-to-end guide run — September 25, 2026

- **Ran as written:** fresh GitHub copies of `f128f0c` (English sparse clone, Korean ZIP); route B's 34 core blocks in one terminal per
  language (zsh, bash 3.2) with typed prompt answers; route A's portal steps of Labs 01–03, 07 and 09 in each portal language and Lab 05 A's terminal command.
- **Results:** every block exited 0; baseline 6/6, candidate 6/6, holdout 4/4 and `ready-for-human-review` in both languages;
  D01–D06 met their criteria in both portals; the traces showed `invoke_agent <agent>:2` with a child `chat` span.
- **Fixed:** the changed **Create an agent** dialog (new screenshots), the model check moved from **Details** to **Playground**,
  the recording's agent name, the `answer` nesting, the English round-limit item and the Korean feedback prompts.
- **Cleanup:** every object of the run was deleted and read back as 404.

[Details and objects](../live-run.md#end-to-end-20260925).

<a id="gpt-6-sol-20260924"></a>

## Re-recording with the optional evaluation steps — September 24, 2026

**Recordings:** new English and Korean recordings, started after 00:00 KST, in the same Sweden Central project with
`gpt-6-sol` / `gpt-6-sol-judge` and the prefixes `mfv2-sol-20260924-<language>`.

- **Scope:** the main A/B steps of Labs 00–09 and 11 and the optional Foundry evaluation steps.
- **English:** 98 actions, 293 lossless captures, videos 6:29 / 3:11 / 2:55 and 262 source segments (minimum SSIM 0.9922)
  from one terminal and two portal recordings.
- **Korean:** 91 actions, 272 captures, videos 6:03 / 2:57 / 2:43 and 244 segments (minimum SSIM 0.9923).
- **Playback:** local byte-range playback and all 11 chapter seeks were verified in each language; nothing was uploaded or pushed.
- **Removed:** the `g6sol-20260923` recordings and the separate `eval-portal-20260923` captures (git history at `90b18b3`).
  `videos/` holds `gpt-6-sol-20260924-en-summary.mp4` and `-ko-summary.mp4`, copies of each guide-ordered video.

[Recordings](../video-summary.md) · [Actual results](../live-run.md).

**Failures kept in the recording and what changed:**

- `E07-011`: the business-rubric baseline run returned groundedness and relevance but no `business_rubric` (0 errored), although
  its evaluation had three testing criteria. The CLI rejected it as invalid. The Korean `K07-011` returned all three the first time.
- `cloud-evaluate` gained `--retry-failed` (the native retry already existed) and an error that names the missing evaluator.
  `E07-013` retried once and kept the first attempt under `native-attempts/attempt-1`.
- `E07-012` then refused `--reference baseline`: the rebuilt retry state had lost `item_fields`, a bug in that retry path.
  The retry now keeps `item_fields` (regression test added); `E07-014` read the completed retry back without a new job and
  `E07-015` joined the candidate. Both source updates and hashes are in `live-results.json` (`source_updates`).
  After the recording, a `--reference` run can also be retried: the retry stays in the reference's evaluation as
  `<label>-retry-N`, and the advice to use `--retry-failed` appears only in `cloud-evaluate` errors. This change has offline
  and SDK tests only; it was not run against Azure.
- Opened from the playground, the portal evaluation wizard preselected agent **Version 1**, which still had Web search. The English
  capture tool kept it (`EP07-202`), so `EP07-206`/`EP07-207` scored Version 1 (TaskAdherence 4/6; D05 answered with an external U.S.
  rate). Both languages repeated the evaluation with Version 2 (`*P07-211` to `*P07-217`): Relevance 6/6, Coherence 6/6,
  TaskAdherence 0/6. Item 2 of Lab 07 A step 4 and item 1 of the Lab 09 A trace evaluation now tell learners to keep only the saved version.
- Capture-tool timing, not Foundry failures: `EP07-205` clicked before the evaluator list loaded, `KP07-203` waited for a dataset
  row that did not refresh after a successful upload, `KP07-215` typed before the rename dialog loaded. Later, separately named
  actions completed each step.

**Results in each language:** business checks baseline 6/6, candidate 6/6 and holdout 4/4; the no-evidence diagnostic 0/6 with
0 errors; cloud judge groundedness 6/6 and relevance 5/6 (D05). Business-rubric agreement was 6/6 for both runs; **Compare runs**
showed mean relevance 3.83 → 4.83 (English) and 4.17 → 4.50 (Korean) with **Too few samples** (captures `EP07-301`, `KP07-301`). MAF tool calls: English 6/6 and
6/6; Korean tool_call_accuracy 5/6 (D03's search query named `APPROVAL-01`, which the evaluator called a fabricated parameter) and
relevance 5/6 (D05). Trace evaluation: English 10/10, Korean 15/15, including five conversations that the earlier portal evaluation created.

**Azure changes:** under the new prefixes — portal agents (versions 1–2) and SDK agents, Search indexes, IQ knowledge sources and
bases, datasets, evaluations and runs, and custom evaluator versions `mfv2_sol_20260924_en_business_rubric` 1 and
`mfv2_sol_20260924_ko_business_rubric` 1 — plus billable model and judge calls. The portal language was switched to Korean for the
Korean recording and restored to English. No deployment, role assignment or default-subscription change.

**Local verification:** 256 offline tests passed on each of Python 3.13 and 3.14; the SDK import check and 77 installed-SDK tests
passed; Ruff, formatting, compilation and documentation checks passed.

<a id="previously-not-run-items"></a>

## Previously not-run evaluation, safety and release items — September 23, 2026

The owner asked for the items the evaluation additions left unrun. They ran the same evening against the same project,
`gpt-6-sol` / `gpt-6-sol-judge` and the prefix `mfv2-sol-20260923-<language>`; none is part of the edited videos.

| Item | Owner action first | English | Korean |
|---|---|---|---|
| Existing-traces evaluation (Lab 09 A) | **Monitoring Reader** for the project identity on Application Insights | 15/15 on Relevance, Coherence and TaskAdherence | 15/15 on each |
| Recurring evaluation | none beyond that role | first run on save 5/5; next hourly run sampled the planned request, 5/5; paused | first run 5/5; next hourly run 5/5 without the planned request; paused |
| Agent Optimizer | temporary `gpt-5.5` optimizer deployment, deleted afterwards | baseline only, 0.979 | baseline only, 0.938 (D05 relevance 2) |
| Cloud red teaming (Preview) | taxonomy reviewed; only the portal run was scoped, by deleting actions (SDK `enabled` flags did not limit generated attacks) | SDK: displayed ASR 89% (75/84); portal: 100% (6/6) | SDK: displayed ASR 57% (48/84) |
| Approved Hosted release | CI identity given project-scoped **Foundry Project Manager** and account **Reader**; environment variables pointed at this project | [run 35856612314](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35856612314): 6/6, 0 errors | [run 35857252318](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35857252318): 6/6, 0 errors |

**Findings kept as findings:**

- What an evaluator receives decides what it can verify. Each trace's `query` carried the agent's instructions with the six policies,
  so TaskAdherence passed 15/15; the dataset-based run in Lab 07 A sent only the question and scored 1/6 (English) and 0/6 (Korean).
- Recurring runs sample the latest seven days, not only the last hour: the first ran as soon as the schedule was saved and
  re-scored earlier conversations, and a random 5 of 16 took the English planned request but not the Korean one.
  Schedule configuration and evaluated samples stay separate evidence; nothing was re-sent to populate a run.
- The red-team service labelled rows as attack successes (score 0 against threshold 3) whose own reasoning said the response refused;
  every response was read and none performed or claimed a prohibited action, and 3 attacks were blocked by the content filter.
  The displayed ASR is therefore marked invalid. Taxonomy `enabled` flags did not limit attack generation; deleting actions in the
  portal did. A taxonomy PATCH needs the complete object, and a read right after a change can return the previous version.
- The optimizer's generic early-stop message said all candidates were perfect while rows failed, and its Groundedness judge compared
  each answer with itself, so no candidate was promoted; `optimizer-review.txt` records `pending-human-review`.
- Default model pickers can point at the wrong deployment: while the temporary optimizer deployment existed, a new evaluation's
  **Judge model** defaulted to it, and the optimizer's **Evaluation model** defaulted to `gpt-6-sol`. Both were set to `gpt-6-sol-judge`.
- Red-team calls left no agent traces; optimizer runs left 27 per agent, so the optimizer used isolated agent copies and the recurring
  schedule's sample was not affected.
- The Korean portal names the red-team wizard **빨간색 팀 실행 만들기** and the tabs **레드 팀 미리 보기** and **최적화 미리 보기**;
  the Korean scans and optimizer run were submitted from the English UI.

**Azure changes:** role assignments (Monitoring Reader for the project identity on Application Insights; the CI identity's
project-scoped Foundry Project Manager and account Reader; Foundry User for the Hosted runtime, granted by the pipeline);
deployment `mfv2-sol-20260923-opt-gpt55` created and deleted; agents `mfv2-sol-20260923-<language>-optimize` (version 1) and
`mfv2-sol-20260923-ci-hosted` (versions 1–2); datasets `mfv2-sol-20260923-<language>-optimizer-dev`; trace, optimizer and red-team
evaluations, red-team taxonomies and two paused schedules; changed `foundry-workshop` environment variables (previous values kept
in the session record). The CI identity's roles on the September 14 project were kept. No default-subscription change.

**Still not run:** Lab 08's local server and the learner's own Hosted deployment, server-side tracing for a Hosted agent,
guardrail attachment with `gpt-6-sol`, and the **Continuous** recurring mode (unavailable for trace evaluations).

<a id="foundry-evaluation-additions"></a>

## Optional Foundry evaluation additions — September 23, 2026

This revision adds optional Foundry Evaluation practice to the existing A/B routes; the core routes, their commands and
the recorded videos are unchanged.

| Where | Addition | Status |
|---|---|---|
| Lab 07 A step 4 | Run the saved agent on `dev-questions.jsonl` (new, questions only) as a portal evaluation with Relevance, Coherence and TaskAdherence, then compare with the manual worksheet | Optional; TaskAdherence is Preview |
| Lab 07 B step 2 | If the baseline passes, `collect --retrieval none` creates a real, dev-only failure to diagnose; `feedback` and `cloud-evaluate` reject it | Optional |
| Lab 07 B step 5 | `cloud-evaluate --business-evaluator` registers or reuses an owned code-based evaluator with the local business rules; `--reference` adds candidate to baseline's evaluation for **Compare runs** | Optional Preview |
| Lab 04 section 5 | `maf-evaluate` scores the MAF function-tool agent's calls with `tool_call_accuracy` and `relevance` | Optional; experimental MAF API |
| Lab 09 A | Owner-prepared existing-traces evaluation and the **Recurring** option | Documented here; run later that day after the owner's actions ([previously not-run items](#previously-not-run-items)) |

**Live Azure checks, English and Korean separately, with `gpt-6-sol` / `gpt-6-sol-judge`:**

| Check | English | Korean |
|---|---|---|
| Portal evaluation (Relevance / Coherence / TaskAdherence) | 5/6, 6/6, 1/6 | 5/6, 6/6, 0/6 |
| Manual business assessment of the same agent | 6/6 | 6/6 |
| New dev collections, business checks (baseline / candidate) | 6/6, 6/6 | 6/6, 6/6 |
| No-evidence diagnostic | 0/6, 0 errors, `feedback` rejected | 0/6, 0 errors, `feedback` rejected |
| Cloud judges with `business_rubric` (groundedness / relevance / business, each run) | 6/6, 6/6, 6/6; agreement 6/6 | 6/6, 5/6, 6/6; agreement 6/6 |
| Portal comparison of the two runs | relevance 4.33 → 4.83, too few samples | relevance 3.83 → 4.50, too few samples |
| `maf-evaluate` (tool_call_accuracy / relevance) | 6/6, 6/6; re-run after review fixes (code `408b1b57…`, `eval_fd079e29…`) 6/6, 6/6 | 6/6, 5/6; re-run after review fixes (`eval_e330c6aa…`) 6/6, 6/6 |
| Cloud judges on the no-evidence diagnostic (before the refusal was added) | invalid (`evalrun_2b495a2e…` in `eval_f231e23c…`): Groundedness skipped 3/6 rows; nothing counted | invalid (`evalrun_1e0790d4…` in `eval_910a4729…`): Groundedness skipped 4/6 rows; nothing counted |
| Conversation evaluation module (turn; conversation groundedness) | 6/6 and 6/6; 1/2 | 6/6 and 6/6; 2/2 |

**Findings kept as findings:** TaskAdherence and Relevance disagreed with the business assessment because the evaluators receive
only the question and answer, not the policies inside **Instructions**. Relevance marked down D05's correct withholding, and its
result varied between runs (5/6 in the recording, 6/6 in the English verification; 5/6, then 6/6 in the two Korean `maf-evaluate`
runs). Groundedness returns *skipped* (`not_applicable`) for a row with empty context; the workshop never counts a skipped row, and
`cloud-evaluate` now refuses a no-evidence run before submission. In the Korean portal, the localized default
names of the Relevance and Coherence evaluators failed the evaluator-name check and kept **Next** disabled until renamed; the guide
states this workaround. Six cases are too few for the portal's statistical comparison.

**Run later the same day:** the existing-traces evaluation, recurring evaluation, Agent Optimizer, cloud red teaming and a new
release pipeline run, after the owner's actions listed in [the next section](#previously-not-run-items).

**Azure changes:** two uploaded dev-question datasets, datasets that `cloud-evaluate` creates automatically, portal and SDK
evaluations and runs (three evaluations named `...-trial-...` were scaffolding checks, one of them grading offline fixture rows; the
invalid diagnostic runs are kept), and owned custom evaluator versions (`mfv2_sol_20260923_en_business_rubric` 1–2, `mfv2_sol_20260923_ko_business_rubric` 1),
all under the `mfv2-sol-20260923-<language>` prefixes, plus billable agent and judge calls. The portal language was switched to
Korean for the Korean captures and restored to English. No deployment, role assignment or default-subscription change.
[English results](../live-run.md#optional-evaluation-additions--separate-verification-september-23-2026) · [September 24 recording of the same portal steps](../action-captures.md)

**Local verification:** 255 offline tests passed on each of Python 3.13 and 3.14, and 73 installed-SDK tests passed with stub
transports. New tests cover the grader's parity with the local rules, the diagnostic's rejection paths, skipped judge rows,
custom-evaluator criteria, shared reference runs, tool-result mapping and the new captures. Ruff 0.16.6, compilation, both learner
bundles, the CI offline commands in a clean copy and documentation checks (117 Markdown files, 58 language pairs, 340 CLI examples)
passed. Final code hash: `67e7ac04…`.

<a id="gpt-6-sol-20260923"></a>

## gpt-6-sol environment, recordings and removal of earlier media — September 23, 2026

**Environment:** a dedicated Sweden Central resource group with a Foundry account (API keys disabled) and project,
Basic Search with a system-assigned identity and key authentication disabled, Log Analytics (30 days, 1 GB/day cap),
Application Insights, keyless Search and Application Insights project connections, and resource-scoped roles only.
Resource names keep the environment's original `g6luna` label. The default Azure CLI subscription was not changed.

**Model switch:** `gpt-6-luna` deployed but failed on the project Responses, prompt-agent and MAF paths (HTTP 500; the
portal agent reported `reasoning.effort` unsupported). `gpt-6-sol` and `gpt-6-astra` passed the same agent checks and
`gpt-6-sol` was selected ([model choice](model-choice.md)). The environment now has `gpt-6-sol` (150K TPM) and
`gpt-6-sol-judge` (100K TPM), Data Zone Standard `2026-09-22` with `NoAutoUpgrade`. The `gpt-6-luna`, `gpt-6-luna-judge`
and `gpt-6-astra` deployments, probe agents and a temporary North Central US account (also purged) were deleted.
Opening the first portal agent created a `text-embedding-3-large` deployment (Standard, 110K) that the labs do not use.
Search accepted no GPT-6 model for knowledge bases, so the optional IQ Chat preset stays on `gpt-5.6-luna`.

**Recordings:** independent English and Korean runs of the main A/B steps of Labs 00–09 and 11 — 69 actions and
207 lossless captures per language, three edited videos each (English 4:36 / 2:30 / 1:43, Korean 4:32 / 2:27 / 1:43),
175 and 176 source segments with minimum midpoint SSIM 0.9925 (English) and 0.9922 (Korean), local byte-range playback
and all 11 chapter seeks verified. Not uploaded or pushed. Every recorded action exited 0; the feedback step was not run
because neither baseline had a failed case. In each language the business checks were baseline 6/6, candidate 6/6 and
holdout 4/4, and the optional cloud judge on the candidate returned groundedness 6/6 and relevance 5/6 (D05, a correct
abstention). [Recordings](../video-summary.md) · [Actual results](../live-run.md).

**Removed:** the September 15 foundation recordings, the September 16 extension recordings, the September 23
`gpt-6-luna` recordings and their pages were deleted from the working tree; they remain in git history at `47f3b49`.
Earlier GitHub attachment URLs are no longer linked; removing those hosted copies is a separate manual action.
The September 17 IQ Chat configuration captures remain because that preset is unchanged.

**Local verification:** 244 offline tests passed on each of Python 3.13 and 3.14; 67 installed-SDK tests passed with
stub transports. Ruff 0.16.6 lint/format, compilation, the CI offline commands in a clean copy and both learner bundles passed.
Documentation checks cover 117 Markdown files, 58 language pairs and 330 CLI examples, with no pending translations.
Azure changes in this revision were limited to the deployments above and the recorded agents, Search objects and
evaluation runs under each `mfv2-sol-20260923-<language>` prefix; no role or default-subscription change.

## Local checks to run

```bash
python3.13 -S -m unittest discover -s tests -t . -q
python3.14 -S -m unittest discover -s tests -t . -q
python -m unittest discover -s tests_sdk -t . -q
python -m ruff check .
python -m ruff format --check .
python -m compileall -q src scripts examples tests tests_sdk
python scripts/check_docs.py
python scripts/build_learner_materials.py
python -m pip check
python scripts/check_sdk.py
```

Maintainers can also run `python scripts/check_dependency_drift.py` (advisory, needs PyPI access; never edits pins)
and, after upgrading azd or its Foundry extensions, `python scripts/record_azd_surface.py` to refresh the help snapshot
used by `check_docs.py`. The **Approved live smoke check** workflow is manual and cost-gated.

SDK tests use the actual installed libraries with explicitly stubbed transports.
They are not counted as real Azure responses.
Each dated record on this page states what passed for its revision.

## Not established

Real company/Microsoft 365 data, external Work IQ/Fabric connections, operational SLAs,
statistical superiority, automatic retraining/weight changes, human production approval,
and deletion of other users' resources are outside this evidence.
Stopping sessions does not eliminate all model/Search/log/storage costs.

<a id="straightforwardness-95"></a>

## Straightforwardness review: guides and documents — September 24–25, 2026

**Round 7: guides 99.5/100 and documents 98/100.** Earlier rounds: 97/100 and 86.5/100; 97.5/100 and 94/100;
93.5/100 and 92.5/100; 96.5/100 and 92/100; 100/100 and 98.5/100; 94/100 and 90/100.
Rounds 1–4 and 6 each used seven new, independent AI cold reads: English A, English B and Korean guides (D1–D10), and two English
and two Korean document groups (R1–R10). Rounds 5 and 7 are the previous round's reviewers re-reading their whole scope after the fixes.
Round 6, on September 25, is the final check after the review refresh, the live verification, the supplement recording and the cleanup.
Each dimension starts at 10, loses 3, 2, 1 or 0.5 points per critical, major, moderate or minor finding and takes the lowest
reviewer score; D10 and R10 come from the Korean reviews. New reviewers kept finding a few different small issues, so rounds 2–4 and 6
moved up and down. This is an editorial assessment, not a human usability pilot, a learner-success rate or a measured completion time.

| Guides | What earns full points | Round 1 | Round 2 | Round 3 | Round 4 | Round 5 | Round 6 | Round 7 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| D1 | Entry and route choice reach the first action of either route | 10 | 9.5 | 10 | 10 | 10 | 8 | 9.5 |
| D2 | One linear core path; optional, owner and historical material collapsed or marked | 10 | 10 | 9 | 10 | 10 | 10 | 10 |
| D3 | Numbered, imperative steps with exact UI labels, file names and values | 10 | 10 | 9 | 10 | 10 | 9 | 10 |
| D4 | A visible success or failure check after every action or command | 10 | 9 | 9 | 10 | 10 | 9.5 | 10 |
| D5 | Commands run as written, in order, with named output files | 10 | 10 | 10 | 7 | 10 | 10 | 10 |
| D6 | Plain, lean language in the core path | 10 | 10 | 9 | 9.5 | 10 | 10 | 10 |
| D7 | Concrete recovery, including what to ask the owner for | 9 | 10 | 9 | 10 | 10 | 10 | 10 |
| D8 | Explicit done criteria, correct A/B next links and a clear handoff | 10 | 10 | 10 | 10 | 10 | 9.5 | 10 |
| D9 | Current, consistent model, date, screenshot and link claims | 10 | 10 | 9.5 | 10 | 10 | 9 | 10 |
| D10 | Korean pages mirror the English and read naturally | 8 | 9 | 9 | 10 | 10 | 9 | 10 |

| Documents | What earns full points | Round 1 | Round 2 | Round 3 | Round 4 | Round 5 | Round 6 | Round 7 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| R1 | Purpose, audience and the current answer come first | 8 | 10 | 10 | 9.5 | 10 | 8 | 10 |
| R2 | Headings, tables and anchors find an answer in seconds | 9 | 10 | 10 | 9.5 | 10 | 10 | 10 |
| R3 | Procedures are numbered, with the actor and a success check | 10 | 10 | 10 | 9 | 10 | 10 | 10 |
| R4 | Numbers, flags, links and results agree with guides, CLI and evidence | 7 | 9 | 8 | 9 | 9 | 7 | 9 |
| R5 | Each fact lives in one place; dated history stays compact | 9 | 10 | 10 | 9.5 | 10 | 9 | 10 |
| R6 | Short sentences and explained terms | 9.5 | 10 | 10 | 10 | 9.5 | 10 | 10 |
| R7 | Brief, consistent evidence boundaries, Preview status and dates | 10 | 9 | 9 | 9 | 10 | 8 | 10 |
| R8 | Paid calls, cloud writes, roles and cleanup name approver and actor | 9 | 8 | 8 | 9 | 10 | 9 | 9 |
| R9 | Every page gives a next step; no dead or removed links | 9 | 9.5 | 10 | 9.5 | 10 | 10 | 10 |
| R10 | Korean pages mirror the English and read naturally | 6 | 8.5 | 7.5 | 8 | 10 | 9 | 10 |

**Round 6, the final check on September 25:** no critical finding. Its 14 findings named 12 distinct issues; all were fixed,
English first and then Korean:

- **Lab 05's two A options:** README, learning paths, the setup card, owner setup, the instructor handoff and Lab 00 now name the
  prepared Hosted workflow agent in Playground as well as the prepared terminal, and send learners to Lab 00 B and Lab 02 B only when
  neither was supplied.
- **Status made stale by later runs:** the not-run answer above, Lab 08's evidence limits and the live-run not-run list now separate
  section 6's one `curl` request from section 3's server, `azd ai agent invoke --local` and a remote deployment; the advanced path,
  evidence hub, model choice and coverage note now include the September 24–25 module runs and the Tool Search/Skills block.
- **Steps and checks:** Lab 01 checks the pasted endpoint because the screen cuts it off; Lab 09's cleanup sentence points to step 4;
  the screenshot note names the September 25 supplement; the Korean Lab 09 start card again asks for Lab 03 B's `response_id` and
  trace access.
- **One fact, one place:** the September 25 supplement record no longer repeats the documentation-check counts.

**Afterward, not re-scored:** round 7's two findings, the setup card's route sentence and endpoint row and the evidence hub's list of
items waiting for owner approval, were corrected.

**Verification, September 25:** 305 offline tests on each of Python 3.13 and 3.14, Ruff 0.16.6 lint/format, Python compilation,
`check_docs.py` at commit `f128f0c` (127 Markdown files, 2,612 local links, 554 anchors, 328 CLI examples, 84 azd examples, 63 language pairs) and
the learner-bundle checks passed; changed pairs have exact completion hashes in `docs/localization.json`. The reviewers were
read-only, and no Azure call, resource change or push was made for this review.

**Rejected after verification, rounds 1 and 4:** two critical findings came from errors in the reviewers' brief, not from the pages.
Round 1's R4 finding said the coverage page over-claimed the September 23 `gpt-6-sol` runs; those claims are correct, but the
README sentence denying any re-run was wrong and is fixed. Round 4's D5 finding assumed core paid commands take `--confirm-cost`;
by design they do not, and the reviewer withdrew it after the correction (Lab 07 B now states its billable calls).
Without them, round 1 documents would score 89.5 and round 4 guides 99.5. Round 1's proposal to add `--language ko` to every
Korean core command was not adopted because the Korean recordings use the default form; Lab 00 now states both Korean forms.

**What changed after rounds 1–4, English first and then Korean:**

- **Validation page:** a current-answer table comes first; current evidence, local checks and limits precede the collapsed
  review and September 15–17 history; the recording summary is a list.
- **Checks that match the code:** Lab 00's Python note and install check, Lab 02's `usage` fields, `echo $?` for the Lab 04/07
  expected failures, Lab 08's printed package path and rebuild command, `maf-evaluate --output` and the Hosted `stop-session` receipt.
- **Approver and actor at the command:** A2A writes, `routine create`, the agent-safety redeploy, the optimizer submission,
  `stop-session` and Lab 07 B's billable collections.
- **Less to read on the core path:** Lab 09 A's optional review and the cleanup rows for optional modules are collapsed;
  both learner `START-HERE.txt` files say the guide pages are outside the ZIP.
- **One fact, one wording:** the four modules re-run on September 23, conversation evaluation among the September 23 runs,
  the fixture files, the guide-ordered video's "Labs 00–09 and 11", the release deployment, version and schedules, and the
  Lab 09 A status in the September 23 table now agree across pages.
- **Navigation:** per-lab jumps in both action indexes, next or return links on coverage and developer tools, the current page
  marked in the evidence footers, and one 51-row full error reference in both languages.
- **Korean:** every extension page, Lab 10 and the flagged guide and reference sections were compared sentence by sentence,
  keeping Korean-edition results and Korean-UI steps; the A route, Lab 00's language note and several reference sentences read naturally.

**Afterward, not re-scored:** round 5's two findings, a missing verb on the model-choice page and one schedule count on the
coverage page, were corrected.

**Verification, September 24:** 287 offline tests passed on each of Python 3.13 and 3.14; five new tests cover this record's arithmetic,
the validation layout, the mirrored error reference, the `--output` command list and the learner start files.
Ruff 0.16.6 lint/format, Python compilation, documentation checks (117 Markdown files, 58 language pairs, 328 CLI examples)
and byte-for-byte learner-bundle checks passed. Changed pairs have exact completion hashes in `docs/localization.json`;
no translation is deferred.

**Boundaries, September 24:** workshop command lines, Foundry request logic, prompts, synthetic policies, evaluation datasets, fixtures and
recordings are unchanged; only one Korean `printf` prompt was translated. The learner `START-HERE.txt` text changed, so both
learner ZIPs were regenerated. No Azure call, resource or permission change, deployment, publishing or push was performed.

## Older validation history

Older guide reviews, September 17 records and September 15 media/execution history moved to [Validation history](validation-history.md). The current page keeps the current answer, recent dated evidence, local checks and boundaries.
