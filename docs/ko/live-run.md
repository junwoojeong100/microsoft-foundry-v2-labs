# gpt-6-sol 실제 실행·평가 결과 — 2026-09-23

[English](../live-run.md) | **한국어**

**2026-09-23 국문 녹화의 실제 Azure 실행 결과입니다.** 영문 실행, 이전 `gpt-5.6-luna` 판, 원본 저장소의 결과를 복사하지 않았습니다.

## 환경

| 항목 | 값 |
|---|---|
| 리전 / 프로젝트 | Sweden Central / `mfv2-g6luna-20260923` |
| 응답 배포 | `gpt-6-sol` → `gpt-6-sol` `2026-09-22`, DataZoneStandard 150K TPM, NoAutoUpgrade |
| 평가 배포 | `gpt-6-sol-judge` → `gpt-6-sol` `2026-09-22`, DataZoneStandard 100K TPM |
| 포털이 만든 배포 | `text-embedding-3-large` Standard 110K — 첫 포털 agent를 열 때 자동 생성; 이 실습에서는 사용하지 않음 |
| 소유 prefix | `mfv2-sol-20260923-ko` |

리소스 이름에는 환경을 처음 만들 때의 `g6luna`가 남아 있지만 녹화에 사용한 배포는 `gpt-6-sol`입니다. 로컬 키는 비활성화했으며 모든 호출은 Microsoft Entra ID를 사용했습니다.

## Lab 07 업무 기준 평가

| Cohort | Split | 지침 | 행 | 오류 | 업무 기준 | 지연 중앙값 |
|---|---|---|---:|---:|---:|---:|
| baseline | dev | v1 | 6 | 0 | 6/6 | 3.00 s |
| candidate | dev | v2 | 6 | 0 | 6/6 | 2.67 s |
| final-holdout | holdout | v2 (고정) | 4 | 0 | 4/4 | 2.86 s |

- 실제 baseline에 실패 사례가 없어 feedback/regression 단계는 **실행하지 않았습니다.** 전 문항 통과는 그대로 기록하며 v2가 더 낫다는 증거로 쓰지 않습니다.
- holdout 한 번 실행 전에 후보를 고정했으며 holdout을 지침 개발에 쓰지 않았습니다.
- 인수 판단: `ready-for-human-review`, `deployment_approved: false`. 작은 공개 합성 데이터이며 운영 검증이 아닙니다.

## 선택 Foundry cloud judge

candidate dev 6행을 `gpt-6-sol-judge`로 평가했습니다. evaluation `eval_dcf423a3bfc543b4be4302bd768bdbc0`, run `evalrun_4867d27cfee6416d85fd8205b07ebefc`, 상태 `completed`.

| Evaluator | 통과 | 실패 | 오류 |
|---|---:|---:|---:|
| groundedness | 6 | 0 | 0 |
| relevance | 5 | 1 | 0 |

relevance 실패 행은 의도한 보류 사례인 **D05**(점수 2)입니다. 해외 규정이 없으므로 금액을 주지 않은 답변이 맞습니다. 올바른 보류에 낮은 relevance가 나온 것은 검토할 judge의 한계이며 금액을 지어낼 이유가 아닙니다. 점수는 바꾸지 않았고 native judge 점수는 인수 판단에 포함하지 않습니다.

## 그 밖의 실제 결과

- **Lab 02:** 첫 SDK 요청은 `response_model: gpt-6-sol`, 검증된 구조화 답변은 `TRAVEL-2026`, `RECEIPT-01`, `APPROVAL-01`을 인용했습니다.
- **Lab 03:** 포털 agent `mfv2-sol-20260923-ko-policy`는 버전 2로 저장했고 답변은 화면으로만 기록했습니다(점수 아님). SDK agent `mfv2-sol-20260923-ko-policy-sdk` 버전 1을 생성·호출했습니다.
- **Lab 04–05:** `tools: none`·`function`·`local-mcp` MAF 실행과 sequential·concurrent·group-chat workflow가 모두 종료 코드 0으로 끝났습니다.
- **Lab 06:** 합성 정책 6개로 로컬·Search·GA IQ 검색을 실행했습니다. IQ 근거 답변은 `APPROVAL-01`, `RECEIPT-01`, `TRAVEL-2025`, `TRAVEL-2026`을 검색해 `TRAVEL-2026`, `APPROVAL-01`, `RECEIPT-01`을 인용했습니다(`needs_approval`, 150,000원).
- **Lab 08–09:** 패키징만(Hosted 배포 없음), 정리 목록만(삭제 없음) 실행했습니다.

## 계보

- base commit `47f3b492d5146d8050faf303b4060db2dfc75185`, 작업 트리 source hash `40e47905763c482d964e49d3925322df4f9d9f7700833686b653379e9d513b99`
- `baseline` run `9e580bed-b058-4aaf-a18c-175eb09b6b2d`: dataset `84e2b286e92e73f3…`, corpus `3556faa7cb0099cf…`, code `466558728a75693c…`, prompt `fb6e5f43288e2aa5…`, responses `7db267763206633a…`
- `candidate` run `edfc93ff-e95e-4923-9f8a-82cb8d710699`: dataset `84e2b286e92e73f3…`, corpus `3556faa7cb0099cf…`, code `466558728a75693c…`, prompt `2b4a2b5e322a8534…`, responses `3d16a909e84f16e6…`
- `final-holdout` run `dd5125d8-5427-4aaf-9ea5-bae14cac2e82`: dataset `9d478d727527064c…`, corpus `3556faa7cb0099cf…`, code `466558728a75693c…`, prompt `2b4a2b5e322a8534…`, responses `d3cb72bb228d96af…`
- cloud judge: input `13c236a677a9c5fa…`, evaluator `a0e7f44a59d34f75…`, results `7f24c791f13c23dc…`

전체 hash는 [live-results.json](../assets/g6sol-20260923-ko/live-results.json)에 있습니다.

## 선택 평가 추가분 — 별도 검증, 2026-09-23

녹화 이후 추가한 선택 평가 단계를 확인한 실행입니다. 같은 소스(code hash `b160d84d2e0e1087…`)의 별도 복사본에서 새 label로,
같은 `gpt-6-sol` / `gpt-6-sol-judge` 배포와 prefix `mfv2-sol-20260923-ko`를 사용했습니다.
편집 영상에는 포함되지 않으며 포털 단계는 별도 [캡처](../assets/eval-portal-20260923/captures.json)로 남겼습니다.

| 단계 | 결과 |
|---|---|
| Lab 07 A 선택 포털 평가(`eval_b69ed3d1…`, `dev-questions.jsonl`의 6문항) | Coherence 6/6, Relevance 5/6(D05), TaskAdherence(Preview) 0/6. 같은 에이전트의 직접 업무 평가는 6/6 |
| Lab 07 B dev 수집(`baseline` `9ea18c52…`, `candidate` `9ed0ca38…`) | 업무 기준 6/6, 6/6, 오류 0 |
| Lab 07 B 근거 없음 진단(`diagnostic-no-evidence` `1e85d477…`) | 업무 기준 0/6, 오류 0. 모든 답변이 보류(`insufficient_evidence`). `feedback`은 이 실행을 거부 |
| Lab 07 B 업무 기준을 포함한 cloud judge(`eval_910a4729…`, 실행 2개) | baseline·candidate 모두 groundedness 6/6, relevance 5/6, `business_rubric` 6/6. 로컬 검사와 일치 6/6. 포털 비교 relevance 3.83 → 4.50, **샘플이 너무 적음** |
| Lab 04 선택 `maf-evaluate`(`eval_e3d8fa2f…`) | tool_call_accuracy 6/6, relevance 5/6(D05). 질문마다 `lookup_policy` 호출 1회 |

사용자 지정 평가자 `mfv2_sol_20260923_ko_business_rubric`은 버전 1입니다.
한국어 포털에서는 관련성·일관성 평가자의 기본 이름이 이름 검사를 통과하지 못해 `Relevance`, `Coherence`로 바꾼 뒤 제출했습니다.
TaskAdherence 실패 이유는 인용 금액을 검증할 수 없다는 것이었으며, 평가자에게 질문과 답변만 전달되기 때문입니다.
기존 추적 평가는 Application Insights의 모니터링 읽기 권한자 역할이 필요하다는 안내가 표시되었고 역할을 할당하지 않아 실행하지 않았습니다.

**코드 검토 후 재확인(code `408b1b57…`):** 결과 매핑을 다시 작성한 `maf-evaluate`를 다시 실행했습니다(`eval_e330c6aa…`).
tool_call_accuracy 6/6, relevance 6/6이며 모든 출력 항목이 해당 질문과 연결되었습니다.
근거 없음 진단의 cloud judge(`eval_910a4729…`의 실행 `evalrun_1e0790d4…`)는 완료되었지만, context가 비어 있어 Groundedness가
6행 중 4행을 건너뛰었습니다. 서비스는 relevance 0/6, `business_rubric` 0/6을 보고했지만 워크숍은 결과를 무효로 표시하고
아무것도 집계하지 않았습니다. 최종 코드(`67e7ac04…`)는 이런 실행을 클라우드 호출 전에 거부하며, 같은 label에서 확인했습니다.

## gpt-6-sol로 실행하지 않은 것

- Lab 03 포털 File Search
- Lab 06 IQ Chat preset(gpt-5.6-luna)과 하이브리드 RAG
- Lab 07 feedback/regression 단계(baseline 실패 없음. 별도 근거 없음 진단은 설계상 거부)
- Lab 07 Hosted 모델 matrix
- Lab 08 로컬 서버와 Hosted 배포
- Lab 09 서버 측 tracing 확인, 기존 추적 평가, continuous evaluation
- Lab 10 외부 IQ 확장
- 확장 모듈

이전 `gpt-5.6-luna` 녹화와 결과 페이지(2026-09-15~17)는 작업 트리에서 삭제했습니다. git 기록에만 남아 있으며 이 preset의 결과가 아닙니다.

[영상](video-summary.md) · [액션과 화면](action-captures.md) · [챕터](video-chapters.md) · [실제 결과](live-run.md) · [모델 선택](reference/model-choice.md)
