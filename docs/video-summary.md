# 새 실습의 액션별 영상

[실습 경로](paths.md) · [236개 액션과 화면](action-captures.md) · [실제 결과·한계](live-run.md)

**2026-09-14 새 Azure 환경에서 처음부터 다시 촬영했습니다.**
CLI **14분 02초**, 포털 **9분 09초**입니다.
아래 영상과 액션 인덱스의 이미지는 모두 이 촬영본입니다.
명령 입력·생성·설정·저장·질문·응답·오류 확인을 남기고 긴 대기를 제거했습니다.
남긴 구간은 원래 속도이며, 스크린샷을 이어 붙인 영상이 아닙니다.

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

[CLI 로컬 재생](http://127.0.0.1:8765/?video=cli-edited.mp4) ·
[포털 로컬 재생](http://127.0.0.1:8765/?video=portal-edited.mp4)

[액션 인덱스](action-captures.md)의 로컬 시각 링크는 이 서버를 실행한 뒤 이용합니다.
끝나면 `Ctrl+C`로 종료하고, 포트 충돌 시 `python scripts/play_recordings.py --port 8766`으로 바꿉니다.
아래 MP4 링크는 다운로드용이며 위의 GitHub 재생 링크와 구분합니다.

| 영상 | 길이 | 파일 |
|---|---|---|
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

- 실제 원본 영상의 구간만 잘라 연결했습니다. 모델 응답·평가 점수·실패를 바꾸지 않았습니다.
- CLI의 두 터미널은 병행 실행 화면을 교차 편집했으며 각 원본 안의 순서는 유지했습니다.
- 영상 길이는 모델 지연이나 배포 소요시간이 아닙니다. 필요하면 정지해 명령과 결과를 읽으세요.
- 촬영 보조 `RUN_TOOLS` 명령은 강사 준비용입니다. 학습자가 실행할 명령은 해당 랩에 있습니다.
- 로그인·PIN·MFA는 촬영하지 않았습니다. 실습 리소스 식별정보는 외부 공유 전 검토하세요.

[파일·해시](assets/live-20260914-action/media.json) ·
[원본/편집 프레임 대응](assets/live-20260914-action/edit-timeline.json) ·
[재생 게시 상태](assets/live-20260914-action/github-playback.json)
