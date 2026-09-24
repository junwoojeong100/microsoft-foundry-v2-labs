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
9월 23일에는 대화 평가, Agent Optimizer, 안전 제어의 red-team 단계, 릴리스 운영만 `gpt-6-sol`로 다시 실행했고 녹화는 없었습니다. 나머지 모듈은 다시 실행하지 않았습니다.

## 이 판에서 아직 실행하지 않음(2026-09-24 추가)

다음 추가 사항은 refresh 문서에 들어갔지만 **아직 실행하거나 녹화하지 않았습니다**: B의 관리형 agent, 이제 핵심인 trace 단계, 브라우저 Lab 05 hosted-workflow 옵션, Insights 모듈, 최소 SDK recipe, SDK pin refresh.
이 항목의 증거로 이전 screenshot이나 녹화를 재사용하지 않습니다.
