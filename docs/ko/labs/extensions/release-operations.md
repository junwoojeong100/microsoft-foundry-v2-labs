# 릴리스 운영: 제한된 모니터링과 명시적 배포 gate

[English](../../../labs/extensions/release-operations.md) | **한국어**

**C 선택.** 기존 CI의 로컬 로직·SDK·문서 검사는 배포된 agent의 품질 gate나 continuous evaluation과 다릅니다.

**근거 상태:** 2026-09-23 `gpt-6-sol`로 다시 실행했습니다. 두 OIDC 릴리스, 기존 추적 평가, 언어별 매시간 되풀이 일정 하나씩을 확인했고 두 일정 모두 일시 중지했습니다([결과](../../live-run.md#이전에-실행하지-않은-항목--2026-09-23)).

반복 유료 작업이나 배포 push에는 별도 승인이 필요합니다.

**첫 회차:** 두 경로 중 하나만 선택합니다.

| 경로 | 순서 | 준비·완료 |
|---|---|---|
| 제한된 모니터링 | 1–3절 | 완료된 추적 평가가 하나 있는 본인 agent·trace 접근·예산. 표본 결과와 일시 중지한 일정 기록 |
| CI 릴리스 | 4–6절 | 담당자가 준비한 GitHub OIDC·배포/런타임 권한. 실제 workflow 결과와 rollback/정리 판단 보관 |

**준비:** 선택 경로의 조건만 필요합니다. 모니터링에 GitHub ID가 필수인 것은 아닙니다.
**완료:** 해당 설정·실제 실행·품질 결정을 구분합니다.
**중단:** 기존 배포를 유지하고 누락된 권한/설정을 명시합니다. 성공처럼 보이는 대체 결과를 만들지 않습니다.
모니터링에서는 조사 전에 활성 일정을 일시 중지합니다. 중지 상태를 확인할 수 없다면 지정한 담당자에게 정리 대기로 인계합니다.

## 1. 자동화 전 근거

선택한 대상의 기존 근거를 재사용합니다. [Hosted 평가 워크북](../../reference/evaluation-workbook.md)은
전체 matrix를 얻는 방법 하나이지 이 페이지의 새 필수 실행이 아닙니다.
실제 버전, 모델 map,
원문/prompt/data hash, evaluator 버전, trace와 사람의 인수 상태를 보관합니다.
실패를 본 뒤 threshold를 재정의하거나 실패/누락 행을 빼거나 다른 대상 점수를 복사하지 않습니다.

## 2. 제한된 반복 평가 설정

전용 실습 agent의 완료된 추적 평가 하나([Lab 09 A](../09-operations.md#path-a))에서 시작해 그 평가 페이지의 **되풀이 설정**을 누릅니다.

| 방식 | 목적 | 첫 실습 경계 |
|---|---|---|
| 예약됨 | 라이브 트래픽(또는 데이터 세트의 기존 데이터)을 예약 평가 | 짧은 승인된 시험 후 즉시 일시 중지 |
| 연속 | 발생한 traffic을 표본 평가 | 지원되는 최소 sampling/run 제한, 무제한 요청 생성 금지. 2026-09-23 추적 평가에서는 사용할 수 없음 |

첫 회차는 **예약됨**과 **라이브 트래픽**을 유지하고 **실행 간격**을 **1시간(시간별)**로, 무작위 샘플링을 유지하고 실행당 최대 추적 수를 `5`로 둡니다.
**저장 전에** 담당자와 일시 중지할 정확한 시각을 정하고 `session-notes.txt`에 기록합니다.
즉시 시작할 수 있는 실행의 예산을 확보하고, 다음 시간별 실행은 추가 실행과 대기 시간이 승인된 경우에만 관찰합니다.
추적 5개는 실행당 제한이지 총 실행 횟수나 지출 상한이 아닙니다.
그런 다음 **저장**을 누릅니다. 페이지 버튼이 **일시 중지**로 바뀝니다. 일정 ID(SDK에서는 `<agent>-scheduled-<suffix>`), agent/버전 filter,
sampling, 최대 추적 수, evaluator 버전, 소유자와 일시 중지 계획을 기록합니다.
일정 생성/활성화는 실제 평가 증거가 아닙니다.
계획한 합성 요청 한 번 뒤 그 일정의 실행을 확인하고, 차트를 채우려고 모델 요청을 반복하지 않습니다.

## 3. 실제 결과와 일시 중지 상태

예약 실행은 같은 평가 페이지의 일회성 실행 옆에 표시됩니다. 실행마다 추적 창·버전·표본 대화·완료/실패·개별 결과를 확인합니다.
telemetry가 없으면 **미검증**이지 오류 0/비용 0이 아닙니다.

2026-09-23에는 일정을 저장하자마자 첫 예약 실행이 시작되었고, 모든 실행이 마지막 1시간이 아니라 최근 7일(일회성 실행의 시간 범위)에서
무작위 표본을 뽑았습니다. 다음 시간별 실행은 영문 계획 요청을 표본에 포함했지만(5/5 통과) 국문 계획 요청은 포함하지 않았습니다
(이전 대화 5/5). 이는 기록할 sampling 결과이지 요청을 다시 보낼 이유가 아닙니다.

계획한 관찰을 마쳤거나 **약속한 중지 시각에 도달하면** 대기·실패 상태 또는 조회 오류여도 **일시 중지**를 누릅니다.
중지 상태를 다시 읽습니다. 과거 SDK 확인에서는 두 일정이 `enabled: false`였습니다.
완료된 표본을 관찰하지 못했다면 `schedule configured; sample unverified`와 상태·오류를 보존하고 인계합니다.
근거를 기다리면서 반복 작업을 활성 상태로 남겨 두지 않습니다.
결과 파일은 그대로 보존하고 그 경로, 일정/실행 ID, 확인한 중지 상태를 `session-notes.txt`에 기록합니다.
중지를 검증하지 못했다면 모듈 완료가 아니라 담당자를 명시한 정리 대기로 남깁니다.
일시 중지해도 이미 발생한 모델·Search·로그 비용은 사라지지 않습니다.

**모니터링 완료:** 해당 기록을 [Lab 11](../11-capstone.md)에 추가합니다.
CI 경로를 별도로 선택하지 않았다면 OIDC ID를 만들지 않습니다.

## 4. 범위를 좁힌 GitHub OIDC

담당자와 별도 승인이 필요합니다.
의도한 저장소 및 branch/protected environment만 trust하도록 구성합니다.
필요한 training-project 배포/모델/도구 권한만 부여합니다.
client secret이나 구독 전체 Owner는 사용하지 않습니다.

이 workflow는 프로젝트 범위 **Foundry Project Manager**와 account metadata 읽기 권한을 사용합니다.
실제 배포된 runtime ID에 프로젝트 범위 **Foundry User**만 줄 수 있게 구성합니다.
helper가 반환된 agent/버전/principal을 확인하며 dispatch 입력의 임의 principal을 신뢰하지 않습니다.

tenant/subscription/client/project의 비밀 아닌 식별자는 환경 변수로 저장합니다.
토큰이나 `.env` 전체를 workflow log에 출력하지 않습니다.
[공식 Hosted CI/CD](https://learn.microsoft.com/azure/foundry/agents/quickstarts/set-up-cicd-hosted-agent)를
이 저장소의 패키지/profile과 정확한 smoke 계약에 맞춥니다.
stdout이 비어 있지 않다는 사실만으로 agent가 유효한 결과를 반환했다는 증거가 되지는 않습니다.

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
이 변수들에 client secret은 포함하지 않습니다.

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

Dispatch 전에 정확히 배포할 commit의 [Workshop checks](../../../../.github/workflows/check.yml)에서
`offline`과 `sdk-imports` job이 모두 성공했는지 확인하고 실행 URL·commit SHA를 기록합니다.
릴리스 workflow는 이 검사를 실행하거나 완료를 기다리지 않습니다. 근거가 없거나 실패했다면 dispatch 전에 멈춥니다.

첫 workflow는 수동 실행하며 언어와 배포·역할·추론 비용 동의를 명시합니다.
동의가 없으면 skipped-success가 아니라 실패합니다.
시연 때문에 매 push 배포나 scheduled trigger를 추가하지 않습니다.
아직 게시/실행하지 않았다면 **설정만 완료**입니다.

실행 뒤 **Actions → 해당 실행 → Artifacts**에서 `foundry-lab-<language>-<run-id>`를 **14일** 보존 기간이 끝나기 전에 내려받습니다.
해당 실행의 archive와 URL/commit SHA를 보관하고, 생성됐다면 `ci-binding.json`과 `benchmarks/ci-dev/`의 실패·정리 receipt까지 확인합니다.
초기 실패로 artifact가 없거나 일부만 있으면 빠진 단계를 기록하며 다른 실행의 근거로 대신하지 않습니다.

**2026-09-23 `gpt-6-sol` 실행:** 담당자가 `foundry-workshop` 변수를 `gpt-6-sol` 프로젝트(prefix `mfv2-sol-20260923-ci`)로 바꾸고,
기존 CI ID에 프로젝트 범위 **Foundry Project Manager**와 계정 **Reader**를 부여했습니다. federated credential은 바꾸지 않았습니다.
수동 dispatch한 [영문](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35856612314)·
[국문](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35857252318) 릴리스가 모두 첫 시도에 통과했습니다.
Hosted agent `mfv2-sol-20260923-ci-hosted` 버전 1·2가 배포되었고, 런타임 ID에 **Foundry User**를 한 번 부여해 버전 2도 재사용했습니다.
언어마다 dev 6문항 gate가 배포 `gpt-6-sol`(model version `2026-09-22`)에서 6/6, 오류 0이었고 생성한 session은 idle로 확인했습니다.
두 실행 모두 native 평가와 holdout은 실행하지 않았습니다.

## 6. 명시적 rollback

변경 전에 이전 agent/model/configuration 버전을 식별합니다.
smoke/quality 실패 시 rollout을 멈추고 실패 근거를 유지합니다.
rollback은 승인된 별도 작업이며 예외 처리 안에서 다른 모델을 고르는 동작이 아닙니다.

**다음:** [모델 운영](model-operations.md), [Lab 11](../11-capstone.md).
[모니터링·반복 평가](https://learn.microsoft.com/azure/foundry/observability/how-to/how-to-monitor-agents-dashboard).
