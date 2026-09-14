# Lab 07. 평가하고, 실패에서 배우고, 다시 확인하기

**완료 목표:** “답변이 좋아 보인다” 대신 같은 업무 기준과 실행 이력으로 개선을 판단합니다.

이전: [Lab 06](06-knowledge.md) · 다음: A는 [Lab 09](09-operations.md), B는 [Lab 08](08-hosted.md)

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

## A. 브라우저 — 6문항의 실제 답변을 직접 평가

1. `data/evaluation/dev.jsonl`의 질문 6개를 편집기로 엽니다. holdout은 아직 열지 않습니다.
2. [Lab 03](03-prompt-agent.md)의 에이전트에 질문마다 **새 대화**로 요청합니다.
3. 아래 표에 실제 답변의 판단·금액·근거와 실패 이유를 기록합니다.
4. 지침에서 빠진 조건 하나를 고치고, 같은 6문항을 다시 질문합니다.
5. 전후의 모든 결과를 남깁니다. 성공한 질문만 골라 표에 넣지 않습니다.

모든 사례가 통과하고 빠진 조건이 없다면 그 사실을 기록합니다.
실패를 만들거나 불필요한 지침 변경을 강요하지 않습니다. 코드 경로의 고정 v1/v2 비교는 별도로 확인할 수 있습니다.

| ID | 업무 기준 | 실제 응답/문서 ID | 통과 여부·실패 이유 |
|---|---|---|---|
| D01 | 현행 숙박 150000원 / 현행 규정 | 직접 기록 | 직접 기록 |
| D02 | 과거 숙박 120000원 / 과거 규정 | 직접 기록 | 직접 기록 |
| D03 | 초과 → 사전 승인 / 현행+승인 규정 | 직접 기록 | 직접 기록 |
| D04 | 식비 1일 30000원 / 식비 규정 | 직접 기록 | 직접 기록 |
| D05 | 해외 규정 없음 → 보류 | 직접 기록 | 직접 기록 |
| D06 | 규정 무시 요구에도 승인 불가 | 직접 기록 | 직접 기록 |

이 표는 **실제 응답에 대한 수동 업무 평가**입니다.
포털의 Foundry Evaluation을 실행한 결과로 표현하지 않습니다.
포털 batch 평가가 준비된 수업에서는 강사가 evaluator·judge·데이터 매핑·비용을
확인한 뒤 같은 데이터를 사용해 별도 실행합니다.

![D03의 실제 포털 답변에서 금액과 승인 경계 확인](../assets/live-20260914-action/shots/portal-0299-P07-001-d03-send-screen-change.webp)

**화면 확인:** D03 행에는 실제 답변의 150,000원 한도, 예약 전 승인 조건, 문서 ID를 기록합니다.
사진처럼 답했다고 가정해서 표를 채우지 말고 본인 응답을 읽어 판정하세요.

![D05의 실제 해외 규정 보류 답변](../assets/live-20260914-action/shots/portal-0336-P07-001-d05-send-ready.webp)

**화면 확인:** D05는 금액을 주지 않았다는 이유만으로 업무 실패가 되지 않습니다.
제공된 자료에 해외 규정이 없는지, 추측을 멈추고 확인 경로를 안내했는지 평가합니다.

## B. 코드 — 재현 가능한 실행 단위

여기부터는 실제 Azure 모델 호출입니다. 기본 예시는 Search를 만들지 않은 사람도
완료할 수 있도록 `--retrieval local`을 사용합니다.
IQ를 평가하려면 **세 실행 모두** `--retrieval iq`로 바꿉니다.
서로 다른 검색 방식을 같은 단일변수 실험으로 비교하지 않습니다.
프로그램은 프로젝트·출력 한도·Search endpoint/index/source/base 설정도 고정해 비교합니다.
`corpus_hash`는 로컬 합성 원본의 hash이지 원격 index의 불변성을 증명하는 값은 아닙니다.
실험 중 원격 자료를 수정하지 말고, 실제 반환된 근거와 `context_hash`도 함께 확인합니다.

### 1. dev baseline 수집

```bash
python scripts/workshop.py collect --split dev --label baseline --prompt v1 --retrieval local
python scripts/workshop.py evaluate --label baseline
```

`evaluate`의 종료 코드 `1`은 업무 게이트 불합격입니다. 파일을 열고 실패 항목을 확인합니다.
수집 중 오류가 난 행도 6문항의 분모에 남습니다. 누락/중복/다른 질문이 있으면 평가를 거부합니다.
**v1이 반드시 실패한다고 보장하지 않습니다.** 결과를 만들기 위해 실제 모델 답변을 고치지 않습니다.

![baseline 업무 검사에서 사례별 체크를 읽는 화면](../assets/live-20260914-action/shots/cli-1-0494-07-004-evaluate-baseline-result.webp)

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

실패 case가 D03이라고 가정한 예입니다. 실제 실패 ID와 실제 이유를 사용합니다.

```bash
python scripts/workshop.py feedback --label baseline --case D03 --reason "실제 응답의 승인 조건과 인용을 원문 규정과 대조하고 누락 원인을 검토합니다."
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

![같은 데이터로 비교할 v1과 v2 지침의 차이](../assets/live-20260914-action/shots/cli-1-0509-07-006-compare-prompts-result.webp)

**화면 확인:** 추가·변경된 지침을 보고 어떤 누락을 막으려는지 설명합니다.
이것은 텍스트 차이이며 평가 점수 자체가 아닙니다. 촬영에서 비교한 두 고정 지침도 성능 우위를 보장하지 않습니다.

```bash
python scripts/workshop.py collect --split dev --label candidate --prompt v2 --retrieval local
python scripts/workshop.py evaluate --label candidate
python scripts/workshop.py compare --baseline baseline --candidate candidate --variable prompt
```

JSONL의 응답이나 평가 점수를 직접 수정하지 않습니다.
지침·코드를 바꾸었다면 새로운 label로 다시 수집합니다.
명령은 기존 label을 덮어쓰지 않으며, 입력/응답 hash가 달라지면 비교를 거부합니다.

![candidate의 사례별 업무 검사 결과](../assets/live-20260914-action/shots/cli-1-0520-07-008-evaluate-candidate-result.webp)

**화면 확인:** candidate도 baseline과 같은 항목으로 검사합니다.
마지막 몇 행만 보고 전부 통과했다고 하지 말고 `business-evaluation.json` 전체를 확인합니다.

![비교 명령이 확인한 고정 변수와 context 변경 수](../assets/live-20260914-action/shots/cli-1-0525-07-009-compare-dev-result.webp)

**화면 확인:** `variable: prompt`, `changed_context_count`, `unchanged_config`를 읽습니다.
촬영의 두 업무 점수는 모두 6/6입니다. 같아진 점수나 짧은 실행 시간만으로 v2의 우월성을 주장하지 않습니다.

### 4. 선택: Foundry cloud judge

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

![Foundry native 평가의 실제 전체 지표와 상세 표](../assets/live-20260914-action/shots/portal-0476-P07-020-native-report-screen-change.webp)

**화면 확인:** **Run details**와 **Overall metric results**에서 어떤 run과 evaluator를 보고 있는지 확인합니다.
아래 상세 표의 각 사례와 실패 이유까지 읽어야 하며 업무 검사 6/6과 같은 점수가 아닙니다.

![Native judge의 12개 평가 항목과 D05 실패 이유를 확인](../assets/live-20260914-action/shots/cli-1-0683-07-010b-native-results-result.webp)

**화면 확인:** 촬영의 원시 결과를 정리한 표에서 groundedness 6/6, relevance 5/6과 **D05 2점**을 확인합니다.
기본 relevance가 올바른 보류를 낮게 평가한 이유를 검토하되 점수는 바꾸지 않습니다.
이 화면의 `RUN_TOOLS` 명령은 강사용 요약 도구이며 참가자는 자신의 native 결과 파일을 읽습니다.

`data/evaluation/calibration.jsonl`에는 명시적으로 맞는 답/틀린 답 두 개가 있습니다.
실제 운영 전에 이런 예를 포털 또는 별도 evaluator 실험으로 평가해 judge의 판별 능력을
확인합니다. 이 두 고정 예제를 target 모델이 생성한 응답으로 집계하지 않습니다.
두 예만 통과해도 judge 전체가 신뢰할 만하다는 뜻은 아닙니다.

### 5. 후보를 고정한 뒤 holdout 한 번

후보의 지침·모델·검색 설정을 더 이상 고치지 않을 때 진행합니다.
`--candidate`는 어떤 dev 후보를 고정했는지 연결합니다.

```bash
python scripts/workshop.py collect --split holdout --label final-holdout --prompt v2 --retrieval local --candidate candidate --unlock-holdout
python scripts/workshop.py evaluate --label final-holdout
python scripts/workshop.py accept --candidate candidate --holdout final-holdout
```

holdout은 4건입니다. 실패를 보고 지침을 고치면 그 holdout은 더 이상 미사용 검증셋이
아닙니다. 새로운 holdout을 준비하기 전까지 최종 합격이라고 하지 않습니다.
저장소 파일 분리는 교육적 절차이지 접근 통제나 데이터 비밀화를 보장하는 장치가 아닙니다.

![고정 후보와 연결한 교육용 holdout의 마지막 사례 검사](../assets/live-20260914-action/shots/cli-2-0843-07-013-evaluate-holdout-result.webp)

**화면 확인:** 후보를 고정한 뒤 전체 4개 사례를 검사하고 후보와의 연결을 확인합니다.
사진의 마지막 H03/H04만 확인하는 것으로 끝내지 않습니다.
촬영의 4/4는 이미 사용된 교육용 세트의 인수 절차 예시이며, 새로운 미사용 holdout 합격 증거가 아닙니다.

### 6. 모델 교체 실험 — 별도 실험으로

`.env`에서 **검증된 다른 배포 이름만** 바꾸고 지침·코드·검색·dev를 고정합니다.

```bash
python scripts/workshop.py collect --split dev --label model-b --prompt v2 --retrieval local
python scripts/workshop.py compare --baseline candidate --candidate model-b --variable model
```

검색 근거가 달라졌다면 모델만의 순위가 아니라 end-to-end 결과로 해석합니다.
작은 6문항/4문항은 교육용 게이트이며 통계적 우월성·운영 SLA의 증거가 아닙니다.

## 완료 기준

2026-09-14 새 실행은 같은 업무 검사에서 v1 6/6, v2 6/6을 기록했습니다.
이미 사용된 교육용 holdout의 마지막 인수 절차도 4/4였으나 새로운 미사용 검증셋으로 주장하지 않습니다.
이 작은 집합에서는 v2의 우월성을 주장하지 않습니다.
숫자는 이번 작은 합성 사례의 결과이지 일반적인 성능 보장이 아닙니다.
데이터·실패 원인·분리된 평가 경로는 [실행 기록](../live-run.md)을 확인합니다.

실제 baseline/candidate 이력, 실패 검토 또는 전부 통과했다는 기록, 고정 후보의 holdout
결과와 사람의 판단이 남습니다. `accept`는 인수 자료를 만들며 **자동 배포/운영 승인을 하지 않습니다.**
업무 검사의 100% 통과가 답변 전체의 의미적 정확성·보안·법적 적합성을 보장하지 않습니다.
