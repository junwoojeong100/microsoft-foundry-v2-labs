# 시작 체크리스트: 하나의 환경, 하나의 값 목록

[English](../setup.md) | **한국어**

**Lab 00 전에 한 번만 준비합니다.** 가이드는 실습 절차를 설명하지만 Azure 구독·권한·모델 quota·과금 승인을 대신 제공하지는 않습니다.
아래 준비가 끝났다면 강사가 대신 조작하지 않아도 본인이 가이드 순서대로 실행할 수 있습니다.

## 1. 지금 내 시작점 선택

| 현재 상황 | 할 일 |
|---|---|
| 실습 환경을 이미 받음 | 아래 환경 카드를 채우고 학습자 자료를 내려받은 뒤 Lab 00 시작 |
| 본인 Azure 구독은 있지만 환경이 없음 | 4절의 환경 담당자 준비를 먼저 완료한 뒤 같은 카드 사용 |
| Azure 권한·quota를 기다리는 중 | Lab 00의 offline 체험만 진행하고 cloud 실습은 미실행으로 기록 |

A·B·C를 동시에 따라가지 않습니다. **처음이면 [학습 경로](paths.md)의 A를 선택합니다.**
A는 Lab 05의 준비된 MAF 단계 전까지 브라우저 중심이고 B/C가 코드·선택 배포·평가를 추가합니다.
한 회차는 같은 언어로 진행합니다. 언어를 바꾸면 입력 번들이 달라지므로 새 label을 쓰고 다른 언어의 점수를 재사용하지 않습니다.

## 2. 환경 카드 채우기

담당자가 실제 값을 제공합니다. 녹화의 이름을 복사하지 않으며 비밀번호·key·token은 적지 않습니다.

| 값 | 어디서 확인 / 이번 기본값 |
|---|---|
| Azure tenant·subscription ID | Azure 포털 → 구독·디렉터리 |
| Foundry 계정·프로젝트·리소스 그룹 | 실습 프로젝트의 리소스 상세 |
| 전체 project endpoint | Foundry 프로젝트 홈. `/api/projects/<project>`를 유지 |
| **응답 모델 배포** | **`gpt-5.6-luna`**, 실제 모델도 같은 이름, 이 날짜의 실습 preset은 **`2026-07-09`** 버전 |
| Prefix | 소문자 영문·숫자·하이픈으로 고유하게 지정. 예: `mfv2-team01-0915`, 최대 32자 |
| Search endpoint | 기존 실습 Search 서비스. Lab 06 IQ를 선택할 때만 필요 |
| 계정 OpenAI endpoint | `https://<your-account>.openai.azure.com`, 프로젝트와 같은 계정 |
| IQ chat base | `iq-chat setup`의 `knowledge_base`. 기본은 `<prefix>-chat-ko-kb` |
| 코드 환경 | 저장소 폴더·Python 3.13·활성화된 `.venv`·학습자 본인의 Azure 로그인 |
| 선택 Hosted 값 | 실제 project ARM ID·본인 agent 이름·배포 승인. Lab 08/C에서만 필요 |

**첫 실습에서 모델 선택 실험은 하지 않습니다.** Luna를 사용하고 `-judge`·Astra·router를 고르지 않습니다.
해당 배포/버전이 없으면 환경 담당자가 가용성을 해결하거나 다른 에디션을 명시적으로 재검증해야 합니다.
코드는 다른 모델을 자동 선택하지 않습니다. 모델 고정은 흔한 불일치를 예방하지만 서비스 가동·quota까지 보장하지는 않습니다.

## 3. 바로 쓰는 학습자 자료 내려받기

[국문 learner-materials.zip](../../data/learner/ko/learner-materials.zip)을 열고 **Download raw file**로 내려받아 압축을 풉니다.
작은 ZIP이므로 Python이 필요 없고, 영상·holdout·정답 기준 필드는 포함하지 않습니다.
비공개 저장소에서는 읽기 권한이 있는 GitHub 계정을 사용합니다.

| 파일 | 용도 |
|---|---|
| `START-HERE.txt` | 파일별 사용 순서 |
| `instructions-with-policies.txt` | 전체를 새 Prompt Agent의 **Instructions(지침)**에 복사하고 저장 |
| `instructions.txt` | 인라인 근거 없는 지침. 선택 File Search 경로에서 사용 |
| `policies/` | File Search에 올릴 합성 TXT 원문 정확히 6개 |
| `dev-questions.txt` | 매번 새 대화에 질문 하나만 복사. ID나 평가 레코드 전체는 보내지 않음 |
| `assessment.csv` | 빈 6문항 평가표. 실제 응답·인용·통과/실패 기록 |
| `SOURCE.json` | 언어와 canonical 입력 hash |

[완성된 인라인 지침](../../data/learner/ko/instructions-with-policies.txt)이나
[질문 전용 파일](../../data/learner/ko/dev-questions.txt)을 직접 열어도 됩니다.
`dev.jsonl`의 정답 열을 agent에 붙여 넣지 않습니다.

## 4. 환경 담당자의 준비

혼자 학습하면 본인이 환경 담당자 역할도 맡습니다. 아래는 준비 단계이며 다음 랩 안에 숨겨 둔 선행 조건이 아닙니다.

1. 전용 실습 구독·리소스 그룹과 필요한 모델 quota가 있는 리전을 선택합니다.
   [현재 Foundry 준비 가이드](https://learn.microsoft.com/azure/foundry/quickstarts/get-started-code)를 사용하고
   classic Hub/threads-runs 튜토리얼을 섞지 않습니다.
2. **`gpt-5.6-luna` / `2026-07-09`**를 배포 이름 **`gpt-5.6-luna`**로 준비하고 상태 `Succeeded`를 확인합니다.
   설명되지 않은 오류 뒤에 다른 모델을 새로 만들지 않습니다.
3. 학습자에게 필요한 Foundry 프로젝트/모델 권한을 줍니다.
   CLI의 배포 사전 조회에는 **실습 Foundry 계정의 Reader**도 필요합니다. 관리자뿐 아니라 학습자 계정으로 실제 호출을 점검합니다.
4. 선택 IQ 단계를 진행한다면 Basic 이상 Search, system-assigned identity, semantic/knowledge retrieval 사용 조건과
   합성 index를 작성할 사람의 Search 읽기/쓰기 권한을 준비합니다.
5. 모델의 Foundry 계정에서 **Search identity**에 `Cognitive Services User`를 부여합니다.
   사용자나 Hosted agent에 준 역할이 Search에 생기는 것은 아닙니다.
6. 아래 담당자 명령 전에 `.env`를 포함한 [Lab 00 B 설치](labs/00-start.md#b-코드--한-폴더-한-환경)를 완료합니다.
   Lab 05용 터미널을 받지 못한 학습자도 이 경로로 직접 준비한 뒤 돌아옵니다.

IQ Chat 학습자는 서비스/객체 정의를 읽는 **Search의 Reader**와 검색하는 **Search Index Data Reader**가 필요합니다.
위 모델 계정 Reader와는 다른 범위이며 `check`는 모델 계정의 역할 할당도 읽습니다.
Source를 seed하거나 객체를 만드는 담당자만 Search Service Contributor·Search Index Data Contributor가 필요합니다.
모두에게 구독 Owner를 주지 말고 리소스 범위를 사용합니다.
[공식 Search 권한 표](https://learn.microsoft.com/azure/search/search-security-rbac#summary-of-permissions), 2026-09-15 확인.

**실습 객체 작성·비용 승인을 받은 뒤** 별도의 고정 모델 chat base를 준비합니다.

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

**2026-09-15 확인한 선택 Preview preset**은 Luna, Search system-assigned identity,
`2026-08-01-preview`, `low`, `answerSynthesis`로 고정됩니다.
Preview 계획·합성은 A의 원문 확인이나 B의 GA 검색 완료에 필수가 아닙니다.
이전 진단에서 거절된 필드 대신 검증된 `maxOutputSize` 요청 필드를 사용합니다.
출력된 chat-base 이름을 학습자에게 전달합니다. 모델 없는 `<prefix>-kb`가 아니라 **그 chat base**를 열어야 합니다.

## 5. 시작 가능 여부

- [ ] 본인 계정으로 정확한 프로젝트를 열 수 있습니다.
- [ ] 실제 Luna 배포/버전이 준비되었습니다.
- [ ] 학습자 ZIP을 받았고 Instructions와 대화창에 넣을 파일을 구분합니다.
- [ ] Lab 05용 터미널이 준비됐거나 Lab 00 B 설치를 먼저 완료할 예정입니다.
- [ ] Lab 06 IQ Chat을 선택했다면 고정 설정과 실제 모델 activity를 담당자가 확인했고, 아니라면 미선택으로 표시했습니다.
- [ ] 비용·권한 담당자를 알고 있으며 승인 없이 리소스 생성·역할 부여를 하지 않습니다.

준비되지 않은 항목은 해당 준비 단계에서 멈춥니다. Fixture를 실제 응답으로 대신하지 않습니다.
**다음: [Lab 00](labs/00-start.md).**
