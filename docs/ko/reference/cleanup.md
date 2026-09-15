# 실습 정리: 공유 자산을 지우지 않기

[English](../../reference/cleanup.md) | **한국어**

**삭제보다 먼저 “누가 만든 어떤 자산인가”를 확인합니다.**
이 저장소는 Azure 리소스/권한을 자동 삭제하지 않습니다.

## 1. 증거와 소유권 확인

```bash
python scripts/workshop.py cleanup-plan
```

`outputs/azure-objects.json`은 이 복사본에서 만든 Search index/source/base의 기록입니다.
모든 Azure 리소스를 포괄하는 inventory나 삭제 권한의 증명은 아닙니다.
개인 결과가 필요한지 먼저 판단하고, 공개 저장소에는 비밀/환경 식별자를 올리지 않습니다.

## 2. 실행 중인 로컬 프로세스와 Hosted session

1. `serve`를 실행한 터미널에서 `Ctrl+C`로 **그 서버만** 종료합니다.
2. azd 프로젝트 폴더에서 자신의 Hosted session을 조회합니다.

```bash
azd ai agent sessions list --limit 10
```

continuation token이 있으면 다음 페이지도 확인합니다.
여러 서비스가 있으면 실제 서비스 이름으로 `--agent-name`을 지정합니다.
자신의 session ID와 agent를 확인한 뒤:

```bash
azd ai agent sessions stop "<my-session-id>"
```

중지는 컴퓨트를 종료하지만 persistent filesystem을 보존합니다.
다음 호출로 다시 실행될 수 있으므로 완전 삭제나 과금 0의 보장이 아닙니다.
사용자 데이터까지 정리해야 한다면 별도 삭제 동작의 범위와 복구 불가 여부를 검토합니다.
다른 조의 session을 중지하지 않습니다.

## 3. 본인이 만든 객체만 정리

| 자산 | 확인과 정리 |
|---|---|
| Prompt/Hosted agent·version | 정확한 프로젝트·이름·version·소유자 확인 후 담당자가 삭제 |
| Search knowledge base/source/index | 의존 순서: base → source → index; ledger의 본인 이름만 |
| 업로드 파일/벡터 저장소 | 내 File Search 자료와 공유 자료를 구분 |
| 모델 배포 | 조별 전용인지 공유 배포인지 확인; 공유 모델 유지 |
| Search 서비스 | index 삭제만으로 서비스의 고정 비용이 사라지지 않음 |
| Application Insights/Log Analytics | 필요한 증거·보존 정책·공유 여부 확인 |
| Fabric/Work IQ | 전용 capacity/billing/연결을 별도 확인; 조직 consent 임의 삭제 금지 |
| Resource Group | 완전히 실습 전용이고 모든 자산을 확인한 경우에만 소유자가 삭제 |

포털에서 정확한 자산 이름·구독·삭제 경고를 읽고 최종 삭제를 수행합니다.
리소스 그룹 전체를 지우는 복사-붙여넣기 명령은 제공하지 않습니다.

## `azd down`은 모든 환경의 같은 정리 명령이 아닙니다

현재 공식 Hosted quickstart는 다음을 구분합니다.

- azd가 새 프로젝트를 만든 경우: Resource Group과 안의 모든 리소스를 삭제할 수 있음.
- 기존 프로젝트를 선택한 경우: project/RG/hosted agent 등 실습 자산이 남을 수 있음.

따라서 무조건 `azd down`을 실행하거나, 성공 메시지만 보고 비용이 끝났다고 하지 않습니다.
사용한 provider·생성 계획·기존 자원 여부를 [공식 안내](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)와 대조합니다.

## 4. 최종 확인

- [ ] 내 로컬 서버가 종료됨.
- [ ] 내 활성 Hosted session이 남지 않았는지 재조회함.
- [ ] 내 agent/파일/Search 객체의 처리 결과를 확인함.
- [ ] 공유 자원과 타인의 데이터를 유지함.
- [ ] 서비스·모델·로그·storage·capacity의 잔여 비용을 담당자가 확인함.
- [ ] 보존할 결과와 지울 민감정보를 구분함.

비용 화면은 지연되어 반영될 수 있습니다. 마지막 조회 시각과 담당자를 기록합니다.
예산 알림은 자동 중지 장치가 아닙니다.

## Hosted matrix의 세션과 증거

새 `benchmark` 경로는 생성한 session ID와 exact version을 immutable manifest에 남깁니다.
실제 trace 확인 후 해당 label의 세션만 중지합니다.

```bash
python scripts/workshop.py benchmark stop-session --label wf-baseline
python scripts/workshop.py benchmark stop-session --label wf-candidate
python scripts/workshop.py benchmark stop-session --label wf-final
```

cleanup receipt는 별도 파일이므로 frozen candidate와 regression source hash를 바꾸지 않습니다.
`outputs/benchmarks/`, `outputs/judge-calibration/`, `outputs/regressions/`의 원본·실패 시도·검토 계보는 보존합니다.
새 `.build/workflow-*` 프로필을 정리하기 전 현재 `azure.yaml`의 실제 참조 경로와 hash를 확인합니다.
별도 smoke 세션은 raw HTTP/azd 목록에서 본인의 ID를 확인해 중지합니다.

## 5. 로컬 `outputs`와 생성 디렉토리

**2026-09-14 한국어 원본과 2026-09-15 새 영문 촬영본을 구분해 보존합니다.**
[새 영문 촬영본](../english-recordings.md)의 기준 목록은 `docs/assets/english-20260915/media.json`,
한국어 원본은 `docs/assets/live-20260914-action/media.json`입니다.
기본 로컬 재생은 영문 촬영본이며 `--edition ko`로 한국어 원본을 선택합니다.
다른 언어의 촬영일이 최신이라는 이유만으로 기존 언어의 미디어를 지우지 않습니다.
날짜만 보고 지우지 말고 이 목록의 파일명·해시를 먼저 대조합니다.
평가 입력·응답·평가자·소유권 기록은 미디어와 별개이며, Git에서 제외됐다는 이유로 삭제하지 않습니다.

| 위치 | 보존 기준 |
|---|---|
| `docs/assets/english-20260915/` | 새 영상 3개·lossless 이미지 537개·234개 액션·실행/프레임/재생 계보 |
| `outputs/english-20260915/` | 원시 실행·원본 영상 6개·캡처 계보·해시 manifest의 비공개 보관본. Git에 게시하지 않음 |
| `docs/assets/live-20260914-action/` | 개별 편집 영상 2개와 가이드 순서 통합본 1개·236개 액션의 캡처·프레임/해시 계보. 각 버전의 역할을 구분 |
| `outputs/azure-objects.json` | 현재 Search 객체의 소유권 기록. 단순 로그가 아니므로 유지 |
| `outputs/live-20260914-action/` | 새 환경의 원시 응답·평가자·File Search·포털·정리 증거. 개인정보가 있어 Git에서 제외 |
| `outputs/<label>/` | 해당 실행의 manifest·응답·평가 결과. 고유한 평가 계보를 보존 |
| `outputs/policy-documents/` | 초보자 경로에 배포하는 합성 텍스트 파일 |
| `outputs/live-20260914-action/sources/` | 이번 촬영의 편집 전 source 영상 4개. 해시 검증용 개인 보관본이며 기본 재생 영상과 구분 |
| `.build/hosted/` | 현재 `azure.yaml`이 참조하는 소스와 `.foundry` 평가 계보. 통째로 삭제하지 않음 |

캡처의 중복 파일·단순 대기 갱신·임시 인코딩 결과는 최종 파일의 해시와 원본 대응을 확인한 뒤 정리합니다.
평가 증거를 압축 보관한다면 각 파일의 해시를 검증하고, 이미지·영상이 섞여 있는지도 확인합니다.
촬영 제작 도구·가상환경은 참가자 저장소에 추가하지 않습니다.
로컬 재생기, 실제 실습 명령, 합성 데이터와 회귀 검사는 유지합니다.

보관 내용을 확인하려면 저장소 루트에서 다음 읽기 전용 명령을 사용합니다.

```bash
tar -tzf outputs/live-20260914-action/evidence.tar.gz
```

압축본에는 개인 환경·실행 식별자가 들어 있을 수 있으므로 외부에 게시하지 않습니다.
`.git`, 루트 `.venv`, 현재 `.env`·`.azure`, 실습 소스·합성 원본·테스트는 정리 대상이 아닙니다.

이 정리는 현재 파일과 가이드 참조에 대한 것입니다. Git 이력이나 GitHub의 별도 첨부 저장소까지
삭제하는 작업과는 구분하며, 확인하지 않은 영구 삭제를 완료했다고 표시하지 않습니다.
