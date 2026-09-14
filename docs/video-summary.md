# 핵심 변화만 보는 실습 영상

[실습 경로](paths.md) · [단계별 화면](video-chapters.md) · [실행 결과와 한계](live-run.md)

처음 보는 분은 **포털 3분 30초**, 코드 경로를 따라가는 분은 **CLI 6분 54초** 영상을 참고하세요.
실제 녹화에서 긴 대기·변화 없는 구간을 잘라냈으며, 남긴 조작과 결과는 원래 속도입니다.
**실시간 무편집 영상이 아니며 영상 길이가 모델 응답 속도나 배포 소요시간을 뜻하지 않습니다.**

## 재생하기

아래 GitHub 플레이어의 ▶ 버튼을 누르면 재생됩니다. 로컬 서버는 필요 없습니다.
비공개 저장소에 접근 가능한 GitHub 계정으로 로그인하세요.

### CLI 핵심 실행 — 6분 54초 · 10.1 MB

명령 입력과 결과를 중심으로 줄였으며 **72개 실행 단계의 결과를 모두 유지**했습니다.
native 평가의 실패와 중지된 세션의 monitor 오류도 포함합니다.

https://github.com/user-attachments/assets/7b3f79b1-15ba-4f6a-b0f9-5d144f236da8

### Foundry 포털 핵심 조작 — 3분 30초 · 2.9 MB

모델 선택·Web Search 제거·질문 입력·에이전트 지침·정책 답변·평가·Trace·Knowledge의 변화를 볼 수 있습니다.
원본에서 확인한 주요 화면 17개를 빠뜨리지 않았습니다.

https://github.com/user-attachments/assets/7290586e-628e-4a2f-823d-8a5c0c5a1b3e

## 편집 기준

- 단순 배속이나 스크린샷 재생이 아니라 **실제 원본 동영상 구간을 잘라 연결**했습니다.
- 클릭·입력·페이지 이동과 결과 확인 구간을 남기고, 그 사이의 긴 대기를 제거했습니다.
- 결과를 성공한 것만 고르거나 평가 점수·실패 내용을 바꾸지 않았습니다.
- 필요한 곳에서는 일시 정지하여 명령이나 결과를 읽으세요.
- 원본 시각과 편집 시각의 대응, 프레임 수, 원본 일치도는 [편집 계보](assets/live-20260913-swc/edit-timeline.json)에 있습니다.

## 선택: 로컬 재생·파일 다운로드

저장소를 내려받았다면 다음 명령으로 같은 편집본을 재생할 수 있습니다. Azure 호출·업로드는 없습니다.

```bash
python scripts/play_recordings.py
```

[CLI 로컬 재생](http://127.0.0.1:8765/?video=cli-edited.mp4) ·
[포털 로컬 재생](http://127.0.0.1:8765/?video=portal-edited.mp4)

서버 실행 후 링크를 열고, 끝나면 터미널에서 `Ctrl+C`로 종료합니다.
포트가 사용 중이면 `python scripts/play_recordings.py --port 8766`으로 바꿀 수 있습니다.

[CLI 편집본 파일](assets/live-20260913-swc/cli-edited.mp4) ·
[포털 편집본 파일](assets/live-20260913-swc/portal-edited.mp4) ·
[파일 해시](assets/live-20260913-swc/media.json)

## 참고: 대기시간이 포함된 실시간 원본

전체 경과시간을 검토할 때만 아래 원본을 사용하세요. 가이드의 기본 영상은 위 편집본입니다.

- [CLI 실시간 원본 — 95분 50초](https://github.com/user-attachments/assets/75dd6df4-c615-4c28-8621-8a416ea31cbe)
- [포털 실시간 원본 — 82분 16초](https://github.com/user-attachments/assets/19b9097b-a4e9-41ad-9cc6-ddab5a1e5f14)

원본은 기존 GitHub 첨부와 Git 이력으로 보존하고 큰 MP4 중복본은 현재 트리에서 제거했습니다.
실습 계정·리소스 식별정보가 포함될 수 있으므로 외부 공유 전 검토하세요.
