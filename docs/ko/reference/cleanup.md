# 실습 정리: 공유 자산을 지우지 않기

[English](../../reference/cleanup.md) | **한국어**

**삭제보다 먼저 “누가 만든 어떤 자산인가”를 확인합니다.**
이 저장소는 Azure 리소스/권한을 자동 삭제하지 않습니다.

**A는 이 페이지에서 터미널이 필요 없습니다.** 기존 `operations-checklist.txt`와 아래 소유권 확인을 사용합니다.
**B는 Lab 09의 목록을 재사용합니다.** 실제 사용한 자산의 명령 구간만 펼칩니다.
담당자 관리·승인 대기 정리는 이름과 잔여 비용을 기록하며 삭제가 끝났다고 표시하지 않습니다.

## 1. 증거와 소유권 확인

<details>
<summary>선택 로컬 목록 명령 — B에서 다시 출력해야 하는 경우만 사용합니다</summary>

```bash
python scripts/workshop.py cleanup-plan
```

</details>

`outputs/azure-objects.json`은 이 복사본에서 만든 Search index/source/base의 기록입니다.
모든 Azure 리소스를 포괄하는 inventory나 삭제 권한의 증명은 아닙니다.
개인 결과가 필요한지 먼저 판단하고, 공개 저장소에는 비밀/환경 식별자를 올리지 않습니다.

<a id="hosted-sessions"></a>

## 2. 실행 중인 로컬 프로세스와 Hosted session

<details>
<summary>로컬 서버·Hosted를 실행한 경우만 — 아니라면 건너뜁니다</summary>

`serve`를 실행한 터미널에서 `Ctrl+C`로 **그 서버만** 종료합니다.
저장소 터미널에서 기록한 **독립 azd 폴더·서비스 이름**을 복원합니다.
관련 없는 `azure.yaml`을 대상으로 실행하지 않습니다.

```bash
printf 'Standalone Hosted directory used for this agent: '
read -r HOSTED_DIRECTORY
printf 'Owned Hosted agent service name: '
read -r HOSTED_AGENT_NAME
azd ai agent sessions list --cwd "${HOSTED_DIRECTORY:?Use the recorded standalone directory}" --agent-name "${HOSTED_AGENT_NAME:?Use the owned service name}" --limit 10
```

Continuation token이 있으면 같은 범위의 list 명령에 `--pagination-token`을 넣어 다음 페이지도 확인합니다.
본인 session ID와 agent를 확인합니다. 이미 idle/stopped이면 상태만 기록하고 다시 중지하지 않습니다.
본인의 **활성** session에만 실행합니다.

```bash
printf 'Owned active session ID from the list: '
read -r OWNED_SESSION_ID
azd ai agent sessions stop "${OWNED_SESSION_ID:?Use the owned active session ID}" --cwd "${HOSTED_DIRECTORY:?Use the recorded standalone directory}" --agent-name "${HOSTED_AGENT_NAME:?Use the owned service name}" &&
azd ai agent sessions list --cwd "${HOSTED_DIRECTORY:?Use the recorded standalone directory}" --agent-name "${HOSTED_AGENT_NAME:?Use the owned service name}" --limit 10
```

중지는 컴퓨트를 종료하지만 persistent filesystem을 보존합니다.
다음 호출로 다시 실행될 수 있으므로 완전 삭제나 과금 0의 보장이 아닙니다.
사용자 데이터까지 정리해야 한다면 별도 삭제 동작의 범위와 복구 불가 여부를 검토합니다.
다른 조의 session을 중지하지 않습니다.

</details>

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
선택 `iq-chat setup`은 API `2026-08-01-preview`의 **별도 chat base**를 같은 ledger에 추가합니다.
삭제 승인 후 source/index보다 먼저 그 source를 참조하는 본인 base를 모두 정리합니다.
GA base를 유지한다면 공유 source/index도 유지합니다. Chat base만 삭제하면서 GA 평가를 깨뜨리지 않습니다.
이 base 하나를 지웠다는 이유로 Search identity의 공유 모델 역할까지 회수하지 않습니다.

## `azd down`은 모든 환경의 같은 정리 명령이 아닙니다

현재 공식 Hosted quickstart는 다음을 구분합니다.

- azd가 새 프로젝트를 만든 경우: Resource Group과 안의 모든 리소스를 삭제할 수 있음.
- 기존 프로젝트를 선택한 경우: project/RG/hosted agent 등 실습 자산이 남을 수 있음.

따라서 무조건 `azd down`을 실행하거나, 성공 메시지만 보고 비용이 끝났다고 하지 않습니다.
사용한 provider·생성 계획·기존 자원 여부를 [공식 안내](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)와 대조합니다.

## 4. 최종 확인

- [ ] 실행한 로컬 서버만 종료함. 미사용이면 미실행으로 기록함.
- [ ] 사용한 Hosted session의 최종 상태 또는 승인된 담당자 대기 작업을 기록함.
- [ ] 내 agent/파일/Search 객체의 처리 결과를 확인함.
- [ ] 공유 자원과 타인의 데이터를 유지함.
- [ ] 서비스·모델·로그·storage·capacity의 잔여 비용을 담당자가 확인함.
- [ ] 보존할 결과와 지울 민감정보를 구분함.

비용 화면은 지연되어 반영될 수 있습니다. 마지막 조회 시각과 담당자를 기록합니다.
예산 알림은 자동 중지 장치가 아닙니다.

**학습자 정리 인계 기준:** `operations-checklist.txt`에 사용한 자산별 확인 상태 또는
승인된 담당자 대기 작업·보존 근거·잔여 비용이 있습니다.
사용하지 않은 로컬/Hosted 서비스는 삭제가 아니라 **미실행**입니다.
[Lab 11](../labs/11-capstone.md)로 돌아갑니다. 아래 미디어 유지보수는 학습자 완료 조건이 아닙니다.

## Hosted matrix의 세션과 증거

<details>
<summary>실제로 있는 matrix 실행만 — A·입문 B에는 해당하지 않습니다</summary>

아래의 실제 matrix label이 있을 때만 실행합니다. A와 입문 B는 건너뜁니다.

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

</details>

## 5. 로컬 `outputs`와 생성 디렉토리

<details>
<summary>별도로 승인된 미디어 교체의 유지보수 담당자만 — 학습자는 저장소의 데이터·영상을 보존합니다</summary>

**새 국문·영문 세트를 각각 검증한 뒤 기존 미디어를 교체합니다.**
국문은 `docs/assets/refresh-20260915-ko/media.json`,
영문은 대응하는 `refresh-20260915-en/media.json`의 실제 파일·해시를 기준으로 검수합니다.
한쪽만 완성한 상태에서 다른 언어의 기존 파일을 먼저 삭제하지 않습니다.
평가 입력·응답·실패·평가자·소유권 기록은 관련 실행 증거이므로 미디어와 별도로 보존합니다.

| 위치 | 보존 기준 |
|---|---|
| `docs/assets/refresh-20260915-ko/` | 별도 국문 새 캡처·영상·액션·source-frame 검증 |
| `docs/assets/refresh-20260915-en/` | 별도 영문 새 캡처·영상·액션·source-frame 검증 |
| `outputs/azure-objects.json` | 현재 Search 객체의 소유권 기록. 단순 로그가 아니므로 유지 |
| `outputs/benchmarks/<label>/` | 실제 matrix, 원시 오류, dataset/corpus/response/native/trace/cleanup 계보 |
| `outputs/judge-calibration/` | target과 분리된 평가자 calibration |
| `outputs/regressions/` | 검토된 원본 dev와 source lineage |
| `outputs/iq-chat/<label>/` | 모델/KB 사전 확인·요청·실제 응답/근거·실패. Benchmark 점수가 아님 |
| `data/learner/<language>/` | 저장소의 시작 자료. 학습자의 작성 평가표는 다른 곳에 보관 |
| `outputs/policy-documents/` | 학습자 ZIP에 이미 있는 동일 합성 TXT 6개의 선택 export |
| `.build/<profile>/` | 현재 배포에 사용한 source와 profile manifest. 참조 여부를 확인해 필요한 것만 유지 |

캡처의 중복 파일·단순 대기 갱신·임시 인코딩 결과는 최종 파일의 해시와 원본 대응을 확인한 뒤 정리합니다.
평가 증거를 압축 보관한다면 각 파일의 해시를 검증하고, 이미지·영상이 섞여 있는지도 확인합니다.
촬영 제작 도구·가상환경은 참가자 저장소에 추가하지 않습니다.
로컬 재생기, 실제 실습 명령, 합성 데이터와 회귀 검사는 유지합니다.

압축본에는 개인 환경·실행 식별자가 들어 있을 수 있으므로 외부에 게시하지 않습니다.
`.git`, 루트 `.venv`, 현재 `.env`·`.azure`, 실습 소스·합성 원본·테스트는 정리 대상이 아닙니다.

이 정리는 현재 파일과 가이드 참조에 대한 것입니다. Git 이력이나 GitHub의 별도 첨부 저장소까지
삭제하는 작업과는 구분하며, 확인하지 않은 영구 삭제를 완료했다고 표시하지 않습니다.

</details>
