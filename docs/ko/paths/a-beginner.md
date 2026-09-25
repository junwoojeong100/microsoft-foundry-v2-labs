# A. 입문: Python을 작성하지 않고 근거 있는 에이전트 하나 만들기

[English](../../paths/a-beginner.md) | **한국어**

**본인 에이전트·6문항 평가표·workflow 검토 한 건·trace 상태·정리 인계를 남깁니다.**
아래 표의 A 구간만 따라갑니다. 270분 수업 계획은 환경·권한·설치가 이미 준비된 상태를 기준으로 하며 학습자 완료 시간의 실측값이 아닙니다.

## 먼저 준비하기

[준비](../setup.md)에서 국문 학습자 ZIP을 받은 뒤 담당자의 값을 기록합니다.
**혼자 학습하나요?** 본인이 담당자이기도 하므로 먼저 [혼자 학습 준비](../setup-owner.md#self-study)를 완료합니다.
`START-HERE.txt`를 엽니다. 준비된 **gpt-6-sol** 배포와 ZIP의 완성 지침·질문·빈 기록 양식을 사용합니다.
입력 파일이나 보고서 형식을 따로 만들지 않습니다.
Lab 05에서는 준비된 방식 하나를 실행합니다. 기본은 워크숍 코드가 설치되고 본인 계정으로 Azure에 로그인한 터미널입니다.
Hosted Responses Playground는 수업 전에 담당자가 검증한 경우에만 사용합니다.
둘 다 없다면 시간표를 시작하기 전에 [Lab 00 B](../labs/00-start.md#path-b)와 [Lab 02 B](../labs/02-models.md#path-b)를 완료합니다.

**첫 회차의 선택은 정해져 있습니다:** 인라인 정책, 준비된 workflow 실행 한 번, 수동 dev 평가, Lab 09 trace 상태 기록입니다.
File Search·IQ Chat·Hosted 배포·cloud judge·C 모듈은 별도로 선택하지 않는 한 **미선택**입니다.
아래 번호 링크는 A의 정확한 구간을 열며, 각 랩에서 **A 완료** 링크로 나갑니다.

## 진행 순서

| 순서 | 열고 실행할 곳 | 여기까지 확인하면 다음으로 |
|---|---|---|
| 1 | [Lab 00 A](../labs/00-start.md#path-a): 계정·프로젝트·파일 | `session-notes.txt`의 설정 카드가 채워짐 |
| 2 | [Lab 01 A](../labs/01-foundry.md#path-a): account/project/deployment/agent 구분 | 네 객체의 관계 그림과 실제 endpoint 추가 |
| 3 | [Lab 02 A](../labs/02-models.md#path-a): Playground | 실제 답변과 근거 부족 관찰을 `session-notes.txt`에 기록 |
| 4 | [Lab 03 A](../labs/03-prompt-agent.md#path-a): 전체 지침 붙여넣기·저장 | `instructions-baseline.txt` 저장. `session-notes.txt`에 해당 에이전트/버전·실제 확인 4건 연결 |
| 5 | [Lab 05 A](../labs/05-workflows.md#path-a): 준비된 Hosted Playground 방식 또는 준비된 순차 터미널 명령 하나 | `workflow-review.txt`에 실행 방식, 실제 출력/ID 전체와 내 검토가 있음 |
| 6 | [Lab 06 A](../labs/06-knowledge.md#path-a): 정책 ID·날짜 확인 | `session-notes.txt`에 원문 확인 기록. 기본 경로는 IQ Chat 미선택 |
| 7 | [Lab 07 A](../labs/07-evaluation.md#path-a): 저장한 버전 하나로 dev 6문항 평가 | `assessment-baseline.csv`에 실제 응답·인용·이유 6건. `session-notes.txt`에 버전·통과 수 / 6 기록. Candidate는 정당한 변경이 있을 때만 |
| 8 | [Lab 09 A](../labs/09-operations.md#path-a): 운영과 trace 확인 | `operations-checklist.txt`에 소유 자산, 잔여 비용, 실제 trace 근거 또는 `추적 미확인: <이유>`가 있음 |
| 9 | [Lab 11 A](../labs/11-capstone.md#path-a): 인계 | 근거 폴더와 정리 책임자가 명확함 |

**합계:** 휴식·진행 버퍼 포함 270분입니다. A 아래에 B/C 설명이 있어도 계속 따라가지 않습니다.
Preview 승인, 새 인프라, SDK 설치 대기는 별도입니다.

## A에서 하지 않는 일

Toolbox 생성, Hosted 배포, workflow 작성, Optimizer 실행, 회사/Microsoft 365 데이터 접근은 요구하지 않습니다.
준비된 Toolbox 시연을 보더라도 본인이 생성·실행한 증거로 기록하지 않습니다.

브라우저 에이전트의 지침, 업로드 파일, IQ base, Toolbox, Memory는 서로 다른 자산입니다.
도구·인용·유창한 문장이 있다는 이유만으로 답변이 옳다고 판단하지 않습니다.

## 막히면

계정·모델·권한 문제는 담당자와 [설정 카드](../setup.md)부터 확인합니다. 혼자 학습하면 해당하는
[혼자 학습 준비 단계](../setup-owner.md#self-study)를 직접 해결합니다.
잘못된 답변도 평가표에 그대로 남깁니다. 다른 사람의 결과, fixture, 녹화 속 답변으로 교체하지 않습니다.
선택 기능이 없으면 **미실행**으로 남기고, trace가 없으면 `추적 미확인: <이유>`로 남깁니다.

**중단·재개:** `session-notes.txt`에 마지막 완료 Lab/단계·에이전트 버전·다음 링크를 적습니다.
같은 프로젝트와 저장한 버전을 다시 열고, 새 유료 질문을 보내기 전에 기존 결과부터 확인합니다.
재개하려고 에이전트를 다시 만들거나 앞 랩을 전부 반복하지 않습니다.

**완료:** [Lab 11 인계](../labs/11-capstone.md#path-a).
**나중에 확장:** [B. 구현](b-practitioner.md)의 [Lab 00 B 소스 폴더 준비](../labs/00-start.md#source-folder)부터 시작합니다.
A의 작은 학습자 ZIP은 코드 저장소가 아닙니다. 준비된 소스 복사본이 이미 있다면 그대로 유지합니다.
