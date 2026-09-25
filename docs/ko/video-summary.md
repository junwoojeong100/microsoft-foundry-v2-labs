# gpt-6-sol 실습 녹화 — 2026-09-24

[English](../video-summary.md) | **한국어**

**2026-09-24 새 국문 녹화입니다.** Sweden Central 실습 프로젝트에서 `gpt-6-sol` / `2026-09-22`로 Lab 00–09·11의 A(포털)·B(CLI) 주요 단계와 선택 Foundry 평가 단계(포털 평가, 추적 평가, 업무 기준을 포함한 cloud judge와 **실행 비교**, MAF 도구 호출 채점)를 실제로 실행했습니다. 모든 judge는 별도 `gpt-6-sol-judge` 배포를 사용했습니다. 영문 화면에 자막을 붙인 영상이 아니며 국문 지침·정책·평가 데이터와 별도 브라우저 세션으로 촬영했습니다.

| 영상 | 길이 | 파일 |
|---|---:|---|
| Lab 00–09·11 가이드 순서 통합본 | 06:03 | [guide-ordered.mp4](../assets/g6sol-20260924-ko/guide-ordered.mp4) |
| B · CLI 실행 | 02:57 | [cli-edited.mp4](../assets/g6sol-20260924-ko/cli-edited.mp4) |
| A · Foundry 포털 | 02:43 | [portal-edited.mp4](../assets/g6sol-20260924-ko/portal-edited.mp4) |

**액션 91개, 무손실 화면 272장입니다.** 실제 원본 구간을 1배속으로 이어 대기 시간만 줄였고, 제목 카드는 앱 화면과 구분합니다. 이어 붙인 244개 구간을 모두 원본 프레임과 대조했습니다(최소 SSIM 0.9923).

**로컬 재생과 챕터 이동을 확인했습니다. GitHub에 영상을 업로드하지 않았습니다.** 저장소를 받은 뒤 검증된 파일만 localhost에서 재생합니다.

```bash
python scripts/play_recordings.py --edition ko
```

## 녹화한 범위

- **Lab 00:** 오프라인 doctor, v1/v2 fixture(모델 응답 아님), 가상환경, 설정 카드로 채운 `.env`, 읽기 전용 사전 확인.
- **Lab 01–02:** 프로젝트·계정 endpoint 구분, 배포 목록, Web search를 제거한 Playground 답변 2건, 첫 SDK 요청과 검증된 구조화 답변.
- **Lab 03:** 포털 agent(저장 버전 2)의 D01/D02/D03/D05 답변, 선택 SDK prompt agent 버전 1.
- **Lab 04–06:** 도구 없는 MAF·함수 도구·로컬 MCP, 선택 `maf-evaluate`(tool_call_accuracy 5/6, relevance 5/6), 순차·병렬·제한된 Group Chat workflow, 로컬 검색·소유 Search index·GA Foundry IQ knowledge base와 IQ 근거 답변.
- **Lab 07:** dev baseline v1 6/6, candidate v2 6/6, 고정한 후보의 holdout 1회 4/4, 인수 판단 `ready-for-human-review`, 근거 없음 진단 0/6·오류 0, cloud judge groundedness 6/6·relevance 5/6(실패: D05), 업무 기준 일치 6/6·6/6과 **실행 비교**, 포털 D01–D06과 포털 평가(Relevance 6/6, Coherence 6/6, TaskAdherence 0/6).
- **Lab 08–11:** Hosted bundle 패키징만, agent 세부 정보·추적·모니터링 탭, 기록한 대화의 추적 평가(Relevance 15/15, Coherence 15/15, TaskAdherence 15/15), 소유 자산 정리 목록(삭제 없음), 인계 요약.

## 이번 녹화에 포함하지 않은 것

Lab 10, 선택 IQ Chat preset(`gpt-5.6-luna`; Search가 GPT-6 모델을 받지 않음), Lab 03 포털 File Search, Lab 06 하이브리드 RAG, Lab 08 로컬·원격 Hosted 실행, Lab 09 되풀이 평가, 심화 C 경로와 확장 모듈은 **이번 녹화에 포함하지 않았습니다.** Lab 09 B 서버 측 추적 검색은 [2026-09-25 보충 녹화](#review-refresh-supplement)에 있습니다. 대화 평가 모듈, 되풀이 평가, Agent Optimizer, 클라우드 red teaming, CI 릴리스는 2026-09-23에 별도로 실행했습니다([결과](live-run.md#이전에-실행하지-않은-항목--2026-09-23), 대화 평가: [검증 기록](reference/validation.md#foundry-evaluation-additions)). 이전 녹화는 삭제했으며 이번 판의 근거로 쓰지 않습니다.

인증·암호·MFA 입력은 녹화하지 않았습니다. 기록된 종료 코드는 품질 점수가 아니며 어떤 결과도 운영 승인이 아닙니다. 본인의 리소스 이름·버전·결과를 사용합니다.

<a id="review-refresh-supplement"></a>

## 검토 반영 보충 녹화 — 2026-09-25

**2026-09-24 검토에서 핵심으로 추가한 단계의 짧은 국문 영상 2개입니다.** 같은 프로젝트, `gpt-6-sol` / `2026-09-22`, 소스 commit `f990af3`에서 새 agent 버전 1개와 모델 호출 1회를 사용했습니다. 바뀌지 않은 단계는 2026-09-24 영상을 그대로 참고합니다.

**이후 가이드 변경(2026-09-25):** [Lab 03 B 호출 블록](labs/03-prompt-agent.md#sdk-invoke-recording-scope)은
이제 저장된 이름·버전을 모두 입력받고 빈 값을 거절합니다. 이 영상은 이전 입력 방식이며, 오프라인으로 확인한 재개 변경의 근거가 아닙니다.

| 영상 | 길이 | 파일 |
|---|---:|---|
| B · Lab 03 `--output` 생성과 호출(실제 zsh 터미널) | 00:57 | [ko-terminal.mp4](../assets/review-refresh-20260925/ko-terminal.mp4) |
| Lab 03 B 포털 확인 · Lab 09 B `response_id` 추적 검색 | 01:07 | [ko-portal.mp4](../assets/review-refresh-20260925/ko-portal.mp4) |

두 영상 모두 1배속입니다. 터미널 영상은 동작 앞뒤의 대기 시간만 잘랐고 포털 영상은 자르지 않았습니다. 무손실 화면 6장은 [Lab 03 B](labs/03-prompt-agent.md#path-b)와 [Lab 09 B](labs/09-operations.md#path-b)에 있습니다.
[captures.json](../assets/review-refresh-20260925/captures.json)에 hash, ID, 확인 결과를 기록했습니다. 영문 첫 시도 하나는 터미널에 로컬 홈 디렉터리 경로가 보여 폐기했고, 그 시도의 결과물은 공개하지 않았으며 해당 agent는 2026-09-25에 삭제했습니다.

**영상** · [액션과 화면](action-captures.md) · [챕터](video-chapters.md) · [실제 결과](live-run.md) · [모델 선택](reference/model-choice.md)
