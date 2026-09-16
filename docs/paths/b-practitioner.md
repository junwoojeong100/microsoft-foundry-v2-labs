# B. Implementation: connect models, tools, knowledge and hosting

**English** | [한국어](../ko/paths/b-practitioner.md)

**Use one repository, one language and one set of verified values.**
B builds the executable system. C adds independent advanced capabilities; it is not the mandatory next command after every B lab.

## Before the first command

Complete [Lab 00 B](../labs/00-start.md#b-code-one-folder-one-environment), including participant sign-in,
`.env`, the activated environment and read-only preflight. A successful token is not a successful model request:
finish Lab 02's actual Responses and structured-answer checks.

Run code blocks from the repository root. Never shell-`source` `.env`.
Preserve the explicit English `--language en` flag and use a fresh label for each new collection.

## Core sequence

| Step | Lab | Your result |
|---|---|---|
| 1 | [00. Shared setup](../labs/00-start.md) | Environment, authentication and fixture/live distinction |
| 2 | [02. Model APIs](../labs/02-models.md) | Actual response, validated structured answer, response ID and usage |
| 3 | [04. Functions and MCP](../labs/04-agents-tools.md) | No-tool/function/MCP outputs with their real execution paths |
| 4 | [05. MAF workflows](../labs/05-workflows.md) | Sequential/concurrent/group-chat results and a human review |
| 5 | [06. Search and IQ](../labs/06-knowledge.md) | Original document IDs, retrieval activity and evidence hashes |
| 6 | [07. Controlled evaluation](../labs/07-evaluation.md) | Baseline/candidate, errors, review and frozen final acceptance |
| 7 | [08. Hosted basics](../labs/08-hosted.md) | Package, local response and approved remote work reported separately |
| 8 | [09. Operations](../labs/09-operations.md) → [11. Handoff](../labs/11-capstone.md) | Reproducible records and ownership-aware cleanup |

The original prepared B sequence is six hours. Additional capability modules are **extra sessions**;
do not claim the expanded course still fits that schedule without measuring it.

## Implementation extensions

The first added implementation module is a **[managed Toolbox](../labs/extensions/toolbox.md)**:
create a small approved tool collection, connect MAF, make one real call, inspect its version,
and demonstrate controlled default-version changes. It must not be confused with the local MCP server in Lab 04.

The [OpenAPI and Code Interpreter exercises](../labs/extensions/additional-tools.md) are separate optional tool modules. They use only the supplied synthetic
source/evaluation artifacts; they do not connect company APIs or perform business actions.
Check [the capability coverage record](../coverage.md) for each module's guide, code, live and media status.
For editor setup and command compatibility, use [Developer tools](../labs/extensions/developer-toolkit.md).

## Choose the right stopping point

No Azure write approval: complete local inspection/packaging, not an inferred deployment.
No cloud judge approval: retain local business evaluation and mark native evaluation **not run**.
No Search permission: stop the Search module; do not relabel local retrieval as Search/IQ.
Do not change providers in the middle of the prompt-only comparison.

**Finish:** [Lab 11](../labs/11-capstone.md).
**Choose an advanced module:** [C. Advanced](c-advanced.md).
