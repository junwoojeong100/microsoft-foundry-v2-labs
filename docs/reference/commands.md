# Command quick reference

**English** | [한국어](../ko/reference/commands.md)

**Run all commands from the repository root. Do not shell-`source` `.env`.**
Activate the dedicated virtual environment for cloud SDKs.

| Command | Azure/side effects | Purpose |
|---|---|---|
| `python scripts/workshop.py doctor` | None | Python/synthetic-data checks |
| `doctor --cloud` | Read-only | Explicit subscription/tenant/deployment/token preflight, not inference |
| `demo --label demo-v2 --prompt v2` | Local output only | Fixed fixture |
| `retrieve --provider local` | None | Local keyword search |
| `retrieve --provider search` | Possible Search charges | Ordinary search |
| `retrieve --provider iq` | Possible IQ charges | GA knowledge-base retrieval |
| `model --question "question"` | Paid model call | Direct Responses |
| `answer --prompt v2 --retrieval local` | Paid model call | Structured answer with sources |
| `maf --tools` / `maf --mcp` | Paid model calls | Read-only function / local MCP |
| `workflow --pattern sequential` | Paid model calls | Alternatives: concurrent, group-chat |
| `seed-search --confirm-create` | Creates/uploads owned Search objects | Existing service only |
| `seed-search --iq --confirm-create` | Above plus GA source/base | Ownership checks |
| `prompt-agent create ... --confirm-create` | Creates an actual agent version | Exact prefix required |
| `prompt-agent invoke ... --version ...` | Calls a real agent | Explicit version |
| `collect --label baseline --prompt v1` | Paid calls for all dev cases | Preserves errors; concurrency one |
| `evaluate --label baseline` | None | Deterministic business checks |
| `compare --baseline baseline --candidate candidate` | None | Controlled dev comparison |
| `feedback --label baseline --case D03 --reason "specific review reason"` | Local review record | Real dev only; pending approval |
| `cloud-evaluate --label candidate --confirm-cost` | Paid cloud judge | Evaluator version and job lineage |
| `collect --split holdout ... --candidate candidate --unlock-holdout` | Frozen candidate's actual final requests | No reuse for development |
| `accept --candidate candidate --holdout final-holdout` | None | Human acceptance evidence, not automatic approval |
| `serve` | Local server; paid model on invocation | Hosted SDK needed |
| `cleanup-plan` | None | Deletes nothing |
| `python scripts/export_policy_docs.py` | Creates six local text files | Instructor distributes them to A learners |
| `python scripts/package_hosted.py` | Local package | No deployment/installation |
| `python scripts/play_recordings.py` | Localhost video server | Verified guide-ordered default with Lab 00–11 chapters; individual videos selectable; no Azure/upload |

Abbreviated rows are not complete executable examples. Read
`python scripts/workshop.py --help` and subcommand `--help` for required arguments.
Full commands appear in the [labs](../paths.md).

Add `--debug` before a subcommand for local diagnostics. Stack/service errors can
contain environment paths; do not publish raw logs.
Commands do not overwrite existing run labels. Never alter raw responses or scores
to bypass hash verification.

Both language editions use identical CLI options and canonical policy inputs.
See [Languages](languages.md) before translating a retrieval or evaluation question.
