# Capability coverage and evidence boundaries

**English** | [한국어](ko/coverage.md)

**English-first extension execution — September 16, 2026 (earlier `gpt-5.6-luna` preset).**
The September 24, 2026 `gpt-6-sol` recording re-ran the main A/B steps of Labs 00–09 and 11 together with the optional
Foundry evaluation steps (portal and trace evaluation, business rubric with **Compare runs**, MAF tool-call scoring); the earlier
recordings were removed. On September 23, separate verifications ran the optional evaluation steps, the conversation
evaluation module, the existing-traces and recurring evaluations, Agent Optimizer, cloud red teaming and the approved Hosted release
with `gpt-6-sol`; the other extension evidence below was not re-run with `gpt-6-sol`.
This page is a coverage record, not a claim that every Foundry feature has been executed.
The production order is English guide → English recording → English refinement → Korean guide →
independent Korean recording → Korean refinement.

## Read the status honestly

| Status | Meaning |
|---|---|
| Existing lab | Executable guidance already exists; use the linked validation record for the exact historical scope |
| In preparation | Additional guide/code is being authored; no new live or media completion claim |
| Live verified | A dated, versioned response and required source/error/usage evidence exist for this edition |
| Recorded | Actual action/video/source-frame records exist; a screenshot alone is not execution |
| Design only | Architecture or prerequisite review; no service connection is claimed |
| Not run / blocked | Required approval, access, feature availability or data is absent |

GA/Preview is a **product property**, not one of these completion states.
An installed prerelease SDK does not make the entire service Preview; a GA service does not make all SDKs or tool modes GA.

## Current course map

| Capability | Path | Current workshop coverage | September 16 expansion |
|---|---|---|---|
| Models, Prompt Agents, synthetic source evidence | A/B | Existing Labs 00–03 | Preserve the fixed first-pass model and simplify navigation |
| Functions, local MCP, MAF orchestration | B | Existing Labs 04–05 | Preserve the executable patterns and their limits |
| Search/hybrid/GA IQ and separate MI chat preset | B/C | Existing Lab 06 and keyless preset | Keep GA and Preview planning/synthesis separate |
| Business/native evaluation and frozen acceptance | A/B | Existing Lab 07, plus optional portal evaluation, no-evidence diagnostic, code-based business evaluator and **Compare runs** | September 24 `gpt-6-sol` recording and September 23 verification in both languages ([results](live-run.md)); custom evaluators and TaskAdherence are Preview |
| Tool-call evaluation of the MAF agent | B | Optional `maf-evaluate` in Lab 04 | September 24 `gpt-6-sol` recording and September 23 verification in both languages; experimental MAF evaluation API |
| Hosted workflow/matrix/calibration/regression/traces | C | Existing workbook | Preserve historical evidence; new code needs new run labels |
| Managed Toolbox lifecycle | B | Executable owned/versioned path | English direct query, MAF, local/remote Hosted and downloaded evidence verified |
| Tool Search, Skills and private skill catalog | C | Executable Tool Search/Skill path | English discovery, pinning, exact Skill readback and actual load verified; catalog infrastructure not provisioned |
| Full-conversation evaluation and reusable datasets | C | Executable dev-only multi-turn path | Re-verified with `gpt-6-sol` on September 23 in both languages; both native levels ran |
| Agent Optimizer | C | One bounded Prompt Agent wizard | Re-run with `gpt-6-sol` on September 23 in both languages with a temporary `gpt-5.5` optimizer model: baseline only; Groundedness compared each answer with itself, so no promotion |
| Durable human approval, restart recovery and steering | C | Real local SDK demonstration | English restart/checkpoint proof with simulated decisions; not actual human authorization |
| A2A 1.0 | C | Explicit card/configuration and delegation | English original paired call/output verified; wire packets not captured |
| Memory and Routines | C | Owned lifecycle and bounded timer | Memory verified; routine delivery verified, answer retrieval unavailable |
| Applied guardrails and controlled red teaming | C | Dedicated policy/target | English attachment and two unblocked cases recorded (earlier preset). Cloud red-team scans (Preview) ran with `gpt-6-sol` on September 23; the displayed ASR contradicted every row's reasoning, so no red-team result is claimed |
| Continuous evaluation and deployment quality gates | C | Manual guarded workflow and OIDC setup | September 23 `gpt-6-sol`: English and Korean OIDC releases passed the six-case business gate; existing-traces evaluations scored 15/15 per evaluator in both languages; an hourly recurring schedule was verified and paused ([results](live-run.md#previously-not-run-items--september-23-2026)); production approval remains separate |
| Model retirement/migration and Router tradeoffs | C | Fixed-model comparison and Router observation | Temporary supported optimizer model and frozen version recorded; no Router migration claim |
| OpenAPI/Code Interpreter, Toolkit, governance/networking | B/C | Executable tools and explicit owner boundaries | English API/file results, tooling and scoped role checks recorded; private network not tested |
| Actual company/Microsoft 365 access | Specialist | Excluded | Remains excluded |
| Fine-tuning, voice/multimodal, browser/computer business actions | Specialist | Design/scope only | Separate specialist curriculum, not an implied implementation |

## Evidence that already exists

The [September 24 `gpt-6-sol` execution](live-run.md), its [recordings](video-summary.md) and the
[validation scope](reference/validation.md) keep their own dates, code versions and results.
The September 24 recording is not relabeled as an execution of the extension modules.
The September 16 extension results and videos (earlier `gpt-5.6-luna` preset) were removed from the working tree;
the dated outcomes in the table above remain historical notes, not evidence for `gpt-6-sol`.

New evidence must identify the language, source commit/package, actual model and agent version,
question/dataset/corpus/evaluator hashes, all responses and failures, and resource cleanup state.
Record requests and actual source activity, not a recreated success screen.
Authentication, passwords, tokens and MFA interactions are excluded from recordings.

## Straightforwardness acceptance

Every runnable module must have one recommended first pass, exact input files/values, complete commands,
an observable completion criterion, a stop/recovery path, and an explicit next link.
Optional alternatives follow the first success rather than competing with it.
Costs, roles and feature access appear **before** the first side-effecting command.

Do not mark a module complete because documentation links work or a fixture passes.
Read-only checks, real model calls, local-only demonstrations, Preview service execution and recorded actions are reported separately.
