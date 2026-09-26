# Beginner glossary

**English** | [한국어](../ko/reference/glossary.md)

| Term | One-line explanation |
|---|---|
| Tenant/directory | Boundary managing an organization's accounts and identities |
| Subscription | Azure resource, billing, and administration unit |
| Resource group | Management container for related Azure resources |
| Endpoint | Service address to which a program sends requests |
| Deployment name | Name used to invoke a deployed model |
| Stable agent endpoint / active version | A Foundry agent has a stable endpoint; the active version receives traffic until changed |
| Prefix | Your `mfv2-...` naming boundary for owned cloud objects; not a run label |
| Label | A name for one saved run, such as `baseline`; not an agent name, version or file path |
| Model key | A local alias such as `a` for one explicitly configured deployment in a matrix |
| SDK | Programming library for working with a service |
| CLI/terminal | Interface for entering commands and running tools |
| Virtual environment/venv | Project-specific isolated Python packages |
| `.env` | Configuration file; this lab stores no secrets in it |
| JSON/JSONL | Structured data / one JSON object per line |
| Prompt/instructions | A model request / business rules an agent follows |
| Prompt Agent | Foundry-managed model/instructions agent; Lab 03 creates it through [A's portal](../labs/03-prompt-agent.md#path-a) or [B's SDK](../labs/03-prompt-agent.md#path-b) |
| MAF (Microsoft Agent Framework) | Framework for agents and workflows; [Lab 04](../labs/04-agents-tools.md#path-b) runs the agent in local Python while calling the model in Azure |
| Hosted agent | Custom agent code hosted by Foundry; [Lab 08 B](../labs/08-hosted.md#path-b) only builds its local package, not a deployment |
| Tool | Function/API requested by the model and executed by the application |
| MCP | Standard protocol between model/agent clients and tool servers |
| RAG | Retrieve relevant material before generating a grounded answer |
| Grounding | Connecting an answer to actual evidence |
| Citation | Original source location or document identifier |
| Knowledge source/base | IQ retrieval source / collection searched together |
| Managed identity | Azure-managed runtime identity instead of a password |
| OBO/delegated | Access to another service in an end user's permission context |
| Trace/span | Request execution flow / one operation within it |
| Server-side vs client-side tracing | Server-side traces appear after the project is connected to Application Insights; client-side tracing is separate instrumentation in the caller process |
| Insights in Foundry (preview) | Preview portal analysis that scans recent agent traces, groups recurring behavior and suggests likely causes/actions for human review |
| Evaluation/evaluator | Assessment against criteria / its rules or model |
| Dev/holdout | Cases for development/selection / cases reserved until final acceptance |
| Lineage | Links showing which data, instructions, models, and versions produced a result |
| Manifest / hash | An inventory of inputs/settings / a fingerprint used to detect changed bytes; neither proves model quality |
| Fixture | Predefined checker data, not a fresh LLM result |
| GA/Preview | Generally available / availability with separate limits and possible change |
| Session | Hosted persistent-state/compute unit with costs and cleanup requirements |

You do not need to know every term before starting. Return to the lab or page that linked you here;
if you are starting fresh, choose [A or B](../paths.md).
