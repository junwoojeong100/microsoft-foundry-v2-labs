# Troubleshooting: find the cause before the next command

**English** | [한국어](../ko/reference/troubleshooting.md)

**Do not chain deployment, evaluation, or deletion while the previous step is failing.**
Creating a new model, subscription, or resource for the same unexplained error is not recovery.

| Symptom | Check first | Return to lab |
|---|---|---|
| Project missing | Tenant, account, project role; never select an unrelated production project | 00–01 |
| No `python3.13` | Supported Python installation or prepared environment | 00 |
| `ModuleNotFoundError` | Venv, required extra, `python -m pip check` | 00 |
| Package TLS/connection error | Network policy, official PyPI access, prepared environment | 00 |
| `.env` changes have no effect | Process variables taking precedence; fresh terminal | 00 |
| 401 | Sign-in, tenant, credential type; local vs. runtime identity | 00 |
| `AADSTS90072` / wrong default account | Configured subscription/account profile and subscription-scoped authentication; do not change the default, invite guests, or log everyone out | 00 |
| 403 | Management/data-plane roles, actual identity/scope, propagation | 01 |
| Model 404 | Actual deployment name rather than catalog name; full project endpoint | 02 |
| 429 | Quota, TPM, concurrency, other teams, service retry guidance | 02 |
| `json_schema`/option 400 | Model Structured Outputs support and SDK contract | 02 |
| `incomplete` response | Output limit, filters, model support; no silent repair | 02 |
| Label `FileExistsError` | Preserve the existing run; use a new label | 07 |
| Source hash mismatch | Changed response/data; recollect under a new version | 07 |
| MCP failure | Same-venv `mcp`, server path, non-JSON stdout | 04 |
| Workflow timeout | Round/output bounds, tool latency, quota | 05 |
| Search 403 | Entra data-plane auth and Index Data Reader/Contributor | 06 |
| Partial Search upload | Per-document status, count/keys, index fields | 06 |
| Existing Search object rejected | Prefix and ownership ledger; no shared-object overwrite | 06 |
| IQ 400 | GA intents mixed with Preview messages; actual API version | 06 |
| IQ references/activity error | sourceData/docKey, sources, semantic settings, billing consent | 06 |
| Cloud judge timeout | Poll the same label and saved evaluation/run IDs | 07 |
| Evaluator schema error | Actual catalog's `model`/`deployment_name` and version | 07 |
| Holdout rejected | Passed/frozen dev candidate, matching code/prompt/model/provider, explicit unlock | 07 |
| Local succeeds; Hosted 403 | Runtime identity roles, not repeated local sign-in | 08 |
| Missing logs/traces | App Insights, exporter, date range, retention/protected-table access | 09 |
| English query uses Korean material | Select `--language en` and the dedicated English index/source/base; never fall back to Korean after an error | 00–07 |
| Missing English file | Restore the frozen English bundle; preserve original Korean files | 00 |
| `--agent-endpoint` conflicts with `--protocol` | The full endpoint already specifies the protocol; local invocations still select it explicitly | 08 |
| Batch API version missing | Merge session query parameters instead of replacing `api-version=v1` | 07–08 |
| Project embeddings 404 | Explicitly choose the same account API and required endpoint; retain the original failure | 06 |
| Trace-query `InvalidTokenError` | App Insights audience and the intended subscription/tenant credential; no identity/resource substitution | 09 |
| Stop returns 409 for idle session | Re-read the exact recorded session/version and record the idle state without another stop request | 09 |
| Host profile/contract mismatch | Exact profile language, model map, source package, actual version and retrieval configuration | 08 |
| Native quality score is low | Preserve the completed run; review the evaluator against business requirements, not retries until a favorable score | 07 |

## Network isolation

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

Main CLI exit codes: `0` success, `1` failed business gate/collection error,
`2` configuration/input/dependency/precondition error.
`demo` generates a fixture, so v1's intentionally low score is not generation failure;
the separate `evaluate` command returns a score-based exit code.
