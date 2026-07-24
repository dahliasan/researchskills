---
name: literature-review
description: >-
  Manage an evidence-grounded literature workflow from an exploratory research
  question through paper discovery, full-text retrieval, structured extraction,
  synthesis, and citation checking. Use for preliminary reviews, research-question
  refinement, methods searches, formal reviews, evidence updates, synthesis
  matrices, or checking whether papers support manuscript claims. Routes internally
  to protocol, discover-papers, find-pdf, and Zotero/ZotSeek when available.
  Does not treat search snippets or abstracts as full-text evidence.
metadata:
  version: 0.1.1
---

# Literature Review

You coordinate the literature workflow and its durable evidence artifacts.
Use existing literature capabilities rather than reimplementing search, PDF
retrieval, library management, or screening engines.

`literature-review` is a peer of `research-project-ops`, `analysis-design`, and
`manuscript-writing`. It does not own those skills.

## Core rule

Do not complete a literature task at a lower evidence level than it requires.
Never fill missing scientific detail from convention, memory, or a likely method.
Record unavailable information as unavailable.

## Step 0: Detect the mode

| User need | Mode |
|---|---|
| Understand a topic or build a core reading set | `orient` |
| Refine or test a provisional research question | `question-refinement` |
| Find evidence for sampling, processing, modelling, or validation choices | `methods-search` |
| Run a scoping, systematic, or other reproducible review | `formal-review` |
| Update an earlier search with newer literature | `update-search` |
| Extract study information from selected papers | `extract` |
| Compare studies, build a synthesis matrix, or identify gaps | `synthesise` |
| Check whether a citation supports a claim | `citation-check` |
| Resume or hand off an existing review | `handoff` |

If multiple modes apply, use this order:

```text
orient or formal-review
→ discover
→ retrieve
→ extract
→ synthesise
→ citation-check
→ handoff
```

Do not force a formal protocol onto a one-off exploratory search.

## Step 1: Inspect existing evidence

Before searching, inspect what already exists when accessible:

- review scope or `PROTOCOL.md`
- `references.bib`
- Zotero collections and attached PDFs
- prior search logs and candidate lists
- screening decisions
- extraction records
- synthesis matrices
- manuscript claims that need evidence

When the review belongs to a larger research project, read relevant project files
for context, but do not take ownership of them.

Reuse verified evidence rather than searching from scratch. Report stale,
conflicting, or duplicate review artifacts.

## Step 2: Apply the evidence-access gate

| Task | Minimum evidence |
|---|---|
| Candidate discovery | bibliographic metadata |
| Relevance screening | abstract, when available |
| Study design or methods extraction | full Methods and relevant supplements |
| Numerical results extraction | full Results, tables, and figures |
| Limitations appraisal | full Discussion and limitations |
| Citation verification | exact supporting passage, table, figure, or result |
| Cross-study synthesis | verified extraction from relevant full-text sections |

Use these review statuses:

```text
discovered
abstract-screened
full-text-screened
extracted
verified
synthesised
excluded
```

Also record access level:

```text
metadata-only
abstract-only
full-text
full-text-plus-supplement
```

If required full text is unavailable:

1. route to `find-pdf`
2. try authorised or lawful retrieval routes available to the user
3. keep the paper in the corpus with its access limitation
4. do not promote detailed claims from that paper to `verified`
5. provide a limited preliminary answer only when useful and label it clearly

PDF failure must not stop discovery or corpus building, but it must block
full-text extraction and claim verification.

## Step 3: Route within the literature workflow

| Need | Internal route |
|---|---|
| Durable review question, eligibility, and search plan | `protocol` |
| External paper discovery | `discover-papers` |
| Existing-library keyword or bibliographic search | `zotero` |
| Existing-library semantic search | `zotseek` |
| PDF or full-text retrieval | `find-pdf` |
| Batch discovery, screening, and library sync | optional local batch engine, when installed |

The skill is the literature review-state router. Search engines, PDF libraries,
credentials, and heavy pipelines remain external.

## Peer handoffs

These are peer skills, not parts of the literature-review workflow:

- Hand accepted research-question, scope, project-status, or artifact changes to
  `research-project-ops`.
- Hand accepted study-design or analytical implications to `analysis-design`.
- Hand verified literature evidence to `manuscript-writing` when drafting or
  revising manuscript prose.

Do not edit another peer skill's authoritative artifacts unless the user asks for
that handoff and the peer workflow is available.

## Mode workflows

### `orient`

Use for a preliminary review or first pass around a topic.

1. Restate the provisional topic or question.
2. Search broadly enough to learn terminology and field structure.
3. Prioritise recent reviews, landmark studies, directly related primary studies,
   and useful methods papers.
4. Retrieve full text for the small core set needed for decisions.
5. Produce a compact thematic synthesis and research implications.
6. State what remains unsearched or unverified.

Default output is a core reading set and compact synthesis, not a formal review report.

### `question-refinement`

Assess whether the provisional question is:

- already answered
- scientifically meaningful
- specific and measurable
- feasible with likely data and methods
- framed at an appropriate spatial, temporal, taxonomic, or conceptual scale

Produce established knowledge, unresolved uncertainty, a candidate gap, question
revisions with reasons, methods or data implications, and remaining search needs.

Do not independently overwrite project files. Hand accepted changes to
`research-project-ops`.

### `methods-search`

Search specifically for evidence relevant to:

- study design and sampling
- measurement and preprocessing
- model or test selection
- assumptions and diagnostics
- validation and sensitivity analysis
- common failure modes
- reporting standards

Full Methods and relevant supplements are required before extracting detailed
parameters or presenting a paper as methodological precedent.

Return a methods evidence table containing citation, research step, method,
context, important parameters, validation, author-stated limitations,
transferability, and evidence location.

Hand accepted analytical implications to `analysis-design`.

### `formal-review`

1. Route to `protocol` unless an adequate locked protocol already exists.
2. Run discovery from the approved queries and sources.
3. Preserve search provenance and raw candidate records.
4. Deduplicate using stable identifiers first, then normalized metadata.
5. Screen title, abstract, and full text as required.
6. Record exclusion reasons.
7. Extract using the protocol-defined schema.
8. Synthesize across studies rather than summarizing papers one by one.
9. Produce the reporting artifacts required by the review type.

Do not describe the work as systematic unless the documented process supports that claim.

### `update-search`

1. Read the prior protocol, search log, and last search date.
2. Re-run the locked searches for the new date window.
3. Preserve the original corpus and identify newly discovered records.
4. Deduplicate against the existing corpus.
5. Screen and extract only new or materially changed evidence.
6. Update conclusions only where the new evidence warrants it.

### `extract`

Canonical paper card: [../../schemas/paper-extraction.v1.schema.json](../../schemas/paper-extraction.v1.schema.json)
(`schema_version`: `researchskills.extraction.v1`). Example:
[../../schemas/examples/paper-extraction.v1.example.json](../../schemas/examples/paper-extraction.v1.example.json).

**Prompt (PROTOCOL-templated, project-agnostic base):**

```bash
python skills/literature-review/scripts/render_extraction_prompt.py \
  --protocol PROTOCOL.md \
  -o /tmp/extract_prompt.txt
```

Template: [references/extraction-prompt.md](references/extraction-prompt.md).
Review colour (question, eligibility, overview, `extraction.extra_fields`) is
injected from PROTOCOL.md — do not reuse project-local corpus-engine prompts.

**Validate:**

```bash
python skills/literature-review/scripts/validate_extraction.py path/to/card.json
```

Optional review worksheets: [references/evidence-artifacts.md](references/evidence-artifacts.md).

For each paper:

1. verify identity using DOI or another stable identifier
2. render the extraction prompt from the locked PROTOCOL.md
3. write a JSON paper card that validates against the v1 schema
4. put review-specific fields only in `protocol_extra` keys declared by PROTOCOL
5. attach page, section, table, or figure locations when practical
6. distinguish author-reported findings from reviewer inference
7. record uncertainty, caveats, and missing information
8. save the extraction before writing synthesis prose

Do not use abstract-only extraction as a substitute for full-text extraction.
Abstract extraction may be stored as a separate preliminary layer.

### `synthesise`

Build synthesis from verified extraction records. Organise by question, theme,
context, method, agreement, disagreement, evidence strength, limitations, and gaps.

Use a synthesis matrix rather than paper-by-paper summaries. Distinguish:

```text
reported evidence
cross-study pattern
reviewer inference
open uncertainty
```

Do not claim that no evidence exists when the search was limited. Prefer:

> The reviewed search identified no directly relevant studies within the stated scope.

### `citation-check`

For each manuscript claim:

1. identify the exact cited source
2. open the relevant full text
3. locate the supporting passage, result, table, or figure
4. classify it as `supported`, `partially-supported`, `unsupported`, or
   `source-unavailable`
5. explain any mismatch
6. propose narrower wording or a better source when needed

A paper being topically related is not enough. It must support the specific claim.

### `handoff`

Summarise:

- review purpose and mode
- current protocol or scope
- sources searched and dates
- corpus counts by status
- full-text access gaps
- completed extractions
- synthesis state
- unresolved decisions
- exact next action
- files or collections to read first

When the review is part of a larger project, hand this summary to
`research-project-ops` for project-status updates.

## Artifact policy

Use the minimum artifact set that fits the review.

### Preliminary review

```text
literature/
├── REVIEW.md
├── papers.jsonl or core-papers.csv
├── synthesis-matrix.csv
└── references.bib
```

### Formal or larger review

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

Equivalent existing files are acceptable. Do not create duplicate sources of truth.
See [references/evidence-artifacts.md](references/evidence-artifacts.md).

## Scientific integrity rules

- Do not use search snippets as scientific evidence.
- Do not present abstract-only details as full-text verified.
- Do not invent sample sizes, methods, effect estimates, limitations, or quotations.
- Do not cite a review as though it were the primary study unless explicit.
- Mark preprints, reports, and non-peer-reviewed sources clearly.
- Preserve conflicting and null findings.
- Keep discovery source and access status separate from evidence strength.
- Do not infer novelty from a single database or quick search.
- Keep exact quotations short and attach their source location.
- Respect access controls, licences, and sensitive material.

## Output contract

After substantive work, report:

```markdown
## Mode
[mode]

## Evidence level
[highest evidence level actually used]

## Artifacts created or updated
- `path`: purpose

## Main findings
- [verified synthesis only]

## Limitations
- [search, access, screening, or evidence limitations]

## Next action
[one highest-value next step]
```

## Internal literature components

- `protocol`
- `discover-papers`
- `find-pdf`
- `zotero`
- `zotseek`
- optional local batch literature engine (when installed)

## Peer skills

- `research-project-ops`
- `analysis-design`
- `manuscript-writing`
