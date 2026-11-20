# Mode: revise

## Steps

1. Apply evidence and conflict gates to claims you will change.
2. Load the target section contract from [reference.md](../reference.md)
   only for sections you are revising.
3. Load [scaffolding.md](../scaffolding.md); remove scaffolding leaks in
   touched prose.
4. Run **separate** revision passes — do not mix jobs in one pass
   ([reference.md](../reference.md#revision-passes)):
   1. scientific accuracy and completeness
   2. central contribution and whole-paper argument
   3. section role and result logic
   4. citation–sentence support (use `fact-check` when needed)
   5. paragraph logic and transitions
   6. sentence clarity and concision
   7. terminology, numbers, figures, tables, and citations
   8. journal compliance when requirements are available
   9. deterministic lint
5. Return revised text plus only material remaining issues.

**Done when** each required pass above has been applied to the changed
scope (or explicitly marked N/A), gates hold for edited claims, and routine
edit notes are omitted from the user-facing return.

## Style defaults

Prefer clear subjects and concrete verbs; active voice when clearer; one main
idea per sentence/paragraph where practical; no filler or stacked hedges;
define study-specific terms at first use; follow local journal and project
conventions over generic preferences.

## Section boundaries and epistemic discipline

- **IMRaD separation:** state inclusion thresholds, definitions, data sources,
  and analytical rules once in Methods without repeating them in Results. Keep
  Results strictly to the study's own empirical findings, and move
  prior-literature comparisons or historical context to Discussion. In
  Discussion, distinguish underlying drivers (for example, prey shifts or
  immigration) from the measured outcomes they affect (for example, survival
  or recruitment).
- **Preserve epistemic boundaries:** when cleaning internal notes, caveats, or
  `[TBC]` flags, never resolve an unverified data gap through prose
  tightening. Keep distinct states separate (for example, "no count reported"
  versus "not surveyed" versus an observed zero) until verified against
  primary records.

## Output

1. Revised section (or manuscript span)
2. Material unresolved issues only
