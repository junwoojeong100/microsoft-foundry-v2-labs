# 추가 도구: 실제 생성 파일과 API 경계 검증하기

[English](../../../labs/extensions/additional-tools.md) | **한국어**

**B/C 선택.** 먼저 동봉 합성 정책 record 6개를 사용하는 **Code Interpreter**를 진행합니다.

**근거 상태:** 영문 Code Interpreter·OpenAPI 결과는 2026-09-16(이전 `gpt-5.6-luna` preset) 기록이며 `gpt-6-sol`로 다시 실행하지 않았습니다.

OpenAPI는 별도 분기이며 어느 쪽도 실제 회사 데이터가 필요하지 않습니다.

**준비:** 프로젝트/모델, 도구의 지역·모델 지원, 전용 agent/파일 생성 권한, 모델과 sandbox 비용 승인.
**완료:** 실제 code call이 생성한 CSV를 내려받아 원문 ID/title 6행을 모두 검증함.
**중단:** 원래 오류·파일 ID를 남깁니다. 로컬에서 정답 파일을 만들어 도구 결과라고 표시하지 않습니다.

**첫 회차:** Code Interpreter 1–4절 후 인계합니다. OpenAPI는 별도 선택이며
CSV를 확인한 뒤 반드시 실행할 두 번째 도구가 아닙니다.

## 1. 검증 범위

입력 CSV는 canonical 정책 문서 6개에서 파생됩니다.
요청한 출력은 정확히 `id,title` 두 열과 같은 순서의 6행입니다.
정책 답변·금액 계산·모델 순위를 평가하는 실험이 아닙니다.

Code Interpreter에는 모델 token 외에 session/container 비용이 추가됩니다.
예시는 chat 중지가 그런 비용을 즉시 없앤다고 약속하지 않습니다.

## 2. 한 번 실행

```bash
python scripts/workshop.py --language ko code-interpreter run --label code-policy-table --confirm-create --confirm-cost
```

helper는 생성한 합성 CSV만 업로드하고 고유 이름의 Prompt Agent를 만듭니다.
반환된 버전을 request에 고정하고 실제 Code Interpreter 도구 호출을 요구합니다.
임의 사용자 선택 파일을 load하거나 다른 input corpus를 허용하지 않습니다.

## 3. 원본 결과 확인

`outputs/code-interpreter/code-policy-table/`:

| 파일 | 확인 |
|---|---|
| `policy-records.csv` | 원래 합성 입력 6행 |
| `ownership.json` | 업로드 파일·agent/버전·container의 실제 ID |
| `request.json` | 고정 작업과 버전 |
| `response.json` | 실제 completed code call과 생성 파일 인용 |
| `policy-summary.csv` | 실제 container file API에서 내려받은 파일 |
| `summary.json` | 원본/생성 hash와 `verified_rows: 6` |

helper는 code call이 실제 보고한 container의 생성 CSV citation 하나만 허용합니다.
모델이 제시한 경로를 그대로 신뢰하지 않고 고정 로컬 파일명에 저장합니다.
열·누락·중복·순서·title 변경은 검증 실패입니다. 틀린 출력도 그대로 보관합니다.

## 4. 내 임시 리소스 정리

```bash
python scripts/workshop.py --language ko code-interpreter cleanup --label code-policy-table --confirm-delete
```

기록된 전용 agent 버전·업로드 파일·container만 처리합니다.
추가 버전이나 프로젝트/이름 불일치가 있으면 거부하고 로컬 근거를 유지합니다.
resource 상태를 다시 읽고 잔여 청구를 확인합니다. cleanup 요청은 비용이 0이라는 증거가 아닙니다.

## 5. OpenAPI 분기: 기존 합성 Search API

<details>
<summary>선택적인 독립 OpenAPI 실습 — Lab 06의 본인 index와 런타임 ID가 필요합니다</summary>

OpenAPI는 HTTP API 계약이며 Python 함수, A2A endpoint, sandbox와 다릅니다.
Lab 06의 **내 정책 index**만 사용하는 read-only Search REST 작업을 노출합니다.
API Management, 새 API server, 회사 연결을 만들지 않습니다.
여기서 POST는 검색 요청이지 문서 업로드/수정/삭제가 아닙니다.

호출 전 담당자가 다음을 확인합니다.

- synthetic seed ledger와 같은 `AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_INDEX_NAME`.
- 인증과 token audience. prompt에 key나 secret을 복사하지 않습니다.
- caller identity와 target 권한.
- 정확한 요청/응답 shape, 안전한 test input, 비용/rate 한계, cleanup owner.

OpenAPI runtime의 managed identity에는 해당 service의 Search Index Data Reader가 필요합니다.
token audience는 Foundry project endpoint가 아니라 **`https://search.azure.com`**입니다.
이는 local user의 Search 접근과 별개입니다.

```bash
python scripts/workshop.py --language ko openapi plan
```

서버·index 하나의 읽기 전용 계획과 런타임 권한을 확인한 뒤 유료 요청을 실행합니다.

```bash
python scripts/workshop.py --language ko openapi invoke --label openapi-policy --confirm-cost
```

계획은 server 하나, 내 index 경로 하나, `SearchSyntheticPolicies` 작업 하나여야 합니다.
`outputs/openapi-runs/openapi-policy/`의 plan/request/response/summary를 확인합니다.
응답에는 실제 completed `openapi_call`이 있어야 합니다. 그럴듯한 답변이나 native Search 호출만으로는 충분하지 않습니다.
명세 hash, 실제 source data, response/model metadata를 보존합니다.

오류 뒤에 key를 추가하거나 `retrieve --provider search`로 바꾸지 않습니다.
index/ID 권한이 없으면 **미실행**입니다.
직접 Responses 요청은 영구 Prompt Agent를 만들지 않지만 source/index/model과 추가 역할은 담당자가 정리합니다.

</details>

**다음:** [Toolbox](toolbox.md), [C 모듈](../../paths/c-advanced.md), [Lab 11](../11-capstone.md).
[Code Interpreter](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/code-interpreter) ·
[OpenAPI](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/openapi).
