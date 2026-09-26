# B. 구현: 모델·에이전트·도구·지식·호스팅 연결하기

[English](../../paths/b-practitioner.md) | **한국어**

**응답 파일 14개·관리형 Prompt Agent trace 조회·dev/holdout 평가·로컬 패키지·정리 인계를 남깁니다.**
480분 핵심 수업 계획은 4시간 세션 두 번이며 학습자 완료 시간의 실측값이 아닙니다. 배포와 C 모듈은 필수가 아닙니다.

## 첫 명령 전

1. [준비](../setup.md) 후 [Lab 00 B](../labs/00-start.md#path-b)에서 소스 폴더·개인 기록·`.venv`·`.env`·로그인·사전 확인을 마칩니다. 이번 회차에서 이미 마쳤다면 아래 표의 첫 미완료 행부터 재개합니다.
2. `.venv`가 활성화된 저장소 루트에서 블록별로 실행합니다. 국문은 기본값이며 `--language ko`로 명시할 수도 있습니다. `.env`는 셸 `source`로 읽지 않습니다.
3. 각 **저장** 지점에서 JSON을 연 뒤 다음 요청으로 갑니다. `session-notes.txt`의 **B - 코드 근거와 인계**에 파일명과 확인 결과를 적고, Lab 05의 상세 검토는 `workflow-review.txt`에 둡니다. 응답 전체는 `--output`이 저장하므로 기록란에 다시 붙여 넣지 않습니다.

**파일 위치:** Lab 00이 핵심 JSON 14개와 개인 기록을 위한 `outputs/learner-notes-ko/`를 만듭니다.
자동 생성된 평가 실행은 `outputs/<label>/`에 그대로 둡니다. B에는 브라우저 agent나 두 번째 학습자 ZIP이 필요 없습니다.
[파일 목록](../labs/11-capstone.md#b-evidence) · [코드 블록 읽는 법](../labs/00-start.md#reading-code-blocks).

| 첫 회차의 선택 | 사용할 것 |
|---|---|
| 응답 모델 | 준비된 `gpt-6-sol`. Lab 02에서 토큰뿐 아니라 실제 Responses·Structured Outputs 확인 |
| Lab 03 관리형 agent | SDK로 만든 Prompt Agent. 반환된 변경 불가능한 정확한 버전을 호출 |
| Lab 05 workflow | 순차·병렬·Group Chat |
| Lab 06 검색 학습 | 일반 Search 다음 GA IQ |
| Lab 07 지침 비교 | 로컬 검색 + 실제 Azure 모델을 고정. dev v1/v2 비교 뒤 게이트를 통과하면 최종 holdout |
| Lab 08 호스팅 | 패키징만. 로컬 서버·원격 배포는 **미실행** |
| Lab 09 trace | Lab 03 B `response_id`로 Traces 검색. 로컬 MAF 실행에는 서버 측 trace가 없음 |

Lab 07은 의도적으로 별도의 로컬 검색 실험을 시작하며 Lab 06 오류의 대체 경로가 아닙니다.
Holdout 전 [dev 게이트](../labs/07-evaluation.md#final-acceptance)를 통과하려면 candidate 6문항 통과·오류 0건뿐 아니라 고정 설정으로 비교가 성립해야 합니다.
막히면 최종 평가를 **미완료**로 남기고 [미완료 인계](../labs/11-capstone.md#incomplete-handoff)를 합니다. Holdout을 수집하지 않습니다.
File Search·hybrid/Preview IQ·cloud judge는 선택입니다.

**비용·쓰기 경계:** Lab 02/03/04/05/07은 실제 모델을 호출하고, Lab 03은 관리형 agent 버전을 만듭니다.
Lab 06은 본인 Search 객체 작성과 검색 비용도 발생하므로 시작 전에 해당 범위의 승인을 받습니다.
Search 권한이 없으면 Lab 06을 미완료로 기록하고 전체 B 완료라고 하지 않습니다.

## 핵심 순서

| 순서 | 실습 | 확인할 산출물 |
|---|---|---|
| 1 | [Lab 00 B](../labs/00-start.md#path-b): 공통 준비 | 환경·개인 기록 폴더·인증·fixture/실제 실행 구분 |
| 2 | [Lab 02 B](../labs/02-models.md#path-b): 모델 API | 실제 응답·구조 검증·response ID·사용량 |
| 3 | [Lab 03 B](../labs/03-prompt-agent.md#path-b): 관리형 Prompt Agent | `prompt-agent-create.json`, `prompt-agent-invoke.json`, 정확한 버전과 response ID |
| 4 | [Lab 04 B](../labs/04-agents-tools.md#path-b): 함수와 MCP | 명령이 저장한 JSON 세 개를 각각 검토 |
| 5 | [Lab 05 B](../labs/05-workflows.md#path-b): MAF workflow | 자동 저장된 세 패턴 출력과 본인의 검토 |
| 6 | [Lab 06 B](../labs/06-knowledge.md#path-b): Search와 IQ | 검색·응답 출력과 `outputs/azure-objects.json` 소유권 보존 |
| 7 | [Lab 07 B](../labs/07-evaluation.md#path-b): 통제된 평가 | 오류를 포함한 `outputs/baseline/`·`outputs/candidate/`. `outputs/final-holdout/`은 dev 게이트 통과 후에만 |
| 8 | [Lab 08 B](../labs/08-hosted.md#path-b): 패키징만 | `.build/hosted/package-manifest.json`. 로컬·원격 실행은 미실행 |
| 9 | [Lab 09 B](../labs/09-operations.md#path-b): 운영과 trace | 기존 이력, Prompt Agent trace 조회 또는 미확인 이유, 정리 목록·담당자·남은 비용 |
| 10 | [Lab 11 B](../labs/11-capstone.md#path-b): 인계 | 실제 인수/반려 보고서 또는 누락 단계를 명시한 미완료 인계 |

**권장 분할:** Day 1은 Labs `00, 02, 03, 04, 05, 06`을 다룹니다. Day 2는 Labs `07, 08, 09, 11`을 다룹니다.
각 세션은 핵심 실습 195분과 휴식·진행 버퍼 45분입니다([세션별 시간표](../paths.md#b-session-budget)).
첫째 날 Search ledger와 출력을 유지하고 둘째 날에는 설치나 seed를 반복하지 않고 Lab 07에서 재개합니다.
추가 모듈은 **추가 세션**입니다. 확장된 전체 과정을 측정 없이 같은 시간 안에 끝낼 수 있다고 안내하지 않습니다.

## 구현 확장

<details>
<summary>기본 과정 인계 후 선택 — 다음 필수 명령이 아닙니다</summary>

클라우드 기능을 더하기 전에 명령 뒤의 코드를 이해하려면 [오프라인 코드 연습](../code-along.md)을 사용합니다.
개인 사본에서 어떤 동작 조건이 실패할지 예상하고 직접 고칩니다.
고정된 SDK 테스트이며 B의 Azure 결과를 대신하거나 holdout을 사용하지 않습니다.

먼저 **[관리형 Toolbox](../labs/extensions/toolbox.md)**를 선택합니다.
승인된 작은 도구 모음 생성 → MAF 연결 → 실제 요청 → 버전·근거 보관 순서입니다.
기본 버전 변경은 별도 선택 실습입니다.
Lab 04의 로컬 MCP 서버와 구분합니다.

[OpenAPI와 Code Interpreter](../labs/extensions/additional-tools.md)는 별도 선택 실습입니다.
동봉한 합성 데이터만 사용하며 회사 API 연결이나 실제 업무 처리는 하지 않습니다.
[기능·근거 상태](../coverage.md)에서 코드·실제 실행·영상 상태를 따로 확인합니다.
도구 설치와 명령 호환성은 [개발 도구](../labs/extensions/developer-toolkit.md)를 참고합니다.

</details>

## 올바른 중단점

Azure 쓰기 승인이 없으면 로컬 계획·패키징까지만 진행합니다.
클라우드 judge 승인이 없으면 로컬 업무 검사를 남기고 native 평가는 **미실행**으로 표시합니다.
Search 권한이 없으면 Search 실습을 중단합니다. 로컬 검색을 Search/IQ로 표시하지 않습니다.
프롬프트만 비교하는 실험 도중 provider를 바꾸지 않습니다.
필수 게이트가 계속 막혀 있다면 기존 파일과 정확한 이유로 [Lab 11 미완료 인계](../labs/11-capstone.md#incomplete-handoff)를 합니다.
현재 작업을 정직하게 인계하는 것이며 **전체 B 완료는 아닙니다**.

**중단·재개:** 마지막 완료 단계와 정확한 label을 적습니다. 새 터미널에서는 저장소 루트로 돌아와
`source .venv/bin/activate`만 다시 실행하며 재설치하거나 `.env`를 다시 만들지 않습니다.
`evaluate`·`compare`·`accept`는 저장된 실행을 로컬에서 읽습니다. `collect`는 새 유료 호출이므로 새 label이 필요합니다.
Lab 07은 [저장된 결과별 재개 표](../labs/07-evaluation.md#resume-evaluation)에서 재수집 없이 이어갈 단계를 찾습니다.
오류가 났다면 명령을 반복하기 전에 [복구 표](../reference/troubleshooting.md#resume-safely)를 확인합니다.

**완료:** [Lab 11](../labs/11-capstone.md#path-b).
**추가 선택:** [C. 고급 모듈](c-advanced.md).
