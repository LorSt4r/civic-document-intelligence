from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DocumentRecord:
    path: Path
    title: str
    body: str
    amounts: tuple[float, ...]
    supplier: str | None
    procedure: str | None
    status: str | None
    year: int | None
