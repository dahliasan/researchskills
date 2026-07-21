#!/usr/bin/env python3
"""Smoke tests for the manuscript-writing validator."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "skills/manuscript-writing/validator.py"


class TestValidatorFixture(unittest.TestCase):
    def run_validator(self, text: str, *args: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "draft.md"
            path.write_text(text, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(VALIDATOR), "--file", str(path), *args],
                capture_output=True,
                text=True,
            )

    def test_unresolved_placeholder_is_blocker(self) -> None:
        proc = self.run_validator("# Methods\n\nWe used [TBC] folds.\n")
        self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("unresolved_placeholder", proc.stdout)

    def test_section_filter_excludes_other_sections(self) -> None:
        text = "# Methods\n\nWe used [TBC] folds.\n\n# Results\n\nOccupancy increased.\n"
        proc = self.run_validator(text, "--section", "Results")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertNotIn("unresolved_placeholder", proc.stdout)

    def test_results_interpretation_is_warning_not_blocker(self) -> None:
        proc = self.run_validator("# Results\n\nThis suggests that prey limitation drove the pattern.\n")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("results_interpretation", proc.stdout)
        self.assertIn("causal_language", proc.stdout)


if __name__ == "__main__":
    unittest.main()
