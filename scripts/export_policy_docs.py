#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from foundry_workshop.contracts import load_documents  # noqa: E402


def export(root: Path) -> Path:
    destination = root / "outputs/policy-documents"
    destination.mkdir(parents=True, exist_ok=False)
    for document in load_documents(root):
        text = (
            "SYNTHETIC WORKSHOP POLICY - NOT A REAL COMPANY POLICY\n\n"
            f"Document ID: {document['id']}\n"
            f"Title: {document['title']}\n"
            f"Effective: {document['effective_from']} through {document['effective_to']}\n\n"
            f"{document['content']}\n"
        )
        (destination / f"{document['id']}.txt").write_text(text, encoding="utf-8")
    return destination


if __name__ == "__main__":
    try:
        print(export(ROOT))
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
