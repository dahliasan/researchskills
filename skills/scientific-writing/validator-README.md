# Prose Validator

Deterministic gates and guardrails for scientific writing based on SKILL.md rules.

## Installation

**Required:**
```bash
pip install textstat
```

**Without textstat:** Readability checks (Flesch-Kincaid, Coleman-Liau) are disabled, but all other checks (em-dashes, semicolons, acronyms, etc.) run. Install textstat to enable full validation.

## Usage

```bash
# Quick check (blockers only)
python validator.py --file manuscript.md

# Strict mode (blockers + warnings)
python validator.py --file manuscript.md --mode strict

# Quiet mode (no output)
python validator.py --file manuscript.md --quiet
```

## What it checks

### Blockers (fail if found)
- **Em dashes (—)** in prose: use semicolons, periods, or conjunctions instead
- **Author names** in narrative (e.g., "Smith et al. found…"): rewrite as "Finding [@cite]"
- **Readability critical**: Flesch-Kincaid grade level > 16 (too dense)
- **Numbers in Discussion** without figure/table reference: likely new data (move to Results)
- **Jargon density** > 8%: too many technical terms

### Warnings (check but don't block)
- **Readability high**: Flesch-Kincaid > 14 grade level (simplify if possible)
- **Semicolons** in prose: use conjunction or period instead
- **Abbreviations** (i.e., e.g.) in open text: use spelled-out forms or parenthetical
- **Acronyms** used before definition: define at first use
- **Jargon density** 5–8%: close to threshold
- **Weak verbs**: `was/were conducted`, `carried out` → use counted/sampled/estimated/measured
- **Vague reconciled**: `reconciled` without mean/sum/combined on the same line

## Output example

```
❌ FAIL: draft.md
   Blockers: 2, Warnings: 3

❌ Line 42: em_dash
   Em dash found. Use semicolon, period, or conjunction instead.
   > Results showed that whales—in all three bays—reduced occupancy.

⚠️  Line 156: readability_high
   Readability high (avg grade 15.2 > 14). Consider simplifying.
   > Flesch-Kincaid: 15.8, Coleman-Liau: 14.6

⚠️  Line 203: discussion_newdata
   Numbers in Discussion may be new data. Reference Results instead: see [Fig. X].
   > We found that catch rates increased 2.4-fold.
```

## Technical notes

- **Readability metrics**: Uses Flesch-Kincaid and Coleman-Liau indices (average reported)
- **Jargon detection**: Checks against domain dictionary (~40 marine/ecology/stats terms)
- **False positives**: Filters for common abbreviations (DNA, GPS, RNA, UK, US, EU, Fig) and parenthetical citations [@a; @b]
- **Section detection**: Looks for Markdown headers (# RESULTS, # DISCUSSION)

## Calibration

- **Flesch-Kincaid target**: ≤14 (senior college level for field-literate readers)
- **Jargon cap**: ≤5% (successful lay summaries)
- **Em dash threshold**: 0 (never use in instructional prose)

## Exit codes

- `0`: PASS (no blockers)
- `1`: FAIL (blockers found)

## Integration with workflow

Run in STYLE phase, after manual edit pass:

```
WRITE → CITE-CHECK → CLARITY EDIT → [manual checklist] → validator.py → prose-lint → EXPORT
```

## Limitations

- Does not check semantic accuracy (use citation verification for that)
- Does not detect all instances of author-in-narrative (manual review recommended)
- Readability assumes English prose; may over/under-estimate for specialized language
- Jargon detection uses simple substring matching (may flag false positives like "discuss" matching "discussion")

## Future enhancements

- [ ] Section-specific thresholds (Methods may need higher jargon tolerance)
- [ ] Custom domain dictionaries per project
- [ ] Integration with Zotero/Pandoc for citation validation
- [ ] Sentence-length histogram
- [ ] Passive-voice detector
