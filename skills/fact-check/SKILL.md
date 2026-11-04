---
name: fact-check
description: >-
  Verify scientific claims against source papers or project results, assess
  claim-citation fit, and suggest evidence-supported replacements. Use for
  fact-checking a sentence or manuscript passage, checking numbers or attribution,
  or finding evidence for an unsupported claim. Distinguishes a paper's own
  findings from its interpretation and the prior work it cites.
metadata:
  version: 0.2.0
---

# Fact-check

Check the claim against direct evidence before accepting or changing it. A
citation, reviewer comment, search hit, or fluent summary is a lead to investigate.

## Verification process

1. Quote the exact claim and record its manuscript location. Split compound
   sentences into claims that can be checked separately. Preserve nearby context.
2. Resolve the source and version. For a paper, confirm title, authors, year,
   DOI or stable identifier, and relevant corrections. For project findings,
   identify the authoritative output, input version, and analysis code.
3. Read the direct evidence. Use PaperKit when available, otherwise accessible
   full text, tables, figures, supplements, or project outputs. Record the page,
   section, table, figure, or artifact path beside each check. Abstracts and
   snippets cannot verify detailed methods or quantitative claims.
4. Identify whose finding it is: this study's result, the source authors'
   interpretation, cited background, a review's synthesis, or your inference.
   Follow cited background to the original source before calling it verified.
5. Compare the claim with the evidence: population/system, setting, period,
   measure, comparison, direction, magnitude, uncertainty, and inference.
   Check units, denominators, and reported versus calculated values. Trace
   project numbers to outputs and code; comments alone do not establish behavior.
6. Look for qualifications or conflicting results that materially change the
   claim. For broad claims, search beyond the supplied citation. State the search
   scope; a single supporting passage does not establish a field-wide consensus.
7. Assign a verdict with a reason: `supported`, `partially supported`,
   `contradicted`, `unsupported`, `misattributed`, or `unverified`.
   `Unsupported` means the inspected evidence does not establish the claim;
   `contradicted` requires evidence against it. Missing access is `unverified`.
8. Keep accurate wording. For each issue, suggest the smallest replacement the
   evidence supports, with its source and locator. Verify the replacement by the
   same process. If no replacement is supported, leave the gap explicit.

A quote match proves textual presence, not scientific support. Label abstract-only
checks and unresolved source chains. Never turn unavailable evidence into a
negative finding or invent a locator.

## Find evidence when needed

Use this branch when a claim lacks a source or its current citation fails.

1. Define the claim's scope and what evidence could support or refute it.
2. Search the existing library through ZotSeek or Zotero semantic search. Use
   exact author/title/DOI lookup for identity. If the library is insufficient,
   use `discover-papers` for external discovery. Use `pp-scite` citation context
   as a lead to inspect, rather than a support vote.
3. Curate a small set of candidates by study design and claim fit. Resolve their
   identities and run the verification process before recommending a citation.
4. Separate verified support from promising papers whose full text remains
   unchecked. Revise the claim if the evidence supports only a narrower statement.

For backend selection and failure recovery, read
[the tool map](references/tool-map.md).

## Output

Scale the report to the request. A single sentence needs a compact check; a
passage can use a table:

| Claim and draft location | Source and evidence locator | Whose finding / access level | Verdict and reason | Keep or suggested replacement |
|---|---|---|---|---|

Include a short evidence excerpt when it helps the reader inspect the verdict.
For calculated values, show the inputs and calculation. Report what remains
unchecked. Match the manuscript's terminology and voice in proposed wording.
Do not create a separate claims ledger unless the user requests one.

## Boundaries

- `paper-brief` owns explaining one paper, including its methods and findings.
- `manuscript-writing` owns manuscript prose and whole-manuscript audit. Use
  this verification process for its factual checks; return proposed changes
  rather than silently settling scientific disagreements.
- `literature-review` owns review corpora, screening, extraction, and synthesis.
- `zotero`, `zotseek`, `pp-scite`, `find-pdf`, and `paperkit` own their tool
  procedures. Load installation skills only for setup or connection failures.
- `manuscript-markdown` owns Word roundtrip and citation fields.
