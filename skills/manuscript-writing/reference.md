# Manuscript writing reference

Single source of truth for section contracts, planning detail, citations, and
statistical reporting. Project and journal rules take priority. Load only the
headings the active mode requests.

## Evidence hierarchy

Use the strongest available source for each statement:

1. implemented code, configuration, and validated outputs for what the project did and found
2. maintained project specifications for scientific intent and approved decisions
3. full-text papers for external scientific claims
4. abstracts for screening and preliminary orientation only
5. search results for discovery only

When evidence levels differ, label the limitation. Never upgrade an
abstract-only claim to full-text verified.

## Planning sequence

For a new manuscript or substantial section:

1. state the central contribution
2. map objectives to final results
3. build the reverse figure outline
4. order the scientific argument
5. create the paragraph storyboard
6. draft only after material evidence gaps are visible

A storyboard is a writing plan, not another store for results or literature
evidence. Link to authoritative result IDs and citations rather than copying
their contents.

## Reverse figure outline

For each final figure or table record:

| Field | Question |
|---|---|
| Purpose | Why must this output exist? |
| Question | Which study question does it answer? |
| Claim | What result does it establish? |
| Evidence | Which exact estimate, interval, sample, or comparison supports the claim? |
| Boundary | What does the analysis not establish? |
| Methods | Which method must be reported for this result to be understood and reproduced? |
| Sequence | Why does this output appear before or after the next output? |

```text
question answered
→ result claim
→ exact supporting output
→ estimate and uncertainty
→ interpretation boundary
→ required Methods
→ next logical result
```

A figure may support more than one secondary observation, but it should have
one clear primary purpose. Order Results by scientific logic, not analysis
chronology. Route visual design to `figure-design`.

## Paragraph storyboard

Before drafting, structure each paragraph as:

| Field | Question |
|---|---|
| Purpose | What must the reader understand? |
| Claim | What single point does the paragraph make? |
| Evidence | Which result, figure, table, or source supports it? |
| Boundary | What does the evidence not establish? |
| Transition | Why does the next paragraph follow? |

```text
purpose → claim → evidence or reasoning → boundary → transition
```

Use citation keys, result IDs, and figure references. Do not draft unsupported
bridging claims merely to make the story sound complete.

## Introduction

```text
problem → established knowledge → unresolved gap → why it matters → objective/question
```

Useful sequence:

1. establish the broad scientific problem
2. narrow to the relevant process, system, or population
3. synthesise what prior work establishes
4. identify the unresolved problem precisely
5. explain why resolving it matters
6. state the objective, question, and predictions

Rules:

- Build only the background needed to understand the gap.
- Synthesize by idea, not paper-by-paper summaries.
- Match gap language to the scope of the literature search.
- End with the study objective, question, and predictions where applicable.
- Do not pre-report or interpret the study results.

Common failures: opening too broadly and never narrowing; listing papers one
at a time; claiming a universal gap from a limited search; introducing methods
detail before the question; ending without a clear objective; building context
that never contributes to the central question.

## Methods

```text
study design → data → eligibility → processing → variables → analysis → validation
```

Write in the order a reader needs to reproduce the study:

1. study design and scope
2. data sources or sampling
3. eligibility and exclusions
4. preprocessing and quality control
5. variables and measurements
6. analytical procedure
7. validation, diagnostics, and sensitivity analyses

Rules:

- Report the implemented method, not the history of exploratory attempts.
- Keep consequential rationale brief; preserve fuller history in decision records.
- Put rules in Methods and resulting counts in Results or QC outputs.
- State exact thresholds, units, software, versions, and validation where material.
- Use `[TBC]` rather than inventing missing details.
- Name packages, published functions, and named statistical methods inline at
  first use, with version where reproducibility depends on it. These are
  citable dependencies, not scaffolding ([scaffolding.md](scaffolding.md)).
- Do not narrate what the study does *not* do unless the omission is a material
  methodological choice a reader would otherwise assume differently.
- Do not restate simple arithmetic when the reported statistic already makes
  the aggregation self-evident.

Software, packages, and versions are not a separate trailing step. Cite each
tool inline at the point its method is described. A single-sentence "analyses
were conducted in R version X" opener is fine; a standalone software dump is
not.

Distinguish: planned from implemented; rules from counts; routine
implementation from consequential rationale; exploratory from confirmatory;
citable dependencies from internal-only artifacts.

Avoid vague verbs such as “cleaned”, “processed”, or “analysed” without the
operation, rule, and parameter.

Data and code availability belongs in a dedicated availability statement
outside the IMRAD body — match the venue.

### Sentence-level economy in Methods

Fuse rationale and action into one or two clauses, then move on. Do not gloss
a named method inline when a citation alone lets a reader look it up. Write
transitions as a forward handoff, not a recap or inserted caveat.

**Before (rationale and action separated):**
> Collinearity filtering used Spearman rank correlation via
> `tidysdm::filter_collinear()` with method `vif_cor` and absolute pairwise
> correlation cutoff 0.8... This is an automated VIF-aware correlation
> filter; it does not retain variables by manual ecological relevance. The
> 0.8 cutoff sits within published SDM collinearity practice: Dormann et al.
> (2013) identify severe distortion around |r| > 0.7, and published cutoffs
> commonly fall between about 0.7 and 0.85 [@dormann2013collinearity].

**After (rationale fused into the action):**
> Collinear predictors distort model estimation above approximately |r| =
> 0.7 [@dormann2013collinearity]. We therefore removed collinear predictors
> using a variance-inflation-factor-aware correlation filter in the R
> package `tidysdm` (version 0.9.5, cutoff |r| = 0.8): for each pair of
> predictors above this cutoff, the variable with the higher variance
> inflation factor was dropped.

**Before (caveat as a stalling aside):**
> Ensemble predictions were summarised as the cell-wise mean suitability
> across retained iterations and the cell-wise standard deviation across
> those same iterations... That standard deviation reflects disagreement
> among the retained model iterations at a fixed month, and is distinct from
> month-to-month habitat variability, which is summarised separately below.

**After (caveat folded into the method sentence):**
> Ensemble predictions were summarised as the cell-wise mean suitability
> across retained iterations, written as GeoTIFF and GeoJSON files for each
> species and month at 1° resolution, and the cell-wise standard deviation
> across those same iterations, reflecting disagreement among retained
> model iterations at a fixed month rather than month-to-month habitat
> variability (summarised separately below).

## Results

```text
question → finding → estimate and uncertainty → figure/table → bounded answer
```

Organise around objectives and final outputs, not analysis chronology.

A strong result unit includes: the question; the finding in scientific terms;
direction and magnitude; uncertainty; sample or unit where needed; figure or
table reference; a bounded answer that sets up the next result.

Rules:

- Lead with the biological or scientific finding, then support with numbers.
- Report effect size, uncertainty, sample, unit, and comparison where relevant.
- Do not explain mechanisms or broader implications.
- Do not repeat every number already visible in a table or figure.
- Distinguish primary, secondary, sensitivity, and exploratory results.
- Embed each number in the sentence making its claim.
- Apply Methods sentence-economy rules (fuse; no inserted-caveat transitions).

Report exact values selectively. Use prose for the message and tables for
dense exact detail.

## Enumerable detail belongs in tables

Across Methods, Results, and captions: push enumerable detail (full variable
lists, per-group inclusion sets, per-item parameters, sample breakdowns) into
a table; state only the rule, rationale, or headline number in prose and
point to the table. Reserve prose for what a table cannot show.

**Before (full list in prose):**
> We selected 19 candidate predictor variables (Table S1): distance to coast
> (dist_coast), distance to shelf (dist_shelf), bathymetric depth (depth),
> chlorophyll-a (chl)... Flying species retained air temperature (temp2m) and
> wind variables...; all other taxonomic groups retained ocean current
> variables...

**After (rule in prose; membership in the table):**
> We selected 19 candidate environmental predictors spanning static
> geography, ocean circulation, thermal and atmospheric forcing, and
> surface and subsurface ocean conditions, chosen as widely used correlates
> of marine megafauna habitat (Table S1). Predictor sets differed by
> taxonomic group to reflect the environments species occupy: flying
> species retained atmospheric predictors in place of the ocean circulation
> predictors retained by all other taxa, with all remaining predictors
> common to both groups (Table S1).

## Discussion

```text
main interpretation → literature comparison → alternatives → limitations → implications
```

Map each important interpretation before drafting:

| Field | Question |
|---|---|
| Result | Which confirmed result is being interpreted? |
| Interpretation | What does the result mean? |
| Literature | Which verified studies agree, conflict, or define the context? |
| Alternative | What else could explain the pattern? |
| Boundary | How do the design, data, and uncertainty limit the claim? |
| Implication | What broader conclusion follows within that boundary? |

```text
result ID → supported interpretation → literature agreement or conflict
→ plausible alternative → evidence boundary → implication
```

Whole-section sequence:

1. interpret the main finding
2. compare with relevant literature
3. examine plausible mechanisms and alternatives
4. explain how design and data affect interpretation
5. state material limitations where they constrain claims
6. broaden to the supported scientific or practical implication

Rules: start with meaning, not a Results recap; separate evidence from
speculation; integrate limitations with the claims they constrain; match
causal language to design; end at the broadest implication the evidence
supports. Do not turn association into causation. Do not use “consistent
with” as proof of a mechanism. Do not create a detached limitations inventory
when limitations can attach to the affected interpretation.

## Abstract

Write after the manuscript stabilises:

```text
context → gap/objective → methods → main results → conclusion
```

Use the most decision-relevant results. Include exact estimates only when they
materially improve understanding.

## Captions

A caption should let the figure or table stand alone. Define: what is shown;
population, period, or sample; panels, symbols, lines, intervals, and units;
statistical summaries and uncertainty; abbreviations not obvious from the
visual. Do not interpret the result in the caption unless the venue requires
it.

## Citations

- Place each citation next to the exact claim it supports.
- Group citations only when all sources support the same claim.
- Split compound sentences when different sources support different clauses.
- Narrative citations are valid when identity, chronology, or contrast matters.
- Finding-first prose is usually more concise when author identity does not matter.
- Preserve the project’s citation syntax and house style.
- Verify the paper, passage, and bibliographic record before submission.

## Statistical reporting

Prefer estimates and uncertainty over threshold-only statements. Include as
relevant: effect size or model estimate; confidence or credible interval;
sample size or effective sample size; units and comparison group;
model-performance metric; sensitivity or validation result.

Match precision to measurement and model uncertainty. Distinguish absence of
evidence from evidence of no effect. Do not turn prediction or association
into causation. State exploratory status when relevant.

## Revision passes

Use separate passes to avoid mixing jobs:

1. scientific accuracy and completeness
2. central contribution and whole-paper argument
3. section role and result logic
4. claim-evidence traceability
5. paragraph logic and transitions
6. sentence clarity and concision
7. terminology, numbers, figures, tables, and citations
8. journal formatting and final proof

Run deterministic lint only after the scientific and structural passes.
