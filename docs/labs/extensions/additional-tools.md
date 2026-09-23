# Additional tools: verify a generated artifact and an API boundary

**English** | [한국어](../../ko/labs/extensions/additional-tools.md)

**Path B/C, optional.** Start with **Code Interpreter over the six bundled synthetic policy records**.

**Evidence status:** the English Code Interpreter and OpenAPI results date from September 16, 2026 (earlier `gpt-5.6-luna` preset); not re-run with `gpt-6-sol`.

OpenAPI is a separate integration branch. Neither requires real company data.

**Need:** working project/model access, regional/model support for the selected tool,
permission to create a dedicated agent/uploaded file and approval for model plus sandbox charges.
**Stop when:** an actual code call produced a downloaded CSV that preserves every original policy ID/title.
**If blocked:** keep the original error/file IDs; do not generate the expected artifact locally and claim the tool made it.

**First pass:** Code Interpreter steps 1–4, then handoff. OpenAPI is a separate choice,
not a second tool you must run after a verified CSV.

## 1. Know what is being tested

The input CSV is derived from the canonical six policy documents.
The requested output contains exactly two columns, `id,title`, and the same six rows in order.
No policy answer, financial calculation or model ranking is being evaluated.

Code Interpreter has additional session/container charges beyond model tokens.
The example does not promise that stopping a chat eliminates those charges immediately.

## 2. Execute once

```bash
python scripts/workshop.py --language en code-interpreter run --label code-policy-table --confirm-create --confirm-cost
```

The helper uploads only its generated synthetic CSV, creates a uniquely named Prompt Agent,
pins the returned version in the request, and requires a real Code Interpreter tool call.
It does not load an arbitrary user-selected file or allow a different input corpus.

## 3. Inspect the exact artifacts

Open `outputs/code-interpreter/code-policy-table/`:

| File | What to verify |
|---|---|
| `policy-records.csv` | The six original synthetic inputs |
| `ownership.json` | Actual uploaded file, agent/version and container identifiers |
| `request.json` | Fixed task and exact agent version |
| `response.json` | Actual completed code call and generated-file citation |
| `policy-summary.csv` | Downloaded from the actual container file API, not created as a fallback |
| `summary.json` | Source/output hashes and `verified_rows: 6` |

The helper accepts one generated CSV citation from a container actually reported by the code call.
It writes to a fixed local filename rather than trusting a model-provided path.
Wrong columns, missing/duplicate/reordered rows or modified titles fail verification.
Keep the mismatched output unchanged for diagnosis.

## 4. Clean up the owned temporary resources

```bash
python scripts/workshop.py --language en code-interpreter cleanup --label code-policy-table --confirm-delete
```

The command acts only on the recorded dedicated agent version, uploaded file and generated container.
It retains local evidence and refuses a name/project mismatch or additional agent versions.
Read back resource states and check residual billing; cleanup requests are not proof of zero cost.

## 5. OpenAPI branch: use the already-owned synthetic Search API

<details>
<summary>Optional independent OpenAPI exercise — requires Lab 06's owned index and runtime identity</summary>

An OpenAPI tool exposes an HTTP API contract. It is not the same as a Python function,
an A2A endpoint or Code Interpreter's sandbox.

This branch uses the existing Search REST API and your **owned six-document index** from Lab 06.
No new API Management, custom API server or company connection is needed.
The generated OpenAPI 3.1 specification exposes only the index's read-only search operation.
HTTP POST here means a query; it does not upload, update or delete documents.

Before invoking, the owner verifies:

- The same `AZURE_SEARCH_ENDPOINT` and `AZURE_SEARCH_INDEX_NAME` as the synthetic seed ledger.
- Authentication and token audience; no keys or secrets copied into prompts.
- Caller identity and target permissions.
- Exact request/response shape, a safe test input, cost/rate bounds and cleanup owner.

The OpenAPI runtime's managed identity needs Search Index Data Reader on that service.
Its token audience is **`https://search.azure.com`**, not the Foundry project endpoint.
This is separate from your local user's Search access.

```bash
python scripts/workshop.py --language en openapi plan
```

Verify the one-server, one-index, read-only plan and runtime permissions before the billable request:

```bash
python scripts/workshop.py --language en openapi invoke --label openapi-policy --confirm-cost
```

The plan must contain one server, one owned index path and one `SearchSyntheticPolicies` operation.
Inspect `outputs/openapi-runs/openapi-policy/plan.json`, `request.json`, `response.json` and `summary.json`.
The response must contain an actual completed `openapi_call`; a plausible answer or a native Search call is not enough.
Keep the specification hash, actual source data and response/model metadata.

Do not add a key or silently replace this tool with `retrieve --provider search` after an authentication or schema error.
If the Search index or managed-identity permission is not prepared, stop and record **not run**.
The direct Responses request creates no persistent Prompt Agent definition; source/index/model costs and any newly added role still require owner review.

</details>

**Next:** [Toolbox](toolbox.md), [C modules](../../paths/c-advanced.md), or [Lab 11](../11-capstone.md).
[Code Interpreter lifecycle](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/code-interpreter) ·
[OpenAPI authentication and contracts](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/openapi).
