# 전체 녹화 — 실습 구간별 재생

**약 111분의 전체 과정을 12개 파일로 나눴습니다. 모든 파일은 100 MB 미만입니다.**

[20분 배속본 재생](video-summary.md) · [실제 실행 결과](live-run.md)

필요한 구간의 **재생**을 선택하면 해당 영상만 플레이어로 열립니다. 영상은 같은 비공개 리포에 연결된 GitHub 동영상 첨부파일이며, 접근 권한이 있는 계정으로 로그인해야 합니다.

| 구간 | 내용 | 전체본 위치 | 길이 | 파일 크기 | 링크 |
|---|---|---|---:|---:|---|
| 01 | Foundry 시작과 새 경험 | 00:00–11:29 | 11:29 | 60.0 MB | [재생](videos/chapter-01.md) · [다운로드](https://github.com/user-attachments/assets/880b2bc7-9ab8-44a2-8171-1394cd81865a) |
| 02 | 실제 CLI 환경·모델 확인 | 11:29–14:08 | 02:40 | 14.0 MB | [재생](videos/chapter-02.md) · [다운로드](https://github.com/user-attachments/assets/f55a0dba-f27f-49f2-a1b3-fe47770d8a6e) |
| 03 | 모델 Playground | 14:08–18:13 | 04:05 | 18.4 MB | [재생](videos/chapter-03.md) · [다운로드](https://github.com/user-attachments/assets/54d1dec9-adb0-4918-b28b-43c2f7f8965e) |
| 04 | Prompt Agent | 18:13–23:49 | 05:36 | 31.6 MB | [재생](videos/chapter-04.md) · [다운로드](https://github.com/user-attachments/assets/7fbf5191-7c6d-451e-9e1b-d03ad826b349) |
| 05 1/2 | MAF 함수·MCP·워크플로 | 23:49–35:42 | 11:53 | 56.3 MB | [재생](videos/chapter-05-part-01.md) · [다운로드](https://github.com/user-attachments/assets/027e52ff-1df4-48d6-b55a-e939b3757e30) |
| 05 2/2 | MAF 함수·MCP·워크플로 | 35:42–44:54 | 09:12 | 56.2 MB | [재생](videos/chapter-05-part-02.md) · [다운로드](https://github.com/user-attachments/assets/fade4ec7-bab9-412f-9cc9-6f048c6245a3) |
| 06 | Search·Foundry IQ | 44:54–59:28 | 14:34 | 71.0 MB | [재생](videos/chapter-06.md) · [다운로드](https://github.com/user-attachments/assets/560f6f7c-fc28-4197-8396-67842eeaeb40) |
| 07 1/2 | 실제 평가 | 59:28–1:14:49 | 15:22 | 81.2 MB | [재생](videos/chapter-07-part-01.md) · [다운로드](https://github.com/user-attachments/assets/0f3d6291-d57d-42b3-987b-2ee5075bb8d9) |
| 07 2/2 | 실제 평가 | 1:14:49–1:29:25 | 14:36 | 81.1 MB | [재생](videos/chapter-07-part-02.md) · [다운로드](https://github.com/user-attachments/assets/ece9b1c6-cb38-4324-b654-b93240d92bb4) |
| 08 | Hosted 배포 | 1:29:25–1:41:19 | 11:54 | 63.0 MB | [재생](videos/chapter-08.md) · [다운로드](https://github.com/user-attachments/assets/f478a5da-ff74-4cbf-a5f9-2990615eaa9d) |
| 09 | Trace·Monitor | 1:41:19–1:48:08 | 06:49 | 35.2 MB | [재생](videos/chapter-09.md) · [다운로드](https://github.com/user-attachments/assets/f9091ea8-8a2b-4f0f-848b-dc11a0533a91) |
| 10 | 세션 중지·인수 확인 | 1:48:08–1:51:02 | 02:53 | 15.1 MB | [재생](videos/chapter-10.md) · [다운로드](https://github.com/user-attachments/assets/c9649f04-935b-44e0-b870-1f1805a8a9ea) |

## 분할 기준

20분본과 12개 구간 모두 실제 headless 브라우저 재생과 중간 지점 탐색을 확인했습니다.
비로그인 접근은 거부되므로, 접근 권한이 있는 GitHub 계정으로 로그인한 뒤 이용하세요.

- 대기시간을 포함한 원래 순서를 유지했습니다. 분할은 총용량을 줄이는 압축 작업이 아닙니다.
- 재인코딩 없이 keyframe 경계에서 나눴으며, 원본과 분할본의 영상 packet 수는 모두 **66,615개**입니다.
- 긴 MAF/평가 구간은 두 파일로 나눴습니다. 가장 큰 파일은 약 **81.2 MB**입니다.
- 영상 본문은 Git 히스토리에 추가하지 않았습니다. 기존에 커밋했던 20분 파일의 과거 이력은 재작성하지 않습니다.
- 로그인 화면 제외와 식별정보 가림은 분할본에도 그대로 유지됩니다.

[파일별 메타데이터·SHA-256](assets/live-20260913/video-parts.json)
