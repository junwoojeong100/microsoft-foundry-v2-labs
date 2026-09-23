# Lab 02. 준비된 모델을 실제로 호출하기

[English](../../labs/02-models.md) | **한국어**

**완료 목표:** 모델 이름과 배포 이름을 구분하고, 한 번의 실제 응답을 확인합니다.

**내 구간 바로 열기:** [A — Playground](#path-a) · [B — SDK](#path-b) · [학습 경로](../paths.md)

## 시작 전

**이번 순서:** A는 Playground, B는 CLI 확인과 구조화 출력을 실행합니다. 첫 회차에는 모델 비교를 건너뜁니다.

**준비물:** 준비된 gpt-6-sol 배포. B는 Lab 00의 활성 환경과 .env.

**다음으로 갈 기준:** 실제 응답과 배포 이름을 기록했습니다. B는 구조화된 답변도 확인했습니다.

**막히면:** 멈추고 오류를 담당자에게 알립니다. 401/403이면 프로젝트의 **Foundry User** 역할을, 429이면 배포의 quota(TPM)를 확인해 달라고 요청합니다. 배포가 없으면 `gpt-6-sol` 준비를 요청합니다. 모델을 바꾸지 않습니다.

[한 번만 하는 준비와 학습자 파일](../setup.md).

<a id="path-a"></a>

## A. 브라우저 — Playground에서 시작

승인된 수업 예산으로 실제 모델을 호출합니다. 두 실제 관찰을 `session-notes.txt`에 저장합니다.

### 1. 사용할 배포 확인

프로젝트 **홈**에서 **배포 보기**를 선택한 뒤 **`gpt-6-sol`** 행을 선택합니다.
모델 **`gpt-6-sol`**, 버전 **`2026-09-22`**를 확인하고 배포 이름·모델·버전을 `session-notes.txt`에 적습니다
(여기서는 배포 이름과 모델 이름이 같지만 서로 다른 대상입니다).

![2026-09-23 국문 녹화: gpt-6-sol을 선택하고 버전 2026-09-22 확인](../../assets/g6sol-20260923-ko/screenshots/KP02-002-select-sol-2.webp)

**화면 확인:** **이름**은 호출할 배포 이름, **모델**·**버전**은 기반 모델 정보입니다.
2026-09-23 환경은 응답용 `gpt-6-sol`과 평가용 `gpt-6-sol-judge`를 따로 배포합니다.
오른쪽 패널 코드에 judge가 보이더라도 질문은 응답용 `gpt-6-sol` 플레이그라운드에서 보냅니다.

### 2. 외부 웹 도구 끄기

**`gpt-6-sol`** 이름 링크를 선택해 플레이그라운드를 엽니다. **도구**에서 **웹 검색** 행의
**⋮** 메뉴를 열고 **제거**를 선택합니다. 이 기본 경로는 외부 웹을 조회하지 않습니다.

![2026-09-23 국문 녹화: 기본 웹 검색 도구의 ⋮ 메뉴 열기](../../assets/g6sol-20260923-ko/screenshots/KP02-006-web-menu-2.webp)

**화면 확인:** **웹 검색** 행의 **⋮** 메뉴에 **제거**가 보입니다.
그 위 안내 상자의 **X**는 안내만 닫으며 도구를 제거하지 않습니다.

![2026-09-23 국문 녹화: 질문 전에 외부 웹 검색 제거](../../assets/g6sol-20260923-ko/screenshots/KP02-007-remove-web-2.webp)

**화면 확인:** **웹 검색** 행이 도구 목록에서 사라졌는지 확인한 뒤 질문을 입력합니다.
다른 플레이그라운드나 새 에이전트로 이동하면 도구 설정을 다시 확인해야 합니다.

### 3. 질문을 입력하고 응답 확인

> Foundry 리소스, 프로젝트, 모델 배포, 에이전트의 차이를 초보자에게 네 문장으로 설명해 주세요.

![2026-09-23 국문 녹화: 개념 질문과 실제 gpt-6-sol 답변](../../assets/g6sol-20260923-ko/screenshots/KP02-008-question-1.webp)

**화면 확인:** 오른쪽 아래 **모델과 채팅...**에 질문을 넣고 보내기 화살표를 선택합니다.
왼쪽 **지침**은 시스템 지침 입력란이므로 질문 입력란과 혼동하지 않습니다.

![2026-09-23 국문 녹화: 개념 질문과 실제 gpt-6-sol 답변](../../assets/g6sol-20260923-ko/screenshots/KP02-008-question-2.webp)

**화면 확인:** 응답 내용뿐 아니라 답변 아래의 모델 이름·시간·토큰 표시도 기록합니다.
이 화면은 촬영 환경의 예시이며, 참가자의 결과가 자동으로 같아지는 것은 아닙니다.

### 4. 근거 없는 질문과 비교

채팅 오른쪽 위의 **새 채팅**(+ 아이콘)을 선택한 뒤 “한빛기술의 2026년 9월 숙박비 한도는?”을 질문합니다.
**아직 합성 규정을 주지 않았으므로 금액을 아는 척하면 안 됩니다.**
실제 회사 정책을 아는지 시험하는 질문이 아닙니다.


![2026-09-23 국문 녹화: 새 대화: 정책 근거 없이 질문](../../assets/g6sol-20260923-ko/screenshots/KP02-009-new-chat-2.webp)

**화면 확인:** 근거를 제공하지 않았을 때 확인이 필요하다고 답하는지 봅니다.
그럴듯한 금액을 제시했다면 성공이 아니라 근거 없는 응답으로 기록하세요.

이제 모델만으로는 회사의 규정·적용 시점·승인 기준이 생기지 않는다는 점을 확인합니다.

뒤로 화살표(←)나 다른 메뉴를 선택하면 저장 확인 창이 나타날 수 있습니다.
**저장하지 않고 나가기**를 선택합니다. 이 임시 플레이그라운드 설정은 필요 없고 새 에이전트에도 적용되지 않습니다.

![2026-09-23 국문 녹화: 임시 플레이그라운드 설정을 저장하지 않고 나가기](../../assets/g6sol-20260923-ko/screenshots/KP02-010-leave-2.webp)

**화면 확인:** 화면 이동이 멈춘 것처럼 보이면 확인 창이 열려 있는지 봅니다.
저장하지 않을 임시 설정만 버립니다.

### 배포가 아직 없다면

멈추고 담당자에게 [준비 카드](../setup.md)대로 **`gpt-6-sol`**(버전 `2026-09-22`) 준비를 요청합니다.
통과하려고 `gpt-6-sol-judge`, router, 다른 모델을 선택하지 않습니다([이 모델을 쓰는 이유](../reference/model-choice.md)).

**A 완료:** 실제 배포·버전, 개념 응답 한 건, 정책 근거 없는 관찰 한 건이 있습니다.
[Lab 03 A](03-prompt-agent.md#path-a)로 이동합니다. Lab 05 터미널을 직접 준비하는 경우가 아니라면 B의 SDK 호출은 실행하지 않습니다.

<a id="path-b"></a>

## B. 코드 — 같은 프로젝트를 Responses API로 호출

저장소 루트·활성 `.venv`에서 실행합니다. 사전 검사는 읽기 전용이며 모델·구조화 답변 요청은 유료입니다.

```bash
python scripts/workshop.py doctor --cloud
```

의도한 배포가 `Succeeded`인지 사전 확인한 뒤에만 실제 요청을 보냅니다.

```bash
python scripts/workshop.py model \
  --question "Foundry와 Agent Framework의 차이를 한국어로 세 문장으로 설명해 주세요." \
  --output outputs/learner-notes-ko/model.json
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

![2026-09-23 국문 녹화: 프로젝트 Responses API로 첫 실제 gpt-6-sol 요청](../../assets/g6sol-20260923-ko/screenshots/K02-001-model-2.webp)

**화면 확인:** 마지막 명령 아래의 `text`, `response_model`, `response_id`, `usage`를 읽습니다. `gpt-6-sol`은 짧은 답에도 `usage`에 reasoning token을 보고합니다.
`trace_id: null`과 `trace_export: not-configured`도 그대로 기록하며, 생성된 응답 ID를 Trace ID로 바꾸지 않습니다.

**저장:** `model.json`은 `--output`이 Lab 00 기록 폴더에 작성합니다. 저장된 응답 전체를 연 뒤 다음 요청으로 갑니다.

### 구조화 출력까지 확인

```bash
python scripts/workshop.py answer --prompt v2 --retrieval local \
  --output outputs/learner-notes-ko/answer-local.json
```

이 명령은 합성 문서에서 로컬 키워드 검색을 한 뒤 **실제 Azure 모델**을 호출합니다.
JSON의 `answer`, `decision`, `limit_krw`, `citations`를 확인합니다.
`local`은 검색 위치를 뜻할 뿐 **모델 호출이 오프라인이라는 뜻이 아닙니다.**


![2026-09-23 국문 녹화: 로컬 근거를 사용한 검증된 구조화 답변](../../assets/g6sol-20260923-ko/screenshots/K02-002-answer-2.webp)

**화면 확인:** 답변 필드·`source_ids`·`response_id`·`usage`·`trace_export`를 포함한 출력 전체를 읽습니다.
금액만 맞고 근거가 없는 것으로는 충분하지 않습니다.

**저장:** `answer-local.json`이 같은 기록 폴더에 작성됩니다. 답변뿐 아니라 원문과 응답 metadata도 확인합니다.

지원하지 않는 모델이 `json_schema`를 거부하면 여기서 중단합니다.
코드는 일반 텍스트로 몰래 전환하거나 JSON을 임의로 고치지 않습니다.
강사가 지원 여부를 확인한 배포로 명시적으로 다시 구성한 후 새 실행으로 기록합니다.

**B 완료:** Lab 00 기록 폴더에 `model.json`, `answer-local.json`으로 출력 전체를 저장합니다.
Response ID·사용량·원문 ID도 포함합니다.
[Lab 04 B](04-agents-tools.md#path-b)로 이동합니다. A 터미널 준비 때문에 왔다면 [Lab 05 A](05-workflows.md#path-a)로 돌아갑니다.

## 경험자 확장: 모델을 어떻게 비교할까?

<details>
<summary>선택 모델 비교·Router — 첫 요청의 필수 단계가 아닙니다</summary>

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

</details>

<details>
<summary>2026-09-23 gpt-6-sol 녹화 화면 더 보기 (참고; 그대로 재실행할 단계가 아님)</summary>

2026-09-23 `gpt-6-sol` / `2026-09-22` 국문 녹화 화면입니다. 본인의 리소스 이름·버전·결과를 사용합니다.

![2026-09-23 국문 녹화: 배포 목록 열기: gpt-6-sol과 judge](../../assets/g6sol-20260923-ko/screenshots/KP02-001-deployments-2.webp)

**화면 확인:** 목록에는 응답용 `gpt-6-sol`, 별도의 `gpt-6-sol-judge`, 포털이 만든 `text-embedding-3-large`가 있습니다. 질문은 응답용 배포로만 보냅니다.

![2026-09-23 국문 녹화: judge나 카탈로그 모델이 아닌 응답 배포 확인](../../assets/g6sol-20260923-ko/screenshots/KP02-004-deployments-list-2.webp)

**화면 확인:** 모델 선택 목록은 기존 배포와 카탈로그 모델을 따로 보여 줍니다. `gpt-6-sol`을 유지하고 judge나 카탈로그 모델을 고르지 않습니다.

[전체 액션 인덱스](../action-captures.md) · [녹화 영상](../video-summary.md)

</details>

## 완료·복구

모델·배포·실제 평가 범위는 [실행 기록](../live-run.md)에 구분했습니다.

- 완료: 실제 모델 응답과 배포 이름이 있고, 근거 없는 회사 정책 질문의 한계를 설명합니다.
- 401/403: `az login`을 다시 실행합니다. 계속되면 담당자에게 프로젝트의 **Foundry User**를 요청합니다([역할](../reference/troubleshooting.md)). Owner는 필요 없습니다.
- 404: 전체 프로젝트 엔드포인트와 **배포 이름** `gpt-6-sol`을 확인합니다.
- 429: 반복 호출을 멈추고 담당자에게 `gpt-6-sol` quota(TPM) 확인을 요청합니다. 반복 재시도하지 않습니다.

다음: A → [Lab 03](03-prompt-agent.md#path-a) · B → [Lab 04](04-agents-tools.md#path-b)
