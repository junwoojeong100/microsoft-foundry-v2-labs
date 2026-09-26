# 실습 품질 기준과 공개 리포 비교

[English](../../reference/quality.md) | **한국어**

**비교 확인일: 2026-09-26.** 초보자가 이해할 수 있는 학습 흐름과 재현 가능한 엔지니어링 근거를 함께 갖추는 것이 목표입니다.
GitHub에서 객관적으로 가장 좋은 실습이라는 주장은 **하지 않습니다.** 이번 비교에서 전체 리포 순위 조사·독립적인 학습자 시범 운영·모든 기능의 Azure 실행을 수행하지 않았습니다.
스타 수·기능 수·AI 편집 평가 점수로 그런 주장을 증명할 수는 없습니다.

## 완성도 있는 실습이 보여 주어야 할 것

| 기준 | 이 저장소의 구현 | 근거의 한계 |
|---|---|---|
| 명확한 첫 경로 | [A의 설명·그림·정확한 순서](../paths/a-beginner.md) | 준비된 프로젝트와 Lab 05 실행 방식이 필요하며 완전한 브라우저 전용 과정은 아님 |
| 자습 준비와 오류 복구 | [준비](../setup.md), [담당자 준비](../setup-owner.md), [문제 해결](troubleshooting.md) | 계정 접근·quota·비용·권한을 가정하지 않음 |
| 이해하고 바꿔 볼 수 있는 코드 | [코드 따라 만들기](../code-along.md), 작은 SDK 예제 6개 | 모의 전송 검사이지 모델 추론이나 B 경로의 대체물이 아님 |
| 실행 가능한 지침 | 실제 parser로 CLI 예제 검사, A/B 경로·출력 형식 테스트 | 문법과 fixture만으로 현재 Azure 가용성을 증명하지 않음 |
| 재현 가능한 입력과 결과 | 언어별 고정 데이터, 명시적 모델/provider, 저장한 응답과 해시 | 오류 후 다른 모델·provider·언어·fixture로 대체하지 않음 |
| 의미 있는 평가 | [Lab 07](../labs/07-evaluation.md), dev 통과 조건, 실패 보존, 최종 확인 전용 holdout | dev 6개와 공개된 교육용 holdout 4개로 통계적 우월성을 주장하지 않음 |
| 정리까지 이어지는 운영 | [Lab 09](../labs/09-operations.md), [인계](../labs/11-capstone.md), [정리](cleanup.md) | 추적 상태·승인 권한·공유 소유권·남은 비용을 명시 |
| 정직한 기능 범위 | [날짜별 기능 상태](../coverage.md)와 [실제 결과](../live-run.md) | 설계만 한 기능·차단·이전 모델·미실행을 현재 실행 근거로 바꾸지 않음 |
| 최신 내용에 맞는 번역 | 현재 revision뿐 아니라 검토된 **모든** 영문·국문 쌍의 정확한 완료 해시 | 번역 대기는 경고 유지. 명령을 안 바꿔도 본문 수정으로 완료 해시가 달라질 수 있음 |
| 반복 가능한 유지보수 | [한 번에 실행하는 로컬 검사](#verify-this-copy), CI, 의존성 변경 확인 | 통과 보고서는 해당 소스 해시와 선택한 로컬 검사에만 적용 |

2026-09-26에 확인한 공식 [Foundry 에이전트 개발 수명 주기](https://learn.microsoft.com/azure/foundry/agents/concepts/development-lifecycle)는
생성·도구·불변 버전·추적·평가·게시·관측을 연결합니다.
이 실습도 그 요소를 다루지만 수업 완료가 자동 게시나 역할 변경으로 이어지지는 않습니다.
게시된 에이전트의 identity 권한은 별도로 검토해야 하며, 실제 회사/Microsoft 365 데이터는 계속 제외합니다.

<a id="public-reference-sample"></a>

## 비교한 공개 리포

GitHub 전체가 아니라 **대표 리포 7개**입니다.
GitHub 리포 검색과 기본 브랜치 파일을 읽고 확인한 커밋을 아래에 고정했습니다.
날짜는 **커밋 날짜**이며 리포 갱신 시각이나 실제 실행 성공의 증거가 아닙니다.
언어·대상 학습자·범위가 달라 하나의 수치 순위로 나열하면 오해를 줄 수 있습니다.

| 확인한 커밋의 공개 리포 | 커밋 날짜 | 관찰한 학습 방식 | 이 실습에 반영할 원칙 |
|---|---|---|---|
| [microsoft/ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners/tree/25b7985f3b2dc37a84f4a7387ccd3c9f0e5b1595) | 2026-09-09 | 주제별 수업·코드 예제·영상·다국어 | 개념과 코드를 쉽게 찾되 영문·국문 실행 근거의 버전은 독립 유지 |
| [MicrosoftLearning/mslearn-ai-agents](https://github.com/MicrosoftLearning/mslearn-ai-agents/tree/7eafc3c339d31a8fd125af71ee7fd2465c083be8) | 2026-09-22 | 과제 중심 실습과 필요한 시점의 개념 설명. 확인한 A3 클라이언트 과제는 `draft` 상태 | 모든 과제를 wrapper 명령으로 끝내지 않고 예상 → 수정 → 검사 → 설명 과정 추가 |
| [Azure-Samples/foundry-hosted-agents-workshop](https://github.com/Azure-Samples/foundry-hosted-agents-workshop/tree/bf12d4e12f2a44c2251ba54b24fd1355ab1b4534) | 2026-08-18 | 여행 도우미 하나를 확장, 단계별 이동·사전 확인·로컬 진행 | 단일 시나리오와 명확한 확인 지점을 유지하되 push를 요구하거나 이전 작업을 덮어쓰지 않음 |
| [Azure-Samples/microsoft-foundry-e2e-agent-observability-workshop](https://github.com/Azure-Samples/microsoft-foundry-e2e-agent-observability-workshop/tree/75eb82dfe36e5aae3375829a85433d940e422070) | 2026-04-17 | 관측 → 최적화 → 보호, SDK와 skill 경로 | 평가·추적·실패 검토를 장식용 화면이 아닌 핵심 학습으로 유지 |
| [Azure-Samples/multi-agent-orchestration-workshop](https://github.com/Azure-Samples/multi-agent-orchestration-workshop/tree/4095e86d52e644e691ee19d0076741104dd8111c) | 2026-05-27 | .NET 패턴별 시작 코드와 구조 설명 | builder·역할 순서를 설명하고 Python 연습에서 참여자 구성이 틀렸을 때의 실패 확인 |
| [Azure-Samples/foundry-agent-sdk-workshop-kr](https://github.com/Azure-Samples/foundry-agent-sdk-workshop-kr/tree/79d3f03e645f7189861bb09b15a40697690b644c) | 2026-08-20 | 한국어 SDK 노트북·단계별 준비·명시된 검증일 | 한국어를 완전한 실행 경로로 유지하고 호환성 주장에 날짜 표시 |
| [monuminu/foundry-workshop](https://github.com/monuminu/foundry-workshop/tree/f8a810ee4e611f25a3c1bb3c4ee2d60c438b46d9) | 2026-06-19 | 읽기 쉬운 웹 수업·생성형 노트북·예상 출력 | 예상 결과와 해석법을 보여 주되 예시와 본인의 실제 응답을 구분 |

확인 범위는 각 README와 추가로
[Microsoft Learn A3 과제](https://github.com/MicrosoftLearning/mslearn-ai-agents/blob/7eafc3c339d31a8fd125af71ee7fd2465c083be8/Instructions/Consolidated/A3-call-your-agent-from-a-client-app.md),
[Hosted 사전 검사](https://github.com/Azure-Samples/foundry-hosted-agents-workshop/blob/bf12d4e12f2a44c2251ba54b24fd1355ab1b4534/.workshop/scripts/preflight.py),
[순차 패턴 코드 실습](https://github.com/Azure-Samples/multi-agent-orchestration-workshop/blob/4095e86d52e644e691ee19d0076741104dd8111c/docs/01-sequential-pattern.md),
[노트북 실습 준비](https://github.com/monuminu/foundry-workshop/blob/f8a810ee4e611f25a3c1bb3c4ee2d60c438b46d9/docs/setup.md)입니다.
이 자료는 학습 방식의 근거이지 **여기에서 해당 코드를 실행했다는 주장이 아닙니다.**
외부 코드·미디어·수업 본문은 이 에디션에 복사하지 않았으며 각 원본의 라이선스는 독립적입니다.

## 비교 후 실제로 보완한 것

기본 경로가 이미 프로젝트부터 평가·정리까지 연결하므로 기능 수를 늘리려고 무관한 서비스를 더하지 않습니다.
이번에는 다음 세 가지를 추가합니다.

1. **실행 가능한 코드 연습:** 개인 사본·고정 SDK 전송·의도한 세 가지 동작 오류와 보존되는 실패 기록.
2. **소스에 연결된 품질 보고서:** 명령 하나로 선택한 검사 전체·실패·Python·시각·실행 전후 소스 해시 기록.
3. **완료 해시 강제 검사:** `check_docs.py`가 현재 번역 대기뿐 아니라 이전 개정에서 완료한 번역의 변경도 거절.

Codespaces·추가 모델 계열·음성·fine-tuning을 이번에 암묵적으로 추가하거나 검증했다고 하지 않습니다.
다른 교육 과정에 있다는 사실이 이 저장소에서 테스트된 구현의 근거는 아닙니다.

<a id="verify-this-copy"></a>

## 현재 복사본을 로컬에서 검증

소스 저장소 루트에서 분리된 Python **3.13** 또는 **3.14** 환경을 사용합니다. 설치된 SDK 검사는 3.13에서 합니다.
활성화된 기존 `.venv`는 유지합니다. **새 검사 전용 환경**이면 아래 블록을 사용하며, `.venv`가 이미 있으면 교체하지 않고 멈춥니다.

```bash
mkdir .venv &&
python3.13 -m venv .venv &&
source .venv/bin/activate &&
python -m pip install -e ".[dev]"
```

`.venv`가 이미 있으면 위 블록은 건너뛰고 `source .venv/bin/activate`로 활성화한 뒤 필요할 때만 `".[dev]"`를 설치합니다.
Python 3.14는 오프라인 전용 대안이며 위의 `python3.13`을 명시적으로 바꿉니다. Windows는 WSL을 사용합니다.
이 검사에 Azure 계정·`.env`·역할 부여·모델 배포는 필요 없습니다.

```bash
python scripts/verify_workshop.py --label quality-check
```

Ruff 문법·형식, Python 컴파일, 오프라인 테스트, 문서 검사, 학습자 번들 검사를 실행합니다.
오프라인 테스트는 가이드의 fixture 체험 명령을 실행하고 덮어쓰기·실패 보존도 확인합니다.
**`outputs/verification/quality-check/report.json`**에 저장하며 다음 시도는 새 label을 사용합니다.
기존 폴더가 있으면 검사 시작 전에 멈추며 이전 근거를 지우거나 교체하지 않습니다.

| 보고서 항목 | 뜻 |
|---|---|
| `mode: offline-verification` | 실제 agent 평가가 아닌 로컬 엔지니어링 검사 |
| `status: passed` | 선택한 검사 전체가 통과했고 실행 중 관련 소스가 바뀌지 않음 |
| `checks` | 정확한 명령·상태·종료 코드·소요 시간. 실패도 목록에 유지 |
| `source_before_sha256`, `source_after_sha256` | 관련 코드·가이드·합성 데이터·검사 설정의 해시. `.env`와 개인 `outputs/`는 제외 |
| `sdk_checks_selected` | 설치된 SDK 계약·전송 테스트까지 추가 실행했는지 표시 |
| `azure_tested`, `learner_pilot_performed`, `global_ranking_established`, `deployment_approved` | 모두 `false`. 로컬 통과로 추론할 수 없는 항목 |

종료 `0`은 선택 검사 통과, `1`은 검사 실패, `2`는 잘못된 입력이나 준비·보고서 오류, `130`은 중단입니다.
터미널의 실제 오류를 읽습니다. 보고서에는 환경변수 값이나 로그 본문이 들어가지 않으며 인증정보 내보내기가 아닙니다.
소스 해시 변경·시간 초과·도구 누락·미실행 검사·중단이 있으면 통과 보고서가 되지 않습니다.

**설치된 SDK까지 선택 검사**하려면 Python 3.13을 유지하고, 전체 고정 조합이 없을 때 설치합니다.

```bash
python -m pip install -r requirements.lock.txt -e ".[cloud,agents,hosted,dev]" &&
python scripts/verify_workshop.py --sdk --label quality-sdk-check
```

`--sdk`는 `pip check`·import 계약·SDK 테스트를 더합니다. Azure 로그인이 아니라 고정 전송을 사용합니다.
이를 실행해도 실제 Azure 근거가 되지 않습니다. CI도 같은 로컬 검사기를 사용하며 별도 SDK job은 계속 로컬/stub 전용입니다.

## 여전히 실제 근거가 필요한 부분

특정 수업을 준비 완료라고 하려면 담당자가 실제 참가자 권한으로 선택 경로를 리허설하고,
모델·버전·입력·응답·실패·정리 기록을 남겨야 합니다. [강사 리허설](../instructor.md#rehearse-route)을 사용합니다.
이 페이지를 채우려고 새 배포를 만들거나 유료 비교를 실행하지 않습니다.

독립적인 초보자 시범 운영은 AI 검토와 다른 **별도의 미실행 활동**입니다.
동의한 학습자에게 고정 가이드와 준비된 환경만 제공하고, 이름·인증정보 없이 경로·revision·시작/완료/차단 수,
도움을 받은 지점·소요 시간을 기록합니다. 막힌 학습자도 분모에 포함하고 도움받은 완료와 독립 완료를 구분합니다.
환경 준비 시간이나 모델 응답 시간을 학습자 완주 시간으로 바꾸어 적지 않습니다.

이번 공개 비교와 로컬 검사는 확인 가능한 개선의 근거입니다. 전체 순위·운영 승인·실측 학습 성과·모든 기능의 새로운 Azure 결과를 증명하지는 않습니다.

[입문 가이드](../paths/a-beginner.md), [구현 가이드](../paths/b-practitioner.md), [실제 검증 범위](validation.md)로 돌아갑니다.
