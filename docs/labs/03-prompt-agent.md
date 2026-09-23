# Lab 03. Your first agent with instructions and evidence

**English** | [한국어](../ko/labs/03-prompt-agent.md)

**Goal:** Add synthetic business instructions and documents so the agent can explain its sources and limitations.

**Open your section:** [A — inline agent](#path-a) · B: [skip to Lab 04 B](04-agents-tools.md#path-b) · [Paths](../paths.md)

## Before you start

**This pass:** A creates one Prompt Agent with the ready inline instruction file. File Search and SDK creation are separate optional branches.

**Need:** The learner ZIP, your prefix and the model that succeeded in Lab 02.

**Continue when:** The saved agent name/version and your own answers to the four checks are recorded.

**If blocked:** If answers ignore the policies, check that the whole file is in **Instructions** (not the chat box) and saved. Use your own agent name and the version the portal returns.

[One-time setup and learner files](../setup.md).

<a id="path-a"></a>

## A. Browser: the smallest useful agent

This creates an agent, saves a version and makes billable test calls. Use the approved training project and your own prefix.
Keep `session-notes.txt` open for the returned version and actual answers; no deployment or Publish action is required.

### 1. Create the agent

#### Creation menu and name

Select **Build** in the top bar and **Agents** in the left menu, then **New agent** → **Build an agent**.


![September 23 English recording: New agent → Build an agent](../assets/g6sol-20260923-en/screenshots/EP03-002-build-agent-2.webp)

**What to check:** This is a Prompt Agent with editable instructions. Do not select
**Code an agent** or an external-agent connection.

In **Agent name**, replace the generated name with one that starts with your prefix, for example `mfv2-team01-en-policy`.
Select **Create and open playground** and wait for completion.


![September 23 English recording: Use the owned agent name, then create and open the playground](../assets/g6sol-20260923-en/screenshots/EP03-003-name-2.webp)

**What to check:** Use your own **Agent name**, not the recording's `mfv2-sol-20260923-en-policy`
name. If the button is disabled while creating, wait rather than submitting twice.
Opening the first agent can also create a `text-embedding-3-large` deployment; note it for the Lab 09 cleanup inventory.

#### Model and tools

Open the **Model** list at the top left and select **`gpt-6-sol`** under **Deployments** (the deployment that answered in [Lab 02](02-models.md)).


![September 23 English recording: Select the gpt-6-sol answer deployment under Deployments](../assets/g6sol-20260923-en/screenshots/EP03-004-model-2.webp)

**What to check:** Select your answer deployment under **Deployments**.
`gpt-6-sol-judge` is for evaluation; do not select it or another catalog model.

In **Tools**, if **Web search** is listed, open its **⋮** menu and select **Remove**.
Removing it in Lab 02 does not remove it from a new agent.


![September 23 English recording: Remove Web search from the new agent](../assets/g6sol-20260923-en/screenshots/EP03-005-remove-web-2.webp)

**What to check:** The Web search row must be gone before the first question.
Do not connect company data or tools that modify external systems.

#### Instructions and saving

1. Open **`instructions-with-policies.txt`** from the [learner ZIP](../setup.md#3-download-the-ready-learner-materials) in a text editor.
2. Select all of its text and copy it.
3. Paste it into **Instructions** on the left, not into the chat box on the right.
4. Select **Save** at the top right and write the **Version** shown next to it in `session-notes.txt`.

The file already contains the instructions and all six synthetic policies; do not add other text.


![September 23 English recording: Paste instructions-with-policies.txt into Instructions](../assets/g6sol-20260923-en/screenshots/EP03-006-instructions-2.webp)

**What to check:** the pasted text is in **Instructions** and ends with the file's last paragraph, **Browser output format: …**.
After **Save**, a version number appears at the top. **Publish** is not needed in this lab.

### 2. Verify the supplied policies

The pasted file puts six synthetic policies directly into the agent's context (not File Search or Foundry IQ).

1. In **Instructions**, find the six IDs: `TRAVEL-2025`, `TRAVEL-2026`, `APPROVAL-01`, `RECEIPT-01`, `MEAL-01` and `SCOPE-01`.
2. Open the same six files in the ZIP's `policies/` folder and compare each amount and effective period.
3. If one is missing or different, paste the whole file again and select **Save**; otherwise change nothing.

![September 23 English recording: Save and read the returned agent version](../assets/g6sol-20260923-en/screenshots/EP03-007-save-2.webp)

**What to check:** all six IDs, amounts and effective periods match `policies/`. **Save** is greyed out after saving,
and **Version** shows your returned number (the recording shows version 2; yours may differ).

<details>
<summary>Optional: retrieve the same synthetic files with File Search</summary>

Proceed only if File Search is available and the instructor has approved storage/retrieval costs.
This optional branch was not re-recorded with `gpt-6-sol` on September 23, 2026, so it has no screenshots.

1. Create a **separate** agent using your prefix plus `-files`; keep the inline agent unchanged for Lab 07.
2. Paste the ZIP's **`instructions.txt`** into its **Instructions**, select `gpt-6-sol`, remove **Web search**, and select **Save**.
3. In **Tools**, select **Upload files → Attach files**, choose **Create a new index** with your unique name, then use
   **browse for files** to select only the six **`.txt` files inside `policies/`** (not the ZIP, CSV or inline instruction file).
4. Check that all six names show **Success**, then select **Attach**. Upload success does not mean indexing has finished.
5. Open the store and wait for **1–6 of 6** and **Completed** on every file. Resolve missing or failed files first.
6. Ask one question, then compare the cited filename and content with the supplied original.
   Do not combine inline policies and File Search in this comparison.

**What to check:** the **File search** tool is listed and the answer cites policy filenames. One response is not a full-dev score.
The new index is a File Search store, not Lab 06's Azure AI Search index. Do not assume citation chips open the source.

If the menu is unavailable, leave this optional branch unselected. If an attempted upload/retrieval fails,
retain that failure and stop the branch; do not relabel the inline response as File Search.

</details>

### 3. Check four questions

Ask D01, D02, D03 and D05 one at a time. Copy **only the question** from the ZIP's `dev-questions.txt`;
do not send the criteria column below.

| Case | Topic | Expected business criteria |
|---|---|---|
| D01 | September 2026 lodging | Current KRW 150000, `TRAVEL-2026` |
| D02 | May 2026 lodging | Historical KRW 120000, `TRAVEL-2025` |
| D03 | Over-limit booking | KRW 150000 limit; approval **before booking**; `TRAVEL-2026` + `APPROVAL-01`; the agent cannot approve |
| D05 | International travel | Withhold the amount; explain insufficient evidence and cite `SCOPE-01` |

These amounts are **synthetic ground-truth criteria** (the same ones Lab 07 uses), not proof that your agent already passes.

For each of the four questions:

1. Select **New chat** (+ icon) and check that the previous answer is gone, so earlier answers do not leak into later checks.
2. Paste the question into **Message the agent...** and send it.
3. Copy the full answer into that case's line in the **Lab 03** section of `session-notes.txt`.
4. Compare its amount, applicable date, cited IDs and approval conditions with that case's row in the table above, and write your finding.
   For D05, withholding the amount is correct, but a missing `SCOPE-01` citation is still a finding.

<details>
<summary>September 23 English recording — not the results of your own four questions</summary>

![September 23 English recording: D01 · new chat, question and actual answer](../assets/g6sol-20260923-en/screenshots/EP03-101-d01-2.webp)

**What to check:** D01: KRW 150,000 per night from July 1, 2026 with `TRAVEL-2026`. Compare the receipt and approval conditions too.

![September 23 English recording: D02 · new chat, question and actual answer](../assets/g6sol-20260923-en/screenshots/EP03-102-d02-2.webp)

**What to check:** D02: May 2026 uses the historical KRW 120,000 and `TRAVEL-2025`, not the current policy.

![September 23 English recording: D03 · new chat, question and actual answer](../assets/g6sol-20260923-en/screenshots/EP03-103-d03-2.webp)

**What to check:** D03: KRW 170,000 exceeds the limit, so approval is needed before booking. The agent must not claim approval.

![September 23 English recording: D05 · new chat, question and actual answer](../assets/g6sol-20260923-en/screenshots/EP03-105-d05-2.webp)

**What to check:** D05: no international policy exists, so the amount is withheld. Check whether `SCOPE-01` is cited.

These four images are recording examples. Record your own actual answers and failures separately.

</details>

**Save:** in your saved agent's **Instructions**, select all text (Ctrl+A or Cmd+A), copy it and save it as
`instructions-baseline.txt` in your personal evidence folder. Record that filename and version in `session-notes.txt`.
The downloaded instruction file alone does not establish what was actually saved. Do not overwrite an earlier pass's snapshot.

**A done:** keep `instructions-baseline.txt`, its agent version and four checks in your evidence folder.
Continue to [Lab 05 A](05-workflows.md#path-a); Lab 04 and the SDK branch below are not required for A.

## B. Optional SDK branch: managed Prompt Agent versus local MAF

<details>
<summary>Optional SDK agent — creates a different agent; not required by either core route</summary>

This is not required for A or B's first pass. It creates a separate agent.
Enter a new name starting with your `.env` `WORKSHOP_PREFIX`; do not reuse the browser agent's name.

```bash
printf 'New agent name (<your prefix>-policy-sdk): '
read -r AGENT_NAME
python scripts/workshop.py --language en prompt-agent create --name "$AGENT_NAME" --confirm-create
```

Replace the name with one matching your `.env` `WORKSHOP_PREFIX`.
The command **creates an actual agent version in the project**; record name and version.
The SDK example includes small document context for comparison and does not claim to create File Search.


![September 23 English recording: Optional SDK Prompt Agent: create an owned version](../assets/g6sol-20260923-en/screenshots/E03-001-sdk-create-2.webp)

**What to check:** Use the returned `agent_name` and `agent_version` for invocation.
The recorded SDK agent (version 1) and browser agent (version 2) are different agents.

```bash
printf 'agent_version returned above: '
read -r AGENT_VERSION
python scripts/workshop.py --language en prompt-agent invoke --name "$AGENT_NAME" --version "$AGENT_VERSION" --question "What is the domestic business-trip lodging limit for September 2026?"
```

Use the actual returned version in the same terminal. Do not type `1` from a recording or invoke "latest."

![September 23 English recording: Invoke the returned SDK agent version](../assets/g6sol-20260923-en/screenshots/E03-002-sdk-invoke-2.webp)

**What to check:** The SDK call names the exact returned version (`1` in this recording), not "latest".

[Versions](../reference/versions.md) documents the SDK's explicit binding.

</details>

## Boundaries become more important as tools grow

- File Search retrieves files, Foundry IQ retrieves knowledge sources, and Web Search queries the external web.
- Public web search does not establish internal company-policy evidence.
- The core lab connects no company APIs, email, payments, Graph, or Microsoft 365 permissions.
- Content Safety/guardrails and instructions do not replace authorization checks.
- Limit Web Search/Toolbox to approved domains in the [optional extension](10-iq-extensions.md).

## Completion

The [execution record](../live-run.md) separates the browser agent (version 2) and the SDK agent (version 1)
recorded on September 23. Record your agent name/version, all four real responses, evidence
method, and one wrong or withheld answer. Fluent prose and correct policy application
are different; [Lab 07](07-evaluation.md) turns that distinction into evaluation criteria.

Next: A → [Lab 05](05-workflows.md#path-a) · B: [skip to Lab 04](04-agents-tools.md#path-b)
