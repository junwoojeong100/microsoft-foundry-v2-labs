# Lab 00. 시작과 공통 환경

**완료 목표:** 내가 사용할 계정·프로젝트·경로를 알고, 다음 실습의 출발점을 확인합니다.

상위: [학습 경로](../paths.md) · 다음: [Lab 01](01-foundry.md)

## A. 브라우저 — 코드를 몰라도 됩니다

1. Edge 또는 Chrome에서 `https://ai.azure.com`을 엽니다.
2. 강사가 지정한 **Microsoft Entra 계정과 디렉터리(tenant)**로 로그인합니다.
   개인 Microsoft 계정·GitHub 로그인과 Azure 업무 계정은 같은 개념이 아닙니다.
3. 강사가 알려 준 프로젝트를 선택합니다. 이름이 비슷한 운영 프로젝트를 선택하지 않습니다.
4. 아래 워크시트의 앞 네 칸을 적습니다. 화면 전체나 개인 정보를 공유 채팅에 올리지 않습니다.
5. [Lab 01](01-foundry.md)로 이동합니다. 설치 절은 강사가 준비하므로 여기서는 건너뜁니다.
   [Lab 05](05-workflows.md)에서는 준비된 MAF 터미널에서 명령을 복사해 실행합니다.
   Python 코드를 직접 작성하거나 포털에서 workflow를 만들지는 않습니다.

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

## 이 랩의 완료 기준

- A: 올바른 프로젝트를 열고, 배포 이름과 내 경로를 설명할 수 있습니다.
- B: 오프라인 검사와 SDK 설치를 마쳤고, cloud preflight의 결과를 이해합니다.
- 승인 대기자: 오프라인 체험만 마쳤다면 `Azure 실습 미실행`으로 기록합니다.
