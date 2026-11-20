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
- paragraph openers that announce a subject instead of stating the point (`announcing_opener`)
- claims about what others lack, in the Abstract or Introduction (`unsupported_gap`)
- the same citation more than twice, or the same threshold value more than three times, in one section (`repeated_citation`, `repeated_value`)
- a Discussion over 1.5 times the Introduction's length (`discussion_length`)
- words on the author's avoid list with `--avoid-words FILE` (`avoid_word`). FILE is one word per line, or a Markdown voice profile whose backticked terms sit under a heading containing "avoid".

## Design choices

- `--section` actually limits checks to the named Markdown section.
- Methods receives a higher readability threshold than narrative sections.
- Em dashes, semicolons, narrative citations, and technical density are not universal scientific errors.
- The validator reports causal wording for review rather than deciding whether causality is justified.

## Exit codes

- `0`: no blockers
- `1`: blockers found
- `2`: input file missing

Run lint after scientific accuracy, structure, and citation–sentence checks.
