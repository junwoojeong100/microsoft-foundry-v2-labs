# gpt-6-sol 실제 실행·평가 결과 — 2026-09-24

[English](../live-run.md) | **한국어**

**2026-09-24 국문 녹화의 실제 Azure 실행 결과입니다.** 영문 실행, 이전 `gpt-5.6-luna` 판, 원본 저장소의 결과를 복사하지 않았습니다.

## 환경

| 항목 | 값 |
|---|---|
| 리전 / 프로젝트 | Sweden Central / `mfv2-g6luna-20260923` |
| 응답 배포 | `gpt-6-sol` → `gpt-6-sol` `2026-09-22`, DataZoneStandard 150K TPM, NoAutoUpgrade |
| 평가 배포 | `gpt-6-sol-judge` → `gpt-6-sol` `2026-09-22`, DataZoneStandard 100K TPM |
| 포털이 만든 배포 | `text-embedding-3-large` Standard 110K — 녹화한 실습자가 첫 포털 agent를 열 때 자동 생성; 이 실습에서는 사용하지 않음 |
| 소유 prefix | `mfv2-sol-20260924-ko` |

리소스 이름에는 환경을 처음 만들 때의 `g6luna`가 남아 있지만 녹화에 사용한 배포는 `gpt-6-sol`입니다. 로컬 키는 비활성화했으며 모든 호출은 Microsoft Entra ID를 사용했습니다.

## Lab 07 업무 기준 평가

| Cohort | Split | 지침 | 행 | 오류 | 업무 기준 | 지연 중앙값 |
|---|---|---|---:|---:|---:|---:|
| baseline | dev | v1 | 6 | 0 | 6/6 | 2.65 s |
| candidate | dev | v2 | 6 | 0 | 6/6 | 2.94 s |
| final-holdout | holdout | v2 (고정) | 4 | 0 | 4/4 | 2.81 s |

- 실제 baseline에 실패 사례가 없어 feedback 단계 대신 dev 전용 근거 없음 진단을 실행했습니다: 0/6, 오류 0, 모든 답변 보류. 전 문항 통과는 그대로 기록하며 v2가 더 낫다는 증거로 쓰지 않습니다.
- holdout 한 번 실행 전에 후보를 고정했으며 holdout을 지침 개발에 쓰지 않았습니다.
- 인수 판단: `ready-for-human-review`, `deployment_approved: false`. 작은 공개 합성 데이터이며 운영 검증이 아닙니다.

## 선택 Foundry cloud judge

candidate dev 6행을 `gpt-6-sol-judge`로 평가했습니다. evaluation `eval_32edb7c982dc4f4081672bdbdef2a6ec`, run `evalrun_03d3b7eb480b49b2a57704ecab2d6db9`, 상태 `completed`.

| Evaluator | 통과 | 실패 | 오류 |
|---|---:|---:|---:|
| groundedness | 6 | 0 | 0 |
| relevance | 5 | 1 | 0 |

relevance 실패 행은 의도한 보류 사례인 **D05**(점수 3)입니다. 해외 규정이 없으므로 금액을 주지 않은 답변이 맞습니다. 올바른 보류에 낮은 relevance가 나온 것은 검토할 judge의 한계이며 금액을 지어낼 이유가 아닙니다. 점수는 바꾸지 않았고 native judge 점수는 인수 판단에 포함하지 않습니다.

## 이번 녹화의 선택 Foundry 평가

| 평가 | 범위 | 결과 |
|---|---|---|
| 포털 평가(Lab 07 A) | `mfv2-sol-20260924-ko-portal-dev`, dev 6문항 | Relevance 6/6, Coherence 6/6, TaskAdherence 0/6 |
| 추적 평가(Lab 09 A) | `mfv2-sol-20260924-ko-traces`, 기록한 대화 | Relevance 15/15, Coherence 15/15, TaskAdherence 15/15 |
| 업무 기준(Lab 07 B, Preview) | `eval_3af44930ff5c423989b6cad9077befc0` | baseline: groundedness 6/6, relevance 5/6, business_rubric 6/6, 일치 6/6; candidate: groundedness 6/6, relevance 5/6, business_rubric 6/6, 일치 6/6 |
| MAF 도구 호출(Lab 04, 실험 API) | `eval_99190873d4204f6f93e95b2c795e6e8d` | tool_call_accuracy 5/6, relevance 5/6 |

judge 점수는 업무 판단이 아닙니다. 행마다 이유를 읽습니다. 포털 평가는 녹화한 이름으로 찾았고 행별 점수는 live-results.json에 있습니다.

## 이번 녹화에 남긴 실패

실패한 액션은 실제 출력 그대로 영상과 화면에 남겼습니다. 재시도나 수정은 별도의 이후 액션이며 실패한 액션을 대신하지 않습니다.

| ID | 종료 코드 | 내용 |
|---|---:|---|
| KP07-203-dataset | 캡처 도구 | 업로드는 성공했습니다(업로드 완료 메시지와 국문 질문 미리 보기가 표시됨). 하지만 데이터 세트 목록이 새로 고쳐지지 않아 캡처 도구가 새 행을 기다리다 시간 초과됐습니다. Foundry 실패가 아니며, KP07-213-dataset이 새 마법사에서 같은 데이터 세트를 선택했습니다. |
| KP07-215-criteria | 캡처 도구 | 이름 변경 창이 아직 로드 중일 때 캡처 도구가 입력하려 해 대상을 찾지 못했습니다(Target count 0). judge 선택과 제거는 이미 적용됐고, KP07-215-criteria-resume이 창이 열린 뒤 이름을 바꾸고 TaskAdherence를 추가했습니다. Foundry 실패가 아닙니다. |
| KP07-202-target-scope | 대체됨 | 대체됨: 대상 목록이 버전 1(Web search가 남아 있던 첫 버전)을 미리 선택했고 캡처 도구가 바꾸지 않았습니다. KP07-211~KP07-217에서 버전 2로 평가를 다시 실행했으며 버전 1 평가는 제출하지 않았습니다. |

## 그 밖의 실제 결과

- **Lab 02:** 첫 SDK 요청은 `response_model: gpt-6-sol`, 검증된 구조화 답변은 `TRAVEL-2026`, `RECEIPT-01`, `APPROVAL-01`을 인용했습니다.
- **Lab 03:** 포털 agent `mfv2-sol-20260924-ko-policy`는 버전 2로 저장했고 답변은 화면으로 기록했습니다(선택 Lab 09 추적 평가가 이후 이 대화를 채점). SDK agent `mfv2-sol-20260924-ko-policy-sdk` 버전 1을 생성·호출했습니다.
- **Lab 04–05:** `tools: none`·`function`·`local-mcp` MAF 실행과 sequential·concurrent·group-chat workflow가 모두 종료 코드 0으로 끝났습니다.
- **Lab 06:** 합성 정책 6개로 로컬·Search·GA IQ 검색을 실행했습니다. IQ 근거 답변은 `APPROVAL-01`, `RECEIPT-01`, `TRAVEL-2025`, `TRAVEL-2026`을 검색해 `TRAVEL-2026`, `APPROVAL-01`, `RECEIPT-01`을 인용했습니다(`needs_approval`, 150,000원).
- **Lab 08–09:** 패키징만(Hosted 배포 없음), 정리 목록만(삭제 없음) 실행했습니다.

## 계보

- base commit `90b18b305721c73398c92071f3ba7f85540c4d5d`, 작업 트리 source hash `71d81e13d0eb4ae4bac00c5185712d3ca9dbaf353f324159103a036aed1f0f3a`
- `baseline` run `148f3aab-acd3-4c67-a0f2-683ad82c9f95`: dataset `84e2b286e92e73f3…`, corpus `3556faa7cb0099cf…`, code `1632ec72c74c70fc…`, prompt `fb6e5f43288e2aa5…`, responses `a1b1dbf411a40ec8…`
- `candidate` run `018d1482-3672-4550-a7ea-19d706c68134`: dataset `84e2b286e92e73f3…`, corpus `3556faa7cb0099cf…`, code `1632ec72c74c70fc…`, prompt `2b4a2b5e322a8534…`, responses `47c23148ad3d6c3a…`
- `final-holdout` run `a04768a3-55aa-4839-9d74-8af8eea012a5`: dataset `9d478d727527064c…`, corpus `3556faa7cb0099cf…`, code `1632ec72c74c70fc…`, prompt `2b4a2b5e322a8534…`, responses `a3a39c3d9427ea25…`
- cloud judge: input `755439d5b4a4b468…`, evaluator `a0e7f44a59d34f75…`, results `47a12e3ba9d121a0…`

전체 hash는 [live-results.json](../assets/g6sol-20260924-ko/live-results.json)에 있습니다.

## 선택 평가 추가분 — 별도 검증, 2026-09-23

2026-09-24 녹화가 다시 실행하기 전에 선택 평가 단계를 확인한 실행입니다. 같은 소스(code hash `b160d84d2e0e1087…`)의 별도 복사본에서
새 label로, 같은 `gpt-6-sol` / `gpt-6-sol-judge` 배포와 prefix `mfv2-sol-20260923-ko`를 사용했으며 편집 영상에는 포함되지 않습니다.

| 단계 | 결과 |
|---|---|
| Lab 07 A 선택 포털 평가(`eval_b69ed3d1…`, `dev-questions.jsonl`의 6문항) | Coherence 6/6, Relevance 5/6(D05), TaskAdherence(Preview) 0/6. 같은 에이전트의 직접 업무 평가는 6/6 |
| Lab 07 B dev 수집(`baseline` `9ea18c52…`, `candidate` `9ed0ca38…`) | 업무 기준 6/6, 6/6, 오류 0 |
| Lab 07 B 근거 없음 진단(`diagnostic-no-evidence` `1e85d477…`) | 업무 기준 0/6, 오류 0. 모든 답변이 보류(`insufficient_evidence`). `feedback`은 이 실행을 거부 |
| Lab 07 B 업무 기준을 포함한 cloud judge(`eval_910a4729…`, 실행 2개) | baseline·candidate 모두 groundedness 6/6, relevance 5/6, `business_rubric` 6/6. 로컬 검사와 일치 6/6. 포털 비교 relevance 3.83 → 4.50, **샘플이 너무 적음** |
| Lab 04 선택 `maf-evaluate`(`eval_e3d8fa2f…`) | tool_call_accuracy 6/6, relevance 5/6(D05). 질문마다 `lookup_policy` 호출 1회 |

발견 사항, 코드 검토 후 재확인과 Azure 변경은 [검증 기록](reference/validation.md#foundry-evaluation-additions)에 있습니다.

## 이전에 실행하지 않은 항목 — 2026-09-23

같은 날 저녁 같은 프로젝트·배포와 prefix `mfv2-sol-20260923-<language>`로 실행했으며 편집 영상에는 포함되지 않습니다.

| 항목 | 실행한 내용 | 결과 |
|---|---|---|
| Lab 09 A 기존 추적 평가 | 담당자가 Application Insights에 대한 프로젝트 ID의 **모니터링 읽기 권한자**를 할당. 언어마다 기록된 대화 15개를 포털에서 평가(`eval_a68f080f…` 영문, `eval_71cf2435…` 국문) | 두 언어 모두 Relevance·Coherence·TaskAdherence 각 15/15. 각 `query`에 정책을 포함한 에이전트 지침이 들어 있음 |
| 되풀이 평가 | 추적 평가마다 **되풀이 설정**: 예약됨, 시간별, 라이브 트래픽, 무작위 샘플링, 실행당 추적 5개. 언어마다 계획한 D01 요청 1회 후 **일시 중지** | 일정을 저장하자 첫 실행이 시작됨(언어마다 5/5). 다음 시간별 실행은 영문 계획 요청을 표본에 포함했지만(5/5) 국문 계획 요청은 포함하지 않음(이전 대화 5/5). 매 실행이 최근 7일에서 표본을 뽑음. 두 일정은 일시 중지 후 비활성으로 다시 확인 |
| Agent Optimizer | 임시 `gpt-5.5` optimizer 배포, 격리 복사본 `mfv2-sol-20260923-<language>-optimize` v1, Instruction만·후보 2개·judge `gpt-6-sol-judge`(`opt_63e8e1d5…`, `opt_607d539e…`) | baseline만 반환: 영문 0.979, 국문 0.938(D05 relevance 2). Groundedness가 답변을 자기 자신과 비교. 승격 없음. 임시 배포는 이후 삭제 |
| 클라우드 red teaming(Preview) | Lab 03 prompt agent의 SDK scan(금지된 작업 taxonomy, Flip·Base64, 1턴)과 행동 2개 taxonomy로 한 영문 포털 scan | 표시된 ASR은 영문 89%(75/84), 국문 57%(48/84), 포털 100%(6/6)였지만 모든 행의 reasoning은 응답이 안전하다고 판단. 금지 행동을 수행한 응답 없음. ASR을 무효로 표시 |
| 승인된 Hosted 릴리스 | 기존 CI ID에 이 프로젝트 범위 역할 부여. `hosted-lab-release` 실행 [35856612314](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35856612314)(영문), [35857252318](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35857252318)(국문) | 둘 다 첫 시도에 통과: Hosted agent `mfv2-sol-20260923-ci-hosted` 버전 1·2, dev 6문항 gate 6/6·오류 0, session idle |

발견 사항, 담당자 조치와 Azure 변경은 [검증 기록](reference/validation.md#previously-not-run-items)에 있습니다.

<a id="review-refresh-live-verification"></a>

## 검토 반영 실제 검증 — 2026년 9월 24일(저녁)

위와 같은 프로젝트와 배포를 사용했습니다. commit `a9c3990`의 새 복사본 두 개에서 prefix `mfv2-rr-20260924-en`·`mfv2-rr-20260924-ko`와
갱신한 고정 버전(`azure-ai-projects` 2.6.1, `openai` 3.16.1, MAF core 1.18.0, `agent-framework-foundry` 1.13.0,
hosting 1.0.0b260910, `mcp` 1.30.0)을 사용했습니다. 모든 호출은 실습 구독을 고정한 Microsoft Entra ID로 했고,
Azure CLI 기본 구독은 바꾸지 않았습니다. 이 검증은 녹화하지 않았고, [2026-09-25 보충 녹화](#review-refresh-supplement)에서 Lab 03 B와 Lab 09 B 추적 검색을 녹화했습니다.

| B 핵심 단계 | 영문 | 국문 |
|---|---|---|
| Lab 00 `doctor --cloud` | `gpt-6-sol` `2026-09-22`, `Succeeded` | 같음 |
| Lab 02 `model` / `answer` | `response_model: gpt-6-sol`, 150,000원(`TRAVEL-2026`, `APPROVAL-01` 인용) | 같은 모델, 150,000원(`TRAVEL-2026`, `RECEIPT-01`, `APPROVAL-01` 인용) |
| Lab 03 B 관리형 agent | `mfv2-rr-20260924-en-policy-sdk` 버전 1, 호출 `resp_0e84a5df…`(1,124 / 101 token), `TRAVEL-2026` | `mfv2-rr-20260924-ko-policy-sdk` 버전 1, 호출 `resp_0883c0c2…`(1,290 / 157 token), `TRAVEL-2026` |
| Lab 04 함수 / MCP | `needs_approval`(`TRAVEL-2026`, `APPROVAL-01`, `RECEIPT-01`) / 120,000원(`TRAVEL-2025`) | 같은 판단과 인용 |
| Lab 05 workflow | 순차 1개, 병렬 4개, Group Chat 4개 출력, 모두 `pending-human-review` | 같음 |
| Lab 06 검색 | 로컬·Search는 원문 6개, GA IQ는 4개. IQ 답변 `needs_approval`(`TRAVEL-2026`, `APPROVAL-01`) | 같음 |
| Lab 07 | baseline 6/6, candidate 6/6, holdout 4/4, 오류 0, `ready-for-human-review`, `deployment_approved: false` | 같음 |
| Lab 08–09 | 패키지 `cloud_deployed: false`, `cleanup-plan`에 소유 Search 객체 3개 | 같음 |

지연 시간 중앙값: 영문 2.51 / 2.67 / 3.53초, 국문 2.46 / 3.17 / 2.56초(baseline / candidate / holdout). 두 baseline 모두 실패 사례가 없어
`feedback`은 실행하지 않았습니다. Lab 07 실행: 영문 `9a8d3d81…`, `9e187bee…`, `8953197f…`, 국문 `bf510464…`, `4924c781…`, `ded07977…`.

**추적(Lab 09 B):** response ID로 읽기 전용 Application Insights 조회를 실행해 모든 관리형 agent 호출에서 `invoke_agent <agent>:1`과
`chat gpt-6-sol-2026-09-22` span을 찾았습니다. token 수는 저장된 `usage`와 같았고 약 3분 안에 나타났습니다.
Responses API를 직접 호출한 명령(`model`, `answer`, `maf`, `workflow`, `collect`)은 서버 측 span을 남기지 않았습니다.

| 선택·C 항목 | 결과 |
|---|---|
| Lab 04 `maf-evaluate`(영문) | `complete: true`, 오류 0, tool_call_accuracy 6/6, relevance 6/6. Pydantic serializer 경고가 출력됐지만 결과에는 영향 없음 |
| Lab 07 `cloud-evaluate` candidate(영문) | groundedness 6/6, relevance 5/6(D05 점수 2, 올바른 보류) |
| A2A 1.0(영문) | 형식이 있는 SDK 요청으로 target·caller 생성, card는 1.0 JSONRPC와 0.3을 함께 제공, 위임 호출 1회(`a2a_preview_call`) 완료, caller 사용량 676 / 228 token |
| Insights(영문, SDK) | trace 22개 분석, insight 4개, judge token 227,246개. 이후 monitor 삭제 |
| Lab 08 6절 workflow 서버(영문, 로컬) | `healthy`, Responses 요청 1회가 모델 호출 3회와 `pending-human-review`로 완료(`azd ai agent invoke --local`이 아니라 curl로 전송) |
| 예제 02–06·08(영문) | 아래 두 가지를 고친 뒤 모두 완료 |

**이 확인에서 찾고 고친 것:**

1. 예제가 구독 없이 `AzureCliCredential()`을 만들었습니다. Azure CLI 계정이 여러 개일 때 다른 tenant의 기본 계정을 사용해 호출이 403으로 실패했으므로 이제 `AZURE_SUBSCRIPTION_ID`를 고정합니다.
2. 예제 05와 08은 정책 근거를 보내지 않아 모델이 사용할 정책이 없다고 답했습니다. 이제 합성 정책을 데이터로 함께 보냅니다.
3. `openai` 3.x에서 `maf-evaluate`는 Pydantic serializer 경고를 출력합니다. 가이드는 `complete`와 `errors`로 판단하도록 안내합니다.
4. 기본 계정에 묶인 도구로 Application Insights를 조회하면 `InvalidTokenError`가 났습니다. 가이드는 실습 tenant용 token을 쓰도록 안내합니다.

**미실행:** A Lab 05 브라우저 선택지를 위한 원격 Hosted 배포(별도 승인 필요), 타사 모델 비교(프로젝트에 OpenAI 외 배포 없음),
Toolbox·Tool Search·Skills(그날 저녁에는 시도하지 않음. 2026-09-25 확인에서 keyless 연결은 있었지만 Search가 프로젝트 ID를 거부함, [아래](#not-run-feasibility)), Memory·Routines·대화 평가·Agent Optimizer·red teaming(코드 변경 없음, 재실행 안 함),
A 경로의 포털 단계.

**생성한 소유 객체:** agent `mfv2-rr-20260924-en-policy-sdk`, `-ko-policy-sdk`, `-en-recipe-sdk`, `-en-a2a-target-en`, `-en-a2a-caller-en`(각 버전 1),
연결 `mfv2-rr-20260924-en-a2a-link-en`, prefix별 Search index·knowledge source·knowledge base, `maf-evaluate`와 `cloud-evaluate`가 만든 Foundry 평가.
그날 저녁에는 Insights monitor 외에는 삭제하지 않았고, 나머지는 2026-09-25에 삭제했습니다([정리 기록](#cleanup-20260925)).

<a id="review-refresh-supplement"></a>

## 보충 녹화와 미실행 항목 검토 — 2026년 9월 25일

**영문·국문 녹화.** commit `f990af3`의 중립 작업 복사본, prefix `mfv2-sup-20260925-<language>`, 같은 프로젝트와 배포를 사용했습니다.
가이드 블록을 실제 zsh 터미널에 그대로 붙여 넣고 `read` 프롬프트에는 직접 입력했습니다.

| 단계 | 영문 | 국문 |
|---|---|---|
| Lab 03 B 생성(`--output`) | `mfv2-sup-20260925-en-policy-sdk` 버전 1 | `mfv2-sup-20260925-ko-policy-sdk` 버전 1 |
| Lab 03 B 호출(`--output`) | `resp_0ba4d3d0…`, 1,124 / 145 token; `TRAVEL-2026`을 인용한 150,000원 | `resp_01227453…`, 1,290 / 160 token; `TRAVEL-2026`, `RECEIPT-01`, `APPROVAL-01`을 인용한 150,000원 |
| Lab 03 B 포털 확인 | 플레이그라운드: 버전 1, 지침이 CLI 정의와 같음; 세부 정보: `Latest (Version 1)`; 메시지 보내지 않음 | 같음; 세부 정보는 `최신(Version 1)` |
| Lab 09 B 추적 검색 | 한 행; trace `0ef25bf8…`가 Application Insights `operation_Id`와 같음; `invoke_agent …:1`과 `chat gpt-6-sol-2026-09-22` | 한 행; trace `71804741…`; 같은 span |

화면과 영상: [요약](video-summary.md#review-refresh-supplement) · [captures.json](../assets/review-refresh-20260925/captures.json).
영문 첫 시도(`mfv2-cap-20260925-en-policy-sdk`, 호출 1회)는 터미널에 로컬 홈 디렉터리 경로가 보여 폐기했습니다.

<a id="not-run-feasibility"></a>

### 미실행 항목에 필요한 것

영문만, prefix `mfv2-nr-20260925-en`, 같은 프로젝트, 실습 구독 고정.

| 항목 | 결과 또는 막힌 이유 |
|---|---|
| 대화 평가, 갱신한 고정 버전 | 6개 턴, 업무 검사 6/6; 턴 수준 groundedness 6/6·coherence 6/6(`eval_e07e2e35…`); 대화 수준 groundedness 2/2·coherence 2/2(`eval_e82b6f87…`) |
| Memory, `gpt-6-sol` + `text-embedding-3-large` | store 생성; alpha 항목 저장 후 새 요청에서 recall; beta recall은 비어 있음; update·forget·store 삭제 후 부재 확인 |
| Routines, azd `azure.ai.routines` 1.0.0-beta.6 | 비활성 일회성 timer; 수동 dispatch 1회 `Finished`; 비활성화 후 삭제. SDK helper는 여전히 응답을 가져오지 못했지만, 그 `response_id`로 추적을 검색하니 `invoke_agent …:1`과 `chat` span이 나왔습니다 |
| Toolbox | 소유 index를 만들고 Toolbox 버전 1 생성; MCP 탐색에서 `policy_search` 확인. 직접 query는 Search에서 **Access denied**: keyless `workshop-search` 연결은 있지만 프로젝트 ID에는 Search Index Data Reader만 있습니다. Toolbox는 삭제했고 역할은 바꾸지 않았습니다 |
| Tool Search와 Skills | 같은 Search 접근 문제로 막힘 |
| A 경로 Lab 09 추적 확인 | 읽기 전용: **7일** 범위에서 2026-09-24 브라우저 agent의 추적 16개가 보였고, 연 12개 모두 `invoke_agent <agent>:2`와 자식 `chat` span이 있었습니다 |
| 원격 Hosted 배포(A Lab 05 브라우저 선택지) | 배포와 런타임 역할 할당이 필요하므로 담당자 승인 필요 |
| 타사 모델 비교 | OpenAI 외 배포 1개가 필요합니다. 읽기 전용 확인: 계정 카탈로그에 예를 들어 `grok-4-1-fast-reasoning`(GlobalStandard), `Mistral-Large-3`(DataZoneStandard)가 있고 할당량이 남아 있습니다. 담당자 승인 필요 |
| Agent Optimizer | `gpt-5.5` 같은 지원 optimizer 배포가 필요합니다(할당량 있음). 담당자 승인 필요 |
| 클라우드 red teaming | 워크숍 코드 경로가 바뀌지 않았으므로 2026-09-23 결과를 유지하고 재실행하지 않음 |
| Foundry Dev Pack | 작업 PC의 전역 `az`/`azd` 도구를 설치·업그레이드하므로 깨끗한 PC에서 실행; 실행하지 않음 |

**2026-09-25에 만든 소유 객체:** agent `mfv2-cap-20260925-en-policy-sdk`, `mfv2-sup-20260925-en-policy-sdk`, `mfv2-sup-20260925-ko-policy-sdk`,
`mfv2-nr-20260925-en-policy-sdk`(각 버전 1), Search index `mfv2-nr-20260925-en-policies`, 대화 평가 2개.
Memory store, Toolbox, routine은 각 모듈 명령으로 삭제했고, 나머지도 같은 날 삭제했습니다.

<a id="cleanup-20260925"></a>

### 정리 — 2026년 9월 25일

2026-09-24·25 확인에서 만든 소유 객체를, 정의와 평가 결과를 비공개 기록에 내보낸 뒤 삭제했습니다.
삭제 후 각 객체를 다시 조회해 모두 404임을 확인했습니다.

| 객체 | 삭제한 것 |
|---|---|
| Agent(각 버전 1) | `mfv2-rr-20260924-en-a2a-caller-en`, `mfv2-rr-20260924-en-a2a-target-en`, `mfv2-rr-20260924-en-policy-sdk`, `mfv2-rr-20260924-ko-policy-sdk`, `mfv2-rr-20260924-en-recipe-sdk`, `mfv2-cap-20260925-en-policy-sdk`, `mfv2-sup-20260925-en-policy-sdk`, `mfv2-sup-20260925-ko-policy-sdk`, `mfv2-nr-20260925-en-policy-sdk` |
| 연결 | `mfv2-rr-20260924-en-a2a-link-en`. 호출 agent 다음, 대상 agent 전에 삭제 |
| 평가 | `mfv2-rr-20260924-en-maf-tools`, `mfv2-rr-20260924-en-candidate`, `mfv2-nr-20260925-en-conversations-first-turn`, `mfv2-nr-20260925-en-conversations-first-conversation` |
| 데이터 세트 | 위 평가 실행과 함께 서비스가 만든 `eval-data-2026-09-24_…_UTC` 데이터 세트 4개. 시각과 행 내용으로 대응을 확인 |
| Search | `mfv2-rr-20260924-en`·`mfv2-rr-20260924-ko`의 knowledge base → knowledge source → index, index `mfv2-nr-20260925-en-policies` |

삭제한 각 agent의 Entra agent ID와 청사진도 404였고, 남겨 둔 agent의 것은 계속 200이었습니다.
평가 삭제 호출의 응답에는 `deleted: true` 필드가 없었으므로 다시 조회해서만 삭제를 확인했습니다.
남긴 것: 2026-09-23·24 녹화의 agent·평가·데이터 세트, 공유 연결·배포·Search 서비스·Application Insights.

<a id="end-to-end-20260925"></a>

## 가이드대로 끝까지 실행 — 2026년 9월 25일

**두 기본 경로를 같은 프로젝트와 배포에서 영문·국문 모두 가이드에 적힌 그대로 실행했습니다.** commit `f128f0c`의 새 복사본을
GitHub에서 받았습니다. 영문은 안내된 sparse clone, 국문은 **Download ZIP**을 사용했고 prefix는 `mfv2-e2e-20260925-<language>`입니다.
B 경로는 Lab 00–11의 핵심 bash 블록을 순서대로 한 터미널(영문 zsh, 국문 macOS bash 3.2)에서 실행하고 각 `read` 프롬프트에 직접 입력했습니다.
블록 밖에서 한 일은 가이드가 설명하는 두 가지뿐입니다. 이미 로그인한 계정으로 `az login`을 대신했고(이 공유 PC의 기본 구독도 바꾸기 때문),
`.env`를 설정 카드 값으로 채웠습니다. A 경로는 영문·국문 포털 UI에서 Lab 01–03, 07, 09 단계를 실행했고, 영문에서 Lab 05 A 터미널 명령도 실행했습니다.

| 확인 | 영문 | 국문 |
|---|---|---|
| B 경로 블록 | 34개 모두 종료 코드 0. baseline이 6/6이라 feedback 블록은 건너뜀 | 같음 |
| B 경로 결과 | baseline 6/6, candidate 6/6, holdout 4/4, `ready-for-human-review`, `deployment_approved: false`, Lab 03 B 버전 1, Search·IQ 문서 6개, Lab 08은 패키징만 | 같음 |
| A 경로 Lab 01–02 | 전체 project endpoint, `gpt-6-sol` `2026-09-22` **Succeeded**, **빌드** 메뉴의 네 항목, Web search가 있어 제거, 근거 없는 질문에는 정책을 요청 | 같음(국문 UI) |
| A 경로 Lab 03·07 | 정책 ID 6개가 든 버전 2로 저장, D01–D06 모두 그 버전에서 기준 충족 | 같음 |
| A 경로 Lab 09 | **Details** `Latest (Version 2)`, 추적 10개, 연 추적에 `invoke_agent <agent>:2`와 자식 `chat` span, `web.run` 없음 | **세부 정보** `최신(Version 2)`, 추적 같음 |

**찾아서 고친 가이드 내용:**

1. 포털의 **에이전트 만들기** 창에 필수 **상호 작용 모드**(기본 **텍스트**, 만든 뒤 변경 불가)가 생겼고 버튼 이름이
   **에이전트 만들기 및 플레이그라운드 열기**로 바뀌었습니다. Lab 03 A에 반영하고 [새 창](../assets/e2e-check-20260925/captures.json)을 보여 줍니다.
2. agent의 **세부 정보** 탭에는 이름과 활성 버전만 있고 모델은 없습니다. Lab 09 A는 이제 **플레이그라운드** 탭에서 모델을 확인합니다.
3. Lab 03 A가 삭제된 2026-09-23 녹화의 agent 이름을 적고 있었습니다. 이제 2026-09-24 녹화 이름을 적습니다.
4. Lab 02 B는 필드가 최상위 `answer` 객체 안에 있다고 설명하고, Lab 05 B는 국문 실행에도 나오는 영문 라운드 상한 문구
   `The group chat has reached the maximum number of rounds.`를 그대로 적습니다.
5. 국문 Lab 07 feedback 블록의 입력 안내를 한국어로 바꿨습니다.

**정리:** agent `mfv2-e2e-20260925-<language>-policy`(버전 1–2)와 `mfv2-e2e-20260925-<language>-policy-sdk`(버전 1),
언어별 Search knowledge base·knowledge source·index를 삭제하고 다시 조회해 404를 확인했고, agent의 Entra agent ID도 404였습니다.
평가나 데이터 세트는 만들지 않았습니다.

## gpt-6-sol로 실행하지 않은 것

- Lab 03 포털 File Search
- Lab 06 IQ Chat preset(gpt-5.6-luna)과 하이브리드 RAG
- Lab 07 feedback/regression 단계(baseline 실패 없음, 대신 근거 없음 진단 실행)
- Lab 07 Hosted 모델 matrix
- Lab 08 기본 로컬 서버, `azd ai agent invoke --local`, 학습자 본인의 Hosted 배포(위의 승인된 CI 릴리스는 별도 Hosted agent를 배포했고, 검토 반영 확인에서 6절 workflow 서버가 `curl` 요청 하나에 답변)
- Lab 09 Hosted agent의 서버 측 tracing 확인
- Lab 10 외부 IQ 확장
- 대화 평가, Agent Optimizer, 안전 제어의 red-team 단계, 릴리스 운영, 검토 반영의 A2A와 Insights 확인, 2026-09-25의 Memory·routine·Toolbox 탐색 확인을 제외한 확장 모듈

이전 `gpt-5.6-luna` 녹화와 결과 페이지(2026-09-15~17)는 작업 트리에서 삭제했습니다. git 기록에만 남아 있으며 이 preset의 결과가 아닙니다.

[영상](video-summary.md) · [액션과 화면](action-captures.md) · [챕터](video-chapters.md) · **실제 결과** · [모델 선택](reference/model-choice.md)
