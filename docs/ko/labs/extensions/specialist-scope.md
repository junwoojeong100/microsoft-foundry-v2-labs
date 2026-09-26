# 전문 기능: 설계 경계와 실제 실행을 구분하기

[English](../../../labs/extensions/specialist-scope.md) | **한국어**

**참고·담당자 계획 · 2026-09-16 기준.**

**근거 상태:** 설계와 범위만 다루며 이 페이지의 내용은 실행하지 않았습니다.

아래 기능은 Foundry 기능 지도에 속하지만 별도 데이터·ID·인프라·런타임이 필요하며 A/B/핵심 C의 숨은 필수 조건이 아닙니다.

**첫 회차:** 행 하나를 선택해 기록 폴더의 `specialist-scope.txt`를 작성하고 **설계만**으로 인계합니다.
새 서비스·계정·데이터 연결·모델 호출은 필요하지 않습니다.

| 기능 | 이해할 것 | 이 과정의 실행 경계 |
|---|---|---|
| Fabric IQ | 게시 data agent, semantic model/ontology, 자산별 delegated/OBO/workload ID | 별도로 준비한 합성 자산만 가능, 회사 분석 금지 |
| Work IQ | 사용자 context·동의·비용·Microsoft 365 동작 | 회사/Microsoft 365 연결·데이터 접근 없음 |
| Autopilot / Agent 365 | agent ID와 user account, blueprint/instance, 관리자·거버넌스 | 개념/설계만, mailbox·Teams·조직 계정 생성 없음 |
| Private skill catalog | API Center 등록·허용 도구·검색·평가 | 별도 인프라, Toolbox에 Skill 연결만으로 생성되지 않음 |
| Fine-tuning | prompt/retrieval/optimizer의 한계와 가중치 변경 | 별도 전문 과정, 현재 dev/holdout을 자동 학습 데이터로 쓰지 않음 |
| Content Understanding receipts | field extraction 설계, validation, 사람 검토 | 본인 언어의 준비된 학습자 자료에서 `policies/RECEIPT-01.txt`를 읽음. 영수증 이미지가 아닌 합성 규정이며, 업로드·서비스 호출 없이 설계만 |
| Voice-based prompt agents | Portal quickstart, realtime media, SDK 버전 경계 | 설계만. Python voice SDK 지원은 이 edition pin 밖인 `azure-ai-projects` 2.7.0 beta |
| Microsoft 365 Copilot/Teams 게시 | 안정 endpoint, active version, tenant 게시 workflow | 개념만. M365 tenant와 별도 승인 필요 |
| Voice / Realtime / image | 모달리티별 모델·protocol·안전·평가 | 별도 승인, text agent 성공을 멀티모달 검증으로 표시하지 않음 |
| Browser / computer actions | 명시적 동작 승인·신뢰 목적지·감사 | 업무 시스템 동작이나 인증 정보 녹화 없음 |

## 설계 워크시트

기능 하나의 목적, 허용된 **합성** source, 실제 호출 ID, resource/region/SDK,
기대 출력, 평가 기준, 비용 담당자와 정리 계획을 기록합니다.
필수 자산이 없으면 **미준비 / 미실행**으로 적고 데이터나 답변을 만들어 넣지 않습니다.
설계 note만 작성합니다. 이 페이지를 위해 명령을 실행하거나 Azure 서비스를 호출하거나 파일을 업로드하지 않습니다.

이전 workshop을 복제한 것만으로 SDK·role·Preview 조건이 유지된다고 가정하지 않습니다.
현재 공식 계약과 [IQ 워크북](../../reference/iq-workbook.md)의 공통 ID/데이터 경계를 확인합니다.

## 실행 증거가 아닌 것

문서 읽기, routing 그림, portal 기능 목록, 과거 영상 재생은 새 연결/protocol 실행이 아닙니다.
실제 연결이 있어도 의미적 정확성·모든 사용자 인가·안전·운영 준비를 자동 증명하지 않습니다.

## 2026-09-24 추가된 설계 전용 prompt

| 연습 | 기록할 설계 note |
|---|---|
| `policies/RECEIPT-01.txt`에 연결한 Content Understanding receipt extraction | 준비된 합성 규정으로 `date`, `amount`, `merchant`, `category` field와 validation rule 설계. 불확실하거나 정책상 중요한 값은 사람 검토로 보냄. 영수증 이미지·업로드·서비스 호출 없이 설계 note 인계 |
| Voice-based Prompt Agent | Portal quickstart 선행 조건과 기대 사용자 경험 mapping. Python voice-agent SDK 지원은 이 edition pin 밖인 `azure-ai-projects` 2.7.0 beta에만 있음을 기록 |
| Microsoft 365 Copilot/Teams 게시 | 안정 endpoint와 active version 개념 설명. M365 tenant, app/게시 검토, 사용자 governance 필요성을 기록. 게시 작업 없음 |

**다음:** 선택한 범위와 한계를 [Lab 11](../11-capstone.md)에 기록합니다.
[Foundry 기능 지도](https://learn.microsoft.com/azure/foundry/concepts/capability-reference) ·
[Autopilot ID](https://learn.microsoft.com/azure/foundry/agents/concepts/autopilot-overview).
