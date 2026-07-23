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
   4. claim-evidence traceability
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

## Output

1. Revised section (or manuscript span)
2. Material unresolved issues only
