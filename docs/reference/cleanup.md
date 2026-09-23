# Cleanup, ownership, and retained evidence

**English** | [한국어](../ko/reference/cleanup.md)

**Stop only your own resources and verify their state. Never delete a shared project/resource group to finish a lab.**

**A needs no terminal here.** Use your existing `operations-checklist.txt` and the ownership checks below.
**B reuses Lab 09's inventory.** Expand a command section only for an asset you actually used.
An owner-managed or pending authorized cleanup must name its owner and remaining cost; it is not a claim that deletion occurred.

## 1. Inventory before changing anything

<details>
<summary>Optional local inventory command — B only if you need to print it again</summary>

```bash
python scripts/workshop.py --language en cleanup-plan
```

</details>

This prints an inventory/guide, not a deletion command.
Record the subscription, project, prefix, agent/version/session IDs, model deployments, Search objects, and logging/storage ownership.
Unknown ownership is a reason to stop, not to widen the deletion scope.

<a id="hosted-sessions"></a>

## 2. Hosted compute and persistent state

<details>
<summary>Only if you ran a local server or Hosted agent — otherwise skip</summary>

Skip this section if you did not run a local server or Hosted agent. Otherwise stop your own `serve` with `Ctrl+C` in its terminal.
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

## 3. Search, models, and other Azure resources

`outputs/azure-objects.json` is ownership evidence for index/source/base operations.
It is not permission to delete an entire Search service.
The optional `iq-chat setup` adds a **separate chat base** to that ledger with API `2026-08-01-preview`.
After deletion approval, remove every owned base that references a source **before** its source/index.
If retaining the GA base, retain its shared source/index too; deleting only the chat base must not break the GA evaluation.
Do not revoke the Search identity's shared model role merely because this one chat base is removed.
Models, Search capacity, evaluation, telemetry retention, and persistent storage have separate costs.
Stopping a Hosted session does not stop every one of them.
Do not use `azd down`, subscription changes, or resource-group deletion as a shortcut in a shared environment.

Optional Fabric/Work IQ connections require their own approved restoration plan.
Do not revoke organizational consent or remove another team's capacity.

## 4. Preserve evaluation lineage

Keep original questions, reference answers, prompts, corpus, model/agent versions, evaluator definitions,
all responses/errors, trace-query receipts, and review records.
Do not delete failed rows to improve a score.
Holdout remains final-acceptance material, not a regression source.

**Learner cleanup handoff is ready when** `operations-checklist.txt` identifies each used asset,
its verified state or pending authorized owner, preserved evidence and residual costs.
Mark unused local/Hosted services **not run**, not “deleted.”
Return to [Lab 11](../labs/11-capstone.md); maintainer media work below is not part of learner completion.

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
Use each `docs/assets/g6sol-20260923-ko/` and `g6sol-20260923-en/` media manifest,
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
