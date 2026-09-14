# 실습 가이드 순서 통합 영상과 챕터

**2026-09-14 촬영 · 통합본 23분 35초 · Lab 00–11 · 236개 액션**

[통합본 MP4 다운로드](assets/live-20260914-action/guide-walkthrough.mp4) ·
[재생 방법](video-summary.md#실습-가이드-순서-통합본) ·
[액션별 화면·정확한 시각](action-captures.md) · [실제 실행 결과](live-run.md)

통합본은 CLI와 포털의 실제 장면을 **실습 가이드 순서로 교차 편집**한 영상입니다.
제목 화면에서 다음 랩을 확인하고, 같은 장 안에서 조작과 실행 결과를 이어 볼 수 있습니다.
실제 작업 시각 순서는 아니며, 강사가 준비한 환경에서 진행하는 가이드 기준입니다.
서로 다른 에이전트 버전이나 평가 경로를 하나의 실행처럼 해석하지 않습니다.

## 통합본 챕터

아래 시각 링크는 로컬 재생기에서 해당 챕터로 이동합니다.
`python scripts/play_recordings.py` 실행 후 통합본이 기본 선택되며,
플레이어의 **이동할 실습**에서도 같은 12개 챕터를 고를 수 있습니다.
통합본은 아직 별도 GitHub 첨부로 업로드하지 않았습니다.

| 시작 | 실습 | 이어 보는 내용 |
|---|---|---|
| [00:00](http://127.0.0.1:8765/?video=guide-walkthrough.mp4&t=0.00) | [00. 시작](labs/00-start.md) | 포털 프로젝트 선택 → 로컬 설치·설정·점검 |
| [02:37](http://127.0.0.1:8765/?video=guide-walkthrough.mp4&t=157.28) | [01. Foundry](labs/01-foundry.md) | 강사 준비 예시, 리소스·권한·endpoint 구분 |
| [04:02](http://127.0.0.1:8765/?video=guide-walkthrough.mp4&t=242.00) | [02. 모델](labs/02-models.md) | 배포 → 포털 질문 → SDK 호출 |
| [05:39](http://127.0.0.1:8765/?video=guide-walkthrough.mp4&t=339.88) | [03. 에이전트](labs/03-prompt-agent.md) | 생성·지침 저장 → 선택 File Search → 기본 질문 → SDK |
| [10:43](http://127.0.0.1:8765/?video=guide-walkthrough.mp4&t=643.80) | [04. MAF 도구](labs/04-agents-tools.md) | 단일 Agent → 함수 → MCP → 입력 경계 |
| [11:27](http://127.0.0.1:8765/?video=guide-walkthrough.mp4&t=687.24) | [05. 워크플로](labs/05-workflows.md) | A의 현행/과거 순차 예제 → B의 세 패턴 |
| [12:12](http://127.0.0.1:8765/?video=guide-walkthrough.mp4&t=732.12) | [06. Search / IQ](labs/06-knowledge.md) | 포털 관찰 → 실제 Search/IQ 코드와 원문 확인 |
| [13:48](http://127.0.0.1:8765/?video=guide-walkthrough.mp4&t=828.16) | [07. 평가](labs/07-evaluation.md) | 포털 dev → v1/v2 → native 실패 → 고정 후보 인수 절차 |
| [17:05](http://127.0.0.1:8765/?video=guide-walkthrough.mp4&t=1025.80) | [08. Hosted](labs/08-hosted.md) | 패키지·설정 → 두 로컬 터미널 → 원격 배포·별도 평가 |
| [21:19](http://127.0.0.1:8765/?video=guide-walkthrough.mp4&t=1279.28) | [09. 운영](labs/09-operations.md) | 관측 설정·로그 → 같은 Trace → 오류 구분·세션 정리 |
| [23:21](http://127.0.0.1:8765/?video=guide-walkthrough.mp4&t=1401.44) | [10. 확장](labs/10-iq-extensions.md) | 합성 라우팅 설계. 실제 Fabric/Microsoft 365 연결 없음 |
| [23:28](http://127.0.0.1:8765/?video=guide-walkthrough.mp4&t=1408.16) | [11. 인수](labs/11-capstone.md) | 검사 자료와 사람의 운영 승인을 구분 |

## 개별 영상도 유지합니다

CLI **14분 02초**, 포털 **9분 09초**의 [기존 GitHub 플레이어](video-summary.md#재생하기)는
로컬 서버 없이 계속 이용할 수 있습니다. 개별 영상의 파일·URL·원본 순서는 바꾸지 않았습니다.

전체 액션과 실패 기록은 [액션 인덱스](action-captures.md)에 있으며,
두 입력 영상의 모든 프레임을 통합본에 한 번씩 사용한 대응은
[통합 편집 계보](assets/live-20260914-action/combined-timeline.json)에서 확인합니다.
