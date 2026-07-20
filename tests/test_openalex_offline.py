#!/usr/bin/env python3
"""Offline tests for discover-papers OpenAlex helper (no network)."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/discover-papers/scripts/openalex_search.py"


def load_mod():
    spec = importlib.util.spec_from_file_location("openalex_search", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


class TestQueryResolution(unittest.TestCase):
    def setUp(self) -> None:
        self.mod = load_mod()

    def test_queries_list_wins(self) -> None:
        qs = self.mod.search_queries_from_snapshot(
            {"search": {"queries": [" a ", "", "b"]}, "question": {"population": "P"}}
        )
        self.assertEqual(qs, ["a", "b"])

    def test_pcc_fallback(self) -> None:
        qs = self.mod.search_queries_from_snapshot(
            {
                "question": {
                    "population": "fur seals",
                    "concept": "census",
                    "context": "Heard Island",
                }
            }
        )
        self.assertEqual(qs, ["fur seals census Heard Island"])

    def test_name_fallback(self) -> None:
        qs = self.mod.search_queries_from_snapshot({"name": "my-review"})
        self.assertEqual(qs, ["my-review"])

    def test_protocol_template_parses_queries(self) -> None:
        template = (
            ROOT / "skills/protocol/references/protocol-template.md"
        ).read_text(encoding="utf-8")
        snap = self.mod._parse_yaml_frontmatter(template)
        qs = self.mod.search_queries_from_snapshot(snap)
        self.assertTrue(qs)
        self.assertIn("OpenAlex", qs[0])

    def test_protocol_file_roundtrip(self) -> None:
        body = """---
name: t
search:
  queries:
    - "alpha beta"
    - "gamma"
question:
  population: "P"
date_range:
  from: "2020-01-01"
  to: "2024-12-31"
---

## Overview
x
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "PROTOCOL.md"
            path.write_text(body, encoding="utf-8")
            snap = self.mod._parse_yaml_frontmatter(path.read_text(encoding="utf-8"))
            self.assertEqual(
                self.mod.search_queries_from_snapshot(snap), ["alpha beta", "gamma"]
            )


if __name__ == "__main__":
    unittest.main()
