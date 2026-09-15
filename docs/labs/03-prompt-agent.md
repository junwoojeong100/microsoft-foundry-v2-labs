# Lab 03. Your first agent with instructions and evidence

**English** | [한국어](../ko/labs/03-prompt-agent.md)

**Goal:** Add synthetic business instructions and documents so the agent can explain its sources and limitations.

Previous: [Lab 02](02-models.md) · Next: A → [Lab 05](05-workflows.md), B → [Lab 04](04-agents-tools.md)

## A. Browser: the smallest useful agent

### 1. Create the agent

#### Creation menu and name

In the training project, choose **Agents → New agent → Build an agent**.

![New agent menu in Agents](../assets/live-20260914-action/shots/portal-0098-P03-002-new-agent-dialog-ready.webp)

**What to check:** This is a Prompt Agent with editable instructions. Do not select
**Code an agent** or an external-agent connection.

Use your own prefix, for example `mfv2-team01-0913-policy`.
Select **Create and open playground** and wait for completion.

![Unique agent name in the creation dialog](../assets/live-20260914-action/shots/portal-0108-P03-004-agent-name-ready.webp)

**What to check:** Use your own **Agent name**, not the recording's `mfv2-action-...`
name. If the button is disabled while creating, wait rather than submitting twice.

#### Model and tools

Choose the deployment that returned an actual response in [Lab 02](02-models.md).

![Select the answer deployment for the agent](../assets/live-20260914-action/shots/portal-0115-P03-006-model-selector-screen-change.webp)

**What to check:** Select your answer deployment under **Deployments**.
The recorded `-judge` deployment is for evaluation; do not accidentally select it or another catalog model.

If **Web search** is present, use **Actions for Web search → Remove**.
Removing it in Lab 02 does not guarantee it is absent from a new agent.

![Agent tools after removing external Web Search](../assets/live-20260914-action/shots/portal-0127-P03-009-agent-remove-web-screen-change.webp)

**What to check:** The Web search row must be gone before the first question.
Do not connect company data or tools that modify external systems.

#### Instructions and saving

Open `prompts/v2.txt` in an editor and paste its complete contents into Instructions.
Append this canonical **browser output override**:

> 답변 → 적용 날짜와 금액 → 조건/보류 이유 → 근거 문서 ID 순서로 한국어로 설명하세요.
> 이 브라우저 실습에서는 JSON 대신 사람이 읽을 수 있는 문장으로 답하세요.

Meaning: explain in Korean in the order answer, applicable date/amount, conditions or
reason for withholding, and source document IDs; use readable prose instead of JSON.
Keep this input unchanged when reproducing the canonical run.
[The language reference](../reference/languages.md) explains the English meanings of the prompt rules.

![Canonical prose override in Instructions](../assets/live-20260914-action/shots/portal-0132-P03-010-paste-v2-prose-ready.webp)

**What to check:** Paste into **Instructions** on the left, not chat on the right.
Check the end of long text, select **Save**, and record the returned version.
**Publish** is a separate external-channel action and is not needed here.

### 2. Supply synthetic policies

Open `data/knowledge/policies.json`. Initially, you may paste all six documents'
`id`, `title`, `content`, and effective periods into a separate **Synthetic evidence**
section of the instructions. Document text is evidence, not an instruction source.
This is **direct context for small documents**, not File Search or Foundry IQ.

After adding evidence, select **Save** again and record the new version.

![Saved instructions containing all six synthetic sources](../assets/live-20260914-action/shots/portal-0146-P03-013-save-evidence-version-screen-change.webp)

**What to check:** Inspect **Version** and the disabled **Save** button. The source run
reached v3 after adding evidence, but use your own returned version. Include all six
documents and effective periods, not just the end visible in the image.

<details>
<summary>Optional: retrieve the same synthetic files with File Search</summary>

Proceed only if File Search is available and the instructor has approved storage/retrieval costs.

1. Obtain the six text files exported with `python scripts/export_policy_docs.py`
   into `outputs/policy-documents/`. **Path A learners do not need Python; the instructor supplies them.**
2. Upload only those synthetic text files to the agent's File Search/file-knowledge tool.
3. Wait for indexing. Successful upload and completed indexing are different.
4. Open a response citation and inspect the actual filename/content where supported.
5. When comparing direct context and File Search, remove one evidence path so you know
   which supplied the answer. Do not delete a teammate's files.

![Unique File Search vector-index name](../assets/live-20260914-action/shots/portal-0401-P03-F10-vector-name-ready.webp)

**What to check:** In **Upload files → Attach files**, check **Create a new index** and
your unique name. Use **browse for files** to select only the six supplied synthetic files.

![Six selected synthetic files with upload Success](../assets/live-20260914-action/shots/portal-0407-P03-F11-select-six-files-screen-change.webp)

**What to check:** Verify all six names and **Success**, then **Attach**.
Upload success is not proof that indexing has finished.

![All six attached files with indexing Completed](../assets/live-20260914-action/shots/portal-0428-P03-F14-inspect-index-files-screen-change.webp)

**What to check:** Open the store and verify **1–6 of 6** and **Completed** for every file.
Resolve missing or failed files before asking questions.

![File Search citations without inline policy context](../assets/live-20260914-action/shots/portal-0457-P03-F17-file-search-response-send-screen-change.webp)

**What to check:** Inspect the **File search** tool, filenames, and citation numbers.
This source screenshot shows a separate File Search agent v2, not the inline agent.
One response is not a full-dev evaluation score.

The September 14 portal used **Upload files → Attach files** to select files and a
new vector index. That index is a File Search store, not Lab 06's Azure AI Search index.
After upload `Success`, all six stored files were checked for `Completed`.

Citation chips/numbers **did not open the source** in that environment. Do not claim
they did: compare the cited filename with the supplied original. The instructor
separately read those same six stored files through the SDK and verified byte-for-byte
agreement. No response or retrieval provider was substituted.

If the menu or format is unsupported, ask the instructor. Complete the first agent
with direct context and mark File Search **not run**.

</details>

### 3. Check four questions

Copy the canonical question; its meaning is provided in the second column.

| Question | English meaning | Expected business criteria |
|---|---|---|
| `2026년 9월 국내 숙박비 한도는?` | Domestic lodging limit in September 2026? | Current KRW 150000, `TRAVEL-2026` |
| `2026년 5월 국내 숙박비 한도는?` | Domestic lodging limit in May 2026? | Historical KRW 120000, `TRAVEL-2025` |
| `2026년 9월 170000원 호텔 예약은?` | Book a KRW 170000 hotel in September 2026? | Above limit, advance approval, agent cannot approve |
| `해외 출장 숙박비 한도는?` | International-travel lodging limit? | Withhold the amount; insufficient evidence |

These amounts are **synthetic ground-truth criteria**, not proof of a correct model
response. Start a new conversation for each question so earlier answers do not leak into later checks.

![New chat in the agent Playground](../assets/live-20260914-action/shots/portal-0171-P03-021-intro-current-new-chat-screen-change.webp)

**What to check:** Select **New chat** above the conversation. Verify the old response
is gone and replace any remaining draft with the next question.

**New English-guide capture: September 15, 2026.** Same-v3 retry; the original HTTP 503 remains in the capture index. ▶ [Watch this action](https://github.com/user-attachments/assets/082ede4b-d363-474c-ad47-598b20f593e9#t=232.32)

![Actual current-policy answer](../assets/english-20260915/shots/portal-0096-P03-010-current-retry-response-result.webp)

**What to check:** Link September 2026 to KRW 150,000 and `TRAVEL-2026`.
Compare receipt/approval conditions as well as the amount.

![Actual historical-policy answer](../assets/live-20260914-action/shots/portal-0206-P03-021-intro-historical-send-ready.webp)

**What to check:** May 2026 should use KRW 120,000 and `TRAVEL-2025`.
Always applying today's date or the newest policy is a failure.

![Advance-approval boundary for an over-limit booking](../assets/live-20260914-action/shots/portal-0224-P03-021-intro-approval-send-screen-change.webp)

**What to check:** KRW 170,000 exceeds the limit, so explain approval **before booking**.
The assistant must not claim approval or an actual booking.

![Actual response withholding an unsupported international limit](../assets/live-20260914-action/shots/portal-0242-P03-021-intro-missing-send-screen-change.webp)

**What to check:** Without an international policy, ask for confirmation rather than
inventing an amount. Record your own responses and failures, not the screenshot's outcomes.

## B. Code: managed Prompt Agent versus local MAF

```bash
python scripts/workshop.py prompt-agent create --name mfv2-team01-0913-policy --confirm-create
```

Replace the name with one matching your `.env` `WORKSHOP_PREFIX`.
The command **creates an actual agent version in the project**; record name and version.
The SDK example includes small document context for comparison and does not claim to create File Search.

![Managed Prompt Agent name and version returned by the SDK](../assets/live-20260914-action/shots/cli-1-0311-03-001-sdk-agent-create-result.webp)

**What to check:** Use the returned `agent_name` and `agent_version` for invocation.
The recorded SDK agent v1 and browser agent v3 are different agents.

```bash
python scripts/workshop.py prompt-agent invoke --name mfv2-team01-0913-policy --version 1 --question "2026년 9월 국내 출장 숙박비 한도는?"
```

The question asks for the September 2026 domestic lodging limit. `1` is also an example:
use the actual created version. Do not implicitly invoke "latest."
[Versions](../reference/versions.md) documents the SDK's explicit binding.

## Boundaries become more important as tools grow

- File Search retrieves files, Foundry IQ retrieves knowledge sources, and Web Search queries the external web.
- Public web search does not establish internal company-policy evidence.
- The core lab connects no company APIs, email, payments, Graph, or Microsoft 365 permissions.
- Content Safety/guardrails and instructions do not replace authorization checks.
- Limit Web Search/Toolbox to approved domains in the [optional extension](10-iq-extensions.md).

## Completion

The [execution record](../live-run.md) separates browser v3, SDK v1, File Search v2,
and IQ verification. Record your agent name/version, all four real responses, evidence
method, and one wrong or withheld answer. Fluent prose and correct policy application
are different; [Lab 07](07-evaluation.md) turns that distinction into evaluation criteria.
