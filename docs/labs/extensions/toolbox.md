# Managed Toolbox: one synthetic policy tool, one pinned version

**English** | [한국어](../../ko/labs/extensions/toolbox.md)

**Path B extension.** A Toolbox is a managed MCP endpoint for reusable tools.
This first pass uses only the six bundled synthetic policies already seeded in Search.
It does not connect Work IQ, company APIs, public web search or an arbitrary MCP server.

**First pass:** steps 1–5, then step 7's handoff/cleanup. Step 6's default-version changes are optional.

**Need:** successful [Lab 06 Search](../06-knowledge.md), the [Hosted/Toolbox SDK extra](developer-toolkit.md#hosted-sdk) in the same B environment,
a prepared keyless Search project connection, and approval to create your own Toolbox.
**Stop when:** one pinned MAF request has a real tool result, model response and version binding.
**If blocked:** preserve the error and return to the prerequisite owner; never replace the provider.

**Evidence status, September 16, 2026 (earlier `gpt-5.6-luna` edition):** an English MCP discovery, direct Search query,
MAF answer and version binding were executed; they were not re-run with the `gpt-6-sol` preset.

## 1. Get the two owner values first

Keep the existing `.env` project/model/Search values from Lab 06. Add:

```dotenv
TOOLBOX_SEARCH_CONNECTION_NAME=<actual-keyless-search-project-connection>
TOOLBOX_NAME=<your-prefix>-tools-en
```

The connection must target the **same** `AZURE_SEARCH_ENDPOINT`, and the tool uses the
same `AZURE_SEARCH_INDEX_NAME`. This is a Search connection in the Foundry project,
not a Search index name, an IQ base or a File Search store.

The owner creates the connection once with Microsoft Entra authentication and verifies the actual
upstream identity's Search permission. In this edition's native Toolbox path, the **project managed identity**
already had Search Index Data Reader and additionally needed Search Service Contributor for the native connector.
Giving contributor roles only to the account identity did not resolve the denial; those trial grants were removed.
API keys remain disabled. If no approved connection exists, stop here rather than inventing its name.
The caller needs Foundry project access for Toolbox metadata/creation and actual tool execution.
Creating a connection or granting a role is a separate authorization step.
Search Service Contributor can manage Search objects; it is **not a read-only role**.
Use a dedicated synthetic training service and owner-approved scope, not a production Search service.
Identity behavior can differ by integration: do not confuse this caller with the Search identity
used by the [IQ chat preset](../../reference/iq-model-identity.md).
The direct query in step 4, not a role name or successful local login, verifies downstream access.

## 2. Inspect the exact local plan

```bash
python scripts/workshop.py --language en toolbox plan
```

Check your actual project and owned name. The definition must contain one named
`policy_search` tool, type `azure_ai_search`, query type `simple`, and `top_k: 6`.
The local plan names the connection logically. Creation resolves it to the **actual full project connection resource ID**
and records that resolved request. Do not send a bare connection name as a raw `project_connection_id` and assume runtime access is equivalent.
`azure_requests_sent: false` means this is a configuration plan, not a live test.
Do not add Tool Search or Skills until the ordinary tool path works.

## 3. Create your first version

After the owner approves this write:

```bash
python scripts/workshop.py --language en toolbox create --confirm-create
```

Keep the actual `selected_version`, `default_version`, version-specific `endpoint`,
`definition_hash`, and `ledger` path. The command refuses an existing name rather than adopting another person's Toolbox.
The ownership record is under `outputs/toolboxes/<name>/ownership.json`.

Enter the returned version once in the **same terminal**:

```bash
printf 'Actual selected_version from create: '
read -r TOOLBOX_VERSION
python scripts/workshop.py --language en toolbox inspect --version "$TOOLBOX_VERSION"
```

The consumer endpoint without `/versions/...` follows the Toolbox's current default.
This workshop invokes the **version-specific endpoint** so a later promotion cannot silently change an experiment.
The current default and the version you chose are separate values.
Toolbox versions are immutable, but the referenced connection and Search index can change.
Keep them frozen during a comparison and retain the returned tool evidence, not only a local corpus hash.

## 4. Inspect the actual MCP tool list

```bash
python scripts/workshop.py --language en toolbox probe --version "$TOOLBOX_VERSION" --label toolbox-first-list
```

The live list must contain exactly `policy_search`.
`model_invoked: false` and `tool_invoked: false` are correct: this step checks MCP connection/discovery, not an answer.
Review `binding.json`, `tool-list.json` and `summary.json` under `outputs/toolbox-runs/toolbox-first-list/`.

If authentication, initialization or tool discovery fails, do not bypass it with another endpoint,
an API key, or the local MCP server from Lab 04.

Before paying for an answer-model request, query the synthetic tool directly:

```bash
python scripts/workshop.py --language en toolbox query --version "$TOOLBOX_VERSION" --label toolbox-direct-query --confirm-cost
```

This separates **client → Toolbox discovery** from **Toolbox → Search access**.
The result must report `tool_invoked: true` and `model_invoked: false`.
If Search denies access, the owner corrects only the actual upstream identity's scoped role and retains the failed attempt.
Do not repeat model calls to diagnose a known downstream permission error.

## 5. Make one actual MAF request

After cost approval:

```bash
python scripts/workshop.py --language en toolbox ask --version "$TOOLBOX_VERSION" --label toolbox-first-answer --confirm-cost
```

The command asks the bundled September-2026 over-limit hotel question.
It uses MAF with the installed `FoundryToolbox` wrapper and your explicit model deployment.
The wrapper handles authenticated MCP requests; it is not a custom imitation of the Toolbox service.

Check:

- `model_invoked: true` and `tool_invoked: true`.
- The exact Toolbox version/hash and real service model-call IDs.
- The actual `tool-results.json` and the answer's policy IDs/date/approval conditions.
- A required prior approval is not a booking, payment or business approval performed by this code.

The run preserves raw tool/model results and failures. A model answer without an actual tool result is rejected.
The demonstration is bounded to six logical model calls and a 180-second invocation timeout;
SDK/service work can add usage, so these are not a currency spending cap.
Use a **new label** for every new request. Do not repeat a successful paid request merely to obtain another screenshot.

## 6. Practice a controlled version change

<details>
<summary>Optional version exercise — not required after your first verified answer</summary>

This creates a new version with a revised description while retaining the same tool configuration.
The purpose is to learn version selection, not to claim a quality improvement.

```bash
python scripts/workshop.py --language en toolbox add-version --confirm-create
```

Record the new returned version as `TOOLBOX_CANDIDATE`. Inspect/probe that version before changing the consumer default:

```bash
printf 'New selected_version from add-version: '
read -r TOOLBOX_CANDIDATE
python scripts/workshop.py --language en toolbox probe --version "$TOOLBOX_CANDIDATE" --label toolbox-candidate-list
```

Continue only after the probe succeeds and the returned binding/tool list matches the candidate.
After approval, change the default:

```bash
python scripts/workshop.py --language en toolbox select --version "$TOOLBOX_CANDIDATE" --confirm-update
```

Check the returned default version, then restore the original:

```bash
python scripts/workshop.py --language en toolbox select --version "$TOOLBOX_VERSION" --confirm-update
```

The last command is the explicit rollback to your original version.
Both changes require approval and local ownership. No agent is redeployed by a Toolbox default change.
A version-pinned run still points to the version it recorded, even when the consumer default changes.

</details>

## 7. Handoff or cleanup

If continuing to Tool Search/Skills or Hosted Toolbox, keep the owned Toolbox and its ledger.
Save the chosen version and next module in `session-notes.txt`; do not run cleanup first.
If finishing, confirm no other approved agent depends on it, then delete only this owned Toolbox:

```bash
python scripts/workshop.py --language en toolbox cleanup --confirm-delete
```

The command refuses deletion if remote versions differ from the locally recorded set.
It preserves result/ownership/cleanup records and does not delete the Search connection, index, service, models or project.
The owner separately handles shared resource costs.

## Recovery

| Symptom | Do this |
|---|---|
| Connection name is missing/wrong | Owner verifies the keyless CognitiveSearch connection and target service |
| 403 on metadata or tool call | Identify the actual calling identity and scope; local sign-in and runtime permissions differ |
| Existing Toolbox name rejected | Use your own unique prefix/name; do not delete another learner's object |
| Default points to an unowned version | Stop and review the other owner's change before selecting or deleting |
| MCP result reports an error | Keep `failure.json` and the raw tool result; no endpoint/provider retry |
| Model did not use the tool | Inspect the real request/response and tool description; do not count prose alone as completion |

**Next:** optionally [host this same Toolbox agent](toolbox-hosted.md),
[C. Advanced module selection](../../paths/c-advanced.md), or [Lab 11 handoff](../11-capstone.md).

**Dated references:** [Toolbox lifecycle](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/toolbox) ·
[MAF wrapper](https://learn.microsoft.com/agent-framework/integrations/by-component/tools/foundry-toolbox).
