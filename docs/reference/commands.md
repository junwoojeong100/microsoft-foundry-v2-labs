# Command quick reference

**English** | [한국어](../ko/reference/commands.md)

**Run all commands from the repository root. Do not shell-`source` `.env`.**
Activate the dedicated virtual environment for cloud SDKs.

**Lookup table, not an execution sequence.** Rows without `python scripts/...` are abbreviated:
prefix workshop commands with `python scripts/workshop.py --language en`.
Do not paste `...` or run every row; use the selected lab's complete block and approval boundary.
[Code-block rules](../labs/00-start.md#reading-code-blocks) explain placeholders, prompted values and where each block belongs.
[Read the result](#reading-results) before deciding that a successful command means the lab passed.

## Core B and offline lookup

Follow [B's ordered route](../paths/b-practitioner.md), not this table from top to bottom.

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
| `collect --label baseline --prompt v1` | Paid calls for all dev cases | Preserves errors; concurrency one |
| `evaluate --label baseline` | None | Deterministic business checks |
| `compare --baseline baseline --candidate candidate` | None | Controlled dev comparison |
| `feedback --label baseline --case D03 --reason "specific review reason"` | Local review record | Real dev only; pending approval |
| `collect --split holdout ... --candidate candidate --unlock-holdout` | Frozen candidate's actual final requests | No reuse for development |
| `accept --candidate candidate --holdout final-holdout` | None | Human acceptance evidence, not automatic approval |
| `cleanup-plan` | None | Deletes nothing; returns the cleanup guide for the selected language |
| `python scripts/package_hosted.py --language en` | Local package | No deployment/installation |

Abbreviated rows are not complete executable examples. Read
`python scripts/workshop.py --language en --help` and subcommand `--help` for required arguments.
Full commands appear in the [labs](../paths.md).

<a id="saving-json"></a>

## Save one response without copying terminal text

`model`, `answer`, `maf`, `workflow`, `workflow-agent` and `retrieve` accept **`--output FILE` after the command**.
They still print the same JSON and save that complete object without changing response IDs, sources, usage or unverified fields.
Core B already supplies all 12 filenames. Prepare [the notes directory](../labs/00-start.md#prepare-notes) once.

For an extra **local-only** retrieval example after that preparation:

```bash
python scripts/workshop.py --language en retrieve --provider local \
  --output outputs/learner-notes-en/retrieve-example.json
```

The file must be a new `.json` under this source copy's `outputs/`, with an existing parent directory.
Existing files and unsafe paths are rejected **before the request**. Open the existing result to resume; use a new filename only for a new request.
Without `--output`, the print-only behavior is unchanged.

`Saved JSON: ...` appears on stderr; stdout remains the JSON. **Saved is not assessed or approved.**
A failed request creates no successful-response file. If the response printed but saving failed, preserve that stdout and the error;
save it manually rather than repeating a paid call. `collect`/`evaluate` and advanced run families already manage their own evidence directories;
do not add `--output` to them or replace their manifests with an exported response.

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
| Interactive commands with `--output` | The exact file you selected; core B uses `outputs/learner-notes-en/*.json` |
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

## Optional command families

<details>
<summary>Choose only the module you selected — these are not extra core-B steps</summary>

Local plans can need the selected module's SDKs and `.env` even when they make no Azure request.
Every family's own `--help` and linked lab specify its required values and create/cost/delete approvals.

| Family | Purpose / boundary | Complete guide |
|---|---|---|
| `prompt-agent` | Create/invoke a separately versioned managed agent, not the local MAF agent | [Lab 03 SDK branch](../labs/03-prompt-agent.md) |
| `iq-chat` | Fixed Luna/SMI preflight, owned chat-base creation, then billable planning/synthesis | [Owner setup](../setup.md#4-environment-owner-checklist) |
| `workflow-agent` / `runtime-contract` | Validated workflow output / local frozen profile and hashes | [Lab 05 C](../labs/05-workflows.md) |
| `benchmark` | Version-pinned Hosted smoke, matrices, evaluation, traces and acceptance | [Evaluation workbook](evaluation-workbook.md) |
| `cloud-evaluate` / `calibrate-judge` | Billable native judges on recorded responses / separate calibration fixtures | [Lab 07](../labs/07-evaluation.md), [workbook](evaluation-workbook.md) |
| `serve` | Local host; inference is still billable | [Lab 08](../labs/08-hosted.md) |
| `toolbox` | Owned managed tools, versions, readback and MAF calls | [Toolbox](../labs/extensions/toolbox.md) |
| `prepare-extensions` | Local advanced inputs from bundled dev/policies only; never holdout | [Developer tools](../labs/extensions/developer-toolkit.md) |
| `conversations` | Multi-turn dev collection and separate turn/conversation evaluation | [Conversation evaluation](../labs/extensions/conversation-evaluation.md) |
| `memory` | Explicit synthetic store/scope lifecycle, not automatic agent memory | [Memory](../labs/extensions/memory.md) |
| `a2a` | Owned A2A 1.0 target/caller and recorded delegation | [A2A](../labs/extensions/a2a.md) |
| `routines` | Inspect an existing dispatch; delivery alone does not prove a target response | [Routines](../labs/extensions/routines.md) |
| `code-interpreter` / `openapi` | Generated synthetic-policy CSV / read-only query of the owned Search index | [Additional tools](../labs/extensions/additional-tools.md) |

The default GA `retrieve --provider iq` is deliberately different from the optional `iq-chat` model-based path.

### Supporting scripts

| Script | Purpose / side effect |
|---|---|
| `scripts/export_policy_docs.py --language en` | Optional local six-file export; A's learner ZIP already contains it |
| `scripts/build_learner_materials.py` | Check both committed learner bundles; maintainer `--write` regenerates them without model/holdout use |
| `scripts/prepare_hosted_azd.py --kind runtime` | Generate the separate local v2 Responses project from a verified package; [Lab 08](../labs/08-hosted.md) supplies the complete command |
| `scripts/prepare_hosted_azd.py --kind matrix` | Separate sequential IQ/account-chat/Invocations v1/v2 project; [workbook](evaluation-workbook.md) supplies its values |
| `scripts/play_recordings.py` | Localhost video server; English by default, `--edition ko` selects the separate Korean set |

These are script names, not complete terminal commands. Prefix them with `python` only when following the linked procedure.
Hosted preparation can create/read back local azd environment state; it does not provision, deploy or assign roles.

</details>

## Hosted workflow and evaluation extension

<details>
<summary>Advanced matrix flags — use only after the workbook's preparation</summary>

Prepend `python scripts/workshop.py --language en` to these abbreviated commands.

| Command | Contract |
|---|---|
| `runtime-contract --kind workflow ...` | Local profile, language, model map and data/prompt/code hashes |
| `workflow-agent --pattern sequential` | Actual case-isolated MAF pipeline with one validated answer |
| `seed-search --hybrid --confirm-create --confirm-cost` | Real embeddings and a separately owned vector index |
| `retrieve --provider hybrid` | Combined text/vector search, not a renamed keyword query |
| `benchmark plan` | Model/case/cost shape only; no Azure call |
| `benchmark smoke --local --azd-directory ...` | Actual local host plus billable model; the directory is required, never inferred from the source copy |
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

</details>

## Find the code behind a command

The entry point is [`scripts/workshop.py`](../../scripts/workshop.py), then [`cli.py`](../../src/foundry_workshop/cli.py).
The CLI parses/validates input, selects one implementation and prints/saves its result.
Cloud branches load `.env` through `settings.py`; offline branches do not.
Start at the matching file below rather than reading every module in order.

| What to inspect | File under `src/foundry_workshop/` |
|---|---|
| Settings, input/output schemas and hashes | `settings.py`, `contracts.py` |
| Local retrieval, core collection and business gates | `knowledge.py`, `experiments.py`, `evaluation.py` |
| Project model calls and managed Prompt Agents | `cloud.py` |
| Local MAF and the deployable workflow | `agents.py`, `runtime.py` |
| Search/hybrid and the separate IQ Chat preset | `search.py`, `iq_chat.py` |
| Runtime profiles, packages and Hosted transport | `profiles.py`, `packaging.py`, `hosted.py` |
| Hosted matrix, native judges and traces | `benchmark_cli.py`, `benchmark.py`, `cloud_evaluation.py`, `native.py`, `calibration.py`, `observability.py` |
| Managed tools and conversations | `toolbox.py`, `toolbox_host.py`, `conversations.py` |
| Selected specialist exercises | `a2a_lab.py`, `memory_lab.py`, `routines_lab.py`, `openapi_lab.py`, `code_interpreter_lab.py`, `resilience.py` |
| Deterministic learner/extension material generation | `materials.py`, `extension_materials.py` |

The matching `tests/` contracts run offline. `tests_sdk/` uses installed SDKs with explicit stub transports, not live Azure.
