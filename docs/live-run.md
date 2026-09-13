# Sweden Central — GPT-5.6 Luna 실제 실행

**2026-09-13, `rg-mfv2-luna-20260913`을 같은 이름으로 재생성하고 모든 지역 리소스를 Sweden Central에 배치했습니다.**
지정한 실습 계정으로 실행했으며 기본 Azure CLI 구독은 변경하지 않았습니다.
입력은 저장소의 합성 정책과 평가 데이터뿐입니다. 회사·Microsoft 365 데이터에는 연결하지 않았습니다.

## 환경과 모델

| 항목 | 이번 실행 |
|---|---|
| 리소스 그룹 | `rg-mfv2-luna-20260913` |
| Foundry 계정 / 프로젝트 | `ai-mfv2-luna-swc-20260913` / `mfv2-luna-20260913` |
| Search | `srch-mfv2-luna-swc-20260913`, Basic, Entra ID 인증 |
| 관측 | 같은 리전의 Application Insights / Log Analytics, 30일 보존·일일 1GB 수집 제한 설정 |
| 응답 모델 | `gpt-5.6-luna`, `2026-07-09`, Data Zone Standard 100K TPM |
| 별도 judge 배포 | `gpt-5.6-luna-judge`, 같은 Luna 버전, Data Zone Standard 50K TPM |
| 버전 정책 | 두 모델 배포 모두 `NoAutoUpgrade` |

리소스의 배치 리전과 추론 처리 범위는 구분합니다. Data Zone Standard는 **EU 데이터 존 처리 유형**이며,
추론이 Sweden Central의 단일 데이터센터에서만 처리된다는 뜻은 아닙니다.
별도 judge 배포도 같은 기반 모델이므로 서로 독립적인 모델의 평가라고 주장하지 않습니다.

처음 시도한 East US 2에서는 Search 신규 생성이 용량 부족으로 거부되었습니다.
사용자 선택에 따라 그 시도의 전용 그룹을 삭제하고 같은 그룹명을 Sweden Central에 다시 만들었습니다.
새 시도에서는 Search 생성 완료를 먼저 확인했습니다. 다른 모델·검색 provider·fixture로 우회하지 않았습니다.

## 실제 화면과 실시간 영상

- [CLI 전체 영상 바로 열기](https://github.com/user-attachments/assets/75dd6df4-c615-4c28-8621-8a416ea31cbe)
- [Foundry 포털 영상 바로 열기](https://github.com/user-attachments/assets/19b9097b-a4e9-41ad-9cc6-ddab5a1e5f14)
- [재생·다운로드 안내](video-summary.md#재생하기)
- [단계별 영상·캡처 안내](video-chapters.md)
- [파일 정보·해시·촬영 계보](assets/live-20260913-swc/media.json)

**아래 GitHub 플레이어의 ▶ 버튼으로 바로 재생할 수 있습니다. 로컬 서버는 필요 없습니다.**
비공개 저장소에 접근 가능한 GitHub 계정으로 로그인한 상태에서 이용하세요.

### CLI 전체 영상 — 95분 50초

https://github.com/user-attachments/assets/75dd6df4-c615-4c28-8621-8a416ea31cbe

### Foundry 포털 전체 영상 — 82분 16초

https://github.com/user-attachments/assets/19b9097b-a4e9-41ad-9cc6-ddab5a1e5f14

**72개 CLI 실행 단계와 실제 포털 조작을 실행 중에 녹화했고 PNG 122개를 남겼습니다.**
기록한 JSON을 나중에 4초씩 재생한 영상이 아닙니다. 대기시간을 제거하거나 결과를 재현 화면으로 바꾸지 않았습니다.
CLI 화면은 실제 프로세스 출력을 표시하는 전용 콘솔이며, 포털 영상은 실제 `ai.azure.com` 화면입니다.
두 영상 모두 Playwright 1.62.0 headless Edge로 촬영했습니다. 로그인·MFA 화면은 녹화하지 않았습니다.
CLI 식별자와 Bearer 값은 마스킹했습니다. 포털 화면에는 실습 계정·리소스 식별정보가 있을 수 있어 외부 게시 전 검토가 필요합니다.

![새 프로젝트의 실제 Luna 응답](assets/live-20260913-swc/P03-luna-playground-response.png)

## 실습 결과

| 경로 | 확인한 결과 |
|---|---|
| 모델 | 새 Luna 배포의 SDK·포털 실제 응답. 포털 기본 Web Search는 요청 전에 제거 |
| A. 포털 에이전트 | `mfv2-swc-20260913-portal` 버전 2, 합성 원문 직접 컨텍스트, dev 6건을 각각 새 대화로 수집 |
| SDK Prompt Agent | `mfv2-swc-20260913-policy` 버전 1, 현행·과거·승인·근거 부족 응답 |
| MAF | 단일·함수·로컬 MCP·순차·병렬·Group Chat 실제 실행 |
| Search / Foundry IQ | 합성 6건 업로드, 전용 source/base, GA `2026-04-01` 실제 검색과 원문 인용 |
| File Search | `mfv2-swc-20260913-files` 버전 1, 합성 파일 6개 색인 완료, 실제 검색 호출 및 파일 인용 3개 |
| B. v1 / v2 dev | **6/6 / 6/6**, 수집 오류 0, 비교 시 검색 컨텍스트 변경 0 |
| 고정 후보 holdout | **4/4**, 후보 고정 후 한 번만 수집 |
| 별도 native judge | groundedness **5/6**, relevance **5/6** |
| Hosted | `mfv2-swc-20260913-hosted` 버전 1, 로컬·원격 실제 응답 |
| Hosted 별도 평가 | 기존 합성 dev 6건으로 실제 원격 응답을 새로 생성, 생성형 rubric **6/6** |
| Lab 10 | 합성 라우팅 설계 수행. Fabric·Work IQ 실제 연결과 데이터 조회는 미실행 |

Group Chat은 설정된 **3라운드 상한으로 종료**했습니다. 사람의 승인이나 자연스러운 합의 완료를 뜻하지 않습니다.
포털 자연어 답변 관찰, 결정적 업무 검사, native judge, Hosted rubric은 서로 다른 확인 경로입니다.
한 경로의 점수를 다른 경로의 품질로 재사용하지 않습니다.

![포털의 현행 규정 답변](assets/live-20260913-swc/P06-D01-portal-response.png)

## 실패와 평가의 한계

v1과 v2가 모두 6/6이므로 이 작은 dev 집합에서 v2의 우월성을 주장하지 않습니다.
업무 검사의 통과가 답변 전체의 의미적 정확성을 보장하지도 않습니다.

| native 실패 | 실제 관찰 |
|---|---|
| D01 groundedness, 2점 | 검색 컨텍스트에는 `APPROVAL-01`이 없는데 답변에 팀장·예약 전 승인 조건이 포함됨. 지침의 기여와 검색 근거를 구분해야 함 |
| D05 relevance, 2점 | 해외 규정이 없어 금액을 보류한 답변을 일반 relevance가 낮게 채점. 업무상 올바른 보류와 일반 judge 기준의 차이를 검토해야 함 |

이 실패를 삭제하거나 통과로 바꾸지 않았습니다. holdout을 보고 지침을 수정하거나 회귀 데이터를 만들지도 않았습니다.
Hosted 평가는 별도의 생성형 rubric과 **0.5 임계값**을 사용했습니다.
CLI가 실행에 기록한 evaluator version selector는 빈 값이어서, 조회한 catalog 버전 1을 보관하되
**평가자를 명시적으로 버전 고정해 실행했다고 소급해서 주장하지 않습니다.**
생성 평가자의 `input_quality` 경고, SDK 직렬화·MCP/Pydantic·hosting prerelease 경고도 보존했습니다.

![실패를 포함한 native 평가](assets/live-20260913-swc/P12-native-evaluation-report.png)

## Hosted와 Trace

실제 배포의 환경 변수에서 새 프로젝트 endpoint, `gpt-5.6-luna`,
`WORKSHOP_AUTH_MODE=managed-identity`를 확인했습니다.
원격 응답은 `needs_approval`, 150,000원 한도와 실제 규정 ID를 반환했습니다.

원격 호출의 Trace ID `9a829b6e14dc188afdbf494cf0d804dd`를 포털에서 직접 찾았습니다.
해당 버전 1의 trace는 **14 spans, chat 1회, 도구 1회, 약 6.4초, root Completed**로 표시됐습니다.
Hosted 평가 6건의 실제 질문·응답·도구 결과·response/trace ID와 모든 per-item 점수도 따로 내려받았습니다.

![같은 원격 호출의 실제 Trace](assets/live-20260913-swc/P16-hosted-trace-detail.png)

`monitor` 조회 시 해당 세션은 이미 멈춰 있어 `stream_interrupted`가 반환되었습니다.
이를 정상적인 실시간 로그 스트리밍 성공으로 표시하지 않습니다.
로컬 console trace와 프로젝트 Responses 결과의 `trace_export: not-configured`도 Azure 서버 trace와 구분합니다.

## 정리와 남은 비용

이전 MFV2 실행의 에이전트 3개, 모델 배포 4개, Search 객체 6개, 평가 3개,
생성 평가자·아티팩트 2개를 정리했습니다.
공유 `microsoft-iq-workflow-agent`, `gpt-5.4-mini`, 기존 공유 Foundry/Search/관측 기반은 보존했습니다.
새 Hosted 세션 2개는 중지 후 모두 `idle`임을 확인했습니다.

새 Sweden Central 그룹은 재현·검토용으로 남겨 두었습니다.
세션 중지는 파일시스템 삭제가 아니며 **Search 고정비·저장소·로그·향후 모델 호출 비용이 없어졌다는 뜻이 아닙니다.**
이전 화면·영상과 불필요한 로컬 생성물을 정리했으며 Git 이력은 재작성하지 않았습니다.
개인 원시 실행 자료와 로컬 환경 설정은 Git에서 제외합니다.

오프라인 검사와 실제 Azure 결과는 [검증 기록](reference/validation.md)에 구분했습니다.
