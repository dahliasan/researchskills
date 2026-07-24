---
name: manuscript-writing
description: >-
  Manuscript writing from verified project artifacts. Use when outlining,
  drafting, revising, surgically editing, auditing, checking for AI-shaped prose,
  or answering reviewers for empirical research manuscripts. When another skill
  needs manuscript prose or audit, invoke this skill.
metadata:
  version: 3.7.0
---

# Manuscript writing

Write manuscripts from maintained evidence, not from memory.

## Scope

Owns manuscript argument, structure, prose, and manuscript-level quality
control. Does not own literature discovery, analysis design, project
scaffolding, statistical execution, figure rendering, or submission packaging.

Companions when available: `research-project-ops`, `literature-review`,
`analysis-design`, Zotero tooling, `manuscript-markdown` (default MD↔DOCX).

## Router

Classify the request, then **read only that mode file** before editing:

| Mode | Use when | Load |
|---|---|---|
| `outline` | Planning a manuscript or section | [modes/outline.md](modes/outline.md) |
| `draft` | Writing a new section | [modes/draft.md](modes/draft.md) |
| `revise` | Improving logic, clarity, or structure | [modes/revise.md](modes/revise.md) |
| `surgical-edit` | Minimal changes; preserve wording | [modes/surgical-edit.md](modes/surgical-edit.md) |
| `audit` | Check scientific coherence before review or submission | [modes/audit.md](modes/audit.md) |
| `prose-audit` | Detect or remove formulaic, inflated, generic, or AI-shaped manuscript prose | [modes/prose-audit.md](modes/prose-audit.md) |
| `response-to-reviewers` | Revising from reviewer comments | [modes/response-to-reviewers.md](modes/response-to-reviewers.md) |

**Done when** the chosen mode file is loaded and its completion criterion is
met. Do not load other mode files.

Section contracts, planning detail, citations, and statistical reporting live
in [reference.md](reference.md). Conclusion-specific guidance lives in
[conclusion.md](conclusion.md). Load only the sections the mode asks for.

## Shared gates

Apply before substantive writing (every mode except pure proofreading).

### Evidence

| Section | Required inputs |
|---|---|
| Introduction | Research question, scope, verified literature synthesis, references |
| Methods | Implemented methods, data docs, configuration, code or workflow map |
| Results | Final tables/registry, figures, uncertainty, analytical sample |
| Discussion | Confirmed results, verified literature, limitations, alternatives |
| Conclusion | Stable main finding, supported implication, scope boundary |
| Abstract | Stable section summaries or stable full manuscript |
| Captions | Final figure/table, source variables, abbreviations, statistical defs |

Label evidence status: `verified full text` | `abstract only` | `project result`
| `user supplied` | `agent inference` | `[TBC]`.

Do not use search snippets as scientific evidence. Do not cite a paper for a
claim unchecked against the accessible source.

Readiness before substantial drafting: `READY` | `READY WITH GAPS` (visible
`[TBC]`) | `NOT READY`. `research-project-ops` decides project manuscript-
readiness; this skill decides whether *this writing task* can proceed.

### Conflict

Stop and report when Methods disagree with code/config; sample sizes disagree
across prose/tables/figures; a result has no traceable output; a citation does
not support the sentence; planned methods are written as completed. Route to
`research-project-ops` or `analysis-design`. Do not guess which version is
correct.

## Shared rules

**Prose vs scaffolding.** Manuscript prose holds only what a reader needs to
understand or reproduce the science. Citable packages, published functions, and
named methods stay in prose. Internal paths, custom function names, decision
tags, and claim IDs go in provenance notes. Worked examples:
[scaffolding.md](scaffolding.md).

**Citations.** Cite immediately after the claim; group only when every source
supports the same claim; preserve project cite syntax. Detail:
[reference.md](reference.md#citations).

**Statistical honesty.** Report uncertainty; distinguish absence of evidence
from evidence of no effect; do not upgrade association to causation. Detail:
[reference.md](reference.md#statistical-reporting).

## Workflow

1. Identify mode → load that mode file only.
2. Load evidence artifacts the mode requires.
3. Apply evidence, readiness, and conflict gates.
4. Execute the mode steps until its completion criterion is met.
5. Run the deterministic validator when the mode requires it.
6. Return only the mode’s output contract (plus material `[TBC]` / conflicts).

**Done when** every required mode step is complete, gates are applied or
explicitly waived by the mode, and the output matches the mode contract.

## Deterministic validator

```bash
python skills/manuscript-writing/validator.py --file manuscript.md --mode normal
python skills/manuscript-writing/validator.py --file manuscript.md --mode strict
python skills/manuscript-writing/validator.py --file manuscript.md --section Results
```

Guardrail only — not scientific truth. See [validator-README.md](validator-README.md).