# Lab 10. Fabric IQ, Work IQ, Toolbox 확장

[English](../../labs/10-iq-extensions.md) | **한국어**

**선택 심화입니다. 기본 실습은 실제 Fabric/Microsoft 365 계정에 접근하지 않고 완료됩니다.**

다음: A/B → [Lab 11](11-capstone.md) · 선택 선행: [Lab 06](06-knowledge.md) · [학습 경로](../paths.md)

## 시작 전

**이번 순서:** 선택 확장입니다. A/B는 이 모듈 없이 Lab 11에서 끝낼 수 있습니다.

**준비물:** 합성 라우팅 설계만 기본이며 외부 서비스에는 별도 자산·승인이 필요합니다.

**다음으로 갈 기준:** 설계 결과는 설계로 기록합니다. Work IQ/Fabric 연결을 실행했다고 표시하지 않습니다.

**막히면:** 동의·과금·사용자 context 조건이 없으면 멈추며 회사 데이터를 기본 연결하지 않습니다.

[한 번만 하는 준비와 학습자 파일](../setup.md).

## 세 IQ를 같은 API로 보지 않기

| 구분 | 주된 맥락 | 이번 통합 가이드의 기본 범위 |
|---|---|---|
| Foundry IQ | 기업 지식 검색, knowledge source/base | 합성 Search index의 GA retrieval |
| Fabric IQ | 의미 모델·분석·ontology·OneLake·data agent | 합성 자산을 준비한 경우의 별도 연결 설계 |
| Work IQ | Microsoft 365 업무·협업 맥락 | 기본 비활성화; 실제 사용자 연결은 별도 승인 |

“둘 다 IQ니까 같은 키를 넣으면 된다”거나 “Copilot 라이선스가 있으니 백엔드가
app-only로 자유롭게 호출할 수 있다”는 결론을 내리지 않습니다.

## 1. 누구나 할 수 있는 합성 설계 실습

실제 서비스에 로그인하지 않고 다음 세 질문의 라우팅 표를 만듭니다.

| 질문 | 적절한 근거 | 필요한 권한/검증 |
|---|---|---|
| 출장 숙박 한도가 얼마인가? | 버전이 있는 정책 문서 / Foundry IQ | 원문·적용일·인용 |
| 이번 분기 부서별 출장비 합계는? | 합성 분석 모델 / Fabric | 집계 정의·사용자 데이터 권한 |
| 출장 검토 회의에서 합의한 내용은? | 승인된 업무 맥락 / Work IQ | 사용자 동의·위임 권한·민감정보 보호 |

본인의 `iq-routing-design.txt`에 표를 복사하고 행마다 **원본 준비 여부 / 필요한 identity / 실행·미실행**을 적습니다.
기본 실습에는 번들 정책 원본만 있으며 분기별 분석·회의 dataset은 제공하지 않습니다.
Fabric과 Work IQ는 **설계만 / 미실행**으로 표시하고 응답 JSON이나 회사 데이터를 만들어 넣지 않습니다.

**화면 확인:** 이 과제의 결과는 본인의 설계 기록입니다. 연결 상태 flag를 출력하거나 실제 연결을 입증하는 명령은 없습니다.
선택한 범위가 설계뿐이면 여기서 멈추고 [Lab 11](11-capstone.md)로 이동합니다.

<details>
<summary>선택 준비 참고 — 외부 서비스는 별도 자산·권한·비용 승인이 필요합니다</summary>

## 2. Fabric 연결 — 준비된 합성 자산이 있을 때만

필요 조건을 먼저 기록합니다.

1. 합성 데이터만 있는 Fabric workspace와 현재 지원되는 capacity.
2. 게시된 Data Agent/의미 모델과 해당 데이터 원본의 읽기 권한.
3. Foundry/Search/Fabric의 tenant·network·지역·data processing 요구사항.
4. MCP 또는 Foundry tool/knowledge source의 현재 지원 방식.
5. 필요한 delegated 사용자 인증/OBO와 실제 호출자의 권한.
6. capacity 활성 시간, 호출 비용, 종료·복원 계획.

자산이 없다면 [공식 Fabric Data Agent 튜토리얼](https://learn.microsoft.com/fabric/data-science/data-agent-end-to-end-tutorial)에서
합성 자산을 먼저 만듭니다. 자산 준비는 이 랩의 45–90분에 포함하지 않습니다.
자산별 연결 순서는 [통합 IQ 워크북](../reference/iq-workbook.md)과
[현재 공식 Fabric IQ 가이드](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/fabric-iq)를 사용합니다.
Data Agent MCP의 app-only 지원을 ontology/semantic model의 delegated/OBO 지원과 혼동하지 않습니다.

**완료 증거:** 실제 사용자의 질문, 선택된 Data Agent/데이터 원본, 응답·근거,
user-context/OBO 검증 결과. 관리자 계정으로 한 번 성공했다고 모든 사용자에게 권한이 있는 것은 아닙니다.

## 3. Work IQ — 명시적 옵트인과 추가 과금

현재 [Work IQ knowledge-source 가이드](https://learn.microsoft.com/azure/search/agentic-knowledge-source-how-to-work-iq)의
요구사항을 관리자가 먼저 확인해야 합니다.

- tenant enablement, 실제 사용자 sign-in, 사용자에게 할당된 usage-based billing.
- delegated `WorkIQAgent.Ask` 권한과 관리자/사용자 동의.
- tenant·네트워크·지원 경계, 데이터 이동/보존/규제 요구.
- 사용자별 데이터 접근과 차단/삭제 정책.
- 비용과 동작 범위: Preview Work IQ가 읽기뿐 아니라 **행동을 수행할 가능성**.

이 리포에는 실제 Work IQ를 자동 활성화하거나 계정/서비스 principal을 생성하는 스크립트가 없습니다.
개인 계정을 강제로 로그인시키거나 Graph/Microsoft 365 token을 복사해 넣지 않습니다.
M365 Copilot 보유 여부만으로 위 조건을 충족했다고 판단하지 않습니다.

**중단 조건:** 승인/과금/tenant/위임 권한/행동 범위 중 하나라도 불명확하면 실제 연결을 하지 않고
합성 라우팅 실습에서 멈춥니다.

## 4. Toolbox / 원격 MCP / 웹

기본 [Lab 04](04-agents-tools.md)는 로컬 MCP입니다.
원격 도구로 확장할 때는 승인된 Microsoft Learn 등 공개 문서 조회부터 시작합니다.

| 추가할 것 | 연결 전에 정할 것 |
|---|---|
| Microsoft Learn MCP | 신뢰할 서버 URL, 노출 도구, 호출 예산 |
| Web Search | 허용 도메인, 최신성, 출처 URL, query의 민감도 |
| 사내 API | OpenAPI/MCP 스키마, 입력 검증, 사용자별 권한 |
| 변경 작업 | 별도 승인, idempotency, 감사·보상 동작 |

Web IQ와 일반 Web Search를 같은 기능으로 표시하지 않습니다.
도구가 등록되었다는 것과 실제 권한으로 올바른 결과를 받았다는 것도 구분합니다.
`FoundryToolbox`는 prerelease hosting 패키지에 속하며 upstream 프로젝트 연결을 만들지 않습니다.
실제 수명 주기·자격 증명·Fabric·Work IQ 경계는 [IQ 확장 워크북](../reference/iq-workbook.md)을 확인합니다.

## 5. Richer IQ Preview — GA 코드와 분리

현재 richer 경로는 `2026-08-01-preview`를 확인합니다.
메시지 기반 planning, 추론 노력, synthesis, 추가 source는 GA `2026-04-01`과 body가 다릅니다.
이 리포의 `seed-search --iq`에 Preview 필드를 끼워 넣지 않습니다.

별도 실험 복사본·접두사·설정에서 [공식 API migration](https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-migrate)을
따릅니다. Preview Search SDK가 필요하면 별도 환경에 해당 버전을 설치합니다.
기본 GA 실습의 패키지를 한꺼번에 업그레이드하지 않습니다.
사용되지 않는 planner 환경변수 대신 실제 KB 모델 연결을 설정합니다.
Managed identity 지원 여부와 Preview 여부는 별개입니다.
[IQ 모델 identity 가이드](../reference/iq-model-identity.md)에 검증한 계획·합성 경로와 버전별 요청 필드를 설명합니다.
번들 Search 원본에는 새 모델 연결을 설계하지 말고 Lab 06의 **`iq-chat` Luna/SMI preset**을 선택합니다.
고정 HTTP 클라이언트를 사용하므로 Preview Search SDK를 추가 설치할 필요가 없습니다.

</details>

## 종료

설계만 했다면 cloud 자산을 만들지 않았습니다. 사용하지 않은 서비스를 정리하지 않습니다.
추가 연결을 제거/복원하고, 본인 Fabric capacity·Work IQ billing·session 상태를 확인합니다.
capacity를 멈추기 전에 공유 에이전트가 그 source를 여전히 참조하는지 점검합니다.
다른 조의 연결이나 조직 전체 consent를 임의로 삭제하지 않습니다.

Lab 10은 선택 단원이며 2026-09-24 `gpt-6-sol` 녹화에 포함하지 않았습니다. [전체 액션 인덱스](../action-captures.md) · [녹화 영상](../video-summary.md)

다음: A: [Lab 11로 이동](11-capstone.md) · B: [Lab 11로 이동](11-capstone.md)
