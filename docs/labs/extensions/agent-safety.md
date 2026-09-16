# Agent safety: verify an applied control, not just a policy name

**English** | [한국어](../../ko/labs/extensions/agent-safety.md)

**Path C, optional; agent/tool intervention controls include Preview features as of September 16, 2026.**
Use only a dedicated lab agent and the bundled synthetic policy questions.
Do not weaken a shared guardrail, access company data or create real booking/payment tools.

**Need:** an actual lab agent/version, an owner-created RAI policy on the same Foundry account,
permission to attach it, an approved test scope and cost budget.
**Stop when:** the actual policy exists, the selected agent references it, and allowed/blocked or unblocked outcomes are recorded accurately.
**If blocked:** preserve the policy/agent IDs and error; do not disable controls to manufacture a success.

## 1. Separate the controls

| Control | What it addresses | What it does not establish |
|---|---|---|
| Azure RBAC | Which identity can access a resource | Whether an answer is correct |
| Agent/content guardrail | A configured risk at an input/output intervention point | Business authorization or every kind of safety |
| Tool-call/tool-response control | Agentic input/output risks at tool boundaries | Permission to execute a tool |
| Network egress rule | Which outbound destinations a hosted agent can reach | Correctness of data at an allowed destination |
| Human approval | A person's authorized decision about a particular action | A substitute for input validation or scoped permissions |

Start with one owner-approved control and one test goal.
An ordinary instruction to “follow the rules” is not proof that a platform guardrail was applied.

## 2. Record a baseline without changing shared controls

Use an existing response from your dedicated synthetic agent if available.
Inspect a normal policy question and dev D06's instruction to ignore the approval boundary.
Do not generate harmful content merely to fill a safety screenshot.

Record the exact agent/version, tool set, policy configuration, question and actual result.
A correct D06 refusal alone is not proof of a guardrail intervention; the model may have followed its instructions.

## 3. Verify the actual RAI policy

The owner supplies the **full ARM resource ID** of an existing or newly approved lab policy:

```text
/subscriptions/<subscription>/resourceGroups/<group>/providers/Microsoft.CognitiveServices/accounts/<account>/raiPolicies/<policy-name>
```

Read that policy in the account's guardrail management view before attaching it.
Confirm the intended controls, intervention points and blocking behavior.
Do not edit `Microsoft.DefaultV2` or another team's policy.

**An active agent is not proof of a valid guardrail.** A nonexistent policy ID can fail open on some subscriptions.
You must verify the policy resource itself and observe the resulting behavior.

## 4. Attach to an owned Hosted agent version

For azd, edit only the intended service in its generated `azure.yaml`:

```yaml
policies:
  - type: rai_policy
    raiPolicyName: <actual-full-RAI-policy-ARM-ID>
```

This is a mapping inside the existing agent service, not a complete replacement `azure.yaml`.
azd maps it to the agent definition's `rai_config.rai_policy_name`.
Do not put it in `agent.manifest.yaml` and assume deploy reads that file.

After deployment approval:

```bash
azd deploy
azd ai agent show --output json
```

This example assumes exactly one owned service. In a multi-service project, select only the intended service.
Record the new actual version and policy reference. Do not reuse a previous version's quality score.

## 5. Test the declared intervention

Run only the approved synthetic cases against the new exact version.
Inspect actual response status, guardrail annotations or blocking details, and any corresponding trace.

Keep these outcomes separate:

- The policy was attached.
- The request completed or was blocked.
- The expected control actually intervened.
- The underlying answer remained correct.

If D06 is not blocked, record that result. Do not invent a block or lower the threshold until the screenshot looks right.
A business-boundary refusal and a platform safety block are different evidence.

For network egress controls, use a separate approved allow/deny test against non-sensitive destinations.
Do not alter shared networking or describe an unconfigured private network as tested.

<!-- edition-checkpoint:EP21-006-honest-safety-outcomes -->

![Recorded English checkpoint: Preserve both unblocked outcomes and stop only their owned sessions; do not claim a filter intervention](../../assets/edition-20260916-en/screenshots/EP21-006-honest-safety-outcomes-2.webp)

**What to check:** Both original cases were unblocked. The correct approval-boundary refusal does not prove that a platform filter intervened. Your resource names and IDs will differ.

[Watch this recorded action](https://github.com/user-attachments/assets/798a020d-664c-480e-83ba-f2cb381139da#t=629.56) · [All actions and failures](../../edition-actions.md)

## 6. Optional AI red teaming

Cloud red teaming is a separate evaluation workload, not the same as replaying six dev questions.
Its generated attack inputs and results require their own lineage and budget.

The [current cloud workflow](https://learn.microsoft.com/azure/foundry/how-to/develop/run-ai-red-teaming-cloud)
uses an explicit target name/version, a red-team evaluation group, and a taxonomy for agentic prohibited-action tests.
Use only the policy assistant's permitted scope; generated material must not introduce real data or live business actions.

Before submitting a scan:

1. Pin the target agent/version and record its tool/guardrail definitions.
2. Generate or provide a taxonomy scoped to the approved synthetic policy.
3. Review the taxonomy before using it to generate attacks. A pending review remains pending.
4. Select the smallest supported strategy/turn budget appropriate to the test and obtain cost approval.
5. Submit one run; retain its taxonomy version, strategy settings, every input/output/error and actual denominator.
6. Review Attack Success Rate and individual failures separately from ordinary business/native quality scores.

If the taxonomy cannot be reviewed or the service/region is unavailable, record **red-team scan not run**.
Do not relabel local D06 checks as a cloud red-team scan.

## 7. Restore only your additions

Retain the baseline and tested policy/agent versions, actual responses and findings.
Restore or remove only the newly created lab policy/attachment after checking references.
Do not delete shared policies, models or evaluation evidence.

**Next:** [Governance and identity](governance-networking.md), [C module selection](../../paths/c-advanced.md), or [Lab 11](../11-capstone.md).
[Hosted guardrail attachment and fail-open warning](https://learn.microsoft.com/azure/foundry/agents/how-to/add-hosted-agent-guardrails) ·
[Guardrail intervention points](https://learn.microsoft.com/azure/foundry/guardrails/guardrails-overview).
