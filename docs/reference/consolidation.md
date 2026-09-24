# v2 consolidation and archive acceptance

**English** | [한국어](../ko/reference/consolidation.md)

**Checked September 15, 2026; the main A/B steps were re-run with `gpt-6-sol` on September 24 ([results](../live-run.md)).** Core v2 labs use this repository's code, synthetic data, and commands.
There is no hidden requirement to clone another workshop or reuse its reported results.
README tables show learning content; attribution, comparison, and limits stay here and in [sources](sources.md).

## Consolidated scope

Existing introductory commands retain their defaults.
The advanced path adds actual `Workflow.as_agent()` hosting, pinned-version model matrices,
judge calibration, consumed reviewed regressions, and trace/acceptance checks.
Single-agent/project/portal scores are not reused as Hosted-workflow scores.

| Capability | Self-contained v2 location | Boundary |
|---|---|---|
| Agent, function, MCP | [Lab 04](../labs/04-agents-tools.md), `agents.py`, `mcp_server.py` | Bundled synthetic policies; external MCP is optional |
| Three workflow patterns | [Lab 05](../labs/05-workflows.md), `build_orchestration`, `runtime.py` | Concurrent/group-chat use a final reviewer for the deployable answer |
| Workflow → Hosted | [Lab 08](../labs/08-hosted.md), profile packaging | Responses and typed Invocations are distinct |
| Keyword/hybrid RAG | [Lab 06](../labs/06-knowledge.md), SearchGateway | Hybrid uses real embeddings and text/vector requests |
| IQ/evidence lineage | [IQ workbook](iq-workbook.md) | GA intents, references, activity, and document IDs; separate Preview contracts |
| Hosted model matrix | [Evaluation workbook](evaluation-workbook.md) | 1–8 explicit deployments; four models produce 24/24/16 rows |
| Native/business evaluation | `native.py`, `grade_strict` | Actual Hosted response data; errors/missing rows never become success |
| Reviewed regression reuse | `benchmark regression`, `--regressions` | Frozen dev references are actually consumed by the next collection |
| Calibration | `calibrate-judge` | Prewritten correct/incorrect examples test the judge, not the target |
| Trace/Monitor/acceptance | `trace-plan`, `monitor`, `verify` | Exact trace sets and actual scoped queries; IDs alone are not export proof |
| Fabric/Work IQ/Toolbox/OBO | [Lab 10](../labs/10-iq-extensions.md), [IQ workbook](iq-workbook.md) | Optional approval and service-specific identity/data requirements |

## Pinned comparison points

These archive states were **read-only observations**, not changes made by this work.

| Repository | Compared commit | Observed state |
|---|---|---|
| `agent-framework-labs` | `cca14163def4c88616dcd4c93fcfd6441fb08f30` | Already archived |
| `foundry-maf-workshop` | `d07c614a616446e63ee50b0b34540b5481aff5b2` | Already archived |
| `microsoft-iq-on-foundry` | `fa16c84f9800377823edd9aea1cb20d6a56a1edf` | Already archived |
| `foundry-evaluation` | `0b91e47f88ca4d1a5e1dd961d45ea6b40afbb33b` | Active |

The plan to maintain IQ/Evaluation for another month or two is separate from their observed state.
Unarchiving, archiving, or deleting repositories requires a separate operational decision.
Archiving does not remove code or existing URLs.

## Practices intentionally not carried forward

- No recording-specific model/region/quota values presented as universal availability; the dated first-pass Luna preset is prepared explicitly. No error-triggered endpoint substitution.
- No default Azure subscription changes.
- No relabeling keyword search, fixtures, or synthetic routing as real IQ/Work IQ success.
- No assumption that user, project, and Hosted identities share permissions.
- No blanket package upgrades or mandatory experimental functional workflow APIs.
- No reuse of upstream response counts, scores, or traces as this edition's evidence.
- No evaluation references, calibration, or reports inside the deployment package.

## Archive readiness requires execution evidence

| Gate | Required evidence |
|---|---|
| Independent execution | Fresh v2 setup, doctor, policies, model/MAF/MCP requests |
| Hosted workflow | Profile package, actual local response, exact deployed version/protocol/contract |
| IQ/hybrid | Actual provider/API/documents/embedding dimensions; unselected paths remain unexecuted |
| Evaluation replacement | Complete 24/24/16 rows for four models, same evaluators, real traces, honest regression lineage |
| Acceptance | Model-level failures, native findings, costs, uncertainty, and human review |
| Media | New captures matching current commands; no single-agent footage relabeled as workflow proof |
| Languages | Follow the active source-language order; each language's recording needs its own execution/corrections |

On September 15, 2026 (earlier `gpt-5.6-luna` edition) the Korean follow-up verified actual workflow deployment,
four-model 24/24/16 rows, native evaluation, calibration and 64 root traces; that matrix was not re-run with `gpt-6-sol`.
That does not validate every optional external Work IQ/Fabric/Toolbox path.
The September 24 [live results](../live-run.md) cover the main A/B steps and the optional evaluation steps with `gpt-6-sol`.

## Release sequence

**The September 15 Korean-first sequence is historical, not a standing instruction.**
Follow the user's current order and the active `source_language` / `revision` in
[`docs/localization.json`](../localization.json).

1. Revise and check the source-language guide against the executable commands.
2. Perform new live execution/capture only when separately requested and authorized; preserve all failures.
3. Incorporate observations into the source guide, then update its counterpart.
4. If new media is requested, use independent execution/capture for each language.

Any deferred counterpart has a visible warning and exact source/target hashes.
Both languages' commands are parsed even during a deferral. A guide-only revision does not establish new live or media evidence.
