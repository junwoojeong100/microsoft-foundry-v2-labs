# 공통 설정 계약

[English](../../reference/configuration.md) | **한국어**

**한 저장소 안에서는 하나의 환경변수 이름을 씁니다. 원본 리포의 서로 다른 이름을 혼합하지 않습니다.**

클라우드 설정이 필요한 명령은 루트 `.env`를 읽으며 이미 프로세스에 있는 값이 우선합니다.
오프라인 `doctor`·`demo`·로컬 `retrieve`, 저장된 실행의 `evaluate`·`compare`·`accept`·`feedback`·`cleanup-plan`은 이 파일을 읽지 않습니다.
오프라인 PASS가 입력한 환경값의 검증 성공을 뜻하지는 않습니다.
영어 실행은 `--language en`을 명시하며 기존 기본값은 한국어입니다.
언어별 지침·corpus·dataset을 선택하고 Hosted profile에 고정합니다.
따라서 오래된 터미널에서 예상하지 않은 값을 상속하지 않았는지 확인합니다.

## 현재 실습에 필요한 값만 입력하기

녹화나 오래된 `azure.yaml`이 아니라 [`.env.example`](../../../.env.example)의 번호 구간을 사용합니다.

| 현재 단계 | 입력·유지할 값 |
|---|---|
| 오프라인 체험 | 없음. 해당 명령은 `.env`를 읽지 않음 |
| 첫 실제 모델·MAF·로컬 검색 평가 | 1번 구간에 검증된 준비 카드 값 입력. `WORKSHOP_AUTH_MODE=cli`, 출력 한도 2048 유지 |
| 기본 B의 Lab 06 Search/IQ | 2번 구간의 `AZURE_SEARCH_ENDPOINT` 추가. 객체 이름 기본값은 본인 prefix 사용 |
| 선택 IQ Chat·hybrid·Toolbox·Hosted·cloud judge | 선택한 모듈이 명시한 추가 값만 입력 |

잘못된 UUID·출력 한도는 단순 파서 오류 대신 **설정 이름**을 알려 줍니다.
그 값만 고치며 관계없는 배포나 identity를 바꾸지 않습니다.
소스 루트의 `azure.yaml`, `.azure/`, `.env`는 Git에서 제외되는 개인 상태이며 배포되는 실습 기본값이 아닙니다.
Hosted 도우미가 검증된 값으로 별도 프로젝트를 생성하며, 로컬 matrix smoke에는 `--azd-directory`가 필수입니다.

## 설정 찾아보기

| 이름 | 쓰는 곳 | 비고 |
|---|---|---|
| `AZURE_SUBSCRIPTION_ID` | 로컬 CLI 인증과 ARM 조회 | UUID, 이 구독의 계정 프로필을 선택하며 기본 구독은 변경하지 않음 |
| `AZURE_TENANT_ID` | 로컬 인증 전 검증 | 선택한 구독의 실제 tenant와 대조 |
| `AZURE_RESOURCE_GROUP` | 배포 확인 | 실제 실습 그룹 |
| `AZURE_AI_ACCOUNT_NAME` | 배포 확인 | 실제 Foundry account |
| `AZURE_AI_PROJECT_ENDPOINT` | 모델·agent·평가 SDK | 전체 `/api/projects/...` endpoint |
| `AZURE_AI_MODEL_DEPLOYMENT_NAME` | target 모델 | 템플릿 기본 `gpt-5.6-luna`; 실제 배포를 먼저 준비. 자동 대체 없음 |
| `WORKSHOP_AUTH_MODE` | 인증 | `cli` 또는 `managed-identity` |
| `AZURE_CLIENT_ID` | 선택 user-assigned managed identity | 실제 런타임에 필요할 때만 |
| `WORKSHOP_PREFIX` | 생성할 agent/Search 이름 | `mfv2-`로 시작. 소문자 영문·숫자를 하이픈 하나로 구분하며 끝 하이픈 금지. 전체 최대 32자 |
| `WORKSHOP_MAX_OUTPUT_TOKENS` | 모델 출력 상한 | 기본 2048, 허용 256–8192 |
| `AZURE_SEARCH_ENDPOINT` | Search/IQ | 서비스 루트 |
| `AZURE_SEARCH_RESOURCE_GROUP` | `iq-chat check` ARM 조회 | 선택값. Search가 같은 그룹에 있으면 `AZURE_RESOURCE_GROUP` 사용 |
| `AZURE_SEARCH_INDEX_NAME` | 일반 검색/IQ 원문 | 기본 `<prefix>-policies` |
| `AZURE_SEARCH_KNOWLEDGE_SOURCE_NAME` | IQ | 기본 `<prefix>-source` |
| `AZURE_SEARCH_KNOWLEDGE_BASE_NAME` | IQ | 기본 `<prefix>-kb` |
| `AZURE_SEARCH_CHAT_KNOWLEDGE_BASE_NAME` | 선택 IQ Chat preset | 별도 소유 base. 국문 기본 `<prefix>-chat-ko-kb`, 영문 `<prefix>-chat-en-kb` |
| `TOOLBOX_SEARCH_CONNECTION_NAME` | 선택 관리형 Toolbox | 담당자가 같은 프로젝트에 준비한 keyless CognitiveSearch 연결 |
| `TOOLBOX_NAME` | 선택 관리형 Toolbox | 기본 `<prefix>-tools-<language>`. 기존의 소유하지 않은 이름은 거절 |
| `AZURE_AI_EVALUATION_MODEL_DEPLOYMENT_NAME` | cloud judge | target와 구분해 명시 |

IQ Chat 모델과 Search의 호출 identity는 **knowledge base의 모델 연결**에서 설정합니다.
Seed/retrieve 명령은 planner 환경변수 placeholder를 읽거나 그 모델 연결을 자동 설정하지 않습니다.
`WORKSHOP_AUTH_MODE`/`AZURE_CLIENT_ID`는 Python 호출자를 선택하며 Search identity 설정이 아닙니다.
[Keyless IQ 모델 설정](iq-model-identity.md)을 확인하세요.

**2026-09-15 IQ Chat preset:** 배포/모델 `gpt-5.6-luna`, 실제 버전 `2026-07-09`,
Search **system-assigned** identity, `2026-08-01-preview`, `low`, `answerSynthesis`입니다.
응답 모델 환경변수를 바꿔도 이 preset은 바뀌지 않습니다.
`AZURE_OPENAI_ENDPOINT`에는 프로젝트와 같은 Foundry 계정의 OpenAI root가 필요합니다.
`iq-chat check`가 실제 배포·source·명시된 역할을 검사하고 `setup`은 source/corpus가 맞는 로컬 소유권 기록을 요구합니다.
기본 GA base는 변경하지 않으며 새 chat-base 이름은 본인 prefix로 시작해야 합니다.
[준비 명령](../setup.md#4-환경-담당자의-준비)을 따릅니다.

<a id="workspace-scope"></a>

## Search 소유 복사본 하나, prefix 하나, 언어 하나

`--language en`은 영문 데이터를 선택할 뿐 **Search 객체 이름이나 `.env`를 바꾸지 않습니다**.
Search 이름을 비우면 두 언어 모두 `<prefix>-policies`, `<prefix>-source`, `<prefix>-kb`를 사용합니다.
두 언어를 준비한다면 `mfv2-team01-en-0917`, `mfv2-team01-ko-0917`처럼 별도 prefix를 정합니다.

| 변경 상황 | 안전한 준비 |
|---|---|
| 같은 언어·범위에서 모델/dev 실행 반복 | 새 실행 label을 쓰고 Search 소유권 기록은 유지 |
| 소유한 Search 객체 없이 로컬 검색·모델 평가의 언어 변경 | 새 label 묶음과 해당 언어 번들 사용. 번역 데이터는 같은 입력의 비교가 아님 |
| Seed 후 언어·Search 서비스·prefix 변경 | 검토한 `.env`·새 소유 이름·새 label을 가진 새 소스 복사본 사용. 기존 복사본과 정리 ledger 보존 |
| 강사가 준비한 객체 사용 | 언어·범위·ledger가 맞는 승인된 준비 작업 폴더 사용 또는 명시적으로 선택한 읽기 전용 실습만 진행 |
| 원격 객체는 있지만 이 복사본에 대응 ledger가 없음 | 덮어 seed하거나 다른 조의 ledger를 복사·조작하지 않음. 담당자가 해결하거나 새 복사본/prefix 준비 |

`outputs/azure-objects.json`은 Search endpoint·prefix·corpus hash에 묶입니다.
Label만 또는 `WORKSHOP_PREFIX`만 바꾸어 초기화할 수 없습니다. 거절을 우회하려고 ledger를 삭제·편집하지 않습니다.
새 복사본을 시작하더라도 원래 담당자가 정리할 수 있도록 기존 결과를 유지합니다.

## 구버전 변수와의 대응

| 원본에서 사용한 이름 | 이 저장소에서 사용할 이름 |
|---|---|
| `PROJECT_ENDPOINT`, `FOUNDRY_PROJECT_ENDPOINT` | `AZURE_AI_PROJECT_ENDPOINT` |
| `MODEL_DEPLOYMENT_NAME`, `FOUNDRY_MODEL` | `AZURE_AI_MODEL_DEPLOYMENT_NAME` |
| `LAB_PREFIX` | `WORKSHOP_PREFIX` |
| `LAB_AUTH_MODE` | `WORKSHOP_AUTH_MODE` |

자동 alias/fallback은 없습니다. 오타가 있으면 다른 프로젝트로 연결하기보다
명시적으로 실패하는 편이 안전합니다.

여러 계정이 Azure CLI에 로그인되어 있어도 인증은 설정된 구독에 고정합니다.
`--tenant`만 지정하면 다른 기본 계정이 선택될 수 있고, Azure CLI는
`--tenant`와 `--subscription`을 동시에 받지 않으므로 구독의 tenant를 먼저 검증합니다.

## 한국어 통합 개정의 명시적 설정

| 이름 | 쓰는 곳 | 계약 |
|---|---|---|
| `WORKSHOP_MODEL_DEPLOYMENTS_JSON` | typed Hosted matrix | 1–8개 key→실제 배포 이름. key/배포 중복 금지, 기본 배포 포함 |
| `AZURE_OPENAI_ENDPOINT` | `--api account-chat` | 같은 Foundry account의 root. 오류 후 자동 사용하지 않음 |
| `WORKSHOP_HOSTED_AGENT_NAME` | benchmark | 실제 `mfv2-...` 이름 |
| `WORKSHOP_HOSTED_AGENT_VERSION` | benchmark 원격 | 실제 숫자 version, `latest` 금지 |
| `WORKSHOP_HOSTED_AGENT_ENDPOINT` | benchmark 원격 | `azd show`의 실제 Invocations endpoint; 프로젝트/name과 대조 |
| `AZURE_AI_EMBEDDING_DEPLOYMENT_NAME` | hybrid | 실제 기존 embedding 배포 |
| `WORKSHOP_EMBEDDING_DIMENSIONS` | hybrid | 실제 embedding의 차원. 자동 자르기/0 채우기 없음 |
| `WORKSHOP_EMBEDDING_API` | hybrid | `project` 또는 `account`를 명시. 현재 실제 실행은 같은 account API 사용, 자동 fallback 없음 |
| `WORKSHOP_IQ_RERANKER_THRESHOLD` | IQ 검색 | 선택적 0–4 필터, 빈 값은 서비스 기본값. 평가자의 통과 threshold가 아님 |
| `AZURE_APPLICATION_INSIGHTS_APP_ID` | trace 검증 | 연결한 Application Insights의 application ID UUID |

프로필의 `kind/pattern/retrieval/prompt/api/protocol/language`는 `runtime-profile.json`으로 패키지에 고정합니다.
기존 6필드 profile은 한국어로 읽으며 영어 profile은 `language: en`을 명시합니다.
계정·endpoint·배포 이름은 해당 환경 설정에서 읽되 runtime contract로 실제 응답과 대조합니다.
서버 요청은 `question/model_key/case_id/run_id`만 받으며 정답·임의 model/endpoint override를 거부합니다.

로컬 `.env`와 azd env를 혼합하지 않습니다.
원격 설정에서 client secret/API key로 managed identity 오류를 우회하지 않습니다.
기본 protocol은 Responses이며, 평가 matrix의 명령은 Invocations를 명시적으로 사용합니다.

## 데이터·출력 계약

합성 정책: `id`, `title`, `content`, `effective_from`, `effective_to`.
답변: `answer`, `decision`, `limit_krw`, `citations`.
`limit_krw`는 실제 지출액이 아니라 질문에 맞는 **한도**이며, 근거가 없으면 `null`입니다.

`decision`은 `answer`, `needs_approval`, `insufficient_evidence` 중 하나입니다.
정답 금액을 code가 몰래 보정하지 않으며 잘못된 JSON/중복 키/잘못된 타입을 거부합니다.

실행은 `outputs/<label>/`에 저장합니다. label은 경로가 아니라 제한된 이름입니다.
기존 실행 디렉터리는 덮어쓰지 않습니다.
`manifest.json`의 hash는 재현을 돕는 장치이며 전자서명이나 변조 방지 저장소는 아닙니다.
대화형 명령은 [`--output`으로 JSON 전체를 저장](commands.md#saving-json)할 수도 있습니다.
이 파일이 batch manifest나 Azure 소유권 기록을 대체하지는 않습니다.

한국어와 영어는 별도 dataset/prompt/corpus hash를 사용하며 ID·한도·적용일·정답 기준은 동등하게 유지합니다.
영어 파일 누락을 한국어로 대신하지 않습니다. [언어 번들](../../../data/README.ko.md)을 확인하세요.
