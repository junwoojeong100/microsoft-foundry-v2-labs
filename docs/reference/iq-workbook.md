# Foundry IQ, Toolbox, Fabric, and Work IQ workbook

**English** | [한국어](../ko/reference/iq-workbook.md)

**Checked September 15, 2026. The default workshop uses only the bundled synthetic policies.**
External connections are separate opt-in paths. This edition does not query real company, Microsoft 365, or Fabric business data.
Reading the readiness procedure is not proof that a connection works.

## 1. Complete the default IQ path in this repository

This is a reference, not a second run of Lab 06. Reuse completed steps and their evidence.
Only if the selected source has not been seeded, use the approved writer's matching working copy:

```bash
python scripts/workshop.py --language en seed-search --iq --confirm-create
```

After successful seeding, inspect retrieval and the local workflow:

```bash
python scripts/workshop.py --language en retrieve --provider iq --question "Domestic lodging and advance approval for over-limit costs in September 2026"
python scripts/workshop.py --language en workflow-agent --pattern sequential --retrieval iq --prompt v2
```

The path is **actual GA retrieval → original IDs/activity → MAF participants → validated final answer**.
Keep local CLI identity separate from remote managed identity.
For the remote IQ matrix, continue at [the evaluation workbook's preparation](evaluation-workbook.md#matrix-setup).
It builds its own explicit IQ/account-chat/Invocations profile.
Lab 08's local-retrieval Responses package is a different target, not a shortcut for this IQ run.

| Asset | Purpose | Do not confuse it with |
|---|---|---|
| Search index | Actual synthetic source documents | Service creation or successful retrieval |
| Knowledge source/base | IQ source and retrieval unit | A File Search vector store |
| References | Returned reference metadata | Numeric reference labels instead of document IDs |
| Activity | Actual retrieval processing evidence | Invented zero cost or latency |
| Context hash | Actual returned document set | Proof that a remote index never changed |

The default `2026-04-01` path uses direct intents and extractive retrieval without a KB model.
**Configuring a Chat model with managed identity is supported.**
Grant model access to the Search identity and verify model-based planning/synthesis in a separate owned base.
A missing-model form message is not an MI authentication failure.
Follow the [configuration, caller identity, and actual verification guide](iq-model-identity.md).
For that optional chat experiment, the first-pass choice is **`iq-chat` with `gpt-5.6-luna` / `2026-07-09`, Search SMI, `low` and `answerSynthesis`**,
separate from the `gpt-6-sol` answer model (Search accepted no GPT-6 model on September 23, 2026).
Use [the prepared setup sequence](../setup.md#4-environment-owner-checklist); it creates a separate base and does not change the GA workflow/evaluation target above.

## 2. Choose hybrid and IQ explicitly

[Lab 06](../labs/06-knowledge.md)'s hybrid path uses actual embeddings and a text/vector query.
`search` remains keyword search and `iq` remains knowledge-base retrieval.
No provider replaces another after an error.

A retrieval comparison is a **separate experiment** that freezes data, questions, model, and prompt.
Inspect actual evidence and costs/latency.
Creating a vector index does not prove that IQ used those vectors.

## 3. Optional managed Toolbox and Microsoft Learn

For the **executable synthetic-policy Toolbox**, follow [the Toolbox lab](../labs/extensions/toolbox.md).
The older Microsoft Learn example below is an optional documentation-tool pattern, not its prerequisite.

<details>
<summary>Optional documentation-tool integration reference — not another policy-tool exercise</summary>

**Only an instructor with approved connections should proceed.**
The synthetic policy task does not need the public web, so no external toolbox is automatically attached.
Use an approved source such as Microsoft Learn for separate platform-documentation questions.

1. Choose a dedicated toolbox in the current project's Tools/Toolbox area.
2. Connect only approved read-only servers. Verify the real server and permissions, not merely a read-only-looking name.
3. Do not include Work IQ, Graph, booking, mail, or payment actions in this workshop toolbox.
4. Record the actual returned MCP endpoint and tool list.
5. Verify caller access to Foundry separately from the upstream server-side connection authentication.
6. Inspect actual tool calls/results/errors in traces. `tools/list` alone is not answer-quality validation.

The September 15 Python contract uses `agent_framework.foundry.FoundryToolbox`.
It comes from the prerelease hosting package and does not create the underlying project connection.

```text
https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/<name>/mcp?api-version=v1
```

The following **integration pattern assumes an already approved client, credential, and endpoint**.
It is not a ready-to-run authorization bypass.

```python
from agent_framework import Agent
from agent_framework.foundry import FoundryToolbox
from agent_framework_foundry_hosting import ResponsesHostServer

toolbox = FoundryToolbox(credential, url=approved_toolbox_endpoint, load_prompts=False)
agent = Agent(
    client=client,
    name="ApprovedDocumentationGuide",
    instructions="Explain platform concepts using approved official documentation. Do not infer company policy.",
    tools=[toolbox],
    default_options={"store": False},
)
server = ResponsesHostServer(agent)
```

The host manages the Agent/MCP connection lifecycle.
Never paste bearer tokens into code or `.env`.
For a managed `FoundryAgent`, attach the toolbox to the stored **agent definition**;
adding a local client object does not modify the remote agent.
Follow the current [Toolbox contract](https://learn.microsoft.com/agent-framework/integrations/by-component/tools/foundry-toolbox)
and [Hosted connection guide](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/use-toolbox-hosted-agent).

</details>

## 4. Fabric IQ: authentication depends on the asset

Prepare a synthetic-only workspace, approved capacity, the actual published asset type/ID, minimum read permissions,
and explicit tenant/network/region/retention/cost/cleanup ownership.

The September 15 [official guide](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/fabric-iq) distinguishes:

| Asset | Authentication boundary |
|---|---|
| Ontology / Power BI semantic model | Delegated user/OBO context |
| Published Fabric Data Agent MCP | That endpoint may support user or service-principal tokens |
| Direct Data Agent MCP | Verify the documented `https://api.fabric.microsoft.com/.default` scope and actual identity permissions |

Do not generalize Data Agent MCP's app-only support to every Fabric IQ source.
One administrator's successful call does not establish every user's permissions.
In an approved separate session: prepare the asset, configure the connection, ask a first question with the intended identity,
verify source/aggregation semantics, test a lower-privilege denial, and restore connections/cost settings.
Capacity preparation is outside the workshop timing.

## 5. Work IQ is not connected by default

The default never accesses Microsoft 365.
For a separately approved project, administrators must check current
[Work IQ knowledge-source requirements](https://learn.microsoft.com/azure/search/agentic-knowledge-source-how-to-work-iq).

The September 15 requirements include:

1. A Copilot Studio usage-based billing plan and **per-user assignment**.
2. Tenant Work IQ enablement and required administrator actions.
3. A client that signs in users and sends user assertions.
4. `WorkIQAgent.Ask` delegated permission and required consent.
5. The `2026-08-01-preview` customer-owned Entra application/federated-credential contract.

`applicationId` is the application client ID. `federatedCredentialId` is the **credential object ID**, not its name or Search principal ID.
Check current same/cross-tenant rules rather than copying an old same-tenant example as a universal limit.
Never work around authentication by storing a client secret on the source or in `.env`.

Without approval, record **not executed**.
Do not replace an error with synthetic output and label it a real Work IQ success.
Older references to “synthetic fallback” are treated here only as a **separately labeled synthetic design exercise**.

## 6. Hosted identity/OBO checklist

| Check | Required evidence |
|---|---|
| Actual caller | The user/workload identity required by this service |
| Audience | Whether the token is for Foundry, Search, Fabric, or Work IQ |
| Access boundary | Appropriate differences for authorized and lower-privilege users |
| Propagation | Actual identity propagation locally and remotely |
| Recording | Content capture, sensitive-data policy, retention, and readers |
| Restore | Owners of consent, connections, capacity, billing, and cleanup |

This checklist does not automatically implement impersonation.
A host managed identity cannot replace required user context.
Never work around consent, authentication, or networking by silently changing account or source.

## 7. Evaluate and clean up

Evaluate IQ-backed Hosted answers using the [same-target evaluation workbook](evaluation-workbook.md).
Do not combine platform-documentation, policy, Fabric-aggregation, and Work IQ collaboration tasks into an unexplained score.
Preserve tools, sources, dates, identities, and actual evaluator inputs.

Restore only owned workshop connections; never delete organizational consent or another team's capacity.
Record disabled/unexecuted features and remaining costs.
Claiming these optional paths replace the old curricula requires their separate [live acceptance gates](consolidation.md).
