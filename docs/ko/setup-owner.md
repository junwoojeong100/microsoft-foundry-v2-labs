# 환경 담당자 준비

[English](../setup-owner.md) | **한국어**

**학습자가 준비를 시작하기 전에 공유 Azure 환경을 준비합니다.** 이 페이지는 구독/프로젝트 담당자나 강사용이며, 학습자 단계 안에 숨겨 둔 조건이 아닙니다.

혼자 학습하면 본인이 환경 담당자 역할도 맡습니다. 아래는 준비 단계이며 다음 랩 안에 숨겨 둔 선행 조건이 아닙니다.

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
