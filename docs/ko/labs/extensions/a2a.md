# A2A 1.0: 별도 주소의 정책 전문 agent에 위임하기

[English](../../../labs/extensions/a2a.md) | **한국어**

**C 경로 · A2A 1.0 GA 계약 확인일 2026-09-16.**

**근거 상태:** 영문 짝 호출과 그 출력을 2026-09-16 이전 `gpt-5.6-luna` preset으로 실행했습니다(wire packet은 캡처하지 않음). `gpt-6-sol`로 다시 실행하지 않았습니다.

로컬 MAF 참여자 두 명은 A2A endpoint 통합이 아닙니다.
내 합성 전문 agent endpoint와 별도 relay agent를 연결합니다.

**준비:** B의 모델/agent 설정, 기존 프로젝트/모델 접근, 새 agent 두 개와 keyless A2A 연결 권한,
실제 호출 ID의 endpoint 접근, 비용 승인.
**완료:** 인증된 card가 1.0을 알리고 실제 caller 응답에 성공한 A2A 도구 호출이 포함됨.
**중단:** 0.3, 다른 agent, 익명 인증으로 바꾸지 않습니다.

**첫 회차:** 1–5절입니다. 필요하면 [azd 준비](developer-toolkit.md#azd-check)를 먼저 마칩니다.
Target → 연결 → caller 순서로 만들며 각 결과를 확인한 뒤 다음 쓰기를 수행합니다.

## 1. 계획

```bash
python scripts/workshop.py --language ko a2a plan
```

target/caller/connection은 내 prefix와 언어로 이름이 정해집니다.
target에는 동봉한 합성 정책과 지침만 들어갑니다.
공통 고정 SDK의 typed surface보다 새로운 필드는 명시적 REST 1.0 계약을 사용합니다.
전체 교육 환경의 SDK를 몰래 교체하지 않습니다.

## 2. 전문 agent와 incoming A2A

2–4단계는 **준비**에 적힌 두 agent, 연결, 모델 비용을 담당자가 승인한 뒤에만 실행합니다.
승인된 그 프로젝트에서 실행하며, 생성되는 객체는 내 prefix로 이름이 지정됩니다.

```bash
python scripts/workshop.py --language ko a2a target --confirm-create
python scripts/workshop.py --language ko a2a inspect
```

새 Prompt Agent 버전 하나를 만들고 공식 card/endpoint patch를 적용합니다.
Python 목록에 다른 로컬 agent를 추가하는 것만으로 incoming A2A가 구성되지 않습니다.
실제 버전·base path·연결 이름·소유 기록을 보관합니다.

card URL은 **`/agentCard/v1.0`**으로 끝납니다.
`supportedInterfaces`에 `protocolVersion: 1.0`, `protocolBinding: JSONRPC`,
정확한 내 base URL 조합이 있어야 합니다.
0.3도 함께 표시될 수 있지만 1.0을 명시적으로 선택합니다.
인증된 card 읽기는 모델 호출과 별도입니다.

이 경로는 현재 text/non-streaming JSONRPC입니다.
protocol을 지정하지 않으면 오래된 0.3 동작이 선택될 수 있으므로 이 모듈은 그 기본값에 의존하지 않습니다.
target endpoint는 불변 버전 URL이 아니므로 실험 중 추가 target 버전을 거부합니다.

## 3. keyless 연결

반환값과 설정 카드의 값을 같은 터미널에 넣습니다.

```bash
printf '전체 프로젝트 endpoint: '
read -r PROJECT_ENDPOINT
printf 'target 결과의 target_base: '
read -r A2A_BASE
printf 'target 결과의 connection_name: '
read -r A2A_CONNECTION
azd ai connection create "${A2A_CONNECTION:?Use the returned connection name}" --kind remote-a2a \
  --target "${A2A_BASE:?Use the returned target base}" --auth-type project-managed-identity \
  --audience https://ai.azure.com --project-endpoint "${PROJECT_ENDPOINT:?Enter the full project endpoint}"
```

대상은 card URL이 아니라 **A2A base path**입니다.
빈 값은 azd 실행 전에 차단됩니다. 보호 문법을 제거하지 말고 실제 반환값을 복구합니다.
`--force`나 API key를 사용하지 않습니다.
담당자가 연결의 실제 ID와 target agent/project의 필요한 접근 권한만 확인합니다.
로그인한 학습자와 서비스 ID를 같은 주체로 보지 않습니다.

## 4. relay 생성·호출

```bash
python scripts/workshop.py --language ko a2a caller --confirm-create
```

기록된 caller 버전과 의도한 target을 확인한 뒤 추론을 승인합니다.

```bash
python scripts/workshop.py --language ko a2a invoke --label a2a-first --confirm-cost
```

caller는 `type: a2a`, `a2a_version: 1.0`이며 모델 요청은 기록된 실제 caller 버전을 참조합니다.
위임 없이 생성한 답변을 완료로 계산하지 않습니다.

`outputs/a2a-runs/a2a-first/`의
`request.json`, `binding.json`, 전체 `response.json`, `summary.json`을 확인합니다.
성공한 A2A call item, 원문 정책 ID, caller/target 버전과 반환 model/request metadata를 유지합니다.
caller 사용량만 있으면 target 사용량을 만들어 더하지 않습니다.

서비스는 GA 설정에도 `a2a_preview_call`이라는 기존 event 이름을 반환할 수 있습니다.
helper는 실제로 수락된 `a2a/1.0` 설정과 일치하는 target output을 확인하고 원래 event 이름을 남깁니다.
이것을 wire packet을 캡처한 프로토콜 검증이라고 주장하지 않습니다.

## 5. 검토·정리

card는 기능 설명이지 사용 권한이 아닙니다. 성공한 위임도 예약·승인·지급 권한을 주지 않습니다.
소유/응답 근거를 보관하고 참조 확인 후 새 caller → 연결 → target만 담당자가 정리합니다.
공유 모델과 프로젝트는 삭제하지 않습니다. Foundry의 A2A task/context 보존은 별도 서비스 정책입니다.
agent 삭제가 보존된 모든 record의 영구 삭제를 의미한다고 주장하지 않습니다.

## 복구

| 증상 | 확인 |
|---|---|
| card 401/403 | 실제 caller ID와 Foundry endpoint-access role을 확인합니다 |
| 일치하는 1.0 JSONRPC interface 없음 | 최상위 version field를 가정하지 말고 `supportedInterfaces`를 검사합니다. downgrade 금지 |
| 추가 target 버전 감지 | 전용 target을 고정하거나 새 실험을 시작합니다. endpoint가 어느 버전을 제공했는지 추측하지 않습니다 |
| 연결 target 불일치 | 전체 base path와 프로젝트를 비교합니다. 다른 팀 agent를 가리키지 않습니다 |
| 응답에 A2A call 없음 | raw output을 실패한 통합 검사로 보존합니다. 위임 성공으로 기록하지 않습니다 |
| typed SDK symbol 미지원 | 이 실습의 문서화된 REST 경로나 독립적으로 검증된 SDK 환경을 사용합니다. protocol fallback 금지 |

**다음:** [Memory](memory.md), [C 모듈](../../paths/c-advanced.md), [Lab 11](../11-capstone.md).
[Incoming A2A](https://learn.microsoft.com/azure/foundry/agents/how-to/enable-agent-to-agent-endpoint) ·
[A2A 도구 연결](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/agent-to-agent).
