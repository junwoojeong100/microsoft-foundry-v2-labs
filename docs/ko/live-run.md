# gpt-6-sol 실제 실행·평가 결과 — 2026-09-24

[English](../live-run.md) | **한국어**

**2026-09-24 국문 녹화의 실제 Azure 실행 결과입니다.** 영문 실행, 이전 `gpt-5.6-luna` 판, 원본 저장소의 결과를 복사하지 않았습니다.

**이후 확인:** [9월 25일 Azure 가이드 점검](#azure-guide-audit-20260925)은 두 언어의 CLI 경로와 trace API를 확인했고 요청 실패 한 건을 보존합니다. 새 포털 녹화가 아닙니다.
그 뒤 [headless 포털 후속 확인](#headless-guide-audit-20260925)으로 브라우저 인증 문제를 해결하고 새 응답·실측값·스크린샷을 추가했습니다. 새 영상은 아닙니다.
**최신:** [최종 마무리 확인](#final-guide-closeout-20260925)은 가이드 최종 수정과 오프라인 검사 후에만 범위를 제한한 핵심 검증을 실행했습니다. 새 결과와 남은 경계는 아래에 별도로 기록합니다.

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

<a id="azure-guide-audit-20260925"></a>

## Azure 가이드 점검 — 2026-09-25(CLI·trace API)

**범위:** `b741473` 이후의 미커밋 가이드 수정까지 포함한 작업 트리를 영문·국문 별도 복사본으로 실행했습니다.
위의 기존 프로젝트와 `gpt-6-sol` / `2026-09-22` 배포를 읽기 전용으로 확인했습니다.
원본 저장소의 개인 `.env`는 이전 프로젝트와 `gpt-5.6-luna`를 가리키고 있었으며 그대로 두었습니다.
새 복사본에는 확인한 현재 가이드의 설정과 본인 prefix `mfv2-a2-0f01-en`, `mfv2-a2-0f01-ko`를 사용했습니다.
대체 결과를 얻으려고 이전 모델을 호출하지 않았습니다.

| 확인 | 영문 | 국문 |
|---|---|---|
| 기본 B 터미널 블록 | 서로 다른 33개 블록 완료. 첫 Group Chat 실패로 총 34회 시도 | 33개 블록 모두 첫 시도 완료 |
| 저장 응답 파일 | 기본 JSON 14개 모두 보존 | 독립 국문 파일 14개 보존 |
| 관리형 Prompt Agent | `mfv2-a2-0f01-en-policy-sdk`, 버전 `1` | `mfv2-a2-0f01-ko-policy-sdk`, 버전 `1` |
| 함수 / 로컬 MCP | 170000원 예약 전 승인 조건, 과거 120000원·`TRAVEL-2025` 확인 | 같은 기준의 독립 국문 응답 |
| 순차 / 병렬 / Group Chat | 출력 1/4/4개. 사람 검토 대기, 외부 동작 없음 | 같은 출력 구조. 순차 최종 문구는 날짜를 생략하고 한도 초과 조건으로 금액을 설명해 검토 사항으로 보존 |
| Search / GA IQ | 합성 정책 6건 색인. Local·일반 Search는 6건, IQ는 `TRAVEL-2026`·`APPROVAL-01`을 포함한 4건 | 국문 corpus에서 같은 수 확인 |
| IQ 근거 답변 | `needs_approval`, 150000원, 필수 인용 두 개. 재검색 context hash가 앞선 IQ 결과와 같음 | 같은 기준이며 독립 국문 context hash 일치 |
| Lab 07 baseline / candidate / 최종 holdout | 6/6 / 6/6 / 4/4. 수집 오류 0 | 6/6 / 6/6 / 4/4. 수집 오류 0 |
| 인수 | `ready-for-human-review`, `deployment_approved: false` | 영문에서 복사하지 않은 같은 판단 |
| Lab 09 trace API | 같은 `invoke_agent`·`chat` span. input/output token 1124/123 | 같은 방식으로 일치. 1290/216 |
| A Lab 05 터미널 | 정확한 170000원 질문을 한 번 실행·검토 | 국문도 독립적으로 한 번 실행·검토 |
| Lab 08 / Lab 11 | 로컬 패키지만 생성. `accept`를 반복하지 않고 기존 인수 보고서를 읽음 | 동일 |

Baseline이 모두 통과해 `feedback`은 올바르게 건너뛰었습니다. 각 후보를 검토·고정한 뒤 holdout을 한 번만 수집했습니다.
평가 실행 여섯 개의 code hash는 `d105b70b726458f70c1f7820ae8f6a921f0d42a2e008e8100af083e876f59ae4`이며,
언어마다 별도 prompt·corpus·dataset·response hash를 보존했습니다. 공개 교육용 holdout은 미사용 운영 인수 세트가 아닙니다.

**보존한 실패와 코드 수정:** 영문 Group Chat 첫 시도에서 `az account get-access-token`이 설정된 subprocess timeout 30초를 넘었습니다.
MAF가 인증 오류를 `ChatClientException`으로 감싸 기존 CLI 오류 처리 밖으로 빠져나가 traceback·종료 코드 `1`이 나왔습니다.
이제 CLI는 명시적인 Agent Framework 예외 계열을 처리해 하위 원인을 알리고 표준 실패 코드 `2`로 종료하며 성공 파일을 만들지 않습니다.
자동 재시도·대체 경로를 추가하지 않았고 timeout·모델·endpoint·prompt도 바꾸지 않았습니다.
읽기 전용 token 확인 성공 뒤 같은 설정으로 새 Group Chat 시도 한 번이 완료됐으며 최초 로그는 그대로 남았습니다.

**브라우저 경계:** Playwright headless 관찰에서 계정·tenant 불일치를 확인했습니다. 프로젝트 머리글과 **Loading...**만으로
SDK agent가 로드됐다고 판단할 수 없었습니다. 실습 계정용 인증 전용 브라우저를 화면에 열었지만 올바른 tenant의 포털 확인은 인증 대기입니다.
A 포털 순서나 B의 포털 agent/trace 확인을 이번에 새로 완료했다고 주장하지 않습니다.
위 trace 결과는 포털이 아닌 scope가 고정된 읽기 전용 API에서 얻었습니다. 새 스크린샷·영상 자산은 만들지 않았습니다.
이는 해당 CLI 점검 시점의 경계이며, 아래 별도 headless 후속 확인에서 포털 인증 문제를 해결했습니다.

**추가 명확화:** `Succeeded`만이 아니라 정확한 preset을 확인하고, A의 명시적 workflow 질문과 B 기본 질문을 구분하며,
IQ의 `agenticReasoning`·검색 token을 응답 모델 `usage`와 분리합니다.
두 GA IQ 결과에는 각각 reasoning token 413·505가 있었지만 선택 모델 계획/합성의 실행 증거는 아닙니다.

**검토를 위해 보존한 소유 자산:** SDK agent 두 개와 언어별 prefix의 `-policies` index, `-source` knowledge source,
`-kb` knowledge base. 각 작업 폴더에 원본 소유권 ledger·오류·결과를 보존했습니다.
정리 목록만 작성했고 클라우드 객체를 삭제하지 않았습니다. 공유 모델·Search·로그는 담당자 관리로 남깁니다.
모델 배포·역할 할당·Hosted 배포·기본 구독 변경·push는 하지 않았습니다.
기존에 로그인된 CLI 계정을 사용했으며 최소 권한만 가진 학습자 계정은 별도로 시험하지 않았습니다.

[결과·hash·trace ID의 JSON 기록](../assets/azure-guide-audit-20260925/results.json) ·
[검증과 수정](reference/validation.md#azure-guide-audit-20260925).

<a id="headless-guide-audit-20260925"></a>

## Headless 포털 후속 확인과 응답시간 실측 — 2026-09-25

**인증 때문에 남아 있던 A/B 포털 확인에 새 실제 근거를 추가했습니다.** 화면에 보이는 브라우저는 인증에만 사용했고,
모든 확인은 같은 실습 프로젝트에서 **Playwright MCP headless**로 영문부터 진행한 뒤 국문을 확인했습니다.
포털 언어는 영어로 복원했고 임시 인증 전달 파일은 삭제했습니다.

기존 A agent `mfv2-sol-20260924-<language>-policy`의 **버전 2**를 새 버전 저장 없이 재사용했습니다.
실제 저장 지침은 합성 정책 6개를 포함한 현재 학습자 파일과 정확히 일치했습니다.
만들기 창은 확인 후 취소했으므로 **새 agent 생성 실행이 아니라 재개·읽기 확인과 실제 요청 검증**입니다.

| 확인 | 영문 | 국문 |
|---|---|---|
| Lab 02 모델 Playground | 새 응답 2건. 근거 없는 질문에서 금액을 보류 | 독립 국문 응답 2건. 금액을 보류 |
| Lab 03 / Lab 06 인라인 근거 | 새 smoke 응답 4건이 적용일·금액·승인·인용 기준 충족. 외부 도구·지식 연결 없음 | 국문 질문·지침으로 같은 네 기준 확인 |
| Lab 07 고정 버전 dev 평가 | **6/6**, 요청 오류·누락 행 없음 | **6/6**, 요청 오류·누락 행 없음 |
| dev 6행의 보내기 → 응답 표시 시간 | 중앙값 **6.75초**, 범위 **5.69–9.29초** | 중앙값 **5.41초**, 범위 **4.11–7.01초** |
| Lab 09 A, 이번 D06 | 응답·버전 2·`invoke_agent` → `chat` 일치. input/output **1144/153** | 응답·버전 2·span 일치. **1339/273** |
| Lab 03 B / Lab 09 B, 원래 점검 요청 | SDK 지침이 CLI 정의와 정확히 일치. 버전 1, trace **79b867e1985015fdd02cfe8a47fa9ee7**, token **1124/123** | 지침 정확히 일치. 버전 1, trace **87fad9894be9e9c55f0a9b3d8b5199bc**, token **1290/216** |

**실측 경계:** 새 요청은 총 24건으로 언어별 모델 2건·smoke 4건·dev 6건입니다.
질문마다 새 채팅을 시작했습니다. B 추적을 찾으려고 재호출하지 않았으며 candidate·holdout·cloud judge도 실행하지 않았습니다.
시간은 보내기 클릭부터 해당 응답 ID의 복사 동작이 화면에 나타날 때까지로, 포털·네트워크·렌더링 시간이 포함됩니다.
서버 span 시간, 실제 학습자 시범 운영, 270분 수업 검증 또는 어느 언어가 더 빠르다는 근거가 아닙니다.
국문 개념 응답은 Foundry 리소스를 작업 공간으로 단순화했으므로, 리소스·프로젝트 구분은 Lab 01의 설명을 기준으로 합니다.

**수집 실패 보존:** 초기 계측 도구에서 VM·endpoint·응답 본문·스트림 종료 처리의 제약이 발생했습니다.
원래 응답과 response ID를 화면에서 보존했으며 같은 질문을 다시 보내지 않았습니다.
초기 요청 4건은 고해상도 시간이 없고 임의 값을 채우지 않았습니다. 언어별 dev 6행에는 모두 실측 시간이 있습니다.
이 수집 오류가 앞선 CLI 점검의 Group Chat 실패를 대체하지도 않습니다.

**계속 미실행:** File Search는 선택한 `gpt-6-sol` 모델에서 **파일 업로드**가 비활성화되고 모델 미지원 안내가 표시됐습니다.
원격 Lab 05 Hosted **Responses** Playground 방식, 새 배포·역할·기본 구독 변경, 선택 cloud judge·C 모듈도 실행하지 않았습니다.
A Lab 05의 완료된 터미널 결과는 앞선 점검에 그대로 두었고 재실행하거나 Hosted 결과로 바꾸어 적지 않았습니다.
Agent 정의·prompt·corpus·dataset·채점 기준을 바꾸지 않았고 게시·push·클라우드 삭제도 하지 않았습니다.
새 대화·응답 기록과 기존 공유 서비스에는 담당자의 정리·비용 관리 계획이 계속 적용됩니다.

**근거:** 새 스크린샷 28개, 두 언어의 6행 평가 CSV, 실제 지침 스냅샷, 응답·token,
trace 메타데이터·SHA-256 hash를 이전 녹화와 분리해 보존했습니다.
[결과와 hash](../assets/headless-guide-audit-20260925/results.json) ·
[영문 평가표](../assets/headless-guide-audit-20260925/en/assessment-baseline.csv) ·
[국문 평가표](../assets/headless-guide-audit-20260925/ko/assessment-baseline.csv) ·
[영문 trace](../assets/headless-guide-audit-20260925/en-b-trace-detail.png) ·
[국문 trace](../assets/headless-guide-audit-20260925/ko-b-trace-detail.png).

<a id="final-guide-closeout-20260925"></a>

## 최종 마무리: 가이드 수정 후 실행 확인 — 2026-09-25

**순서:** 영문 가이드 수정 → 국문·학습자 파일 정합 → 모든 오프라인 검사 → 소스 고정 → 영문 CLI →
국문 CLI → headless 읽기 확인·trace 대조. 고정 시각은 `2026-09-25T07:04:32Z`,
기준은 `b741473`과 작업 트리 수정이며 code hash는 `e92c1be2716a3a65608de16bd217a72439d606594ca2506910881974996b1682`입니다.
새 독립 실행 복사본에서 기존 실습 소유 prefix와 원래 ledger를 재사용했습니다. 원본 `.env`와 Azure CLI 기본 구독은 바꾸지 않았습니다.
준비된 환경의 확인이지 새 학습자 설치·리소스 생성·배포 실행은 아닙니다.

| 항목 | 영문·국문 새 결과 |
|---|---|
| Lab 00/02 사전 확인 | 정확한 `gpt-6-sol` / `2026-09-22`, `Succeeded`. 사전 확인만으로 추론 성공을 주장하지 않음 |
| Lab 02 | 실제 모델 응답과 로컬 근거 구조화 답변. 현행 150000원 한도와 실제 인용 확인 |
| Lab 03 B | 기존 `mfv2-a2-0f01-<language>-policy-sdk` 버전 1을 언어별 한 번 호출. 저장 지침이 현재 CLI 정의와 일치하며 생성은 반복하지 않음 |
| Lab 04 | 도구 없음·함수·로컬 MCP 명령 완료. 한도 초과 승인과 과거 120000원 답변 확인. 설정된 도구 표시만으로 실제 tool-event trace를 캡처한 것은 아님 |
| Lab 05 B | 순차/병렬/Group Chat 출력 1/4/4개. 외부 동작 없이 사람 검토 대기 |
| Lab 05 A 기본 터미널 | 정확한 170000원 질문을 언어별 한 번 실행. 최종 문장 두 개 모두 150000원·예약 전 승인·`TRAVEL-2026` + `APPROVAL-01` 포함 |
| Lab 06 | 기존 local/Search/GA IQ 근거는 언어별 6/6/4건. 실제 본문이 합성 원문과 일치. IQ 반환 필드는 `id`, `title`, `content`였고 별도 날짜 필드를 만들어 넣지 않음 |
| Lab 06 답변 | 새 IQ 근거 답변은 `needs_approval`, 150000원, 필수 ID 두 개. 각 언어에서 재검색 hash가 앞선 IQ 조회와 같음 |
| Lab 08 | 로컬 패키징 명령 두 개 완료. 두 manifest의 `cloud_deployed: false` 유지 |
| Lab 09 | 새 영문·국문 SDK response ID가 포털 trace·input/output token과 일치. 정리 목록은 보존한 로컬 ledger만 읽고 아무것도 삭제하지 않음 |
| Lab 07/10/11 경계 | 새 수집·judge·인수 없음. 이전 평가 이력 보존, 외부 IQ는 설계만, 새 출력·패키지·trace 인계 근거 확인 |

**개수:** 가이드 CLI 명령 32개 모두 종료 코드 0, 별도 로컬 패키징 명령 2개, 새 JSON 출력 28개입니다.
이는 **실제 내부 모델 호출 수가 아니라 명령 수**입니다. MAF workflow·도구·변경하지 않은 SDK 재시도 정책에 따라
더 많은 호출이 생길 수 있습니다. 검증 드라이버의 재시도, 대체 모델·endpoint/provider·fixture 사용은 없었습니다.
A 인라인 agent는 저장 버전 2와 정확한 지침 hash를 읽기 확인했으며 앞선 6문항 브라우저 평가를 반복하지 않았습니다.
이번 포털 읽기 확인은 영문 UI에서 두 agent 언어를 확인한 것이며 새 국문 UI 녹화로 바꾸어 적지 않습니다.

| 새 관리형 agent 호출 | Response ID | 서버 trace ID | Input / output token |
|---|---|---|---|
| 영문 버전 1 | `resp_0131ce4e1fd7c0f2016ab61dcaebb88194acd3fea76cd13212` | `bd829da0e764532e45c5cc134b1585ac` | 1124 / 113 |
| 국문 버전 1 | `resp_07b8501455f6649a016ab61e946b588195ae3734eb853b81e1` | `4d5f22d02ca12433bbdd18c8f8203d51` | 1290 / 114 |

**보존한 실패와 검토 사항:** 별도 Foundry MCP `agent_get` 조회는 설정된 ID에 `agents/read` 권한이 없어 **403**을 반환했습니다.
역할을 추가하거나 성공으로 표시하지 않았습니다. 가이드에서 미리 선택한 구독 고정 CLI와 인증된 headless 포털은 별도로 확인했습니다.
국문 concurrent의 출력 인덱스 2에는 금액·승인 조건이 있지만 정책 ID가 없습니다.
집계에 다른 참가자의 인용이 있다고 그 개별 답변을 고친 것으로 처리하지 않습니다. 원본 JSON을 그대로 보존했습니다.
이 관찰을 개선하려고 prompt·corpus·dataset·기준을 조정하지 않았습니다.

**새로 실행하지 않은 것:** agent 생성/저장, Search seed, v1/v2 dev/holdout 수집, cloud judge, 로컬/원격 Hosted 서버,
원격 A Hosted Responses 방식, 별도 게이트가 있는 확장 모듈입니다. 이전 6/6·6/6·4/4는 이 code hash의 새 인수가 아닙니다.
기능 정보 로드 후 File Search는 계속 비활성화됐으며, 처음 잠깐 활성화된 것처럼 보인 버튼을 지원으로 세지 않았습니다.
회사/Microsoft 365 데이터, 역할·기본 구독 변경, 게시·push·클라우드 삭제도 없습니다.
실제 참가자 계정 준비와 학습자 수업시간 검증은 담당자·시범 운영의 몫이며 운영자 실행 성공으로 주장하지 않습니다.

[결과와 원본 출력 hash](../assets/final-guide-closeout-20260925/results.json) ·
[랩·확장 항목별 상태](../assets/final-guide-closeout-20260925/module-checks.csv) ·
[문서 쌍 검사](../assets/final-guide-closeout-20260925/document-checks.json) ·
[가이드 수정과 로컬 검증](reference/validation.md#final-guide-closeout-20260925).

## gpt-6-sol로 실행하지 않은 것

- Lab 03 포털 File Search(9월 25일 headless 확인에서 선택 모델의 업로드 비활성화 확인)
- Lab 06 IQ Chat preset(gpt-5.6-luna)과 하이브리드 RAG
- Lab 07 feedback/regression 단계(baseline 실패 없음, 대신 근거 없음 진단 실행)
- Lab 07 Hosted 모델 matrix
- Lab 08 기본 로컬 서버, `azd ai agent invoke --local`, 학습자 본인의 Hosted 배포(위의 승인된 CI 릴리스는 별도 Hosted agent를 배포했고, 검토 반영 확인에서 6절 workflow 서버가 `curl` 요청 하나에 답변)
- Lab 09 Hosted agent의 서버 측 tracing 확인
- Lab 10 외부 IQ 확장
- 대화 평가, Agent Optimizer, 안전 제어의 red-team 단계, 릴리스 운영, 검토 반영의 A2A와 Insights 확인, 2026-09-25의 Memory·routine·Toolbox 탐색 확인을 제외한 확장 모듈

이전 `gpt-5.6-luna` 녹화와 결과 페이지(2026-09-15~17)는 작업 트리에서 삭제했습니다. git 기록에만 남아 있으며 이 preset의 결과가 아닙니다.

[영상](video-summary.md) · [액션과 화면](action-captures.md) · [챕터](video-chapters.md) · **실제 결과** · [모델 선택](reference/model-choice.md)
