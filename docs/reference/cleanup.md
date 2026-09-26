# Cleanup, ownership, and retained evidence

**English** | [한국어](../ko/reference/cleanup.md)

**Stop only your own resources and verify their state. Never delete a shared project/resource group to finish a lab.**

**A needs no terminal here.** Use your existing `operations-checklist.txt` and the ownership checks below.
**B reuses Lab 09's inventory.** Expand a command section only for an asset you actually used.
An owner-managed or pending authorized cleanup must name its owner and remaining cost; it is not a claim that deletion occurred.

<a id="self-study-cleanup"></a>

**Learning alone in your own resource group?** After Lab 11, or if setup stopped before Lab 00, keep your evidence and follow these checks.
If the learner worksheets are not prepared yet, record these findings in your personal `setup-attempts.txt`;
transfer them to item 4 of `operations-checklist.txt` when your notes are ready. An unfinished setup can still leave resources behind.
If you will continue with B, retain the required resources and record their owner and ongoing costs instead of deleting them.

1. In the Azure portal, check each recorded group: the current course group and every group from earlier attempts in `setup-attempts.txt`.
   Check their contents separately; the working project's group is not the whole inventory.
   If tracing was configured, also check the actual resource groups
   of the connected **Application Insights** and **Log Analytics workspace**. Record those names and groups in item 4 of
   `operations-checklist.txt`. Logging resources can be in **other resource groups**; a connection does not place them inside the course group.
   If tracing was not configured, record **not run**; do not create logging resources for cleanup.
2. For each recorded group from [self-study step 2](../setup-owner.md#self-study), delete it only if it contains only this course's resources
   and you own the cleanup: **Resource groups → your group → Delete resource group**.
   Plan this deletion around **only resources in that group**, not every connected service. Never delete a shared group this way.
3. Refresh the resource list and record each group's actual outcome. Check the recorded logging resources separately
   and retain shared ones. For anything remaining or unverified, record its state, authorized owner and residual cost;
   a disappeared course group alone does not establish that all costs stopped.

**Managed workspace exception:** Application Insights can create its own Log Analytics workspace in a separate managed group.
Deleting Application Insights initiates that group's cleanup, but a lock, policy or other dependency can leave it behind.
Verify the outcome; do not delete a managed workspace directly or remove protection to force cleanup.
The authorized owner follows [managed-workspace cleanup](https://learn.microsoft.com/azure/azure-monitor/app/managed-workspaces#remove-managed-workspaces)
for a remaining group. This distinction was checked against Microsoft Learn on September 26, 2026, not by deleting workshop resources.

## 1. Inventory before changing anything

<details>
<summary>Optional local inventory command — B only if you need to print it again</summary>

```bash
python scripts/workshop.py --language en cleanup-plan
```

This prints an inventory/guide, not a deletion command.

</details>

Record the subscription, project, prefix, agent/version/session IDs, model deployments, Search objects, and logging/storage ownership.
`outputs/azure-objects.json` records only the Search index/source/base objects this copy created; it is not a full Azure inventory or proof of deletion rights.
In `cleanup-plan`, `search_ownership.objects` comes from that file, not an Azure query; `search_ownership: null` means the file is missing.
Neither `null` nor an empty list proves there are no resources or costs. If you created objects, recover the matching ledger with the owner,
not a fabricated replacement. Complete `required_manual_inventory` from your own records and the owner's checks even when the ledger is missing.
Unknown ownership is a reason to stop, not to widen the deletion scope.

<a id="hosted-sessions"></a>

## 2. Hosted compute and persistent state

<details>
<summary>Only if you ran a local server or attempted/used a remote Hosted deployment</summary>

If you ran `serve`, stop only that server with `Ctrl+C` in its terminal.
**Local-only:** if no remote Hosted deployment was attempted or used, record the server as stopped and remote Hosted sessions as **not run**, then skip the azd blocks below. Local model-call charges already incurred remain.
Continue below only for a remote deployment you attempted or used; a failed deployment is not proof that no resources remain. Never deploy merely to complete cleanup.
From the repository terminal, restore the **standalone azd directory and service name** from your notes.
Do not run these commands against an unrelated `azure.yaml`.

```bash
printf 'Standalone Hosted directory used for this agent: '
read -r HOSTED_DIRECTORY
printf 'Owned Hosted agent service name: '
read -r HOSTED_AGENT_NAME
azd ai agent sessions list --cwd "${HOSTED_DIRECTORY:?Use the recorded standalone directory}" --agent-name "${HOSTED_AGENT_NAME:?Use the owned service name}" --limit 10
```

Follow any continuation token with `--pagination-token` on that same scoped list command.
If your session is already idle/stopped, record that state without another stop request.
For your own **active** session only:

```bash
printf 'Owned active session ID from the list: '
read -r OWNED_SESSION_ID
azd ai agent sessions stop "${OWNED_SESSION_ID:?Use the owned active session ID}" --cwd "${HOSTED_DIRECTORY:?Use the recorded standalone directory}" --agent-name "${HOSTED_AGENT_NAME:?Use the owned service name}" &&
azd ai agent sessions list --cwd "${HOSTED_DIRECTORY:?Use the recorded standalone directory}" --agent-name "${HOSTED_AGENT_NAME:?Use the owned service name}" --limit 10
```

Use stop when persistent files must remain. Deleting a session removes compute and persistent filesystem state.
Inspect the selected agent/session and stop only IDs you created.
An already-idle session is verified as idle without submitting another conflicting stop request.
Never treat an unverified stop request as a confirmed stopped state.

</details>

## 3. Clean up only objects you created

| Asset | Check and cleanup |
|---|---|
| Prompt/Hosted agent and version | Confirm the exact project, name, version and owner, including the Lab 03 B SDK managed agent now core in B; the owner deletes it. In the 2026-09-25 check, deleting a prompt agent also removed its Entra agent identity and blueprint |
| Search knowledge base/source/index | Dependency order base → source → index; only your names in the ledger |
| Uploaded files/vector stores | Separate your File Search material from shared material |
| Evaluation datasets, evaluations and custom evaluators | Your `<prefix>-dev-questions` dataset, `<prefix>-...` evaluations, the `eval-data-<UTC time>` dataset the service creates with each evaluation run (`cloud-evaluate`, `maf-evaluate`, `conversations evaluate`; its time is within seconds of the evaluation's creation; other people's runs create the same kind), and `<prefix>_business_rubric` versions (hyphens become underscores); keep results first, then the owner deletes them |
| Model deployments | Check whether it is team-only or shared; keep shared models |
| Search service | Deleting an index does not remove the service's fixed cost |
| Application Insights/Log Analytics | Inventory both resources and their actual groups. Check shared versus managed workspace ownership and verify each cleanup outcome; retention and cost remain owner-managed, including the Lab 09 trace requirement |
| Resource group | Only its owner deletes it, and only if it is training-only and every asset is checked |

<details>
<summary>Only if you ran recurring evaluation, Agent Optimizer, red teaming, CI or Fabric/Work IQ modules</summary>

| Asset | Check and cleanup |
|---|---|
| Recurring evaluation schedules | Your `<agent>-scheduled-...` schedule: select **Pause** on its evaluation page and read back the paused state; pausing keeps earlier results |
| Optimizer datasets and runs | Your `<prefix>-optimizer-dev` dataset and optimization runs; keep results first, then the owner deletes them |
| Red-team taxonomies and red teams | Your `<prefix>-...redteam` taxonomies, red teams and runs; keep every output item and the review record before the owner deletes them |
| Roles added for monitoring or CI | Only the owner removes roles they added, for example **Monitoring Reader** for the project identity on Application Insights, the CI identity's project roles and a Hosted runtime's **Foundry User** |
| Temporary optimizer deployment | Only the owner who created it deletes it, after every optimizer run that used it has finished and been reviewed; confirm the answer and judge deployments remain |
| Fabric/Work IQ | Check dedicated capacity, billing and connections separately; never revoke organizational consent |

</details>

The optional `iq-chat setup` adds a **separate chat base** to that ledger with API `2026-08-01-preview`.
After deletion approval, remove every owned base that references a source **before** its source/index.
If retaining the GA base, retain its shared source/index too; deleting only the chat base must not break the GA evaluation.
Do not revoke the Search identity's shared model role merely because this one chat base is removed.
Do not use `azd down`, subscription changes, or resource-group deletion as a shortcut in a shared environment: with an existing project
`azd down` can leave lab assets behind, and with an azd-created project it can delete the whole resource group
([official guidance](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)).

## 4. Final check

- [ ] Only the local servers you ran are stopped; unused ones are recorded as **not run**.
- [ ] Each Hosted session you used has a recorded final state or a pending authorized owner.
- [ ] Your agents, files and Search objects have a verified outcome: read each deleted object back, because a delete response alone is not proof.
- [ ] Shared resources and other people's data are kept.
- [ ] The owner has confirmed residual costs for services, models, logs, storage and capacity.
- [ ] Results to keep are separated from sensitive data to remove.
- [ ] Evaluation lineage is kept: questions, reference answers, prompts, corpus, model/agent versions, evaluator definitions,
  all responses/errors, trace-query receipts and review records. Failed rows are never deleted to improve a score,
  and holdout stays final-acceptance material, not a regression source.

Cost views can lag; record when you last checked and who owns the remaining cost. Budget alerts do not stop resources.

<a id="learner-finish"></a>

**Learner cleanup handoff is ready when** `operations-checklist.txt` identifies each used asset,
its verified state or pending authorized owner, preserved evidence and residual costs.
Mark unused local/Hosted services **not run**, not “deleted.”

**End of this session:** if you came from Lab 11 and the handoff is done, stop here.
Keep the learning outcome in `session-notes.txt`: missing required stages remain **incomplete** and a failed B final gate remains **rejected**.
Finishing cleanup does not complete an unrun exercise or turn a rejected result into acceptance.
If resuming later, use the recorded unfinished step and resolve its blocker first; do not rerun exposed holdout to improve a score.
If the handoff is not done yet, return to [Lab 11](../labs/11-capstone.md).
The maintainer media work below is not part of learner completion.

## Hosted matrix sessions

<details>
<summary>Only for existing matrix runs — not A or introductory B</summary>

Only run this block if these actual matrix labels exist; A and introductory B skip it.

The matrix manifest records the created session and exact agent version.
After actual trace verification:

```bash
python scripts/workshop.py --language en benchmark stop-session --label wf-baseline
python scripts/workshop.py --language en benchmark stop-session --label wf-candidate
python scripts/workshop.py --language en benchmark stop-session --label wf-final
```

Cleanup receipts are separate from immutable manifests, so candidate and regression hashes remain valid.
Inspect separately created smoke sessions using their own raw HTTP/azd records.

</details>

## 5. Local outputs and final media

<details>
<summary>Maintainers only, after a separately authorized media replacement — learners preserve the repository's data and videos</summary>

Verify both new language sets before replacing older screenshots/videos.
Use each `docs/assets/g6sol-20260924-ko/` and `g6sol-20260924-en/` media manifest,
actual byte hashes, frame checks, playback, and document links.
Do not delete one language's old assets while only the other replacement is ready.

| Location | Retain |
|---|---|
| Current language asset directories | New videos, lossless captures, action/timestamp/frame lineage |
| `outputs/benchmarks/<label>/` | Complete matrix, raw failures, dataset/corpus/response/native/trace/cleanup evidence |
| `outputs/judge-calibration/` | Calibration kept separate from target responses |
| `outputs/regressions/` | Reviewed original dev references and source lineage |
| `outputs/azure-objects.json` | Ownership of Azure objects |
| `outputs/iq-chat/<label>/` | Model/KB preflight, request, actual response/source evidence and failures; not benchmark scores |
| `data/learner/<language>/` | Committed starter materials; keep learner-filled worksheets elsewhere |
| `outputs/policy-documents/` | Optional export of the same six synthetic files already in the learner ZIP |
| `.build/<profile>/` | Needed deployment source/profile manifests after checking active references |

After both language sets and final checks pass, remove obsolete media, duplicate temporary encodes, and files unrelated to the final workshop.
Keep executable code, tests, synthetic inputs, necessary configuration, licenses, and evaluation/failure lineage.
Production tooling environments and private authentication/capture helpers do not belong in the learner repository.

This cleanup concerns current files and guide references, not rewriting Git history or claiming unverified permanent deletion from external attachment storage.
Never recursively delete a repository root, home directory, or whole session folder.

</details>
