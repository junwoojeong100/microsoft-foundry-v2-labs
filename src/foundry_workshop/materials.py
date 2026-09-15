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
            "1. Use the prepared gpt-5.6-luna deployment, not the judge or a router.\n"
            "2. Paste instructions-with-policies.txt into the agent's Instructions field, then Save.\n"
            "3. Copy one question at a time from dev-questions.txt into a new chat. Do not paste assessment columns.\n"
            "4. Record your own responses in assessment.csv; it contains no answer keys.\n"
            "5. policies/ contains the six original text files for the optional File Search path.\n"
            "Follow docs/labs/00-start.md and docs/setup.md for prerequisites, costs and permissions.\n"
            if language == "en"
            else "합성 실습 자료만 포함하며 실제 회사 데이터가 아닙니다.\n"
            "1. 준비된 gpt-5.6-luna 배포를 사용합니다. judge나 router를 고르지 않습니다.\n"
            "2. instructions-with-policies.txt 전체를 agent의 Instructions(지침)에 붙여 넣고 Save(저장)합니다.\n"
            "3. dev-questions.txt에서 질문 하나만 복사해 새 대화에 보냅니다. 평가 열을 붙여 넣지 않습니다.\n"
            "4. 실제 응답을 assessment.csv에 기록합니다. 이 파일에는 정답표가 없습니다.\n"
            "5. policies/는 선택 File Search 경로에 올릴 원문 텍스트 6개입니다.\n"
            "준비물·비용·권한은 docs/ko/labs/00-start.md와 docs/ko/setup.md를 따릅니다.\n"
        ).encode(),
        "instructions.txt": instructions.encode(),
        "instructions-with-policies.txt": inline.encode(),
        "dev-questions.txt": "\n\n".join(
            f"{case['case_id']}\n{case['question']}" for case in cases
        ).encode()
        + b"\n",
    }
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
