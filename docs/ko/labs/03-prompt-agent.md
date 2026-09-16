# Lab 03. 지침과 근거를 가진 첫 에이전트

[English](../../labs/03-prompt-agent.md) | **한국어**

**완료 목표:** 모델에 합성 업무 지침과 문서를 붙여, 출처와 한계를 설명하는 답변을 만듭니다.

**내 구간 바로 열기:** [A — 인라인 agent](#path-a) · B: [Lab 04 B로 이동](04-agents-tools.md#path-b) · [학습 경로](../paths.md)

## 시작 전

**이번 순서:** A는 완성된 인라인 지침 파일로 Prompt Agent 하나를 만듭니다. File Search·SDK 생성은 별도 선택 경로입니다.

**준비물:** 학습자 ZIP·본인 prefix·Lab 02에서 성공한 모델.

**다음으로 갈 기준:** 저장한 agent 이름/버전과 네 확인 질문의 실제 답변을 기록했습니다.

**막히면:** 지침은 대화창이 아니라 Instructions에 넣습니다. 녹화의 이름이나 version 1을 그대로 쓰지 않습니다.

[한 번만 하는 준비와 학습자 파일](../setup.md).

<a id="path-a"></a>

## A. 브라우저 — 먼저 성공하는 가장 작은 형태

Agent 생성·버전 저장·유료 확인 호출을 합니다. 승인된 실습 프로젝트와 본인 prefix를 사용합니다.
반환 버전과 실제 답변을 적을 `session-notes.txt`를 열어 둡니다. 배포나 Publish는 필요하지 않습니다.

### 1. 에이전트 만들기

#### 생성 메뉴와 이름

현재 실습 프로젝트에서 **Agents → New agent → Build an agent**를 선택합니다.

![2026-09-15 새 국문 촬영: 새 에이전트 생성 대화상자 열기](../../assets/refresh-20260915-ko/screenshots/KP03-011-new-agent-2.webp)

**화면 확인:** 이 경로는 지침을 편집하는 Prompt Agent입니다.
코드 배포용 **Code an agent**나 외부 에이전트 연결 메뉴를 선택하지 않습니다.

이름은 내 접두사로 시작합니다. 예: `mfv2-team01-0915-policy`.
입력 후 **Create and open playground**를 누르고 생성 완료를 기다립니다.

![2026-09-15 새 국문 촬영: 새 국문 합성 파일 Agent의 고유 이름 입력](../../assets/refresh-20260915-ko/screenshots/KP03-013-agent-name-2.webp)

**화면 확인:** **Agent name**에 본인 접두사를 사용합니다. 촬영의 `mfv2-action-...` 이름을 그대로 쓰지 않습니다.
생성 요청 중 버튼이 비활성화되어 있으면 중복 클릭하지 말고 결과를 기다립니다.

#### 모델과 도구 선택

[Lab 02](02-models.md)에서 실제 응답을 확인한 모델 배포를 선택합니다.

![2026-09-15 새 국문 촬영: 추론 전에 실습의 명시적 Luna 모델 선택](../../assets/refresh-20260915-ko/screenshots/KP03-015-select-model-2.webp)

**화면 확인:** **Deployments**에서 본인의 응답용 배포를 선택합니다.
촬영의 `-judge` 배포는 평가용이며, 아래의 다른 카탈로그 모델을 무심코 선택하지 않습니다.

Tools에 기본 **Web search**가 있으면 **Actions for Web search → Remove**로 제거합니다.
Lab 02에서 제거했더라도 새 에이전트에 다시 추가될 수 있습니다.

![2026-09-15 새 국문 촬영: 추론 전에 웹 검색 제거](../../assets/refresh-20260915-ko/screenshots/KP03-018-remove-web-2.webp)

**화면 확인:** 첫 질문 전에 Web search 행이 사라졌는지 확인합니다.
이 단계에서는 실제 회사 연결이나 외부 시스템을 변경하는 도구를 추가하지 않습니다.

#### 지침 입력과 저장

[학습자 ZIP](../setup.md#3-바로-쓰는-학습자-자료-내려받기)의 **`instructions-with-policies.txt`**를 텍스트 편집기로 엽니다.
파일의 전체 텍스트를 복사해 **Instructions(지침)**에 붙여 넣고 **Save(저장)**합니다.
v2 규칙·합성 정책 6개·브라우저용 한국어 문장 출력 지시가 이미 들어 있습니다.
JSON 파일을 직접 조립하거나 지침을 추가로 붙이지 않으며 ZIP 자체를 넣지 않습니다.
이 파생 브라우저 자료는 코드 평가의 엄격한 JSON 출력 계약과 별개입니다.

![2026-09-15 새 국문 촬영: 합성 파일 근거·승인 경계 지침 입력](../../assets/refresh-20260915-ko/screenshots/KP03-019-instructions-2.webp)

**화면 확인:** 왼쪽 **Instructions**가 지침 입력란입니다. 오른쪽 대화 입력란에 지침을 넣지 않습니다.
내용이 길면 끝까지 입력됐는지 확인한 뒤 **Save**로 저장하고 실제 버전을 기록합니다.
**Publish**는 외부 채널 게시와 관련된 별도 작업이며 이 실습에는 필요하지 않습니다.

### 2. 포함된 합성 규정 확인

방금 붙인 파일에는 `TRAVEL-2025`, `TRAVEL-2026`, `APPROVAL-01`, `RECEIPT-01`,
`MEAL-01`, `SCOPE-01`이 있습니다. ZIP의 `policies/` 파일과 ID·내용·적용 기간을 대조합니다.
문서는 명령이 아니라 근거입니다. **작은 문서를 직접 컨텍스트에 넣는 방식**이지 File Search나 Foundry IQ가 아닙니다.
누락을 발견한 경우가 아니라면 다시 붙여 넣거나 저장할 필요가 없습니다.

![2026-09-15 새 국문 촬영: 합성 정책을 가진 기존 프롬프트 Agent 열기](../../assets/refresh-20260915-ko/screenshots/KP03-002-inline-agent-2.webp)

**화면 확인:** 상단 **버전**과 비활성화된 **저장**을 확인합니다.
위 화면은 이미 준비된 인라인 근거 에이전트 v3을 새로 관찰한 것입니다.
이어지는 파일 검색 경로는 별도의 새 국문 에이전트를 생성했습니다. 본인에게 반환된 버전을 기록해야 합니다.
사진에 보이는 지침 끝부분만 복사하지 말고 원문 6개와 적용 기간을 빠짐없이 넣으세요.

<details>
<summary>선택: File Search로 같은 합성 파일을 검색하기</summary>

포털에 File Search가 제공되고 강사가 파일 저장/검색 비용을 승인했다면 다음을 추가로 합니다.

1. 본인 prefix에 `-files`를 붙인 **별도 agent**를 만듭니다. 인라인 agent는 Lab 07용으로 그대로 둡니다.
2. ZIP의 **`instructions.txt`**를 Instructions에 붙이고 Luna 선택·Web Search 제거 후 저장합니다.
3. **`policies/` 안의 TXT 6개만** 올립니다. ZIP·CSV·인라인 지침 파일은 올리지 않으며 Python/export 단계도 필요 없습니다.
4. 모든 파일의 색인 상태가 **Completed**가 될 때까지 기다립니다.
5. 질문 하나를 보낸 뒤 실제 인용 파일 이름/내용과 원문을 대조합니다. 이 비교에 인라인 정책과 File Search를 동시에 사용하지 않습니다.

![2026-09-15 새 국문 촬영: 새 국문 파일 인덱스의 고유 이름](../../assets/refresh-20260915-ko/screenshots/KP06-021-index-name-2.webp)

**화면 확인:** **Upload files → Attach files**에서 **Create a new index**와 본인의 고유 이름을 확인합니다.
**browse for files**로 강사가 제공한 합성 텍스트 파일 6개만 선택합니다.

![2026-09-15 새 국문 촬영: 해시로 검증한 6개 합성 원문 선택](../../assets/refresh-20260915-ko/screenshots/KP06-022-choose-files-2.webp)

**화면 확인:** 파일 이름 6개와 **Success**를 확인한 뒤 **Attach**합니다.
이 표의 업로드 성공을 색인 완료로 판단하지 않습니다.

![2026-09-15 새 국문 촬영: 실제 업로드한 파일들의 인덱싱 상태 확인](../../assets/refresh-20260915-ko/screenshots/KP06-025-vector-files-2.webp)

**화면 확인:** 연결된 저장소를 열어 **1–6 of 6**과 각 파일의 **Completed**를 확인합니다.
누락·실패 파일이 있다면 질문으로 넘어가지 말고 원인을 확인합니다.

![2026-09-15 새 국문 촬영: FILES-D01 · 실제 응답과 근거 확인](../../assets/refresh-20260915-ko/screenshots/KP06-028-file-response-send-2.webp)

**화면 확인:** 도구 목록의 **File search**, 답변의 파일 이름과 인용 번호를 함께 확인합니다.
새 국문 촬영은 인라인 에이전트와 별도인 File Search 에이전트 v3이며, 이 한 응답을 dev 전체 평가 점수로 사용하지 않습니다.

이번 새 국문 촬영에서는 **Upload files → Attach files**에서 새 vector index 이름과 파일을
선택했습니다. 여기의 vector index는 File Search의 저장소이며 Lab 06의 Azure AI Search
인덱스와 같은 객체가 아닙니다. 업로드의 `Success` 이후 저장소의 6개 파일이 `Completed`인지 확인했습니다.
이번 새 실행에서도 인용 버튼 클릭의 다운로드는 확인되지 않았습니다. 열린 것으로 기록하지 말고,
파일 이름과 제공된 합성 원문을 대조하세요. 강사 실행에서는 같은 저장 원문 6개를 SDK로 읽어
원본과 바이트 일치까지 확인했습니다.

메뉴가 없으면 이 선택 경로를 미선택으로 둡니다. 업로드/검색을 시도하다 실패했다면
실패를 보존하고 해당 경로에서 멈춥니다. 인라인 응답을 File Search 성공으로 바꾸어 적지 않습니다.

</details>

### 3. 네 질문으로 확인

ZIP의 `dev-questions.txt`에서 각 ID의 **질문만** 복사합니다. 아래 정답 기준 열을 보내지 않습니다.

| 사례 | 확인할 점 |
|---|---|
| D01 · 2026년 9월 국내 숙박 | 현행 150000원, `TRAVEL-2026` |
| D02 · 2026년 5월 국내 숙박 | 과거 120000원, `TRAVEL-2025` |
| D03 · 한도 초과 예약 | 사전 승인, 에이전트는 승인 불가 |
| D05 · 해외 출장 | 추측하지 않고 근거 부족을 안내 |

위 숫자는 **합성 규정의 정답 기준**이지 모델이 이미 맞혔다는 실측 결과가 아닙니다.
질문마다 새 대화를 시작해 앞 질문의 정답이 뒤 실험으로 흘러가지 않게 합니다.

![2026-09-15 새 국문 촬영: D01 · 이전 대화와 분리](../../assets/refresh-20260915-ko/screenshots/KP07-d01-new-chat-2.webp)

**화면 확인:** 질문을 바꾸기 전에 대화 영역 위의 **New chat**을 누릅니다.
이전 응답이 없어졌는지 확인하고 입력란에 남은 초안도 다음 질문으로 바꿉니다.


![2026-09-15 새 국문 촬영: D01 · 실제 응답과 근거 확인](../../assets/refresh-20260915-ko/screenshots/KP07-d01-send-2.webp)

**화면 확인:** 현행 날짜에 150,000원과 `TRAVEL-2026`을 연결하는지 읽습니다.
금액만 맞는지 보지 말고 영수증·승인 조건도 원문과 비교합니다.

![2026-09-15 새 국문 촬영: D02 · 실제 응답과 근거 확인](../../assets/refresh-20260915-ko/screenshots/KP07-d02-send-2.webp)

**화면 확인:** 2026년 5월 질문에는 120,000원과 `TRAVEL-2025`가 적용되는지 확인합니다.
오늘 날짜나 최신 문서를 무조건 적용하면 실패로 기록합니다.

![2026-09-15 새 국문 촬영: D03 · 실제 응답과 근거 확인](../../assets/refresh-20260915-ko/screenshots/KP07-d03-send-2.webp)

**화면 확인:** 170,000원은 한도 초과이므로 예약 전 승인 절차를 안내해야 합니다.
도우미가 승인됐다고 말하거나 직접 예약했다고 주장하지 않았는지 확인합니다.

![2026-09-15 새 국문 촬영: D05 · 실제 응답과 근거 확인](../../assets/refresh-20260915-ko/screenshots/KP07-d05-send-2.webp)

**화면 확인:** 해외 규정이 없으면 금액을 추측하지 않고 확인을 요청해야 합니다.
위 네 이미지는 촬영 예시입니다. 본인의 실제 응답과 실패 여부를 따로 기록하세요.

**A 완료:** 실제 저장 지침·agent 버전·확인 4건을 증거 폴더에 보관합니다.
[Lab 05 A](05-workflows.md#path-a)로 이동합니다. Lab 04와 아래 SDK 경로는 A의 필수 단계가 아닙니다.

## B. 선택 SDK 경로 — 관리형 prompt agent와 로컬 MAF 구분

<details>
<summary>선택 SDK agent — 다른 agent를 생성하며 A/B 기본 경로에는 필수가 아닙니다</summary>

A/B 첫 회차에 필수는 아닙니다. 브라우저 agent와 다른 새 agent를 만듭니다.
`.env`의 `WORKSHOP_PREFIX`로 시작하는 새 이름을 입력하고 브라우저 agent 이름은 재사용하지 않습니다.

```bash
printf 'New agent name (<your prefix>-policy-sdk): '
read -r AGENT_NAME
python scripts/workshop.py prompt-agent create --name "$AGENT_NAME" --confirm-create
```

위 이름의 접두사는 `.env`의 `WORKSHOP_PREFIX`와 같아야 합니다. 본인 이름으로 바꿉니다.
명령은 **실제 프로젝트에 새 agent version을 생성**합니다. 에이전트 이름과 버전을 기록합니다.
SDK 예제는 비교가 쉬운 작은 문서 컨텍스트를 지침에 포함하며 **File Search를 만든다고 주장하지 않습니다.**

![2026-09-15 새 국문 촬영: SDK로 새 합성 정책 Agent 생성](../../assets/refresh-20260915-ko/screenshots/K03-100-sdk-create-2.webp)

**화면 확인:** `agent_name`과 `agent_version`을 다음 호출에 그대로 사용합니다.
촬영의 SDK agent v1과 위 브라우저 agent v3은 별도 에이전트이므로 버전을 혼용하지 않습니다.

```bash
printf 'agent_version returned above: '
read -r AGENT_VERSION
python scripts/workshop.py prompt-agent invoke --name "$AGENT_NAME" --version "$AGENT_VERSION" --question "2026년 9월 국내 출장 숙박비 한도는?"
```

같은 터미널에서 생성 결과의 실제 version을 입력합니다. 녹화의 `1`을 따라 쓰지 않습니다.
같은 이름에 새 버전이 생겼다면 “최신 버전”을 묵시적으로 호출하지 않습니다.
SDK의 버전 고정 방식은 [버전 기준](../reference/versions.md)에 기록합니다.

</details>

## 도구가 늘어날수록 지켜야 할 경계

- File Search는 파일 검색, Foundry IQ는 지식 소스 검색, Web Search는 외부 웹 검색입니다.
  서로 같은 기능이 아닙니다.
- 공개 웹을 검색한다고 사내 정책의 근거가 생기지는 않습니다.
- 이 기본 랩에는 회사 API, 이메일 전송, 결제, Graph/Microsoft 365 권한을 연결하지 않습니다.
- Content Safety/guardrails와 지침은 방어 수단이지 권한 검사의 대체물이 아닙니다.
- Web Search/Toolbox는 승인된 공식 문서 등 제한된 도메인으로만 [선택 확장](10-iq-extensions.md)합니다.

## 완료 확인

브라우저 agent v3, 별도 SDK agent v1, File Search agent v3, IQ 검색의 실제 확인 범위는
[실행 기록](../live-run.md)에서 구분합니다.

에이전트 이름/버전, 실제 네 응답, 근거 제공 방식, 틀리거나 보류한 사례 하나를 기록합니다.
답변이 자연스럽다는 사실과 회사 규정이 맞다는 사실은 별개입니다.
이 차이를 [Lab 07](07-evaluation.md)에서 평가 기준으로 바꿉니다.

다음: A → [Lab 05](05-workflows.md#path-a) · B: [Lab 04로 이동](04-agents-tools.md#path-b)
