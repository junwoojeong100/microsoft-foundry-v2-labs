# 출처와 통합 계보

**원본 모듈의 학습 구조를 통합했고, 실행 결과까지 물려받았다고 주장하지 않습니다.**
확인일: 2026-09-13. 외부 리포의 main이 바뀌어도 아래 커밋은 고정된 비교 기준입니다.

## 통합한 사용자 소유 원본

| 원본 | 확인 커밋 / 커밋 날짜 | 반영 범위 |
|---|---|---|
| [microsoft-foundry-labs](https://github.com/junwoojeong100/microsoft-foundry-labs/tree/23e831f367b37d41ea1ad1df47f22b076bc372ff) | `23e831f367b37d41ea1ad1df47f22b076bc372ff` / 2025-12-14 | 기존 7개 주제와 포털/코드 이원 경로 |
| [foundry-evaluation](https://github.com/junwoojeong100/foundry-evaluation/tree/a73c7b89169aff457b55647e4e68d1610b029860) | `a73c7b89169aff457b55647e4e68d1610b029860` / 2026-09-11 | learning loop, dev/holdout, 실패·원문·평가 계보 |
| [foundry-maf-workshop](https://github.com/junwoojeong100/foundry-maf-workshop/tree/d07c614a616446e63ee50b0b34540b5481aff5b2) | `d07c614a616446e63ee50b0b34540b5481aff5b2` / 2026-07-13 | 모델 SDK, MAF 함수, code deployment 학습 순서 |
| [agent-framework-labs](https://github.com/junwoojeong100/agent-framework-labs/tree/1d3e3652784a421eeeed4c7f3f6b9476208ceb07) | `1d3e3652784a421eeeed4c7f3f6b9476208ceb07` / 2026-07-11 | FoundryChatClient, workflow builder, MCP 패턴 |
| [microsoft-iq-on-foundry](https://github.com/junwoojeong100/microsoft-iq-on-foundry/tree/fa16c84f9800377823edd9aea1cb20d6a56a1edf) | `fa16c84f9800377823edd9aea1cb20d6a56a1edf` / 2026-07-25 | IQ/Toolbox 구분, read-only 기본, 실제 M365 연결의 승인 경계 |

이 에디션의 시나리오·합성 데이터·통합 코드·문서는 새로 구성했습니다.
MIT가 명시된 MAF Workshop/Agent Framework 원본의 저작권 표기는 루트 MIT 표기에
유지했습니다. 원본 전체나 영상/이미지를 일괄 복사·재배포하지 않았습니다.
별도 LICENSE가 확인되지 않은 원본 전체에 MIT가 적용된다고 주장하지 않습니다.

## 공식 근거

날짜는 문서의 표시/편집 시점으로, 기능 출시일과 같지 않습니다.

| 주제 | 공식 출처 | 확인한 중요 계약 |
|---|---|---|
| 현재 Foundry와 classic | [Migration](https://learn.microsoft.com/azure/foundry/how-to/navigate-from-classic) | SDK 2.x, Agents v2, 이행/종료 경계 |
| Prompt Agent | [Quickstart](https://learn.microsoft.com/azure/foundry/agents/quickstarts/prompt-agent) | `create_version`, 프로젝트·agent client |
| 권한 | [Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) | Foundry 역할 이름, 관리/데이터 평면 |
| MAF Python | [2026 significant changes](https://learn.microsoft.com/agent-framework/support/upgrade/python-2026-significant-changes) | `FoundryChatClient`, `FoundryAgent`, `model=` |
| MAF 샘플 | [python-1.18.0](https://github.com/microsoft/agent-framework/tree/python-1.18.0/python/samples) | 실제 provider·함수 도구 API |
| Foundry IQ 개념 | [What is Foundry IQ?](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq) | IQ별 역할, 포털/REST 계약 차이 |
| IQ 버전 | [Agentic retrieval migration](https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-migrate) | GA `2026-04-01`와 `2026-08-01-preview` |
| IQ GA REST | [Retrieve](https://learn.microsoft.com/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-04-01&preserve-view=true) | OData 경로, intents, references/activity |
| Search 실습 | [Agentic retrieval quickstart](https://learn.microsoft.com/azure/search/search-get-started-agentic-retrieval?pivots=python) | index·semantic·identity·비용 |
| 평가 입력 | [Cloud evaluation datasets](https://learn.microsoft.com/azure/foundry/observability/how-to/cloud-evaluation-datasets) | item schema, inline `file_content` |
| 평가 출력 | [Cloud evaluation results](https://learn.microsoft.com/azure/foundry/observability/how-to/cloud-evaluation-results) | run status, 모든 output page, native score |
| 자동 trace 데이터 | [Traces to dataset](https://learn.microsoft.com/azure/foundry/observability/how-to/traces-to-dataset) | Preview, SDK/권한 조건 |
| Hosted 시작 | [Quickstart](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent) | code deployment, 기존/새 프로젝트 정리 차이 |
| Hosted 운영 | [Concepts](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents) | 서비스 GA, 리전, session별 scaling/billing |
| Trace | [Tracing setup](https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup) | App Insights 연결, 민감 데이터·권한 |
| Work IQ | [Knowledge source](https://learn.microsoft.com/azure/search/agentic-knowledge-source-how-to-work-iq) | delegated 사용자, usage billing, 행동 가능성 |

패키지 버전은 각 프로젝트의 PyPI 공식 release metadata와 대조했습니다.
문서의 `Unreleased` 절을 설치 가능한 릴리스로 가정하지 않았습니다.
본문 예시의 URL/ID/점수와 실제 실행 결과는 [검증 기록](validation.md)에서 구분합니다.
