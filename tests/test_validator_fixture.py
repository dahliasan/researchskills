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

    # Each case below follows a sentence an author had to correct in a real draft (wording generalised).
    def test_announcing_opener_from_real_drafts(self) -> None:
        for opener in (
            "Connectivity and food may also differ between the study island and other colonies. At a second island, growth slowed.",
            "The endangered study species provides a direct conservation test of this question (IUCN, 2025).",
        ):
            proc = self.run_validator(f"# Discussion\n\n{opener}\n")
            self.assertIn("announcing_opener", proc.stdout, opener)
        proc = self.run_validator("# Discussion\n\nReduced immigration could also slow growth at the study island.\n")
        self.assertNotIn("announcing_opener", proc.stdout)

    def test_unsupported_gap_claim_from_real_draft(self) -> None:
        text = ("# Abstract\n\nHigh early pup mortality limits recovery of the endangered study species, "
                "yet managers lack a weather threshold to identify when daily mortality rises.\n")
        self.assertIn("unsupported_gap", self.run_validator(text).stdout)

    def test_repeated_threshold_and_citation(self) -> None:
        paras = [
            "Mortality rose on days at or below 0 °C (Smith & Jones, 2019).",
            "Days at or below 0 °C were also wet (Smith & Jones, 2019).",
            "Forecasts of 0 °C could guide monitoring (Smith & Jones, 2019).",
            "Testing the 0 °C threshold elsewhere would help.",
        ]
        proc = self.run_validator("# Discussion\n\n" + "\n\n".join(paras) + "\n")
        self.assertIn("repeated_citation", proc.stdout)
        self.assertIn("repeated_value", proc.stdout)

    def test_discussion_much_longer_than_introduction(self) -> None:
        text = "# Introduction\n\n" + "word " * 200 + "\n\n# Discussion\n\n" + "word " * 500 + "\n"
        self.assertIn("discussion_length", self.run_validator(text).stdout)

    def test_avoid_words_read_from_voice_profile(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            profile = Path(td) / "voice.md"
            profile.write_text("# Voice\n\n## Words to avoid\n\n- `precipitate`, `confer`, `bound how...`\n\n## Other\n\n- `keep`\n", encoding="utf-8")
            proc = self.run_validator("# Discussion\n\nCold weather may precipitate deaths in lean pups.\n", "--avoid-words", str(profile))
        self.assertIn("avoid_word", proc.stdout)
        self.assertIn("precipitate", proc.stdout)


if __name__ == "__main__":
    unittest.main()
