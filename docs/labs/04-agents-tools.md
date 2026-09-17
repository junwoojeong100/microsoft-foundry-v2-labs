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

## 1. Agent without tools

Run from the repository root with `.venv` active. All three commands make billable model calls.
After each succeeds, save its complete JSON as `maf-none.json`, `maf-function.json` or `maf-mcp.json`
in your Lab 00 notes directory. These commands do not create labeled run folders.

```bash
python scripts/workshop.py --language en maf --question "Explain the difference between Foundry and Agent Framework in three sentences."
```

The question asks for a three-sentence explanation of Foundry versus Agent Framework.


**What to check:** Read `mode: live`, `orchestration: local`, and `tools: none`.
Local Python owns execution, but the answer model is called in Azure.

**Save:** `maf-none.json` in your Lab 00 notes directory.

Open `src/foundry_workshop/agents.py` and locate:

1. `FoundryChatClient`: the project and deployment it calls.
2. `Agent`: the name, instructions, tools, and execution options.
3. `agent.run()`: the actual model request.

Creating an `Agent` object does not automatically register a managed portal agent.
This one belongs to your Python process. Compare it with
`project.agents.create_version()` in [Lab 03](03-prompt-agent.md).

## 2. Read-only function tool

```bash
python scripts/workshop.py --language en maf --tools --question "My domestic business-trip hotel in September 2026 costs KRW 170000. May I book it? State the limit and procedure."
```

Meaning: may I book a KRW 170000 domestic hotel in September 2026; what limit and
procedure apply? `lookup_policy` reads only bundled synthetic JSON, not the Internet
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



**What to check:** Inspect `tools: function` and the nested `decision`, `limit_krw`,
and `citations`. `needs_approval` means prior human approval is required, not granted.

Verify evidence corresponding to `TRAVEL-2026` and `APPROVAL-01`, an explanation without
booking/approving, and that `never_require` applies only to **side-effect-free synthetic lookup**.
If the model skips the tool or evidence, inspect the actual answer, instructions,
tool description, and tracing. A connected tool alone is not success.

**Save:** `maf-function.json` in the same notes directory before starting MCP.

## 3. Move the same lookup into a local MCP server

```bash
python scripts/workshop.py --language en maf --mcp --question "What was the domestic business-trip lodging limit per night in May 2026?"
```

Meaning: what is the per-night domestic lodging limit in May 2026?
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


**What to check:** Verify `tools: local-mcp` and the historical limit/`TRAVEL-2025`
for May 2026. A function-tool response cannot stand in for an MCP execution.

**Save:** `maf-mcp.json` in the same notes directory. Keep the original error instead if this request failed.

**B done:** retain the three actual outputs and explain no tool, function and local MCP.
Continue to [Lab 05 B](05-workflows.md#path-b); the negative test below is optional.

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


**What to check:** Read `FAIL: Question must contain 1-2000 characters.` and exit code `2`.
This is expected input rejection before Azure, not a broken environment.

Pasting a long string directly can hit terminal-input truncation. A model answer to
that truncated input does not prove the application's length check failed.
Do not create real messaging or payment tools just for this exercise.

</details>

<details>
<summary>Recorded reference screens (optional; not steps to repeat)</summary>

These are newly recorded English actions using the separate English prompt/data bundle. Use your own returned resource IDs and record your own results.

![Run the real MAF agent](../assets/refresh-20260915-en/screenshots/E04-100-maf-2.webp)

**What to check:** Read the actual command/output and distinguish no tool, the local function, and the separate MCP server.

![Invoke the read-only function tool](../assets/refresh-20260915-en/screenshots/E04-101-tools-2.webp)

**What to check:** Read the actual command/output and distinguish no tool, the local function, and the separate MCP server.

![Use the real local MCP policy tool](../assets/refresh-20260915-en/screenshots/E04-102-mcp-2.webp)

**What to check:** Read the actual command/output and distinguish no tool, the local function, and the separate MCP server.

[Full action index](../action-captures.md) · [Recordings](../video-summary.md)

</details>

## Completion and troubleshooting

The [source execution record](../live-run.md) includes function/MCP calls and exact
2001-character rejection. Keep all three actual outputs and explain the tool boundaries.
For MCP failures, use [Troubleshooting](../reference/troubleshooting.md);
never substitute a function-tool answer while claiming MCP success.

Next: A: [skip to Lab 05](05-workflows.md#path-a) · B → [Lab 05](05-workflows.md#path-b)
