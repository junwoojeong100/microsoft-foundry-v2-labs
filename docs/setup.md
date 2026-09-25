# Start checklist: one environment, one set of values

**English** | [한국어](ko/setup.md)

**Finish with the files and verified values for your chosen route. Then start Lab 00.**
The environment owner supplies Azure access, permissions, model quota and billing approval.
This page does not ask learners to create resources.

## 1. Choose your starting point

| Your situation | Do this |
|---|---|
| A training environment is ready | Follow sections **1 → 2 → 3 → 4** on this page |
| You own an Azure subscription but have no environment | Complete [owner preparation](setup-owner.md), then follow sections 2–4 |
| You have no Azure permission or quota yet | Run only [Lab 00's offline rehearsal](labs/00-start.md#offline-rehearsal) and mark the cloud labs **not run** |

**Choose one route for the whole pass:** **A** if you are new to Azure or agents (browser steps and one prepared
Lab 05 workflow option), or **B** if you are comfortable with Python and APIs. [Compare the routes](paths.md).
Keep one language for the whole pass: English and Korean use different input files (in B, a switch also needs new run labels).

<a id="learner-files"></a>
<a id="3-download-the-ready-learner-materials"></a>

## 2. Get the files for your route

**A: download the learner ZIP below before filling the card in section 3.**
**B: skip this download.** Keep a supplied source copy; otherwise [Lab 00 B](labs/00-start.md#source-folder)
walks through downloading it. It already contains the blank note templates.
Keep the owner's values from section 3 ready; record them in the personal notes that Lab 00 prepares after opening the source folder.

### A's learner ZIP

Open [English learner-materials.zip](../data/learner/en/learner-materials.zip), choose **Download raw file**, and extract it.
This approximately 20 KB ZIP delivers all 16 learner files in one download, without Python, Git or the full source repository.
It is a generated handout, not another source of truth. It contains no videos, holdout or reference-answer fields; B already has the files and skips it.
For private repositories, use a GitHub account with read access.

| File | Use |
|---|---|
| `START-HERE.txt` | File-by-file instructions |
| `instructions-with-policies.txt` | Copy the entire file into a new Prompt Agent's **Instructions**, then Save |
| `instructions.txt` | Instructions without inline evidence, for the optional File Search path |
| `policies/` | Six original synthetic TXT files to inspect in core Labs 03 and 06; upload only for separately selected, available File Search |
| `dev-questions.txt` | Copy one question, not the case ID or an evaluation record, into each new chat |
| `dev-questions.jsonl` | The same six questions as a dataset for the optional Lab 07 Foundry evaluation; no answers |
| `assessment.csv` | Blank six-case worksheet; record your actual answers/citations/pass or fail |
| `session-notes.txt` | Blank setup card, Lab 01–03/06 observations, Lab 07 A versions/results, last completed step and resume link |
| `workflow-review.txt` | Blank Lab 05 command/output and human review record |
| `operations-checklist.txt` | Blank Lab 09 owned/shared asset, cleanup and residual-cost checklist |
| `SOURCE.json` | Language and canonical input hashes |

You can also open [the complete inline instructions](../data/learner/en/instructions-with-policies.txt) or
[questions-only file](../data/learner/en/dev-questions.txt) directly.
`dev-questions.txt` and `dev-questions.jsonl` contain questions only; paste only the question text into a chat.

Keep the extracted folder as your **personal evidence folder outside the repository**.
Fill the note templates as you go; in Lab 07, save `assessment.csv` as `assessment-baseline.csv`.
Empty templates are not completed evidence. Nothing in this ZIP installs a code environment.

<a id="environment-card"></a>
<a id="2-fill-this-environment-card"></a>

## 3. Collect the environment values

Get these values from your instructor or environment owner.
Confirm the **sign-in account as well as the tenant**. Your usual work account and the workshop account can be different;
browser sign-in and Azure CLI sign-in are also separate sessions. Never share credentials to make them match.
**A:** fill `session-notes.txt` from the ZIP you just extracted.
**B:** keep the owner's values; copy them into `outputs/learner-notes-en/session-notes.txt` when Lab 00 prepares that file.
You do not need to install anything just to collect the values. Never record passwords, keys or tokens.

| Value | Needed for | Where to get it |
|---|---|---|
| Azure tenant and subscription IDs | A and B | Azure portal → Subscriptions / directory |
| Foundry account, project and resource group | A and B | Your training project's resource details |
| Full project endpoint | A and B | Foundry project **Home**; keep the `/api/projects/<project>` ending |
| **Answer deployment** | A and B | **`gpt-6-sol`**, model version **`2026-09-22`** |
| Prefix for your objects | A and B | Starts with **`mfv2-`**; lowercase letters, digits and single hyphens; no trailing hyphen; at most 32 characters. Example: `mfv2-team01-en` |
| Code environment | B; A's default Lab 05 terminal option | Repository folder, Python 3.13, activated `.venv`, your own Azure sign-in |
| Prepared Hosted workflow agent | Only for A's separately selected Lab 05 browser option | Owner-verified name/version and Playground location; sequential local/v2 Responses profile in your language, not the Lab 03 Prompt Agent |
| Search endpoint | B's Lab 06 | The prepared Search service: `https://<search>.search.windows.net` |

**For answers, use exactly `gpt-6-sol`.** Do not pick `gpt-6-sol-judge` (it only scores answers in optional evaluations), another listed model or a router.
If the deployment or its version is missing, stop and ask the owner to fix it; the code never switches models.
[Why this model](reference/model-choice.md).

<details>
<summary>Optional values — only for separately selected IQ Chat, hosting or cloud evaluation</summary>

| Value | Needed for | Where to get it |
|---|---|---|
| Account OpenAI endpoint | Optional IQ Chat / advanced account API | `https://<your-account>.openai.azure.com`; same account as the project |
| IQ chat base | Optional IQ Chat only | The `knowledge_base` returned by `iq-chat setup`, normally `<prefix>-chat-en-kb` |
| Hosted inputs | Optional local/remote hosting only | Project ARM ID and location code, owned agent name, an empty standalone local directory and approvals; **not needed to package** |
| Judge deployment | Optional Foundry evaluations (Lab 07 A step 4, Lab 07 B step 5, Lab 04 section 5) | **`gpt-6-sol-judge`**, a separate deployment of the same model used only to score answers; each evaluation needs the owner's cost approval |

</details>

<a id="5-ready-to-start"></a>

## 4. Ready to start

- [ ] I can open the intended project with my own account.
- [ ] The actual `gpt-6-sol` deployment and version `2026-09-22` are prepared.
- [ ] A: I have the learner ZIP and know which file goes into Instructions versus chat. B: I know the source-copy and notes-preparation steps in Lab 00.
- [ ] I have the default prepared Lab 05 terminal, or the owner has preselected and verified the optional Hosted Responses Playground path. If neither was supplied, I complete Lab 00 B and Lab 02 B **before** starting the timed A route.
- [ ] For B, Search access and owned-object creation costs are approved. For A, IQ Chat is **not selected** unless separately prepared.
- [ ] I know who owns costs/permissions and will not create resources or grant roles without approval.

If a required box is not ticked, stop and finish that preparation first. An offline fixture never replaces a live result.
**Ready: [A → Lab 00 browser](labs/00-start.md#path-a) · [B → Lab 00 code](labs/00-start.md#path-b).**
The owner reference below is not another learner step.

<a id="4-environment-owner-checklist"></a>

## Environment-owner preparation

The owner checklist moved to [Environment owner preparation](setup-owner.md). It includes the Azure resource, permission, Application Insights, optional Hosted workflow, optional Dev Pack and IQ Chat preparation steps.

Return here after the owner has supplied the values above. **Ready: [A → Lab 00 browser](labs/00-start.md#path-a) · [B → Lab 00 code](labs/00-start.md#path-b).**
