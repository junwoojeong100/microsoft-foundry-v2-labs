# 이 에디션의 검증 기록

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

[프레임 대응과 비교 결과](../assets/live-20260914-action/edit-timeline.json) ·
[미디어 해시](../assets/live-20260914-action/media.json)

새 영상 파일과 가이드를 저장소에 반영하는 것과 GitHub 내장 플레이어용 첨부 업로드는 별개입니다.
새 동영상 첨부는 아직 업로드하지 않았으며, 로컬 재생 확인을 GitHub 첨부 재생 확인으로 표시하지 않습니다.

## 재검증 명령

이번 변경에서 오프라인 **56개**, 설치 SDK 계약 **7개**, Ruff·format·Python compilation,
SDK 버전·의존성 검사를 통과했습니다. 문서 **31개**, 로컬 링크 **1,268개**,
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
