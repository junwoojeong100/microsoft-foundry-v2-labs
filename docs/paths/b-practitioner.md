# B. Implementation: connect models, agents, tools, knowledge and hosting

**English** | [한국어](../ko/paths/b-practitioner.md)

**Finish with 14 saved response files, a managed Prompt Agent trace lookup, a dev/holdout evaluation, a local package and a cleanup handoff.**
The 480-minute core route is best delivered as two 4-hour sessions. Deployment and C modules are not required.

## Before the first command

1. Complete [setup](../setup.md), then [Lab 00 B](../labs/00-start.md#path-b): source folder, personal notes, `.venv`, `.env`, sign-in and preflight.
2. Run each block from the repository root with `.venv` active and `--language en` intact. Never shell-`source` `.env`.
3. At each **Save** checkpoint, open the JSON before the next request. Write the filename and your finding in `session-notes.txt`'s **B - code evidence and handoff** section; keep Lab 05's detailed review in `workflow-review.txt`. `--output` saves the full response, so do not paste it into the notes again.

**Where files go:** Lab 00 prepares `outputs/learner-notes-en/` for the 14 core JSON files and your notes.
Generated evaluation runs stay in `outputs/<label>/`. B needs no browser agent or second learner ZIP.
[File inventory](../labs/11-capstone.md#b-evidence) · [Code-block rules](../labs/00-start.md#reading-code-blocks).

| First-pass decision | Use |
|---|---|
| Answer model | Prepared `gpt-6-sol`; Lab 02 verifies actual Responses and Structured Outputs, not just a token |
| Lab 03 managed agent | SDK-created Prompt Agent; invoke the exact returned immutable version |
| Lab 05 workflows | Sequential, concurrent and Group Chat |
| Lab 06 retrieval lesson | Ordinary Search, then GA IQ |
| Lab 07 prompt comparison | Local retrieval + a real Azure model, held fixed for all three collections |
| Lab 08 hosting | Package only; local serving and remote deployment **not run** |
| Lab 09 trace | Search Traces by the Lab 03 B `response_id`; local MAF runs have no server-side trace |

Lab 07 deliberately starts a local-retrieval experiment; it is not a fallback for a Lab 06 error.
File Search, hybrid/Preview IQ and cloud judges are optional.

**Cost/write boundary:** Labs 02/03/04/05/07 call the real model; Lab 03 creates a managed agent version. Lab 06 also writes owned
Search objects and may incur retrieval costs; obtain that scope's approval before starting it.
Without Search access, record Lab 06 incomplete rather than claiming the full B route.

## Core sequence

| Step | Lab | Your result |
|---|---|---|
| 1 | [Lab 00 B](../labs/00-start.md#path-b): shared setup | Environment, personal notes directory, authentication and fixture/live distinction |
| 2 | [Lab 02 B](../labs/02-models.md#path-b): model APIs | Actual response, validated structured answer, response ID and usage |
| 3 | [Lab 03 B](../labs/03-prompt-agent.md#path-b): managed Prompt Agent | `prompt-agent-create.json`, `prompt-agent-invoke.json`, exact version and response ID |
| 4 | [Lab 04 B](../labs/04-agents-tools.md#path-b): functions and MCP | Three complete JSON files saved by the commands; review each |
| 5 | [Lab 05 B](../labs/05-workflows.md#path-b): MAF workflows | Three automatically saved pattern outputs and your human review |
| 6 | [Lab 06 B](../labs/06-knowledge.md#path-b): Search and IQ | Save retrieval/answer output and `outputs/azure-objects.json` ownership |
| 7 | [Lab 07 B](../labs/07-evaluation.md#path-b): controlled evaluation | `outputs/baseline/`, `outputs/candidate/`, `outputs/final-holdout/`, including errors |
| 8 | [Lab 08 B](../labs/08-hosted.md#path-b): package only | `.build/hosted-en/package-manifest.json`; local/remote execution marked not run |
| 9 | [Lab 09 B](../labs/09-operations.md#path-b): operations and trace | Existing lineage, Prompt Agent trace lookup or unverified reason, cleanup inventory, owner and remaining costs |
| 10 | [Lab 11 B](../labs/11-capstone.md#path-b): handoff | Actual acceptance/rejection report, or an explicitly incomplete handoff with missing steps |

**Suggested split:** Day 1 covers Labs 00, 02, 03, 04 and 05. Day 2 covers Labs 06, 07, 08, 09 and 11.
Additional capability modules are **extra sessions**; do not claim the expanded course still fits that schedule without measuring it.

## Implementation extensions

<details>
<summary>Optional after the core handoff — not the next required command</summary>

The first added implementation module is a **[managed Toolbox](../labs/extensions/toolbox.md)**:
create a small approved tool collection, connect MAF, make one real call, inspect its version,
and save its evidence. Default-version changes are a separate optional exercise.
It must not be confused with the local MCP server in Lab 04.

The [OpenAPI and Code Interpreter exercises](../labs/extensions/additional-tools.md) are separate optional tool modules. They use only the supplied synthetic
source/evaluation artifacts; they do not connect company APIs or perform business actions.
Check [the capability coverage record](../coverage.md) for each module's guide, code, live and media status.
For editor setup and command compatibility, use [Developer tools](../labs/extensions/developer-toolkit.md).

</details>

## Choose the right stopping point

No Azure write approval: complete local inspection/packaging, not an inferred deployment.
No cloud judge approval: retain local business evaluation and mark native evaluation **not run**.
No Search permission: stop the Search module; do not relabel local retrieval as Search/IQ.
Do not change providers in the middle of the prompt-only comparison.
If a required gate remains blocked, use [Lab 11's incomplete handoff](../labs/11-capstone.md#incomplete-handoff)
with the existing files and exact reason. That closes the session honestly; it is **not full B completion**.

**Pause/resume:** record the last completed step and exact labels. In a new terminal,
return to the repository root and run `source .venv/bin/activate`; do not reinstall or recreate `.env`.
`evaluate`, `compare` and `accept` read saved runs locally; `collect` makes new paid calls and requires a new label.
For Lab 07, use [the saved-run restart table](../labs/07-evaluation.md#resume-evaluation) to find the next unfinished step without recollecting.
For errors, use [the recovery table](../reference/troubleshooting.md#resume-safely) before repeating a command.

**Finish:** [Lab 11](../labs/11-capstone.md#path-b).
**Choose an advanced module:** [C. Advanced](c-advanced.md).
