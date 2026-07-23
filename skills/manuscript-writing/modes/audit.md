# Mode: audit

Audit before rewriting. Do not broadly rewrite unless asked.

## Steps

1. Apply evidence and conflict gates across the audited span.
2. Classify each finding:
   - `BLOCKER`: scientific contradiction, unsupported claim, missing
     provenance, or wrong section
   - `MAJOR`: logic, completeness, traceability, or interpretation problem
   - `MINOR`: clarity, consistency, or local structure problem
   - `EDITORIAL`: grammar, punctuation, or formatting
3. Check:
   1. central contribution, question, objectives, analyses, results, and
      conclusions align
   2. Methods match implementation
   3. all reported values trace to authoritative outputs
   4. tables, figures, captions, and prose agree
   5. citations support the exact claims
   6. section boundaries are respected
   7. terminology, abbreviations, sample sizes, and units are consistent
   8. `[TBC]`, placeholder citations, and missing figure references are
      resolved
4. Do not automatically rewrite scientific conflicts — report them first.
5. Optionally run the deterministic validator as a lint guardrail.
6. Load section contracts from [reference.md](../reference.md) only to judge
   section-role violations, not to redraft.

**Done when** readiness is stated, every material finding is severity-tagged
with location and required action, and the highest-value next action is
named. No silent prose rewrite of BLOCKER/MAJOR science conflicts.

## Output

```markdown
## Readiness
READY | READY WITH GAPS | NOT READY

## Findings
- [severity] location: issue and required action

## Highest-value next action
...
```
