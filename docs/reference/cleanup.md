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
