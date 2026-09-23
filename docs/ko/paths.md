# 학습 경로와 완료 기준

[English](../paths.md) | **한국어**

**A는 코드를 작성하지 않고 브라우저에서 준비된 예제를 실행하며, B는 코드와 저장된 실행 기록을 직접 다룹니다.**
둘 다 같은 한빛기술 시나리오를 언어별로 동등하게 고정된 합성 규정으로 진행합니다.

Azure나 agent가 처음이면 **A**, Python·API에 익숙하면 **B**를 선택합니다.
[준비 카드](setup.md)를 완료한 뒤 경로 페이지를 체크리스트로 사용합니다:
[A — 입문](paths/a-beginner.md) · [B — 구현](paths/b-practitioner.md).
아래 표는 시간표이며 추가 과제가 아닙니다. 각 랩은 `path-a` / `path-b`로 들어가 **A 완료 / B 완료**로 나옵니다.
[C — 고급 모듈](paths/c-advanced.md)은 핵심 경로 이후의 별도 세션입니다.

**랩 진행 방법:** 시작 카드를 읽고 조작·명령을 실행한 뒤 결과를 **화면 확인**과 비교합니다.
화면은 2026-09-24 국문 녹화이며 이름·ID·답변은 본인 환경과 다릅니다
([화면 읽는 법](labs/00-start.md#이-가이드의-화면-읽는-법)).
국문 명령은 기본 국문 입력 파일을 사용합니다([언어 규칙](reference/languages.md)).

## A. 완전초보자 — 준비된 환경에서 4시간

브라우저, Entra 계정, 준비된 Foundry 프로젝트·**`gpt-6-sol` 배포**가 필요합니다.
Lab 05에는 SDK 설치와 본인 계정 로그인이 끝난 **준비된 MAF 실행 환경**도 필요합니다.
학습자는 명령을 복사해 실행하고 결과를 읽습니다. Python 코드 작성·설치·구독 결제 설정은 사전 준비입니다.
혼자 학습하면 [환경 담당자 체크리스트](setup.md#4-환경-담당자의-준비),
[Lab 00 B](labs/00-start.md#b-코드--한-폴더-한-환경), [Lab 02 B](labs/02-models.md#path-b)를 먼저 완료합니다.

| 순서 | 실습 | 시간 | 직접 남길 결과 |
|---|---|---:|---|
| 1 | [00. 시작](labs/00-start.md#path-a) | 20분 | 계정·프로젝트·진행 경로 확인 |
| 2 | [01. Foundry](labs/01-foundry.md#path-a) | 25분 | 리소스·프로젝트·모델 구분 그림 |
| 3 | [02. 모델 — A](labs/02-models.md#path-a) | 20분 | Playground 실제 응답과 배포 이름 |
| 4 | [03. 에이전트 — A](labs/03-prompt-agent.md#path-a) | 35분 | 인라인 합성 정책을 사용하는 에이전트 |
| 5 | [05. MAF 워크플로 — A](labs/05-workflows.md#path-a) | 25분 | 준비된 순차 MAF 실행 + 사람 검토 기록 |
| 6 | [06. 지식 — A](labs/06-knowledge.md#path-a) | 35분 | 원문 인용·적용 시점 확인. IQ Chat은 기본 미선택 |
| 7 | [07. 평가 — A](labs/07-evaluation.md#path-a) | 30분 | dev 6문항의 수동 업무 평가표 |
| 8 | [09. 운영 — A](labs/09-operations.md#path-a) | 25분 | 운영 위험·비용·정리 확인 |
| 9 | [11. 캡스톤 — A](labs/11-capstone.md#path-a) | 15분 | 본인 평가표·실행 증거 인계 |
| — | 휴식·진행 버퍼 | 10분 | 합계 240분 |

**A의 완료:** 실제 Playground/에이전트 응답, 준비된 MAF 순차 실행, 근거 문서 확인,
dev 평가표, Lab 11의 정리·증거 인계가 있습니다. Python 코드 작성이나 서버 배포는 완료 조건이 아닙니다.

Lab 05 명령은 본인이 직접 실행합니다. 다른 사람의 실행을 본 것은 완료가 아닙니다.
IQ Chat은 선택입니다. 준비되지 않았다면 시작 전에 **미실행**으로 표시합니다(오류 뒤의 대체가 아닌 범위 선택).

## B. 경험자 — 준비된 환경에서 6시간

Python 기초, JSON, 터미널, `async/await`를 읽을 수 있어야 합니다.
리전/모델/권한 승인, SDK 다운로드, Search 생성은 사전 준비입니다.

| 순서 | 실습 | 시간 | 직접 남길 결과 |
|---|---|---:|---|
| 1 | [00. doctor와 공통 설정](labs/00-start.md#path-b) | 15분 | 환경 검사 |
| 2 | [02. SDK — B](labs/02-models.md#path-b) | 20분 | 실제 Responses 응답 |
| 3 | [04. MAF·함수·MCP](labs/04-agents-tools.md#path-b) | 45분 | 세 실행 방식의 차이 |
| 4 | [05. MAF 워크플로 — B](labs/05-workflows.md#path-b) | 40분 | 순차·병렬·Group Chat 코드와 결과 |
| 5 | [06. Search/IQ — B](labs/06-knowledge.md#path-b) | 45분 | GA references·activity·context hash |
| 6 | [07. 학습 루프 — B](labs/07-evaluation.md#path-b) | 50분 | 로컬 검색·실제 모델의 baseline/candidate/holdout 이력 |
| 7 | [08. Hosted Agent](labs/08-hosted.md#path-b) | 40분 | 패키지·manifest 검토. 서버 실행·배포는 필수 아님 |
| 8 | [09. 관측·운영](labs/09-operations.md#path-b) | 30분 | 기존 실행 ID 이력과 읽기 전용 정리 계획 |
| 9 | [11. 캡스톤](labs/11-capstone.md#path-b) | 45분 | 기존 인수 보고서·산출물 체크리스트 |
| — | 휴식·진행 버퍼 | 30분 | 합계 360분 |

**B의 핵심 완료:** 표에 있는 실제 모델·도구·workflow·Search/IQ 결과,
비교 가능한 dev 이력·고정된 최종 평가·패키지·정리 인계가 있습니다.
Hosted 서버/배포·실제 telemetry·유료 cloud judge는 선택 게이트이며, 수행하지 않았으면
캡스톤에 `미실행`으로 남깁니다. 할당량이 없다고 fixture를 실제 응답 대신 제출하지 않습니다.
필수 단계가 계속 막혀 있다면 [미완료 인계](labs/11-capstone.md#incomplete-handoff)로 실제 작업과 복구 담당자를 보존합니다.
이는 빠진 B 완료 요건을 충족한 것으로 처리하지 않습니다.

[10. Fabric/Work IQ 확장](labs/10-iq-extensions.md)은 45–90분의 별도 세션입니다.
승인·라이선스·capacity 준비 시간은 이 시간에 포함하지 않습니다.

## C. 통합 심화 — 150–180분 추가

이것은 **선택 가능한 C 경로 하나**이지 [모든 C 모듈](paths/c-advanced.md)의 선행 조건이 아닙니다.
버전을 고정한 Hosted matrix는 [Hosted 평가 워크북](reference/evaluation-workbook.md)에서 이어 갑니다.
실제 모델 배포, IQ/Search 역할, Hosted ID, judge, App Insights 접근을 먼저 준비합니다.
환경 생성·권한·quota·인코딩 대기는 수업 시간 밖입니다.

| 순서 | 작업 | 시간 | 근거 |
|---|---|---:|---|
| 1 | [배포 가능한 MAF workflow](labs/05-workflows.md#c-경험자-심화--같은-워크플로를-배포-가능한-agent로) | 25분 | 실제 최종 답변과 모델 호출 계보 |
| 2 | [Hosted Responses/Invocations](labs/08-hosted.md) | 30분 | 고정 프로필, 실제 로컬 응답, 정확한 원격 버전 |
| 3 | 모델 matrix와 native 평가 | 40분 | 4모델 dev cohort 24행과 고정한 평가자 |
| 4 | 검토한 regression·calibration | 25분 | 정당한 dev 검토·소비 또는 전 문항 통과 기록, 실제 judge calibration |
| 5 | 고정 holdout·trace·인수 | 30분 | 4모델 최종 세트 16행, 실제 root trace, 사람 검토 근거 |

비교마다 corpus·정답·코드·API·모델 목록·검색 방식·평가자를 고정합니다.
선택 [IQ 확장](reference/iq-workbook.md)에는 서비스별 별도 승인이 필요합니다.

## 독립 모듈로 다시 방문하기

| 필요한 모듈 | 최소 선행 결과 | 재시작 지점 |
|---|---|---|
| 모델/프롬프트 | 프로젝트·배포·Foundry User 권한 | [02 B](labs/02-models.md#path-b) |
| MAF·MCP·워크플로 | SDK 설치, `doctor --cloud`, `model` 성공 | [04 B](labs/04-agents-tools.md#path-b) |
| Foundry IQ | 위 조건 + 준비된 Search·knowledge retrieval 설정·권한 | [06 B](labs/06-knowledge.md#path-b) |
| 평가 | `outputs/<label>`의 완전한 실제 실행 또는 명시적 fixture | [07 B](labs/07-evaluation.md#path-b). Fixture로 실제 인수를 열지 않음 |
| Hosted 패키징 | 저장소·Python. 런타임 게이트는 별도 | [08 B](labs/08-hosted.md#path-b) |
| IQ 확장 | IQ 기본 완료 + 서비스별 별도 승인 | [10](labs/10-iq-extensions.md) |

**실습 경로를 바꾸지 않는 원칙:** 모델이 실패하면 다른 모델로 자동 교체하지 않습니다.
IQ가 실패하면 일반 검색을 IQ 결과로 표시하지 않습니다. SDK 설치가 실패하면
버전을 제각각 올리지 말고 [버전 기준](reference/versions.md)과 강사 환경으로 복귀합니다.
