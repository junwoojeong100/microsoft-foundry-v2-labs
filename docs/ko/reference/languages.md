# 언어·실행·미디어 계약

[English](../../reference/languages.md) | **한국어**

**영어를 기본 문서로 제공하고 한국어 경로를 유지합니다. 화면과 영상은 언어별로 별도 제작합니다.**

## 문서

영어는 `README.md`와 `docs/`, 한국어는 `README.ko.md`와 `docs/ko/`에 있습니다.
양쪽 페이지에 대응 언어 링크를 제공합니다.
원문 언어 우선 개정의 유예는 `docs/localization.json`의 파일 hash와 visible warning으로 제한합니다.
그 파일의 현재 source language와 revision을 따르며, 대응 문서를 완성한 뒤 경고를 제거하고 명령 동등성을 다시 검사합니다.
`check_docs.py`는 이전 revision을 포함한 **모든 번역 완료 기록**의 해시를 현재 파일과 대조합니다.
실행 명령을 바꾸지 않았더라도 어느 언어든 수정하면 완료 기록이 더 이상 일치하지 않습니다.
`scripts/update_localization.py`로 해당 쌍을 번역 대기로 표시하고 번역을 마친 뒤 완료를 기록합니다.
두 페이지를 검토하지 않고 오류만 없애려고 해시를 교체하지 않습니다.

## 실행 데이터와 답변

한국어 원본은 그대로 유지하고 영어 v1/v2 지침·정책 6개·dev/holdout/calibration·offline fixture를 별도로 제공합니다.
영어 실행은 `--language en`을 명시하며 기존 명령의 기본값은 한국어입니다.
[데이터 번들](../../../data/README.ko.md)의 원본/번역 hash를 구분하고 ID·한도·적용일·판단·필수 인용의 동등성을 검사합니다.
번역 텍스트는 별도 dataset이며 오류 뒤의 대체값이 아닙니다.
영문 개발 지침을 고정한 뒤 영어 holdout을 준비했으며 최종 인수에만 사용합니다.

모델/API/SDK 식별자, 파일 경로, CLI flags, schema 필드명은 번역하지 않습니다.
오류 후 다른 언어의 fixture나 모델 응답을 대신 사용하지 않습니다.

언어 선택은 데이터를 바꾸지만 **설정한 Search 이름이나 소유권을 바꾸지는 않습니다**.
모델·로컬 검색 실험은 새 언어별 label로 구분합니다.
Search를 seed한 뒤 언어 또는 prefix를 바꾸려면 새 소유 이름을 가진 새 소스 복사본이 필요합니다.
기존 `outputs/azure-objects.json`은 원래 범위에 남겨 둡니다.
다음 label의 이름만 바꾸지 말고 [작업 폴더 범위 표](configuration.md#workspace-scope)를 따릅니다.

## 별도 촬영

국문/영문은 지침·데이터, 브라우저 locale, 액션 label, CLI/portal source recording, screenshot 디렉토리,
편집 영상, native evaluation run을 별도로 관리합니다.
같은 녹화 파일의 제목만 바꿔 두 언어라고 표시하지 않습니다.
챕터 카드와 실제 앱 화면, offline fixture와 live Azure, 초기 진단과 최종 비교는 명시적으로 구분합니다.

기존 화면·영상은 두 새 언어 세트의 재생과 문서 연결을 확인한 뒤 최종본에서 제거합니다.
원본 평가·실패·data/prompt/corpus/response/evaluator 계보는 보존합니다.

## 검사

```bash
python scripts/check_docs.py
```

두 언어 모두 명령 구문과 로컬 링크를 검사합니다.
해시로 승인하지 않은 번역 유예·오래된 완료 해시·명령 차이는 실패이며, 영문 재촬영 결과를 국문 점수로 복사하지 않습니다.
[로컬 품질 보고서](quality.md#verify-this-copy)에도 이 검사가 포함되며 실제 Azure 실행을 주장하지 않습니다.
