---
name: manuscript-submission
description: >-
  Prepare and audit empirical research manuscripts for submission to a named
  journal or venue. Use for journal requirement extraction, manuscript
  adaptation, reporting-guideline selection, submission checklists, title
  pages, cover letters, declarations, data and code availability, supplements,
  file packaging, and final preflight checks. Preserves scientific meaning and
  routes unresolved prose, evidence, analysis, or figure problems to their
  owning workflows.
metadata:
  version: 0.1.0
---

# Manuscript submission

Turn a scientifically stable manuscript into a complete, traceable submission
package.

## Scope

This skill owns venue requirements, reporting compliance, submission
components, package assembly, and final preflight checks. It does not own:

- the scientific argument or core manuscript drafting
- literature discovery or citation verification
- statistical analysis
- figure design or result selection
- project provenance

Use companion workflows when available:

- `manuscript-writing` for scientific prose and structural revision
- `figure-design` for visual changes and export quality
- `research-project-ops` for provenance, availability statements, ethics, funding, and project facts
- `literature-review` for unsupported external claims
- `analysis-design` for unresolved analytical problems

## Router

| Mode | Use when | Output |
|---|---|---|
| `requirements` | Choosing or inspecting a target venue | Dated venue-requirements matrix |
| `journal-adapt` | Adapting a stable manuscript | Compliant manuscript plus change report |
| `reporting-check` | Applying a study-type guideline | Completed or gap-marked checklist |
| `preflight` | Checking readiness before submission | Prioritised readiness report |
| `package` | Preparing all submission files | File manifest and complete package plan |
| `cover-letter` | Drafting venue correspondence | Evidence-grounded cover letter |

## Source gate

Journal requirements can change. For a named venue, inspect current
authoritative sources where available:

1. journal instructions for authors
2. article-type requirements
3. publisher submission-system guidance
4. named reporting guideline and official checklist
5. project and manuscript artifacts

Record the source URL and access date for consequential requirements. If current
instructions are inaccessible, say so and separate verified requirements from
assumptions.

Do not use an unrelated journal, old manuscript, or generic memory as authority
for venue-specific rules.

## Scientific stability gate

Before full adaptation or packaging, classify the manuscript:

- `STABLE`: scientific content and main outputs are approved for submission work
- `STABLE WITH GAPS`: packaging can proceed with visible missing components
- `UNSTABLE`: unresolved science would make submission adaptation premature

Stop and route material issues when:

- manuscript values conflict with results or figures
- Methods do not match implementation
- citations do not support important claims
- figures require new analysis
- authorship, ethics, funding, or availability facts are disputed
- adapting to the word limit would remove scientifically necessary information

Never silently change scientific meaning to satisfy formatting or length.

## Workflow

1. Identify venue, article type, submission stage, and user goal.
2. Inspect current authoritative venue requirements and record their date.
3. Load the stable manuscript, figures, tables, supplements, and project facts.
4. Build the requirements matrix and choose applicable reporting guidelines.
5. Apply the scientific stability gate.
6. Adapt structure and formatting without changing evidential meaning.
7. Prepare missing submission components from verified facts.
8. Build the file manifest and cross-check every manuscript reference.
9. Run reporting, consistency, anonymity, and technical preflight checks.
10. Return the package or readiness report with only material unresolved items.

Use [assets/submission-checklist.md](assets/submission-checklist.md) when the
project has no existing submission tracker. Read
[references/submission-guidance.md](references/submission-guidance.md) for
component and reporting-guideline details.

## Requirements matrix

Record each requirement before editing:

| Field | Value |
|---|---|
| Venue and article type | |
| Requirement | |
| Verified source and access date | |
| Current manuscript state | |
| Required action | |
| Owner | |
| Status | verified, assumed, complete, blocked, or not applicable |

Cover at minimum:

- article structure and section order
- word, abstract, reference, figure, and table limits
- title and running-title rules
- abstract format
- reference and citation style
- figure dimensions, formats, colour mode, and resolution
- table format
- supplement rules
- anonymisation or double-blind requirements
- reporting guidelines
- mandatory declarations
- data, code, and materials availability
- submission-system file requirements

## Reporting guidelines

Choose guidelines from study design and article type, not discipline alone.

1. Identify the actual study design.
2. Check the journal's named requirements.
3. Find the official current checklist.
4. Map every item to a manuscript location or a visible gap.
5. Treat a checklist as a reporting aid, not proof of methodological quality.
6. Do not mark an item complete merely because related words appear in the manuscript.

If no specific guideline fits, use the journal requirements and a transparent
general completeness audit.

## Manuscript adaptation

Permitted changes include:

- section order and headings
- abstract structure
- length and redundancy reduction
- terminology required by the venue
- citation and reference formatting
- placement of tables, figures, and supplementary references
- declaration and availability sections

Require explicit scientific review for:

- removing methods needed for reproducibility
- removing limitations or uncertainty
- changing hypotheses, outcomes, or analysis labels
- replacing exact results with materially different summaries
- changing causal or novelty claims
- merging categories or results to meet length

Keep a concise change map for material adaptations.

## Submission components

Prepare only from verified project facts:

- title page
- author names, affiliations, and corresponding-author details
- author contributions
- funding
- competing interests
- ethics approvals and permits
- acknowledgements
- data availability
- code availability
- materials availability
- preregistration or protocol registration
- cover letter
- highlights, keywords, graphical abstract, or plain-language summary when required

Use `[TBC]` for missing facts. Never infer authorship order, contributions,
funding, conflicts, ethics identifiers, or repository access conditions.

## Cover letter

A concise cover letter may include:

1. manuscript title and article type
2. research question and central contribution
3. why the work fits the venue
4. confirmation of originality or related manuscripts when verified
5. required ethics, conflict, or author confirmations
6. corresponding-author contact details

Do not use inflated novelty claims or repeat the abstract. Do not claim all
authors approved submission unless confirmed.

## File manifest

For every submitted file record:

| File | Purpose | Version | Manuscript references | Required format | Status |
|---|---|---|---|---|---|

Check:

- figure and table numbering
- supplement numbering
- filenames and allowed characters
- current versions
- anonymised versus identified variants
- embedded versus separate files
- source or editable files when required
- no orphaned references or unreferenced files

## Preflight audit

Classify findings:

- `BLOCKER`: submission cannot proceed reliably
- `MAJOR`: likely rejection, return, or scientific inconsistency
- `MINOR`: correct before submission
- `EDITORIAL`: optional polish

Check:

1. target venue and article type are confirmed
2. current requirements and reporting guidelines are recorded
3. scientific content is stable
4. manuscript structure and limits comply
5. title, abstract, figures, tables, captions, and supplements agree
6. every figure, table, supplement, and citation reference resolves
7. declarations use verified facts
8. data and code statements match actual access conditions
9. anonymisation is complete where required
10. placeholders, tracked changes, comments, and hidden identifying metadata are resolved
11. file formats, dimensions, names, and versions are correct
12. package contents match the file manifest

## Output contract

For requirements or reporting checks:

1. dated requirements matrix or checklist
2. manuscript locations
3. gaps and owners
4. highest-value next action

For adaptation:

1. adapted manuscript or exact edits
2. material change map
3. unresolved scientific or venue questions

For preflight:

```markdown
## Readiness
READY | READY WITH GAPS | NOT READY

## Findings
- [severity] component: issue and required action

## Package manifest
- file: purpose and status

## Highest-value next action
...
```
