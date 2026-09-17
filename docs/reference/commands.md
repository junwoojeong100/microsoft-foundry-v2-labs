# Command quick reference

**English** | [한국어](../ko/reference/commands.md)

**Run all commands from the repository root. Do not shell-`source` `.env`.**
Activate the dedicated virtual environment for cloud SDKs.

**Lookup table, not an execution sequence.** Rows without `python scripts/...` are abbreviated:
prefix workshop commands with `python scripts/workshop.py --language en`.
Do not paste `...` or run every row; use the selected lab's complete block and approval boundary.
[Code-block rules](../labs/00-start.md#reading-code-blocks) explain placeholders, prompted values and where each block belongs.
[Read the result](#reading-results) before deciding that a successful command means the lab passed.

| Command | Azure/side effects | Purpose |
|---|---|---|
| `python scripts/workshop.py --language en doctor` | None | Python/synthetic-data checks |
| `doctor --cloud` | Read-only | Explicit subscription/tenant/deployment/token preflight, not inference |
| `demo --label demo-v2 --prompt v2` | Local output only | Fixed fixture |
| `retrieve --provider local` | None | Local keyword search |
| `retrieve --provider search` | Possible Search charges | Ordinary search |
| `retrieve --provider iq` | Possible IQ charges | GA knowledge-base retrieval |
| `model --question "question"` | Paid model call | Direct Responses |
| `answer --prompt v2 --retrieval local` | Paid model call | Structured answer with sources |
| `maf --tools` / `maf --mcp` | Paid model calls | Read-only function / local MCP |
| `workflow --pattern sequential` | Paid model calls | Alternatives: concurrent, group-chat |
| `seed-search --confirm-create` | Creates/uploads owned Search objects | Existing service only |
| `seed-search --iq --confirm-create` | Above plus GA source/base | Ownership checks |
| `iq-chat check` | Read-only | Fixed Luna/version, Search identity/role/source and separate chat-base readiness |
| `iq-chat setup --confirm-create` | Creates only the owned Preview chat base | No model deployment, role assignment or GA-base rewrite |
| `iq-chat ask --label iq-chat-first --confirm-cost` | Paid planning/synthesis | Fixed Luna + Search MI; saves raw response, source evidence and failures |
| `prompt-agent create ... --confirm-create` | Creates an actual agent version | Exact prefix required |
| `prompt-agent invoke ... --version ...` | Calls a real agent | Explicit version |
| `collect --label baseline --prompt v1` | Paid calls for all dev cases | Preserves errors; concurrency one |
| `evaluate --label baseline` | None | Deterministic business checks |
| `compare --baseline baseline --candidate candidate` | None | Controlled dev comparison |
| `feedback --label baseline --case D03 --reason "specific review reason"` | Local review record | Real dev only; pending approval |
| `cloud-evaluate --label candidate --confirm-cost` | Paid cloud judge | Evaluator version and job lineage |
| `collect --split holdout ... --candidate candidate --unlock-holdout` | Frozen candidate's actual final requests | No reuse for development |
| `accept --candidate candidate --holdout final-holdout` | None | Human acceptance evidence, not automatic approval |
| `serve` | Local server; paid model on invocation | Hosted SDK needed |
| `cleanup-plan` | None | Deletes nothing; returns the cleanup guide for the selected language |
| `python scripts/export_policy_docs.py --language en` | Creates six local text files | Optional export; A's learner ZIP already contains them |
| `python scripts/build_learner_materials.py` | None | Checks both committed learner bundles against canonical dev/prompt/policy inputs |
| `python scripts/build_learner_materials.py --write` | Regenerates the two local learner bundles | Maintainer-only generation; no model or holdout use |
| `python scripts/package_hosted.py --language en` | Local package | No deployment/installation |
| `python scripts/prepare_hosted_azd.py --language en --kind runtime ...` | Local package-verified project; `--initialize-env` also creates/read-checks local azd state | Introductory local v2 Responses packages only; no provision/deploy/role assignment |
| `python scripts/prepare_hosted_azd.py --language en --kind matrix ...` | Local package-verified IQ matrix project and optional azd state | Sequential IQ/account-chat/Invocations v1/v2; exact model map and Search settings, no deployment |
| `python scripts/play_recordings.py` | Localhost video server | English by default; `--edition ko` selects the independently recorded Korean set |

Abbreviated rows are not complete executable examples. Read
`python scripts/workshop.py --language en --help` and subcommand `--help` for required arguments.
Full commands appear in the [labs](../paths.md).
For the first IQ Chat setup, use [the owner sequence](../setup.md#4-environment-owner-checklist) once;
the default GA `retrieve --provider iq` is intentionally a different path.

Interactive `model`/`answer`/`maf`/`workflow`/`retrieve` commands print JSON; use [B's notes directory](../labs/00-start.md#prepare-notes)
for complete copied outputs. Batch runs already write `outputs/<label>/`.
For the complete standalone Hosted preparation command and its required values, use [Lab 08](../labs/08-hosted.md).

<a id="reading-results"></a>

## Finished, verified or accepted?

| What you see | What it means / next action |
|---|---|
| The shell prompt returns | The process finished. Read its output and error; this alone is not a passed check |
| Offline `doctor` says `result: PASS`, `azure_tested: false` | Local inputs/runtime passed. Azure access and inference are still untested |
| `model_invoked: false` in a Toolbox probe | Expected for discovery-only work; do not report a model answer |
| `evaluate` / `accept` exits `1`, `business_gate_passed: false` | Keep the failed business result and inspect every case. Do not lower criteria or unlock holdout for a failing candidate |
| `trace_id: null`, `cloud_deployed: false` or `deployment_approved: false` | An explicit unverified/unperformed stage, not a value to edit into success |
| `pending-human-review` / `ready-for-human-review` | A person still needs to review; no business approval or deployment permission was granted |
| A service error, missing response or failed row | Preserve the exact attempt and use [recovery](troubleshooting.md#resume-safely). A later read/list success does not erase it |

For this workshop CLI, exit `2` identifies an input/configuration/dependency/precondition error.
Do not assume other tools use the same codes. Missing measurements stay missing, never zero.

<a id="saved-results"></a>

## Find a saved result

Use the directory printed by the command, not `outputs/<label>/` for every module.
Keep an existing run and all failures; a new target request needs a new label.

| Run family | Location under the source repository |
|---|---|
| Introductory `demo` / `collect` | `outputs/<label>/` |
| `benchmark smoke` | `outputs/smoke/<label>/` even when local azd uses another directory |
| `benchmark collect` | `outputs/benchmarks/<label>/` |
| `iq-chat ask` | `outputs/iq-chat/<label>/` |
| Toolbox `probe` / `query` / `ask` | `outputs/toolbox-runs/<label>/`; ownership stays in `outputs/toolboxes/<name>/` |
| `conversations collect` | `outputs/conversations/<label>/`; both native evaluation levels stay with that collection |
| `memory recall` | `outputs/memory-runs/<label>/`; store ownership is separate |
| Code Interpreter / OpenAPI / A2A | `outputs/code-interpreter/<label>/`, `outputs/openapi-runs/<label>/`, `outputs/a2a-runs/<label>/` respectively |

Add `--debug` before a subcommand for local diagnostics. Stack/service errors can
contain environment paths; do not publish raw logs.
Commands do not overwrite existing run labels. Never alter raw responses or scores
to bypass hash verification.

English uses `--language en` with its own frozen policies/prompts/datasets.
The other operational flags and schema remain aligned with Korean.
Approved free-text query translations are explicit in `data/guide-questions.json`.

## Hosted workflow and evaluation extension

Prepend `python scripts/workshop.py --language en` to these abbreviated commands.

| Command | Contract |
|---|---|
| `runtime-contract --kind workflow ...` | Local profile, language, model map and data/prompt/code hashes |
| `workflow-agent --pattern sequential` | Actual case-isolated MAF pipeline with one validated answer |
| `seed-search --hybrid --confirm-create --confirm-cost` | Real embeddings and a separately owned vector index |
| `retrieve --provider hybrid` | Combined text/vector search, not a renamed keyword query |
| `benchmark plan` | Model/case/cost shape only; no Azure call |
| `benchmark smoke --local --azd-directory ...` | Actual local host plus billable model; explicitly selects the prepared azd directory while keeping evidence in the source copy |
| `benchmark smoke` | Exact remote version/endpoint, no gold labels in requests |
| `benchmark collect` | Complete explicit model-by-case matrix; errors retained |
| `benchmark evaluate --reference ...` | Actual native scores with a pinned catalog/version/judge |
| `benchmark compare` | Same dataset/corpus/code/model/API/retrieval/concurrency; no cross-language shortcut |
| `benchmark regression ... --confirm-review` | Explicit dev review and preserved source lineage |
| `--regressions <reviewed-label>` | The next dev collection actually consumes reviewed references |
| `calibrate-judge` | Prewritten correct/incorrect answers test the actual judge |
| `benchmark trace-plan` / `monitor` | Local KQL versus actual scoped App Insights verification |
| `benchmark verify` | Independent acceptance gates; not production approval |
| `benchmark stop-session` | Stop only the recorded session/version or confirm it is already idle |

Complete commands and approval boundaries are in the [evaluation workbook](evaluation-workbook.md).
