# A2A 1.0: call a separately addressed policy specialist

**English** | [한국어](../../ko/labs/extensions/a2a.md)

**Path C, A2A 1.0 GA contract checked September 16, 2026.**

**Evidence status:** an English paired call and its output ran on September 16, 2026 with the earlier `gpt-5.6-luna` preset (wire packets not captured); not re-run with `gpt-6-sol`.

Two local MAF participants are not an A2A integration.
This module creates an owned synthetic specialist endpoint and a separate relay agent that delegates through A2A.

**Need:** B's model/agent setup, existing project/model access, permission for two new agents,
a keyless A2A connection, endpoint access for the actual calling identity, and cost approval.
**Stop when:** the authenticated card advertises 1.0 and a real caller response contains a successful A2A tool call.
**If blocked:** do not switch to preview 0.3, another agent or anonymous authentication.

**First pass:** steps 1–5. Use [azd preparation](developer-toolkit.md#azd-check) if needed.
The target, connection and caller are created in that order; inspect each result before the next write.

## 1. Inspect the plan

```bash
python scripts/workshop.py --language en a2a plan
```

The target/caller/connection names use your prefix and language.
The target contains only the bundled synthetic policy instructions and corpus.
The helper uses the explicit REST 1.0 contract for fields newer than the common pinned SDK's typed A2A surface.
It does not silently upgrade the entire course environment.

## 2. Create the specialist and enable incoming A2A

Run steps 2–4 only after the owner has approved the two agents, the connection and the model cost listed under **Need**.
You run them in that approved project; the objects they create are named with your prefix.

```bash
python scripts/workshop.py --language en a2a target --confirm-create
python scripts/workshop.py --language en a2a inspect
```

The first command creates one new Prompt Agent version, then applies the documented agent-card and endpoint patch.
Incoming A2A is not configured by merely adding another local agent to a Python list.

Keep the actual target version, base path, connection name and ownership file.
The card URL ends in **`/agentCard/v1.0`**. Its `supportedInterfaces` must include
`protocolVersion: 1.0`, `protocolBinding: JSONRPC`, and your exact A2A base URL.
The current service can advertise 0.3 alongside 1.0; select the 1.0 interface explicitly.
Authenticated card access is checked separately from model inference.

Foundry's incoming 1.0 endpoint uses JSONRPC and currently supports text without streaming.
An unspecified protocol can select the older 0.3 behavior; this module never relies on that default.
The target endpoint is not an immutable-version URL, so the helper refuses additional target versions during this experiment.

## 3. Create the keyless connection

Use the exact values returned above and the setup card:

```bash
printf 'Full project endpoint: '
read -r PROJECT_ENDPOINT
printf 'target_base from the target result: '
read -r A2A_BASE
printf 'connection_name from the target result: '
read -r A2A_CONNECTION
azd ai connection create "${A2A_CONNECTION:?Use the returned connection name}" --kind remote-a2a \
  --target "${A2A_BASE:?Use the returned target base}" --auth-type project-managed-identity \
  --audience https://ai.azure.com --project-endpoint "${PROJECT_ENDPOINT:?Enter the full project endpoint}"
```

Use the **A2A base path**, not the card URL, as the connection target.
An empty value stops before azd; restore the returned values rather than removing these guards.
Do not use `--force` or an API key.
The owner verifies the identity used by this connection and grants only required endpoint access
on the target agent/project. The signed-in learner and service identity are not interchangeable.

## 4. Create and invoke the relay

```bash
python scripts/workshop.py --language en a2a caller --confirm-create
```

Confirm the recorded caller version and intended target before approving inference:

```bash
python scripts/workshop.py --language en a2a invoke --label a2a-first --confirm-cost
```

The caller definition explicitly selects `type: a2a` and `a2a_version: 1.0`.
The model request references the caller's **actual recorded version**, not latest.
It requires the A2A tool rather than accepting a plausible answer generated without delegation.

Inspect `outputs/a2a-runs/a2a-first/`:
`request.json`, `binding.json`, the full `response.json`, and `summary.json`.
Keep the successful A2A call item, original policy IDs, caller/target versions and returned model/request metadata.
Do not invent target token usage if only caller usage is reported.
In the observed service response, the event can still be named `a2a_preview_call` even when
the accepted definition is `type: a2a`, `a2a_version: 1.0`.
The helper verifies that actual accepted configuration and its matching target output;
it records the event name separately and does not claim packet-level protocol capture.

## 5. Review and clean up

An agent card describes capabilities; it does not grant permission to use them.
A successful caller request does not authorize booking, approval or payment.
The specialist and relay must retain that boundary.

Before cleanup, retain the ownership and response artifacts.
The owner removes only the new caller, its connection and the new target after checking for references.
Do not delete shared models or the project. Foundry's A2A task/context retention is a separate service policy;
deleting an agent is not a claim that every retained record was permanently erased.

## Recovery

| Symptom | Action |
|---|---|
| Card 401/403 | Check the actual caller identity and Foundry endpoint-access role |
| Card has no matching 1.0 JSONRPC interface | Inspect `supportedInterfaces`, not an assumed top-level version field; do not downgrade |
| Additional target versions detected | Freeze a dedicated target or start a new experiment; do not infer which version the endpoint served |
| Connection target mismatch | Compare the full base path and project; never point at another team's agent |
| No A2A call in response | Keep the raw output as a failed integration check, not delegated success |
| Unsupported typed SDK symbol | Use the documented REST path for this lab or an independently verified SDK environment; no protocol fallback |

**Next:** [Memory](memory.md), [C module selection](../../paths/c-advanced.md), or [Lab 11](../11-capstone.md).
[Enable incoming A2A](https://learn.microsoft.com/azure/foundry/agents/how-to/enable-agent-to-agent-endpoint) ·
[Connect an A2A tool](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/agent-to-agent).
