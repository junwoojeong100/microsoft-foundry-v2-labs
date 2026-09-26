# Troubleshooting: find the cause before the next command

**English** | [한국어](../ko/reference/troubleshooting.md)

**Do not continue deployment or paid evaluation while the previous step is failing.**
Separately authorized [cleanup of recorded resources](cleanup.md) can still proceed after preserving the error and evidence;
it does not repair the failed step or authorize a wider deletion scope.
Creating a new model, subscription, or resource for the same unexplained error is not recovery.

<a id="resume-safely"></a>

## Resume without repeating paid work

Read the last completed step and exact version/labels in your notes. Use the **first matching row**:

| What happened | Safe next action | Do not |
|---|---|---|
| Closed the browser | Reopen the same project, agent and saved version; inspect the existing conversation | Create another agent or resend all questions |
| Finished the optional File Search branch | [Return to the recorded inline agent/version](../labs/03-prompt-agent.md#check-inline-agent) before A's four core checks; keep the File Search result separate | Use the `-files` agent or its replies as the inline baseline |
| Lab 07 A's **Save** button is enabled | Preserve any wanted draft separately, then [restore the recorded baseline version](../labs/07-evaluation.md#assessment-version) with no unsaved edits before asking | Save the draft as the baseline, overwrite its snapshot, or mix versions in one assessment |
| Pasting an answer changed several spreadsheet cells | Undo the last paste, then [paste the received answer in cell edit mode](../labs/07-evaluation.md#assessment-sheet); keep all six original case IDs/questions | Resend the question, replace the filled baseline with a blank template, or delete affected cases |
| Opened a new terminal | Return to the repository root; run `source .venv/bin/activate`; keep your existing Azure sign-in | Reinstall everything, overwrite or shell-`source` `.env`, or repeat `az login` merely to resume |
| Paused after Lab 03 B created the agent | Follow [the saved-agent restart table](../labs/03-prompt-agent.md#resume-managed-agent); restore both `agent_name` and `agent_version` from the creation JSON | Run `create` again to restore a shell variable, use a stale name, or invoke `latest` |
| `${NAME:?...}` reports a missing value | Restore the named value from this pass's setup/output notes; the command has not run | Remove the guard, paste a recording's ID or assume another terminal supplied the value |
| A model-comparison command finished or failed | Its [scoped override](../labs/extensions/model-operations.md) leaves the original setup unchanged; inspect the saved comparison/error | Change `.env` to continue or repeat paid work merely to restore the first model |
| B's notes directory already exists | Resume that pass's files, or choose a new directory for a new pass; the guarded copy block intentionally stops | Overwrite your filled records with blank templates |
| `--output` says the file already exists | Open the saved JSON; the new request was not sent. Choose another filename only for an intentionally new request | Delete the evidence or repeat a paid call just to save it again |
| The response printed, but saving failed | Keep the complete stdout and save it manually to a new file; retain the file error | Repeat the model request to recover an already returned answer |
| A label already exists | Inspect the directory printed by that module; [saved-result locations](commands.md#saved-results) distinguish core, matrix, Toolbox and conversation runs | Delete the run or invoke `collect` with that same label |
| Lab 00's v1 fixture reports `passed: 0`, `errors: 0` | This is the [expected citation-check failure](../labs/00-start.md#offline-fixtures); preserve it and continue with v2, provided the command itself succeeded | Reinstall the environment, edit the fixture to pass, or treat it as a real model score |
| `collect` returned `1` with a completed run | Preserve all rows/errors; run local `evaluate` with that same label. Resolve the cause before any new **dev** run | Replace failed rows, silently change model/provider, or recollect exposed holdout |
| `collect` failed or was interrupted before a completed run | Preserve stderr and any partial files; resolve the reported cause using [Common blockers](#common-blockers). There is no complete run to evaluate | Score a missing/partial run, delete its evidence, or recollect exposed holdout |
| `evaluate` returned `1` | Read `total`, `passed`, `errors` and per-case `checks`; review a baseline failure, but keep holdout closed for a failing candidate | Treat a completed request as a passed business gate |
| Candidate and holdout already exist | Read `outputs/<holdout-label>/acceptance.json`, or rerun local `accept` with those exact labels | Recollect an exposed holdout to get a better result |
| Hosted package already exists | Inspect its manifest; preserve that exact generated directory under a new name before a rebuild | Delete source code, the whole `.build`, `outputs`, or azd state |
| `serve` keeps terminal A occupied | Expected: leave it running and use [Lab 08's two-terminal sequence](../labs/08-hosted.md#hosting-gates) for readiness and invocation; finish with `Ctrl+C` in A | Start a second server or deploy to make the shell prompt return |
| Search says scope/corpus differs | Keep the old ledger; follow [the fresh-copy rule](configuration.md#workspace-scope) for a language, prefix or service change | Change only the next run label or delete/edit the ledger |
| Introductory Hosted preparation rejects a directory/profile | Preserve the error/directory, then follow [Lab 08's preparation](../labs/08-hosted.md#hosting-gates) with a new empty directory outside existing azd projects and the exact local v2 Responses package/language | Repeat `azd ai agent init`, use `--force`, or weaken the package checks |
| A required evaluation is still blocked | Save existing records and use [incomplete handoff](../labs/11-capstone.md#incomplete-handoff) | Create an acceptance report for absent runs or call blocked work complete |
| Cloud judge timed out | Resume polling with the **same** `cloud-evaluate --label` command and saved job IDs | Apply the new-collection-label rule to an already submitted judge job |
| Local matrix smoke requires `--azd-directory` | Supply the standalone directory prepared by the workbook; there is no implicit source-project default | Copy another agent's `azure.yaml` into the source root |
| A Toolbox remote-output folder already exists | Preserve its raw stream and verification/failure; choose a new directory in every path only for a genuinely new request | Overwrite the prior raw stream or call the model only to rerun the local verifier |

For core Lab 07, use [the saved-run restart table](../labs/07-evaluation.md#resume-evaluation) before any new collection.
For a genuinely new dev experiment, choose one fresh **baseline/candidate/final-holdout** label set and
use it consistently in Lab 07 and Lab 11. Do not unlock holdout until the new candidate passes and is frozen.
Read-only reinspection does not create new inference evidence. A new label does not make an exposed holdout unseen again.

## Common blockers

| Symptom | First check | Return directly to |
|---|---|---|
| Cannot find `scripts/workshop.py` | The terminal must contain `README.md`, `pyproject.toml`, and `scripts/`; the learner ZIP is not the source ZIP | [00 B](../labs/00-start.md#path-b) |
| Bash commands fail in PowerShell/Command Prompt, or the prompt is `>>>` | Use the WSL terminal on Windows; leave Python with `exit()` before pasting terminal commands | [Terminal check](../labs/00-start.md#terminal-check) |
| Missing Python/package | Supported Python, active `.venv`, then the pinned install step; stop on installation errors | [00 B](../labs/00-start.md#path-b) |
| `--output` directory missing or outside `outputs/` | Prepare Lab 00's notes directory and use a new `.json` path inside this source copy | [Saving JSON](commands.md#saving-json) |
| A setting must be a UUID / output tokens must be an integer | Correct the named setting from the setup card; tokens must be 256–8192. Check inherited process variables too | [Configuration](configuration.md) |
| `check_sdk.py` reports a missing hosting package in core B | That check covers the optional Hosted/Toolbox SDK too. Core B does not require it; selected extensions use the declared extra | [Module SDK preparation](../labs/extensions/developer-toolkit.md#hosted-sdk) |
| Prefix rejected | `mfv2-` is mandatory; lowercase letters/digits, single hyphens, no trailing hyphen and at most 32 characters total | [Configuration](configuration.md#workspace-scope) |
| 401/403 or project missing | Check the intended tenant and caller; renew only expired authentication. For 403, the owner checks resource-scoped permissions, not repeated login | [Sign-in boundary](../labs/00-start.md#azure-sign-in) / [setup](../setup.md) |
| Browser sign-in succeeds but the training project is unavailable | Match both the account and directory to the setup card before requesting more roles | [Portal tenant check](#portal-tenant) |
| Learning alone, and a step says to ask the owner | You are the owner: fix the matching project, model, role or tracing step yourself; never switch to another model | [Self-study preparation](../setup-owner.md#self-study) |
| `MAF request failed` / `Failed to invoke the Azure CLI` | Preserve the SDK cause; a CLI token-process timeout is not a business-check failure | [MAF request recovery](#maf-request-failure) |
| Model 404 / 429 | Full project endpoint and deployment name / quota and concurrency; no replacement model | [02 B](../labs/02-models.md#path-b) |
| HTTP 500 from `model`, `answer`, MAF or an agent right after a model release | The project agent path may not support that model yet (seen with `gpt-6-luna` on September 23, 2026). Stop and record it; no model or endpoint switch | [Model choice](model-choice.md) |
| IQ reports no chat model | Default B uses model-free GA retrieval; optional A IQ Chat needs a different prepared base | [06](../labs/06-knowledge.md) |
| Hosted call selects the wrong local project | Restore the recorded absolute `HOSTED_DIRECTORY` and use `--cwd` on every azd command | [08](../labs/08-hosted.md) |
| Local Hosted readiness fails / port 8088 is in use | Inspect terminal A's startup error and selected profile. Stop only an earlier server you started before restarting; do not stop an unknown process or try remote deployment | [08 execution gates](../labs/08-hosted.md#hosting-gates) |
| No trace appears in Traces | Include the original request's date and agent/version in the filters, then search by Response ID or Trace ID. Confirm Application Insights was connected before the request; local MAF has no server-side agent trace | [09](../labs/09-operations.md#path-b) |
| Traces authorization error | Record **trace unverified**. The owner checks Log Analytics Reader on connected Application Insights and, for protected tables, Privileged Monitoring Data Reader; do not select **Resolve** or add roles yourself | [09 B](../labs/09-operations.md#path-b) |

<details>
<summary>Full error reference — open if the short table does not cover your failure</summary>

| Symptom | Check first | Return to lab |
|---|---|---|
| Project missing | Tenant, account, project role; never select an unrelated production project | 00–01 |
| No `python3.13` | Supported Python installation or prepared environment | 00 |
| `ModuleNotFoundError` | Venv, required extra, `python -m pip check` | 00 |
| Package TLS/connection error | Network policy, official PyPI access, prepared environment | 00 |
| `.env` changes have no effect | Process variables taking precedence; fresh terminal | 00 |
| 401 | Sign-in, tenant, credential type; renew expired local authentication only within the shared-profile boundary | [00](../labs/00-start.md#azure-sign-in) |
| `AADSTS90072` / wrong default account | Configured subscription/account profile and subscription-scoped authentication; do not change the default, invite guests, or log everyone out | 00 |
| 403 | Management/data-plane roles, actual identity/scope, propagation | 01 |
| `CalledProcessError` during `doctor --cloud` | Read `Command stderr:` for the captured Azure CLI diagnostic. Distinguish deployment-read authorization from wrong subscription/resource names or network failure; do not infer a role from the exception type alone | [00 B](../labs/00-start.md#path-b) |
| Model 404 | Actual deployment name rather than catalog name; full project endpoint | 02 |
| 429 | Quota, TPM, concurrency, other teams, service retry guidance | 02 |
| `json_schema`/option 400 | Model Structured Outputs support and SDK contract | 02 |
| `incomplete` response | Output limit, filters, model support; no silent repair | 02 |
| Label `FileExistsError` | Inspect and resume the existing run; new labels are only for a genuinely new experiment | 07 |
| Source hash mismatch | Preserve the original files/error; investigate changed inputs or responses. Recollect only as a new dev experiment, not by retrying exposed holdout | 07 |
| MCP failure | Same-venv `mcp`, server path, non-JSON stdout | 04 |
| Workflow timeout | Round/output bounds, tool latency, quota | 05 |
| Search 401/403 | The owner checks [API access control for Entra tokens](../setup-owner.md#search-authentication), then the caller's Search roles; roles alone do not enable token authentication | 06 |
| Partial Search upload | Per-document status, count/keys, index fields | 06 |
| Existing Search object rejected | Prefix and ownership ledger; no shared-object overwrite | 06 |
| Hybrid index dimension or existing-index conflict | Actual embedding dimension, a separate owned index and the namespace/ledger; never truncate or zero-fill vectors | 06 |
| IQ 400 | GA intents mixed with Preview messages; actual API version | 06 |
| `Chat completions model is required` | Missing model selection, not MI failure. Open the prepared chat base with **`gpt-5.6-luna` + Search SMI**; do not save portal defaults over the model-free GA base | 06 |
| `Unsupported model type in Knowledge Base Model Configuration` | Search does not accept that model for a KB; IQ Chat uses its own `gpt-5.6-luna` deployment, not a GPT-6 model | 06 |
| `iq-chat check` model/version/role failure | Use the [fixed preset](iq-model-identity.md): `gpt-5.6-luna` / `2026-07-09`, Search SMI, account-scoped role. The owner resolves preparation; no replacement model | 06 |
| `ready_for_setup: true`, `configured: false` | Prerequisites pass but the separate chat base does not exist. Owner completes the authorized setup in the source-owning workshop copy | 06 |
| IQ Chat label exists | Read the prior request/response/failure first; use a new label only for an explicitly new paid attempt | 06 |
| IQ model 401/403 | Search → model identity, account scope, role propagation and network access; the Hosted/user role is not inherited by Search | 06 |
| Preview rejects `maxOutputSizeInTokens` | Preserve the parameter-validation error and use the tested version-specific `maxOutputSize` request; do not classify it as authentication failure | 06 |
| IQ references/activity error | sourceData/docKey, sources, semantic settings, billing consent | 06 |
| Cloud judge timeout | Poll the same label and saved evaluation/run IDs; no new job is created automatically | 07 |
| Evaluator schema error | Actual catalog's `model`/`deployment_name` and version | 07 |
| Holdout rejected | Passed/frozen dev candidate, matching code/prompt/model/provider, explicit unlock | 07 |
| Local succeeds; Hosted 403 | Runtime identity roles, not repeated local sign-in | 08 |
| Missing logs/traces | App Insights app ID, exporter, agent, date range, sampling and retention/protected-table access; zero traces are unverified, not healthy operation | 09 |
| No trace appears in Traces | Request date range and agent/version filters, project-connected Application Insights before the request, Response ID/Trace ID search; local MAF has no server-side agent trace | 09 |
| Traces authorization error | Log Analytics Reader on connected Application Insights; Privileged Monitoring Data Reader too when protected tables are enabled | 09 |
| English query uses Korean material | Select `--language en` and the dedicated English index/source/base; never fall back to Korean after an error | 00–07 |
| Missing English file | Restore the frozen English bundle; preserve original Korean files | 00 |
| `--agent-endpoint` conflicts with `--protocol` | The full endpoint already specifies the protocol; local invocations still select it explicitly | 08 |
| Batch API version missing | Merge session query parameters instead of replacing `api-version=v1` | 07–08 |
| Project embeddings 404 | Stop and preserve the failed experiment. Use `WORKSHOP_EMBEDDING_API=account` and the same account's endpoint only as the initial configuration of a separately approved new hybrid experiment; retain separate configuration/results, not a fallback | [06 C](../labs/06-knowledge.md#hybrid-rag) |
| Trace-query `InvalidTokenError` | App Insights audience and the intended subscription/tenant credential; no identity/resource substitution | 09 |
| Stop returns 409 for idle session | Re-read the exact recorded session/version and record the idle state without another stop request | [09](cleanup.md#hosted-sessions) |
| Host profile/contract mismatch or missing `runtime-profile.json` | Package again with the current code, then compare the exact profile language, model map, source package, actual version and retrieval configuration. Collect under a new label; never edit a manifest to pass | 08 |
| Model key not in the allowlist | The same `WORKSHOP_MODEL_DEPLOYMENTS_JSON` map in `.env` and the remote service environment, including the default deployment | 08 |
| `account-chat` endpoint mismatch | The same Foundry account's actual OpenAI root in `AZURE_OPENAI_ENDPOINT`; the CLI never switches URLs after a failure | 06–08 |
| azd raw output cannot be parsed | Only the HTTP status, UTF-8 byte length and known notices are accepted; the CLI never extracts JSON from error text | 08 |
| A CLI extension reports Incompatible | Review the [version gate](versions.md); approve and install a compatible combination separately, then check again | 08 |
| Native quality score is low | Preserve the completed run; review the evaluator against business requirements, not retries until a favorable score | 07 |
| Native run failed or invalid | Rerun the same command once with `--retry-failed`; the original attempt is kept. A completed low score cannot be retried | 07 |
| A regression file changes a question or answer | Keep the existing dev contract or design a separate dataset version; never use holdout as regression | 07 |
| Matrix rows missing or duplicated | Do not evaluate the successful subset; fix the cause, then collect the complete matrix under a new label | 07 |
| `Missing evaluator results … missing ['business_rubric']` | The service omitted one evaluator; the attempt is saved as invalid. Rerun the same `cloud-evaluate` command once with `--retry-failed`; the attempt stays in `native-attempts/`. A retried `--reference` run stays in that evaluation as `<label>-retry-1` | 07 |

</details>

<a id="portal-tenant"></a>

## Browser sign-in is not a tenant or permission check

Compare the portal's directory with the setup card's tenant ID. When the URL includes `tid=`, it must identify that tenant.
Use the owner's project link for that directory and the **specified workshop account**, not simply another signed-in work account.
The project name in a page header can appear while the agent is still **Loading...**; wait for the actual agent name,
version and instructions before calling the page verified.

Browser and Azure CLI sessions can represent different accounts or tenants. SDK success does not prove that the browser
has the same access, and a browser 403 does not prove that the correctly scoped CLI caller is missing a role.
If the account or directory is wrong, correct the sign-in selection first; do not grant roles, invite guests or change
the Azure CLI default subscription to get past it. If the correct account still lacks access, the owner resolves that scope.

<a id="maf-request-failure"></a>

## Recover from a failed MAF request, not a failed answer

`maf`, `workflow`, `workflow-agent`, `maf-evaluate` and `serve` report handled Agent Framework failures as
`FAIL: ValueError: MAF request failed: ...` with exit code `2`. The cause and recovery-guide path are retained.
No successful-response file is written, and the CLI does not retry or replace the model/provider after reporting the failure.
`--debug` retains the complete exception chain; debug logs can contain local paths, so keep them private.

For `TimeoutExpired` around `az account get-access-token` / `Failed to invoke the Azure CLI`, preserve the original stderr
and time. Check the active environment and the **same** subscription/tenant with Lab 00's read-only `doctor --cloud`
before deciding on another paid workflow attempt. Do not print or share access tokens.
Reauthenticate only if authentication actually expired, following [the shared-profile boundary](../labs/00-start.md#azure-sign-in);
a slow local CLI process alone is not a reason to sign in again or grant roles.

A later successful attempt is a new execution, not a replacement for the failed record. Read an existing successful
`--output` file instead of replaying it, and never retry completed low scores until they improve.

## Network isolation

The [IQ model-identity guide](iq-model-identity.md) separates the default model-free GA path from the supported MI-backed planning/synthesis path and records the actual verification.

For `PublicNetworkAccessDisabled`, private-endpoint 403, or timeout, check whether
the caller is outside the project's allowed network.
Do not disable firewalls, private access, or certificate verification.
Use an administrator-approved VNet access path or a prepared environment.
Trying Foundry MCP does not remove network isolation.

## Do not "fix" installation by

- Adding `--trusted-host`, disabling TLS checks, or using an unknown mirror.
- Installing into global Python or modifying another project's venv.
- Upgrading every SDK with `--upgrade --pre`.
- Claiming installation succeeded merely because a version appears on PyPI.

## Information to share when asking for help

Provide lab number, exact command, Python/package versions, error type/HTTP status,
timestamp, and relevant request/response/run IDs to the responsible instructor.
Never paste an entire `.env`, tokens, passwords, real customer messages, or raw traces
into a public issue.

Handled CLI exit codes: `0` success, `1` failed business gate/collection error,
`2` configuration/input/dependency/precondition error or failed individual Azure/MAF request.
`demo` generates a fixture, so v1's intentionally low score is not generation failure;
the separate `evaluate` command returns a score-based exit code.
