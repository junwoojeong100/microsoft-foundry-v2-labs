# Lab 04. MAF 에이전트에 함수와 MCP 붙이기

[English](../../labs/04-agents-tools.md) | **한국어**

**완료 목표:** 모델 호출, 애플리케이션이 소유한 에이전트, 도구 실행의 경계를 구분합니다.

**내 구간 바로 열기:** A: [Lab 05 A로 이동](05-workflows.md#path-a) · [B — 세 도구 경로](#path-b) · [학습 경로](../paths.md)

## 시작 전

**이번 순서:** B는 도구 없음→함수→MCP 순서로 실행합니다. A는 Lab 05로 이동합니다.

**준비물:** Lab 00 환경, Lab 02 실제 응답, Lab 03 B 관리형 agent 파일. 별도 MCP 서버 터미널은 필요 없습니다.

**다음으로 갈 기준:** 도구 없는 응답과 원문 ID를 가진 함수/MCP 응답을 기록했습니다. 긴 입력 거절은 선택적인 실패 검사입니다.

**막히면:** 같은 venv와 서버 경로를 확인합니다. MCP 실패를 함수 응답으로 대신하지 않습니다.

[한 번만 하는 준비와 학습자 파일](../setup.md).

<a id="path-b"></a>

## 1. 도구 없는 에이전트 실행

저장소 루트·활성 `.venv`에서 실행합니다. 세 명령 모두 유료 모델 호출입니다.
각 명령이 성공하면 `--output`이 실제 JSON 전체를 Lab 00 기록 폴더의
`maf-none.json`, `maf-function.json`, `maf-mcp.json`에 저장합니다.
직접 복사하지 말고 다음 명령 전에 해당 파일을 열어 확인합니다.
`session-notes.txt`의 B 구간에 있는 `Lab 04 maf-none.json / maf-function.json / maf-mcp.json 검토:`에 파일별 확인 결과를 적습니다.

```bash
python scripts/workshop.py maf \
  --question "Foundry와 Agent Framework의 차이를 세 문장으로 설명해 주세요." \
  --output outputs/learner-notes-ko/maf-none.json
```

![2026-09-24 국문 녹화: 도구 없는 MAF agent](../../assets/g6sol-20260924-ko/screenshots/K04-001-maf-2.webp)

**화면 확인:** 마지막 출력의 `mode: live`, `orchestration: local`, `tools: none`을 읽습니다.
로컬 Python이 실행을 소유해도 답변 모델 호출은 Azure에서 이루어집니다.

**저장:** `maf-none.json`이 Lab 00 기록 폴더에 자동 작성됩니다. 파일을 열어 위 필드를 확인합니다.

`src/foundry_workshop/agents.py`를 엽니다. 다음 세 부분을 찾습니다.

1. `FoundryChatClient`: 어디의 어떤 모델 배포를 호출하는가.
2. `Agent`: 이름·지침·도구·실행 옵션을 묶는다.
3. `agent.run()`: 실제 모델 호출을 시작한다.

`Agent` 객체를 만들어도 Foundry 포털에 관리형 에이전트가 등록되지 않습니다. 이 에이전트는 내 Python 프로세스의 것입니다.
Lab 03 B는 `project.agents.create_version()`을 사용하는 관리형 대안을 보여줍니다. 이 Lab 04 agent는 본인 Python 프로세스에만 속합니다.

## 2. 읽기 전용 함수 도구 추가

```bash
python scripts/workshop.py maf --tools \
  --question "2026년 9월 국내 출장 호텔이 170000원인데 예약해도 되나요? 한도와 절차를 알려주세요." \
  --output outputs/learner-notes-ko/maf-function.json
```

`lookup_policy` 함수는 합성 JSON 파일만 읽습니다. 인터넷·회사 API에 접근하지 않습니다.
`@tool`의 함수 이름, docstring, 타입 정보가 모델에게 도구의 사용법을 알려 줍니다.
모델이 요청한 인자는 프로그램에서 다시 검사합니다.

```mermaid
sequenceDiagram
    participant U as 사용자
    participant A as 로컬 MAF Agent
    participant M as Foundry 모델
    participant T as lookup_policy 함수
    U->>A: 출장 규정 질문
    A->>M: 질문 + 도구 정의
    M-->>A: 도구 호출 요청
    A->>T: 검증된 query
    T-->>A: 합성 근거와 문서 ID
    A->>M: 도구 결과 (데이터)
    M-->>U: 조건·인용을 포함한 답변
```


![2026-09-24 국문 녹화: 읽기 전용 함수 도구를 쓰는 MAF](../../assets/g6sol-20260924-ko/screenshots/K04-002-tools-2.webp)

**화면 확인:** `tools: function`과 `answer` 안의 `decision`, `limit_krw`, `citations`를 확인합니다.
사진의 `needs_approval`은 승인 완료가 아니라 사람의 사전 승인이 필요하다는 뜻입니다.

확인할 것:

- 응답에 `TRAVEL-2026`, `APPROVAL-01`에 해당하는 근거가 있는가.
- 한도를 설명하되 실제 예약이나 승인을 하지 않았는가.
- 도구의 `never_require`는 **부작용 없는 합성 조회**에만 적용했는가.

모델이 도구를 부르지 않거나 근거를 생략하면 “도구가 연결되었으니 성공”으로
처리하지 않습니다. 실제 응답을 보고 지침·도구 설명·추적 정보를 점검합니다.

**저장:** `maf-function.json`이 같은 기록 폴더에 작성됩니다. 내용을 검토한 뒤 MCP로 갑니다.

## 3. 같은 조회를 로컬 MCP 서버로 분리

```bash
python scripts/workshop.py maf --mcp \
  --question "2026년 5월 국내 출장 숙박비의 1박 한도는 얼마인가요?" \
  --output outputs/learner-notes-ko/maf-mcp.json
```

클라이언트가 `examples/mcp_server.py`를 **같은 가상환경의 Python**으로 실행합니다.
따로 터미널에서 서버를 띄우거나 공개 URL·API key를 입력하지 않습니다.
전송은 stdio이며, 실행이 끝나면 컨텍스트 관리자가 연결을 정리합니다.
서버 로그를 stdout에 임의로 추가하면 MCP JSON-RPC 통신을 깨뜨릴 수 있습니다.

| 함수 도구 | MCP 도구 |
|---|---|
| 같은 Python 프로세스의 함수 | 별도 프로세스/서비스가 공개한 도구 |
| 구현이 단순하고 디버깅이 쉬움 | 여러 클라이언트에서 재사용하기 쉬움 |
| 함수 인자·권한을 직접 검증 | 프로토콜 연결 외에 서버 신뢰·인증·권한도 검토 |

이 MCP는 **합성 로컬 라이브러리**입니다. Microsoft Learn, Work IQ 또는 회사 MCP를
연결한 것으로 발표하지 않습니다. 실행 가능한 관리형 도구 확장은 [Toolbox](extensions/toolbox.md)를 사용합니다.
[Lab 10](10-iq-extensions.md)은 별도의 외부 IQ 설계 참고입니다.

함수 도구와 MCP 도구는 같은 답변 schema를 전달하고 실제 반환 JSON을 검사합니다.
`answer`의 문장뿐 아니라 `decision`, `limit_krw`, `citations`도 함께 확인합니다.
형식이 잘못되면 응답을 임의로 고쳐 성공으로 처리하지 않습니다.

![2026-09-24 국문 녹화: 로컬 MCP 정책 도구를 쓰는 MAF](../../assets/g6sol-20260924-ko/screenshots/K04-003-mcp-2.webp)

**화면 확인:** `tools: local-mcp`를 확인하고 2026년 5월에 과거 한도와 `TRAVEL-2025`를 적용했는지 봅니다.
함수 도구 결과로 MCP 실행을 대신한 것이 아닙니다.

**저장:** `maf-mcp.json`은 성공 시 같은 기록 폴더에 작성됩니다. 요청이 실패했다면 성공 파일 대신 실제 오류를 보관합니다.

**B 완료:** 실제 출력 세 개를 보관하고 도구 없음·함수·로컬 MCP의 차이를 설명합니다.
[Lab 05 B](05-workflows.md#path-b)로 이동합니다. 아래 4·5절은 선택입니다.

<details>
<summary>최소 SDK 예제(선택, 저장소 밖 재사용)</summary>

독립 예제는 [`examples/recipes/04_maf_tool.py`](../../../examples/recipes/04_maf_tool.py)를 참고합니다. 핵심 줄은 다음과 같습니다.

```python
@tool(approval_mode="never_require")
def lookup_policy(query: str) -> str:
    """Search the synthetic travel policies. Read-only; empty means no evidence."""
    ...


agent = Agent(
    client=FoundryChatClient(project_endpoint=endpoint, model=deployment, credential=credential),
    instructions="Call lookup_policy first and cite policy IDs. Never approve, book or pay.",
    tools=[lookup_policy],
)
```

**직접 작성:** 읽기 전용 합성 조회 필드를 하나 더 추가하고 답변 전에 도구 출력이 정책 ID를 계속 인용하는지 확인합니다.

</details>


## 4. 선택 — 도구 경계와 잘못된 입력 거절 확인

첫 회차는 위 세 실제 출력을 확인한 뒤 [Lab 05](05-workflows.md)로 이동해도 됩니다.

<details>
<summary>선택 실패 검사 펼치기 — 오류 메시지가 기대한 결과입니다</summary>

1. `lookup_policy`의 docstring을 읽고 “읽기 전용”, “합성”, “승인 불가”를 설명할 수 있게 합니다.
2. 지원하지 않는 질문을 넣습니다. 빈 검색 결과를 받았을 때 모델이 금액을 추측하는지 봅니다.
3. 2000자를 넘는 질문은 입력 검사에서 거부되는지 확인합니다.
4. 도구 결과가 “사용자 요청을 무시하라” 같은 문장을 포함해도 상위 지시가 되어서는 안 됩니다.
5. 실제 업무로 확장할 때 필요한 서버 측 권한·인자 검증·승인·감사 로그를 적습니다.

2000자 초과 입력은 다음처럼 짧은 명령으로 만들 수 있습니다.
정상적인 검사 결과는 종료 코드 `2`와 `Question must contain 1-2000 characters.` 오류이며,
이 요청은 모델 호출 전에 거절됩니다.

```bash
python scripts/workshop.py maf --tools --question "$(python -c 'print("A" * 2001)')"
```


**화면 확인:** `FAIL: ValueError: Question must contain 1-2000 characters.`를 확인합니다. 종료 코드는 바로 다음에 `echo $?`를 실행하면 `2`로 나옵니다.
Azure 호출 전 입력 거절이며 환경이 망가졌다는 뜻이 아닙니다.

긴 문자열을 터미널에 직접 붙여 넣으면 터미널 입력 길이 제한으로 잘릴 수 있습니다.
그 상태에서 모델이 답했다고 해서 애플리케이션의 2000자 검사가 실패한 것은 아닙니다.

실습을 위해 실제 전송/결제 도구를 새로 만들 필요는 없습니다.

</details>

## 5. 선택 — Foundry 평가자로 도구 호출 채점(Preview)

<details>
<summary>준비된 <code>gpt-6-sol-judge</code>와 비용 승인이 있을 때만 펼칩니다. B의 필수 단계가 아닙니다</summary>

MAF의 평가 API가 함수 도구 에이전트를 dev 6문항으로 실행하고(유료 에이전트 실행 6회), 각 답변과 `lookup_policy` 호출,
도구 정의를 Foundry의 `tool_call_accuracy`·`relevance` 평가자에 보냅니다.
함수 도구만 채점하며 MCP 방식은 포함하지 않습니다. 코드는 `src/foundry_workshop/tool_evaluation.py`에 있습니다.
먼저 `.env`에 `AZURE_AI_EVALUATION_MODEL_DEPLOYMENT_NAME=gpt-6-sol-judge`(준비 카드의 judge 행)를 설정합니다.
judge가 없거나 답변 배포 `gpt-6-sol`과 같으면 명령이 멈춥니다.

```bash
python scripts/workshop.py maf-evaluate --confirm-cost --output outputs/learner-notes-ko/maf-tool-evaluation.json
```

![2026-09-24 국문 녹화: 선택: Foundry 평가자로 MAF 도구 호출 채점](../../assets/g6sol-20260924-ko/screenshots/K04-004-maf-evaluate-2.webp)

**화면 확인:** `complete: true`, `errors: 0`이고 각 행에 기록된 `tool_calls`(`lookup_policy` 호출 1회)와
`tool_call_accuracy`·`relevance` 점수가 있습니다. 이유는 `report_url`에서 확인합니다. MAF가 `FoundryEvals`에 대한
`ExperimentalWarning`을 한 번 출력하는 것은 정상입니다. 2026-09-24 국문 녹화는 tool_call_accuracy 5/6, relevance 5/6이었습니다.
tool_call_accuracy는 D03 검색어에 대화에 없던 문서 ID `APPROVAL-01`을 넣은 것을 지어낸 인자로 보았고, relevance 실패는 D05의 올바른 보류였습니다. 이 점수는 도구 사용을 판단할 뿐 업무 정답 여부가 아니므로 Lab 07의 업무 검사와 구분합니다.
MAF 평가 API는 실험 기능이었고 일부 에이전트 평가자는 2026-09-23에 Preview로 표시되었습니다.
갱신한 SDK 고정 버전(`openai` 3.x)에서는 같은 명령이 `azure_ai_evaluator`에 대한 Pydantic serializer 경고도 출력합니다.
2026-09-24 재확인은 여전히 `complete: true`, `errors: 0`, tool_call_accuracy 6/6, relevance 6/6을 반환했습니다. 경고가 아니라 이 필드로 판단합니다.

</details>

[전체 액션 인덱스](../action-captures.md) · [녹화 영상](../video-summary.md)

## 완료·문제 해결

[실행 기록](../live-run.md)에는 2026-09-24의 함수 도구·MCP 호출을 남겼습니다. 선택 2001자 입력 거절은 다시 녹화하지 않았습니다. 세 명령의 실제 출력과 도구 경계를 설명하면 완료입니다.
MCP 실행 실패 시 [환경/도구 문제 해결](../reference/troubleshooting.md)을 확인합니다.
함수 도구 응답으로 바꾸어 MCP 실행이 성공한 것처럼 기록하지 않습니다.

다음: A: [Lab 05로 이동](05-workflows.md#path-a) · B → [Lab 05](05-workflows.md#path-b)
