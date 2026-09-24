# B. Implementation: connect models, tools, knowledge and hosting

**English** | [한국어](../ko/paths/b-practitioner.md)

**Use one repository, one language and one set of verified values.**
B builds the executable system. C adds independent advanced capabilities; it is not the mandatory next command after every B lab.

## Before the first command

Start at [Lab 00 B](../labs/00-start.md#path-b), including participant sign-in,
`.env`, the activated environment and read-only preflight. A successful token is not a successful model request:
finish Lab 02's actual Responses and structured-answer checks.

Run code blocks from the repository root. Never shell-`source` `.env`.
Preserve the explicit English `--language en` flag and use a fresh label for each new collection.
Lab 00 creates **`outputs/learner-notes-en/`** from the source copy's blank worksheets.
Use it for terminal-output files and review notes; no browser agent or separate learner ZIP is required for B.
Generated evaluation folders remain at `outputs/<label>/`, not inside the notes directory.
Use [the code-block rules](../labs/00-start.md#reading-code-blocks) if a block asks for values.
The core commands save all **12 response JSON files** through `--output`; no terminal-output copying is required.
Open each file at its **Save** checkpoint before the next request, and write your human review separately;
[Lab 11's file inventory](../labs/11-capstone.md#b-evidence) lists everything needed at handoff.

**First-pass choices are already made:** `gpt-6-sol`; all three introductory MAF patterns;
GA Search/IQ in Lab 06; **local retrieval + a real Azure model** for Lab 07; **package only** in Lab 08.
Changing from Lab 06's retrieval lesson to Lab 07's declared local experiment is deliberate, not an IQ-error fallback.
File Search, hybrid/Preview IQ, cloud judges, local Hosted serving and remote deployment are not core steps.

**Cost/write boundary:** Labs 02/04/05/07 call the real model. Lab 06 also writes owned
Search objects and may incur retrieval costs; obtain that scope's approval before starting it.
Without Search access, record Lab 06 incomplete rather than claiming the full B route.

## Core sequence

| Step | Lab | Your result |
|---|---|---|
| 1 | [Lab 00 B](../labs/00-start.md#path-b): shared setup | Environment, personal notes directory, authentication and fixture/live distinction |
| 2 | [Lab 02 B](../labs/02-models.md#path-b): model APIs | Actual response, validated structured answer, response ID and usage |
| 3 | [Lab 04 B](../labs/04-agents-tools.md#path-b): functions and MCP | Three complete JSON files saved by the commands; review each |
| 4 | [Lab 05 B](../labs/05-workflows.md#path-b): MAF workflows | Three automatically saved pattern outputs and your human review |
| 5 | [Lab 06 B](../labs/06-knowledge.md#path-b): Search and IQ | Save retrieval/answer output and `outputs/azure-objects.json` ownership |
| 6 | [Lab 07 B](../labs/07-evaluation.md#path-b): controlled evaluation | `outputs/baseline/`, `outputs/candidate/`, `outputs/final-holdout/`, including errors |
| 7 | [Lab 08 B](../labs/08-hosted.md#path-b): package only | `.build/hosted-en/package-manifest.json`; local/remote execution marked not run |
| 8 | [Lab 09 B](../labs/09-operations.md#path-b): operations | Existing lineage, cleanup inventory, owner and remaining costs |
| 9 | [Lab 11 B](../labs/11-capstone.md#path-b): handoff | Actual acceptance/rejection report, or an explicitly incomplete handoff with missing steps |

The original prepared B sequence is six hours. Additional capability modules are **extra sessions**;
do not claim the expanded course still fits that schedule without measuring it.

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
