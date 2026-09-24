# Validation history

**English** | [한국어](../ko/reference/validation-history.md)

This page preserves older collapsed validation and media records moved from the current validation page. Anchors and tables are unchanged so historical links still resolve here.

<details>
<summary>Earlier guide and document reviews, September 17–24, 2026 — historical, superseded by the review above</summary>

<a id="straightforwardness-review-records"></a>

## Straightforwardness: review notes and cleanup output — September 24, 2026

**The A/B walkthrough found two remaining gaps between a step and its record.**
Twelve page pairs, including this record, were updated English-first, then in Korean; both learner ZIPs were regenerated.

| Friction found | Correction |
|---|---|
| B was told to write findings, but the shared notes mixed browser-only observations with a generic code section and lacked evaluation-decision and package fields | Separate common setup, A-only, B-only and resume sections. Ten blank B review fields are named in the matching Labs 02/04/05/06/07/08 and checked at handoff. Keep JSON in its saved files; append missing fields to older personal notes instead of replacing them |
| Lab 09 assumed `cleanup-plan` would list Search objects, even without a local ownership file | Explain `search_ownership.objects`, `search_ownership: null` and `required_manual_inventory`. The command reads local records, not Azure state; no ledger or an empty list does not mean no resources or costs |

**Verification:** 282 offline tests passed on each of Python 3.13 and 3.14. Four new tests cover route-specific blank notes,
the guide-to-field mapping, cleanup explanations and the CLI's unchanged local-only behavior with and without a ledger.
Ruff 0.16.6 lint/format, Python compilation, documentation checks and byte-for-byte learner-bundle checks passed.
The documentation check covers 117 Markdown files, 58 language pairs and 328 CLI examples.
Changed page pairs have exact completion hashes in `docs/localization.json`; no translations are deferred.

**Boundaries:** executable command blocks, Foundry request logic, prompts, synthetic policies, evaluation datasets, fixtures
and recordings are unchanged. No Azure calls, resource or permission changes, deployment, publishing or push were performed.
There was no human learner pilot, timing measurement or new usability score.

<a id="straightforwardness-cold-read"></a>

## Straightforwardness: cold-read corrections — September 24, 2026

**Three independent cold reads (English A, English B, Korean) found checks that did not match actual output, and names that varied.**
Corrections were made English-first, then in Korean, in 14 page pairs and the generated learner worksheets.
Foundry request logic, prompts, synthetic policies, evaluation datasets, fixtures and recordings are unchanged.

| Friction found | Correction |
|---|---|
| Lab 05 B asked learners to map the sequential output to three roles, but MAF's sequential builder returns only the last participant's reply. The concurrent and Group Chat checks did not name their extra entries | Lab 05 names the one `EvidenceReviewer` entry, the concurrent aggregator's joined copy and the Group Chat round-limit notice, as `build_orchestration`, the pinned `agent-framework-orchestrations` 1.1.1 defaults and the September 24 captures show |
| Lab 07 B said to find a failed case in `responses.jsonl`, which has no pass/fail field | Find `passed: false` under `checks` in `business-evaluation.json`, then read that case's response |
| Lab 00 A's setup table had different rows from the worksheet's setup card. Lab 02 A named no worksheet lines and gave the chat-box location only in a screenshot caption | The table lists the worksheet's nine lines in order. Lab 02 names each line to fill and puts the input location in the step |
| Lab 06 B showed the IQ seed capture and check after the IQ query, and opened with a four-sentence recording caveat | Seed → capture and check → query → capture and check. A two-sentence screenshot note now sits at the first capture |
| Lab 05 A buried its command under a repeated prerequisite paragraph and diagram | Step 1 opens the prepared terminal with a visible check; the diagram explains the output in step 2 |
| Names and statuses varied: Lab 01's only numbered learner step was 1; B was "Practitioner" in schedules; IQ Chat was "not run" or "not selected"; Lab 09 omitted the automatically created `text-embedding-3-large` deployment | Lab 01 has steps 1–3; the routes are **A — Beginner** / **B — Implementation** (Korean **입문** / **구현**) everywhere; IQ Chat is **not selected**; deployments are in the Lab 09 inventory and worksheet |

Smaller changes: the worksheet header tells A to skip the B section; Lab 00 B asks B to fill its setup card;
Lab 07 A gives the exact owner request for 401/403/429 and gates its optional evaluation behind cost approval;
setup no longer names a `dev.jsonl` file that A does not have. Korean-only fixes clarify the prefix hyphen rule,
use **추적 미확인** for missing trace evidence, replace translated phrasing in Labs 00 and 07 and correct a
"start card" mistranslation of *setup card* in Labs 00 and 01.

**Verification:** 278 offline tests passed on each of Python 3.13 and 3.14. Seven new tests cover the corrections; six failed
on the Korean pages before their update, and the seventh keeps every worksheet line cited by a guide real.
Ruff 0.16.6 lint/format, Python compilation and documentation checks passed.
The documentation check covers 117 Markdown files, 58 language pairs and 328 CLI examples. Learner bundles were regenerated
and checked byte-for-byte; changed pairs have exact completion hashes in `docs/localization.json`, with no deferred translations.

**Not established:** no Azure call, recording or re-capture was made for this revision; the output-shape descriptions rest on the
pinned library source and the existing September 24 captures. No provisioning, deployment, role or default-subscription change,
publishing or push was performed. There was no human learner pilot, timing measurement or new editorial score.

<a id="straightforwardness-follow-through"></a>

## Straightforwardness: return paths, evidence and worksheets — September 24, 2026

**Four remaining contradictions were corrected English-first, then in Korean.**
Seven page pairs and the generated learner worksheets were updated. Foundry request logic, prompts, synthetic policies,
evaluation datasets, fixtures and recordings are unchanged.

| Friction found | Correction |
|---|---|
| A's terminal-preparation detour always returned to Lab 05, even before the learner had created an agent | [Lab 02's return table](../labs/02-models.md#a-terminal-ready) distinguishes starting A at Lab 00 from resuming Lab 05 |
| Lab 01's sketch, arrow and portal captions implied different resource hierarchies | Project and deployment are siblings under the Foundry resource; a separate dotted arrow shows the agent calling the deployment |
| Lab 06 changed the question across providers and implied that `answer` consumed the preceding retrieval file | Use one question in all four commands; [compare actual evidence](../labs/06-knowledge.md#retrieval-comparison) and state that `answer` performs another IQ retrieval |
| B saved workflow JSON automatically but the worksheet asked learners to copy it again | B records each saved file path and its human review; A still pastes its complete output. The original JSON files remain part of the handoff |

**ZIP review:** retain the two generated learner ZIPs. Each is approximately 20 KB and contains 16 files identical to the
uncompressed learner files. They provide one small download for browser-only A; B already has the files and needs no second ZIP.
The [setup card](../setup.md#learner-files) states this purpose. They are distribution artifacts, not separately maintained originals.

**Verification:** 271 offline tests passed on each of Python 3.13 and 3.14. Three new tests and the strengthened diagram test
cover the four corrections; both languages failed those checks before the changes. The local retrieval check finds
`TRAVEL-2026` and `APPROVAL-01` for the fixed question. Ruff 0.16.6 lint/format, Python compilation and documentation checks passed.
The documentation check covers 117 Markdown files, 58 language pairs and 328 CLI examples. Learner bundles were regenerated
and checked byte-for-byte; changed page pairs have exact completion hashes in `docs/localization.json`, with no deferred translations.

**Not established:** the revised same-question Search/IQ sequence has not been run against Azure or re-recorded.
Its existing captures are explicitly reference-only for that change. No Azure model/retrieval calls, provisioning, deployment, role/default-subscription
changes, publishing or push were performed. There was no human learner pilot, timing measurement or new editorial score.

<a id="straightforwardness-route-checks"></a>

## Straightforwardness: route and scope checks — September 24, 2026

**The default route now leads with what to do, what to save and where to stop.**
Fifteen English/Korean page pairs, including this record, were updated English-first.
No application code, prompts, datasets, policies, fixtures or media changed.

| Friction found | Change | Evidence |
|---|---|---|
| Entry pages asked for setup before the route choice; setup asked for notes before downloading them | Choose A/B → get the right files → collect values → Lab 00 | Regression tests check both entry sequences and file-before-card ordering |
| SDK explanation and optional hosting prerequisites interrupted core commands | Lab 02 has three numbered actions; Lab 08 packages first and keeps execution gates collapsed | Core-route tests still require exactly the existing commands and output files |
| The evaluation route mixed an action sequence with provider choices | A linked four-step map fixes local retrieval, names outputs and separates grading from the next decision | Tests verify every link, one core command per block and the pre-holdout gate |
| Instructor guidance called core B Search/MCP/workflows optional, but required the Hosted SDK | Rehearse the selected route; require Search for B and reserve Hosted SDK checks for selected modules | Instructor-scope regression test; no new cloud execution |
| A paid no-evidence diagnostic appeared in the core command lookup | Move it to optional commands; state which local checks write reports | Lookup regression test and bilingual CLI parity |

**Measured edit, not a reading-time claim:** the visible Markdown from Lab 08's B entry anchor to its first Bash block
fell from **1,118 to 298 characters in English** and **661 to 186 in Korean**. Counts include Markdown syntax and whitespace,
exclude collapsed sections, and compare this revision with the preceding worktree baseline. The command and package checks are unchanged.

**Verification:** 268 offline tests passed on **each of Python 3.13 and 3.14**. Seven new tests cover the route/scope rules;
the existing isolated journey test now also executes the README's `doctor`, `demo` and `evaluate` blocks in both languages,
confirming fixture `total: 6`, `passed: 6`, `errors: 0` without Azure. Ruff 0.16.6 lint/format checks and Python compilation passed.
The documentation check covers **117 Markdown files, 58 language pairs and 328 CLI examples**, plus local links/anchors.
Changed pairs have exact completion hashes in `docs/localization.json`; **no translation is deferred**.

**Not verified by this revision:** live Azure behavior, the installed-SDK suite, a human learner pilot or completion time.
No provisioning, deployment, role/default-subscription change, publishing, push or recording was performed.
The four-/six-hour schedules remain planned timings, not new measurements. No new editorial percentage is claimed.

<a id="straightforwardness-v3"></a>

## Straightforwardness review v3: guides and documents — September 24, 2026

<details>
<summary>Earlier AI editorial assessment — historical scores and evidence, not the result of the route review above</summary>

**Conservative editorial scores: guides 100/100 and documents 100/100** (round 1: 87/100 and 78.5/100).
Seven independent AI cold-read reviews covered the English A route, the English B route and the Korean guides with the
[v2 guide rubric](#guide-straightforwardness-v2), now including the collapsed optional sections, and two English and two Korean
document groups with a new document rubric. Each dimension takes the lowest reviewer score; D10 and R10 come from the Korean
reviews. Three rounds scored 87, 99.5 and 100 for the guides and 78.5, 89 and 100 for the documents. This is an editorial
assessment, not a human usability pilot, a learner-success rate or a measured completion time.

| Dimension | Guides: what earns full points | Round 1 | Final |
|---|---|---:|---:|
| D1 | Entry and route choice: README → setup → paths reaches the first action of either route | 10 | 10 |
| D2 | One linear core path; optional, owner and historical material is collapsed or marked | 9 | 10 |
| D3 | Numbered, imperative steps with exact UI labels, file names and values | 8.5 | 10 |
| D4 | A visible success or failure check after every action or command | 9 | 10 |
| D5 | Commands run as written, in order, with named output files | 9 | 10 |
| D6 | Plain, lean language without history or evidence commentary in the core path | 9 | 10 |
| D7 | Concrete recovery, including exactly what to ask the owner for | 9.5 | 10 |
| D8 | Explicit done criteria, correct A/B next links and a clear final handoff | 9.5 | 10 |
| D9 | Current, consistent model, date, screenshot and link claims | 7 | 10 |
| D10 | Korean pages mirror the English steps, commands, images and links and read naturally | 6.5 | 10 |

| Dimension | Documents: what earns full points | Round 1 | Final |
|---|---|---:|---:|
| R1 | Purpose, audience and the current answer come first | 7 | 10 |
| R2 | Headings, tables and anchors find a specific answer in seconds | 8 | 10 |
| R3 | Procedures are numbered and exact, with who does them and a success check | 8 | 10 |
| R4 | Numbers, flags, links and results agree with the guides, the CLI and the recorded evidence | 8 | 10 |
| R5 | Each fact lives in one place; dated history stays compact | 9 | 10 |
| R6 | Short sentences and explained terms | 9.5 | 10 |
| R7 | Brief, consistent evidence boundaries, Preview status and dates | 7 | 10 |
| R8 | Paid calls, cloud writes, roles and cleanup name who approves and who acts | 8 | 10 |
| R9 | Every page gives a next step; no dead links or links to removed material | 9.5 | 10 |
| R10 | Korean pages mirror the English facts, numbers, links and structure and read naturally | 4.5 | 10 |

**Main changes:**

- Conclusion first: coverage, versions, the evaluation workbook, IQ model identity and this page now open with the current state;
  dated history moved into dated table cells or collapsed blocks.
- Every extension module states its evidence status (date, preset, re-run or not with `gpt-6-sol`) under its opening line.
- The action index starts with an at-a-glance list of not-run, failed-and-kept, capture-tool and superseded actions;
  the results page keeps compact September 23 tables and points here for findings and Azure changes.
- Guides: Python 3.13/3.14 scope and the `--language en` note (README, Lab 00), checks after `az login` and Lab 01 step 4,
  the portal's dataset preview label and version choice (Lab 07 A), a no-traces stop in Lab 09's optional trace evaluation,
  Lab 08's B-only completion, Lab 10's optional scope and the IQ Chat capture's date.
- Korean parity: index, the paths C section, commands, versions, coverage, configuration, sources, instructor, migration,
  consolidation, cleanup and the routines and A2A modules now mirror the English pages; the Korean portal label **추적 번호**
  carries its meaning, and cleanup uses **일시 중지**.
- A broken official link (`…/workflows/as-agent`, HTTP 404) now points to `…/workflows/as-agents`, and the reference table gained
  six checked links used by the optional evaluation and Hosted steps.

**Verification for this revision:** 257 offline tests passed on each of Python 3.13 and 3.14, and 77 installed-SDK tests
passed with stub transports. Ruff, compilation, the CI offline commands in a clean copy and documentation checks
(117 Markdown files, 58 language pairs, 340 CLI examples) passed, with no pending translations.
A new test keeps both tables' rows and totals consistent.

**Live Azure checks for this revision: not run.** No model request, provisioning, deployment, role or subscription change,
or recording was performed. Portal labels were compared with the September 24 captures. Code, prompts, datasets, policies,
fixtures and media files are unchanged; only documentation and one test changed.

</details>

<a id="guide-straightforwardness-v2"></a>

## Guide straightforwardness review v2 — September 23, 2026

**Conservative editorial score: 98.5/100** (round 1, before these edits: 71.5/100).
Ten dimensions are scored from 0 to 10 in 0.5 steps. Each starts at 10 and loses 3, 2, 1 or 0.5 points per critical, major,
moderate or minor finding. Three independent AI cold-read reviews covered the English A route, the English B route and
Korean parity; each dimension takes the lowest of the three scores, and D10 comes from the Korean review.
Four review rounds scored 71.5, 83, 92.5 and 98.5. This is an editorial assessment of the prepared A/B guides,
not a human usability pilot, a learner-success rate or a measured completion time.

| Dimension | What earns full points | Round 1 | Final |
|---|---|---:|---:|
| D1 | Entry and route choice: README → setup → paths reaches the first action of either route | 7 | 10 |
| D2 | One linear core path; optional, owner and historical material is collapsed or marked | 8 | 10 |
| D3 | Numbered, imperative steps with exact UI labels, file names and values | 7 | 9.5 |
| D4 | A visible success or failure check after every action or command | 8 | 10 |
| D5 | Commands run as written, in order, with named output files | 7 | 10 |
| D6 | Plain, lean language without history or evidence commentary in the core path | 6 | 9.5 |
| D7 | Concrete recovery, including exactly what to ask the owner for | 8 | 10 |
| D8 | Explicit done criteria, correct A/B next links and a clear final handoff | 8.5 | 10 |
| D9 | Current, consistent model, date, screenshot and link claims | 6 | 10 |
| D10 | Korean pages mirror the English steps, commands, images and links and read naturally | 6 | 9.5 |

The final round's only finding, two English UI labels on the Korean setup card, was corrected afterward and not re-scored.

**Main changes:**

- One neutral start: README, the setup card and the path page give the same three steps and an A/B choice; Lab 05's
  prerequisite is Lab 00 B + Lab 02 B everywhere, and optional setup rows are collapsed.
- Portal steps use the exact paths and labels visible in the September 23 English and Korean captures; multi-action steps
  are numbered and each has a check.
- Blocked states name the owner request (Foundry User, Reader, `gpt-6-sol` quota, Search roles) instead of "resolve access".
- Lab 05 A saves `outputs/workflow-a-sequential.json` and names the evidence to expect; Labs 01 and 03 say which
  `session-notes.txt` lines to fill.
- Optional IQ Chat, B-only concepts and dated history moved below the core steps or into collapsed blocks.
- The [cleanup reference](cleanup.md) ends the course explicitly, with the same asset table and final checklist in both languages.

**Verification for this revision:** 245 offline tests passed on each of Python 3.13 and 3.14, and 67 installed-SDK tests
passed with stub transports. Ruff 0.16.6 lint/format, compilation, the CI offline commands in a clean copy and both learner
bundles passed. Documentation checks cover 117 Markdown files, 58 language pairs and 330 CLI examples, with no pending
translations. A new test keeps this table's rows and both totals consistent.

**Live Azure checks for this revision: not run.** No model request, provisioning, deployment, role/subscription change or
recording was performed. Portal labels were compared with the existing September 23 captures and recording action
definitions, not a new portal session. Canonical prompts, datasets, policies, fixtures and media files are unchanged;
only guide text, image placement and alt text, and one documentation test changed.

<a id="repository-straightforwardness"></a>

## Repository straightforwardness: guides, code and settings — September 17, 2026

Reviewed the guide entry points, all 61 language pairs, CLI command families, shared source contracts,
configuration templates and both CI workflows. The existing A/B routes and optional C boundaries remain intact.

| Friction | Change |
|---|---|
| Core B required 12 manual terminal-to-editor JSON copies | Each command now has a non-overwriting `--output` path; the same 12 files lead directly to review and handoff |
| Long CLI usage and generic help hid the first action and several advanced families | Short `COMMAND` usage, an offline starting sequence, distinct live-command help and a complete optional-family/code lookup |
| Malformed UUIDs and output limits produced parser errors without the setting name | Shared named UUID validation and explicit integer/range diagnostics; the model, identity and limits are unchanged |
| First-pass settings were mixed with advanced inputs; one reference template used an undeclared agent variable | Numbered minimal/Search/optional setup, documented Toolbox values and reference manifests aligned with the existing preparation helper |
| Local matrix smoke could silently use the source copy's old azd project | Require `--azd-directory` before smoke output or azd invocation; remote endpoint/version selection is unchanged |
| Documentation parsing rebuilt the same command tree for every example | One parser per check, with strict command, language and output-filename parity retained |

The regression checks exercise actual local JSON saving, both language paths, pre-request overwrite/scope rejection,
preserved stdout after a save race, failed requests, exact setting bounds and explicitly selected local smoke scope.
Source English changes precede Korean completion and hash recording.
This removes **12 required manual JSON-copy steps from B**, not its human review or business gates.
It is not a measured novice completion time or a new usability score.

**Local verification:** 253 offline tests passed on each of Python 3.13 and 3.14 without site packages;
67 installed-SDK tests passed with explicit stub transports.
Ruff 0.16.6 lint/format, compilation on both Python versions, dependency/import checks and both canonical learner bundles passed.
Documentation checks cover 123 Markdown files, 61 language pairs and 330 CLI examples, with no pending translations.

**Live Azure checks for this revision: not run.** No model/judge request, provisioning, deployment,
role/subscription change, recording or company/Microsoft 365 data access was performed.
Canonical prompts, datasets, policies, fixtures and earlier media remain unchanged.
Ignored personal `.env`, `.azure/`, `azure.yaml` and existing outputs are preserved; earlier Azure results do not verify the changed source hashes.

## Manual-assessment follow-through — September 17, 2026

The A/B entry and core-lab review found remaining ambiguity in A's six-question assessment.
The focused correction links [Lab 03's saved instruction snapshot](../labs/03-prompt-agent.md#path-a),
[Lab 07's assessment](../labs/07-evaluation.md#path-a), the learner ZIP's notes and the final handoff.

| Gap | Correction |
|---|---|
| Several assessment rows omitted exact required sources; D03/D06 also omitted the applicable limit | Match all six rows to the selected language's canonical dev amounts and citations; never copy expected IDs into an actual-response field |
| One worksheet could combine versions or a candidate could inherit filled baseline answers | One saved version per six-case sheet, named instruction snapshots and a fresh blank candidate only for a justified change |
| Request failures, unrun rows and a completed assessment could be confused with passing | Preserve the six-case denominator; record errors/unrun counts and incomplete work explicitly; keep all-pass/no-change as a valid stopping point |

**Offline result:** 232 tests passed on each of Python 3.13 and 3.14, including both languages' criteria and snapshot/notes/handoff checks.
Ruff 0.16.6 lint/format, compilation on both Python versions, deterministic learner bundles and documentation checks passed:
61 language pairs, 328 workshop CLI examples and no pending translations.

**Verification boundary:** these checks do not demonstrate novice completion time or a new usability score.
No new Azure calls, deployment, roles or recording were performed; canonical prompts, datasets, policies and prior media are unchanged.
Earlier review counts and live results below retain their original scope.

<a id="learner-action-review"></a>

## Learner-action and handoff review — September 17, 2026

Rechecked all **56 English/Korean core and extension lab pages**, their entry/setup/route guidance
and execution references. This pass addresses what to copy, what to save before moving on,
and how to leave an experiment without changing the next lab's setup.

| Gap | Correction |
|---|---|
| Shell commands, configuration blocks, placeholders and returned flags needed interpretation | Shared [code-block rules](../labs/00-start.md#reading-code-blocks), [result meanings](commands.md#reading-results) and plain-language naming terms |
| Printed JSON filenames appeared only after several requests; B's final list omitted model outputs and the workflow review | A Save checkpoint after each of the 12 printed B results and a complete [handoff inventory](../labs/11-capstone.md#b-evidence) |
| First-agent D03/D05 checks were less explicit than the later assessment | The same canonical dev limit and required citations, including `SCOPE-01`, at the first check |
| The workflow diagram suggested an automatic human-rejection loop | The actual JSON stopping point and the learner's separate review, without an implied approval service |
| Model comparison permanently changed `.env`, with a second abbreviated recipe elsewhere | One complete model-operations route; command-scoped overrides preserve the original file and terminal setting on success and failure |
| Skill, A2A and routine examples accepted empty scope values at the shell boundary | Required name/version/endpoint guards before azd; values come from this pass's actual setup/results |
| Readback reruns and routine enable failures lacked an explicit stopping point | Reject an existing readback directory before downloading again; compare only after a successful download, dispatch only after enable, and still disable/read back after failure |
| Korean evidence links opened the wrong language's results, and one refusal-review instruction reversed the meaning | Link the independent English/Korean results explicitly; do not reclassify a correct approval refusal as an error |

**Local acceptance:** 231 offline tests passed on each of Python 3.13 and 3.14.
Ruff 0.16.6 lint/format, Python compilation, both deterministic learner bundles and documentation checks passed:
61 language pairs, 328 workshop CLI examples and no pending translations.
Seven new regression tests check exact saved filenames/dev criteria and execute the changed shell blocks
with explicit local stubs, including missing/empty values, failures and byte-preserving reruns.
The source guide was checked first, then the Korean counterpart and exact completion hashes were updated.

**Evidence boundary:** this is a guide-only revision, not a new usability score or measured completion time.
No new live Azure/model/judge call, deployment, role assignment, recording or novice pilot was performed.
Canonical prompts, policy/evaluation/fixture data and existing media are unchanged.
The earlier reviews and live outcomes below retain their original scope and counts.

<a id="whole-guide-review"></a>

## Whole-guide straightforwardness review — September 17, 2026

Reviewed **all 12 core labs and 16 extension labs in both languages (56 lab pages)**,
alongside the entry pages, route/setup/instructor guidance and executable reference workbooks.
The review checks whether a learner can identify the next action, its prerequisites,
the expected artifact, the stopping point and recovery without guessing.
It extends beyond the prepared A/B-only assessment below; it does not assign a new usability score.

| Remaining gap | Change |
|---|---|
| B setup still appeared to require the browser ZIP and optional hosting checks | Separate A/B material acquisition; make the full SDK check a selected-module prerequisite |
| C looked like a chain of every capability | A complete module catalog, explicit first-pass ranges, optional promotion/OpenAPI/crash/Router branches and handoff links |
| Hosted commands depended on whichever project the shell found | Explicit, guarded directory/service/version values in Toolbox, safety, matrix and session cleanup |
| A second remote smoke attempt could overwrite the first stream | New evidence directory, preserved raw output and failure-aware invocation/verification |
| Advanced IQ setup still required template initialization and manual YAML merging | Separate `--kind matrix` package preparation; preserve both V1/V2 source copies and exact runtime settings |
| Local matrix smoke still selected the source project's azd state | Explicit local `--azd-directory`, with evidence retained under the source copy |
| Default matrix commands assumed an optional reviewed regression existed | No-regression default, explicit opt-in for consumed reviews, and a visible per-model dev gate before holdout |
| Learner cleanup and language order included outdated maintainer instructions | Browser-compatible cleanup handoff, collapsed media maintenance and the active localization order |

**Local acceptance:** 224 offline tests passed on each of Python 3.13 and 3.14.
Ruff 0.16.6 lint/format, Python compilation, both deterministic learner bundles and documentation checks passed:
61 language pairs, 332 workshop CLI examples and no pending translations.
All guide Bash blocks are syntax-checked without cloud execution; the selected failure-path tests use explicit local stubs.

The associated checks exercise actual local package/manifest generation, invalid-scope rejection,
command blocks with stubbed azd failures, preservation of existing output bytes and language/command parity.
The matrix helper retains the existing `runtime`, Toolbox and CI contracts; it does not provision, deploy,
grant roles, change model/provider, or install a runtime.
Canonical prompt/dataset/corpus/fixture assets and existing media are unchanged.

**Evidence boundary:** no new live Azure/model/judge call, deployment, role assignment, recording or novice pilot.
The historical 95/100 below remains an initial editorial self-assessment, not a completion rate or a rating of the new advanced setup.

<a id="follow-through-review"></a>

## Follow-through review — September 17, 2026

The second review followed configuration, file handoff and optional Hosted setup from the `5cce55b` guide,
rather than treating its editorial score as proof that every learner could finish.
It found gaps the initial structural checklist did not establish:

| Gap | Correction | Evidence boundary |
|---|---|---|
| A new language/label can still conflict with the old Search ownership scope | Exact `mfv2-` grammar, one-copy/scope rules and an explicit instructor ownership handoff | Language/prefix-change refusals reproduced locally before any network request; the old ledger remains unchanged |
| B can enter from the source copy without receiving the browser worksheets | Executable, non-overwriting notes preparation; named JSON outputs and B-specific worksheet fields | Actual file copies and rejected reruns are tested, not inferred from links |
| A blocked dev gate leaves no clear end-of-session handoff | Separate complete, rejected and incomplete handoffs; no acceptance command for absent runs | Missing work stays incomplete; holdout and business thresholds are not weakened |
| Optional Hosted setup requires manual YAML merging and relies on shell state | Reuse the package-verifying helper with `--kind runtime`, a separate directory and guarded, service-scoped azd commands | Actual manifest generation plus stubbed environment/readback contracts; missing scope variables stop before azd runs |

The preparation helper supports only language-matched **local/v2/project-Responses** introductory packages.
The existing Toolbox and CI Invocations contracts remain distinct. No model or retrieval fallback was added.
`cleanup-plan` now links to the selected language's cleanup guide.
Official manifest documentation and installed azd help were reviewed on September 17; this is **not a new Azure deployment result**.

The checks verify concrete behavior, including safe copies, directory/profile rejection and missing-value guards.
The editorial-table test checks arithmetic and the unrun pilot, **not a hardcoded 95-point outcome**.
The earlier score below remains an initial self-assessment; no additional usability points or novice completion rate are claimed.
Canonical prompts, policy/evaluation/fixture data and existing media remain unchanged.
No new paid model/judge call, resource/role change, Azure deployment or novice pilot was performed for this review.

**Local acceptance of this follow-through revision:** 215 offline tests passed on each of Python 3.13 and 3.14.
Ruff 0.16.6 lint/format, Python compilation, both deterministic learner bundles and documentation checks passed
(61 language pairs, 332 workshop CLI examples, no pending translations).
The scope-guard tests use a local azd stub and cover both unset and empty values; they do not run a deployment.

<a id="guide-straightforwardness"></a>

## Initial guide straightforwardness assessment — September 17, 2026

**Self-assessed editorial acceptance: 95/100.** This is an explicit rubric for the **prepared A/B core guides**,
not an independent usability benchmark, a 95% learner-success rate, or a rating of every optional C integration.
Each criterion is worth **5 points**. Source review and the checks below support criteria 01–19.
Criterion 20 receives **0**, because no fresh novice pilot was performed; the advertised hours remain prepared-course allocations, not newly measured completion times.

| # | Acceptance criterion — 5 points each | Evidence | Awarded |
|---|---|---|---:|
| 01 | Setup is the first action; background/videos are not prerequisites | [README](../../README.md) and entry-page checks | 5 |
| 02 | One route and first-pass presets are chosen before execution | [A](../paths/a-beginner.md) / [B](../paths/b-practitioner.md) | 5 |
| 03 | Both nine-step sequences include handoff; schedules total 240/360 minutes | [Schedules](../paths.md) and route-order assertions | 5 |
| 04 | All 36 route steps across both languages have visible entry/exit links to the correct section | [Journey tests](../../tests/test_learner_journey.py) | 5 |
| 05 | Every numbered lab has scope, prerequisites, completion and recovery in one start card | All 24 language lab pages and start-card assertions | 5 |
| 06 | A contains only its one prepared workflow command, not B code or holdout | [A route](../paths/a-beginner.md) and extracted-command assertions | 5 |
| 07 | B's core commands exclude optional judges, hosting and Preview branches | [B route](../paths/b-practitioner.md) and extracted-command assertions | 5 |
| 08 | Owner preparation and optional settings do not interrupt the prepared learner route | [Setup](../setup.md); owner commands are collapsed | 5 |
| 09 | Paid model/retrieval calls, cloud writes and local-only work are distinguished before execution | Lab 02/04/05/06/07/08 scope and command notes | 5 |
| 10 | Learner ZIP and source ZIP have distinct purposes and acquisition steps | [Setup](../setup.md) / [Lab 00](../labs/00-start.md#path-b) | 5 |
| 11 | Ready instructions and questions use the frozen synthetic inputs, without answer keys or holdout | [Learner-material tests](../../tests/test_learner_materials.py) | 5 |
| 12 | Blank evidence templates supply the same filenames required at handoff | [Learner bundle](../../data/README.md) / [Lab 11 A](../labs/11-capstone.md#path-a) | 5 |
| 13 | The browser assessment requires all six real answers, citations and review reasons | [Lab 07 A](../labs/07-evaluation.md#path-a) and worksheet assertions | 5 |
| 14 | Documented output fields and filenames match actual CLI artifacts | Executed offline comparison; no invented comparison fields | 5 |
| 15 | The evaluation mainline is steps 1–4 with a six-case candidate gate before four-case holdout | [Lab 07 B](../labs/07-evaluation.md#path-b) and command/gate assertions | 5 |
| 16 | Resume instructions distinguish local reinspection, a new collection and polling an existing job | [Recovery table](troubleshooting.md#resume-safely); existing fixture bytes survive a rejected rerun | 5 |
| 17 | Package-only and cleanup-plan outputs cannot be mistaken for deployment or deletion | Executed [Lab 08 B](../labs/08-hosted.md#path-b) / [Lab 09 B](../labs/09-operations.md#path-b) CLI examples | 5 |
| 18 | English/Korean commands, links and active-revision file hashes agree | [Documentation tests](../../tests/test_documentation.py) / [localization record](../localization.json) | 5 |
| 19 | Synthetic-data lineage, errors and unverified outcomes remain explicit; older footage is not new proof | [Frozen data hashes](../../data/localization.json), offline contracts and dated records below | 5 |
| 20 | New learners independently finish the prepared routes, with intervention and elapsed-time records | **Not run — no points awarded** | 0 |

**Verification for this revision:** complete offline suites passed on Python 3.13 and 3.14, together with
Ruff 0.16.6 lint/format, Python compilation, deterministic learner bundles, and documentation checks
(61 language pairs, 332 workshop CLI examples, no pending translations).
The guide's offline commands run in temporary copies with no `.env`, inherited Azure credentials or installed SDKs.
They verify actual files, the intentional fixture 0/6 versus 6/6, comparison fields, exit codes, byte-preserving label rejection,
`cloud_deployed: false` packaging, and non-deleting cleanup. Fixture scores are **not model-quality measurements**.

Only the guide, blank learner worksheets and their checks changed. Canonical prompts, policy/evaluation/fixture data and recorded media remain unchanged.
**No new live Azure run, deployment, role assignment, paid evaluation, SDK integration run or recording is claimed for this revision.**
The historical results below retain their original scope and dates.

</details>

<details>
<summary>Earlier execution and media records, September 15–17, 2026 — earlier model editions, not `gpt-6-sol` evidence</summary>

## IQ Chat configuration screen — September 17, 2026

The new [Lab 06 screen](../labs/06-knowledge.md#iq-chat-model) shows an existing saved chat KB with
Luna, Low, Answer synthesis and the matching active synthetic source. The guide now distinguishes that
ready state from the old model-free GA form and its missing-model validation.
The current Foundry model catalog was inspected without deploying anything; opening the saved Luna binding works even though the quick catalog omits it.

This is **live portal observation and read-only deployment verification**, not a new model invocation or evaluation.
The gray MI notice remains visible and is not misreported as an authentication error or proof of permissions.
Fresh PNGs are direct captures of the configuration panel, with no text replacement, error hiding or image editing.
The [capture record](../assets/iq-chat-20260917/captures.json) records language, values, image hashes and verification limits separately from earlier videos.

**Offline verification:** 235 tests passed on each of Python 3.13 and 3.14, including the new screenshot hashes,
complete form values and historical-image boundaries. Ruff 0.16.6 lint/format, compilation and both learner bundles passed.
Documentation checks cover 61 language pairs and 328 CLI examples with no pending translations.

## Extension acceptance — September 17, 2026

The September 16 English/Korean extension source is now checked separately from the historical cohorts below:
**200 offline tests on each of Python 3.13 and 3.14, 67 installed-SDK transport tests**, Ruff check/format,
Python compilation, dependency compatibility and deterministic learner bundles passed.
Documentation checks cover **61 language pairs and 332 executable workshop examples**, with no pending translations.

The English extension has 166 actions, 496 captures and 368 retained source segments;
the independent Korean extension has 172 actions, 516 captures and 363 segments.
Minimum midpoint SSIM is **0.982302 / 0.983325** respectively.
All six extension videos played locally, and every one of the 15 chapter seeks in each combined video
waited for seek completion and a decoded frame. Korean reboot parts keep their own video epochs;
authentication transitions and source tails are explicitly excluded.

The September 16 English and Korean result pages preserved actual failures (removed on September 23, 2026; see git history at `47f3b49`).
The Optimizer's self-referential grounding inputs are not accepted as source verification or a promotion gate.
The separate conversation evaluations retained the original policy JSON in their actual judge inputs.
The Korean safety D06 tool-discovery failure remains a failed response despite CLI exit 0.
On September 17, all six extension attachments were also verified against their actual private GitHub bytes,
native playback and completed chapter seeks. The manually dispatched CI run remains a separate execution check,
not something inferred from local tests or published video URLs.

The first GitHub check exposed a missing SDK-test development dependency, and the initial release dispatch
was rejected because `runner.temp` was used before the runner context exists.
The SDK job now installs the declared `dev` extra, and the release initializes its path from `$RUNNER_TEMP`
inside a step and passes it through `$GITHUB_ENV`. Regression checks and actionlint 1.7.12 workflow
schema/expression validation passed; the original failed GitHub result remains in its run history.
The corrected [GitHub repository check](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35121096979)
passed all jobs. A subsequent OIDC mismatch was narrowed to the exact immutable subject emitted by this repository;
the existing federation was corrected without new credentials, broader roles or weaker GitHub settings.
The [actual OIDC release](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35121162793)
then passed on attempt 2: Korean dev 6/6, zero errors, original artifact hashes and recomputed business checks verified,
with the exact created session independently confirmed idle. This post-publication run did not execute native judging or holdout.

## Korean prerequisite run — September 15, 2026

The existing Sweden Central workshop project was reused; no default subscription or resource group was changed.
Approved Sol/Terra/Astra deployments were added at 100K TPM with minimum scoped model/Search roles.
Existing Luna, judge, and embedding deployments were reused.

| Cohort | Version | Rows | Errors | Business | Groundedness | Relevance | Root traces |
|---|---:|---:|---:|---:|---:|---:|---:|
| `ko-baseline-final` | 7 | 24 | 0 | 24/24 | 24/24 | 19/24 | 24/24 |
| `ko-candidate` | 8 | 24 | 0 | 24/24 | 22/24 | 20/24 | 24/24 |
| `ko-holdout` | 8 | 16 | 0 | 16/16 | 16/16 | 13/16 | 16/16 |

Calibration classified both prewritten correct/incorrect examples as expected.
It did not create two new target responses or certify the judge generally.
The initial version-6 diagnostic cohort remains separate.

The recommendation is `review-native-findings`, not production approval.
Correct abstentions can score poorly on generic relevance. Scores and reasons remain unchanged.
No failure or regression promotion was manufactured for an all-pass baseline.
The public holdout teaches final acceptance; it is not an unseen production test.

## Independent English run — September 15, 2026

English prompts, corpus, dev/calibration/fixtures and final holdout are separate frozen assets.
The initial version-10 baseline was **20/24**: IQ's default retrieval filter omitted the scope document.
That entire cohort remains unchanged. An explicit same-provider recall diagnostic led to a new baseline/candidate pair;
the evaluator/reference labels and frozen prompts were not weakened or tuned on holdout.

| Cohort | Version | Rows | Errors | Business | Groundedness | Relevance | Root traces |
|---|---:|---:|---:|---:|---:|---:|---:|
| `en-baseline-recall` | 11 | 24 | 0 | 24/24 | 24/24 | 20/24 | 24/24 |
| `en-candidate` | 12 | 24 | 0 | 23/24 | 24/24 | 20/24 | 24/24 |
| `en-holdout` | 12 | 12 | 0 | 12/12 | 12/12 | 9/12 | 12/12 |

Astra failed the predeclared citation-relevance check on dev D05.
Only Luna/Sol/Terra were selected **using dev results before any holdout response**; the final denominator is 12, not 16.
The original four-model candidate remains 23/24. English calibration classified both fixed examples correctly.
The D05 regression candidate remains pending human review and was not promoted/consumed without approval.
The full September 15 English lineage page was replaced on September 23, 2026 (git history at `47f3b49`); neither language's outcomes are copied into the other.

## Corrections established by actual calls

Endpoint/protocol CLI conflicts, dropped API-version query parameters, explicit account embeddings,
App Insights credential scoping, and already-idle session cleanup were fixed while preserving original failures.
Changed runtime versions and controlled comparisons remain separately labeled.

## Media evidence — September 15, 2026

These recordings were removed from the working tree on September 23, 2026 (git history at `47f3b49`).
The Korean set contains 182 actions, 543 lossless screenshots, and three edited videos.
Published WebP pixels exactly match source PNGs.
All 435 retained source-video segments were compared, with minimum midpoint SSIM 0.987849.
Full MP4 decoding and frame counts were checked; chapter cards are labeled as non-application footage.

Authentication/password entry is excluded. Failures and diagnostics remain in the source ledger.
One portal trace showed 17 spans/two chat calls while the response recorded three actual model calls:
root trace verification is not proof that every child span was exported.
The six uploaded synthetic files were read back through the Files API and matched byte-for-byte.
An unconfirmed UI citation download was not reported as successful.

The English set has **172 actions, 516 lossless captures, three videos and 407 checked source-video segments**.
Its minimum midpoint SSIM is **0.985156**. Actual native playback, byte ranges and all 12 chapter jumps were verified for each language.
All six new videos were uploaded as private-repository GitHub attachments after user approval.
Their actual hosted bytes/hashes, native playback, and chapter seeks were verified.
Only canonical attachment URLs are saved; temporary signed storage URLs are not retained.
Older current-worktree media files were removed only after both replacements passed these checks.

## Guide and IQ preset revision — September 15, 2026

All 24 language lab pages now have scope, prerequisites, completion/recovery and next-step cards.
The A route includes its capstone and totals 240 minutes **after preparation**.
Ready browser instructions, questions-only files and blank assessments derive from canonical v2/policies/dev;
neither reference-answer columns nor holdout enter the learner ZIP. Original prompts/datasets and media were not changed.

The final **read-only Azure preflight** confirmed `gpt-5.6-luna` / `2026-07-09` in `Succeeded` state,
the actual Search system-assigned identity, its documented account role, and the intended synthetic source.
It returned `ready_for_setup: true`, **`configured: false`**, `model_inference_verified: false`, and `cloud_changes: false`.
The new permanent chat base was **not created**. No new role assignment, deployment or paid inference/evaluation was performed for this revision.

The earlier successful MI binding/response was replayed **locally**, without another Azure request.
This confirmed API-key `null` serialization and the actual `id/title/content` source projection.
Returned fields are checked against the canonical corpus; missing date fields are not invented.
Transport tests cover configuration/model drift before paid requests, explicit errors, ownership, and preserved failures.

These checks are not a new end-to-end Azure run, a novice classroom pilot, or a rerecording of the revised preparation steps.
Earlier live scores/footage retain their original versions and hashes; they do not prove execution of the newly changed code.

**Local verification for that revision:** 126 offline tests on each of Python 3.13 and 3.14, 27 installed-SDK tests, Ruff check/format,
Python compilation, dependency compatibility, and documentation checks passed.
Documentation checks covered 37 language pairs and 218 CLI examples, with no pending translations.
Both deterministic learner bundles matched their canonical inputs on Python 3.13 and 3.14.

</details>
