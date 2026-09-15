# Lab 00. 시작과 공통 환경

[English](../../labs/00-start.md) | **한국어**

**완료 목표:** 내가 사용할 계정·프로젝트·경로를 알고, 다음 실습의 출발점을 확인합니다.

상위: [학습 경로](../paths.md) · 다음: [Lab 01](01-foundry.md)

## 이 가이드의 화면 읽는 법

각 단계의 이미지는 **2026-09-14 원본과 개별 표시한 2026-09-15 새 영문 가이드 촬영 예시**입니다.
[새 영상과 범위](../english-recordings.md)에서 실제 호출·문서 화면·과거 보고서를 구분합니다. 클릭하면 크게 볼 수 있습니다.
화면의 계정·프로젝트·모델·접두사를 그대로 복사하지 말고 강사가 제공한 본인 값과 대조하세요.
터미널 이미지는 **마지막으로 입력한 명령(`workshop $` 뒤에 내용이 있는 줄)과 그 아래 결과**를 읽습니다.
위쪽에는 앞 명령의 출력이 남아 있을 수 있고, 맨 아래의 빈 프롬프트는 명령이 끝났다는 표시입니다.
`OFFLINE FIXTURE`와 `LIVE AZURE`를 구분하고, `RUN_TOOLS`·추가 `tee` 저장 경로는 촬영 보조용이므로
이미지에서 복사하지 않습니다. **실행할 명령은 본문의 코드 블록**입니다.
더 많은 전·후 화면은 [액션 인덱스](../action-captures.md)에 있습니다.

## A. 브라우저 — 코드를 몰라도 됩니다

1. Edge 또는 Chrome에서 `https://ai.azure.com`을 엽니다.
2. 강사가 지정한 **Microsoft Entra 계정과 디렉터리(tenant)**로 로그인합니다.
   개인 Microsoft 계정·GitHub 로그인과 Azure 업무 계정은 같은 개념이 아닙니다.
3. 강사가 알려 준 프로젝트를 선택합니다. 이름이 비슷한 운영 프로젝트를 선택하지 않습니다.
4. 아래 워크시트의 앞 네 칸을 적습니다. 화면 전체나 개인 정보를 공유 채팅에 올리지 않습니다.
5. [Lab 01](01-foundry.md)로 이동합니다. 설치 절은 강사가 준비하므로 여기서는 건너뜁니다.
   [Lab 05](05-workflows.md)에서는 준비된 MAF 터미널에서 명령을 복사해 실행합니다.
   Python 코드를 직접 작성하거나 포털에서 workflow를 만들지는 않습니다.

![프로젝트 목록에서 실습 이름으로 필터링한 화면](../../assets/live-20260914-action/shots/portal-0016-P00-003-search-new-project-screen-change.webp)

**화면 확인:** 프로젝트 선택 메뉴에서 찾기 어렵다면 **View all resources**로 이동하고 검색칸에
실습 프로젝트 이름을 입력합니다. 결과 행의 이름·부모 리소스·리전을 확인한 뒤 프로젝트 링크를 누르세요.

![선택한 프로젝트 홈과 프로젝트 endpoint](../../assets/live-20260914-action/shots/portal-0021-P00-004-select-new-project-ready.webp)

**화면 확인:** 상단의 프로젝트 이름이 바뀌었는지 확인합니다. **Project endpoint**는 뒤의 `.env`에 넣을 값이며,
현재 브라우저 주소 `ai.azure.com`과 다릅니다. 로그인·PIN 화면은 촬영하지 않았습니다.

| 확인 항목 | 내가 확인한 값 |
|---|---|
| 실습용 tenant / 구독 | 강사가 지정한 값 |
| Foundry 리소스 / 프로젝트 | 강사가 지정한 값 |
| 사용할 모델의 **배포 이름** | 카탈로그 모델 이름과 구분 |
| 개인/조별 에이전트 접두사 | 예: `mfv2-team01-0913` |
| 경로 | A / B |
| 실행 상태 | 직접 실행 / 강사 관찰 / 미실행 |

프로젝트가 보이지 않으면 **다른 계정으로 무작정 새 리소스를 만들지 않습니다.**
[문제 해결](../reference/troubleshooting.md)의 tenant/RBAC 항목으로 이동합니다.

## B. 코드 — 한 폴더, 한 환경

지원: macOS/Linux 또는 Windows의 WSL, Bash/zsh, Python 3.13 권장.
Python 3.14는 오프라인 코드에 사용할 수 있지만 hosted 런타임은 3.13으로 맞춥니다.
전역 Python에 패키지를 설치하거나 시스템 기본 구독을 바꾸지 않습니다.

### 1. 폴더 열기

배포받은 ZIP을 풀거나 이 작업 폴더를 VS Code로 엽니다.
터미널의 현재 위치에 `README.md`, `pyproject.toml`, `scripts/`가 있어야 합니다.
새 원격 리포가 아직 게시되지 않았다면 존재하지 않는 GitHub URL을 추측해 clone하지 않습니다.
Hosted까지 확인하려면 다른 azd 프로젝트의 하위 폴더가 아닌 독립된 실습 폴더를 사용합니다.

```bash
pwd
python3.13 --version
python3.13 scripts/workshop.py doctor
```

정상 출력에는 `documents: 6`, `dev_cases: 6`, `holdout_cases: 4`,
`azure_tested: false`, `result: PASS`가 있습니다.
**이 PASS는 Azure 로그인 성공이 아닙니다.**

**새 영문 가이드 촬영: 2026-09-15.** ▶ [이 액션 재생](https://github.com/user-attachments/assets/082ede4b-d363-474c-ad47-598b20f593e9#t=58.68)

![오프라인 doctor의 문서 수와 Azure 미검증 표시](../../assets/english-20260915/shots/terminal-0021-00-004-doctor-result.webp)

**화면 확인:** `documents: 6`, `dev_cases: 6`, `holdout_cases: 4`와 함께 `azure_tested: false`를 읽습니다.
이 단계에서는 파일과 실행 환경만 확인하며 Azure 호출 성공을 판정하지 않습니다.

### 2. Azure 없이 먼저 실행 형태 익히기

```bash
python3.13 scripts/workshop.py demo --label rehearsal-v1 --prompt v1
python3.13 scripts/workshop.py demo --label rehearsal-v2 --prompt v2
python3.13 scripts/workshop.py compare --baseline rehearsal-v1 --candidate rehearsal-v2
```

`outputs/rehearsal-v2/`에서 `manifest.json`, `responses.jsonl`,
`business-evaluation.json`을 엽니다.
v1은 **고정 답변에서 인용을 제거한 검사기 연습**, v2는 고정 답변 원본입니다.
두 점수의 차이를 “프롬프트 개선 실측”이라고 발표하면 안 됩니다.
재실행하려면 `rehearsal2-v1`처럼 새 label을 사용합니다.

![오프라인 fixture 비교 결과와 해석상 주의 문구](../../assets/live-20260914-action/shots/cli-1-0036-00-007-demo-compare-result.webp)

**화면 확인:** 상단의 `OFFLINE FIXTURE` 표시와 결과 끝의 주의 문구를 확인합니다.
고정 답변에 대한 검사 결과이지, 두 프롬프트로 모델을 실제 호출해 얻은 성능 차이가 아닙니다.

### 3. 가상환경과 SDK 설치

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[cloud,agents]"
```

설치 버전은 `pyproject.toml`에 고정되어 있습니다. `agent-framework` 전체 메타패키지를
추가 설치하지 않습니다. Hosted 실습에서만 `.[hosted]`를 추가합니다.
다운로드 실패를 인증서 검증 해제나 출처 불명의 미러로 우회하지 않습니다.

새 터미널을 열 때는 저장소 루트로 돌아와 `source .venv/bin/activate`를 다시 실행합니다.
브라우저의 개발자 콘솔이나 Python의 `>>>` 프롬프트에 Bash 명령을 붙여 넣지 않습니다.

![고정된 cloud와 agents 패키지 설치가 끝난 터미널](../../assets/live-20260914-action/shots/cli-1-0113-00-011-install-core-result.webp)

**화면 확인:** 설치 명령이 끝나고 셸 프롬프트가 돌아왔는지 확인합니다. 설치 중 오류가 있었다면
이 화면과 같다고 넘어가지 말고 해결하세요. 설치 완료도 Azure 연결 성공과는 별개입니다.

### 4. 로그인과 `.env`

Azure CLI 설치는 [공식 설치 가이드](https://learn.microsoft.com/cli/azure/install-azure-cli)를
사용합니다. 로그인은 학습자가 직접 합니다.

```bash
az login
cp .env.example .env
```

VS Code에서 `.env`를 열어 강사가 제공한 값을 입력합니다.
이미 `.env`가 있다면 복사 명령으로 덮어쓰지 말고 기존 파일을 확인합니다.

| 필수 값 | 어디에서 얻나요? |
|---|---|
| `AZURE_SUBSCRIPTION_ID`, `AZURE_TENANT_ID` | 지정된 구독과 디렉터리의 ID |
| `AZURE_RESOURCE_GROUP`, `AZURE_AI_ACCOUNT_NAME` | 강사가 준비한 실습 리소스 |
| `AZURE_AI_PROJECT_ENDPOINT` | 프로젝트의 **전체** endpoint |
| `AZURE_AI_MODEL_DEPLOYMENT_NAME` | 프로젝트가 사용하는 실제 모델 배포 이름 |
| `WORKSHOP_PREFIX` | 본인/조의 고유한 `mfv2-...` 접두사 |
| `WORKSHOP_AUTH_MODE` | 로컬은 `cli`; 실제 Azure 런타임만 `managed-identity` |

스크립트는 `.env`를 읽지만 이미 설정된 환경변수는 덮어쓰지 않습니다.
endpoint가 다른 터미널에 남아 있으면 새 터미널에서 다시 확인합니다.
API key, 비밀번호, access token은 이 파일에 넣지 않습니다.
Microsoft 365 계정이나 실제 고객 문서도 필요하지 않습니다.

### 5. 읽기 전용 Azure 검사

```bash
python scripts/workshop.py doctor --cloud
```

실습 구독, tenant, 배포의 실제 모델·버전과 `Succeeded` 상태를 확인합니다.
이 명령은 리소스를 만들거나 기본 구독을 바꾸지 않습니다.
ARM을 읽을 권한이 없는 참가자는 강사에게 확인을 요청합니다.
검사 통과만으로 모델의 데이터 평면 권한/Structured Outputs 지원이 증명되지는 않습니다.
그 확인은 [Lab 02](02-models.md)의 실제 호출에서 합니다.

![클라우드 doctor의 모델 배포 및 사전 점검 결과](../../assets/live-20260914-action/shots/cli-1-0227-00-015-cloud-doctor-result.webp)

**화면 확인:** 배포의 실제 `model`·`version`, `provisioningState: Succeeded`를 확인합니다.
`inference_tested: false`와 `next_step`도 읽으세요. 다음 랩에서 실제 응답을 받아야 추론 경로까지 확인한 것입니다.

## 이 랩의 완료 기준

- A: 올바른 프로젝트를 열고, 배포 이름과 내 경로를 설명할 수 있습니다.
- B: 오프라인 검사와 SDK 설치를 마쳤고, cloud preflight의 결과를 이해합니다.
- 승인 대기자: 오프라인 체험만 마쳤다면 `Azure 실습 미실행`으로 기록합니다.
