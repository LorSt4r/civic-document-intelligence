# Civic Document Intelligence

A small, testable Python pipeline for turning public-administration documents
into structured records and reproducible anomaly indicators.

This repository is a sanitized engineering extract from a larger personal
research prototype. The original experiment used public municipal documents,
OCR, semantic search, and LLM-assisted investigation. The public version
contains **only synthetic documents** and a dependency-free deterministic
core. It makes no allegation about any real person, supplier, or authority.

## What it demonstrates

- parsing lightweight front matter and mixed European/US currency formats;
- separating deterministic extraction from later OCR or LLM adapters;
- detecting high-value outliers, recurring suppliers, and direct-award values
  above a configurable review threshold;
- identifying low-quality or likely broken OCR before analysis;
- producing machine-readable JSON with a CLI;
- testing the analytical rules against synthetic fixtures.

The indicators are review aids, not findings of wrongdoing. A recurring
supplier or a high amount can be entirely legitimate and always requires
source verification and domain context.

## Quick start

Python 3.11 or newer is sufficient; runtime dependencies are not required.

```bash
python -m pip install -e .
civic-intelligence scan examples/documents
civic-intelligence audit examples/documents
python -m unittest discover -s tests -v
```

## Input format

```markdown
---
title: Preventive maintenance service
supplier: Example Services Ltd
date: 2026-04-18
procedure: direct-award
status: ACTIVE
---

Approved amount: EUR 12,500.00.
```

The example corpus is fictional and exists solely to exercise the code.

## Architecture

```text
Markdown / OCR adapter
        |
        v
parser.py ------> typed DocumentRecord
                         |
              +----------+----------+
              |                     |
              v                     v
         analyzer.py            quality.py
              |                     |
              +----------+----------+
                         v
                    JSON report
```

## AI assistance

AI agents assisted the wider prototype and the extraction of this public
version. I defined the analytical boundaries, reviewed the implementation, and
validated the deterministic core with tests. No generated conclusion about a
real entity is included here.

## License

MIT. See [LICENSE](LICENSE).
