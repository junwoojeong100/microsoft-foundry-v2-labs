# Agent Optimizer: 후보를 만들고 실제 근거로 판단하기

[English](../../../labs/extensions/agent-optimizer.md) | **한국어**

**C 선택 Preview · 2026-09-16 기준, 2026-09-23 `gpt-6-sol`로 재실행.** 첫 경로는 **Prompt Agent 최적화 wizard**입니다.
fine-tuning이나 모델 가중치 변경이 아닙니다. 기존 Hosted matrix와 수동 v1/v2 실험은 별도 대상으로 유지합니다.

**준비:** 전용 합성 Prompt Agent와 baseline 버전, 파생 dev 파일, 지원되는 기존 optimizer 배포, 별도 judge, 비용 승인.
**완료:** 한 실행의 baseline과 모든 반환 후보를 확인하고, 후보 없음/개선 없음도 명시함.
**중단:** 촬영을 끝내려고 다른 모델 생성, holdout 수정, 후보 자동 승격을 하지 않습니다.

**첫 회차:** 1–5절 후 `optimizer-review.txt`를 인계합니다. 승격은 필수가 아닙니다.
후보 없음·개선 없음·잘못된 evaluator binding은 보존할 발견 사항이지 승격 성공이 아닙니다.

## 1. 입력 한 번 준비

[Lab 03](../03-prompt-agent.md)의 전체 합성 정책을 가진 내 agent를 사용합니다.
새 이름의 전용 agent를 만들면 원래 지침/버전을 보존할 수 있습니다.
공유 agent나 이미 고정된 benchmark target을 변경하지 않습니다.

`outputs/extensions-ko/`가 아직 없을 때만:

```bash
python scripts/workshop.py --language ko prepare-extensions --label extensions-ko
```

`optimizer-dev.jsonl`, `SOURCE.json`, `manifest.json`을 확인합니다.
원본 **dev 6행**에서 파생되며 holdout이나 새 target 정답은 만들지 않습니다.
`query`만 agent 입력입니다. `context`, `ground_truth`는 평가 참조이며 target에 보내는 지침이 아닙니다.
wizard가 요구하는 열을 확인하고 임의 column mapping이 가능하다고 가정하지 않습니다.

| 값 | 첫 실행의 선택 |
|---|---|
| Target | 내 합성 Prompt Agent의 실제 baseline 버전 |
| 답변 모델 | 기존 검증된 배포, 첫 실행에서 모델 비교 제외 |
| Optimizer | 담당자와 wizard가 지원을 확인한 기존 배포 |
| Evaluator | 별도로 이름 붙인 승인된 judge |
| Dataset | `optimizer-dev.jsonl` 6행, holdout 금지 |
| Max candidates | **2** |
| 최적화 대상 | **Instruction만** |

지원되는 optimizer 모델이 없으면 미실행으로 멈춥니다.
답변 모델이 동작한다는 사실만으로 optimizer 용도를 지원한다고 판단하지 않습니다. `gpt-6-sol`만 배포된 2026-09-23에는
**Optimize** 탭이 **No supported optimization model**을 표시했습니다. 그날
[Microsoft Learn의 optimizer 모델 목록](https://learn.microsoft.com/azure/foundry/agents/concepts/agent-optimizer-overview#models)은
`gpt-5`, `gpt-5.1`, `gpt-5.2`, `gpt-5.4`, `gpt-5.5`, `DeepSeek-V4-Pro`, `DeepSeek-V-3.2`였습니다. 9월 23일 실행에서는 담당자가
임시 `gpt-5.5` 배포(`<prefix>-opt-gpt55`, DataZoneStandard)를 추가했고 두 언어 실행이 끝난 뒤 삭제했습니다.
최적화 대상은 Lab 03 에이전트와 지침이 같은 격리 복사본 `<prefix>-optimize` 버전 1이었습니다.

## 2. 최적화 마법사 열기

1. **에이전트 → 내 에이전트 → 최적화 미리 보기**(영문 UI: **Optimize Preview**)를 엽니다. 9월 23일 실행은 영문 UI에서 진행했으므로
   이하 wizard 이름은 영문 UI 기준입니다.
2. 처음에는 **Optimize my agent**, 기존 run이 있으면 **Create optimization run**을 선택합니다.
3. Target에서 실제 baseline 버전을 확인합니다.
4. 준비된 optimizer/judge와 후보 수 2를 지정합니다.
   9월 23일에는 **Evaluation model** 기본값이 답변 배포 `gpt-6-sol`이었으므로 `gpt-6-sol-judge`로 바꿉니다.
5. **Choose targets → Instruction**을 선택하고 **Model**을 해제합니다.

명시적 대상 선택으로 전환할 때 Model이 자동 선택되었던 화면을 관찰했습니다.
실제 체크 상태를 확인합니다.
계속하기 전에 agent 이름/버전, 선택한 배포, 원래 지침을 기록합니다.
optimizer model은 변경을 생성하고 target은 질문에 답하며 judge는 답변을 채점합니다. 이들은 서로 다른 역할입니다.
제품의 예시 benchmark 점수는 내 baseline이나 결과가 아닙니다.

## 3. dev와 평가 기준 선택

1. Data에서 **Select dataset and criteria**를 선택합니다. 기본 production-trace 생성 경로를 사용하지 않습니다.
2. **Upload dataset**으로 내 국문 이름을 주고 `outputs/extensions-ko/optimizer-dev.jsonl`을 업로드합니다.
3. 새 dataset 버전과 `case_id`, `query`, `context`, `ground_truth`를 확인합니다.
4. 미리보기는 **상위 5행만** 보여줍니다. 원본 파일과 나중의 실제 평가 결과에서 6행 전체를 확인합니다.
5. Criteria에서 **Custom only**를 해제하고 **Groundedness-Evaluator**, **Relevance-Evaluator**를 고릅니다.
   Service-Groundedness와 혼동하지 않습니다. 고를 때마다 **Configure** 대화상자가 열리면 **Threshold**를 **4**로 두고 **Apply**를 누릅니다.
   실제 버전을 기록하고 같은 criteria, threshold, reference data를 run 전체에서 유지합니다.

필수 인용 기준을 완화하거나 올바른 승인 거절을 오답으로 바꾸거나 어려운 행을 빼서 점수를 올리지 않습니다.
service가 schema 불일치를 보고하면 멈추고 실제 요구 사항을 확인합니다.
열 이름을 몰래 바꾸거나 evaluator label을 target에 보내지 않습니다.

## 4. 비용 검토 후 한 번 제출

Review의 baseline/dataset/모델/평가 기준/후보 상한을 확인합니다.
답변·judge·개선 생성 비용을 구분합니다. 표시된 범위는 **추정치**이지 실제 청구액이나 강제 예산 제한이 아닙니다.
9월 23일에는 agent 호출 약 35회, 채점 약 70회, 개선 생성 약 3회에 추정 $0.27(범위 $0.00–$0.90)로 표시되었습니다.

담당자가 표시된 예상 비용을 승인한 뒤 **Submit**을 한 번 누릅니다. 같은 run ID를 끝까지 확인합니다.
대기하거나 화면을 놓쳤다는 이유로 재제출하지 않습니다.
실패/불완전 실행의 성공 부분만 좋은 후보로 보고하지 않습니다.

## 5. 후보보다 세부 결과 먼저

각 후보에 대해 다음을 보관합니다.

- 전체 evaluator 결과와 실제 case 분모.
- 전후 지침 diff와 바뀐 모델/도구 설정.
- 모델/phase별 실제 token 사용량. 누락된 측정값은 누락된 상태로 둡니다.
- 실패 case와 제안 문구가 여전히 근거·날짜·승인 경계를 보존하는지 여부.

가장 높은 종합점수도 제안일 뿐 자동 수락이 아닙니다.
개선이 없거나 구별되지 않으면 baseline을 유지합니다.
유용하게 측정된 개선 없이 문구만 바뀌는 것은 성공 주장으로 보지 않습니다.

2026-09-23 `gpt-6-sol` 실행은 9월 16일 영문 실행(이전 `gpt-5.6-luna` 판)처럼 두 언어 모두 baseline만 반환했습니다.
영문 0.979, 국문 0.938이며 각각 약 4.5분 걸렸습니다. 실행마다 내부 초안 4개를 3건짜리 미니 배치로 평가했지만 후보로 반환하지 않았습니다.
일반 중단 문구는 모든 후보가 만점이라고 표시했지만, 국문 baseline은 D05 relevance(2)가 실패했고 영문 미니 배치는 D01·D05·D06 relevance가 실패했습니다.
9월 16일 국문 실행은 별도로 실행한 baseline과 두 후보를 남겼습니다.
상태 문구 대신 개별 행을 확인하고 영문 점수를 국문 결과로 옮기지 않습니다.

**업로드한 열뿐 아니라 실제 judge 입력을 확인합니다.** 각 평가자의 `sample.input`과
고정한 dataset을 비교합니다. 9월 23일 두 언어 실행에서도, 9월 16일 영문 baseline과 국문 baseline·두 후보처럼
Groundedness의 `context`에 원래 정책 대신 생성한 답변 자체가 들어갔습니다.
서비스가 6/6을 보고해도 자기 답변과의 비교는 원문 근거 검증이 아닙니다.
원래 점수·입력 hash를 보존하고 참조 binding을 무효로 표시하며 **이 결과로 승격하지 않습니다**.
촬영 결과를 좋게 만들려고 열·기준을 몰래 바꾸거나 새 run을 제출하지 않습니다.

`optimizer-review.txt`에 run, baseline/candidate ID, 관찰, 선택 후보 또는
`pending-human-review`, 이유를 적습니다. AI가 사람의 검토를 사칭하지 않습니다.

## 6. 사람 승인 후에만 승격

<details>
<summary>선택 승격 — Optimizer 종료 뒤 자동으로 실행할 단계가 아닙니다</summary>

검토가 없으면 **미수행**으로 남깁니다.
명시적 승인 후 **Promote candidate → Promote to agent version**을 사용하고
새 실제 버전과 default 변경 여부를 기록합니다.
새 label로 확인한 다음 baseline으로 사용합니다.
이전 버전의 holdout 점수는 새 버전에 자동 적용되지 않습니다.

후보를 고정한 후에만 별도의 최종 인수에서 holdout을 사용합니다.
이 Optimizer 실행은 개발용으로 holdout을 열지 않습니다.

</details>

## 이후 선택 기능

함수 설명 최적화는 실제 함수 실행 검증이 아닙니다.
Prompt Agent 함수는 client에서 실행되며 optimizer는 그 최적화 중 함수를 실행할 수 없습니다.
Hosted 최적화는 optimizer-ready code와 baseline configuration이 필요하고 실제 도구를 반복 실행할 수 있습니다.
read-only 합성 도구와 검토된 비용을 갖춘 별도 준비 workspace에 보관합니다.
이 portal 실습에 flag 하나를 붙인 것과 같지 않습니다.

**다음:** [대화 평가](conversation-evaluation.md), [C 모듈 선택](../../paths/c-advanced.md), 또는 [Lab 11 인계](../11-capstone.md).
[Prompt wizard](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-optimize-prompt-agent) ·
[Agent별 제약](https://learn.microsoft.com/azure/foundry/agents/concepts/agent-optimizer-overview) ·
[비용 계산](https://learn.microsoft.com/azure/foundry/agents/concepts/agent-optimizer-costs).
