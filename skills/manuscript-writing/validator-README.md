# Manuscript validator

The validator is a deterministic lint pass. It flags likely problems but cannot verify scientific truth, citation support, model validity, or argument quality.

## Usage

```bash
python skills/manuscript-writing/validator.py --file manuscript.md
python skills/manuscript-writing/validator.py --file manuscript.md --mode strict
python skills/manuscript-writing/validator.py --file manuscript.md --section Results
python skills/manuscript-writing/validator.py --file manuscript.md --house-style
```

Install optional readability support with `pip install textstat`.

## Blockers

- unresolved placeholders such as `[TBC]`, `[TODO]`, `[CITATION NEEDED]`, `XX`, or `???`

## Warnings

- undefined acronyms
- weak or vague phrasing
- stacked hedges
- likely interpretation in Results
- likely numerical Results recap in Discussion
- causal language requiring design review
- high readability grade in strict mode
- punctuation preferences when `--house-style` is enabled

## Design choices

- `--section` actually limits checks to the named Markdown section.
- Methods receives a higher readability threshold than narrative sections.
- Em dashes, semicolons, narrative citations, and technical density are not universal scientific errors.
- The validator reports causal wording for review rather than deciding whether causality is justified.

## Exit codes

- `0`: no blockers
- `1`: blockers found
- `2`: input file missing

Run lint after scientific accuracy, structure, and claim-evidence checks.
