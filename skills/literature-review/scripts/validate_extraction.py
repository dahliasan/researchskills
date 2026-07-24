#!/usr/bin/env python3
"""Validate a paper-card JSON against researchskills.extraction.v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[3]
DEFAULT_SCHEMA = REPO / "schemas" / "paper-extraction.v1.schema.json"

REQUIRED = [
    "schema_version",
    "file",
    "metadata",
    "reader_summary",
    "background",
    "key_findings",
    "methods",
    "focal_taxa",
    "domain",
    "study_design",
    "evidence_type",
    "gaps_and_recommendations",
    "key_cited_works",
]


def _lightweight_check(doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if doc.get("schema_version") != "researchskills.extraction.v1":
        errors.append(
            f'schema_version must be "researchskills.extraction.v1", got {doc.get("schema_version")!r}'
        )
    for key in REQUIRED:
        if key not in doc:
            errors.append(f"missing required key: {key}")
    file_block = doc.get("file")
    if isinstance(file_block, dict):
        for key in ("paper_id", "extracted_at", "extractor_version"):
            if key not in file_block:
                errors.append(f"missing file.{key}")
    else:
        errors.append("file must be an object")
    return errors


def validate(doc: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    try:
        import jsonschema
    except ImportError:
        return _lightweight_check(doc)

    validator = jsonschema.Draft202012Validator(schema)
    return [
        f"{'/'.join(str(p) for p in err.path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="Extraction JSON file(s)")
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA,
        help="JSON Schema path (default: schemas/paper-extraction.v1.schema.json)",
    )
    args = parser.parse_args(argv)

    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    failed = 0
    for path in args.paths:
        doc = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(doc, dict):
            print(f"FAIL {path}: not a JSON object", file=sys.stderr)
            failed += 1
            continue
        errors = validate(doc, schema)
        if errors:
            failed += 1
            print(f"FAIL {path}", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)
        else:
            print(f"OK {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
