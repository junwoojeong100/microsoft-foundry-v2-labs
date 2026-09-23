# 기능 범위와 실행 근거의 경계

[English](../coverage.md) | **한국어**

**2026-09-16 확장(이전 `gpt-5.6-luna` preset).** 모든 Foundry 기능을 실행했다는 주장이 아니라 범위 기록입니다.
영문 작성 → 영문 촬영 → 영문 보완 → 국문 작성 → 별도 국문 촬영 → 국문 보완 순서로 제작합니다.
2026-09-24 `gpt-6-sol` 녹화는 Lab 00–09·11의 A/B 주요 단계와 선택 Foundry 평가 단계(포털·추적 평가, **실행 비교**를 포함한 업무 기준,
MAF 도구 호출 채점)를 다시 실행했고 이전 녹화는 삭제했습니다. 2026-09-23에는 별도 검증으로 선택 평가 단계, 대화 평가 모듈,
기존 추적·되풀이 평가, Agent Optimizer, 클라우드 red teaming, 승인된 Hosted 릴리스를 `gpt-6-sol`로 실행했습니다. 그 밖의 확장 근거는 다시 실행하지 않았습니다.

## 상태 읽기

| 상태 | 의미 |
|---|---|
| 기존 실습 | 실행 가능한 기존 경로, 날짜와 과거 검증 범위를 확인 |
| 준비 중 | 가이드/코드 작업, 새 live/media 완료 주장 없음 |
| 실제 검증 | 해당 언어·판의 날짜/버전/실제 응답·오류·근거가 있음 |
| 촬영 | 실제 action/video/source-frame 기록, 촬영 상태가 실행 성공은 아님 |
| 설계만 | 구조·준비 조건 검토, 서비스 연결 주장 없음 |
| 미실행/차단 | 승인·접근·지원·데이터가 준비되지 않음 |

GA/Preview는 제품 속성이지 완료 상태가 아닙니다.
prerelease SDK가 전체 서비스를 Preview로 만들거나 GA가 모든 mode를 GA로 만들지 않습니다.

## 과정 지도

| 기능 | 경로 | 이번 확장의 검증 경계 |
|---|---|---|
| 모델·Prompt Agent·원문 | A/B | 기존 Lab 00–03의 고정 첫 모델과 학습자 입력 유지 |
| 함수·로컬 MCP·MAF | B | 기존 Lab 04–05의 실제 패턴과 한계 유지 |
| Search·hybrid·GA IQ·별도 MI chat | B/C | GA 검색과 Preview planning/synthesis 구분 |
| 업무/native 평가·최종 인수 | A/B | 모든 오류와 dataset/evaluator 이력 유지. 선택 포털 평가·근거 없음 진단·코드 기반 업무 평가자·**실행 비교**는 2026-09-24 녹화와 2026-09-23 검증에서 두 언어로 실행([결과](live-run.md)). 사용자 지정 평가자와 TaskAdherence는 Preview |
| MAF 에이전트 도구 호출 평가 | B | Lab 04 선택 `maf-evaluate`. 2026-09-24 녹화와 2026-09-23 검증에서 두 언어로 실행, MAF 평가 API는 실험 기능 |
| Hosted matrix/calibration/trace | C | 기존 워크북의 역사적 결과 유지, 새 코드는 새 label |
| [Toolbox](labs/extensions/toolbox.md) | B | 실제 discovery·query·MAF·고정 버전 확인 |
| [Tool Search/Skills](labs/extensions/tool-search-skills.md) | C | 실제 목록·고정·bytes readback·load, catalog 인프라는 별도 |
| [대화 평가](labs/extensions/conversation-evaluation.md) | C | dev 6턴/2대화와 별도 수준의 평가. 2026-09-23 `gpt-6-sol`로 두 언어 재검증 |
| [Optimizer](labs/extensions/agent-optimizer.md) | C | 2026-09-23 임시 `gpt-5.5` optimizer 모델로 두 언어 재실행: baseline만 반환, Groundedness가 답변을 자기 자신과 비교해 승격 없음. 2026-09-16 결과는 이력 |
| [승인 게이트/복구](labs/extensions/approval-recovery.md) | C | 실제 로컬 SDK와 모의 결정, 실제 사람 승인/Hosted crash 아님 |
| [A2A](labs/extensions/a2a.md) | C | 명시적 1.0 설정/card와 원래 call/output, packet capture 아님 |
| [Memory](labs/extensions/memory.md) | C | API 기반 lifecycle/scope/회상, 사용자 인가 증거 아님 |
| [Routines](labs/extensions/routines.md) | C | 제한된 수동 전달과 정리, 원래 답변 조회는 별도 |
| [안전 제어](labs/extensions/agent-safety.md) | C | 실제 policy/attachment, D01 완료·D06 도구 발견 실패; platform 차단 주장 없음(이전 preset). 2026-09-23 `gpt-6-sol` 클라우드 red-team scan(Preview)은 표시된 ASR이 모든 행의 reasoning과 모순되어 red-team 결과를 주장하지 않음 |
| [릴리스](labs/extensions/release-operations.md) | C | 2026-09-23 `gpt-6-sol` 영문·국문 OIDC 릴리스가 dev 6/6 업무 gate 통과, 기존 추적 평가는 두 언어 모두 평가자별 15/15, 매시간 되풀이 일정을 확인하고 일시 중지([결과](live-run.md#이전에-실행하지-않은-항목--2026-09-23)). 운영 승인은 별도 |
| [모델 운영](labs/extensions/model-operations.md) | C | 기존 배포의 통제 비교, Router/이전은 별도 승인 |
| [추가 도구](labs/extensions/additional-tools.md) | B/C | OpenAPI와 실제 Code Interpreter 파일 검증 |
| [거버넌스](labs/extensions/governance-networking.md) | C | 실제 ID·권한 범위, 사설망 미구성이면 설계만 |
| 회사/Microsoft 365 데이터 | 전문 | 접근하지 않음 |
| Fine-tuning·음성·브라우저 업무 동작 | 전문 | 별도 전문 과정, [설계 범위](labs/extensions/specialist-scope.md)만 |

## 언어와 판을 섞지 않기

[2026-09-24 `gpt-6-sol` 국문 실행](live-run.md)과 [녹화](video-summary.md)는 각자의 날짜와 결과를 유지하며 확장 모듈 실행으로 표시하지 않습니다.
2026-09-16 확장 결과·영상(이전 `gpt-5.6-luna` preset)은 작업 트리에서 삭제했습니다.
위 표의 날짜가 있는 결과는 과거 기록이며 `gpt-6-sol`의 근거가 아닙니다. 영문 결과를 국문 실행으로 복사하지 않습니다.

새 근거는 언어, source/package, 모델/agent 버전, prompt/dataset/corpus/evaluator hash,
모든 응답·실패, 정리 상태를 보존합니다. 인증·암호·token·MFA는 녹화에서 제외합니다.

## Straightforwardness 기준

모듈마다 첫 경로 하나, 정확한 입력·명령, 관찰 가능한 완료 기준, 중단/복구와 다음 링크가 있어야 합니다.
대안은 첫 성공 이후에 둡니다. 비용·권한·접근 조건은 부작용 있는 명령 **앞에** 안내합니다.
링크나 fixture가 통과했다는 이유로 Azure 실행을 완료 처리하지 않습니다.
