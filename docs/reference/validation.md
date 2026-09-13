# 이 에디션의 검증 기록

**작성일: 2026-09-13. 로컬 검증과 실제 Azure 실행을 구분합니다.**
원본 리포의 영상·배포·평가 결과를 이 통합 에디션의 결과로 복사하지 않았습니다.

## 직접 확인한 범위

| 항목 | 결과 | 무엇을 증명하나요? |
|---|---|---|
| 고정 SDK 조합 설치 | 완료 | 프로젝트 전용 Python 3.13 환경에서 설치 가능 |
| `pip check` | 통과 | 설치한 패키지 사이의 선언된 의존성 일치 |
| `scripts/check_sdk.py` | 통과 | 직접 고정한 버전과 실제 import surface 일치 |
| Ruff / format / Python compile | 통과 | 소스 스타일·문법과 배포 패키지 컴파일 |
| 문서 검사 | **27개 문서 / 117개 로컬 링크 / 49개 CLI 예제 통과** | 파일 연결과 실행 인자가 실제 CLI와 일치 |
| 오프라인 단위/계약 검사 | **46개 통과** | 데이터·JSON·검색 계약·행 누락/오류·hash·holdout·패키징 보호 |
| Python 3.14 오프라인 검사 | **동일한 46개 통과** | 외부 SDK 없이 사용하는 core의 추가 Python 버전 확인 |
| 설치된 SDK 계약 검사 | **5개 통과** | 실제 SDK의 요청 직렬화·MAF·3종 workflow·MCP·host adapter |
| 로컬 MCP | 실제 stdio handshake / tool 호출 통과 | 합성 정책 파일을 실제 MCP 프로토콜로 읽음 |
| Hosted readiness | ASGI 메모리 전송에서 HTTP 200 | 설치된 adapter의 readiness 경로; Azure 배포/모델 호출은 아님 |
| offline fixture | v1 0/6, v2 6/6 | 의도적으로 인용을 제거한 고정 예제에 대한 **검사기 동작** |
| 실습 배포물 생성 | 완료 | 포털용 합성 텍스트 6개와 자체 완결형 Hosted 소스 패키지 |

SDK 검사는 모델 HTTP 요청을 **메모리 MockTransport로 가로채므로 Azure에 보내지 않습니다.**
로그의 `unit.invalid` / `unit.services.ai.azure.com`과 응답은 검사 전용입니다.
실제 서비스의 네트워크·권한·모델 가용성·응답 품질을 증명하지 않습니다.

## 명시적으로 실행하지 않은 범위

- Azure 리소스 생성·역할 할당·기본 구독 변경.
- 실제 모델 추론, Search/IQ 업로드·retrieval, 유료 Foundry judge.
- Hosted 원격 배포·원격 모델 응답·원격 버전 평가.
- 실제 Application Insights trace 도착과 운영 모니터링.
- Fabric/Work IQ 연결과 실제 Microsoft 365 데이터 접근.

이 항목의 수업 전 확인은 [강사 가이드](../instructor.md)에 있습니다.
구독·tenant·모델·quota에 따라 달라지는 영역이므로 미실행을 성공으로 표시하지 않습니다.

## 설치 중 해결한 호환성 문제

최신 버전의 공개 메타데이터와 작성 환경에서 실제 설치 가능한 버전이 달랐습니다.
또한 Foundry provider 1.12.0은 Projects `>=2.2.0,<2.4.0`을 요구해
Projects 2.6.0과 함께 설치할 수 없었습니다.
현재 [호환성 스냅샷](versions.md)으로 고정한 뒤 새 프로젝트 가상환경에서 설치와 import를 확인했습니다.
다른 프로젝트의 가상환경을 수정하거나 모델/endpoint를 바꾸어 문제를 숨기지 않았습니다.

## 관찰한 SDK 경고

- MCP/Pydantic의 `lifespan` forward-reference 경고가 나타날 수 있습니다.
  현재 고정 조합에서 실제 handshake와 합성 도구 호출은 통과했습니다.
- Hosting SDK는 experimental task 관련 경고를 출력합니다.
- 기본 Responses hosting의 durable crash recovery가 비활성화되었다는 경고가 나타납니다.
  이 에디션은 durable 승인/복구 시스템을 구현했다고 주장하지 않습니다.

경고를 전역적으로 숨기거나 내부 SDK를 임의로 패치하지 않았습니다.
운영용으로 확장할 때는 지원되는 버전과 resilience/저장소 설정을 별도로 검토합니다.

## 재검증 명령

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
기본 오프라인 검사는 Python 표준 라이브러리만으로 실행됩니다.
CI에도 같은 검사를 구성했지만 **원격 GitHub Actions를 실행했다고 주장하지 않습니다.**

리소스 생성/호출은 위 검사에 포함하지 않습니다.
실제 Azure 확인을 추가했다면 날짜, 명령, 모델/agent version, 실패, 비용·정리 상태를
새 기록에 남기고 개인 식별자·비밀·원문 trace는 공개하지 않습니다.
