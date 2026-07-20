#!/usr/bin/env python3
"""
Scientific writing validator: Deterministic prose gates and guardrails.

Checks Markdown manuscripts against style rules from SKILL.md:
  - Em dashes (blockers)
  - Readability scores (Flesch-Kincaid, Coleman-Liau)
  - Semicolons in prose (warnings)
  - Jargon density (warnings)
  - Acronym definition (warnings)
  - Results/Discussion boundary enforcement (blockers)

Usage:
  python validator.py --file manuscript.md --mode strict
  python validator.py --file manuscript.md --section Results
  python validator.py --file manuscript.md --quiet

Output: PASS / WARN / FAIL with line numbers and suggestions.
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple

try:
    import textstat
except ImportError:
    textstat = None
    print("Warning: textstat not installed. Readability checks disabled.")
    print("Install with: pip install textstat")


class ProseValidator:
    """Validate scientific prose against style rules."""

    # Rule definitions
    RULES = {
        "em_dash": {
            "name": "Em dashes in prose",
            "severity": "BLOCKER",
            "description": "Em dashes (—) obscure logical relationships. Use semicolons, periods, or conjunctions.",
        },
        "semicolon_prose": {
            "name": "Semicolons in prose",
            "severity": "WARNING",
            "description": "Semicolons compress ideas. Use period or conjunctions instead.",
        },
        "ie_eg_text": {
            "name": "Abbreviations (i.e./e.g.) in open text",
            "severity": "WARNING",
            "description": "Use 'that is' or 'for example' instead; or use parenthetical (e.g., …) sparingly.",
        },
        "author_narrative": {
            "name": "Author names in narrative",
            "severity": "BLOCKER",
            "description": "No author names before [@cite]. Use: Finding [@cite], not: Smith et al. found …",
        },
        "readability_high": {
            "name": "Readability too high (>14 grade level)",
            "severity": "WARNING",
            "description": "Consider simplifying for field-literate audience. Target: Flesch-Kincaid ≤14.",
        },
        "readability_critical": {
            "name": "Readability critical (>16 grade level)",
            "severity": "BLOCKER",
            "description": "Text is too dense. Simplify sentence structure and vocabulary.",
        },
        "jargon_high": {
            "name": "Jargon density high (>5%)",
            "severity": "WARNING",
            "description": "Technical vocabulary exceeds threshold. Define terms or use simpler synonyms.",
        },
        "results_numbers": {
            "name": "Numbers in Results without context",
            "severity": "WARNING",
            "description": "Bare numbers in Results. Include unit, proportion, or reference.",
        },
        "discussion_newdata": {
            "name": "Numbers in Discussion (possible new data)",
            "severity": "BLOCKER",
            "description": "Discussion should not report new counts. Move to Results or cite Results.",
        },
        "acronym_undefined": {
            "name": "Acronym used before definition",
            "severity": "WARNING",
            "description": "Define acronyms before first use: term (ACRONYM) on first occurrence.",
        },
        "weak_verb_conducted": {
            "name": "Weak verb: conducted / carried out",
            "severity": "WARNING",
            "description": "Prefer a concrete verb (counted, sampled, estimated, measured). Avoid 'was/were conducted' and 'carried out'.",
        },
        "vague_reconciled": {
            "name": "Vague 'reconciled' without the rule",
            "severity": "WARNING",
            "description": "Say the combination rule (mean, sum, preferred series). Do not write 'reconciled' alone.",
        },
    }

    # Common abbreviations to skip in acronym detection (field-standard, don't require definition)
    COMMON_ACRONYMS = {"DNA", "GPS", "RNA", "UK", "US", "EU", "Fig", "PLACEHOLDER", "PENDING", "BRT", "GLMM"}

    # Common technical terms (domain dictionary for jargon detection)
    TECHNICAL_TERMS = {
        # Marine/megafauna
        "telemetry", "satellite", "tag", "tracking", "occupancy", "habitat", "distribut",
        "range", "movement", "migration", "phenology", "taxonom", "biomass", "phylogenet",
        "ecolog", "species", "subspecies", "population", "cohort", "cohesion",
        # Statistics
        "regression", "correlation", "variance", "coefficient", "probability", "p-value",
        "significance", "bootstrap", "bayesian", "frequentist", "likelihood", "statistical",
        "gaussian", "poisson", "binomial", "glmm", "gam", "additive", "algorithm",
        # Methods
        "kernel", "density", "analysis", "estimation", "interpolat", "standardiz",
        "normaliz", "transform", "spline", "smooth", "cross-validat",
        # Conservation/ecology
        "conservation", "threats", "biodiversity", "ecosystem", "trophic", "predation",
        "competition", "niche", "recruitment", "mortality", "phenotyp", "genotyp",
    }

    def __init__(self, filepath: str, mode: str = "normal", section: str = None, quiet: bool = False):
        """
        Initialize validator.

        Args:
            filepath: Path to Markdown file
            mode: "strict" (blockers + warnings) or "normal" (blockers only)
            section: Limit checks to specific section (e.g., "Results", "Discussion")
            quiet: Suppress non-critical output
        """
        self.filepath = Path(filepath)
        self.mode = mode
        self.section = section
        self.quiet = quiet
        self.issues: List[Dict] = []

        if not self.filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(self.filepath, "r") as f:
            self.text = f.read()
        self.lines = self.text.split("\n")

    def run(self) -> bool:
        """
        Run all checks. Return True if PASS, False if FAIL.
        """
        self._check_em_dashes()
        self._check_semicolons()
        self._check_abbreviations()
        self._check_author_narrative()
        self._check_acronyms()
        self._check_weak_verbs()
        self._check_vague_reconciled()

        if textstat:
            self._check_readability()

        self._check_jargon_density()
        self._check_results_discussion_boundary()

        self._report()
        return not any(issue["severity"] == "BLOCKER" for issue in self.issues)

    def _check_em_dashes(self):
        """Detect em dashes in prose (not in bibliographic references or code)."""
        for i, line in enumerate(self.lines, 1):
            # Skip code blocks, comments, tables
            if line.strip().startswith("```") or line.strip().startswith("|"):
                continue
            # Skip lines that are clearly references (start with -)
            if line.strip().startswith("-"):
                continue
            # Check for em dash
            if "—" in line:
                # Filter out false positives: bibliographic references with "—"
                if not (line.strip().startswith("**") and line.count("—") == 1):
                    self.issues.append({
                        "line": i,
                        "severity": "BLOCKER",
                        "rule": "em_dash",
                        "text": line.strip()[:80],
                        "message": "Em dash found. Use semicolon, period, or conjunction instead.",
                    })

    def _check_semicolons(self):
        """Detect semicolons in prose (not in code or lists)."""
        for i, line in enumerate(self.lines, 1):
            # Skip code blocks, tables, bullet lists
            if line.strip().startswith("```") or line.strip().startswith("|") or line.strip().startswith("-"):
                continue
            # Check for semicolon
            if ";" in line:
                # Filter: semicolon in citations (e.g., [@a; @b]) is OK
                if re.search(r'\[@[^;]+;[^\]]*\]', line):
                    continue
                # Filter: LFD-style [PENDING description; context] placeholders
                line_wo_pending = re.sub(r'\[PENDING[^\]]*\]', '', line)
                if ";" not in line_wo_pending:
                    continue
                self.issues.append({
                    "line": i,
                    "severity": "WARNING",
                    "rule": "semicolon_prose",
                    "text": line.strip()[:80],
                    "message": "Semicolon found. Use period or conjunction instead.",
                })

    def _check_abbreviations(self):
        """Detect i.e. and e.g. in open text (not parenthetical)."""
        for i, line in enumerate(self.lines, 1):
            # Skip code, tables
            if line.strip().startswith("```") or line.strip().startswith("|"):
                continue
            # Check for open-text i.e. or e.g. (not in parentheses)
            if re.search(r'\b(i\.e\.|e\.g\.)\b', line):
                # Filter: parenthetical (e.g., …) is OK
                if not re.search(r'\((e\.g\.|i\.e\.).*?\)', line):
                    self.issues.append({
                        "line": i,
                        "severity": "WARNING",
                        "rule": "ie_eg_text",
                        "text": line.strip()[:80],
                        "message": "Use 'that is' or 'for example' instead of i.e./e.g.",
                    })

    def _check_author_narrative(self):
        """Detect author names woven into narrative before [@cite]."""
        for i, line in enumerate(self.lines, 1):
            # Skip code, tables, references sections
            if line.strip().startswith("```") or line.strip().startswith("|"):
                continue
            # Check for patterns like "Smith et al. found" or "Author (YYYY) showed"
            if re.search(r'\b[A-Z][a-z]+ et al\. ', line) or re.search(r'\b[A-Z][a-z]+ \(\d{4}\) ', line):
                self.issues.append({
                    "line": i,
                    "severity": "BLOCKER",
                    "rule": "author_narrative",
                    "text": line.strip()[:80],
                    "message": "Author name in narrative. Use: Finding [@cite], not Smith et al. found …",
                })

    def _check_weak_verbs(self):
        """Flag hollow verbs that hide the real action (Methods/Results prose)."""
        # Skip skill/docs that discuss the banned word itself
        if self.filepath and "validator" in self.filepath.name.lower():
            return
        for i, line in enumerate(self.lines, 1):
            if line.strip().startswith("```") or line.strip().startswith("|") or line.strip().startswith("#"):
                continue
            if re.search(r'\b(was|were|is|are|been)\s+conducted\b', line, re.IGNORECASE):
                self.issues.append({
                    "line": i,
                    "severity": "WARNING",
                    "rule": "weak_verb_conducted",
                    "text": line.strip()[:80],
                    "message": "Weak verb 'conducted'. Prefer counted/sampled/estimated/measured.",
                })
            if re.search(r'\bcarried out\b', line, re.IGNORECASE):
                self.issues.append({
                    "line": i,
                    "severity": "WARNING",
                    "rule": "weak_verb_conducted",
                    "text": line.strip()[:80],
                    "message": "Weak verb 'carried out'. Prefer a concrete verb for the action.",
                })

    def _check_vague_reconciled(self):
        """Flag 'reconciled' without an explicit mean/sum/rule nearby."""
        for i, line in enumerate(self.lines, 1):
            if line.strip().startswith("```") or line.strip().startswith("|") or line.strip().startswith("#"):
                continue
            if re.search(r'\breconcil', line, re.IGNORECASE):
                # OK if the combination rule is stated on the same line
                if re.search(r'\b(mean|sum|average|combined)\b', line, re.IGNORECASE):
                    continue
                self.issues.append({
                    "line": i,
                    "severity": "WARNING",
                    "rule": "vague_reconciled",
                    "text": line.strip()[:80],
                    "message": "Vague 'reconciled'. State mean, sum, or the exact combination rule.",
                })

    def _check_readability(self):
        """Check readability using Flesch-Kincaid and Coleman-Liau indices."""
        if not textstat:
            return

        # Extract prose (skip headers, code, tables, citations)
        prose_lines = []
        for line in self.lines:
            if line.strip().startswith("#") or line.strip().startswith("```") or line.strip().startswith("|"):
                continue
            if line.strip():
                prose_lines.append(line)

        prose = "\n".join(prose_lines)
        if not prose or len(prose) < 100:
            return

        fk_grade = textstat.flesch_kincaid_grade(prose)
        cl_index = textstat.coleman_liau_index(prose)

        avg_grade = (fk_grade + cl_index) / 2

        if avg_grade > 16:
            self.issues.append({
                "line": 0,
                "severity": "BLOCKER",
                "rule": "readability_critical",
                "text": f"Flesch-Kincaid: {fk_grade:.1f}, Coleman-Liau: {cl_index:.1f}",
                "message": f"Readability critical (avg grade {avg_grade:.1f} > 16). Simplify sentence structure.",
            })
        elif avg_grade > 14 and self.mode == "strict":
            self.issues.append({
                "line": 0,
                "severity": "WARNING",
                "rule": "readability_high",
                "text": f"Flesch-Kincaid: {fk_grade:.1f}, Coleman-Liau: {cl_index:.1f}",
                "message": f"Readability high (avg grade {avg_grade:.1f} > 14). Consider simplifying.",
            })

    def _check_jargon_density(self):
        """Estimate jargon density as percentage of technical terms."""
        if not self.text or len(self.text.split()) < 50:
            return

        words = self.text.lower().split()
        jargon_count = sum(1 for word in words if any(term in word.lower() for term in self.TECHNICAL_TERMS))
        jargon_percent = (jargon_count / len(words)) * 100

        if jargon_percent > 8:
            self.issues.append({
                "line": 0,
                "severity": "WARNING",
                "rule": "jargon_high",
                "text": f"Jargon density: {jargon_percent:.1f}%",
                "message": f"Jargon exceeds 8% threshold ({jargon_percent:.1f}%). Define terms or simplify.",
            })
        elif jargon_percent > 5 and self.mode == "strict":
            self.issues.append({
                "line": 0,
                "severity": "WARNING",
                "rule": "jargon_high",
                "text": f"Jargon density: {jargon_percent:.1f}%",
                "message": f"Jargon at {jargon_percent:.1f}% (target ≤5%). Consider defining or simplifying.",
            })

    def _check_acronyms(self):
        """Detect acronyms used before definition."""
        # Simple heuristic: find uppercase sequences, check if defined nearby
        acronym_pattern = r'\b([A-Z]{2,})\b'
        defined_acronyms = set()

        for i, line in enumerate(self.lines):
            # Skip headers, code, tables
            if line.strip().startswith("#") or line.strip().startswith("```") or line.strip().startswith("|"):
                continue

            # Find definitions: word (ACRONYM)
            definitions = re.findall(r'(\w+)\s*\(([A-Z]{2,})\)', line)
            for word, acronym in definitions:
                defined_acronyms.add(acronym)

            # Find uses
            uses = re.findall(acronym_pattern, line)
            for acronym in uses:
                if acronym not in defined_acronyms and acronym not in self.COMMON_ACRONYMS:
                    self.issues.append({
                        "line": i + 1,
                        "severity": "WARNING",
                        "rule": "acronym_undefined",
                        "text": line.strip()[:80],
                        "message": f"Acronym '{acronym}' used before definition. Define as: term ({acronym}).",
                    })
                    defined_acronyms.add(acronym)  # Avoid duplicate warnings

    def _check_results_discussion_boundary(self):
        """Detect numbers in Discussion section that may be new data."""
        in_discussion = False
        results_section_found = False

        for i, line in enumerate(self.lines, 1):
            # Detect section headers
            if re.match(r'^#+\s+RESULTS', line, re.IGNORECASE):
                in_discussion = False
                results_section_found = True
                continue
            elif re.match(r'^#+\s+DISCUSSION', line, re.IGNORECASE):
                in_discussion = True
                continue
            elif re.match(r'^#+\s+', line):  # Another section
                in_discussion = False

            if not in_discussion:
                continue

            # Skip code, tables, references
            if line.strip().startswith("```") or line.strip().startswith("|") or line.strip().startswith("-"):
                continue

            # Check for bare numbers (not citations)
            # Match patterns like "123", "0.45", "3.2%", "N=50"
            if re.search(r'\b\d+\.?\d*\s*(%|ms|sec|km|m|individuals|samples)?', line):
                # Filter: numbers with figure/table references are OK
                if not re.search(r'\[(Fig\.|Table|Figure)\s*\d+', line):
                    # Only flag if it looks like a new finding (verb + number)
                    if re.search(r'(found|showed|revealed|demonstrated|increased|decreased|ranged|varied)\s+\d', line, re.IGNORECASE):
                        self.issues.append({
                            "line": i,
                            "severity": "BLOCKER",
                            "rule": "discussion_newdata",
                            "text": line.strip()[:80],
                            "message": "Numbers in Discussion may be new data. Reference Results instead: see [Fig. X].",
                        })

    def _report(self):
        """Print formatted report."""
        if not self.issues:
            if not self.quiet:
                print(f"✅ PASS: {self.filepath.name}")
            return

        # Group by severity
        blockers = [i for i in self.issues if i["severity"] == "BLOCKER"]
        warnings = [i for i in self.issues if i["severity"] == "WARNING"]

        # Print summary
        status = "FAIL" if blockers else "WARN"
        symbol = "❌" if blockers else "⚠️"
        print(f"{symbol} {status}: {self.filepath.name}")
        print(f"   Blockers: {len(blockers)}, Warnings: {len(warnings)}\n")

        # Print issues
        for issue in blockers + warnings:
            severity_symbol = "❌" if issue["severity"] == "BLOCKER" else "⚠️"
            print(f"{severity_symbol} Line {issue['line']}: {issue['rule']}")
            print(f"   {issue['message']}")
            if issue['text']:
                print(f"   > {issue['text']}")
            print()

    def summary(self) -> Dict:
        """Return summary stats."""
        return {
            "file": str(self.filepath),
            "total_issues": len(self.issues),
            "blockers": sum(1 for i in self.issues if i["severity"] == "BLOCKER"),
            "warnings": sum(1 for i in self.issues if i["severity"] == "WARNING"),
            "pass": not any(i["severity"] == "BLOCKER" for i in self.issues),
        }


def main():
    parser = argparse.ArgumentParser(
        description="Validate scientific prose against style rules."
    )
    parser.add_argument("--file", "-f", required=True, help="Path to Markdown file")
    parser.add_argument("--mode", "-m", choices=["normal", "strict"], default="normal",
                        help="strict: check warnings; normal: blockers only")
    parser.add_argument("--section", "-s", help="Limit checks to section (e.g., Results)")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress output")

    args = parser.parse_args()

    try:
        validator = ProseValidator(args.file, mode=args.mode, section=args.section, quiet=args.quiet)
        passed = validator.run()
        sys.exit(0 if passed else 1)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
