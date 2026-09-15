# 문제 해결: 다음 명령보다 원인을 먼저

[English](../../reference/troubleshooting.md) | **한국어**

**오류가 난 단계를 해결하기 전에는 배포·평가·삭제를 연속 실행하지 않습니다.**
같은 에러에 새 모델/새 구독/새 리소스를 무작정 만드는 것은 복구가 아닙니다.

| 증상 | 먼저 확인 | 복귀 |
|---|---|---|
| 프로젝트가 안 보임 | tenant, 계정, project 역할; 잘못된 운영 프로젝트 선택 금지 | 00–01 |
| `python3.13` 없음 | 지원 Python 설치 또는 강사가 준비한 환경 | 00 |
| `ModuleNotFoundError` | venv 활성화, 해당 extra 설치, `python -m pip check` | 00 |
| 패키지 다운로드 TLS/연결 오류 | 네트워크 정책·공식 PyPI 접근, 준비 환경 사용 | 00 |
| `.env`를 바꿔도 값이 다름 | 프로세스 환경변수가 우선인지 확인, 새 터미널 | 00 |
| 401 | 로그인/tenant/credential 종류, 로컬과 런타임 identity 구분 | 00 |
| `AADSTS90072` / 다른 기본 계정 선택 | `.env`의 구독과 계정 프로필 확인; 구독 범위 인증 사용. 기본 구독 변경·guest 초대·전체 logout으로 우회하지 않음 | 00 |
| 403 | 관리 평면과 데이터 평면 역할, 올바른 identity/scope, 반영 지연 | 01 |
| 404 모델 | 카탈로그 이름 대신 실제 배포 이름, 정확한 프로젝트 endpoint | 02 |
| 429 | quota·TPM·동시성·다른 조의 사용량, 서비스 retry 안내 | 02 |
| `json_schema`/옵션 400 | 모델별 Structured Outputs 지원, 현재 SDK 계약 | 02 |
| 응답 `incomplete` | 출력 token 한도, content filter, 모델 지원; 임의 보정 금지 | 02 |
| `FileExistsError` label | 기존 결과 보존 후 새로운 label 사용 | 07 |
| 원본 hash 불일치 | 응답/데이터를 수정하지 않았는지 확인; 새 버전으로 재수집 | 07 |
| MCP 실패 | 같은 venv의 `mcp`, 서버 path, stdout에 비-JSON 로그 여부 | 04 |
| workflow timeout | 최대 라운드·출력 한도·도구 지연·quota | 05 |
| Search 403 | Entra 데이터 평면 인증과 Index Data Reader/Contributor | 06 |
| Search 부분 upload 실패 | 개별 `status`, 문서 수·키, index 필드 | 06 |
| 기존 Search 객체 거부 | 내 접두사/소유권 ledger인지 확인; 공유 객체 덮어쓰기 금지 | 06 |
| IQ 400 | GA intents와 Preview messages를 혼합했는지, 실제 API 버전 | 06 |
| `Chat completions model is required` | 모델 미선택이지 MI 실패가 아님. **Luna + Search SMI**로 준비된 chat base를 열고 모델 없는 GA base에 포털 기본값을 저장하지 않음 | 06 |
| `iq-chat check`의 모델/버전/역할 실패 | [고정 preset](iq-model-identity.md)의 `gpt-5.6-luna` / `2026-07-09`·Search SMI·계정 범위 역할 확인. 담당자가 준비를 해결하며 대체 모델을 고르지 않음 | 06 |
| `ready_for_setup: true`, `configured: false` | 선행 조건은 통과했지만 별도 chat base는 아직 없음. Source를 소유한 작업 폴더에서 담당자가 승인된 setup 진행 | 06 |
| IQ Chat label이 이미 있음 | 이전 요청·응답·실패부터 읽고 명시적으로 승인한 새 유료 시도에만 새 label 사용 | 06 |
| IQ 모델 호출 401/403 | Search→모델 identity·계정 scope·RBAC 전파·네트워크 확인. Hosted/사용자 역할이 Search에 상속되지 않음 | 06 |
| Preview가 `maxOutputSizeInTokens` 거절 | 파라미터 검증 오류를 보존하고 확인한 버전별 `maxOutputSize` 요청 사용. 인증 실패로 분류하지 않음 | 06 |
| IQ references/activity 오류 | sourceData/docKey, source 설정, semantic·사용/과금 동의 | 06 |
| cloud judge timeout | 같은 label로 재조회; 저장된 eval/run ID 재사용 | 07 |
| evaluator 초기화 schema 오류 | 실제 catalog의 `model`/`deployment_name` 및 버전 확인 | 07 |
| holdout이 거부됨 | 후보 dev 통과·고정, 같은 code/prompt/model/provider, 명시적 unlock | 07 |
| 로컬은 성공, Hosted는 403 | 런타임 identity의 역할; 로컬 `az login` 반복 금지 | 08 |
| 로그/trace가 없음 | App Insights 연결, exporter, 시간 범위, 보존/보호 테이블 권한 | 09 |

## 새 workflow / benchmark 복구 기준

| 오류 | 확인할 것 |
|---|---|
| `runtime-profile.json` 없음 | 새 코드로 생성한 올바른 profile 패키지인지 확인. 이전 패키지를 새 workflow라고 재사용하지 않음 |
| runtime contract/code/prompt hash 불일치 | 로컬 프로필·소스와 실제 배포 version을 맞춘 뒤 새 label로 수집. manifest를 고쳐 통과시키지 않음 |
| model key가 allowlist에 없음 | `.env`와 remote service env의 같은 JSON map, 기본 배포 포함 여부 |
| `account-chat` endpoint 불일치 | 같은 Foundry account의 실제 OpenAI root. 실패했다고 자동 URL 전환 금지 |
| native timeout | 같은 label로 조회 재개. 새 job 자동 생성 금지 |
| native failed/invalid | 원본 시도를 보존한 `--retry-failed`. 완료된 낮은 점수의 반복 재시도는 거부 |
| 회귀 파일이 질문/정답을 바꿈 | 기존 dev 계약을 유지하거나 별도 dataset version 설계. holdout을 회귀로 사용하지 않음 |
| matrix 누락/중복 | 성공 prefix를 평가하지 않음. 원인을 해결한 후 새 label로 완전 수집 |
| trace 누락 | 정확한 App Insights app ID·agent·기간·권한·sampling을 확인. 0건을 정상 운영으로 처리하지 않음 |
| hybrid 차원/기존 index 충돌 | 실제 embedding 차원, 별도 본인 index, namespace/ledger 확인. 벡터 자르기·0 채우기 금지 |
| azd raw 출력 파싱 | HTTP 상태·UTF-8 바이트 길이·알려진 notice만 허용. 오류 뒤의 임의 JSON 추출 금지 |
| `--agent-endpoint cannot be combined with --protocol` | full endpoint가 protocol을 포함하므로 원격 smoke에서는 `--protocol`을 별도로 붙이지 않음. 로컬은 명시 |
| batch의 API version 누락 | session ID를 추가할 때 URL query를 대체하지 않고 merge. `api-version=v1`과 `agent_session_id`를 둘 다 보존 |
| embedding의 프로젝트 API 404 | 동일 계정 endpoint와 `WORKSHOP_EMBEDDING_API=account`를 사전에 명시. 실패 원본을 남기며 자동 endpoint 전환 금지 |
| App Insights `InvalidTokenError` | 지정된 구독/tenant credential과 App Insights 전용 audience로 동일 query API를 호출. 잘못된 identity로 대체하지 않음 |
| CLI 확장이 Incompatible | [버전 게이트](versions.md)를 검토하고 호환 조합을 따로 승인·설치한 후 재확인 |

## 네트워크 제한

[IQ 모델 identity 가이드](iq-model-identity.md)에 기본 모델 없는 GA 경로와 지원되는 MI 계획·합성 경로, 실제 확인 결과를 구분했습니다.

`PublicNetworkAccessDisabled`, private endpoint 403 또는 timeout이면 공용 네트워크에서
격리된 프로젝트에 접근하는 상황인지 확인합니다.
방화벽·private access·인증서 검증을 끄지 않습니다.
관리자가 승인한 VNet 접근 경로를 쓰거나 준비된 실습 환경으로 이동합니다.
Foundry MCP로 다른 경로를 시도했다고 네트워크 제한이 해제되는 것도 아닙니다.

## 설치 실패 시 하지 않을 일

- `--trusted-host`, TLS 검증 해제, 출처 불명의 패키지 미러 사용.
- 전역 Python에 설치하거나 다른 프로젝트의 가상환경을 수정.
- 전체 SDK를 `--upgrade --pre`로 일괄 변경.
- 실제 설치를 하지 않은 채 PyPI에 버전이 있다는 이유만으로 설치 검증 완료 표기.

## 질문할 때 남길 정보

실습 번호, 실행한 명령, Python/패키지 버전, 에러 종류와 HTTP status, 발생 시각,
관련 request/response/run ID를 담당자에게 전달합니다.
`.env` 전체, 토큰, 비밀번호, 실제 고객 질문/응답, 원문 trace를 공개 issue에 붙이지 않습니다.

CLI의 주요 종료 코드: `0` 실행 성공, `1` 업무 게이트 불합격/수집 오류,
`2` 설정·입력·의존성·실행 조건 오류.
`demo`는 고정 예제 생성 명령이므로 v1의 낮은 점수 자체는 생성 실패가 아닙니다.
별도 `evaluate`가 점수에 따라 종료 코드를 반환합니다.
