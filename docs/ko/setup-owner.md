# 환경 담당자 준비

[English](../setup-owner.md) | **한국어**

**학습자가 준비를 시작하기 전에 Azure 환경을 준비합니다.** 이 페이지는 구독/프로젝트 담당자나 강사용이며, 다음 랩 안에 숨겨 둔 선행 조건이 아닙니다.

**혼자 학습하나요?** 본인이 담당자 역할도 맡습니다. 먼저 [혼자 학습](#self-study)을 따르고, 그 뒤의 [수업 담당자 체크리스트](#class-owner-checklist)는 수업·B Search·선택 준비를 더합니다.

<a id="self-study"></a>

## 혼자 학습: A 경로 환경을 직접 준비하기

**수업 담당자가 넘겨줄 것을 직접 갖춥니다. 본인 프로젝트, 정확한 `gpt-6-sol` 배포, 본인 역할, 설정 카드, Lab 05 터미널입니다.**
Lab 00 전에 한 번만 진행합니다. 본인 구독에 유료 리소스를 만들며, 이 판에서 학습자 소요 시간을 재지 않았습니다.
포털 단계는 아래에 연결한 Microsoft Learn 문서를 따르며 2026-09-25에 확인했습니다. 워크숍 녹화는 미리 준비한 프로젝트를 사용했습니다.
괄호 안은 영문 UI 이름입니다.

**B를 혼자 학습하나요?** 1–5단계만 마친 뒤(B의 Lab 09에는 5단계가 필요) [B의 Search 서비스 준비](#search-service)를 진행합니다.
A의 6–7단계는 건너뜁니다. Search 준비 뒤 B 경로의 [준비](setup.md)로 돌아옵니다.

1. **구독.** Azure 구독에서 리소스를 만들고 역할을 할당할 수 있는 계정(예: 구독 **소유자(Owner)**)으로 `https://ai.azure.com`에 로그인합니다. 모델 호출 비용은 그 구독에 청구됩니다.
   **확인:** Foundry 포털이 열리고 상단의 **새 Foundry** 토글이 켜져 있습니다.
2. **프로젝트.** 왼쪽 위 프로젝트 이름을 선택한 뒤 새 프로젝트 만들기(영문 UI **Create new project**)를 선택합니다(프로젝트가 아직 없으면 포털이 만들기를 안내합니다).
   `mfv2-`로 시작하는 이름을 넣고 고급 옵션(**Advanced options**)을 열어 이 과정 전용 **새 리소스 그룹**을 만들고,
   `gpt-6-sol`을 제공하는 위치(**Location**, 이 판은 **Sweden Central** 사용)를 고른 뒤 만들기(**Create**)를 선택합니다
   ([공식 절차](https://learn.microsoft.com/azure/foundry/how-to/create-projects)).
   **확인:** 새 프로젝트의 **홈**에 **프로젝트 엔드포인트**가 보입니다. `https://<account>.services.ai.azure.com/...`의 `<account>` 부분이 Foundry 리소스 이름입니다.
3. **응답 모델.** 상단 **검색**(영문 UI **Discover**) → **모델**에서 **`gpt-6-sol`**을 검색해 열고 **배포** → 사용자 지정 설정(**Custom settings**)을 선택합니다.
   배포 이름은 **`gpt-6-sol`** 그대로 두고 모델 버전 **`2026-09-22`**를 고른 뒤 **배포**를 선택합니다
   ([공식 절차](https://learn.microsoft.com/azure/foundry/foundry-models/how-to/deploy-foundry-models)).
   `gpt-6-sol-judge`는 나중에 선택 Foundry 평가를 고를 때만 준비합니다.
   **확인:** **홈 → 배포 보기**에 `gpt-6-sol`, 버전 `2026-09-22`, **Succeeded**가 보입니다.
   그 위치에서 이 모델·버전을 제공하지 않거나 quota가 없으면 멈춥니다. 개인 로컬 텍스트 파일 `setup-attempts.txt`에
   구독·리소스 그룹·위치·Foundry 계정/프로젝트·정확한 오류·시각을 적습니다.
   모든 시도를 보존하고 인증정보는 기록하지 않습니다. 같은 위치의 [quota를 요청](https://aka.ms/oai/stuquotarequest)하거나,
   다른 위치의 필요한 모델/버전·quota·비용을 확인한 뒤 새 실습 전용 그룹으로 2단계를 다시 진행할 수 있습니다.
   새 그룹을 만들어도 이전 리소스가 삭제되는 것은 **아닙니다**. 다른 모델을 대신 배포하지 않습니다.
   여기서 준비를 중단한다면 Lab 11까지 기다리지 말고 지금 [정리 확인](reference/cleanup.md#self-study-cleanup)을 따릅니다.
4. **본인 역할.** 역할 할당 권한이 있는 계정으로 포털에서 프로젝트를 만들면 본인과 프로젝트의 관리 ID에
   새 Foundry 리소스의 **Foundry User**가 함께 부여됩니다([공식 RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#minimum-role-assignments-to-get-started)).
   **확인:** Azure 포털에서 새 Foundry 리소스 → **액세스 제어(IAM)** → **역할 할당**을 열고 본인 계정의 **Foundry User**
   (이전 이름 **Azure AI User**)를 찾습니다. 없으면 그 리소스에서 본인 계정에 [역할을 할당](https://learn.microsoft.com/azure/role-based-access-control/role-assignments-portal)합니다.
5. **추적, 선택.** Lab 09의 추적 확인을 하려면 **빌드 → 에이전트**의 **추적** 탭에서 연결(**Connect**)을 선택하고
   새 Application Insights 리소스를 만듭니다([공식 절차](https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup)). 로그 비용이 추가됩니다.
   Azure 포털에서 Application Insights와 연결된 **Log Analytics 작업 영역** 각각의 리소스 그룹을 확인합니다.
   실습 그룹과 다를 수 있습니다. 이름·그룹을 보관했다가 본인 경로의 개인 기록을 준비할 때 `operations-checklist.txt`에 적습니다.
   **확인:** 연결 완료 메시지가 나타납니다. 이 단계를 건너뛰면 Lab 09에서 `추적 미확인: <이유>`를 적습니다.
6. **파일과 설정값.** [준비 2–3절](setup.md#learner-files)을 진행합니다. 학습자 ZIP을 받고, 본인 포털에서 확인한 값으로 설정 카드를 채웁니다.
   `비용·권한 담당자:`에는 본인을 적습니다.
   `setup-attempts.txt`가 있다면 이 개인 증거 폴더에 보관하고, 모든 이전 그룹과 현재 상태·남은 비용·정리 담당자를
   `operations-checklist.txt` 4번에 추가합니다.
   추적을 설정했다면 `operations-checklist.txt` 4번에 로그 리소스 두 개와 각각의 실제 그룹을 추가합니다.
   **확인:** `session-notes.txt`의 **Lab 00 - 설정 카드** 구역이 모두 채워져 있습니다.
7. **Lab 05 터미널.** [Lab 00 B](labs/00-start.md#path-b) 1–5단계와 [Lab 02 B](labs/02-models.md#path-b) 1–3단계를 마치고
   [A 복귀 선택](labs/02-models.md#a-terminal-ready)으로 나갑니다. **정해진 시간의 A 경로를 시작하기 전에** 준비를 마칩니다.
   B의 나머지 단계로 계속 진행하지 않습니다.
   **확인:** `doctor --cloud`가 `gpt-6-sol` / `2026-09-22` / `Succeeded`를 보고하고, Lab 02 B가 `model.json`과 `answer-local.json`을 저장했습니다.

**준비 완료:** **1–7**단계를 마치고(5단계는 건너뛴 것으로 기록 가능) [준비 완료 체크](setup.md#5-시작-가능-여부)를 확인한 뒤
[Lab 00 A](labs/00-start.md#path-a)를 시작합니다. 설정 카드를 채운 것만으로 Lab 05 터미널이 준비되지는 않습니다.
단계가 실패하면 그 단계부터 해결한 뒤 진행합니다. 원인을 모르는 같은 오류 때문에 모델·리소스·프로젝트를 새로 만들지 않습니다.
**Lab 11 뒤:** 증거 폴더를 보관하고 이전 시도를 포함해 준비 중 만든 모든 그룹을 확인합니다.
각 그룹에 이 과정의 리소스만 있을 때만 Azure 포털에서 삭제합니다
(**리소스 그룹** → 본인 그룹 → **리소스 그룹 삭제**). 연결된 로그 리소스가 그 그룹 안에 있거나 함께 삭제됐다고 가정하지 않습니다.
Application Insights·Log Analytics·남은 비용은 [자습 정리 확인](reference/cleanup.md#self-study-cleanup)을 따릅니다.
B 경로로 이어 갈 계획이면 필요한 자원을 남겨 두고 담당자·계속 발생하는 비용을 기록합니다.

<a id="class-owner-checklist"></a>

## 수업 담당자 체크리스트

1. 전용 실습 구독·리소스 그룹과 필요한 모델 quota가 있는 리전을 선택합니다.
   [현재 Foundry 준비 가이드](https://learn.microsoft.com/azure/foundry/quickstarts/get-started-code)를 사용하고
   classic Hub/threads-runs 튜토리얼을 섞지 않습니다.
2. **`gpt-6-sol` / `2026-09-22`**를 배포 이름 **`gpt-6-sol`**로 준비하고 상태 `Succeeded`를 확인합니다.
   설명되지 않은 오류 뒤에 다른 모델을 새로 만들지 않습니다.
3. 학습자에게 필요한 Foundry 프로젝트/모델 권한을 줍니다.
   CLI의 배포 사전 조회에는 **실습 Foundry 계정의 Reader**도 필요합니다. 관리자뿐 아니라 학습자 계정으로 실제 호출을 점검합니다.
4. B의 GA Search/IQ 또는 선택 IQ Chat을 진행한다면 Basic 이상 Search, semantic/knowledge retrieval 사용 조건과
   합성 index를 작성할 사람의 Search 읽기/쓰기 권한을 준비합니다.
   아직 서비스가 없다면 [Search 서비스 준비 단계](#search-service)를 사용합니다.
   아래 역할 할당뿐 아니라 [Search 인증 확인](#search-authentication)도 완료합니다.
   새 복사본으로 시작하는 B 학습자에게는 **서비스·권한**을 준비하고, 새 학습자 prefix의 객체를 미리 만들지 않습니다.
   이미 seed한 객체를 제공한다면 승인된 대응 작업 폴더를 제공합니다. Endpoint/base 이름만으로 로컬 소유권 ledger가 생기지 않습니다.
5. **선택 모델 기반 IQ Chat에서만** Search의 system-assigned identity를 켜고, 별도의
   **`gpt-5.6-luna` / `2026-07-09`** 배포(이름 **`gpt-5.6-luna`**)를 준비합니다. 2026-09-23 Search knowledge base는 GPT-6 모델을 받지 않았습니다.
   모델의 Foundry 계정에서 **Search identity**에 `Cognitive Services User`를 부여합니다.
   사용자나 Hosted agent에 준 역할이 Search에 생기는 것은 아닙니다.
6. 아래 담당자 명령 전에 `.env`를 포함한 [Lab 00 B 설치](labs/00-start.md#b-코드--한-폴더-한-환경)를 완료합니다.
   Lab 05 방식을 하나도 받지 못한 학습자는 이 설치와 [Lab 02 B](labs/02-models.md#path-b)를 마친 뒤 돌아옵니다.
7. 수업 전에 Application Insights를 프로젝트에 연결해 server-side tracing을 켭니다. 코드 변경은 필요 없습니다.
   학습자에게 연결된 Application Insights 리소스의 **Log Analytics Reader**를 부여합니다. 보호된 테이블을 사용한다면 **Privileged Monitoring Data Reader**도 필요합니다.
   이제 핵심이 된 Lab 09 trace 단계에 필요합니다. 2026-09-24 확인: 실습 프로젝트에는 이미 Application Insights가 연결되어 있었고 관리형 agent 호출은 몇 분 안에 추적으로 나타났습니다. 학습자 전용 Log Analytics Reader 부여는 재시험하지 않았습니다.
8. 선택: A 학습자가 Lab 05에서 브라우저 Playground 옵션을 사용할 수 있도록 Lab 05 MAF workflow를 Hosted Agent로 배포합니다.
   별도 승인 뒤 [Lab 05 C](labs/05-workflows.md) / [Lab 08 6절](labs/08-hosted.md#6-maf-워크플로를-hosted-agent로-배포)만 사용합니다.
   학습자 언어의 **순차·local 검색·v2·Responses** workflow profile을 준비합니다. Invocations 평가 agent나
   Lab 03 Prompt Agent는 이 선택지가 아닙니다. 학습자에게 제공하기 전에 참가자 계정으로 실제 Playground 응답을 확인합니다.
   학습자에게 줄 hosted workflow agent 이름과 active version을 기록합니다. 2026-09-24에는 workflow agent가 로컬 Responses 요청 하나에 답했고, 이 확인을 위해 원격 배포는 하지 않았습니다.
9. 선택: 담당자/강사 PC에 [Foundry Dev Pack](labs/extensions/developer-toolkit.md)을 준비하고, 이후 `az`, `azd`, Foundry azd 확장, SDK, extension 버전을 고정해 기록합니다.
   이 판에서는 테스트하지 않았습니다.
10. 선택 lightweight 소스 배포: 큰 media 이력이 필요 없는 학습자에게 `docs/assets/`와 video 파일을 제외한 sparse checkout을 제공합니다.
    전체 저장소가 계속 원본입니다. [Lab 00](labs/00-start.md#source-folder)의 sparse pattern은 2026-09-24에 로컬 확인했습니다.
    `docs/assets/`와 `videos/`는 제외됐고 스크립트와 가이드는 남았습니다.

<a id="search-service"></a>

### Lab 00 전에 B의 Search 서비스 준비

**구독 소유자인 자습 학습자를 포함한 담당자 전용입니다. 기본 A에는 Search가 필요 없습니다.**
담당자가 이미 서비스를 제공했다면 그대로 두고 2–4단계를 확인합니다. 서비스를 하나 더 만들지 않습니다.
서비스 생성이나 과금·역할·네트워크 설정 변경은 담당자의 승인이 필요합니다.

1. Azure 포털에서 **리소스 만들기(Create a resource) → Azure AI Search**를 선택하고 [서비스 생성 양식](https://learn.microsoft.com/azure/search/search-create-service-portal)을 따릅니다.
   실습 구독·리소스 그룹, 전역에서 고유한 `mfv2-`로 시작하는 서비스 이름, **Basic** 요금제
   (또는 담당자가 승인한 상위 요금제), Confidential이 아닌 **Default** 컴퓨팅을 선택합니다.
   만들기 전에 [현재 리전 표](https://learn.microsoft.com/azure/search/search-region-support)에서 선택한 위치의
   **Agentic retrieval**과 **Semantic ranker**를 모두 확인합니다. 모델 제공 여부만으로 Search 기능의 제공 여부를 판단하지 않습니다.
   표시된 서비스 비용을 검토한 뒤 승인된 예산 안에서만 **검토 + 만들기(Review + create) → 만들기(Create)**를 선택합니다.
2. 생성에 성공하면 서비스의 **개요(Overview)**를 열어 구독·리소스 그룹·리전·요금제를 확인합니다.
   **URL**인 `https://<search>.search.windows.net`을 준비 카드의 Search endpoint와 이후 `.env`의 `AZURE_SEARCH_ENDPOINT` 값으로 사용할 수 있게 보관합니다.
   서비스 이름과 실제 그룹도 보관했다가 Lab 00에서 개인 기록을 준비하면 `operations-checklist.txt` 4번에 적습니다.
   담당자가 승인한 네트워크 접근을 사용하며, 접속하려고 공유 방화벽을 끄지 않습니다.
3. **설정(Settings) → 프리미엄 기능(Premium features)**에서 **Semantic ranker**와 **Knowledge retrieval**을 따로 확인합니다.
   새 전용 서비스는 한정된 기본 제공 사용량을 쓰도록 각 기능의 **Free** 플랜을 유지합니다. 이 플랜 때문에 Basic 서비스 자체가 무료가 되는 것은 **아닙니다**.
   기본 `2026-04-01` API의 유료 knowledge retrieval 동의는 semantic ranker와 별개입니다.
   **Standard** 기능 플랜은 별도 비용 승인이 필요합니다. 기본 제공량을 소진하면 멈추고 담당자에게 과금 오류를 확인하도록 요청합니다.
   오류를 우회하려고 공유 플랜이나 검색 방식을 바꾸지 않습니다.
   [Semantic ranker 과금](https://learn.microsoft.com/azure/search/semantic-how-to-enable-disable)과
   [Knowledge retrieval 과금](https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-enable-disable)을 확인하세요.
4. 아래 [토큰 인증 확인](#search-authentication)을 완료합니다. Search 서비스의 **액세스 제어(IAM)**에서
   [역할 할당 추가(Add role assignment)](https://learn.microsoft.com/azure/role-based-access-control/role-assignments-portal)로 실제 학습자 계정에
   **Search Service Contributor**와 **Search Index Data Contributor** 중 빠진 역할을 부여합니다. 그 서비스 범위에서 두 역할을 확인합니다.
   구독 Owner라는 이유만으로 Search 데이터 접근 권한이 생기지는 않습니다.

**준비 완료:** 의도한 서비스·endpoint·기능별 플랜·토큰 인증·작성자 역할 두 개를 확인했습니다.
B의 [준비](setup.md)로 돌아간 뒤 Lab 00을 진행합니다. 아래 선택 담당자 명령으로 계속 내려가지 않습니다.
여기서 데이터를 가져오거나 학습자 index를 미리 만들지 않습니다. [Lab 06 B](labs/06-knowledge.md#path-b)가
동봉한 합성 정책만 사용해 본인 객체를 만들고 소유권을 기록합니다.
위 공식 설정·과금 문서는 **2026-09-26**에 대조했으며, 새 Azure 실제 실행 검증은 아닙니다.

<a id="search-authentication"></a>

### Search 인증과 학습자 역할

**B와 선택 IQ Chat의 담당자 전용입니다.** Workshop은 API key가 아니라 **Microsoft Entra ID 토큰**으로 Search를 호출합니다.
서비스가 그 토큰을 허용해야 **하고**, 호출자에게 필요한 역할도 있어야 합니다. 역할만 할당해도 key 전용 서비스의 인증 설정이 바뀌지는 않습니다.

1. Azure 포털에서 정확한 **Search 서비스 → 설정(Settings) → 키(Keys)**를 열어 **API 액세스 제어(API access control)**를 확인합니다.
   화면에 표시되는 key를 복사하거나 공유하지 않습니다.
2. 새 전용 실습 서비스라면 권한이 있는 담당자가 **역할 기반 액세스 제어(Role-based access control)**를 선택합니다.
   기존 **둘 다(Both)** 설정도 ID 토큰을 허용하므로 공유 클라이언트에 key가 필요하면 그대로 둡니다.
   공유 서비스에서 **API Key**가 선택되어 있다면 멈추고 담당자의 승인된 전환을 기다립니다. 실습을 마치려고 다른 클라이언트의 인증을 끄지 않습니다.
3. **확인:** 설정이 **Role-based access control** 또는 **Both**입니다. 그다음 담당자 계정뿐 아니라
   학습자가 실제 로그인할 계정의 역할을 아래 표와 대조합니다. 토큰 인증을 켜는 것만으로 역할이 부여되지는 않습니다.

[공식 Search 인증 단계](https://learn.microsoft.com/azure/search/search-security-enable-roles), **2026-09-26** 확인.
문서 대조이며 새 Azure 실제 실행 검증은 아닙니다. 인증 오류를 우회하려고 `.env`에 Search key를 넣거나 provider를 바꾸지 않습니다.

IQ Chat 학습자는 서비스/객체 정의를 읽는 **Search의 Reader**와 검색하는 **Search Index Data Reader**가 필요합니다.
위 모델 계정 Reader와는 다른 범위이며 `check`는 모델 계정의 역할 할당도 읽습니다.
강사의 성공한 요청만이 아니라 학습자가 수행할 동작에 맞춰 Search 역할을 준비합니다.

| 학습자 동작 | Search 역할 | 범위 |
|---|---|---|
| `seed-search`를 실행하는 B 학습자 또는 담당자 | **Search Service Contributor**와 **Search Index Data Contributor** | 준비된 실습 Search 서비스 |
| 읽기 전용 `retrieve` 또는 준비된 IQ Chat 사용 | **Search Index Data Reader**. 서비스·객체 정의를 조회할 때는 **Reader**도 필요 | 준비된 실습 Search 서비스 |

새 B 학습자는 Lab 06의 객체 작성자입니다. 담당자가 공유 서비스를 이미 만들었어도 첫 행의 역할이 필요합니다.
역할 할당은 담당자가 승인하며, seed 실습을 한다고 구독 Owner가 필요한 것은 아닙니다.
모두에게 구독 Owner를 주지 말고 리소스 범위를 사용합니다.
[공식 Search 권한 표](https://learn.microsoft.com/azure/search/search-security-rbac#summary-of-permissions), 2026-09-15 확인.

**별도로 선택한 IQ Chat 경로에서만 실습 객체 작성·비용 승인을 받은 뒤** 고정 모델 chat base를 준비합니다.
기본 B GA-only 수업을 위해 아래 블록을 실행하지 않습니다. 담당자의 복사본/ledger를 보존하고 다른 새 학습자 복사본에 같은 seed된 prefix를 주지 않습니다.

이 선택 블록을 실행하기 전에 담당자 복사본의 `.env`를 편집합니다.
`AZURE_SEARCH_ENDPOINT`에는 준비된 Search URL을, `AZURE_OPENAI_ENDPOINT`에는 같은 Foundry 계정의
`https://<account>.openai.azure.com`을 입력합니다. Search의 리소스 그룹이 다르면 `AZURE_SEARCH_RESOURCE_GROUP`도 채웁니다.
응답용 `AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-6-sol`은 유지합니다. IQ Chat은 별도로 준비한 `gpt-5.6-luna`를 사용합니다.
`.env`를 셸에서 source하거나 key를 넣지 않습니다. 준비가 실패하면 `&&` 연결이 다음 단계 실행을 막습니다.

```bash
python scripts/workshop.py seed-search --iq --confirm-create &&
python scripts/workshop.py iq-chat check &&
python scripts/workshop.py iq-chat setup --confirm-create &&
python scripts/workshop.py iq-chat ask --label iq-chat-first --confirm-cost
```

`check`는 읽기 전용이며 모델 버전·Search identity/역할·원본이 맞지 않으면 중단합니다.
`setup`은 본인 새 chat base만 만들며 모델 배포·역할 부여·기존 GA 평가 base 변경은 하지 않습니다.
`ask`는 유료 요청이고 실제 계획·합성·원문 근거를 `outputs/iq-chat/iq-chat-first/`에 남깁니다.
새 요청은 **새 label**을 사용하며 첫 결과를 덮어쓰지 않습니다.

**2026-09-15 확인한 선택 Preview preset**은 `gpt-5.6-luna`, Search system-assigned identity,
`2026-08-01-preview`, `low`, `answerSynthesis`로 고정됩니다.
Preview 계획·합성은 A의 원문 확인이나 B의 GA 검색 완료에 필수가 아닙니다.
이전 진단에서 거절된 필드 대신 검증된 `maxOutputSize` 요청 필드를 사용합니다.
출력된 chat-base 이름을 학습자에게 전달합니다. 모델 없는 `<prefix>-kb`가 아니라 **그 chat base**를 열어야 합니다.

준비 후 [학습자 시작 가능 여부](setup.md#5-시작-가능-여부)로 돌아갑니다. 기본 A를 위해 선택 담당자 명령까지 실행하지 않습니다.
