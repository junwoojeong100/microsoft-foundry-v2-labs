# 이 에디션의 검증 기록

**2026-09-13: 로컬 검사에 이어 요청 계정의 실제 Azure 실행과 headless 녹화를 완료했습니다.**
실제 결과·화면·영상·미실행 범위는 [전체 실행 기록](../live-run.md)에 있습니다.
업스트림 리포의 성공 기록을 이 에디션의 결과로 복사하지 않았습니다.

## 로컬 코드·계약 확인

| 항목 | 결과 | 범위 |
|---|---|---|
| 전용 Python 3.13 환경 / `pip check` | 통과 | 선언된 SDK 의존성 일치 |
| `scripts/check_sdk.py` | 통과 | 고정 버전과 실제 import surface |
| Ruff / format / Python compile | 통과 | 소스 스타일·문법 |
| 오프라인 단위·계약 검사 | **48개 통과** | JSON·검색·오류 분모·hash·holdout·패키징·MAF 경로·공통 schema |
| 설치된 SDK 계약 검사 | **7개 통과** | 요청 직렬화·구독 범위 인증·workflow·MCP·hosting adapter |
| 문서 검사 | 통과 | 로컬 링크·이미지·CLI 예제 인자 |

SDK 단위 검사의 model HTTP 요청은 MockTransport로 가로챕니다.
아래 실제 실행과 혼동하지 않습니다.

## 실제 서비스 확인

| 항목 | 실제 확인 결과 |
|---|---|
| 계정 | 지정 계정의 CLI·azd·브라우저 identity와 tenant 확인 |
| 모델 | 기존 `gpt-5.4-mini`의 SDK 및 포털 응답 |
| Prompt Agent | 새 전용 agent version 1 생성, SDK/포털 실제 응답 |
| MAF | 함수·로컬 MCP·순차·병렬·Group Chat 실제 실행 |
| Search / IQ | 새 index/source/base 생성, GA `2026-04-01` retrieval과 실제 원문 근거 |
| dev 학습 루프 | **4/6 → 5/6 → 6/6**, 실패와 원래 응답 보존 |
| 고정 후보 holdout | **4/4** |
| Foundry 평가 | 별도 GPT-5.4 judge: groundedness **6/6**, relevance **6/6** |
| Hosted | code deployment 버전 1 활성화, 로컬·원격 응답 |
| Trace | 원격 호출과 같은 ID, 20 spans, 모델 2회·도구 1회, root Completed |
| 정리 | 로컬 서버 종료, 새 Hosted session 중지 후 idle 확인 |
| 녹화 | headless Playwright, 전체 약 111분 + 같은 과정의 20분 배속본 |

같은 dev 데이터·업무 기준을 유지했고, 미사용 holdout은 후보 고정 후에만 호출했습니다.
권한·모델·검색 실패를 다른 모델이나 fixture로 바꾸어 성공 처리하지 않았습니다.
초기 실패와 후속 수정은 [실행 기록](../live-run.md)의 표에 있습니다.

## 남겨 둔 자산과 한계

새 실습 agent·judge 배포·Search 객체·평가 결과는 검토와 재현을 위해 남겨 두었습니다.
공유 프로젝트·모델·기존 데이터를 삭제하거나 변경하지 않았습니다.
중지한 session의 파일시스템과 서비스 비용이 사라졌다고 주장하지 않습니다.

실제 Fabric/Work IQ/Microsoft 365 연결, Web Search, File Search 업로드, 추가 모델 A/B,
자동 trace-to-dataset, 자동 Hosted 평가 suite, continuous evaluation, fine-tuning은 미실행입니다.
Hosted smoke 결과에 프로젝트 Responses + IQ 평가 점수를 재사용하지 않습니다.

Trace에는 내부 storage 조회 span 2개의 실패 표시가 있었습니다. root 응답은 Completed였지만
“오류 0”으로 표시하지 않습니다. Monitor의 반올림된 `$0`도 무료 실행의 근거가 아닙니다.
MCP/Pydantic과 hosting SDK의 prerelease/resilience 경고를 숨기지 않았습니다.

## 재검증

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
기본 단위 검사는 표준 라이브러리만 사용합니다.
GitHub Actions 구성은 제공했지만 이번 검증에서 원격 workflow 실행 결과를 주장하지 않습니다.
새 실측을 추가할 때는 날짜·실제 모델/agent version·실패·정리 상태를 기록하고,
비밀·개인 식별자·원시 인증 로그는 공개하지 않습니다.
