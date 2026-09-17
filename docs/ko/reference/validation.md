# 검증 범위와 실제 실행

[English](../../reference/validation.md) | **한국어**

**설치·offline 계약·실제 Azure 실행·모델 품질·미디어 검수는 서로 다른 검증입니다.**
국문과 영문은 별도 label과 촬영 원본을 사용합니다. 이전 영상이나 upstream 성공을 새 결과로 재분류하지 않습니다.

<a id="repository-straightforwardness"></a>

## 저장소 straightforwardness: 가이드·코드·설정 — 2026-09-17

가이드 진입점·전체 언어 쌍 61개·CLI 명령군·공통 소스 계약·설정 템플릿·CI workflow 두 개를 점검했습니다.
기존 A/B 순서와 선택 C의 범위는 유지합니다.

| 불편한 지점 | 개선 |
|---|---|
| 기본 B에서 터미널 JSON을 편집기로 12번 복사해야 함 | 각 명령에 덮어쓰지 않는 `--output` 경로 추가. 같은 파일 12개가 검토·인계로 연결됨 |
| 긴 CLI 사용법·공통 설명 때문에 첫 행동과 일부 심화 명령을 찾기 어려움 | 짧은 `COMMAND` 사용법·오프라인 시작 순서·서로 다른 실제 명령 설명·전체 선택 명령/소스 찾기 표 |
| 잘못된 UUID·출력 한도가 설정 이름 없는 파서 오류로 표시됨 | 공통 UUID 검사와 명시적인 정수/범위 오류. 모델·identity·허용 범위는 유지 |
| 첫 설정과 심화 값이 섞이고 참고 템플릿에 미정의 agent 변수가 있음 | 기본/Search/선택 구간 번호·Toolbox 설정 설명·기존 준비 도우미와 일치하는 참고 manifest |
| 로컬 matrix smoke가 소스의 과거 azd 프로젝트를 자동 선택할 수 있음 | smoke 출력·azd 호출 전에 `--azd-directory` 요구. 원격 endpoint/version 선택은 유지 |
| 문서 예제마다 같은 명령 트리를 다시 만듦 | 검사당 parser 하나 재사용. 명령·언어·출력 파일명 일치는 계속 엄격히 검사 |

회귀 검사는 실제 로컬 JSON 저장·두 언어 경로·요청 전 덮어쓰기/범위 거절·저장 경합 시 stdout 보존·
요청 실패·정확한 설정 경계값·명시적인 로컬 smoke 범위를 확인합니다.
영문 소스를 먼저 수정한 뒤 국문과 완료 hash를 기록합니다.
**B의 필수 JSON 수동 복사 12회**를 없앤 것이며 사람의 검토나 업무 게이트는 없애지 않습니다.
초심자 완주 시간이나 새 사용성 점수를 측정한 것은 아닙니다.

**로컬 검증:** site package 없이 Python 3.13·3.14에서 offline 테스트가 **각 253개** 통과했고,
설치한 SDK와 명시적인 stub 전송을 사용하는 테스트 **67개**도 통과했습니다.
Ruff 0.16.6 lint/format·두 Python 버전의 compilation·의존성/import 검사·두 canonical 학습자 번들도 통과했습니다.
문서 검사는 Markdown 123개·언어 쌍 61개·CLI 예제 330개·번역 보류 0개입니다.

**이번 개정의 실제 Azure 검사: 미실행.** 모델/judge 호출·provision·배포·역할/기본 구독 변경·촬영·
회사/Microsoft 365 데이터 접근은 하지 않았습니다.
Canonical 지침·평가 데이터·정책·fixture·기존 미디어는 그대로입니다.
Git에서 제외되는 개인 `.env`, `.azure/`, `azure.yaml`, 기존 outputs도 보존합니다.
이전 Azure 결과가 바뀐 소스 hash를 검증한 것은 아닙니다.

## IQ Chat 정상 설정 화면 — 2026-09-17

[Lab 06의 새 화면](../labs/06-knowledge.md#iq-chat-model)은 Luna·낮음·응답 합성과 해당 합성 source의 활성 상태가
저장된 기존 chat KB입니다. 모델 없는 과거 GA 폼의 미선택 오류와 이 준비 완료 상태를 구분하도록 안내를 고쳤습니다.
새 배포 없이 현재 Foundry 모델 카탈로그도 확인했습니다. 빠른 카탈로그에 Luna가 없어도 저장된 Luna 연결은 정상 표시됩니다.

**실제 포털 관찰과 배포 정보의 읽기 확인**이며 새 모델 호출이나 평가 결과가 아닙니다.
회색 MI 안내는 그대로 남겼고, 인증 오류나 권한 확인의 증거로 바꾸어 설명하지 않습니다.
새 PNG는 실제 설정 영역을 직접 캡처했으며 텍스트 교체·오류 숨기기·이미지 편집을 하지 않았습니다.
[캡처 기록](../../assets/iq-chat-20260917/captures.json)에 언어·선택값·이미지 hash·검증 한계를 이전 영상과 분리해 기록합니다.

**Offline 검증:** 새 캡처 hash·필수 선택값·과거 이미지의 범위 구분을 포함해 Python 3.13·3.14에서 테스트가 **각 235개** 통과했습니다.
Ruff 0.16.6 lint/format·compilation·두 학습자 번들도 통과했습니다.
문서 검사는 언어 쌍 61개·CLI 예제 328개·번역 보류 0개입니다.

## 수동 평가부터 인계까지 — 2026-09-17

A/B 진입과 기본 랩을 확인하면서 A의 6문항 평가에 남은 모호함을 찾았습니다.
[Lab 03의 실제 저장 지침 사본](../labs/03-prompt-agent.md#path-a)·[Lab 07 평가](../labs/07-evaluation.md#path-a)·
학습자 ZIP의 기록 양식·최종 인계를 연결해 보완했습니다.

| 공백 | 보완 |
|---|---|
| 여러 평가 행에 정확한 필수 원문이 없고 D03/D06에는 적용 한도도 빠짐 | 선택 언어의 canonical dev 금액·필수 인용과 6행 모두 일치. 정답 ID를 실제 응답 칸에 채워 넣지 않도록 명시 |
| 한 평가표에 버전이 섞이거나 candidate에 baseline 답변이 남을 수 있음 | 6문항마다 저장 버전 하나, 이름이 정해진 지침 사본, 정당한 변경이 있을 때만 새 빈 candidate 사용 |
| 요청 실패·미실행과 평가 완료를 통과로 오해할 수 있음 | 6문항 분모 유지, 오류/미실행 수·미완료 명시, 전체 통과/변경 없음도 유효한 종료 상태로 인정 |

**Offline 결과:** 두 언어의 판정 기준·지침 사본/양식/인계 연결을 포함해 Python 3.13·3.14에서 테스트가 **각 232개** 통과했습니다.
Ruff 0.16.6 lint/format·두 Python 버전의 compilation·결정적 학습자 번들·문서 검사도 통과했습니다.
언어 쌍 61개·workshop CLI 예제 328개·번역 보류 0개입니다.

**검증 범위:** 초심자 완주 시간이나 새로운 사용성 점수를 검증한 것은 아닙니다.
새 Azure 호출·배포·역할 변경·촬영은 하지 않았으며 canonical 지침·평가 데이터·정책·기존 미디어는 그대로입니다.
아래 이전 검토의 검사 수와 실제 실행 결과는 당시 범위를 유지합니다.

<a id="learner-action-review"></a>

## 학습자 행동·인계 점검 — 2026-09-17

**영문·국문 기본/확장 랩 전체 56쪽**, 진입·준비·경로 안내와 실행 참조를 다시 확인했습니다.
무엇을 복사하고, 다음 단계 전에 무엇을 저장하며, 다음 실습의 설정을 바꾸지 않고
현재 실험을 마치는 방법에 집중했습니다.

| 공백 | 보완 |
|---|---|
| 셸 명령·설정 블록·자리표시자·반환 flag의 해석이 필요함 | 공통 [코드 블록 읽는 법](../labs/00-start.md#reading-code-blocks)·[결과의 의미](commands.md#reading-results)·쉬운 이름 용어 설명 |
| 여러 요청 뒤에야 출력 JSON 파일명이 나오고 B 최종 목록에 모델 출력·workflow 검토가 빠짐 | B의 출력 12개마다 저장 지점 표시, 전체 [인계 목록](../labs/11-capstone.md#b-evidence) 제공 |
| 첫 agent의 D03/D05 확인이 이후 평가 기준보다 불명확함 | 같은 canonical dev의 한도와 필수 인용 적용. 첫 확인부터 `SCOPE-01` 포함 |
| Workflow 그림이 자동 사람 반려 반복을 암시함 | 실제 JSON 중단점과 학습자의 별도 검토 표시. 승인 서비스가 있는 것처럼 그리지 않음 |
| 모델 비교가 `.env`를 영구 변경하며 다른 곳에 축약 절차도 존재함 | 완전한 모델 운영 경로 하나로 통합. 성공·실패에도 파일·원래 터미널 설정을 유지하는 명령 범위의 모델 지정 |
| Skill·A2A·Routine 예시의 셸 경계에서 빈 범위 값이 전달됨 | azd 전에 필수 이름/버전/endpoint 보호. 이번 회차의 실제 설정/반환값 사용 |
| Readback 재실행과 routine enable 실패의 중단점이 불명확함 | 기존 폴더면 다운로드 전에 중단. 다운로드 성공 후에만 바이트 비교, enable 성공 후에만 dispatch, 실패해도 disable·재조회 |
| 국문 근거 링크가 다른 언어의 결과를 열고 거절 검토 문장 하나의 의미가 반대임 | 독립 영문/국문 결과로 명시적 연결. 올바른 승인 거절을 오답으로 바꾸지 않도록 문구 정정 |

**로컬 인수:** Python 3.13·3.14에서 offline 테스트가 **각 231개** 통과했습니다.
Ruff 0.16.6 lint/format·Python compilation·두 결정적 학습자 번들·문서 검사도 통과했습니다.
언어 쌍 61개·workshop CLI 예제 328개·번역 보류 0개입니다.
새 회귀 검사 7개는 정확한 저장 파일명·dev 기준을 확인하고, 바뀐 셸 블록을 명시적인 로컬 stub으로 실행합니다.
미설정/빈 값·실패·재실행 시 바이트 보존도 검사합니다.
영문 원본을 먼저 확인한 뒤 국문과 정확한 완료 hash를 갱신했습니다.

**근거 범위:** 가이드 개정이며 새 사용성 점수나 실측 완주 시간이 아닙니다.
새 Azure/모델/judge 호출·배포·역할 부여·녹화·초심자 pilot은 하지 않았습니다.
Canonical 지침·정책/평가/fixture 데이터·기존 미디어는 그대로입니다.
아래 이전 검토와 실제 실행 결과는 당시 범위와 수치를 유지합니다.

<a id="whole-guide-review"></a>

## 전체 가이드 straightforwardness 점검 — 2026-09-17

**기본 랩 12개·확장 랩 16개의 두 언어 전체(56개 랩 페이지)**와
진입·경로·준비·강사 문서, 실행형 참고 워크북을 함께 점검했습니다.
다음 행동·선행 조건·기대 파일·중단점·복구를 추측 없이 찾을 수 있는지가 기준입니다.
아래 준비된 A/B 전용 평가보다 범위를 넓혔으며 새 사용성 점수를 부여하지 않습니다.

| 남아 있던 공백 | 보완 |
|---|---|
| B에도 브라우저 ZIP·선택 hosting 검사가 필수처럼 보임 | A/B 자료 획득 분리. 전체 SDK 검사는 선택 모듈의 준비로 이동 |
| C가 모든 기능을 연속 실행하는 과정처럼 보임 | 전체 모듈 목록·명시적 첫 회차 범위·선택 승격/OpenAPI/crash/Router·인계 링크 |
| Hosted 명령이 셸이 찾은 프로젝트에 의존 | Toolbox·안전·matrix·세션 정리에 보호된 폴더/서비스/버전 값 명시 |
| 두 번째 원격 smoke가 첫 stream을 덮어쓸 수 있음 | 새 기록 폴더·원시 출력 보존·실패를 전파하는 호출/검증 |
| 심화 IQ 준비에 template 초기화·YAML 수동 병합이 남음 | 별도 `--kind matrix` 패키지 준비. V1/V2 사본·정확한 런타임 설정 보존 |
| 로컬 matrix smoke가 소스 프로젝트의 azd 상태를 선택 | 로컬 `--azd-directory` 지정. 근거는 원래 소스 복사본에 저장 |
| 기본 matrix 명령이 선택 회귀 파일을 가정 | 회귀 없는 기본값·실제 소비한 검토만 선택·holdout 전 모델별 dev 게이트 |
| 학습자 정리·언어 순서에 예전 유지보수 지시가 섞임 | 브라우저 정리 인계·접힌 미디어 유지보수·현재 번역 순서 |

**로컬 인수:** Python 3.13·3.14에서 offline 테스트가 **각 224개** 통과했습니다.
Ruff 0.16.6 lint/format·Python compilation·두 결정적 학습자 번들·문서 검사도 통과했습니다.
문서는 언어 쌍 61개·workshop CLI 예제 332개·번역 보류 0개입니다.
모든 가이드의 Bash 블록은 cloud 실행 없이 문법을 검사하며, 선택한 실패 경로 검사는 명시적인 로컬 stub을 사용합니다.

관련 검사는 실제 로컬 패키지/manifest 생성, 잘못된 범위 거절,
azd 실패 stub으로 명령 블록 실행, 기존 출력 바이트 보존, 언어·명령 일치를 확인합니다.
Matrix 도우미는 기존 `runtime`·Toolbox·CI 계약을 유지합니다.
Provision·배포·역할 부여·모델/provider 교체·런타임 설치를 수행하지 않습니다.
Canonical prompt/dataset/corpus/fixture 자산과 기존 미디어는 그대로입니다.

**근거 범위:** 새 Azure/모델/judge 호출·배포·역할 부여·녹화·초심자 pilot은 하지 않았습니다.
아래 95/100은 초기 자체 편집 평가로 유지하며 완주율이나 새 심화 준비의 점수로 확대하지 않습니다.

<a id="follow-through-review"></a>

## 실제 따라 하기 재점검 — 2026-09-17

두 번째 검토에서는 `5cce55b` 가이드의 설정·파일 인계·선택 Hosted 준비를 따라가며 확인했습니다.
편집 점수를 모든 학습자가 완주할 수 있다는 증거로 취급하지 않았으며 초기 구조 체크리스트가 입증하지 못한 공백을 찾았습니다.

| 공백 | 보완 | 근거의 범위 |
|---|---|---|
| 언어/label을 바꿔도 이전 Search 소유권 범위와 충돌 가능 | 정확한 `mfv2-` 문법·복사본/범위 규칙·강사 소유권 인계 명시 | 네트워크 요청 전에 언어/prefix 변경 거절을 로컬 재현. 기존 ledger 보존 |
| B가 소스 복사본에서 시작하면 브라우저 기록 양식을 받지 않을 수 있음 | 실행 가능한 덮어쓰기 방지 기록 폴더 준비·JSON 파일명·B 전용 양식 항목 | 실제 복사와 재실행 거절을 검사하며 링크만으로 추정하지 않음 |
| Dev 게이트가 막히면 작업 종료 시 인계 경로가 불명확 | 근거 완비·반려·미완료 인계 분리. 없는 실행에 인수 명령 금지 | 빠진 작업은 미완료로 남기며 holdout·업무 기준을 완화하지 않음 |
| 선택 Hosted 준비가 YAML 수동 병합과 셸 변수 유지에 의존 | `--kind runtime` 패키지 검증 도우미·별도 폴더·보호된 서비스 범위 azd 명령 재사용 | 실제 manifest 생성과 stub 환경/재조회 계약. 값이 없으면 azd 실행 전에 중단 |

준비 도우미는 언어가 맞는 입문 **local/v2/project-Responses** 패키지만 지원합니다.
기존 Toolbox·CI Invocations 계약은 별도로 유지하며 모델·검색 fallback을 추가하지 않았습니다.
`cleanup-plan`도 선택 언어의 정리 가이드로 연결합니다.
공식 manifest 문서와 설치된 azd 도움말은 9월 17일 검토했지만 **새 Azure 배포 결과는 아닙니다**.

검사는 안전한 복사·폴더/profile 거절·필수 값 누락 차단처럼 구체적인 동작을 확인합니다.
편집 점수 검사는 합계와 미실행 pilot만 확인하며 **95점을 하드코딩해 통과시키지 않습니다**.
아래 점수는 초기 자체 평가로 남기며 추가 사용성 점수나 초심자 완주율을 주장하지 않습니다.
Canonical 지침·정책/평가/fixture 데이터·기존 미디어는 그대로입니다.
이번 재점검에서 새 유료 모델/judge 호출·리소스/역할 변경·Azure 배포·초심자 pilot을 수행하지 않았습니다.

**이번 따라 하기 개정의 로컬 인수:** Python 3.13·3.14에서 offline 테스트가 **각 215개** 통과했습니다.
Ruff 0.16.6 lint/format·Python compilation·두 결정적 학습자 번들·문서 검사도 통과했습니다.
문서는 언어 쌍 61개·workshop CLI 예제 332개·번역 보류 0개입니다.
범위 보호 검사는 로컬 azd stub으로 미설정 값과 빈 값을 모두 확인하며 실제 배포는 실행하지 않습니다.

<a id="guide-straightforwardness"></a>

## 초기 가이드 straightforwardness 평가 — 2026-09-17

**자체 편집 인수 평가: 95/100.** 아래는 **준비된 A/B 기본 가이드**에 적용한 명시적인 점검 기준입니다.
독립적인 사용성 벤치마크·학습자 성공률 95%·모든 선택 C 통합의 평가는 아닙니다.
항목당 **5점**이며 원문 검토와 아래 검사로 01–19를 확인했습니다.
20은 새 초심자 실험을 하지 않았으므로 **0점**입니다. 안내한 시간은 준비된 수업의 배정 시간이지 새로 측정한 완주 시간이 아닙니다.

| # | 인수 기준 — 항목당 5점 | 근거 | 부여 점수 |
|---|---|---|---:|
| 01 | 첫 행동이 준비이며 배경·영상은 선행 조건이 아님 | [README](../../../README.ko.md)와 진입 페이지 검사 | 5 |
| 02 | 실행 전에 경로 하나와 첫 회차 기본값을 선택함 | [A](../paths/a-beginner.md) / [B](../paths/b-practitioner.md) | 5 |
| 03 | 두 경로의 9단계에 인계가 있고 시간표 합계가 240/360분임 | [시간표](../paths.md)와 경로 순서 검사 | 5 |
| 04 | 두 언어의 경로 단계 36개에 정확한 구간으로 연결되는 열린 진입·종료 링크가 있음 | [학습 경로 테스트](../../../tests/test_learner_journey.py) | 5 |
| 05 | 모든 번호 랩에 범위·준비물·완료·복구가 하나의 시작 카드로 있음 | 두 언어 랩 24페이지와 시작 카드 검사 | 5 |
| 06 | A에는 준비된 workflow 명령 하나만 있고 B 코드·holdout은 포함되지 않음 | [A 경로](../paths/a-beginner.md)와 추출 명령 검사 | 5 |
| 07 | B 기본 명령에서 선택 judge·호스팅·Preview 경로를 제외함 | [B 경로](../paths/b-practitioner.md)와 추출 명령 검사 | 5 |
| 08 | 담당자 준비와 선택 설정이 준비된 학습자의 흐름을 끊지 않음 | [준비](../setup.md). 담당자 명령은 접힌 구간에 있음 | 5 |
| 09 | 실행 전에 유료 모델/검색·클라우드 쓰기·로컬 전용 작업을 구분함 | Lab 02/04/05/06/07/08의 범위·명령 안내 | 5 |
| 10 | 학습자 ZIP과 소스 ZIP의 목적·받는 방법이 다름을 설명함 | [준비](../setup.md) / [Lab 00](../labs/00-start.md#path-b) | 5 |
| 11 | 준비된 지침·질문이 고정 합성 입력을 사용하며 정답표·holdout이 없음 | [학습자 자료 테스트](../../../tests/test_learner_materials.py) | 5 |
| 12 | 빈 기록 양식의 파일명이 최종 인계에서 요구하는 이름과 같음 | [학습자 번들](../../../data/README.ko.md) / [Lab 11 A](../labs/11-capstone.md#path-a) | 5 |
| 13 | 브라우저 평가에서 실제 6개 응답·인용·검토 이유를 모두 요구함 | [Lab 07 A](../labs/07-evaluation.md#path-a)와 평가표 검사 | 5 |
| 14 | 문서의 출력 필드·파일명이 실제 CLI 산출물과 일치함 | 오프라인 비교 명령 실행. 존재하지 않는 비교 필드 제거 | 5 |
| 15 | 평가 기본 흐름이 1–4단계이며 dev 6건의 후보 통과 후 holdout 4건을 엶 | [Lab 07 B](../labs/07-evaluation.md#path-b)와 명령·게이트 검사 | 5 |
| 16 | 재개 시 로컬 재조회·새 수집·기존 job 조회를 구분함 | [복구 표](troubleshooting.md#resume-safely). 거부된 재실행 뒤 fixture 바이트 보존 | 5 |
| 17 | 패키징·cleanup-plan을 배포·삭제로 오해하지 않음 | [Lab 08 B](../labs/08-hosted.md#path-b) / [Lab 09 B](../labs/09-operations.md#path-b)의 CLI 실제 실행 | 5 |
| 18 | 영·한 명령·링크·현재 개정의 정확한 파일 hash가 일치함 | [문서 테스트](../../../tests/test_documentation.py) / [번역 기록](../../localization.json) | 5 |
| 19 | 합성 데이터 계보·오류·미검증 결과를 구분하며 과거 영상을 새 증거로 쓰지 않음 | [고정 데이터 hash](../../../data/localization.json)·offline 계약·아래 날짜별 기록 | 5 |
| 20 | 새 학습자가 준비된 경로를 독립 완주하고 개입·소요 시간을 기록함 | **미실행 — 점수 부여하지 않음** | 0 |

**이번 개정의 확인:** Python 3.13·3.14의 전체 offline suite, Ruff 0.16.6 lint/format,
Python compilation, 결정적 학습자 번들, 문서 검사(언어 쌍 61개·workshop CLI 예제 332개·번역 보류 0개)를 통과했습니다.
가이드의 오프라인 명령을 `.env`·상속된 Azure 인증정보·설치 SDK가 없는 임시 복사본에서 실행합니다.
실제 파일·의도적인 fixture 0/6 대 6/6·비교 필드·종료 코드·기존 label 거절 뒤 바이트 보존,
`cloud_deployed: false` 패키징·삭제 없는 정리를 확인합니다. Fixture 점수는 **모델 품질 실측이 아닙니다**.

이번 변경은 가이드·빈 학습자 기록 양식·관련 검사에 한정합니다. Canonical 지침·정책/평가/fixture 데이터·녹화 미디어는 그대로입니다.
**이번 개정의 새 Azure 실행·배포·역할 부여·유료 평가·SDK 통합 실행·녹화는 주장하지 않습니다.**
아래 과거 결과는 원래 범위와 날짜를 유지합니다.

## 확장판 인수 검사 — 2026-09-17

9월 16일 영문·국문 확장 소스는 아래의 과거 cohort와 분리해 확인했습니다.
**Python 3.13·3.14 각각 offline 200개, 설치된 SDK transport 67개**와 Ruff check/format,
Python compilation, 의존성 호환성, 결정적 학습자 bundle 검사가 통과했습니다.
문서는 **61개 언어 쌍·실행 가능한 workshop 예제 332개**를 검사했으며 보류된 번역은 없습니다.

영문 확장은 166개 동작·496장 캡처·원본 구간 368개,
독립 국문 확장은 172개 동작·516장 캡처·원본 구간 363개입니다.
최소 midpoint SSIM은 각각 **0.982302 / 0.983325**입니다.
확장 영상 6개를 실제 로컬 player에서 재생하고 각 통합본의 15개 챕터마다 seek 완료와 decoded frame을 확인했습니다.
국문 리부팅 파트는 별도 시간축을 유지하며 인증 전환과 그 뒤의 원본 구간은 공개 영상에서 제외했습니다.

[영문 결과](../../edition-results.md)와 [국문 결과](../edition-results.md)에 실제 실패를 남겼습니다.
Optimizer의 답변 자기 비교를 원문 grounding이나 승격 근거로 인정하지 않았습니다.
별도 대화 평가의 실제 judge 입력에는 원래 정책 JSON이 보존돼 있습니다.
국문 안전 실습 D06은 CLI exit 0이어도 도구 발견 실패에 따른 failed 응답입니다.
9월 17일에는 확장 영상 6개의 실제 비공개 GitHub bytes/hash·native 재생·챕터 seek 완료도 확인했습니다.
수동 CI 실행은 로컬 검사나 게시된 영상 URL로 추정하지 않는 별도 실행 검증입니다.

첫 GitHub 검사에서는 SDK 테스트용 개발 의존성 누락이 드러났고, 초기 release dispatch는
runner context가 없는 위치의 `runner.temp` 참조 때문에 거부됐습니다.
SDK job이 선언된 `dev` extra를 설치하도록 맞추고, 실행 단계에서 `$RUNNER_TEMP`로 경로를 만든 뒤
`$GITHUB_ENV`로 전달하도록 수정했습니다. 회귀 검사와 actionlint 1.7.12의 workflow schema/표현식 검사가 통과했으며
원래 실패한 GitHub 이력은 보존했습니다.
수정된 [실제 GitHub 저장소 검사](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35121096979)는
모든 job이 통과했습니다. 이후 OIDC 불일치는 이 저장소가 실제 발급한 immutable subject로 좁혀 확인했으며
새 credential·확대된 역할·완화된 GitHub 설정 없이 기존 federation만 수정했습니다.
이후 [실제 OIDC release](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/35121162793)가
2차 시도에서 국문 dev 6/6·오류 0으로 통과했습니다. 원래 artifact hash와 업무 결과를 다시 검증했고
정확한 생성 세션의 idle 상태도 별도로 확인했습니다. 영상 게시 후의 이 실행에는 native judge나 holdout을 사용하지 않았습니다.

## 국문 실제 Azure 실행 — 2026-09-15

기존 Sweden Central 실습 프로젝트를 재사용했습니다. 기본 구독을 바꾸거나 새 Resource Group을 만들지 않았습니다.
승인된 Sol/Terra/Astra 배포를 각각 100K TPM으로 추가하고, 해당 Hosted identity에 필요한 최소 모델/Search 역할만 부여했습니다.
Luna·judge·embedding 배포는 기존 자산을 사용했습니다.

| 대상 | 버전 | 행 수 | 실행 오류 | 업무 검사 | Groundedness | Relevance | Root trace 확인 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `ko-baseline-final` | 7 | 24 | 0 | 24/24 | 24/24 | 19/24 | 24/24 |
| `ko-candidate` | 8 | 24 | 0 | 24/24 | 22/24 | 20/24 | 24/24 |
| `ko-holdout` | 8 | 16 | 0 | 16/16 | 16/16 | 13/16 | 16/16 |

Calibration은 고정 정답/오답 두 건 중 두 건을 기대대로 분류했습니다.
이는 target이 생성한 새 응답 두 건이 아니며 judge 전체를 인증하는 결과도 아닙니다.
초기 version 6의 진단용 24행과 native run은 위의 통제된 비교와 분리해 보존했습니다.

`review-native-findings`는 운영 승인이 아닙니다. 업무 기준을 맞힌 보류 답변이 relevance에서 낮게 평가될 수 있으며,
실제 점수와 이유를 그대로 남깁니다. V2가 모든 지표에서 개선됐다고 주장하지 않습니다.
Baseline이 모두 통과해 실패를 만들거나 회귀 승격을 강제하지 않았습니다.

**실행·평가 계보:** [현재 실행 결과](../live-run.md), 새 asset 디렉토리의 `live-results.json`,
원본 `outputs/benchmarks/`의 dataset/corpus/response/native/trace/cleanup 기록으로 연결합니다.
공개 holdout은 최종 인수 절차 교육용이며 미사용 운영 검증셋이 아닙니다.

## 실제 실행에서 수정한 계약

영문은 별도 영어 지침·정책·데이터로 실행했습니다. 초기 IQ 검색 누락에 따른 20/24 결과를 보존한 뒤
같은 provider의 검색 필터를 명시한 새 baseline을 24/24로 확인했습니다.
V2 candidate는 23/24이며 Astra의 dev D05 인용 관련성 실패를 그대로 남겼습니다.
Dev에서 통과한 Luna/Sol/Terra만 사전에 선택해 holdout 12/12를 확인했습니다.
영문 native 결과와 3모델 선택 이유는 [영문 실행 기록](../../live-run.md)에 별도로 있습니다.
국문 결과나 16행 분모를 영문으로 복사하지 않습니다.

- full agent endpoint와 `--protocol`을 동시에 지정하는 azd 인자 충돌.
- session query 추가 시 `api-version=v1`이 사라지지 않도록 URL query merge.
- embedding 404 이후 원래 실패를 보존하고 같은 account API를 명시적으로 선택.
- App Insights 전용 audience와 구독/tenant에 고정된 credential로 동일 query API 호출.
- 이미 idle인 session은 불필요한 stop 요청 없이 관측한 상태를 기록.

수정 중에 결과를 덮어쓰거나 다른 모델/원본/fixture로 성공을 만들지 않았습니다.
Runtime 코드가 바뀐 초기 진단과 최종 비교는 별도 version·label로 남겼습니다.

## 미디어 검증

새 국문은 **182개 액션**, **543개 무손실 캡처**, 세 개의 편집 영상입니다.
선택된 WebP는 원본 PNG와 RGB 픽셀이 동일합니다.
**435개 편집 구간**을 실제 원본 영상과 대조했고 최소 midpoint SSIM은 **0.987849**였습니다.
모든 MP4의 전체 decode·frame 수를 검사했으며 편집은 대기를 제거한 실제 footage입니다.
챕터 카드는 앱 화면이 아니라고 표시합니다.

인증/비밀번호 입력은 녹화하지 않았습니다. UI 실패·설치/인증 오류·초기 진단도 원본과 액션 이력에 남습니다.
한 trace에서 포털에 보이는 17개 span/2개 chat과 응답의 실제 model call 3개를 구분했습니다.
64개 root trace 확인을 모든 child span의 완전한 export 증거라고 부르지 않습니다.

새 파일 검색 원문 여섯 개는 원격 Files API로 읽어 번들 원본과 바이트/hash 일치를 확인했습니다.
UI 인용 버튼의 다운로드가 확인되지 않은 시도는 성공으로 표시하지 않았습니다.

## 재실행할 로컬 검사

```bash
python3.13 -S -m unittest discover -s tests -t . -q
python3.14 -S -m unittest discover -s tests -t . -q
python -m unittest discover -s tests_sdk -t . -q
python -m ruff check .
python -m ruff format --check .
python -m compileall -q src scripts examples tests tests_sdk
python scripts/check_docs.py
python scripts/build_learner_materials.py
python -m pip check
python scripts/check_sdk.py
```

SDK 테스트는 실제 설치 라이브러리와 명시적 transport stub을 사용합니다.
그 성공을 Azure 실제 응답으로 집계하지 않습니다.
가이드/preset 보강 후 Python 3.13·3.14의 offline 테스트는 **각 126개**, 설치 SDK 테스트는 **27개**가 통과했습니다.
Ruff·format·Python compilation·의존성·SDK 계약·문서 검사도 통과했습니다.
문서 검사는 **37개 언어 쌍·218개 CLI 예제**와 번역 유예 0개를 확인했습니다.
Python 3.13·3.14에서 두 학습자 번들의 생성 바이트와 canonical 입력 일치도 확인했습니다.
영문 새 자료는 172개 액션·516개 무손실 캡처·영상 3개이며,
407개 편집 구간의 원본 대비 최소 SSIM은 0.985156입니다.
두 언어의 새 파일을 검수한 뒤 이전 미디어 1,452개와 중복된 구버전 진입 문서를 제거했습니다.
사용자 승인 후 새 영상 6개를 비공개 저장소의 GitHub 첨부로 게시했습니다.
실제 업로드 파일의 byte/hash·재생·챕터 이동을 확인했으며 임시 서명 storage URL은 저장하지 않았습니다.

## 가이드·IQ preset 보강 — 2026-09-15

두 언어의 랩 24페이지에 범위·준비물·완료/복구·다음 단계 카드를 추가했습니다.
A는 캡스톤을 포함하며 **사전 준비 뒤** 합계 240분입니다.
브라우저 지침·질문 전용 파일·빈 평가표는 canonical v2/정책/dev에서 생성하며
학습자 ZIP에는 정답 열·holdout을 넣지 않았습니다. 기존 지침·dataset·미디어는 변경하지 않았습니다.

최종 **읽기 전용 Azure 사전 검사**에서 `gpt-5.6-luna` / `2026-07-09`의 `Succeeded`,
실제 Search system-assigned identity·명시된 계정 역할·의도한 합성 source를 확인했습니다.
결과는 `ready_for_setup: true`, **`configured: false`**, `model_inference_verified: false`, `cloud_changes: false`입니다.
새 영구 chat base는 **만들지 않았으며** 이 보강을 위해 역할 부여·배포·유료 추론/평가를 새로 실행하지 않았습니다.

이전에 성공한 MI 모델 연결/응답을 **로컬에서 재생 검사**했으며 Azure를 다시 호출하지 않았습니다.
API key `null` 직렬화와 실제 `id/title/content` source projection을 확인했습니다.
반환 필드만 canonical 원문과 대조하고 없는 날짜 필드는 만들어 넣지 않습니다.
Transport 검사는 유료 요청 전 설정/모델 변경 거절·명시적 오류·소유권·실패 보존을 확인합니다.

새 end-to-end Azure 실행·초보자 수업 실험·개정 준비 단계의 재촬영을 수행했다는 뜻은 아닙니다.
기존 실제 점수/영상은 원래 버전·hash를 유지하며 새로 바뀐 코드의 실행 증거로 재분류하지 않습니다.

## 확인하지 않은 것

실제 회사/Microsoft 365 데이터, 외부 Work IQ/Fabric 연결, 운영 SLA, 통계적 우월성,
자동 재학습·가중치 변경, 사람 대신한 운영 승인, 다른 사용자 자산 삭제는 수행하지 않았습니다.
모델·Search·로그·파일의 잔여 비용은 session 중지와 별도로 확인합니다.
