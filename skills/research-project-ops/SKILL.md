---
name: research-project-ops
description: "Use when the user wants to start, scaffold, audit, reorganize, document, hand off, resume, or prepare an empirical research project for analysis or manuscript writing. Also use for requests about research repository structure, PROJECT.md, METHODS.md, DECISIONS.md, STATUS.md, claims, results tables and figures, data provenance, reproducibility, or making a research project AI-agent friendly. This skill manages project artifacts and routes work by project phase; it does not replace domain-specific literature review, statistical analysis, or manuscript-writing skills."
metadata:
  version: 1.0.0
---

# Research Project Operations

You manage the durable artifacts of an empirical research project so a human or AI agent can understand:

1. what the project is trying to answer
2. what has been decided
3. what was actually done
4. which data and outputs are authoritative
5. what is currently complete or blocked
6. what evidence supports each manuscript claim

Your goal is not to create every possible document. Create the smallest set that removes the project's current bottleneck.

## Core principles

- **Inspect before changing.** For an existing project, read the repository before proposing structure.
- **Preserve working systems.** Improve the current layout rather than replacing it without need.
- **One source of truth per fact.** Other files should link to it instead of duplicating it.
- **Separate plan, implementation, decision, and result.**
- **Generate outputs from code where practical.**
- **Never invent missing methods, parameters, results, citations, or provenance.** Mark unknowns as `[TBC]`.
- **Prefer surgical updates.** Do not rewrite unrelated content.
- **Use Git history when available.** Do not create changelog prose that merely duplicates commits.
- **Ask only when a missing fact blocks a scientifically important decision.** Otherwise scaffold with visible placeholders.

## Router

Classify the request into one or more modes.

| Mode | Use when | Main action |
|---|---|---|
| `scaffold` | New or nearly empty project | Create the minimum viable structure and initial artifacts |
| `audit` | Existing project is confusing, incomplete, or hard to resume | Inspect and report gaps, contradictions, orphaned outputs, and bottlenecks |
| `reorganize` | Files exist but structure or naming is inconsistent | Propose a migration map, then move or rewrite files without losing history |
| `update` | New decision, method, dataset, result, or project change occurred | Update only the authoritative artifacts affected |
| `handoff` | Another person or agent needs to continue the work | Refresh current state, next actions, blockers, and source-of-truth links |
| `results-package` | Analyses are producing stable outputs | Create traceable tables, figures, captions, result IDs, and manifests |
| `manuscript-ready` | The project is approaching writing or submission | Check whether Methods and Results can be written from maintained artifacts |
| `closeout` | Project is complete or being archived | Freeze versions, reproduce outputs, document availability, and archive state |

If multiple modes apply, use this order:

```text
audit → reorganize → update → results-package → manuscript-ready → handoff
```

For a new project:

```text
scaffold → update → handoff
```

## Step 1: Inspect project context

For an existing project, inspect as available:

1. repository tree
2. root `README*`, `AGENTS.md`, project plans, protocols, notebooks, and manuscript drafts
3. data documentation and file names
4. configuration and environment files
5. code execution order
6. generated tables, figures, reports, and models
7. Git history, issues, and recent pull requests
8. current references or citation library

Do not infer that a file is authoritative because its name contains `final`.

Identify:

- current research question and objectives
- current phase
- active data version
- implemented pipeline
- unresolved methodological choices
- latest valid outputs
- manuscript status
- contradictions between prose, code, config, and outputs

## Step 2: Choose the minimum artifact set

Use the artifact contracts in [references/artifact-contracts.md](references/artifact-contracts.md).

### Base artifacts

Create only those needed now:

```text
README.md
PROJECT.md
STATUS.md
METHODS.md
DECISIONS.md
AGENTS.md
references.bib

data/README.md
config/
src/
outputs/
manuscript/
```

### Activation rules

| Artifact | Create when |
|---|---|
| `README.md` | Always, unless an adequate entry point already exists |
| `PROJECT.md` | Research question, scope, objectives, or contribution need a stable home |
| `STATUS.md` | Work spans sessions, people, or agents |
| `METHODS.md` | Study design, processing, or analysis has begun |
| `DECISIONS.md` | At least one consequential choice has alternatives or may be revisited |
| `AGENTS.md` | AI agents will work in the repository |
| `data/README.md` | The project uses or creates data |
| `config/analysis.yml` | Parameters are repeated across scripts or outputs |
| `CLAIMS.md` | Results are stable enough to support named claims |
| results registry | Multiple final statistics must stay consistent across prose, tables, and figures |
| figure/table manifests | There are several outputs or unclear output versions |
| `manuscript/outline.md` | Manuscript planning has begun |

Do not create empty files for hypothetical future needs.

## Step 3: Protect source-of-truth boundaries

Use this hierarchy unless the project already has a better documented system:

| Question | Authoritative source |
|---|---|
| Why does the project exist? | `PROJECT.md` |
| What is the current research question? | `PROJECT.md` |
| What is the project state now? | `STATUS.md` |
| What was planned and implemented? | `METHODS.md` |
| Why was a consequential choice made? | `DECISIONS.md` |
| What parameter values drive the pipeline? | `config/analysis.yml` or equivalent |
| Where did data come from and what do variables mean? | `data/README.md` and machine-readable metadata |
| What operations were actually implemented? | code and workflow definitions |
| Which run produced an output? | run manifest |
| Which numbers are reportable? | results registry or generated result tables |
| What supports a manuscript claim? | `CLAIMS.md` or claim-evidence map |
| What prose is current? | manuscript source files |

When sources conflict:

1. report the conflict
2. identify which source is newer and which is executable
3. do not silently overwrite scientific intent with code behavior
4. resolve through evidence, history, or a visible `[TBC]`

## Step 4: Execute by mode

### Mode: `scaffold`

1. Determine project type:
   - observational
   - experimental
   - computational/modeling
   - evidence synthesis
   - mixed
2. Create the lean directory structure.
3. Draft artifacts from existing user context or repository evidence.
4. Insert `[TBC]` only for material unknowns.
5. Add a short first-action checklist to `STATUS.md`.
6. Ensure `AGENTS.md` points to authoritative files rather than duplicating them.

Default scaffold:

```text
project/
├── README.md
├── PROJECT.md
├── STATUS.md
├── METHODS.md
├── DECISIONS.md
├── AGENTS.md
├── references.bib
├── config/
├── data/
│   ├── README.md
│   ├── raw/
│   ├── interim/
│   └── processed/
├── src/
├── outputs/
│   ├── checks/
│   ├── tables/
│   ├── figures/
│   └── models/
└── manuscript/
```

Remove directories that do not apply.

### Mode: `audit`

Produce a concise audit with:

1. **Current state**
2. **What is working**
3. **Critical gaps**
4. **Contradictions**
5. **Manuscript bottlenecks**
6. **Recommended minimal changes**
7. **Files to create, merge, retain, move, or archive**

Classify findings:

- `BLOCKER`: prevents trustworthy analysis or writing
- `HIGH`: likely to cause rework or inconsistency
- `MEDIUM`: reduces clarity or handoff quality
- `LOW`: housekeeping

Do not reorganize during an audit unless explicitly asked.

### Mode: `reorganize`

1. Audit first.
2. Prepare a migration table:

| Current path | Proposed path | Action | Reason | Risk |
|---|---|---|---|---|

3. Preserve Git history where tools allow.
4. Avoid renaming files referenced by code without updating references.
5. Do not move raw data into version control when it should remain external.
6. Add redirects or notes for legacy paths when collaborators may rely on them.
7. Update `README.md`, `AGENTS.md`, and workflow paths.
8. Validate that scripts and links still resolve.

### Mode: `update`

Route the new information to the authoritative artifact.

| New information | Update |
|---|---|
| Research question or scope changed | `PROJECT.md`, then `STATUS.md`; add decision if consequential |
| Method planned or implemented | `METHODS.md` |
| Reason for choosing or changing a method | `DECISIONS.md` |
| Parameter value changed | config plus `METHODS.md`; add decision if consequential |
| New dataset or data version | `data/README.md`, provenance metadata, run config |
| New result | generated result table or registry; then `CLAIMS.md` if stable |
| New figure or table | source data, generating code, export, caption, manifest |
| Work completed or blocked | `STATUS.md` |
| Writing progress | manuscript files and `STATUS.md` |
| Deviation from plan | `METHODS.md` current state plus `DECISIONS.md` history |

After an update, check downstream consistency. Example: a changed eligibility threshold may affect config, methods, QC counts, results, figures, and manuscript text.

### Mode: `handoff`

Update `STATUS.md` to include:

- last updated date
- current phase
- current objective
- completed
- in progress
- next actions in order
- blockers
- known uncertainties
- authoritative inputs
- latest valid outputs
- relevant branch or commit
- exact files to read first

A handoff should let the next agent begin without reading the full repository.

### Mode: `results-package`

For each manuscript-level result:

1. assign a stable result ID
2. save the underlying result data
3. record the generating script and configuration
4. identify the objective or hypothesis it answers
5. record estimate, uncertainty, population, units, and comparison
6. link related figure or table
7. state the interpretation boundary

For every figure or table retain:

```text
purpose
claim/result IDs
source data
generating code
final export
caption
status: draft | candidate | final
```

Do not store the only copy of a result inside an image or manuscript sentence.

### Mode: `manuscript-ready`

Evaluate readiness section by section.

#### Introduction ready when

- research problem, gap, question, and contribution are stable
- core references are traceable
- scope matches the study actually conducted

#### Methods ready when

- data provenance is known
- inclusion and exclusion rules are documented
- processing order is documented
- variables and units are defined
- analysis and validation are documented
- final parameters and software versions are recoverable
- deviations are visible
- Methods agree with implemented code

#### Results ready when

- final analytical sample is traceable
- primary outputs are generated
- every reported number has a source
- figures and tables each have one clear purpose
- Results claims avoid interpretation beyond the evidence

#### Discussion ready when

- key findings are identified without duplicating Results
- each interpretation links to results and literature
- alternatives and limitations are recorded
- broader implications stay within the evidence boundary

Return:

- `READY`
- `READY WITH MINOR GAPS`
- `NOT READY`

List only the gaps that block or materially slow writing.

### Mode: `closeout`

1. run or document a clean reproduction
2. freeze data, code, config, and environment versions
3. record the final run manifest
4. confirm manuscript numbers match generated results
5. add data and code availability statements
6. archive superseded outputs
7. update status to complete
8. document unresolved limitations

## Artifact update rules

### `METHODS.md` and `DECISIONS.md`

They overlap only at consequential choices.

- `METHODS.md`: current factual method
- `DECISIONS.md`: context, alternatives, reason, consequences, history

Example:

`METHODS.md`:
> Presences were aggregated to monthly 1° grid cells.

`DECISIONS.md`:
> D-004 records why monthly 1° cells were selected over native and finer resolutions.

### Planned versus actual

Use explicit labels:

```text
Status: planned
Status: implemented
Status: validated
Status: superseded
```

Never write a planned method as though it was completed.

### Rules versus counts

- Methods hold rules.
- Results and QC outputs hold resulting counts.

### Raw versus generated

- Raw data are immutable.
- Interim data may be regenerated.
- Processed data must link to code and source versions.
- Outputs must be reproducible or clearly marked manual.

## AI safety and scientific integrity

- Do not infer novelty from a quick search.
- Do not claim an exhaustive review unless the search supports it.
- Do not change hypotheses to fit results without recording the change.
- Do not hide failed analyses or exclusions that affect interpretation.
- Do not convert exploratory analysis into confirmatory analysis without labeling it.
- Do not manufacture citations, sample sizes, parameter values, effect sizes, or rationales.
- Do not delete superseded scientific decisions when they explain project history.
- Do not expose restricted or sensitive data in repository documentation.

## Output contract

After performing work, report:

```markdown
## Mode
[mode or sequence]

## Changes made
- `path`: concise change

## Scientific issues found
- [only material issues]

## Sources of truth
- [artifact → responsibility]

## Next action
[one highest-value next step]
```

For an audit, include the severity classification.

For a reorganization, include the migration map.

For file changes, prefer a branch and pull request when operating on a shared repository.

## Related skills

Use separate specialist skills where available:

- literature search and evidence synthesis
- statistical analysis
- data visualization
- manuscript writing and editing
- citation verification
- reporting-guideline checks

This skill coordinates artifacts and project state. It should route to specialist skills rather than absorb all scientific work.
