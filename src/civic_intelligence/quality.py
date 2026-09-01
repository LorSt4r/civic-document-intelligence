from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .parser import split_front_matter


@dataclass(frozen=True)
class QualityFinding:
    path: Path
    reason: str


def looks_like_broken_ocr(text: str, *, symbol_threshold: float = 0.35) -> bool:
    compact = re.sub(r"\s+", "", text)
    if not compact:
        return True
    symbols = sum(not character.isalnum() for character in compact)
    return symbols / len(compact) > symbol_threshold


def audit_documents(root: Path, *, minimum_characters: int = 80) -> list[QualityFinding]:
    findings: list[QualityFinding] = []
    for path in sorted(root.rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        _, body = split_front_matter(text)
        clean_body = body.strip()
        if len(clean_body) < minimum_characters:
            findings.append(QualityFinding(path, "content too short"))
        elif looks_like_broken_ocr(clean_body):
            findings.append(QualityFinding(path, "high symbol ratio; possible OCR failure"))
    return findings
