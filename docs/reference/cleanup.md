# 실습 정리: 공유 자산을 지우지 않기

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

## 5. 로컬 `outputs`와 생성 디렉토리

**최종 미디어, 현재 평가 입력/응답, 이전 실행 이력을 같은 종류의 임시 파일로 보지 않습니다.**
파일이 Git에서 제외되어 있다는 이유만으로 삭제해도 되는 것은 아닙니다.

| 위치 | 보존 기준 |
|---|---|
| `docs/assets/live-20260914-action/` | 새 편집 영상 2개·236개 액션의 캡처·프레임/해시 계보. 같은 이미지의 중복본과 대기 갱신은 제외 |
| `outputs/azure-objects.json` | 현재 Search 객체의 소유권 기록. 단순 로그가 아니므로 유지 |
| `outputs/live-20260914-action/` | 새 환경의 원시 응답·평가자·File Search·포털·정리 증거. 개인정보가 있어 Git에서 제외 |
| `outputs/swc-*-0913/`, `outputs/live-20260913-swc/` | 이전 실행의 고유한 평가 계보. 새 실행 결과로 재사용하지 않음 |
| `outputs/policy-documents/` | 초보자 경로에 배포하는 합성 텍스트 파일 |
| `outputs/archive/20260913-history.tar.gz` | 이전 실행, 상세 CLI/포털 기록과 구버전 패키지를 통합한 개인 보관본 |
| `.build/hosted/` | 현재 `azure.yaml`이 참조하는 소스와 `.foundry` 평가 계보. 통째로 삭제하지 않음 |

구버전 `.build/hosted-pre-live`, `.build/hosted-luna-r1`은 현재 설정에서 참조하지 않아 정리했습니다.
고유한 소스·평가 기록은 위 압축본에 보존했고, 재생성 가능한 가상환경·bytecode 캐시는 제외했습니다.
압축본의 각 파일 해시를 원본과 확인한 뒤 개별 원본을 제거했습니다.

이전 녹화·캡처 파일과 가이드의 이전 영상 링크는 새 촬영 자료로 교체합니다.
Git 이력은 재작성하지 않으며, 파일/링크 제거를 GitHub 첨부 원본의 영구 삭제로 표현하지 않습니다.
첨부 영구 삭제는 GitHub 지원 경로 확인이 필요합니다.
새 촬영 제작 도구·가상환경은 참가자 저장소에 추가하지 않습니다.
현재 로컬 재생기, 실제 실습 명령, 합성 데이터와 회귀 검사는 유지합니다.

보관 내용을 확인하려면 저장소 루트에서 다음 읽기 전용 명령을 사용합니다.

```bash
tar -tzf outputs/archive/20260913-history.tar.gz
```

압축본에는 개인 환경·실행 식별자가 들어 있을 수 있으므로 외부에 게시하지 않습니다.
`.git`, 루트 `.venv`, 현재 `.env`·`.azure`, 실습 소스·합성 원본·테스트는 정리 대상이 아닙니다.
