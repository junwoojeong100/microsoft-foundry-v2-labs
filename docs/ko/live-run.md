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

## gpt-6-sol로 실행하지 않은 것

- Lab 03 포털 File Search
- Lab 06 IQ Chat preset(gpt-5.6-luna)과 하이브리드 RAG
- Lab 07 feedback/regression 단계(baseline 실패 없음, 대신 근거 없음 진단 실행)
- Lab 07 Hosted 모델 matrix
- Lab 08 로컬 서버와 학습자 본인의 Hosted 배포(위의 승인된 CI 릴리스는 별도 Hosted agent를 배포)
- Lab 09 Hosted agent의 서버 측 tracing 확인
- Lab 10 외부 IQ 확장
- 대화 평가, Agent Optimizer, 안전 제어의 red-team 단계, 릴리스 운영을 제외한 확장 모듈

이전 `gpt-5.6-luna` 녹화와 결과 페이지(2026-09-15~17)는 작업 트리에서 삭제했습니다. git 기록에만 남아 있으며 이 preset의 결과가 아닙니다.

[영상](video-summary.md) · [액션과 화면](action-captures.md) · [챕터](video-chapters.md) · **실제 결과** · [모델 선택](reference/model-choice.md)
