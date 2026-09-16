# A. 입문: Python을 작성하지 않고 근거 있는 agent 하나 만들기

[English](../../paths/a-beginner.md) | **한국어**

**아래 표의 A 구간만 순서대로 진행합니다.** 고급 평가 워크북을 축약한 과정이 아닙니다.
구독·권한·설치가 끝난 준비 환경을 사용하며, 환경 준비 시간은 수업 시간에 포함하지 않습니다.

## 먼저 준비하기

[설정 카드](../setup.md)를 채우고 국문 학습자 ZIP의 `START-HERE.txt`를 엽니다.
준비된 **gpt-5.6-luna** 배포와 `instructions-with-policies.txt`, `dev-questions.txt`,
복사한 `assessment.csv`를 사용합니다. MAF 실습 한 번에는 학습자 계정으로 로그인된
준비 터미널이 필요합니다. 없다면 [Lab 00 B](../labs/00-start.md#b-코드--한-폴더-한-환경)를 한 번 진행합니다.

## 진행 순서

| 순서 | 열고 실행할 곳 | 여기까지 확인하면 다음으로 |
|---|---|---|
| 1 | [Lab 00 A](../labs/00-start.md): 계정·프로젝트·파일 | 내 설정 카드가 채워짐 |
| 2 | [Lab 01](../labs/01-foundry.md): account/project/deployment/agent 구분 | 실제 endpoint와 답변 배포를 식별함 |
| 3 | [Lab 02 A](../labs/02-models.md): Playground | 실제 답변과 근거 부족 사례를 기록함 |
| 4 | [Lab 03 A](../labs/03-prompt-agent.md): 전체 지침 붙여넣기·저장 | 실제 agent 버전과 답변을 기록함 |
| 5 | [Lab 05 A](../labs/05-workflows.md): 준비된 순차 명령 한 번 | `workflow-review.txt`에 결과와 내 검토가 있음 |
| 6 | [Lab 06 A](../labs/06-knowledge.md): 정책 ID·날짜 확인 | 원문 확인을 기록하고 IQ Chat 실행 여부를 구분함 |
| 7 | [Lab 07 A](../labs/07-evaluation.md): dev 6문항 평가 | 모든 행에 내 실제 결과와 이유가 있음 |
| 8 | [Lab 09 A](../labs/09-operations.md): 운영 확인 4가지 | `operations-checklist.txt`에 소유 자산과 잔여 비용이 있음 |
| 9 | [Lab 11 A](../labs/11-capstone.md): 인계 | 근거 폴더와 정리 책임자가 명확함 |

**A 아래에 B/C 설명이 있어도 계속 따라가지 않습니다.**
준비된 A 과정은 인계와 짧은 여유 시간을 포함해 240분입니다.
Preview 승인, 새 인프라, SDK 설치 대기는 별도입니다.

## A에서 하지 않는 일

Toolbox 생성, Hosted 배포, workflow 작성, Optimizer 실행, 회사/Microsoft 365 데이터 접근은 요구하지 않습니다.
준비된 Toolbox 시연을 보더라도 본인이 생성·실행한 증거로 기록하지 않습니다.

브라우저 agent 지침, 업로드 파일, IQ base, Toolbox, Memory는 서로 다른 자산입니다.
도구·인용·유창한 문장이 있다는 이유만으로 답변이 옳다고 판단하지 않습니다.

## 막히면

계정·모델·권한 문제는 담당자와 [설정 카드](../setup.md)부터 확인합니다.
잘못된 답변도 평가표에 그대로 남깁니다. 다른 사람의 결과, fixture, 녹화 속 답변으로 교체하지 않습니다.
선택 기능이 없으면 **미실행**으로 남깁니다.

**완료:** [Lab 11 인계](../labs/11-capstone.md).
**나중에 확장:** 같은 저장소의 [B. 구현](b-practitioner.md).
