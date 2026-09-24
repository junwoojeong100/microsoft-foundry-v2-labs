# 로컬 SDK 승인 게이트 모의 실험과 복구

[English](../../../labs/extensions/approval-recovery.md) | **한국어**

**선택 Preview · 호환성 확인일 2026-09-16.** Python 3.13,
`azure-ai-agentserver-core==2.1.0`, `azure-ai-agentserver-responses==2.2.0b1`의 준비된 환경을 사용합니다.
Lab 05, 핵심 배포 설정, 원본 데이터를 바꾸지 않습니다.

**실제 SDK 메커니즘이지만 작업은 미리 작성된 합성 예제입니다.**
모델·검색·평가·예약·지급·메일·실제 인가가 없습니다.
`synthetic-runtime-only`는 protocol label이며 Azure 모델 배포가 아닙니다.
국문 dev D03만 사용하고 holdout은 사용하지 않습니다.

**근거 상태:** 영문 stop/restart/continuation을 2026-09-16 이전 `gpt-5.6-luna` 판에서 실행했습니다.
Azure 실행이 아니었고 `gpt-6-sol` preset으로 다시 실행하지 않았습니다.

**첫 회차:** 아래 권장 첫 실행의 1–5단계만 진행하며 재시작·crash는 하지 않습니다.
로컬 완료 근거를 저장하고 본인 서버를 중지한 뒤 인계합니다. 아래 분기·유지보수 검사는 선택입니다.

**준비:** 전용 터미널 두 개와 [준비된 Hosted SDK 환경](developer-toolkit.md#hosted-sdk). 위 agentserver 버전도 정확히 맞아야 합니다.
**완료:** 같은 response/gate와 원래 output ID를 유지하며 `human_authorization: not-granted`인 결과를 확인함.
**중단:** checkpoint와 오류를 보존합니다. 게이트를 우회하거나 실제 승인으로 표시하지 않습니다.

<details>
<summary>Lab 05의 pending-review와 다른 점</summary>

실제 `@multi_turn_task`가 `FoundryStateStore`에 승인 요청을 저장하고 suspended 상태가 됩니다.
나중의 **모의 결정**은 새 input ID로 같은 승인 task를 재개합니다.
별도 background Response는 같은 response ID를 유지합니다.
완전한 메시지마다 `yield stream.checkpoint()`로 commit하고, 복구 시
`context.persisted_response`의 commit된 prefix를 확인해 원래 output ID를 재생성하지 않습니다.

commit되지 않은 단계는 다시 실행될 수 있으며 외부 업무 효과와 transaction으로 묶여 있지 않습니다.
따라서 외부 동작을 추가하지 않습니다. 승인 task와 Response task는 서로 다른 ID이고 명시적으로 연결됩니다.
모의 결정 제한은 downtime 포함 600초, 이후 합성 작업은 최대 2단계입니다.

</details>

## 권장 첫 실행

### 1. 전용 터미널 준비

두 터미널 모두 저장소 루트와 준비된 Python을 사용합니다.

```bash
export WORKSHOP_PYTHON="${WORKSHOP_PYTHON:-$PWD/.venv/bin/python}"
export OTEL_SDK_DISABLED=true
unset FOUNDRY_HOSTING_ENVIRONMENT FOUNDRY_PROJECT_ENDPOINT
unset AZURE_AI_PROJECT_ENDPOINT AZURE_AIPROJECT_ENDPOINT
unset APPLICATIONINSIGHTS_CONNECTION_STRING OTEL_EXPORTER_OTLP_ENDPOINT
unset OTEL_EXPORTER_OTLP_TRACES_ENDPOINT OTEL_EXPORTER_OTLP_LOGS_ENDPOINT
unset OTEL_EXPORTER_OTLP_METRICS_ENDPOINT
"$WORKSHOP_PYTHON" examples/resilient/workshop.py check
```

정확한 두 SDK 버전과 `azure_requests_sent: false`를 확인합니다.
Azure 로그인·구독 변경·`.env` loading·새 패키지 설치·cloud resource가 필요하지 않습니다.
변경은 전용 터미널 안에만 적용됩니다.

### 2. 로컬 server 시작

터미널 A:

```bash
"$WORKSHOP_PYTHON" examples/resilient/workshop.py --language ko --run-id first-pass serve
```

`http://127.0.0.1:8093`, PID, mode, state 경로를 확인하고 실행 상태로 둡니다.
`outputs/resilience/first-pass/sdk-state/`는 실제 SDK 저장소입니다.
run별 lock으로 중복 server/정리를 막으며 이 폴더를 다른 server와 공유하지 않습니다.
인증 없는 실습 port를 외부에 노출하지 않습니다.

port가 사용 중이면 다른 프로세스를 중지하지 않습니다.
이번 실행의 **모든 명령**에 별도 `--port`를 명시합니다.
client는 요청 전 server의 workshop/run ID를 확인합니다.

### 3. Response 생성 후 일시 정지 확인

터미널 B:

```bash
"$WORKSHOP_PYTHON" examples/resilient/workshop.py --language ko --run-id first-pass start
"$WORKSHOP_PYTHON" examples/resilient/workshop.py --language ko --run-id first-pass status
```

실제 request:

```json
{"model":"synthetic-runtime-only","input":"D03","store":true,"background":true,"stream":true}
```

첫 SSE output 이후 연결이 끊겨도 저장된 background Response의 결정/취소가 아닙니다.
client가 server의 commit 증거를 기다린 뒤 `initial-response.json`을 저장합니다.
아래 실제 필드 이름을 확인합니다. ID와 hash는 실행마다 다릅니다.

| `status`의 필드 | 정지 상태 |
|---|---|
| `mode` | `local-sdk-prewritten-synthetic` |
| `response_id` | 이 버전에서 보통 `caresp_`로 시작하는 SDK 발급 ID |
| `response_status` | `in_progress` |
| `approval_task_id` | `approval-` 뒤에 같은 response ID가 붙은 값 |
| `approval_status` | `awaiting_simulated_decision` |
| `gate.decision` | `null` |
| `gate.gate_id`, `gate.request_input_id`, `gate.request_sha256` | 저장된 결정 binding 값 |
| `output_ids` | `approval_request`에 대한 SDK 발급 메시지 ID 하나 |
| `human_authorization` | `not-granted` |

아무 결정도 주지 않으면 스스로 승인하지 않습니다.
SDK test는 승인 task의 실제 `suspended` 상태도 검사합니다.
전체 요청은 메모리 변수나 가정한 `TaskContext.metadata` 표면이 아니라 `FoundryStateStore`에 저장됩니다.

### 4. 모의 결정 후 완료 확인

본인이 실행하거나 AI가 실행해도 **실제 사람 승인 증거가 아닙니다.**

```bash
"$WORKSHOP_PYTHON" examples/resilient/workshop.py --language ko --run-id first-pass decide \
  --decision approve --confirm-simulated-decision
"$WORKSHOP_PYTHON" examples/resilient/workshop.py --language ko --run-id first-pass wait \
  --timeout-seconds 30
```

결정 결과는 `status: simulation_approved`, `decision.kind: simulated`, 보통 `decision.entry_mode: resumed`를 가집니다.
원래 `task_id`, request digest, gate ID를 유지합니다.
SDK의 `input_id` / `if_last_input_id` 순서 사전 조건과 state-store ETag guard가 stale/경합 결정을 거부합니다.
동의 누락, 잘못된 binding, 만료, 이미 내린 결정의 교체는 작업을 열지 않습니다.

`wait`는 `GET /responses/{response_id}`가 `status: completed`를 반환해야 통과합니다.
실제 completed Response의 **3개 순서 있는 메시지**
`approval_request`, `synthetic_review_packet`, `human_handoff_required`를 검사합니다.
원래 payload/ID를 유지하고 전체 output ID가 서로 달라야 합니다.
결과는 `preserved_output_ids`와 `final_output_ids`를 보고하며 전체 최종 Response는
`completed-response.json`에 저장됩니다.

완료 후에도 `human_authorization: not-granted`, `external_actions_performed: false`,
`quality_score: null`, `azure_execution_verified: false`입니다.
누락·변경·실패·취소는 이 검증을 통과할 수 없습니다.

### 5. 내 run 정리

A의 server만 Ctrl+C로 종료한 뒤 B에서:

```bash
"$WORKSHOP_PYTHON" examples/resilient/workshop.py --language ko --run-id first-pass cleanup \
  --confirm-delete-local-state
```

표시된 run의 SDK 작업 상태만 제거합니다. 원래 요청·응답·checkpoint는 남깁니다.
active lock, symlink, 모르는 파일, 소유 marker 누락을 거부합니다.
프로세스나 Azure resource를 강제로 삭제하지 않습니다.
정리한 run ID를 다시 쓰지 않습니다.
SDK multi-turn chain은 최종 turn 뒤에도 suspended 상태로 남습니다.
application 완료와 자동 chain 삭제를 혼동하지 않습니다.

## 첫 실행 이후 선택 분기

<details>
<summary>새 run 하나로 재시작·Linux 전용 crash·거절·만료 중 필요한 것만 선택합니다</summary>

### macOS/Linux의 정상 종료 후 재시작

```bash
# 터미널 A
"$WORKSHOP_PYTHON" examples/resilient/workshop.py --language ko --run-id resume-pass serve
```

```bash
# 터미널 B
"$WORKSHOP_PYTHON" examples/resilient/workshop.py --language ko --run-id resume-pass start
```

gate가 pending일 때 A에서 Ctrl+C를 누릅니다.
같은 `resume-pass serve` 명령과 변경 없는 소스/환경으로 A를 다시 시작합니다.
`start`를 다시 실행하지 않습니다.
SDK startup scanner는 저장된 Response로 다시 들어가며 대체 task를 만들거나 결정을 추론하지 않습니다.

```bash
"$WORKSHOP_PYTHON" examples/resilient/workshop.py --language ko --run-id resume-pass status
"$WORKSHOP_PYTHON" examples/resilient/workshop.py --language ko --run-id resume-pass decide \
  --decision approve --confirm-simulated-decision
"$WORKSHOP_PYTHON" examples/resilient/workshop.py --language ko --run-id resume-pass wait
```

request/gate/task ID가 변하지 않았고 pending gate에 여전히 명시적 모의 결정이 필요했는지 확인합니다.
최종 `checkpoint.json`은 `handler_is_recovery: true`를 기록합니다.
A를 중지하고 `--run-id resume-pass`로 같은 cleanup 명령을 사용합니다.

이 고정 SDK에서 정상 종료는 이전 SSE log를 닫습니다.
이전 event는 replay할 수 있지만 이 판은 재시작을 가로지르는 완전한 무손실 SSE tail을 주장하지 않습니다.
acceptance에는 최종 JSON Response와 저장된 checkpoint의 원래 ID를 사용합니다.
SDK test는 끊기지 않은 SSE replay와 수명 주기를 가로지르는 checkpoint recovery를 구분합니다.
종료 중 `TaskDeferred` future 메시지가 나올 수 있지만 그 문구만으로 성공/실패를 판단하지 않습니다.

### Commit 후 명시적 hard crash: Linux 전용

Linux, WSL 또는 Linux container용 준비 분기입니다.
이 판에서 Linux나 Hosted Azure에서 실행했다고 주장하지 않았습니다.
macOS에서는 hard-crash flag를 거부합니다.
협조적 로컬 재시작을 container/OOM/crash 동작의 증거로 취급하지 않습니다.

```bash
# Linux 터미널 A
"$WORKSHOP_PYTHON" examples/resilient/workshop.py --language ko --run-id crash-pass serve \
  --crash-after-checkpoint 1 --allow-owned-process-crash
```

```bash
# 터미널 B
"$WORKSHOP_PYTHON" examples/resilient/workshop.py --language ko --run-id crash-pass start
"$WORKSHOP_PYTHON" examples/resilient/workshop.py --language ko --run-id crash-pass decide \
  --decision approve --confirm-simulated-decision
```

승인 요청과 첫 작업 메시지의 commit 뒤 `crash-checkpoint.json`을 쓰고 **자기 PID만** exit 86으로 끝냅니다.
HTTP trigger는 없으며 두 flag가 모두 필요합니다. `crash-once.json`이 반복 crash를 막습니다.

```bash
"$WORKSHOP_PYTHON" examples/resilient/workshop.py --language ko --run-id crash-pass serve
```

같은 run/state를 사용해 crash flag 없이 A를 다시 시작합니다.

```bash
"$WORKSHOP_PYTHON" examples/resilient/workshop.py --language ko --run-id crash-pass wait \
  --timeout-seconds 120 --verify-crash-checkpoint
```

새 Response나 결정을 만들지 않습니다. 원래 두 output ID/payload와 response/task를 유지하고
남은 작업 메시지 하나만 추가되어야 합니다.
timeout이면 근거를 남기며 lease·snapshot·ID를 수정하지 않습니다.
끝나면 A를 중지하고 `crash-pass`를 정리합니다.

### 거절·만료·오류

새 run에서 `--decision reject --confirm-simulated-decision`은 요청과 `simulation_rejected`만 생성합니다.
결정을 주지 않고 만료되면 `approval_timeout` 실패이지 성공 답변이 아닙니다.
timeout은 `1..900`, 단계 지연은 `0..5`초, client 대기는 최대 120초입니다.

client 단절/대기 timeout 뒤에는 `status`를 쓰고 새 `start`를 보내지 않습니다.
ID 저장 전 생성 실패는 결과 미상입니다. 근거를 보관하고 내 server를 중지·정리한 뒤 새 run을 명시적으로 사용합니다.
손상된 상태·hash 변경·SDK 불일치·저장 오류는 대체 모델/provider/fixture를 고르는 이유가 아닙니다.

</details>

## 로컬 검증과 Hosted의 별도 경계

<details>
<summary>유지보수·SDK 참고 — 학습자의 다섯 단계 완료에 필요한 추가 실습이 아닙니다</summary>

```bash
PYTHONPATH=src "$WORKSHOP_PYTHON" -m unittest tests.test_resilience tests_sdk.test_resilience
"$WORKSHOP_PYTHON" -m ruff check src/foundry_workshop/resilience.py examples/resilient \
  tests/test_resilience.py tests_sdk/test_resilience.py
"$WORKSHOP_PYTHON" -m compileall -q src/foundry_workshop/resilience.py \
  examples/resilient tests/test_resilience.py tests_sdk/test_resilience.py
```

SDK 테스트는 실제 file provider, host 시작·종료, multi-turn 순서, checkpoint 저장, recovery callback,
원래 output ID를 사용합니다. 이 ASGI 계약 테스트는 network 연결을 막습니다.
테스트마다 새 SDK registry를 쓰고 이전 실행의 file lock을 해제하므로 메모리가 영구 저장소처럼 보이지 않습니다.
이는 **로컬 계약 결과**이지 Linux hard crash 실행, Hosted 배포 결과, 평가 점수가 아닙니다.

**로컬 근거, 2026-09-16:** 대상 테스트 27개가 모두 통과했습니다.
실제 macOS loopback server도 승인 대기 상태에서 정상 종료·재시작한 뒤 명시적인 모의 결정을 받았습니다.
같은 response/task ID로 완료됐고 서로 다른 output 3개와 원래 commit된 output이 보존됐습니다.
사람 승인은 `not-granted`로 남았습니다. hard crash나 Azure 실행은 아니었습니다.

core 2.1.0의 context는 sentinel을 반환하므로 `return await ctx.exit_for_recovery()`를 사용합니다.
Responses context는 제어 신호를 발생시키므로 `await context.exit_for_recovery()`입니다.
테스트는 승인 turn을 receipt 기록 직후 중단하고, 시작 시 복구가 두 번째 receipt를 쓰지 않는지도 확인합니다.
다른 SDK 버전의 idiom을 검증 없이 옮기지 않습니다.

요청에는 dev dataset·질문·corpus·미리 작성한 작업의 hash를 기록합니다.
prompt/model/evaluator는 실행하지 않으므로 그 이력이 명시적으로 없습니다.
SDK Response ID는 모델 추론 응답 ID가 아닙니다.
corpus는 AI 모델이 검색한 것이 아니라 schema 검사와 fingerprint만 거칩니다.
실제 승인 서비스에는 인증된 reviewer, 인가 정책, 서비스 저장소, 만료·취소,
idempotent/transactional 외부 동작 경계가 별도로 필요합니다.
로컬 파일은 container 간 내구성을 증명하지 않습니다.
Linux hard-crash와 Hosted check는 별도로 기록해야 합니다.

</details>

## 구현 및 참고 자료

- [순수 계약과 lineage](../../../../src/foundry_workshop/resilience.py)
- [SDK host와 durable approval task](../../../../examples/resilient/server.py)
- [owned runner, client, cleanup](../../../../examples/resilient/workshop.py)
- [Human-in-the-loop approval step 추가](https://learn.microsoft.com/azure/foundry/agents/how-to/add-human-in-the-loop)
- [resilient agent 배포](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-resilient-agent)
- [Long-running agent API reference](https://learn.microsoft.com/azure/foundry/agents/concepts/long-running-agent-reference)
- [Maintained resilient streaming sample](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/bring-your-own/responses/resilient-streaming/src/resilient-streaming/main.py)

**다음:** [C 모듈](../../paths/c-advanced.md) 또는 [Lab 11 인계](../11-capstone.md).
`local-sdk-prewritten-synthetic`으로 보고하며 모델 품질·실제 승인·Hosted crash 복구로 표시하지 않습니다.
