# 새 Sweden Central 환경의 액션별 실제 실행

[English](../live-run.md) | **한국어**

**새 실행:** [2026-09-15 영문 가이드 촬영 결과](english-recordings.md#실제-결과와-범위).
아래 증거는 2026-09-14 원본 실행의 기록으로 유지합니다.

**2026-09-14, 완전히 새로운 `rg-mfv2-action-swc-20260914`에서 가이드를 다시 실행하고 촬영했습니다.**
지정된 실습 계정으로 실행했으며 기본 Azure CLI 구독은 변경하지 않았습니다.
회사·Microsoft 365 데이터 없이 저장소의 합성 데이터만 사용했습니다.

[영상 재생](video-summary.md) · [236개 액션의 전·후 화면](action-captures.md) ·
[실습별 찾기](video-chapters.md) · [미디어 해시](../assets/live-20260914-action/media.json)

이 가이드의 이미지와 영상은 모두 **2026-09-14 액션별 재촬영 자료**입니다.
사용할 미디어는 `docs/assets/live-20260914-action/` 한 곳에 모았습니다.

## 이번 촬영

| 구분 | 새 결과 |
|---|---|
| CLI | 실제 Bash PTY에서 **131개 액션**, 명령 입력·실행·결과 촬영 |
| 포털 | 실제 `ai.azure.com`의 **105개 액션**, 생성·편집·저장·질문·화면 전환 촬영 |
| 캡처 | 원본 1,500회 중 액션 경계와 의미 있는 변화 1,065회를 보존. 동일 이미지는 공유하여 **898개 lossless WebP**로 제공 |
| CLI 영상 | **14분 02초**, 대기 제거, 실제 원본 구간 1배속 |
| 포털 영상 | **9분 09초**, 대기 제거, 실제 원본 구간 1배속 |
| 실습 순서 통합본 | **23분 35초**, 두 개별 영상의 전체 장면을 Lab 00–11로 재배치. 12개 제목 화면 포함 |
| 촬영 방식 | Playwright 1.62.0 headless Edge. 로그인·PIN·MFA 화면은 제외 |

새 에이전트를 **New agent → Build an agent**로 만드는 과정부터 이름·모델 선택,
기본 Web Search 제거, 지침과 합성 문서 입력, 버전 저장을 각각 촬영했습니다.
각 질문은 새 대화로 실행했습니다. File Search의 파일 선택·업로드·색인 완료,
평가 실패 행, Trace의 하위 오류도 포함합니다.

가이드 순서로 이어 보려면 [통합본과 챕터 목차](video-chapters.md)를 사용합니다.
통합본은 새 실행이 아닌 학습용 순서 편집이며 GitHub에서 바로 재생할 수 있습니다.
CLI·포털 개별 영상도 직접 재생할 수 있습니다.

**아래 GitHub 내장 플레이어에서 바로 재생할 수 있습니다. 로컬 서버는 필요 없습니다.**
비공개 저장소에 접근 가능한 GitHub 계정으로 로그인하세요.
같은 최신 파일의 [직접 재생 링크와 선택적 로컬 재생 방법](video-summary.md#재생하기)을 제공합니다.
촬영 보조 `RUN_TOOLS` 명령은 강사 준비·원문 검증용이며, 학습자는 각 랩에 적힌 명령을 사용합니다.

### 실습 가이드 순서 통합 영상 — 23분 35초

https://github.com/user-attachments/assets/c005e1a6-f577-4d07-b2c3-9a4827750c81

### CLI 실행 영상 — 14분 02초

https://github.com/user-attachments/assets/1e2eb2ac-a164-4c67-8d4f-95cec33e2a3a

### Foundry 포털 영상 — 9분 09초

https://github.com/user-attachments/assets/714599fe-744d-40e2-a945-c4919d0fb0b3

## 환경과 모델

| 항목 | 이번 실행 |
|---|---|
| 리소스 그룹 | `rg-mfv2-action-swc-20260914` |
| Foundry 계정 / 프로젝트 | `ai-mfv2-action-swc-20260914` / `mfv2-action-20260914` |
| Search | `srch-mfv2-action-swc-20260914`, Basic, Entra ID 인증 |
| 관측 | 같은 리전의 Application Insights / Log Analytics, 30일 보존·일일 1GB 제한 |
| 응답 모델 | `gpt-5.6-luna`, `2026-07-09`, Data Zone Standard 100K TPM |
| 별도 judge | `gpt-5.6-luna-judge`, 같은 모델 버전, Data Zone Standard 50K TPM |
| 버전 정책 | 두 배포 모두 `NoAutoUpgrade`, 다른 모델·endpoint로 우회하지 않음 |

Data Zone Standard의 추론 처리 범위는 **EU 데이터 존**입니다.
리소스가 Sweden Central에 있다는 사실을 단일 데이터센터에서만 추론한다는 뜻으로 해석하지 않습니다.
target과 judge도 같은 기반 모델이므로 독립적인 모델 간 검증이 아닙니다.

## 실제 실행 결과

| 경로 | 이번 실행의 증거 |
|---|---|
| 모델 | SDK·포털에서 새 Luna 호출. 근거를 주기 전 숙박비 질문에는 금액을 추측하지 않음 |
| A. 포털 Prompt Agent | `mfv2-action-20260914-portal` **v3**, 인라인 합성 원문. 안내 4문항과 별도 dev 6문항을 각각 새 대화로 실행 |
| SDK Prompt Agent | `mfv2-action-20260914-policy` **v1**, 현행·과거·승인·근거 부족 질문 실행 |
| MAF | 단일·함수·로컬 MCP, A의 현행/과거 순차 실행, B의 순차·병렬·Group Chat 실행 |
| Search / IQ | 합성 6건, 새 index/source/base, GA `2026-04-01` 실제 검색. 포털 관찰 후에도 GA 경로 재확인 |
| File Search | `mfv2-action-20260914-files` **v2**, 인라인 근거 없이 File Search만 사용. 6파일 Completed 및 저장 원문 6개 바이트 일치 확인 |
| v1 / v2 dev | `--retrieval local`을 고정한 새 응답 **6/6 / 6/6**, 수집 오류 0 |
| 교육용 holdout | 고정 후보의 인수 절차 **4/4**. 이미 사용된 공개 교육용 세트이며 새로운 미사용 검증셋이 아님 |
| native judge | groundedness **6/6**, relevance **5/6**, 각 6개 사례를 분모에 유지 |
| Hosted | `mfv2-action-20260914-hosted` **v1**, 새 로컬·원격 응답, 실제 managed identity 실행 |
| Hosted 별도 평가 | 새 원격 응답 **6건**, 생성형 rubric **6/6**. target에 query만 전달됐음을 모든 raw output에서 확인 |
| Lab 10 | 합성 라우팅 설계. 실제 Fabric·Work IQ·Microsoft 365 연결은 하지 않음 |

포털 dev 6문항은 현행 150,000원, 과거 120,000원, 사전 승인, 식비 30,000원,
해외 규정 보류, 규정 무시 요청 거절을 확인했습니다. 이는 assistant의 검토 기록이며
사람의 운영 승인이나 통계적 품질 보증이 아닙니다.
Group Chat도 최대 3라운드 종료이며 실제 예약·승인·지급을 수행하지 않았습니다.

## 실패와 한계도 그대로 보존

- **D05 native relevance 2점:** 해외 규정이 없어 보류한 답변을 “실제 금액을 제시하지 못했다”고 낮게 평가했습니다.
  업무상 올바른 보류와 일반 relevance 기준의 차이입니다. 점수를 바꾸지 않고 dev 검토 대기 기록을 남겼습니다.
- **File Search 원문 열기 UI:** 인용 칩과 본문 번호를 클릭했지만 미리보기나 다운로드가 열리지 않았습니다.
  성공한 것으로 표시하지 않았습니다. 같은 File Search 저장 파일을 SDK로 읽어 6개 모두 합성 원본과 비교했습니다.
  답변을 다시 만들거나 다른 검색 provider로 바꾼 것이 아닙니다.
- **IQ 포털 편집기:** Active인 GA base를 열어도 별도 chat completions model을 요구했습니다.
  Preview 형태로 저장하거나 모델을 추가하지 않았고, GA 호출이 계속 동작함을 재확인했습니다.
- **Hosted evaluator 버전:** 생성된 YAML에는 버전 1이 있지만 실제 run의 version selector는 빈 값이었습니다.
  조회한 catalog v1을 보관하되 버전을 명시적으로 고정해 실행했다고 소급하지 않습니다.
- **작은 평가 집합:** v1과 v2 모두 6/6이므로 우월성을 주장하지 않습니다.
  holdout을 지침 수정이나 회귀 사례 수집에 사용하지 않았습니다.

SDK의 prerelease·직렬화·비영속 실행 경고와 촬영 보조 도구의 재시도도 별도 기록했습니다.
오류·누락 행을 평가 분모에서 빼지 않았습니다.

## 실제 Hosted Trace와 로그

CLI가 반환한 **`e72dc58132dbc461e5fa381c67da3ed9`**를 같은 에이전트의 Traces에서 검색했습니다.
실제 화면은 **20 spans, chat 2회, 도구 1회, 약 7.2초, root Completed**였습니다.

화면의 **2 errors**도 숨기지 않았습니다. 새 상태 저장소와 새 대화 항목의 초기 GET 404이며,
이어진 생성/갱신과 모델·`lookup_policy` 호출은 성공했습니다.
“전체 요청 완료”와 “하위 span 오류 0개”는 같은 말이 아닙니다.

이번에는 원격 호출 **직후** `azd ai agent monitor`를 실행했습니다.
동일 세션의 Running 상태, 두 모델 HTTP 200, 도구 성공, 최종 Responses HTTP 200 로그를 확인했습니다.
SDK의 resilient tasks는 기본 비활성화 상태였으며 durable crash recovery를 검증했다고 주장하지 않습니다.

## 정리와 재현

새 Hosted 세션 2개는 자동 idle 상태에서도 명시적으로 stop하고 다시 조회해 모두 idle임을 확인했습니다.
로컬 서버와 촬영 프로세스도 종료했습니다. 새 그룹은 검토용으로 남겼으므로
**Search·File Search 저장소·로그와 향후 모델 호출 비용은 별도로 남을 수 있습니다.**

실행은 상위 azd 프로젝트가 없는 독립된 폴더에서 수행했습니다.
개인 원시 응답·평가자·설정·정리 증거는 Git에서 제외하며,
[검증 기록](reference/validation.md)과 [액션 인덱스](action-captures.md)에서 확인 범위를 구분합니다.
