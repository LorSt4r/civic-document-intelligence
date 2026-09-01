import tempfile
import unittest
from pathlib import Path

from civic_intelligence.quality import audit_documents, looks_like_broken_ocr


class QualityTest(unittest.TestCase):
    def test_detects_symbol_heavy_text(self):
        self.assertTrue(looks_like_broken_ocr("@@@###%%%abc"))
        self.assertFalse(looks_like_broken_ocr("A normal administrative sentence with words."))

    def test_audit_reports_short_document(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "short.md"
            path.write_text("too short", encoding="utf-8")
            findings = audit_documents(Path(directory))
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].reason, "content too short")


if __name__ == "__main__":
    unittest.main()
