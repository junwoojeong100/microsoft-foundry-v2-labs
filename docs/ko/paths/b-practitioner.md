# B. 구현: 모델·도구·지식·호스팅 연결하기

[English](../../paths/b-practitioner.md) | **한국어**

**저장소 하나, 언어 하나, 검증된 설정값 한 세트를 사용합니다.**
B는 실행 가능한 시스템을 만드는 경로입니다. C는 독립적인 확장 모듈이며 B의 모든 실습 뒤에 필수로 붙지 않습니다.

## 첫 명령 전

[Lab 00 B](../labs/00-start.md#b-코드--한-폴더-한-환경)에서 로그인, `.env`,
가상환경 활성화, 읽기 전용 사전 확인을 마칩니다. 토큰 발급은 모델 실행 성공이 아닙니다.
Lab 02에서 실제 Responses 요청과 구조화된 답변까지 확인합니다.

명령은 저장소 루트에서 실행합니다. `.env`를 셸 `source`로 읽지 않습니다.
국문 명령에는 `--language ko`를 명시하고, 새 수집에는 새 label을 사용합니다.

## 핵심 순서

| 순서 | 실습 | 확인할 산출물 |
|---|---|---|
| 1 | [00. 공통 준비](../labs/00-start.md) | 환경·인증·fixture/실제 실행 구분 |
| 2 | [02. 모델 API](../labs/02-models.md) | 실제 응답·구조 검증·response ID·사용량 |
| 3 | [04. 함수와 MCP](../labs/04-agents-tools.md) | 무도구/함수/MCP의 실제 실행 경로 |
| 4 | [05. MAF workflow](../labs/05-workflows.md) | 순차·동시·group-chat 결과와 사람의 검토 |
| 5 | [06. Search와 IQ](../labs/06-knowledge.md) | 원문 ID·검색 activity·근거 hash |
| 6 | [07. 통제된 평가](../labs/07-evaluation.md) | baseline/candidate·오류·검토·고정된 최종 인수 |
| 7 | [08. Hosted 기본](../labs/08-hosted.md) | 패키징·로컬 응답·승인된 원격 실행의 분리 |
| 8 | [09. 운영](../labs/09-operations.md) → [11. 인계](../labs/11-capstone.md) | 재현 가능한 기록과 소유권 기반 정리 |

기존 준비된 B 과정은 6시간입니다. 추가 모듈은 **추가 세션**입니다.
확장된 전체 과정을 측정 없이 같은 시간 안에 끝낼 수 있다고 안내하지 않습니다.

## 구현 확장

먼저 [관리형 Toolbox](../labs/extensions/toolbox.md)를 선택합니다.
승인된 작은 도구 모음 생성 → MAF 연결 → 실제 요청 → 버전 확인 → 기본 버전 변경 순서입니다.
Lab 04의 로컬 MCP 서버와 구분합니다.

[OpenAPI와 Code Interpreter](../labs/extensions/additional-tools.md)는 별도 선택 실습입니다.
동봉한 합성 데이터만 사용하며 회사 API 연결이나 실제 업무 처리는 하지 않습니다.
[기능·근거 상태](../coverage.md)에서 코드·실제 실행·영상 상태를 따로 확인합니다.
도구 설치와 명령 호환성은 [개발 도구](../labs/extensions/developer-toolkit.md)를 참고합니다.

## 올바른 중단점

Azure 쓰기 승인이 없으면 로컬 계획·패키징까지만 진행합니다.
클라우드 judge 승인이 없으면 로컬 업무 검사를 남기고 native 평가는 **미실행**으로 표시합니다.
Search 권한이 없으면 Search 실습을 중단합니다. 로컬 검색을 Search/IQ로 표시하지 않습니다.
프롬프트만 비교하는 실험 도중 provider를 바꾸지 않습니다.

**완료:** [Lab 11](../labs/11-capstone.md).
**추가 선택:** [C. 고급 모듈](c-advanced.md).
