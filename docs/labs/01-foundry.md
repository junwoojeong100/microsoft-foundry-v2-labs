# Lab 01. Foundry를 이해하고 프로젝트 준비하기

**완료 목표:** Foundry, Agent Framework, 모델 배포, 에이전트의 관계를 설명합니다.

이전: [Lab 00](00-start.md) · 다음: [Lab 02](02-models.md)

## 먼저 네 가지를 구분하기

| 용어 | 쉬운 설명 | 이 실습에서의 예 |
|---|---|---|
| Foundry 리소스 | Azure에서 AI 서비스를 운영하는 자원 | 실습용 Foundry account |
| 프로젝트 | 에이전트·연결·평가를 함께 관리하는 작업 공간 | 한빛기술 실습 프로젝트 |
| 모델 배포 | 특정 모델·버전·SKU를 호출할 수 있게 한 구성 | 강사가 정한 `workshop-chat` 같은 이름 |
| 에이전트 | 모델에 지침·도구·실행 방식을 붙인 업무 단위 | 출장 규정 안내 도우미 |

**Foundry는 클라우드 플랫폼, Microsoft Agent Framework(MAF)는 코드로 에이전트와
워크플로를 만드는 오픈소스 SDK**입니다. MAF를 로컬에서 실행하더라도 그 안의 모델 호출은
Azure에서 과금될 수 있습니다.

```mermaid
flowchart TD
    S["Azure 구독 · 비용과 관리 범위"] --> R["Resource Group"]
    R --> F["Foundry 리소스"]
    F --> D["모델 배포 · 실제 호출 이름"]
    F --> P["Foundry 프로젝트"]
    P --> A["에이전트와 버전"]
    P --> C["지식·도구 연결"]
    P --> E["평가·관측"]
    D --> A
```

## 1. 강사가 준비한 환경 확인

1. `https://ai.azure.com`에서 현재 Foundry 경험과 실습 프로젝트를 엽니다.
2. 프로젝트 이름, 리소스 이름, 연결된 모델 배포를 워크시트에 적습니다.
3. 같은 프로젝트에서 에이전트·모델·평가/관측 기능이 어디에 있는지 찾아봅니다.
4. 메뉴 이름은 언어와 배포 시점에 따라 달라질 수 있습니다. **메뉴 위치보다
   “프로젝트의 모델 배포 목록”처럼 확인할 대상**을 기준으로 이동합니다.
5. classic Hub 기반 프로젝트나 과거 threads/runs 코드를 보게 되면
   [마이그레이션 지도](../reference/migration.md)를 확인합니다. 서로 다른 API를 섞지 않습니다.

## 2. 환경이 없는 경우 — 강사/관리자만 먼저 수행

참가자 수업 시간에 포함하지 않는 준비 단계입니다.

1. 실습용 Azure 구독과 전용 Resource Group을 정합니다.
2. [Foundry 공식 시작 가이드](https://learn.microsoft.com/azure/foundry/quickstarts/get-started-code)에
   따라 Foundry 리소스와 현재 프로젝트를 만듭니다.
3. 리전을 선택하기 전에 필요한 **모델/SKU/할당량**을 확인합니다.
   Hosted를 쓸 경우에는 [Hosted 지원 리전](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)도
   별도로 확인합니다. 두 목록이 항상 같지는 않습니다.
4. 모델을 배포하고, 참가자에게 정확한 배포 이름을 전달합니다.
5. 프로젝트에 필요한 참가자 역할을 부여하고 반영을 기다립니다.
6. 한 명의 학습자 계정으로 실제 모델 호출을 확인합니다.
7. Search·Application Insights·Hosted는 사용할 모듈에만 준비합니다.

리소스를 만들 수 있다고 모델을 호출할 수 있는 것은 아닙니다. **관리 평면과 데이터
평면의 권한이 다릅니다.** 실습자 모두에게 구독 Owner를 부여하지 않습니다.

## 3. 최소 권한의 출발점

| 역할 | 권한의 출발점 | 범위 |
|---|---|---|
| 학습자: 에이전트·평가 개발 | `Foundry User` | 실습 프로젝트 |
| 기존 에이전트 호출만 | `Foundry Agent Consumer` | 해당 에이전트 |
| 기존 프로젝트에 Hosted 배포 | `Foundry Project Manager` 등 배포 가이드의 권한 | 해당 프로젝트 |
| 리소스·역할 준비 담당자 | 생성 권한 + 필요한 역할 할당 권한 | 실습 전용 범위 |
| 로그 조회자 | `Log Analytics Reader` 등 | 연결된 관찰 리소스 |

역할 이름이 아직 `Azure AI User`처럼 보일 수 있습니다. 현재 이름 변경은 기존 역할 ID를
바꾸지 않습니다. 필요한 추가 권한과 역할 ID는 [공식 RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)를
확인합니다. 사용자, Search managed identity, Hosted agent identity는 서로 다른 주체입니다.

## 4. endpoint 혼동 없애기

| 용도 | 모양 |
|---|---|
| 프로젝트 SDK | `https://<account>.services.ai.azure.com/api/projects/<project>` |
| 계정의 Azure OpenAI API | `https://<account>.openai.azure.com/openai/v1/` |
| Azure AI Search | `https://<search>.search.windows.net` |
| 브라우저 포털 | `https://ai.azure.com` — **SDK endpoint가 아님** |

프로젝트 endpoint에서 `/api/projects/<project>`를 지우지 않습니다.
이 랩의 기본 추론은 프로젝트 SDK가 인증과 endpoint를 처리합니다.
다른 endpoint로 자동 우회하거나 토큰 audience를 추측해 바꾸지 않습니다.

## 완료 확인

### 실제 포털 화면

![Sweden Central 새 환경의 클라우드 사전 점검](../assets/live-20260913-swc/031-cloud-doctor.png)

기존 실습 프로젝트를 사용한 실제 화면입니다. 계정 식별자는 가렸습니다.
[전체 실행 기록](../live-run.md)에서 초기 환경과 수행 범위를 확인합니다.

“모델을 바꿔도 프로젝트의 지식과 평가 기준을 남길 수 있나요?”에 답해 보세요.
모델 배포는 바꿀 수 있지만 지식·지침·평가·권한을 자동으로 검증해 주는 것은 아닙니다.
그래서 뒤의 모듈에서 같은 데이터와 기준을 다시 사용합니다.
