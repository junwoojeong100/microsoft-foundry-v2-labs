# Sweden Central — Playwright headless 실시간 녹화

[실제 실행 결과](live-run.md) · [단계별 캡처](video-chapters.md)

## 재생하기

**아래 GitHub 동영상 플레이어에서 ▶ 버튼을 누르면 재생됩니다. 별도 로컬 서버는 필요 없습니다.**
비공개 저장소에 접근 가능한 GitHub 계정으로 로그인하세요.

### CLI 전체 영상 — 95분 50초 · 87.9 MB

https://github.com/user-attachments/assets/75dd6df4-c615-4c28-8621-8a416ea31cbe

### Foundry 포털 전체 영상 — 82분 16초 · 35.1 MB

https://github.com/user-attachments/assets/19b9097b-a4e9-41ad-9cc6-ddab5a1e5f14

기존 파일 보기 링크 대신 같은 저장소에 연결된 동영상 첨부 URL을 사용합니다.
새로 녹화하거나 재인코딩하지 않고 기존 MP4를 그대로 올렸습니다.
[첨부 URL·원본 해시](assets/live-20260913-swc/github-playback.json)에서 동일성을 확인할 수 있습니다.

## 선택: 로컬에서 재생하기

저장소를 내려받은 뒤 루트 터미널에서 다음을 실행하세요. Python 표준 라이브러리만 사용하며 Azure 호출·업로드는 없습니다.

```bash
python scripts/play_recordings.py
```

서버가 실행된 상태에서 **[CLI 영상 재생](http://127.0.0.1:8765/?video=cli-full-run.mp4)** 또는
**[포털 영상 재생](http://127.0.0.1:8765/?video=portal-full-run.mp4)**을 엽니다.
재생 버튼·구간 탐색·브라우저의 속도 조절을 사용할 수 있습니다. 끝나면 터미널에서 `Ctrl+C`로 종료합니다.
8765 포트가 사용 중이면 `python scripts/play_recordings.py --port 8766`을 실행하고 출력된 주소를 엽니다.
서버는 `127.0.0.1`에만 연결되며 검증된 영상 두 개와 플레이어만 제공합니다. `.env`나 `outputs`는 노출하지 않습니다.

## GitHub 파일 보기·다운로드

| 파일 링크 | 내용 |
|---|---|
| [CLI MP4 파일](assets/live-20260913-swc/cli-full-run.mp4) | **95분 50초 · 87.9 MB · 1440×900**, 같은 그룹명 재생성부터 세션 확인까지 실제 72단계 |
| [Foundry 포털 MP4 파일](assets/live-20260913-swc/portal-full-run.mp4) | **82분 16초 · 35.1 MB · 1440×1000**, 실제 모델·에이전트·평가·Trace·Knowledge |

두 영상은 **원래 속도이며 대기시간을 제거하지 않았습니다.**
Playwright headless context의 실제 화면을 실행 중에 녹화했고, H.264 MP4로 인코딩했습니다.
이전의 JSON 결과 재생 영상을 새 실측 영상으로 재사용하지 않았습니다.
인증용 창의 로그인·MFA 과정은 제외했으며 모든 PNG·실습 녹화는 headless에서 생성했습니다.

길이·크기·해시·촬영 방식은 [미디어 메타데이터](assets/live-20260913-swc/media.json)에 있습니다.
포털 자료에는 실습 계정과 리소스 식별정보가 보일 수 있습니다. 외부 게시 전 확인하세요.
원본은 이 저장소의 `assets`에 보존하고, GitHub 재생에는 같은 비공개 저장소의 동영상 첨부파일을 사용합니다.
다른 저장소나 외부 영상 사이트에는 업로드하지 않았습니다.
