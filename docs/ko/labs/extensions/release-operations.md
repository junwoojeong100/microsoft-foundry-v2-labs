# 릴리스 운영: 제한된 모니터링과 명시적 배포 gate

[English](../../../labs/extensions/release-operations.md) | **한국어**

**C 선택.** 기존 CI의 로컬 로직·SDK·문서 검사는 배포된 agent의 품질 gate나 continuous evaluation과 다릅니다.
반복 유료 작업이나 배포 push에는 별도 승인이 필요합니다.

**첫 회차:** 두 경로 중 하나만 선택합니다.

| 경로 | 순서 | 준비·완료 |
|---|---|---|
| 제한된 모니터링 | 1–3절 | 본인 배포 대상·해당 평가/trace 접근·예산. 표본 결과와 disabled 규칙 기록 |
| CI 릴리스 | 4–6절 | 담당자가 준비한 GitHub OIDC·배포/런타임 권한. 실제 workflow 결과와 rollback/정리 판단 보관 |

**준비:** 선택 경로의 조건만 필요합니다. 모니터링에 GitHub ID가 필수인 것은 아닙니다.
**완료:** 해당 설정·실제 실행·품질 결정을 구분합니다.
**중단:** 기존 배포를 유지하고 누락된 권한/설정을 명시합니다. 성공처럼 보이는 대체 결과를 만들지 않습니다.

## 1. 자동화 전 근거

선택한 대상의 기존 근거를 재사용합니다. [Hosted 평가 워크북](../../reference/evaluation-workbook.md)은
전체 matrix를 얻는 방법 하나이지 이 페이지의 새 필수 실행이 아닙니다.
실제 버전, 모델 map,
원문/prompt/data hash, evaluator 버전, trace와 사람의 인수 상태를 보관합니다.
실패를 본 뒤 threshold를 재정의하거나 실패/누락 행을 빼거나 다른 대상 점수를 복사하지 않습니다.

## 2. 제한된 반복 평가 설정

Foundry **Build → Evaluations → Recurring Configs → Create**에서 내 전용 agent와 평가 수준만 선택합니다.

| 방식 | 목적 | 첫 실습 경계 |
|---|---|---|
| Scheduled | 지정 데이터/traffic을 예약 평가 | 짧은 승인된 시험 후 비활성화 |
| Continuous | 발생한 traffic을 표본 평가 | 지원되는 최소 sampling/run 제한, 무제한 요청 생성 금지 |

한 번에 한 방식만 사용합니다. source, evaluator, rule ID, agent filter, sampling,
최대 실행 수, 소유자와 disable 계획을 기록합니다. 지원된다면 시간당 한 실행을 상한으로 둡니다.
규칙 생성/활성화는 실제 평가 증거가 아닙니다.
계획한 합성 요청 한 번의 이력을 확인하고 차트를 채우려고 모델 요청을 반복하지 않습니다.

## 3. 실제 결과와 disabled 상태

Agent Monitor와 연결된 평가에서 시간 범위·버전·표본·완료/실패·개별 결과를 확인합니다.
telemetry가 없으면 **미검증**이지 오류 0/비용 0이 아닙니다.
시험 후 임시 규칙을 비활성화하고 읽어 재확인합니다.
규칙 제거가 모델·Search·로그 비용 전체 삭제를 뜻하지 않습니다.

**모니터링 완료:** 해당 기록을 [Lab 11](../11-capstone.md)에 추가합니다.
CI 경로를 별도로 선택하지 않았다면 OIDC ID를 만들지 않습니다.

## 4. 범위를 좁힌 GitHub OIDC

담당자와 별도 승인이 필요합니다.
의도한 저장소 및 branch/protected environment만 trust하도록 구성합니다.
client secret이나 구독 전체 Owner는 사용하지 않습니다.

이 workflow는 프로젝트 범위 **Foundry Project Manager**와 account metadata 읽기 권한을 사용합니다.
실제 배포된 runtime ID에 프로젝트 범위 **Foundry User**만 줄 수 있게 구성합니다.
helper가 반환된 agent/버전/principal을 확인하며 dispatch 입력의 임의 principal을 신뢰하지 않습니다.

tenant/subscription/client/project의 비밀 아닌 식별자는 환경 변수로 저장합니다.
토큰이나 `.env` 전체를 workflow log에 출력하지 않습니다.
[공식 Hosted CI/CD](https://learn.microsoft.com/azure/foundry/agents/quickstarts/set-up-cicd-hosted-agent)를
이 저장소의 패키지/profile과 정확한 smoke 계약에 맞춥니다.

**기억한 이름 전용 형식이 아니라 실제 subject를 사용합니다.** 저장소의 현재 OIDC 설정을 읽습니다.

```bash
printf '승인된 GitHub 저장소 (owner/name): '
read -r GITHUB_REPO
gh api "repos/$GITHUB_REPO/actions/oidc/customization/sub"
```

immutable subject의 `sub_claim_prefix`에는 소유자·저장소 ID가 포함됩니다.
형식은 `repo:<owner>@<owner-id>/<repository>@<repository-id>`이며
보호된 환경은 `:environment:foundry-workshop`을 덧붙입니다.
`azure/login`이 보고한 실제 subject·issuer·audience와 정확하게 맞추고 raw token은 출력하지 않습니다.
불일치를 해결하려고 immutable claim을 끄거나 wildcard trust·client secret·더 넓은 Azure 역할을 사용하지 않습니다.

9월 17일 CI의 초기 `AADSTS700213`은 기존 이름 전용 subject 때문이었습니다.
기존 federation의 subject만 실제 저장소 ID/환경 claim으로 수정했으며
identity·issuer·audience·Azure 역할·GitHub 보안 설정은 바꾸지 않았습니다.
[GitHub OIDC 계약](https://docs.github.com/en/actions/reference/security/oidc)과
[정확한 federated credential 수정 계약](https://learn.microsoft.com/graph/api/federatedidentitycredential-update)을 확인합니다.

## 5. 릴리스 순서

[수동 hosted-lab-release workflow](../../../../.github/workflows/hosted-lab-release.yml)는
기존 프로젝트 하나만 대상으로 하며 모델 배포를 생성하지 않습니다.
실제 반환 버전을 고정하고 dev 6문항 matrix를 smoke/회귀 gate로 사용합니다.
holdout이나 사람의 운영 승인을 자동으로 처리하지 않습니다.
첫 CI gate는 완전한 dev 6행의 업무 계약을 확인합니다. native 평가·calibration·continuous evaluation·
사람의 운영 인수는 별도로 선언하고 수행해야 합니다.

workflow는 runner의 임시 폴더에 hash·profile을 검증한 별도 azd 프로젝트를 준비합니다.
저장소의 과거 `azure.yaml`을 재사용하거나 이전 프로젝트에 CI service를 덧붙이지 않습니다.
공통 `prepare_hosted_azd.py --kind workflow` helper는 선택한 기존 프로젝트,
단일 primary 모델과 invocations protocol만 연결하며 provision 없이 로컬 환경 값을 초기화합니다.

`foundry-workshop` 환경에 승인된 `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`,
`AZURE_RESOURCE_GROUP`, `AZURE_AI_ACCOUNT_NAME`, `AZURE_AI_PROJECT_ENDPOINT`, 실제 `AZURE_AI_PROJECT_ID`,
`AZURE_AI_MODEL_DEPLOYMENT_NAME`, `WORKSHOP_PREFIX`, `WORKSHOP_HOSTED_AGENT_NAME`을 지정합니다.
agent 이름은 prefix로 시작해야 하고 branch/environment 보호를 설정합니다.

| Gate | 필요한 근거 |
|---|---|
| 로컬 검사 | offline/SDK tests, Ruff, compilation, 문서 계약 |
| Package | source/profile manifest, secret/정답 제외 |
| 승인 | 의도한 실습 target의 수동 dispatch/환경 승인 |
| Deploy | 실제 버전/endpoint/상태 |
| Smoke | 같은 버전의 유효한 실제 응답과 모델/도구 근거 |
| Quality | 완전한 cohort와 미리 정한 업무/native 기준 |
| 사람 결정 | 실제 인수 또는 검토 대기, 자동 운영 승인 금지 |
| 정리/rollback | 내 session/rule과 이전 알려진 버전 |

첫 workflow는 수동 실행하며 언어와 배포·역할·추론 비용 동의를 명시합니다.
동의가 없으면 skipped-success가 아니라 실패합니다.
시연 때문에 매 push 배포나 scheduled trigger를 추가하지 않습니다.
아직 게시/실행하지 않았다면 **설정만 완료**입니다.

## 6. 명시적 rollback

변경 전에 이전 agent/model/configuration 버전을 식별합니다.
smoke/quality 실패 시 rollout을 멈추고 실패 근거를 유지합니다.
rollback은 승인된 별도 작업이며 예외 처리 안에서 다른 모델을 고르는 동작이 아닙니다.

**다음:** [모델 운영](model-operations.md), [Lab 11](../11-capstone.md).
[모니터링·반복 평가](https://learn.microsoft.com/azure/foundry/observability/how-to/how-to-monitor-agents-dashboard).
