# 이 에디션의 검증 기록

[English](../../reference/validation.md) | **한국어**

## 한국어 통합 개정 `ko-integrated-20260915`

**이 절은 아래의 개정 전 촬영 결과와 구분합니다.**
새 workflow/Invocations/profile/모델 matrix/calibration/회귀/trace/hybrid 코드를 추가했습니다.
실제 설치 SDK를 사용하는 transport-stub/ASGI 계약과 offline 회귀 검사를 수행합니다.
새 Azure 배포·유료 matrix/judge 실행·한국어 촬영·영문 번역/촬영은 이번 단계에서 수행하지 않았습니다.

기존 2026-09-14/15 영상과 upstream `foundry-evaluation`의 64응답·trace 기록을
새 구현의 성공으로 재사용하지 않습니다. [아카이브 인수 게이트](consolidation.md)와
[평가 워크북](evaluation-workbook.md)의 실제 실행이 다음 단계입니다.
조회한 CLI/확장의 Incompatible 상태는 [버전 기준](versions.md)에 기록했으며 자동 업그레이드하지 않았습니다.

### 이 개정에서 실제로 수행한 로컬 검사

- Python **3.13 / 3.14**, site packages를 비활성화한 offline 검사 **각 90개 통과**.
- 고정 설치 SDK 계약 **17개 통과**: 세 workflow의 실제 builder, Responses/Invocations ASGI host,
  요청별 상태 격리, 실제 SDK의 두 추론 API 직렬화·token audience, native version 고정·실패 재시도 보존.
- Ruff lint/format, Python compilation, `pip check`, SDK 직접 의존성 버전 검사 통과.
- 문서 **73개**, 언어 쌍 **36개**, CLI 예제 **152개** 검사.
  영어 유예 **23개**는 visible warning과 양쪽 파일 hash로 제한하며 명령 파서는 그대로 적용.
- Headless Edge에서 한국어 **35페이지·이미지 참조 79개**의 로컬 렌더링 확인.
  이 과정의 Azure 요청·새 스크린샷·동영상 녹화는 **0회**.

SDK 검사는 실제 설치 라이브러리를 사용하지만 모델 HTTP transport와 evaluator service 응답은
명시적인 test stub입니다. 이를 live Azure 성공이나 새 모델 품질 점수로 집계하지 않습니다.
표본 24/24/16행, calibration confusion matrix, 누락·오류·tamper 거절, query-only 계약,
회귀 소비와 holdout 차단은 테스트로 확인했습니다.

```bash
python3.13 -S -m unittest discover -s tests -t . -q
python3.14 -S -m unittest discover -s tests -t . -q
python -m unittest discover -s tests_sdk -t . -q
python -m ruff check .
python -m ruff format --check .
python -m compileall -q src scripts examples tests tests_sdk
python scripts/check_docs.py
python -m pip check
python scripts/check_sdk.py
```

## 2026-09-15 새 영문 가이드 촬영·검증

영문 문서 `26d2e80`을 먼저 게시한 뒤 촬영했습니다.
[새 영상과 범위](../english-recordings.md)·[234개 액션](../english-captures.md)은
아래 2026-09-14 증거와 별개입니다. **537개 lossless 캡처**,
통합본 **13분 09초**, CLI **5분 15초**, 포털 **4분 45초**를 제공합니다.

새 원본 dev 결과는 **v1 5/6·v2 6/6**, 각 6행·수집 오류 0이며
v1 D06 판단 실패와 검토 대기 기록을 보존했습니다. 후보 고정 후 교육용 holdout은 **4/4**였지만
이미 알려진 세트이며 새 미사용 검증셋이나 영어 모델 평가로 주장하지 않습니다.
안내 질문의 HTTP 503과 로컬 azd context 누락 오류를 별도 성공 재시도와 함께 보존했습니다.
실제 readiness `{"status":"healthy"}`는 SDK 계약 검사와 양쪽 가이드에 반영하고 문서 장면을 다시 촬영했습니다.

새 원격 Hosted 요청의 동일 Trace `94b4e5f61dc7e93016fc53a57ffa9f78`에서
**보이는 span 15개·chat 1개·tool 1개·root OK**를 확인했습니다.
과거 20-span Trace와 구분하며 native/Hosted rubric 보고서는 재실행하지 않고 관찰만 했습니다.
리소스 생성·배포·역할 변경·기본 구독 변경·회사/M365 접근은 없었고 이번 세션·로컬 서버를 중지했습니다.

최종 로컬 검사는 **오프라인 70개·SDK 계약 7개**, Ruff lint/format·Python compilation·문서 검사를 통과했습니다.
문서 **67개·언어 33쌍·동일 CLI 예제 108개**를 확인했습니다.
Headless Edge에서 **64페이지·이미지 참조 158개**, 두 촬영본의 **24개 챕터 이동**,
영상·시각을 유지하는 언어 전환과 잘못된 입력 거절을 확인했습니다.

실제 GitHub에서 받은 영상 **3개 SHA-256**이 일치했고, 두 언어의 내장 플레이어에서 **18개 위치 재생·탐색**,
GitHub Markdown의 **492개 시각 링크**, 인증된 직접 링크의 **15회 redirect·시각 이동**을 확인했습니다.
mock/로컬 영상으로 대신하거나 서명된 CDN URL을 저장하지 않았습니다.
[재생 검증](../../assets/english-20260915/playback-verification.json)에 결과를 보존합니다.
원시 실행·원본 영상 6개·캡처 계보·해시는 `outputs/english-20260915/`에 비공개로 보존하고 인증 정보는 제외했습니다.

## 과거 원본 증거

**2026-09-14 · 완전히 새로운 Sweden Central 환경 · 새 액션별 촬영**

[실제 실행](../live-run.md) · [영상](../video-summary.md) ·
[236개 액션 증거](../action-captures.md)

이번 실행은 `8d094723d651d011592578a76609695c86570ba7`을 독립된 폴더에 풀어 시작했습니다.
아래 결과는 이 실행에서 직접 확인했으며 업스트림 성공 기록을 복사하지 않았습니다.
촬영에서 확인한 안내 보완은 현재 가이드에 반영했습니다.

## 실제 Azure 결과

| 대상 | 새 실행 결과 |
|---|---|
| 환경 | `rg-mfv2-action-swc-20260914`, 모든 지역 리소스 Sweden Central, 기본 구독 불변 |
| 모델 | 정확한 Luna `2026-07-09`, target 100K / 별도 judge 50K, Data Zone Standard, NoAutoUpgrade |
| 포털 / SDK | 브라우저 생성 agent v3의 안내 4문항·dev 6문항, 별도 SDK agent v1 |
| MAF | 단일·함수·MCP, A의 두 순차 질문, B의 세 패턴 |
| Search / IQ | 합성 6건과 실제 GA retrieval. 포털 관찰 후 동일 GA 호출 재확인 |
| File Search | 별도 agent v2, 6개 Completed, 저장 파일 6개가 합성 원본과 바이트 일치 |
| dev | v1 6/6, v2 6/6, 동일 local retrieval·모델·데이터·출력 한도 |
| native | groundedness 6/6, relevance 5/6. D05의 원래 2점과 이유 보존 |
| 교육용 holdout | 고정 후보의 마지막 인수 절차 4/4. 이미 사용된 세트이며 새 미사용 검증셋으로 주장하지 않음 |
| Hosted | 새 code deployment v1, 로컬·원격 실제 응답, 두 모델 요청과 함수 도구의 성공 로그 |
| Hosted 평가 | 실제 새 원격 응답 6건, query-only 입력 6건 검증, 생성형 rubric 6/6 |
| Trace | 동일 ID `e72dc58132dbc461e5fa381c67da3ed9`, 20 spans, chat 2회·도구 1회, root Completed |
| Trace 하위 오류 | 초기 state store/item GET 404 두 개를 보존. 이후 생성·갱신과 최종 Responses 요청 성공 |
| 정리 | 본인 세션 2개 stop 후 모두 idle, 로컬 서버 종료, 기존 Azure 환경 보존 |

자연어 답변 검토·결정적 업무 검사·native judge·Hosted rubric은 별개의 기준입니다.
실패·누락을 분모에서 제외하거나 모델 지연의 미측정 값을 0으로 채우지 않았습니다.
Hosted 실제 run의 evaluator version selector는 빈 값입니다. 조회한 catalog v1을 소급해 고정 버전이라고 부르지 않습니다.
사람의 운영 승인, durable crash recovery, 실제 Fabric·Work IQ·M365 연결은 수행하지 않았습니다.

## 이번 가이드 보완

- 새 에이전트에도 기본 Web Search가 다시 붙으므로 첫 질문 전에 별도로 제거합니다.
- 실제 메뉴 **New agent → Build an agent**, **Save와 Publish의 차이**를 명시했습니다.
- 모델 탭 이동 시 나타나는 **Leave without saving?** 확인 창을 안내합니다.
- 터미널 자체 길이 제한에 잘리지 않도록 2001자 입력을 짧은 Python 생성 명령으로 검사합니다.
- File Search의 인용 버튼이 원문을 열지 않은 사실을 기록합니다. 같은 저장 원문은 SDK로 별도 확인했습니다.
- GA IQ와 포털 편집기의 chat model 요구를 구분하며, 관찰만 하고 GA 구성을 바꾸지 않습니다.
- Hosted 로그는 호출 직후 확인하고, 성공한 root와 하위 초기화 404를 구분합니다.

## 새 미디어 검증

CLI **841.52초**, 포털 **549.44초**이며, 모두 실제 새 원본 구간을 1배속으로 연결했습니다.
각 원본 안의 순서를 유지했고 명령 출력이나 화면을 스크린샷 슬라이드로 재현하지 않았습니다.

| 검사 | 확인 |
|---|---|
| 액션 경계 | CLI 131개 + 포털 105개에 화면과 영상 구간 연결 |
| 캡처 | 원본 1,500회 → 의미 있는 1,065회, 중복 제거한 898개 lossless WebP |
| 이미지 일치 | PNG와 WebP를 디코딩한 RGB 픽셀 일치 |
| 비디오 무결성 | 모든 프레임을 FFmpeg로 디코딩 |
| 원본 대응 | 227개 구간의 시작·중간·끝 **681프레임** 비교 |
| 최소 SSIM | CLI **0.984467**, 포털 **0.991442** |
| 인증 | 로그인·PIN·MFA는 촬영하지 않음 |

[프레임 대응과 비교 결과](../../assets/live-20260914-action/edit-timeline.json) ·
[미디어 해시](../../assets/live-20260914-action/media.json)

새 영상 파일과 가이드를 저장소에 반영하는 것과 GitHub 내장 플레이어용 첨부 업로드는 별개입니다.
2026-09-14 최신 통합본·CLI·포털 영상 세 개의 해시를 확인한 뒤 같은 비공개 저장소 범위의 동영상 첨부로 업로드했습니다.
가이드에는 고정된 canonical 첨부 URL만 사용하며 서명된 private CDN URL이나 토큰을 저장하지 않습니다.
인증된 GitHub Markdown API로 `video-summary.md`와 `live-run.md`의 변경 본문을 렌더링해
각각 내장 플레이어 3개가 생성되는지 확인했습니다. 실제 private GitHub CDN에서 받은
영상 세 개의 바이트 수·SHA-256이 저장소의 최신 파일과 같았으며,
headless Edge에서 6개 플레이어의 시작·50%·90% 위치 **18회 재생/탐색**을 확인했습니다.
로컬 영상이나 mock 응답으로 대체하지 않았으며, 문서의 재생 링크도 같은 최신 첨부 URL을 가리킵니다.
직접 재생 링크의 인증된 요청은 GitHub 자산으로 리디렉션됐고, 최종 응답은
`video/mp4`와 HTTP 200이었습니다. 그 실제 목적지를 Edge의 기본 동영상 문서로 열어
영상이 재생되는 것도 확인했습니다. GitHub 인증 토큰은 리디렉션 대상에 전달하지 않았습니다.

통합본의 **12개 챕터 시각**은 실제 인증된 GitHub의 첫 302 응답을 브라우저에 전달한 뒤,
브라우저가 실제 자산으로 이동하면서 `#t=` 위치를 유지해 재생하는지 확인했습니다.
**236개 액션과 12개 챕터 링크 전체**가 GitHub Markdown 렌더링 뒤에도 해당 시각을 유지했습니다.
시각 링크 앞의 `▶` 표기는 GitHub가 링크를 중복 동영상 플레이어로 바꾸어 시각을 없애지 않도록 유지합니다.
시각 표에는 중복 플레이어가 생성되지 않았으며, 로컬 영상이나 임의 응답으로 대체하지 않았습니다.

## 단계별 참고 이미지 보완

2026-09-14 촬영 이미지를 실습 절차 옆으로 옮겨 **12개 랩의 직접 이미지 참조를 18개에서 77개로 확대**했습니다.
강사 가이드 2개를 포함하면 79회 참조이며 서로 다른 기존 캡처 77개를 사용합니다.
각 이미지에 조작 위치·확인 항목·해석상 주의를 붙이고, 선택적인 File Search 과정은 접어서 볼 수 있게 했습니다.
완료 화면만 모아 두지 않도록 단계별 배치를 검사합니다.

원본 이미지·영상·미디어 계보와 기존 실습의 명령/코드 블록은 변경하지 않았습니다.
로컬 Markdown 미리보기를 headless Edge에서 열어 **13개 가이드의 이미지 79개**가 로드되는지,
File Search 선택 절의 이미지가 펼쳐지는지 확인했습니다. 외부 업로드나 Azure 호출은 하지 않았습니다.

## 실습 순서 통합 영상

기존 CLI/포털 편집본을 Lab 00–11로 재배치한 **1,414.96초(23분 35초)** 통합본을 추가했습니다.
새 Azure 실행이나 원본 시각 순서라고 표시하지 않습니다. 서로 다른 경로·에이전트 버전·평가 기준도 유지합니다.

- 기존 두 편집본의 **34,774프레임을 중복·누락 없이 한 번씩** 사용했습니다.
- **236개 액션 모두** 통합본 구간과 연결했습니다. 각 챕터는 가이드 순서대로 배치했습니다.
- 별도로 표시한 12개 제목 화면은 600프레임(24초)입니다. 합계는 **35,374프레임**입니다.
- 전체 프레임 디코딩, MP4 안의 12개 챕터와 시각을 확인했습니다.
- 387개 실제 영상 조각의 시작·중간·끝 **1,161프레임**을 원본 편집본과 비교했고 최소 SSIM은 **0.988877**입니다.

[통합본 프레임·챕터 대응](../../assets/live-20260914-action/combined-timeline.json)에 원본 파일 해시와 정확한 대응을 보존합니다.
기존 두 영상과 GitHub 첨부 URL은 변경하지 않았습니다. 통합본도 같은 비공개 저장소의 별도 동영상 첨부로 업로드했습니다.
로컬 재생기에서 통합본 기본 선택과 **12개 챕터의 실제 재생/이동**, 개별 영상 전환,
직접 시각 링크 및 잘못된 시각 거절을 headless Edge로 확인했습니다.

## 재검증 명령

### 2026-09-15 영어 기본 문서 전환

오프라인 63개·설치 SDK 계약 7개, Ruff lint/format, Python compilation,
의존성·SDK 검사를 통과했습니다. 문서 검사에서는 Markdown 63개, 로컬 링크 2,747개,
로컬 heading anchor 12개, CLI 예제 108개, 양방향 언어 문서 31쌍을 확인했습니다.
두 언어의 정책 질문·CLI 옵션은 같고, 합성 원본·프롬프트·Azure 통합 코드는 변경하지 않았습니다.

Headless Edge에서 양쪽 언어의 가이드 60페이지와 이미지 참조 158개를 확인했습니다.
로컬 재생기는 영어 기본, 언어 전환 시 영상·시각 유지, 12개 챕터 이동,
원본 영상 3개 실제 재생, 잘못된 시각·파일·언어 거절을 확인했습니다.
이는 **Azure 요청 0회의 로컬 검사**이며 아래의 2026-09-14 실측과 구분합니다.

이번 변경에서 오프라인 **59개**, 설치 SDK 계약 **7개**, Ruff·format·Python compilation,
SDK 버전·의존성 검사를 통과했습니다. 문서 **31개**, 로컬 링크 **1,338개**,
CLI 예제 **54개**를 확인했습니다.
실제 headless Edge에서 새 영상 두 개의 시작·25%·50%·90% 위치 **8회 재생/탐색**,
영상 전환, 잘못된 시각/파일 이름 거절을 확인했습니다. 외부 요청이나 mock 영상은 사용하지 않았습니다.

```bash
python -m pip check
python scripts/check_sdk.py
python -m ruff check .
python -m ruff format --check .
python -m compileall -q src scripts examples tests tests_sdk
python -m unittest discover -s tests -t . -v
python -m unittest discover -s tests_sdk -t . -v
python scripts/check_docs.py
```

SDK 검사는 `.[cloud,agents,hosted]`, Ruff는 `.[dev]` 설치가 필요합니다.
오프라인 계약 검사는 실제 Azure 품질 점수가 아니며, 원격 GitHub Actions 결과로 바꿔 적지 않습니다.
원시 응답·평가자·실행/정리 증거는 Git에서 제외된 `outputs/live-20260914-action/`에 보존합니다.
`.env`·인증 정보·개인 원문 trace는 Git에 추가하지 않습니다.
