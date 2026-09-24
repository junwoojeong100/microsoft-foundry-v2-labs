# Capability coverage and evidence boundaries

**English** | [한국어](ko/coverage.md)

**Current state:** the September 24, 2026 `gpt-6-sol` recording covers the main A/B steps of Labs 00–09 and 11 and the
optional Foundry evaluation steps (portal and trace evaluation, business rubric with **Compare runs**, MAF tool-call scoring).
Separate September 23 `gpt-6-sol` checks cover the conversation evaluation module, the existing-traces and recurring
evaluations, Agent Optimizer, cloud red teaming and the approved Hosted release. The other extension results below date from
September 16, 2026 (earlier `gpt-5.6-luna` preset) and are not evidence for `gpt-6-sol`.
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

| Capability | Path | Current workshop coverage | Latest dated evidence |
|---|---|---|---|
| Models, Prompt Agents, synthetic source evidence | A/B | Existing Labs 00–03 | 2026-09-24 `gpt-6-sol` recording |
| Managed prompt agent as core route | B | Lab 03 B now treats the managed Prompt Agent as core practitioner work | 2026-09-24 live-verified in English and Korean with the refreshed pins (create, exact-version invoke, trace); no recording |
| Functions, local MCP, MAF orchestration | B | Existing Labs 04–05 | 2026-09-24 `gpt-6-sol` recording |
| Browser option for A Lab 05 | A | Optional owner-prepared Hosted workflow agent can be tested in the portal Playground | 2026-09-24: the workflow agent answered one local Responses request; remote deployment and Playground use not run |
| Search/hybrid/GA IQ and separate MI chat preset | B/C | Existing Lab 06 and keyless preset | 2026-09-24 `gpt-6-sol` recording: local, Search and GA IQ retrieval. Hybrid RAG and the `gpt-5.6-luna` IQ Chat preset not re-run (configuration screen checked 2026-09-17) |
| Business/native evaluation and frozen acceptance | A/B | Existing Lab 07, plus optional portal evaluation, no-evidence diagnostic, code-based business evaluator and **Compare runs** | 2026-09-24 `gpt-6-sol` recording and 2026-09-23 verification in both languages ([results](live-run.md)); custom evaluators and TaskAdherence are Preview |
| Tool-call evaluation of the MAF agent | B | Optional `maf-evaluate` in Lab 04 | 2026-09-24 `gpt-6-sol` recording and 2026-09-23 verification in both languages; experimental MAF evaluation API |
| Trace check as core evidence | A/B | Lab 09 A/B records actual trace evidence or an explicit unverified reason | 2026-09-24: managed agent traces found by response ID in Application Insights (English and Korean); portal search not re-recorded |
| Standalone SDK recipes | B/C | Minimal offline recipe files for model, prompt-agent, MAF, IQ and Hosted patterns | 2026-09-24 offline stub tests and live runs of recipes 02–06 and 08 (English), after two fixes |
| SDK pin refresh | B/C | Refreshed dependency set and provider constraint documented | 2026-09-24 offline tests plus a live run of the core B route in both languages and the optional evaluations |
| [Hosted workflow/matrix/calibration/regression/traces](reference/evaluation-workbook.md) | C | Existing workbook | 2026-09-15 `gpt-5.6-luna` only (Korean four-model matrix); not re-run with `gpt-6-sol` |
| [Managed Toolbox lifecycle](labs/extensions/toolbox.md) | B | Executable owned/versioned path | 2026-09-16 `gpt-5.6-luna`: English direct query, MAF, local/remote Hosted and downloaded evidence verified |
| [Tool Search, Skills and private skill catalog](labs/extensions/tool-search-skills.md) | C | Executable Tool Search/Skill path | 2026-09-16 `gpt-5.6-luna`: English discovery, pinning, exact Skill readback and actual load verified; catalog infrastructure not provisioned |
| [Full-conversation evaluation and reusable datasets](labs/extensions/conversation-evaluation.md) | C | Executable dev-only multi-turn path | 2026-09-23 `gpt-6-sol`: re-verified in both languages; both native levels ran |
| [Agent Optimizer](labs/extensions/agent-optimizer.md) | C | One bounded Prompt Agent wizard | 2026-09-23 `gpt-6-sol`: re-run in both languages with a temporary `gpt-5.5` optimizer model; baseline only, and Groundedness compared each answer with itself, so nothing was promoted |
| [Durable human approval, restart recovery and steering](labs/extensions/approval-recovery.md) | C | Real local SDK demonstration | 2026-09-16: English restart/checkpoint proof with simulated decisions; not actual human authorization |
| [A2A 1.0](labs/extensions/a2a.md) | C | Explicit card/configuration and delegation | 2026-09-24 `gpt-6-sol`: English re-run with typed SDK requests, one delegated call verified (earlier: 2026-09-16 `gpt-5.6-luna`); wire packets not captured |
| [Memory](labs/extensions/memory.md) and [Routines](labs/extensions/routines.md) | C | Owned lifecycle and bounded timer | 2026-09-16 `gpt-5.6-luna`: memory verified; routine delivery verified, answer retrieval unavailable |
| [Applied guardrails and controlled red teaming](labs/extensions/agent-safety.md) | C | Dedicated policy/target | 2026-09-16 `gpt-5.6-luna`: English attachment and two unblocked cases. 2026-09-23 `gpt-6-sol`: cloud red-team scans (Preview) ran, but the displayed ASR contradicted every row's reasoning, so no red-team result is claimed |
| [Continuous evaluation and deployment quality gates](labs/extensions/release-operations.md) | C | Manual guarded workflow and OIDC setup | 2026-09-23 `gpt-6-sol`: both OIDC releases, the existing-traces evaluations and one hourly recurring schedule per language (both then paused) verified ([results](live-run.md#previously-not-run-items--september-23-2026)); production approval remains separate |
| [Agent Insights](labs/extensions/agent-insights.md) | C | Preview portal review of recurring trace patterns and human decision flow | 2026-09-24: one on-demand SDK scan (English, 22 traces, 4 insights); portal path not run |
| [Model retirement/migration and Router tradeoffs](labs/extensions/model-operations.md) | C | Fixed-model comparison and Router observation | 2026-09-16 `gpt-5.6-luna`: temporary supported model and frozen version recorded; no Router migration claim |
| Cross-provider model comparison guidance | C | Model-operations and evaluation workbook explain adding one non-OpenAI Foundry Model under the same gates | Not run: the training project has no non-OpenAI deployment, and creating one needs owner approval |
| [OpenAPI/Code Interpreter](labs/extensions/additional-tools.md), [Toolkit](labs/extensions/developer-toolkit.md), [governance/networking](labs/extensions/governance-networking.md) | B/C | Executable tools and explicit owner boundaries | 2026-09-16 `gpt-5.6-luna`: English API/file results, tooling and scoped role checks recorded; private network not tested |
| Actual company/Microsoft 365 access | Specialist | Excluded | Remains excluded |
| [Fine-tuning, voice/multimodal, browser/computer business actions](labs/extensions/specialist-scope.md) | Specialist | Design/scope only | Separate specialist curriculum, not an implied implementation |

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

**Next:** [actual results](live-run.md) · [recordings](video-summary.md) · [choose a route](paths.md).
