#!/usr/bin/env python3
"""Deterministic manuscript lint.

Flags likely prose and section-boundary issues. It does not validate scientific
truth, citation support, statistical validity, or manuscript logic.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import textstat
except ImportError:  # optional
    textstat = None


@dataclass
class Issue:
    line: int
    severity: str
    rule: str
    message: str
    text: str = ""


class ManuscriptValidator:
    SECTION_RE = re.compile(r"^#{1,6}\s+(abstract|introduction|background|methods?|materials and methods|results?|discussion|conclusions?|references)\b", re.I)
    ACRONYM_RE = re.compile(r"\b([A-Z][A-Z0-9-]{1,})\b")
    COMMON_ACRONYMS = {"DNA", "RNA", "GPS", "UK", "US", "EU", "CI", "SD", "SE", "Fig", "DOI"}

    def __init__(self, path: Path, mode: str, section: str | None, house_style: bool) -> None:
        self.path = path
        self.mode = mode
        self.section_filter = section.lower() if section else None
        self.house_style = house_style
        self.lines = path.read_text(encoding="utf-8").splitlines()
        self.issues: list[Issue] = []
        self._code_fence = False

    def iter_prose(self):
        current_section = ""
        in_code = False
        for number, line in enumerate(self.lines, 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            match = self.SECTION_RE.match(line.strip())
            if match:
                current_section = match.group(1).lower()
                continue
            if in_code or not line.strip() or line.lstrip().startswith(("|", "<!--")):
                continue
            if self.section_filter and self.section_filter not in current_section:
                continue
            yield number, current_section, line

    def add(self, line: int, severity: str, rule: str, message: str, text: str = "") -> None:
        self.issues.append(Issue(line, severity, rule, message, text[:120]))

    def run(self) -> bool:
        self.check_placeholders()
        self.check_punctuation()
        self.check_acronyms()
        self.check_weak_phrasing()
        self.check_section_boundaries()
        self.check_readability()
        self.report()
        return not any(i.severity == "BLOCKER" for i in self.issues)

    def check_placeholders(self) -> None:
        pattern = re.compile(r"\[(TBC|TODO|PENDING|CITATION NEEDED|REF)\]|\bXX\b|\?\?\?")
        for number, _, line in self.iter_prose():
            if pattern.search(line):
                self.add(number, "BLOCKER", "unresolved_placeholder", "Resolve or explicitly retain this placeholder before submission.", line)

    def check_punctuation(self) -> None:
        for number, _, line in self.iter_prose():
            if "—" in line:
                severity = "WARNING" if self.house_style else "INFO"
                self.add(number, severity, "em_dash", "Check whether a conjunction or sentence break states the relationship more clearly.", line)
            if ";" in re.sub(r"\[@[^\]]+\]", "", line):
                severity = "WARNING" if self.house_style else "INFO"
                self.add(number, severity, "semicolon", "Check whether the sentence contains two ideas that should be separated.", line)

    def check_acronyms(self) -> None:
        defined: set[str] = set(self.COMMON_ACRONYMS)
        definition_re = re.compile(r"(?:[A-Za-z][A-Za-z -]{2,})\s*\(([A-Z][A-Z0-9-]{1,})\)")
        for number, _, line in self.iter_prose():
            for acronym in definition_re.findall(line):
                defined.add(acronym)
            for acronym in self.ACRONYM_RE.findall(line):
                if acronym not in defined and not acronym.isdigit():
                    self.add(number, "WARNING", "acronym_undefined", f"Define '{acronym}' at first use or add it to the accepted project list.", line)
                    defined.add(acronym)

    def check_weak_phrasing(self) -> None:
        patterns = {
            "weak_conducted": (re.compile(r"\b(?:was|were|is|are|been) conducted\b|\bcarried out\b", re.I), "Use the concrete action, such as sampled, measured, fitted, or tested."),
            "throat_clearing": (re.compile(r"\b(it is important to note that|it should be noted that|in order to)\b", re.I), "State the claim or action directly."),
            "stacked_hedge": (re.compile(r"\b(may|might|could|possibly|perhaps)\b.*\b(may|might|could|possibly|perhaps)\b", re.I), "Use one calibrated hedge unless the sentence distinguishes separate uncertainties."),
        }
        for number, _, line in self.iter_prose():
            for rule, (pattern, message) in patterns.items():
                if pattern.search(line):
                    self.add(number, "WARNING", rule, message, line)

    def check_section_boundaries(self) -> None:
        result_interpretation = re.compile(r"\b(this suggests|this may indicate|likely because|may reflect|implication|mechanism)\b", re.I)
        causal_language = re.compile(r"\b(caused|led to|resulted in|drove|effect of)\b", re.I)
        numeric_finding = re.compile(r"\b(?:we found|increased|decreased|ranged|was|were)\b[^.]{0,50}\b\d+(?:\.\d+)?(?:%|\b)", re.I)
        for number, section, line in self.iter_prose():
            if section.startswith("result") and result_interpretation.search(line):
                self.add(number, "WARNING", "results_interpretation", "Possible interpretation in Results. Keep the finding here and move mechanism or implication to Discussion.", line)
            if section.startswith("discussion") and numeric_finding.search(line):
                self.add(number, "WARNING", "discussion_result_recap", "Check whether this numerical result should be reported in Results and referred to more briefly here.", line)
            if causal_language.search(line):
                self.add(number, "WARNING", "causal_language", "Confirm that the study design supports causal wording.", line)

    def check_readability(self) -> None:
        if textstat is None:
            return
        by_section: dict[str, list[str]] = {}
        for _, section, line in self.iter_prose():
            by_section.setdefault(section or "document", []).append(re.sub(r"\[@[^\]]+\]", "", line))
        for section, lines in by_section.items():
            text = " ".join(lines)
            if len(text.split()) < 100:
                continue
            grade = textstat.flesch_kincaid_grade(text)
            threshold = 17 if section in {"method", "methods", "materials and methods"} else 15
            if grade > threshold:
                severity = "WARNING" if self.mode == "strict" else "INFO"
                self.add(0, severity, "readability", f"{section.title()} grade level is {grade:.1f}. Review dense sentences; do not remove necessary technical detail.")

    def report(self) -> None:
        blockers = [i for i in self.issues if i.severity == "BLOCKER"]
        warnings = [i for i in self.issues if i.severity == "WARNING"]
        infos = [i for i in self.issues if i.severity == "INFO"]
        status = "FAIL" if blockers else ("WARN" if warnings else "PASS")
        print(f"{status}: {self.path.name}")
        print(f"Blockers: {len(blockers)} | Warnings: {len(warnings)} | Info: {len(infos)}")
        for issue in blockers + warnings + (infos if self.mode == "strict" else []):
            location = f"line {issue.line}" if issue.line else "document"
            print(f"[{issue.severity}] {location} {issue.rule}: {issue.message}")
            if issue.text:
                print(f"  > {issue.text}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint Markdown research manuscripts.")
    parser.add_argument("--file", "-f", required=True)
    parser.add_argument("--mode", "-m", choices=["normal", "strict"], default="normal")
    parser.add_argument("--section", "-s", help="Limit checks to a named Markdown section")
    parser.add_argument("--house-style", action="store_true", help="Promote punctuation preferences to warnings")
    args = parser.parse_args()
    path = Path(args.file)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 2
    validator = ManuscriptValidator(path, args.mode, args.section, args.house_style)
    return 0 if validator.run() else 1


if __name__ == "__main__":
    raise SystemExit(main())
