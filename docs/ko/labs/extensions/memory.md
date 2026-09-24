# Memory: 합성 맥락을 저장·검색·삭제하기

[English](../../../labs/extensions/memory.md) | **한국어**

**C 선택 Preview · 2026-09-16 기준.** 먼저 관리형 Memory Store API를 사용하고
실제 검색 결과를 새 모델 요청에 명시적으로 전달합니다.
핵심 정책 agent에 자동 추출을 켜거나 평가 사례 사이에 Memory를 공유하지 않습니다.

**근거 상태:** 2026-09-25에 `gpt-6-sol`과 `text-embedding-3-large`로 영문 재실행: store, alpha put·recall, 비어 있는 beta recall, update, forget, store 삭제를 확인했습니다. 이전 실행: 2026-09-16(`gpt-5.6-luna`).

**준비:** B 환경, 지원되는 기존 chat/embedding 배포, 프로젝트/모델 권한, 쓰기·모델·정리 승인.
**완료:** 별도 CLI 요청 사이에 항목이 유지되고, alpha/beta 검색이 분리되며 실제 검색 결과로 답하고 삭제를 확인함.
**중단:** 오류를 남깁니다. 다른 scope·계정·모델·provider로 바꾸지 않습니다.

**첫 회차:** 보존 시간 1시간 안에 1–5절을 마칩니다.
반환된 `memory_id`를 같은 터미널에서 수정·삭제에 사용합니다. 자동 agent memory는 포함하지 않습니다.

## 1. 기존 embedding 배포 지정

설정 카드의 프로젝트와 답변 deployment를 유지합니다.
`.env`의 `AZURE_AI_EMBEDDING_DEPLOYMENT_NAME`에 담당자가 준비한 실제 기존 embedding deployment 이름을 넣습니다.
예제 이름으로 추측하거나 오류 뒤에 새 모델을 배포하지 않습니다.

```bash
python scripts/workshop.py --language ko memory plan
```

`<prefix>-memory-ko`, 두 합성 scope와 `default_ttl_seconds: 3600`을 확인합니다.
생성은 하지 않습니다. CRUD는 보존 시간 안에 끝냅니다.
영문 제작 중 보존 시간 이후 항목이 없는 상태를 관찰했지만 정확한 TTL 만료 SLA를 측정한 것은 아닙니다.

## 2. 내 store 생성

```bash
python scripts/workshop.py --language ko memory create --confirm-create
```

store는 검증된 chat/embedding deployment에 연결됩니다.
로컬 소유 기록은 `outputs/memory/<store-name>/ownership.json`에 있습니다.
기존 이름은 가져오지 않습니다.
담당자가 training 계정에서 프로젝트 identity에 모델 접근 권한을 부여해야 할 수 있습니다.
이는 내 CLI 로그인과 별도입니다. 빠진 role을 API key로 대신하지 않습니다.

## 3. 동봉한 학습 질문만 저장

```bash
python scripts/workshop.py --language ko memory put --scope alpha --case D02 --confirm-write --confirm-cost
```

dev D02와 무작위 합성 marker를 저장합니다. 실제 사람의 profile이나 정답을 저장하지 않습니다.

```bash
printf 'put이 반환한 memory_id: '
read -r MEMORY_ID
python scripts/workshop.py --language ko memory inspect --scope alpha
python scripts/workshop.py --language ko memory inspect --scope beta
```

새 store의 alpha에는 내 항목, beta에는 빈 목록이 기대됩니다.
매 명령은 새 client이므로 Python 변수의 유지가 아니라 실제 서비스 저장 상태를 확인합니다.
생성 응답 이후에도 읽기 확인에서 잠시 404가 발생할 수 있습니다.
반환된 ID를 먼저 보관하고 제한된 읽기만 다시 확인합니다. write를 반복하지 않습니다.
확인이 늦으면 같은 항목을 조회하며 중복 항목을 만들지 않습니다.

**scope는 인증된 사람 두 명이 아닙니다.** 같은 권한의 운영자가 어느 쪽도 선택할 수 있으므로 사용자 간 인가를 검증했다고 주장하지 않습니다.
포털 **Memory → 내 store → Memories**에서는 기본 `{{$userId}}` 대신 실제 합성 scope를 입력합니다.
로딩이 끝나기 전 빈 화면을 결과로 해석하지 않습니다.

## 4. 새 요청에서 회상

```bash
python scripts/workshop.py --language ko memory recall --scope alpha --label memory-alpha --confirm-cost
python scripts/workshop.py --language ko memory recall --scope beta --label memory-beta --confirm-cost
```

helper는 실제 검색 API의 `memories[].memory_item` ID·내용·scope를 확인한 후
그 결과만 새 stateless 모델 요청에 전달합니다. beta에 alpha 맥락이나 이전 대화를 넣지 않습니다.

`outputs/memory-runs/<label>/`의 request/search/response/summary를 확인합니다.
실제 search ID, memory ID, 모델·response ID·사용량을 보관합니다.
모델은 다른 scope의 marker를 반복해서는 안 됩니다.
`native_agent_memory_tool_used: false`는 의도된 API 기반 경로입니다.
작성 뒤 alpha 검색이 비어 있으면 진단할 finding이지 recall을 조작해도 된다는 뜻이 아닙니다.
명시적으로 새 시도를 하기 전에 원래 빈 결과와 indexing/service 오류를 보존합니다.

## 5. 항목 수정과 삭제

과거 D02를 현재 D01 질문으로 바꿉니다.

```bash
python scripts/workshop.py --language ko memory update --scope alpha --case D01 --memory-id "$MEMORY_ID" --confirm-write --confirm-cost
python scripts/workshop.py --language ko memory inspect --scope alpha
```

ID와 marker는 유지되며 정확한 새 내용을 읽어 확인합니다.
LLM이 스스로 Memory를 고친 것이 아니라 명시적 CRUD입니다.

삭제 승인을 받은 뒤 실행합니다.

```bash
python scripts/workshop.py --language ko memory forget --memory-id "$MEMORY_ID" --confirm-delete
python scripts/workshop.py --language ko memory inspect --scope alpha
python scripts/workshop.py --language ko memory inspect --scope beta
python scripts/workshop.py --language ko memory cleanup --confirm-delete
```

삭제 receipt를 보관하고 제한된 읽기 재확인으로 부재를 검증합니다. delete 요청을 반복하지 않습니다.
삭제 뒤 항목은 없어야 합니다. 삭제가 표시되기까지 짧은 시간이 걸릴 수 있습니다.
이미 없던 항목은 `already_absent: true`, `delete_requested: false`로 표시하며 새로 지웠다고 주장하지 않습니다.
cleanup은 store 소유 marker를 확인하고 알려진 항목/scope가 비어 있어야 합니다.
공유 프로젝트·모델·다른 store는 삭제하지 않고 원문/응답/소유 기록을 유지합니다.

## 선택: 자동 agent memory는 별도

<details>
<summary>참고 전용 — API 실습을 마치려고 자동 추출을 켜지 않습니다</summary>

Foundry의 `memory_search_preview` 도구는 대화 후 memory를 추출하고 update delay를 가지며 직접 remember/forget 명령도 지원할 수 있습니다.
`{{$userId}}` scope는 호출자 identity나 신뢰된 backend의 `x-memory-user-id` header를 사용할 수 있어도
임의 사용자가 보낸 header를 인가 경계로 신뢰하지 않습니다.

자동 추출·지연된 업데이트·삭제에는 별도 검증이 필요합니다.
이 API 실습은 자동 추출, 실제 사용자 인가, 모든 서비스의 영구 삭제를 증명하지 않습니다.
Memory를 독립 dev/holdout benchmark에 몰래 섞지 않습니다.

</details>

**다음:** [Routines](routines.md), [C 모듈](../../paths/c-advanced.md), [Lab 11](../11-capstone.md).
[공식 Memory 수명 주기](https://learn.microsoft.com/azure/foundry/agents/how-to/memory-usage).
