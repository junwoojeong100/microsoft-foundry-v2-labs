# 합성 데이터와 언어별 번들

[English](README.md) | **한국어**

가상 한빛기술의 실습 자료이며 실제 회사 규정이 아닙니다.

| 자료 | 한국어 원본 | 영어 버전 |
|---|---|---|
| 정책 6개 | `knowledge/policies.json` | `knowledge/en/policies.json` |
| dev 6개 | `evaluation/dev.jsonl` | `evaluation/en/dev.jsonl` |
| 최종 holdout 4개 | `evaluation/holdout.jsonl` | `evaluation/en/holdout.jsonl` |
| 정답/오답 judge fixture | `evaluation/calibration.jsonl` | `evaluation/en/calibration.jsonl` |
| offline 답변 fixture | `fixtures/answers.json` | `fixtures/en/answers.json` |
| v1/v2 지침 | `../prompts/v1.txt`, `../prompts/v2.txt` | `../prompts/en/v1.txt`, `../prompts/en/v2.txt` |

저장소 루트에서 영어 번들을 명시적으로 선택합니다.

```bash
python scripts/workshop.py --language en doctor
python scripts/workshop.py --language en demo --label english-offline --prompt v2
```

기존 명령의 기본 언어는 한국어를 유지합니다. 영어 파일 누락이나 오류 뒤에 한국어로 fallback하지 않습니다.
언어는 Hosted profile과 dataset/prompt/corpus hash에 남습니다.
서로 다른 언어의 데이터셋을 같은 입력의 모델/지침 실험으로 비교하지 않습니다.

`localization.json`은 원본·번역 파일 해시를 고정합니다. ID·날짜·금액·판단·필수 인용은 동등하지만 번역 텍스트의 hash는 별도입니다.
영문 개발 자료와 실제 workflow 지침을 먼저 고정한 뒤 번역된 holdout을 준비했습니다.
Holdout은 최종 인수용이며 fixture는 미리 작성한 예제이지 Azure 응답이 아닙니다.

## 바로 쓰는 브라우저 자료

[국문 학습자 ZIP](learner/ko/learner-materials.zip) · [영문 학습자 ZIP](learner/en/learner-materials.zip) · [준비·파일별 사용 순서](../docs/ko/setup.md)

`data/learner/<language>/`는 해당 언어의 canonical v2 지침·정책 6개·**dev만**으로 생성합니다.
인라인/브라우저 지침, TXT 원문 6개, 정답 필드 없는 질문, 빈 6행 평가표가 있습니다.
빈 `session-notes.txt`, `workflow-review.txt`, `operations-checklist.txt`로 설정·관찰·중단/재개·최종 인계를 기록합니다.
완료된 결과가 들어 있는 파일이 아닙니다. 저장소 밖의 개인 복사본이나 B의 Git-ignored `outputs/learner-notes-ko/`를 채웁니다.
`data/learner/`의 생성 파일에 직접 작성하지 않습니다.
브라우저 문장 출력 지시는 명시적인 추가 규칙이며 동결 지침·평가 데이터를 바꾸지 않습니다.
`SOURCE.json`과 파일별 manifest가 입력/출력 hash를 보존합니다. ZIP에는 holdout·정답표가 없습니다.

관리자는 `python scripts/build_learner_materials.py`로 저장된 바이트를 검사하고
`--write`로 두 번들을 명시적으로 재생성합니다. 학습자의 작성 평가표는 이 생성 폴더 밖에 저장합니다.
