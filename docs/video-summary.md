# 새 실습의 액션별 영상

[실습 경로](paths.md) · [236개 액션과 화면](action-captures.md) · [실제 결과·한계](live-run.md)

**2026-09-14 새 Azure 환경에서 처음부터 다시 촬영했습니다.**
실습 순서 통합본은 **23분 35초**입니다. 개별 영상은 CLI **14분 02초**, 포털 **9분 09초**입니다.
아래 영상과 액션 인덱스의 이미지는 모두 이 촬영본입니다.
명령 입력·생성·설정·저장·질문·응답·오류 확인을 남기고 긴 대기를 제거했습니다.
남긴 구간은 원래 속도이며, 스크린샷을 이어 붙인 영상이 아닙니다.

## 실습 가이드 순서 통합본

CLI와 포털을 **Lab 00 → 11 순서로 교차 편집**했습니다. 각 랩의 시작에는 제목 화면이 나오며
포털 조작·CLI 실행·결과 확인을 같은 장에서 볼 수 있습니다.
단순히 CLI 전체 뒤에 포털 전체를 붙인 영상이 아닙니다.

**[통합본 MP4 다운로드](assets/live-20260914-action/guide-walkthrough.mp4)** ·
**[12개 챕터 목차](video-chapters.md)**

통합본은 아직 별도 GitHub 첨부로 업로드하지 않았으며 **파일·로컬 재생용**입니다.
아래의 기존 CLI/포털 GitHub 재생 링크는 그대로 사용할 수 있습니다.
통합본을 로컬 재생기로 열면 기본 선택되며 **이동할 실습**에서 챕터를 고를 수 있습니다.

두 개별 편집본의 **모든 장면과 236개 액션**을 남겼고, 원래 속도를 유지했습니다.
추가된 24초는 12개 챕터의 제목 화면입니다. 이는 새 Azure 실행이나 원본 작업 시각 순서가 아니라
**가이드를 따라 보기 위한 재배치**입니다. 강사가 준비한 환경을 전제로 보며,
File Search·SDK·Hosted의 다른 에이전트/버전과 평가 기준을 같은 것으로 합치지 않습니다.

## 재생하기

**아래 링크를 클릭하거나 내장 플레이어의 ▶ 버튼을 누르면 재생됩니다.**
저장소 다운로드나 로컬 서버 실행은 필요 없습니다.
비공개 저장소이므로 **이 저장소에 접근 가능한 GitHub 계정으로 로그인**한 상태에서 이용하세요.
Azure 로그인과는 별개입니다.

**[CLI 재생](https://github.com/user-attachments/assets/1e2eb2ac-a164-4c67-8d4f-95cec33e2a3a)** ·
**[포털 재생](https://github.com/user-attachments/assets/714599fe-744d-40e2-a945-c4919d0fb0b3)**

### CLI 실행 영상 — 14분 02초

https://github.com/user-attachments/assets/1e2eb2ac-a164-4c67-8d4f-95cec33e2a3a

### Foundry 포털 영상 — 9분 09초

https://github.com/user-attachments/assets/714599fe-744d-40e2-a945-c4919d0fb0b3

두 첨부파일은 **2026-09-14 최신 편집 영상과 같은 바이트**입니다.
예전 녹화나 편집 전 source 영상으로 연결하지 않습니다.

## 선택: 로컬 재생과 시각별 이동

이미 저장소를 내려받았거나 액션별 시각으로 정확히 이동하려면 다음 재생기를 사용할 수 있습니다.
**위 GitHub 영상 재생에는 이 명령이 필요 없습니다.** 로컬 재생기는 Azure 호출·로그인·업로드를 하지 않습니다.

```bash
python scripts/play_recordings.py
```

[통합본 로컬 재생](http://127.0.0.1:8765/?video=guide-walkthrough.mp4) ·
[CLI 로컬 재생](http://127.0.0.1:8765/?video=cli-edited.mp4) ·
[포털 로컬 재생](http://127.0.0.1:8765/?video=portal-edited.mp4)

[액션 인덱스](action-captures.md)의 로컬 시각 링크는 통합본의 해당 액션으로 이동합니다.
서버 실행 후 **이동할 실습**에서도 Lab 00–11을 선택할 수 있습니다.
끝나면 `Ctrl+C`로 종료하고, 포트 충돌 시 `python scripts/play_recordings.py --port 8766`으로 바꿉니다.
아래 MP4 링크는 다운로드용이며 위의 GitHub 재생 링크와 구분합니다.

| 영상 | 길이 | 파일 |
|---|---|---|
| 실습 순서 통합본 · CLI/포털 교차 편집 | 23분 35초 · 74.5 MB | [MP4 다운로드](assets/live-20260914-action/guide-walkthrough.mp4) |
| CLI · 실제 Bash PTY, 두 터미널 포함 | 14분 02초 · 54.8 MB | [MP4 다운로드](assets/live-20260914-action/cli-edited.mp4) |
| 실제 Foundry 포털 | 9분 09초 · 12.4 MB | [MP4 다운로드](assets/live-20260914-action/portal-edited.mp4) |

## 무엇을 볼 수 있나요?

CLI는 새 그룹·모델 준비, 설치, offline/live 구분, SDK·MAF·MCP·세 워크플로,
Search/IQ, 전체 dev/native/Hosted 평가, 최종 인수와 세션 정리를 담습니다.
포털은 에이전트 생성과 모델 선택부터 지침·문서 입력·버전 저장, 질문마다 새 대화,
File Search 업로드/색인, 평가 실패 행과 실제 Trace의 오류까지 담습니다.

**131개 CLI 액션과 105개 포털 액션의 화면 경계를 유지**했습니다.
원본 캡처 1,500회 중 의미 있는 1,065회를 연결하며, 동일 이미지를 공유해
898개 lossless WebP로 제공합니다. 중간 과정은 [전체 액션 인덱스](action-captures.md)에서 찾습니다.

## 편집과 해석

- 본문 장면은 실제 원본 영상 구간입니다. 통합본의 제목 화면은 별도로 표시했으며,
  모델 응답·평가 점수·실패를 바꾸지 않았습니다.
- 개별 영상은 각 원본 안의 순서를 유지했습니다. 통합본은 가이드 순서로 재배치했으며
  로컬 Hosted의 두 터미널은 해당 절 안에서 실제 시각 순서로 교차 편집했습니다.
- 영상 길이는 모델 지연이나 배포 소요시간이 아닙니다. 필요하면 정지해 명령과 결과를 읽으세요.
- 촬영 보조 `RUN_TOOLS` 명령은 강사 준비용입니다. 학습자가 실행할 명령은 해당 랩에 있습니다.
- 로그인·PIN·MFA는 촬영하지 않았습니다. 실습 리소스 식별정보는 외부 공유 전 검토하세요.

[파일·해시](assets/live-20260914-action/media.json) ·
[원본/편집 프레임 대응](assets/live-20260914-action/edit-timeline.json) ·
[통합본 프레임·챕터 대응](assets/live-20260914-action/combined-timeline.json) ·
[재생 게시 상태](assets/live-20260914-action/github-playback.json)
