# Evidence Artifact Contracts

Use these as interoperable contracts, not mandatory file names. Preserve an existing equivalent when it already serves the same purpose.

## Evidence levels

```text
metadata-only
abstract-only
full-text
full-text-plus-supplement
```

## Paper lifecycle

```text
discovered
→ abstract-screened
→ full-text-screened
→ extracted
→ verified
→ synthesised
```

A paper may also be `excluded` with a recorded reason.

## `REVIEW.md`

Purpose: current review intent and state.

```markdown
# Review title

**Purpose:** preliminary | methods | scoping | systematic | update
**Status:** active | paused | complete
**Last updated:** YYYY-MM-DD

## Research question
## Scope
## Search approach
## Current corpus
## Current synthesis
## Access limitations
## Open questions
## Next action
```

For a formal review, `PROTOCOL.md` remains the source of truth for locked methods. `REVIEW.md` records current state and links to it.

## Candidate and paper record

Prefer JSONL when records will be updated programmatically.

```yaml
paper_id: DOI or stable identifier
title:
authors: []
year:
doi:
source_type: journal-article | preprint | report | review | other
publication_status:
discovery:
  - source:
    query_id:
    run_id:
    searched_at:
access:
  level: metadata-only | abstract-only | full-text | full-text-plus-supplement
  full_text_path:
  full_text_url:
  checked_at:
screening:
  status: discovered | abstract-screened | full-text-screened | excluded
  decision: include | exclude | maybe
  reason:
review_tags: []
```

## Search log

```yaml
run_id:
source:
searched_at:
query_id:
query:
filters:
result_count:
export_path:
notes:
```

Preserve the exact executed query, not only a cleaned summary.

## Screening record

```yaml
paper_id:
stage: title | abstract | full-text
decision: include | exclude | maybe
reason:
reviewer:
decided_at:
model_assistance:
```

Human and AI decisions should remain distinguishable.

## Full-text extraction record

```yaml
paper_id:
review_question:
extraction_version:
access_level: full-text | full-text-plus-supplement
checked_sections: []

study:
  objective:
  design:
  population_or_system:
  location:
  period:
  sample:

methods:
  sampling:
  measurements:
  processing:
  analysis:
  validation:

results:
  outcomes: []
  estimates: []
  uncertainty: []
  null_or_conflicting_results: []

limitations:
  author_stated: []
  reviewer_appraisal: []

relevance:
  review_theme: []
  implications:
  transferability:

verification:
  status: extracted | verified
  verified_at:
  notes:
```

Every material extracted field should include an evidence location when practical:

```yaml
evidence_location:
  section:
  page:
  paragraph:
  table:
  figure:
```

## Claim record

```yaml
claim_id:
paper_id:
claim:
claim_type: author-reported | reviewer-inference | synthesis
support:
  evidence_location:
  short_passage:
  faithful_paraphrase:
evidence_level:
verification_status: candidate | verified | rejected
notes:
```

Do not store a claim as verified without a retrievable evidence location.

## Synthesis matrix

Minimum columns:

```text
theme_or_question
paper_id
study_context
method
relevant_finding
uncertainty_or_limitation
evidence_level
evidence_location
reviewer_interpretation
```

A second theme-level table may contain:

```text
theme
established_evidence
conflicting_evidence
methodological_limits
population_or_context_limits
gap
implication_for_project
supporting_paper_ids
```

## Methods evidence table

```text
paper_id
research_step
method_used
study_context
important_parameters
validation
author_stated_limitations
transferability_to_project
evidence_location
```

## Citation check record

```yaml
manuscript_claim:
cited_paper_id:
classification: supported | partially-supported | unsupported | source-unavailable
supporting_location:
mismatch:
recommended_action:
checked_at:
```

## Minimal preliminary-review set

```text
literature/
├── REVIEW.md
├── core-papers.csv or papers.jsonl
├── synthesis-matrix.csv
└── references.bib
```

## Larger or formal-review set

```text
literature/
├── REVIEW.md
├── PROTOCOL.md
├── search-log.jsonl
├── papers.jsonl
├── screening.jsonl
├── access-status.jsonl
├── extractions/
├── claims/
├── synthesis-matrix.csv
├── gaps.md
└── HANDOFF.md
```

Do not create all files by default. Activate an artifact when it removes a current review bottleneck or provides required traceability.
