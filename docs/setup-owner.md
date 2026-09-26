# Environment owner preparation

**English** | [한국어](ko/setup-owner.md)

**Prepare the Azure environment before learners start setup.** This page is for the subscription/project owner or instructor, not a hidden prerequisite inside a later lab.

**Preparing a class?** Start at the [class owner checklist](#class-owner-checklist), not the self-study steps.
**Environment already supplied?** Return to [learner setup](setup.md#learner-files); do not create another project.
**Learning alone without a prepared environment?** You are also the owner. Follow [Learning alone](#self-study), using its A or B directions.

<a id="self-study"></a>

## Learning alone: prepare route A yourself

**Finish with what a class owner would hand you: your own project, the exact `gpt-6-sol` deployment, your role, the setup card and a Lab 05 terminal.**
Do this once, before Lab 00. It creates billable resources in your subscription; this edition has not timed it with learners.
The portal steps follow the linked Microsoft Learn pages, checked on September 25, 2026. The workshop recordings used a project prepared beforehand.

**Learning B alone?** Complete steps 1–4; step 5 is optional. Lab 09 requires a trace-status record, not a new logging resource:
if you skip step 5, record `trace unverified: not configured` there. Then [prepare B's Search service](#search-service).
Skip A's steps 6–7; the Search section returns you to [setup](setup.md) for B.

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
   If that model or version is not offered, or has no quota, in your location, stop. In a personal local text file named
   `setup-attempts.txt`, record the subscription, resource group, location, Foundry account/project, exact error and time.
   Keep every attempt; do not record credentials. You can [request quota](https://aka.ms/oai/stuquotarequest) for the same location,
   or verify the required model/version, quota and costs elsewhere before repeating step 2 with a new course-only group.
   Creating that new group does **not** remove the earlier resources. Do not deploy another model instead.
   If you stop preparation here, follow [the cleanup check](reference/cleanup.md#self-study-cleanup) now; do not wait for Lab 11.
4. **Your role.** Creating the project in the portal with role-assignment rights also gives you, and the project's managed identity,
   **Foundry User** on the new Foundry resource ([official RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#minimum-role-assignments-to-get-started)).
   **Check:** in the Azure portal, open the new Foundry resource → **Access control (IAM)** → **Role assignments** and find **Foundry User**
   (older name **Azure AI User**) for your account. If it is missing, [assign it](https://learn.microsoft.com/azure/role-based-access-control/role-assignments-portal) to your account on that resource.
5. **Traces, optional.** For Lab 09's trace check, select **Build → Agents**, the **Traces** tab and **Connect**, then create a new
   Application Insights resource ([official steps](https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup)). It adds log costs.
   Check the resource groups of both Application Insights and its linked **Log Analytics workspace** in the Azure portal;
   they need not be the course group. Keep their names/groups for `operations-checklist.txt` when your route prepares its personal notes.
   **Check:** a connection confirmation appears. If you skip this step, Lab 09 records `trace unverified: <reason>`.
6. **Files and values.** Complete [setup sections 2–3](setup.md#learner-files): download the learner ZIP and fill its setup card from your own portal.
   On `Cost and permission owner:` write yourself.
   On `Prepared MAF terminal location:` write `pending step 7` until the terminal is ready; the learner ZIP is not a code environment.
   If you have `setup-attempts.txt`, keep it in this personal evidence folder and add every earlier group and its current state
   to item 4 of `operations-checklist.txt`, with its remaining cost and cleanup owner.
   If you configured tracing, add both logging resources and their actual groups to item 4 of `operations-checklist.txt`.
   **Check:** the portal values are recorded in **Lab 00 - setup card**; only the terminal location is still pending.
7. **Lab 05 terminal.** Complete [Lab 00 B](labs/00-start.md#path-b) steps 1–5, then [Lab 02 B](labs/02-models.md#path-b) steps 1–3,
   and leave through [its A return choices](labs/02-models.md#a-terminal-ready). Finish this preparation **before starting the timed A route**;
   do not continue into the rest of B.
   **Check:** `doctor --cloud` reports `gpt-6-sol` / `2026-09-22` / `Succeeded`, and Lab 02 B saved `model.json` and `answer-local.json`.
   Replace `pending step 7` on the learner ZIP's setup card with this source folder's full path. Keep that folder, `.venv`, `.env`
   and the saved responses for Lab 05; your A notes remain in the learner ZIP, not the B worksheet copy.

**Ready:** complete steps **1–7** (step 5 may be recorded as skipped), then tick [the setup ready check](setup.md#5-ready-to-start)
and start [Lab 00 A](labs/00-start.md#path-a). The setup card alone does not make the Lab 05 terminal ready.
If a step fails, fix that step before continuing. Do not create another model, resource or project for the same unexplained error.
**After Lab 11:** keep your evidence folder, then check every group created during preparation, including earlier attempts.
Delete each in the Azure portal (**Resource groups** → your group → **Delete resource group**) only if it holds nothing but this course's resources.
Do not assume connected logging resources are in that group
or were deleted with it. Follow [the self-study cleanup check](reference/cleanup.md#self-study-cleanup) for Application Insights,
Log Analytics and remaining costs. Keep the resources needed for route B instead if you will continue with it; record the owner and ongoing costs.

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
   and Search read/write permissions for the person who seeds the synthetic index. Use [the Search service steps](#search-service) if no service is ready.
   Complete [the Search authentication check](#search-authentication) as well as the role assignments below.
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
   These prerequisites are required to verify an actual trace. If tracing is unavailable, learners record `trace unverified: <reason>`
   in Lab 09 and continue; that record does not count as verified trace evidence.
   Checked 2026-09-24: the training project already had Application Insights connected
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

**Hand back to learners:** supply [their verified environment values](setup.md#environment-card), unique prefixes and A's selected Lab 05 option.
Learners then complete [setup sections 2–4](setup.md#learner-files) and follow its A or B link to Lab 00.
Continue below only for the Search/IQ preparation selected for the class.

<a id="search-service"></a>

### Prepare B's Search service before Lab 00

**Owner only, including a self-study learner who owns the subscription. Default A does not need Search.**
If the owner already supplied a service, keep it and check steps 2–4; do not create another one.
Creating a service or changing its billing, roles or network settings requires that owner's approval.

1. In the Azure portal, select **Create a resource → Azure AI Search** and follow [the service-creation form](https://learn.microsoft.com/azure/search/search-create-service-portal).
   Select the course subscription/resource group, a globally unique service name starting with `mfv2-`, **Basic** tier
   (or the owner's approved higher tier) and **Default** compute, not Confidential.
   Before creating it, check that the chosen region offers both **Agentic retrieval** and **Semantic ranker** in
   [the current region table](https://learn.microsoft.com/azure/search/search-region-support); model availability alone does not establish Search availability.
   Review the displayed service cost, then select **Review + create → Create** only within the approved budget.
2. After creation succeeds, open the service's **Overview**. Check the subscription, resource group, region and tier.
   Copy its **URL**, `https://<search>.search.windows.net`, for the setup card's Search endpoint and later `AZURE_SEARCH_ENDPOINT` in `.env`.
   Keep the service name and actual group for item 4 of `operations-checklist.txt` when Lab 00 prepares your personal notes.
   Use the owner's approved network access; do not disable a shared firewall to make the service reachable.
3. Open **Settings → Premium features**. Check **Semantic ranker** and **Knowledge retrieval** separately.
   On a new dedicated service, keep their **Free** feature plans for the limited included allowances; these do **not** make the Basic service free.
   For the core `2026-04-01` API, paid knowledge retrieval has its own consent, separate from semantic ranker.
   **Standard** feature plans need separate cost approval. If an allowance is exhausted, stop and have the owner review the billing error;
   do not change a shared plan or switch providers to bypass it.
   See [semantic-ranker billing](https://learn.microsoft.com/azure/search/semantic-how-to-enable-disable) and
   [knowledge-retrieval billing](https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-enable-disable).
4. Complete [the token-authentication check](#search-authentication) below. On the Search service's **Access control (IAM)**,
   use [Add role assignment](https://learn.microsoft.com/azure/role-based-access-control/role-assignments-portal) to give the actual learner account
   **Search Service Contributor** and **Search Index Data Contributor**, if missing. Verify both assignments on that service.
   Being the subscription Owner alone does not grant Search data access.

**Ready:** the intended service, endpoint, feature plans, token authentication and two writer roles are checked.
Return to [setup](setup.md) for B, then Lab 00; do not continue into optional owner commands.
Do not import data or pre-create the learner's index here: [Lab 06 B](labs/06-knowledge.md#path-b) creates the owned objects
and records their ownership using only the bundled synthetic policies.
These official setup and billing pages were checked on **2026-09-26**; this is a documentation check, not a new live Azure run.

<a id="search-authentication"></a>

### Search authentication and learner roles

**B and optional IQ Chat; owner only.** The workshop uses **Microsoft Entra identity tokens**, not API keys, to call Search.
The service must accept those tokens **and** the caller must have the required roles. Assigning roles alone does not change a keys-only service's authentication setting.

1. In the Azure portal, open the intended **Search service → Settings → Keys** and inspect **API access control**.
   Do not copy or share any displayed keys.
2. For a new dedicated training service, the authorized owner selects **Role-based access control**.
   An existing **Both** setting also accepts identity tokens; leave it unchanged if shared clients still need keys.
   If a shared service has **API Key** selected, stop for the owner's approved transition. Do not disable other clients' authentication to finish this lab.
3. **Check:** the setting reads **Role-based access control** or **Both**. Then verify the role assignments below for the learner's actual sign-in account,
   not only the owner's. Enabling token authentication does not itself grant those roles.

[Official Search authentication steps](https://learn.microsoft.com/azure/search/search-security-enable-roles), checked **2026-09-26**.
This documentation check is not a new live Azure verification. Never add a Search key to `.env` or change providers to bypass an authentication error.

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

Before running this optional block, edit this owner's `.env`: fill `AZURE_SEARCH_ENDPOINT` with the prepared Search URL
and `AZURE_OPENAI_ENDPOINT` with `https://<account>.openai.azure.com` for the same Foundry account.
If Search uses another resource group, fill `AZURE_SEARCH_RESOURCE_GROUP` too.
Keep `AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-6-sol`; IQ Chat uses the separately prepared `gpt-5.6-luna`.
Do not shell-source `.env` or add keys. The `&&` chain stops before later steps if any preparation fails.

```bash
python scripts/workshop.py --language en seed-search --iq --confirm-create &&
python scripts/workshop.py --language en iq-chat check &&
python scripts/workshop.py --language en iq-chat setup --confirm-create &&
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
