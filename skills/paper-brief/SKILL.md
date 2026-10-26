---
name: paper-brief
description: >-
  Produce a fast, source-traceable explanation of one research paper. Use when
  the user wants to understand a paper, get its findings quickly, check what it
  actually found, or distinguish its results from literature it cites. Requires
  page/section/table/figure evidence for substantive claims. Uses PaperKit when
  available and otherwise the accessible full text.
metadata:
  version: 0.1.0
---

# Paper Brief

Explain one paper efficiently without asking the reader to take the abstract,
authors' discussion, or agent's summary on trust. Read the full-text passages
needed to check the question, methods, findings, interpretation, and limitations.
Use PaperKit when available; otherwise use the accessible PDF or full text.

## Verify the source

1. If the full text is not in the library, use PaperKit to acquire it when
   available; otherwise route to `find-pdf`. Report if it remains unavailable.
2. Resolve the paper by DOI or another stable identifier. Check title, authors,
   year, article type, and version against publisher or repository metadata.
3. When corrections, retractions, or publication status could affect use, check
   the publisher record and a suitable index. Report what you could not confirm.
4. Treat metadata, abstract, and search hits as navigation. Do not use them as
   evidence for detailed results or methods.

## Read for the question

1. Identify what the user needs to understand. If they gave no particular use,
   prepare a compact overview of the study.
2. Use the paper card or section map to find relevant passages. Read the methods
   and results needed for the question, plus enough introduction and discussion
   to separate prior literature from the authors' interpretation.
3. Check tables, figures, supplements, or appendices when the main result or
   method depends on them. Do not infer a number from a plot when a table or
   exact estimate is available.
4. For each substantive statement, retain a locator: page and section, or table,
   figure, equation, or supplement. Keep a short supporting excerpt when useful.

## Keep source layers separate

Label each point as one of:

- **Study result:** analysis or observation reported from this paper's own data.
- **Authors' interpretation:** the authors' explanation or inference from those
  results. Check whether the data support its strength and scope.
- **Cited background:** a statement attributed to earlier work or accepted
  knowledge. It is not a finding of this paper. Resolve the cited original
  source before using it as direct evidence for a manuscript claim.
- **Brief-writer inference:** a conclusion drawn by comparing or interpreting
  the paper. Mark it as interpretation and show its basis.

For reviews and meta-analyses, label the review's synthesis separately from the
underlying primary-study results. Do not present a cited study's result as if the
review authors generated it.

## Verify each claim

Check that the passage matches the claim's population or system, setting, time,
measure, comparison, direction, magnitude, and uncertainty. Distinguish
association from causation and statistical results from biological or policy
interpretation. A quote match shows that wording appears in the source; it does
not by itself establish that the wording supports the claim.

If a claim fails, state the problem and suggest a narrower replacement that the
located evidence supports. If the full text or needed passage is unavailable,
mark the point as unchecked or abstract-only; do not silently fill the gap.

## Output

Keep the brief as short as the question allows. For a general overview, use:

```text
Citation and source status
Question and why it matters
Study design, data, and setting
What the study directly found [with evidence locations]
What the authors infer [with evidence locations]
What it cites as prior knowledge [clearly attributed]
Limitations and what the paper does not establish
One-sentence takeaway, with a boundary
```

Put a page, section, table, figure, or supplement locator beside each factual
finding. Use exact quotations only when wording matters; otherwise paraphrase
faithfully and cite the locator. State whether the brief used full text or only
an abstract. Do not rate trustworthiness from journal prestige alone.

## Handoff

- For a claim-specific citation search or support check, use `fact-check`.
- For extraction across a review corpus, use `literature-review`.
- For manuscript-level fact-checking and proposed sentence replacements, use
  `manuscript-writing` audit mode.
