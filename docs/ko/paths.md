# 학습 경로와 완료 기준

[English](../paths.md) | **한국어**

**A는 코드를 작성하지 않고 준비된 예제를 실행하며, B는 코드와 실행 이력을 직접 다룹니다.**
둘 다 같은 한빛기술 합성 규정을 사용합니다. A를 마친 뒤 B로 확장할 수 있습니다.
각 랩의 A와 B 중 자기 경로를 따라갑니다. A는 포털 중심이지만 워크플로는 준비된 MAF 환경에서 실행합니다.

**전용 경로:** [A — 입문](paths/a-beginner.md) · [B — 구현](paths/b-practitioner.md) ·
[C — 고급 모듈](paths/c-advanced.md) · [기능·근거 상태](coverage.md).
**처음 방문이면 A를 선택합니다.** 해당 경로 페이지를 체크리스트로 사용하며 아래 시간표는 추가 과제가 아닙니다.
각 랩의 `path-a` / `path-b`로 바로 들어가 **A 완료 / B 완료** 링크로 나옵니다.
아래 시간은 기존 준비된 핵심 과정의 시간입니다.
새 추가 모듈을 같은 4/6시간 안에 몰래 포함하지 않습니다.

**[준비 카드·학습자 ZIP](setup.md)에서 시작하고 자기 경로의 다음 링크만 따라갑니다.**
시작 카드 → 조작·명령 → 완료 기준 순서로 진행하세요.
이미지와 접힌 녹화 갤러리는 선택 참고 자료이며 본인 실행 결과가 아닙니다.
새 workflow/benchmark 기능을 포함한 2026-09-15 국문 촬영본을 사용합니다.
국문과 영문은 별도 실행·별도 원본이며 본인의 값과 결과는 따로 확인합니다.
[현재 국문 영상](video-summary.md)과 [새 액션 인덱스](action-captures.md)를 제공합니다.
[화면 읽는 법](labs/00-start.md#이-가이드의-화면-읽는-법)과 [전체 액션 인덱스](action-captures.md)를 보조 자료로 사용하세요.

## A. 완전초보자 — 준비된 환경에서 4시간

브라우저, Entra 계정, 준비된 Foundry 프로젝트·**`gpt-5.6-luna` 배포**가 필요합니다.
Lab 05에는 SDK 설치와 본인 계정 로그인이 끝난 **준비된 MAF 실행 환경**도 필요합니다.
학습자는 명령을 복사해 실행하고 결과를 읽습니다. Python 코드 작성·설치·구독 결제 설정은 사전 준비입니다.
혼자 학습하면 [환경 담당자 체크리스트](setup.md#4-환경-담당자의-준비)와
[Lab 00 B 설치](labs/00-start.md#b-코드--한-폴더-한-환경)를 먼저 완료합니다.

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

MAF를 직접 실행하지 못했으면 관찰과 직접 실행을 구분합니다. 포털 workflow 작성으로 대신하지 않습니다.
Preview IQ Chat은 선택입니다. 준비된 경우만 선택하고, 아니라면 **미실행**으로 표시한 뒤
이미 만든 agent의 원문 확인을 완료합니다. 이는 실행 전 범위 선택이지 IQ 오류 뒤의 fallback이 아닙니다.

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

B의 기본 모델·MAF·IQ 개념을 익힌 뒤 [평가 워크북](reference/evaluation-workbook.md)을 진행합니다.
전체 주제를 하나의 6시간 수업에 억지로 압축하지 않습니다. B+C는 **8.5–9시간의 준비된 실습**이며
리소스 준비·권한 전파·배포/평가 대기는 별도입니다.

| 순서 | 직접 수행 | 남길 자산 |
|---|---|---|
| 1 | Lab 05의 배포용 workflow와 Lab 08 프로필 패키지 | 실제 MAF builder, runtime/profile/code hash |
| 2 | 전용 Hosted Invocations version과 명시적 모델 목록 | query-only 계약·배포 허용 목록·smoke |
| 3 | 완전한 dev model matrix와 native 평가 | 4모델이면 24행, 전체 오류·점수 |
| 4 | 실제 trace 검토, dev regression 승인/소비 | 원래 정답·source response/trace·검토 기록 |
| 5 | 새 version, 동일 dev/evaluator, calibration | 전후 비교·평가자 오탐/미탐 |
| 6 | 후보 고정 후 holdout과 통합 인수 | 4모델이면 16행, 독립 gate·사람 판단 |
| 7 | 본인 session 정리 및 잔여 비용 확인 | 해시가 유지된 실행 이력·cleanup receipt |

질문 수 64개와 실제 모델 호출 수는 다릅니다.
순차 workflow이면 논리 모델 호출만 최대 192회이고 검색·retry·judge는 추가입니다.
`benchmark plan`으로 본인의 모델 목록과 예상량을 확인합니다.
이 경로의 완료는 기존 single-agent 영상이나 upstream 성공 횟수로 대신할 수 없습니다.

## 독립 모듈로 다시 방문하기

| 필요한 모듈 | 최소 선행 결과 | 재시작 지점 |
|---|---|---|
| 모델/프롬프트 | 프로젝트·배포·Foundry User 권한 | [02 B](labs/02-models.md#path-b) |
| MAF·MCP·워크플로 | SDK 설치, `doctor --cloud`, `model` 성공 | [04 B](labs/04-agents-tools.md#path-b) |
| Foundry IQ | 위 조건 + 준비된 Search·knowledge retrieval 설정·권한 | [06 B](labs/06-knowledge.md#path-b) |
| 평가 | `outputs/<label>`의 완전한 실제 실행 또는 명시적 fixture | [07 B](labs/07-evaluation.md#path-b). Fixture로 실제 인수를 열지 않음 |
| Hosted 패키징 | 저장소·Python. 런타임 게이트는 별도 | [08 B](labs/08-hosted.md#path-b) |
| Hosted workflow 평가 | 프로필·모델 목록·고정 Invocations version·IQ·judge·App Insights 준비 | C 워크북 |
| IQ 확장 | IQ 기본 완료 + 서비스별 별도 승인 | [10](labs/10-iq-extensions.md) |

**실습 경로를 바꾸지 않는 원칙:** 모델이 실패하면 다른 모델로 자동 교체하지 않습니다.
IQ가 실패하면 일반 검색을 IQ 결과로 표시하지 않습니다. SDK 설치가 실패하면
버전을 제각각 올리지 말고 [버전 기준](reference/versions.md)과 강사 환경으로 복귀합니다.
