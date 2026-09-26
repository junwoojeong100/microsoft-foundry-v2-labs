# 출처와 통합 계보

[English](../../reference/sources.md) | **한국어**

**원본 모듈의 학습 구조를 통합했고, 실행 결과까지 물려받았다고 주장하지 않습니다.**
확인일: 2026-09-15. 외부 리포의 main이 바뀌어도 아래 커밋은 고정된 비교 기준입니다.
2026-09-24 확인으로 표시한 새 공식 근거 행은 이번 review refresh를 반영하며, 새 워크숍 실행을 뜻하지 않습니다.
원본 기능의 v2 대체 위치와 미실행 게이트는 [통합·아카이브 기준](consolidation.md)에 구분했습니다.

별도 [9월 26일 공개 실습 비교](quality.md#public-reference-sample)에는 GitHub 참고 리포 7개를 불변 커밋으로 고정했습니다.
코드·실행 결과를 가져오거나 전체 순위를 매긴 것이 아니라 학습 방식을 비교한 것입니다.

## 통합한 사용자 소유 원본

| 원본 | 확인 커밋 / 커밋 날짜 | 반영 범위 |
|---|---|---|
| [microsoft-foundry-labs](https://github.com/junwoojeong100/microsoft-foundry-labs/tree/23e831f367b37d41ea1ad1df47f22b076bc372ff) | `23e831f367b37d41ea1ad1df47f22b076bc372ff` / 2025-12-14 | 기존 7개 주제와 포털/코드 이원 경로 |
| [foundry-evaluation](https://github.com/junwoojeong100/foundry-evaluation/tree/0b91e47f88ca4d1a5e1dd961d45ea6b40afbb33b) | `0b91e47f88ca4d1a5e1dd961d45ea6b40afbb33b` / 2026-09-15 | 형식이 고정된 Hosted matrix, 보존한 실패·계보, trace, native 평가 |
| [foundry-maf-workshop](https://github.com/junwoojeong100/foundry-maf-workshop/tree/d07c614a616446e63ee50b0b34540b5481aff5b2) | `d07c614a616446e63ee50b0b34540b5481aff5b2` / 2026-07-13 | 모델 SDK, MAF 함수, code deployment 학습 순서 |
| [agent-framework-labs](https://github.com/junwoojeong100/agent-framework-labs/tree/cca14163def4c88616dcd4c93fcfd6441fb08f30) | `cca14163def4c88616dcd4c93fcfd6441fb08f30` / 2026-09-15 | MAF builder, Hosted adapter, MCP 패턴 |
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
| IQ 모델 identity | [포털 keyless 모델 설정](https://learn.microsoft.com/azure/search/get-started-portal-agentic-retrieval#create-a-knowledge-base) · [모델/source/API 지원](https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-create-knowledge-base) | Search identity, `Cognitive Services User`, source별 LLM 모드 |
| IQ Preview 요청 | [2026-08-01-preview retrieve](https://learn.microsoft.com/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true) | `messages`, 계획·합성, 실측 `maxOutputSize`; endpoint/schema 차이 기록 |
| Search 실습 | [Agentic retrieval quickstart](https://learn.microsoft.com/azure/search/search-get-started-agentic-retrieval?pivots=python) | index·semantic·identity·비용 |
| 평가 입력 | [Cloud evaluation datasets](https://learn.microsoft.com/azure/foundry/observability/how-to/cloud-evaluation-datasets) | item schema, inline `file_content` |
| 평가 출력 | [Cloud evaluation results](https://learn.microsoft.com/azure/foundry/observability/how-to/cloud-evaluation-results) | run status, 모든 output page, native score |
| 자동 trace 데이터 | [Traces to dataset](https://learn.microsoft.com/azure/foundry/observability/how-to/traces-to-dataset) | Preview, SDK/권한 조건 |
| Hosted 시작 | [Quickstart](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent) | code deployment, 기존/새 프로젝트 정리 차이 |
| Hosted 운영 | [Concepts](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents) | 서비스 GA, 리전, session별 scaling/billing |
| Trace | [Tracing setup](https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup) | App Insights 연결, 민감 데이터·권한; 2026-09-24 확인 |
| Agent Insights | [Insights](https://learn.microsoft.com/azure/foundry/observability/how-to/agent-insights) | Preview trace scan, judge model, 연결 trace, 역할 요구 사항; 2026-09-24 확인 |
| Agent 구성·게시 | [Configure](https://learn.microsoft.com/azure/foundry/agents/how-to/configure-agent) · [Copilot/Teams 게시](https://learn.microsoft.com/azure/foundry/agents/how-to/publish-copilot) | 안정 endpoint, active version, Agent Applications와 M365 게시 경계; 2026-09-24 확인 |
| Workflows retirement | [Workflow concepts](https://learn.microsoft.com/azure/foundry/agents/concepts/workflow) | Portal Workflows visual Preview는 2026-12-01 retire. Microsoft Agent Framework 사용; 2026-09-24 확인 |
| Classic agents retirement | [Threads/runs/messages](https://learn.microsoft.com/azure/foundry-classic/agents/concepts/threads-runs-messages) | Classic agents는 2027-03-31 retire; 2026-09-24 확인 |
| Assistants retirement | [Assistants code interpreter](https://learn.microsoft.com/azure/foundry-classic/openai/how-to/code-interpreter) | Azure OpenAI Assistants API는 2026-08-26 retire; 2026-09-24 확인 |
| Classic agent migration | [Migration guide](https://learn.microsoft.com/azure/foundry/agents/how-to/migrate) | classic agent에서 현재 Foundry agent로 이전; 2026-09-24 확인 |
| Work IQ | [Knowledge source](https://learn.microsoft.com/azure/search/agentic-knowledge-source-how-to-work-iq) | delegated 사용자, 사용량 과금, user assertion, customer-owned app과 federated credential, 행동 가능성 |
| Workflow를 agent로 | [Using workflows as agents](https://learn.microsoft.com/agent-framework/workflows/as-agents) | start executor는 `list[Message]`를 받음. 실제 `.as_agent()`를 쓰고 builder 동작 보존 |
| Hosted adapter | [Foundry Hosted Agents](https://learn.microsoft.com/agent-framework/hosting/foundry-hosted-agent) | 서비스 GA와 prerelease Python 패키지를 구분, Responses와 Invocations |
| Functional workflow | [Functional workflow API](https://learn.microsoft.com/agent-framework/concepts/workflows/functional) | 실험 기능. 필수 선행 조건이 아님 |
| MAF 평가 | [Foundry evaluation integration](https://learn.microsoft.com/agent-framework/integrations/by-component/evaluation/microsoft-foundry) | 기존 응답 평가와 agent-target 평가를 구분 |
| Agent-target 평가 | [Evaluate agents](https://learn.microsoft.com/azure/foundry/observability/how-to/evaluate-agent) | 서비스가 target을 다시 호출하는 별도 경로 |
| Hybrid query | [Hybrid query](https://learn.microsoft.com/azure/search/hybrid-search-how-to-query) | text와 vector를 함께 전달 |
| Toolbox | [MAF FoundryToolbox](https://learn.microsoft.com/agent-framework/integrations/by-component/tools/foundry-toolbox) | 관리형 MCP lifecycle과 준비된 연결 조건, prerelease |
| Fabric IQ | [Tool guide](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/fabric-iq) | 자산별 delegated/OBO ID와 Data Agent MCP의 app-only ID 구분 |
| 운영·되풀이 평가 | [Monitoring dashboard](https://learn.microsoft.com/azure/foundry/observability/how-to/how-to-monitor-agents-dashboard) | batch·trace·되풀이 sampling의 조건이 각각 다름 |
| AI-103 / AI-102 | [AI-103 study guide](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-103) · [AI-102 study guide](https://learn.microsoft.com/credentials/certifications/resources/study-guides/ai-102) · [retirement announcement](https://learn.microsoft.com/partner-center/announcements/2026-june) | AI-103 기술 비중과 AI-102 retirement; 2026-09-24 확인 |
| Learn path와 Applied Skills | [Develop AI agents on Azure](https://learn.microsoft.com/training/paths/develop-ai-agents-on-azure/) · [APL-0302](https://learn.microsoft.com/credentials/applied-skills/resources/study-guides/apl-0302) | 다음 학습 path와 task 평가; 2026-09-24 확인 |
| Foundry capability map | [Capabilities](https://learn.microsoft.com/azure/foundry/concepts/capabilities) | 전문 기능 범위 지도; 2026-09-24 확인 |
| Grok Responses 지원 | [Use Grok models](https://learn.microsoft.com/azure/foundry/foundry-models/how-to/use-foundry-models-grok) | Chat Completions와 Responses 지원 문서화. Structured Outputs는 배포별 확인 필요; 2026-09-24 확인 |
| Foundry Dev Pack | [Announcement](https://devblogs.microsoft.com/foundry/foundry-devpack-announcement/) · [Installer](https://aka.ms/foundrydevpack) | 현재 Foundry tooling bundle 설치; 2026-09-24 확인 |
| Microsoft Foundry skill | [Use the skill](https://learn.microsoft.com/azure/foundry/how-to/develop/use-microsoft-foundry-skill) | coding agent의 Foundry workflow 통합; 2026-09-24 확인 |
| Voice-based prompt agents | [Quickstart](https://learn.microsoft.com/azure/foundry/agents/quickstarts/prompt-voice-agent) | Portal voice quickstart. Python SDK 지원은 이 edition의 pin 밖; 2026-09-24 확인 |
| Content Understanding | [Overview](https://learn.microsoft.com/azure/ai-services/content-understanding/overview) | 전문 문서/receipt extraction 설계 경계; 2026-09-24 확인 |
| Web IQ preview tool | [azure-ai-projects release history](https://pypi.org/project/azure-ai-projects/) | `WebIQPreviewTool`은 2.6.0에서 추가; 2026-09-24 확인 |

패키지 버전은 PyPI 공식 release metadata와 대조했습니다. 문서의 `Unreleased` 절을 설치 가능한 릴리스로 보지 않았습니다.
공식 문서의 오래된 `ChatAgent`/middleware 예제는 설치한 SDK와 다를 수 있으며, SDK 계약 검사는 설치본의 `Agent`, `ChatContext`,
`Workflow.as_agent`와 host route를 대조합니다. 확인일은 모든 구독·지역의 지원을 보장하지 않습니다.
본문 예시의 URL/ID/점수와 실제 실행 결과는 [검증 기록](validation.md)에서 구분합니다.
