# Lab 09. Trace, 운영 게이트, 비용과 정리

[English](../../labs/09-operations.md) | **한국어**

**완료 목표:** 한 번 잘 답한 데모를 운영 가능한 시스템으로 착각하지 않고, 다음 판단의 근거를 남깁니다.

**내 구간 바로 열기:** [A — 기존 결과 네 항목](#path-a) · [B — 이력·정리](#path-b) · [학습 경로](../paths.md)

## 시작 전

**이번 순서:** A는 브라우저 네 확인과 정리 목록을 완료합니다. B는 본인 이력을 대조하고 matrix 명령은 심화 워크북 이후에만 씁니다.

**준비물:** A: 본인 에이전트와 버전, 증거 파일. B: 본인 output label과 Lab 03 B의 `response_id`. 담당자가 Application Insights를 연결하고 추적 읽기 권한을 주었어야 하며, 그렇지 않으면 미확인으로 기록합니다.

**다음으로 갈 기준:** 사용 버전·근거·비용·본인 정리 대상을 구분하며 공유 리소스를 삭제하지 않습니다.

**막히면:** 추적 근거가 없다면 미확인이지 오류 0개가 아닙니다. 캡처를 위해 모델 호출을 반복하지 않습니다.

[한 번만 하는 준비와 학습자 파일](../setup.md).

<a id="path-a"></a>

## A. 브라우저 — 무엇을 관리해야 하나?

모델을 다시 호출하지 말고 **본인의 기존 결과**로 다음 네 항목을 확인합니다.

1. 왼쪽 메뉴의 **에이전트**에서 Lab 03의 본인 에이전트를 엽니다. **세부 정보** 탭에서 이름과 활성 버전(`최신(Version N)`)을
   Lab 07에서 평가한 버전과 대조합니다.
2. **플레이그라운드** 탭에서 **모델**(`gpt-6-sol`)·**지침**·**도구**·**지식**을 확인합니다. 기본 A 경로에서는 **지침**에 합성 정책 6개가 들어 있고
   **지식**은 비어 있습니다. File Search나 IQ를 따로 선택했다면 그 연결을 적습니다.
   승인하지 않은 웹 검색·회사 연결이 없어야 합니다.
3. 본인의 agent **추적** 탭을 엽니다. 환경 담당자가 수업 전에 Application Insights를 연결해 두었어야 합니다. 본인의 Lab 03 또는 Lab 07 작업에서 저장된 요청 하나를 찾아 엽니다. `invoke_agent <agent>:<version>`과 자식 `chat` span을 찾습니다. `execute_tool web.run` span은 그 요청이 Web search 도구로 실행됐다는 뜻입니다(예: 도구를 제거하기 전 버전). tracing이나 권한을 사용할 수 없으면 `실제 추적 근거 또는 조회할 수 없을 때 추적 미확인:`에 `추적 미확인: <이유>`를 적습니다. 이 확인을 위해 새 메시지를 보내지 않습니다.
   목록은 **날짜 범위** **어제**(지난 1일)로 열립니다. 더 이전 요청은 **7일**을 고릅니다. 2026-09-25에 2026-09-24 브라우저 agent로 확인했을 때 연 추적마다 `invoke_agent <agent>:2`와 자식 `chat` span이 있었습니다.
   그다음 본인의 6행 평가표와 `workflow-review.txt`를 열고 위치를 적습니다. 이 평가표는 수동 검토이며, Lab 07의 선택 Foundry 평가는 별도 실행입니다.
4. [정리 체크리스트](../reference/cleanup.md)로 본인 agent, 실습 중 만들어진 모델 배포(예: Lab 03의 `text-embedding-3-large`),
   선택 파일/chat base, 직접 만든 평가 데이터 세트와 평가, session을 목록화합니다.
   공유 서비스는 **담당자 관리**로 표시하고 잔여 비용과 승인된 자산별 중지/삭제 담당자를 확인합니다.

학습자 ZIP의 빈 `operations-checklist.txt`에 네 결과를 채웁니다.

**화면 확인:** `operations-checklist.txt`의 1–4번에 본인 agent와 버전, 결과 위치, 본인이 소유한 자산,
**담당자 관리**로 표시한 공유 서비스, 남는 비용의 담당자가 적혀 있습니다.
**A 완료:** [Lab 11 A](11-capstone.md#path-a)로 이동합니다. 새 모델·trace·matrix 명령은 필요 없습니다.

<details>
<summary>선택 추가 검토 — 본인 권한으로 보이는 자산만. A 단계가 아닙니다</summary>

| 관찰 대상 | 직접 확인할 질문 |
|---|---|
| 에이전트·버전·assets | 지금 사용자가 호출하는 버전은 어느 것인가? |
| 모델 배포·quota | 모델 이름, 실제 배포, 용량 제한을 구분했는가? |
| 도구·지식 연결 | 어느 데이터와 외부 시스템에 접근하는가? |
| 평가 결과 | 어떤 데이터와 evaluator로 측정했는가? |
| 추적/모니터링 | 실패한 요청의 처리 흐름을 찾을 수 있는가? |
| 비용·사용량 | 모델뿐 아니라 Search·session·로그 비용도 있는가? |
| 보안/거버넌스 설정 | 누가 호출·변경·배포·승인할 수 있는가? |

기존 종합 랩의 Control Plane 관점을 이 표로 통합했습니다.
Fleet/관리 메뉴가 보이지 않으면 역할 범위상 정상일 수 있습니다.
전체 구독 권한을 추가하는 것이 학습의 목표가 아닙니다.

</details>

<details>
<summary>선택, 담당자 준비 필요: 에이전트가 이미 한 답변을 추적에서 평가하기</summary>

Lab 03·07에서 기록된 대화를 새 에이전트 호출 없이 채점합니다. judge 호출 비용은 발생합니다.

1. 에이전트의 **평가** 탭에서 **만들기**를 선택합니다. 저장한 **버전**만 선택한 **에이전트**([Lab 07 A 4단계](07-evaluation.md#path-a)의 2번과 같음),
   **개별 턴**, **일회성**을 유지합니다.
2. **데이터**에서 **기존 추적**을 선택합니다. **추적 번호**(평가에 포함할 최대 추적 수) `15`와 **시간 범위** **7일**을 유지하면
   대화가 추적 ID·응답 ID와 함께 표시됩니다. 마지막 질문 뒤 3–5분 기다립니다.
   5분 뒤에도 대화가 보이지 않으면 `operations-checklist.txt`의 3번에 `추적 평가 실행 안 함: 추적 없음`이라고 적고 여기서 멈춥니다.
   추적을 만들려고 에이전트에 새로 질문하지 않습니다.
3. **설정이 완료되지 않음** 안내가 프로젝트 관리 ID에 Application Insights의 **모니터링 읽기 권한자** 역할을 요구하면
   멈추고 담당자에게 요청합니다. **해결**을 선택하지 않습니다. 역할 할당을 바꾸는 동작입니다.
4. 안내가 없다면 **다음**을 선택하고 Lab 07 A 4단계처럼 **조건**을 정합니다. **판단 모델**을 열어 **배포** 아래 `gpt-6-sol-judge`를 고릅니다
   (기본값이 다른 배포일 수 있음). 안전·에이전트는 **모두 제거**, 근거성·유창성은 제거하고, 관련성·일관성은 이름을 `Relevance`, `Coherence`로
   바꿔 남깁니다. **새 평가자 추가** → **Task-Adherence-Evaluator-(Preview)** → **확인**을 선택합니다. **다음**을 선택하고 이름을 `<내 prefix>-traces`로 입력한 뒤 **제출**합니다.
5. 실행이 **완료됨**이 되면(약 2분) 엽니다.

![2026-09-24 국문 녹화: 각 추적의 query에 에이전트 지침이 포함됨](../../assets/g6sol-20260924-ko/screenshots/KP09-105-traces-results-2.webp)

**화면 확인:** **전체 메트릭 결과**에 Relevance·Coherence·TaskAdherence가 통과 수 / N(내 대화 수, 최대 15)으로 표시되고, 각 행의 `query`는 질문 앞에
내 에이전트의 **지침**(정책 6개 포함)으로 시작합니다. 그래서 질문만 보낸 Lab 07 A 데이터 세트 실행과 달리 TaskAdherence가 통과할 수 있습니다.
2026-09-24 국문 녹화는 대화 15개에서 세 평가자 모두 15/15였습니다.

평가 페이지의 **되풀이 설정**(추적 평가가 한 번 성공한 뒤 활성화)은 **라이브 트래픽**에 대한 **예약됨** 실행을 **시간별** 간격,
무작위 또는 지능형 샘플링, 실행당 최대 추적 수로 제공합니다. 2026-09-23에는 일정을 저장하자마자 첫 실행이 시작되었고,
매 실행이 마지막 1시간이 아니라 최근 7일(일회성 실행의 **시간 범위**)에서 표본을 뽑아 이전 대화를 다시 채점했습니다.
**연속**은 사용할 수 없었고, 데이터 세트 기반 평가에서는 같은 대화상자가 **기존 데이터**에 대한 **예약됨**을 제공합니다.
평가 페이지의 **일시 중지**로 일정을 멈춥니다. 되풀이 실행은 별도 비용 승인과 일시 중지할 담당자가 필요합니다.

</details>

<a id="path-b"></a>

## B. 코드 — 실행 이력 연결과 추적 상태 기록

### 1. 로컬 이력부터 찾기

`outputs/<label>/manifest.json`과 `responses.jsonl`에서 다음 값을 찾습니다.

- 실행과 질문: `run_id`, `case_id`.
- 지침·데이터·코드·근거: hash와 버전.
- 요청: `response_id`, `request_id`, 실제 응답 모델.
- 검색: provider, 문서 ID, IQ references/activity.
- 결과: 정상/오류, token usage, latency.

사용한 실행 label과 ID를 `outputs/learner-notes-ko/operations-checklist.txt`의 3번에 적습니다.

**화면 확인:** 성공한 모든 응답 행에 `response_id`가 있고, 오류 행은 오류 필드를 유지한 채 그대로 집계됩니다.
Tracing을 설정하지 않았다면 `trace_id`는 `null`, `trace_export`는 `not-configured`로 남습니다.
response ID가 저절로 Azure Monitor trace가 되지는 않습니다.

### 2. Lab 03 B의 서버 측 trace 검색

포털 **추적** 검색을 열고 `outputs/learner-notes-ko/prompt-agent-invoke.json`의 `response_id`를 붙여 넣습니다. Application Insights가 연결되어 있고 접근 권한이 있으면 일치하는 추적 근거를 기록합니다. 사용할 수 없으면 `operations-checklist.txt`의 `실제 추적 근거 또는 조회할 수 없을 때 추적 미확인:`에 `추적 미확인: <이유>`를 적습니다.

![2026-09-25 국문 녹화: Lab 03 B response_id로 추적을 검색하면 한 행이 나옴](../../assets/review-refresh-20260925/KP09-201-trace-search.webp)

![2026-09-25 국문 녹화: 추적을 열면 invoke_agent와 자식 chat span이 보임](../../assets/review-refresh-20260925/KP09-202-trace-detail.webp)

**화면 확인:** 자식 `chat gpt-6-sol-2026-09-22` span이 있는 `invoke_agent <your agent>:<version>` span 하나를 확인합니다.
자식 span의 input/output token은 `prompt-agent-invoke.json`의 `usage`와 같습니다. 추적 근거로는 response ID가 아니라 trace 또는 operation ID를 기록합니다.
2026-09-24 확인(영문·국문)에서는 invoke가 `store: false`였어도 각 관리형 agent 호출이 약 3분 안에 나타났습니다.
2026-09-25 녹화에서는 언어마다 정확히 한 행이 나왔고, token 열은 `usage`와, trace ID는 Application Insights `operation_Id`와 같았습니다.
5분 뒤에도 아무것도 보이지 않으면 더 요청하지 말고 **추적 미확인**으로 기록합니다.

Lab 04와 05의 로컬 MAF 실행은 Python process에서 실행되므로 Foundry server-side agent trace를 만들지 않습니다. Client-side tracing은 별도 선택 설정입니다.
같은 확인에서 Responses API를 직접 호출한 명령(`model`, `answer`, `maf`, `workflow`, `collect`)은 서버 측 span을 전혀 남기지 않았고, 관리형 agent 호출만 남겼습니다.

### 3. 실제 실패 또는 전체 통과 결과 설명

기존 dev 응답을 사용합니다. 모델/요청 오류·도구 오류·근거 누락·잘못된 규정 적용을 구분합니다.
`operations-checklist.txt`의 3번에 서비스마다 한 줄씩 적습니다. 예:
`모델: 내 Azure CLI 사용자, response resp_…` · `Search: 내 Azure CLI 사용자, prefix mfv2-…` · `Hosted: 미실행`.
모두 통과했다면 그 사실과 남은 한계를 기록하며 실패를 만들지 않습니다.
변경은 [Lab 07](07-evaluation.md#path-b)의 dev로만 검토하고 노출된 holdout은 사용하지 않습니다.

### 4. 정리 목록 출력

```bash
python scripts/workshop.py cleanup-plan
```

이 명령은 **로컬 소유권 파일만 읽으며 Azure를 조회하거나 삭제하지 않습니다**.
`operations-checklist.txt`의 4번에 본인 객체·공유 서비스·승인된 담당자 작업·남은 비용을 구분해 적습니다.

| 출력 | 기록할 내용 |
|---|---|
| `search_ownership.objects` | 이 복사본의 `outputs/azure-objects.json`에 기록된 Search 객체. 현재 cloud 상태를 확인한 것은 아님 |
| `search_ownership: null` | 로컬 소유권 파일이 없음. Lab 06 미실행이면 그렇게 적고, 객체를 만들었다면 담당자와 대응하는 ledger를 복구. 임의로 만들지 않음 |
| `required_manual_inventory` | agent·모델 배포·Search·로그 등 담당자와 확인할 항목. 실제 존재하는 자원을 조회한 목록이 아님 |

**화면 확인:** `deletes_resources: false`는 삭제한 것이 없다는 뜻입니다. Ledger가 없거나 객체 목록이 비어 있어도
**cloud 자원이나 잔여 비용이 없다는 증거는 아닙니다**.
별도로 승인된 작업은 [정리](../reference/cleanup.md)를 따릅니다.

**B 완료:** 본인 이력·실패/전체 통과 검토·정리 목록을 저장했습니다.
[Lab 11 B](11-capstone.md#path-b)로 이동합니다. 추적이 준비되지 않았다면 **추적 미확인**으로 기록합니다.
이 기본 단계를 마치려고 Hosted를 배포하거나 새 모델 요청을 보내지 않습니다.

<details>
<summary>추적 포인터(선택, 핵심 경로에 새 코드 없음)</summary>

Prompt/Hosted agent의 서버 측 tracing은 프로젝트에 Application Insights를 연결하면 코드 변경 없이 시작됩니다. Response ID 또는 Trace ID로 검색할 수 있습니다. https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup

로컬 MAF agent의 span이 필요하면 별도 client-side instrumentation이 필요합니다. 로컬 response ID를 서버 trace로 바꾸어 적지 않습니다.

Log Analytics Reader가 있는 practitioner는 같은 조회를 read-only Application Insights query로 실행할 수 있습니다
(2026-09-24 확인에 사용한 query):

```text
dependencies
| where timestamp > ago(24h)
| where tostring(customDimensions["gen_ai.response.id"]) == "<response_id>"
| project timestamp, name, success, operation_Id,
    agentId = tostring(customDimensions["gen_ai.agent.id"]),
    inputTokens = toint(customDimensions["gen_ai.usage.input_tokens"]),
    outputTokens = toint(customDimensions["gen_ai.usage.output_tokens"])
```

Lab tenant용 token을 사용합니다. Azure CLI 계정이 여러 개이면 기본 계정을 쓰는 query 도구가 `InvalidTokenError`로 실패할 수 있습니다.

</details>

### 선택: 서버 측 tracing 준비

<details>
<summary>실제 telemetry는 준비된 agent·trace 접근·별도 호출/비용 승인이 필요합니다</summary>

강사는 프로젝트와 Application Insights 연결, 로그 보존·비용·접근 권한을 확인합니다.
[공식 tracing 설정](https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup)을
따라 서버 측 tracing을 활성화하고, 필요할 때만 로컬 client instrumentation을 더합니다.
이 저장소의 Hosted 진입점은 민감한 입력/출력 캡처를 기본 활성화하지 않습니다.

1. 준비된 에이전트에 합성 질문을 한 번 보냅니다.
2. 응답/대화/agent version을 기록합니다.
3. Foundry의 해당 tracing 화면에서 같은 실행을 찾습니다.
4. span의 부모/자식 관계, 모델·도구 호출, 지연·오류를 확인합니다.
5. 보존 정책과 권한을 확인하고, 필요 이상의 원문을 export하지 않습니다.


![2026-09-24 국문 녹화: 기록된 에이전트 요청의 추적](../../assets/g6sol-20260924-ko/screenshots/KP09-002-traces-2.webp)

**화면 확인:** 본인 에이전트의 **추적** 탭 → **추적 보기**에서 **날짜 범위**와 에이전트 버전을 먼저 확인합니다.
최신 행이라는 이유만으로 방금 보낸 요청이라고 판단하지 않습니다.


**화면 확인:** 검색칸(**추적 ID, 대화 ID 또는 응답 ID로 검색**)에 실제 추적 ID를 넣고 정확히 같은 ID의 행을 엽니다.
`response_id`, conversation ID, Trace ID는 서로 다른 값입니다.


**화면 확인:** 트리의 최상위 `invoke_agent`와 Metadata의 상태를 확인합니다.
포털에 보이는 일부 span 수를 응답 `model_calls`의 전체 호출 수로 바꾸어 적지 않습니다.

보호된 테이블은 일반 로그 조회 역할 외에 추가 권한을 요구할 수 있습니다.
트레이스가 늦게 도착하는 동안 호출을 반복해 비용을 늘리지 않습니다.
없으면 **미확인**으로 남기고 연결·exporter·역할·시간 범위를 점검합니다.


전체 요청의 존재는 아래 `benchmark monitor`로 별도 검증합니다.
포털의 부분 span 관측과 해당 요청의 성공/실패·사용량을 분리합니다.

### Trace 실패 설명

> “D03은 403이었다”에서 멈추지 말고, 사용자/프로젝트/agent identity 중 누가
> 어느 서비스에 접근하다 실패했는지 설명합니다.

모델 실패, 도구 실패, 검색 근거 부족, 잘못된 정책 적용을 구분합니다.
원문을 바탕으로 사람이 개선 이유를 검토한 뒤 [Lab 07](07-evaluation.md)의 dev 비교로 돌아갑니다.
자동 trace-to-dataset 기능은 Preview이므로 이 기본 경로의 필수 조건이 아닙니다.


서비스 실행 오류와 native 평가자의 낮은 점수를 같은 실패로 합치지 않습니다.

</details>

## 운영 승인 게이트

| 게이트 | 이번 실습에서 남길 증거 |
|---|---|
| 품질 | 전체 dev/holdout, 실패·누락 포함, 업무 기준과 의미 검토 |
| 권한 | 최소 권한, 사용자/런타임 identity 구분 |
| 데이터 | 합성/승인된 데이터만 사용, 적용 시점·출처·보존 기간 |
| 안전 | 실제 행동 도구의 서버 측 검증과 사람 승인 계획 |
| 비용 | 예상 호출량, Search 고정비, session 수, 로그 보존 |
| 릴리스 | 정확한 agent/model/prompt/dataset/code 버전 |
| 복구 | 이전 버전·되돌릴 설정·담당자 |

자동 최적화나 continuous evaluation을 기본으로 켜지 않습니다.
운영 중 샘플링·평가 비용·데이터 정책을 승인한 뒤 별도 설정합니다.
수업의 6문항 통과만으로 운영 배포를 승인하지 않습니다.

> ⛔ **승인된 선택 단계가 아니면 여기서 멈춥니다.** 아래는 선택/C 단계이며 유료 자원이나 추가 역할이 필요할 수 있습니다. A/B 학습자는 위의 다음 랩 링크로 이동합니다.

## C. 새 Hosted matrix의 Trace·Monitor 인수

<details>
<summary>심화 C 전용 — 입문 Lab 07이 아니라 Hosted matrix를 수집한 뒤 펼칩니다</summary>

**2026-09-15에 이전 `gpt-5.6-luna` preset으로 확인한 경로이며 `gpt-6-sol`로는 다시 실행하지 않았습니다.**
[평가 워크북](../reference/evaluation-workbook.md)에서 실제 만든 matrix label을 사용합니다.
`wf-candidate`는 입문의 `candidate`가 아닙니다. 모든 명령에서 본인의 실제 matrix label로 바꿉니다.

```bash
python scripts/workshop.py benchmark trace-plan --label wf-candidate
python scripts/workshop.py benchmark monitor --label wf-candidate
```

`trace-plan`은 로컬 KQL만 작성하며 Azure를 조회하지 않습니다.
`monitor`는 `.env`의 **AZURE_APPLICATION_INSIGHTS_APP_ID**와 명시적 구독을 사용해 실제 조회합니다.
credential은 지정된 구독/tenant로 scope를 고정하고
`https://api.applicationinsights.io/.default` 토큰으로 동일 Application Insights query API를 호출합니다.
2026-09-15 국문 실행(이전 `gpt-5.6-luna` 판)에서 일반 CLI query의 `InvalidTokenError`를 보존한 뒤 이 인증 경로를 수정했습니다.
다른 사용자·다른 App Insights로 바꾸는 우회가 아닙니다.
Application ID는 workspace ID나 instrumentation key와 다릅니다.
쿼리는 실행 전에 표시하고, 해당 run의 agent·기간·trace ID만 조회합니다.

조회는 `requests`에서 Foundry agent 이름을 찾습니다.
코드 내부 참여자 이름을 가진 `dependencies`를 같은 agent 이름으로 무작정 필터링하거나
부모 요청과 자식 span의 token/latency를 합산하지 않습니다.
현재 구현의 기본 trace gate는 root 요청의 성공/존재 검사이며, 개별 모델·도구·검색의 의미적 검토는 별도입니다.

누락·중복·실패 요청·미측정 duration은 인수 통과가 아닙니다.
한 번 확인한 정확한 immutable run의 receipt는 hash를 검증해 재사용하며,
새 live 조회를 한 것처럼 시간을 갱신하지 않습니다.

```bash
python scripts/workshop.py benchmark stop-session --label wf-candidate
```

이 명령은 그 label에서 만든 agent/version/session만 중지하고 상태를 다시 확인합니다.
공유 서비스·모델·평가 이력이나 persistent filesystem은 삭제하지 않습니다.
별도 smoke 세션은 자기 목록과 raw HTTP 기록으로 확인해 정리합니다.

### 선택: continuous evaluation

기본 batch/trace 검증과 다른 운영 기능입니다. 데이터 범위, sample 비율, 시간당 상한,
평가자 버전, 지속 비용, 비활성화 책임자를 먼저 승인합니다.
현재 [공식 recurring/continuous evaluation 안내](https://learn.microsoft.com/azure/foundry/observability/how-to/how-to-monitor-agents-dashboard#set-up-continuous-evaluation)를
확인하고 별도 rule을 구성합니다. 포털에서는 완료된 추적 평가의 **되풀이 설정**으로 이런 일정을 만듭니다
(2026-09-23 확인, [릴리스 운영](extensions/release-operations.md#2-제한된-반복-평가-설정) 참고).
한 번의 요청이 sampling되지 않았다고 모델을 반복 호출해
성공 화면을 만들지 않습니다. Rule enabled와 실제 평가 sample의 존재를 따로 기록합니다.
이 개정은 continuous evaluation을 자동으로 켜지 않습니다.

</details>

<details>
<summary>2026-09-24 gpt-6-sol 녹화 화면 더 보기 (참고; 그대로 재실행할 단계가 아님)</summary>

2026-09-24 `gpt-6-sol` / `2026-09-22` 국문 녹화 화면입니다. 본인의 리소스 이름·버전·결과를 사용합니다.

![2026-09-24 국문 녹화: 에이전트 세부 정보: 이름·활성 버전](../../assets/g6sol-20260924-ko/screenshots/KP09-001-details-2.webp)

**화면 확인:** 세부 정보에서 agent 이름과 활성 버전(여기서는 `최신(Version 2)`)을 평가표와 대조합니다. 모델은 **플레이그라운드** 탭에 표시됩니다.

![2026-09-24 국문 녹화: 모니터링 합계는 평가 정답 여부가 아님](../../assets/g6sol-20260924-ko/screenshots/KP09-003-monitor-2.webp)

**화면 확인:** 모니터링 합계는 요청·토큰 수이며 평가 정답 여부가 아닙니다.

![2026-09-24 국문 녹화: 소유 자산 정리 목록 (삭제하지 않음)](../../assets/g6sol-20260924-ko/screenshots/K09-001-cleanup-plan-2.webp)

**화면 확인:** 정리 목록은 본인 prefix로 기록된 Search 객체만 보여 주고 `deletes_resources: false`입니다. 나머지는 수동 점검 목록입니다.

[전체 액션 인덱스](../action-captures.md) · [녹화 영상](../video-summary.md)

</details>

## 반드시 정리하고 끝내기

Hosted matrix를 선택한 경우에만 본인 실행의 root trace와 세션 상태를 확인합니다.
A와 기본 B는 선택적인 telemetry 없이 정리 인계를 마칠 수 있습니다.
2026-09-24 `gpt-6-sol` 녹화는 agent 세부 정보·추적·모니터링 탭, 선택 추적 평가와 정리 목록을 포함하고, 2026-09-25 보충 녹화는 B의 `response_id` 추적 검색을 더합니다.
전체 요청의 확인을 모든 하위 span이 빠짐없이 export되었다는 의미로 확대하지 않습니다.
이미 idle인 세션은 다시 stop을 호출해 409를 만들지 않고 실제 상태를 확인합니다.
활성 세션은 중지 후 재조회하고 [실행 기록](../live-run.md)에 별도 receipt를 남깁니다.

A는 위 체크리스트·담당자 인계를 사용합니다. B는 4단계에서 로컬 목록을 이미 출력했습니다.
[정리 체크리스트](../reference/cleanup.md)를 따라 본인 자산을 확인하고,
공유 서비스와 다른 조의 데이터를 유지합니다.
정리 완료는 “명령을 실행했다”가 아니라 **활성 session·잔여 리소스·과금 상태를 다시 확인했다**는 뜻입니다.


**화면 확인:** 본인 세션의 상태와 다음 페이지 여부를 확인합니다.
화면의 세션 ID를 그대로 중지하지 말고 자신의 ID를 사용합니다. idle이어도 파일 저장소·Search·로그 비용이 모두 사라지는 것은 아닙니다.

다음: A → [Lab 11](11-capstone.md#path-a) · B → [Lab 11](11-capstone.md#path-b)
