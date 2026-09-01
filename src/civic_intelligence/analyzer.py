from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import median

from .models import DocumentRecord
from .parser import parse_document


@dataclass(frozen=True)
class AnalysisReport:
    document_count: int
    median_amount: float
    high_value: tuple[dict, ...]
    recurring_suppliers: tuple[dict, ...]
    direct_awards_for_review: tuple[dict, ...]

    def as_dict(self) -> dict:
        return asdict(self)


def load_documents(root: Path) -> list[DocumentRecord]:
    documents = [parse_document(path) for path in sorted(root.rglob("*.md"))]
    return [doc for doc in documents if (doc.status or "").casefold() != "quarantined"]


def analyze_documents(
    documents: list[DocumentRecord],
    *,
    recurring_threshold: int = 2,
    outlier_multiplier: float = 3.0,
    high_value_floor: float = 10_000,
    direct_award_review_threshold: float = 40_000,
) -> AnalysisReport:
    all_amounts = [amount for document in documents for amount in document.amounts]
    median_amount = float(median(all_amounts)) if all_amounts else 0.0
    high_threshold = max(high_value_floor, median_amount * outlier_multiplier)

    supplier_documents: Counter[str] = Counter()
    supplier_amounts: defaultdict[str, list[float]] = defaultdict(list)
    high_value: list[dict] = []
    direct_awards: list[dict] = []

    for document in documents:
        if document.supplier:
            supplier_documents[document.supplier] += 1
            supplier_amounts[document.supplier].extend(document.amounts)

        for amount in document.amounts:
            item = {
                "title": document.title,
                "supplier": document.supplier,
                "amount": amount,
                "source": str(document.path),
            }
            if amount > high_threshold:
                high_value.append(item)
            if (
                (document.procedure or "").casefold() == "direct-award"
                and amount > direct_award_review_threshold
            ):
                direct_awards.append(item)

    recurring = [
        {
            "supplier": supplier,
            "document_count": count,
            "total_extracted_amount": round(sum(supplier_amounts[supplier]), 2),
        }
        for supplier, count in supplier_documents.most_common()
        if count >= recurring_threshold
    ]

    return AnalysisReport(
        document_count=len(documents),
        median_amount=round(median_amount, 2),
        high_value=tuple(sorted(high_value, key=lambda item: item["amount"], reverse=True)),
        recurring_suppliers=tuple(recurring),
        direct_awards_for_review=tuple(
            sorted(direct_awards, key=lambda item: item["amount"], reverse=True)
        ),
    )
