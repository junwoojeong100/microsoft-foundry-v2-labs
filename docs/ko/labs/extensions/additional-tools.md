# 추가 도구: 실제 생성 파일과 API 경계 검증하기

[English](../../../labs/extensions/additional-tools.md) | **한국어**

**B/C 선택.** 먼저 동봉 정책 6개를 사용하는 **Code Interpreter**를 진행합니다.
OpenAPI는 별도 분기이며 어느 쪽도 실제 회사 데이터가 필요하지 않습니다.

**준비:** 프로젝트/모델, 도구의 지역·모델 지원, 전용 agent/파일 생성 권한, 모델과 sandbox 비용 승인.
**완료:** 실제 code call이 생성한 CSV를 내려받아 원문 ID/title 6행을 모두 검증함.
**중단:** 원래 오류·파일 ID를 남깁니다. 로컬에서 정답 파일을 만들어 도구 결과라고 표시하지 않습니다.

**첫 회차:** Code Interpreter 1–4절 후 인계합니다. OpenAPI는 별도 선택이며
CSV를 확인한 뒤 반드시 실행할 두 번째 도구가 아닙니다.

## 1. 검증 범위

원문 6개로 CSV를 만들고, 같은 순서의 `id,title` 두 열을 요청합니다.
정책 답변·금액 계산·모델 순위를 평가하는 실험이 아닙니다.
Code Interpreter의 session/container 비용은 모델 토큰과 별도이며 채팅 중지가 즉시 모든 과금을 없애지는 않습니다.

## 2. 한 번 실행

```bash
python scripts/workshop.py --language ko code-interpreter run --label code-policy-table --confirm-create --confirm-cost
```

helper가 합성 CSV만 업로드하고 새 이름의 Prompt Agent를 만듭니다.
반환된 버전을 고정하고 실제 Code Interpreter 호출을 요구합니다.
임의 사용자 파일이나 다른 corpus로 교체하지 않습니다.

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

실제 code call이 보고한 container의 CSV 하나만 허용합니다.
모델이 제시한 경로를 그대로 신뢰하지 않고 고정 로컬 파일명에 저장합니다.
열·누락·중복·순서·title 변경은 검증 실패입니다. 틀린 출력도 그대로 보관합니다.

## 4. 내 임시 리소스 정리

```bash
python scripts/workshop.py --language ko code-interpreter cleanup --label code-policy-table --confirm-delete
```

기록된 전용 agent 버전·업로드 파일·container만 처리합니다.
추가 버전이나 프로젝트/이름 불일치가 있으면 거부하고 로컬 근거를 유지합니다.
삭제 상태와 잔여 비용은 별도로 확인합니다.

## 5. OpenAPI 분기: 기존 합성 Search API

<details>
<summary>선택적인 독립 OpenAPI 실습 — Lab 06의 본인 index와 런타임 ID가 필요합니다</summary>

OpenAPI는 HTTP API 계약이며 Python 함수, A2A endpoint, sandbox와 다릅니다.
Lab 06의 **내 정책 index**만 사용하는 read-only Search REST 작업을 노출합니다.
API Management, 새 API server, 회사 연결을 만들지 않습니다.
여기서 POST는 검색 요청이지 문서 업로드/수정/삭제가 아닙니다.

담당자가 같은 Search endpoint/index와 seed ledger, 실제 호출 ID/권한,
token audience, 요청/응답 schema, 비용 제한과 정리 책임을 확인합니다.
관리 ID의 Search Index Data Reader와 audience **`https://search.azure.com`**가 필요합니다.
로컬 사용자 권한이나 Foundry endpoint와 구분합니다.

```bash
python scripts/workshop.py --language ko openapi plan
```

서버·index 하나의 읽기 전용 계획과 런타임 권한을 확인한 뒤 유료 요청을 실행합니다.

```bash
python scripts/workshop.py --language ko openapi invoke --label openapi-policy --confirm-cost
```

계획은 server 하나, 내 index 경로 하나, `SearchSyntheticPolicies` 작업 하나여야 합니다.
`outputs/openapi-runs/openapi-policy/`의 plan/request/response/summary를 확인합니다.
실제 completed `openapi_call`과 원문 결과·명세 hash·응답/모델 metadata를 남깁니다.
그럴듯한 답변이나 다른 native Search 호출은 이 도구의 증거가 아닙니다.

오류 뒤에 key를 추가하거나 `retrieve --provider search`로 바꾸지 않습니다.
index/ID 권한이 없으면 **미실행**입니다.
직접 Responses 요청은 영구 Prompt Agent를 만들지 않지만 source/index/model과 추가 역할은 담당자가 정리합니다.

</details>

**다음:** [Toolbox](toolbox.md), [C 모듈](../../paths/c-advanced.md), [Lab 11](../11-capstone.md).
[Code Interpreter](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/code-interpreter) ·
[OpenAPI](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/openapi).
