---
name: manuscript-writing
description: >-
  Plan, storyboard, draft, revise, and audit empirical research manuscripts from
  verified project artifacts. Use for manuscript outlines, Introduction, Methods,
  Results, Discussion, Abstract, captions, surgical edits, and consistency checks.
  Reads the project question, implemented methods, verified literature, final
  tables and figures, and result claims before writing. Does not invent missing
  scientific details or silently resolve conflicts between prose, code,
  configuration, and outputs.
metadata:
  version: 3.1.0
---

# Manuscript writing

Write manuscripts from maintained evidence, not from memory.

## Scope

This skill owns manuscript argument, structure, prose, and manuscript-level
quality control. It does not own literature discovery, analysis design, project
scaffolding, statistical execution, figure rendering, or submission packaging.

Use companion workflows when available:

- `research-project-ops` for project state, authoritative artifacts, and conflicts
- `literature-review` for verified external evidence and citation support
- `analysis-design` for unresolved design or statistical questions
- Zotero tooling for citekeys and bibliography management
- `manuscript-markdown` for any Markdown↔DOCX conversion (default; not pandoc)

## Router

Classify the request before editing.

| Mode | Use when | Output |
|---|---|---|
| `outline` | Planning a manuscript or section | Central contribution, result logic, and paragraph storyboard |
| `draft` | Writing a new section | Evidence-grounded prose |
| `revise` | Improving logic, clarity, or structure | Revised section plus material issues |
| `surgical-edit` | User wants minimal changes | Only necessary edits; preserve wording and structure |
| `audit` | Checking a draft before review or submission | Prioritised issue report; no broad rewrite unless asked |
| `response-to-reviewers` | Revising from reviewer comments | Response map and manuscript changes |

## Evidence gate

Before planning or drafting, load the strongest available sources for the section.

| Section | Required inputs |
|---|---|
| Introduction | Current research question, scope, verified literature synthesis, references |
| Methods | Implemented methods, data documentation, configuration, code or workflow map |
| Results | Final result tables or registry, figures, uncertainty, analytical sample |
| Discussion | Confirmed results, verified literature, limitations, alternative explanations |
| Abstract | Stable section summaries or a stable full manuscript |
| Captions | Final figure or table, source variables, abbreviations, statistical definitions |

Evidence status must remain visible:

- `verified full text`
- `abstract only`
- `project result`
- `user supplied`
- `agent inference`
- `[TBC]`

Do not use search snippets as scientific evidence. Do not cite a paper for a
claim that has not been checked against the accessible source.

### Section readiness

Before substantial drafting, classify the requested section:

- `READY`: all material inputs are available and consistent
- `READY WITH GAPS`: drafting can proceed with visible `[TBC]` items
- `NOT READY`: a missing or conflicting input would make the draft unreliable

`research-project-ops` decides whether the underlying project is
manuscript-ready. This skill decides whether the requested writing task can
proceed from the available artifacts.

## Conflict gate

Stop and report a material conflict when, for example:

- Methods prose disagrees with code or configuration
- sample sizes differ across Results, tables, and figures
- a result in prose has no traceable output
- a citation does not support the sentence
- planned methods are written as completed methods

Route the conflict to `research-project-ops` or `analysis-design`. Do not
guess which version is correct.

## Workflow

1. Identify mode, manuscript type, audience, and available journal constraints.
2. Read the relevant project and evidence artifacts.
3. Apply the evidence, readiness, and conflict gates.
4. State or verify the central contribution.
5. Build or verify the result logic and paragraph storyboard when required.
6. Draft in the correct section role.
7. Revise in separate scientific, structural, and editorial passes.
8. Check claim-evidence traceability and cross-manuscript consistency.
9. Run deterministic lint as a final guardrail.
10. Return the finished artifact and only material unresolved issues.

## Planning gate

A storyboard is required for:

- a new manuscript
- a new complete section
- a major structural revision
- an Introduction or Discussion with several linked claims

It may be skipped for:

- surgical edits
- a single isolated paragraph
- captions
- proofreading or formatting

Use an existing `manuscript/outline.md` when present. Do not create a second
source of truth.

### Central contribution contract

Before outlining a whole paper, record:

| Field | Question |
|---|---|
| Research question | What exact question does the study answer? |
| Answer | What do the results establish? |
| Contribution | What changes because this study exists? |
| Evidence | Which result IDs, figures, or tables support the answer? |
| Boundary | What is the strongest claim the design and evidence permit? |
| Significance | Why does this contribution matter beyond the study? |

Every main figure, Results subsection, and Discussion claim should establish,
qualify, or interpret this contribution.

### Reverse figure outline

Before planning Results prose, map each final figure or table:

```text
question answered
→ result claim
→ exact supporting output
→ estimate and uncertainty
→ interpretation boundary
→ required Methods
→ next logical result
```

Order Results by scientific logic, not analysis chronology. Route visual design
or figure production to `figure-design`.

### Paragraph storyboard

Each planned paragraph should have one main job:

```text
purpose → claim → evidence or reasoning → boundary → transition
```

Record:

- what the reader must understand
- the paragraph's main claim
- supporting result IDs, figures, tables, or citations
- what the evidence does not establish
- why the next paragraph follows

See [reference.md](reference.md) for expanded section guidance. Use
[assets/manuscript-outline.md](assets/manuscript-outline.md) when a project does
not already have an outline format.

## Section contracts

### Introduction

Move from broad problem to the exact study:

```text
problem → established knowledge → unresolved gap → why it matters → objective/question
```

- Build only the background needed to understand the gap.
- Synthesize by idea, not paper-by-paper summaries.
- Match gap language to the scope of the literature search.
- End with the study objective, question, and predictions where applicable.
- Do not pre-report or interpret the study results.

### Methods

Move from overall design to reproducible detail:

```text
study design → data → eligibility → processing → variables → analysis → validation
```

- Report the implemented method, not the history of exploratory attempts.
- Keep consequential rationale brief; preserve the fuller history in decision records.
- Put rules in Methods and resulting counts in Results or QC outputs.
- State exact thresholds, units, software, versions, and validation where material.
- Use `[TBC]` rather than inventing missing details.

### Results

Follow the result logic and corresponding Methods:

```text
question → finding → estimate and uncertainty → figure/table → bounded answer
```

- Lead with the biological or scientific finding, then support it with numbers.
- Report effect size, uncertainty, sample, unit, and comparison where relevant.
- Do not explain mechanisms or broader implications.
- Do not repeat every number already visible in a table or figure.
- Distinguish primary, secondary, sensitivity, and exploratory results.

### Discussion

Use the inverse hourglass:

```text
main interpretation → literature comparison → alternatives → limitations → implications
```

For each important interpretation, connect:

```text
result ID → supported interpretation → literature agreement or conflict
→ plausible alternative → evidence boundary → implication
```

- Start with what the key findings mean, not a numerical Results recap.
- Separate direct evidence from interpretation and speculation.
- Address credible alternatives and contradictory literature.
- Integrate limitations with the claims they constrain.
- Match causal language to the study design.
- End at the broadest implication supported by the evidence.

### Abstract

Write the Abstract after the manuscript stabilises:

```text
context → gap/objective → methods → main results → conclusion
```

Use the most decision-relevant results. Include exact estimates only when they
materially improve understanding.

### Captions

A caption should let the figure or table stand alone. Define:

- what is shown
- population, period, or sample
- panels, symbols, lines, intervals, and units
- statistical summaries and uncertainty
- abbreviations not obvious from the visual

Do not interpret the result in the caption unless the venue requires it.

## Citation rules

- Put citations directly after the claim they support.
- Group citations only when all sources support the same claim.
- Use narrative author names only when identity, chronology, or contrast matters.
- Preserve the project's citation syntax and house style.
- Verify citekeys, bibliographic metadata, and claim support before submission.

## Statistical honesty

- Match precision to the data and analysis.
- Report uncertainty, not only point estimates.
- Distinguish absence of evidence from evidence of no effect.
- Do not turn prediction or association into causation.
- State exploratory status when relevant.
- Avoid threshold-only reporting when effect size and uncertainty are available.

## Revision passes

Do not mix all editing jobs in one pass:

1. scientific accuracy and completeness
2. central contribution and whole-paper argument
3. section role and result logic
4. claim-evidence traceability
5. paragraph logic and transitions
6. sentence clarity and concision
7. terminology, numbers, figures, tables, and citations
8. journal compliance when requirements are available
9. deterministic lint

## Style defaults

- Prefer clear subjects and concrete verbs.
- Use active voice when it improves clarity.
- Keep one main idea per sentence and paragraph where practical.
- Remove filler, repetition, and unnecessary nominalisations.
- Define study-specific terms and uncommon abbreviations at first use.
- Calibrate hedging to evidence; avoid stacked hedges.
- Preserve technical terms that carry necessary precision.
- Follow local journal and project conventions over generic preferences.

## Audit mode

Audit before rewriting. Classify findings:

- `BLOCKER`: scientific contradiction, unsupported claim, missing provenance, or wrong section
- `MAJOR`: logic, completeness, traceability, or interpretation problem
- `MINOR`: clarity, consistency, or local structure problem
- `EDITORIAL`: grammar, punctuation, or formatting

Check:

1. central contribution, question, objectives, analyses, results, and conclusions align
2. Methods match implementation
3. all reported values trace to authoritative outputs
4. tables, figures, captions, and prose agree
5. citations support the exact claims
6. section boundaries are respected
7. terminology, abbreviations, sample sizes, and units are consistent
8. `[TBC]`, placeholder citations, and missing figure references are resolved

Do not automatically rewrite scientific conflicts. Report them first.

## Deterministic validator

Run after the scientific and structural edit:

```bash
python skills/manuscript-writing/validator.py --file manuscript.md --mode normal
python skills/manuscript-writing/validator.py --file manuscript.md --mode strict
python skills/manuscript-writing/validator.py --file manuscript.md --section Results
```

The validator flags likely issues. It cannot determine scientific truth,
citation support, causal validity, or whether a paragraph makes the right
argument.

See [validator-README.md](validator-README.md) for check definitions.

## Output contract

For outlining:

1. provide the central contribution
2. provide the reverse figure outline when Results are in scope
3. provide the paragraph storyboard
4. list unresolved evidence or decisions

For drafting or revision:

1. provide the finished text
2. list material `[TBC]` items or scientific conflicts separately
3. do not add a long explanation of routine edits

For audit:

```markdown
## Readiness
READY | READY WITH GAPS | NOT READY

## Findings
- [severity] location: issue and required action

## Highest-value next action
...
```
