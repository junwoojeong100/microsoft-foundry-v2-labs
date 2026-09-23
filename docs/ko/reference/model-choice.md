# 모델 선택: 이 에디션이 gpt-6-sol을 쓰는 이유 — 2026-09-23

[English](../../reference/model-choice.md) | **한국어**

**응답 preset은 `gpt-6-sol`, 모델 버전 `2026-09-22`이고 별도 평가 judge는 `gpt-6-sol-judge`입니다.**
전용 Sweden Central 실습 프로젝트에서 날짜를 적어 관찰한 결과이며 지원을 보장하지 않습니다.
수업 직전에 다시 확인합니다.

## 실제로 확인한 것

| 실습 경로 | `gpt-6-sol` | `gpt-6-astra` | `gpt-6-luna` |
|---|---|---|---|
| 프로젝트 Responses: `model`·`answer`·`collect` (Lab 02·06·07) | ✅ | ✅ | ❌ HTTP 500 |
| 포털 Prompt Agent 채팅 (Lab 03·07 A) | ✅ | ✅ | ❌ `reasoning.effort` 미지원 |
| SDK Prompt Agent 호출 | ✅ | ✅ | ❌ HTTP 500 |
| MAF 함수 도구·로컬 MCP (Lab 04) | ✅ | ✅ | ❌ HTTP 500 |
| dev 6문항 업무 기준 (`v2`, 로컬 검색) | 6/6, 중앙값 2.1초 | 6/6, 중앙값 4.3초 | 실행 불가 |
| Sweden Central Data Zone Standard | ✅ | ❌ Global Standard만 | ✅ |
| 공개 가격 (1M 토큰, 입력/출력) | 아직 미공개 | USD 10 / 50 | 아직 미공개 |
| Lab 00–09·11 A/B 주요 단계 녹화 ([녹화](../video-summary.md)) | ✅ 영문·국문 | 실행 안 함 | 실행 안 함 |

`gpt-6-luna`는 배포되고 포털 모델 Playground에서도 답했지만, 프로젝트 agent 경로는 UTC 23:52~01:53 반복 확인에서
Data Zone·Global Standard 배포와 다른 리전 모두 HTTP 500이었습니다.
같은 프로젝트의 `gpt-6-astra`는 동작했으므로 그날 실패는 `gpt-6-luna`에 한정됐습니다.
`gpt-6-astra`는 동작하지만 비용이 크고 이번 확인에서 더 느렸으며 Sweden Central에서 Data Zone Standard가 없습니다.

**선택:** `gpt-6-sol`은 위에서 확인한 모든 경로를 통과했고 EU Data Zone 처리를 유지하며 할당량 등급 요청이 필요 없습니다.
File Search·하이브리드 RAG·학습자가 직접 하는 Hosted 배포와 대부분의 확장 모듈은 이 모델로 다시 실행하지 않았습니다. 승인된 CI 릴리스와 확장 모듈 4개는 다시 실행했습니다([결과](../live-run.md#이전에-실행하지-않은-항목--2026-09-23)).
수업 전에 공개 가격을 확인합니다. 오류가 나면 다른 모델로 바꾸지 말고 멈춘 뒤 기록합니다.

## 고정된 예외 두 가지

- **IQ Chat은 `gpt-5.6-luna` / `2026-07-09`를 유지합니다.** 2026-09-23 Search knowledge base는 GPT-6 모델을 받지 않았습니다
  (`Unsupported model type in Knowledge Base Model Configuration`). 선택 경로에서만 별도 배포를 준비합니다.
  [IQ Chat preset](iq-model-identity.md).
- **포털 부수 효과:** 첫 포털 agent를 열 때 `text-embedding-3-large` Standard 배포가 함께 생성됐습니다.
  실습은 사용하지 않으며 Lab 09에서 소유 자산으로 기록합니다.

`gpt-6-sol`은 짧은 답에도 reasoning token을 보고하며 출력 사용량에 포함됩니다.

[설정](../setup.md) · [문제 해결](troubleshooting.md) · [버전](versions.md) · [검증](validation.md)
