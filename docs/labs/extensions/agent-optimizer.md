# Agent Optimizer: generate candidates, review the evidence

**English** | [한국어](../../ko/labs/extensions/agent-optimizer.md)

**Path C, optional Preview — September 16, 2026.**
This first pass uses the **Prompt Agent optimization wizard**. It is not fine-tuning and does not change model weights.
Keep the existing Hosted matrix and manual v1/v2 experiments as separate targets and records.

**Need:** a dedicated synthetic Prompt Agent, its exact baseline version, the derived dev file,
an owner-verified supported optimizer deployment, a separate evaluator deployment and cost approval.
**Stop when:** one run has a checked baseline and every returned candidate, including an explicit baseline-only/no-improvement outcome.
**If blocked:** do not create another model, modify holdout, or promote a candidate to finish a recording.

**First pass:** steps 1–5, then hand off `optimizer-review.txt`. Promotion is not required;
baseline-only, no improvement or invalid evaluator binding are valid findings to retain, not successful promotion.

## 1. Prepare the inputs once

Use the [Lab 03](../03-prompt-agent.md) agent built with all six inline synthetic policies.
For an isolated experiment, create a new agent with your own prefix and preserve the baseline instructions/version.
Do not optimize a shared agent or change a previously frozen benchmark target.

If `outputs/extensions-en/` is not already prepared:

```bash
python scripts/workshop.py --language en prepare-extensions --label extensions-en
```

Open `optimizer-dev.jsonl`, `SOURCE.json` and `manifest.json`.
The six records derive from canonical **dev**; no holdout or new target answers were generated.
The `query` is the agent input. `context` and `ground_truth` are evaluation references, not instructions to send to the target.
The wizard does not offer arbitrary column mapping: verify its required columns before submitting.

| Input | Required choice |
|---|---|
| Target agent | Dedicated synthetic Prompt Agent and its actual baseline version |
| Target model | The existing verified answer deployment; do not add a model-comparison branch on the first pass |
| Optimizer model | A supported **existing** deployment confirmed by the owner and wizard |
| Evaluator model | A separately named approved judge deployment |
| Dataset | The six-row `optimizer-dev.jsonl`, never holdout |
| Candidate limit | **2** for this bounded first pass |
| Targets to optimize | **Instructions only** initially |

If the prepared project has no supported optimizer model, record **not run** and stop.
A working answer model is not automatically a supported optimizer model.
On September 23, 2026 the training project's agent **Optimize** tab showed **No supported optimization model** with only
`gpt-6-sol` deployed, so this module was not re-run with the `gpt-6-sol` preset; deploying another model is an owner decision.

## 2. Open the optimization wizard

1. In Foundry, open **Agents → your dedicated agent → Optimize Preview**.
2. On a first-use page, select **Optimize my agent**. If runs already exist, use **Create optimization run** instead.
3. In **Target**, explicitly choose the baseline version rather than accepting an unknown latest default.
4. Select the prepared optimizer/evaluator deployments and set the candidate limit to 2.
5. Choose **Choose targets**, select **Instruction**, and clear **Model**.
   The observed wizard preselected Model after switching to explicit targets, so check the actual boxes.

Record the agent name/version, selected deployments and original instructions before continuing.
An optimizer model generates changes; the target answers questions; the judge scores answers. These are different roles.
The first-use page can show a product/example benchmark. Those advertised scores are not this workshop's baseline or results.

## 3. Select dev data and criteria

1. In **Data**, choose **Select dataset and criteria**. Do not use the default production-trace generation option.
2. Select **Upload dataset**, give it your own language-specific name, and upload `outputs/extensions-en/optimizer-dev.jsonl`.
3. Confirm that the selected dataset is your new version and has `case_id`, `query`, `context`, and `ground_truth`.
   The portal preview shows only the **top five rows**; verify all six in the source file and later in the actual evaluation outputs.
4. In **Criteria**, clear **Custom only**. Select **Groundedness-Evaluator** and **Relevance-Evaluator**,
   not the similarly named Service-Groundedness variant. Use threshold **4** for both.
5. Record their actual versions and keep the same criteria, thresholds and reference data across the run.

Do not weaken required citations, turn an approval refusal into an error, or omit a difficult case to improve the result.
If the service reports a schema mismatch, stop and inspect the actual requirements;
do not silently rename columns or send evaluator labels to the target.

## 4. Review costs and submit once

In **Review**, verify the baseline, dataset, evaluator settings, deployments and maximum candidates.
Expand the cost breakdown for running the agent, scoring responses and generating improvements.
The displayed range is an **estimate**, not a spending cap.

After approval, select **Submit** once. Save the run ID and inspect that same run until it finishes.
Do not submit another job because the first one is waiting or because a screenshot is missing.

An incomplete/failed run is not an improved candidate.
Retain the error and partial artifacts without presenting the successful subset as a completed optimization.

## 5. Read candidates before considering promotion

For every candidate, retain:

- Complete evaluator results and the actual case denominator.
- The before/after instruction diff and any changed model/tool settings.
- Actual token usage by model/phase, with missing measurements kept missing.
- Failure cases and whether the proposed wording still preserves evidence, dates and approval boundaries.

The highest aggregate score is a **proposal**, not automatic acceptance.
If all candidates are worse or indistinguishable on this small dataset, keep the baseline.
Changing wording without a useful measured improvement is not a success claim.
The September 16 English run (earlier `gpt-5.6-luna` edition; not re-run with `gpt-6-sol`) returned only the baseline.
Its generic early-stop message said the samples were perfect, but detailed results included a failed D05 relevance score.
Read the individual rows rather than treating a successful job status or generic message as all-pass evidence.

**Check the actual judge input, not only the uploaded columns.** Compare each evaluator's
`sample.input` with the frozen dataset. The September 16 English baseline and all Korean candidates
used the generated answer itself as the Groundedness `context`.
That self-comparison does not establish grounding in the original policies, even when the service reports 6/6.
Keep the original scores and input hashes, mark the reference binding invalid, and **do not promote on that result**.
Do not silently repair columns, relax thresholds or submit another run to produce a better-looking recording.

Save an `optimizer-review.txt` containing the run ID, baseline/candidate IDs, findings,
the selected candidate **or** `pending-human-review`, and the review reason.
Do not impersonate a human reviewer in that record.

## 6. Promote only after a person approves

<details>
<summary>Optional promotion — never the automatic next step after an optimizer run</summary>

If no human has reviewed the candidate, this step remains **not performed**.
That is a valid recorded boundary, not a reason to fabricate approval.

After explicit approval, use **Promote candidate → Promote to agent version**.
Record the new actual version and whether the active/default version changed.
Test the new version under a new label before using it as a future baseline.
Do not overwrite old responses or claim a previous version's holdout applies automatically.

Only after the candidate is frozen may a separately designed final-acceptance process use holdout.
This optimizer run never opens holdout for candidate development.

</details>

## Optional targets after the first pass

Function-tool description optimization is not tool execution validation:
Prompt Agent functions run on the client, and the optimizer cannot execute those functions during that optimization.
Hosted optimization requires optimizer-ready code and baseline configuration, and may execute actual tools repeatedly.
Keep it in a separate prepared workspace with read-only synthetic tools and reviewed costs.
It is not enabled by adding a flag to this portal exercise.

**Next:** [Conversation evaluation](conversation-evaluation.md), [C module selection](../../paths/c-advanced.md), or [Lab 11 handoff](../11-capstone.md).

[Prompt optimization wizard](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-optimize-prompt-agent) ·
[Agent-type capabilities and constraints](https://learn.microsoft.com/azure/foundry/agents/concepts/agent-optimizer-overview) ·
[Cost and token accounting](https://learn.microsoft.com/azure/foundry/agents/concepts/agent-optimizer-costs).
