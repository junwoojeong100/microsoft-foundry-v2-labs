# 시작 체크리스트: 하나의 환경, 하나의 값 목록

[English](../setup.md) | **한국어**

**고른 경로의 파일과 검증된 설정값을 준비한 뒤 Lab 00으로 갑니다.**
Azure 접근·권한·모델 quota·과금 승인은 환경 담당자가 제공합니다.
이 페이지에서 학습자에게 리소스 생성을 요구하지 않습니다.

## 1. 지금 내 시작점 선택

| 현재 상황 | 할 일 |
|---|---|
| 실습 환경을 이미 받음 | 이 페이지의 **1 → 2 → 3 → 4**절을 진행 |
| 본인 Azure 구독으로 혼자 학습함 | [혼자 학습 준비](setup-owner.md#self-study)를 진행하면 2–4절까지 안내합니다 |
| 아직 Azure 권한·quota가 없음 | [Lab 00 오프라인 체험](labs/00-start.md#offline-rehearsal)만 진행하고 cloud 실습은 **미실행**으로 기록 |

**한 회차 동안 경로 하나를 사용합니다.** Azure나 agent가 처음이면 **A**(브라우저 조작과 Lab 05의 준비된 workflow 경로),
Python·API에 익숙하면 **B**를 고릅니다. [경로 비교](paths.md).
한 회차 전체를 같은 언어로 진행합니다. 국문과 영문은 입력 파일이 다릅니다(B는 언어를 바꾸면 새 실행 label도 필요합니다).

<a id="learner-files"></a>
<a id="3-바로-쓰는-학습자-자료-내려받기"></a>

## 2. 경로에 맞는 파일 준비

**A는 아래 학습자 ZIP부터 받은 뒤 3절의 카드를 채웁니다.**
**B는 이 ZIP을 받지 않습니다.** 제공받은 소스 복사본을 유지합니다. 없다면 [Lab 00 B](labs/00-start.md#source-folder)에서
내려받는 방법을 안내합니다. 빈 기록 양식도 그 소스에 있습니다.
3절에서 받은 담당자의 설정값을 보관했다가 Lab 00에서 준비하는 개인 기록에 옮깁니다.

### A의 학습자 ZIP

[국문 learner-materials.zip](../../data/learner/ko/learner-materials.zip)을 열고 **Download raw file**로 내려받아 압축을 풉니다.
약 20KB인 이 ZIP은 Python·Git·전체 소스 저장소 없이 학습자 파일 16개를 한 번에 받기 위한 배포본입니다.
원본에서 생성하므로 별도 원본을 관리하는 것이 아닙니다. 영상·holdout·정답 기준 필드는 없으며, B는 이미 파일이 있어 받지 않습니다.
비공개 저장소에서는 읽기 권한이 있는 GitHub 계정을 사용합니다.

| 파일 | 용도 |
|---|---|
| `START-HERE.txt` | 파일별 사용 순서 |
| `instructions-with-policies.txt` | 전체를 새 Prompt Agent의 **지침**에 복사하고 저장 |
| `instructions.txt` | 인라인 근거 없는 지침. 선택 File Search 경로에서 사용 |
| `policies/` | 기본 Lab 03·06에서 확인할 합성 TXT 원문 6개. File Search 업로드는 기능을 사용할 수 있고 별도 선택한 경우에만 진행 |
| `dev-questions.txt` | 매번 새 대화에 질문 하나만 복사. ID나 평가 레코드 전체는 보내지 않음 |
| `dev-questions.jsonl` | 선택 Lab 07 Foundry 평가에 올리는 같은 6문항 데이터 세트. 정답 없음 |
| `assessment.csv` | 빈 6문항 평가표. 실제 응답·인용·통과/실패 기록 |
| `session-notes.txt` | 빈 설정 카드·Lab 01–03/06 관찰·Lab 07 A 버전/평가 결과·마지막 완료 단계·재개 링크 |
| `workflow-review.txt` | Lab 05의 실제 명령·출력·사람 검토용 빈 양식 |
| `operations-checklist.txt` | Lab 09의 소유/공유 자산·정리·남은 비용용 빈 양식 |
| `SOURCE.json` | 언어와 canonical 입력 hash |

[완성된 인라인 지침](../../data/learner/ko/instructions-with-policies.txt)이나
[질문 전용 파일](../../data/learner/ko/dev-questions.txt)을 직접 열어도 됩니다.
`dev-questions.txt`와 `dev-questions.jsonl`에는 질문만 있습니다. 채팅에는 질문 문장만 붙여 넣습니다.

압축을 푼 폴더를 **저장소 밖의 개인 증거 폴더**로 사용합니다.
진행하면서 기록 양식을 채우고 Lab 07에서는 `assessment.csv`를 `assessment-baseline.csv`로 저장합니다.
빈 양식은 완료된 증거가 아니며, 이 ZIP으로 코드 환경이 설치되는 것도 아닙니다.

<a id="local-tools"></a>

### A의 로컬 편집 도구

평가 단계에 도착해서가 아니라 **Lab 00 전에** 다음을 준비합니다.

- `.txt` 파일을 편집할 일반 텍스트 편집기. Windows 메모장이나 일반 텍스트 모드의 macOS TextEdit 등을 사용합니다.
- Lab 07의 CSV 표를 편집할 로컬 스프레드시트 편집기. CSV는 행과 쉼표로 구분한 열을 저장한 텍스트 파일입니다.
  데스크톱 Excel이 설치되어 있으면 그대로 사용합니다. 스프레드시트 편집기가 없다면 [LibreOffice Calc](https://www.libreoffice.org/download/)를 무료로 사용할 수 있습니다.
  브라우저 미리보기뿐 아니라 **UTF-8 CSV**를 열고 저장할 수 있어야 합니다. 유료 Office 구독은 필요하지 않습니다.

**지금 확인:** `session-notes.txt`를 편집 가능한 텍스트로, `assessment.csv`를 스프레드시트 편집기로 엽니다.
표에는 D01–D06 데이터 6행과 `case_id`부터 `review_note`까지 **6개 열**이 보여야 합니다.
모든 내용이 한 열에 보이면 **UTF-8** 인코딩과 **쉼표** 구분자로 가져옵니다
([Lab 07의 평가표 안내](labs/07-evaluation.md#assessment-sheet)).
빈 평가표는 수정하지 않고 닫습니다. Lab 07에서 별도 baseline 복사본을 만들어 작성합니다.
편집기를 사용할 수 없다면 경로를 시작하기 전에 준비를 마칩니다. 도구를 확인하려고 모델 요청을 보내지 않습니다.

<a id="environment-card"></a>
<a id="2-환경-카드-채우기"></a>

## 3. 환경 설정값 받기

강사나 환경 담당자에게 다음 값을 받습니다. 혼자 학습하면 표의 마지막 열대로 본인 포털에서 확인합니다.
Tenant뿐 아니라 **로그인할 계정**도 확인합니다. 평소 회사 계정과 실습 계정은 다를 수 있으며,
브라우저 로그인과 Azure CLI 로그인도 별도 세션입니다. 둘을 맞추려고 인증정보를 공유하지 않습니다.
**A:** 방금 압축을 푼 ZIP의 `session-notes.txt`에 적습니다.
**B:** 받은 값을 보관했다가 Lab 00에서 `outputs/learner-notes-ko/session-notes.txt`를 만들면 옮깁니다.
값을 받기 위해 설치부터 할 필요는 없습니다. 비밀번호·key·token은 기록하지 않습니다.

| 값 | 필요한 경로 | 어디서 확인 |
|---|---|---|
| Azure tenant·subscription ID | A·B | Azure 포털 → 구독·디렉터리 |
| Foundry 계정·프로젝트·리소스 그룹 | A·B | 실습 프로젝트의 리소스 상세. 계정 이름은 project endpoint의 `<account>` 부분과도 같음 |
| 전체 project endpoint | A·B | Foundry 프로젝트 **홈**. 끝의 `/api/projects/<project>`를 유지 |
| **응답 모델 배포** | A·B | **`gpt-6-sol`**, 모델 버전 **`2026-09-22`** |
| 내 객체 prefix | A·B | **`mfv2-`**로 시작. 소문자 영문·숫자·하이픈만 사용하고 하이픈을 연달아 쓰거나 끝에 두지 않음, 최대 32자. 예: `mfv2-team01-ko` |
| 코드 환경 | B와 A의 기본 Lab 05 터미널 방식 | 저장소 폴더·Python 3.13·활성화된 `.venv`·본인 Azure 로그인 |
| 준비된 Hosted workflow agent | A에서 Lab 05 브라우저 방식을 별도 선택했을 때만 | 담당자가 확인한 이름·버전·Playground 위치. 본인 언어의 순차 local/v2 Responses profile이며 Lab 03 Prompt Agent가 아님 |
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
- [ ] A: 학습자 ZIP을 받고 [로컬 편집기를 확인](#local-tools)했으며 **지침**과 대화창에 넣을 파일을 구분합니다. B: Lab 00의 소스 복사본·기록 준비 순서를 확인했습니다.
- [ ] 기본 Lab 05 준비 터미널이 있거나, 담당자가 선택 Hosted Responses Playground 방식을 미리 지정·검증했습니다. 둘 다 받지 못했다면 시간표의 A를 시작하기 **전에** Lab 00 B와 Lab 02 B를 완료합니다.
- [ ] B라면 담당자가 [Search 인증과 작성자 역할](setup-owner.md#search-authentication)을 확인하고 본인 객체 작성 비용을 승인했습니다. A의 IQ Chat은 별도 준비하지 않았다면 **미선택**입니다.
- [ ] 비용·권한 담당자를 알고 있으며 승인 없이 리소스 생성·역할 부여를 하지 않습니다.

체크하지 못한 필수 항목이 있으면 멈추고 그 준비부터 마칩니다. 오프라인 fixture는 실제 응답을 대신하지 않습니다.
**준비 완료: [A → Lab 00 브라우저](labs/00-start.md#path-a) · [B → Lab 00 코드](labs/00-start.md#path-b).**
아래 담당자 참고 자료는 학습자의 다음 단계가 아닙니다.

<a id="4-환경-담당자의-준비"></a>

## 환경 담당자 준비

담당자 체크리스트는 [환경 담당자 준비](setup-owner.md)로 이동했습니다. Azure 리소스, 권한, Application Insights, 선택 Hosted workflow, 선택 Dev Pack, IQ Chat 준비 단계를 포함합니다.

담당자가 위 값을 제공한 뒤 여기로 돌아옵니다. **준비 완료: [A → Lab 00 브라우저](labs/00-start.md#path-a) · [B → Lab 00 코드](labs/00-start.md#path-b).**
