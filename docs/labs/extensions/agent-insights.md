# Insights in Foundry: from recurring trace patterns to a reviewed change

**English** | [한국어](../../ko/labs/extensions/agent-insights.md)

**Path C, optional Preview — checked 2026-09-24.**
Insights analyzes recent Foundry agent traces and proposes recurring behavior patterns to review.
It is decision support, not ground truth, and it does not replace the evaluation workflow.

**Evidence status:** Not run in this edition yet (added 2026-09-24).

**Need:** the learner's own Lab 03 Prompt Agent, connected Application Insights, recent representative synthetic dev traces,
an owner-prepared `gpt-6-sol-judge` judge deployment, and owner-prepared roles. Learners do not assign roles.
**Stop when:** one Insight is reviewed against its linked traces and the synthetic policies, and the human decision is recorded.
**If blocked:** record the missing prerequisite, or write **not enough traces** when the agent has too few representative traces.

**First pass:** steps 1–5. Do not generate new traffic just to fill Insights.
Use the existing synthetic dev traffic/traces from Lab 03 and later Lab 07 dev checks.

## 1. Confirm owner-prepared prerequisites

The environment owner prepares the access before class:

| Prerequisite | Owner-prepared requirement |
|---|---|
| Application Insights | Connected to the Foundry project before the scan |
| Learner access | Foundry User for the prompt agent and Monitoring Reader on the connected Application Insights |
| Project managed identity | Monitoring Reader on the connected Application Insights |
| Protected content tables | Privileged Monitoring Data Reader when `AppGenAIContent` is protected |
| Judge deployment | Project managed identity can call `gpt-6-sol-judge` |
| Trace data | Recent synthetic, representative traces from the learner's own agent |

Do not add roles, change the project identity, or switch the default subscription as part of this module.
Local MAF runs do not create Foundry server-side traces unless separate client-side tracing was implemented.

## 2. Start a bounded scan in the portal

1. Open Foundry.
2. Go to **Build → Agents**.
3. Open your Lab 03 Prompt Agent.
4. Open **Insights**.
5. Choose Judge model **`gpt-6-sol-judge`**.
6. Select **Run scan now**.

The first scan looks back over recent traces. If the page reports too few traces, record **not enough traces**
and stop. Do not send extra prompts only to create a more interesting Insight.

The Python SDK exposes `beta` Agent Insight operations in `azure-ai-projects` 2.6.x, but this workshop module uses
the portal and adds no SDK code.

## 3. Review one Insight, not just its severity

Open one returned Insight and retain:

| Field | What to check |
|---|---|
| Category and severity | Triage hints only; severity does not replace risk assessment |
| Linked/highlighted traces | Open the actual trace evidence and compare it with the Insight summary |
| Likely cause | Verify whether the cause follows from the linked traces |
| Proposed action | Check whether it preserves synthetic policy scope, dates, citations and approval boundaries |

An AI-generated Insight can be incomplete, stale or wrong.
Do not report an Insight as a defect until a person has reviewed the trace evidence.

## 4. Choose a human decision

Record one of these outcomes in `insights-review.txt`:

| Decision | Boundary |
|---|---|
| Evaluate | Add or prioritize a dev evaluation case derived from the existing synthetic policy scenario |
| Change instructions in a new version | Create a reviewed candidate version; do not overwrite the current baseline |
| Route | Send the finding to the owner of data, tools, access or operations |
| No action | Keep the evidence and reason when the Insight is not actionable or is unsupported |

If the decision changes instructions, test only on dev through the Lab 07 process.
Holdout opens only after a candidate is frozen.

## 5. Cost and cleanup

Insight generation calls the selected judge model and can add cost.
Record the scan time, judge deployment and whether scheduled generation was enabled.
If you enabled scheduled generation for an experiment, pause it before finishing unless the owner explicitly keeps it.

**Next:** [Conversation evaluation](conversation-evaluation.md), [Model operations](model-operations.md), or [C module selection](../../paths/c-advanced.md).

[Agent Insights](https://learn.microsoft.com/azure/foundry/observability/how-to/agent-insights) ·
[Tracing setup](https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup).
