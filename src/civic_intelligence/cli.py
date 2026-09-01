from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .analyzer import analyze_documents, load_documents
from .quality import audit_documents


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="civic-intelligence")
    subcommands = parser.add_subparsers(dest="command", required=True)

    scan = subcommands.add_parser("scan", help="analyze a directory of Markdown documents")
    scan.add_argument("root", type=Path)
    scan.add_argument("--output", type=Path)

    audit = subcommands.add_parser("audit", help="report likely extraction-quality failures")
    audit.add_argument("root", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "scan":
        report = analyze_documents(load_documents(args.root)).as_dict()
        rendered = json.dumps(report, indent=2, ensure_ascii=False)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered + "\n", encoding="utf-8")
        print(rendered)
        return 0

    findings = [
        {**asdict(finding), "path": str(finding.path)}
        for finding in audit_documents(args.root)
    ]
    print(json.dumps(findings, indent=2, ensure_ascii=False))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
