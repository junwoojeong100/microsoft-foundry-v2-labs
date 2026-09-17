# Lab 07. 평가하고, 실패에서 배우고, 다시 확인하기

[English](../../labs/07-evaluation.md) | **한국어**

**완료 목표:** “답변이 좋아 보인다” 대신 같은 업무 기준과 실행 이력으로 개선을 판단합니다.

**내 구간 바로 열기:** [A — 수동 평가](#path-a) · [B — 코드 실험 네 단계](#path-b) · [학습 경로](../paths.md)

> **2026-09-15 한국어 개정:** 아래 A/B는 기존 입문 평가를 유지합니다.
> 원본 평가 실습을 대체하는 심화 경로는 [Hosted 워크플로 평가 워크북](../reference/evaluation-workbook.md)입니다.
> 새 국문 촬영은 실제 Hosted workflow의 24/24/16행과 native 평가·trace를 포함합니다.
> 아래 입문 B의 단일 모델 예제와 심화 C의 다중 모델 실측은 구분합니다.

## 시작 전

**이번 순서:** A는 질문 전용 파일·빈 평가표, B는 6문항 dev 비교를 사용합니다. cloud judge/matrix는 선택입니다.

**준비물:** A: Lab 03에서 저장한 agent와 학습자 ZIP. B: 동작하는 코드 환경과 새 label.

**다음으로 갈 기준:** A는 실제 응답 6개와 검토를 저장합니다. B는 baseline/candidate·게이트 이후 최종 holdout·인수/반려 보고서를 보관하거나 빠진 단계를 미완료로 인계합니다.

**막히면:** 정답 JSON을 agent에 붙여 넣지 않습니다. Dev 실패를 고치려고 holdout을 열지 않습니다.

[한 번만 하는 준비와 학습자 파일](../setup.md).

## 무엇이 조직의 자산으로 남는가?

```mermaid
flowchart LR
    K["지식·업무 기준"] --> B["dev baseline"]
    B --> F["실패 응답·원문·request/trace 연결"]
    F --> H["사람이 원인과 개선 이유 검토"]
    H --> P["새 지침"]
    P --> C["같은 dev 재평가"]
    C --> T["고정 후보 + 미사용 holdout"]
    T --> G["사람의 채택/반려"]
    G --> O["운영 관찰"]
    O --> F
```

로그를 모은다고 모델 가중치가 자동 학습되지 않습니다.
이번 실습의 learning loop는 **지식·지침·평가·사람의 판단을 개선하는 과정**입니다.

<a id="path-a"></a>

## A. 브라우저 — 6문항의 실제 답변을 직접 평가

1. ZIP의 **`dev-questions.txt`**를 열고 **`assessment.csv`**를 `assessment-baseline.csv`로 복사해 저장합니다.
   저장소의 생성 파일 `data/learner/`가 아니라 본인 증거 폴더에서 작업합니다. Holdout은 열지 않습니다.
2. [Lab 03](03-prompt-agent.md)의 agent 이름/버전을 기록합니다. **New chat**마다 **질문 텍스트 하나만** 보냅니다.
   ID·정답·평가 열은 보내지 않습니다.
3. 6개 행을 모두 채웁니다. `actual_answer`는 실제 응답, `actual_document_ids`는 실제 인용,
   `pass_or_fail`은 통과/실패, `review_note`는 판단 이유입니다.
4. 검토에서 지침 누락을 찾았다면 원래 지침·평가표를 보존하고 그 조건을 고친 뒤 **Save**하여 새 버전을 기록합니다.
5. 같은 6문항을 새 대화로 다시 묻고 `assessment-candidate.csv`에 저장합니다.
   두 버전과 모든 실패를 남깁니다. 정당한 변경 이유가 없으면 전부 통과했다는 검토로 대신합니다.

모든 사례가 통과하고 빠진 조건이 없다면 그 사실을 기록합니다.
실패를 만들거나 불필요한 지침 변경을 강요하지 않습니다. 코드 경로의 고정 v1/v2 비교는 별도로 확인할 수 있습니다.

| ID | 업무 기준 | 실제 응답/문서 ID | 통과 여부·실패 이유 |
|---|---|---|---|
| D01 | 현행 숙박 150000원 / 현행 규정 | 직접 기록 | 직접 기록 |
| D02 | 과거 숙박 120000원 / 과거 규정 | 직접 기록 | 직접 기록 |
| D03 | 초과 → 사전 승인 / 현행+승인 규정 | 직접 기록 | 직접 기록 |
| D04 | 식비 1일 30000원 / 식비 규정 | 직접 기록 | 직접 기록 |
| D05 | 해외 규정 없음 → 보류, `SCOPE-01` 인용 | 직접 기록 | 직접 기록 |
| D06 | 규정 무시 요구에도 승인 불가 | 직접 기록 | 직접 기록 |

이 표는 **실제 응답에 대한 수동 업무 평가**입니다.
포털의 Foundry Evaluation을 실행한 결과로 표현하지 않습니다.
포털 batch 평가가 준비된 수업에서는 강사가 evaluator·judge·데이터 매핑·비용을
확인한 뒤 같은 데이터를 사용해 별도 실행합니다.
**A 완료:** `assessment-baseline.csv`·정당한 변경이 있었을 때의 candidate 표·실패/전체 통과 검토를 저장합니다.
[Lab 09 A](09-operations.md#path-a)로 이동합니다. 아래 명령은 별도 B 실험이지 브라우저 경로의 추가 단계가 아닙니다.

![2026-09-15 새 국문 촬영: D03 · 실제 응답과 근거 확인](../../assets/refresh-20260915-ko/screenshots/KP07-d03-send-2.webp)

**화면 확인:** D03 행에는 실제 답변의 150,000원 한도, 예약 전 승인 조건, 문서 ID를 기록합니다.
사진처럼 답했다고 가정해서 표를 채우지 말고 본인 응답을 읽어 판정하세요.

![2026-09-15 새 국문 촬영: D05 · 실제 응답과 근거 확인](../../assets/refresh-20260915-ko/screenshots/KP07-d05-send-2.webp)

**화면 확인:** D05는 금액을 주지 않았다는 이유만으로 업무 실패가 되지 않습니다.
제공된 자료에 해외 규정이 없는지, 추측을 멈추고 확인 경로를 안내했는지 평가합니다.

<a id="path-b"></a>

## B. 코드 — 재현 가능한 실행 단위

여기부터는 실제 Azure 모델 호출입니다. 기본 예시는 Search를 만들지 않은 사람도
완료할 수 있도록 `--retrieval local`을 사용합니다.
IQ를 평가하려면 **세 실행 모두** `--retrieval iq`로 바꿉니다.
서로 다른 검색 방식을 같은 단일변수 실험으로 비교하지 않습니다.
첫 회차는 `local`을 유지하고 **1 → 2 → 3 → 4**로 진행합니다.
5–6은 기본 결과 이후의 선택 확장입니다. 기본 target 요청은 **6 + 6 + 4 = 16개**이며 서비스/도구/재시도는 추가입니다.
기존 label이 있으면 새 baseline/candidate/holdout 이름 묶음을 정해 모든 참조를 함께 바꿉니다. 기존 실행을 삭제·덮어쓰지 않습니다.

| 실행 | 저장소 루트 아래 저장 위치 | 기대 사례 수 |
|---|---|---:|
| Baseline / v1 | `outputs/baseline/` | dev 6 |
| Candidate / v2 | `outputs/candidate/` | dev 6 |
| Final / 고정 v2 | `outputs/final-holdout/` | 후보 통과 후에만 holdout 4 |

**블록 하나 실행 → 결과 확인 → 다음 블록** 순서입니다. `collect`는 Azure 호출,
`evaluate`·`compare`·`feedback`·`accept`는 모델 호출 없는 로컬 근거 조회/작성입니다.
수집 오류는 파일을 보존하고 다음 수집 전에 원인을 해결합니다. 저장된 오류 확인을 위한 `evaluate`는 실행해도 됩니다.
업무 검사 실패와 요청 실패는 다릅니다.

프로그램은 프로젝트·출력 한도·Search endpoint/index/source/base 설정도 고정해 비교합니다.
`corpus_hash`는 로컬 합성 원본의 hash이지 원격 index의 불변성을 증명하는 값은 아닙니다.
실험 중 원격 자료를 수정하지 말고, 실제 반환된 근거와 `context_hash`도 함께 확인합니다.

### 1. dev baseline 수집

```bash
python scripts/workshop.py collect --split dev --label baseline --prompt v1 --retrieval local
```

`outputs/baseline/manifest.json`과 `responses.jsonl`에서 성공/오류를 포함한 6행을 보관한 뒤 로컬 평가를 실행합니다.

```bash
python scripts/workshop.py evaluate --label baseline
```

`evaluate`의 종료 코드 `1`은 업무 게이트 불합격입니다. 파일을 열고 실패 항목을 확인합니다.
수집 중 오류가 난 행도 6문항의 분모에 남습니다. 누락/중복/다른 질문이 있으면 평가를 거부합니다.
**v1이 반드시 실패한다고 보장하지 않습니다.** 결과를 만들기 위해 실제 모델 답변을 고치지 않습니다.
`business-evaluation.json`의 `total`, `passed`, `errors`, `business_gate_passed`와 모든 사례의 `checks`를 읽습니다.


**화면 확인:** `checks` 안의 `completed`, `schema`, `decision`, `required_citations`를 읽습니다.
사진은 출력의 마지막 사례들입니다. 전체 6개 행과 파일 위쪽 summary를 확인해야 누락 여부까지 판단할 수 있습니다.

### 2. 실패를 한 건 골라 원인 분리

`outputs/baseline/responses.jsonl`에서 실패 case를 찾습니다.

| 현상 | 먼저 확인할 것 |
|---|---|
| 올바른 문서가 없음 | 검색 query·index·knowledge source |
| 문서는 맞는데 날짜 적용이 틀림 | 질문 속 출장일·지침 |
| 금액은 맞는데 출처가 없음 | 인용 지침·schema·원문 ID |
| 승인됐다고 주장함 | 업무 권한 경계·도구 구현 |
| JSON/요청 오류 | 모델 지원·출력 제한·SDK·서비스 오류 |

**실제 baseline 실패가 있을 때만** 아래를 실행하고 그 case ID와 **15자 이상**의 구체적인 검토 이유를 입력합니다.
6개가 모두 통과했다면 검토 기록에 그 사실을 저장하고 3으로 이동합니다. D03 실패 기록을 억지로 만들지 않습니다.

```bash
printf 'Actual failed dev case ID: '
read -r FAILED_CASE
printf 'Your specific review reason: '
read -r REVIEW_REASON
python scripts/workshop.py feedback --label baseline --case "$FAILED_CASE" --reason "$REVIEW_REASON"
```

이 명령은 **사람의 검토 대기 기록**을 만들 뿐 승인 처리하지 않습니다.
원래 dev 정답과 source run/response/request/trace ID를 연결합니다.
모델의 답변 자체를 정답으로 승격하지 않습니다.
실제 trace가 아직 없으면 `null`로 남습니다. 임의 UUID를 Azure trace ID처럼 쓰지 않습니다.

모든 dev가 통과했다면 그 사실을 그대로 남기고, 설명 가능한 지침 개선을 비교하거나
새로운 **dev 버전**을 별도로 설계합니다. holdout을 열어 실패를 찾아 prompt를 조정하지 않습니다.

### 3. 같은 dev에 개선 지침 적용

`prompts/v1.txt`와 `prompts/v2.txt`를 비교합니다.
v2는 적용일, 증빙/승인, 문서 ID, 근거 부족 처리의 우선순위를 명확히 합니다.

![2026-09-15 새 국문 촬영: v1·v2 제공 지침의 실제 차이 읽기](../../assets/refresh-20260915-ko/screenshots/K07C-prompt-diff-2.webp)

**화면 확인:** 추가·변경된 지침을 보고 어떤 누락을 막으려는지 설명합니다.
이것은 텍스트 차이이며 평가 점수 자체가 아닙니다. 촬영에서 비교한 두 고정 지침도 성능 우위를 보장하지 않습니다.

```bash
python scripts/workshop.py collect --split dev --label candidate --prompt v2 --retrieval local
```

후보 6행 전체를 확인한 뒤 로컬 검사를 실행합니다.

```bash
python scripts/workshop.py evaluate --label candidate
python scripts/workshop.py compare --baseline baseline --candidate candidate --variable prompt
```

JSONL의 응답이나 평가 점수를 직접 수정하지 않습니다.
지침·코드를 바꾸었다면 새로운 label로 다시 수집합니다.
명령은 기존 label을 덮어쓰지 않으며, 입력/응답 hash가 달라지면 비교를 거부합니다.


**화면 확인:** candidate도 baseline과 같은 항목으로 검사합니다.
마지막 몇 행만 보고 전부 통과했다고 하지 말고 `business-evaluation.json` 전체를 확인합니다.


**화면 확인:** `outputs/candidate/comparison-vs-baseline.json`에서
`variable: prompt`, `baseline_metrics`, `candidate_metrics`, `changed_context_cases`를 읽습니다.
`changed_context_cases`가 빈 목록이면 검색 근거가 같습니다. 비교 조건이 다르면 보고서를 쓰기 전에 거부합니다.
입문 B는 실행당 6문항입니다. 새 심화 촬영의 업무 점수는 네 모델 각각 6/6, 총 24/24였습니다.
서로 다른 경로의 점수를 옮겨 쓰거나 같은 점수만으로 v2의 우월성을 주장하지 않습니다.

### 4. 후보를 고정한 뒤 holdout 한 번

**Holdout 호출 전 게이트:** `outputs/candidate/business-evaluation.json`에
`total: 6`, `passed: 6`, `errors: 0`, `business_gate_passed: true`가 있어야 하며 비교에서 고정 설정을 인정해야 합니다.
아니라면 여기서 멈추고 dev 실패·반려 후보를 보존합니다. Holdout을 열거나 검사 기준을 낮추지 않습니다.
오류 없는 수집이나 `compare` 종료 코드 `0`만으로는 이 게이트를 통과하지 않습니다.
현재 작업 시간 안에 해결할 수 없다면 holdout을 건너뛰고 **최종 평가 미완료**로 남깁니다.
로컬 [패키징](08-hosted.md#path-b)·[운영](09-operations.md#path-b)·[미완료 인계](11-capstone.md#incomplete-handoff)는 진행할 수 있지만,
어느 것도 반려된 후보를 인수 통과로 바꾸지는 않습니다.

지침·모델·검색 설정을 더 이상 고치지 않을 때 진행합니다.
`--candidate`는 어떤 dev 후보를 고정했는지 연결합니다.

```bash
python scripts/workshop.py collect --split holdout --label final-holdout --prompt v2 --retrieval local --candidate candidate --unlock-holdout
```

실패를 포함한 실제 4행을 모두 보관한 뒤 로컬 평가와 사람 검토용 보고서를 만듭니다.

```bash
python scripts/workshop.py evaluate --label final-holdout
python scripts/workshop.py accept --candidate candidate --holdout final-holdout
```

Holdout은 4건입니다. 실패를 보고 지침을 고치면 더 이상 미사용 검증셋이 아닙니다.
새 holdout 없이 최종 합격이라고 하지 않습니다. 저장소 파일 분리는 교육적 절차이지 접근 통제나 비밀 보장이 아닙니다.
`accept` 종료 코드 `1`은 업무 게이트 반려입니다. 같은 holdout이 통과할 때까지 재시도하지 않고 그 결과를 보존합니다.

**화면 확인:** 4개 사례와 후보 연결을 확인한 뒤 `outputs/final-holdout/acceptance.json`을 엽니다.
`recommendation`, `deployment_approved: false`를 유지합니다.
기존 촬영의 교육용 세트는 이미 노출된 자료이며 새로운 미사용 holdout의 증거가 아닙니다.

**B 완료:** 실행 폴더 세 개·비교·검토 기록·인수/반려 보고서를 보관합니다.
[Lab 08 B](08-hosted.md#path-b)에서 **패키징만** 진행합니다. 인수 보고서는 배포 승인이 아닙니다.

### 5. 선택: Foundry cloud judge

<details>
<summary>Judge 준비·별도 비용 승인이 있을 때만 펼칩니다. B 완료에 필수는 아닙니다</summary>

추가 비용·평가 권한·별도 judge 배포가 필요합니다.
`.env`의 `AZURE_AI_EVALUATION_MODEL_DEPLOYMENT_NAME`을 설정합니다.
다른 배포 이름이어도 같은 모델일 수 있으므로 underlying model의 편향도 기록합니다.

```bash
python scripts/workshop.py cloud-evaluate --label candidate --timeout 300 --confirm-cost
```

- 이미 수집한 응답을 평가합니다. **새 target-agent 답변을 생성하는 명령이 아닙니다.**
- 실제 evaluator catalog에서 초기화 스키마와 버전을 확인합니다.
- `groundedness`와 `relevance`의 native 결과를 업무 검사와 별도 저장합니다.
- 평가 ID, run ID, judge 설정, report URL, 모든 output page를 보존합니다.
- timeout이면 같은 label 명령으로 조회를 재개합니다. 새 job을 몰래 다시 만들지 않습니다.
- evaluator 오류/누락/중복은 좋은 점수로 바꾸지 않습니다.


**화면 확인:** **Run details**와 **Overall metric results**에서 어떤 run과 evaluator를 보고 있는지 확인합니다.
상세 표의 각 사례와 실패 이유까지 읽어야 하며 결정적 업무 검사와 같은 점수가 아닙니다.


**화면 확인:** 새 심화 촬영의 baseline은 groundedness 24/24, relevance 19/24였습니다.
실제 D05 보류 답변의 낮은 relevance 이유도 확인합니다.
기본 relevance가 올바른 보류를 낮게 평가한 이유를 검토하되 점수는 바꾸지 않습니다.
이 화면의 `RUN_TOOLS` 명령은 강사용 요약 도구이며 참가자는 자신의 native 결과 파일을 읽습니다.

`data/evaluation/calibration.jsonl`에는 명시적으로 맞는 답/틀린 답 두 개가 있습니다.
실제 운영 전에 이런 예를 포털 또는 별도 evaluator 실험으로 평가해 judge의 판별 능력을
확인합니다. 이 두 고정 예제를 target 모델이 생성한 응답으로 집계하지 않습니다.
두 예만 통과해도 judge 전체가 신뢰할 만하다는 뜻은 아닙니다.

</details>

### 6. 선택 — 모델 교체는 별도 실험으로

<details>
<summary>별도 모델 실험 펼치기 — 첫 회차에 필수는 아닙니다</summary>

`.env`에서 **검증된 다른 배포 이름만** 바꾸고 지침·코드·검색·dev를 고정합니다.

```bash
python scripts/workshop.py collect --split dev --label model-b --prompt v2 --retrieval local
python scripts/workshop.py compare --baseline candidate --candidate model-b --variable model
```

검색 근거가 달라졌다면 모델만의 순위가 아니라 end-to-end 결과로 해석합니다.
작은 6문항/4문항은 교육용 게이트이며 통계적 우월성·운영 SLA의 증거가 아닙니다.
이 새 dev 실험이 이전 holdout을 튜닝용으로 다시 열거나 교체 모델의 인수를 증명하는 것은 아닙니다.

</details>

## C. Hosted 모델 matrix와 평가자까지 검증하기

<details>
<summary>심화 C — Hosted matrix 게이트와 입문 평가 비교 펼치기</summary>

실제 배포 버전의 답을 평가하려면 [평가 워크북](../reference/evaluation-workbook.md)을 순서대로 진행합니다.
핵심 차이는 다음과 같습니다.

| 기준 | 기존 입문 B | Hosted 심화 |
|---|---|---|
| target | 프로젝트 Responses + 사전 검색 | 정확한 Hosted version의 MAF policy/workflow |
| 모델 | 실행당 한 배포 | 명시적 모델 목록 1–8개, 4개면 dev 24행 |
| 입력 | question + 근거 | query-only 요청 4필드; evaluator 라벨은 server에 전달하지 않음 |
| 업무 검사 | schema·판단·한도·인용 | 위 + 답변 본문의 한도·관련 인용, p50/p95·불확실성 |
| 회귀 | 검토 대기 기록 | 명시적 dev 검토 후 다음 matrix가 실제 소비 |
| judge | native 결과 별도 기록 | evaluator snapshot 재사용·실패 시도 보존·정답/오답 calibration |
| trace | 없는 값은 null | 실제 App Insights 조회로 모든 trace의 존재와 요청 상태 확인 |
| 인수 | 고정 candidate + holdout | 모델별 gate·native findings·회귀·calibration·trace의 묶음 |

평가기는 답을 고치지 않습니다. `benchmark report`의 HTML도 저장된 응답과 실제 점수를
표시할 뿐이며, 실패한 native 점수를 통과로 바꾸지 않습니다.
초기 baseline에 실패가 없어도 그 사실을 유지합니다.

심화의 같은 데이터 전후 비교에는 **동일한 code/corpus/model map/API/retrieval/concurrency/evaluator**가 필요합니다.
검색 근거 또는 관측 모델이 달라졌다면 순수한 prompt 개선 효과로 발표하지 않습니다.
holdout을 보고 v2를 고치거나 회귀로 가져오면 최종 검증 경계가 깨집니다.

</details>

<details>
<summary>녹화 당시 참고 화면 (선택; 그대로 재실행할 단계가 아님)</summary>

아래는 이번 국문 실행에서 새로 캡처한 화면입니다. 초기 진단·실패와 최종 비교 결과를 구분하며, 영문 촬영본을 재사용하지 않았습니다.

![2026-09-15 새 국문 촬영: 실제 모델×사례 전체 수집](../../assets/refresh-20260915-ko/screenshots/K07F-collect-2.webp)

**화면 확인:** 실제 command·언어·version·label·근거와 출력 상태를 확인합니다. 촬영 결과를 본인의 실행이나 운영 승인으로 대신하지 않습니다.

![2026-09-15 새 국문 촬영: 통제된 baseline 24행의 실제 native 결과](../../assets/refresh-20260915-ko/screenshots/KP07-030-controlled-baseline-2.webp)

**화면 확인:** 실제 command·언어·version·label·근거와 출력 상태를 확인합니다. 촬영 결과를 본인의 실행이나 운영 승인으로 대신하지 않습니다.

![2026-09-15 새 국문 촬영: v2 후보 24행의 실제 native 결과](../../assets/refresh-20260915-ko/screenshots/KP07-031-candidate-native-2.webp)

**화면 확인:** 실제 command·언어·version·label·근거와 출력 상태를 확인합니다. 촬영 결과를 본인의 실행이나 운영 승인으로 대신하지 않습니다.

![2026-09-15 새 국문 촬영: 실제 보류 응답과 relevance의 낮은 점수 확인](../../assets/refresh-20260915-ko/screenshots/KP07-014-abstention-detail-2.webp)

**화면 확인:** 실제 command·언어·version·label·근거와 출력 상태를 확인합니다. 촬영 결과를 본인의 실행이나 운영 승인으로 대신하지 않습니다.

![2026-09-15 새 국문 촬영: 정답/오답 calibration 2개: agent 응답 아님](../../assets/refresh-20260915-ko/screenshots/KP07-032-calibration-2.webp)

**화면 확인:** 실제 command·언어·version·label·근거와 출력 상태를 확인합니다. 촬영 결과를 본인의 실행이나 운영 승인으로 대신하지 않습니다.

![2026-09-15 새 국문 촬영: 동결한 후보의 최종 holdout 16행 결과](../../assets/refresh-20260915-ko/screenshots/KP07-033-holdout-native-2.webp)

**화면 확인:** 실제 command·언어·version·label·근거와 출력 상태를 확인합니다. 촬영 결과를 본인의 실행이나 운영 승인으로 대신하지 않습니다.

[새 영상과 액션 인덱스](../video-summary.md) · [실제 결과·계보](../live-run.md)

</details>

## 완료 기준

2026-09-15 새 국문 실행은 네 모델의 baseline 24/24, candidate 24/24, holdout 16/16 업무 통과를 기록했습니다.
Native groundedness는 각각 24/24, 22/24, 16/16이고 relevance는 19/24, 20/24, 13/16입니다.
판단 결과는 `review-native-findings`이며 v2의 일괄적 우월성이나 운영 승인을 주장하지 않습니다.
숫자는 이번 작은 합성 사례의 결과이지 일반적인 성능 보장이 아닙니다.
데이터·실패 원인·분리된 평가 경로는 [실행 기록](../live-run.md)을 확인합니다.

A: 6문항 평가표·실제 agent 버전/지침·실패 또는 전부 통과 검토가 남습니다. Holdout·CLI 인수는 필요 없습니다.
B: 실제 baseline/candidate 이력, 실패 검토 또는 전부 통과했다는 기록, 고정 후보의 holdout
결과와 사람의 판단이 남습니다. `accept`는 인수 자료를 만들며 **자동 배포/운영 승인을 하지 않습니다.**
업무 검사의 100% 통과가 답변 전체의 의미적 정확성·보안·법적 적합성을 보장하지 않습니다.

다음: A → [Lab 09](09-operations.md#path-a) · B → [Lab 08](08-hosted.md#path-b)
