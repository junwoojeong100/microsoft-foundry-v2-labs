# 2025년 종합 랩에서 v2로

[English](../../reference/migration.md) | **한국어**

**개념은 이어받고, 실행 계약과 학습 경로는 다시 구성했습니다.**
원본 종합 랩의 마지막 확인 커밋은 2025-12-14입니다.

| 기존 종합 랩 | v2에서 이어지는 위치 | 달라진 점 |
|---|---|---|
| 01 환경 설정 | 00–01 | 브라우저와 Python 분리, 학습자에게 구독 Owner를 요구하지 않음 |
| 02 모델/Router | 02 + 07 | 배포 이름 고정, 실제 모델 비교와 routing 실험 구분 |
| 03 에이전트/도구 | 03–04 | 관리형 prompt agent와 로컬 MAF 구분, 합성 읽기 전용 도구 |
| 04 Foundry IQ | 06 + 10 | GA intents와 richer Preview 분리, 참조 번호와 문서 ID 구분 |
| 05 포털 Workflow | 05 + 08 | 포털 작성 경로 제외, MAF 코드 오케스트레이션·사람 검토·Hosted 기반 구분 |
| 06 Evaluation | 07 | dev/holdout, 오류를 포함한 분모, 고정 후보, 실제 evaluator 이력 |
| 07 Control Plane | 09 | 버전·권한·trace·quota·비용·정리의 운영 게이트 |

## 작은 모듈을 어떻게 통합했나?

| 원본 모듈 | 가져온 학습 구조 | 통합하면서 바꾼 것 |
|---|---|---|
| foundry-maf-workshop | 포털 → 모델 SDK → Agent → tool → workflow → hosted | 공통 CLI/환경, 합성 정책 시나리오 |
| agent-framework-labs | 단일/순차/병렬/Group Chat/MCP/RAG | 같은 입력·권한 경계·명시적 종료 조건 |
| microsoft-iq-on-foundry | knowledge source/base, Toolbox, IQ 구분 | GA 기본과 실제 외부 데이터 옵트인 분리 |
| foundry-evaluation | 기업의 학습 루프, 실패 이력, dev/holdout, 사람 검토 | 특정 네 모델 강제 제거, 작은 공통 데이터·provider 선택 |

## 그대로 복사하지 않은 것

- 포털 workflow의 노드 생성·연결·게시 절차는 가져오지 않습니다. Lab 05의 MAF builder로 학습합니다.
- 구독별로 검증된 특정 모델 ID·리전·quota를 모든 사람의 기본값으로 삼지 않았습니다.
- 개별 리포마다 다른 `.env` 이름과 Python/SDK 조합을 혼합하지 않았습니다.
- 실제 고객·개인 환경, resource ID, 토큰, 영상의 환경 식별자를 복사하지 않았습니다.
- 다른 리포의 성공 기록/평가 점수를 이 에디션의 검증 결과로 사용하지 않았습니다.
- 2025년의 notebook 셀과 현재 SDK 2.x를 섞어 실행하지 않습니다.
- Portal, local MAF, Hosted, offline fixture를 같은 실행 경로라고 하지 않습니다.

기존 classic의 threads/runs/Assistants 또는 `azure-ai-inference` 예제를 가져오기 전에는
[공식 current Foundry 이동 가이드](https://learn.microsoft.com/azure/foundry/how-to/navigate-from-classic)를
확인합니다. 현재 문서의 관련 종료·이행 일정은 과거 실습의 동작을 보장하지 않습니다.

핵심 과정에는 다른 저장소를 추가로 clone할 필요가 없습니다. 원본 링크는 깊은 확장과 출처 확인을 위한 참고이며,
실행 가능한 핵심·데이터·문서는 이 저장소에 있습니다.
이제 영문이 기본 진입점이며, 같은 내용의 [국문 가이드](../../../README.ko.md)가 있습니다.
