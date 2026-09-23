# Routines: 예약·수동 전달·실제 답변을 구분하기

[English](../../../labs/extensions/routines.md) | **한국어**

**C 선택 · 2026-09-16 기준.** 처음에는 전용 agent와 미래 timer 하나만 사용합니다.
설정 생성, queue 접수, 전달 완료, 답변 확인, 예약 시각 실행은 다른 단계입니다.

**준비:** 내 agent, 실제 프로젝트 endpoint, 예약·모델 비용·정리 승인.
**완료:** 원래 dispatch의 전달 이력과 검증 한계를 기록하고 timer를 비활성화/정리함.
**중단:** 실행 이력이 없다고 직접 agent를 호출한 뒤 Routine 결과로 바꾸지 않습니다.

**첫 회차:** 1–5절에서 수동 전달 한 번과 최종 disabled 상태를 확인합니다.
미래 예약 시각의 실행을 검증하는 것은 아닙니다. 같은 터미널과 실제 반환 dispatch ID를 사용합니다.

## 1. 가장 작은 trigger 선택

미래의 일회성 timer를 **disabled**로 만듭니다.
첫 실습에서는 recurring, GitHub event, 실사용 traffic을 동시에 추가하지 않습니다.
time zone, 예정 시각, 담당자와 비활성화 계획을 먼저 기록합니다.
기본 호출 주체는 agent identity이며 그 ID의 모델·도구 권한을 담당자가 준비합니다.
개발자의 로컬 로그인이나 별도 delegated-user 계약으로 대신하지 않습니다.

## 2. 명령과 값 확인

```bash
azd ai routine create --help
azd ai routine dispatch --help
azd ai routine run list --help
```

같은 터미널에서 설정 카드 값을 입력합니다.

```bash
printf '전체 프로젝트 endpoint: '
read -r PROJECT_ENDPOINT
printf '내 전용 agent 이름: '
read -r AGENT_NAME
printf '새 routine 이름 (<내 prefix>-timer-ko): '
read -r ROUTINE_NAME
WHEN=$(python -c 'from datetime import datetime, timedelta, UTC; print((datetime.now(UTC) + timedelta(days=1)).isoformat())')
```

현재 UTC에서 하루 뒤를 계산합니다. 영상 속 지난 날짜를 복사하지 않습니다.
대상은 모델 배포 이름이 아니라 승인된 실제 agent입니다. 실제 호출 버전을 기록하며 mutable target을 불변 benchmark로 취급하지 않습니다.

## 3. Disabled 상태로 생성

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

승인된 합성 입력 한 번만 보냅니다. 중간에 오류가 나도 비활성화 명령은 실행합니다.
Dispatch와 disable을 `&&`로 연결하면 실패 시 정리가 생략되므로 그렇게 바꾸지 않습니다.

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

dispatch/action correlation ID를 보관합니다.
관찰한 CLI 버전의 `run list`는 실제 SDK 이력이 있는데도 `value: null`을 출력할 수 있습니다.
그 모양만으로 미실행이라고 판단하지 않습니다.

```bash
printf '반환된 dispatch ID: '
read -r DISPATCH_ID
python scripts/workshop.py --language ko routines inspect --name "$ROUTINE_NAME" --dispatch-id "$DISPATCH_ID" --label routine-result
```

helper는 **전달**을 확인합니다. 답변 내용이나 미래 timer 발화를 증명하지 않습니다.
영문 agent-ID Routine은 Finished 이력이 있었지만 response ID 조회는 404였습니다.
`--verify-response`와 새 label은 원래 답변을 엄격하게 조회하며 불가하면 오류를 남깁니다.
모델 요청을 새로 보내지 않습니다.

## 5. 기록·정리

생성 설정, 정확한 dispatch/run ID, 보고된 대상 버전, 답변/오류 또는 미검증 상태,
최종 disabled 상태를 보관합니다.
다른 workflow가 사용하지 않는 내 routine만 현재 delete 명령으로 정리합니다.
삭제 전에는 `azd ai routine delete --help`를 확인합니다. 공유 agent/model은 지우지 않습니다.

## 복구와 경계

과거 timer 시각, 지원되지 않는 trigger, 권한 부족, CLI/SDK shape 차이를 구분합니다.
원래 dispatch를 다시 보내지 않고 그 이력부터 읽습니다.
비활성화로 취소된 미래 timer 시도는 성공한 예약 실행으로 집계하지 않습니다.
수동 전달 성공과 반복 자동화 성공도 구분합니다.

**다음:** [릴리스 운영](release-operations.md), [C 모듈](../../paths/c-advanced.md), [Lab 11](../11-capstone.md).
