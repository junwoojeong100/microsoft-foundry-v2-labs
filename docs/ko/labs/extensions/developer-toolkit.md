# 개발 도구: 환경 하나와 선택적인 편집기 통합

[English](../../../labs/extensions/developer-toolkit.md) | **한국어**

**B 준비.** 기준 경로는 저장소의 Python CLI입니다.

**근거 상태:** 도구 확인은 2026-09-16(이전 `gpt-5.6-luna` preset) 기록이며 `gpt-6-sol`로 다시 실행하지 않았습니다.

Foundry Toolkit은 선택 편집기 UI이며 다른 구현이나 모든 최신 SDK 설치의 이유가 아닙니다.

**첫 회차:** 기본 B는 1절 후 자기 경로로 돌아갑니다. 아래 Hosted SDK·azd·편집기 확장은 별도로 선택한 모듈에만 필요합니다.

**준비:** Lab 00 B의 소스 폴더, `.venv`, `.env`, 본인의 `az login`.
`doctor --cloud`는 read-only 사전 확인이며 아무것도 만들지 않습니다.

## 1. 실제 Python과 프로젝트

[Lab 00 B](../00-start.md#b-코드--한-폴더-한-환경) 이후 VS Code에서 저장소를 열고
**Python: Select Interpreter**로 같은 `.venv`를 선택합니다. 새 터미널도 같은 루트와 환경을 사용합니다.

```bash
source .venv/bin/activate
python --version
python -m pip check
python scripts/workshop.py --language ko doctor
python scripts/workshop.py --language ko doctor --cloud
```

offline PASS는 cloud 인증이 아닙니다. cloud 사전 확인도 기능 지원 증거가 아니므로 Lab 02의 실제 요청을 완료합니다.

**기본 B 완료:** [B의 다음 미완료 단계](../../paths/b-practitioner.md)로 돌아갑니다.
기본 경로에 필요 없는 검사를 통과시키려고 Hosted 패키지·azd를 설치하지 않습니다.

<a id="hosted-sdk"></a>

### 선택한 모듈만: Hosted·Toolbox SDK

<details>
<summary>Toolbox·로컬 Hosted 서버·matrix·로컬 복구 전에 한 번 준비. B의 패키징 전용 단계에는 불필요</summary>

저장소 루트·활성 `.venv`에서 선언된 extra가 없을 때만 설치합니다.

```bash
python -m pip install -e ".[hosted]"
python -m pip check &&
python scripts/check_sdk.py
```

`check_sdk.py`는 `ResponsesHostServer`를 포함한 **cloud + agents + hosted**를 검사합니다.
기본 B 검사가 아닙니다. `passed: true`, `azure_requests_sent: false`를 확인합니다.
동작하는 준비 환경은 모듈마다 재설치하지 않습니다.
[로컬 복구 모듈](approval-recovery.md)은 agentserver 버전도 별도로 확인합니다.
필요하면 담당자가 [잠금 버전을 사용하는 리허설 환경](../../instructor.md#4-하루-전-같은-배포본으로-리허설)을 준비합니다.
SDK 불일치는 준비 오류이며 임의 패키지 upgrade나 Azure 호출로 해결하지 않습니다.

</details>

<a id="azd-check"></a>

## 2. 공유 설정을 바꾸지 않고 azd 확인

azd를 사용하는 모듈에만 필요합니다. 도구가 없다면
[공식 준비](https://learn.microsoft.com/azure/foundry/agents/how-to/install-cli-foundry-extensions)로 설치·로그인합니다.
설치·로그인은 agent 배포가 아닙니다.

```bash
azd version
azd ext list
azd auth login --check-status
azd ai agent init --help
```

설정 카드의 계정/프로젝트/모델과 일치해야 합니다.
수업 중 기본 구독을 바꾸거나 모든 extension을 전역 upgrade하지 않습니다.
호환성 문제는 준비 차단 사유이며 오류를 생략할 이유가 아닙니다.

## 3. 선택: Foundry Toolkit

[공식 설치/설정](https://learn.microsoft.com/azure/foundry/how-to/develop/install-foundry-toolkit-visual-studio-code)을 따릅니다.
해당 컴퓨터에서 담당자가 확장을 승인한 뒤에만 설치합니다.
설치 후:

1. VS Code Activity Bar에서 **Foundry Toolkit**을 엽니다.
2. 같은 의도된 Entra 계정으로 로그인합니다. terminal login이 자동 상속된다고 가정하지 않습니다.
3. **My Resources**에서 정확한 training project를 선택합니다.
4. 모델/agent inventory를 살펴보고 ID/endpoint를 설정 카드와 비교합니다.
5. 같은 workspace에서 source file과 terminal을 엽니다. 관련 없는 template에서 중복 project를 만들지 않습니다.

Toolbox는 [실행 가능한 CLI 경로](toolbox.md)부터 완료하고 Toolkit으로 같은 자산을 확인합니다.
설치/접근이 없으면 CLI 경로를 유지하고 편집기 통합은 **미실행**으로 표시합니다.
Marketplace 화면은 통합 성공 증거가 아닙니다.

## 4. 호환성 snapshot

고정 dependency는 검증한 조합이지 항상 최신을 사용한다는 약속이 아닙니다.
MAF Python 1.18의 vector store/tool-loop/dependency·serialization 변경은
별도 환경에서 provider/Projects/OpenAI/hosting 전체 조합으로 검토합니다.
단일 library import 성공만으로 호환성을 추정하지 않습니다.

도움말과 생성된 `azure.yaml`도 실행 계약입니다.
과거 화면/샘플과 다르면 차이를 보존하고 실제 작업을 확인한 뒤 가이드를 수정합니다.

**다음:** 이곳으로 보낸 모듈로 돌아가거나 [B의 다음 미완료 단계](../../paths/b-practitioner.md)로 이동합니다.
[MAF 1.18](https://github.com/microsoft/agent-framework/releases/tag/python-1.18.0) ·
[호환성 기록](../../reference/versions.md).
