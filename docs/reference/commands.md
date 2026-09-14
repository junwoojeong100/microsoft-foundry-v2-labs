# 명령 빠른 참조

**아래 명령은 모두 저장소 루트에서 실행합니다. `.env`를 shell로 `source`하지 않습니다.**
전용 가상환경을 활성화하면 클라우드 명령의 SDK를 사용할 수 있습니다.

| 명령 | Azure / 부작용 | 상세 |
|---|---|---|
| `python scripts/workshop.py doctor` | 없음 | Python·합성 데이터 검사 |
| `doctor --cloud` | 읽기만 | 명시된 구독/tenant/배포/token 확인, 추론 아님 |
| `demo --label demo-v2 --prompt v2` | 없음, 로컬 결과 생성 | 고정 fixture |
| `retrieve --provider local` | 없음 | 로컬 키워드 검색 |
| `retrieve --provider search` | Search 조회 비용 가능 | 일반 검색 |
| `retrieve --provider iq` | IQ 조회 비용 가능 | GA knowledge base |
| `model --question "질문"` | 유료 모델 호출 | 직접 Responses |
| `answer --prompt v2 --retrieval local` | 유료 모델 호출 | 구조화 답변 + 원문 |
| `maf --tools` / `maf --mcp` | 유료 모델 호출 | 읽기 전용 함수 / 로컬 MCP |
| `workflow --pattern sequential` | 유료 모델 호출 | 대안: concurrent, group-chat |
| `seed-search --confirm-create` | 본인 Search 객체 생성/업로드 | 기존 서비스만 사용 |
| `seed-search --iq --confirm-create` | 위 + GA source/base | 소유권 검사 |
| `prompt-agent create ... --confirm-create` | 실제 agent version 생성 | 정확한 접두사 필요 |
| `prompt-agent invoke ... --version ...` | 실제 agent 호출 | 버전 고정 |
| `collect --label baseline --prompt v1` | dev 전체 유료 호출 | 오류 보존, 동시성 1 |
| `evaluate --label baseline` | 없음 | 결정적 업무 검사 |
| `compare --baseline baseline --candidate candidate` | 없음 | 통제된 dev 비교 |
| `feedback --label baseline --case D03 --reason "구체적인 검토 이유"` | 없음, 로컬 검토 기록 | 실제 dev만, 승인 대기 |
| `cloud-evaluate --label candidate --confirm-cost` | 유료 cloud judge | evaluator version·job 이력 |
| `collect --split holdout ... --candidate candidate --unlock-holdout` | 고정 후보의 실제 평가 요청 | 개발용 재사용 금지 |
| `accept --candidate candidate --holdout final-holdout` | 없음 | 사람의 인수 자료, 자동 승인 아님 |
| `serve` | 로컬 서버 시작, 호출 시 유료 모델 | Hosted SDK 필요 |
| `cleanup-plan` | 없음 | 삭제 안 함 |
| `python scripts/export_policy_docs.py` | 없음, 텍스트 6개 생성 | A 경로 강사 배포용 |
| `python scripts/package_hosted.py` | 없음, 패키지 생성 | 배포/설치 실행 안 함 |
| `python scripts/play_recordings.py` | 없음, localhost 영상 서버 | 대기 제거 편집본의 해시 확인 후 재생·구간 탐색 지원. Azure 호출·업로드 없음 |

표에서 생략한 옵션은 실행용 완전한 예제가 아닙니다.
정확한 필수 인자는 `python scripts/workshop.py --help`와 각 하위 명령의 `--help`로 확인합니다.
전체 실행 예는 해당 [실습 모듈](../paths.md)에 있습니다.

로컬 진단에는 명령 앞에 `--debug`를 넣을 수 있습니다.
추가 스택·서비스 오류에는 환경 경로가 포함될 수 있으므로 원시 로그를 공개하지 않습니다.

실행 결과를 바꾸는 명령은 기존 label을 덮어쓰지 않습니다.
점수나 raw 응답을 수정해 hash 검사를 통과시키려 하지 않습니다.
