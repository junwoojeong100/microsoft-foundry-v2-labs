# Shared configuration contract

**English** | [한국어](../ko/reference/configuration.md)

<!-- translation-pending: ko-integrated-20260915 -->

> **Translation pending** — The [Korean-first integration revision](../ko/reference/configuration.md) is current for the new workflow/evaluation curriculum. This English page retains the earlier material. English expansion and new media follow Korean execution, capture, and corrections.

**Use one environment-variable vocabulary in this repository; do not mix names from the source workshops.**

Every CLI reads root `.env`, but existing process variables win.
Check for unexpected inherited values in old terminals.

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

`AZURE_OPENAI_ENDPOINT`, `WORKSHOP_IQ_PLANNER_DEPLOYMENT`, and
`WORKSHOP_IQ_PLANNER_MODEL` are optional richer-Preview experiment settings,
unused by default GA IQ code.

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
Guide language does not change dataset/prompt hashes or response schemas.
