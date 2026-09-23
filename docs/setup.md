# Start checklist: one environment, one set of values

**English** | [한국어](ko/setup.md)

**Do this once before Lab 00.** The labs explain every step, but only an Azure owner can grant the subscription,
permissions, model quota and billing approval.

## 1. Choose your starting point

| Your situation | Do this |
|---|---|
| A training environment is ready | Follow sections **1 → 2 → 3 → 4** on this page |
| You own an Azure subscription but have no environment | Complete [owner preparation](#4-environment-owner-checklist), then return to section 2 |
| You have no Azure permission or quota yet | Run only [Lab 00's offline rehearsal](labs/00-start.md#offline-rehearsal) and mark the cloud labs **not run** |

**Choose one route for the whole pass:** **A** if you are new to Azure or agents (browser steps and one prepared
command in Lab 05), or **B** if you are comfortable with Python and APIs. [Compare the routes](paths.md).
Keep one language for the pass: English and Korean use different input files, so switching needs new run labels.

## 2. Fill this environment card

Your instructor or environment owner gives you these values. Write them in `session-notes.txt`:
A finds that file in the learner ZIP (section 3); B copies it from the source repository in Lab 00.
Never write passwords, keys or tokens in the card.

| Value | Needed for | Where to get it |
|---|---|---|
| Azure tenant and subscription IDs | A and B | Azure portal → Subscriptions / directory |
| Foundry account, project and resource group | A and B | Your training project's resource details |
| Full project endpoint | A's Lab 05 terminal and B | Foundry project **Home**; keep the `/api/projects/<project>` ending |
| **Answer deployment** | A and B | **`gpt-6-sol`**, model version **`2026-09-22`** |
| Prefix for your objects | A and B | Starts with **`mfv2-`**; lowercase letters, digits and single hyphens; no trailing hyphen; at most 32 characters. Example: `mfv2-team01-en` |
| Code environment | A's Lab 05 (prepared for you) and B | Repository folder, Python 3.13, activated `.venv`, your own Azure sign-in |
| Search endpoint | B's Lab 06 | The prepared Search service: `https://<search>.search.windows.net` |

<details>
<summary>Optional rows — only if IQ Chat, Hosted serving or an optional evaluation was selected for you</summary>

| Value | Needed for | Where to get it |
|---|---|---|
| Account OpenAI endpoint | Optional IQ Chat / advanced account API | `https://<your-account>.openai.azure.com`; same account as the project |
| IQ chat base | Optional IQ Chat only | The `knowledge_base` returned by `iq-chat setup`, normally `<prefix>-chat-en-kb` |
| Hosted inputs | Optional local/remote hosting only | Project ARM ID and location code, owned agent name, an empty standalone local directory and approvals; **not needed to package** |
| Judge deployment | Optional Foundry evaluations (Lab 07 A step 4, Lab 07 B step 5, Lab 04 section 5) | **`gpt-6-sol-judge`**, a separate deployment of the same model used only to score answers; each evaluation needs the owner's cost approval |

</details>

**For answers, use exactly `gpt-6-sol`.** Do not pick `gpt-6-sol-judge` (it only scores answers in optional evaluations), another listed model or a router.
If the deployment or its version is missing, stop and ask the owner to fix it; the code never switches models.
[Why this model](reference/model-choice.md).

## 3. Download the ready learner materials

**A: follow this section. B: use [Lab 00's source download and notes preparation](labs/00-start.md#path-b);
you do not need this additional ZIP.** The source repository already contains the same blank note templates.

Open [English learner-materials.zip](../data/learner/en/learner-materials.zip), choose **Download raw file**, and extract it.
This small ZIP requires no Python and does not include videos, holdout or reference-answer fields.
For private repositories, use a GitHub account with read access.

| File | Use |
|---|---|
| `START-HERE.txt` | File-by-file instructions |
| `instructions-with-policies.txt` | Copy the entire file into a new Prompt Agent's **Instructions**, then Save |
| `instructions.txt` | Instructions without inline evidence, for the optional File Search path |
| `policies/` | Exactly six synthetic TXT files to upload for File Search |
| `dev-questions.txt` | Copy one question, not the case ID or an evaluation record, into each new chat |
| `dev-questions.jsonl` | The same six questions as a dataset for the optional Lab 07 Foundry evaluation; no answers |
| `assessment.csv` | Blank six-case worksheet; record your actual answers/citations/pass or fail |
| `session-notes.txt` | Blank setup card, Lab 01–03/06 observations, Lab 07 A versions/results, last completed step and resume link |
| `workflow-review.txt` | Blank Lab 05 command/output and human review record |
| `operations-checklist.txt` | Blank Lab 09 owned/shared asset, cleanup and residual-cost checklist |
| `SOURCE.json` | Language and canonical input hashes |

You can also open [the complete inline instructions](../data/learner/en/instructions-with-policies.txt) or
[questions-only file](../data/learner/en/dev-questions.txt) directly.
Do not paste `dev.jsonl` reference-answer columns into an agent.

Keep the extracted folder as your **personal evidence folder outside the repository**.
Fill the note templates as you go; in Lab 07, save `assessment.csv` as `assessment-baseline.csv`.
Empty templates are not completed evidence. Nothing in this ZIP installs a code environment.

<a id="5-ready-to-start"></a>

## 4. Ready to start

- [ ] I can open the intended project with my own account.
- [ ] The actual `gpt-6-sol` deployment and version `2026-09-22` are prepared.
- [ ] A: I have the learner ZIP and know which file goes into Instructions versus chat. B: I know the source-copy and notes-preparation steps in Lab 00.
- [ ] My Lab 05 terminal is ready; if not, I complete Lab 00 B and Lab 02 B **before** starting the timed A route.
- [ ] For B, Search access and owned-object creation costs are approved. For A, IQ Chat is **not selected** unless separately prepared.
- [ ] I know who owns costs/permissions and will not create resources or grant roles without approval.

If a required box is not ticked, stop and finish that preparation first. An offline fixture never replaces a live result.
**Ready: [A → Lab 00 browser](labs/00-start.md#path-a) · [B → Lab 00 code](labs/00-start.md#path-b).**
The owner reference below is not another learner step.

<a id="4-environment-owner-checklist"></a>

## Environment-owner preparation

<details>
<summary>Only if preparing the environment yourself — separate authorization, time and costs</summary>

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

Return to [the ready check](#4-ready-to-start) after preparation; do not run optional owner commands for the default A route.

</details>
