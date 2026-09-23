# 모델 운영: 통제해서 비교하고 rollback 보존하기

[English](../../../labs/extensions/model-operations.md) | **한국어**

**C 경로.** 모델 이전은 배포 이름만 바꾸는 작업이 아닙니다.

**근거 상태:** 마지막 실행은 2026-09-16 이전 `gpt-5.6-luna` preset입니다. `gpt-6-sol`로 다시 실행하지 않았고 Router 이전은 주장하지 않습니다.

처음에는 **이미 승인된 두 배포**를 같은 dev로 비교합니다. Router와 폐기는 별도입니다.

**준비:** [Lab 07](../07-evaluation.md)의 실제 candidate, 승인된 두 번째 배포, API/구조화 응답 호환성, 비용과 새 label.
**완료:** 실제 모델 ID·모든 행/오류를 포함한 비교와 이전 결정을 기록함.
**중단:** 기존 모델을 유지합니다. 오류가 다른 배포/endpoint를 선택하지 않습니다.

**첫 회차:** 1–4절 후 기록 폴더에 `model-migration-review.txt`를 저장합니다.
비교 label·판단·변경 없이 유지한 원래 설정을 기록합니다. Router나 폐기 작업은 필수가 아닙니다.

## 1. Baseline 고정

deployment/model/version, project/API, prompt, corpus, retrieval, 출력 제한과 data hash를 기록합니다.
원래 run 폴더를 유지하고 Router를 고정 모델 baseline으로 사용하지 않습니다.
다른 언어 결과도 재사용하지 않습니다. 이 실습은 모델 생성이나 quota 증액을 하지 않습니다.

## 2. 저장된 설정을 바꾸지 않고 두 번째 모델 확인

`.env`는 그대로 둡니다. 카탈로그 모델 이름이 아니라 승인된 두 번째 **배포 이름**을 입력합니다.
괄호 안에서 이 읽기 전용 사전 검사에만 모델을 적용하며 다른 설정은 유지합니다.

```bash
printf 'Approved second deployment name: '
read -r MODEL_B
(
  export AZURE_AI_MODEL_DEPLOYMENT_NAME="${MODEL_B:?Enter the approved second deployment}"
  python scripts/workshop.py --language ko doctor --cloud
)
```

실제 하위 모델/버전·배포 상태를 확인합니다.
API/schema가 맞지 않으면 이전 검토 결과로 남깁니다. 이 모델만 다른 API로 우회하지 않습니다.
3절에서도 같은 터미널의 `MODEL_B`를 사용합니다. 값이 없으면 요청 전에 멈춥니다.

## 3. 새 dev 수집과 비교

원래 candidate가 Lab 07의 `local` 예제를 사용했다면:

```bash
(
  export AZURE_AI_MODEL_DEPLOYMENT_NAME="${MODEL_B:?Enter the approved second deployment}"
  python scripts/workshop.py --language ko collect --split dev --label migration-model-b --prompt v2 --retrieval local
)
```

수집한 6행 전체를 확인한 뒤 로컬 검사를 실행합니다. 새 모델을 고르지 않고 해당 실행에 저장된 배포 정보를 읽습니다.

```bash
python scripts/workshop.py --language ko evaluate --label migration-model-b
python scripts/workshop.py --language ko compare --baseline candidate --candidate migration-model-b --variable model
```

다른 provider였다면 양쪽 모두 그 provider로 고정합니다.
실패 행만 교체하거나 분모에서 빼지 않습니다.
금액·날짜·인용·승인 경계·지연·실제 토큰을 함께 확인합니다.
두 subshell은 실패해도 원래 터미널 배포 설정과 `.env`를 바꾸지 않습니다.
이전이 별도로 승인되지 않았다면 응답용 배포를 영구 변경하지 않습니다.

## 4. 수명 주기 계획

| 단계 | 근거 |
|---|---|
| 발견 | 실제 폐기 공지/날짜 또는 이전 사유 |
| 평가 | 모델·지역·quota·API·정책 적합성 |
| 수정 | 별도 버전에서 검토된 prompt/schema/tool 변경 |
| 검증 | 통제된 dev, 고정 후에만 최종 인수 |
| 배포 | 작은 승인 rollout, 실제 버전 모니터링과 rollback 조건 |
| 폐기 | 기존 호출자가 없음을 확인한 뒤 담당자 삭제 |

`versionUpgradeOption`과 실제 배포 유형을 확인합니다.
자동 업그레이드 후에도 endpoint가 답한다는 사실은 같은 동작의 증거가 아닙니다.
학습자가 공유 upgrade 설정이나 모델을 바꾸지 않습니다.

## 선택: Router는 다른 target

<details>
<summary>별도 Router 실험 — 두 모델 비교의 다음 필수 단계가 아닙니다</summary>

Router는 명시적으로 선택한 routing system이지 실패한 직접 모델의 fallback이 아닙니다.
버전·mode·허용 모델 subset을 고정하고 같은 dev로 품질·추정 비용·지연·실제 선택 모델 분포를 확인합니다.
mock report와 실제 요청을 구분합니다. 작은 데이터로 통계적 우월성을 주장하지 않습니다.
준비된 Router가 없으면 **미실행**으로 남깁니다.

</details>

**다음:** 비교·이전/rollback 계획·미검증 항목을 [Lab 11](../11-capstone.md)에 기록합니다.
[모델 이전](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/model-migration) ·
[Router 평가](https://learn.microsoft.com/azure/foundry/openai/how-to/evaluate-model-router).
