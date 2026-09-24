# Foundry Insights: 반복되는 trace 패턴에서 검토된 변경까지

[English](../../../labs/extensions/agent-insights.md) | **한국어**

**C 경로, 선택 Preview — 2026-09-24 확인.**
Insights는 최근 Foundry agent trace를 분석해 반복되는 동작 패턴을 검토 대상으로 제안합니다.
이는 의사 결정 보조 자료이지 정답이 아니며, 평가 workflow를 대체하지 않습니다.

**근거 상태:** 2026-09-24에 녹화된 영문 Lab 03 agent를 대상으로 포털이 아닌 Python SDK로 on-demand scan을 1회 실행했습니다. 결과는 아래에 있으며 녹화는 없습니다.

**준비:** 학습자 본인의 Lab 03 Prompt Agent, 연결된 Application Insights, 최근의 대표적인 합성 dev trace,
담당자가 준비한 `gpt-6-sol-judge` judge 배포, 담당자가 준비한 역할. 학습자는 역할을 부여하지 않습니다.
**완료:** Insight 하나를 연결 trace와 합성 정책에 대조해 검토하고 사람의 결정을 기록합니다.
**중단:** 누락된 선행 조건을 기록합니다. 대표 trace가 너무 적으면 **not enough traces**라고 적습니다.

**첫 회차:** 1–5절. Insights를 채우려고 새 traffic을 만들지 않습니다.
Lab 03과 이후 Lab 07 dev 확인에서 이미 생긴 합성 dev traffic/trace를 사용합니다.

## 1. 담당자가 준비한 선행 조건 확인

환경 담당자는 수업 전에 접근 권한을 준비합니다.

| 선행 조건 | 담당자가 준비할 요구 사항 |
|---|---|
| Application Insights | scan 전에 Foundry 프로젝트에 연결 |
| 학습자 접근 | prompt agent에 대한 Foundry User, 연결된 Application Insights에 대한 Monitoring Reader |
| 프로젝트 managed identity | 연결된 Application Insights에 대한 Monitoring Reader |
| 보호된 content table | `AppGenAIContent`가 보호되는 경우 Privileged Monitoring Data Reader |
| Judge 배포 | 프로젝트 managed identity가 `gpt-6-sol-judge`를 호출 가능 |
| Trace 데이터 | 학습자 본인 agent의 최근 합성 대표 trace |

이 모듈에서 역할을 추가하거나, 프로젝트 identity를 바꾸거나, 기본 구독을 바꾸지 않습니다.
별도 client-side tracing을 구현하지 않은 로컬 MAF 실행은 Foundry server-side trace를 만들지 않습니다.

## 2. Portal에서 제한된 scan 시작

1. Foundry를 엽니다.
2. 상단 **빌드** → 왼쪽 **에이전트**로 이동합니다.
3. 본인의 Lab 03 Prompt Agent를 엽니다.
4. **Insights** 탭을 엽니다(UI 언어에 따라 표시 이름이 다를 수 있음).
5. Judge model **`gpt-6-sol-judge`**를 선택합니다.
6. **Run scan now**를 선택합니다.

첫 scan은 최근 trace를 돌아봅니다. 페이지가 trace가 너무 적다고 표시하면 **not enough traces**라고 기록하고 멈춥니다.
더 흥미로운 Insight를 만들려고 추가 prompt를 보내지 않습니다.

Python SDK는 `azure-ai-projects` 2.6.x에서 `beta` Agent Insight 작업을 노출하지만,
이 워크숍 모듈은 portal을 사용하며 SDK 코드를 추가하지 않습니다.

## 3. Severity만 보지 말고 Insight 하나 검토

반환된 Insight 하나를 열고 다음을 보존합니다.

| 필드 | 확인할 것 |
|---|---|
| Category와 severity | triage 힌트일 뿐이며 severity는 위험 평가를 대체하지 않음 |
| 연결/highlight trace | 실제 trace 근거를 열어 Insight 요약과 비교 |
| Likely cause | 원인이 연결 trace에서 따라오는지 확인 |
| Proposed action | 합성 정책의 범위·날짜·인용·승인 경계를 보존하는지 확인 |

AI가 생성한 Insight는 불완전하거나 오래됐거나 틀릴 수 있습니다.
사람이 trace 근거를 검토하기 전에는 Insight를 결함으로 보고하지 않습니다.

## 4. 사람의 결정 선택

`insights-review.txt`에 다음 중 하나를 기록합니다.

| 결정 | 경계 |
|---|---|
| Evaluate | 기존 합성 정책 시나리오에서 파생한 dev 평가 사례를 추가하거나 우선순위 지정 |
| Change instructions in a new version | 검토된 candidate version 생성. 현재 baseline을 덮어쓰지 않음 |
| Route | 데이터·도구·접근·운영 담당자에게 전달 |
| No action | Insight가 실행 가능하지 않거나 근거가 부족하면 evidence와 이유 보존 |

결정이 instruction 변경이라면 Lab 07 절차로 dev에서만 테스트합니다.
Holdout은 candidate가 고정된 뒤에만 엽니다.

## 2026-09-24 확인 결과

| 항목 | 관찰값 |
|---|---|
| 기간 / trace | 기본 7일 lookback, 기간 안의 trace 22개를 모두 분석 |
| 소요 시간 / judge token | 약 2분, `gpt-6-sol-judge`에서 227,246 token(입력 214,651, 출력 12,595) |
| Insight | 활성 4개: **Output quality** 2개(medium 1, low 1), **Cost & tokens** 2개(low) |
| 버전 | 4개 중 3개는 지침 저장 전 Web search 도구가 공개 검색(`execute_tool web.run`)을 실행한 **버전 1**에 관한 것이고, 1개는 저장한 **버전 2**에 관한 것 |
| 버전 2 finding | `TRAVEL-2026`은 올바르게 적용했지만 지침이 요구하는 적용일 설명을 자주 빠뜨림 |
| 제안된 수정 | 반환되지 않음 |

교훈: 조치하기 전에 `agent_version`을 확인합니다. 이미 지난 버전에 대한 finding은 지금 적용할 변경이 아닙니다.
작은 agent라도 scan이 token을 많이 쓸 수 있습니다. 버전 2 finding은 dev 평가 사례로 삼을 만한 후보이지 판정이 아닙니다.
먼저 연결된 trace와 합성 정책으로 확인합니다.

<details>
<summary>확인에 사용한 SDK 대안(Preview, `azure-ai-projects` 2.6.1)</summary>

```python
project = AIProjectClient(endpoint=endpoint, credential=credential, allow_preview=True)
monitors = project.beta.agent_insight_monitors
monitor = monitors.create(
    AgentInsightMonitorCreate(
        agent_name=agent, enabled=False, model_deployment_name="gpt-6-sol-judge"
    )
)
monitors.begin_create_run(monitor.id, AgentInsightRunCreate(lookback_hours=168)).result()
insights = list(monitors.list_insights(monitor.id, include_details=True))
monitors.delete(monitor.id)  # removes the monitor, its runs and insights
```

`enabled=False`는 scheduled generation을 꺼 둡니다. 보관할 insight를 저장한 뒤에만 monitor를 삭제하세요.

</details>

## 5. 비용과 정리

Insight 생성은 선택한 judge model을 호출하므로 비용이 생길 수 있습니다.
scan 시각, judge 배포, 예약 생성이 켜졌는지를 기록합니다.
실험을 위해 예약 생성을 켰다면 담당자가 명시적으로 유지하지 않는 한 끝나기 전에 일시 중지합니다.

**다음:** [대화 평가](conversation-evaluation.md), [모델 운영](model-operations.md), 또는 [C 모듈 선택](../../paths/c-advanced.md).

[Agent Insights](https://learn.microsoft.com/azure/foundry/observability/how-to/agent-insights) ·
[Tracing 설정](https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup).
