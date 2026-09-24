# 관리형 Toolbox: 합성 정책 도구 하나와 고정 버전 하나

[English](../../../labs/extensions/toolbox.md) | **한국어**

**B 확장.** Toolbox는 재사용 도구를 제공하는 관리형 MCP endpoint입니다.
첫 실습은 Search에 적재한 동봉 정책 6개만 읽습니다. Work IQ, 회사 API, 공개 웹,
임의의 MCP 서버를 연결하지 않습니다.

**첫 회차:** 1–5절 후 7절의 인계·정리로 끝냅니다. 6절의 default 버전 변경은 선택입니다.

**준비:** 성공한 [Lab 06 Search](../06-knowledge.md), 같은 B 환경의 [Hosted/Toolbox SDK extra](developer-toolkit.md#hosted-sdk), 준비된 키 없는 Search 프로젝트 연결, 내 Toolbox 생성 승인.
**완료:** 고정 버전의 MAF 요청에 실제 도구 결과·모델 응답·버전 근거가 있음.
**중단:** 오류를 보존하고 담당자에게 돌아갑니다. 다른 provider로 교체하지 않습니다.

**근거 상태, 2026-09-16(이전 `gpt-5.6-luna` 판):** 영문 MCP discovery, 직접 Search 조회, MAF 답변, 버전 연결을 실행했습니다.
아래 `gpt-6-sol` 시도는 직접 query에서 멈췄습니다.

**2026-09-25(`gpt-6-sol`, 영문):** keyless `workshop-search` 연결로 생성·조회·MCP 탐색은 성공했습니다.
프로젝트 managed identity에 Search Index Data Reader만 있어 직접 query는 **Access denied**였고, 답변 요청은 하지 않았습니다.
소유 Toolbox는 삭제했고 역할은 바꾸지 않았습니다.

## 1. 담당자에게 두 값을 받기

기존 `.env`의 프로젝트·모델·Search 설정을 유지하고 추가합니다.

```dotenv
TOOLBOX_SEARCH_CONNECTION_NAME=<실제-keyless-Search-프로젝트-연결>
TOOLBOX_NAME=<내-prefix>-tools-ko
```

연결 대상은 같은 `AZURE_SEARCH_ENDPOINT`, 도구의 index는 같은 `AZURE_SEARCH_INDEX_NAME`이어야 합니다.
이는 Foundry 프로젝트의 Search 연결이며 Search index 이름, IQ base, File Search store 이름이 아닙니다.

담당자는 Microsoft Entra 인증으로 연결을 한 번 만들고 실제 upstream identity의 Search 권한을 확인합니다.
영문 실험에서는 **프로젝트 관리 ID**의 기존
Search Index Data Reader에 Search Service Contributor가 추가로 필요했습니다.
account ID에 contributor 역할만 주는 시도는 해결하지 못했고 그 시험 권한은 제거했습니다.
API key는 사용하지 않습니다. 승인된 연결이 없으면 이름을 만들어내지 말고 여기서 멈춥니다.
호출자는 Toolbox metadata/생성과 실제 도구 실행을 위해 Foundry 프로젝트 접근 권한이 필요합니다.
연결 생성이나 역할 부여는 별도 승인 작업입니다.
Search Service Contributor는 Search object를 관리할 수 있으며 **읽기 전용 역할이 아닙니다**.
프로덕션 Search service가 아니라 전용 합성 학습 서비스와 담당자가 승인한 scope를 사용합니다.
통합 방식에 따라 identity 동작이 다를 수 있으므로 이 호출자를
[IQ chat preset에서 사용하는 Search identity](../../reference/iq-model-identity.md)와 혼동하지 않습니다.
4절의 직접 조회가 downstream 접근을 검증하며, 역할 이름이나 성공한 로컬 로그인만으로는 충분하지 않습니다.

## 2. 실제 계획 확인

```bash
python scripts/workshop.py --language ko toolbox plan
```

내 프로젝트·이름과 `policy_search`, `azure_ai_search`, `simple`, `top_k: 6`을 확인합니다.
생성 시 논리적 연결 이름을 **실제 전체 프로젝트 연결 resource ID**로 해석해 기록합니다.
raw `project_connection_id`에 이름만 넣고 같은 동작이라고 가정하지 않습니다.
`azure_requests_sent: false`는 계획일 뿐 실행 성공이 아닙니다.
일반 도구 경로가 동작하기 전에는 Tool Search나 Skills를 추가하지 않습니다.

## 3. 첫 버전 생성

담당자가 이 쓰기 작업을 승인한 뒤 실행합니다.

```bash
python scripts/workshop.py --language ko toolbox create --confirm-create
```

`selected_version`, `default_version`, 버전별 endpoint, `definition_hash`, ledger를 보관합니다.
기존 이름은 가져오거나 덮어쓰지 않고 거부합니다.
소유 기록은 `outputs/toolboxes/<name>/ownership.json`입니다.

같은 터미널에서 반환된 버전을 입력합니다.

```bash
printf '생성 결과의 selected_version: '
read -r TOOLBOX_VERSION
python scripts/workshop.py --language ko toolbox inspect --version "$TOOLBOX_VERSION"
```

버전 없는 endpoint는 Toolbox의 현재 default를 따라갑니다. 이 실습은 이후 promotion이 실험을 조용히 바꾸지 못하도록 **버전별 endpoint**를 호출합니다.
현재 default와 선택한 버전은 별도 값입니다.
Toolbox 버전은 불변이지만 연결과 Search index의 내용은 바뀔 수 있습니다.
비교 중에는 함께 고정하고 로컬 corpus hash만이 아니라 반환된 실제 도구 근거를 보존합니다.

## 4. MCP 연결과 실제 검색을 따로 확인

```bash
python scripts/workshop.py --language ko toolbox probe --version "$TOOLBOX_VERSION" --label toolbox-first-list
```

실제 목록에는 정확히 `policy_search`가 있어야 합니다. 이때 `model_invoked: false`,
`tool_invoked: false`는 MCP 연결/discovery를 확인하는 단계라 정상이며 답변을 확인하는 단계가 아닙니다.
`binding.json`, `tool-list.json`, `summary.json`을 확인합니다.
인증, 초기화 또는 도구 discovery가 실패해도 다른 endpoint, API key, Lab 04의 로컬 MCP server로 우회하지 않습니다.

모델 비용을 쓰기 전에 upstream Search를 직접 확인합니다.

```bash
python scripts/workshop.py --language ko toolbox query --version "$TOOLBOX_VERSION" --label toolbox-direct-query --confirm-cost
```

`tool_invoked: true`, `model_invoked: false`가 기준입니다.
이 단계는 **client → Toolbox discovery**와 **Toolbox → Search access**를 분리합니다.
권한 문제에는 원래 실패를 남기고 실제 주체의 범위만 수정합니다. 알려진 권한 오류에 모델 호출을 반복하지 않습니다.

## 5. 실제 MAF 요청 한 번

비용 승인 후 실행합니다.

```bash
python scripts/workshop.py --language ko toolbox ask --version "$TOOLBOX_VERSION" --label toolbox-first-answer --confirm-cost
```

동봉한 2026년 9월 한도 초과 숙박 질문을 사용합니다.
설치된 `FoundryToolbox` wrapper와 명시한 model deployment로 MAF를 사용합니다.
wrapper가 인증된 MCP 요청을 처리하며 Toolbox service의 임의 모사가 아닙니다.

**확인:**

- `model_invoked: true`와 `tool_invoked: true`.
- 정확한 Toolbox 버전/hash와 실제 service model-call ID.
- 실제 `tool-results.json`과 답변의 정책 ID·날짜·승인 조건.
- 필요한 사전 승인은 이 코드가 수행한 예약, 지급 또는 업무 승인이 아닙니다.

실행은 raw 도구/모델 결과와 실패를 보존합니다. 실제 도구 결과 없는 모델 답변은 거부합니다.

논리 모델 호출 6회와 180초 제한이 있으나 SDK/service 사용량까지 포함한 화폐 상한은 아닙니다.
새 요청에는 새 label을 사용합니다. 촬영을 위해 성공한 유료 요청을 반복하지 않습니다.

## 6. 통제된 버전 변경

<details>
<summary>선택 버전 실습 — 첫 실제 답변 확인 뒤에 반드시 할 단계가 아닙니다</summary>

같은 도구 설정을 유지하면서 설명만 바꾸는 새 버전을 생성합니다.
목적은 버전 선택을 배우는 것이며 품질 개선을 주장하는 단계가 아닙니다.

```bash
python scripts/workshop.py --language ko toolbox add-version --confirm-create
```

반환된 새 버전을 `TOOLBOX_CANDIDATE`로 기록합니다.

```bash
printf '새 selected_version: '
read -r TOOLBOX_CANDIDATE
python scripts/workshop.py --language ko toolbox probe --version "$TOOLBOX_CANDIDATE" --label toolbox-candidate-list
```

Probe가 성공하고 반환된 binding·도구 목록이 candidate와 일치한 뒤에만 계속합니다.
승인을 받은 뒤 default를 변경합니다.

```bash
python scripts/workshop.py --language ko toolbox select --version "$TOOLBOX_CANDIDATE" --confirm-update
```

반환된 default 버전을 확인한 뒤 원래 버전으로 복구합니다.

```bash
python scripts/workshop.py --language ko toolbox select --version "$TOOLBOX_VERSION" --confirm-update
```

마지막 명령은 원래 버전으로의 명시적 rollback입니다.
두 변경 모두 승인과 로컬 소유 기록이 필요합니다.
Toolbox default 변경으로 agent가 재배포되지는 않습니다.
버전 고정 실행은 consumer default가 바뀌어도 기록한 버전을 계속 가리킵니다.

</details>

## 7. 인계 또는 정리

Tool Search/Skills 또는 Hosted Toolbox로 계속 가면 소유한 Toolbox와 ledger를 유지합니다.
선택 버전·다음 모듈을 `session-notes.txt`에 적고 먼저 cleanup을 실행하지 않습니다.
끝내면 다른 승인된 agent가 참조하지 않는지 확인한 후 내 Toolbox만 삭제합니다.

```bash
python scripts/workshop.py --language ko toolbox cleanup --confirm-delete
```

원격 버전 집합과 소유 기록이 다르면 삭제를 거부합니다.
결과/소유/정리 기록을 보존하며 Search 연결·index·서비스·모델·프로젝트는 삭제하지 않습니다.
공유 리소스 비용은 담당자가 별도로 처리합니다.

## 복구

| 증상 | 할 일 |
|---|---|
| 연결 이름 누락·오류 | 담당자가 keyless CognitiveSearch 연결과 대상 서비스를 확인합니다 |
| metadata 또는 tool call에서 403 | 실제 호출 identity와 scope를 식별합니다. 로컬 로그인과 runtime 권한은 다릅니다 |
| 기존 Toolbox 이름 거부 | 내 고유 prefix/name을 사용합니다. 다른 학습자의 object를 삭제하지 않습니다 |
| default가 소유하지 않은 버전을 가리킴 | 선택하거나 삭제하기 전에 멈추고 다른 담당자의 변경을 검토합니다 |
| MCP 결과가 오류를 보고 | `failure.json`과 raw tool result를 보관합니다. endpoint/provider를 재시도하지 않습니다 |
| 모델이 도구를 사용하지 않음 | 실제 request/response와 도구 설명을 점검합니다. prose만으로 완료로 계산하지 않습니다 |

**다음:** [같은 Toolbox의 Hosted 실행](toolbox-hosted.md), [C 모듈](../../paths/c-advanced.md), [Lab 11](../11-capstone.md).
**날짜가 있는 참고 자료:** [Toolbox 수명 주기](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/toolbox) ·
[MAF wrapper](https://learn.microsoft.com/agent-framework/integrations/by-component/tools/foundry-toolbox).
