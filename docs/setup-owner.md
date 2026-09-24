# Environment owner preparation

**English** | [한국어](ko/setup-owner.md)

**Prepare the shared Azure environment before learners start setup.** This page is for the subscription/project owner or instructor, not a hidden learner step.

If you are learning alone, you are also the environment owner. These are preparation steps, not hidden prerequisites inside a later lab.

1. Select a dedicated training subscription/resource group and a region with the required model quota.
   Use the [current Foundry setup guide](https://learn.microsoft.com/azure/foundry/quickstarts/get-started-code);
   do not choose a classic Hub/threads-runs tutorial.
2. Prepare **`gpt-6-sol` / `2026-09-22`** with deployment name **`gpt-6-sol`**.
   Verify its state is `Succeeded`. Do not create another model after an unexplained error.
3. Give the learner the appropriate Foundry project/model permissions.
   The CLI's deployment preflight also needs **Reader on the training Foundry account**. Test with that learner's account, not only an administrator.
4. For B's GA Search/IQ or optional IQ Chat, prepare Basic-or-higher Search, semantic/knowledge retrieval access,
   and Search read/write permissions for the person who seeds the synthetic index.
   For B learners starting from a fresh copy, prepare the **service and permissions**, not objects under their new prefixes.
   If supplying pre-seeded objects, supply the authorized matching working copy; endpoint/base names alone do not supply its local ownership ledger.
5. **Only for optional model-based IQ Chat**, enable Search's system-assigned identity and prepare a separate
   **`gpt-5.6-luna` / `2026-07-09`** deployment named **`gpt-5.6-luna`**; Search knowledge bases accepted no GPT-6 model on September 23, 2026.
   On the model's Foundry account, give **the Search identity** `Cognitive Services User`.
   A role assigned to the user or Hosted agent does not grant it to Search.
6. Complete [Lab 00 B setup](labs/00-start.md#b-code-one-folder-one-environment), including `.env`, before running the owner commands below.
   The same setup, followed by [Lab 02 B](labs/02-models.md#path-b), is the self-service route if no prepared terminal is available for Lab 05.
7. Connect Application Insights to the project before class for server-side tracing. No code change is needed.
   Give learners **Log Analytics Reader** on the connected Application Insights resource; if protected tables are enabled, also give **Privileged Monitoring Data Reader**.
   This is required for the now-core Lab 09 trace step. **Not run in this edition yet (added 2026-09-24).**
8. Optional: deploy the Lab 05 MAF workflow as a Hosted Agent so A learners can use the browser Playground option in Lab 05.
   Use [Lab 05 C](labs/05-workflows.md) / [Lab 08 section 6](labs/08-hosted.md) hosted-workflow path only after separate approval.
   Record the hosted workflow agent name and active version for learners. **Not run in this edition yet (added 2026-09-24).**
9. Optional: prepare the owner/instructor machine with the [Foundry Dev Pack](labs/extensions/developer-toolkit.md), then pin and record `az`, `azd`, the Foundry azd extension, SDK, and extension versions afterward.
   **Not run in this edition yet (added 2026-09-24).**
10. Optional lightweight source distribution: provide a sparse checkout that omits `docs/assets/` and video files for learners who need the source without large media history.
    The full repository remains the source of truth. **Not run in this edition yet (added 2026-09-24).**

For an IQ Chat learner, **Reader on Search** allows inspection of service/object definitions,
and **Search Index Data Reader** allows retrieval; these are separate from the model-account Reader above.
The read-only `check` also reads role assignments at the model-account scope.
Only the owner who seeds/creates objects needs Search Service Contributor and Search Index Data Contributor.
Use resource-level scopes, not subscription Owner for everyone. [Official Search role matrix](https://learn.microsoft.com/azure/search/search-security-rbac#summary-of-permissions), checked September 15, 2026.

**Only for the separately selected IQ Chat branch, after authorization for these training objects**, prepare the fixed-model chat base.
Do not run this block for a default B GA-only class. Keep the owner's copy/ledger; do not give another fresh learner copy the same seeded prefix.

```bash
python scripts/workshop.py --language en seed-search --iq --confirm-create
python scripts/workshop.py --language en iq-chat check
python scripts/workshop.py --language en iq-chat setup --confirm-create
python scripts/workshop.py --language en iq-chat ask --label iq-chat-first --confirm-cost
```

`check` is read-only and rejects a wrong model version, missing Search identity/role, or wrong source.
`setup` creates only the new owned chat base; it does not deploy a model, grant roles, or rewrite the GA evaluation base.
`ask` is billable and records actual planning, synthesis and original evidence under `outputs/iq-chat/iq-chat-first/`.
Use a **new label** for each new request; do not overwrite the first result.

As checked on **September 15, 2026**, the optional Preview preset fixes `gpt-5.6-luna`, Search system-assigned identity,
`2026-08-01-preview`, `low`, and `answerSynthesis`. Preview planning/synthesis is not required for A's source checks or B's GA retrieval.
It uses the verified `maxOutputSize` request field rather than the field rejected in the earlier diagnostic.
Return the printed chat-base name to the learner. They should open **that base**, not the model-free `<prefix>-kb`.

Return to [the learner ready check](setup.md#5-ready-to-start) after preparation; do not run optional owner commands for the default A route.
