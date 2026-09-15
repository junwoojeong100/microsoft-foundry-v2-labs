# Instructor guide: resolve setup risks before class

**English** | [한국어](ko/instructor.md)

**Class time is not installation, subscription creation, or feature-approval time. Verify every team's environment first.**

Parent: [Learning paths](paths.md) · Evidence: [Validation record](reference/validation.md)

## 1. Choose the class scope

| Class | Prepare | Optional exclusions |
|---|---|---|
| A. Beginner | Browser accounts, project, model, synthetic documents, assessment sheet, prepared MAF environment | Python authoring, Hosted, actual M365/Fabric |
| B. Practitioner | Above plus Python/SDKs, read permissions, code environment | Paid judge and remote Hosted deployment are separate gates |
| IQ advanced | Search, authentication, semantic/knowledge retrieval settings | Planner, embeddings, richer Preview are unnecessary for basic GA |
| Hosted advanced | Python 3.13 runtime, actual ARM ID, deployment/identity permissions | Local Docker is unnecessary for code deployment |

Do not make beginners depend on every Preview approval or company M365 connection.
Give each team a unique agent/Search prefix. Only instructors manage shared service
creation and deletion. Do not prepare a portal Workflow Designer exercise: A's Lab 05
runs existing MAF code. Check the SDK, venv, and each learner's model-call permission.

English and Korean use **separate frozen language bundles** with equivalent IDs, dates, amounts and judgments.
English commands explicitly select `--language en`; neither language silently substitutes the other.
Give each learner [the setup card and ready ZIP](setup.md), not raw evaluation records or a request to assemble policy JSON.
The ZIP supplies complete instructions, six TXT sources, questions only and a blank assessment. [Language lineage](reference/languages.md) stays intact.

## 2. Three to seven days before: accounts, permissions, costs

1. Assign an owner and a dedicated training subscription/resource group; keep production separate.
2. Verify the current Foundry project and **`gpt-5.6-luna` / `2026-07-09`**, deployed as **`gpt-5.6-luna`**.
   Check quota, SKU and region; do not let first-time learners guess a replacement.
3. Assign the required project roles, such as `Foundry User`, to participants.
4. Prepare separate Search data read/write roles.
5. Prepare the roles the remote agent identity needs for models and tools.
6. Send a first request using an **actual participant account**, not an administrator.
7. Set budget alerts and log retention. Budget alerts are not an automatic spending cap.
8. Review optional-feature approvals, cross-region processing, and tenant policies.

Role names may still appear as `Azure AI ...`. Check the current
[Foundry role table](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).


**What to check:** This is a September 14, 2026 preparation example. Distinguish `used`,
`limit`, and SKU, and query again immediately before class. These numbers and Sweden
Central availability do not apply automatically to another subscription or date.

### Values to give each team

Distribute **values only**, separately, in `.env.example` format. Never distribute passwords, keys, or tokens.

- Subscription/tenant IDs, resource group, and Foundry account.
- Full project endpoint, including `/api/projects/...`.
- Exact `gpt-5.6-luna` answer deployment and verified model version `2026-07-09`.
- Unique `WORKSHOP_PREFIX`.
- Optional Search endpoint, account OpenAI root, and the **chat-base name printed by `iq-chat setup`**, distinct from the GA base.
- Optional judge deployment and underlying model.
- Actual project ARM ID and unique agent name if Hosted is selected.

Also hand over the repository location and an activated, participant-signed-in MAF terminal for Lab 05.
For self-study, [Lab 00 B](labs/00-start.md#b-code-one-folder-one-environment) is the full setup route, not an assumed instructor action.

## 3. Prepare Search/IQ

The default is a text index and **GA `2026-04-01` minimal/extractive retrieval**.
Check these separately:

| Item | Check |
|---|---|
| Service tier/region | Support for the selected features |
| Data-plane authentication | Document reads/writes with Entra ID |
| Participant roles | Reader + Search Index Data Reader; Search Service/Index Data Contributor only for required writers |
| Semantic ranker | Configuration and separate charges for GA semantic intent |
| Knowledge retrieval | Management-plane usage/billing consent; `free`/`standard` conditions |
| Source citations | Returned `id`, `title`, and `content` |

Scripts do not silently change billing to `standard`. An administrator reviews
[official migration/configuration guidance](https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-migrate).
For a Chat completion model, give **the Search service's identity** `Cognitive Services User` on the model's Foundry account.
Selecting managed identity is supported; it does not borrow the local user's or Hosted agent's role.
The model-based Preview path is separate from the default direct-intent retrieval experiment.
For that optional segment, use the fixed **Luna + Search system-assigned identity + `low` + `answerSynthesis`** preset.
Follow [the owner sequence](setup.md#4-environment-owner-checklist) once and give learners its exact chat-base name.
Do not hand out the model-free GA base as a ready-to-chat configuration.
`iq-chat check` is read-only; `iq-chat setup --confirm-create` creates only the owned separate base;
`iq-chat ask --label <new-label> --confirm-cost` verifies actual paid planning/synthesis.
Neither command deploys a model or grants roles. [Details and recovery](reference/iq-model-identity.md).
For the learner's CLI checks, verify Reader on the training Foundry account/Search service
and Search Index Data Reader for retrieval. Project-only access is not account-level ARM/role visibility;
do not discover that missing prerequisite halfway through Lab 06.

## 4. The day before: rehearse the same edition

Freeze the documentation/code version and rehearse in a fresh, independent folder.
Hosted initialization can discover a parent `azure.yaml`; stay outside another azd project.
Complete Lab 00 B's `.env` and participant sign-in first. Run the block below only with the approved training values.

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock.txt -e ".[cloud,agents,hosted,dev]"
python -m pip check
python scripts/check_sdk.py
python -m unittest discover -s tests -t . -v
python -m unittest discover -s tests_sdk -t . -v
python scripts/check_docs.py
python scripts/workshop.py --language en doctor
python scripts/workshop.py --language en doctor --cloud
python scripts/workshop.py --language en model --question "This is a synthetic workshop connectivity check. Reply briefly in English."
python scripts/workshop.py --language en answer --prompt v2 --retrieval local
python scripts/workshop.py --language en workflow --pattern sequential
```

The connection-check question means: "This response checks the synthetic workshop
connection. Answer briefly in English." If a real model call fails, rehearsal has not
passed. Resolve roles, quota, and tool/Structured Outputs support before proceeding.


**What to check:** Review project, Search, and logging resources together. One successful
resource creation is not a ready environment. The participant's first model call is a separate gate.

Check only the additional modules selected:

```bash
python scripts/export_policy_docs.py --language en
python scripts/workshop.py --language en maf --tools
python scripts/workshop.py --language en maf --mcp
python scripts/workshop.py --language en workflow --pattern concurrent
python scripts/workshop.py --language en workflow --pattern group-chat
python scripts/workshop.py --language en seed-search --iq --confirm-create
python scripts/workshop.py --language en retrieve --provider iq
```

The ready learner ZIP already contains those same exported policies; an export is optional regeneration, not a missing A prerequisite.
Export and seed operations check ownership/name collisions. Do not hide rerun failures
with `--force`. Use dedicated prefixes and ownership records instead of shared objects.

### Record the actual environment

```bash
mkdir -p outputs/instructor
python -m pip freeze > outputs/instructor/environment.txt
```

Record model ID/version/SKU, Python/SDK versions, installation date, region, successful
commands, failures, remediation, and unselected features. **Upstream success is not
this edition's validation.** Never publish `.env`, tokens, personal identifiers, or raw traces.

## 5. Budget and request planning

- Lab 07 collects dev 6 + dev 6 + holdout 4 = **16 target-case requests**.
- Tools, SDK retries, reasoning, and additional comparisons consume more.
- Six candidates with two evaluators produce **12 evaluation items**, not necessarily 12 internal LLM calls.
- Search can incur SKU charges while idle.
- Hosted compute/storage costs must be checked **per active session**.
- Application Insights/Log Analytics ingestion and retention also cost money.

Default collection concurrency is one; Group Chat is capped at three rounds.
Calculate aggregate team quota. Do not promise an unsupported fixed low price.

## 6. During class

| Situation | Instructor response |
|---|---|
| A team is blocked by setup for over ten minutes | Use a preverified team environment and explicitly record account/model changes |
| No model/region quota | Use an approved prepared environment or mark live work not run |
| A's MAF environment is missing | Restore it or record "observed; not personally executed"; no portal-workflow substitute |
| IQ Preview access unavailable | GA path or design observation, labeled as different outcomes |
| SDK download unavailable | Prepared environment/browser path; never disable certificate verification |
| Baseline passes everything | Record it honestly; discuss coverage rather than manufacturing failures |
| Hosted deployment fails | Separate package/local verification; avoid repeated costly deployment attempts |

Recordings and demonstrations help learners but are not evidence of personal execution.
Explain screen/version differences when using a source video.

## Advanced Hosted workflow/evaluation preparation

Use the [evaluation workbook](reference/evaluation-workbook.md) after the basic rehearsal.
Prepare actual API support for every listed deployment, a separate judge, the intended runtime identity,
the dedicated English policy index/source/base, and App Insights query access.
The English corpus/prompts/dev/calibration/holdout are separate frozen assets selected by `--language en`.
Never reuse Korean run outcomes or rename its footage.

The local user and Hosted identity are distinct. Check account inference and Search roles separately.
Validate actual local/remote responses, not just readiness or successful package creation.
For four models, budget 24/24/16 target rows plus internal workflow/retrieval/retry/judge calls.
Preserve all failures and native findings; an all-pass baseline does not need a fabricated regression.
Keep holdout out of prompt development.

## 7. End of class and pre-Ignite freeze

- Separate real participant outputs from fixtures.
- Check all session-list pages and stop only owned active sessions.
- Use both `--new-session --new-conversation` for independent Responses checks.
- Separate team agents, Search objects, and connections from shared resources.
- Check residual service, model, log, and capacity charges.
- Update the dates in [Versions](reference/versions.md) and actual evidence in [Validation](reference/validation.md).
- Keep both languages, CLI, code, checks, and configuration tables aligned when APIs change.
- Do not add unverified Ignite 2026 announcements or future support promises.
