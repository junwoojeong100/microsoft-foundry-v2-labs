# 같은 고정 버전 Toolbox agent를 Hosted로 실행하기

[English](../../../labs/extensions/toolbox-hosted.md) | **한국어**

**B/C 확장.** [Toolbox 로컬 요청](toolbox.md)을 먼저 완료합니다.
같은 MAF wrapper·버전 검증·오류 보존 코드를 사용합니다. 이전 workflow의 품질 점수를 새 대상에 옮기지 않습니다.

**근거 상태:** 영문 로컬·원격 Hosted Toolbox 실행은 2026-09-16(이전 `gpt-5.6-luna` preset) 기록이며 `gpt-6-sol`로 다시 실행하지 않았습니다.

**준비:** 실제 동작한 소유 Toolbox 버전, 합성 seed ledger, Hosted SDK, [준비된 azd 접근](developer-toolkit.md#azd-check), 기존 프로젝트의 전체 ARM ID,
새 agent 이름과 배포/모델/도구 권한 승인.
**완료:** 새 원격 버전이 실제 도구·모델·근거 metadata를 반환함.
**중단:** 시도한 단계·오류·생성된 ID는 **실패/차단**으로 보관하고 시도하지 않은 단계는 **미실행**으로 적습니다.
패키징만 선택했다면 1절 뒤에 멈추고 [Lab 11](../11-capstone.md)로 돌아갑니다. 패키징은 로컬·원격 서비스 실행 검증이 아닙니다.

**첫 회차:** 1절은 로컬 패키징입니다. 2–3절은 격리된 azd 상태를 준비하며, 2절은 `azd ai project show`도 실행합니다.
그 azd/프로젝트 확인은 패키징만 하는 준비와 구분합니다. 4절은 로컬 서버에서 실행하지만
실제 Foundry 모델과 Toolbox/Search를 호출하는 **Azure 실행이며 오프라인 fixture가 아닙니다**.
4절의 요청 전에 모델·도구 비용 승인을 받습니다. 5절의 Hosted 배포와 원격 요청은 별도로 승인합니다.
사용한 자산은 6절로 마무리합니다. 두 터미널 모두 **소스 저장소 루트**와
[Hosted SDK 환경](developer-toolkit.md#hosted-sdk)을 유지하고 `--cwd`로 독립 azd 프로젝트를 선택합니다.

## 1. 런타임과 질문만 패키징

패키징 **전에 분기를 선택**합니다.

- **일반 Toolbox:** [Toolbox 실습](toolbox.md)에서 검증한 버전을 입력하고 아래 명령을 그대로 사용합니다.
- **Skill이 연결된 Toolbox:** [Tool Search/Skills](tool-search-skills.md)에서 검증한 `SKILLED_VERSION` 값을 입력합니다.
  아래 패키징 명령과 4절 서버 명령을 **실행하기 전에** 두 명령 모두에 `--with-skill`을 추가합니다.

이 선택은 패키지에 고정됩니다. 옵션 없이 먼저 패키징한 뒤 기존 패키지를 덮어쓰려고 하지 않습니다.
저장소 터미널에서 선택한 분기의 검증된 버전을 입력합니다.

```bash
printf '검증한 Toolbox 버전: '
read -r TOOLBOX_VERSION
python scripts/package_toolbox.py --language ko --version "$TOOLBOX_VERSION"
```

`.build/toolbox-ko-<version>/`에는 코드·합성 정책·질문·고정된 `toolbox-profile.json`만 들어갑니다.
정답, holdout, `.env`, 이전 출력은 제외합니다.
`package-manifest.json`과 파일 hash를 보관합니다. `cloud_deployed: false`는 패키징만 했다는 기록이지 Hosted 준비 완료가 아닙니다.
프로젝트·모델·Toolbox·Search 연결/원문 설정을 고정합니다.

Hosted의 `/app`은 읽기 전용입니다. 요청 근거는
`/app/outputs`가 아니라 `$HOME/workshop-evidence/toolbox-runs`에 저장합니다.
세션 삭제 전에 기록된 세션의 `files` 명령으로 내려받습니다.
출력된 **절대 패키지 경로**를 아래 준비의 `HOSTED_PACKAGE`로 보관하고 기존 패키지를 덮어쓰지 않습니다.
패키징 뒤 runtime 값을 몰래 바꾸거나 기존 package 위에 다시 빌드하지 않습니다.

## 2. 별도 azd 실행 폴더 준비

기존 azd 프로젝트의 상위/하위 경로가 아닌 빈 폴더를 사용합니다.
교육 저장소를 따로 만드는 것이 아니라 실행 상태를 격리하는 단계입니다.
package는 원래 repository 폴더에 남아 있어도 됩니다.
저장소 터미널 A에서 실제 값을 입력합니다. `~` 축약형 없이 절대 경로를 사용하고
새 터미널에서도 복원하도록 폴더·이름을 `session-notes.txt`에 기록합니다.
준비된 azd 접근이 있을 때만 계속합니다. helper가 성공하면 이어지는 `azd ai project show`가 기존 프로젝트를 조회합니다.
모델 추론은 아니지만, 패키징 성공만으로 그 접근 권한이 검증된 것은 아닙니다.

```bash
printf '절대 Toolbox 패키지 경로: '
read -r HOSTED_PACKAGE
printf '실제 기존 프로젝트 ARM ID: '
read -r PROJECT_ARM_ID
printf '새 agent 이름 (<내 prefix>-toolbox-hosted-ko): '
read -r HOSTED_AGENT_NAME
printf '비어 있는 azd 폴더의 절대 경로: '
read -r HOSTED_DIRECTORY
printf '실제 기존 프로젝트의 리전 코드 (예: swedencentral): '
read -r PROJECT_LOCATION
python scripts/prepare_hosted_azd.py --language ko --kind toolbox \
  --package "$HOSTED_PACKAGE" --directory "$HOSTED_DIRECTORY" \
  --agent-name "$HOSTED_AGENT_NAME" --initialize-env \
  --project-id "$PROJECT_ARM_ID" --location "$PROJECT_LOCATION" &&
azd ai project show --cwd "${HOSTED_DIRECTORY:?Use the prepared standalone directory}" --output json
```

helper는 모든 package 파일을 확인하고 정확한 package 사본과 JSON 형식의 YAML manifest를 만듭니다.
agent 하나와 기존 프로젝트 endpoint만 포함하고 `azd env new/set/get-value`로
이 폴더의 로컬 azd 환경만 초기화합니다. provision이나 deploy는 절대 실행하지 않습니다.
실제 ARM ID를 설정된 구독·계정·프로젝트와 대조합니다.
비어 있지 않은 폴더, 기존 azd 프로젝트의 하위 폴더, 변경된 package나 설정은 거부합니다.
9월 16일 CLI에서 빈 폴더의 `init --src ... --no-prompt`는 template 선택을 요구할 수 있고,
template 내부에서 자기 자신을 채택하면 source/destination 중첩 오류가 발생할 수 있습니다.
이 경로는 완성된 manifest를 이미 제공하므로 두 초기화 경로를 실행하지 않습니다.
다른 모델을 만드는 sample을 선택하거나 새 프로젝트용 `azd provision`을 실행하지 않습니다.
준비가 실패하면 폴더·오류를 보존하고 멈춥니다. 다음 azd 명령을 소스 프로젝트의 context에서 실행하지 않습니다.

## 3. 원격 설정을 패키지와 맞추기

helper는 저장소 `.env`를 데이터로 읽고 package profile과 비교한 뒤
프로젝트·모델·Toolbox·Search의 명시적 값만 agent service의 `env`에 기록합니다.
`WORKSHOP_AUTH_MODE: managed-identity`, 출력 토큰 2048, 1 CPU / 2 GiB도 지정합니다.
credential, 정답, 대체 모델이나 새 모델 배포는 포함하지 않습니다.
로컬 환경의 `AZURE_AI_PROJECT_ENDPOINT`와 project extension이 요구하는
`FOUNDRY_PROJECT_ENDPOINT`도 같은 원래 endpoint로 설정하고 다시 읽어 비교합니다.
배포 전에 실제 값을 확인하며 `.env`를 셸 `source`로 읽거나 manifest 전체·영상 속 ID로 덮어쓰지 않습니다.
runtime binding이나 schema가 달라졌다면 배포 전에 멈춥니다.

원격 identity는 upstream Search identity 권한과 별개로 Foundry 프로젝트 접근 권한이 필요합니다.
배포 후 담당자는 새 agent 버전에서 반환된 **실제 runtime principal ID**를 읽고 필요하면 프로젝트 범위 Foundry User를 부여합니다.
가정한 principal에는 권한을 부여하지 않습니다. 로컬 사용자의 권한이 Hosted ID로 이전되지 않습니다.

## 4. 두 터미널로 로컬 동작 확인

저장소 터미널 A에서 1절과 같은 분기로 실행합니다.
Skill이 연결된 버전이면 아래 명령에도 실행 전에 `--with-skill`을 추가합니다.

```bash
OTEL_SDK_DISABLED=true python scripts/workshop.py --language ko toolbox serve --version "$TOOLBOX_VERSION"
```

터미널 B도 소스 저장소 루트에서 2절의 폴더를 복원합니다.
A의 셸 변수가 자동으로 전달되지는 않습니다.

```bash
printf '2절에서 준비한 독립 Hosted 폴더: '
read -r HOSTED_DIRECTORY
curl --fail http://127.0.0.1:8088/readiness &&
azd ai agent invoke --cwd "${HOSTED_DIRECTORY:?Use the prepared standalone directory}" --local --new-session --new-conversation --timeout 210 "2026년 9월 국내 출장에서 170000원 호텔의 사전 승인 조건은?"
```

readiness만으로 완료하지 않습니다. JSON 답변에는 선택된 Toolbox 버전/hash, 실제 모델 호출, 성공한 함수/도구 작업, 원문 정책 근거가 포함되어야 합니다.
로컬 명령은 방대한 콘솔 metrics 출력을 피하려고 telemetry SDK를 명시적으로 끕니다.
따라서 App Insights export 검증이 아니며, 이 설정을 원격 환경에 넣지 않습니다.
이 실습 host는 동봉 dev와 지정된 Toolbox 질문만 받습니다.
마치면 A에서 내 server만 Ctrl+C로 종료합니다.

## 5. 실제 버전을 배포·호출·검증

배포 승인 후 서버를 종료한 터미널 A로 돌아옵니다.
1–2절의 정확한 패키지·폴더·agent 값이 남아 있어야 합니다.

```bash
azd deploy "${HOSTED_AGENT_NAME:?Use the prepared agent service name}" --cwd "${HOSTED_DIRECTORY:?Use the prepared standalone directory}" &&
azd ai agent show --cwd "${HOSTED_DIRECTORY:?Use the prepared standalone directory}" --output json
```

배포 오류 시 멈춥니다. 이전 active version을 새 배포로 표시하지 않습니다.
`show`에서 의도한 agent의 활성 상태를 확인한 뒤 새 실제 버전을 입력합니다.

```bash
printf '실제 새 agent 버전: '
read -r HOSTED_AGENT_VERSION
```

한 번 요청한 원래 stream을 저장·검증합니다. 새 기록 폴더가 이전 시도의 덮어쓰기를 막고
`pipefail`이 호출 실패를 `tee` 성공으로 숨기지 않게 합니다.

```bash
(
  set -o pipefail
  : "${HOSTED_PACKAGE:?Use the verified package directory}" &&
  mkdir -p outputs &&
  mkdir outputs/toolbox-remote-ko &&
  azd ai agent invoke "${HOSTED_AGENT_NAME:?Use the prepared agent service name}" \
    --cwd "${HOSTED_DIRECTORY:?Use the prepared standalone directory}" \
    --version "${HOSTED_AGENT_VERSION:?Use the version returned by show}" \
    --new-session --new-conversation --output raw --timeout 240 \
    "2026년 9월 국내 출장에서 170000원 호텔의 사전 승인 조건은?" \
    | tee outputs/toolbox-remote-ko/response.raw &&
  python scripts/verify_toolbox_response.py --file outputs/toolbox-remote-ko/response.raw \
    --package "$HOSTED_PACKAGE" --agent-name "$HOSTED_AGENT_NAME" \
    --agent-version "$HOSTED_AGENT_VERSION" --output outputs/toolbox-remote-ko/verified.json
)
```

`outputs/toolbox-remote-ko/`가 있으면 먼저 읽습니다. 실제 새 요청에는 폴더명을 바꾸고
**파일 경로 세 곳과 `mkdir`을 모두** 맞춥니다. 이전 결과를 삭제하지 않습니다.
agent/Session/Conversation/Trace ID와 실제 Toolbox 결과를 보관합니다.
**CLI가 0으로 끝났지만 답변이 없으면 통과가 아닙니다.**
재시도하거나 완료를 주장하기 전에 정확한 session log/trace와 response state를 점검합니다.
검증기는 원래 HTTP/SSE의 completed 상태, 정확한 버전, package hash, 실제 모델/도구/Skill 근거를 확인합니다.
모델을 다시 호출하지 않습니다.
package는 다른 프로젝트/모델/Toolbox/connection 값을 runtime에서 대안으로 선택하지 않고 거부합니다.
연결이나 index 자체는 바뀔 수 있으므로 그 설정과 실제 결과도 별도로 고정·확인합니다.

## 6. 공유 도구를 망가뜨리지 않고 마무리

[owned-session cleanup](../../reference/cleanup.md)을 이 새 Hosted agent에 사용합니다.
기록한 azd 폴더·agent·session을 지정해 `azd ai agent files list`와 `files download`로 남아 있는 근거를 받습니다.
경로는 세션 home 기준입니다. 성공했다면 검증기의 `remote_evidence_directory`를 사용하고,
검증에 실패했다면 같은 세션의 `workshop-evidence/toolbox-runs/`를 확인합니다.
Binding·request·model/function/tool 결과·summary 또는 `failure.json`과 package·response 근거를 보존합니다.
회수가 막히면 이유와 담당자를 적습니다. 소유 compute 중지는 회수가 끝날 때까지 기다릴 필요가 없으며 stopped/idle 상태를 확인합니다.
단, session이나 agent를 삭제하기 전에는 근거를 보존합니다.

새 Hosted agent를 삭제한다면 Toolbox, skill 또는 Search source를 제거하기 전에 참조 관계를 확인합니다.
공유 프로젝트·모델·Search 리소스를 삭제하거나 이전 endpoint/버전 ID를 재사용하지 않습니다.

**다음:** [C 모듈](../../paths/c-advanced.md), [Lab 11](../11-capstone.md).
