# Specialist capabilities: useful boundaries, not implied live completion

**English** | [한국어](../../ko/labs/extensions/specialist-scope.md)

**Reference / owner planning, September 16, 2026.**

**Evidence status:** design and scope only; nothing on this page was executed.

These capabilities belong on the Foundry feature map, but require their own data, identities, infrastructure or runtime.
They are not hidden prerequisites for A, B or the core C modules.

**First pass:** choose one row, complete `specialist-scope.txt` in your notes directory,
and hand it off as **design-only**. No new service, account, data connection or model call is required.

| Capability | What to understand | This course's execution boundary |
|---|---|---|
| Fabric IQ | Published data agents versus semantic models/ontology, asset-specific delegated/OBO or workload identity | Only a separately prepared synthetic asset may be used; no company analytics |
| Work IQ | User context, consent, billing and possible actions in Microsoft 365 | No real company/Microsoft 365 connection or data access |
| Autopilot / Agent 365 | Agent identity versus agent user account, blueprint versus instances, manager and governance | Concept/design only; no mailbox, Teams presence or organizational account creation |
| Private skill catalog | API Center registration, allowed tools, discovery and assessment | Separate API Center infrastructure; not created by attaching a skill to a Toolbox |
| Fine-tuning | When prompting/retrieval/optimization is insufficient; training data and model-weight changes | Separate specialist curriculum; current dev/holdout are not automatically training data |
| Content Understanding receipts | Field extraction design, validation and human review | Design only with synthetic RECEIPT-01; no service calls and no real receipts |
| Voice-based prompt agents | Portal quickstart, realtime media, SDK version boundaries | Design only; Python voice SDK support is in `azure-ai-projects` 2.7.0 beta, outside this edition's pins |
| Publish to Microsoft 365 Copilot/Teams | Stable endpoint, active version and tenant publishing workflow | Concept only; requires an M365 tenant and separate approval |
| Voice / Realtime / image | Modality-specific models, protocols, artifacts, safety and evaluation | Separate approved assets/runtime; text-agent success is not multimodal validation |
| Browser / computer actions | Explicit action permissions, trusted destinations, human approvals and audit | No business-system actions or credentials recorded by this workshop |

## Complete the design worksheet

Pick one capability and record its intended purpose, permitted **synthetic** source, actual calling identity,
resource/region/SDK prerequisites, expected output, evaluation criteria, cost owner and cleanup plan.
If a required asset is absent, write **not prepared / not run** rather than inventing data or a response.
Use design notes only. Do not run commands, call Azure services or upload files for this page.

Do not clone an older workshop and assume its SDK, role or Preview assumptions still apply.
Use the current official contract and this repository's [IQ workbook](../../reference/iq-workbook.md)
for the shared identity and data boundaries.

## What does not count as execution

Reading an article, drawing a routing diagram, listing a feature in the portal,
or replaying an older recording does not establish that a new connection or protocol works.
Likewise, a live connection does not establish semantic correctness, safety, authorization for every user or production readiness.

## Design-only prompts added 2026-09-24

| Exercise | Design notes to capture |
|---|---|
| Content Understanding receipt extraction tied to `RECEIPT-01` | Define fields `date`, `amount`, `merchant` and `category`; apply validation rules from the synthetic policy; route uncertain or policy-significant values to human review; no real receipts, no service calls |
| Voice-based Prompt Agent | Map the portal quickstart prerequisites and expected user experience; record that Python voice-agent SDK support is only in `azure-ai-projects` 2.7.0 beta, outside this edition's pins |
| Publish to Microsoft 365 Copilot/Teams | Explain the stable endpoint and active version concept; record the need for an M365 tenant, app/publishing review and user-facing governance; no publishing action |

**Next:** record the selected scope and limitations in [Lab 11](../11-capstone.md).
[Foundry capability map](https://learn.microsoft.com/azure/foundry/concepts/capability-reference) ·
[Autopilot identity model](https://learn.microsoft.com/azure/foundry/agents/concepts/autopilot-overview).
