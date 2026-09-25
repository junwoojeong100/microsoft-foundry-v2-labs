# 검증 범위와 실제 실행

[English](../../reference/validation.md) | **한국어**

**설치·offline 계약·실제 Azure 실행·모델 품질·미디어 검수는 서로 다른 검증입니다.**
국문과 영문은 별도 label과 촬영 원본을 사용합니다. 이전 영상이나 upstream 성공을 새 결과로 재분류하지 않습니다.

<a id="current-answer"></a>

## 현재 답 — 2026-09-25

| 질문 | 답 | 자세히 |
|---|---|---|
| 무엇을 녹화했나요? | Lab 00–09·11의 A/B 주요 단계와 선택 Foundry 평가 단계를 영문·국문으로 녹화. Sweden Central 실습 프로젝트의 `gpt-6-sol` / `gpt-6-sol-judge`(`2026-09-22`) 사용 | [재녹화](#gpt-6-sol-20260924) · [영상](../video-summary.md) |
| 실제 실행 결과는? | 두 언어 모두 업무 검사 baseline 6/6, candidate 6/6, holdout 4/4. 인수 판단은 `ready-for-human-review`, `deployment_approved: false`. Judge 점수는 따로 보관하며 인수를 결정하지 않음 | [실제 결과](../live-run.md) |
| 녹화 없이 `gpt-6-sol`로 더 실행한 것은? | 2026-09-23: 선택 평가 단계의 검증 실행(9월 24일 녹화에서 다시 실행), 대화 평가 모듈, 기존 추적·되풀이 평가, Agent Optimizer(baseline만), 클라우드 red teaming(표시된 ASR 무효), 승인된 Hosted CI 릴리스 | [추가분](#foundry-evaluation-additions) · [이전에 실행하지 않은 항목](#previously-not-run-items) |
| `gpt-6-sol`로 실행하지 않은 것은? | Lab 03 포털 File Search, Lab 06 IQ Chat·hybrid RAG, Lab 07 feedback/회귀·Hosted matrix, Lab 08 기본 로컬 서버·`azd ai agent invoke --local`·학습자 본인의 Hosted 배포(6절 workflow 서버는 2026-09-24에 `curl` 요청 하나에 답함), Hosted server-side tracing, Lab 10, [기능 범위](../coverage.md)에 재실행으로 적히지 않은 확장 모듈 | [미실행 목록](../live-run.md#gpt-6-sol로-실행하지-않은-것) |
| 작업 폴더는 어떻게 확인하나요? | 아래 offline 테스트·Ruff·compilation·문서·학습자 번들 검사를 실행합니다. 날짜별 기록마다 해당 revision에서 통과한 검사를 적습니다 | [로컬 검사](#재실행할-로컬-검사) |
| 이 근거 밖에 있는 것은? | 회사/Microsoft 365 데이터, 외부 Work IQ/Fabric 연결, SLA, 통계적 우월성, 자동 재학습, 운영 승인, 다른 사용자의 자산 | [확인하지 않은 것](#확인하지-않은-것) |
| 9월 24일 검토 반영에서 바뀐 것은? | SDK 고정 버전 갱신, B 핵심에 Lab 03 B 관리형 agent 추가, trace 확인 필수화, A Lab 05 브라우저 선택지, Insights 모듈, 독립 SDK 예제, 새 CI 검사. 그날 저녁 새 고정 버전으로 핵심 B 경로를 두 언어에서 실제 실행했고 추적 조회, 예제, A2A, Insights scan 1회를 함께 확인했으며 가이드·예제 결함 4개를 수정 | [검토 반영](#review-refresh-20260924) · [live 확인](#review-refresh-live-20260924) |
| 9월 25일에 더한 것은? | 두 기본 경로를 두 언어로 가이드대로 끝까지 실행(가이드 수정 5건), Lab 03 B와 Lab 09 B 추적 검색의 화면·짧은 영상(두 언어), 대화 평가·Memory·routine·Toolbox 탐색까지의 영문 실행. 나머지 항목은 담당자 승인이 필요 | [보충 녹화와 미실행 검토](#review-refresh-supplement-20260925) |
| 가이드·문서는 얼마나 straightforward한가요? | AI 편집 검토: 2026-09-25 최종 점검에서 새 검토자는 가이드 94/100, 문서 90/100(6차)을, 수정 뒤 재검토는 99.5/100, 98/100(7차)을 주었습니다. 학습자 시범 운영이나 시간 측정이 아님 | [최신 검토](#straightforwardness-95) |

<a id="review-refresh-20260924"></a>

## 검토 반영(오프라인만) — 2026-09-24

**변경:** SDK 고정 버전(`azure-ai-projects` 2.6.1, `openai` 3.16.1, MAF core 1.18.0, `agent-framework-foundry` 1.13.0,
hosting 1.0.0b260910, `mcp` 1.30.0, [버전](versions.md)), 형식이 있는 A2A SDK 요청, raw REST API 버전을 모은
날짜 기록 `compatibility.py`, `prompt-agent --output`, B 핵심 단계가 된 Lab 03 B, Lab 09 trace 확인,
A Lab 05 브라우저 선택지, [Insights 모듈](../labs/extensions/agent-insights.md), `examples/recipes/`의 독립 예제 6개,
녹화된 help snapshot 기준의 azd 명령 검증, 읽기 전용 SDK drift 보고서, 수동·비용 승인형 live smoke workflow.

**오프라인 검증:** Python 3.13·3.14(site package 없이)에서 오프라인 테스트 297개, 설치한 고정 라이브러리와 transport stub을 쓴 SDK 테스트 87개, Ruff, 포맷, 컴파일, `check_docs.py`(Markdown 127개, 로컬 링크 2,520개, anchor 510개, workshop CLI 예제 328개, azd 예제 84개, 언어 쌍 63개), 학습자 번들, `pip check`, `check_sdk.py`, CI 오프라인 doctor/demo/evaluate/package 단계가 통과했습니다.

**이 오프라인 단계에서 미실행:** Azure 호출·배포·역할 변경·녹화·live smoke 실행은 하지 않았습니다. 실제 확인은 아래에 이어집니다.
위의 녹화와 실제 결과는 이전 고정 버전과 이전 가이드 revision으로 만든 것이며 새 단계의 근거가 아닙니다.

<a id="review-refresh-live-20260924"></a>

## 검토 반영 실제 검증 — 2026년 9월 24일(저녁)

**범위:** 갱신한 고정 버전을 적용한 commit `a9c3990`의 새 복사본, prefix `mfv2-rr-20260924-<language>`, 같은 Sweden Central
프로젝트와 `gpt-6-sol` / `gpt-6-sol-judge`. 실습 구독을 고정했고 Azure CLI 기본 구독은 바꾸지 않았습니다.

- **핵심 B 경로, 영문·국문:** 문서의 모든 명령이 종료 코드 0. Lab 07 baseline 6/6, candidate 6/6, holdout 4/4, 오류 0.
  인수 판단은 `ready-for-human-review`, `deployment_approved: false`. Lab 03 B는 각 언어에서 버전 1을 만들고 그 버전으로 호출했습니다.
- **추적:** 각 관리형 agent 호출은 약 3분 안에 token이 일치하는 `invoke_agent`와 `chat` span을 만들었습니다.
  Responses API를 직접 호출한 명령은 span을 만들지 않았습니다.
- **선택 및 C 항목:** `maf-evaluate` 6/6과 6/6, `cloud-evaluate` groundedness 6/6, relevance 5/6(D05), 형식이 있는
  SDK 요청을 쓴 A2A 1.0 위임 호출 1회, trace 22개를 분석해 insight 4개를 반환한 Insights scan 1회, 로컬 workflow 서버의
  Responses 요청 1회, 예제 02–06·08 완료.
- **수정:** 예제는 이제 `AZURE_SUBSCRIPTION_ID`를 고정합니다(고정하지 않은 CLI credential이 다른 tenant 계정으로 403 반환).
  예제 05·08은 합성 근거를 함께 보냅니다. `maf-evaluate`의 Pydantic 경고와 tenant를 지정한 추적 조회를 문서화했습니다.
- **미실행:** A Lab 05 브라우저 선택지를 위한 원격 Hosted 배포, 타사 모델 비교, Toolbox/Tool Search/Skills,
  Memory, Routines, 대화 평가, Agent Optimizer, red teaming, A 경로의 포털 단계.

[세부 정보·ID·소유 객체](../live-run.md#review-refresh-live-verification).

<a id="review-refresh-supplement-20260925"></a>

## 보충 녹화와 미실행 항목 검토 — 2026-09-25

- **영문·국문 녹화:** Lab 03 B의 `--output` 생성·호출(실제 zsh 터미널, 가이드 블록을 그대로 붙여 넣고 `read` 프롬프트에 직접 입력), Lab 03 B 포털 확인, Lab 09 B 추적 검색.
  무손실 WebP 화면 12장은 원본 PNG와 픽셀 단위로 같게 디코딩되고, 1배속 H.264 영상 4개는 끝까지 디코딩됩니다. 포털 지침은 CLI 정의와 같았고, 각 trace ID는 Application Insights `operation_Id`와 같았습니다.
- **폐기:** 터미널에 로컬 홈 디렉터리 경로가 출력된 영문 시도 1개. 중립 작업 폴더에서 다시 녹화했습니다.
- **영문 실행:** 갱신한 고정 버전의 대화 평가, Memory 수명 주기, routine dispatch 1회, MCP 탐색까지의 Toolbox, 읽기 전용 A 경로 추적 확인. Toolbox 직접 query는 프로젝트 ID에 Search Index Data Reader만 있어 Search가 거부했습니다.
- **담당자 승인 필요:** 런타임 역할을 포함한 원격 Hosted 배포, 타사 모델 비교용 OpenAI 외 배포 1개, 지원 optimizer 배포, Toolbox·Tool Search·Skills용 Search 역할. Dev Pack 설치는 작업 PC의 전역 도구를 바꿉니다.

- **오프라인 검사:** Python 3.13·3.14의 오프라인 테스트 305개, 고정 라이브러리의 SDK 테스트 87개, Ruff check·format, compilation, `check_docs.py`, 학습자 번들, CI 오프라인 doctor·demo·evaluate·package 단계가 통과했습니다.

[ID·결과·소유 객체](../live-run.md#review-refresh-supplement).

<a id="end-to-end-20260925"></a>

## 가이드대로 끝까지 실행 — 2026-09-25

- **적힌 그대로 실행:** GitHub에서 받은 `f128f0c` 새 복사본(영문 sparse clone, 국문 ZIP). B 경로 핵심 블록 34개를 언어마다 한 터미널(zsh, bash 3.2)에서
  실행하고 프롬프트에 직접 입력했습니다. A 경로는 언어별 포털에서 Lab 01–03, 07, 09 단계와 Lab 05 A 터미널 명령을 실행했습니다.
- **결과:** 모든 블록 종료 코드 0. 두 언어 모두 baseline 6/6, candidate 6/6, holdout 4/4, `ready-for-human-review`.
  두 포털에서 D01–D06이 기준을 충족했고, 추적에는 `invoke_agent <agent>:2`와 자식 `chat` span이 있었습니다.
- **수정:** 바뀐 **에이전트 만들기** 창(새 화면), 모델 확인 위치를 **세부 정보**에서 **플레이그라운드**로 변경, 녹화 agent 이름,
  `answer` 중첩 설명, 영문 라운드 상한 문구, 국문 feedback 입력 안내.
- **정리:** 이 실행의 모든 객체를 삭제하고 다시 조회해 404를 확인했습니다.

[세부 내용과 객체](../live-run.md#end-to-end-20260925).

<a id="gpt-6-sol-20260924"></a>

## 선택 평가 단계를 포함한 재녹화 — 2026-09-24

**녹화:** 00:00 KST 이후 새로 시작한 영문·국문 녹화입니다. 같은 Sweden Central 프로젝트에서
`gpt-6-sol` / `gpt-6-sol-judge`와 prefix `mfv2-sol-20260924-<language>`를 사용했습니다.

- **범위:** Lab 00–09·11의 A/B 주요 단계와 선택 Foundry 평가 단계.
- **영문:** 액션 98개, 무손실 캡처 293장, 영상 6:29 / 3:11 / 2:55, 터미널 녹화 1개와 포털 녹화 2개에서 나온
  원본 구간 262개(최소 SSIM 0.9922).
- **국문:** 액션 91개, 캡처 272장, 영상 6:03 / 2:57 / 2:43, 구간 244개(최소 SSIM 0.9923).
- **재생:** 두 언어 모두 로컬 byte-range 재생과 챕터 11개 이동을 확인했고 업로드·push는 하지 않았습니다.
- **삭제:** `g6sol-20260923` 녹화와 별도 `eval-portal-20260923` 캡처(git 기록 `90b18b3`).
  `videos/`에는 각 언어 통합본의 사본 `gpt-6-sol-20260924-en-summary.mp4`, `-ko-summary.mp4`가 있습니다.

[녹화](../video-summary.md) · [실제 결과](../live-run.md).

**녹화에 남긴 실패와 바뀐 점:**

- `E07-011`: 업무 기준 baseline 실행이 groundedness·relevance만 반환하고 `business_rubric`은 반환하지 않았습니다(오류 0).
  평가에는 testing criteria 3개가 있었습니다. CLI는 이 시도를 invalid로 거부했습니다. 국문 `K07-011`은 첫 시도에 세 결과를 모두 반환했습니다.
- `cloud-evaluate`에 `--retry-failed`(native 재시도는 이미 있었음)와 빠진 평가자 이름을 알려 주는 오류를 추가했습니다.
  `E07-013`이 한 번 재시도했고 첫 시도는 `native-attempts/attempt-1`에 보존했습니다.
- 이어서 `E07-012`가 `--reference baseline`을 거부했습니다. 재시도에서 다시 만든 상태에 `item_fields`가 빠진 재시도 경로 버그였습니다.
  이제 재시도가 `item_fields`를 유지합니다(회귀 테스트 추가). `E07-014`가 새 작업 없이 완료된 재시도를 다시 읽었고
  `E07-015`에서 candidate를 추가했습니다. 두 source 변경과 hash는 `live-results.json`의 `source_updates`에 있습니다.
  녹화 뒤에는 `--reference` 실행도 재시도할 수 있게 했습니다. 재시도는 참조한 평가에 `<label>-retry-N`으로 남고,
  `--retry-failed` 안내는 `cloud-evaluate` 오류에만 표시됩니다. 이 변경은 offline·SDK 테스트만 했으며 Azure에서 실행하지 않았습니다.
- playground에서 연 포털 평가 마법사는 Web search가 남아 있던 에이전트 **버전 1**을 미리 선택했습니다. 영문 캡처 도구가 이를 그대로 두어(`EP07-202`)
  `EP07-206`/`EP07-207`은 버전 1을 채점했습니다(TaskAdherence 4/6, D05에 외부의 미국 기준 금액을 답함). 두 언어 모두 버전 2로 평가를 다시
  실행했습니다(`*P07-211`~`*P07-217`): Relevance 6/6, Coherence 6/6, TaskAdherence 0/6. Lab 07 A 4단계의 2번과 Lab 09 A 추적 평가의 1번에 저장한 버전만 남기라는 안내를 추가했습니다.
- Foundry 실패가 아닌 캡처 도구 타이밍 문제: `EP07-205`는 평가자 목록이 열리기 전에 클릭했고, `KP07-203`은 업로드가 성공한 뒤
  새로 고쳐지지 않은 데이터 세트 행을 기다렸으며, `KP07-215`는 이름 변경 창이 열리기 전에 입력했습니다. 각 단계는 이름이 다른 이후 액션이 완료했습니다.

**언어별 결과:** 업무 검사 baseline 6/6, candidate 6/6, holdout 4/4. 근거 없음 진단 0/6·오류 0. cloud judge groundedness 6/6, relevance 5/6(D05).
업무 기준 일치는 두 실행 모두 6/6이었고 **실행 비교**의 relevance 평균은 3.83 → 4.83(영문), 4.17 → 4.50(국문)으로 **샘플이 너무 적음**이 표시되었습니다(캡처 `EP07-301`, `KP07-301`).
MAF 도구 호출은 영문 6/6·6/6, 국문 tool_call_accuracy 5/6(D03 검색어의 `APPROVAL-01`을 평가자가 지어낸 인자로 판단)·relevance 5/6(D05)이었습니다.
추적 평가는 영문 10/10, 국문 15/15이며 국문에는 앞선 포털 평가가 만든 대화 5개가 포함되었습니다.

**Azure 변경:** 새 prefix 아래 포털 에이전트(버전 1–2)와 SDK 에이전트, Search index, IQ knowledge source·base, 데이터 세트, 평가와 실행,
사용자 지정 평가자 버전 `mfv2_sol_20260924_en_business_rubric` 1과 `mfv2_sol_20260924_ko_business_rubric` 1을 만들었고
유료 모델·judge 호출이 발생했습니다. 국문 녹화를 위해 포털 언어를 한국어로 바꾼 뒤 영어로 되돌렸습니다. 배포·역할 할당·기본 구독 변경은 없습니다.

**로컬 검증:** offline 테스트 256개가 Python 3.13·3.14에서 각각 통과했고, SDK import 검사와 설치 SDK 테스트 77개,
Ruff·서식·컴파일·문서 검사가 통과했습니다.

<a id="previously-not-run-items"></a>

## 이전에 실행하지 않은 평가·안전·릴리스 항목 — 2026-09-23

담당자가 평가 추가분에서 실행하지 않은 항목을 요청했습니다. 같은 날 저녁 같은 프로젝트, `gpt-6-sol` / `gpt-6-sol-judge`,
prefix `mfv2-sol-20260923-<language>`로 실행했으며 편집 영상에는 포함되지 않습니다.

| 항목 | 먼저 한 담당자 조치 | 영문 | 국문 |
|---|---|---|---|
| 기존 추적 평가(Lab 09 A) | Application Insights에 대한 프로젝트 ID의 **모니터링 읽기 권한자** | Relevance·Coherence·TaskAdherence 15/15 | 각 15/15 |
| 되풀이 평가 | 위 역할 외 없음 | 저장 시 첫 실행 5/5, 다음 시간별 실행이 계획 요청을 표본에 포함해 5/5, 일시 중지 | 첫 실행 5/5, 다음 시간별 실행은 계획 요청 없이 5/5, 일시 중지 |
| Agent Optimizer | 임시 `gpt-5.5` optimizer 배포, 이후 삭제 | baseline만, 0.979 | baseline만, 0.938(D05 relevance 2) |
| 클라우드 red teaming(Preview) | taxonomy 검토. 행동 삭제로 범위를 줄인 것은 포털 실행뿐(SDK의 `enabled` 플래그는 생성 공격을 제한하지 않음) | SDK 표시 ASR 89%(75/84), 포털 100%(6/6) | SDK 표시 ASR 57%(48/84) |
| 승인된 Hosted 릴리스 | CI ID에 프로젝트 범위 **Foundry Project Manager**와 계정 **Reader** 부여, 환경 변수를 이 프로젝트로 변경 | [실행 35856612314](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35856612314): 6/6, 오류 0 | [실행 35857252318](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35857252318): 6/6, 오류 0 |

**발견 사항은 그대로 남깁니다:**

- 평가자가 받는 입력이 검증할 수 있는 범위를 정합니다. 추적의 `query`에는 정책 6개를 포함한 에이전트 지침이 들어 있어
  TaskAdherence가 15/15였고, 질문만 보낸 Lab 07 A의 데이터 세트 기반 실행은 영문 1/6, 국문 0/6이었습니다.
- 되풀이 실행은 마지막 1시간이 아니라 최근 7일에서 표본을 뽑습니다. 첫 실행은 일정을 저장하자마자 시작해 이전 대화를 다시 채점했고,
  16개 중 무작위 5개에 영문 계획 요청은 들어갔지만 국문 계획 요청은 들어가지 않았습니다.
  일정 설정과 실제 평가된 표본은 별도 증거로 두며, 표본을 채우려고 요청을 다시 보내지 않았습니다.
- red-team 서비스는 reasoning이 "응답이 거절했다"고 적은 행을 공격 성공(점수 0, threshold 3)으로 표시했습니다. 모든 응답을 읽었고
  금지 행동을 수행하거나 수행했다고 주장한 응답은 없었으며, 공격 3개는 콘텐츠 필터가 차단했습니다. 따라서 표시된 ASR은 무효로 둡니다.
  taxonomy의 `enabled` 플래그는 공격 생성 범위를 제한하지 않았고 포털에서 행동을 삭제하면 제한되었습니다. taxonomy PATCH에는
  전체 객체가 필요하고 변경 직후 조회는 이전 버전을 반환할 수 있습니다.
- optimizer의 일반 중단 문구는 모든 후보가 만점이라고 했지만 실패한 행이 있었고, Groundedness judge는 각 답변을 자기 자신과
  비교했습니다. 그래서 어떤 후보도 승격하지 않았고 `optimizer-review.txt`에는 `pending-human-review`를 기록했습니다.
- 기본 모델 선택이 잘못된 배포를 가리킬 수 있습니다. 임시 optimizer 배포가 있는 동안 새 평가의 **판단 모델** 기본값이 그 배포였고,
  optimizer의 **Evaluation model** 기본값은 `gpt-6-sol`이었습니다. 둘 다 `gpt-6-sol-judge`로 바꿨습니다.
- red-team 호출은 에이전트 추적을 남기지 않았고 optimizer 실행은 에이전트마다 27개를 남겼습니다. 그래서 optimizer는 격리한 에이전트
  복사본을 사용했고 되풀이 일정의 표본은 영향을 받지 않았습니다.
- 한국어 포털은 red-team wizard를 **빨간색 팀 실행 만들기**, 탭을 **레드 팀 미리 보기**, **최적화 미리 보기**로 표시했습니다.
  국문 scan과 optimizer 실행은 영문 UI에서 제출했습니다.

**Azure 변경:** 역할 할당(Application Insights에 대한 프로젝트 ID의 모니터링 읽기 권한자, CI ID의 프로젝트 범위 Foundry Project Manager와
계정 Reader, 파이프라인이 부여한 Hosted 런타임의 Foundry User), 배포 `mfv2-sol-20260923-opt-gpt55` 생성 후 삭제, 에이전트
`mfv2-sol-20260923-<language>-optimize`(버전 1)와 `mfv2-sol-20260923-ci-hosted`(버전 1–2), 데이터 세트 `mfv2-sol-20260923-<language>-optimizer-dev`,
추적·optimizer·red-team 평가와 red-team taxonomy, 일시 중지한 일정 2개, 바뀐 `foundry-workshop` 환경 변수(이전 값은 세션 기록에 보관).
9월 14일 프로젝트에 대한 CI ID의 역할은 그대로 두었습니다. 기본 구독은 바꾸지 않았습니다.

**여전히 실행하지 않음:** Lab 08의 로컬 서버와 학습자 본인의 Hosted 배포, Hosted agent의 서버 측 tracing, `gpt-6-sol`로의 guardrail 연결,
되풀이의 **연속** 모드(추적 평가에서는 사용할 수 없음).

<a id="foundry-evaluation-additions"></a>

## 선택 Foundry 평가 추가분 — 2026-09-23

기존 A/B 경로에 선택 Foundry Evaluation 실습을 추가했습니다. 핵심 경로와 그 명령, 녹화 영상은 바뀌지 않았습니다.

| 위치 | 추가 내용 | 상태 |
|---|---|---|
| Lab 07 A 4단계 | 저장한 에이전트를 새 `dev-questions.jsonl`(질문만)로 포털 평가(Relevance·Coherence·TaskAdherence)하고 직접 만든 평가표와 비교 | 선택. TaskAdherence는 Preview |
| Lab 07 B 2단계 | baseline이 모두 통과하면 `collect --retrieval none`으로 진단할 실제 dev 실패를 만듦. `feedback`과 `cloud-evaluate`는 거부 | 선택 |
| Lab 07 B 5단계 | `cloud-evaluate --business-evaluator`가 로컬 업무 규칙과 같은 본인 소유 코드 기반 평가자를 등록·재사용. `--reference`는 candidate를 baseline 평가에 추가해 **실행 비교** | 선택 Preview |
| Lab 04 5절 | `maf-evaluate`가 MAF 함수 도구 에이전트의 호출을 `tool_call_accuracy`·`relevance`로 채점 | 선택. MAF API는 실험 기능 |
| Lab 09 A | 담당자가 준비한 기존 추적 평가와 **되풀이** 옵션 | 여기서는 안내만 했고, 같은 날 담당자 조치 뒤 실행([이전에 실행하지 않은 항목](#previously-not-run-items)) |

**실제 Azure 확인(영문·국문 별도, `gpt-6-sol` / `gpt-6-sol-judge`):**

| 확인 | 영문 | 국문 |
|---|---|---|
| 포털 평가(Relevance / Coherence / TaskAdherence) | 5/6, 6/6, 1/6 | 5/6, 6/6, 0/6 |
| 같은 에이전트의 직접 업무 평가 | 6/6 | 6/6 |
| 새 dev 수집의 업무 검사(baseline / candidate) | 6/6, 6/6 | 6/6, 6/6 |
| 근거 없음 진단 | 0/6, 오류 0, `feedback` 거부 | 0/6, 오류 0, `feedback` 거부 |
| `business_rubric`을 포함한 cloud judge(groundedness / relevance / 업무, 실행마다) | 6/6, 6/6, 6/6. 일치 6/6 | 6/6, 5/6, 6/6. 일치 6/6 |
| 두 실행의 포털 비교 | relevance 4.33 → 4.83, 샘플 부족 | relevance 3.83 → 4.50, 샘플 부족 |
| `maf-evaluate`(tool_call_accuracy / relevance) | 6/6, 6/6. 검토 수정 후 재실행(code `408b1b57…`, `eval_fd079e29…`) 6/6, 6/6 | 6/6, 5/6. 검토 수정 후 재실행(`eval_e330c6aa…`) 6/6, 6/6 |
| 근거 없음 진단의 cloud judge(거부 기능 추가 전) | 무효(`eval_f231e23c…`의 `evalrun_2b495a2e…`): Groundedness가 3/6행을 건너뜀, 집계하지 않음 | 무효(`eval_910a4729…`의 `evalrun_1e0790d4…`): Groundedness가 4/6행을 건너뜀, 집계하지 않음 |
| 대화 평가 모듈(턴, 대화 수준 groundedness) | 6/6·6/6, 1/2 | 6/6·6/6, 2/2 |

**발견 사항은 그대로 남깁니다:** TaskAdherence와 Relevance는 업무 평가와 달랐습니다. 평가자에게 **지침** 안의 정책이 아니라
질문과 답변만 전달되기 때문입니다. Relevance는 D05의 올바른 보류를 낮게 평가했고 실행마다 결과가 달랐습니다(녹화 5/6,
영문 검증 6/6, 국문 `maf-evaluate` 두 번은 5/6 후 6/6). context가 빈 행에서 Groundedness는 *건너뜀*(`not_applicable`)을
반환합니다. 워크숍은 건너뛴 행을 집계하지 않으며, 이제 `cloud-evaluate`가 근거 없음 실행을 제출 전에 거부합니다.
한국어 포털에서는 Relevance·Coherence 평가자의 한국어 기본 이름이 평가자 이름 검사를 통과하지 못해 이름을 바꾸기 전까지
**다음**이 비활성화되었습니다. 가이드에 우회 방법을 적었습니다. 6문항은 포털의 통계 비교에 너무 적습니다.

**같은 날 나중에 실행:** 기존 추적 평가, 되풀이 평가, Agent Optimizer, cloud red teaming, 새 릴리스 파이프라인 실행.
담당자 조치는 [다음 절](#previously-not-run-items)에 적었습니다.

**Azure 변경:** 업로드한 dev 질문 데이터 세트 2개, `cloud-evaluate`가 자동으로 만든 데이터 세트, 포털·SDK 평가와 실행(`...-trial-...` 이름의 평가 3개는 사전 점검이며 그중 하나는 오프라인 fixture 행을 채점, 무효 처리된 진단 실행도 남겨 둠),
본인 소유 사용자 지정 평가자 버전(`mfv2_sol_20260923_en_business_rubric` 1–2, `mfv2_sol_20260923_ko_business_rubric` 1).
모두 `mfv2-sol-20260923-<language>` prefix 아래에 있으며 유료 에이전트·judge 호출이 발생했습니다. 국문 캡처를 위해 포털 언어를
한국어로 바꾼 뒤 영어로 되돌렸습니다. 배포·역할 할당·기본 구독 변경은 없습니다.
[국문 결과](../live-run.md#선택-평가-추가분--별도-검증-2026-09-23) · [같은 포털 단계의 2026-09-24 녹화](../action-captures.md)

**로컬 검증:** 오프라인 테스트 255개가 Python 3.13과 3.14에서 각각 통과했고, 설치 SDK 테스트 73개가 stub transport로
통과했습니다. 새 테스트는 grader와 로컬 규칙의 일치, 진단 실행의 거부 경로, 건너뛴 judge 행, 사용자 지정 평가자 기준,
공유 reference 실행, 도구 결과 매핑, 새 캡처를 확인합니다. Ruff 0.16.6, 컴파일, 두 학습자 묶음, 깨끗한 복사본의 CI 오프라인 명령,
문서 검사(Markdown 117개, 언어 쌍 58개, CLI 예제 340개)가 통과했습니다. 최종 code hash: `67e7ac04…`.

<a id="gpt-6-sol-20260923"></a>

## gpt-6-sol 환경·녹화·이전 미디어 삭제 — 2026-09-23

**환경:** 전용 Sweden Central 리소스 그룹에 Foundry 계정(API 키 비활성)·프로젝트, system-assigned identity를 켜고
키 인증을 끈 Basic Search, Log Analytics(30일·일 1GB 한도), Application Insights, 키 없는 Search·Application Insights
프로젝트 연결과 리소스 범위 역할만 만들었습니다. 리소스 이름에는 처음 만든 `g6luna`가 남아 있습니다. 기본 Azure CLI 구독은 바꾸지 않았습니다.

**모델 변경:** `gpt-6-luna`는 배포됐지만 프로젝트 Responses·프롬프트 agent·MAF 경로에서 실패했습니다(HTTP 500, 포털 agent는
`reasoning.effort` 미지원). `gpt-6-sol`과 `gpt-6-astra`는 같은 agent 확인을 통과했고 `gpt-6-sol`을 선택했습니다
([모델 선택](model-choice.md)). 현재 환경에는 Data Zone Standard `2026-09-22`·`NoAutoUpgrade`의 `gpt-6-sol`(150K TPM)과
`gpt-6-sol-judge`(100K TPM)가 있습니다. `gpt-6-luna`·`gpt-6-luna-judge`·`gpt-6-astra` 배포, probe agent, 임시 North Central US
계정(purge 포함)은 삭제했습니다. 첫 포털 agent를 열 때 실습에서 쓰지 않는 `text-embedding-3-large`(Standard, 110K) 배포가 생성됐습니다.
Search knowledge base가 GPT-6 모델을 받지 않아 선택 IQ Chat preset은 `gpt-5.6-luna`를 유지합니다.

**녹화:** Lab 00–09·11의 A/B 주요 단계를 영문·국문 따로 실행했습니다. 언어별 69개 액션·무손실 캡처 207장·편집 영상 3개
(영문 4:36 / 2:30 / 1:43, 국문 4:32 / 2:27 / 1:43), 원본 구간 175·176개의 최소 중간 프레임 SSIM은 영문 0.9925·국문 0.9922이며
로컬 byte-range 재생과 챕터 이동 11개를 모두 확인했습니다. 업로드·push는 하지 않았습니다. 녹화한 모든 액션이 종료 코드 0이었고,
두 언어 모두 baseline 실패가 없어 feedback 단계는 실행하지 않았습니다. 언어별 업무 기준은 baseline 6/6·candidate 6/6·holdout 4/4,
candidate의 선택 cloud judge는 groundedness 6/6·relevance 5/6(D05, 올바른 보류)입니다.
[녹화](../video-summary.md) · [실제 결과](../live-run.md).

**삭제:** 2026-09-15 기본 과정 녹화, 2026-09-16 확장 녹화, 2026-09-23 `gpt-6-luna` 녹화와 해당 페이지를 작업 트리에서 삭제했습니다.
git 기록의 `47f3b49`에는 남아 있습니다. 이전 GitHub 첨부 URL은 더 이상 연결하지 않으며, 호스팅된 사본 삭제는 별도 수동 작업입니다.
IQ Chat preset은 바뀌지 않았으므로 2026-09-17 IQ Chat 설정 캡처는 유지합니다.

**로컬 검증:** Python 3.13·3.14 각각 offline 테스트 244개, stub transport를 쓰는 설치 SDK 테스트 67개가 통과했습니다.
Ruff 0.16.6 lint/format, compilation, 깨끗한 복사본의 CI offline 명령, 두 학습자 bundle 검사가 통과했습니다.
문서 검사는 Markdown 117개·언어 쌍 58개·CLI 예제 330개이며 보류된 번역은 없습니다.
이번 개정의 Azure 변경은 위 배포와 언어별 `mfv2-sol-20260923-<language>` prefix의 녹화용 agent·Search 객체·평가 run뿐이며
역할이나 기본 구독은 바꾸지 않았습니다.

## 재실행할 로컬 검사

```bash
python3.13 -S -m unittest discover -s tests -t . -q
python3.14 -S -m unittest discover -s tests -t . -q
python -m unittest discover -s tests_sdk -t . -q
python -m ruff check .
python -m ruff format --check .
python -m compileall -q src scripts examples tests tests_sdk
python scripts/check_docs.py
python scripts/build_learner_materials.py
python -m pip check
python scripts/check_sdk.py
```

유지보수 담당자는 `python scripts/check_dependency_drift.py`(권고용, PyPI 접근 필요, 고정 버전을 바꾸지 않음)와
azd 또는 Foundry 확장을 올린 뒤 `python scripts/record_azd_surface.py`(`check_docs.py`가 쓰는 help snapshot 갱신)를 실행할 수 있습니다.
**Approved live smoke check** workflow는 수동이며 비용 승인이 필요합니다.

SDK 테스트는 실제 설치 라이브러리와 명시적 transport stub을 사용합니다.
그 성공을 Azure 실제 응답으로 집계하지 않습니다.
이 페이지의 날짜별 기록마다 해당 revision에서 통과한 검사를 적습니다.

## 확인하지 않은 것

실제 회사/Microsoft 365 데이터, 외부 Work IQ/Fabric 연결, 운영 SLA, 통계적 우월성,
자동 재학습·가중치 변경, 사람 대신한 운영 승인, 다른 사용자 자산 삭제는 수행하지 않았습니다.
모델·Search·로그·파일의 잔여 비용은 session 중지와 별도로 확인합니다.

<a id="straightforwardness-95"></a>

## Straightforwardness 검토: 가이드와 문서 — 2026-09-24~25

**7차: 가이드 99.5/100, 문서 98/100.** 이전 차수(가이드, 문서): 1차 97/100, 86.5/100 · 2차 97.5/100, 94/100 ·
3차 93.5/100, 92.5/100 · 4차 96.5/100, 92/100 · 5차 100/100, 98.5/100 · 6차 94/100, 90/100.
1–4차와 6차는 매번 새로운 독립 AI cold read 7개를 사용했습니다. 영문 A·영문 B·국문 가이드(D1–D10)와 영문 2개·국문 2개 문서 그룹(R1–R10)입니다.
5차와 7차는 직전 차수 검토자들이 수정 뒤 자기 범위 전체를 다시 읽은 결과입니다.
6차(2026-09-25)는 검토 반영, 실제 검증, 보충 녹화, 정리 이후의 최종 점검입니다.
각 항목은 10점에서 시작해 치명·주요·중간·경미 발견마다 3·2·1·0.5점을 빼고, 검토자 중 가장 낮은 점수를 씁니다.
D10과 R10은 국문 검토에서 나옵니다. 새 검토자마다 다른 작은 문제를 찾았기 때문에 2–4차와 6차 점수가 오르내렸습니다.
이는 편집 평가이며 실제 학습자 시범 운영, 학습 성공률, 측정한 완료 시간이 아닙니다.

| 가이드 | 만점 기준 | 1차 | 2차 | 3차 | 4차 | 5차 | 6차 | 7차 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| D1 | 진입과 경로 선택이 각 경로의 첫 행동까지 이어짐 | 10 | 9.5 | 10 | 10 | 10 | 8 | 9.5 |
| D2 | 하나의 선형 핵심 경로. 선택·담당자·과거 자료는 접거나 표시 | 10 | 10 | 9 | 10 | 10 | 10 | 10 |
| D3 | 정확한 UI 이름·파일·값이 있는 번호 매긴 명령형 단계 | 10 | 10 | 9 | 10 | 10 | 9 | 10 |
| D4 | 모든 행동·명령 뒤에 보이는 성공/실패 확인 | 10 | 9 | 9 | 10 | 10 | 9.5 | 10 |
| D5 | 명령이 적힌 그대로 순서대로 실행되고 출력 파일 이름이 있음 | 10 | 10 | 10 | 7 | 10 | 10 | 10 |
| D6 | 핵심 경로의 쉽고 간결한 문장 | 10 | 10 | 9 | 9.5 | 10 | 10 | 10 |
| D7 | 담당자에게 요청할 내용까지 포함한 구체적 복구 | 9 | 10 | 9 | 10 | 10 | 10 | 10 |
| D8 | 명확한 완료 기준, 올바른 A/B 다음 링크와 인계 | 10 | 10 | 10 | 10 | 10 | 9.5 | 10 |
| D9 | 모델·날짜·화면·링크 설명이 최신이고 일관됨 | 10 | 10 | 9.5 | 10 | 10 | 9 | 10 |
| D10 | 국문이 영문을 그대로 반영하고 자연스럽게 읽힘 | 8 | 9 | 9 | 10 | 10 | 9 | 10 |

| 문서 | 만점 기준 | 1차 | 2차 | 3차 | 4차 | 5차 | 6차 | 7차 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| R1 | 목적·대상·현재 답이 먼저 나옴 | 8 | 10 | 10 | 9.5 | 10 | 8 | 10 |
| R2 | 제목·표·anchor로 답을 바로 찾음 | 9 | 10 | 10 | 9.5 | 10 | 10 | 10 |
| R3 | 번호 매긴 절차에 수행자와 성공 확인이 있음 | 10 | 10 | 10 | 9 | 10 | 10 | 10 |
| R4 | 숫자·flag·링크·결과가 가이드·CLI·근거와 일치 | 7 | 9 | 8 | 9 | 9 | 7 | 9 |
| R5 | 사실은 한 곳에만 두고 날짜별 이력은 간결 | 9 | 10 | 10 | 9.5 | 10 | 9 | 10 |
| R6 | 짧은 문장과 설명된 용어 | 9.5 | 10 | 10 | 10 | 9.5 | 10 | 10 |
| R7 | 간결하고 일관된 근거 경계·Preview 상태·날짜 | 10 | 9 | 9 | 9 | 10 | 8 | 10 |
| R8 | 유료 호출·클라우드 쓰기·역할·정리에 승인자와 수행자 명시 | 9 | 8 | 8 | 9 | 10 | 9 | 9 |
| R9 | 모든 페이지에 다음 단계. 끊기거나 삭제된 링크 없음 | 9 | 9.5 | 10 | 9.5 | 10 | 10 | 10 |
| R10 | 국문이 영문을 그대로 반영하고 자연스럽게 읽힘 | 6 | 8.5 | 7.5 | 8 | 10 | 9 | 10 |

**6차, 2026-09-25 최종 점검:** 치명 발견은 없었습니다. 발견 14건은 서로 다른 문제 12건이었고, 모두 영문 먼저, 이어서 국문을 고쳤습니다.

- **Lab 05의 A 방식 두 가지:** README, 학습 경로, 준비 카드, 담당자 준비, 강사 인계, Lab 00이 준비된 터미널과 함께
  Playground의 준비된 Hosted workflow agent를 안내하고, 둘 다 받지 못한 경우에만 Lab 00 B와 Lab 02 B로 보냅니다.
- **나중 실행으로 낡은 상태:** 위 미실행 답, Lab 08의 근거 한계, live-run 미실행 목록이 6절의 `curl` 요청 1회와
  3절 서버·`azd ai agent invoke --local`·원격 배포를 구분합니다. 고급 경로, 근거 허브, 모델 선택, coverage 설명에
  2026-09-24~25 모듈 실행과 Tool Search·Skills 차단을 반영했습니다.
- **단계와 확인:** Lab 01은 화면에서 잘리는 엔드포인트를 붙여 넣은 값으로 확인하고, Lab 09 정리 문장은 4단계를 가리킵니다.
  화면 안내에 2026-09-25 보충 녹화를 적었고, 국문 Lab 09 시작 카드는 다시 Lab 03 B의 `response_id`와 추적 접근을 요구합니다.
- **한 사실, 한 곳:** 2026-09-25 보충 기록에서 문서 검사 수치를 반복하지 않습니다.

**이후 수정, 재채점하지 않음:** 7차의 두 발견(준비 카드의 경로 문장·endpoint 행, 근거 허브의 담당자 승인 대기 목록)을 고쳤습니다.

**검증(2026-09-25):** Python 3.13·3.14 각각에서 offline 테스트 305개, Ruff 0.16.6 lint/format, Python compilation,
commit `f128f0c`의 `check_docs.py`(Markdown 127개, 로컬 링크 2,612개, anchor 554개, CLI 예제 328개, azd 예제 84개, 언어 쌍 63개), 학습자 번들 검사가
통과했고, 바뀐 언어 쌍은 `docs/localization.json`에 정확한 완료 hash가 있습니다. 검토자는 읽기만 했고,
이 검토에서 Azure 호출, 리소스 변경, push는 하지 않았습니다.

**검증 후 제외(1·4차):** 치명 발견 두 건은 문서가 아니라 검토자 안내의 오류에서 나왔습니다.
1차의 R4 발견은 coverage 페이지가 2026-09-23 `gpt-6-sol` 실행을 과장했다고 봤지만 그 내용은 맞았고,
모든 재실행을 부정한 README 문장이 틀려 이를 고쳤습니다. 4차의 D5 발견은 핵심 유료 명령에 `--confirm-cost`가 있다고 가정했지만
설계상 그런 flag는 없으며, 안내를 바로잡자 검토자가 철회했습니다(Lab 07 B에 유료 호출 수를 명시).
이 둘을 빼면 1차 문서는 89.5, 4차 가이드는 99.5입니다. 국문 핵심 명령마다 `--language ko`를 붙이자는 1차 제안은
국문 녹화가 기본 형태를 사용하므로 채택하지 않았고, 대신 Lab 00에 두 국문 형태를 모두 설명했습니다.

**1–4차 뒤 바뀐 점(영문 먼저, 이어서 국문):**

- **검증 페이지:** 현재 답 표를 맨 앞에 두고, 현재 근거·로컬 검사·범위 밖 항목을 접은 검토 이력과
  2026-09-15~17 기록보다 먼저 배치했습니다. 녹화 요약은 목록으로 바꿨습니다.
- **코드와 맞는 확인:** Lab 00의 Python 안내와 설치 확인, Lab 02의 `usage` 필드, Lab 04/07의 예상 실패를 확인하는 `echo $?`,
  Lab 08의 출력 경로와 기존 패키지 재생성 명령, `maf-evaluate --output`, Hosted `stop-session` receipt.
- **명령 바로 앞의 승인자·수행자:** A2A 쓰기, `routine create`, agent-safety 재배포, optimizer 제출, `stop-session`,
  Lab 07 B의 유료 수집.
- **핵심 경로에서 읽을 양 축소:** Lab 09 A의 선택 추가 검토와 선택 모듈의 정리 행을 접었고,
  두 학습자 `START-HERE.txt`에 가이드 페이지가 ZIP 밖에 있다고 적었습니다.
- **한 사실, 한 표현:** 9월 23일에 다시 실행한 네 모듈, 9월 23일 실행 목록의 대화 평가, fixture 파일,
  통합본 제목 "Lab 00–09·11", 릴리스의 배포·버전·일정, 9월 23일 표의 Lab 09 A 상태를 페이지마다 맞췄습니다.
- **탐색:** 두 액션 인덱스의 Lab별 바로 가기, coverage·개발 도구의 다음/복귀 링크, 근거 페이지 하단의 현재 페이지 표시,
  두 언어가 같은 51행 전체 오류 참조.
- **국문:** 모든 확장 페이지, Lab 10, 표시된 가이드·참조 절을 문장 단위로 대조했고 국문 edition 결과와 한국어 UI 단계는 유지했습니다.
  A 경로, Lab 00의 언어 안내, 여러 참조 문장을 자연스럽게 고쳤습니다.

**이후 수정, 재채점하지 않음:** 5차의 두 발견(model-choice의 빠진 서술어, coverage의 일정 수)을 고쳤습니다.

**검증(2026-09-24):** Python 3.13·3.14 각각에서 offline 테스트 287개가 통과했습니다. 새 테스트 5개가 이 기록의 계산,
검증 페이지 구성, 두 언어의 오류 참조 일치, `--output` 명령 목록, 학습자 START-HERE 파일을 확인합니다.
Ruff 0.16.6 lint/format, Python compilation, 문서 검사(Markdown 117개, 언어 쌍 58개, CLI 예제 328개),
학습자 번들 byte 비교가 통과했습니다. 바뀐 언어 쌍은 `docs/localization.json`에 정확한 완료 hash가 있고 유예한 번역은 없습니다.

**범위(2026-09-24):** workshop 명령 줄, Foundry 요청 로직, prompt, 합성 정책, 평가 데이터, fixture, 녹화는 바꾸지 않았습니다
(국문 `printf` 안내 문구 하나만 번역). 학습자 `START-HERE.txt` 문구가 바뀌어 두 학습자 ZIP을 다시 생성했습니다.
Azure 호출, 리소스·권한 변경, 배포, 게시, push는 하지 않았습니다.

## 이전 검증 기록

이전 가이드 검토, 2026-09-17 기록, 2026-09-15 미디어/실행 이력은 [검증 기록 보관](validation-history.md)으로 이동했습니다. 현재 페이지에는 현재 답, 최근 날짜별 근거, 로컬 검사와 범위 경계만 남깁니다.
