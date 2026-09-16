# 9월 16일 국문 확장 결과: 실제 실행과 한계

[English](../edition-results.md) | **한국어**

**국문 합성 입력으로 독립 실행·촬영한 결과입니다.**
영문 수치나 9월 15일 기본 과정 영상을 국문 확장 결과로 재사용하지 않았습니다.
동봉한 국문 정책과 dev만 사용했으며 holdout은 개발·오류 수집에 사용하지 않았습니다.

[국문 영상](edition-videos.md)은 **172개 동작·516장 무손실 캡처·영상 3개**입니다.
리부팅 전후 원본을 서로 다른 시간축의 녹화 파트로 보존했고, 인증 전환 두 구간은 공개 영상에서 제외했습니다.
원본 구간 363개의 최소 midpoint SSIM은 **0.983325**이며, 실제 로컬 재생과 15개 챕터의 seek 완료를 확인했습니다.
업로드 여부는 영상 페이지에서 별도로 확인합니다. [기계 판독용 결과·hash](../assets/edition-20260916-ko/live-results.json)도 제공합니다.

## 실제 결과

| 모듈 | 확인한 결과 | 주장하지 않는 것 |
|---|---|---|
| IQ chat | 별도 국문 Search/GA IQ와 MI chat 구성, 실제 planning/synthesis와 원래 reference | 기존 GA base 변경이나 모델 fallback |
| Toolbox/Skills | 직접 query·MAF 답변, 버전 변경/rollback, Toolbox v4·Skill v1의 실제 load/search/call | 목록 조회만으로 downstream 검색 성공 |
| 대화 평가 | 두 독립 3턴 대화, 업무 **6/6**; native Groundedness/Coherence 각각 턴 **6/6**, 대화 **2/2** | 서로 다른 분모가 품질 개선이라는 주장 |
| Optimizer | 한 run, baseline과 두 후보 모두 보존; **개선 없음**, 참조 binding 결함 확인, 승격 없음 | 서비스 점수가 유효한 원문 grounding이나 운영 인수라는 주장 |
| 로컬 복구 | 실제 SDK 종료·재시작과 원래 response/gate/output ID 유지, 명시적 모의 결정 | 실제 사람 승인, Azure 실행 또는 production crash 검증 |
| Memory | 저장·alpha/beta 회상·수정; 재개 시 원래 항목은 이미 없음; 내 빈 store 삭제 확인 | 이미 없던 항목을 새로 삭제했다는 주장, 사용자 간 인가/정확한 TTL SLA |
| A2A | 원래 HTTP400 보존 후 같은 target/버전/프로토콜의 진단에서 paired call/output 확인 | legacy event 이름만으로 wire protocol 확정, packet capture |
| OpenAPI/Code Interpreter | 국문 index 범위 권한 수정 후 같은 API에서 원문 6건; 실제 생성 CSV 6행 대조·임시 code 자원 정리 | 다른 검색 경로나 로컬 CSV를 실제 도구 결과로 대체 |
| Hosted Toolbox | 원격 v1의 completed SSE와 정확한 package, 근거 파일 8개, exact trace **146행** 확인 | CLI exit 0/readiness만으로 완료, 모든 child span export |
| Routines | 원래 수동 전달 Finished; 답변 조회는 **404**; 비활성화·소유 routine 삭제 확인 | 원래 답변 내용 또는 미래 timer 발화 검증 |
| 안전 제어 | 실제 policy와 Hosted v2 연결 확인; D01 완료, D06은 **Tool Search no-match로 failed** | failed를 platform guardrail 차단이나 성공한 답변으로 포장 |
| OIDC/CI | 촬영 당시 설정 검증; 게시 후 실제 OIDC 배포·국문 dev **6/6**, 오류 **0** 확인 | 영문 CI 결과, native judge 또는 운영 인수 |

대화 평가의 실제 judge 입력에서도 원래 정책 JSON을 확인했습니다.
턴 평가에는 query 메시지 배열, 전체 평가에는 formatted messages에 원문이 들어 있습니다.
이는 아래 Optimizer의 답변 자기 비교와 다른 입력 계약입니다.

## Optimizer: 원래 점수와 잘못된 참조를 함께 읽기

`opt_1a4531cbb37540fea56b947fdf024b7a`의 표시 점수는 baseline **0.938**,
candidate_1 **0.896**, candidate_2 **0.938**입니다. 최고 점수가 baseline과 같으므로 개선이 없었습니다.
세 묶음 각각 원래 dev 6행과 모든 지침·평가 결과를 보존했습니다.

서비스는 각 묶음에 Groundedness 6/6, Relevance 5/6을 보고했지만,
**Groundedness 입력 18개 모두 `context`가 생성 답변 자체였습니다.**
업로드한 정책 원문을 참조한 평가가 아니므로 해당 Groundedness 결과를 품질·승격 gate로 인정하지 않았습니다.
저장된 영문 baseline 6개에서도 같은 결함을 확인했으며, 영어 모델을 다시 호출하지 않았습니다.
어려운 행·기준·입력을 바꾸거나 후보를 승격하지 않았습니다.

보고된 토큰은 agent 67,245, judge 157,726, reflection 18,831입니다.
화면의 US$0.27 예상 / US$0.90 최대는 추정치이지 실제 청구액이나 강제 상한이 아닙니다.
두 언어 실험 뒤 승인된 임시 GPT-5.5 배포만 정리했으며 응답·judge·embedding 배포는 유지했습니다.

## 실패를 숨기지 않은 수정과 경계

빈 azd 폴더의 template 선택/중첩 문제와 기존 프로젝트 endpoint alias 누락을 보존하고,
정확한 package를 별도 폴더에 연결하는 공통 초기화 helper로 수정했습니다. 과거 저장소의 `azure.yaml`은 재사용하지 않습니다.
녹화 PTY의 긴 입력이 일부만 전달되는 문제도 재현·수정했으며 Azure 실패로 바꾸어 설명하지 않습니다.

안전 실습 D06에서는 `tool_search`가 같은 질의에 두 번 `No tools matched`를 반환했습니다.
workshop의 도구 오류 gate가 후속 유창한 응답을 거부해 실제 Hosted 상태는 `failed`였습니다.
원래 HTTP/SSE, 두 실패 도구 결과와 세션 파일을 보존했고 요청을 성공처럼 만들려고 반복하지 않았습니다.
이는 실제 guardrail 개입 증거가 아닙니다.

Hosted v1의 네 모델 response ID 중 trace에서 확인된 ID는 세 개입니다.
내려받은 모델 호출 원본 네 개는 보존했지만, trace 146행이 모든 child span의 export를 보장한다고 주장하지 않습니다.
각 소유 Hosted 세션은 근거 보존 뒤 중지했습니다.

실제 회사/Microsoft 365 데이터, 사설망 변경, Router 이전, continuous evaluation과 red-team 실측은 이 결과에 포함하지 않습니다.
[국문 영상 상태](edition-videos.md), [기능 범위](coverage.md), [별도 영문 결과](../edition-results.md)를 함께 확인합니다.

## 게시 후 실제 CI 확인 — 2026-09-17

[OIDC release 실행 35121162793](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35121162793)의
두 번째 시도에서 `336325d` 소스로 `mfv2-course-20260916-ci-hosted` v1을 배포했습니다.
원래 국문 dev D01–D06을 Luna 한 모델로 실행해 **6/6, 오류 0**을 확인했습니다.
다운로드한 artifact의 dataset/corpus/response/runtime/rubric hash를 검증하고 업무 검사를 로컬에서 다시 계산했습니다.
CI가 만든 정확한 세션은 `idle`이며, 별도 Azure 읽기에서도 같은 상태를 확인했습니다.

첫 시도의 OIDC subject 불일치와 앞선 GitHub 설정/의존성 실패는 이력에 남아 있습니다.
federation의 subject만 실제 저장소 고유 ID와 환경 claim에 맞췄으며 trust 범위·역할·GitHub 보안 설정은 넓히지 않았습니다.
이 결과는 **영상 제작 후의 별도 국문 CI 검증**입니다. 영문 응답, native 평가, trace export 전체 또는 사람의 운영 승인을 뜻하지 않습니다.
