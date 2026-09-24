# C. 고급: 필요한 기능을 선택하고 근거 남기기

[English](../../paths/c-advanced.md) | **한국어**

**C는 모듈 목록이지 하나의 거대한 필수 순서가 아닙니다.**
기존 Hosted workflow 평가 워크북도 고급 경로로 유지합니다.
새 모듈은 각자의 준비 조건과 완료 기준을 충족한 범위만 검증되었다고 기록합니다.

**아래에서 모듈 하나만 선택합니다.** 명령 전에 **첫 회차·준비·완료 기준**을 읽습니다.
[개발 도구 준비](../labs/extensions/developer-toolkit.md)는 그 모듈에 부족한 도구만 보완할 때 사용합니다.
언어를 유지하고 마지막 단계·정확한 label을 `session-notes.txt`에 기록하며 자동 결과 폴더는 원래 위치에 둡니다.
미선택 기능은 **미실행**, 시도한 오류는 **실패/차단**입니다. 다른 결과로 성공을 대신하지 않습니다.

## 목표로 고르기

| 하고 싶은 일 | 시작할 곳 | 나중에 할 일 |
|---|---|---|
| 여러 agent에서 도구 하나 재사용 | [관리형 Toolbox](../labs/extensions/toolbox.md) | Tool Search/Skills 또는 Hosted Toolbox |
| 답변 하나가 아닌 대화 평가 | [대화 평가](../labs/extensions/conversation-evaluation.md) | Optimizer 또는 반복 평가 |
| 반복 trace 패턴을 검토된 결정으로 전환 | [Agent Insights](../labs/extensions/agent-insights.md) | severity를 ground truth로 취급하거나 dev 평가 없이 instruction 변경 |
| 모델 호출 없이 중단·재개 이해 | [로컬 승인/복구 시뮬레이션](../labs/extensions/approval-recovery.md) | 실제 인가나 Hosted crash 검증 |
| 리소스 변경 없이 접근·구조 검토 | [거버넌스·네트워크](../labs/extensions/governance-networking.md) 또는 [전문 범위](../labs/extensions/specialist-scope.md) | 부족한 인프라 생성 |
| 고정 버전의 Hosted 시스템 인수 | B의 모델·MAF·IQ 결과 이후 [Hosted 평가 워크북](../reference/evaluation-workbook.md) | 운영 릴리스 승인 |

독립적인 시작점이지 차례로 마쳐야 할 다섯 단계가 아닙니다. 아래 전체 목록에서 모듈별 준비 조건을 확인합니다.

## 추가 모듈

| 모듈 | 배우는 것 | 첫 실습의 준비 조건·경계 |
|---|---|---|
| [관리형 Toolbox](../labs/extensions/toolbox.md) | 버전을 고정한 합성 정책 도구 재사용 | Lab 06 Search·승인된 keyless 연결·Hosted/Toolbox SDK. Default 변경은 선택 |
| [Hosted Toolbox](../labs/extensions/toolbox-hosted.md) | 같은 도구 agent의 원격 실행 | 검증한 로컬 Toolbox·별도 azd 폴더·런타임 권한·배포 승인 |
| [Code Interpreter / OpenAPI](../labs/extensions/additional-tools.md) | 실제 CSV 생성 또는 읽기 전용 API 호출 검증 | 도구 하나 선택. 첫 회차는 Code Interpreter, OpenAPI는 본인 Search index 필요 |
| [Tool Search와 Skills](../labs/extensions/tool-search-skills.md) | 도구 발견·검토된 절차의 버전 재사용 | 실제 동작하는 내 Toolbox, Preview 선택 |
| [대화 평가](../labs/extensions/conversation-evaluation.md) | 개별 턴과 전체 대화 평가 구분 | 동봉 dev를 사용한 실제 다중 턴, holdout 개발 금지 |
| [Agent Insights](../labs/extensions/agent-insights.md) | AI 생성 trace 패턴 finding을 검토한 뒤 평가·routing·instruction 변경을 결정 | Lab 03 Prompt Agent, 연결된 App Insights, 충분한 기존 합성 trace. Preview이며 ground truth가 아님 |
| [Agent Optimizer](../labs/extensions/agent-optimizer.md) | 고정된 dev baseline에 대한 후보 검토 | 준비된 optimizer/judge 모델, 비용 승인, Preview |
| [승인 게이트와 복구](../labs/extensions/approval-recovery.md) | 실제 SDK 중단·체크포인트·재개 | 로컬 모의 결정, 실제 사람 승인/Hosted crash 증거 아님 |
| [A2A](../labs/extensions/a2a.md) | 별도 주소의 agent에 위임 | 명시적인 1.0과 호출 권한, 0.3 fallback 금지 |
| [Memory](../labs/extensions/memory.md) | 합성 맥락 저장·검색·삭제 | 준비된 모델, API 기반 경로, 자동 추출/사용자 인가 증거 아님 |
| [Routines](../labs/extensions/routines.md) | 제한된 예약과 전달 이력 | 대상 agent·예약·비용·정리 책임 |
| [Agent 안전 제어](../labs/extensions/agent-safety.md) | 적용된 정책과 실제 개입 구분 | 실습 전용 정책·대상, 추가 권한/Preview 경계 |
| [릴리스 운영](../labs/extensions/release-operations.md) | OIDC·평가 gate·승인·rollback | 전용 배포 ID와 수동 릴리스 승인 |
| [모델 운영](../labs/extensions/model-operations.md) | 교체·Router·폐기 판단 | 고정된 작업과 모델 허용 목록, 실제 사용량·지연 |
| [거버넌스·네트워크](../labs/extensions/governance-networking.md) | 호출 주체·정책·사설망 경계 | 담당자가 준비한 인프라, 공유 설정 변경 금지 |

[기능 상태](../coverage.md)를 함께 읽습니다. 공식 문서나 설치된 SDK는 이 실습이 실행되었다는 증거가 아닙니다.
모듈은 2026-09-16에 이전 `gpt-5.6-luna` preset으로 실행했으며(예: 후보가 없는 최적화, 답변이 아닌 전달만 확인된 Routine)
`gpt-6-sol`로는 대화 평가, Agent Optimizer, 안전 제어의 red-team 단계, 릴리스 운영만 2026-09-23에 다시 실행했습니다.
2026-09-24 저녁에는 A2A를 `gpt-6-sol`과 형식이 있는 SDK 요청으로 영문 재실행했고, SDK로 on-demand Insights scan을 1회 실행했습니다. 각 모듈은 직접 확인합니다.

## 실험 조건 유지

독립 평가 사례끼리 Memory나 대화 상태를 공유하지 않습니다.
사람이 검토하고 고정하기 전의 optimizer 후보를 holdout 평가에 넣지 않습니다.
모두 통과하거나 개선이 없는 baseline도 유효한 결과입니다. 실패나 개선을 만들지 않습니다.
Hosted 워크북은 버전·protocol을 고정하고 모델×문항 행과 오류, judge calibration, 검토한 regression과 실제 root trace를 보존합니다.
패키징·로컬 호출·배포·평가·승인은 각각 별도 결과입니다.

## 별도 전문 영역

Fabric/Work IQ, Autopilot/Agent 365, fine-tuning, 음성·멀티모달, 브라우저 업무 동작은
다른 데이터·ID·런타임 준비가 필요합니다. 실제 회사/Microsoft 365 데이터는 접근하지 않습니다.
[설계·범위 문서](../labs/extensions/specialist-scope.md)를 실제 구현 결과로 표시하지 않습니다.

**선택한 모듈 종료:** 근거를 남기고 승인된 내 자산만 정리한 뒤 [Lab 11](../labs/11-capstone.md)에 실제 결과를 추가합니다.
