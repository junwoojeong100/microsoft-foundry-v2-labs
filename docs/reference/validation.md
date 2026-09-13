# 이 에디션의 검증 기록

**2026-09-13 · 새 Sweden Central 전용 환경 · GPT-5.6 Luna**

[실제 실행 기록](../live-run.md)과 [headless 미디어](../video-summary.md)는 이번 실행의 결과입니다.
업스트림이나 이전 Luna 실행의 성공 기록을 새 결과로 복사하지 않았습니다.

## 2026-09-14: 게시된 가이드를 새 폴더에서 재실행

`b1ff68d`의 새 checkout과 Python 3.13 가상환경에서 가이드의 설치·명령을 실행했습니다.
이전 결과를 복사하지 않고 기존 Sweden Central 프로젝트의 같은 Luna 배포를 호출했습니다.
리소스 그룹 생성, 모델 재배포, 역할 변경, 기본 구독 변경은 하지 않았습니다.

| 확인 경로 | 새 실행 결과 |
|---|---|
| Lab 00 | `.[cloud,agents]`, 선택 `.[hosted]`, 강사의 lock 파일 설치 모두 성공. offline doctor·fixture v1/v2·compare 정상 |
| Lab 02–05 | 모델·구조화 답변·새 Prompt Agent·함수·MCP·세 워크플로 명령 실행 성공 |
| Lab 03 A | 가이드의 자연어 출력 지침과 합성 원문으로 새 버전 구성. 현행·과거·승인·근거 부족 4문항을 headless 새 대화로 확인 |
| Lab 06 | 별도 접두사의 Search index/source/base 생성과 Search/IQ 실제 검색·답변 성공 |
| Lab 07 | 가이드 기본값 `--retrieval local`로 새 baseline **6/6**, candidate **6/6**, native groundedness **6/6**, relevance **5/6** |
| Lab 08 | 새 패키징·azd 초기화·로컬 readiness/실제 답변 성공. 기존 원격 Hosted v1도 새 응답 확인; 재배포는 수행하지 않음 |
| Lab 09 | `cleanup-plan`이 삭제하지 않음을 확인하고 이번 원격 세션만 중지 |

Native relevance의 보류 답변 실패는 보존했습니다. 기존에 사용한 holdout을 회귀 검증에 재사용하지 않았으며,
이번에는 `--unlock-holdout` 없는 호출이 거부되는 잠금 동작만 확인했습니다.
따라서 9월 13일의 holdout 4/4를 이번 재실행 점수로 표시하지 않습니다.

### 실행 중 확인해 보완한 안내

- **독립된 azd 폴더:** 하위 checkout에서 `azd init`이 상위 `azure.yaml`을 선택했습니다.
  검증 중 추가된 서비스만 원복하고 상위 프로젝트 바깥에서 재실행해 현재 폴더에 생성됨을 확인했습니다.
- **명시적 Hosted 설정:** 생성된 agent `env`에는 모델만 있었습니다.
  endpoint·managed identity 모드·출력 한도를 넣는 정확한 YAML과 azd 값 설정/조회 명령을 Lab 08에 추가했습니다.
- **새 세션과 새 대화 구분:** 원격 `--new-session` 호출에서도 이전 conversation ID가 재사용됐습니다.
  독립 확인 명령은 `--new-session --new-conversation`을 함께 사용하도록 보완했습니다.
- **TLS 타임아웃:** 첫 azd 초기화는 Microsoft 로그인 서버 연결 타임아웃으로 실패했습니다.
  인증과 AAD discovery HTTP 200을 확인하고 동일 명령 재시도에 성공했습니다. 인증서 검증을 끄거나 endpoint를 바꾸지 않았습니다.
- **영상 링크:** MP4 링크는 파일 보기 링크이고 GitHub Markdown은 이를 내장 플레이어로 바꾸지 않았습니다.
  별도 GitHub 업로드 승인은 없으므로 기존 파일을 보존하고, 로컬에서 검증·재생·구간 탐색하는
  [플레이어 실행 방법](../video-summary.md#재생하기)을 추가했습니다.

새 원시 응답·명령·실패 기록은 Git에서 제외된 `outputs/guide-check-20260914/`에 보존합니다.
GitHub 브라우저의 비공개 문서 접근은 별도 로그인 대기 상태이므로 로그인 후 GitHub 내장 재생 검증 완료를 주장하지 않습니다.
보완 후 오프라인 **55개**·설치 SDK **7개**, Ruff·format·Python compile·문서 검사를 통과했습니다.
새 플레이어의 가이드 링크 두 개는 실제 headless 브라우저에서 열어 시작·50%·90% 위치의 재생과 탐색을 확인했습니다.
이번 검증용 에이전트·평가·Search 객체는 제거하고 원본 응답·정리 기록은 보존했습니다.

## 로컬 검사와 실제 Azure 실행

| 구분 | 확인 결과 |
|---|---|
| 오프라인 단위·계약 검사 | 51개. JSON·오류 분모·hash·holdout·검색·패키징·영상 분할 |
| 설치 SDK 계약 검사 | 7개. MockTransport 기반 직렬화·workflow·MCP·hosting 계약이며 Azure 품질 점수가 아님 |
| 정적 검사 | Ruff, format, Python compile, SDK import/version, `pip check` |
| 문서 검사 | 로컬 링크·이미지·실행 예제 인자 |
| 실제 모델·Prompt Agent | 새 Luna 모델, SDK agent v1, 포털 agent v2의 실제 응답 |
| MAF / Search / IQ | 함수·MCP·세 워크플로, 합성 6건과 GA IQ retrieval |
| File Search | 합성 6파일 색인 완료, 실제 검색 호출과 파일 인용 3개 |
| dev / holdout | v1 6/6, v2 6/6, 고정 후보 holdout 4/4. 오류·누락을 분모에서 제외하지 않음 |
| native judge | 별도 Luna 배포. groundedness 5/6, relevance 5/6 |
| Hosted v1 | 실제 로컬·원격 응답. 별도로 생성한 원격 dev 응답 6건을 rubric으로 평가해 6/6 |
| Trace | 원격 호출과 같은 ID. 포털에서 14 spans, chat 1회, 도구 1회, root Completed 확인 |
| 정리 | 이전 전용 자산 18개 정리, 공유 기반 보존, 새 Hosted 세션 2개 중지 후 idle |
| 미디어 | 실제 CLI 72단계와 실제 포털 조작. Playwright headless PNG 122개와 원래 속도 영상 2개 |

## 해석상 제한

- 업무 검사, 포털 자연어 응답 관찰, native judge, Hosted rubric은 서로 다른 기준입니다.
- v1과 v2의 작은 dev 점수가 같으므로 개선의 통계적 우월성을 주장하지 않습니다.
- native 실패 D01·D05는 원래 점수와 이유를 보존했습니다. holdout을 개발·회귀 수집에 재사용하지 않았습니다.
- Hosted rubric의 임계값은 0.5입니다. CLI가 기록한 evaluator version selector는 빈 값이며, 조회한 버전 1을 소급해 고정 실행으로 취급하지 않습니다.
- 생성 평가자의 `input_quality` 경고와 SDK의 직렬화·prerelease 경고를 보존했습니다.
- 중지된 session의 `monitor`는 `stream_interrupted`를 반환했습니다. 실제 Trace 확인과 정상적인 live log streaming은 구분합니다.
- `trace_export: not-configured`인 로컬 결과를 Azure trace로 바꾸어 적지 않았습니다.
- Fabric·Work IQ·M365 실제 연결, 외부 Web Search, 다른 모델 A/B, Model Router 호출, fine-tuning, continuous evaluation은 수행하지 않았습니다. Lab 10은 합성 설계 경로입니다.
- 지역 리소스는 Sweden Central에 있지만 모델의 Data Zone Standard 처리 범위는 EU 데이터 존입니다.

## 미디어와 계보

기존 JSON을 페이지별로 재생한 자료 대신 실제 실행 중인 CLI와 실제 포털을 녹화했습니다.
로그인 화면은 제외했고 촬영은 모두 headless입니다. CLI 식별자는 마스킹했으며 포털 자료의 식별정보는 외부 공유 전 검토해야 합니다.
영상 길이·크기·해시와 모든 이미지 목록은 [미디어 메타데이터](../assets/live-20260913-swc/media.json)에 있습니다.

개인 원시 결과는 Git에서 제외된 `outputs/live-20260913-swc/`, `outputs/swc-*-0913/`와
현재 Hosted 소스의 `.foundry/`에 보존합니다.
Hosted 평가의 입력, 전체 출력, evaluator 정의, 실제 target response/trace ID를 함께 저장했습니다.
상세 CLI/포털 녹화 기록과 이전 실행·구버전 패키지는
`outputs/archive/20260913-history.tar.gz` 한 파일로 통합하고 원본 해시를 확인했습니다.
현재 평가 세트와 응답은 원래 경로에 유지하며, 최종 PNG와 일치하는 `outputs`의 중복 캡처만 삭제했습니다.
디렉토리별 보존 기준은 [로컬 정리 기준](cleanup.md)에 있습니다.
`.agentignore`는 `.foundry/`, `eval*.yaml`과 평가 데이터를 제외해 재배포 시 정답이 에이전트 코드에 섞이지 않게 합니다.
이전 캡처·영상과 불필요한 생성물을 정리했지만 Git 이력은 재작성하지 않았습니다.
개인 원시 실행 자료와 로컬 환경 설정은 Git에 추가하지 않습니다.

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
원격 GitHub Actions 실행 결과는 이번 검증 결과로 주장하지 않습니다.
