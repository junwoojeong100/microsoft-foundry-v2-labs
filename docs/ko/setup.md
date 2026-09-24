# 시작 체크리스트: 하나의 환경, 하나의 값 목록

[English](../setup.md) | **한국어**

**고른 경로의 파일과 검증된 설정값을 준비한 뒤 Lab 00으로 갑니다.**
Azure 접근·권한·모델 quota·과금 승인은 환경 담당자가 제공합니다.
이 페이지에서 학습자에게 리소스 생성을 요구하지 않습니다.

## 1. 지금 내 시작점 선택

| 현재 상황 | 할 일 |
|---|---|
| 실습 환경을 이미 받음 | 이 페이지의 **1 → 2 → 3 → 4**절을 진행 |
| 본인 Azure 구독은 있지만 환경이 없음 | [담당자 준비](#4-환경-담당자의-준비) 후 2–4절 진행 |
| 아직 Azure 권한·quota가 없음 | [Lab 00 오프라인 체험](labs/00-start.md#offline-rehearsal)만 진행하고 cloud 실습은 **미실행**으로 기록 |

**한 회차 동안 경로 하나를 사용합니다.** Azure나 agent가 처음이면 **A**(브라우저 조작과 Lab 05의 준비된 명령 한 번),
Python·API에 익숙하면 **B**를 고릅니다. [경로 비교](paths.md).
한 회차는 같은 언어로 진행합니다. 국문과 영문은 입력 파일이 다르므로 언어를 바꾸면 새 실행 label이 필요합니다.

<a id="learner-files"></a>
<a id="3-바로-쓰는-학습자-자료-내려받기"></a>

## 2. 경로에 맞는 파일 준비

**A는 아래 학습자 ZIP부터 받은 뒤 3절의 카드를 채웁니다.**
**B는 이 ZIP을 받지 않습니다.** 제공받은 소스 복사본을 유지합니다. 없다면 [Lab 00 B](labs/00-start.md#source-folder)에서
내려받는 방법을 안내합니다. 빈 기록 양식도 그 소스에 있습니다.
3절에서 받은 담당자의 설정값을 보관했다가 Lab 00에서 준비하는 개인 기록에 옮깁니다.

### A의 학습자 ZIP

[국문 learner-materials.zip](../../data/learner/ko/learner-materials.zip)을 열고 **Download raw file**로 내려받아 압축을 풉니다.
작은 ZIP이므로 Python이 필요 없고, 영상·holdout·정답 기준 필드는 포함하지 않습니다.
비공개 저장소에서는 읽기 권한이 있는 GitHub 계정을 사용합니다.

| 파일 | 용도 |
|---|---|
| `START-HERE.txt` | 파일별 사용 순서 |
| `instructions-with-policies.txt` | 전체를 새 Prompt Agent의 **지침**에 복사하고 저장 |
| `instructions.txt` | 인라인 근거 없는 지침. 선택 File Search 경로에서 사용 |
| `policies/` | File Search에 올릴 합성 TXT 원문 정확히 6개 |
| `dev-questions.txt` | 매번 새 대화에 질문 하나만 복사. ID나 평가 레코드 전체는 보내지 않음 |
| `dev-questions.jsonl` | 선택 Lab 07 Foundry 평가에 올리는 같은 6문항 데이터 세트. 정답 없음 |
| `assessment.csv` | 빈 6문항 평가표. 실제 응답·인용·통과/실패 기록 |
| `session-notes.txt` | 빈 설정 카드·Lab 01–03/06 관찰·Lab 07 A 버전/평가 결과·마지막 완료 단계·재개 링크 |
| `workflow-review.txt` | Lab 05의 실제 명령·출력·사람 검토용 빈 양식 |
| `operations-checklist.txt` | Lab 09의 소유/공유 자산·정리·남은 비용용 빈 양식 |
| `SOURCE.json` | 언어와 canonical 입력 hash |

[완성된 인라인 지침](../../data/learner/ko/instructions-with-policies.txt)이나
[질문 전용 파일](../../data/learner/ko/dev-questions.txt)을 직접 열어도 됩니다.
`dev.jsonl`의 정답 열을 agent에 붙여 넣지 않습니다.

압축을 푼 폴더를 **저장소 밖의 개인 증거 폴더**로 사용합니다.
진행하면서 기록 양식을 채우고 Lab 07에서는 `assessment.csv`를 `assessment-baseline.csv`로 저장합니다.
빈 양식은 완료된 증거가 아니며, 이 ZIP으로 코드 환경이 설치되는 것도 아닙니다.

<a id="environment-card"></a>
<a id="2-환경-카드-채우기"></a>

## 3. 환경 설정값 받기

강사나 환경 담당자에게 다음 값을 받습니다.
**A:** 방금 압축을 푼 ZIP의 `session-notes.txt`에 적습니다.
**B:** 받은 값을 보관했다가 Lab 00에서 `outputs/learner-notes-ko/session-notes.txt`를 만들면 옮깁니다.
값을 받기 위해 설치부터 할 필요는 없습니다. 비밀번호·key·token은 기록하지 않습니다.

| 값 | 필요한 경로 | 어디서 확인 |
|---|---|---|
| Azure tenant·subscription ID | A·B | Azure 포털 → 구독·디렉터리 |
| Foundry 계정·프로젝트·리소스 그룹 | A·B | 실습 프로젝트의 리소스 상세 |
| 전체 project endpoint | A의 Lab 05 터미널·B | Foundry 프로젝트 **홈**. 끝의 `/api/projects/<project>`를 유지 |
| **응답 모델 배포** | A·B | **`gpt-6-sol`**, 모델 버전 **`2026-09-22`** |
| 내 객체 prefix | A·B | **`mfv2-`**로 시작. 소문자 영문·숫자·하이픈 하나씩, 끝 하이픈 금지, 최대 32자. 예: `mfv2-team01-ko` |
| 코드 환경 | A의 Lab 05(준비해 줌)·B | 저장소 폴더·Python 3.13·활성화된 `.venv`·본인 Azure 로그인 |
| Search endpoint | B의 Lab 06 | 준비된 Search 서비스: `https://<search>.search.windows.net` |

**답변에는 `gpt-6-sol`만 사용합니다.** `gpt-6-sol-judge`(선택 평가에서 답변 채점에만 사용)·목록의 다른 모델·router를 고르지 않습니다.
배포나 버전이 없으면 멈추고 담당자에게 해결을 요청합니다. 코드는 다른 모델로 바꾸지 않습니다.
[이 모델을 고른 이유](reference/model-choice.md).

<details>
<summary>선택 설정값 — IQ Chat·호스팅·클라우드 평가를 별도로 선택한 경우만</summary>

| 값 | 필요한 경로 | 어디서 확인 |
|---|---|---|
| 계정 OpenAI endpoint | 선택 IQ Chat / 심화 계정 API | `https://<your-account>.openai.azure.com`, 프로젝트와 같은 계정 |
| IQ chat base | 선택 IQ Chat만 | `iq-chat setup`이 반환한 `knowledge_base`. 기본은 `<prefix>-chat-ko-kb` |
| Hosted 값 | 선택 로컬·원격 호스팅만 | project ARM ID·location 코드·본인 agent 이름·빈 독립 로컬 폴더·필요한 승인. **패키징에는 불필요** |
| Judge 배포 | 선택 Foundry 평가(Lab 07 A 4단계, Lab 07 B 5단계, Lab 04 5절) | 답변 채점에만 쓰는 같은 모델의 별도 배포 **`gpt-6-sol-judge`**. 평가마다 담당자의 비용 승인 필요 |

</details>

<a id="5-시작-가능-여부"></a>

## 4. 시작 가능 여부

- [ ] 본인 계정으로 정확한 프로젝트를 열 수 있습니다.
- [ ] 실제 `gpt-6-sol` 배포와 버전 `2026-09-22`가 준비되었습니다.
- [ ] A: 학습자 ZIP을 받았고 **지침**과 대화창에 넣을 파일을 구분합니다. B: Lab 00의 소스 복사본·기록 준비 순서를 확인했습니다.
- [ ] Lab 05 터미널이 준비됐습니다. 아니라면 시간표의 A를 시작하기 **전에** Lab 00 B와 Lab 02 B를 완료합니다.
- [ ] B라면 Search 접근·본인 객체 작성 비용이 승인됐습니다. A의 IQ Chat은 별도 준비하지 않았다면 **미선택**입니다.
- [ ] 비용·권한 담당자를 알고 있으며 승인 없이 리소스 생성·역할 부여를 하지 않습니다.

체크하지 못한 필수 항목이 있으면 멈추고 그 준비부터 마칩니다. 오프라인 fixture는 실제 응답을 대신하지 않습니다.
**준비 완료: [A → Lab 00 브라우저](labs/00-start.md#path-a) · [B → Lab 00 코드](labs/00-start.md#path-b).**
아래 담당자 참고 자료는 학습자의 다음 단계가 아닙니다.

<a id="4-환경-담당자의-준비"></a>

## 환경 담당자 준비

<details>
<summary>환경을 직접 준비할 때만 — 별도 승인·시간·비용이 필요합니다</summary>

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
   Lab 05용 터미널을 받지 못한 학습자는 이 설치와 [Lab 02 B](labs/02-models.md#path-b)를 마친 뒤 돌아옵니다.

IQ Chat 학습자는 서비스/객체 정의를 읽는 **Search의 Reader**와 검색하는 **Search Index Data Reader**가 필요합니다.
위 모델 계정 Reader와는 다른 범위이며 `check`는 모델 계정의 역할 할당도 읽습니다.
Source를 seed하거나 객체를 만드는 담당자만 Search Service Contributor·Search Index Data Contributor가 필요합니다.
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

준비 후 [시작 가능 여부](#4-시작-가능-여부)로 돌아갑니다. 기본 A를 위해 선택 담당자 명령까지 실행하지 않습니다.

</details>
