# Prose vs scaffolding

Manuscript prose, in every section, contains only what a reader needs to
understand and evaluate the science. It never contains the scaffolding a
project uses to build, track, or verify that science internally — regardless
of form: code identifiers (function names, file paths, variable names),
pipeline or task-runner references, decision-log tags, or claim-tracking /
traceability IDs from an internal audit system.

The test is not "is this a code artifact" — it is "does a reader need this to
understand or reproduce the finding." A package name, a published function,
or a named statistical method is a citable dependency and belongs in prose.
A custom function name, an internal file path, or a claim-tracking tag tells
the project team where a number lives, not what it means — put it in a
provenance note, not the sentence.

Scan Results as carefully as Methods: claim IDs and file paths leak into
result prose as easily as function names leak into Methods.

**Before (scaffolding leaking into Results):**
> Of the 94 BRT-trained species, two were dropped at the dual cross-validation
> production gate (DEC-014): Blacktip shark and Northern Right whale. ... so
> they have no dual-CV production packs (C-FUNNEL-94 → C-FUNNEL-92; C-FUNNEL-2).

**After (finding only; decision tag and claim IDs moved to a provenance note):**
> Two of the 94 fitted species, Blacktip shark and Northern Right whale,
> failed spatial cross-validation in every fold despite succeeding under
> stratified cross-validation, and were excluded from performance,
> predictor-importance, and habitat-map summaries.
> `{>>Provenance: DEC-014; claim IDs C-FUNNEL-94/92/2.<<}`

**Before (Methods, function name in prose):**
> Extraction in this codebase is via `summarise_gbm_model()` in
> `R/functions_rep.R`, which stores `rel.inf` from `summary(model, plotit = FALSE)`.

**After (citable package kept, internal wrapper moved to a note):**
> ...using relative influence, computed with the `relative.influence` method
> in the R package `gbm` (version 2.2.2) [@elith2008boosting].
> `{>>Provenance: extraction wrapped by summarise_gbm_model() in R/functions_rep.R.<<}`
