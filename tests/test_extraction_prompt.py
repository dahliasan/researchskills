"""Offline tests for PROTOCOL-templated extraction prompt rendering."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "literature-review" / "scripts"
TEMPLATE = ROOT / "skills" / "literature-review" / "references" / "extraction-prompt.md"
EXAMPLE = ROOT / "schemas" / "examples" / "paper-extraction.v1.example.json"

import importlib.util


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


class RenderExtractionPromptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.render_mod = _load(
            "render_extraction_prompt",
            SCRIPTS / "render_extraction_prompt.py",
        )
        cls.validate_mod = _load(
            "validate_extraction",
            SCRIPTS / "validate_extraction.py",
        )

    def test_render_injects_protocol_fields(self) -> None:
        protocol = """---
name: nzsl-pup-weather
review_type: scoping
question_framework: PCC
question:
  population: New Zealand sea lion pups
  concept: weather-related mortality
  context: Campbell Island
eligibility:
  include:
    - Weather or climate effects on pinniped pup survival
  exclude:
    - Unrelated fisheries bycatch only
extraction:
  schema: researchskills.extraction.v1
  extra_fields:
    - name: weather_metric
      type: string
      description: Named weather exposure metric if stated.
---

## Overview

Review of weather drivers of NZSL pup mortality.

## Question

How do cold and rain relate to pup deaths?
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "PROTOCOL.md"
            path.write_text(protocol, encoding="utf-8")
            data, sections = self.render_mod.parse_protocol(path.read_text(encoding="utf-8"))
            prompt = self.render_mod.render(
                TEMPLATE.read_text(encoding="utf-8"), data, sections
            )
        self.assertIn("researchskills.extraction.v1", prompt)
        self.assertIn("nzsl-pup-weather", prompt)
        self.assertIn("New Zealand sea lion pups", prompt)
        self.assertIn("weather_metric", prompt)
        self.assertIn("Weather or climate effects on pinniped pup survival", prompt)
        self.assertNotIn("{{", prompt)
        self.assertNotIn("MegaMove", prompt)
        self.assertNotIn("BRT", prompt)

    def test_example_validates(self) -> None:
        import json

        doc = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        schema = json.loads(
            (ROOT / "schemas" / "paper-extraction.v1.schema.json").read_text(encoding="utf-8")
        )
        errors = self.validate_mod.validate(doc, schema)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
