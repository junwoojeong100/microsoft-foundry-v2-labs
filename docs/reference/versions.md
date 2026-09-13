# 버전과 기능 상태 — 2026-09-13

**이 문서의 확인일은 기능 출시일이나 향후 지원 보장일이 아닙니다.**
Ignite 2026 발표를 예측하지 않고, 현재 공식 문서와 소스의 계약을 기준으로 작성했습니다.

## 기능별 경계

| 기능 | 이 에디션의 선택 | 구분 |
|---|---|---|
| 현재 Foundry / Agents v2 / Responses | 기본 경로 | classic SDK 1.x/threads/runs와 분리 |
| Prompt Agent | 모델+지침, 명시적 버전 | 생성/호출의 실제 API를 기록 |
| MAF | `Agent`, `FoundryChatClient`, `model=` | 공급자 패키지의 버전이 core와 같을 필요 없음 |
| 워크플로 작성 | MAF의 Sequential/Concurrent/GroupChat builder | 포털 Workflow Designer에 의존하지 않음 |
| 일반 Search | REST `2024-07-01`, 텍스트 index | 벡터/하이브리드 검색으로 부르지 않음 |
| IQ GA | REST `2026-04-01`, `intents` | 별도 planner 배포 없이 사용; 실제 activity/요금은 별도 확인 |
| richer IQ | `2026-08-01-preview` | 별도 환경·설정·승인; 기본 코드와 혼합 금지 |
| 포털 IQ | 포털이 사용하는 Preview 계약 | GA REST 코드와 동일하다고 가정하지 않음 |
| Hosted Agent 서비스 | GA, 선택 배포 | 지역·권한·session 비용은 별도 |
| Python hosting 패키지 | 고정 prerelease 패키지 | 서비스 GA와 패키지 상태를 따로 표시 |
| cloud evaluation | 프로젝트 OpenAI `evals` | evaluator/카탈로그의 기능·스키마를 별도 확인 |
| 자동 trace-to-dataset | Preview | 기본은 수동 검토 이력; 자동 학습 아님 |
| Work IQ | 별도 Preview/사용자 동의·과금 | 기본 비활성화 |

## 고정한 직접 의존성

정확한 설치 계약은 `pyproject.toml`입니다. 아래 버전은 공식 릴리스 메타데이터와
현재 SDK 계약과 작성 환경의 실제 설치 가능 버전을 대조해 선정했습니다.
패키지 메타데이터에 표시되는 가장 최신 버전과 이 워크숍의 호환성 스냅샷은 다를 수 있습니다.
**설치·SDK 실행·Azure 검증은 각각 다른 수준이며**
실제로 확인한 수준은 [검증 기록](validation.md)에 적습니다.

| 영역 | 패키지 | 버전 |
|---|---|---|
| 프로젝트 | `azure-ai-projects` | 2.3.0 |
| OpenAI 인터페이스 | `openai` | 2.54.0 |
| 인증 | `azure-identity` | 1.25.3 |
| MAF core | `agent-framework-core` | 1.17.0 |
| Foundry provider | `agent-framework-foundry` | 1.12.0 |
| orchestration | `agent-framework-orchestrations` | 1.1.1 |
| 로컬 MCP | `mcp` | 1.27.2 |
| Hosted adapter | `agent-framework-foundry-hosting` | 1.0.0b260903 |
| HTTP / 환경 | `httpx` / `python-dotenv` | 0.28.1 / 1.2.3 |

Python 3.13을 권장하며 본문 명령은 Bash 기준입니다.
오프라인 코드는 3.13–3.14를 대상으로 합니다. Hosted 패키지는 3.13으로 준비합니다.
직접 의존성만 고정한 것과 전체 transitive lock은 같지 않습니다.
루트 `requirements.lock.txt`에는 작성 환경의 실제 해석 결과 103개를 고정했습니다
(macOS ARM64 / Python 3.13; editable 경로와 개발용 Ruff 제외).
다른 OS와 원격 build에서도 설치 결과를 다시 확인합니다.

선정한 Foundry provider 1.12.0은 Projects SDK `>=2.2.0,<2.4.0`을 요구합니다.
따라서 공개 메타데이터의 최신 Projects 2.6.0을 섞지 않고, 공식 prompt quickstart의
최소 버전 조건을 만족하는 2.3.0을 선택했습니다. “각 패키지의 최신”보다
**같이 설치되고 같은 API로 동작하는 조합**을 우선합니다.

이 조합의 prompt-agent 호출은 프로젝트 OpenAI endpoint에
`agent_reference: {type, name, version}`을 명시합니다.
설치한 Foundry provider의 non-preview 요청 계약과 같은 방식이며,
`get_openai_client(agent_name=...)`의 Preview 바인딩이나 암묵적인 최신 버전 호출과 구분합니다.

## 공식 문서에서 발견한 드리프트

- 프로젝트 endpoint를 짧게 표시한 문장이 있어도 SDK에는 전체 `/api/projects/...`를 사용합니다.
- GA IQ REST의 경로는 `knowledgesources`입니다. 일부 설명의 `knowledge-sources`를 그대로 복사하지 않습니다.
- 최신 evaluator는 `model`, 이전 예제는 `deployment_name`을 초기화 필드로 사용합니다.
  코드가 실제 catalog schema를 확인하고 그 스키마와 버전을 기록합니다.
- azd 도움말/트러블슈팅 일부에는 이전 manifest/extension 표현이 남아 있습니다.
  실제 설치된 `azd ai agent ... --help`와 생성된 `azure.yaml`을 대조합니다.
- `https://ai.azure.com/.default`와 예전 Azure OpenAI audience 예제를 섞지 않습니다.
  기본 모델 호출은 프로젝트 SDK가 인증을 처리하도록 합니다.

## 수업 직전 동결 체크

1. 새 환경에서 직접/전이 의존성을 설치하고 `pip check`를 확인합니다.
2. offline·SDK 계약 검사와 최소 실제 모델 호출을 수행합니다.
3. 서비스/API별 GA/Preview·지원 리전·모델 기능·quota·가격을 확인합니다.
4. 버전 변경은 지침·코드·데이터·CLI·가이드·평가를 함께 재검증합니다.
5. 실패했다고 package 전체를 `--upgrade --pre`로 바꾸지 않습니다.

공식 출처와 고정 원본은 [sources](sources.md)에 있습니다.
