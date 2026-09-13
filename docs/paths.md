# 학습 경로와 완료 기준

**A는 코딩이 없어도 완료할 수 있고, B는 실제 코드와 실행 이력을 남깁니다.**
둘 다 같은 한빛기술 합성 규정을 사용합니다. A를 마친 뒤 B로 확장할 수 있습니다.
각 랩의 `A. 브라우저`와 `B. 코드` 중 자기 경로만 따라갑니다.

## A. 완전초보자 — 준비된 환경에서 4시간

브라우저, Entra 계정, 강사가 준비한 Foundry 프로젝트·모델 배포가 필요합니다.
설치·CLI·Python 문법·Azure 구독 결제 설정을 수업 중 새로 배우는 경로가 아닙니다.
환경을 직접 만들고 싶으면 [강사 준비](instructor.md)의 관리자 단계를 먼저 진행합니다.

| 순서 | 실습 | 시간 | 직접 남길 결과 |
|---|---|---:|---|
| 1 | [00. 시작](labs/00-start.md) | 20분 | 계정·프로젝트·진행 경로 확인 |
| 2 | [01. Foundry](labs/01-foundry.md) | 25분 | 리소스·프로젝트·모델 구분 그림 |
| 3 | [02. 모델 — A](labs/02-models.md) | 20분 | Playground 실제 응답과 배포 이름 |
| 4 | [03. 에이전트 — A](labs/03-prompt-agent.md) | 35분 | 합성 정책을 사용하는 에이전트 |
| 5 | [05. 워크플로 — A](labs/05-workflows.md) | 25분 | 사람 검토가 포함된 실행 설계 |
| 6 | [06. 지식 — A](labs/06-knowledge.md) | 35분 | 원문 인용·적용 시점 확인 |
| 7 | [07. 평가 — A](labs/07-evaluation.md) | 30분 | dev 6문항의 수동 업무 평가표 |
| 8 | [09. 운영 — A](labs/09-operations.md) | 25분 | 운영 위험·비용·정리 확인 |
| — | 휴식·진행 버퍼 | 25분 | 합계 240분 |

**A의 완료:** 실제 Playground/에이전트 응답, 근거 문서 확인, dev 평가표, 정리 기록이
있습니다. 서버 배포나 Python 실행은 완료 조건이 아닙니다.

워크플로 디자이너·IQ 포털 기능이 해당 프로젝트에 없으면 **설계/관찰만 수행한 것**으로
기록합니다. 강사의 배포된 IQ 데모를 관찰한 경우도 본인의 IQ 배포 완료로 적지 않습니다.

## B. 경험자 — 준비된 환경에서 6시간

Python 기초, JSON, 터미널, `async/await`를 읽을 수 있어야 합니다.
리전/모델/권한 승인, SDK 다운로드, Search 생성은 사전 준비입니다.

| 순서 | 실습 | 시간 | 직접 남길 결과 |
|---|---|---:|---|
| 1 | [00. doctor와 공통 설정](labs/00-start.md) | 15분 | 환경 검사 |
| 2 | [02. SDK — B](labs/02-models.md) | 20분 | 실제 Responses 응답 |
| 3 | [04. MAF·함수·MCP](labs/04-agents-tools.md) | 45분 | 세 실행 방식의 차이 |
| 4 | [05. 워크플로 — B](labs/05-workflows.md) | 40분 | 순차·병렬·Group Chat 결과 |
| 5 | [06. Search/IQ — B](labs/06-knowledge.md) | 45분 | references·activity·context hash |
| 6 | [07. 학습 루프 — B](labs/07-evaluation.md) | 50분 | baseline/candidate/holdout 이력 |
| 7 | [08. Hosted Agent](labs/08-hosted.md) | 40분 | 로컬 패키지와 선택적 원격 응답 |
| 8 | [09. 관측·운영](labs/09-operations.md) | 30분 | 실행 ID 상관관계·운영 게이트 |
| 9 | [11. 캡스톤](labs/11-capstone.md) | 45분 | 인수 체크리스트 |
| — | 휴식·진행 버퍼 | 30분 | 합계 360분 |

**B의 핵심 완료:** 실제 Azure 모델을 사용한 코드 응답과 비교 가능한 dev 실행 이력이
있습니다. Hosted 배포·유료 cloud judge는 선택 게이트이며, 수행하지 않았으면
캡스톤에 `미실행`으로 남깁니다. 할당량이 없다고 fixture를 실제 응답 대신 제출하지 않습니다.

[10. Fabric/Work IQ 확장](labs/10-iq-extensions.md)은 45–90분의 별도 세션입니다.
승인·라이선스·capacity 준비 시간은 이 시간에 포함하지 않습니다.

## 독립 모듈로 다시 방문하기

| 필요한 모듈 | 최소 선행 결과 | 재시작 지점 |
|---|---|---|
| 모델/프롬프트 | 프로젝트·배포·Foundry User 권한 | 02 |
| MAF·MCP·워크플로 | SDK 설치, `doctor --cloud`, `model` 성공 | 04 |
| Foundry IQ | 위 조건 + 준비된 Search·knowledge retrieval 설정·권한 | 06 |
| 평가 | `outputs/<label>`의 완전한 실제 실행 또는 명시적 fixture | 07 |
| Hosted Agent | `maf --tools` 성공 + hosted SDK + 배포 권한 | 08 |
| IQ 확장 | IQ 기본 완료 + 서비스별 별도 승인 | 10 |

**실습 경로를 바꾸지 않는 원칙:** 모델이 실패하면 다른 모델로 자동 교체하지 않습니다.
IQ가 실패하면 일반 검색을 IQ 결과로 표시하지 않습니다. SDK 설치가 실패하면
버전을 제각각 올리지 말고 [버전 기준](reference/versions.md)과 강사 환경으로 복귀합니다.
