# September 16 extension results: what actually ran

**English** | [한국어](ko/edition-results.md)

**New English execution: September 16, 2026.** These results belong to the added B/C modules,
not to the September 15 foundational labs. Only bundled English synthetic policies and dev questions were used.
No canonical holdout was used for prompt development or these extension demonstrations.

The English actions were recorded separately from authentication. The [new extension recordings](edition-videos.md)
contain 166 actions, 496 lossless captures and three source-frame/local-playback-verified videos.
GitHub publication is a separate check; a local recording is not automatically published media.
Korean authoring and independent recording followed the English refinement step.
The [independent Korean results](ko/edition-results.md) and
[machine-readable English lineage](assets/edition-20260916-en/live-results.json) remain separate evidence.

## Results and limits

| Module | Observed result | Do not infer |
|---|---|---|
| IQ chat preset | Actual Luna query planning and answer synthesis with original Search references | A benchmark score, model fallback, or modification of the existing GA base |
| Toolbox | Discovery, direct downstream query, and MAF policy answer succeeded after correcting scoped permissions; actual version bindings retained | Local login or `tools/list` proves Search access |
| Tool Search / Skills | Skill v1 downloaded byte-for-byte; actual `load_skill → tool_search → call_tool` sequence recorded with Toolbox v4 | Merely attaching a skill proves it was loaded |
| Conversation evaluation | Two isolated three-turn conversations; business checks **6/6**; native groundedness/coherence **6/6** at turn level and **2/2** at conversation level | Different denominators establish a quality improvement |
| Agent Optimizer | One instruction-only dev run, maximum two candidates; baseline only, **no improvement**, no promotion | The generic early-stop message proves every detailed metric passed |
| Local recovery | Real SDK process stop/restart; same response, gate and first output ID preserved; explicit simulated continuation | Real human approval, Azure execution, or production crash recovery |
| Memory | Actual create/read/recall/update/remove operations; alpha/beta partition checks; owned store removed | Partition selection by one operator proves authorization between users |
| A2A | Accepted `a2a` / `1.0` configuration and same-endpoint JSONRPC interface; original paired delegation/output verified | A legacy `a2a_preview_call` event name alone identifies the wire protocol |
| OpenAPI / Code Interpreter | OpenAPI returned all six original policies; real generated CSV matched all six source rows; temporary code resources removed | A local CSV, plain answer, or another retrieval path proves the tool ran |
| Hosted Toolbox | Version 1 exposed a read-only `/app` bug; version 2 used session `$HOME`, returned a verified completed stream, and yielded eight downloaded evidence files plus **166 exact-trace rows** | `azd invoke` exit 0 or healthy readiness alone is completion |
| Routines | One manual dispatch had a finished SDK delivery record; timer disabled and removed; cancelled future attempts retained | Future timer firing or answer content: the original response ID returned 404 on retrieval |
| Safety | Actual policy resource and Hosted v3 attachment verified. D01 and D06 both completed **unblocked**; D06 retained `needs_approval` | An observed platform block or a general safety certification |
| Release/OIDC | Secretless identity bound to this private repository/environment; main-only environment and scoped roles configured | A successful workflow run before the workflow is published and executed |
| Specialist / networking | Boundaries documented; no company/Microsoft 365 data, Fabric/Work IQ connection, shared firewall or private-link change | Execution of design-only specialist capabilities |

## Read the optimizer result carefully

Run `opt_8222200dcaff4a5ea20a7b3a1688e333` stopped early with only the baseline.
Its displayed aggregate was **0.938** (rounded); no optimized candidate was generated.
The actual baseline output contained all **six exact dev queries**. The service reported Groundedness **6/6**
and relevance **5/6**, with **D05 scoring 2 and failing**.
The service's generic “perfect scores” stop warning therefore does not replace the detailed results.
No input, threshold or difficult row was changed to make the run look better.

**Grounding-reference defect found during the September 16 readback:** in all six saved English
Groundedness evaluator inputs, `context` was the generated `response` itself, not the frozen policy context
uploaded in the dataset. This is **not independent source-grounding verification**.
The same binding defect occurred in all 18 baseline/candidate rows of the independent Korean run.
The reported scores are preserved as service output, not accepted as valid grounding evidence or a promotion gate.
The English check used saved artifacts only; it did not rerun inference or relabel the English recording.

Reported tokens were 35,336 for the agent, 99,208 for the judge, and 9,561 for reflection.
The pre-run USD 0.27 estimate / USD 0.90 displayed maximum was an estimate, not an invoice or hard spending limit.
No candidate was promoted and no human approval was fabricated.

## Keep failure and lineage evidence

Each new request has its own label and retained response/error. Source patches retain before/after
hashes rather than rewriting the source history of earlier recordings.
Important recorded corrections include:

- Verify the actual native Search caller and full connection ID before paying for model requests.
- Retain original HTTP JSON when SDK tool-event types lag the service; do not change protocols or providers.
- Put Hosted evidence in the documented session home, not the read-only application directory.
- Verify the completed HTTP/SSE response, not CLI exit status; download session evidence before cleanup.
- Distinguish an already-absent memory item from a new delete, and allow bounded read-back for eventual deletion.
- Treat routine delivery, stored-answer retrieval and scheduled firing as different observations.

Read [coverage](coverage.md) to choose a module, then use that module's **Need → Do → Check → Stop** path.
Historical [foundational results](live-run.md) and [recordings](video-summary.md) keep their original dates.
