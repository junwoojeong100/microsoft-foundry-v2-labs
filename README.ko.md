# Microsoft Foundry v2 Hands-on Labs

[English](README.md) | **한국어**

## 여기에서 시작하세요

**출장 규정 안내 도우미 하나를 만들고, 검토한 답변과 자원 정리 기록을 남깁니다.**
동봉한 합성 데이터만 사용합니다.

1. 아래에서 **A** 또는 **B**를 고릅니다.
2. **고른 경로에 맞춰** [준비 카드](docs/ko/setup.md)를 완료합니다.
3. 경로의 체크리스트를 따라 Lab 00부터 진행합니다. 페이지의 다음 절이 아니라 **A 완료 / B 완료** 링크로 이동합니다.

| 경로 | 이런 분께 | 하는 일 | 끝나면 남는 것 |
|---|---|---|---|
| **[A — 입문](docs/ko/paths/a-beginner.md)** | Azure나 에이전트가 처음인 분 | 브라우저 조작과 준비된 Lab 05 workflow 경로. Python 작성 없음 | 내 에이전트·6문항 평가표·workflow 검토·정리 인계 |
| **[B — 구현](docs/ko/paths/b-practitioner.md)** | Python·API에 익숙한 분 | SDK 호출·관리형 prompt agent·도구·workflow·Search/IQ·통제된 평가·trace·로컬 패키징 | 저장된 실행 기록과 인수 보고서 |

**준비 후 소요 시간:** A 4시간 30분, B 8시간(4시간 세션 2회). **파일:** A는 작은 학습자 ZIP, B는 소스 저장소만 사용하며 두 번째 ZIP은 필요 없습니다.
두 경로 모두 준비된 Azure 환경이 필요합니다. Lab 05는 브라우저의 준비된 Hosted workflow agent 또는 준비된 터미널 중 하나를 사용합니다(수업 전 담당자가 결정).
둘 다 제공받지 않았다면 수업 전에 [Lab 00 B](docs/ko/labs/00-start.md#path-b)와 [Lab 02 B](docs/ko/labs/02-models.md#path-b)를 완료합니다.
Azure 권한이 없다면 [오프라인 체험](docs/ko/labs/00-start.md#offline-rehearsal)만 하고 cloud 실습은 **미실행**으로 기록합니다.

기본 경로를 마친 뒤에는 선택 [C. 고급 모듈](docs/ko/paths/c-advanced.md)을 고를 수 있습니다. 수업을 준비한다면 [강사 가이드](docs/ko/instructor.md),
구버전에서 돌아왔다면 [변경 지도](docs/ko/reference/migration.md)를 사용합니다.
아래 배경 설명과 녹화는 선택 참고 자료이며 선행 조건이 아닙니다.

<details>
<summary>배경과 이전 녹화 — 선택 참고 자료이며 선행 조건이 아닙니다</summary>

## 이 실습의 배경: Learning loops와 Frontier ecosystems

사티야 나델라는 [2026년 6월 14일 글](https://x.com/satyanadella/status/2066182223213293753)에서
**프런티어 모델 하나를 넘어 프런티어 생태계를 만들어야 한다**고 강조했습니다.
모델을 교체하더라도 조직의 지식과 전문성이 남는 학습 시스템을 구축해야 한다는 관점입니다.
이어 [2026년 7월 29일 Microsoft 실적 발표](https://www.microsoft.com/en-us/Investor/events/FY-2026/earnings-fy-2026-q4)에서도
각 조직이 자체적인 **지속적 학습 루프(continuous learning loop)**를 만들고 핵심 IP를 통제해야 한다고 재차 설명했습니다.
관심의 중심을 가장 뛰어난 모델을 고르는 데서, 조직이 계속 학습하고 가치를 축적할 수 있는 생태계를 만드는 데로 옮기는 것입니다.

이 실습은 그 관점을 **실행 → 관측·평가 → 사람의 검토 → 개선 → 재검증**이라는 엔지니어링 루프로 구체화합니다.
번들 합성 데이터만 사용해 Foundry와 Microsoft Agent Framework(MAF)의 에이전트,
지식·도구·워크플로·Hosted 배포·평가를 하나의 시스템으로 연결합니다.
여기서 학습은 검토를 거친 지침·검색·도구·워크플로의 개선을 뜻하며, 모델 가중치의 자동 재학습이 아닙니다.
Dev 데이터로 반복 개선하고 holdout은 최종 인수에만 사용합니다.

**처음에는 에이전트 하나를 만들고, 마지막에는 지식·평가·운영 기준이 남는 시스템을 만듭니다.**

> **2026-09-15 국문 심화 실행(이전 `gpt-5.6-luna` 판)**
> MAF workflow→Hosted, 네 모델의 24/24/16행, native 평가·calibration·trace 인수를 실제 실행했습니다.
> `gpt-6-sol`로는 다시 실행하지 않았습니다.
> [통합 범위와 인수 기준](docs/ko/reference/consolidation.md) ·
> [Hosted 평가 워크북](docs/ko/reference/evaluation-workbook.md) ·
> [IQ 확장 워크북](docs/ko/reference/iq-workbook.md).

한국어 · 합성 데이터

실행 근거, 녹화 metadata, action 수, 재생 확인, coverage와 날짜별 실행 결과는 이제 [실행 근거와 녹화](docs/ko/evidence.md)에 모았습니다.
그 hub에서 [실측 결과](docs/ko/live-run.md), [녹화](docs/ko/video-summary.md), [action/capture](docs/ko/action-captures.md), [coverage](docs/ko/coverage.md), [검증](docs/ko/reference/validation.md)을 확인합니다.

</details>

## 하나의 시나리오, 점점 확장되는 시스템

가상 기업 **한빛기술의 출장 규정 안내 도우미**를 만듭니다.
현재/과거 숙박 한도, 식비, 사전 승인, 근거 없는 해외 출장 질문을 다룹니다.
실제 회사 문서·개인 정보·Microsoft 365 데이터는 사용하지 않습니다.
에이전트는 안내만 하며 출장 승인·예약·지급을 실행하지 않습니다.

```mermaid
flowchart LR
    U["사용자 질문"] --> A["Foundry Agent / MAF"]
    K["합성 규정 6건"] --> R["문서 근거 / Search / Foundry IQ"]
    R --> A
    T["읽기 전용 함수·MCP"] --> A
    A --> E["답변·인용·실행 이력"]
    E --> V["업무 검사 + 선택적 Foundry 평가"]
    V --> H["사람의 실패 검토"]
    H --> P["개선 지침 + 회귀 자산"]
    P --> A
    E --> O["추적 / 모니터링 / 비용"]
```

| 모듈 | 내용 |
|---|---|
| [00. 시작과 환경](docs/ko/labs/00-start.md) | 학습 경로, 브라우저/코드 준비, offline/cloud 구분 |
| [01. Foundry와 프로젝트](docs/ko/labs/01-foundry.md) | 플랫폼·SDK 구분, 리소스·프로젝트·권한 |
| [02. 모델](docs/ko/labs/02-models.md) | 배포 이름, 플레이그라운드, SDK, 모델 비교·Router |
| [03. 첫 에이전트](docs/ko/labs/03-prompt-agent.md) | 지침, 합성 문서, 인용, 도구와 권한 경계 |
| [04. MAF와 도구](docs/ko/labs/04-agents-tools.md) | 단일 에이전트, 함수, 로컬 MCP |
| [05. MAF 워크플로](docs/ko/labs/05-workflows.md) | 준비된 예제, 순차·병렬·Group Chat 코드, 사람의 검토 |
| [06. RAG와 Foundry IQ](docs/ko/labs/06-knowledge.md) | Search와 IQ 구분, GA API, 원문 인용 |
| [07. 평가와 학습 루프](docs/ko/labs/07-evaluation.md) | dev, 실패 분석, 지침 개선, holdout |
| [08. Hosted Agent](docs/ko/labs/08-hosted.md) | 안전한 패키징, 로컬 서버, 코드 배포 |
| [09. 관측·운영·정리](docs/ko/labs/09-operations.md) | trace, 운영 게이트, 비용과 소유권 기반 정리 |
| [10. IQ 확장](docs/ko/labs/10-iq-extensions.md) | Fabric·Work IQ·Toolbox·Preview 승인 경계 |
| [11. 캡스톤](docs/ko/labs/11-capstone.md) | 지식·모델·평가·운영을 묶은 최종 인수 |

## 코드 경로의 가장 짧은 시작

**선택 오프라인 체험이며 B의 Azure 설정은 아닙니다.** **저장소 루트**의 Bash에서 실행합니다
(Windows는 WSL). 전체 코드 경로에는 Python 3.13을 사용하며 3.14는 오프라인 검사만 지원합니다.
A 학습자는 이 절을 건너뛰어도 됩니다.

```bash
# 외부 패키지나 Azure 없이 가능한 검사기 체험
python3.13 scripts/workshop.py doctor
python3.13 scripts/workshop.py demo --label first-offline --prompt v2
python3.13 scripts/workshop.py evaluate --label first-offline
```

**확인:** `doctor`는 `result: PASS`, `azure_tested: false`를 반환합니다.
`outputs/first-offline/business-evaluation.json`을 열면 동봉한 v2 fixture의 결과는
`total: 6`, `passed: 6`, `errors: 0`이어야 합니다. **검사기를 확인한 것이며 모델 품질·Azure 연결의 증거가 아닙니다.**
다시 실행하려면 `demo`와 `evaluate`에 같은 새 label을 씁니다. 기존 실행은 덮어쓰지 않습니다.
SDK 설치·인증·실제 호출은 [Lab 00 B](docs/ko/labs/00-start.md#path-b)에서 진행합니다.

## 이 버전의 범위

- 현재 Foundry / Projects SDK **2.x** 고정 버전은 2026-09-24에 갱신했고 그날 저녁 두 언어의 핵심 B 경로에서 실제 검증했습니다. 2026-09-24 녹화는 이전 고정 버전을 사용했습니다. 새 고정 버전으로 Lab 03 B와 Lab 09 B 추적 검색을 2026-09-25에 녹화했습니다([보충 녹화](docs/ko/video-summary.md#review-refresh-supplement)). [버전](docs/ko/reference/versions.md)을 확인하세요.
- 워크플로 작성·오케스트레이션은 **MAF 코드**를 사용합니다. 포털 workflow 생성/게시 단계는 포함하지 않습니다. Assistants는 2026-08-26 retired, 포털 Workflows는 2026-12-01 retire, classic threads/runs agents는 2027-03-31 retire 예정입니다. [변경 지도](docs/ko/reference/migration.md)를 확인하세요.
- 첫 실습 preset은 **`gpt-6-sol`**, 같은 이름의 배포, 모델 버전 **`2026-09-22`**입니다.
  2026-09-23에 선택했고 2026-09-24에 이 모델로 주요 단계를 녹화했습니다([이 모델을 고른 이유](docs/ko/reference/model-choice.md)).
  Search knowledge base가 GPT-6 모델을 받지 않아 선택 IQ Chat 경로는 별도 `gpt-5.6-luna` 배포를 유지합니다.
  다른 모델은 명시적인 비교 실험에서 사용합니다.
- 서비스 GA와 SDK Preview는 따로 표시합니다. Hosted Agent 서비스는 GA지만 이 랩의 Python hosting
  패키지는 prerelease입니다. Foundry IQ도 GA 계약과 기능이 더 많은 Preview 계약을 구분합니다.
- 모델 교체, 지침 개선, 평가 데이터 축적을 다룹니다. **자동 가중치 학습·fine-tuning·RL을 수행하지 않습니다.**
- 실제 배포, 유료 평가, 외부 데이터 연결은 학습자가 별도로 실행하는 선택 단계입니다.
  이 저장소를 열거나 `doctor`를 실행한다고 리소스가 생성되지 않습니다.
- Ignite 2026에서 발표될 기능이나 가격·리전·할당량을 미리 보장하지 않습니다.

**기준과 증거:** [버전·기능 상태](docs/ko/reference/versions.md) ·
[이 에디션의 검증 범위](docs/ko/reference/validation.md) ·
[원본 커밋·공식 출처](docs/ko/reference/sources.md) ·
[문제 해결](docs/ko/reference/troubleshooting.md) ·
[리소스 정리](docs/ko/reference/cleanup.md)

처음 보는 용어는 [용어 사전](docs/ko/reference/glossary.md), 다음 학습은 [학습 자료](docs/ko/reference/learning-resources.md), 실행 옵션은
[명령 참조](docs/ko/reference/commands.md), 환경변수는 [공통 설정](docs/ko/reference/configuration.md)을 확인하세요.

## 저장소 구성

```text
docs/                  기본 영어 실습·학습 경로·강사·참고 문서
docs/ko/               같은 내용의 한국어 가이드
src/foundry_workshop/   공통 설정·검색·에이전트·평가·실행 이력
scripts/               실습 CLI, 패키징, 문서 검사
data/knowledge/        합성 정책 6건
data/evaluation/       dev 6건 / holdout 4건 / judge calibration 2건
data/fixtures/         Azure 없이 검사기만 체험하는 고정 예제
data/learner/          바로 쓰는 국문·영문 브라우저 자료와 ZIP
prompts/               비교할 v1 / v2 지침
examples/              로컬 MCP 서버, Hosted Agent 진입점, 독립 SDK 예제(recipes)
tests/                 Azure 없는 로직·계약 검사
outputs/               개인 실행 결과; Git에서 제외
```

자료의 라이선스는 [MIT](LICENSE)입니다. 원본 리포별 출처·라이선스 경계는
[출처 문서](docs/ko/reference/sources.md)에 구분했습니다.
