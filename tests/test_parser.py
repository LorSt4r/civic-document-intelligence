import tempfile
import unittest
from pathlib import Path

from civic_intelligence.parser import extract_amounts, parse_document


class ParserTest(unittest.TestCase):
    def test_extracts_european_and_us_amounts(self):
        self.assertEqual(extract_amounts("€ 12.500,00 and EUR 145,000.50"), (12500.0, 145000.5))

    def test_parses_metadata_and_year(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.md"
            path.write_text(
                "---\ntitle: Test record\nsupplier: Example Ltd\ndate: 2026-04-18\n---\nEUR 10.00",
                encoding="utf-8",
            )
            record = parse_document(path)
        self.assertEqual(record.title, "Test record")
        self.assertEqual(record.supplier, "Example Ltd")
        self.assertEqual(record.year, 2026)
        self.assertEqual(record.amounts, (10.0,))


if __name__ == "__main__":
    unittest.main()
