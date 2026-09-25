# Environment owner preparation

**English** | [한국어](ko/setup-owner.md)

**Prepare the Azure environment before learners start setup.** This page is for the subscription/project owner or instructor, not a hidden prerequisite inside a later lab.

**Learning alone?** You are also the owner. Follow [Learning alone](#self-study) first; the [class owner checklist](#class-owner-checklist) after it adds class, B Search and optional preparation.

<a id="self-study"></a>

## Learning alone: prepare route A yourself

**Finish with what a class owner would hand you: your own project, the exact `gpt-6-sol` deployment, your role, the setup card and a Lab 05 terminal.**
Do this once, before Lab 00. It creates billable resources in your subscription; this edition has not timed it with learners.
The portal steps follow the linked Microsoft Learn pages, checked on September 25, 2026. The workshop recordings used a project prepared beforehand.

1. **Subscription.** Sign in at `https://ai.azure.com` with an account that can create resources and assign roles in your Azure subscription, for example its **Owner**. Model calls are billed to that subscription.
   **Check:** the Foundry portal opens and **New Foundry** at the top is switched on.
2. **Project.** Select the project name at the top left, then **Create new project** (if you have no project yet, the portal offers to create one).
   Enter a name that starts with `mfv2-`, open **Advanced options**, create a **new resource group** used only for this course,
   choose a **Location** that offers `gpt-6-sol` (this edition used **Sweden Central**) and select **Create**
   ([official steps](https://learn.microsoft.com/azure/foundry/how-to/create-projects)).
   **Check:** your new project's **Home** shows **Project endpoint**; its `<account>` part, `https://<account>.services.ai.azure.com/...`, is your Foundry resource name.
3. **Answer model.** Select **Discover** in the top bar, then **Models**, search for and open **`gpt-6-sol`**, and select **Deploy → Custom settings**.
   Keep the deployment name **`gpt-6-sol`**, choose model version **`2026-09-22`** and select **Deploy**
   ([official steps](https://learn.microsoft.com/azure/foundry/foundry-models/how-to/deploy-foundry-models)).
   Skip `gpt-6-sol-judge` unless you later choose an optional Foundry evaluation.
   **Check:** **Home → View deployments** shows `gpt-6-sol`, version `2026-09-22` and **Succeeded**.
   If that model or version is not offered, or has no quota, in your location, stop: repeat step 2 in another location
   with a new resource group, or [request quota](https://aka.ms/oai/stuquotarequest). Do not deploy another model instead.
4. **Your role.** Creating the project in the portal with role-assignment rights also gives you, and the project's managed identity,
   **Foundry User** on the new Foundry resource ([official RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#minimum-role-assignments-to-get-started)).
   **Check:** in the Azure portal, open the new Foundry resource → **Access control (IAM)** → **Role assignments** and find **Foundry User**
   (older name **Azure AI User**) for your account. If it is missing, [assign it](https://learn.microsoft.com/azure/role-based-access-control/role-assignments-portal) to your account on that resource.
5. **Traces, optional.** For Lab 09's trace check, select **Build → Agents**, the **Traces** tab and **Connect**, then create a new
   Application Insights resource ([official steps](https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup)). It adds log costs.
   **Check:** a connection confirmation appears. If you skip this step, Lab 09 records `trace unverified: <reason>`.
6. **Files and values.** Complete [setup sections 2–3](setup.md#learner-files): download the learner ZIP and fill its setup card from your own portal.
   On `Cost and permission owner:` write yourself.
   **Check:** every line of the **Lab 00 - setup card** section in `session-notes.txt` is filled.
7. **Lab 05 terminal.** Complete [Lab 00 B](labs/00-start.md#path-b) steps 1–5, then [Lab 02 B](labs/02-models.md#path-b) steps 1–3,
   and leave through [its A return choices](labs/02-models.md#a-terminal-ready). You can also do this step when you reach Lab 05.
   **Check:** `doctor --cloud` reports `gpt-6-sol` / `2026-09-22` / `Succeeded`, and Lab 02 B saved `model.json` and `answer-local.json`.

**Ready:** after step 6, or step 7 if you do it now, start [Lab 00 A](labs/00-start.md#path-a).
If a step fails, fix that step before continuing. Do not create another model, resource or project for the same unexplained error.
**Learning B alone?** Complete steps 1–5 (B's Lab 09 needs step 5), then step 4 of the [class owner checklist](#class-owner-checklist)
for the Search service and your two Search roles, and continue with [setup](setup.md) for route B.
**After Lab 11:** keep your evidence folder, then delete the step 2 resource group in the Azure portal (**Resource groups** → your group →
**Delete resource group**) only if it holds nothing but this course's resources. That removes the project, its deployments and any
Application Insights together; [cleanup](reference/cleanup.md) shows how to confirm and record it. Keep the group instead if you will continue with route B.

<a id="class-owner-checklist"></a>

## Class owner checklist

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
   The same setup, followed by [Lab 02 B](labs/02-models.md#path-b), is the self-service route if neither Lab 05 option is prepared.
7. Connect Application Insights to the project before class for server-side tracing. No code change is needed.
   Give learners **Log Analytics Reader** on the connected Application Insights resource; if protected tables are enabled, also give **Privileged Monitoring Data Reader**.
   This is required for the now-core Lab 09 trace step. Checked 2026-09-24: the training project already had Application Insights connected
   and managed agent calls appeared as traces within minutes; a learner-only Log Analytics Reader grant was not re-tested.
8. Optional: deploy the Lab 05 MAF workflow as a Hosted Agent so A learners can use the browser Playground option in Lab 05.
   Use [Lab 05 C](labs/05-workflows.md) / [Lab 08 section 6](labs/08-hosted.md#6-deploy-a-maf-workflow-as-a-hosted-agent) only after separate approval.
   Prepare the **sequential, local-retrieval, v2, Responses** workflow profile in the learner's language; an Invocations evaluation
   agent or the Lab 03 Prompt Agent is not this option. Verify an actual Playground reply with a participant account before offering it.
   Record the hosted workflow agent name and active version for learners. On 2026-09-24 the workflow agent answered one local Responses request;
   no remote deployment was made for that check.
9. Optional: prepare the owner/instructor machine with the [Foundry Dev Pack](labs/extensions/developer-toolkit.md), then pin and record `az`, `azd`, the Foundry azd extension, SDK, and extension versions afterward.
   Not tested in this edition.
10. Optional lightweight source distribution: provide a sparse checkout that omits `docs/assets/` and video files for learners who need the source without large media history.
    The full repository remains the source of truth. The sparse pattern in [Lab 00](labs/00-start.md#source-folder) was checked locally on 2026-09-24:
    `docs/assets/` and `videos/` were excluded while scripts and guides remained.

For an IQ Chat learner, **Reader on Search** allows inspection of service/object definitions,
and **Search Index Data Reader** allows retrieval; these are separate from the model-account Reader above.
The read-only `check` also reads role assignments at the model-account scope.
Assign Search roles for the action the learner will perform, not only for an instructor's successful request:

| Learner action | Search roles | Scope |
|---|---|---|
| B participant or owner running `seed-search` | **Search Service Contributor** and **Search Index Data Contributor** | Prepared training Search service |
| Read-only `retrieve` or prepared IQ Chat use | **Search Index Data Reader**; also **Reader** when inspecting service/object definitions | Prepared training Search service |

Fresh B learners are object writers in Lab 06. They need the first row even when the owner already created the shared service.
The owner authorizes role assignments; running the seeding exercise does not require subscription Owner.
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
