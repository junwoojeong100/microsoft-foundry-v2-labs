# gpt-6-sol 실습 녹화 — 2026-09-23

[English](../video-summary.md) | **한국어**

**2026-09-23 새 국문 녹화입니다.** 새 Sweden Central 실습 프로젝트에서 `gpt-6-sol` / `2026-09-22`로 Lab 00–09·11의 A(포털)·B(CLI) 주요 단계를 실제로 실행했습니다. 선택 cloud judge는 별도 `gpt-6-sol-judge` 배포를 사용했습니다. 영문 화면에 자막을 붙인 영상이 아니며 국문 지침·정책·평가 데이터와 별도 브라우저 세션으로 촬영했습니다.

| 영상 | 길이 | 파일 |
|---|---:|---|
| Lab 00–11 가이드 순서 통합본 | 04:32 | [guide-ordered.mp4](../assets/g6sol-20260923-ko/guide-ordered.mp4) |
| B · CLI 실행 | 02:27 | [cli-edited.mp4](../assets/g6sol-20260923-ko/cli-edited.mp4) |
| A · Foundry 포털 | 01:43 | [portal-edited.mp4](../assets/g6sol-20260923-ko/portal-edited.mp4) |

**액션 69개, 무손실 화면 207장입니다.** 실제 원본 구간을 1배속으로 이어 대기 시간만 줄였고, 제목 카드는 앱 화면과 구분합니다. 이어 붙인 176개 구간을 모두 원본 프레임과 대조했습니다(최소 SSIM 0.9922).

**로컬 재생과 챕터 이동을 확인했습니다. GitHub에 영상을 업로드하지 않았습니다.** 저장소를 받은 뒤 검증된 파일만 localhost에서 재생합니다.

```bash
python scripts/play_recordings.py --edition ko
```

## 녹화한 범위

- **Lab 00:** 오프라인 doctor, v1/v2 fixture(모델 응답 아님), 가상환경, 설정 카드로 채운 `.env`, 읽기 전용 사전 확인.
- **Lab 01–02:** 프로젝트·계정 endpoint 구분, 배포 목록, Web search를 제거한 Playground 답변 2건, 첫 SDK 요청과 검증된 구조화 답변.
- **Lab 03:** 포털 agent(저장 버전 2)의 D01/D02/D03/D05 답변, 선택 SDK prompt agent 버전 1.
- **Lab 04–06:** 도구 없는 MAF·함수 도구·로컬 MCP, 순차·병렬·제한된 Group Chat workflow, 로컬 검색·소유 Search index·GA Foundry IQ knowledge base와 IQ 근거 답변.
- **Lab 07:** dev baseline v1 6/6, candidate v2 6/6, 고정한 후보의 holdout 1회 4/4, 인수 판단 `ready-for-human-review`, 선택 cloud judge groundedness 6/6·relevance 5/6(D05), 포털 D01–D06.
- **Lab 08–11:** Hosted bundle 패키징만, agent 세부 정보·추적·모니터링 탭, 소유 자산 정리 목록(삭제 없음), 인계 요약.

## 이번 녹화에 포함하지 않은 것

Lab 10, 선택 IQ Chat preset(`gpt-5.6-luna`; Search가 GPT-6 모델을 받지 않음), Lab 03 포털 File Search, Lab 06 하이브리드 RAG, Lab 08 로컬·원격 Hosted 실행, Lab 09 서버 측 tracing·continuous evaluation, 심화 C 경로와 확장 모듈은 **`gpt-6-sol`로 다시 실행하지 않았습니다.** 이전 `gpt-5.6-luna` 녹화는 삭제했으며 이 preset의 근거로 쓰지 않습니다.

인증·암호·MFA 입력은 녹화하지 않았습니다. 기록된 종료 코드는 품질 점수가 아니며 어떤 결과도 운영 승인이 아닙니다. 본인의 리소스 이름·버전·결과를 사용합니다.

[영상](video-summary.md) · [액션과 화면](action-captures.md) · [챕터](video-chapters.md) · [실제 결과](live-run.md) · [모델 선택](reference/model-choice.md)
