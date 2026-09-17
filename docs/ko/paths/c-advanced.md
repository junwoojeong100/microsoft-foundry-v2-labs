# C. 고급: 필요한 기능을 선택하고 근거 남기기

[English](../../paths/c-advanced.md) | **한국어**

**C는 모듈 목록이지 하나의 거대한 필수 순서가 아닙니다.**
기존 Hosted workflow 평가 워크북도 고급 경로로 유지합니다.
새 모듈은 각자의 준비 조건과 완료 기준을 충족한 범위만 검증되었다고 기록합니다.

**아래에서 모듈 하나만 선택합니다.** 명령 전에 **첫 회차·준비·완료 기준**을 읽습니다.
[개발 도구 준비](../labs/extensions/developer-toolkit.md)는 그 모듈에 부족한 도구만 보완할 때 사용합니다.
언어를 유지하고 마지막 단계·정확한 label을 `session-notes.txt`에 기록하며 자동 결과 폴더는 원래 위치에 둡니다.
미선택 기능은 **미실행**, 시도한 오류는 **실패/차단**입니다. 다른 결과로 성공을 대신하지 않습니다.

## 기존 통합 경로

B의 실제 모델·MAF·IQ 결과를 준비한 뒤 [Hosted 평가 워크북](../reference/evaluation-workbook.md)을 진행합니다.
실제 Hosted 버전과 protocol을 고정하고 모든 모델×문항 행과 오류, judge calibration,
검토된 regression 이력, 실제 root trace를 보존합니다.
패키징·로컬 호출·원격 배포·native 평가·사람의 승인은 서로 다른 결과입니다.

## 추가 모듈

| 모듈 | 배우는 것 | 첫 실습의 준비 조건·경계 |
|---|---|---|
| [관리형 Toolbox](../labs/extensions/toolbox.md) | 버전을 고정한 합성 정책 도구 재사용 | Lab 06 Search·승인된 keyless 연결·Hosted/Toolbox SDK. Default 변경은 선택 |
| [Hosted Toolbox](../labs/extensions/toolbox-hosted.md) | 같은 도구 agent의 원격 실행 | 검증한 로컬 Toolbox·별도 azd 폴더·런타임 권한·배포 승인 |
| [Code Interpreter / OpenAPI](../labs/extensions/additional-tools.md) | 실제 CSV 생성 또는 읽기 전용 API 호출 검증 | 도구 하나 선택. 첫 회차는 Code Interpreter, OpenAPI는 본인 Search index 필요 |
| [Tool Search와 Skills](../labs/extensions/tool-search-skills.md) | 도구 발견·검토된 절차의 버전 재사용 | 실제 동작하는 내 Toolbox, Preview 선택 |
| [대화 평가](../labs/extensions/conversation-evaluation.md) | 개별 턴과 전체 대화 평가 구분 | 동봉 dev를 사용한 실제 다중 턴, holdout 개발 금지 |
| [Agent Optimizer](../labs/extensions/agent-optimizer.md) | 고정된 dev baseline에 대한 후보 검토 | 준비된 optimizer/judge 모델, 비용 승인, Preview |
| [승인 게이트와 복구](../labs/extensions/approval-recovery.md) | 실제 SDK 중단·체크포인트·재개 | 로컬 모의 결정, 실제 사람 승인/Hosted crash 증거 아님 |
| [A2A](../labs/extensions/a2a.md) | 별도 주소의 agent에 위임 | 명시적인 1.0과 호출 권한, 0.3 fallback 금지 |
| [Memory](../labs/extensions/memory.md) | 합성 맥락 저장·검색·삭제 | 준비된 모델, API 기반 경로, 자동 추출/사용자 인가 증거 아님 |
| [Routines](../labs/extensions/routines.md) | 제한된 예약과 전달 이력 | 대상 agent·예약·비용·정리 책임 |
| [Agent 안전 제어](../labs/extensions/agent-safety.md) | 적용된 정책과 실제 개입 구분 | 실습 전용 정책·대상, 추가 권한/Preview 경계 |
| [릴리스 운영](../labs/extensions/release-operations.md) | OIDC·평가 gate·승인·rollback | 전용 배포 ID와 수동 릴리스 승인 |
| [모델 운영](../labs/extensions/model-operations.md) | 교체·Router·폐기 판단 | 고정된 작업과 모델 허용 목록, 실제 사용량·지연 |
| [거버넌스·네트워크](../labs/extensions/governance-networking.md) | 호출 주체·정책·사설망 경계 | 담당자가 준비한 인프라, 공유 설정 변경 금지 |

[기능 상태](../coverage.md)와 [이번 판의 결과](../edition-results.md)를 함께 읽습니다.
공식 문서나 설치된 SDK는 이 실습이 실행되었다는 증거가 아닙니다.
후보가 없는 최적화, 답변이 아닌 전달만 확인된 Routine도 그대로 표시합니다.

## 선택 순서

재사용 도구가 목표라면 Toolbox 이후 Tool Search/Skills **또는** Hosted Toolbox를 선택합니다.
학습·개선 루프는 대화 평가부터 시작하며 Optimizer·반복 평가는 각각 나중의 별도 선택입니다.
모델 호출 없이 SDK를 익히려면 로컬 승인 게이트/복구를 선택합니다. A2A·Memory·예약·릴리스의 선행 조건은 아닙니다.
읽기·설계만 하려면 거버넌스·네트워크 또는 전문 범위를 선택하고, 빈 워크시트를 채우려고 자원을 만들지 않습니다.

독립 평가 사례끼리 Memory나 대화 상태를 공유하지 않습니다.
사람이 검토하고 고정하기 전의 optimizer 후보를 holdout 평가에 넣지 않습니다.
모두 통과하거나 개선이 없는 baseline도 유효한 결과입니다. 실패나 개선을 만들지 않습니다.

## 별도 전문 영역

Fabric/Work IQ, Autopilot/Agent 365, fine-tuning, 음성·멀티모달, 브라우저 업무 동작은
다른 데이터·ID·런타임 준비가 필요합니다. 실제 회사/Microsoft 365 데이터는 접근하지 않습니다.
[설계·범위 문서](../labs/extensions/specialist-scope.md)를 실제 구현 결과로 표시하지 않습니다.

**선택한 모듈 종료:** 근거를 남기고 승인된 내 자산만 정리한 뒤 [Lab 11](../labs/11-capstone.md)에 실제 결과를 추가합니다.
