---
name: manuscript-writing
description: >-
  Plan, draft, revise, and audit empirical research manuscripts from verified project artifacts. Use for manuscript outlines, Introduction, Methods, Results, Discussion, Abstract, captions, journal adaptation, surgical edits, and consistency checks. Reads the project question, implemented methods, verified literature, final tables and figures, and result claims before writing. Does not invent missing scientific details or silently resolve conflicts between prose, code, configuration, and outputs.
metadata:
  version: 3.0.0
---

# Manuscript writing

Write manuscripts from maintained evidence, not from memory.

## Scope

This skill owns manuscript prose and manuscript-level quality control. It does not own literature discovery, analysis design, project scaffolding, or statistical execution.

Use companion workflows when available:

- `research-project-ops` for project state, authoritative artifacts, and conflicts
- `literature-review` for verified external evidence and citation support
- `analysis-design` for unresolved design or statistical questions
- Zotero tooling for citekeys and bibliography management

## Router

Classify the request before editing.

| Mode | Use when | Output |
|---|---|---|
| `outline` | Planning a manuscript or section | Claim-evidence paragraph plan |
| `draft` | Writing a new section | Evidence-grounded prose |
| `revise` | Improving logic, clarity, or structure | Revised section plus material issues |
| `surgical-edit` | User wants minimal changes | Only necessary edits; preserve wording and structure |
| `audit` | Checking a draft before review or submission | Prioritised issue report; no broad rewrite unless asked |
| `journal-adapt` | Adapting to a named venue | Structure, length, terminology, and formatting changes |
| `response-to-reviewers` | Revising from reviewer comments | Response map and manuscript changes |

## Evidence gate

Before drafting, load the strongest available sources for the section.

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

Do not use search snippets as scientific evidence. Do not cite a paper for a claim that has not been checked against the accessible source.

## Conflict gate

Stop and report a material conflict when, for example:

- Methods prose disagrees with code or configuration
- sample sizes differ across Results, tables, and figures
- a result in prose has no traceable output
- a citation does not support the sentence
- planned methods are written as completed methods

Route the conflict to `research-project-ops` or `analysis-design`. Do not guess which version is correct.

## Workflow

1. Identify mode, manuscript type, target journal, audience, and word limit when available.
2. Read the relevant project artifacts.
3. Build or verify the claim-evidence map.
4. Draft in the correct section role.
5. Check scientific boundaries and internal consistency.
6. Run deterministic lint as a final guardrail, not as a substitute for scientific review.
7. Return the revised text and list only material unresolved issues.

## Paragraph contract

Each paragraph should have one main job:

```text
purpose → claim → evidence or reasoning → boundary → transition
```

Before drafting a paragraph, identify:

- what the reader must understand
- the main claim
- the evidence supporting it
- the figure, table, result ID, or citation involved
- what the paragraph must not claim

## Section contracts

### Introduction

Move from broad problem to the exact study:

```text
problem → established knowledge → unresolved gap → why it matters → objective/question
```

Rules:

- Build only the background needed to understand the gap.
- Synthesize by idea, not paper-by-paper summaries.
- End with the study objective, question, and predictions where applicable.
- Do not pre-report or interpret the study results.

### Methods

Move from overall design to reproducible detail:

```text
study design → data → eligibility → processing → variables → analysis → validation
```

Rules:

- Report the implemented method, not the history of exploratory attempts.
- Keep consequential rationale brief; preserve the fuller history in decision records.
- Put rules in Methods and resulting counts in Results or QC outputs.
- State exact thresholds, units, software, versions, and validation where material.
- Use `[TBC]` rather than inventing missing details.

### Results

Follow the order of objectives and corresponding Methods:

```text
question → finding → estimate and uncertainty → figure/table
```

Rules:

- Lead with the biological or scientific finding, then support it with numbers.
- Report effect size, uncertainty, sample, unit, and comparison where relevant.
- Do not explain mechanisms or broader implications.
- Do not repeat every number already visible in a table or figure.
- Distinguish primary, secondary, sensitivity, and exploratory results.

### Discussion

Use the inverse hourglass:

```text
main interpretation → comparison with literature → explanations and alternatives → limitations → broader implications
```

Rules:

- Start with what the key findings mean, not a numerical Results recap.
- Separate direct evidence from interpretation and speculation.
- Address credible alternatives and contradictory literature.
- Match causal language to the study design.
- End at the broadest implication supported by the evidence.

### Abstract

Write the Abstract after the manuscript stabilises:

```text
context → gap/objective → methods → main results → conclusion
```

Use the most decision-relevant results. Include exact estimates only when they materially improve understanding.

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
- Use narrative author names only when the identity of the study or researcher is rhetorically relevant. Otherwise lead with the finding.
- Preserve the project's citation syntax and house style.
- Verify citekeys, bibliographic metadata, and claim support before submission.

## Statistical honesty

- Match precision to the data and analysis.
- Report uncertainty, not only point estimates.
- Distinguish absence of evidence from evidence of no effect.
- Do not turn prediction into causation.
- State exploratory status when relevant.
- Avoid threshold-only reporting when effect size and uncertainty are available.

## Style defaults

- Prefer clear subjects and concrete verbs.
- Use active voice when it improves clarity; passive voice is acceptable when the actor is irrelevant or the action should be foregrounded.
- Keep one main idea per sentence and paragraph where practical.
- Remove filler, repetition, and unnecessary nominalisations.
- Define study-specific terms and uncommon abbreviations at first use.
- Calibrate hedging to evidence; avoid stacked hedges.
- Preserve technical terms that carry necessary precision.
- Follow local journal and project conventions over generic style preferences.

## Audit mode

Audit before rewriting. Classify findings:

- `BLOCKER`: scientific contradiction, unsupported claim, missing provenance, or wrong section
- `MAJOR`: logic, completeness, traceability, or interpretation problem
- `MINOR`: clarity, consistency, or local structure problem
- `EDITORIAL`: grammar, punctuation, or formatting

Check:

1. question, objectives, analyses, results, and conclusions align
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

The validator flags likely issues. It cannot determine scientific truth, citation support, causal validity, or whether a paragraph makes the right argument.

See [reference.md](reference.md) for expanded guidance and [validator-README.md](validator-README.md) for check definitions.

## Output contract

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
