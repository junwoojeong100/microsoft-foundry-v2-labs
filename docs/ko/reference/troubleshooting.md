# 문제 해결: 다음 명령보다 원인을 먼저

[English](../../reference/troubleshooting.md) | **한국어**

**오류가 난 단계를 해결하기 전에는 배포·평가·삭제를 연속 실행하지 않습니다.**
같은 에러에 새 모델/새 구독/새 리소스를 무작정 만드는 것은 복구가 아닙니다.

<a id="resume-safely"></a>

## 유료 작업을 반복하지 않고 재개하기

기록에서 마지막 완료 단계와 정확한 버전·label을 읽고 **처음 해당하는 행**을 따릅니다.

| 상황 | 안전한 다음 행동 | 하지 않을 일 |
|---|---|---|
| 브라우저를 닫았음 | 같은 프로젝트·agent·저장 버전을 열고 기존 대화 확인 | 새 agent 생성·모든 질문 재전송 |
| 선택 File Search 분기를 마침 | A의 기본 질문 4개 전에 [기록한 인라인 agent·버전으로 복귀](../labs/03-prompt-agent.md#check-inline-agent). File Search 결과는 별도 보존 | `-files` agent나 그 응답을 인라인 baseline으로 사용 |
| Lab 07 A의 **저장** 버튼이 활성화됨 | 보관할 초안은 따로 복사한 뒤 [기록된 baseline 버전 복구](../labs/07-evaluation.md#assessment-version). 미저장 수정이 없는 상태에서 질문 | 초안을 baseline으로 저장·원래 지침 파일 덮어쓰기·한 평가표에 여러 버전 혼합 |
| 답변을 붙여 넣자 여러 셀이 바뀜 | 마지막 붙여넣기를 실행 취소하고 [셀 편집 상태에서 받은 답변을 다시 붙여넣기](../labs/07-evaluation.md#assessment-sheet). 원래 ID·질문 6개 유지 | 질문 재전송·작성한 baseline을 빈 양식으로 교체·영향받은 문항 삭제 |
| 새 터미널을 열었음 | 저장소 루트로 돌아와 `source .venv/bin/activate`. 기존 Azure 로그인 유지 | 전체 재설치·`.env` 덮어쓰기·셸 `source .env`·단순 재개를 위한 `az login` 반복 |
| Lab 03 B에서 agent를 만든 뒤 중단함 | [저장된 agent별 재개 표](../labs/03-prompt-agent.md#resume-managed-agent)에 따라 생성 JSON의 `agent_name`·`agent_version`을 모두 복구 | 셸 변수 복구를 위한 `create` 재실행·이전 이름 사용·`latest` 호출 |
| `${NAME:?...}`가 값 누락을 알림 | 이번 회차의 설정/출력 기록에서 해당 값을 복구. 아직 명령은 실행되지 않음 | 보호 문법 제거·녹화 ID 복사·다른 터미널 값의 자동 전달 가정 |
| 모델 비교 명령이 종료되거나 실패함 | [명령 범위의 모델 지정](../labs/extensions/model-operations.md)은 원래 설정을 유지하므로 저장된 비교/오류 확인 | 계속하려고 `.env` 변경·첫 모델 복원을 위한 유료 작업 반복 |
| B 기록 폴더가 이미 있음 | 같은 회차의 파일로 재개하거나 새 회차용 새 폴더 선택. 보호된 복사 블록이 멈추는 것은 의도된 동작 | 작성한 기록을 빈 양식으로 덮어쓰기 |
| `--output` 파일이 이미 있다고 나옴 | 저장된 JSON 확인. 새 요청은 보내지 않았음. 의도적인 새 요청에만 다른 파일명 사용 | 근거 삭제·다시 저장하려고 유료 호출 반복 |
| 응답은 출력됐지만 저장이 실패함 | stdout 전체를 새 파일에 직접 보관하고 파일 오류도 유지 | 이미 받은 답변을 복구하려고 모델 재호출 |
| Label이 이미 있음 | 모듈이 출력한 폴더 확인. [저장 위치 표](commands.md#saved-results)에서 입문·matrix·Toolbox·대화 구분 | 결과 삭제·같은 label로 `collect` |
| Lab 00의 v1 fixture가 `passed: 0`, `errors: 0` 보고 | [의도된 인용 검사 실패](../labs/00-start.md#offline-fixtures). 결과를 보존하고 명령 자체가 성공했다면 v2로 진행 | 환경 재설치·통과시키려고 fixture 수정·실제 모델 점수로 해석 |
| `collect`가 0이 아닌 종료 코드 반환 | 모든 행·오류 보존, `evaluate`로 확인, 원인 해결 후 명시적인 새 dev label로 수집 | 실패 행을 fixture로 대체·모델/provider 자동 변경 |
| `evaluate`가 `1` 반환 | `total`, `passed`, `errors`, 사례별 `checks` 확인. Baseline 실패는 검토하되 실패한 candidate는 holdout을 열지 않음 | 요청 완료를 업무 게이트 통과로 해석 |
| Candidate·holdout이 이미 있음 | `outputs/<holdout-label>/acceptance.json`을 읽거나 정확한 기존 label로 로컬 `accept` 재실행 | 같은 노출 holdout을 재수집해 좋은 점수 만들기 |
| Hosted 패키지가 이미 있음 | Manifest 확인. 재빌드 시 그 정확한 생성 폴더를 다른 이름으로 보관 | 소스·`.build` 전체·`outputs`·azd 상태 삭제 |
| Search의 scope/corpus 불일치 | 기존 ledger 보존. 언어·prefix·서비스 변경은 [새 복사본 규칙](configuration.md#workspace-scope) 적용 | 다음 label만 변경·ledger 삭제/편집 |
| 입문 Hosted 준비에서 폴더/profile 거절 | 기존 azd 프로젝트 밖의 새 빈 폴더와 정확한 local/v2/Responses 패키지/언어 선택 | `azd ai agent init` 반복·`--force`·패키지 검사 완화 |
| 필수 평가가 계속 막힘 | 기존 기록과 [미완료 인계](../labs/11-capstone.md#incomplete-handoff) 사용 | 없는 실행의 인수 보고서 생성·막힌 작업을 완료로 표시 |
| Cloud judge가 timeout | 저장한 job ID와 **같은** `cloud-evaluate --label` 명령으로 조회 재개 | 이미 제출한 judge job에 새 수집 label 규칙 적용 |
| 로컬 matrix smoke가 `--azd-directory`를 요구 | 워크북에서 준비한 독립 폴더 지정. 소스 프로젝트를 자동 선택하는 기본값은 없음 | 다른 agent의 `azure.yaml`을 소스 루트에 복사 |
| Toolbox 원격 결과 폴더가 이미 있음 | 원래 stream·검증/실패 보존. 실제 새 요청일 때만 모든 경로의 폴더명을 함께 변경 | 이전 raw stream 덮어쓰기·로컬 검증기 재실행을 위한 모델 재호출 |

기본 Lab 07은 새 수집 전에 [저장된 결과별 재개 표](../labs/07-evaluation.md#resume-evaluation)를 확인합니다.
새 dev 실험에는 새로운 **baseline/candidate/final-holdout** 이름 묶음을 정해 Lab 07·11에서 일관되게 사용합니다.
새 후보가 통과하고 고정되기 전에는 holdout을 열지 않습니다. 읽기 전용 재조회는 새 추론 증거가 아닙니다.
새 label을 붙여도 이미 노출된 holdout이 다시 미사용 검증셋이 되지는 않습니다.

## 자주 막히는 지점

| 증상 | 첫 확인 | 바로 복귀 |
|---|---|---|
| `scripts/workshop.py`를 찾지 못함 | 현재 폴더에 `README.md`, `pyproject.toml`, `scripts/`가 있어야 함. 학습자 ZIP과 소스 ZIP은 다름 | [00 B](../labs/00-start.md#path-b) |
| PowerShell/Command Prompt에서 Bash 명령 오류 또는 `>>>` 표시 | Windows는 WSL 터미널 사용. Python 안이면 `exit()`로 나온 뒤 터미널 명령 붙여넣기 | [터미널 확인](../labs/00-start.md#terminal-check) |
| Python·패키지 없음 | 지원 Python·활성 `.venv`·고정 설치 단계 확인. 설치 오류를 무시하지 않음 | [00 B](../labs/00-start.md#path-b) |
| `--output` 폴더가 없거나 `outputs/` 밖임 | Lab 00 기록 폴더를 준비하고 이 소스 복사본 안의 새 `.json` 경로 사용 | [JSON 저장](commands.md#saving-json) |
| UUID 또는 출력 token 정수 오류 | 준비 카드로 명시된 설정만 수정. Token은 256–8192이며 프로세스에서 상속한 값도 확인 | [설정](configuration.md) |
| 기본 B에서 `check_sdk.py`가 hosting 패키지 누락을 보고 | 선택 Hosted/Toolbox까지 검사하는 명령임. 기본 B에는 불필요하며 확장 선택 시 선언한 extra 준비 | [모듈 SDK 준비](../labs/extensions/developer-toolkit.md#hosted-sdk) |
| Prefix 거절 | `mfv2-` 필수. 소문자 영문·숫자·하이픈 하나씩, 끝 하이픈 금지, 전체 최대 32자 | [설정](configuration.md#workspace-scope) |
| 401/403·프로젝트 없음 | 의도한 tenant·호출 주체를 확인하고 만료된 인증만 갱신. 403은 반복 로그인 대신 담당자가 리소스 범위 권한 확인 | [로그인 경계](../labs/00-start.md#azure-sign-in) / [준비](../setup.md) |
| 브라우저 로그인은 성공했지만 실습 프로젝트를 쓸 수 없음 | 역할을 추가로 요청하기 전에 계정과 디렉터리를 모두 준비 카드와 대조 | [포털 tenant 확인](#portal-tenant) |
| 혼자 학습하는데 단계가 담당자에게 요청하라고 함 | 본인이 담당자입니다. 해당 프로젝트·모델·역할·추적 단계를 직접 해결하고 다른 모델로 바꾸지 않음 | [혼자 학습 준비](../setup-owner.md#self-study) |
| `MAF request failed` / `Failed to invoke the Azure CLI` | SDK 원인 보존. CLI token 프로세스 timeout은 업무 검사 실패가 아님 | [MAF 요청 복구](#maf-request-failure) |
| 모델 404 / 429 | 전체 project endpoint·배포 이름 / quota·동시성. 모델 대체 금지 | [02 B](../labs/02-models.md#path-b) |
| 새 모델 출시 직후 `model`·`answer`·MAF·agent에서 HTTP 500 | 프로젝트 agent 경로가 아직 그 모델을 지원하지 않을 수 있음(2026-09-23 `gpt-6-luna`). 멈추고 기록. 모델·endpoint 변경 금지 | [모델 선택](model-choice.md) |
| IQ에 Chat 모델이 없다고 나옴 | 기본 B는 모델 없는 GA 검색. 선택 A IQ Chat은 별도로 준비한 base 필요 | [06](../labs/06-knowledge.md) |
| Hosted 명령이 다른 로컬 프로젝트를 선택 | 기록한 절대 경로 `HOSTED_DIRECTORY`를 복구하고 모든 azd 명령에 `--cwd` 사용 | [08](../labs/08-hosted.md) |
| Traces에 trace가 보이지 않음 | 원래 요청 날짜·agent·버전을 필터에 포함하고 Response ID 또는 Trace ID로 검색. 요청 전에 Application Insights가 연결됐는지 확인. 로컬 MAF에는 server-side agent trace가 없음 | [09](../labs/09-operations.md#path-b) |
| Traces 권한 오류 | 학습자에게 연결된 Application Insights 리소스의 Log Analytics Reader가 필요. 보호된 테이블이 있으면 Privileged Monitoring Data Reader도 필요 | [09](../labs/09-operations.md) |

<details>
<summary>전체 오류 참조 — 위 짧은 표에 없는 오류일 때 펼칩니다</summary>

| 증상 | 먼저 확인 | 복귀 |
|---|---|---|
| 프로젝트가 안 보임 | tenant, 계정, project 역할; 잘못된 운영 프로젝트 선택 금지 | 00–01 |
| `python3.13` 없음 | 지원 Python 설치 또는 강사가 준비한 환경 | 00 |
| `ModuleNotFoundError` | venv 활성화, 해당 extra 설치, `python -m pip check` | 00 |
| 패키지 다운로드 TLS/연결 오류 | 네트워크 정책·공식 PyPI 접근, 준비 환경 사용 | 00 |
| `.env`를 바꿔도 값이 다름 | 프로세스 환경변수가 우선인지 확인, 새 터미널 | 00 |
| 401 | 로그인·tenant·credential 종류 확인. 만료된 로컬 인증만 공유 프로필 경계를 지켜 갱신 | [00](../labs/00-start.md#azure-sign-in) |
| `AADSTS90072` / 다른 기본 계정 선택 | `.env`의 구독과 계정 프로필 확인; 구독 범위 인증 사용. 기본 구독 변경·guest 초대·전체 logout으로 우회하지 않음 | 00 |
| 403 | 관리 평면과 데이터 평면 역할, 올바른 identity/scope, 반영 지연 | 01 |
| 404 모델 | 카탈로그 이름 대신 실제 배포 이름, 정확한 프로젝트 endpoint | 02 |
| 429 | quota·TPM·동시성·다른 조의 사용량, 서비스 retry 안내 | 02 |
| `json_schema`/옵션 400 | 모델별 Structured Outputs 지원, 현재 SDK 계약 | 02 |
| 응답 `incomplete` | 출력 token 한도, content filter, 모델 지원; 임의 보정 금지 | 02 |
| `FileExistsError` label | 기존 실행을 확인하고 재개. 실제 새 실험에만 새 label 사용 | 07 |
| 원본 hash 불일치 | 원본 파일·오류 보존 후 입력/응답 변경 조사. 새 dev 실험으로만 재수집하며 노출 holdout을 재시도하지 않음 | 07 |
| MCP 실패 | 같은 venv의 `mcp`, 서버 path, stdout에 비-JSON 로그 여부 | 04 |
| workflow timeout | 최대 라운드·출력 한도·도구 지연·quota | 05 |
| Search 401/403 | 담당자가 [API access control의 Entra 토큰 허용](../setup-owner.md#search-authentication)과 호출자의 Search 역할을 순서대로 확인. 역할만으로 토큰 인증이 활성화되지는 않음 | 06 |
| Search 부분 upload 실패 | 개별 `status`, 문서 수·키, index 필드 | 06 |
| 기존 Search 객체 거부 | 내 접두사/소유권 ledger인지 확인; 공유 객체 덮어쓰기 금지 | 06 |
| 하이브리드 index 차원 또는 기존 index 충돌 | 실제 embedding 차원, 별도 본인 index, namespace/ledger 확인. 벡터 자르기·0 채우기 금지 | 06 |
| IQ 400 | GA intents와 Preview messages를 혼합했는지, 실제 API 버전 | 06 |
| `Chat completions model is required` | 모델 미선택이지 MI 실패가 아님. **`gpt-5.6-luna` + Search SMI**로 준비된 chat base를 열고 모델 없는 GA base에 포털 기본값을 저장하지 않음 | 06 |
| `Unsupported model type in Knowledge Base Model Configuration` | Search가 그 모델을 KB에 허용하지 않음. IQ Chat은 GPT-6 모델이 아닌 별도 `gpt-5.6-luna` 배포 사용 | 06 |
| `iq-chat check`의 모델/버전/역할 실패 | [고정 preset](iq-model-identity.md)의 `gpt-5.6-luna` / `2026-07-09`·Search SMI·계정 범위 역할 확인. 담당자가 준비를 해결하며 대체 모델을 고르지 않음 | 06 |
| `ready_for_setup: true`, `configured: false` | 선행 조건은 통과했지만 별도 chat base는 아직 없음. Source를 소유한 작업 폴더에서 담당자가 승인된 setup 진행 | 06 |
| IQ Chat label이 이미 있음 | 이전 요청·응답·실패부터 읽고 명시적으로 승인한 새 유료 시도에만 새 label 사용 | 06 |
| IQ 모델 호출 401/403 | Search→모델 identity·계정 scope·RBAC 전파·네트워크 확인. Hosted/사용자 역할이 Search에 상속되지 않음 | 06 |
| Preview가 `maxOutputSizeInTokens` 거절 | 파라미터 검증 오류를 보존하고 확인한 버전별 `maxOutputSize` 요청 사용. 인증 실패로 분류하지 않음 | 06 |
| IQ references/activity 오류 | sourceData/docKey, source 설정, semantic·사용/과금 동의 | 06 |
| cloud judge timeout | 같은 label로 재조회; 저장된 eval/run ID 재사용. 새 job을 자동으로 만들지 않음 | 07 |
| evaluator 초기화 schema 오류 | 실제 catalog의 `model`/`deployment_name` 및 버전 확인 | 07 |
| holdout이 거부됨 | 후보 dev 통과·고정, 같은 code/prompt/model/provider, 명시적 unlock | 07 |
| 로컬은 성공, Hosted는 403 | 런타임 identity의 역할; 로컬 `az login` 반복 금지 | 08 |
| 로그/trace가 없음 | App Insights app ID·exporter·agent·시간 범위·sampling·보존/보호 테이블 권한. trace 0건은 정상 운영이 아니라 미확인 | 09 |
| Traces에 trace가 보이지 않음 | 요청 날짜 범위·agent/버전 필터, 요청 전에 연결된 Application Insights, Response ID/Trace ID 검색. 로컬 MAF에는 server-side agent trace가 없음 | 09 |
| Traces 권한 오류 | 연결된 Application Insights의 Log Analytics Reader. 보호된 테이블이 켜져 있으면 Privileged Monitoring Data Reader도 필요 | 09 |
| 영문 질문에 국문 자료가 사용됨 | `--language en`과 영문 전용 index/source/base 선택. 오류 뒤 국문 자료로 대체하지 않음 | 00–07 |
| 영문 파일 누락 | 고정된 영문 번들을 복원하고 기존 국문 파일은 보존 | 00 |
| `--agent-endpoint`와 `--protocol` 충돌 | full endpoint에 protocol이 이미 포함됨. 로컬 호출은 protocol을 명시 | 08 |
| batch의 API version 누락 | session query parameter를 대체하지 않고 merge해 `api-version=v1`을 보존 | 07–08 |
| 프로젝트 embedding 404 | `WORKSHOP_EMBEDDING_API=account`와 같은 계정 endpoint를 명시. 원래 실패를 보존 | 06 |
| trace 조회 `InvalidTokenError` | App Insights audience와 지정된 구독/tenant credential. identity·리소스 대체 금지 | 09 |
| idle 세션 중지가 409 반환 | 기록된 session/version을 다시 조회하고 추가 stop 요청 없이 idle 상태를 기록 | 09 |
| Host profile/contract 불일치 또는 `runtime-profile.json` 없음 | 현재 코드로 다시 패키징한 뒤 profile 언어·model map·source package·실제 version·retrieval 설정 비교. 새 label로 수집하며 manifest를 고쳐 통과시키지 않음 | 08 |
| model key가 allowlist에 없음 | `.env`와 원격 서비스 환경의 `WORKSHOP_MODEL_DEPLOYMENTS_JSON`이 같은 map이고 기본 배포를 포함하는지 확인 | 08 |
| `account-chat` endpoint 불일치 | `AZURE_OPENAI_ENDPOINT`에 같은 Foundry 계정의 실제 OpenAI root 사용. 실패 후 CLI가 URL을 바꾸지 않음 | 06–08 |
| azd raw 출력 파싱 실패 | HTTP 상태·UTF-8 바이트 길이·알려진 notice만 허용. 오류 텍스트에서 JSON을 추출하지 않음 | 08 |
| CLI 확장이 Incompatible로 표시 | [버전 게이트](versions.md)를 검토하고 호환 조합을 따로 승인·설치한 뒤 다시 확인 | 08 |
| native 품질 점수가 낮음 | 완료된 실행을 보존하고 평가자를 업무 요구와 비교해 검토. 좋은 점수가 나올 때까지 재시도하지 않음 | 07 |
| native 실행 failed/invalid | 같은 명령에 `--retry-failed`를 붙여 한 번 재실행. 원래 시도는 보존. 완료된 낮은 점수는 재시도할 수 없음 | 07 |
| 회귀 파일이 질문·정답을 바꿈 | 기존 dev 계약을 유지하거나 별도 dataset version 설계. holdout을 회귀로 사용하지 않음 | 07 |
| matrix 행 누락·중복 | 성공한 일부만 평가하지 않음. 원인을 해결한 뒤 새 label로 전체 matrix 수집 | 07 |
| `Missing evaluator results … missing ['business_rubric']` | 서비스가 평가자 하나를 빠뜨려 시도가 invalid로 저장됨. 같은 `cloud-evaluate` 명령에 `--retry-failed`를 붙여 한 번 재실행. 시도는 `native-attempts/`에 보존. `--reference`로 추가한 실행은 재시도해도 그 평가에 `<label>-retry-1`로 남음 | 07 |

</details>

<a id="portal-tenant"></a>

## 브라우저 로그인만으로 tenant·권한이 확인되지는 않습니다

포털의 디렉터리를 준비 카드의 tenant ID와 비교합니다. URL에 `tid=`가 있다면 그 tenant를 가리켜야 합니다.
다른 회사 계정으로 로그인됐다는 이유만으로 계속하지 말고, 해당 디렉터리의 담당자 제공 프로젝트 링크와
**지정된 실습 계정**을 사용합니다. Agent가 **Loading...** 상태여도 페이지 머리글에는 프로젝트 이름이 보일 수 있습니다.
실제 agent 이름·버전·지침이 로드된 뒤에 페이지 확인을 완료로 기록합니다.

브라우저와 Azure CLI는 서로 다른 계정·tenant의 세션일 수 있습니다. SDK 성공이 브라우저의 같은 접근 권한을 증명하지 않으며,
브라우저 403이 올바른 scope의 CLI 호출 주체에도 역할이 없다는 뜻은 아닙니다.
계정·디렉터리가 다르면 로그인 대상을 먼저 바로잡습니다. 역할 추가·guest 초대·Azure CLI 기본 구독 변경으로 우회하지 않습니다.
올바른 계정에도 접근 권한이 없을 때 담당자가 해당 범위를 해결합니다.

<a id="maf-request-failure"></a>

## 답변 실패가 아닌 MAF 요청 실패에서 복구하기

`maf`·`workflow`·`workflow-agent`·`maf-evaluate`·`serve`는 처리한 Agent Framework 실패를
`FAIL: ValueError: MAF request failed: ...`와 종료 코드 `2`로 보고합니다. 원인과 복구 문서 경로도 유지합니다.
성공 응답 파일을 만들지 않으며, 실패를 보고한 뒤 CLI가 자동으로 재시도하거나 모델/provider를 바꾸지 않습니다.
`--debug`는 예외 연결 전체를 보존합니다. Debug 로그에는 로컬 경로가 들어갈 수 있으므로 비공개로 보관합니다.

`az account get-access-token`의 `TimeoutExpired` / `Failed to invoke the Azure CLI`라면 원래 stderr와 시각을 보존합니다.
새 유료 workflow 시도를 결정하기 전에 활성 환경과 **같은** 구독·tenant를 Lab 00의 읽기 전용 `doctor --cloud`로 확인합니다.
Access token을 출력하거나 공유하지 않습니다. 실제 인증이 만료됐을 때만
[공유 프로필 경계](../labs/00-start.md#azure-sign-in)를 지켜 다시 로그인합니다.
로컬 CLI 프로세스가 느리다는 이유만으로 재로그인하거나 역할을 부여하지 않습니다.

이후 성공한 시도는 새 실행이지 실패 기록의 대체가 아닙니다. 성공한 `--output` 파일이 이미 있다면 재실행 대신 읽습니다.
완료된 낮은 점수를 높이려고 재시도하지 않습니다.

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

CLI가 처리한 종료 코드: `0` 실행 성공, `1` 업무 게이트 불합격/수집 오류,
`2` 설정·입력·의존성·실행 조건 오류 또는 개별 Azure/MAF 요청 실패.
`demo`는 고정 예제 생성 명령이므로 v1의 낮은 점수 자체는 생성 실패가 아닙니다.
별도 `evaluate`가 점수에 따라 종료 코드를 반환합니다.
