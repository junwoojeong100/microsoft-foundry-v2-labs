# 검증 범위와 실제 실행 — 2026-09-15

[English](../../reference/validation.md) | **한국어**

**설치·offline 계약·실제 Azure 실행·모델 품질·미디어 검수는 서로 다른 검증입니다.**
국문과 영문은 별도 label과 촬영 원본을 사용합니다. 이전 영상이나 upstream 성공을 새 결과로 재분류하지 않습니다.

## 국문 실제 Azure 실행

기존 Sweden Central 실습 프로젝트를 재사용했습니다. 기본 구독을 바꾸거나 새 Resource Group을 만들지 않았습니다.
승인된 Sol/Terra/Astra 배포를 각각 100K TPM으로 추가하고, 해당 Hosted identity에 필요한 최소 모델/Search 역할만 부여했습니다.
Luna·judge·embedding 배포는 기존 자산을 사용했습니다.

| 대상 | 버전 | 행 수 | 실행 오류 | 업무 검사 | Groundedness | Relevance | Root trace 확인 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `ko-baseline-final` | 7 | 24 | 0 | 24/24 | 24/24 | 19/24 | 24/24 |
| `ko-candidate` | 8 | 24 | 0 | 24/24 | 22/24 | 20/24 | 24/24 |
| `ko-holdout` | 8 | 16 | 0 | 16/16 | 16/16 | 13/16 | 16/16 |

Calibration은 고정 정답/오답 두 건 중 두 건을 기대대로 분류했습니다.
이는 target이 생성한 새 응답 두 건이 아니며 judge 전체를 인증하는 결과도 아닙니다.
초기 version 6의 진단용 24행과 native run은 위의 통제된 비교와 분리해 보존했습니다.

`review-native-findings`는 운영 승인이 아닙니다. 업무 기준을 맞힌 보류 답변이 relevance에서 낮게 평가될 수 있으며,
실제 점수와 이유를 그대로 남깁니다. V2가 모든 지표에서 개선됐다고 주장하지 않습니다.
Baseline이 모두 통과해 실패를 만들거나 회귀 승격을 강제하지 않았습니다.

**실행·평가 계보:** [현재 실행 결과](../live-run.md), 새 asset 디렉토리의 `live-results.json`,
원본 `outputs/benchmarks/`의 dataset/corpus/response/native/trace/cleanup 기록으로 연결합니다.
공개 holdout은 최종 인수 절차 교육용이며 미사용 운영 검증셋이 아닙니다.

## 실제 실행에서 수정한 계약

영문은 별도 영어 지침·정책·데이터로 실행했습니다. 초기 IQ 검색 누락에 따른 20/24 결과를 보존한 뒤
같은 provider의 검색 필터를 명시한 새 baseline을 24/24로 확인했습니다.
V2 candidate는 23/24이며 Astra의 dev D05 인용 관련성 실패를 그대로 남겼습니다.
Dev에서 통과한 Luna/Sol/Terra만 사전에 선택해 holdout 12/12를 확인했습니다.
영문 native 결과와 3모델 선택 이유는 [영문 실행 기록](../../live-run.md)에 별도로 있습니다.
국문 결과나 16행 분모를 영문으로 복사하지 않습니다.

- full agent endpoint와 `--protocol`을 동시에 지정하는 azd 인자 충돌.
- session query 추가 시 `api-version=v1`이 사라지지 않도록 URL query merge.
- embedding 404 이후 원래 실패를 보존하고 같은 account API를 명시적으로 선택.
- App Insights 전용 audience와 구독/tenant에 고정된 credential로 동일 query API 호출.
- 이미 idle인 session은 불필요한 stop 요청 없이 관측한 상태를 기록.

수정 중에 결과를 덮어쓰거나 다른 모델/원본/fixture로 성공을 만들지 않았습니다.
Runtime 코드가 바뀐 초기 진단과 최종 비교는 별도 version·label로 남겼습니다.

## 미디어 검증

새 국문은 **182개 액션**, **543개 무손실 캡처**, 세 개의 편집 영상입니다.
선택된 WebP는 원본 PNG와 RGB 픽셀이 동일합니다.
**435개 편집 구간**을 실제 원본 영상과 대조했고 최소 midpoint SSIM은 **0.987849**였습니다.
모든 MP4의 전체 decode·frame 수를 검사했으며 편집은 대기를 제거한 실제 footage입니다.
챕터 카드는 앱 화면이 아니라고 표시합니다.

인증/비밀번호 입력은 녹화하지 않았습니다. UI 실패·설치/인증 오류·초기 진단도 원본과 액션 이력에 남습니다.
한 trace에서 포털에 보이는 17개 span/2개 chat과 응답의 실제 model call 3개를 구분했습니다.
64개 root trace 확인을 모든 child span의 완전한 export 증거라고 부르지 않습니다.

새 파일 검색 원문 여섯 개는 원격 Files API로 읽어 번들 원본과 바이트/hash 일치를 확인했습니다.
UI 인용 버튼의 다운로드가 확인되지 않은 시도는 성공으로 표시하지 않았습니다.

## 재실행할 로컬 검사

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

SDK 테스트는 실제 설치 라이브러리와 명시적 transport stub을 사용합니다.
그 성공을 Azure 실제 응답으로 집계하지 않습니다.
최종 영어 확장과 미디어 교체 후 전체 검사를 다시 수행합니다.

최종 검사에서 Python 3.13·3.14의 offline 테스트는 **각 98개**, 설치 SDK 테스트는 **21개**가 통과했습니다.
Ruff·format·Python compilation·의존성·SDK 계약·문서 검사도 통과했습니다.
문서 검사는 **35개 언어 쌍·200개 CLI 예제**와 번역 유예 0개를 확인했습니다.
영문 새 자료는 172개 액션·516개 무손실 캡처·영상 3개이며,
407개 편집 구간의 원본 대비 최소 SSIM은 0.985156입니다.
두 언어의 새 파일을 검수한 뒤 이전 미디어 1,452개와 중복된 구버전 진입 문서를 제거했습니다.
사용자 승인 후 새 영상 6개를 비공개 저장소의 GitHub 첨부로 게시했습니다.
실제 업로드 파일의 byte/hash·재생·챕터 이동을 확인했으며 임시 서명 storage URL은 저장하지 않았습니다.

## 확인하지 않은 것

실제 회사/Microsoft 365 데이터, 외부 Work IQ/Fabric 연결, 운영 SLA, 통계적 우월성,
자동 재학습·가중치 변경, 사람 대신한 운영 승인, 다른 사용자 자산 삭제는 수행하지 않았습니다.
모델·Search·로그·파일의 잔여 비용은 session 중지와 별도로 확인합니다.
