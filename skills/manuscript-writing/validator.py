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

    NARRATIVE = ("abstract", "introduction", "background", "discussion", "conclusion")
    # Paragraph openers that announce a subject instead of stating the point.
    ANNOUNCING_OPENERS = re.compile(
        r"^(?:(?:this|the present|our) (?:study|paper|section|paragraph|work)\b"
        r"|[^.]{0,120}\b(?:provides?|offers?|represents?) (?:a|an) (?:useful|direct|ideal|unique|good|valuable|natural)?\s*(?:conservation |model |case |natural )?(?:test|case|opportunity|system|model)\b"
        r"|[^.]{0,120}\bmay also (?:differ|vary|play a role|matter)\b"
        r"|it is (?:also )?(?:worth|important|interesting)\b"
        r"|(?:we )?turn(?:ing)? (?:now )?to\b"
        r"|in this (?:section|paragraph)\b)",
        re.I,
    )
    GAP_CLAIM = re.compile(r"\b(?:managers|practitioners|researchers|decision[- ]makers|conservationists)\s+(?:still\s+|currently\s+)?(?:lack|do not know|don't know|have no|cannot predict)\b", re.I)
    CITATION_RE = re.compile(r"\([^()]*[A-Z][^()]*\b(?:1[6-9]|20)\d{2}[a-z]?\)|\[@[^\]]+\]")
    VALUE_RE = re.compile(r"[−-]?\d+(?:\.\d+)?\s?°C|\b\d{1,2}:\d{2}\b")

    def __init__(self, path: Path, mode: str, section: str | None, house_style: bool,
                 avoid_words: list[str] | None = None) -> None:
        self.path = path
        self.avoid_words = avoid_words or []
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
        self.check_paragraph_openers()
        self.check_repetition()
        self.check_proportion()
        self.check_avoid_words()
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

    def check_paragraph_openers(self) -> None:
        for number, section, line in self.iter_prose():
            if not section.startswith(self.NARRATIVE) or line.lstrip().startswith("#"):
                continue
            first = re.split(r"(?<=[.!?])\s+", line.strip(), maxsplit=1)[0]
            if section.startswith(("abstract", "introduction", "background")) and self.GAP_CLAIM.search(line):
                self.add(number, "WARNING", "unsupported_gap", "Claims about what others lack or don't know need a source. Otherwise state why the result is useful.", line)
            if self.ANNOUNCING_OPENERS.search(first):
                self.add(number, "WARNING", "announcing_opener", "Open the paragraph with its point, not an announcement of its subject. If the point is uncertain, state it as an uncertain claim.", first)

    def check_repetition(self) -> None:
        cites: dict[tuple[str, str], list[int]] = {}
        values: dict[tuple[str, str], list[int]] = {}
        for number, section, line in self.iter_prose():
            if section.startswith(("method", "materials", "reference")):
                continue
            for m in self.CITATION_RE.finditer(line):
                cites.setdefault((section, m.group(0)), []).append(number)
            for m in self.VALUE_RE.finditer(line):
                values.setdefault((section, re.sub(r"\s", "", m.group(0))), []).append(number)
        for (section, cite), where in cites.items():
            if len(where) > 2:
                self.add(where[0], "WARNING", "repeated_citation", f"{cite} is cited {len(where)} times in {section.title()}. Check whether the same claim is being repeated; give it one home.", cite)
        for (section, value), where in values.items():
            if len(where) > 3:
                self.add(where[0], "WARNING", "repeated_value", f"{value} appears {len(where)} times in {section.title()}. Once defined, refer to it by name (for example 'the threshold') instead of restating it.", value)

    def check_proportion(self) -> None:
        if self.section_filter:
            return
        words: dict[str, int] = {}
        for _, section, line in self.iter_prose():
            key = "introduction" if section.startswith(("introduction", "background")) else section
            words[key] = words.get(key, 0) + len(line.split())
        intro, disc = words.get("introduction", 0), words.get("discussion", 0)
        if intro and disc > 400 and disc > 1.5 * intro:
            self.add(0, "WARNING", "discussion_length", f"Discussion has {disc} words against {intro} in the Introduction. Check that each Discussion paragraph answers something the Introduction set up, and cut points that don't.")

    def check_avoid_words(self) -> None:
        if not self.avoid_words:
            return
        pattern = re.compile(r"\b(" + "|".join(re.escape(w) for w in self.avoid_words) + r")\w*", re.I)
        for number, _, line in self.iter_prose():
            for m in pattern.finditer(line):
                self.add(number, "WARNING", "avoid_word", f"'{m.group(0)}' is on the author's avoid list. Use a plain verb from the author voice profile.", line)

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


def load_avoid_words(path: Path) -> list[str]:
    """Read an avoid list: plain lines, or backticked terms under Markdown headings containing 'avoid'."""
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() != ".md":
        return [w.strip() for w in text.splitlines() if w.strip() and not w.startswith("#")]
    terms, active = [], False
    for line in text.splitlines():
        if line.startswith("#"):
            active = "avoid" in line.lower()
            continue
        if active:
            terms += [t for t in re.findall(r"`([^`]+)`", line) if not t.endswith("...")]
    return terms


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint Markdown research manuscripts.")
    parser.add_argument("--file", "-f", required=True)
    parser.add_argument("--mode", "-m", choices=["normal", "strict"], default="normal")
    parser.add_argument("--section", "-s", help="Limit checks to a named Markdown section")
    parser.add_argument("--house-style", action="store_true", help="Promote punctuation preferences to warnings")
    parser.add_argument("--avoid-words", metavar="FILE", help="Words the author avoids: one per line, or a Markdown file whose backticked terms sit under a heading containing 'avoid'")
    args = parser.parse_args()
    path = Path(args.file)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 2
    avoid = load_avoid_words(Path(args.avoid_words)) if args.avoid_words else []
    validator = ManuscriptValidator(path, args.mode, args.section, args.house_style, avoid)
    return 0 if validator.run() else 1


if __name__ == "__main__":
    raise SystemExit(main())
