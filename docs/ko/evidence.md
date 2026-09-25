# 실행 근거와 녹화

[English](../evidence.md) | **한국어**

**실제로 실행·녹화·검증했거나 미검증으로 남긴 항목을 찾는 hub입니다.** 이전 녹화는 2026-09-24 새 추가 사항의 증거가 아닙니다.

## 현재 근거 링크

| 필요한 것 | 링크 |
|---|---|
| 실제 실행 결과와 한계 | [live-run.md](live-run.md) |
| 녹화 요약 | [video-summary.md](video-summary.md) |
| Action/capture index | [action-captures.md](action-captures.md) |
| 기능과 모듈별 근거 | [coverage.md](coverage.md) |
| 검증 범위와 로컬 검사 | [reference/validation.md](reference/validation.md) |

## 2026-09-15 기본 실행 상자

**Pre-Ignite 2026 Edition / 현재 workflow·평가 curriculum: 2026-09-15.** [입문 또는 구현 가이드](paths.md)를 따릅니다. 각 lab은 관련 action이나 command 옆에 참고 이미지와 **확인할 것** 설명을 둡니다. 먼저 [화면 읽는 법](labs/00-start.md#이-가이드의-화면-읽는-법)을 확인합니다.

## 2026-09-24 `gpt-6-sol` 녹화

국문 녹화: [요약](video-summary.md) · [action/capture index](action-captures.md) · [챕터](video-chapters.md) · [실제 결과와 한계](live-run.md).
국문 세트는 **91개 action, 272개 capture, 영상 3개**입니다. 시간은 **가이드 순서 6:03**, **CLI 2:57**, **포털 2:43**입니다.
Sweden Central 실습 프로젝트에서 Lab 00–09·11의 A(포털)·B(CLI) 주요 단계와 선택 Foundry 평가 단계를 `gpt-6-sol` / `2026-09-22`로 실행했습니다.
실패한 시도는 재시도 옆에 그대로 남깁니다. 로컬 재생과 챕터 이동을 확인했으며 GitHub에는 업로드하지 않았습니다.
로컬에서는 `python scripts/play_recordings.py --edition ko`로 재생합니다. 이전 녹화는 삭제했습니다.

영문 녹화는 별도입니다: [영문 영상](../video-summary.md). 영문 세트는 **98개 action, 293개 무손실 capture, 영상 3개**이며 시간은 **가이드 순서 6:29**, **CLI 3:11**, **포털 2:55**입니다.

## 실행과 언어 metadata

국문과 영문은 각자 고정된 지침, 합성 정책, dev/calibration/holdout dataset, fixture를 사용합니다.
국문은 기본 언어이고, 영문만 `--language en`으로 명시 선택합니다.
[언어 계약](reference/languages.md)과 [버전별 data bundle](../../data/README.ko.md)이 언어별 lineage를 보존합니다.

## 추가 모듈과 실행 근거

**9월 16일 확장 경로:** [A — 입문](paths/a-beginner.md) · [B — 구현](paths/b-practitioner.md) · [C — 고급 모듈](paths/c-advanced.md).
[기능·근거 상태](coverage.md)에서 기존 기본 과정, 실행 가능한 모듈, 실제 Azure 검증 범위를 구분합니다.
확장 모듈은 2026-09-16에 이전 `gpt-5.6-luna` preset으로 실행했으며 해당 녹화는 삭제했습니다.
`gpt-6-sol`로는 녹화 없이 다음을 다시 실행했습니다. 2026-09-23: 대화 평가, Agent Optimizer, 안전 제어의 red-team 단계, 릴리스 운영. 2026-09-24: A2A, Insights scan 1회. 2026-09-25: 대화 평가, Memory, routine dispatch 1회, 탐색까지의 Toolbox. 모듈별 최신 근거는 [기능·근거 상태](coverage.md)에 있습니다.

## 가이드대로 끝까지 실행 — 2026-09-25

두 기본 경로를 GitHub에서 받은 새 복사본으로 영문·국문 모두 가이드대로 실행했습니다. B 경로는 핵심 블록을 한 터미널에서, A 경로는 포털에서 실행했습니다.
모든 블록이 종료 코드 0이었고 D01–D06이 기준을 충족했습니다. 바뀐 포털 **에이전트 만들기** 창을 포함해 가이드 결함 5건을 고쳤습니다.
[실행 기록](live-run.md#end-to-end-20260925)을 확인하세요.

## 검토 반영 실제 검증 — 2026-09-24

갱신한 SDK 고정 버전, Lab 03 B를 포함한 핵심 B 경로, Lab 09 추적 조회, SDK 예제, 형식이 있는 요청을 쓴 A2A, Insights scan 1회를
2026-09-24 저녁 같은 실습 프로젝트에서 Azure로 실행했습니다. [실제 결과](live-run.md#review-refresh-live-verification)를 확인하세요.
위 2026-09-24 녹화는 이 추가 사항보다 앞선 것이며 그 증거로 사용하지 않습니다.

**2026-09-25 보충 녹화:** Lab 03 B의 `--output` 생성·호출, Lab 03 B 포털 확인, Lab 09 B `response_id` 추적 검색을 영문·국문으로 녹화했습니다.
무손실 화면 12장과 짧은 영상 4개: [요약](video-summary.md#review-refresh-supplement) · [화면](action-captures.md#review-refresh-supplement) · [captures.json](../assets/review-refresh-20260925/captures.json).
나머지 추가 사항은 새 녹화가 없습니다. 아직 실행하지 않았거나 담당자 승인을 기다리는 것: A Lab 05 브라우저 선택지를 위한 원격 배포, 타사 모델 비교, 새 Agent Optimizer 실행(지원 optimizer 배포 필요), Toolbox 조회·Tool Search·Skills(Search 역할 필요), Dev Pack. [각각에 필요한 것](live-run.md#not-run-feasibility)을 확인하세요.
