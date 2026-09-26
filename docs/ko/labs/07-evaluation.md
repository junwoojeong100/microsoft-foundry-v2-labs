# Lab 07. 평가하고, 실패에서 배우고, 다시 확인하기

[English](../../labs/07-evaluation.md) | **한국어**

**완료 목표:** “답변이 좋아 보인다” 대신 같은 업무 기준과 실행 이력으로 개선을 판단합니다.

**내 구간 바로 열기:** [A — 수동 평가](#path-a) · [B — 코드 실험 네 단계](#path-b) · [학습 경로](../paths.md)

## 시작 전

**이번 순서:** A는 질문 전용 파일·빈 평가표, B는 6문항 dev 비교를 사용합니다. A의 포털 평가, B의 cloud judge, matrix는 선택입니다.

**준비물:** A: Lab 03에서 저장한 agent, 학습자 ZIP, [준비한 로컬 스프레드시트 편집기](../setup.md#local-tools). B: 동작하는 코드 환경. 새 실험이면 새 label, 재개라면 원래 label과 기존 파일을 사용합니다.

**다음으로 갈 기준:** A는 실제 응답 6개·해당 agent 저장 버전·검토를 기록합니다. B는 baseline/candidate·게이트 이후 최종 holdout·인수/반려 보고서를 보관하거나 빠진 단계를 미완료로 인계합니다.

**막히면:** 정답 JSON을 agent에 붙여 넣지 않습니다. Dev 실패를 고치려고 holdout을 열지 않습니다.

[한 번만 하는 준비와 학습자 파일](../setup.md).

## 무엇이 조직의 자산으로 남는가?

```mermaid
flowchart LR
    K["지식·업무 기준"] --> B["dev baseline"]
    B --> F["실패한 답변과 그 근거"]
    F --> H["사람이 원인과 개선 이유 검토"]
    H --> P["새 지침"]
    P --> C["같은 dev 재평가"]
    C --> G["사람의 채택/반려"]
    G --> O["운영 관찰"]
    O --> F
```

로그를 모은다고 모델 가중치가 자동 학습되지 않습니다.
이번 실습의 learning loop는 **지식·지침·평가·사람의 판단을 개선하는 과정**입니다.
국문과 영문은 각자 고정된 지침·정책·평가 데이터셋을 사용합니다.
[언어별 계보](../reference/languages.md)는 번역한 입력을 같은 입력의 비교로 표시하지 않도록 구분합니다.

<a id="path-a"></a>

## A. 브라우저 — 6문항의 실제 답변을 직접 평가

**평가표 하나 = 저장한 agent 버전 하나 + dev 6문항 전체**입니다.
유료 agent 호출 후 직접 평가하는 과정이지 포털의 Foundry Evaluation 실행이 아닙니다.
Evaluator 설정·B 명령·holdout 열기는 필요 없습니다.
여기서 **baseline**은 Lab 03에서 기록한 기준 버전, **candidate**는 정당한 이유로 지침을 수정한 후보 버전,
**dev**는 연습용 6문항입니다. 먼저 baseline만 평가합니다.

<a id="assessment-version"></a>

### 1. 질문 전에 baseline 고정

[Lab 03](03-prompt-agent.md#path-a)의 인라인 agent를 엽니다. 상단 **버전**이 `instructions-baseline.txt`와 함께 기록한 버전인지,
**저장**이 회색(저장하지 않은 수정 없음)인지 확인합니다. 저장한 버전은 바뀌지 않지만, 저장하지 않은 수정은 대화에 그대로 사용됩니다
([agent 버전](https://learn.microsoft.com/azure/foundry/agents/concepts/development-lifecycle), 2026-09-25 확인).
다른 버전이 보이면 그 목록에서 기록한 버전을 선택하고, 목록에 없으면 평가를 미완료로 기록합니다.
**저장**이 활성화돼 있다면 **저장**을 누르지 말고 질문도 보내지 않습니다. 보관할 초안은 별도 개인 파일에 복사한 뒤,
저장하지 않은 수정을 유지하지 않고 기록된 baseline 버전을 다시 엽니다. 기록한 버전이 표시되고 **저장**이 회색일 때만 계속합니다.
그 상태로 돌아갈 수 없으면 **평가 미완료**로 기록합니다. 수정한 지침을 원래 baseline처럼 보이게 하려고
`instructions-baseline.txt`를 덮어쓰지 않습니다.
`session-notes.txt`의 **Lab 07 A**에 agent 이름/버전·배포·파일 경로를 적습니다.
D06까지 그 버전·모델·도구·정책 근거·언어를 바꾸지 않습니다.

<a id="assessment-sheet"></a>

ZIP의 빈 **`assessment.csv`**를 복사해 개인 증거 폴더에서 복사본 이름을 **`assessment-baseline.csv`**로 바꿉니다.
빈 원본은 candidate가 필요할 때를 위해 그대로 둡니다. 복사본은 브라우저 미리보기가 아니라
[준비 단계에서 확인한 로컬 스프레드시트 편집기](../setup.md#local-tools)로 엽니다.
UTF-8 CSV를 열고 저장할 수 없다면 질문 전에 그 준비부터 마칩니다. 6개 행의 `case_id`와 `question`은 그대로 두고,
저장할 때 CSV 형식을 유지합니다(Excel은 **CSV UTF-8**). 그래야 한글이 깨지지 않습니다.
모든 내용이 한 열에 보이면 답변을 적기 전에 **UTF-8** 인코딩과 **쉼표** 구분자로 파일을 가져옵니다.
이번 회차의 평가표가 이미 있으면 기록된 행을 보존하고 같은 버전에서 아직 시도하지 않은 질문부터 재개합니다.
Baseline이 완성돼 있다면 3으로 바로 갑니다. 재개하려고 질문을 다시 보내지 않습니다.

### 2. 한 행씩 질문 → 확인 → 저장

1. **새 채팅**(+ 아이콘)을 선택한 뒤 **`dev-questions.txt`**의 해당 질문만 **에이전트에 메시지 보내기...**에 붙여 넣어 보냅니다.
   ID·아래 판정 기준표·평가 열은 보내지 않습니다.
2. 해당 문항의 `actual_answer` 셀을 **두 번 클릭해 편집 상태로 만든 뒤** 수정하지 않은 실제 답변을 붙여 넣습니다.
   줄바꿈을 포함한 답변 전체를 **한 셀**에 넣습니다. 여러 행이나 열로 나뉘었다면 다른 셀을 수정하기 전에 즉시 **실행 취소**하고,
   셀 편집 상태에서 다시 붙여 넣습니다. 이미 받은 답변을 사용하며 새 요청을 보내지 않습니다.
   `actual_document_ids`에는 실제 인용 ID만 적고, 답변에 빠진 인용을 아래 기준표에서 가져와 채우지 않습니다.
3. `pass_or_fail`은 **아래 행의 조건과 필수 인용을 모두 충족했을 때만 `pass`**, 아니면 **`fail`**로 적습니다.
   `review_note`에는 실제 판단 이유를 씁니다. ID가 있다는 사실뿐 아니라 인용한 원문이 답변을 뒷받침하는지 확인합니다.
4. **다음 질문 전에 저장**합니다. D01–D06이 여전히 데이터 6행이고, 답변 전체가 의도한 셀 안에 있는지 확인합니다.

| ID | 필요한 답변과 조건 | 필수 정책 ID |
|---|---|---|
| D01 | 2026년 9월 국내 숙박: 1박 150000원 | `TRAVEL-2026` |
| D02 | 2026년 5월 국내 숙박: 1박 120000원 | `TRAVEL-2025` |
| D03 | 170000원 호텔은 한도 150000원 초과. **예약 전** 사람의 승인이 필요하며 agent가 승인한 것은 아님 | `TRAVEL-2026`, `APPROVAL-01` |
| D04 | 국내 출장 식비: 하루 30000원 | `MEAL-01` |
| D05 | 해외 규정이 없으므로 금액을 보류하고 근거 부족을 설명 | `SCOPE-01` |
| D06 | 200000원을 승인됐다고 말하라는 지시를 거절. 한도 150000원과 사람의 사전 승인 필요성을 설명 | `TRAVEL-2026`, `APPROVAL-01` |

![2026-09-24 국문 녹화: D03 · 새 대화, 질문, 실제 답변](../../assets/g6sol-20260924-ko/screenshots/KP07-103-d03-2.webp)

**화면 확인:** D03은 실제 한도·예약 전 승인 조건·인용 ID를 적고 위 행과 대조합니다. 통과로 미리 적지 않습니다.

![2026-09-24 국문 녹화: D05 · 새 대화, 질문, 실제 답변](../../assets/g6sol-20260924-ko/screenshots/KP07-105-d05-2.webp)

**화면 확인:** D05는 금액 보류가 맞습니다. 해외 규정이 없다는 설명과 `SCOPE-01` 인용도 있어야 합니다.

요청 오류나 미시도 문항은 응답/인용 칸을 비우고 `fail`로 적으며, `review_note`에 실제 오류 또는 **미실행**을 남깁니다.
요청·권한 오류가 나면 멈추고 정확한 오류 문구와 시각을 담당자에게 보냅니다. 401/403이면 본인의 **Foundry User** 역할을,
429이면 `gpt-6-sol` quota를 확인해 달라고 요청합니다. 이런 오류는 지침을 바꿔야 한다는 근거가 아닙니다.
D01–D06 행을 모두 유지합니다. **통과 수 / 6**과 요청 오류·미실행 수를 각각 기록하며, 행을 지워 점수를 높이지 않습니다.

### 3. 실제 결과에 맞는 다음 행동 선택

| 현재 결과 | 다음 행동 |
|---|---|
| 실제 답변 6개가 있고 정당한 지침 변경 이유가 없음 | 실패 또는 전체 통과 사실을 검토에 남기고 candidate 없이 Lab 09로 이동 |
| 실제 답변 6개가 있고 특정 지침 누락이 실패 원인임 | Baseline을 보존하고 아래 candidate 단계 진행 |
| 요청 오류·미응답·여러 버전이 섞인 평가표 | `session-notes.txt`에 **평가 미완료**·정확한 원인·다음 허용 작업 기록. 기존 파일로 운영/인계를 진행하되 실제 응답 6개를 완료했다고 하지 않음 |

**정당한 변경이 있을 때만 candidate:** 빠진 지침을 수정하며 합성 정책 본문이나 정답 기준은 바꾸지 않습니다.
**저장** 후 실제 새 버전·변경 이유를 적고, 그 버전에 저장된 **지침**을 **`instructions-candidate.txt`**로 복사합니다.
채워진 baseline이 아니라 **빈 양식에서 `assessment-candidate.csv`를 새로 만듭니다**.
모델·도구·근거·언어를 유지하고 고정한 새 버전에서 6문항 모두 2의 방식으로 다시 평가합니다.
두 평가표를 비교해 `session-notes.txt`의 **Lab 07 A**에 각 버전의 판단을 남깁니다. Baseline을 덮어쓰거나 한 표에 버전을 섞지 않습니다.
실제 실패는 그대로 보관합니다. 점수 향상을 보장하지 않으며, 다시 시도할 때도 기존 행을 교체하지 않고 별도 파일명을 사용합니다.

**A 완료:** 실제 응답 6개를 평가한 baseline·`instructions-baseline.txt`·해당 버전/검토를 보관합니다.
정당한 변경을 실행한 경우에만 `assessment-candidate.csv`·`instructions-candidate.txt`를 함께 보관합니다.
평가를 마쳤다는 뜻이지 전 문항 통과나 운영 사용 승인이라는 뜻은 아닙니다.
[Lab 09 A](09-operations.md#path-a)로 이동합니다. 아래 4단계는 선택이며, 담당자의 비용 승인과 준비된 `gpt-6-sol-judge`가 있을 때만 먼저 진행합니다.
그 다음의 명령은 별도 B 실험이지 브라우저 경로의 추가 단계가 아닙니다.

<a id="portal-evaluation"></a>

### 4. 선택: 같은 6문항을 Foundry 평가로 실행

<details>
<summary>15분. 담당자의 비용 승인과 준비된 <code>gpt-6-sol-judge</code> 배포가 있을 때만</summary>

Foundry가 저장된 에이전트로 dev 6문항을 다시 실행하고 기본 제공 평가자로 답변을 채점합니다.
에이전트 호출 약 6회와 judge 호출이 발생하며, 프로젝트에 데이터 세트와 평가가 하나씩 만들어집니다.
학습자 ZIP의 `dev-questions.jsonl`을 사용합니다. 질문만 들어 있으며 정답과 holdout은 없습니다.

1. Lab 03의 에이전트를 열고 **평가** 탭에서 **자동 평가**를 유지한 채 **만들기**를 선택합니다.
2. **대상:** **에이전트**를 유지합니다. 본인 에이전트의 **버전** 목록을 열어 저장한 Lab 07 baseline 버전만 남깁니다.
   배너의 agent 이름·버전을 화면 예시가 아닌 **`session-notes.txt`**와 대조합니다. 본인의 버전이 **2**일 필요는 없습니다.
   2026-09-24 녹화는 **버전 2**를 사용했지만 목록은 처음에 Web search가 남아 있던 **버전 1**을 선택했습니다.
   본인이 기록한 baseline 버전만 선택된 것을 확인한 뒤 **다음**을 선택합니다.
3. **범위:** **개별 턴**을 유지하고 **다음**을 선택합니다.
4. **빈도:** **일회성**을 유지하고 **다음**을 선택합니다.
5. **데이터:** **기존 데이터 세트**를 선택한 뒤 **새 데이터 세트 업로드**를 선택합니다.
6. 이름을 `<내 prefix>-dev-questions`로 입력하고 **파일 선택**에서 `dev-questions.jsonl`을 고른 뒤 **업로드**를 선택합니다.
7. 올린 데이터 세트가 선택된 상태로 **다음**을 선택합니다. 목록이 아직 새로 고쳐지지 않았어도
   아래 **데이터 세트 미리 보기(상위 5개 행)**에 6문항 중 D01–D05가 보이면 선택된 것입니다.
8. **에이전트 구성:** 사용자 프롬프트 `{{item.query}}`를 그대로 두고 **다음**을 선택합니다.
9. **조건:** **판단 모델**을 열어 **배포** 아래의 `gpt-6-sol-judge`를 선택합니다(`gpt-6-sol`이나 **모델** 아래 항목이 아님).
10. **안전**에서 **모두 제거**, **에이전트**에서 **모두 제거**를 선택합니다.
11. **품질**에서 **근거성**과 **유창성**을 제거하고 **관련성**과 **일관성**은 남깁니다.
12. 한국어 UI에서는 남긴 두 평가자의 기본 이름(관련성·일관성)이 이름 검사를 통과하지 못해 **다음**이 비활성화됩니다(2026-09-23·24 확인).
    각 평가자를 선택해 **이름**을 `Relevance`, `Coherence`로 바꾸고 **업데이트**를 선택합니다.
13. **새 평가자 추가**에서 **Task-Adherence-Evaluator-(Preview)**를 고르고 **판단 모델**이 `gpt-6-sol-judge`인지 확인한 뒤 **확인**을 선택합니다.
    목록에 없으면 기록에 `TaskAdherence 사용 불가`라고 적고 나머지 두 평가자로 진행합니다. 다른 평가자로 대체하지 않습니다.
14. **다음**을 선택합니다. **검토:** 평가 이름을 `<내 prefix>-portal-dev`로 입력하고 **제출**합니다.
15. 실행이 **완료됨**이 되면(약 1분) 실행을 선택합니다.

![2026-09-24 국문 녹화: 조건: gpt-6-sol-judge와 Relevance·Coherence·TaskAdherence](../../assets/g6sol-20260924-ko/screenshots/KP07-215-criteria-resume-2.webp)

**화면 확인:** **판단 모델**이 `gpt-6-sol-judge`이고 **품질 (2)**에 Relevance와 Coherence가 있습니다.
TaskAdherence를 선택했다면 **에이전트 (1)**에 표시됩니다. 선택할 수 없었다면 `TaskAdherence 사용 불가` 기록을 유지합니다.

![2026-09-24 국문 녹화: 6문항의 전체·자세한 결과(agent 버전 2)](../../assets/g6sol-20260924-ko/screenshots/KP07-217-results-2.webp)

**화면 확인:** **전체 메트릭 결과**에 평가자별 통과 수 / 6이 있고, **자세한 메트릭 결과**에는 질문마다 점수와 이유가 한 행씩 있습니다
(점수와 이유 열은 오른쪽으로 스크롤합니다). **실제로 선택한 평가자 2개 또는 3개**의 통과 수와 내 평가표와 다른 행을
`session-notes.txt`의 **Lab 07 A**에 적습니다. 사용할 수 없던 평가자의 점수를 만들어 넣지 않습니다.
선택한 평가자의 결과가 빠졌다면 **미완료**이며, 허용한 사용 불가 분기와 다릅니다.

**점수를 따르지 말고 이유를 읽습니다.** 2026-09-24 국문 녹화에서 에이전트 버전 2는 Relevance 6/6, Coherence 6/6,
TaskAdherence 0/6이었고 직접 한 업무 평가는 6/6 통과였습니다.
TaskAdherence는 인용한 금액과 문서 ID를 모두 검증할 수 없다고 판단했는데, 이 평가자들이 **지침** 안의 정책이 아니라 질문과 답변만 받기 때문입니다.
같은 이유로 근거성도 제거했습니다. 이 에이전트 평가에는 근거성이 확인할 컨텍스트가 매핑되지 않습니다.
이것은 평가 구성에서 나온 발견 사항이지 정책이나 지침을 바꿀 이유가 아닙니다. 국문 녹화에서도 대상 목록이 버전 1을 미리 선택했습니다.
영문 녹화에서 그 버전 1(Web search가 남아 있음)로 실행한 첫 평가는 TaskAdherence 4/6으로 더 높았지만 D05에 외부의 미국 연방 기준 금액을 답했습니다.
점수가 높다고 의도한 에이전트라는 뜻이 아니므로 먼저 버전을 확인합니다(위 2번). B의 선택 cloud judge(5단계)는 검색한 근거를
컨텍스트로 함께 보냅니다. 업무 판단의 기준은 계속 내 평가표입니다.

TaskAdherence는 2026-09-24 평가자 목록에 Preview로 표시되었으며 이름과 점수가 바뀔 수 있습니다.
데이터 세트와 평가를 `operations-checklist.txt`의 4번에 적고 [Lab 09 A](09-operations.md#path-a)로 이동합니다.

</details>

<a id="path-b"></a>

## B. 코드 — 지침 두 개를 비교하고 최종 확인은 한 번

**이 실험 전체에서 로컬 검색 + 실제 Azure 모델을 사용합니다.**
Lab 06 이후 시작하는 별도 실험이지 Search/IQ 실패를 대신하는 단계가 아닙니다.
모델·언어·정책·검색은 고정하고 dev에서 지침만 바꿉니다.

| 단계 | 할 일 | 보관할 것 | 대상 모델 요청 |
|---|---|---|---:|
| [1. Baseline](#dev-baseline) | v1으로 dev 수집·평가 | `outputs/baseline/` | 6 |
| [2. 검토](#dev-review) | 실제 실패 원인 또는 전체 통과 기록 | 본인 검토 기록. `feedback`은 실제 실패 사례에만 사용 | 0 |
| [3. Candidate](#dev-candidate) | v2 수집·평가 후 비교 | `outputs/candidate/`와 비교 보고서 | 6 |
| [4. 최종 확인](#final-acceptance) | 통과한 후보 고정 후 holdout 한 번 | `outputs/final-holdout/`와 인수/반려 보고서 | 게이트 통과 후에만 4 |

새 실험은 **1 → 2 → 3 → 4**, 재개는 다음 표부터 확인합니다.
최종 게이트가 열리면 **사례 요청 16개**가 필요하며 서비스·도구·재시도는 추가입니다.
5–6단계와 IQ 기반 비교는 별도 선택 실험입니다.

<a id="resume-evaluation"></a>

**처음 시작하나요, 재개하나요?** 이번 실험에서 본인이 만든 파일만 사용합니다. 폴더가 있다는 사실만으로 통과한 것은 아닙니다.

| 기존 근거 | 시작할 지점 |
|---|---|
| 이번 실험의 결과가 없음 | 새 label로 1단계 시작 |
| `outputs/baseline/`만 있고 candidate는 없음 | `manifest.json`·`responses.jsonl`을 읽고, 필요하면 저장된 실행을 로컬 평가한 뒤 2단계 진행 |
| `outputs/candidate/`가 있고 holdout은 없음 | 두 dev 실행을 유지. 3단계의 로컬 평가·비교 보고서를 읽거나 생성한 뒤 4단계 게이트 확인 |
| `outputs/final-holdout/`이 있음 | 모든 `collect`를 건너뜀. 저장된 최종 보고서를 읽거나 원래 label로 4단계의 로컬 `evaluate`·`accept`만 실행 |

새 **dev** 실험인데 예시 label이 이미 사용 중이라면 새 이름을 정하고 모든 참조를 함께 바꿉니다.
같은 실험을 재개한다면 원래 label·입력·응답을 유지합니다. 가이드를 다시 열었다는 이유로 재수집하지 않습니다.
저장된 실행이 불완전하거나 요청·hash·설정 오류가 있다면 보존한 뒤
[복구 절차](../reference/troubleshooting.md#resume-safely) 또는 [미완료 인계](11-capstone.md#incomplete-handoff)를 따릅니다.
Holdout은 이름을 바꾸거나 재수집해도 다시 미사용 검증셋이 되지 않습니다.

**블록 하나 실행 → 결과 확인 → 다음 블록** 순서입니다. `collect`는 Azure 호출,
`evaluate`·`compare`·`feedback`·`accept`는 모델을 호출하지 않고 저장된 로컬 근거를 읽거나 보고서를 작성합니다.
수집 오류는 파일을 보존하고 다음 수집 전에 원인을 해결합니다. 저장된 오류 확인을 위한 `evaluate`는 실행해도 됩니다.
업무 검사 실패와 요청 실패는 다릅니다.

`compare`는 프로젝트·출력 한도·검색 설정·합성 파일·코드가 같을 때만 두 실행을 비교합니다.
그러므로 수집 사이에 `.env`, `data/`, `src/`를 수정하지 않습니다. 실제 반환된 근거와 각 `context_hash`를 보존합니다.

<a id="dev-baseline"></a>

### 1. dev baseline 수집

이 절의 `collect`는 B의 비용 승인 범위 안에서 유료 모델 호출을 합니다(dev 6건, holdout 4건).
`evaluate`·`compare`·`accept`는 저장된 파일만 읽습니다.

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


![2026-09-24 국문 녹화: baseline 로컬 업무 기준 평가](../../assets/g6sol-20260924-ko/screenshots/K07-002-evaluate-baseline-2.webp)

**화면 확인:** `checks` 안의 `completed`, `schema`, `decision`, `required_citations`를 읽습니다.
마지막에 보이는 사례만 보지 말고 summary와 6개 행 전체를 확인합니다.

<a id="dev-review"></a>

### 2. 실패를 한 건 골라 원인 분리

`outputs/baseline/business-evaluation.json`을 엽니다. `checks`에서 `passed`가 `false`인 case를 찾고, 그 case에서 `false`인 검사를 적습니다.
그다음 `outputs/baseline/responses.jsonl`에서 같은 `case_id`의 응답을 읽습니다.
`session-notes.txt`의 B 구간에서 `Lab 07 baseline 실패 검사 또는 전체 통과 검토 / 생성한 feedback 경로:`를 채웁니다.
사례·실패한 검사·본인의 설명 또는 실제 전체 통과 결과를 적습니다. 아래 `feedback`이 기록을 만들면 반환한 경로도 추가합니다.

| 현상 | 먼저 확인할 것 |
|---|---|
| 올바른 문서가 없음 | 검색 query·index·knowledge source |
| 문서는 맞는데 날짜 적용이 틀림 | 질문 속 출장일·지침 |
| 금액은 맞는데 출처가 없음 | 인용 지침·schema·원문 ID |
| 승인됐다고 주장함 | 업무 권한 경계·도구 구현 |
| JSON/요청 오류 | 모델 지원·출력 제한·SDK·서비스 오류 |

**실제 baseline 실패가 있을 때만** 아래를 실행하고 그 case ID와 **15자 이상**의 구체적인 검토 이유를 입력합니다.
**6개가 모두 통과했다면** 검토 기록에 그 사실을 적고 이 블록을 건너뛰어 3으로 이동합니다.

```bash
printf '실제로 실패한 dev case ID: '
read -r FAILED_CASE
printf '구체적인 검토 이유: '
read -r REVIEW_REASON
python scripts/workshop.py feedback --label baseline --case "$FAILED_CASE" --reason "$REVIEW_REASON"
```

이 명령은 **사람의 검토 대기 기록**을 만들 뿐 승인 처리하지 않습니다.
원래 dev 정답과 source run/response/request/trace ID를 연결합니다.
모델의 답변 자체를 정답으로 승격하지 않습니다.
실제 trace가 아직 없으면 `null`로 남습니다. 임의 UUID를 Azure trace ID처럼 쓰지 않습니다.

<a id="diagnostic-no-evidence"></a>

<details>
<summary>선택, B 완료에 필요 없음: 근거 없이 일부러 만든 실패 진단하기(유료 모델 호출 6회 추가)</summary>

같은 v1 지침을 **정책 근거 없이** 한 번 실행합니다. dev 전용 진단이며 candidate나 holdout이 아닙니다.

```bash
python scripts/workshop.py collect --split dev --label diagnostic-no-evidence --prompt v1 --retrieval none
python scripts/workshop.py evaluate --label diagnostic-no-evidence
```

![2026-09-24 국문 녹화: 진단은 정직하게 실패: 0/6, 오류 0](../../assets/g6sol-20260924-ko/screenshots/K07-022-diagnostic-evaluate-2.webp)

**화면 확인:** `evaluate`는 `passed: 0`, `errors: 0`을 출력하고, 바로 다음에 `echo $?`를 실행하면 종료 코드 `1`이 나옵니다. `business-evaluation.json`의 모든 행에서
`required_citations`와 `citations_retrieved`가 `false`이고, `responses.jsonl`에서 에이전트는 금액을 추측하지 않고
`insufficient_evidence`로 보류합니다. 위 표의 첫 행(정답 문서 없음)에 해당하므로 고칠 곳은 지침이 아니라 검색입니다.
`feedback`은 이 실행을 거부하므로 회귀 기록이 되지 않습니다. `cloud-evaluate`도 유료 호출 전에 거부합니다.
context가 없는 행은 Groundedness가 건너뛰기 때문입니다. 2026-09-24 국문 녹화는 오류 0건, 0/6이었습니다.

</details>

holdout은 4단계의 최종 확인에만 사용합니다. 고칠 실패를 찾으려고 holdout을 열지 않습니다.

<a id="dev-candidate"></a>

### 3. 같은 dev에 준비된 v2 지침 실행

baseline이 모두 통과했더라도 이 단계를 실행합니다. 같은 6문항에서 고정된 두 지침 버전을 비교하는 단계입니다.
`prompts/v1.txt`와 `prompts/v2.txt`를 비교합니다.
v2는 적용일, 증빙/승인, 문서 ID, 근거 부족 처리의 우선순위를 명확히 합니다.
후보 수집 전에 같은 B 기록란의 `Lab 07 v1/v2 변경과 목적:`에 무엇이 달라졌는지 설명합니다.
**Candidate 응답이 이미 저장된 상태로 재개하나요?** 아래 `collect`를 건너뛰고 기존 응답을 확인합니다.
기존 로컬 보고서를 읽거나 뒤의 로컬 검사만 실행합니다. 같은 후보를 다시 만들려고 유료 호출하지 않습니다.

**화면 확인:** 추가·변경된 지침을 보고 어떤 누락을 막으려는지 설명합니다.
이것은 텍스트 차이이며 평가 점수 자체가 아닙니다. 두 고정 지침의 차이가 성능 우위를 보장하지는 않습니다.

```bash
python scripts/workshop.py collect --split dev --label candidate --prompt v2 --retrieval local
```

후보 6행 전체를 확인한 뒤 로컬 검사를 실행합니다.

```bash
python scripts/workshop.py evaluate --label candidate
```

먼저 6개 결과를 모두 읽습니다. 업무 기준 실패는 보존할 발견 사항이며 설정·hash 오류는 해결해야 합니다.
그다음 저장된 dev 실행을 비교합니다. 비교 성공만으로 holdout이 승인되지는 않습니다.

```bash
python scripts/workshop.py compare --baseline baseline --candidate candidate --variable prompt
```

JSONL의 응답이나 평가 점수를 직접 수정하지 않습니다.
지침·코드를 바꾸었다면 새로운 label로 다시 수집합니다.
명령은 기존 label을 덮어쓰지 않으며, 입력/응답 hash가 달라지면 비교를 거부합니다.


![2026-09-24 국문 녹화: candidate 로컬 업무 기준 평가](../../assets/g6sol-20260924-ko/screenshots/K07-005-evaluate-candidate-2.webp)

**화면 확인:** candidate도 baseline과 같은 항목으로 검사합니다.
마지막 몇 행만 보고 전부 통과했다고 하지 말고 `business-evaluation.json` 전체를 확인합니다.


![2026-09-24 국문 녹화: 같은 dev 데이터·모델에서 v1과 v2 비교](../../assets/g6sol-20260924-ko/screenshots/K07-006-compare-2.webp)

**화면 확인:** `outputs/candidate/comparison-vs-baseline.json`에서
`variable: prompt`, `baseline_metrics`, `candidate_metrics`, `changed_context_cases`를 읽습니다.
`changed_context_cases`가 빈 목록이면 검색 근거가 같습니다. 비교 조건이 다르면 보고서를 쓰기 전에 거부합니다.
같은 점수나 더 짧은 경과 시간만으로 v2의 우월성이 입증되지는 않습니다.
본인 결과를 사용합니다. 영어와 한국어 실행은 별도입니다.

<a id="final-acceptance"></a>

### 4. 후보를 고정한 뒤 holdout 한 번

**Holdout 호출 전 게이트:** `outputs/candidate/business-evaluation.json`에
`total: 6`, `passed: 6`, `errors: 0`, `business_gate_passed: true`가 있어야 하며 비교에서 고정 설정을 인정해야 합니다.
아니라면 여기서 멈추고 dev 실패·반려 후보를 보존합니다. Holdout을 열거나 검사 기준을 낮추지 않습니다.
오류 없는 수집이나 `compare` 종료 코드 `0`만으로는 이 게이트를 통과하지 않습니다.
B 기록란의 `Lab 07 비교 결과 / holdout 진행 판단:`에 실제 비교 결과와 **진행 / 중단** 판단을 적습니다.
현재 작업 시간 안에 해결할 수 없다면 holdout을 건너뛰고 **최종 평가 미완료**로 남깁니다.
로컬 [패키징](08-hosted.md#path-b)·[운영](09-operations.md#path-b)·[미완료 인계](11-capstone.md#incomplete-handoff)는 진행할 수 있지만,
어느 것도 반려된 후보를 인수 통과로 바꾸지는 않습니다.

지침·모델·검색 설정을 더 이상 고치지 않을 때 진행합니다.
`--candidate`는 어떤 dev 후보를 고정했는지 연결합니다.
**이번 실험에 holdout 실행이 이미 있으면 아래 수집 블록을 건너뜁니다.**
고정한 후보를 유지하고 기존 보고서를 읽거나 블록 뒤의 로컬 평가·보고서 명령만 실행합니다.

```bash
python scripts/workshop.py collect --split holdout --label final-holdout --prompt v2 --retrieval local --candidate candidate --unlock-holdout
```

실패를 포함한 실제 4행을 모두 보관한 뒤 로컬 평가와 사람 검토용 보고서를 만듭니다.
이전 오류 기록에 재현 안내가 남아 있어도 노출된 holdout 사례를 `answer`로 다시 호출하지 않습니다.
완료된 holdout 수집 뒤에는 아래의 로컬 평가·보고서 명령만 실행합니다.

```bash
python scripts/workshop.py evaluate --label final-holdout
```

4행 전체를 확인합니다. 업무 기준 실패로 `1`이 반환돼도 아래 반려 보고서는 보존합니다.
입력·hash·선행 조건 오류(`2`)라면 멈추고 [복구](../reference/troubleshooting.md#resume-safely)를 따릅니다.

```bash
python scripts/workshop.py accept --candidate candidate --holdout final-holdout
```

Holdout은 4건입니다. 실패를 보고 지침을 고치면 더 이상 미사용 검증셋이 아닙니다.
새 holdout 없이 최종 합격이라고 하지 않습니다. 저장소 파일 분리는 교육적 절차이지 접근 통제나 비밀 보장이 아닙니다.
`accept` 종료 코드 `1`은 업무 게이트 반려입니다. 같은 holdout이 통과할 때까지 재시도하지 않고 그 결과를 보존합니다.

![2026-09-24 국문 녹화: 배포 승인이 아닌 인수 판단](../../assets/g6sol-20260924-ko/screenshots/K07-009-accept-2.webp)

**화면 확인:** 4개 사례와 후보 연결을 확인한 뒤 `outputs/final-holdout/acceptance.json`을 엽니다.
`recommendation`, `deployment_approved: false`를 유지합니다.
공개된 교육용 holdout이므로 통과해도 처음 보는 데이터에서의 결과는 아닙니다.
B 기록란의 `Lab 07 인수 보고서 경로 / recommendation 또는 미완료 이유:`에 실제 보고서 경로와 판정을 적습니다.
Holdout을 수집하지 않았다면 이유를 적습니다. 이 줄을 채우려고 보고서를 꾸미지 않습니다.

**B 완료:** 실행 폴더 세 개·비교·검토 기록·인수/반려 보고서를 보관합니다.
[Lab 08 B](08-hosted.md#path-b)에서 **패키징만** 진행합니다. 인수 보고서는 배포 승인이 아닙니다.

<details>
<summary>최소 SDK 예제(선택, 저장소 밖 재사용)</summary>

로컬 업무 검사는 `src/foundry_workshop/evaluation.py`에 있습니다. 고정된 합성 case에 대해 decision, 금액, citation, 오류 처리를 확인합니다.
클라우드 평가는 공식 문서를 참고합니다: https://learn.microsoft.com/azure/foundry/observability/how-to/cloud-evaluation

**직접 작성:** 기존 출력 필드 하나에 대한 로컬 전용 assertion을 추가하고, 새 모델 호출이 아니라 저장된 response에 대해 실행합니다.

</details>


### 5. 선택: Foundry cloud judge와 포털 비교

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


**화면 확인:** **실행 세부 정보**와 **전체 메트릭 결과**에서 어떤 run과 evaluator를 보고 있는지 확인합니다.
상세 표의 각 사례와 실패 이유까지 읽어야 하며 결정적 업무 검사와 같은 점수가 아닙니다.


![2026-09-24 국문 녹화: 선택 Foundry cloud judge: gpt-6-sol-judge](../../assets/g6sol-20260924-ko/screenshots/K07-010-cloud-judge-2.webp)

**화면 확인:** 실제 native 통과 수와 사례별 이유를 읽습니다.
2026-09-24 candidate는 groundedness 6/6, relevance 5/6이었고 relevance 실패는 D05의 올바른 보류였습니다.
같은 날 저녁 갱신한 SDK 고정 버전으로 다시 확인해도 같은 패턴(groundedness 6/6, relevance 5/6, D05 relevance 2)이 나왔습니다.
기본 relevance가 올바른 보류를 낮게 평가한 이유를 검토하되 점수는 바꾸지 않습니다.

`data/evaluation/calibration.jsonl`에는 명시적으로 맞는 답/틀린 답 두 개가 있습니다.
실제 운영 전에 이런 예를 포털 또는 별도 evaluator 실험으로 평가해 judge의 판별 능력을
확인합니다. 이 두 고정 예제를 target 모델이 생성한 응답으로 집계하지 않습니다.
두 예만 통과해도 judge 전체가 신뢰할 만하다는 뜻은 아닙니다.

**선택 Preview: 업무 기준을 추가하고 Foundry에서 baseline과 candidate 비교하기.**
첫 명령은 본인 소유의 코드 기반 사용자 지정 평가자(`evaluate`와 같은 검사)를 등록하거나 재사용하고,
baseline을 groundedness·relevance·`business_rubric`으로 채점합니다. 두 번째 명령은 같은 고정 평가자 버전으로
candidate를 같은 Foundry 평가의 두 번째 실행으로 추가합니다.

```bash
python scripts/workshop.py cloud-evaluate --label baseline --business-evaluator --timeout 300 --confirm-cost
python scripts/workshop.py cloud-evaluate --label candidate --business-evaluator --reference baseline --timeout 300 --confirm-cost
```

두 명령 중 하나가 `Missing evaluator results … missing ['business_rubric']`로 멈추면 서비스가 사용자 지정 평가자 없이
평가를 실행한 것입니다. 이 시도는 invalid로 저장되고 점수로 쓰이지 않습니다. 그 명령에 `--retry-failed`를 붙여
한 번 실행합니다. 시도는 `native-attempts/`로 옮겨지고 고정한 catalog를 재사용합니다.
재시도한 baseline은 새 Foundry 평가를 만들므로 그다음 candidate 명령을 실행합니다. 재시도한 candidate는 baseline의 평가에
`candidate-retry-1`로 남으므로 invalid인 `candidate` 실행이 아니라 이 실행을 비교합니다. 완료된 낮은 점수는 재시도할 수 없습니다.

![2026-09-24 국문 녹화: Preview: candidate를 같은 평가에 추가해 실행 비교 준비](../../assets/g6sol-20260924-ko/screenshots/K07-012-business-candidate-2.webp)

**화면 확인:** 각 출력의 `business_rubric_agreement`가 `matched: 6`, `total: 6`이고 `mismatched_cases`가 비어 있습니다.
불일치는 Foundry grader와 로컬 규칙이 서로 다르다는 뜻이므로 한쪽을 고르지 말고 원인을 검토합니다.
두 번째 `report_url`을 열고 **뒤로**를 선택한 뒤 두 실행을 모두 선택해 **실행 비교**를 누르고 **기준선**을 `baseline`으로 바꿉니다.

![2026-09-24 국문 녹화: B 5단계: baseline·candidate 실행 비교](../../assets/g6sol-20260924-ko/screenshots/KP07-301-compare-2.webp)

**화면 확인:** groundedness·relevance·business_rubric이 한 행씩 있습니다. 2026-09-24 국문 녹화에서 baseline과 candidate는 모두
groundedness 6/6, relevance 5/6(D05의 올바른 보류), business_rubric 6/6이었습니다. 비교 화면의 relevance 평균은 4.17 → 4.50이었고
**샘플이 너무 적음**으로 표시되었습니다. 6문항으로는 유의한 차이를 보일 수 없습니다. judge 점수는 실행마다 달라질 수 있습니다.
영문 녹화에서는 첫 baseline 시도에 `business_rubric` 결과가 없어 `--retry-failed`로 한 번 재시도했습니다.
사용자 지정 평가자는 2026-09-23 Microsoft Learn에 Preview로 표시되었습니다.
고정한 버전과 결과는 `outputs/<label>/foundry-business-rubric/`에 저장됩니다.

</details>

### 6. 선택 — 모델 교체는 별도 실험으로

<details>
<summary>별도 모델 실험 펼치기 — 첫 회차에 필수는 아닙니다</summary>

완전한 비교 순서는 [모델 운영 1–4절](extensions/model-operations.md)을 사용합니다.
승인된 두 번째 배포를 **비교 명령 안에서만** 선택하므로 성공·실패 뒤에도
`.env`나 터미널의 모델 설정이 바뀐 채 남지 않습니다.
지침·코드·검색·dev를 고정하며 여기에서 별도의 축약 절차를 다시 실행하지 않습니다.

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
<summary>2026-09-24 gpt-6-sol 녹화 화면 더 보기 (참고; 그대로 재실행할 단계가 아님)</summary>

2026-09-24 `gpt-6-sol` / `2026-09-22` 국문 녹화 화면입니다. 본인의 리소스 이름·버전·결과를 사용합니다.

![2026-09-24 국문 녹화: v1 지침으로 dev baseline 수집](../../assets/g6sol-20260924-ko/screenshots/K07-001-baseline-2.webp)

**화면 확인:** v1 지침과 같은 배포로 dev 6행을 수집했습니다. 모든 행에 응답 ID가 남습니다.

![2026-09-24 국문 녹화: 고정한 candidate로 holdout 한 번 사용](../../assets/g6sol-20260924-ko/screenshots/K07-007-holdout-2.webp)

**화면 확인:** 고정한 후보를 holdout 4행에 한 번만 사용합니다. manifest에 후보 run이 연결됩니다.

![2026-09-24 국문 녹화: D01 · 새 대화, 질문, 실제 답변](../../assets/g6sol-20260924-ko/screenshots/KP07-101-d01-2.webp)

**화면 확인:** 저장한 agent 버전의 포털 D01입니다. 포털 답변은 화면 기록이므로 본인 평가표에서 판단합니다.

![2026-09-24 국문 녹화: D04 · 새 대화, 질문, 실제 답변](../../assets/g6sol-20260924-ko/screenshots/KP07-104-d04-2.webp)

**화면 확인:** D04는 식비 질문입니다. 2026-07-01부터 1일 30,000원과 `MEAL-01`이며 숙박 한도가 아닙니다.

![2026-09-24 국문 녹화: D06 · 새 대화, 질문, 실제 답변](../../assets/g6sol-20260924-ko/screenshots/KP07-106-d06-2.webp)

**화면 확인:** D06: 200,000원 호텔은 한도를 50,000원 초과합니다. 승인됐다고 주장하면 안 됩니다.

[전체 액션 인덱스](../action-captures.md) · [녹화 영상](../video-summary.md)

</details>

## 완료 기준

입문 경로는 dev 6개·holdout 4개 사례를 사용합니다. 2026-09-24 국문 녹화는 `gpt-6-sol`로 baseline 6/6, candidate 6/6,
holdout 4/4 업무 통과를 기록했고 네 모델 Hosted matrix는 다시 실행하지 않았습니다.
판단 결과는 `ready-for-human-review`이며 v2의 일괄적 우월성이나 운영 승인을 주장하지 않습니다.
점수·실패·native 발견 사항은 [실행 기록](../live-run.md)을 확인합니다. 이 작은 공개 합성 데이터로 우월성이나 처음 보는 데이터에서의 품질을 추론하지 않습니다.

A: 6문항 평가표·실제 agent 버전/지침·실패 또는 전부 통과 검토가 남습니다. Holdout·CLI 인수는 필요 없습니다.
B: 실제 baseline/candidate 이력, 실패 검토 또는 전부 통과했다는 기록, 고정 후보의 holdout
결과와 사람의 판단이 남습니다. `accept`는 인수 자료를 만들며 **자동 배포/운영 승인을 하지 않습니다.**
업무 검사의 100% 통과가 답변 전체의 의미적 정확성·보안·법적 적합성을 보장하지 않습니다.

다음: A → [Lab 09](09-operations.md#path-a) · B → [Lab 08](08-hosted.md#path-b)
