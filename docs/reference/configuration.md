# Shared configuration contract

**English** | [한국어](../ko/reference/configuration.md)

**Use one environment-variable vocabulary in this repository; do not mix names from the source workshops.**

Commands that need cloud configuration read root `.env`, but existing process variables win.
Offline `doctor`, `demo`, local `retrieve`, and saved-run `evaluate`/`compare`/`accept`/`feedback`/`cleanup-plan`
do not load that file. An offline PASS does not validate the values you entered.
Check for unexpected inherited values in old terminals.
English commands explicitly use `--language en`; existing commands default to Korean.
The language freezes prompt/corpus/dataset selection and is part of the Hosted profile.

## Fill only what your current lab needs

Use the numbered sections of [`.env.example`](../../.env.example), not a recording or an old `azure.yaml`.

| Current step | Fill / keep |
|---|---|
| Offline rehearsal | Nothing; these commands do not load `.env` |
| First live model, MAF and local-retrieval evaluation | Section 1's verified setup-card values; keep `WORKSHOP_AUTH_MODE=cli` and output limit 2048 |
| Core B Search/IQ in Lab 06 | Also section 2's `AZURE_SEARCH_ENDPOINT`; default names use your prefix |
| Optional IQ Chat, hybrid, Toolbox, Hosted or cloud judge | Only the additional settings named by that selected module |

Invalid UUIDs and token limits report the **setting name**, not just a parser error.
Correct that field; do not change an unrelated deployment or identity.
The source-root `azure.yaml`, `.azure/` and `.env` are ignored personal state, not distributed workshop defaults.
Hosted helpers generate a separate project from verified settings. Local matrix smoke requires an explicit `--azd-directory`.

## Setting lookup

| Setting | Used by | Contract |
|---|---|---|
| `AZURE_SUBSCRIPTION_ID` | Local CLI authentication/ARM | UUID; selects this subscription's account without changing the default |
| `AZURE_TENANT_ID` | Preauthentication check | Compared with the selected subscription's actual tenant |
| `AZURE_RESOURCE_GROUP` | Deployment verification | Actual training group |
| `AZURE_AI_ACCOUNT_NAME` | Deployment verification | Actual Foundry account |
| `AZURE_AI_PROJECT_ENDPOINT` | Model/agent/evaluation SDK | Full `/api/projects/...` endpoint |
| `AZURE_AI_MODEL_DEPLOYMENT_NAME` | Target model | Template default `gpt-6-sol`; prepare the real deployment first. No automatic replacement |
| `WORKSHOP_AUTH_MODE` | Authentication | `cli` or `managed-identity` |
| `AZURE_CLIENT_ID` | Optional user-assigned managed identity | Only when needed in the actual runtime |
| `WORKSHOP_PREFIX` | Agent/Search object names | Must start with `mfv2-`; lowercase letters/digits separated by single hyphens, no trailing hyphen, at most 32 characters in total |
| `WORKSHOP_MAX_OUTPUT_TOKENS` | Model output limit | Default 2048; allowed 256–8192 |
| `AZURE_SEARCH_ENDPOINT` | Search/IQ | Service root |
| `AZURE_SEARCH_RESOURCE_GROUP` | `iq-chat check` ARM lookup | Optional; defaults to `AZURE_RESOURCE_GROUP` when Search is in the same group |
| `AZURE_SEARCH_INDEX_NAME` | Ordinary search/IQ sources | Default `<prefix>-policies` |
| `AZURE_SEARCH_KNOWLEDGE_SOURCE_NAME` | IQ | Default `<prefix>-source` |
| `AZURE_SEARCH_KNOWLEDGE_BASE_NAME` | IQ | Default `<prefix>-kb` |
| `AZURE_SEARCH_CHAT_KNOWLEDGE_BASE_NAME` | Optional IQ Chat preset | Separate owned base; default `<prefix>-chat-en-kb` for English or `<prefix>-chat-ko-kb` for Korean |
| `TOOLBOX_SEARCH_CONNECTION_NAME` | Optional managed Toolbox | Owner-prepared keyless CognitiveSearch connection in the same project |
| `TOOLBOX_NAME` | Optional managed Toolbox | Default `<prefix>-tools-<language>`; existing unowned names are rejected |
| `AZURE_AI_EVALUATION_MODEL_DEPLOYMENT_NAME` | Cloud judge | Explicitly separate from target |
| `WORKSHOP_MODEL_DEPLOYMENTS_JSON` | Hosted matrix | 1–8 explicit unique key/deployment pairs; no model substitution |
| `WORKSHOP_HOSTED_AGENT_NAME` | Hosted matrix | Exact approved agent name |
| `WORKSHOP_HOSTED_AGENT_VERSION` | Hosted matrix | Actual fixed numeric version, never `latest` |
| `WORKSHOP_HOSTED_AGENT_ENDPOINT` | Hosted matrix | Full returned Invocations endpoint, including API version |
| `AZURE_APPLICATION_INSIGHTS_APP_ID` | Matrix traces | Connected application ID, not workspace ID or instrumentation key |
| `AZURE_AI_EMBEDDING_DEPLOYMENT_NAME` | Hybrid | Verified actual embedding deployment |
| `WORKSHOP_EMBEDDING_DIMENSIONS` | Hybrid | Actual returned dimensions; no truncation or zero padding |
| `WORKSHOP_EMBEDDING_API` | Hybrid | Explicit `project`/`account`; failures never switch it |
| `WORKSHOP_IQ_RERANKER_THRESHOLD` | IQ retrieval | Optional finite 0–4 filter; empty retains the service default. This is not an evaluator threshold |

`AZURE_OPENAI_ENDPOINT` is required for explicitly selected account Chat Completions, embeddings, or `iq-chat`
and must belong to the same Foundry account as the project.
The IQ Chat model and its outbound Search identity are configured in the **knowledge-base model binding**.
The seed/retrieve commands do not read planner environment placeholders or automatically configure that binding.
`WORKSHOP_AUTH_MODE`/`AZURE_CLIENT_ID` select the Python caller, not the Search service identity.
See [keyless IQ model configuration](iq-model-identity.md).

**September 15, 2026 IQ Chat preset:** deployment/model `gpt-5.6-luna`, underlying version `2026-07-09`,
Search **system-assigned** identity, `2026-08-01-preview`, `low`, `answerSynthesis`.
Changing the answer deployment does not change this preset: on September 23, 2026 Search accepted no GPT-6 model for KB binding. `iq-chat check` verifies its actual deployment, source and documented role;
`setup` requires the matching local source/corpus ownership ledger. Neither modifies the default GA base.
The new chat-base name must start with your prefix. [Setup sequence](../setup.md#4-environment-owner-checklist).

`runtime-profile.json` freezes kind/pattern/retrieval/prompt/API/protocol/language.
Legacy six-field profiles mean Korean; English profiles explicitly contain `language: en`.
The runtime request remains exactly `question/model_key/case_id/run_id` and rejects reference answers or arbitrary endpoint overrides.
Keep local `.env` and azd env aligned; do not bypass managed identity with client secrets.

<a id="workspace-scope"></a>

## One Search-owning copy, one prefix, one language

`--language en` selects English data; it **does not rename Search objects or select another `.env`**.
Blank Search names still resolve to `<prefix>-policies`, `<prefix>-source` and `<prefix>-kb` in either language.
Use distinct prefixes such as `mfv2-team01-en-0917` and `mfv2-team01-ko-0917` when preparing both languages.

| Change | Safe preparation |
|---|---|
| Repeat a model/dev run with the same language and scope | Use new run labels; keep the Search ownership ledger |
| Change language for local-only retrieval or model evaluation, without owned Search objects | Use a new label set and the correct language bundle; translated data is not the same-input comparison |
| Change language, Search service or prefix after seeding | Use a fresh source copy with a reviewed `.env`, new owned names and new run labels; preserve the old copy and its cleanup ledger |
| Use instructor-prepared objects | Use the authorized prepared working copy with its matching language/scope/ledger, or run only the explicitly selected read-only exercise |
| An object exists but this copy has no matching ledger | Do not seed over it or copy/fabricate another team's ledger; have the owner resolve it or prepare a new copy/prefix |

`outputs/azure-objects.json` is bound to the Search endpoint, prefix and corpus hash.
Changing only a label or only `WORKSHOP_PREFIX` cannot reset it. Do not delete or edit the ledger to bypass a refusal.
When starting a fresh copy, leave the original results available for the original owner's cleanup.

## Previous names

| Name in a source workshop | Name here |
|---|---|
| `PROJECT_ENDPOINT`, `FOUNDRY_PROJECT_ENDPOINT` | `AZURE_AI_PROJECT_ENDPOINT` |
| `MODEL_DEPLOYMENT_NAME`, `FOUNDRY_MODEL` | `AZURE_AI_MODEL_DEPLOYMENT_NAME` |
| `LAB_PREFIX` | `WORKSHOP_PREFIX` |
| `LAB_AUTH_MODE` | `WORKSHOP_AUTH_MODE` |

There are no automatic aliases/fallbacks. An explicit typo failure is safer than
connecting to a different project. Authentication stays pinned to the configured
subscription even when several accounts are signed in.
`--tenant` alone can select a different default account; Azure CLI does not accept
`--tenant` and `--subscription` together for this token selection, so tenant is verified first.

## Data and output

Synthetic policy fields: `id`, `title`, `content`, `effective_from`, `effective_to`.
Answer fields: `answer`, `decision`, `limit_krw`, `citations`.
`limit_krw` is the applicable **limit**, not actual spending; no evidence means `null`.

`decision` is one of `answer`, `needs_approval`, or `insufficient_evidence`.
The code does not silently correct an amount. Invalid JSON, duplicate keys, and wrong
types are rejected.

Runs live under `outputs/<label>/`; a label is a restricted name, not a path.
Existing run directories are not overwritten. Manifest hashes aid reproduction but
are not digital signatures or tamper-proof storage.
Interactive commands can also [save their complete JSON with `--output`](commands.md#saving-json).
That file does not replace a batch manifest or an Azure ownership ledger.
English uses separate translated dataset/prompt/corpus hashes with unchanged schema, IDs, amounts, dates, and reference judgments.
Missing English assets do not fall back to Korean. See [language bundles](../../data/README.md).
