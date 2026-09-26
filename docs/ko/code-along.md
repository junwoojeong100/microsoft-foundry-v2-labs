# 코드 따라 만들기: SDK 동작을 예상하고, 틀려 보고, 고치기

[English](../code-along.md) | **한국어**

**본인 코드 사본, 이유를 설명할 수 있는 실패 기록, 수정 후 통과 결과를 남깁니다.**
기본 B 인계 후 또는 [Lab 00의 로컬 환경 준비](labs/00-start.md#path-b) 후에 선택하는 연습입니다.
A/B의 추가 필수 랩이 아닙니다.

**실행 방식:** 설치된 SDK와 미리 정한 합성 테스트 응답을 사용합니다. **Azure 로그인·모델 호출·배포·`.env`는 필요 없습니다.**
두 언어의 가이드 모두 같은 **영어 테스트 fixture**를 사용합니다. 영문·국문 모델을 새로 비교하는 실험이 아닙니다.
검사 대상은 API 연결 방식이며 답변 품질을 측정하지 않습니다.

## 1. 로컬 연습 환경 준비

소스 저장소 루트에서 Bash/zsh(Windows는 WSL)와 활성화된 Python **3.13** 가상환경을 사용합니다.
기존 `.venv`를 유지하며, 잘 동작하는 환경을 교체하거나 다시 설치하지 않습니다.
새 환경이면 [Lab 00 3단계](labs/00-start.md#3-가상환경과-sdk-설치)를 완료하고,
그 다음 `.env` 설정과 Azure 로그인으로 가지 말고 **이 페이지로 돌아옵니다.**

이 선택 연습은 Hosted 어댑터도 다루므로 전체 SDK 조합이 필요합니다.
현재 환경에 아직 설치되지 않았다면 실행합니다.

```bash
python -m pip install -r requirements.lock.txt -e ".[cloud,agents,hosted,dev]" &&
python -m pip check
```

패키지를 내려받을 인터넷 연결은 필요하지만 아래 연습에는 Azure가 필요하지 않습니다.
모의 테스트를 통과시키려고 인증정보를 추가하지 않습니다.

## 2. 개인 사본을 한 번만 만들기

작은 예제 여섯 개는 완성된 시작 코드이며 워크숍 CLI를 대신할 운영 코드가 아닙니다.
이번 연습에서는 `examples/recipes/`·`src/`·`prompts/`·`data/`·테스트 원본을 수정하지 않습니다.
진행 중인 Lab 07 비교를 멈추고 그 입력을 바꾸지 않습니다.

```bash
mkdir -p outputs &&
mkdir outputs/code-along-ko &&
cp examples/recipes/{02_responses.py,03_prompt_agent.py,04_maf_tool.py,05_maf_sequential.py,06_iq_retrieve.py,08_hosted_agent.py} outputs/code-along-ko/
```

대상 폴더가 이미 있으면 실행이 멈춥니다. 이번 회차의 사본이라면 복사로 덮어쓰지 말고 다시 엽니다.
새 회차라면 새 폴더를 정하고 아래 모든 명령의 경로도 일관되게 바꿉니다.

| 내 사본에서 열 파일 | 찾을 코드 | 실행 전에 설명해 볼 것 |
|---|---|---|
| `02_responses.py` | `client.responses.create`, `store=False` | 어떤 모델을 호출하며, 어떤 서비스 ID를 돌려받나요? |
| `03_prompt_agent.py` | `create_version`, `agent_reference` | 왜 `latest` 대신 반환된 버전을 호출하나요? |
| `04_maf_tool.py` | `@tool`, `lookup_policy`, `tools=[...]` | 함수를 실행하는 주체는 누구이며, 근거가 없으면 어떤 뜻인가요? |
| `05_maf_sequential.py` | `SequentialBuilder(participants=[analyst, writer])` | 어떤 역할이 먼저 실행되고 어떤 출력을 돌려주나요? |
| `06_iq_retrieve.py` | `/knowledgebases(`, `api-version`, `raise_for_status` | 왜 실패한 IQ 요청을 오류로 남겨야 하나요? |
| `08_hosted_agent.py` | `ResponsesHostServer`, `build_server` | 로컬에서 프로토콜을 제공하는 것이 배포 완료는 아닌 이유는 무엇인가요? |

`main()`만 보지 말고 표에 나온 함수를 읽습니다.
**복사한 `.py` 파일을 직접 실행하지 않습니다.** 그 파일의 `main()`은 실제 Azure 실행 예제입니다.
이 오프라인 연습에는 `scripts/check_recipes.py`만 사용합니다. 고정 전송·정책 fixture를 테스트 전에 선택하며,
실제 요청의 오류 뒤에 대체하지 않습니다. 소켓 차단은 추가 보호 장치이지 **보안 샌드박스가 아닙니다.** 신뢰할 수 있는 본인 사본만 실행합니다.

## 3. 수정 전 사본 확인

```bash
(
  set -C
  python scripts/check_recipes.py --directory outputs/code-along-ko > outputs/code-along-ko/check-baseline.json
)
```

테스트 진행은 터미널에 표시되고 JSON 요약은 `check-baseline.json`에 저장됩니다.
괄호는 `set -C`의 적용 범위를 이 블록으로 한정합니다. 출력 파일이 이미 있으면 **Python 실행 전에** 거절합니다.
새 시도에는 새 보고서 이름을 사용하며, 자리를 만들려고 이전 결과를 지우지 않습니다.

**확인:** JSON을 열어 `mode: offline-sdk-practice`, `status: passed`, `tests_run`과 `tests_expected`의 일치,
`failures`·`errors`·`skipped`·`expected_failures` 모두 0, `source_unchanged: true`를 확인합니다.
`azure_tested: false`와 `model_quality_measured: false`는 그대로 둡니다.
테스트·예제·fixture 해시로 어떤 입력을 확인했는지 구분합니다.
수정 전 사본부터 실패한다면 일부러 코드를 틀리게 만들기 전에 그 원인부터 해결합니다.

## 4. 동작 조건 하나를 틀리게 만든 뒤 고치기

**내 사본**의 `02_responses.py`에서 `ask` 안의 `store=False`를 찾아 그 값만 `store=True`로 바꿉니다.
어떤 검사가 실패해야 할지 먼저 예상합니다. 요청의 저장 동작이 조용히 바뀌면 안 됩니다.

```bash
(
  set -C
  python scripts/check_recipes.py --directory outputs/code-along-ko > outputs/code-along-ko/check-store-broken.json
)
```

**예상한 실패:** 종료 코드 `1`, `status: failed`,
`test_responses_recipe_returns_service_ids_without_storing`의 실패입니다.
모의 요청이므로 Azure에 실제 응답을 저장한 것은 아닙니다. 패키지 누락이나 문법 오류는 다른 실패입니다.
빨간 결과라면 무엇이든 정답이라고 하지 말고 터미널 메시지를 읽습니다.

같은 사본을 `store=False`로 복구한 뒤 실행합니다.

```bash
(
  set -C
  python scripts/check_recipes.py --directory outputs/code-along-ko > outputs/code-along-ko/check-store-repaired.json
)
```

**확인:** 수정 후 선택된 검사 전체가 통과해야 합니다. 예제 해시를 baseline과 비교합니다. 바이트까지 똑같이 복구했다면 해시도 같습니다.
실패한 것을 포함한 요약 세 개를 모두 보관하고, 무엇을 바꾸었으며 어떤 영향이 있는지 본인 기록에 설명합니다.
통과시키려고 테스트·기대값·저장된 JSON을 수정하지 않습니다.

## 5. 선택: 두 가지 실수 더 연습하기

한 행씩 시도하고 원래대로 고친 뒤 다음 행으로 갑니다. 모두 내 사본에서만 수정합니다.

| 파일 | 일부러 만들 실수 | 거절해야 하는 검사 | 복구 |
|---|---|---|---|
| `03_prompt_agent.py` | `invoke`의 `"version": version`을 `"version": "latest"`로 변경 | `test_prompt_agent_recipe_creates_a_prompt_version_and_pins_it` | 반환된 `version`으로 복구 |
| `05_maf_sequential.py` | `participants=[analyst, writer]`를 `participants=[writer]`로 변경 | `test_sequential_recipe_runs_both_agents_and_returns_outputs` | 두 참여자와 원래 순서 복구 |

각 실패·복구 상태마다 새 보고서 이름으로 같은 검사기를 실행합니다.

```bash
(
  set -C
  python scripts/check_recipes.py --directory outputs/code-along-ko > outputs/code-along-ko/check-extra-01.json
)
```

다음 시도 **전에** `check-extra-01.json`을 `check-extra-02.json` 등으로 바꿉니다.
각 파일이 어느 실수·상태의 결과인지 적습니다. 변경한 예제가 테스트 실패 또는 SDK 오류를 낼 수 있습니다.
둘 다 보존하며 어느 것도 Azure 서비스 실행 결과가 아닙니다.

## 6. 마무리 또는 복구

| 상황 | 다음 행동 |
|---|---|
| `No module named ...` | Python 3.13과 활성화된 `.venv`를 확인한 뒤 1단계의 고정된 선택 SDK 조합 설치 |
| `Missing or redirected recipe` | 복사한 폴더의 파일 이름 여섯 개 확인. ZIP이나 심볼릭 링크를 가리키지 않음 |
| 출력 파일이 이미 있음 | 해당 결과를 읽거나 새 보고서 이름 사용. 이전 파일 보존 |
| `blocked a network connection` | 중단. 사본이 정해진 모의 실행 경로를 벗어나려 했으므로 로그인하거나 차단을 풀지 말고 변경 내용 확인 |
| 수정 후에도 실패 | 실제 첫 오류를 읽고 원래 예제와 대조한 뒤 내 사본만 수정 |

**완료:** baseline과 수정 후 요약이 통과하고, 의도한 실패 요약이 남아 있으며, 어떤 API 동작 조건을 어겼는지 설명할 수 있습니다.
이는 **SDK 연습 완료**이지 B의 Azure 실습 완료·모델 점수·배포 승인이 아닙니다.
코드 사본과 보고서는 로컬에 보관합니다. 이 연습만 했다면 정리할 클라우드 리소스는 없습니다.

[B의 구현 확장](paths/b-practitioner.md)으로 돌아가거나 [C 모듈](paths/c-advanced.md)을 고릅니다.
