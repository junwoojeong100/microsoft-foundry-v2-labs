# 기능 범위와 실행 근거의 경계

[English](../coverage.md) | **한국어**

**현재 상태:** 2026-09-24 `gpt-6-sol` 녹화는 Lab 00–09·11의 A/B 주요 단계와 선택 Foundry 평가 단계
(포털·추적 평가, **실행 비교**를 포함한 업무 기준, MAF 도구 호출 채점)를 다룹니다.
2026-09-23 별도 `gpt-6-sol` 확인은 대화 평가 모듈, 기존 추적·되풀이 평가, Agent Optimizer, 클라우드 red teaming,
승인된 Hosted 릴리스를 다룹니다. 아래의 나머지 확장 결과는 2026-09-16(이전 `gpt-5.6-luna` preset) 기록이며, 2026-09-24·25 행에 따로 적은 경우를 빼면 `gpt-6-sol`의 근거가 아닙니다.
2026-09-25에는 짧은 보충 녹화로 Lab 03 B와 Lab 09 B 추적 검색을 두 언어로 남기고, 대화 평가·Memory·routine·Toolbox 탐색까지를 영문으로 실행했습니다.
이 페이지는 범위 기록이지 모든 Foundry 기능을 실행했다는 주장이 아닙니다.
제작 순서는 영문 가이드 → 영문 녹화 → 영문 보완 → 국문 가이드 → 별도 국문 녹화 → 국문 보완입니다.

## 상태를 정직하게 읽기

| 상태 | 의미 |
|---|---|
| 기존 실습 | 실행 가능한 안내가 이미 있음. 정확한 과거 범위는 연결된 검증 기록에서 확인 |
| 준비 중 | 추가 가이드·코드를 작성 중. 새 실행·미디어 완료를 주장하지 않음 |
| 실제 검증 | 이 판의 날짜·버전이 있는 응답과 필요한 원문·오류·사용량 근거가 있음 |
| 녹화 | 실제 액션·영상·원본 프레임 기록이 있음. 스크린샷만으로는 실행이 아님 |
| 설계만 | 구조·선행 조건 검토. 서비스 연결을 주장하지 않음 |
| 미실행/차단 | 필요한 승인·접근·기능 지원·데이터가 없음 |

GA/Preview는 **제품 속성**이지 위 완료 상태가 아닙니다.
설치한 prerelease SDK가 서비스 전체를 Preview로 만들지 않고, GA 서비스라고 모든 SDK·도구 모드가 GA인 것도 아닙니다.

## 현재 과정 지도

| 기능 | 경로 | 현재 워크숍 범위 | 최신 날짜 근거 |
|---|---|---|---|
| 모델·Prompt Agent·합성 원문 근거 | A/B | 기존 Lab 00–03 | 2026-09-24 `gpt-6-sol` 녹화 |
| 관리형 Prompt Agent를 핵심 경로로 | B | Lab 03 B는 관리형 Prompt Agent를 B의 핵심 작업으로 다룸 | 2026-09-24 갱신한 고정 버전으로 영문·국문 실제 검증(생성, 정확한 버전 호출, 추적). 2026-09-25 두 언어 화면과 짧은 영상 |
| 함수·로컬 MCP·MAF orchestration | B | 기존 Lab 04–05 | 2026-09-24 `gpt-6-sol` 녹화 |
| A Lab 05 브라우저 선택지 | A | 담당자가 준비한 선택 Hosted workflow agent를 포털 Playground에서 사용 | 2026-09-24: workflow agent가 로컬 Responses 요청 1개에 답함. 원격 배포와 Playground 사용은 실행하지 않음 |
| Search·hybrid·GA IQ와 별도 MI chat preset | B/C | 기존 Lab 06과 keyless preset | 2026-09-24 `gpt-6-sol` 녹화: 로컬·Search·GA IQ 검색. 하이브리드 RAG와 `gpt-5.6-luna` IQ Chat preset은 다시 실행하지 않음(설정 화면은 2026-09-17 확인) |
| 업무 평가·native 평가와 고정된 인수 기준 | A/B | 기존 Lab 07과 선택 포털 평가·근거 없음 진단·코드 기반 업무 평가자·**실행 비교** | 2026-09-24 `gpt-6-sol` 녹화와 2026-09-23 검증, 두 언어([결과](live-run.md)). 사용자 지정 평가자와 TaskAdherence는 Preview |
| MAF 에이전트의 도구 호출 평가 | B | Lab 04의 선택 `maf-evaluate` | 2026-09-24 `gpt-6-sol` 녹화와 2026-09-23 검증, 두 언어. MAF 평가 API는 실험 기능 |
| 추적 확인을 핵심 근거로 | A/B | Lab 09 A/B는 실제 추적 근거 또는 명시적인 미확인 이유를 기록 | 2026-09-24: Application Insights에서 response ID로 관리형 agent 추적을 찾음(영문·국문). 2026-09-25: 포털 **추적** 검색을 두 언어로 녹화하고 A 경로 추적 확인을 읽기 전용으로 반복 |
| 독립 SDK 예제 | B/C | 모델, Prompt Agent, MAF, IQ, Hosted 패턴의 최소 예제 파일 | 2026-09-24 오프라인 stub 테스트, 두 가지 수정 뒤 예제 02–06·08 실제 실행(영문) |
| SDK 고정 버전 갱신 | B/C | 갱신한 의존성 조합과 공급자 제약 문서화 | 2026-09-24 오프라인 테스트와 두 언어 핵심 B 경로·선택 평가 실제 실행 |
| [Hosted workflow·모델 matrix·calibration·regression·trace](reference/evaluation-workbook.md) | C | 기존 워크북 | 2026-09-15 `gpt-5.6-luna`만(국문 4모델 matrix). `gpt-6-sol`로 다시 실행하지 않음 |
| [관리형 Toolbox lifecycle](labs/extensions/toolbox.md) | B | 실행 가능한 소유·버전 경로 | 2026-09-25 `gpt-6-sol`(영문): 생성과 MCP 탐색 확인. 프로젝트 ID에 Search Index Data Reader만 있어 직접 query는 Search가 거부함. 이전: 2026-09-16 `gpt-5.6-luna` 직접 조회·MAF·로컬/원격 Hosted·다운로드 근거 확인 |
| [Tool Search·Skills·사설 skill catalog](labs/extensions/tool-search-skills.md) | C | 실행 가능한 Tool Search/Skill 경로 | 2026-09-25: Toolbox의 Search 접근 문제로 막힘. 이전: 2026-09-16 `gpt-5.6-luna` 영문 도구 탐색·고정, 정확한 Skill 재조회와 실제 load 확인. catalog 인프라는 구성하지 않음 |
| [전체 대화 평가와 재사용 데이터 세트](labs/extensions/conversation-evaluation.md) | C | 실행 가능한 dev 전용 다중 턴 경로 | 2026-09-23 `gpt-6-sol`: 두 언어 재검증, native 두 수준 모두 실행. 2026-09-25 갱신한 고정 버전으로 영문 재실행: 턴 6/6·6/6, 대화 2/2·2/2 |
| [Agent Optimizer](labs/extensions/agent-optimizer.md) | C | 범위를 제한한 Prompt Agent 마법사 하나 | 2026-09-23 `gpt-6-sol`: 임시 `gpt-5.5` optimizer 모델로 두 언어 재실행. baseline만 반환했고 Groundedness가 각 답변을 자기 자신과 비교해 승격 없음 |
| [지속 사람 승인·재시작 복구·steering](labs/extensions/approval-recovery.md) | C | 실제 로컬 SDK 시연 | 2026-09-16: 모의 결정을 쓴 영문 재시작·checkpoint 확인. 실제 사람 승인이 아님 |
| [A2A 1.0](labs/extensions/a2a.md) | C | 명시적 card·설정과 위임 | 2026-09-24 `gpt-6-sol`: 형식이 있는 SDK 요청으로 영문 재실행, 위임 호출 1회 확인(이전: 2026-09-16 `gpt-5.6-luna`). wire packet은 캡처하지 않음 |
| [Memory](labs/extensions/memory.md)와 [Routines](labs/extensions/routines.md) | C | 소유 lifecycle과 제한된 timer | 2026-09-25 `gpt-6-sol`(영문): Memory 수명 주기 확인, routine dispatch 1회 완료와 추적 확인, 답변 조회는 불가. 이전: 2026-09-16 `gpt-5.6-luna` |
| [적용 가드레일과 통제된 red teaming](labs/extensions/agent-safety.md) | C | 전용 policy·대상 | 2026-09-16 `gpt-5.6-luna`: 영문 attachment와 차단되지 않은 두 사례. 2026-09-23 `gpt-6-sol`: 클라우드 red-team scan(Preview)을 실행했지만 표시된 ASR이 모든 행의 판단 근거(reasoning)와 모순되어 red-team 결과를 주장하지 않음 |
| [지속 평가와 배포 품질 게이트](labs/extensions/release-operations.md) | C | 수동 guarded workflow와 OIDC 설정 | 2026-09-23 `gpt-6-sol`: 두 OIDC 릴리스, 기존 추적 평가, 언어별 매시간 되풀이 일정 하나씩(두 일정 모두 이후 일시 중지)을 확인([결과](live-run.md#이전에-실행하지-않은-항목--2026-09-23)). 운영 승인은 별도 |
| [Agent Insights](labs/extensions/agent-insights.md) | C | 반복되는 trace 패턴과 사람의 결정 흐름을 검토하는 Preview 포털 경로 | 2026-09-24: SDK on-demand scan 1회(영문, trace 22개, insight 4개). 포털 경로는 실행하지 않음 |
| [모델 퇴역·이전과 Router 절충](labs/extensions/model-operations.md) | C | 고정 모델 비교와 Router 관찰 | 2026-09-16 `gpt-5.6-luna`: 지원되는 임시 모델과 고정 버전 기록. Router 이전은 주장하지 않음 |
| 타사 모델 비교 가이드 | C | 모델 운영과 평가 워크북에서 같은 게이트로 OpenAI 외 Foundry Model 하나를 추가하는 방법 설명 | 미실행: 실습 프로젝트에 OpenAI 외 배포가 없고, 만들려면 담당자 승인이 필요함. 2026-09-25 읽기 전용 확인: `grok-4-1-fast-reasoning`, `Mistral-Large-3`가 남은 할당량과 함께 제공됨 |
| [OpenAPI·Code Interpreter](labs/extensions/additional-tools.md), [Toolkit](labs/extensions/developer-toolkit.md), [거버넌스·네트워크](labs/extensions/governance-networking.md) | B/C | 실행 가능한 도구와 명시적 담당자 경계 | 2026-09-16 `gpt-5.6-luna`: 영문 API·파일 결과, 도구, 범위 지정 역할 확인 기록. 사설망은 테스트하지 않음 |
| 실제 회사/Microsoft 365 접근 | 전문 | 제외 | 계속 제외 |
| [Fine-tuning·음성/멀티모달·브라우저/컴퓨터 업무 동작](labs/extensions/specialist-scope.md) | 전문 | 설계·범위만 | 별도 전문 과정. 구현을 암시하지 않음 |

## 이미 있는 근거

[2026-09-24 `gpt-6-sol` 실행](live-run.md), 그 [녹화](video-summary.md), [검증 범위](reference/validation.md)는
각자의 날짜·코드 버전·결과를 유지합니다. 2026-09-24 녹화를 확장 모듈 실행으로 표시하지 않습니다.
2026-09-16 확장 결과·영상(이전 `gpt-5.6-luna` preset)은 작업 트리에서 삭제했습니다.
위 표의 2026-09-16 결과는 과거 기록이며 `gpt-6-sol`의 근거가 아닙니다. 2026-09-23~25로 적은 행은 해당 항목의 `gpt-6-sol` 근거입니다.

새 근거에는 언어, source commit·패키지, 실제 모델과 agent 버전, 질문·데이터 세트·corpus·평가자 hash,
모든 응답과 실패, 리소스 정리 상태가 있어야 합니다.
다시 만든 성공 화면이 아니라 요청과 실제 원본 활동을 기록합니다.
인증·암호·token·MFA 상호작용은 녹화에서 제외합니다.

## Straightforwardness 기준

실행 가능한 모듈마다 권장 첫 경로 하나, 정확한 입력 파일·값, 완전한 명령, 관찰 가능한 완료 기준,
중단·복구 경로, 명시적인 다음 링크가 있어야 합니다. 대안은 첫 성공 뒤에 두어 첫 경로와 경쟁하지 않게 합니다.
비용·역할·기능 접근 조건은 부작용이 있는 첫 명령 **앞에** 나옵니다.

문서 링크가 동작하거나 fixture가 통과했다는 이유로 모듈을 완료 처리하지 않습니다.
읽기 전용 검사, 실제 모델 호출, 로컬 전용 시연, Preview 서비스 실행, 녹화한 액션은 따로 보고합니다.

**다음:** [실제 결과](live-run.md) · [녹화](video-summary.md) · [경로 선택](paths.md).
