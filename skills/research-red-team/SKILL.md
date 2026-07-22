---
name: research-red-team
description: >-
  Critically stress-test an entire research project from premise through data,
  analysis, results, interpretation, figures, manuscript claims, and
  reproducibility. Use for reviewer-2 reviews, pre-mortems, replication audits,
  failure-mode analysis, or when the user wants an opposing or sceptical lens.
  Inspects primary project evidence where available and records actionable,
  evidence-linked challenges without taking ownership of project decisions.
metadata:
  version: 0.1.0
---

# Research Red Team

Critically examine the research argument as a whole. Do not merely edit the
manuscript or generate generic reviewer comments.

The purpose is to find credible ways the project could be wrong, fragile,
incomplete, misleading, irreproducible, or overstated, then convert those
challenges into proportionate actions.

## Core principles

1. **Challenge the project, not the researcher.** Use neutral, specific language.
2. **Inspect evidence before criticising.** Do not manufacture objections from
   generic checklists when the project may already address them.
3. **Separate fact from inference.** State what was inspected, what is missing,
   what is inferred, and how confident the challenge is.
4. **Prefer consequential challenges.** Prioritise issues that could change the
   question, method, result, interpretation, or reproducibility.
5. **Do not take ownership.** This skill identifies and substantiates challenges.
   Peer skills and the researcher decide and implement responses.
6. **Keep valid null outcomes.** A challenge may be marked `not-substantiated`
   when the evidence shows the project already handles it.

## Step 0: Detect the mode

| User need | Mode |
|---|---|
| Challenge the claimed gap, premise, or contribution | `premise` |
| Challenge study design, sampling, controls, or scope of inference | `design` |
| Challenge data processing, modelling, validation, or sensitivity | `analysis` |
| Challenge manuscript claims and interpretation | `claims` |
| Simulate a demanding peer reviewer | `reviewer-2` |
| Ask whether an independent team could reproduce the work | `replication` |
| Identify plausible ways the result could be wrong | `failure-modes` |
| Assume rejection or failure and explain why | `pre-mortem` |
| Inspect the complete project | `full-project` |
| Reassess responses to earlier challenges | `follow-up` |

When the user does not specify a mode, use `full-project` for project-wide
requests and the narrowest applicable mode for targeted requests.

## Step 1: Declare the evidence tier

Use the highest tier available. Never imply a stronger audit than the evidence
supports.

### Tier 1: Documentation review

Available evidence may include:

- project brief, status, methods, decisions, and claims registries
- manuscript drafts and figure plans
- issue and pull-request discussions
- literature search records and references

This tier can identify inconsistencies, unsupported claims, unclear decisions,
and plausible weaknesses. It cannot establish that implementation or data are
correct.

### Tier 2: Evidence audit

Adds:

- code and configuration
- Git history
- generated outputs and logs
- failed and excluded cases
- full-text literature and exact citation evidence

This tier can verify Methods-code agreement, result provenance, citation
support, validation implementation, and whether important failures are hidden.

### Tier 3: Computational stress test

Adds:

- raw or analysis-ready data
- model objects and intermediate artifacts
- the runtime environment, HPC, or cloud outputs
- permission to run bounded recomputations or sensitivity analyses

This tier can independently recompute summaries, test alternatives, inspect
leakage, and run targeted robustness checks.

If access is partial, list the unavailable evidence and continue at the lower
tier.

## Step 2: Inspect sources of truth

Start with project-owned artifacts when present:

```text
PROJECT.md
STATUS.md
METHODS.md
DECISIONS.md
CLAIMS.md
PROTOCOL.md
manuscript drafts
figure storyboard or specifications
result registries
```

Then trace outward to implementation and evidence:

```text
research question
↔ project decisions
↔ Methods
↔ code and configuration
↔ executed outputs and logs
↔ figures and tables
↔ manuscript claims
↔ verified literature
```

Do not assume any one file is authoritative merely because it is labelled as a
source of truth. Report conflicts between artifacts.

## Step 3: Use the truth hierarchy

Use this default hierarchy when evidence conflicts:

1. authoritative raw or source data
2. executed outputs and run logs
3. code and configuration used for that run
4. versioned generated summaries
5. verified full-text literature
6. project decisions and documentation
7. manuscript prose
8. agent memory, convention, or assumptions

This hierarchy is contextual, not mechanical. For example, code shows what was
implemented, while logs and outputs show what actually ran. Preserve conflicts
instead of silently selecting the convenient source.

## Step 4: Build the argument map

Before challenging details, reconstruct the project argument:

```text
problem
→ knowledge gap
→ research question or objective
→ study design
→ data and processing
→ analysis
→ result claims
→ interpretation
→ contribution
```

Record missing or broken links. A technically correct analysis may still fail
if it does not answer the stated question.

## Step 5: Run the challenge lenses

### Premise and contribution

Check whether:

- the claimed gap is supported by a sufficiently broad and current search
- the question is scientifically meaningful, specific, and answerable
- key concepts and scales are defined
- the contribution is distinct from prior work
- novelty language is stronger than the search evidence allows
- the project solves the stated problem rather than a nearby easier problem

Use `literature-review` for deeper novelty or citation investigation.

### Study design and sampling

Check whether:

- the design can identify the intended effect or pattern
- comparison groups, baselines, controls, or counterfactuals are appropriate
- sampling creates selection bias, pseudoreplication, leakage, or confounding
- spatial, temporal, taxonomic, or population coverage matches the inference
- exclusions or failed cases could systematically alter conclusions
- sample size and information content are adequate for the analysis
- post hoc decisions are presented as if they were pre-specified

Use `analysis-design` when available for redesign or formal methodological work.

### Data and processing

Check whether:

- raw-to-analysis transformations are traceable
- missingness, duplicates, outliers, and exclusions are quantified
- preprocessing decisions encode unacknowledged assumptions
- data quality differs across relevant groups, locations, periods, or sources
- joins, filters, resampling, aggregation, and unit conversions are defensible
- manual interventions are recorded
- dataset versions and external dependencies are identifiable

Prefer direct data inspection over assumptions based on documentation.

### Analysis and validation

Check whether:

- the model or test answers the stated question
- assumptions and diagnostics are examined
- validation matches the intended deployment or inference setting
- folds or partitions are genuinely independent
- leakage is possible through preprocessing, grouping, space, or time
- thresholds and tuning choices are outcome-driven or weakly justified
- uncertainty is propagated and reported
- reasonable alternative specifications would change conclusions
- random processes, software versions, and seeds are controlled
- failed analyses and unstable models are visible

Do not demand every imaginable analysis. Recommend sensitivity tests only when
they can resolve a consequential challenge.

### Results and visual evidence

Check whether:

- manuscript numbers trace to generated evidence
- figures and tables reproduce the reported values
- averages hide important heterogeneity or failure cases
- axes, scales, colour, aggregation, or map choices could exaggerate findings
- uncertainty and sample sizes are visible where needed
- null and contradictory results are retained
- main-text selection creates a distorted view of the complete results
- captions and surrounding prose make the same claim as the visual

Use `figure-design` for detailed visual redesign or figure-quality work.

### Claims and interpretation

Check whether:

- each important claim has the correct evidence type
- causal language exceeds the design
- the Discussion adds interpretation without inventing results
- alternative explanations are considered
- comparisons use genuinely comparable studies
- project-specific findings are not generalised beyond their evidence
- limitations explain consequences for inference
- claims are narrowed when support is partial
- citation full text supports the exact wording rather than the general topic

Use `manuscript-writing` to revise accepted wording changes and
`literature-review` to verify external claims.

### Reproducibility and auditability

Check whether:

- another researcher could locate the authoritative inputs
- Methods, code, configuration, outputs, and manuscript agree
- the executed run and its environment can be identified
- generated artifacts can be reproduced or their provenance verified
- external services, credentials, and unavailable data are documented
- consequential decisions have reasons and dates
- project state distinguishes completed, planned, and hypothetical work

Use `research-project-ops` to record accepted project-level actions and status.

## Step 6: Substantiate each challenge

A challenge is reportable only when it contains:

```text
challenge
why it matters
project evidence inspected
external evidence inspected, if relevant
evidence unavailable
reasoning or inference
severity
confidence
required response
```

Do not inflate generic possibilities into findings. Use one of these finding
states:

- `substantiated`
- `partially-substantiated`
- `plausible-unverified`
- `not-substantiated`
- `resolved`

## Step 7: Assign severity and response

### Severity

| Severity | Meaning |
|---|---|
| `critical` | Could invalidate the central result, ethics, or core inference |
| `high` | Could materially change a major result, method, or conclusion |
| `moderate` | Important weakness that requires analysis, narrowing, or disclosure |
| `low` | Local improvement with limited effect on the scientific argument |
| `not-substantiated` | Evidence does not support the proposed challenge |

### Required response

Every substantiated challenge must recommend one primary response:

- `fix`
- `additional-analysis`
- `sensitivity-test`
- `documentation-change`
- `scope-reduction`
- `claim-narrowing`
- `limitation-disclosure`
- `no-change-with-justification`

Do not create issues or modify scientific decisions unless the user asks.

## Step 8: Write the challenge register

Default artifact:

```text
RED_TEAM.md
```

Use an equivalent existing file rather than creating a duplicate source of
truth.

Recommended summary table:

```markdown
| ID | Area | Challenge | Evidence | State | Severity | Confidence | Response | Status |
|---|---|---|---|---|---|---|---|---|
```

Use stable IDs such as:

```text
RT-PREMISE-001
RT-DESIGN-001
RT-DATA-001
RT-ANALYSIS-001
RT-RESULTS-001
RT-CLAIMS-001
RT-REPRO-001
```

For each high or critical item, add a detailed record:

```markdown
## RT-ANALYSIS-001 — [short title]

**Challenge:**

**Why it matters:**

**Evidence inspected:**

**Evidence unavailable:**

**Assessment:**

**State:** substantiated | partially-substantiated | plausible-unverified |
not-substantiated | resolved

**Severity:** critical | high | moderate | low | not-substantiated

**Confidence:** high | moderate | low

**Required response:**

**Resolution evidence:**
```

Keep speculative lower-severity observations concise.

## Mode-specific outputs

### `reviewer-2`

Write a realistic peer-review report, but retain evidence links and distinguish:

- major concerns
- minor concerns
- questions requiring clarification
- strengths that should be preserved

Do not perform hostile role-play or add objections merely to sound demanding.

### `pre-mortem`

Assume the work was rejected, failed replication, or produced a misleading
conclusion. Identify the smallest set of plausible causes that best explains
that outcome, then inspect whether evidence supports them.

### `failure-modes`

Organise findings by failure mechanism, such as:

- sampling bias
- leakage
- confounding
- unstable preprocessing
- validation mismatch
- hidden heterogeneity
- selective reporting
- unsupported generalisation
- irreproducible execution

### `follow-up`

For each prior challenge:

1. inspect the claimed response
2. verify the new evidence
3. mark `resolved`, `partially-resolved`, or `open`
4. retain the original challenge and resolution history

## Tool contract

The skill is documentation-first and must degrade gracefully. Use available
project tools in this order:

1. **Repository and files:** project artifacts, code, configuration, Git history,
   issues, PRs, and generated reports.
2. **Data and computation:** shell plus suitable readers or runtimes such as
   Python, R, SQL, tabular, raster, or NetCDF tools.
3. **Executed evidence:** logs, pipeline metadata, model objects, intermediate
   outputs, final tables, and figures.
4. **Literature:** scholarly discovery, Zotero/ZotSeek, authorised full-text
   retrieval, and exact passage or table verification.
5. **Authoritative external sources:** official dataset documentation, software
   documentation, standards, and original research papers.

Do not require every tool for every audit. Match tool use to the challenge and
state the resulting evidence tier.

## Safety and scope boundaries

- Do not run destructive, expensive, or full production analyses without
  explicit permission.
- Prefer bounded diagnostic checks and targeted sensitivity analyses.
- Respect restricted, confidential, personal, and licensed data.
- Do not expose secrets or credentials in reports.
- Do not treat clean code as proof of scientific correctness.
- Do not treat a recent output as valid without provenance.
- Do not treat an abstract or search snippet as detailed scientific evidence.
- Do not silently resolve conflicts or change accepted scientific decisions.
- Do not turn every hypothetical concern into a blocker.

## Peer handoffs

`research-red-team` is a peer skill. It reads across the project but does not
own the artifacts it challenges.

| Accepted challenge | Handoff |
|---|---|
| project state, unresolved decision, or dependency | `research-project-ops` |
| literature gap, novelty, or citation verification | `literature-review` |
| design, model, validation, or sensitivity change | `analysis-design`, when available |
| figure or visual-integrity problem | `figure-design` |
| manuscript wording, structure, or reviewer response | `manuscript-writing` |

## Output contract

After an audit, report:

```markdown
## Audit scope
- mode:
- evidence tier:
- artifacts and evidence inspected:
- important evidence unavailable:

## Overall assessment
[Brief assessment of whether the central argument appears robust, fragile, or
not yet assessable.]

## Priority challenges
1. [highest-consequence substantiated challenge]
2. [next challenge]
3. [next challenge]

## Challenges not substantiated
- [important concern checked and ruled out]

## Actions
- [challenge ID] → [required response and owning peer skill]

## Artifact
- `RED_TEAM.md`: created or updated, when applicable
```

Never claim the project is valid merely because no problems were found. State
the limits of the audit and the evidence tier used.
