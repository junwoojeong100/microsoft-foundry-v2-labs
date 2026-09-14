# 공통 설정 계약

[English](../../reference/configuration.md) | **한국어**

**한 저장소 안에서는 하나의 환경변수 이름을 씁니다. 원본 리포의 서로 다른 이름을 혼합하지 않습니다.**

모든 CLI는 루트 `.env`를 읽습니다. 이미 프로세스에 있는 값이 우선합니다.
따라서 오래된 터미널에서 예상하지 않은 값을 상속하지 않았는지 확인합니다.

| 이름 | 쓰는 곳 | 비고 |
|---|---|---|
| `AZURE_SUBSCRIPTION_ID` | 로컬 CLI 인증과 ARM 조회 | UUID, 이 구독의 계정 프로필을 선택하며 기본 구독은 변경하지 않음 |
| `AZURE_TENANT_ID` | 로컬 인증 전 검증 | 선택한 구독의 실제 tenant와 대조 |
| `AZURE_RESOURCE_GROUP` | 배포 확인 | 실제 실습 그룹 |
| `AZURE_AI_ACCOUNT_NAME` | 배포 확인 | 실제 Foundry account |
| `AZURE_AI_PROJECT_ENDPOINT` | 모델·agent·평가 SDK | 전체 `/api/projects/...` endpoint |
| `AZURE_AI_MODEL_DEPLOYMENT_NAME` | target 모델 | 배포 이름, 자동 대체 없음 |
| `WORKSHOP_AUTH_MODE` | 인증 | `cli` 또는 `managed-identity` |
| `AZURE_CLIENT_ID` | 선택 user-assigned managed identity | 실제 런타임에 필요할 때만 |
| `WORKSHOP_PREFIX` | 생성할 agent/Search 이름 | 고유한 `mfv2-...`, 최대 32자 |
| `WORKSHOP_MAX_OUTPUT_TOKENS` | 모델 출력 상한 | 기본 2048, 허용 256–8192 |
| `AZURE_SEARCH_ENDPOINT` | Search/IQ | 서비스 루트 |
| `AZURE_SEARCH_INDEX_NAME` | 일반 검색/IQ 원문 | 기본 `<prefix>-policies` |
| `AZURE_SEARCH_KNOWLEDGE_SOURCE_NAME` | IQ | 기본 `<prefix>-source` |
| `AZURE_SEARCH_KNOWLEDGE_BASE_NAME` | IQ | 기본 `<prefix>-kb` |
| `AZURE_AI_EVALUATION_MODEL_DEPLOYMENT_NAME` | cloud judge | target와 구분해 명시 |

`AZURE_OPENAI_ENDPOINT`, `WORKSHOP_IQ_PLANNER_DEPLOYMENT`, `WORKSHOP_IQ_PLANNER_MODEL`은
richer Preview를 별도 실험할 때의 선택 설정입니다. 기본 GA IQ 코드에서 사용하지 않습니다.

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

## 데이터·출력 계약

합성 정책: `id`, `title`, `content`, `effective_from`, `effective_to`.
답변: `answer`, `decision`, `limit_krw`, `citations`.
`limit_krw`는 실제 지출액이 아니라 질문에 맞는 **한도**이며, 근거가 없으면 `null`입니다.

`decision`은 `answer`, `needs_approval`, `insufficient_evidence` 중 하나입니다.
정답 금액을 code가 몰래 보정하지 않으며 잘못된 JSON/중복 키/잘못된 타입을 거부합니다.

실행은 `outputs/<label>/`에 저장합니다. label은 경로가 아니라 제한된 이름입니다.
기존 실행 디렉터리는 덮어쓰지 않습니다.
`manifest.json`의 hash는 재현을 돕는 장치이며 전자서명이나 변조 방지 저장소는 아닙니다.
