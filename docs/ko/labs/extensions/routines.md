# Routines: 예약·수동 전달·실제 답변을 구분하기

[English](../../../labs/extensions/routines.md) | **한국어**

**C 선택.** Routine은 기존 agent를 트리거합니다. agent를 새로 만들거나 지속 승인 서비스를 구현하거나
회사/Microsoft 365 접근을 승인하지 않습니다. 확인한 azd 확장은 2026-09-16에 routine 명령을 Preview로 표시했습니다.

**근거 상태:** 영문 routine 전달을 2026-09-16 이전 `gpt-5.6-luna` preset으로 실행했습니다(답변 조회는 불가). `gpt-6-sol`로 다시 실행하지 않았습니다.

**준비:** 승인된 기존 Prompt 또는 Hosted Responses agent, 실제 프로젝트 endpoint, azd routine 명령, 소유 routine 이름, 비용 승인.
**완료:** dispatch 하나에서 식별 가능한 실행 결과를 얻고 이후 routine을 비활성화함.
**막히면:** 조사하기 전에 소유 routine을 비활성화하고 dispatch ID·오류를 보존합니다.

**첫 회차:** 1–5절에서 수동 전달 한 번과 최종 disabled 상태를 확인합니다.
미래 예약 시각의 실행을 검증하는 것은 아닙니다. 같은 터미널과 실제 반환 dispatch ID를 사용합니다.

## 1. 가장 작은 trigger 선택

하루 뒤의 **비활성화된 일회성 timer**를 만들고 실습 중 수동으로 트리거합니다.
그러면 수업 내내 반복 작업이 조용히 실행되는 일을 피할 수 있습니다.
이 첫 회차에서는 지정된 합성 정책 질문만 시험하고 Teams/GitHub event source를 연결하지 않습니다.

Routine은 기본적으로 **agent identity**를 사용합니다.
그 identity에는 필요한 모델·도구 권한이 이미 있어야 하며 개발자의 로컬 로그인으로 대신되지 않습니다.
creator/delegated-user identity는 다른 선택 계약이며 여기서는 선택하지 않습니다.

## 2. 명령과 값 확인

```bash
azd ai routine create --help
azd ai routine dispatch --help
azd ai routine run list --help
```

다음 단계에는 같은 터미널을 사용합니다.

```bash
printf '전체 프로젝트 endpoint: '
read -r PROJECT_ENDPOINT
printf '승인된 기존 Responses agent 이름: '
read -r AGENT_NAME
printf '새 routine 이름 (<내 prefix>-timer-ko): '
read -r ROUTINE_NAME
WHEN=$(python -c 'from datetime import datetime, timedelta, UTC; print((datetime.now(UTC) + timedelta(days=1)).isoformat())')
```

대상은 모델 배포 이름이 아니라 승인된 실제 agent입니다. 실제 호출 버전을 기록하며 mutable target을 불변 benchmark로 취급하지 않습니다.

## 3. Disabled 상태로 생성

담당자가 이 소유 routine과 비용을 승인한 뒤 실행합니다.

```bash
azd ai routine create "${ROUTINE_NAME:?Enter the owned routine name}" --trigger timer \
  --at "${WHEN:?Calculate a future UTC trigger time}" --agent-name "${AGENT_NAME:?Enter the approved target agent}" \
  --action agent-response --enabled=false --project-endpoint "${PROJECT_ENDPOINT:?Enter the full project endpoint}" --output json
azd ai routine show "${ROUTINE_NAME:?Enter the owned routine name}" \
  --project-endpoint "${PROJECT_ENDPOINT:?Enter the full project endpoint}" --output json
```

이름·agent·trigger·time zone과 `enabled: false`를 확인합니다.
이미 존재하는 routine에 `--force`로 생성하지 않습니다.
필수 값이 없으면 azd 실행 전에 멈춥니다. 새 터미널에서는 기록한 정확한 routine 이름과 project endpoint를 복구합니다.

## 4. 한 번 전달하고 비활성화

다음 호출은 과금 대상입니다. 미래 timer를 활성 상태로 남겨 두면 안 됩니다.
dispatch가 실패하더라도 **비활성화 명령을 실행한 뒤** 오류를 조사합니다.
disable을 dispatch와 `&&`로 연결하면 실패 시 정리가 생략되므로 그렇게 바꾸지 않습니다.

```bash
azd ai routine enable "${ROUTINE_NAME:?Enter the owned routine name}" \
  --project-endpoint "${PROJECT_ENDPOINT:?Enter the full project endpoint}" &&
azd ai routine dispatch "${ROUTINE_NAME:?Enter the owned routine name}" \
  --input "2026년 9월 국내 출장에서 170000원 호텔의 사전 승인 조건은?" \
  --project-endpoint "${PROJECT_ENDPOINT:?Enter the full project endpoint}" --output json
azd ai routine disable "${ROUTINE_NAME:?Enter the owned routine name}" \
  --project-endpoint "${PROJECT_ENDPOINT:?Enter the full project endpoint}"
azd ai routine run list "${ROUTINE_NAME:?Enter the owned routine name}" \
  --project-endpoint "${PROJECT_ENDPOINT:?Enter the full project endpoint}" --output json
azd ai routine show "${ROUTINE_NAME:?Enter the owned routine name}" \
  --project-endpoint "${PROJECT_ENDPOINT:?Enter the full project endpoint}" --output json
```

Enable이 실패하면 dispatch하지 않습니다. Disable과 재조회는 의도적으로 별도 실행합니다.
각 명령의 결과를 보관합니다. 마지막 `show`의 성공이 실패한 dispatch를 성공으로 바꾸지는 않습니다.

dispatch ID와 action correlation ID를 보관합니다. queued dispatch는 완료된 agent 응답이 아닙니다.
관찰한 CLI 버전의 `run list`는 실제 SDK 이력이 있는데도 `value: null`을 출력할 수 있습니다.
그 CLI 모양만으로 미실행이라고 판단하지 않습니다.
read-only SDK helper로 정확히 반환된 dispatch를 확인합니다.

```bash
printf '반환된 dispatch ID: '
read -r DISPATCH_ID
python scripts/workshop.py --language ko routines inspect --name "$ROUTINE_NAME" --dispatch-id "$DISPATCH_ID" --label routine-result
```

helper는 **전달**을 확인합니다. 답변 내용이나 미래 timer 발화를 증명하지 않습니다.
관찰된 agent-identity routine은 완료됐지만 반환된 response ID는 나중 조회에서 404였습니다.
그 경계를 기록하고 agent를 직접 호출해 대체 답변을 routine 답변처럼 제시하지 않습니다.
`--verify-response`와 새 label은 명시적 response 검증을 시도하고 원래 response가 없으면 명확히 실패합니다.
모델 요청을 반복하지 않습니다.
일치하는 run의 상태와 반환된 답변/오류를 확인합니다.
다시 list할 때도 같은 run을 보기 위한 것이지 다른 dispatch를 만들기 위한 것이 아닙니다.
실습을 떠나기 전에 최종 routine 상태가 disabled인지 확인합니다.

## 5. 기록·정리

생성 설정, 정확한 dispatch/run ID, 보고된 대상 버전, 답변/오류 또는 미검증 상태,
최종 disabled 상태를 보관합니다.
누락된 run 결과를 직접 agent 호출로 대체해 routine 성공이라고 부르지 않습니다.

다른 workflow가 사용하지 않는지 확인한 뒤 현재
`azd ai routine delete --help` 문법이나 프로젝트의 routine 관리 페이지로 소유 routine만 제거합니다.
routine 삭제는 대상 agent, 모델, Search service, 과거 run 근거를 삭제하지 않습니다.

## 복구와 경계

과거 timer 시각, 지원되지 않는 trigger, 권한 부족, CLI/SDK shape 차이를 구분합니다.
원래 dispatch를 다시 보내지 않고 그 이력부터 읽습니다.
비활성화로 취소된 미래 timer 시도는 성공한 예약 실행으로 집계하지 않습니다.
수동 전달 성공과 반복 자동화 성공도 구분합니다.

| 증상 | 대응 |
|---|---|
| 알 수 없는 `routine` 명령 | 호환되는 azd/extension 조합을 준비하고 멈춥니다. 공유 도구를 무작정 모두 업그레이드하지 않습니다 |
| CLI가 `created_at` 또는 다른 응답 필드를 decode하지 못함 | 쓰기는 성공했을 수 있습니다. 다시 create하기 전에 오류를 보존하고 show/list를 확인합니다 |
| 대상 모델/도구 403 | routine의 실제 dispatch identity와 대상 권한을 확인합니다 |
| 아직 일치하는 run이 없음 | 같은 dispatch의 비동기 이력을 관찰합니다. 반복 과금 run을 만들지 않습니다 |
| 잘못된 trigger 또는 agent | 먼저 비활성화하고 소유 definition을 검토한 뒤 명시적으로 승인된 변경을 수행합니다 |

반복 schedule, GitHub issue trigger 또는 Teams event는 별도 실습과 동의/비용 검토, 정리 담당자가 필요합니다.
여기서는 자동으로 활성화하지 않습니다.

**다음:** [C 모듈 선택](../../paths/c-advanced.md) 또는 [Lab 11 인계](../11-capstone.md).
[공식 routine lifecycle](https://learn.microsoft.com/azure/foundry/agents/how-to/use-routines).
