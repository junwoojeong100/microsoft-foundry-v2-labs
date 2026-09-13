# 실제 실행 · 주요 화면 · headless 녹화

**2026-09-13에 요청 계정으로 핵심 실습을 직접 실행했습니다.**
아래 결과는 offline fixture가 아니라 실제 Foundry 모델·서비스 응답입니다.
로그인 후 별도 **headless Edge / Playwright** 컨텍스트에서 포털과 실제 CLI 로그 화면을 녹화했습니다.

## 녹화 보기

- **[20분 배속본 바로 재생](video-summary.md)** — GitHub 동영상 플레이어로 열립니다.
- **[111분 전체본 — 구간별 재생·다운로드](video-chapters.md)** — 실습 영역별 12개 파일, 각 100 MB 미만입니다.
- 단일 파일 전체본은 로컬 `outputs/live-20260913/full-headless-redacted.mp4`에도 보존했습니다.
  영상은 이 비공개 리포에 연결된 첨부파일로 제공하며, GitHub 로그인과 리포 접근 권한이 필요합니다.
- [녹화 구성 정보](assets/live-20260913/recording.json)

인증·패스키 화면은 녹화하지 않았습니다. 계정 이름·이메일·구독 식별자는 가렸습니다.
CLI 장면은 **실제 명령의 로그를 브라우저로 표시한 화면**이며, Foundry 포털을 모사한 화면이 아닙니다.
실패·진단·재시도도 기록에 남겼으며, 배속본을 실제 소요 시간으로 해석하면 안 됩니다.
전체본의 구간 분할은 대기시간을 제거하거나 내용을 생략한 편집이 아닙니다.
이전 MP4 파일 조회 링크는 실제 플레이어로 렌더링되는 재생 페이지로 교체했습니다.

| 내용 | 전체본 위치 | 배속본 위치 |
|---|---:|---:|
| Foundry 시작과 새 경험 | 01:00 | 00:11 |
| 실제 CLI 환경·모델 확인 | 11:27 | 02:04 |
| 모델 Playground 응답 | 14:08 | 02:33 |
| Prompt Agent와 근거·보류 응답 | 18:12 | 03:17 |
| MAF 함수·MCP·3종 workflow | 23:48 | 04:17 |
| Search와 Foundry IQ | 44:53 | 08:05 |
| 별도 judge 배포·dev/holdout·Foundry 평가 | 59:27 | 10:43 |
| Hosted Agent 패키징·배포 | 1:29:24 | 16:06 |
| 실제 Hosted Trace·Monitor | 1:41:18 | 18:15 |
| 실습 세션 중지·인수 확인 | 1:48:07 | 19:29 |

## 실제 결과

**[전체 캡처 41장 파일 목록](assets/live-20260913/)** — 아래와 각 랩 본문에는 주요 장면을 연결했습니다.

같은 합성 규정과 dev 6문항을 사용했습니다. target은 `gpt-5.4-mini`,
별도 cloud judge는 `gpt-5.4`입니다. 기존 실습용 프로젝트·모델·Search 서비스를
재사용하고, 이번 실행의 새 자산에는 `mfv2-live-20260913` 접두사를 사용했습니다.

| 실행 | 실제 결과 | 해석 |
|---|---|---|
| v1 baseline | **4/6** | 승인 필요 문장과 구조화 `decision`이 불일치한 사례 2건 |
| 최초 v2 candidate | **5/6** | 실제 검색 결과에 없는 문서 ID를 인용한 사례 1건 |
| 인용 규칙을 보강한 v2 | **6/6** | 실제 반환된 문서 ID만 인용하도록 개선 |
| 고정 후보의 미사용 holdout | **4/4** | 후보 고정 후 별도 사례로 확인 |
| Foundry `groundedness` | **6/6 통과** | 별도 GPT-5.4 judge의 native 결과 |
| Foundry `relevance` | **6/6 통과** | 업무 검사와 별개의 native 결과 |
| Hosted Agent | **버전 1 배포·원격 응답 성공** | `needs_approval`, 150000원, 실제 정책 ID 반환 |
| Hosted Trace | **같은 Trace ID 확인** | 20 spans, 모델 2회·도구 1회, root Completed |

![Foundry에서 확인한 실제 평가 결과](assets/live-20260913/32-foundry-evaluation-metrics.png)

평가 데이터나 채점 기준을 바꾸지 않았고, 실패한 행을 분모에서 빼지 않았습니다.
전후 dev의 `changed_context_cases`는 빈 목록이었습니다.
이 작은 사례 수로 모델 우월성이나 운영 SLA를 주장하지 않습니다.
Hosted smoke test는 프로젝트 Responses + IQ 평가와 다른 경로이므로
위 dev/holdout 점수를 Hosted 버전의 품질 점수로 재사용하지 않습니다.

## 실행하면서 수정한 부분

| 발견한 문제 | 반영한 수정 |
|---|---|
| 기본 CLI 계정이 요청 계정과 다름 | 구독에 인증을 고정하고 tenant를 검증; 기본 구독은 변경하지 않음 |
| 녹화용 하위 프로세스가 전역 Python을 사용 | 프로젝트 `.venv/bin/python` 경로를 명시적으로 사용 |
| MCP 지침에 답변 schema 누락 | 함수/MCP에 같은 schema 전달, 실제 반환 JSON 검사 |
| Group Chat에 종료 안내만 반환 | 참여자 응답을 명시적으로 수집; 최대 3라운드는 유지 |
| IQ GA에서 작은 출력 한도 거부 | 서비스가 요구한 5000 초과 조건에 맞춰 6000 사용 |
| 검색되지 않은 문서를 인용 | 실제 입력 문서 목록의 ID만 사용하도록 v2 지침 강화 |
| HTTPX 오류에 HTTP 상태가 누락 | 실제 response status를 표시하고 선택적 debug 진단 제공 |

![MCP 실제 실행 결과](assets/live-20260913/16-maf-mcp-response.png)

## 포털과 GA IQ 계약의 차이

GA API로 만든 knowledge base는 정상 검색되었지만, 포털의 Preview 편집 화면은
별도 chat model을 필수로 표시했습니다. 이 화면에서 **Save를 눌러 GA 구성을
Preview 설정으로 바꾸지 않았습니다.** 실제 API 응답의 references·activity를 확인했습니다.

![정상 검색된 GA knowledge base의 포털 편집 경고](assets/live-20260913/24-knowledge-base-detail.png)

요청에 planner 모델을 지정하지 않았어도 실제 activity에 `agenticReasoning` 및
reasoning token 항목이 나타났습니다. 서비스 내부 처리나 요금을 0으로 단정하지 않습니다.

## 운영 확인과 남겨 둔 자산

![실제 Hosted Agent 도구 호출 Trace](assets/live-20260913/39-hosted-tool-trace.png)

포털 Trace에서 CLI가 반환한 같은 ID를 찾고 `lookup_policy` 호출을 확인했습니다.
root는 Completed였으나 내부 storage 조회 span 2개가 실패로 표시되었습니다.
이를 숨기거나 “모든 span 오류 0”으로 보고하지 않습니다.
Monitor의 `$0` 표시는 화면의 반올림/추정값이며 무료 실행의 증거가 아닙니다.

실습의 **로컬 서버는 종료**했고, 새 Hosted session은 중지 후 **`idle`** 상태를 확인했습니다.
기존 사용자의 자원은 수정·삭제하지 않았습니다.
검토와 재현을 위해 다음 새 자산은 남겨 두었습니다.

- Prompt Agent `mfv2-live-20260913-policy`
- Hosted Agent `mfv2-live-20260913-hosted`, 버전 1
- judge 배포 `mfv2-live-20260913-judge` — GPT-5.4, Data Zone Standard, 50K TPM
- 해당 접두사의 Search index / knowledge source / knowledge base
- 이번 Foundry evaluation 결과

중지한 session의 파일시스템과 별도 서비스 비용은 남을 수 있습니다.
완전히 제거할 때는 [정리 가이드](reference/cleanup.md)에서 소유권을 확인합니다.
공유 Resource Group 전체를 삭제하지 않습니다.

## 수행하지 않은 선택 확장

실제 Fabric/Work IQ·Microsoft 365 데이터 연결, 외부 Web Search, File Search 업로드,
추가 모델 A/B 비교, 자동 trace-to-dataset, 자동 Hosted 평가 suite 생성,
continuous evaluation 및 fine-tuning은 이번 실행에 포함하지 않았습니다.
기본 도구에 표시된 Web Search도 요청 전에 제거했습니다.
이 기능들을 수행한 것처럼 캡처나 결과를 만들지 않았습니다.

재현·검증 명령과 SDK 조합은 [검증 기록](reference/validation.md)과
[버전 기준](reference/versions.md)에 있습니다.
