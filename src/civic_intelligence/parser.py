from __future__ import annotations

import re
from pathlib import Path

from .models import DocumentRecord


AMOUNT_PATTERN = re.compile(
    r"(?:EUR|€)\s*([0-9][0-9., ]*)|([0-9][0-9., ]*)\s*(?:EUR|€)",
    re.IGNORECASE,
)


def split_front_matter(text: str) -> tuple[dict[str, str], str]:
    """Parse the intentionally small `key: value` metadata subset we accept."""
    if not text.startswith("---\n"):
        return {}, text

    marker = text.find("\n---\n", 4)
    if marker < 0:
        return {}, text

    metadata: dict[str, str] = {}
    for line in text[4:marker].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip().casefold()] = value.strip().strip('"')
    return metadata, text[marker + 5 :]


def normalize_amount(raw: str) -> float:
    value = raw.replace(" ", "")
    if "," in value and "." in value:
        decimal = "," if value.rfind(",") > value.rfind(".") else "."
        thousands = "." if decimal == "," else ","
        value = value.replace(thousands, "").replace(decimal, ".")
    elif "," in value:
        head, tail = value.rsplit(",", 1)
        value = f"{head.replace(',', '')}.{tail}" if len(tail) <= 2 else value.replace(",", "")
    elif "." in value:
        head, tail = value.rsplit(".", 1)
        value = f"{head.replace('.', '')}.{tail}" if len(tail) <= 2 else value.replace(".", "")
    return float(value)


def extract_amounts(text: str) -> tuple[float, ...]:
    amounts: list[float] = []
    for match in AMOUNT_PATTERN.finditer(text):
        raw = (match.group(1) or match.group(2)).strip()
        try:
            amount = normalize_amount(raw)
        except ValueError:
            continue
        if 0 < amount < 1_000_000_000:
            amounts.append(amount)
    return tuple(amounts)


def parse_document(path: Path) -> DocumentRecord:
    text = path.read_text(encoding="utf-8", errors="replace")
    metadata, body = split_front_matter(text)
    date_match = re.search(r"\b(20\d{2})\b", metadata.get("date", "") or path.name)
    return DocumentRecord(
        path=path,
        title=metadata.get("title", path.stem.replace("_", " ")),
        body=body,
        amounts=extract_amounts(body),
        supplier=metadata.get("supplier") or None,
        procedure=metadata.get("procedure") or None,
        status=metadata.get("status") or None,
        year=int(date_match.group(1)) if date_match else None,
    )
