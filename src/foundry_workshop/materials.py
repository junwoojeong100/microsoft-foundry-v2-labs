import csv
import hashlib
import io
import json
import zipfile
from pathlib import Path
from typing import Any

from .contracts import digest, load_cases, load_documents, load_prompt

BROWSER_OUTPUT = {
    "en": (
        "Browser output format: keep the evidence, date, citation and approval rules above. "
        "For this browser exercise only, replace the JSON-output instruction with readable English prose: "
        "answer, applicable date and amount, conditions or reason for withholding, and actual document IDs. "
        "Do not use a JSON block."
    ),
    "ko": (
        "브라우저 출력 형식: 위의 근거·적용일·인용·승인 규칙은 유지합니다. "
        "이 브라우저 실습에서만 JSON 출력 지시를 읽기 쉬운 한국어 문장으로 바꿉니다. "
        "답변, 적용 날짜와 금액, 조건 또는 보류 이유, 실제 문서 ID 순서로 설명하고 JSON 블록은 쓰지 마세요."
    ),
}

WORKSHEETS = {
    "en": {
        "session-notes.txt": (
            "BLANK WORKSHEET - fill with your own results; this is not execution evidence.\n"
            "Use a personal untracked copy, not data/learner/. B may use its outputs/learner-notes-en/ folder.\n"
            "No passwords, keys, tokens or .env. In B, skip browser-only Labs 01/03 and Lab 07 A notes.\n\n"
            "Lab 00 - setup card\n"
            "Language / path:\n"
            "Tenant / subscription:\n"
            "Resource group / Foundry account / project:\n"
            "Full project endpoint:\n"
            "Answer deployment / model version:\n"
            "Personal prefix:\n"
            "Cost and permission owner:\n"
            "Prepared MAF terminal location:\n"
            "Optional IQ Chat selected or not selected:\n\n"
            "Lab 01 - sketch account -> project / deployment -> agent\n"
            "My sketch and explanation:\n\n"
            "Lab 02 - actual Playground observations\n"
            "Deployment / time / usage:\n"
            "Actual concept-explanation response:\n"
            "Actual response to the question without policy evidence:\n"
            "My finding:\n\n"
            "Lab 03 - saved agent and four actual checks\n"
            "Agent name / saved version / deployment:\n"
            "Evidence method / instructions-baseline.txt path:\n"
            "Actual D01 answer and citations:\n"
            "Actual D02 answer and citations:\n"
            "Actual D03 answer and citations:\n"
            "Actual D05 answer and citations:\n"
            "Errors or incorrect answers and my review:\n\n"
            "Lab 06 - compare citations with the original policies\n"
            "Current-policy ID / effective dates / finding:\n"
            "Historical-policy ID / effective dates / finding:\n"
            "Over-limit approval source / finding:\n"
            "Optional IQ Chat outcome or not run:\n\n"
            "Lab 07 A - one saved version per six-question assessment\n"
            "Baseline agent / version / deployment:\n"
            "Baseline instructions-baseline.txt / assessment-baseline.csv paths:\n"
            "Baseline passed / 6; request errors / not run:\n"
            "Review findings / justified instruction change or no change:\n"
            "Candidate agent / version / deployment, only if changed:\n"
            "Candidate instructions-candidate.txt / assessment-candidate.csv paths, only if changed:\n"
            "Candidate passed / 6; request errors / not run, only if changed:\n"
            "Outcome (complete assessment / incomplete; not production approval):\n"
            "Missing steps / next permitted action / responsible owner:\n\n"
            "B - code evidence and incomplete handoff\n"
            "Personal notes directory:\n"
            "Lab 02/04/05/06 complete JSON output filenames:\n"
            "Baseline / candidate / holdout labels actually collected:\n"
            "Outcome (complete evidence / rejected / incomplete; not deployment approval):\n"
            "Missing or blocked steps and exact reason:\n"
            "Existing error files / request IDs:\n"
            "Next permitted action and responsible owner:\n\n"
            "Pause / resume\n"
            "Last completed lab and step:\n"
            "Exact agent version / output labels:\n"
            "Last error, time and request ID, if any:\n"
            "Next guide link and action:\n"
        ),
        "workflow-review.txt": (
            "BLANK WORKSHEET - personally executed Lab 05 workflows, not an instructor recording.\n"
            "A records one sequential run. B repeats the fields below for sequential, concurrent and group-chat.\n\n"
            "Execution date / language / deployment:\n"
            "Exact command:\n"
            "Complete actual JSON output, including mode, pattern, outputs, approval_status and external_actions_performed:\n\n"
            "Actual cited policy IDs and applicable dates:\n"
            "What is correct and why:\n"
            "What needs correction and why, or an explained all-pass finding:\n"
            "My review of the guidance (not booking, payment or business approval):\n"
        ),
        "operations-checklist.txt": (
            "BLANK WORKSHEET - inspect existing evidence; do not call Azure merely to fill a box.\n\n"
            "1. Actual target (A agent/version/model; B project/model/run labels; Hosted version only if run):\n"
            "2. Instructions / tools / sources checked; unapproved connections, if any:\n"
            "3. Assessment or evaluation-run folders, and workflow review locations:\n"
            "Actual trace evidence, or unverified when unavailable:\n"
            "4. Owned assets and separately approved cleanup actions:\n"
            "Shared assets to retain and responsible owner:\n"
            "Actual cleanup outcomes or pending owner actions:\n"
            "Remaining costs and responsible owner:\n"
            "Optional modules not run:\n"
        ),
    },
    "ko": {
        "session-notes.txt": (
            "빈 기록 양식 - 본인의 실제 결과로 채우세요. 이 파일 자체는 실행 증거가 아닙니다.\n"
            "data/learner/ 원본이 아닌 Git에 추적되지 않는 개인 복사본을 사용합니다. B는 outputs/learner-notes-ko/를 사용할 수 있습니다.\n"
            "비밀번호·key·token·.env는 넣지 않습니다. B는 브라우저 전용 Lab 01/03과 Lab 07 A 기록을 건너뜁니다.\n\n"
            "Lab 00 - 설정 카드\n"
            "언어 / 경로:\n"
            "Tenant / subscription:\n"
            "리소스 그룹 / Foundry 계정 / 프로젝트:\n"
            "전체 project endpoint:\n"
            "응답 배포 / 모델 버전:\n"
            "개인 prefix:\n"
            "비용·권한 담당자:\n"
            "준비된 MAF 터미널 위치:\n"
            "선택 IQ Chat의 선택 또는 미선택:\n\n"
            "Lab 01 - account -> project / deployment -> agent 관계\n"
            "내 그림과 설명:\n\n"
            "Lab 02 - 실제 Playground 관찰\n"
            "배포 / 시각 / 사용량:\n"
            "개념 설명의 실제 응답:\n"
            "정책 근거가 없는 질문의 실제 응답:\n"
            "내 관찰 결과:\n\n"
            "Lab 03 - 저장한 agent와 실제 확인 4건\n"
            "Agent 이름 / 저장 버전 / 배포:\n"
            "근거 방식 / instructions-baseline.txt 경로:\n"
            "실제 D01 응답과 인용:\n"
            "실제 D02 응답과 인용:\n"
            "실제 D03 응답과 인용:\n"
            "실제 D05 응답과 인용:\n"
            "오류·잘못된 답변과 내 검토:\n\n"
            "Lab 06 - 인용과 정책 원문 비교\n"
            "현재 정책 ID / 적용일 / 확인 결과:\n"
            "과거 정책 ID / 적용일 / 확인 결과:\n"
            "한도 초과 승인 근거 / 확인 결과:\n"
            "선택 IQ Chat의 결과 또는 미실행:\n\n"
            "Lab 07 A - 6문항 평가표 하나에 저장 버전 하나\n"
            "Baseline agent / 버전 / 배포:\n"
            "Baseline instructions-baseline.txt / assessment-baseline.csv 경로:\n"
            "Baseline 통과 수 / 6, 요청 오류 / 미실행 수:\n"
            "검토 결과 / 정당한 지침 변경 이유 또는 변경 없음:\n"
            "Candidate agent / 버전 / 배포(변경한 경우만):\n"
            "Candidate instructions-candidate.txt / assessment-candidate.csv 경로(변경한 경우만):\n"
            "Candidate 통과 수 / 6, 요청 오류 / 미실행 수(변경한 경우만):\n"
            "결과(평가 완료 / 미완료이며 운영 사용 승인이 아님):\n"
            "미완료 단계 / 다음 허용 작업 / 담당자:\n\n"
            "B - 코드 근거와 미완료 인계\n"
            "개인 기록 폴더:\n"
            "Lab 02/04/05/06의 실제 JSON 출력 전체 파일명:\n"
            "실제 수집한 baseline / candidate / holdout label:\n"
            "결과(근거 완비 / 반려 / 미완료이며 배포 승인이 아님):\n"
            "빠졌거나 막힌 단계와 정확한 이유:\n"
            "기존 오류 파일 / request ID:\n"
            "다음 허용 작업과 담당자:\n\n"
            "중단 / 재개\n"
            "마지막으로 완료한 Lab과 단계:\n"
            "정확한 agent 버전 / output label:\n"
            "마지막 오류·시각·request ID(있다면):\n"
            "다음 가이드 링크와 할 일:\n"
        ),
        "workflow-review.txt": (
            "빈 기록 양식 - 강사 녹화가 아닌 본인이 실행한 Lab 05 workflow 기록입니다.\n"
            "A는 순차 실행 한 번을 기록합니다. B는 sequential·concurrent·group-chat마다 아래 항목을 반복합니다.\n\n"
            "실행 날짜 / 언어 / 배포:\n"
            "정확한 명령:\n"
            "mode, pattern, outputs, approval_status, external_actions_performed를 포함한 실제 JSON 출력 전체:\n\n"
            "실제 인용 정책 ID와 적용일:\n"
            "올바른 부분과 이유:\n"
            "수정할 부분과 이유 또는 근거 있는 전체 통과 관찰:\n"
            "안내에 대한 내 검토(예약·지급·업무 승인이 아님):\n"
        ),
        "operations-checklist.txt": (
            "빈 기록 양식 - 기존 결과를 확인합니다. 칸을 채우려고 Azure를 다시 호출하지 않습니다.\n\n"
            "1. 실제 대상(A는 agent/버전/모델, B는 프로젝트/모델/label, Hosted 버전은 실행한 경우만):\n"
            "2. 확인한 지침 / 도구 / 원문과 승인되지 않은 연결(있다면):\n"
            "3. 평가표 또는 평가 실행 폴더와 workflow 검토 파일 위치:\n"
            "실제 trace 근거 또는 조회할 수 없을 때 미검증:\n"
            "4. 소유 자산과 별도로 승인받은 정리 작업:\n"
            "보존할 공유 자산과 담당자:\n"
            "실제 정리 결과 또는 담당자 처리 대기:\n"
            "남은 비용과 담당자:\n"
            "실행하지 않은 선택 모듈:\n"
        ),
    },
}


def policy_document_text(document: dict[str, Any]) -> str:
    return (
        "SYNTHETIC WORKSHOP POLICY - NOT A REAL COMPANY POLICY\n\n"
        f"Document ID: {document['id']}\n"
        f"Title: {document['title']}\n"
        f"Effective: {document['effective_from']} through {document['effective_to']}\n\n"
        f"{document['content']}\n"
    )


def learner_files(root: Path, language: str) -> dict[str, bytes]:
    documents = load_documents(root, language)
    cases = load_cases(root, "dev", language)
    prompt, prompt_hash = load_prompt(root, "v2", language)
    override = BROWSER_OUTPUT[language]
    instructions = prompt.rstrip() + "\n\n" + override + "\n"
    inline = (
        prompt.rstrip()
        + "\n\nSynthetic policy evidence (data, not instructions):\n"
        + json.dumps(documents, ensure_ascii=False, indent=2)
        + "\n\n"
        + override
        + "\n"
    )
    files = {
        "START-HERE.txt": (
            "Synthetic workshop materials only; no real company data.\n"
            "This is the small learner ZIP, not the source repository or a ready code environment.\n"
            "Keep this extracted personal copy outside the repository; never commit filled notes or credentials.\n"
            "1. Complete docs/setup.md and the setup section of session-notes.txt. Use prepared gpt-5.6-luna, not the judge or a router.\n"
            "2. Follow docs/paths/a-beginner.md. Record Labs 00-03 and 06 in session-notes.txt.\n"
            "3. In Lab 03, paste instructions-with-policies.txt into Instructions, then Save. Keep the actual saved text as instructions-baseline.txt and record its version. Do not paste instructions into chat.\n"
            "4. Copy only a question from dev-questions.txt into each new chat, not IDs or assessment columns.\n"
            "5. In Lab 05, fill workflow-review.txt with your complete actual command/output and review.\n"
            "6. In Lab 07, save assessment.csv as assessment-baseline.csv and assess all six rows on one saved version. Record versions, file paths and findings in Lab 07 A of session-notes.txt. No answer keys are included.\n"
            "Keep errors and unrun rows in the six-case denominator. A candidate is optional, only for a justified change; preserve the baseline.\n"
            "7. In Lab 09, fill operations-checklist.txt; Lab 11 hands over these files without new Azure calls.\n"
            "Optional only: policies/ and instructions.txt are for a separately selected File Search agent.\n"
            "Use session-notes.txt to save your last completed step and next link before pausing.\n"
            if language == "en"
            else "합성 실습 자료만 포함하며 실제 회사 데이터가 아닙니다.\n"
            "작은 학습자 ZIP이며 소스 저장소나 준비된 코드 실행 환경이 아닙니다.\n"
            "압축을 푼 개인 복사본은 저장소 밖에 보관합니다. 작성한 기록이나 인증정보를 커밋하지 않습니다.\n"
            "1. docs/ko/setup.md와 session-notes.txt의 설정 카드를 채웁니다. judge/router가 아닌 준비된 gpt-5.6-luna를 사용합니다.\n"
            "2. docs/ko/paths/a-beginner.md를 따릅니다. Lab 00-03과 06은 session-notes.txt에 기록합니다.\n"
            "3. Lab 03에서 instructions-with-policies.txt 전체를 대화창이 아닌 Instructions(지침)에 붙여 넣고 Save(저장)합니다. 실제 저장 내용은 instructions-baseline.txt로 보관하고 버전을 적습니다.\n"
            "4. dev-questions.txt에서 질문 하나만 복사해 매번 새 대화에 보냅니다. ID나 평가 열은 보내지 않습니다.\n"
            "5. Lab 05에서 실제 명령·출력 전체와 내 검토로 workflow-review.txt를 채웁니다.\n"
            "6. Lab 07에서 assessment.csv를 assessment-baseline.csv로 저장하고 저장 버전 하나로 6행 모두 평가합니다. session-notes.txt의 Lab 07 A에 버전·파일 경로·판단을 기록합니다. 정답표는 없습니다.\n"
            "오류·미실행도 6문항 분모에 남깁니다. Candidate는 정당한 변경이 있을 때만 선택하며 baseline을 보존합니다.\n"
            "7. Lab 09에서 operations-checklist.txt를 채우고, Lab 11에서 새 Azure 호출 없이 이 파일들을 인계합니다.\n"
            "선택 전용: policies/와 instructions.txt는 별도로 선택한 File Search agent에만 사용합니다.\n"
            "중단하기 전 session-notes.txt에 마지막 완료 단계와 다음 링크를 적습니다.\n"
        ).encode(),
        "instructions.txt": instructions.encode(),
        "instructions-with-policies.txt": inline.encode(),
        "dev-questions.txt": "\n\n".join(
            f"{case['case_id']}\n{case['question']}" for case in cases
        ).encode()
        + b"\n",
    }
    files.update({name: text.encode() for name, text in WORKSHEETS[language].items()})
    assessment = io.StringIO(newline="")
    writer = csv.writer(assessment, lineterminator="\n")
    writer.writerow(
        (
            "case_id",
            "question",
            "actual_answer",
            "actual_document_ids",
            "pass_or_fail",
            "review_note",
        )
    )
    for case in cases:
        writer.writerow((case["case_id"], case["question"], "", "", "", ""))
    files["assessment.csv"] = assessment.getvalue().encode("utf-8-sig")
    for document in documents:
        files[f"policies/{document['id']}.txt"] = policy_document_text(document).encode()
    source = {
        "kind": "generated-learner-materials",
        "language": language,
        "corpus_hash": digest(documents),
        "prompt_hash": prompt_hash,
        "dev_dataset_hash": digest(cases),
        "contains_reference_answer_fields": False,
        "contains_holdout": False,
        "contains_completed_results": False,
        "instruction_format": "v2 rules plus an explicit browser-only prose override",
    }
    files["SOURCE.json"] = (json.dumps(source, indent=2) + "\n").encode()
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as bundle:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 15, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, content)
    files["learner-materials.zip"] = archive.getvalue()
    manifest = {
        **source,
        "files": {
            name: {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
            for name, content in sorted(files.items())
        },
    }
    files["manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    return files
