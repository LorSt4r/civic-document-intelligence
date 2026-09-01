import unittest
from pathlib import Path

from civic_intelligence.analyzer import analyze_documents
from civic_intelligence.models import DocumentRecord


def record(title: str, supplier: str, amount: float, procedure: str = "open-procedure"):
    return DocumentRecord(
        path=Path(f"{title}.md"),
        title=title,
        body="synthetic",
        amounts=(amount,),
        supplier=supplier,
        procedure=procedure,
        status="ACTIVE",
        year=2026,
    )


class AnalyzerTest(unittest.TestCase):
    def test_flags_review_indicators_without_claiming_wrongdoing(self):
        report = analyze_documents(
            [
                record("one", "Example Ltd", 1_000),
                record("two", "Example Ltd", 2_000),
                record("three", "Another PLC", 60_000, "direct-award"),
            ]
        )
        self.assertEqual(report.document_count, 3)
        self.assertEqual(report.recurring_suppliers[0]["supplier"], "Example Ltd")
        self.assertEqual(report.direct_awards_for_review[0]["amount"], 60_000)
        self.assertEqual(report.high_value[0]["title"], "three")


if __name__ == "__main__":
    unittest.main()
