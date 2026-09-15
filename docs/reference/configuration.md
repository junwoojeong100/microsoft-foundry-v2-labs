# Shared configuration contract

**English** | [한국어](../ko/reference/configuration.md)

**Use one environment-variable vocabulary in this repository; do not mix names from the source workshops.**

Every CLI reads root `.env`, but existing process variables win.
Check for unexpected inherited values in old terminals.
English commands explicitly use `--language en`; existing commands default to Korean.
The language freezes prompt/corpus/dataset selection and is part of the Hosted profile.

| Setting | Used by | Contract |
|---|---|---|
| `AZURE_SUBSCRIPTION_ID` | Local CLI authentication/ARM | UUID; selects this subscription's account without changing the default |
| `AZURE_TENANT_ID` | Preauthentication check | Compared with the selected subscription's actual tenant |
| `AZURE_RESOURCE_GROUP` | Deployment verification | Actual training group |
| `AZURE_AI_ACCOUNT_NAME` | Deployment verification | Actual Foundry account |
| `AZURE_AI_PROJECT_ENDPOINT` | Model/agent/evaluation SDK | Full `/api/projects/...` endpoint |
| `AZURE_AI_MODEL_DEPLOYMENT_NAME` | Target model | Actual deployment; no automatic replacement |
| `WORKSHOP_AUTH_MODE` | Authentication | `cli` or `managed-identity` |
| `AZURE_CLIENT_ID` | Optional user-assigned managed identity | Only when needed in the actual runtime |
| `WORKSHOP_PREFIX` | Agent/Search object names | Unique `mfv2-...`, at most 32 characters |
| `WORKSHOP_MAX_OUTPUT_TOKENS` | Model output limit | Default 2048; allowed 256–8192 |
| `AZURE_SEARCH_ENDPOINT` | Search/IQ | Service root |
| `AZURE_SEARCH_INDEX_NAME` | Ordinary search/IQ sources | Default `<prefix>-policies` |
| `AZURE_SEARCH_KNOWLEDGE_SOURCE_NAME` | IQ | Default `<prefix>-source` |
| `AZURE_SEARCH_KNOWLEDGE_BASE_NAME` | IQ | Default `<prefix>-kb` |
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

`AZURE_OPENAI_ENDPOINT` is required for explicitly selected account Chat Completions or embeddings
and must belong to the same Foundry account as the project.
The IQ Chat model and its outbound Search identity are configured in the **knowledge-base model binding**.
The seed/retrieve commands do not read planner environment placeholders or automatically configure that binding.
`WORKSHOP_AUTH_MODE`/`AZURE_CLIENT_ID` select the Python caller, not the Search service identity.
See [keyless IQ model configuration](iq-model-identity.md).

`runtime-profile.json` freezes kind/pattern/retrieval/prompt/API/protocol/language.
Legacy six-field profiles mean Korean; English profiles explicitly contain `language: en`.
The runtime request remains exactly `question/model_key/case_id/run_id` and rejects reference answers or arbitrary endpoint overrides.
Keep local `.env` and azd env aligned; do not bypass managed identity with client secrets.

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
English uses separate translated dataset/prompt/corpus hashes with unchanged schema, IDs, amounts, dates, and reference judgments.
Missing English assets do not fall back to Korean. See [language bundles](../../data/README.md).
