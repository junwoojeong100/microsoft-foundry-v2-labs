# Release operations: bounded monitoring and an explicit deployment gate

**English** | [한국어](../../ko/labs/extensions/release-operations.md)

**Path C, optional.** The repository's existing CI checks local logic, SDK contracts and documentation.
That is not a deployed-agent quality gate or continuous evaluation.
Do not enable recurring paid work or push a deployment without its own approval.

**First pass:** choose one lane, not both.

| Lane | Follow | Need / finish |
|---|---|---|
| Bounded monitoring | Steps 1–3 | Owned agent with one completed trace evaluation, trace access and budget; record the sample outcome and the paused schedule |
| CI release | Steps 4–6 | Owner-prepared GitHub OIDC and deployment/runtime permissions; retain the actual workflow result and rollback/cleanup decision |

**Need:** only the selected lane's prerequisites. Monitoring does not require a GitHub identity.
**Stop when:** its configuration, execution and quality decisions are recorded separately.
**If blocked:** retain the current deployment and report the missing permission/configuration; no success-shaped fallback.

## 1. Establish the evidence before automation

Reuse the existing evidence for your selected target. The [Hosted evaluation workbook](../../reference/evaluation-workbook.md)
is one way to obtain a full matrix, not a new mandatory run for this page.
Record the target version, model map, source/prompt/data hashes, native evaluator versions,
trace evidence and human acceptance status.

An automation workflow must not redefine thresholds after seeing a failing result.
It must not omit failed/missing cases or copy another target's scores.

## 2. Create a bounded recurring evaluation configuration

Start from one completed trace evaluation of your dedicated lab agent ([Lab 09 A](../09-operations.md#path-a)),
then select **Make recurring** on that evaluation's page.

Choose one mode, not both on the first pass:

| Mode | Purpose | First-pass boundary |
|---|---|---|
| Scheduled | Evaluate live traffic (or a dataset's existing data) on a schedule | A short, explicitly approved test; pause immediately afterward |
| Continuous | Sample agent traffic as it occurs | Lowest supported sampling/run limit; no uncontrolled traffic generation. Unavailable for trace evaluations on September 23, 2026 |

For the first pass keep **Scheduled** and **Live traffic**, set **Run interval** to 1 **Hourly**, keep **Random** sampling and set
**Maximum traces to evaluate per run** to `5`, then select **Save**. The page's button changes to **Pause**.
Record the schedule ID (listed by the SDK as `<agent>-scheduled-<suffix>`), agent/version filter, sampling mode, maximum traces,
evaluator versions, owner and pause plan.

Creating or enabling a schedule does not prove that a sample was evaluated.
Use one planned synthetic request, then inspect that schedule's runs.
Do not send repeated model calls solely to make a chart populate.

## 3. Inspect actual results, then pause

Scheduled runs appear on the same evaluation page next to the one-time run.
Verify each run's trace window, agent/version, sampled conversations, completed/failed status and individual findings.
Keep missing telemetry as **unverified**, not zero errors or zero cost.

On September 23, 2026 the first scheduled run started as soon as the schedule was saved, and every run drew its random sample
from the latest seven days (the one-time run's time range), not only the last hour. The next hourly run sampled the English
planned request (5/5 passed) but not the Korean one (5/5 from earlier conversations). That is a sampling outcome to record,
not a reason to send the request again.

Select **Pause** after the test and read back the paused state: the SDK listed both schedules with `enabled: false`.
Keep the schedule/run IDs and result artifacts. Pausing does not erase model, Search or logging charges already incurred.

**Monitoring done:** add those records to [Lab 11](../11-capstone.md).
Do not create an OIDC identity unless you separately chose the CI lane.

## 4. Prepare a narrowly scoped GitHub OIDC identity

This step requires an owner and separate approval.
The identity must trust only the intended repository and branch or protected GitHub environment.
Grant only the required training-project deployment/model/tool permissions.
Do not create client secrets or grant subscription-wide Owner.
For this workflow, the deployment identity uses project-scoped **Foundry Project Manager**
and read-only account metadata access. It can then grant only project-scoped **Foundry User**
to the actual deployed runtime identity. The helper verifies the returned agent/version/principal
instead of accepting an arbitrary principal ID from a dispatch input.

Store non-secret project/tenant/subscription/client identifiers as repository or environment variables.
Do not print tokens or entire `.env` files in workflow logs.

**Use the actual subject, not a remembered name-only template.** Read the repository's current OIDC configuration:

```bash
printf 'Approved GitHub repository (owner/name): '
read -r GITHUB_REPO
gh api "repos/$GITHUB_REPO/actions/oidc/customization/sub"
```

For immutable subjects, the returned `sub_claim_prefix` includes owner and repository IDs:
`repo:<owner>@<owner-id>/<repository>@<repository-id>`.
The protected environment adds `:environment:foundry-workshop`.
Match the exact `subject`, issuer and audience emitted by `azure/login`; never print the raw token.
Do not disable immutable claims, add wildcard trust, switch to a client secret, or broaden Azure roles to fix a mismatch.

The September 17 CI check initially returned `AADSTS700213` for a legacy name-only subject.
Only the existing federation's subject was corrected to the actual immutable repository/environment claim;
the identity, issuer, audience, Azure roles and GitHub security settings were unchanged.
See the [GitHub OIDC reference](https://docs.github.com/en/actions/reference/security/oidc) and
[exact federated credential update contract](https://learn.microsoft.com/graph/api/federatedidentitycredential-update).

The official [Hosted CI/CD quickstart](https://learn.microsoft.com/azure/foundry/agents/quickstarts/set-up-cicd-hosted-agent)
is the deployment/authentication reference. Adapt it to this repository's actual package/profile and version-pinned smoke contract;
nonempty stdout alone is not proof that an agent returned a valid result.

## 5. Define the release sequence

This repository includes the manually dispatched
[hosted-lab-release workflow](../../../.github/workflows/hosted-lab-release.yml).
It targets one existing project, creates no model deployments, pins the returned agent version,
and uses a six-case dev matrix as both the first-request smoke contract and the regression gate.
It does not open holdout or grant human production approval.
This first CI gate checks the complete six-row business contract. Native judging, calibration,
continuous evaluation and human production acceptance remain separately declared checks.

The workflow builds a hash-verified, profile-pinned azd project under the runner's temporary directory.
It does not reuse this repository's historical `azure.yaml` or append a CI service to an older project.
The shared `prepare_hosted_azd.py --kind workflow` helper binds only the selected existing project,
the single primary model and the invocations protocol; it initializes local environment values without provisioning.

Configure the `foundry-workshop` GitHub environment with the approved `AZURE_CLIENT_ID`,
`AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`, `AZURE_RESOURCE_GROUP`, `AZURE_AI_ACCOUNT_NAME`,
`AZURE_AI_PROJECT_ENDPOINT`, the **actual** `AZURE_AI_PROJECT_ID`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`,
`WORKSHOP_PREFIX`, and `WORKSHOP_HOSTED_AGENT_NAME`.
The agent name must begin with that prefix. Set branch/environment protections appropriate to the training scope.
No client secret belongs in these variables.

| Gate | Required evidence |
|---|---|
| Local checks | Offline/SDK tests, lint, compilation and documentation contracts |
| Package | Exact source/profile manifest; no secrets or evaluator answer files in the runtime |
| Deployment authorization | Manual dispatch or protected environment approval for the intended training target |
| Deploy | Actual version/endpoint and successful state, not just a log line |
| Smoke | A valid response from that exact version with real model/tool/evidence metadata |
| Quality | Complete chosen evaluation cohort and predeclared business/native requirements |
| Human decision | Explicit acceptance or pending review; no automated claim of production approval |
| Cleanup/rollback | Recorded owned sessions/rules and the previous known version |

Run the deployment workflow manually for the first exercise.
Select the dataset language and explicitly acknowledge the deployment/inference cost in its dispatch form.
The workflow fails rather than returning a skipped success when that acknowledgement is absent.
Do not add a scheduled trigger or a deploy-on-every-push rule just to demonstrate automation.
If the workflow has not been published/executed, mark **pipeline configuration only**, not CI/CD verified.

**September 23, 2026 with `gpt-6-sol`:** the owner pointed the `foundry-workshop` variables at the `gpt-6-sol` project
(prefix `mfv2-sol-20260923-ci`) and gave the existing CI identity project-scoped **Foundry Project Manager** and account **Reader**;
its federated credential was unchanged. The manually dispatched
[English](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35856612314) and
[Korean](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35857252318) releases passed on the first attempt:
Hosted agent `mfv2-sol-20260923-ci-hosted` versions 1 and 2, **Foundry User** granted once to its runtime identity (reused by version 2),
the six-case dev gate 6/6 with 0 errors on `gpt-6-sol-2026-09-22` in each language, and the created session confirmed idle.
Neither run executed native judging or holdout.

## 6. Roll back deliberately

Identify the exact previous agent/model/configuration versions before making a change.
If the smoke or quality gate fails, stop rollout and keep the failed version's artifacts.
Restoring a previous version is an explicit authorized operation; it is not another model chosen inside an exception handler.

**Next:** [Model operations](model-operations.md) or [Lab 11 handoff](../11-capstone.md).
[Monitoring and recurring-evaluation lifecycle](https://learn.microsoft.com/azure/foundry/observability/how-to/how-to-monitor-agents-dashboard).
