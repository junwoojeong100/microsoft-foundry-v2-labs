# Cleanup: preserve shared assets

**English** | [한국어](../ko/reference/cleanup.md)

**Identify the owner and exact asset before deleting anything.**
This repository does not automatically delete Azure resources or roles.

## 1. Check evidence and ownership

```bash
python scripts/workshop.py cleanup-plan
```

`outputs/azure-objects.json` records Search index/source/base objects created by this
copy. It is neither a full Azure inventory nor proof of deletion authority.
Decide which personal results to retain; never publish secrets/environment identifiers.

## 2. Local processes and Hosted sessions

Stop **only your server** with `Ctrl+C` in the terminal running `serve`.
From the azd project folder, inspect owned Hosted sessions:

```bash
azd ai agent sessions list --limit 10
```

Follow continuation tokens through all pages. With multiple services, explicitly use
the actual service name via `--agent-name`. Verify the session and agent before:

```bash
azd ai agent sessions stop "<my-session-id>"
```

Stop terminates compute but retains the persistent filesystem. Another invocation can
restart it; this is not deletion or guaranteed zero cost. Separately review the scope
and irreversibility of any user-data deletion. Do not stop other teams' sessions.

## 3. Clean up only owned objects

| Asset | Ownership-aware action |
|---|---|
| Prompt/Hosted agent/version | Owner verifies project, name, version, and scope before deletion |
| Search base/source/index | Dependency order: base → source → index; only owned ledger names |
| Uploaded files/vector stores | Separate your File Search data from shared data |
| Model deployments | Preserve shared models; verify whether a deployment is team-exclusive |
| Search service | Deleting an index does not end the service's fixed cost |
| App Insights/Log Analytics | Review evidence, retention, and shared ownership |
| Fabric/Work IQ | Separately review capacity, billing, connections; no arbitrary tenant consent deletion |
| Resource group | Owner deletes only if entirely training-exclusive and every asset has been reviewed |

Read the exact asset name, subscription, and warning in the portal.
No copy/paste "delete the whole resource group" command is provided.

## `azd down` is not equivalent in every environment

The official Hosted quickstart distinguishes a newly created project, where the
resource group and all its resources may be deleted, from an existing project, where
project/group/agent assets may remain.
Do not run `azd down` indiscriminately or infer zero cost from a success message.
Compare provider, creation plan, and existing-resource status with
[official guidance](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent).

## 4. Final checks

- [ ] My local server stopped.
- [ ] I reread session state and checked for remaining active owned sessions.
- [ ] I verified outcomes for my agents, files, and Search objects.
- [ ] Shared resources and other people's data remain.
- [ ] The owner checked residual service/model/log/storage/capacity costs.
- [ ] Evidence to retain and sensitive data to remove are distinguished.

Cost reporting can lag. Record the last check time and owner.
Budget alerts are not automatic shutdown controls.

## 5. Local outputs and generated directories

Keep the [new English-guide recording](../english-recordings.md) and the Korean source
recording as separate, manifest-verified editions. The default English catalog is
`docs/assets/english-20260915/media.json`; `--edition ko` selects the original set.
Do not delete one language's assets merely because the other has a newer recording date.

The source guide media is the **September 14 action-level recording** in
`docs/assets/live-20260914-action/media.json`. Compare manifest filenames/hashes
before cleanup; dates alone are insufficient.
Evaluation inputs, responses, evaluator definitions, and ownership records are separate
from media. Git exclusion does not make them disposable.

| Location | Retention rule |
|---|---|
| `docs/assets/english-20260915/` | Three new videos, 537 lossless images, 234 action records, run/frame/playback lineage |
| `outputs/english-20260915/` | Private raw runs, six source videos, capture ledgers, and hash manifest; not for Git publication |
| `docs/assets/live-20260914-action/` | Two edited videos, one guide-ordered video, 236-action captures, frame/hash lineage |
| `outputs/azure-objects.json` | Current Search ownership; not a disposable log |
| `outputs/live-20260914-action/` | Raw responses/evaluators/File Search/portal/cleanup evidence; private and Git-excluded |
| `outputs/<label>/` | Unique run manifest, responses, and evaluation lineage |
| `outputs/policy-documents/` | Synthetic text files distributed to beginners |
| `outputs/live-20260914-action/sources/` | Four unedited recording sources for private hash verification, not default playback |
| `.build/hosted/` | Source referenced by current `azure.yaml` and `.foundry` evaluation lineage; never delete wholesale |

Remove duplicate captures, wait-only frames, and temporary encodes only after final
hash/source correspondence checks. Verify every file hash if archiving evaluation
evidence, and inspect whether media is mixed in.
Keep production tools/venvs out of the learner repository; retain the player,
executable labs, synthetic inputs, and regression checks.

Read an existing private archive without extracting it:

```bash
tar -tzf outputs/live-20260914-action/evidence.tar.gz
```

The archive can contain private environment/run identifiers. Do not publish it.
`.git`, root `.venv`, current `.env`/`.azure`, workshop source, synthetic inputs, and
tests are not cleanup targets.
Cleaning current files is separate from deleting Git history or GitHub attachments;
do not claim unverified permanent deletion.
