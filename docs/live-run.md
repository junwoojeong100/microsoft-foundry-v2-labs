# English live execution and evaluation results

**English** | [한국어](ko/live-run.md)

**These are this language edition's actual Azure execution results.** They are not copied from upstream repositories or the other language run.

| Cohort | Version | Rows | Errors | Business | Groundedness | Relevance | Root traces |
|---|---:|---:|---:|---:|---:|---:|---:|
| en-baseline-recall | 11 | 24 | 0 | 24/24 | 24/24 | 20/24 | 24/24 |
| en-candidate | 12 | 24 | 0 | 23/24 | 24/24 | 20/24 | 24/24 |
| en-holdout | 12 | 12 | 0 | 12/12 | 12/12 | 9/12 | 12/12 |

Business gates and native scores measure different things. `review-native-findings` is not production approval. This is a small, public synthetic dev/holdout set, not proof of statistical superiority or an unseen production validation set.

The initial English baseline's actual 20/24 result is preserved separately. Its missing scope-policy evidence led to an explicit same-provider retrieval-recall experiment, not a changed evaluator or reference answer. The new controlled baseline/candidate use that same recall setting. D05 remains pending human review and was not consumed as an approved regression.

## Execution corrections

The Korean prerequisite run identified and corrected endpoint/protocol flag conflicts, dropped API-version query parameters, explicit account embedding configuration, App Insights credential scoping, and cleanup of already-idle sessions. The English run uses the corrected code. Earlier diagnostics are retained separately; no model, endpoint, provider, or fixture is substituted automatically after errors.

## Lineage

### Retained initial diagnostic cohort

- `en-baseline-final`: version 10, 20/24 business checks, 0 execution errors; original response hash `6dec763ba04058a5947179d03b130207c7d9f48efae4bc8c76d01709480ba374`.
- Actual native eval/run: `eval_043b9f00f88841c4ba8f7ff8815d3c23` / `evalrun_aef67541bd7e4d65bb6cdf006712b707`.

### Dev-based final model selection

The English V2 candidate retained Astra's failed `citations_relevant` check on dev D05 (5/6 for that model). Only the dev-eligible Luna/Sol/Terra models were frozen for final holdout, before any holdout response was generated. Its denominator is therefore 3 models × 4 cases = 12, not 16. The original four-model candidate score remains visible.

### en-baseline-recall

- Agent version: `11`
- Target run: `matrix-6b49cdf3234f4d458f313b01fa25af77`
- Foundry eval/run: `eval_7ea2977e60c042d5a86a182b84d96870` / `evalrun_756a28a027bc47d6ba48d488a2694c16`
- Dataset: `1fa5362e46e027e3835ebf682dd2a991ca102e5f93e0326ac5e6ce551f8ed66e`
- Corpus: `9df56da4500a010ce8960dab08b1f8114720812a61455fac796b24925ffbfc14`
- Runtime code: `7eeeb72da904805d20e8ca9233d343198839527590c3b142f1a172778dd14fcd`
- Responses: `29052db55de360270317fc1810e2234250a4959b9f307319d6c49653a24c7a84`
- Evaluator: `841f69a07fb66f5d05d27f8175b016ec9d923759b62e49abd71f8f1c289f328e`

### en-candidate

- Agent version: `12`
- Target run: `matrix-dd16b7f1eaac4c7a8ceae602af7a0c8a`
- Foundry eval/run: `eval_57f2a3c163734e39b70947492a1d7cb8` / `evalrun_0eefc4c313414900b60d975f01f05a1e`
- Dataset: `1fa5362e46e027e3835ebf682dd2a991ca102e5f93e0326ac5e6ce551f8ed66e`
- Corpus: `9df56da4500a010ce8960dab08b1f8114720812a61455fac796b24925ffbfc14`
- Runtime code: `7eeeb72da904805d20e8ca9233d343198839527590c3b142f1a172778dd14fcd`
- Responses: `a615918e81bcb301190cd5c2221b21f75daa89a6839e2350d13ec6fb936f45d4`
- Evaluator: `841f69a07fb66f5d05d27f8175b016ec9d923759b62e49abd71f8f1c289f328e`

### en-holdout

- Agent version: `12`
- Target run: `matrix-ced9f6d46031434aad9907018d73523b`
- Foundry eval/run: `eval_322b9e08d490427599460ccddfc94462` / `evalrun_4b526d17261b41ba9d53b58421d902f2`
- Dataset: `e276e82bbac04260e11747f802b6671b2ad2a5c340c3af4a5b44895ca2aa14b9`
- Corpus: `9df56da4500a010ce8960dab08b1f8114720812a61455fac796b24925ffbfc14`
- Runtime code: `7eeeb72da904805d20e8ca9233d343198839527590c3b142f1a172778dd14fcd`
- Responses: `3b0f05045abe44ebfc52086994c36bea2694600450989fa3ba4efe717c6581ee`
- Evaluator: `841f69a07fb66f5d05d27f8175b016ec9d923759b62e49abd71f8f1c289f328e`

Original responses, native output, failures, trace-query results, and cleanup receipts are retained. Stopping sessions does not remove all persistent files, models, Search, or log costs.

[Recordings](video-summary.md) · [Acceptance](reference/consolidation.md)
