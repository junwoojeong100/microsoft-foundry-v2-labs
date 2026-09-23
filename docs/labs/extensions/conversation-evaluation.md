# Evaluate a conversation, not just its last answer

**English** | [한국어](../../ko/labs/extensions/conversation-evaluation.md)

**Path C.** Complete [Lab 07](../07-evaluation.md) first.
The existing matrix evaluates isolated cases. This module instead sends the same six **dev** questions
as two three-turn conversations, retaining each conversation's earlier answers.

**Need:** working model/Structured Outputs, a separate judge deployment, new labels and cost approval.
**Stop when:** six turn records and two complete conversation records exist, with separate native results at both levels.
**If blocked:** keep partial/error records; never evaluate only the successful prefix.

**First pass:** steps 1–6, in order. Keep the same collection label for both evaluation levels;
a new target conversation needs a new label, but polling the saved judge job does not.

**Evidence status, September 16, 2026 (earlier `gpt-5.6-luna` edition):** the English six-turn collection and both native
evaluation levels ran; they were not re-run with the `gpt-6-sol` preset.
Each execution freezes the real evaluator catalog it reads; catalog availability alone is not an evaluation result.

## 1. Read the plan before calling a model

```bash
python scripts/workshop.py --language en conversations plan
```

| Conversation | Canonical dev turns | What the interaction tests |
|---|---|---|
| `dates-and-approval` | D01 → D02 → D03 | Changing the travel date and then asking about an over-limit hotel |
| `scope-and-boundaries` | D04 → D05 → D06 | Different policy scope and resisting a request to ignore constraints |

The plan uses all six original dev questions exactly once. It does not generate new questions or read holdout.
The source context is the complete six-document synthetic bundle, **not an IQ or Toolbox call**.
This keeps the first multi-turn experiment focused on conversation behavior rather than a simultaneous retrieval change.

Maximum target work is **six logical model turns**; service/SDK retries can add usage.
Native turn evaluation has six input items; whole-conversation evaluation has two.
Those denominators are different and must not be compared as if they measured the same unit.

## 2. Collect actual conversations once

```bash
python scripts/workshop.py --language en conversations collect --label conversations-first --prompt v2 --confirm-cost
```

Open `outputs/conversations/conversations-first/`:

| File | What to verify |
|---|---|
| `plan.json`, `corpus.json`, `manifest.json` | Language, exact inputs, hashes, model configuration and run ID |
| `D01-request.json` … `D06-request.json` | Only actual questions/history and synthetic evidence; no reference-answer fields |
| Per-turn response files | Original text/structured response, service IDs, usage and any errors |
| `turns.json` | Six rows, including errors or turns blocked by an earlier failure |
| `conversations.json` | Two separate histories; the second must not inherit the first |
| `business-evaluation.json` | Original per-case business checks, not a semantic conversation score |

Within one conversation, the next turn sees previous actual answers.
Each new conversation starts from fresh state. The code sends explicit history and uses `store=False`;
it does not claim to create a managed memory store or an Azure conversation resource.

If a turn fails, later turns of that conversation are marked blocked rather than fabricated.
The other independent conversation can still run. The original six-case denominator remains visible.
Native evaluation requires a complete real collection and will not score the surviving subset.

## 3. Inspect local business checks

```bash
python scripts/workshop.py --language en conversations report --label conversations-first
```

Review the current/historical limits, required citations and approval decisions in all six rows.
A conversation passing all local turn checks is **not** proof of coherence, successful task resolution or safe production behavior.
Keep wrong answers unchanged; the report never repairs them.

## 4. Evaluate individual turns with prior context

Set the same separate `AZURE_AI_EVALUATION_MODEL_DEPLOYMENT_NAME` used for approved judge work.
Do not use the target deployment as its own judge.

```bash
python scripts/workshop.py --language en conversations evaluate --label conversations-first --level turn --confirm-cost
```

Each input contains the history through one target answer.
The command checks the real evaluator catalog for the requested level and preserves its version, schema and threshold.
Read all **six** result items under `native-turn/`.

## 5. Evaluate complete conversations

```bash
python scripts/workshop.py --language en conversations evaluate --label conversations-first --level conversation --confirm-cost
```

This uses explicit `evaluation_level: conversation`, full message histories,
and the catalog-compatible groundedness/coherence evaluators.
Read all **two** result items under `native-conversation/`.
Turn-only evaluators such as relevance must not be copied into this step without checking supported levels.

Compare the reasons, not just pass percentages:

1. Did the agent revise the applicable date instead of repeating the prior amount?
2. Did it keep meal, lodging and international-travel scope separate?
3. Did it retain the approval boundary when a later user turn challenged it?
4. Does the native explanation match the actual transcript and business policy?

Generic evaluator disagreement is a finding to review, not permission to edit the score or repeatedly rerun for a favorable result.
A timeout resumes the same saved evaluation job when you rerun the same command; it does not silently create a new target conversation.

## 6. Handoff

Keep both native directories, their catalogs, all raw response/error files and the local business report.
Record that the scenario order is a **derived dev experiment**, not the unchanged isolated-case matrix and not a new holdout.
This module adds no automatic deployment approval.

**Next:** [C module selection](../../paths/c-advanced.md), or add the evidence to [Lab 11](../11-capstone.md).

[Official conversation evaluation](https://learn.microsoft.com/azure/foundry/observability/how-to/cloud-evaluation-conversations) ·
[Evaluation units and sources](https://learn.microsoft.com/azure/foundry/observability/how-to/cloud-evaluation).
