# 정리, 소유권, 보존할 증거

[English](../../reference/cleanup.md) | **한국어**

**본인이 만든 자산만 중지하고 상태를 확인합니다. 실습을 끝내려고 공유 프로젝트나 리소스 그룹을 삭제하지 않습니다.**

**A는 이 페이지에서 터미널이 필요 없습니다.** 기존 `operations-checklist.txt`와 아래 소유권 확인을 사용합니다.
**B는 Lab 09의 목록을 재사용합니다.** 실제 사용한 자산의 명령 구간만 펼칩니다.
담당자 관리·승인 대기 정리는 담당자와 잔여 비용을 기록하며, 삭제가 끝났다는 뜻이 아닙니다.

## 1. 바꾸기 전에 목록 확인

<details>
<summary>선택 로컬 목록 명령 — B에서 다시 출력해야 하는 경우만 사용합니다</summary>

```bash
python scripts/workshop.py cleanup-plan
```

</details>

이 명령은 목록과 안내를 출력할 뿐 삭제하지 않습니다.
구독·프로젝트·prefix·agent/version/session ID·모델 배포·Search 객체·로그/저장소 소유자를 기록합니다.
`outputs/azure-objects.json`은 이 복사본이 만든 Search index/source/base만 기록하며 전체 Azure 목록이나 삭제 권한의 증명이 아닙니다.
소유자를 모르면 멈춥니다. 삭제 범위를 넓히는 이유가 아닙니다.

<a id="hosted-sessions"></a>

## 2. Hosted 컴퓨트와 영구 상태

<details>
<summary>로컬 서버·Hosted를 실행한 경우만 — 아니라면 건너뜁니다</summary>

로컬 서버나 Hosted agent를 실행하지 않았다면 이 절을 건너뜁니다. 실행했다면 `serve` 터미널에서 `Ctrl+C`로 본인 서버만 종료합니다.
저장소 터미널에서 기록해 둔 **독립 azd 폴더와 서비스 이름**을 복원합니다.
관련 없는 `azure.yaml`을 대상으로 이 명령을 실행하지 않습니다.

```bash
printf 'Standalone Hosted directory used for this agent: '
read -r HOSTED_DIRECTORY
printf 'Owned Hosted agent service name: '
read -r HOSTED_AGENT_NAME
azd ai agent sessions list --cwd "${HOSTED_DIRECTORY:?Use the recorded standalone directory}" --agent-name "${HOSTED_AGENT_NAME:?Use the owned service name}" --limit 10
```

Continuation token이 있으면 같은 범위의 list 명령에 `--pagination-token`을 넣어 이어서 확인합니다.
본인 session이 이미 idle/stopped이면 다시 중지하지 말고 상태만 기록합니다.
본인의 **활성** session에만 실행합니다.

```bash
printf 'Owned active session ID from the list: '
read -r OWNED_SESSION_ID
azd ai agent sessions stop "${OWNED_SESSION_ID:?Use the owned active session ID}" --cwd "${HOSTED_DIRECTORY:?Use the recorded standalone directory}" --agent-name "${HOSTED_AGENT_NAME:?Use the owned service name}" &&
azd ai agent sessions list --cwd "${HOSTED_DIRECTORY:?Use the recorded standalone directory}" --agent-name "${HOSTED_AGENT_NAME:?Use the owned service name}" --limit 10
```

영구 파일을 남겨야 하면 중지(stop)를 사용합니다. session을 삭제하면 컴퓨트와 영구 파일 시스템 상태가 함께 사라집니다.
선택한 agent/session을 확인하고 본인이 만든 ID만 중지합니다.
이미 idle인 session은 충돌하는 중지 요청을 다시 보내지 않고 idle로 확인합니다.
확인하지 않은 중지 요청을 중지 완료로 기록하지 않습니다.

</details>

## 3. 본인이 만든 객체만 정리

| 자산 | 확인과 정리 |
|---|---|
| Prompt/Hosted agent·version | 정확한 프로젝트·이름·version·소유자 확인 후 담당자가 삭제 |
| Search knowledge base/source/index | 의존 순서 base → source → index; ledger의 본인 이름만 |
| 업로드 파일/벡터 저장소 | 내 File Search 자료와 공유 자료를 구분 |
| 모델 배포 | 조별 전용인지 공유 배포인지 확인; 공유 모델 유지 |
| Search 서비스 | index 삭제만으로 서비스의 고정 비용이 사라지지 않음 |
| Application Insights/Log Analytics | 필요한 증거·보존 정책·공유 여부 확인 |
| Fabric/Work IQ | 전용 capacity·billing·연결을 별도 확인; 조직 consent는 회수하지 않음 |
| Resource Group | 실습 전용이고 모든 자산을 확인한 경우에만 소유자가 삭제 |

선택 `iq-chat setup`은 API `2026-08-01-preview`의 **별도 chat base**를 같은 ledger에 추가합니다.
삭제 승인 후 source/index보다 먼저 그 source를 참조하는 본인 base를 모두 정리합니다.
GA base를 유지한다면 공유 source/index도 유지합니다. chat base만 지우면서 GA 평가를 깨뜨리지 않습니다.
이 base 하나를 지웠다는 이유로 Search identity의 공유 모델 역할까지 회수하지 않습니다.
공유 환경에서는 `azd down`, 구독 변경, 리소스 그룹 삭제를 지름길로 쓰지 않습니다. 기존 프로젝트에서는
`azd down` 후에도 실습 자산이 남을 수 있고, azd가 만든 프로젝트에서는 리소스 그룹 전체가 삭제될 수 있습니다
([공식 안내](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)).

## 4. 최종 확인

- [ ] 실행한 로컬 서버만 종료했고, 사용하지 않은 것은 **미실행**으로 기록했습니다.
- [ ] 사용한 Hosted session마다 최종 상태 또는 승인된 담당자 대기 작업을 기록했습니다.
- [ ] 내 agent·파일·Search 객체의 처리 결과를 확인했습니다.
- [ ] 공유 자원과 다른 사람의 데이터를 유지했습니다.
- [ ] 서비스·모델·로그·저장소·capacity의 잔여 비용을 담당자가 확인했습니다.
- [ ] 보존할 결과와 지울 민감 정보를 구분했습니다.
- [ ] 평가 계보를 보존했습니다: 질문·정답 기준·프롬프트·corpus·모델/agent 버전·평가자 정의,
  모든 응답/오류·trace 조회 기록·검토 기록. 점수를 올리려고 실패 행을 지우지 않으며,
  holdout은 최종 인수 자료로만 두고 회귀 자료로 쓰지 않습니다.

비용 화면은 늦게 반영될 수 있습니다. 마지막 조회 시각과 남은 비용의 담당자를 기록합니다. 예산 알림은 자원을 중지하지 않습니다.

**학습자 정리 인계 기준:** `operations-checklist.txt`에 사용한 자산별 확인 상태 또는
승인된 담당자 대기 작업·보존 근거·잔여 비용이 있습니다.
사용하지 않은 로컬/Hosted 서비스는 삭제가 아니라 **미실행**입니다.
Lab 11에서 왔고 인계를 마쳤다면 **과정을 모두 완료한 것입니다**. 아니면 [Lab 11](../labs/11-capstone.md)로 돌아갑니다.
아래 미디어 유지보수는 학습자 완료 조건이 아닙니다.

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
국문은 `docs/assets/g6sol-20260923-ko/media.json`,
영문은 대응하는 `g6sol-20260923-en/media.json`의 실제 파일·해시를 기준으로 검수합니다.
한쪽만 완성한 상태에서 다른 언어의 기존 파일을 먼저 삭제하지 않습니다.
평가 입력·응답·실패·평가자·소유권 기록은 관련 실행 증거이므로 미디어와 별도로 보존합니다.

| 위치 | 보존 기준 |
|---|---|
| `docs/assets/g6sol-20260923-ko/` | 별도 국문 캡처·영상·액션·source-frame 검증 |
| `docs/assets/g6sol-20260923-en/` | 별도 영문 캡처·영상·액션·source-frame 검증 |
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
