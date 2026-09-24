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

이 명령은 목록과 안내를 출력할 뿐 삭제하지 않습니다.

</details>

구독·프로젝트·prefix·agent/version/session ID·모델 배포·Search 객체·로그/저장소 소유자를 기록합니다.
`outputs/azure-objects.json`은 이 복사본이 만든 Search index/source/base만 기록하며 전체 Azure 목록이나 삭제 권한의 증명이 아닙니다.
`cleanup-plan`의 `search_ownership.objects`는 Azure 조회가 아닌 그 파일의 내용이며, `search_ownership: null`은 파일이 없다는 뜻입니다.
`null`이나 빈 목록은 자원·비용이 없다는 증거가 아닙니다. 객체를 만들었다면 담당자와 대응하는 ledger를 복구하고 임의로 대체하지 않습니다.
Ledger가 없어도 본인 기록과 담당자의 확인을 바탕으로 `required_manual_inventory`를 작성합니다.
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
| Prompt/Hosted agent·version | B의 핵심이 된 Lab 03 B SDK 관리형 agent를 포함해 정확한 프로젝트·이름·version·소유자 확인 후 담당자가 삭제. 2026-09-25 확인에서 prompt agent를 삭제하면 그 Entra agent ID와 청사진도 함께 삭제됨 |
| Search knowledge base/source/index | 의존 순서 base → source → index; ledger의 본인 이름만 |
| 업로드 파일/벡터 저장소 | 내 File Search 자료와 공유 자료를 구분 |
| 평가 데이터 세트·평가·사용자 지정 평가자 | 본인의 `<prefix>-dev-questions` 데이터 세트, `<prefix>-...` 평가, 평가 실행마다 서비스가 만드는 `eval-data-<UTC 시각>` 데이터 세트(`cloud-evaluate`, `maf-evaluate`, `conversations evaluate`. 시각은 평가 생성 시각과 몇 초 차이이며, 다른 사람의 실행도 같은 이름 형식을 만듦), `<prefix>_business_rubric` 버전(하이픈은 밑줄로 바뀜). 결과를 먼저 보존한 뒤 담당자가 삭제 |
| 모델 배포 | 조별 전용인지 공유 배포인지 확인; 공유 모델 유지 |
| Search 서비스 | index 삭제만으로 서비스의 고정 비용이 사라지지 않음 |
| Application Insights/Log Analytics | 필요한 증거와 공유 여부 확인. Lab 09 trace 요구 사항을 포함해 보존 기간과 비용은 담당자가 관리 |
| Resource Group | 실습 전용이고 모든 자산을 확인한 경우에만 소유자가 삭제 |

<details>
<summary>되풀이 평가·Agent Optimizer·red teaming·CI·Fabric/Work IQ 모듈을 실행한 경우에만</summary>

| 자산 | 확인과 정리 |
|---|---|
| 되풀이 평가 일정 | 본인의 `<agent>-scheduled-...` 일정: 평가 페이지에서 **일시 중지**를 선택하고 일시 중지 상태를 다시 읽음. 일시 중지해도 이전 결과는 남음 |
| Optimizer 데이터 세트·실행 | 본인의 `<prefix>-optimizer-dev` 데이터 세트와 최적화 실행. 결과를 먼저 보존한 뒤 담당자가 삭제 |
| Red-team taxonomy·red team | 본인의 `<prefix>-...redteam` taxonomy, red team과 실행. 모든 출력 항목과 검토 기록을 먼저 보존한 뒤 담당자가 삭제 |
| 모니터링·CI용으로 추가한 역할 | 추가한 담당자만 제거. 예: Application Insights에 대한 프로젝트 ID의 **Monitoring Reader**, CI ID의 프로젝트 역할, Hosted 런타임의 **Foundry User** |
| 임시 optimizer 배포 | 만든 담당자만, 그 배포를 쓴 optimizer 실행이 모두 끝나고 검토된 뒤 삭제. 답변·judge 배포가 남았는지 확인 |
| Fabric/Work IQ | 전용 capacity·billing·연결을 별도 확인; 조직 consent는 회수하지 않음 |

</details>

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
- [ ] 내 agent·파일·Search 객체의 처리 결과를 확인했습니다. 삭제 응답만으로는 증거가 되지 않으므로 삭제한 객체를 다시 조회합니다.
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

cleanup receipt는 변경하지 않는 manifest와 별도 파일이므로 candidate와 regression hash가 그대로 유효합니다.
별도로 만든 smoke 세션은 그 세션의 raw HTTP/azd 기록으로 확인합니다.

</details>

## 5. 로컬 출력과 최종 미디어

<details>
<summary>별도로 승인된 미디어 교체의 유지보수 담당자만 — 학습자는 저장소의 데이터·영상을 보존합니다</summary>

기존 스크린샷·영상을 교체하기 전에 새 언어 세트 두 개를 모두 검증합니다.
`docs/assets/g6sol-20260924-ko/`와 `g6sol-20260924-en/`의 media manifest,
실제 byte hash, frame 검사, 재생, 문서 링크를 사용합니다.
한 언어의 교체본만 준비된 상태에서 다른 언어의 기존 asset을 먼저 삭제하지 않습니다.

| 위치 | 보존 기준 |
|---|---|
| 현재 언어별 asset 디렉터리 | 새 영상, 무손실 캡처, action/timestamp/frame 계보 |
| `outputs/benchmarks/<label>/` | 전체 matrix, 원시 실패, dataset/corpus/response/native/trace/cleanup 근거 |
| `outputs/judge-calibration/` | target 응답과 분리한 calibration |
| `outputs/regressions/` | 검토한 원래 dev 기준과 source 계보 |
| `outputs/azure-objects.json` | Azure 객체의 소유권 |
| `outputs/iq-chat/<label>/` | 모델/KB 사전 확인·요청·실제 응답/근거·실패. Benchmark 점수가 아님 |
| `data/learner/<language>/` | 커밋된 시작 자료. 학습자가 작성한 기록은 다른 곳에 보관 |
| `outputs/policy-documents/` | 학습자 ZIP에 이미 있는 같은 합성 파일 6개의 선택 export |
| `.build/<profile>/` | 활성 참조를 확인한 뒤 필요한 배포 source/profile manifest |

두 언어 세트와 최종 검사가 모두 통과한 뒤 쓸모없는 미디어, 중복 임시 인코딩, 최종 워크숍과 무관한 파일을 제거합니다.
실행 코드, 테스트, 합성 입력, 필요한 설정, 라이선스, 평가/실패 계보는 유지합니다.
운영 도구 환경과 비공개 인증/촬영 helper는 학습자 저장소에 두지 않습니다.

이 정리는 현재 파일과 가이드 참조에 관한 것이며, Git 이력을 다시 쓰거나 외부 첨부 저장소에서 확인하지 않은 영구 삭제를 주장하는 작업이 아닙니다.
저장소 루트, 홈 디렉터리 또는 전체 세션 폴더를 재귀적으로 삭제하지 않습니다.

</details>
