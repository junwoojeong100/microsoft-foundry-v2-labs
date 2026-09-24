# 명령 빠른 참조

[English](../../reference/commands.md) | **한국어**

**아래 명령은 모두 저장소 루트에서 실행합니다. `.env`를 shell로 `source`하지 않습니다.**
전용 가상환경을 활성화하면 클라우드 명령의 SDK를 사용할 수 있습니다.

**찾아보는 표이지 실행 순서가 아닙니다.** `python scripts/...`가 없는 행은 축약형이며
workshop 명령 앞에는 `python scripts/workshop.py`를 붙입니다.
`...`를 그대로 복사하거나 모든 행을 실행하지 말고 선택한 실습의 완전한 블록·승인 경계를 따릅니다.
[코드 블록 읽는 법](../labs/00-start.md#reading-code-blocks)에서 자리표시자·입력값·붙여 넣을 위치를 확인합니다.
명령 성공을 실습 통과로 판단하기 전에 [결과의 의미](#reading-results)를 읽습니다.

## 기본 B·오프라인 명령

이 표를 위에서 아래로 실행하지 말고 [B의 순서](../paths/b-practitioner.md)를 따릅니다.

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
| `collect --split dev --label baseline --prompt v1 --retrieval local` | dev 전체 유료 호출 | 오류 보존, 동시성 1 |
| `evaluate --label baseline` | 로컬 평가 보고서 작성. Azure 호출 없음 | 결정적 업무 검사 |
| `compare --baseline baseline --candidate candidate` | 로컬 비교 보고서 작성. Azure 호출 없음 | 통제된 dev 비교 |
| `feedback --label baseline --case D03 --reason "구체적인 검토 이유"` | 없음, 로컬 검토 기록 | 실제 dev만, 승인 대기 |
| `collect --split holdout --label final-holdout --prompt v2 --retrieval local --candidate candidate --unlock-holdout` | 고정 후보의 실제 평가 요청 | 개발용 재사용 금지 |
| `accept --candidate candidate --holdout final-holdout` | 로컬 인수/반려 보고서 작성. Azure 호출 없음 | 사람의 인수 자료, 자동 승인 아님 |
| `cleanup-plan` | 없음 | 삭제 안 함. 선택 언어의 정리 가이드 반환 |
| `python scripts/package_hosted.py` | 없음, 패키지 생성 | 배포/설치 실행 안 함 |

표에서 생략한 옵션은 실행용 완전한 예제가 아닙니다.
정확한 필수 인자는 `python scripts/workshop.py --help`와 각 하위 명령의 `--help`에서 확인합니다.
전체 명령은 해당 [실습](../paths.md)에 있습니다.

<a id="saving-json"></a>

## 터미널 텍스트를 복사하지 않고 응답 저장하기

`model`·`answer`·`maf`·`workflow`·`workflow-agent`·`retrieve`와 선택 명령 `maf-evaluate`는 **명령 뒤에 `--output FILE`**을 받습니다.
화면에 출력하는 것과 같은 JSON 전체를 저장하며 response ID·원문·사용량·미검증 필드를 바꾸지 않습니다.
기본 B 명령에는 파일명 12개가 이미 들어 있습니다. [기록 폴더](../labs/00-start.md#prepare-notes)만 한 번 준비합니다.

준비 후 추가로 실행할 수 있는 **로컬 전용** 검색 예시입니다.

```bash
python scripts/workshop.py retrieve --provider local \
  --output outputs/learner-notes-ko/retrieve-example.json
```

이 소스 복사본의 `outputs/` 안에 있는 새 `.json`이어야 하며 상위 폴더가 있어야 합니다.
파일이 이미 있거나 안전한 범위 밖이면 **요청 전에 거절**합니다. 재개할 때는 저장된 결과를 열고, 새 요청에만 새 파일명을 사용합니다.
`--output`을 생략하면 기존처럼 출력만 합니다.

`Saved JSON: ...`는 stderr에, JSON은 stdout에 나옵니다. **저장은 평가 통과나 승인이 아닙니다.**
요청이 실패하면 성공 응답 파일을 만들지 않습니다. 응답은 출력됐지만 저장에 실패했다면 stdout과 오류를 보관하고
유료 요청을 반복하는 대신 직접 새 파일에 저장합니다.
`collect`·`evaluate`·`cloud-evaluate`·`benchmark`처럼 `--help`에 `--output`이 없는 실행 명령은 자체 기록 폴더를 관리합니다.
`--output`을 붙이거나 manifest를 출력 사본으로 대체하지 않습니다.

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
| `--output`을 지정한 대화형 명령 | 지정한 정확한 파일. 기본 B는 `outputs/learner-notes-ko/*.json` |
| 입문 `demo` / `collect` | `outputs/<label>/` |
| `cloud-evaluate` | `outputs/<label>/`. `--business-evaluator`를 쓰면 `outputs/<label>/foundry-business-rubric/` |
| `benchmark smoke` | 로컬 azd가 다른 폴더여도 `outputs/smoke/<label>/` |
| `benchmark collect` | `outputs/benchmarks/<label>/` |
| `iq-chat ask` | `outputs/iq-chat/<label>/` |
| Toolbox `probe` / `query` / `ask` | `outputs/toolbox-runs/<label>/`. 소유권은 `outputs/toolboxes/<name>/` |
| `conversations collect` | `outputs/conversations/<label>/`. 두 native 평가도 같은 수집 폴더 |
| `memory recall` | `outputs/memory-runs/<label>/`. Store 소유권은 별도 |
| Code Interpreter / OpenAPI / A2A | 각각 `outputs/code-interpreter/<label>/`, `outputs/openapi-runs/<label>/`, `outputs/a2a-runs/<label>/` |

로컬 진단에는 하위 명령 앞에 `--debug`를 넣습니다. 스택·서비스 오류에는 환경 경로가 들어 있을 수 있으므로 원시 로그를 공개하지 않습니다.
명령은 기존 실행 label을 덮어쓰지 않습니다. hash 검사를 통과시키려고 raw 응답이나 점수를 고치지 않습니다.

영문은 별도로 고정한 정책·지침·데이터와 함께 `--language en`을 사용합니다.
그 밖의 실행 옵션과 schema는 국문과 같습니다.
승인된 자유 입력 질문 번역은 `data/guide-questions.json`에 명시되어 있습니다.

## 선택 명령군

<details>
<summary>선택한 모듈만 확인 — 기본 B의 추가 필수 단계가 아닙니다</summary>

로컬 계획도 Azure 요청을 하지 않을 뿐 선택한 모듈의 SDK·`.env`가 필요할 수 있습니다.
각 명령군의 `--help`와 연결된 실습에서 필수 값·생성/비용/삭제 승인을 확인합니다.

| 명령군 | 목적·경계 | 전체 가이드 |
|---|---|---|
| `prompt-agent` | 별도 버전의 관리형 agent 생성/호출. 로컬 MAF와 구분 | [Lab 03 SDK](../labs/03-prompt-agent.md) |
| `collect --retrieval none` | 선택 dev 진단 6회. 정책 근거가 없으며 baseline/candidate 경로가 아님. `feedback`·`cloud-evaluate`는 거부 | [Lab 07 진단](../labs/07-evaluation.md#diagnostic-no-evidence) |
| `iq-chat` | `gpt-5.6-luna`/SMI 사전 확인·본인 chat base 생성·유료 계획/합성 | [담당자 준비](../setup.md#4-환경-담당자의-준비) |
| `workflow-agent` / `runtime-contract` | 검증된 workflow 출력 / 로컬 고정 profile·hash | [Lab 05 C](../labs/05-workflows.md) |
| `benchmark` | 버전 고정 Hosted smoke·matrix·평가·trace·인수 | [평가 워크북](evaluation-workbook.md) |
| `cloud-evaluate` / `calibrate-judge` | 저장된 응답의 유료 native 평가(Preview `--business-evaluator`는 본인 소유 코드 기반 업무 기준 추가, `--reference`는 다른 label의 평가에 합쳐 **실행 비교**, `--retry-failed`는 실패/invalid 시도만 보존하고 재시도) / 별도 calibration fixture | [Lab 07](../labs/07-evaluation.md), [워크북](evaluation-workbook.md) |
| `maf-evaluate` | Preview: MAF 함수 도구 에이전트를 dev 6문항으로 실행하고 Foundry에서 도구 호출·relevance를 채점 | [Lab 04](../labs/04-agents-tools.md) |
| `serve` | 로컬 host. 추론은 여전히 유료 | [Lab 08](../labs/08-hosted.md) |
| `toolbox` | 본인 관리형 도구·버전·재조회·MAF 호출 | [Toolbox](../labs/extensions/toolbox.md) |
| `prepare-extensions` | 동봉 dev/정책으로 로컬 심화 입력 생성. Holdout 사용 안 함 | [개발 도구](../labs/extensions/developer-toolkit.md) |
| `conversations` | 다중 턴 dev 수집·턴/대화별 평가 구분 | [대화 평가](../labs/extensions/conversation-evaluation.md) |
| `memory` | 명시적인 합성 store/scope 관리. 자동 agent memory 아님 | [Memory](../labs/extensions/memory.md) |
| `a2a` | 본인 A2A 1.0 target/caller·위임 기록 | [A2A](../labs/extensions/a2a.md) |
| `routines` | 기존 dispatch 확인. 전달 성공만으로 target 응답을 입증하지 않음 | [Routines](../labs/extensions/routines.md) |
| `code-interpreter` / `openapi` | 합성 정책 CSV 생성 / 본인 Search index 읽기 | [추가 도구](../labs/extensions/additional-tools.md) |

기본 GA `retrieve --provider iq`와 선택한 모델 기반 `iq-chat`은 의도적으로 다른 경로입니다.

### 보조 스크립트

| 스크립트 | 목적·부작용 |
|---|---|
| `scripts/export_policy_docs.py --language ko` | 선택 로컬 파일 6개 export. A의 학습자 ZIP에 이미 포함 |
| `scripts/build_learner_materials.py` | 두 언어 번들 검사. 관리자의 `--write`는 모델/holdout 없이 재생성 |
| `scripts/prepare_hosted_azd.py --kind runtime` | 검증된 패키지에서 별도 local/v2/Responses 프로젝트 생성. 전체 명령은 [Lab 08](../labs/08-hosted.md) |
| `scripts/prepare_hosted_azd.py --kind matrix` | 별도 순차 IQ/account-chat/Invocations v1/v2 프로젝트. 값은 [워크북](evaluation-workbook.md)에서 준비 |
| `scripts/play_recordings.py` | Localhost 영상 서버. 영어 기본, `--edition ko`로 독립 국문 세트 선택 |

완전한 터미널 명령이 아니라 스크립트 이름입니다. 연결된 절차를 따라갈 때만 앞에 `python`을 붙입니다.
Hosted 준비는 로컬 azd 상태를 생성/재조회할 수 있지만 provision·배포·역할 부여는 하지 않습니다.

</details>

## Hosted workflow와 평가 확장

<details>
<summary>심화 matrix 옵션 — 워크북의 준비를 마친 뒤에만 사용합니다</summary>

아래 줄인 명령 앞에 `python scripts/workshop.py`를 붙입니다.

| 명령 | 계약 |
|---|---|
| `runtime-contract --kind workflow ...` | 로컬 profile, 언어, 모델 map, 데이터·지침·코드 hash |
| `workflow-agent --pattern sequential` | case별로 분리한 실제 MAF pipeline과 검증된 답변 하나 |
| `seed-search --hybrid --confirm-create --confirm-cost` | 실제 embedding과 별도로 소유한 vector index |
| `retrieve --provider hybrid` | text·vector 결합 검색. 이름만 바꾼 키워드 조회가 아님 |
| `benchmark plan` | 모델·case·비용 규모만 계산. Azure 호출 없음 |
| `benchmark smoke --local --azd-directory ...` | 실제 로컬 host와 유료 모델. 폴더는 필수이며 소스 복사본에서 추론하지 않음 |
| `benchmark smoke` | 정확한 원격 version·endpoint. 요청에 정답 label을 넣지 않음 |
| `benchmark collect` | 명시한 모델×case matrix 전체. 오류 보존 |
| `benchmark evaluate --reference ...` | 고정한 catalog·version·judge로 실제 native 점수 |
| `benchmark compare` | 같은 dataset·corpus·코드·모델·API·검색·동시성. 언어 간 지름길 없음 |
| `benchmark regression ... --confirm-review` | 명시적 dev 검토와 원본 계보 보존 |
| `--regressions <reviewed-label>` | 다음 dev 수집이 검토한 reference를 실제로 사용 |
| `calibrate-judge` | 미리 작성한 정답·오답으로 실제 judge 검사 |
| `benchmark trace-plan` / `monitor` | 로컬 KQL / 범위를 지정한 실제 App Insights 확인 |
| `benchmark verify` | 독립 인수 게이트. 운영 승인이 아님 |
| `benchmark stop-session` | 기록한 session·version만 중지하거나 이미 idle인지 확인 |

완전한 명령과 승인 경계는 [평가 워크북](evaluation-workbook.md)에 있습니다.

</details>

## 명령에 대응하는 코드 찾기

시작점은 [`scripts/workshop.py`](../../../scripts/workshop.py), 다음은 [`cli.py`](../../../src/foundry_workshop/cli.py)입니다.
CLI가 입력을 해석·검증하고 구현 하나를 선택해 결과를 출력/저장합니다.
Cloud 분기는 `settings.py`로 `.env`를 읽고 오프라인 분기는 읽지 않습니다.
모든 모듈을 순서대로 읽지 말고 아래의 해당 파일부터 확인합니다.

| 확인할 내용 | `src/foundry_workshop/` 아래 파일 |
|---|---|
| 설정·입출력 schema·hash | `settings.py`, `contracts.py` |
| 로컬 검색·기본 수집·업무 게이트 | `knowledge.py`, `experiments.py`, `evaluation.py` |
| 프로젝트 모델 호출·관리형 Prompt Agent | `cloud.py` |
| 로컬 MAF·배포용 workflow | `agents.py`, `runtime.py` |
| Search/hybrid·별도 IQ Chat preset | `search.py`, `iq_chat.py` |
| Runtime profile·패키지·Hosted 전송 | `profiles.py`, `packaging.py`, `hosted.py` |
| Hosted matrix·native judge·trace | `benchmark_cli.py`, `benchmark.py`, `cloud_evaluation.py`, `native.py`, `calibration.py`, `observability.py` |
| 관리형 도구·대화 | `toolbox.py`, `toolbox_host.py`, `conversations.py` |
| 선택 심화 실습 | `a2a_lab.py`, `memory_lab.py`, `routines_lab.py`, `openapi_lab.py`, `code_interpreter_lab.py`, `resilience.py` |
| 결정적 학습자/확장 자료 생성 | `materials.py`, `extension_materials.py` |

대응하는 `tests/` 계약은 오프라인으로 실행합니다. `tests_sdk/`도 설치한 SDK와 명시적인 stub 전송을 사용하며 실제 Azure 실행이 아닙니다.
