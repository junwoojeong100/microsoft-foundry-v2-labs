# Lab 09. Trace, 운영 게이트, 비용과 정리

**완료 목표:** 한 번 잘 답한 데모를 운영 가능한 시스템으로 착각하지 않고, 다음 판단의 근거를 남깁니다.

이전: [Lab 07](07-evaluation.md) 또는 [Lab 08](08-hosted.md) · 다음: [캡스톤](11-capstone.md)

## A. 브라우저 — 무엇을 관리해야 하나?

실습 프로젝트에서 본인 권한으로 보이는 범위를 관찰합니다.

| 관찰 대상 | 직접 확인할 질문 |
|---|---|
| 에이전트·버전·assets | 지금 사용자가 호출하는 버전은 어느 것인가? |
| 모델 배포·quota | 모델 이름, 실제 배포, 용량 제한을 구분했는가? |
| 도구·지식 연결 | 어느 데이터와 외부 시스템에 접근하는가? |
| 평가 결과 | 어떤 데이터와 evaluator로 측정했는가? |
| Trace/Monitor | 실패한 요청의 처리 흐름을 찾을 수 있는가? |
| 비용·사용량 | 모델뿐 아니라 Search·session·로그 비용도 있는가? |
| 보안/거버넌스 설정 | 누가 호출·변경·배포·승인할 수 있는가? |

기존 종합 랩의 Control Plane 관점을 이 표로 통합했습니다.
Fleet/관리 메뉴가 보이지 않으면 역할 범위상 정상일 수 있습니다.
전체 구독 권한을 추가하는 것이 학습의 목표가 아닙니다.

## B. 코드 — 실행 이력과 실제 telemetry 연결

### 1. 로컬 이력부터 찾기

`outputs/<label>/manifest.json`과 `responses.jsonl`에서 다음 값을 찾습니다.

- 실행과 질문: `run_id`, `case_id`.
- 지침·데이터·코드·근거: hash와 버전.
- 요청: `response_id`, `request_id`, 실제 응답 모델.
- 검색: provider, 문서 ID, IQ references/activity.
- 결과: 정상/오류, token usage, latency.

여기 있는 request/response ID는 **자동으로 Azure Monitor trace가 되지 않습니다.**
`trace_id: null`, `trace_export: not-configured`이면 그렇게 보고해야 합니다.

### 2. 서버 측 tracing부터 준비

강사는 프로젝트와 Application Insights 연결, 로그 보존·비용·접근 권한을 확인합니다.
[공식 tracing 설정](https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup)을
따라 서버 측 tracing을 활성화하고, 필요할 때만 로컬 client instrumentation을 더합니다.
이 저장소의 Hosted 진입점은 민감한 입력/출력 캡처를 기본 활성화하지 않습니다.

1. 준비된 에이전트에 합성 질문을 한 번 보냅니다.
2. 응답/대화/agent version을 기록합니다.
3. Foundry의 해당 tracing 화면에서 같은 실행을 찾습니다.
4. span의 부모/자식 관계, 모델·도구 호출, 지연·오류를 확인합니다.
5. 보존 정책과 권한을 확인하고, 필요 이상의 원문을 export하지 않습니다.

보호된 테이블은 일반 로그 조회 역할 외에 추가 권한을 요구할 수 있습니다.
트레이스가 늦게 도착하는 동안 호출을 반복해 비용을 늘리지 않습니다.
없으면 **미확인**으로 남기고 연결·exporter·역할·시간 범위를 점검합니다.

### 3. 실패 하나를 설명하기

> “D03은 403이었다”에서 멈추지 말고, 사용자/프로젝트/agent identity 중 누가
> 어느 서비스에 접근하다 실패했는지 설명합니다.

모델 실패, 도구 실패, 검색 근거 부족, 잘못된 정책 적용을 구분합니다.
원문을 바탕으로 사람이 개선 이유를 검토한 뒤 [Lab 07](07-evaluation.md)의 dev 비교로 돌아갑니다.
자동 trace-to-dataset 기능은 Preview이므로 이 기본 경로의 필수 조건이 아닙니다.

## 운영 승인 게이트

| 게이트 | 이번 실습에서 남길 증거 |
|---|---|
| 품질 | 전체 dev/holdout, 실패·누락 포함, 업무 기준과 의미 검토 |
| 권한 | 최소 권한, 사용자/런타임 identity 구분 |
| 데이터 | 합성/승인된 데이터만 사용, 적용 시점·출처·보존 기간 |
| 안전 | 실제 행동 도구의 서버 측 검증과 사람 승인 계획 |
| 비용 | 예상 호출량, Search 고정비, session 수, 로그 보존 |
| 릴리스 | 정확한 agent/model/prompt/dataset/code 버전 |
| 복구 | 이전 버전·되돌릴 설정·담당자 |

자동 최적화나 continuous evaluation을 기본으로 켜지 않습니다.
운영 중 샘플링·평가 비용·데이터 정책을 승인한 뒤 별도 설정합니다.
수업의 6문항 통과만으로 운영 배포를 승인하지 않습니다.

## 반드시 정리하고 끝내기

```bash
python scripts/workshop.py cleanup-plan
```

이 명령은 **목록과 절차만 출력**하며 삭제하지 않습니다.
[정리 체크리스트](../reference/cleanup.md)를 따라 본인 자산을 확인하고,
공유 서비스와 다른 조의 데이터를 유지합니다.
정리 완료는 “명령을 실행했다”가 아니라 **활성 session·잔여 리소스·과금 상태를 다시 확인했다**는 뜻입니다.
