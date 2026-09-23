# Foundry IQ·Toolbox·Fabric·Work IQ 확장 워크북

[English](../../reference/iq-workbook.md) | **한국어**

**확인 기준 2026-09-15. 기본 실습은 번들 합성 정책만 사용합니다.**
외부 연결은 기본 경로와 별도이며, 이 개정에서 실제 회사·Microsoft 365·Fabric 데이터를 조회하지 않습니다.
아래 설계/승인 절차를 읽은 것을 실제 연결 성공으로 표시하지 않습니다.

## 1. 기본 IQ 경로를 이 저장소에서 끝내기

참고 문서이지 Lab 06을 한 번 더 실행하는 순서가 아닙니다. 완료한 단계와 근거를 재사용합니다.
선택한 source를 아직 seed하지 않았다면 승인된 작성자의 대응 작업 폴더에서만 실행합니다.

```bash
python scripts/workshop.py seed-search --iq --confirm-create
```

Seed 성공 후 검색과 로컬 workflow를 확인합니다.

```bash
python scripts/workshop.py retrieve --provider iq --question "2026년 9월 국내 출장 숙박비와 한도 초과 사전 승인 규정"
python scripts/workshop.py workflow-agent --pattern sequential --retrieval iq --prompt v2
```

핵심 흐름은 **실제 GA retrieve → 원문/ID/activity 보존 → MAF 참여자 → 검증된 최종 답**입니다.
인증은 로컬 CLI 계정과 원격 managed identity를 구분합니다.
원격 IQ matrix는 [평가 워크북 준비](evaluation-workbook.md#matrix-setup)에서 이어갑니다.
그곳에서 IQ/account-chat/Invocations 프로필을 별도로 만듭니다.
Lab 08의 로컬 검색·Responses 패키지는 다른 대상이며 이 IQ 실행의 단축 경로가 아닙니다.

| 자산 | 역할 | 혼동하지 않을 것 |
|---|---|---|
| Search index | 실제 합성 원문 | 서비스 생성 자체와 문서 적재/조회 |
| Knowledge source/base | IQ 검색 원본/검색 단위 | File Search vector store |
| `references` | 응답 내부 참조 정보 | 참조 번호와 실제 document ID |
| `activity` | 실제 검색 처리 정보 | 측정되지 않은 비용·지연을 0으로 채우기 |
| `context_hash` | 실제 반환된 원문 집합 | 로컬 corpus hash만으로 원격 index 불변성 보장하기 |

현재 기본 코드는 `2026-04-01`의 직접 intents·extractive 검색이며 KB 모델을 구성하지 않습니다.
**Chat 모델을 managed identity로 구성하는 경로는 정상 지원됩니다.**
Search identity에 모델 권한을 부여하고 별도 base에서 모델 기반 계획·합성을 검증합니다.
포털의 모델 미선택 메시지와 MI 인증 오류를 구분하세요.
[설정 순서·호출 주체·실제 확인 결과](iq-model-identity.md)를 따릅니다.
선택 Chat 실험의 첫 선택은 **`iq-chat`의 `gpt-5.6-luna` / `2026-07-09`, Search SMI, `low`, `answerSynthesis`**입니다.
`gpt-6-sol` 응답 모델과 별도입니다(2026-09-23 Search가 GPT-6 모델을 받지 않음).
[준비 순서](../setup.md#4-환경-담당자의-준비)는 별도 base를 만들며 위 GA workflow/평가 target을 변경하지 않습니다.

## 2. 하이브리드와 IQ의 선택

[Lab 06](../labs/06-knowledge.md)의 `--hybrid`는 실제 embedding과 text/vector query를 사용합니다.
`--provider search`는 텍스트, `--provider iq`는 knowledge-base retrieve입니다.
한 provider의 오류를 다른 provider로 숨기지 않습니다.

비교 실험은 같은 데이터·질문·model/prompt를 고정하고 **retrieval만 바꾸는 별도 실험**으로 기록합니다.
이때 결과의 실제 원문과 비용/지연을 함께 봅니다.
벡터 index를 만들었다고 IQ가 그 벡터를 사용했다고 단정하지 않습니다.

## 3. 선택: 관리형 Toolbox와 Microsoft Learn

**실행 가능한 합성 정책 Toolbox**는 [Toolbox 실습](../labs/extensions/toolbox.md)을 따릅니다.
아래의 기존 Microsoft Learn 예제는 선택적인 문서 조회 패턴이지 그 선행 조건이 아닙니다.

<details>
<summary>선택적인 문서 도구 연결 참고 — 정책 도구를 다시 만드는 실습이 아닙니다</summary>

**도구 연결을 준비/승인한 강사만 진행합니다.**
기본 정책 답변에 외부 웹이 필요하지 않으므로, 공통 v2 pipeline에는 자동 연결하지 않습니다.
공개 플랫폼 설명을 확인하는 별도 질문에만 Microsoft Learn 같은 승인된 원본을 사용합니다.

1. 현재 Foundry 프로젝트의 **Tools / Toolbox**에서 전용 toolbox를 정합니다.
2. Microsoft Learn MCP 등 승인된 읽기 전용 서버만 연결합니다. 이름만 읽기 전용이라고 믿지 말고 실제 서버·권한을 검토합니다.
3. Work IQ/Graph/예약/메일/결제 같은 변경 도구는 이 실습 toolbox에 넣지 않습니다.
4. 관리 화면에서 반환한 **실제 MCP endpoint와 도구 목록**을 기록합니다.
5. 호출자의 Foundry 권한과 upstream MCP의 서버 측 connection 인증을 각각 확인합니다.
6. 실제 실행 후 trace에서 도구 호출과 결과/오류를 확인합니다. `tools/list` 성공만으로 올바른 답변을 받았다고 하지 않습니다.

2026-09-15 공식 Python 계약은 `agent_framework.foundry.FoundryToolbox`입니다.
이 클래스는 prerelease hosting 패키지에서 제공되며 별도의 project connection을 대신 생성해 주지는 않습니다.
명시적 endpoint 형식은 다음과 같습니다.

```text
https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/<name>/mcp?api-version=v1
```

다음은 **이미 준비한 client/credential에 toolbox를 결합하는 코드 패턴**입니다.
실제 endpoint·connection·allowed tool 검토 없이 그대로 실행하는 예제가 아닙니다.

```python
from agent_framework import Agent
from agent_framework.foundry import FoundryToolbox
from agent_framework_foundry_hosting import ResponsesHostServer

toolbox = FoundryToolbox(credential, url=approved_toolbox_endpoint, load_prompts=False)
agent = Agent(
    client=client,
    name="ApprovedDocumentationGuide",
    instructions="승인된 공식 문서로 플랫폼 개념만 설명하세요. 회사 정책을 추측하지 마세요.",
    tools=[toolbox],
    default_options={"store": False},
)
server = ResponsesHostServer(agent)
```

호스트가 Agent/MCP 연결의 생명주기를 관리합니다.
수동 bearer token을 코드·`.env`에 복사하지 않습니다.
동일 toolbox를 managed `FoundryAgent`에 쓰려면 서비스에 저장된 **agent definition**에 연결해야 하며,
로컬 client 객체에 도구를 붙였다는 것만으로 원격 agent가 바뀌지 않습니다.
구체적인 최신 연결·패키징 방식은 [Toolbox 공식 계약](https://learn.microsoft.com/agent-framework/integrations/by-component/tools/foundry-toolbox)
및 [Hosted 연결 가이드](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/use-toolbox-hosted-agent)에서 확인합니다.

</details>

## 4. Fabric IQ — 자산 종류에 따라 인증을 구분

필수 준비:

- **합성 데이터만** 담긴 Fabric workspace와 사용 가능한 capacity.
- 실제 게시된 Data Agent/semantic model/ontology의 종류와 ID.
- 사용자 또는 workload identity의 최소 읽기 권한.
- tenant·network·지역·처리/보존 정책, 비용과 종료 책임자.

2026-09-15 [공식 Fabric IQ 가이드](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/fabric-iq)는
자산별 인증을 구분합니다.

| 자산 | 확인할 인증 경계 |
|---|---|
| Ontology / Power BI semantic model | 사용자 delegated/OBO 맥락 |
| 게시된 Fabric Data Agent MCP | 해당 endpoint는 user 또는 service-principal token을 지원할 수 있음 |
| 직접 Data Agent MCP 호출 | 공식 문서의 `https://api.fabric.microsoft.com/.default` 범위와 실제 identity 권한 확인 |

Data Agent MCP의 app-only 지원을 **모든 Fabric IQ source가 app-only를 지원한다**는 뜻으로 확대하지 않습니다.
관리자 한 명의 성공은 모든 사용자의 권한을 증명하지 않습니다.

승인된 별도 세션에서는 자산 준비 → 연결 정의 → 대상 identity로 첫 질문 → 원문/집계 정의 확인 →
낮은 권한 사용자 거절 확인 → 연결/비용 복원 순으로 진행합니다.
자산 생성·capacity 준비는 이 워크북의 수업 시간에 포함하지 않습니다.

## 5. Work IQ — 이 기본 실습에서는 연결하지 않음

이 저장소의 기본 경로는 Microsoft 365에 접근하지 않습니다.
실제 Work IQ가 필요한 별도 프로젝트에서는 관리자가 현재
[knowledge-source 요구사항](https://learn.microsoft.com/azure/search/agentic-knowledge-source-how-to-work-iq)을 확인합니다.

2026-09-15 확인한 중요 항목:

1. Copilot Studio에서 구성한 usage-based billing plan과 **사용자별 할당**.
2. tenant의 Work IQ enablement 및 관리자 작업.
3. 사용자를 로그인시키고 user assertion을 보내는 client.
4. `WorkIQAgent.Ask` delegated permission과 필요한 관리자 동의.
5. `2026-08-01-preview`의 customer-owned Entra app + federated identity credential 방식.

`entraAppAuthentication.applicationId`는 app client ID,
`federatedCredentialId`는 **credential 객체 ID**입니다. credential 이름이나 Search principal ID가 아닙니다.
같은 tenant와 다른 tenant의 조건도 현재 공식 문서로 확인하며 과거 same-tenant 예제를 보편적 제한으로 복사하지 않습니다.
client secret을 knowledge source나 `.env`에 저장하는 방식으로 우회하지 않습니다.

기본 실습에서 Work IQ 승인이 없으면 `미실행`입니다.
오류 후 synthetic 결과로 전환하거나, 합성 라우팅을 실제 Work IQ 성공으로 제출하지 않습니다.
기존 자료에 `synthetic fallback` 표현이 있어도 v2에서는 **명시적으로 분리한 합성 설계 실습**으로만 다룹니다.

## 6. Hosted ID와 사용자 대리(OBO) 확인표

| 확인 | 필요한 증거 |
|---|---|
| 실제 caller | 서비스별로 요구하는 user 또는 workload identity |
| token audience | Foundry/Search/Fabric/Work IQ 중 어느 서비스용인가 |
| 권한 경계 | 같은 질문에 권한 있는 사용자와 낮은 권한 사용자의 결과가 다른가 |
| 전달 경로 | 로컬/원격에서 identity propagation이 실제로 이루어졌는가 |
| 기록 범위 | message-content capture, 민감정보, 보존 기간과 조회 권한 |
| 취소/복원 | consent·connection·capacity·billing의 담당자와 복원 범위 |

이 표는 검증 절차이지 자동으로 사용자 impersonation을 구현하는 코드가 아닙니다.
source가 user context를 요구하면 host의 managed identity만으로 대신하지 않습니다.
동의/인증/네트워크 오류를 다른 계정·다른 source로 우회하지 않습니다.

## 7. 평가와 정리

IQ를 사용한 Hosted 업무 응답은 [같은 target의 평가 워크북](evaluation-workbook.md)으로 평가합니다.
공식 문서 질문, 합성 정책 질문, Fabric 집계, Work IQ 협업 질문의 rubric을 하나의 점수로 합치지 않습니다.
도구·원문·날짜·identity·실제 evaluator의 input을 각각 보존합니다.

추가 connection은 본인 실습 자산만 복원/정리하고 조직 전체 consent나 다른 팀의 capacity를 지우지 않습니다.
비활성화 상태, 남은 비용, 선택 기능 `미실행` 여부를 기록합니다.
이 선택 경로까지 원본을 대체했다고 선언하려면 [아카이브 인수 기준](consolidation.md)의 별도 live 게이트를 먼저 통과해야 합니다.
