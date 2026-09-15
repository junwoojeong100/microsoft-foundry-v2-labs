# Cleanup, ownership, and retained evidence

**English** | [한국어](../ko/reference/cleanup.md)

**Stop only your own resources and verify their state. Never delete a shared project/resource group to finish a lab.**

## 1. Inventory before changing anything

```bash
python scripts/workshop.py --language en cleanup-plan
```

This prints an inventory/guide, not a deletion command.
Record the subscription, project, prefix, agent/version/session IDs, model deployments, Search objects, and logging/storage ownership.
Unknown ownership is a reason to stop, not to widen the deletion scope.

## 2. Hosted compute and persistent state

Use stop when persistent files must remain. Deleting a session removes compute and persistent filesystem state.
Inspect the selected agent/session and stop only IDs you created.
An already-idle session is verified as idle without submitting another conflicting stop request.
Never treat an unverified stop request as a confirmed stopped state.

## 3. Search, models, and other Azure resources

`outputs/azure-objects.json` is ownership evidence for index/source/base operations.
It is not permission to delete an entire Search service.
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

## Hosted matrix sessions

The matrix manifest records the created session and exact agent version.
After actual trace verification:

```bash
python scripts/workshop.py --language en benchmark stop-session --label wf-baseline
python scripts/workshop.py --language en benchmark stop-session --label wf-candidate
python scripts/workshop.py --language en benchmark stop-session --label wf-final
```

Cleanup receipts are separate from immutable manifests, so candidate and regression hashes remain valid.
Inspect separately created smoke sessions using their own raw HTTP/azd records.

## 5. Local outputs and final media

Verify both new language sets before replacing older screenshots/videos.
Use each `docs/assets/refresh-20260915-ko/` and `refresh-20260915-en/` media manifest,
actual byte hashes, frame checks, playback, and document links.
Do not delete one language's old assets while only the other replacement is ready.

| Location | Retain |
|---|---|
| Current language asset directories | New videos, lossless captures, action/timestamp/frame lineage |
| `outputs/benchmarks/<label>/` | Complete matrix, raw failures, dataset/corpus/response/native/trace/cleanup evidence |
| `outputs/judge-calibration/` | Calibration kept separate from target responses |
| `outputs/regressions/` | Reviewed original dev references and source lineage |
| `outputs/azure-objects.json` | Ownership of Azure objects |
| `outputs/policy-documents/` | The six synthetic files used by the browser path |
| `.build/<profile>/` | Needed deployment source/profile manifests after checking active references |

After both language sets and final checks pass, remove obsolete media, duplicate temporary encodes, and files unrelated to the final workshop.
Keep executable code, tests, synthetic inputs, necessary configuration, licenses, and evaluation/failure lineage.
Production tooling environments and private authentication/capture helpers do not belong in the learner repository.

This cleanup concerns current files and guide references, not rewriting Git history or claiming unverified permanent deletion from external attachment storage.
Never recursively delete a repository root, home directory, or whole session folder.
