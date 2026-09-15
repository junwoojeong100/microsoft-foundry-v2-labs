# v2 통합 범위와 아카이브 인수 기준

[English](../../reference/consolidation.md) | **한국어**

**한국어 개정 `ko-integrated-20260915` · 조사 기준 2026-09-15.**
v2의 핵심 실습은 이 저장소의 코드·합성 자료·명령으로 진행합니다.
다른 실습 저장소를 clone하거나 그 저장소의 실행 결과를 가져올 필요가 없습니다.
README에는 모듈과 학습 내용만 표시하고, 원본 대조·저작권·한계는 이 문서와 [출처](sources.md)에 남깁니다.

## 이번 개정의 범위

기존 `model`, `answer`, `maf`, `workflow`, `collect`, `demo`의 기본 동작은 유지합니다.
그 위에 **MAF 워크플로를 실제 `Workflow.as_agent()`로 감싸는 Hosted 경로**,
**배포 버전을 고정한 다중 모델 평가**, **평가자 calibration·회귀 소비·trace 인수 검사**를 추가했습니다.
기존 SDK/포털/single-agent 점수를 새 Hosted workflow의 점수로 재사용하지 않습니다.

| 대조 기준 | v2에서 직접 수행할 위치 | 범위·차이 |
|---|---|---|
| 단일 Agent·함수·MCP | [Lab 04](../labs/04-agents-tools.md), `agents.py`, `examples/mcp_server.py` | 실제 데이터는 번들 합성 정책뿐. 외부 MCP는 선택 확장 |
| Sequential·Concurrent·Group Chat | [Lab 05](../labs/05-workflows.md), `build_orchestration`, `runtime.py` | 세 패턴 모두 실행. 동시/Group Chat의 배포용 답은 별도 최종 reviewer로 합침 |
| Workflow → Hosted | [Lab 08](../labs/08-hosted.md), `build_workflow_agent`, `package_hosted.py` | Responses와 평가용 Invocations를 명시적으로 분리 |
| 일반·하이브리드 RAG | [Lab 06](../labs/06-knowledge.md), `SearchGateway`, `embed_texts` | 일반 검색은 문자열 검색으로 표시. 하이브리드는 실제 embedding+text/vector 요청 |
| Foundry IQ·지식 계보 | [Lab 06](../labs/06-knowledge.md), [IQ 확장 워크북](iq-workbook.md) | GA intents·references·activity·문서 ID 보존. Preview body와 혼합하지 않음 |
| 다중 모델 Hosted 비교 | [평가 워크북](evaluation-workbook.md), `benchmark.py`, `hosted.py` | 고정 4종 강제 대신 1–8개 명시적 배포. 4개 선택 시 dev 24+24, holdout 16행 |
| Native 평가·업무 rubric | `native.py`, `grade_strict` | 실제 Hosted 응답 데이터의 평가. 누락·오류를 성공으로 보정하지 않음 |
| 실패 → 검토 → 회귀 재실행 | `benchmark regression`, `--regressions` | 기존 dev 질문·정답만 승인 기록에 연결하고 다음 수집에서 실제 소비 |
| Judge calibration | `calibrate-judge`, `calibration.py` | 번들 정답/오답 예제로 오탐·미탐 검사. target의 새 답변으로 집계하지 않음 |
| Trace·Monitor·인수 | `trace-plan`, `monitor`, `verify`, `observability.py` | 정확한 trace 집합·시간·agent로 조회. 실제 조회와 단순 ID 기록을 구분 |
| Fabric·Work IQ·Toolbox·OBO | [Lab 10](../labs/10-iq-extensions.md), [IQ 확장 워크북](iq-workbook.md) | 별도 승인·SDK/리전/데이터 조건이 있는 선택 경로. 회사/M365 접근을 기본으로 만들지 않음 |

## 원본의 현재 상태와 고정 비교 지점

아래 `archived`는 **읽기 전용 조회 결과**입니다. 이번 작업에서 원본 저장소 상태를 변경하지 않았습니다.

| 저장소 | 비교 커밋 | 조회 당시 상태 |
|---|---|---|
| `agent-framework-labs` | `cca14163def4c88616dcd4c93fcfd6441fb08f30` | 이미 archived |
| `foundry-maf-workshop` | `d07c614a616446e63ee50b0b34540b5481aff5b2` | 이미 archived |
| `microsoft-iq-on-foundry` | `fa16c84f9800377823edd9aea1cb20d6a56a1edf` | 이미 archived |
| `foundry-evaluation` | `0b91e47f88ca4d1a5e1dd961d45ea6b40afbb33b` | active |

IQ/Evaluation을 한두 달 더 유지하려는 운영 계획과 별개로, IQ는 조회 당시 이미 archived였습니다.
해제·재아카이브·삭제는 별도 운영 결정입니다. 아카이브는 코드 삭제나 기존 URL의 소멸과 같지 않습니다.

## 그대로 가져오지 않은 관행

- 모델 이름·리전·quota를 고정해 모든 사용자에게 강제하거나 실패 시 다른 endpoint로 전환하지 않습니다.
- 기본 Azure CLI 구독을 바꾸지 않습니다. 실행 credential과 ARM 조회의 구독을 명시합니다.
- 일반 검색·로컬 fixture·합성 라우팅을 실제 IQ/Work IQ 연결 성공으로 표시하지 않습니다.
- user/프로젝트/Hosted instance identity를 같은 권한 주체로 다루지 않습니다.
- 원본의 모든 패키지를 일괄 upgrade하거나 `@workflow` experimental API를 핵심 선행 조건으로 넣지 않습니다.
- 원본 성공 횟수·64행 점수·trace 수를 이 개정판의 검증 결과로 복사하지 않습니다.
- 평가 정답·calibration·보고서를 Hosted 배포 패키지에 넣지 않습니다.

## 아카이브 완료 판단은 문서 수가 아니라 실행 증거

| 인수 게이트 | 필요한 증거 |
|---|---|
| 독립 실행 | v2 새 복사본에서 설치·doctor·정책 export·기본 모델/MAF/MCP 실행 |
| Workflow Hosted | 새 프로필 패키지, 로컬 실제 응답, 배포된 정확한 version·protocol·runtime contract |
| IQ/하이브리드 | 실제 provider·API·원문·embedding 차원 확인. 선택하지 않은 방식은 미실행 |
| 평가 대체 | 네 모델을 선택했다면 완전한 24/24/16행, 동일 evaluator, 실제 trace, 소비된 회귀 계보 |
| 안전한 인수 | 모델별 실패·native findings·비용·오류·사람 검토를 포함한 보고서 |
| 문서·미디어 | 현재 한국어 명령의 새 촬영. 기존 single-agent 영상으로 workflow 완료를 주장하지 않음 |
| 영문 | 한국어 촬영/보완 이후 번역, 영문 촬영, 최종 명령·링크 재검사 |

**코드/문서 검사와 실제 Azure 인수는 별개입니다.**
국문 후속 실행에서는 실제 workflow 배포, 네 모델의 24/24/16행, native 평가·calibration·64개 root trace와 새 촬영을 확인했습니다.
외부 Work IQ/Fabric/Toolbox 연결까지 자동으로 검증한 것은 아니며, 기능별 실제 범위는 [실행 결과](../live-run.md)에 구분합니다.

## 이후 작업 순서

1. 한국어 가이드와 코드의 offline/SDK 계약을 동결합니다.
2. 승인된 환경에서 한국어 실습을 실제 실행하고 액션별 캡처·녹화·오류를 보존합니다.
3. 촬영에서 발견한 차이를 한국어 명령과 문서에 반영합니다.
4. 그 개정본을 영어로 번역/보강하고 영어 촬영·검증을 수행합니다.

영문 유예는 `docs/localization.json`에 파일 해시와 함께 기록합니다.
유예 중에도 영어/한국어의 모든 CLI 예제 자체는 파서 검사를 통과해야 합니다.
