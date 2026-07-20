#!/usr/bin/env python3
"""Smoke the scientific-writing validator on a fixture with known blockers."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "skills/scientific-writing/validator.py"

BAD_FIXTURE = """# Results

Whales were abundant—especially near shipping lanes; density was high.
We conducted analyses and reconciled the patterns.
"""


class TestValidatorFixture(unittest.TestCase):
    def test_validator_flags_bad_prose(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "bad.md"
            path.write_text(BAD_FIXTURE, encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(VALIDATOR), "--file", str(path), "--mode", "normal"],
                capture_output=True,
                text=True,
            )
            combined = (proc.stdout or "") + (proc.stderr or "")
            self.assertNotEqual(
                proc.returncode,
                0,
                msg=f"expected non-zero exit; out={combined!r}",
            )
            self.assertTrue(
                "em_dash" in combined.lower() or "em dash" in combined.lower(),
                msg=combined,
            )


if __name__ == "__main__":
    unittest.main()
