# Lab 02. 모델을 배포하고 실제로 호출하기

[English](../../labs/02-models.md) | **한국어**

**완료 목표:** 모델 이름과 배포 이름을 구분하고, 한 번의 실제 응답을 확인합니다.

이전: [Lab 01](01-foundry.md) · 다음: [Lab 03](03-prompt-agent.md)

## A. 브라우저 — Playground에서 시작

### 1. 사용할 배포 확인

1. 실습 프로젝트의 모델/배포 목록을 엽니다.
2. 강사가 준비한 배포를 선택합니다. 카탈로그 모델 이름, 버전, 배포 이름을 따로 적습니다.

![모델 배포 목록에서 응답 모델과 judge를 구분](../../assets/live-20260914-action/shots/portal-0026-P02-002-deployments-ready-before.webp)

**화면 확인:** **Name**은 호출할 배포 이름, **Model / Version**은 기반 모델 정보입니다.
촬영에서는 응답용 `gpt-5.6-luna`와 평가용 `gpt-5.6-luna-judge`를 구분했습니다.
상세 패널에 judge가 보이더라도 질문은 강사가 지정한 응답용 배포의 Playground에서 보냅니다.

### 2. 외부 웹 도구 끄기

해당 모델의 Playground를 엽니다.
Tools에 기본 Web Search가 있으면 **Actions → Remove**로 제거합니다. 이 기본 경로는 외부 웹을 조회하지 않습니다.

![Web Search의 Actions 메뉴에서 Remove 찾기](../../assets/live-20260914-action/shots/portal-0041-P02-004-web-search-menu-ready.webp)

**화면 확인:** **Web search** 행의 Actions 메뉴를 열고 **Remove**를 선택합니다.
안내 배너를 닫는 **Dismiss**는 도구 제거가 아닙니다.

![Web Search를 제거한 뒤의 비어 있는 도구 목록](../../assets/live-20260914-action/shots/portal-0043-P02-005-remove-web-search-transition.webp)

**화면 확인:** Web search 행이 도구 목록에서 사라졌는지 확인한 뒤 질문을 입력합니다.
다른 Playground나 새 에이전트로 이동하면 도구 설정을 다시 확인해야 합니다.

### 3. 질문을 입력하고 응답 확인

> Foundry 리소스, 프로젝트, 모델 배포, 에이전트의 차이를 초보자에게 네 문장으로 설명해 주세요.

![모델 Playground의 질문 입력 위치와 전송 버튼](../../assets/live-20260914-action/shots/portal-0049-P02-006-model-question-ready.webp)

**화면 확인:** 오른쪽 아래 **Chat with the model...**에 질문을 넣고 전송합니다.
왼쪽 **Instructions**는 시스템 지침 입력란이므로 질문과 혼동하지 않습니다.

![새 Luna 배포가 반환한 실제 모델 응답](../../assets/live-20260914-action/shots/portal-0056-P02-007-model-response-screen-change.webp)

**화면 확인:** 응답 내용뿐 아니라 답변 아래의 모델 이름·시간·토큰 표시도 기록합니다.
이 화면은 촬영 환경의 예시이며, 참가자의 결과가 자동으로 같아지는 것은 아닙니다.

### 4. 근거 없는 질문과 비교

**New chat**으로 새 대화를 시작한 뒤 “한빛기술의 2026년 9월 숙박비 한도는?”을 질문합니다.
**아직 합성 규정을 주지 않았으므로 금액을 아는 척하면 안 됩니다.**
실제 회사 정책을 아는지 시험하는 질문이 아닙니다.

![정책 문서 없이 질문했을 때 금액을 보류한 실제 응답](../../assets/live-20260914-action/shots/portal-0073-P02-008-no-policy-send-screen-change.webp)

**화면 확인:** 근거를 제공하지 않았을 때 확인이 필요하다고 답하는지 봅니다.
그럴듯한 금액을 제시했다면 성공이 아니라 근거 없는 응답으로 기록하세요.

이제 모델만으로는 회사의 규정·적용 시점·승인 기준이 생기지 않는다는 점을 확인합니다.

2026-09-14 실제 화면에서는 도구를 제거한 뒤 다른 탭으로 이동할 때
**Leave without saving?** 확인 창이 나타났습니다. 이 모델 Playground의 임시 설정을
유지할 필요가 없다면 **Leave without saving**으로 이동합니다.
새 에이전트에 이 설정이 자동 적용되는 것은 아니므로 [Lab 03](03-prompt-agent.md)에서
모델과 도구 목록을 다시 확인합니다.

![다른 탭으로 이동하기 전에 나타난 저장 확인 창](../../assets/live-20260914-action/shots/portal-0078-P02-009-model-details-screen-change.webp)

**화면 확인:** 화면 이동이 멈춘 것처럼 보이면 **Leave without saving?** 창이 있는지 확인합니다.
임시 모델 설정을 유지하지 않을 때만 **Leave without saving**을 선택합니다.

### 배포가 아직 없다면

모델을 배포할 권한이 있는 강사가 카탈로그에서 **텍스트 입력, 도구 호출,
Structured Outputs를 지원하는 배포 가능한 모델**을 고릅니다.
배포 이름, SKU, 용량, 리전, 가격·할당량을 확인한 뒤 생성합니다.
특정 신형 모델의 접근 권한을 이 워크숍의 필수 조건으로 삼지 않습니다.

`workshop-chat`은 배포 이름을 설명하기 위한 예일 뿐, 이미 존재하는 리소스가 아닙니다.
모델 버전·리전·TPM 숫자를 이 문서에서 복사해 강제로 생성하지 않습니다.

## B. 코드 — 같은 프로젝트를 Responses API로 호출

```bash
python scripts/workshop.py doctor --cloud
python scripts/workshop.py model --question "Foundry와 Agent Framework의 차이를 한국어로 세 문장으로 설명해 주세요."
```

핵심 코드는 `src/foundry_workshop/cloud.py`의 `project_clients`, `call_model`입니다.

```python
with AIProjectClient(endpoint=project_endpoint, credential=credential) as project:
    with project.get_openai_client() as client:
        response = client.responses.create(
            model=deployment_name,
            input="Foundry와 MAF의 차이를 설명해 주세요.",
            store=False,
        )
```

위 블록은 흐름 설명용입니다. 실행에는 위 CLI와 `.env`의 실제 값을 사용합니다.
`response_id`, 실제 `response_model`, 토큰 사용량이 결과에 기록됩니다.
`trace_id: null`은 아직 Application Insights trace를 수집한 것이 아니라는 뜻입니다.
`response_id`를 임의의 trace ID로 바꿔 적지 않습니다.

![Responses API가 반환한 텍스트와 실제 모델 및 요청 이력](../../assets/live-20260914-action/shots/cli-1-0294-02-003-live-model-result.webp)

**화면 확인:** 마지막 명령 아래의 `text`, `response_model`, `response_id`, `usage`를 읽습니다.
`trace_id: null`과 `trace_export: not-configured`도 그대로 기록하며, 생성된 응답 ID를 Trace ID로 바꾸지 않습니다.

### 구조화 출력까지 확인

```bash
python scripts/workshop.py answer --prompt v2 --retrieval local
```

이 명령은 합성 문서에서 로컬 키워드 검색을 한 뒤 **실제 Azure 모델**을 호출합니다.
JSON의 `answer`, `decision`, `limit_krw`, `citations`를 확인합니다.
`local`은 검색 위치를 뜻할 뿐 **모델 호출이 오프라인이라는 뜻이 아닙니다.**

**새 영문 가이드 촬영: 2026-09-15.** ▶ [이 액션 재생](https://github.com/user-attachments/assets/082ede4b-d363-474c-ad47-598b20f593e9#t=175.32)

![구조화 답변 실행에서 보존한 요청과 검색 이력](../../assets/english-20260915/shots/terminal-0064-02-002-answer-result.webp)

**화면 확인:** 사진은 긴 출력의 하단입니다. `source_ids`, `response_id`, `usage`,
`trace_export`를 확인하고, 출력 위쪽의 `answer`·`decision`·`limit_krw`·`citations`와 함께 읽습니다.
답변만 복사하고 이력을 버리지 않습니다.

지원하지 않는 모델이 `json_schema`를 거부하면 여기서 중단합니다.
코드는 일반 텍스트로 몰래 전환하거나 JSON을 임의로 고치지 않습니다.
강사가 지원 여부를 확인한 배포로 명시적으로 다시 구성한 후 새 실행으로 기록합니다.

## 경험자 확장: 모델을 어떻게 비교할까?

같은 질문 하나만으로 모델 순위를 정하지 않습니다.
[Lab 07](07-evaluation.md)에서 **같은 dev·지식·지침·출력 한도·동시성**을 사용하고
배포 하나만 바꾸어 비교합니다. judge 모델도 응답 모델과 구분합니다.
정확한 비용은 토큰 종류, 실제 배포 가격, 캐시·추론 토큰, 도구/검색 요금을 함께 계산합니다.
이 저장소는 불확실한 단가로 원화 비용을 만들어 내지 않습니다.

### Model Router — 선택 관찰

해당 프로젝트에 Model Router가 제공되면 같은 질문이 어떤 라우팅 구성으로 처리되는지
살펴봅니다. Router 배포를 사용하는 것과 모델 A/B를 고정해 평가하는 것은 다른 실험입니다.
라우팅 정책·가능한 후보·실제 응답 모델을 기록할 수 없다면 고정 모델 순위로 발표하지 않습니다.
Router의 접근 권한/모델 목록은 수업 직전 공식 모델 문서와 포털에서 확인합니다.
Router가 없어도 이 랩은 완료할 수 있습니다.

## 완료·복구

모델·배포·실제 평가 범위는 [실행 기록](../live-run.md)에 구분했습니다.

- 완료: 실제 모델 응답과 배포 이름이 있고, 근거 없는 회사 정책 질문의 한계를 설명합니다.
- 401/403: [인증·권한](../reference/troubleshooting.md). 무조건 Owner를 추가하지 않습니다.
- 404: 프로젝트 endpoint와 **배포 이름**부터 확인합니다.
- 429: 동시 호출을 멈추고 quota/TPM을 확인합니다. 무한 재시도하지 않습니다.
