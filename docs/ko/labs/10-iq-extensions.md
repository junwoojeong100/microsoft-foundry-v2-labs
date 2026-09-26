# Lab 10. Fabric IQ, Work IQ, Toolbox 확장

[English](../../labs/10-iq-extensions.md) | **한국어**

**선택 심화입니다. 첫 회차는 설계만 하며 실제 회사/Microsoft 365 데이터는 이 워크숍의 범위 밖입니다.**

다음: A/B → [Lab 11](11-capstone.md) · 선택 선행: [Lab 06](06-knowledge.md) · [학습 경로](../paths.md)

## 시작 전

**이번 순서:** 선택 확장입니다. A/B는 이 모듈 없이 Lab 11에서 끝낼 수 있습니다.

**준비물:** 동봉한 정책 원본과 본인의 기록 폴더뿐입니다. 2–5절은 담당자의 계획을 위한 참고 자료이며,
이 랩을 마치려고 없는 자산을 만들거나 서비스를 연결하라는 지시가 아닙니다.

**다음으로 갈 기준:** 설계 결과는 설계로 기록합니다. Work IQ/Fabric 연결을 실행했다고 표시하지 않습니다.

**막히면:** 빠진 원본·identity·승인을 **미준비 / 미실행**으로 기록하고 Lab 11로 돌아갑니다.
이 설계 실습을 위해 Fabric/Microsoft 365에 로그인하거나 없는 자산을 만들지 않습니다.

[한 번만 하는 준비와 학습자 파일](../setup.md).

## 세 IQ를 같은 API로 보지 않기

| 구분 | 주된 맥락 | 이번 통합 가이드의 기본 범위 |
|---|---|---|
| Foundry IQ | 기업 지식 검색, knowledge source/base | Lab 06의 합성 Search 경로. 이 페이지에서는 검색을 실행하지 않음 |
| Fabric IQ | 의미 모델·분석·ontology·OneLake·data agent | 연결 설계만. 분석 자산은 제공하지 않음 |
| Work IQ | Microsoft 365 업무·협업 맥락 | 설계만. 이 과정에서는 Microsoft 365 연결·데이터 접근 없음 |

“둘 다 IQ니까 같은 키를 넣으면 된다”거나 “Copilot 라이선스가 있으니 백엔드가
app-only로 자유롭게 호출할 수 있다”는 결론을 내리지 않습니다.

## 1. 합성 설계 실습(서비스 접근 없음)

실제 서비스에 로그인하지 않고 다음 세 질문의 라우팅 표를 만듭니다.

| 질문 | 적절한 근거 | 필요한 권한/검증 |
|---|---|---|
| 출장 숙박 한도가 얼마인가? | 버전이 있는 정책 문서 / Foundry IQ | 원문·적용일·인용 |
| 이번 분기 부서별 출장비 합계는? | 합성 분석 모델 / Fabric | 집계 정의·사용자 데이터 권한 |
| 출장 검토 회의에서 합의한 내용은? | 승인된 업무 맥락 / Work IQ | 사용자 동의·위임 권한·민감정보 보호 |

본인의 `iq-routing-design.txt`에 표를 복사하고 행마다 **원본 준비 여부 / 필요한 identity / 실행·미실행**을 적습니다.
기본 실습에는 번들 정책 원본만 있으며 분기별 분석·회의 dataset은 제공하지 않습니다.
Fabric과 Work IQ는 **설계만 / 미실행**으로 표시하고 응답 JSON이나 회사 데이터를 만들어 넣지 않습니다.

**화면 확인:** 이 과제의 결과는 설계 기록뿐이며 연결 상태 flag나 서비스 결과가 아닙니다.
이전 Lab 06 근거는 따로 보관합니다. 첫 회차는 끝났으므로 [Lab 11의 선택 모듈 인계](11-capstone.md#path-c)로 이동합니다.
아래 참고 자료는 추가 필수 단계가 아닙니다.

<details>
<summary>참고 전용 — 선행 조건을 계획하되 이 랩을 마치려고 없는 서비스를 만들지 않습니다</summary>

## 2. Fabric 연결 — 준비된 합성 자산이 있을 때만

필요 조건을 먼저 기록합니다.

1. 합성 데이터만 있는 Fabric workspace와 현재 지원되는 capacity.
2. 게시된 Data Agent/의미 모델과 해당 데이터 원본의 읽기 권한.
3. Foundry/Search/Fabric의 tenant·network·지역·data processing 요구사항.
4. MCP 또는 Foundry tool/knowledge source의 현재 지원 방식.
5. 자산별 identity: ontology/semantic model 경로는 delegated/OBO context가 필요하고, 게시된 Data Agent MCP는 별도로 승인된 service principal을 지원할 수 있습니다.
6. capacity 활성 시간, 호출 비용, 종료·복원 계획.

자산이 없다면 **미준비 / 미실행**으로 기록하고 복구 단계로 새로 만들지 않습니다.
[공식 Fabric Data Agent 튜토리얼](https://learn.microsoft.com/fabric/data-science/data-agent-end-to-end-tutorial),
[IQ 워크북](../reference/iq-workbook.md),
[Fabric IQ 가이드](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/fabric-iq)는
별도로 승인한 합성 프로젝트를 위한 담당자 참고 자료이지 첫 회차의 과제가 아닙니다.

**별도 승인 실험의 근거:** 실제 합성 질문, 선택한 agent/원본, 응답·근거, 자산별 호출 identity 검증 결과.
관리자 계정으로 한 번 성공했다고 모든 사용자에게 권한이 있는 것은 아닙니다.

## 3. Work IQ — 명시적 옵트인과 추가 과금

**이 워크숍에서는 계획만 합니다.** 아래 조건을 충족해도 여기서 Microsoft 365에 접근해도 된다는 뜻이 아닙니다.
별도 프로젝트의 담당 관리자는
[Work IQ knowledge-source 요구사항](https://learn.microsoft.com/azure/search/agentic-knowledge-source-how-to-work-iq)을 검토합니다.
tenant enablement, 실제 사용자 로그인과 할당된 사용량 기반 과금,
delegated `WorkIQAgent.Ask` 및 관리자/사용자 동의, 네트워크·tenant·지원 경계,
데이터 이동·보존·규제와 사용자별 접근/삭제 정책을 확인합니다.
Preview Work IQ는 단순히 읽는 것이 아니라 **작업을 수행할 수 있습니다**.

이 리포에는 실제 Work IQ를 자동 활성화하거나 계정/서비스 principal을 생성하는 스크립트가 없습니다.
개인 계정을 강제로 로그인시키거나 Graph/Microsoft 365 token을 복사해 넣지 않습니다.
M365 Copilot 보유 여부만으로 위 조건을 충족했다고 판단하지 않습니다.
2026년 9월 15일 계약에는 사용자별 할당이 있는 Copilot Studio 사용량 기반 과금 plan, tenant enablement, user assertion,
`WorkIQAgent.Ask` 위임 동의, `2026-08-01-preview` 경로용 고객 소유 Entra 앱/페더레이션 자격 증명이 포함됩니다.
`applicationId`는 client ID이고 `federatedCredentialId`는 credential object ID입니다.
이전의 같은 tenant 예시를 일반화하거나 사용자 context를 host identity로 대체하지 않습니다.

**중단 조건:** 다른 프로젝트가 필요한 동의·과금 조건을 갖췄더라도 이 경로의 Work IQ는 **설계만 / 미실행**으로 남깁니다.
워크숍을 마치려고 Microsoft 365를 연결하지 않습니다.

## 4. Toolbox / 원격 MCP / 웹

기본 [Lab 04](04-agents-tools.md)는 로컬 MCP입니다. 동봉 데이터로 실행하는 확장을 원한다면
Lab 06 선행 조건을 갖춘 뒤 [관리형 Toolbox](extensions/toolbox.md)를 선택합니다.
아래 행은 계획 예시이지 이 페이지에서 연결할 서비스가 아닙니다.

| 추가할 것 | 연결 전에 정할 것 |
|---|---|
| Microsoft Learn MCP | 신뢰할 서버 URL, 노출 도구, 호출 예산 |
| Web Search | 허용 도메인, 최신성, 출처 URL, query의 민감도 |
| 사내 API | OpenAPI/MCP 스키마, 입력 검증, 사용자별 권한 |
| 변경 작업 | 별도 승인, idempotency, 감사·보상 동작 |

Web IQ와 일반 Web Search를 같은 기능으로 표시하지 않습니다.
2026-09-24 확인: `azure-ai-projects` 2.6.0에 Web IQ Preview tool(`WebIQPreviewTool`)이 추가됐습니다.
이 워크숍에서는 다루지 않습니다. 다른 Preview web grounding처럼 승인된 domain만 사용하고,
freshness/source URL을 기록하며, 민감 query를 보내지 않습니다.
도구가 등록되었다는 것과 실제 권한으로 올바른 결과를 받았다는 것도 구분합니다.
`FoundryToolbox`는 prerelease hosting 패키지에 속하며 upstream 프로젝트 연결을 만들지 않습니다.
실제 수명 주기·자격 증명·Fabric·Work IQ 경계는 [IQ 확장 워크북](../reference/iq-workbook.md)을 확인합니다.

## 5. Richer IQ Preview — GA 코드와 분리

현재 richer 경로는 `2026-08-01-preview`를 확인합니다.
메시지 기반 planning, 추론 노력, synthesis, 추가 source는 GA `2026-04-01`과 body가 다릅니다.
이 리포의 `seed-search --iq`에 Preview 필드를 끼워 넣지 않습니다.

번들 `iq-chat` preset을 벗어난 별도 Preview 실험에만 새 복사본·접두사·설정과 [공식 API migration](https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-migrate)을
따릅니다. Preview Search SDK가 필요하면 별도 환경에 해당 버전을 설치합니다.
기본 GA 실습의 패키지를 한꺼번에 업그레이드하지 않습니다.
사용되지 않는 planner 환경변수 대신 실제 KB 모델 연결을 설정합니다.
Managed identity 지원 여부와 Preview 여부는 별개입니다.
[IQ 모델 identity 가이드](../reference/iq-model-identity.md)에 검증한 계획·합성 경로와 버전별 요청 필드를 설명합니다.
번들 Search 원본에는 새 모델 연결을 설계하지 말고 Lab 06의 **`iq-chat` Luna/SMI preset**을 선택합니다.
이 preset은 source를 소유한 원래 작업 폴더에서 같은 언어·접두사·소유권 ledger로 실행하고 GA base는 그대로 둡니다.
고정 HTTP 클라이언트를 사용하므로 Preview Search SDK를 추가 설치할 필요가 없습니다.

</details>

Lab 10은 선택 단원이며 2026-09-24 `gpt-6-sol` 녹화에 포함하지 않았습니다. [전체 액션 인덱스](../action-captures.md) · [녹화 영상](../video-summary.md)

## 종료

설계만 했다면 cloud 자산을 만들지 않았습니다. 라우팅 기록과 **미실행** 항목을 Lab 11용으로 보관하고,
사용하지 않은 서비스의 capacity·billing·consent를 바꾸지 않습니다.
별도로 승인한 실행 모듈에서 돌아왔다면 그 모듈의 소유 리소스 정리 절차를 따릅니다.
다른 조의 연결이나 조직 전체 설정을 변경하지 않습니다.

다음: [선택한 모듈 인계](11-capstone.md#path-c).
