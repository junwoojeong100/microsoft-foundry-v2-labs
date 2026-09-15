# 새 국문 실제 실행과 평가 결과

[English](../live-run.md) | **한국어**

**이번 언어의 실제 Azure 실행 결과**입니다. 다른 저장소나 다른 언어의 결과를 복사하지 않았습니다.

| Cohort | Version | Rows | Errors | Business | Groundedness | Relevance | Root traces |
|---|---:|---:|---:|---:|---:|---:|---:|
| ko-baseline-final | 7 | 24 | 0 | 24/24 | 24/24 | 19/24 | 24/24 |
| ko-candidate | 8 | 24 | 0 | 24/24 | 22/24 | 20/24 | 24/24 |
| ko-holdout | 8 | 16 | 0 | 16/16 | 16/16 | 13/16 | 16/16 |

업무 gate와 native 점수는 다릅니다. `review-native-findings`를 운영 승인으로 처리하지 않습니다. 작은 공개 합성 dev/holdout이며 통계적 우월성·미사용 운영 검증셋을 주장하지 않습니다.

Baseline이 모두 통과했으므로 실패를 만들거나 정답을 바꾸지 않았습니다. 회귀 승격을 강제하지 않았고 실제 소비 여부를 기록했습니다.

## 실제 발견한 문제와 수정

- 전체 endpoint와 protocol 옵션의 충돌을 수정했습니다.
- batch session query에 API version을 보존했습니다.
- 프로젝트 embedding 404 이후 원본 실패를 보존하고 같은 account API를 명시적으로 설정했습니다.
- App Insights 전용 audience와 고정 구독/tenant credential을 적용했습니다.
- 이미 idle인 세션은 불필요한 stop 충돌 없이 실제 상태를 확인합니다.

초기 진단용 24행은 본 비교와 분리해 보존했습니다. 모델/endpoint/provider/fixture를 오류 뒤에 자동으로 바꾸지 않습니다.

## Lineage

### ko-baseline-final

- Agent version: `7`
- Target run: `matrix-9530742c2acd40de97a0d3cce4dc6a6a`
- Foundry eval/run: `eval_59324eff64524d27bd35c29557101648` / `evalrun_b9cc9ae783244a7eb6396f38c5c874ae`
- Dataset: `84e2b286e92e73f3e4998339c1826ca140cbc28d2aa7cb46c24182b4b57a6e22`
- Corpus: `3556faa7cb0099cf01794a3e4da995f5fd8524982299fe34aafa636173287d39`
- Runtime code: `08325304035042a9f697eaa262c355d214a62e8bf314c01e46ffaf2da977690b`
- Responses: `af3b0ced94d6e63b12e8cfc83523f85504f1123b827a01cb333f4e497188752c`
- Evaluator: `841f69a07fb66f5d05d27f8175b016ec9d923759b62e49abd71f8f1c289f328e`

### ko-candidate

- Agent version: `8`
- Target run: `matrix-36556fe3863a4247b84d7d78b21a5823`
- Foundry eval/run: `eval_cc623f5cd1dc4c2e9a38e1cb09a210e2` / `evalrun_a6c99fd13c66435cb14ecebd8364a75f`
- Dataset: `84e2b286e92e73f3e4998339c1826ca140cbc28d2aa7cb46c24182b4b57a6e22`
- Corpus: `3556faa7cb0099cf01794a3e4da995f5fd8524982299fe34aafa636173287d39`
- Runtime code: `08325304035042a9f697eaa262c355d214a62e8bf314c01e46ffaf2da977690b`
- Responses: `9e8d331112b7b0dbd6ee677f44a1eaddd6e662913c4afd01e14d70b0fcc0eaba`
- Evaluator: `841f69a07fb66f5d05d27f8175b016ec9d923759b62e49abd71f8f1c289f328e`

### ko-holdout

- Agent version: `8`
- Target run: `matrix-9794a3a0b3e84471b1fe95d8c32398e1`
- Foundry eval/run: `eval_9d62c3804cb748aca4a85d52cf648b76` / `evalrun_3932c6e8aefd4afab33240b55f64154a`
- Dataset: `9d478d727527064c78985201052e86a94eaeb551327d19f29b83cc23e5c53e9c`
- Corpus: `3556faa7cb0099cf01794a3e4da995f5fd8524982299fe34aafa636173287d39`
- Runtime code: `08325304035042a9f697eaa262c355d214a62e8bf314c01e46ffaf2da977690b`
- Responses: `065059c0cc2e85f5b66b947a66c8a2f764b7054bcdaa9e34e21548b102d597cf`
- Evaluator: `841f69a07fb66f5d05d27f8175b016ec9d923759b62e49abd71f8f1c289f328e`

현재 원본 응답·native output·실패·trace 조회·cleanup receipt는 실행 이력으로 보존합니다. 세션 중지는 파일·모델·Search·로그 비용이 모두 삭제됨을 의미하지 않습니다.

[새 촬영본 / Recordings](video-summary.md) · [인수 기준 / Acceptance](reference/consolidation.md)
