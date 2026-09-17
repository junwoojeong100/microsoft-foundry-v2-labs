# 명령 빠른 참조

[English](../../reference/commands.md) | **한국어**

**아래 명령은 모두 저장소 루트에서 실행합니다. `.env`를 shell로 `source`하지 않습니다.**
전용 가상환경을 활성화하면 클라우드 명령의 SDK를 사용할 수 있습니다.

**찾아보는 표이지 실행 순서가 아닙니다.** `python scripts/...`가 없는 행은 축약형이며
workshop 명령 앞에는 `python scripts/workshop.py`를 붙입니다.
`...`를 그대로 복사하거나 모든 행을 실행하지 말고 선택한 실습의 완전한 블록·승인 경계를 따릅니다.
[코드 블록 읽는 법](../labs/00-start.md#reading-code-blocks)에서 자리표시자·입력값·붙여 넣을 위치를 확인합니다.
명령 성공을 실습 통과로 판단하기 전에 [결과의 의미](#reading-results)를 읽습니다.

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
| `iq-chat check` | 읽기 전용 | 고정 Luna/버전·Search identity/역할/source·별도 chat-base 준비 확인 |
| `iq-chat setup --confirm-create` | 본인 Preview chat base만 생성 | 모델 배포·역할 부여·GA base 변경 없음 |
| `iq-chat ask --label iq-chat-first --confirm-cost` | 유료 계획·합성 | 고정 Luna + Search MI; 원시 응답·원문 근거·실패 저장 |
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
| `cleanup-plan` | 없음 | 삭제 안 함. 선택 언어의 정리 가이드 반환 |
| `python scripts/export_policy_docs.py` | 없음, 텍스트 6개 생성 | 선택 export. A의 학습자 ZIP에 이미 포함 |
| `python scripts/build_learner_materials.py` | 없음 | 두 언어의 학습자 자료를 canonical dev/지침/정책과 대조 |
| `python scripts/build_learner_materials.py --write` | 두 로컬 학습자 번들 재생성 | 관리자용 생성. 모델·holdout 사용 없음 |
| `python scripts/package_hosted.py` | 없음, 패키지 생성 | 배포/설치 실행 안 함 |
| `python scripts/prepare_hosted_azd.py --language ko --kind runtime ...` | 패키지를 검증한 로컬 프로젝트. `--initialize-env`는 로컬 azd 상태 생성/재조회도 수행 | 입문 local/v2/Responses 패키지만. Provision·배포·역할 부여 없음 |
| `python scripts/prepare_hosted_azd.py --language ko --kind matrix ...` | 패키지를 검증한 로컬 IQ matrix 프로젝트와 선택 azd 상태 | 순차 IQ/account-chat/Invocations v1/v2·정확한 모델 목록/Search 값. 배포 없음 |
| `python scripts/play_recordings.py` | 없음, localhost 영상 서버 | 영어 기본·Lab 00–11 챕터 이동. `--edition ko`로 별도 국문 새 촬영본 선택. Azure 호출·업로드 없음 |

표에서 생략한 옵션은 실행용 완전한 예제가 아닙니다.
첫 IQ Chat 설정은 [담당자 실행 순서](../setup.md#4-환경-담당자의-준비)를 한 번 진행합니다.
기본 GA `retrieve --provider iq`는 의도적으로 다른 경로입니다.

대화형 `model`·`answer`·`maf`·`workflow`·`retrieve`는 JSON을 출력합니다.
[B 기록 폴더](../labs/00-start.md#prepare-notes)에 출력 전체를 저장하며 batch는 이미 `outputs/<label>/`를 작성합니다.
필수 값을 포함한 독립 Hosted 준비 명령 전체는 [Lab 08](../labs/08-hosted.md)을 사용합니다.

<a id="reading-results"></a>

## 종료·검증·인수는 다릅니다

| 보이는 결과 | 의미와 다음 행동 |
|---|---|
| 셸 프롬프트가 돌아옴 | 프로세스가 끝났다는 뜻입니다. 출력·오류를 읽으며 이것만으로 통과로 판단하지 않습니다 |
| Offline `doctor`의 `result: PASS`, `azure_tested: false` | 로컬 입력/환경을 확인했습니다. Azure 접근·추론은 아직 미검증입니다 |
| Toolbox probe의 `model_invoked: false` | 도구 목록 조회에서는 정상입니다. 모델 답변으로 기록하지 않습니다 |
| `evaluate` / `accept`의 종료 코드 `1`, `business_gate_passed: false` | 실패 결과·모든 사례를 확인합니다. 기준을 낮추거나 실패한 candidate의 holdout을 열지 않습니다 |
| `trace_id: null`, `cloud_deployed: false`, `deployment_approved: false` | 해당 단계가 미검증/미수행이라는 명시적 한계입니다. 값을 편집해 성공으로 바꾸지 않습니다 |
| `pending-human-review` / `ready-for-human-review` | 사람의 검토가 남았습니다. 업무 승인이나 배포 권한을 부여한 것이 아닙니다 |
| 서비스 오류·응답 누락·실패 행 | 원래 시도를 보관하고 [복구](troubleshooting.md#resume-safely)로 갑니다. 이후 조회 성공이 원래 실패를 없애지 않습니다 |

Workshop CLI의 종료 코드 `2`는 입력·설정·의존성·선행 조건 오류입니다.
다른 도구도 같은 코드를 쓴다고 가정하지 않습니다. 측정하지 않은 값은 0이 아니라 미측정으로 둡니다.

<a id="saved-results"></a>

## 저장 결과 찾기

모든 모듈을 `outputs/<label>/`에서 찾지 말고 명령이 출력한 폴더를 사용합니다.
기존 실행·실패는 보존하며 새 target 요청에는 새 label이 필요합니다.

| 실행 종류 | 소스 저장소 아래 위치 |
|---|---|
| 입문 `demo` / `collect` | `outputs/<label>/` |
| `benchmark smoke` | 로컬 azd가 다른 폴더여도 `outputs/smoke/<label>/` |
| `benchmark collect` | `outputs/benchmarks/<label>/` |
| `iq-chat ask` | `outputs/iq-chat/<label>/` |
| Toolbox `probe` / `query` / `ask` | `outputs/toolbox-runs/<label>/`. 소유권은 `outputs/toolboxes/<name>/` |
| `conversations collect` | `outputs/conversations/<label>/`. 두 native 평가도 같은 수집 폴더 |
| `memory recall` | `outputs/memory-runs/<label>/`. Store 소유권은 별도 |
| Code Interpreter / OpenAPI / A2A | 각각 `outputs/code-interpreter/<label>/`, `outputs/openapi-runs/<label>/`, `outputs/a2a-runs/<label>/` |

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
| `benchmark smoke --local --azd-directory ...` | 로컬 host + 유료 모델 | 준비한 azd 폴더를 명시적으로 선택하며 근거는 소스 복사본에 저장 |
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
