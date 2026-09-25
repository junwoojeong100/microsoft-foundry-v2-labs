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
   그 위치에서 이 모델·버전을 제공하지 않거나 quota가 없으면 멈춥니다. 다른 위치와 새 리소스 그룹으로 2단계를 다시 하거나
   [quota를 요청](https://aka.ms/oai/stuquotarequest)합니다. 다른 모델을 대신 배포하지 않습니다.
4. **본인 역할.** 역할 할당 권한이 있는 계정으로 포털에서 프로젝트를 만들면 본인과 프로젝트의 관리 ID에
   새 Foundry 리소스의 **Foundry User**가 함께 부여됩니다([공식 RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#minimum-role-assignments-to-get-started)).
   **확인:** Azure 포털에서 새 Foundry 리소스 → **액세스 제어(IAM)** → **역할 할당**을 열고 본인 계정의 **Foundry User**
   (이전 이름 **Azure AI User**)를 찾습니다. 없으면 그 리소스에서 본인 계정에 [역할을 할당](https://learn.microsoft.com/azure/role-based-access-control/role-assignments-portal)합니다.
5. **추적, 선택.** Lab 09의 추적 확인을 하려면 **빌드 → 에이전트**의 **추적** 탭에서 연결(**Connect**)을 선택하고
   새 Application Insights 리소스를 만듭니다([공식 절차](https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup)). 로그 비용이 추가됩니다.
   **확인:** 연결 완료 메시지가 나타납니다. 이 단계를 건너뛰면 Lab 09에서 `추적 미확인: <이유>`를 적습니다.
6. **파일과 설정값.** [준비 2–3절](setup.md#learner-files)을 진행합니다. 학습자 ZIP을 받고, 본인 포털에서 확인한 값으로 설정 카드를 채웁니다.
   `비용·권한 담당자:`에는 본인을 적습니다.
   **확인:** `session-notes.txt`의 **Lab 00 - 설정 카드** 구역이 모두 채워져 있습니다.
7. **Lab 05 터미널.** [Lab 00 B](labs/00-start.md#path-b) 1–5단계와 [Lab 02 B](labs/02-models.md#path-b) 1–3단계를 마치고
   [A 복귀 선택](labs/02-models.md#a-terminal-ready)으로 나갑니다. 이 단계는 Lab 05에 도착했을 때 해도 됩니다.
   **확인:** `doctor --cloud`가 `gpt-6-sol` / `2026-09-22` / `Succeeded`를 보고하고, Lab 02 B가 `model.json`과 `answer-local.json`을 저장했습니다.

**준비 완료:** 6단계 뒤(지금 7단계도 했다면 그 뒤) [Lab 00 A](labs/00-start.md#path-a)를 시작합니다.
단계가 실패하면 그 단계부터 해결한 뒤 진행합니다. 원인을 모르는 같은 오류 때문에 모델·리소스·프로젝트를 새로 만들지 않습니다.
**B를 혼자 학습하나요?** 1–5단계(B의 Lab 09에는 5단계가 필요)를 마친 뒤 [수업 담당자 체크리스트](#class-owner-checklist) 4단계로
Search 서비스와 본인의 Search 역할 두 개를 준비하고, B 경로의 [준비](setup.md)로 이어 갑니다.
**Lab 11 뒤:** 증거 폴더를 보관한 뒤, 2단계의 리소스 그룹에 이 과정의 리소스만 있을 때만 Azure 포털에서 삭제합니다
(**리소스 그룹** → 본인 그룹 → **리소스 그룹 삭제**). 프로젝트·배포·Application Insights가 함께 삭제되며,
확인·기록 방법은 [정리](reference/cleanup.md)에 있습니다. B 경로로 이어 갈 계획이면 그룹을 남겨 둡니다.

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

```bash
python scripts/workshop.py seed-search --iq --confirm-create
python scripts/workshop.py iq-chat check
python scripts/workshop.py iq-chat setup --confirm-create
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
