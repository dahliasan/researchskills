# Mode: audit

Audit the manuscript against its sources and project records before rewriting.
Comments, reviewer suggestions, and tracked changes are leads to investigate;
they are not evidence that a scientific claim is correct. Do not let comment
resolution substitute for checking the underlying source or result.

## Steps

1. Identify the manuscript version and scope. Read the relevant project methods,
   authoritative results, figures/tables, and source papers.
2. Use [fact-check](../../fact-check/SKILL.md) for material factual claims.
   Its verification process owns source identity, direct evidence, attribution,
   scope, verdicts, and evidence-supported replacements. Apply it to both external
   sources and the project's own results. Keep accurate wording and report
   inaccessible evidence as unverified.
3. Check that the detail level fits the section and that wording fits the
   manuscript's established terminology and voice. Use the [style and detail
   guidance](../reference.md#style-and-detail) and the nearest approved prose as
   the style sample.
4. Also check alignment across question, methods, analyses, results, figures,
   tables, citations, and conclusions. Optionally run the deterministic
   validator as a lint guardrail.

## Output

```markdown
## Readiness
READY | READY WITH GAPS | NOT READY

## Claim checks
| Draft location and claim | Evidence source and locator | Provenance | Verdict and reason | Suggested wording |
|---|---|---|---|---|

## Other material findings
- [severity] location: issue and required action

## Highest-value next action
...
```

Use page and section, table, figure, or project-output locators. State `abstract
only`, `source unavailable`, or `not checked` when appropriate. If the manuscript
contains many claims, summarize checked claims by section and include the claim
table as a separate artifact rather than implying that unchecked text passed.

**Done when** each material claim in scope has a verdict and source locator or a
visible access gap, proposed replacements preserve the evidence boundary, and
remaining blockers are named. No broad rewrite unless requested.
