# 명령 빠른 참조

[English](../../reference/commands.md) | **한국어**

**아래 명령은 모두 저장소 루트에서 실행합니다. `.env`를 shell로 `source`하지 않습니다.**
전용 가상환경을 활성화하면 클라우드 명령의 SDK를 사용할 수 있습니다.

| 명령 | Azure / 부작용 | 상세 |
|---|---|---|
| `python scripts/workshop.py doctor` | 없음 | Python·합성 데이터 검사 |
| `doctor --cloud` | 읽기만 | 명시된 구독/tenant/배포/token 확인, 추론 아님 |
| `demo --label demo-v2 --prompt v2` | 없음, 로컬 결과 생성 | 고정 fixture |
| `retrieve --provider local` | 없음 | 로컬 키워드 검색 |
| `retrieve --provider search` | Search 조회 비용 가능 | 일반 검색 |
| `retrieve --provider iq` | IQ 조회 비용 가능 | GA knowledge base |
| `model --question "질문"` | 유료 모델 호출 | 직접 Responses |
| `answer --prompt v2 --retrieval local` | 유료 모델 호출 | 구조화 답변 + 원문 |
| `maf --tools` / `maf --mcp` | 유료 모델 호출 | 읽기 전용 함수 / 로컬 MCP |
| `workflow --pattern sequential` | 유료 모델 호출 | 대안: concurrent, group-chat |
| `seed-search --confirm-create` | 본인 Search 객체 생성/업로드 | 기존 서비스만 사용 |
| `seed-search --iq --confirm-create` | 위 + GA source/base | 소유권 검사 |
| `prompt-agent create ... --confirm-create` | 실제 agent version 생성 | 정확한 접두사 필요 |
| `prompt-agent invoke ... --version ...` | 실제 agent 호출 | 버전 고정 |
| `collect --label baseline --prompt v1` | dev 전체 유료 호출 | 오류 보존, 동시성 1 |
| `evaluate --label baseline` | 없음 | 결정적 업무 검사 |
| `compare --baseline baseline --candidate candidate` | 없음 | 통제된 dev 비교 |
| `feedback --label baseline --case D03 --reason "구체적인 검토 이유"` | 없음, 로컬 검토 기록 | 실제 dev만, 승인 대기 |
| `cloud-evaluate --label candidate --confirm-cost` | 유료 cloud judge | evaluator version·job 이력 |
| `collect --split holdout ... --candidate candidate --unlock-holdout` | 고정 후보의 실제 평가 요청 | 개발용 재사용 금지 |
| `accept --candidate candidate --holdout final-holdout` | 없음 | 사람의 인수 자료, 자동 승인 아님 |
| `serve` | 로컬 서버 시작, 호출 시 유료 모델 | Hosted SDK 필요 |
| `cleanup-plan` | 없음 | 삭제 안 함 |
| `python scripts/export_policy_docs.py` | 없음, 텍스트 6개 생성 | A 경로 강사 배포용 |
| `python scripts/package_hosted.py` | 없음, 패키지 생성 | 배포/설치 실행 안 함 |
| `python scripts/play_recordings.py` | 없음, localhost 영상 서버 | 새 영문 촬영본 기본·Lab 00–11 챕터 이동. `--edition ko`로 한국어 원본 선택. Azure 호출·업로드 없음 |

표에서 생략한 옵션은 실행용 완전한 예제가 아닙니다.

## 한국어 통합 개정의 추가 명령

| 명령 | 부작용 | 목적 |
|---|---|---|
| `workflow-agent --pattern sequential --retrieval iq` | 실제 모델·검색 호출 | 배포용 MAF workflow와 검증된 최종 답 |
| `runtime-contract --kind workflow --protocol invocations` | 로컬 설정/파일 읽기 | code/prompt/corpus/model/retrieval 계약. Azure 검증은 아님 |
| `serve --kind workflow --protocol responses` | 로컬 서버, 요청 시 모델 호출 | 실제 Workflow.as_agent 호스팅 |
| `serve --kind workflow --protocol invocations` | 위와 같음 | strict query-only 평가 endpoint |
| `seed-search --hybrid --confirm-create --confirm-cost` | 본인 index + 실제 embedding | 6개 합성 원문으로 별도 hybrid index |
| `retrieve --provider hybrid` | 실제 embedding·Search 조회 | text + vector query |
| `benchmark plan ...` | 없음 | 명시적 모델 목록과 호출량 계획 |
| `benchmark smoke ... --confirm-cost` | 실제 local/remote 모델 호출 | exact runtime contract와 응답 검사 |
| `benchmark collect ... --confirm-cost` | 원격 session + 전체 matrix | 모델×case, 오류/원문/계보 보존 |
| `benchmark evaluate --label LABEL --confirm-cost` | 실제 native judge | frozen responses의 평가 |
| `benchmark evaluate ... --reference BASELINE` | 위와 같음 | 같은 evaluator/version/judge/threshold |
| `benchmark evaluate ... --retry-failed` | 새 유료 시도 | 실패/invalid 시도만 재실행, 원본 보존 |
| `benchmark regression ... --confirm-review` | 로컬 승인 기록 | 원본 dev만, 다음 dev의 `--regressions`로 소비 |
| `calibrate-judge ... --confirm-cost` | 실제 judge | 고정 정답/오답 fixture의 오탐·미탐 |
| `benchmark compare ...` / `benchmark report --label LABEL` | 로컬 보고서 | controlled dev 비교 / 모든 행의 HTML |
| `benchmark trace-plan --label LABEL` | 로컬 KQL | 실제 조회 아님 |
| `benchmark monitor --label LABEL` | App Insights 읽기 | agent·기간·모든 trace ID의 실제 대조 |
| `benchmark verify ...` | 로컬 gate | native/trace/regression/calibration과 최종 후보 인수 |
| `benchmark stop-session --label LABEL` | 기록한 session 중지 | 파일·공유 서비스 삭제 없음 |

위 표의 `...`, `LABEL`은 설명용입니다.
완전한 복사 명령은 [평가 워크북](evaluation-workbook.md)과 [Lab 08](../labs/08-hosted.md)에 있습니다.
`benchmark`의 `stop-session`은 해당 label에서 생성한 session만 대상으로 하며 일반 Azure 정리 도구가 아닙니다.

정확한 필수 인자는 `python scripts/workshop.py --help`와 각 하위 명령의 `--help`로 확인합니다.
전체 실행 예는 해당 [실습 모듈](../paths.md)에 있습니다.

로컬 진단에는 명령 앞에 `--debug`를 넣을 수 있습니다.
추가 스택·서비스 오류에는 환경 경로가 포함될 수 있으므로 원시 로그를 공개하지 않습니다.

실행 결과를 바꾸는 명령은 기존 label을 덮어쓰지 않습니다.
점수나 raw 응답을 수정해 hash 검사를 통과시키려 하지 않습니다.
