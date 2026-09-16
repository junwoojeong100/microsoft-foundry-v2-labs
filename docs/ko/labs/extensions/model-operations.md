# 모델 운영: 통제해서 비교하고 rollback 보존하기

[English](../../../labs/extensions/model-operations.md) | **한국어**

**C 경로.** 모델 이전은 배포 이름만 바꾸는 작업이 아닙니다.
처음에는 **이미 승인된 두 배포**를 같은 dev로 비교합니다. Router와 폐기는 별도입니다.

**준비:** [Lab 07](../07-evaluation.md)의 실제 candidate, 승인된 두 번째 배포, API/구조화 응답 호환성, 비용과 새 label.
**완료:** 실제 모델 ID·모든 행/오류를 포함한 비교와 이전 결정을 기록함.
**중단:** 기존 모델을 유지합니다. 오류가 다른 배포/endpoint를 선택하지 않습니다.

## 1. Baseline 고정

deployment/model/version, project/API, prompt, corpus, retrieval, 출력 제한과 data hash를 기록합니다.
원래 run 폴더를 유지하고 Router를 고정 모델 baseline으로 사용하지 않습니다.
다른 언어 결과도 재사용하지 않습니다. 이 실습은 모델 생성이나 quota 증액을 하지 않습니다.

<!-- edition-checkpoint:KP24-001-fixed-model-and-scoped-role-readback -->

![실제 국문 촬영: 모델·버전과 제한된 역할 조건만 읽기·새 배포 없음](../../../assets/edition-20260916-ko/screenshots/KP24-001-fixed-model-and-scoped-role-readback-2.webp)

**확인할 것:** 모델과 실제 버전을 읽었으며 새 응답 모델을 만들지 않았습니다. 별도 승인한 임시 Optimizer 모델은 두 실험 뒤 정리했습니다. Router 이전이나 모델 우열 검증은 아닙니다. 내 리소스 이름과 ID는 영상과 다릅니다.

[이 동작 영상 보기](https://github.com/user-attachments/assets/126a7406-b8ff-4d9f-9b3d-1780b9fad328#t=622.92) · [전체 액션과 실패](../../edition-actions.md)

## 2. 모델 선택 하나만 변경

`.env`의 `AZURE_AI_MODEL_DEPLOYMENT_NAME`만 승인된 두 번째 배포로 바꾸고 나머지를 유지합니다.

```bash
python scripts/workshop.py --language ko doctor --cloud
```

실제 하위 모델/버전·배포 상태를 확인합니다.
API/schema가 맞지 않으면 이전 검토 결과로 남깁니다. 이 모델만 다른 API로 우회하지 않습니다.

## 3. 새 dev 수집과 비교

원래 candidate가 Lab 07의 `local` 예제를 사용했다면:

```bash
python scripts/workshop.py --language ko collect --split dev --label migration-model-b --prompt v2 --retrieval local
python scripts/workshop.py --language ko evaluate --label migration-model-b
python scripts/workshop.py --language ko compare --baseline candidate --candidate migration-model-b --variable model
```

다른 provider였다면 양쪽 모두 그 provider로 고정합니다.
실패 행만 교체하거나 분모에서 빼지 않습니다.
금액·날짜·인용·승인 경계·지연·실제 토큰을 함께 확인합니다.
이전이 별도로 승인되지 않았다면 원래 배포 설정으로 돌려놓습니다.

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

Router는 명시적으로 선택한 routing system이지 실패한 직접 모델의 fallback이 아닙니다.
버전·mode·허용 모델 subset을 고정하고 같은 dev로 품질·추정 비용·지연·실제 선택 모델 분포를 확인합니다.
mock report와 실제 요청을 구분합니다. 작은 데이터로 통계적 우월성을 주장하지 않습니다.
준비된 Router가 없으면 **미실행**으로 남깁니다.

**다음:** 비교·이전/rollback 계획·미검증 항목을 [Lab 11](../11-capstone.md)에 기록합니다.
[모델 이전](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/model-migration) ·
[Router 평가](https://learn.microsoft.com/azure/foundry/openai/how-to/evaluate-model-router).
