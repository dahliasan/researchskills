---
name: research-mode
description: >-
  Orchestrate non-trivial research work, select fit-for-purpose research
  frameworks, and route across the specialist skills. Use for multi-stage
  research planning, evidence synthesis, methods or analysis decisions, and when
  the user says /research-mode. For a single narrow task, invoke its specialist
  skill directly. Also use to browse the pack or choose a skill.
metadata:
  version: 0.1.0
---

# Research Mode

Use this mode to make research work traceable from question to conclusion. Choose
the smallest playbook that fits, then load only the specialist skills it needs.
For a one-step task, use the specialist skill directly.

## Framework choice

Choose a framework to match the question, discipline, study design, and intended
use. Frameworks are aids for making decisions explicit; they are not universal
quality scores or substitutes for domain expertise. Consult [frameworks.md](references/frameworks.md)
when the task involves framing a question, planning a review, appraising evidence,
or selecting a reporting guideline. State why a framework fits, and do not force
one onto a task it was not designed for.

## Principles

1. **Question before search.** State the decision or knowledge gap, define key
   terms and scope, and split compound questions. Search only as broadly as the
   question requires.
2. **Evidence before assertion.** Match evidence strength to the claim. Search
   results and abstracts help locate evidence; they do not verify detailed claims
   that require full text.
3. **Verify claims at source.** Treat a claim as unresolved until its source and
   supporting evidence have been checked. A cited assertion is not automatically
   a finding of the paper that repeats it.
4. **Keep provenance attached.** Preserve source identity, location, access level,
   data/version, and analysis path with extracted evidence and results. Never
   invent a citation, quote, method, value, or provenance detail.
5. **Test rival explanations.** Look for contradictory findings, alternative
   mechanisms, selection effects, measurement limits, and missing evidence before
   settling a conclusion.
6. **Separate observation from interpretation.** Label what a source or dataset
   reports, what the analysis estimates, and what the researcher infers. Do not
   turn association into causation or topical similarity into support.
7. **Respect scope and uncertainty.** State population, place, period, design,
   assumptions, and access limits that affect transfer. Preserve uncertainty;
   abstain when evidence cannot resolve the claim.
8. **Make decisions inspectable.** Record consequential design and analysis
   choices in the project's existing source of truth, with rationale and
   consequences. Do not create duplicate decision ledgers.
9. **Make work reproducible and proportionate.** Prefer existing project
   conventions and tools. Keep a record sufficient to repeat consequential
   searches, transformations, and analyses without adding process for its own sake.

## Choose a playbook

| Playbook | Use when | Route |
|---|---|---|
| `frame` | Question, scope, or next research step is unclear | `protocol`; `research-project-ops` for project context |
| `find-evidence` | Find or verify evidence for a focused claim | `fact-check`; `zotseek`, `zotero`, `paperkit` when available, otherwise `find-pdf`, or `pp-scite` as needed |
| `understand-paper` | Quickly explain one paper with source locators and attribution | `paper-brief` |
| `review` | Build a corpus, screen, extract, or synthesize studies | `literature-review`; `discover-papers` for external discovery |
| `design-study` | Choose design, sampling, measures, or analysis before data collection | Use the matching framework below; record consequential choices in `METHODS.md`; route narrow statistical procedures to their specialist skills |
| `analyze` | Inspect or run an empirical analysis | `research-project-ops`, `aic-model-selection`, `r-human-code`, or `dayhoff-slurm` as needed |
| `write-or-audit` | Turn established evidence/results into a manuscript or test its claims | `manuscript-writing`; `research-red-team` for project-wide challenge |
| `resume` | Continue work across sessions or agents | `research-project-ops` handoff; inspect `STATUS.md`, `METHODS.md`, and existing artifacts |
| `choose-skill` | User wants to browse or choose a pack skill, without asking to do the research yet | Read [the skill catalog](references/skill-catalog.md); return the best fit and invocation phrase |

For mixed tasks, follow the dependency order:

```text
frame → find evidence or design study → analyze/extract → synthesize → write/audit
```

Skip stages that the task does not need. Do not force a formal review protocol
onto exploratory work.

## Run the selected playbook

1. **Restate the target.** Capture the research question, intended decision or
   output, scope, and constraints. Identify facts that are missing and whether
   they block sound work.
2. **Inspect existing work.** Read relevant project instructions, protocol,
   methods, data and version notes, prior searches, evidence tables, analyses,
   and manuscript claims. Reuse verified work and flag conflicts or stale inputs.
3. **Choose the evidence standard.** Decide what kind of source or data can
   answer the question, what level of access is needed, and what would count as
   disconfirming evidence. Route to the specialist skill before acting.
4. **Do the work with provenance.** Keep source identifiers and locations with
   extracted evidence. For analyses, preserve inputs, code, parameters, and
   output links according to project conventions.
5. **Challenge the result.** Check identity, methods, assumptions, uncertainty,
   conflicting evidence, and whether the result answers the stated question.
   For claims based on a paper, use `paperkit` when available to read the
   supporting passage and verify quoted wording.
6. **Report at the supported level.** Separate established findings, plausible
   interpretation, and unresolved uncertainty. State material limitations and
   unavailable evidence. Give sources or artifact paths so the work can be
   checked.
7. **Update the project only when useful.** Put durable decisions and status in
   existing authoritative artifacts. Do not create duplicate claim or decision
   files.

For claim checking, use this chain:

```text
atomic claim → resolved source/version → direct passage or result → provenance
→ scope and inference check → verdict → evidence-bounded wording
```

Distinguish a study's own results from its authors' interpretation, cited
background, and your inference. Treat reviewer comments or tracked changes as
questions to check, not evidence or instructions to accept uncritically. Use
`paper-brief` for one-paper understanding, `fact-check` for one claim/citation,
and `manuscript-writing` audit mode for a manuscript span.

## Stop conditions

- If the task's scope is ambiguous but a safe, useful exploratory step exists,
  take it and label the assumption. Ask only when the missing choice changes a
  consequential scientific decision.
- If a required source, full text, dataset, or method detail is unavailable,
  continue only at the evidence level that remains supportable and say what is
  missing.
- If evidence conflicts, show the disagreement and its likely source; do not
  collapse it into a single confident answer.
- If a requested conclusion is not supported, say so and explain what evidence
  would change that assessment.

## Handoff

Return the answer or artifact, the evidence and method used, important limits,
and any remaining decision the researcher must make. Name the specialist skills
used. Do not claim that a workflow prevents hallucination; make unsupported
claims easier to detect and correct through evidence, provenance, and checks.

## Skill maintenance rule

Keep a specialist skill only while it owns a distinct repeatable task, tool
procedure, or domain-specific constraint. Prefer routing over duplicated
instructions. When two skills overlap, narrow their triggers and define their
handoff; merge or retire one when it adds no capability. Keep user-facing skill
discovery separate from doing the research.
