# Lab 04. Add functions and MCP to a MAF agent

**English** | [한국어](../ko/labs/04-agents-tools.md)

**Goal:** Distinguish model invocation, application-owned agents, and tool execution.

**Open your section:** A: [skip to Lab 05 A](05-workflows.md#path-a) · [B — three tool paths](#path-b) · [Paths](../paths.md)

## Before you start

**This pass:** B runs no-tool, function-tool and MCP commands in order. A skips directly to Lab 05.

**Need:** Lab 00 environment plus a real Lab 02 response; no separate MCP server terminal is required.

**Continue when:** You have the no-tool response plus function/MCP responses with their source IDs. The long-input rejection is an optional negative test.

**If blocked:** Check the same venv and server path. A function response is not a substitute for a failed MCP run.

[One-time setup and learner files](../setup.md).

<a id="path-b"></a>

## 1. Run an agent without tools

Run from the repository root with `.venv` active. All three commands make billable model calls.
Each successful command saves its complete JSON as `maf-none.json`, `maf-function.json` or `maf-mcp.json`
in your Lab 00 notes directory through `--output`. Open that file before the next command; no copying is needed.
Record each file's finding on `Lab 04 maf-none.json / maf-function.json / maf-mcp.json findings:` in the B section of `session-notes.txt`.

```bash
python scripts/workshop.py --language en maf \
  --question "Explain the difference between Foundry and Agent Framework in three sentences." \
  --output outputs/learner-notes-en/maf-none.json
```


![September 24 English recording: MAF agent without tools](../assets/g6sol-20260924-en/screenshots/E04-001-maf-2.webp)

**What to check:** Read `mode: live`, `orchestration: local`, and `tools: none`.
Local Python owns execution, but the answer model is called in Azure.

**Save:** `maf-none.json` is written automatically in your Lab 00 notes directory. Open it and check the fields above.

Open `src/foundry_workshop/agents.py` and locate:

1. `FoundryChatClient`: the project and deployment it calls.
2. `Agent`: the name, instructions, tools, and execution options.
3. `agent.run()`: the actual model request.

Creating an `Agent` object does not register a managed portal agent; this one belongs to your Python process.
(Optional: Lab 03's [SDK branch](03-prompt-agent.md#b-optional-sdk-branch-managed-prompt-agent-versus-local-maf) shows the managed alternative, `project.agents.create_version()`.)

## 2. Add a read-only function tool

```bash
python scripts/workshop.py --language en maf --tools \
  --question "My domestic business-trip hotel in September 2026 costs KRW 170000. May I book it? State the limit and procedure." \
  --output outputs/learner-notes-en/maf-function.json
```

`lookup_policy` reads only bundled synthetic JSON, not the Internet
or a company API. Its `@tool` name, docstring, and types describe usage to the model.
The program validates model-supplied arguments again.

```mermaid
sequenceDiagram
    participant U as User
    participant A as Local MAF Agent
    participant M as Foundry model
    participant T as lookup_policy function
    U->>A: Travel-policy question
    A->>M: Question + tool definition
    M-->>A: Tool-call request
    A->>T: Validated query
    T-->>A: Synthetic evidence and document IDs
    A->>M: Tool result as data
    M-->>U: Answer with conditions and citations
```



![September 24 English recording: MAF with the read-only function tool](../assets/g6sol-20260924-en/screenshots/E04-002-tools-2.webp)

**What to check:** Inspect `tools: function` and the nested `decision`, `limit_krw`,
and `citations`. `needs_approval` means prior human approval is required, not granted.

Verify evidence corresponding to `TRAVEL-2026` and `APPROVAL-01`, an explanation without
booking/approving, and that `never_require` applies only to **side-effect-free synthetic lookup**.
If the model skips the tool or evidence, inspect the actual answer, instructions,
tool description, and tracing. A connected tool alone is not success.

**Save:** `maf-function.json` is written to the same notes directory. Review it before starting MCP.

## 3. Move the same lookup into a local MCP server

```bash
python scripts/workshop.py --language en maf --mcp \
  --question "What was the domestic business-trip lodging limit per night in May 2026?" \
  --output outputs/learner-notes-en/maf-mcp.json
```

The client starts `examples/mcp_server.py` using **the same venv's Python**.
No separate server terminal, public URL, or API key is needed. Transport is stdio;
the context manager cleans up the connection. Extra stdout logging can break MCP JSON-RPC.

| Function tool | MCP tool |
|---|---|
| Function in the same Python process | Tool exposed by another process/service |
| Simple implementation and debugging | Reusable across clients |
| Validate arguments and permissions directly | Also review server trust, authentication, and authorization |

This MCP is a **local synthetic library**, not Microsoft Learn, Work IQ, or company MCP.
For an executable managed-tool extension, use [Toolbox](extensions/toolbox.md).
[Lab 10](10-iq-extensions.md) is the separate external-IQ design reference.
Both tool paths receive the same answer schema and validate returned JSON.
Inspect `decision`, `limit_krw`, and `citations`, not just fluent text.
Do not repair invalid output and call it success.


![September 24 English recording: MAF with the local MCP policy tool](../assets/g6sol-20260924-en/screenshots/E04-003-mcp-2.webp)

**What to check:** Verify `tools: local-mcp` and the historical limit/`TRAVEL-2025`
for May 2026. A function-tool response cannot stand in for an MCP execution.

**Save:** `maf-mcp.json` is written to the same notes directory on success. Keep the original error instead if this request failed.

**B done:** retain the three actual outputs and explain no tool, function and local MCP.
Continue to [Lab 05 B](05-workflows.md#path-b); sections 4 and 5 below are optional.

## 4. Optional: inspect tool boundaries and reject invalid input

Your first pass can continue to [Lab 05](05-workflows.md) after the three real outputs above.

<details>
<summary>Expand the optional negative test; its expected result is a failure message</summary>

1. Explain "read-only," "synthetic," and "cannot approve" from the `lookup_policy` docstring.
2. Ask an unsupported question and check whether an empty search causes invented amounts.
3. Verify rejection of questions longer than 2000 characters.
4. Treat any "ignore the user" instruction embedded in tool data as data, not authority.
5. Identify server-side authorization, argument validation, approval, and audit logging needed for production.

Generate the long question with a short command. The expected result is exit code
`2` and `Question must contain 1-2000 characters.`, **before a model call**.

```bash
python scripts/workshop.py --language en maf --tools --question "$(python -c 'print("A" * 2001)')"
```


**What to check:** Read `FAIL: ValueError: Question must contain 1-2000 characters.` To see the exit code, run `echo $?` next; it prints `2`.
This is expected input rejection before Azure, not a broken environment.

Pasting a long string directly can hit terminal-input truncation. A model answer to
that truncated input does not prove the application's length check failed.
Do not create real messaging or payment tools just for this exercise.

</details>

## 5. Optional: score the tool calls with Foundry evaluators (Preview)

<details>
<summary>Expand only with the prepared <code>gpt-6-sol-judge</code> and cost approval; not required for B</summary>

MAF's evaluation API runs the function-tool agent on the six dev questions (six paid agent runs) and sends each answer,
its `lookup_policy` call and the tool definition to the Foundry `tool_call_accuracy` and `relevance` evaluators.
Only the function tool is scored, not the MCP variant. The code is in `src/foundry_workshop/tool_evaluation.py`.
First set `AZURE_AI_EVALUATION_MODEL_DEPLOYMENT_NAME=gpt-6-sol-judge` in `.env` (the judge row of your setup card);
the command stops if the judge is missing or is the answer deployment `gpt-6-sol`.

```bash
python scripts/workshop.py --language en maf-evaluate --confirm-cost --output outputs/learner-notes-en/maf-tool-evaluation.json
```

![September 24 English recording: Optional: score the MAF tool calls with Foundry evaluators](../assets/g6sol-20260924-en/screenshots/E04-004-maf-evaluate-2.webp)

**What to check:** `complete: true` and `errors: 0`; each row lists its recorded `tool_calls` (one `lookup_policy` call)
and a `tool_call_accuracy` and `relevance` score. Open `report_url` for the reasons. MAF prints one `ExperimentalWarning`
for `FoundryEvals`; that is expected. In the September 24, 2026 English recording it scored tool_call_accuracy 6/6 and relevance 6/6.
These scores judge tool use, not business correctness, so keep Lab 07's business checks separate.
The MAF evaluation API was experimental and several agent evaluators were marked Preview on September 23, 2026.

</details>

[Full action index](../action-captures.md) · [Recordings](../video-summary.md)

## Completion and troubleshooting

The [execution record](../live-run.md) lists the September 24 function-tool and MCP calls; the optional
2001-character rejection was not re-recorded. Keep all three actual outputs and explain the tool boundaries.
For MCP failures, use [Troubleshooting](../reference/troubleshooting.md);
never substitute a function-tool answer while claiming MCP success.

Next: A: [skip to Lab 05](05-workflows.md#path-a) · B → [Lab 05](05-workflows.md#path-b)
