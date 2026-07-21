# Manuscript writing reference

This file expands the core contracts in `SKILL.md`. Project and journal rules
take priority.

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

A figure may support more than one secondary observation, but it should have one
clear primary purpose.

## Paragraph storyboard

Before drafting, structure each paragraph as:

| Field | Question |
|---|---|
| Purpose | What must the reader understand? |
| Claim | What single point does the paragraph make? |
| Evidence | Which result, figure, table, or source supports it? |
| Boundary | What does the evidence not establish? |
| Transition | Why does the next paragraph follow? |

Use citation keys, result IDs, and figure references. Do not draft unsupported
bridging claims merely to make the story sound complete.

## Introduction

A useful sequence is:

1. establish the broad scientific problem
2. narrow to the relevant process, system, or population
3. synthesise what prior work establishes
4. identify the unresolved problem precisely
5. explain why resolving it matters
6. state the objective, question, and predictions

Common failures:

- opening too broadly and never narrowing
- listing papers one at a time
- claiming a universal gap from a limited search
- introducing methods detail before the question
- ending without a clear objective
- building context that never contributes to the central question

## Methods

Write in the order a reader needs to reproduce the study:

1. study design and scope
2. data sources or sampling
3. eligibility and exclusions
4. preprocessing and quality control
5. variables and measurements
6. analytical procedure
7. validation, diagnostics, and sensitivity analyses
8. software, versions, and reproducibility information

Distinguish:

- planned from implemented
- rules from resulting counts
- routine implementation from consequential methodological rationale
- exploratory analyses from confirmatory analyses

Avoid vague verbs such as “cleaned”, “processed”, or “analysed” without the
operation, rule, and parameter.

## Results

Organise Results around objectives and final outputs, not the chronological
order of analysis.

A strong result unit includes:

- the question being answered
- the finding in scientific terms
- direction and magnitude
- uncertainty
- sample or analytical unit where needed
- figure or table reference
- a bounded answer that sets up the next result

Report exact values selectively. Use prose for the message and tables for dense
exact detail.

## Discussion

Map each important interpretation before drafting:

| Field | Question |
|---|---|
| Result | Which confirmed result is being interpreted? |
| Interpretation | What does the result mean? |
| Literature | Which verified studies agree, conflict, or define the context? |
| Alternative | What else could explain the pattern? |
| Boundary | How do the design, data, and uncertainty limit the claim? |
| Implication | What broader conclusion follows within that boundary? |

A useful whole-section sequence is:

1. interpret the main finding
2. compare it with relevant literature
3. examine plausible mechanisms and alternatives
4. explain how design and data affect interpretation
5. state material limitations where they constrain claims
6. broaden to the supported scientific or practical implication

Do not turn association into causation. Do not use “consistent with” as proof of
a mechanism. Do not create a detached limitations inventory when limitations
can be connected to the affected interpretation.

## Citations

- Place each citation next to the exact claim it supports.
- Split compound sentences when different sources support different clauses.
- Narrative citations are valid when identity, chronology, or contrast matters.
- Finding-first prose is usually more concise when author identity does not matter.
- Preserve the project’s citation syntax.
- Verify the paper, passage, and bibliographic record before submission.

## Statistical reporting

Prefer estimates and uncertainty over threshold-only statements. Include as
relevant:

- effect size or model estimate
- confidence or credible interval
- sample size or effective sample size
- units and comparison group
- model-performance metric
- sensitivity or validation result

Use precision that matches measurement and model uncertainty.

## Revision passes

Use separate passes to avoid mixing jobs:

1. scientific accuracy and completeness
2. central contribution and whole-paper argument
3. section role and result logic
4. claim-evidence traceability
5. paragraph logic and transitions
6. sentence clarity
7. terminology, numbers, figures, tables, and citations
8. journal formatting and final proof

Run deterministic lint only after the scientific and structural passes.
