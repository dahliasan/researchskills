---
name: manuscript-writing
description: >-
  Manuscript writing from verified project artifacts. Use when outlining,
  drafting, revising, surgically editing, auditing, or answering reviewers for
  empirical research manuscripts. When another skill needs manuscript prose or
  audit, invoke this skill.
metadata:
  version: 3.8.0
---

# Manuscript writing

Write manuscripts from maintained evidence, not from memory.

## Scope

Owns manuscript argument, structure, prose, and manuscript-level quality
control. Does not own literature discovery, study or analysis design, project
scaffolding, statistical execution, figure rendering, or submission packaging.

Companions when available: `research-project-ops`, `literature-review`,
`research-mode` for study or analysis design, Zotero tooling, and
`manuscript-markdown` (default MD↔DOCX).

## Router

Classify the request, then **read only that mode file** before editing:

| Mode | Use when | Load |
|---|---|---|
| `outline` | Planning a manuscript or section | [modes/outline.md](modes/outline.md) |
| `draft` | Writing a new section | [modes/draft.md](modes/draft.md) |
| `revise` | Improving logic, clarity, or structure | [modes/revise.md](modes/revise.md) |
| `surgical-edit` | Minimal changes; preserve wording | [modes/surgical-edit.md](modes/surgical-edit.md) |
| `audit` | Check before review or submission | [modes/audit.md](modes/audit.md) |
| `response-to-reviewers` | Revising from reviewer comments | [modes/response-to-reviewers.md](modes/response-to-reviewers.md) |

**Done when** the chosen mode file is loaded and its completion criterion is
met. Do not load other mode files.

Section contracts, planning detail, citations, and statistical reporting live
in [reference.md](reference.md) — load the sections the mode asks for, not the
whole file unless the mode requires it.

## Shared gates

Apply before substantive writing (every mode except pure proofreading).

### Evidence

| Section | Required inputs |
|---|---|
| Introduction | Research question, scope, verified literature synthesis, references |
| Methods | Implemented methods, data docs, configuration, code or workflow map |
| Results | Final tables/registry, figures, uncertainty, analytical sample |
| Discussion | Confirmed results, verified literature, limitations, alternatives |
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
`research-project-ops` or `research-mode`. Do not guess which version is
correct.

## Shared rules

**Prose vs scaffolding.** Manuscript prose holds only what a reader needs to
understand or reproduce the science. Citable packages, published functions, and
named methods stay in prose. Internal paths, custom function names, and decision
IDs (from `METHODS.md` Decision ledger) go in provenance notes — never claim-ID
maps. Worked examples: [scaffolding.md](scaffolding.md).

**Verify, don't guess.** If a tool you have can settle a fact, use it before
writing or asking. For example, measure a distance from coordinates, count from
the data, open the cited paper, or check a publication date. Ask the user only
for what no tool can reach, and never present an estimate as a checked fact.
Build the evidence from several sources in the library rather than leaning on
one convenient review for every claim.

**Relevance.** Every sentence, clause and detail must serve this paper's
question, result or implication. When citing another species or system, keep
the finding that transfers and drop details that only matter there. A fact that
is true but does no work in the argument is filler. This applies to what you
add; it is not a licence to cut existing coauthor text without a reason.

**Say it once.** Give each point, definition and threshold one home. After
Methods defines a threshold, time or term, refer to it by name instead of
restating the value. Don't repeat the Introduction's background in the
Discussion, and don't cite the same claim to the same source in several
paragraphs.

**Point-first paragraphs.** Open each paragraph with its point, not an
announcement of its subject ("X may also differ…", "This provides a test
of…"). If the point is uncertain, state the uncertain point plainly; the hedge
belongs in the claim, not in a vague opener.

**Proportion.** Frame the work at its real size. Don't invent a gap by
claiming what managers or researchers lack or don't know unless a source says
so; state why the result is useful instead. Don't force tension into a
straightforward story, and keep the register neutral rather than persuasive.
Keep the Discussion in proportion to the Introduction and to the number of
real findings.

**Limitations: the materiality test.** Mention a limitation only if it could
change the direction, size or certainty of a main conclusion, or how a reader
can use the result. Ask: at its worst, would this change what we conclude?
- **Yes:** state it once, plainly, with what it means for the conclusion.
- **No, and we checked:** report the check as a result in one clause (for
  example "results were unchanged when…"), not as a limitation.
- **No, probably nothing:** leave it out. Small data gaps, routine
  approximations and minor definitional choices that don't affect the result
  are not limitations, and listing them invites doubt the data don't support.
Never hide a material limitation; the test removes noise, not honesty.

**Citations.** Cite immediately after the claim; group only when every source
supports the same claim; preserve project cite syntax. Detail:
[reference.md](reference.md#citations).

**Word files.** When editing a `.docx` the user may have open in Word, check
it, save and close it before reading, edit the file now on disk, then reopen
it. Write tracked changes with the shared tool `scripts/track_edit.py`; don't
write a new OOXML script. Have a Claude model run the Word step. Detail:
[word-documents.md](word-documents.md).

**Statistical honesty.** Report uncertainty; distinguish absence of evidence
from evidence of no effect; do not upgrade association to causation. Detail:
[reference.md](reference.md#statistical-reporting).

## Workflow

1. Identify mode → load that mode file only.
2. Load evidence the mode requires (METHODS, results tables/figures, verified literature — not a claims file).
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
