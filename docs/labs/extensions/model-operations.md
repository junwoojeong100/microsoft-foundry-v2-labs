# Model operations: compare deliberately, preserve rollback

**English** | [한국어](../../ko/labs/extensions/model-operations.md)

**Path C.** Model migration is more than changing a deployment name.

**Evidence status:** last run September 16, 2026 with the earlier `gpt-5.6-luna` preset; not re-run with `gpt-6-sol`, and no Router migration is claimed.

The first pass compares **two already approved deployments** with the same dev inputs;
Router and retirement planning are separate extensions.
When the learning goal is provider diversity, prefer making the second approved deployment a non-OpenAI Foundry Model,
for example a Grok model whose Azure documentation lists Responses API support (checked 2026-09-24).

**Need:** the real [Lab 07](../07-evaluation.md) candidate, a second approved deployment,
matching API/Structured Outputs support, cost approval and new labels.
**Stop when:** the comparison includes actual model identities, all rows/errors and a written migration decision.
**If blocked:** retain the existing model; never let an error choose another deployment or endpoint.

**First pass:** steps 1–4; save a `model-migration-review.txt` beside your notes.
Record the compared labels, decision and unchanged original setting. Router and retirement actions are not required.

## 1. Freeze the baseline

Record the candidate's actual deployment/model/version, project/API, prompt, corpus, retrieval,
output limit and data hashes. Preserve its original run directory.
Do not use a Router as a fixed-model baseline or reuse results from another language.

The new deployment must already exist and be permitted in the same experiment.
This lab does not deploy models or increase quota.

## 2. Check the second model without changing your saved setup

Keep `.env` unchanged. Enter the approved second **deployment name**, not its catalog model name.
The parentheses limit the override to this read-only preflight; all other settings remain the same.

```bash
printf 'Approved second deployment name: '
read -r MODEL_B
(
  export AZURE_AI_MODEL_DEPLOYMENT_NAME="${MODEL_B:?Enter the approved second deployment}"
  python scripts/workshop.py --language en doctor --cloud
)
```

Confirm the actual underlying model/version and deployment state.
If the API or output schema is incompatible, stop. That is a migration finding, not permission to use another API for only this model.
For a non-OpenAI provider, the project Responses path and strict `json_schema` Structured Outputs must both be accepted.
If either is rejected, stop and record an API-compatibility finding. Do not switch APIs, loosen the schema or fall back to plain text.
Keep `MODEL_B` in this terminal for step 3; a missing value stops before any request.

## 3. Collect a new dev run and compare

If the original candidate used the Lab 07 `local` example:

```bash
(
  export AZURE_AI_MODEL_DEPLOYMENT_NAME="${MODEL_B:?Enter the approved second deployment}"
  python scripts/workshop.py --language en collect --split dev --label migration-model-b --prompt v2 --retrieval local
)
```

Inspect all six collected rows, then run the local checks. These read the saved deployment from the run, not a new model choice:

```bash
python scripts/workshop.py --language en evaluate --label migration-model-b
python scripts/workshop.py --language en compare --baseline candidate --candidate migration-model-b --variable model
```

If your baseline used another provider, explicitly use that same provider throughout this separate comparison.
Do not replace only the failed cases or omit errors from the denominator.
Inspect amounts, dates, citations, approval behavior, latency and token measurements together.
Both subshells leave the original terminal deployment and `.env` unchanged, including after failure.
Do not permanently switch the answer deployment unless a migration is separately approved.

## 4. Write the lifecycle plan

| Phase | Your evidence |
|---|---|
| Discover | Actual retirement notice/date or a documented reason to migrate |
| Assess | Supported model, region, quota, API and policy fit |
| Adapt | Reviewed prompt/schema/tool changes in a separate version |
| Validate | Controlled dev comparison; final acceptance only after freezing the candidate |
| Roll out | Approved small rollout, monitored actual version and rollback trigger |
| Retire | Confirm no active callers require the old deployment before its owner removes it |

Check `versionUpgradeOption` and the actual deployment type with the owner.
An endpoint continuing to answer after an automatic model upgrade does not prove unchanged behavior.
Do not change shared upgrade settings or delete a shared model as part of a learner's experiment.

## Optional: compare Model Router as a different target

<details>
<summary>Separate Router experiment — not the next step after the two-model comparison</summary>

A Router is an explicitly selected routing system, not the fallback for a failed direct model.
Before testing it, record its version, routing mode and permitted model subset.
Use the same representative dev workload and read quality, estimated cost, latency and **actual selected-model distribution** together.

Use the [official Router evaluation methodology](https://learn.microsoft.com/azure/foundry/openai/how-to/evaluate-model-router)
to choose metrics and workload categories. Keep mock reports visibly distinct from real requests.
Do not report a fixed-model ranking or statistical superiority from this workshop's tiny dataset.
If a Router deployment is not prepared, record **Router not run**; do not create one implicitly.

</details>

**Next:** [Lab 11](../11-capstone.md) with the comparison, migration/rollback plan and unverified items.
[Official model migration lifecycle](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/model-migration).
