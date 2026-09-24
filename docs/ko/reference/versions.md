# 버전과 기능 경계

[English](../../reference/versions.md) | **한국어**

**현재 preset:** `gpt-6-sol` / `2026-09-22`와 별도 `gpt-6-sol-judge`(2026-09-23부터).
코드 버전 표시는 `2026.9.24`입니다.
아래 갱신된 의존성 조합은 2026-09-24에 설치하고 import 계약 검사와 mock SDK 테스트로 오프라인 확인한 뒤, 같은 날 저녁 실제 검증했습니다. 핵심 B 경로(영문·국문), `maf-evaluate`, `cloud-evaluate`, A2A, Insights scan 1회와 예제가 포함됩니다([결과](../live-run.md#review-refresh-live-verification)).
**호환성 확인일은 출시일이나 향후 지원 보장이 아닙니다.**
이 에디션은 Ignite 발표나 모든 tenant·지역의 가용성을 예측하지 않습니다.

## 확인한 계약

Python 직접 의존성은 아래의 호환 확인 조합을 유지합니다.
설치 SDK·transport stub 검사와 실제 Azure 실행은 서로 다른 근거입니다.

| 영역 | 계약 |
|---|---|
| 응답 모델 preset | 2026-09-23부터 `gpt-6-sol` / `2026-09-22`, 별도 `gpt-6-sol-judge`. 확인한 agent 경로와 녹화한 A/B 주요 단계 통과. 그날 `gpt-6-luna`는 agent 경로에서 실패. [모델 선택](model-choice.md) |
| 현재 Foundry | Projects SDK 2.x와 Responses. classic threads/runs와 분리 |
| MAF | `Agent`, 공급자 `model=`, sequential/concurrent/group-chat builder |
| Workflow host | 실제 `Workflow.as_agent()`와 ResponsesHostServer |
| 평가용 host | InvocationAgentServerHost, 로컬 POST `/invocations`, query-only 4필드 |
| 서비스 호출 계보 | workflow wrapper UUID가 아니라 실제 ChatResponse ID·model·usage |
| Middleware | 고정한 core 1.18.0은 `await call_next()`를 사용. 예전 `next(context)` 예제가 아님 |
| Functional workflow | 실험 기능. 필수 선행 조건이 아님 |
| 키워드 Search | REST `2024-07-01`. hybrid로 부르지 않음 |
| Hybrid | 실제 embedding 차원과 text/vector 요청. project/account API를 명시적으로 선택 |
| IQ GA | REST `2026-04-01`, intents/minimal/extractive |
| 확장 IQ | `2026-08-01-preview`, 별도 설정·승인 |
| IQ Chat 모델 + managed identity | 2026-09-15 확인: Search SMI → `gpt-5.6-luna`, `low` 계획 + `answerSynthesis`, HTTP 200. MI 자체는 Preview 기능이 아님. [정확한 설정과 요청 계약](iq-model-identity.md) |
| 첫 Chat preset | `iq-chat check/setup/ask`: 배포/모델 `gpt-5.6-luna`, 버전 `2026-07-09`, Search SMI, `2026-08-01-preview`, 별도 소유 chat base. 2026-09-23 Search가 GPT-6 모델을 받지 않아 이 preset은 응답 모델을 따르지 않음. 새 명령의 사전 검사는 읽기 전용이었고 이전 임시 base 추론은 별도 |
| Hosted 서비스와 패키지 | 서비스 상태와 prerelease Python 패키지 상태는 서로 독립 |
| Native 평가 | 실제 catalog의 initialization schema와 고정한 evaluator·version·threshold |
| Work IQ/Fabric/Toolbox | 서비스별 접근·ID·과금·Preview 조건을 따로 확인 |

## CLI 호환성

처음 환경은 azd 1.31.1과 microsoft.foundry 1.0.0-beta.2였습니다.
설치된 agents 1.0.0-beta.10과 projects 1.0.0-beta.6은 그 CLI와 호환되지 않는다고 표시됐습니다.
후속 실제 실행은 checksum을 확인한 **세션 전용 azd 1.34.0**을 사용했습니다.
공유 전역 CLI는 바꾸지 않았고 기존 확장은 호환 상태가 되었습니다.

배포 전에 실제 설치한 help·schema와 승인된 호환 조합을 확인합니다.
오류가 났다고 모든 패키지·확장을 무작정 업그레이드하지 않습니다.
[azd 설치](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)와
[Hosted quickstart](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)를 참고합니다.

## 고정한 직접 의존성

실행 가능한 제약의 기준은 `pyproject.toml`입니다.
2026-09-24 녹화와 실제 결과는 이전 pin을 사용했습니다:
`azure-ai-projects` 2.3.0, `openai` 2.54.0, `agent-framework-core` 1.17.0,
`agent-framework-foundry` 1.12.0, `agent-framework-orchestrations` 1.1.1,
`agent-framework-foundry-hosting` 1.0.0b260903, `mcp` 1.28.1.
그 실행 결과는 아래 갱신된 pin의 증거가 아닙니다.

| 패키지 | 버전 |
|---|---|
| `azure-ai-projects` | 2.6.1 |
| `azure-identity` | 1.25.3 |
| `openai` | 3.16.1 |
| `httpx` | 0.28.1 |
| `python-dotenv` | 1.2.3 |
| `agent-framework-core` | 1.18.0 |
| `agent-framework-foundry` | 1.13.0 |
| `agent-framework-orchestrations` | 1.1.1 |
| `agent-framework-foundry-hosting` | 1.0.0b260910 |
| `mcp` | 1.30.0 |

Hosted 패키지에는 Python 3.13을 사용합니다. 오프라인 코드는 3.13–3.14에서 테스트합니다.
공급자는 Projects SDK `>=2.2.0,<2.7.0`을 요구하며, 각 패키지의 최신 버전이 서로 호환된다는 보장은 없습니다.
OpenAI 3.x는 내부적으로 httpx2를 사용합니다. 이 워크숍의 고정 표면에서는 legacy httpx client도 계속 허용됩니다.
`azure-ai-projects` 2.7.0, `openai` 3.19.2, `agent-framework-core` 1.19.0,
`agent-framework-foundry` 1.13.1, `agent-framework-orchestrations` 1.2.0,
`agent-framework-foundry-hosting` 1.0.0b260918, `mcp` 2.2.0 같은 더 새 PyPI release가 있습니다.
이 에디션에서는 설치하거나 검증하지 않았습니다.
해석된 lock 파일은 작성 환경을 설명할 뿐 모든 OS나 원격 빌드를 설명하지 않습니다.
실제 원격 빌드에서 해석된 버전을 기록합니다.

## Retirement 날짜

오래된 Assistants, classic agent, portal Workflows는 서로 다른 일정으로 retire됩니다.
오래된 tutorial을 가져오기 전에는 [migration](migration.md#오래된-tutorial에-영향을-주는-retirement-날짜)을 확인합니다.

## 실제 실행에서 발견한 차이

- 전체 프로젝트 endpoint는 `/api/projects/...`를 유지합니다.
- 전체 `--agent-endpoint`에는 이미 프로토콜이 들어 있으므로 `--protocol`을 함께 넘기지 않습니다.
- session 매개변수를 추가해도 endpoint의 API-version query를 유지해야 합니다.
- 실제 환경에서 프로젝트 embeddings는 404를 반환했습니다. account API는 자동 대체가 아니라 명시적으로 선택했습니다.
- 프로젝트 요청은 AI audience를, 명시적으로 선택한 account 추론은 Cognitive Services audience를 사용합니다.
- App Insights에는 별도 audience와 의도한 구독·tenant의 자격 증명이 필요합니다.
- 이미 idle인 session은 충돌하는 중지 요청을 다시 보내지 않고 확인합니다.

## 수업 전에 고정하기

의존성, 오프라인·SDK 계약, 실제 모델 요청 하나, 모델·SKU·지역·quota·비용, 실제 생성된 설정을 확인합니다.
버전이 바뀌면 관련 명령·코드·데이터·가이드·평가를 다시 확인합니다.
공식 출처와 비교 기준은 [출처](sources.md)에 있습니다.
