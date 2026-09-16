# B. 구현: 모델·도구·지식·호스팅 연결하기

[English](../../paths/b-practitioner.md) | **한국어**

**저장소 하나, 언어 하나, 검증된 설정값 한 세트를 사용합니다.**
B는 실행 가능한 시스템을 만드는 경로입니다. C는 독립적인 확장 모듈이며 B의 모든 실습 뒤에 필수로 붙지 않습니다.

## 첫 명령 전

[Lab 00 B](../labs/00-start.md#path-b)부터 로그인, `.env`,
가상환경 활성화, 읽기 전용 사전 확인을 마칩니다. 토큰 발급은 모델 실행 성공이 아닙니다.
Lab 02에서 실제 Responses 요청과 구조화된 답변까지 확인합니다.

명령은 저장소 루트에서 실행합니다. `.env`를 셸 `source`로 읽지 않습니다.
국문 기본 명령은 Korean 번들을 사용하며 `--language ko`로도 명시할 수 있습니다. 새 수집에는 새 label을 사용합니다.
Lab 00에서 소스 복사본의 빈 양식으로 **`outputs/learner-notes-ko/`**를 만듭니다.
터미널 출력 파일과 검토 기록은 여기에 저장합니다. B에는 브라우저 agent나 별도 학습자 ZIP이 필요 없습니다.
자동 생성된 평가 폴더는 기록 폴더 안이 아니라 `outputs/<label>/`에 그대로 둡니다.

**첫 회차의 선택은 정해져 있습니다:** Luna, 입문 MAF 세 패턴, Lab 06의 GA Search/IQ,
Lab 07의 **로컬 검색 + 실제 Azure 모델**, Lab 08의 **패키징만**입니다.
Lab 06의 검색 학습 뒤 Lab 07의 명시된 로컬 실험으로 이동하는 것이며 IQ 오류 뒤의 자동 대체가 아닙니다.
File Search·hybrid/Preview IQ·cloud judge·로컬 Hosted 서버·원격 배포는 기본 단계가 아닙니다.

**비용·쓰기 경계:** Lab 02/04/05/07은 실제 모델을 호출합니다.
Lab 06은 본인 Search 객체 작성과 검색 비용도 발생하므로 시작 전에 해당 범위의 승인을 받습니다.
Search 권한이 없으면 Lab 06을 미완료로 기록하고 전체 B 완료라고 하지 않습니다.

## 핵심 순서

| 순서 | 실습 | 확인할 산출물 |
|---|---|---|
| 1 | [Lab 00 B](../labs/00-start.md#path-b): 공통 준비 | 환경·개인 기록 폴더·인증·fixture/실제 실행 구분 |
| 2 | [Lab 02 B](../labs/02-models.md#path-b): 모델 API | 실제 응답·구조 검증·response ID·사용량 |
| 3 | [Lab 04 B](../labs/04-agents-tools.md#path-b): 함수와 MCP | 세 명령의 실제 출력 전체를 개인 증거 폴더에 저장 |
| 4 | [Lab 05 B](../labs/05-workflows.md#path-b): MAF workflow | 세 패턴의 출력과 사람 검토 저장 |
| 5 | [Lab 06 B](../labs/06-knowledge.md#path-b): Search와 IQ | 검색·응답 출력과 `outputs/azure-objects.json` 소유권 보존 |
| 6 | [Lab 07 B](../labs/07-evaluation.md#path-b): 통제된 평가 | 오류를 포함한 `outputs/baseline/`, `outputs/candidate/`, `outputs/final-holdout/` |
| 7 | [Lab 08 B](../labs/08-hosted.md#path-b): 패키징만 | `.build/hosted/package-manifest.json`. 로컬·원격 실행은 미실행 |
| 8 | [Lab 09 B](../labs/09-operations.md#path-b): 운영 | 기존 이력·정리 목록·담당자·남은 비용 |
| 9 | [Lab 11 B](../labs/11-capstone.md#path-b): 인계 | 실제 인수/반려 보고서 또는 누락 단계를 명시한 미완료 인계 |

기존 준비된 B 과정은 6시간입니다. 추가 모듈은 **추가 세션**입니다.
확장된 전체 과정을 측정 없이 같은 시간 안에 끝낼 수 있다고 안내하지 않습니다.

## 구현 확장

<details>
<summary>기본 과정 인계 후 선택 — 다음 필수 명령이 아닙니다</summary>

먼저 [관리형 Toolbox](../labs/extensions/toolbox.md)를 선택합니다.
승인된 작은 도구 모음 생성 → MAF 연결 → 실제 요청 → 버전 확인 → 기본 버전 변경 순서입니다.
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
명령을 반복하기 전에 [재개 표](../reference/troubleshooting.md#resume-safely)를 확인합니다.

**완료:** [Lab 11](../labs/11-capstone.md#path-b).
**추가 선택:** [C. 고급 모듈](c-advanced.md).
