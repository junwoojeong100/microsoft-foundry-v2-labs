# Lab 05. MAF workflows and human review

**English** | [한국어](../ko/labs/05-workflows.md)

<!-- translation-pending: ko-integrated-20260915 -->

> **Translation pending** — The [Korean-first integration revision](../ko/labs/05-workflows.md) is current for the new workflow/evaluation curriculum. This English page retains the earlier material. English expansion and new media follow Korean execution, capture, and corrections.

**Goal:** Connect agents in MAF code and distinguish a reviewer model from an actual approver.

Previous: A → [Lab 03](03-prompt-agent.md), B → [Lab 04](04-agents-tools.md) · Next: [Lab 06](06-knowledge.md)

## This lab uses MAF workflows only

Do not create/connect/publish nodes in the portal Workflow Designer.
**Microsoft Agent Framework Python code** owns roles, order, and termination.
Foundry supplies the model and optional hosting/observability.
Using the Agent Playground is different from authoring a workflow in the portal.

## A. Beginner: run the prepared example yourself

No code authoring is required. The instructor provides the repository, Python/SDKs,
learner-authorized Azure sign-in, `.env`, and an activated venv in a **prepared MAF
environment**. Use its browser IDE or VS Code terminal; never share an administrator account.

Three roles process the same travel question:

```mermaid
flowchart LR
    Q["Question and synthetic evidence"] --> A["MAF / PolicyAnalyst"]
    A --> W["MAF / AnswerWriter"]
    W --> R["MAF / EvidenceReviewer"]
    R --> H{"Human review"}
    H -->|Reject| W
    H -->|Finalize guidance| D["Guidance to user"]
    D -. "Not executed by this lab" .-> X["Booking / Actual approval / Payment"]
```

### 1. Run one sequential command

Confirm the prepared terminal is at the repository root. This command makes real,
billable Azure model calls within the instructor's budget.

```bash
python scripts/workshop.py workflow --pattern sequential --question "2026년 9월 국내 출장 호텔이 170000원입니다. 적용 한도와 예약 전 필요한 절차를 알려주세요."
```

Meaning: a domestic hotel costs KRW 170000 in September 2026; explain the applicable
limit and the steps required before booking.

![Prepared sequential MAF example for the beginner path](../assets/live-20260914-action/shots/cli-1-0404-05-003-beginner-sequential-result.webp)

**What to check:** Read the last command's `pattern: sequential` and `outputs`.
This is a terminal-executed MAF result, not portal Workflow Designer activity.

### 2. Read the actual output

| Field | What it establishes |
|---|---|
| `mode: live`, `pattern: sequential` | Execution of the prepared MAF code |
| `outputs` | Current limit and advance-approval conditions supported by evidence |
| `approval_status: pending-human-review` | Model review has not become human approval |
| `external_actions_performed: false` | No actual booking/payment |

Run again with a historical travel date and compare the applied policy.
Personally read the answer and sources, then record corrections and the final guidance.

![Sequential result after changing the travel date to May 2026](../assets/live-20260914-action/shots/cli-1-0410-05-004-beginner-historical-result.webp)

**What to check:** Compare the changed policy and limit. Both runs must retain
`approval_status: pending-human-review` and `external_actions_performed: false`.

### 3. Determine completion

You need an **actual MAF run and human review record**.
Manually copying answers between portal conversations is not MAF execution.
If you only watched an instructor, record **MAF observed; personal execution incomplete**.
Local MAF does not create a managed workflow resource or Hosted Agent.

## B. Code: compare three orchestration patterns

All commands call a real Azure model. Inspect `run_workflow` in
`src/foundry_workshop/agents.py`. Keep data, model, and instructions fixed while
examining builders and execution order. No command creates a portal workflow resource.

| Concept | MAF implementation in this lab |
|---|---|
| Agent node | `Agent` + `FoundryChatClient`, role-specific instructions |
| Ordered connection | `SequentialBuilder(participants=...)` |
| Same input to multiple roles | `ConcurrentBuilder(participants=...)` |
| Short shared discussion | `GroupChatBuilder`, speaker selector, maximum rounds |
| Business approval boundary | Human review after output; production approval design is separate |

Branches, persisted state, and durable approval are not automatically migrated.
Explicitly design business state, errors, and retries in code.

### 1. Sequential: each stage feeds the next

```bash
python scripts/workshop.py workflow --pattern sequential
```

Compare `PolicyAnalyst → AnswerWriter → EvidenceReviewer` with the builder's participants
and actual outputs. An incorrect source interpretation can propagate to the draft.

![Sequential code-path output](../assets/live-20260914-action/shots/cli-1-0416-05-005-sequential-result.webp)

**What to check:** Map the output to the three roles. Fluent review does not
automatically remove an earlier evidence error.

### 2. Concurrent: independent views of the same input

```bash
python scripts/workshop.py workflow --pattern concurrent
```

`ConcurrentBuilder` sends the same question/evidence to three roles.
It returns three perspectives, **not automatic consensus or one final answer**.
Read and combine them yourself or design a separately validated aggregation step.
Lower wall-clock time does not necessarily mean fewer calls or lower costs.

**New English-guide capture: September 15, 2026.** ▶ [Watch this action](https://github.com/user-attachments/assets/082ede4b-d363-474c-ad47-598b20f593e9#t=388.76)

![Multiple perspectives returned by concurrent execution](../assets/english-20260915/shots/terminal-0143-05-004-concurrent-result.webp)

**What to check:** Verify `pattern: concurrent` and multiple participant outputs.
Compare them rather than treating them as an agreed answer.

### 3. Group Chat: shared discussion with a stopping rule

```bash
python scripts/workshop.py workflow --pattern group-chat
```

The example uses a fixed speaker order and at most **three rounds**.
`output_from=participants` retains real participant responses; a termination notice
alone is not a business answer. The entire workflow also has a 240-second timeout.
Calculate call/token budgets before increasing either bound.

![Actual Group Chat participant output and review boundary](../assets/live-20260914-action/shots/cli-1-0428-05-007-group-chat-result.webp)

**What to check:** Read `pattern: group-chat`, participant responses, and pending
human review. Reaching the round limit is not model consensus or business approval.

| Pattern | Appropriate use | Main caution |
|---|---|---|
| Sequential | Analysis, draft, review | Error propagation |
| Concurrent | Independent perspectives | Aggregation criteria and cost |
| Group Chat | Short mutual review/coordination | Stopping rules, repetition, conformity |
| Single agent | Simple rules | Do not add agents without a reason |

## Understand human-in-the-loop precisely

`approval_status: pending-human-review` is a **stop sign**, not an approval service.
No booking, email, or payment API exists here, so `external_actions_performed` is
`false`. **This is not persistent approval or a restartable durable workflow.**

A production extension must separately implement the request ID and draft hash,
approver Entra identity/authorization, approve/reject/expire states, idempotency and
retries, revalidation immediately before tools, persistence/restarts, audit records,
and rollback or compensation.

Telling a model "you are the approver" cannot replace human authorization.

## Completion

[Execution records](../live-run.md) distinguish actual patterns and recorded actions.
A retains a sequential run and human review. B compares call counts, output shapes,
and review effort for all three patterns. Concluding that one agent is better for this
scenario is valid; the number of agents is not a success metric.
