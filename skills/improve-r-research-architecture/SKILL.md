---
name: improve-r-research-architecture
description: >-
  Audit, then incrementally refactor, an existing R research repository so that its
  workflow is clear, reproducible and verifiable. Use when asked to reorganise R
  scripts, improve or refactor an analysis codebase, remove hidden dependencies or
  global state, separate raw and derived data, or decide whether renv, targets,
  testthat or package structure is justified. Pairs with r-human-code for line-level
  readability. Not for building new analyses.
---

# Improve R research architecture

Find real friction in an existing R research project, recommend a few high-leverage
changes, and implement them one at a time **without changing scientific results**.

Method borrowed from Matt Pocock's improve-codebase-architecture: explore actual
friction, prefer deep modules with small interfaces, show concrete before/after
candidates, and let the user choose before redesigning. The emphasis on baselines,
equivalence and scientific invariants is this skill's own. See `references/principles.md`.

Code-level readability (names, function size, comments, error handling) belongs to the
`r-human-code` skill. Use this skill for structure, data flow, provenance and
verification. Apply `r-human-code` findings within the structural change you are making.

## Operating rules

- **Audit before editing.** Default to review mode. Refactor when the user asks to
  implement, or approves a candidate. An explicit request to refactor authorises small
  verified changes within the stated scope.
- **Two kinds of change, never mixed silently.**
  - *Architecture change*: same inputs, same results, better organisation.
  - *Scientific change*: different processing, model, filter, seed, threshold or output.
    Requires separate review and its own commit. If a refactor moves a number, stop and
    diagnose; do not call it "just refactoring".
- **Raw data is immutable.** Never modify, delete, rename or overwrite source data. Derived
  data must be distinguishable from raw data and regenerable from it.
- **Use project conventions first.** Read `README*`, `AGENTS.md`, `CLAUDE.md`, the
  `.Rproj`, existing headers and comments, any ADRs. Do not impose a folder tree.
- **Smallest architecture that solves the observed friction.** No `targets`, `renv`,
  testthat, package structure or new directory without a concrete reason (see §3).
- **Never claim reproducibility or equivalence that was not checked.** Report what was
  run and what was not.
- **Protect the working tree.** Check `git status` first. Do not overwrite uncommitted
  work or run destructive Git commands. Commit or push only when asked.

## Judge findings by purpose and consequence

Before a finding is reported as a problem, answer three questions. Write the answers down.

1. **What is this code for?** Name the purpose the code serves now: a result, a
   workflow step, a check, a record, a convenience for a collaborator.
2. **What would go wrong without it, and how likely is that?** Name the failure, not
   the discomfort. "Results change silently" is a consequence. "It looks old" is not.
3. **What is the root cause?** A symptom (a stale path, a long function, a duplicated
   block) often traces back to a process: a rename that missed a reference, a variant
   kept alive after its purpose ended. Fix the cause, or say that the cause is outside
   this change.

Then classify by consequence, not by how it looks:

- **Consequential**: it changes a result, breaks a documented workflow, or stops a
  current run. Fix it, or raise it first if the fix changes science.
- **Maintenance**: it makes the next change harder or riskier, but nothing is broken.
  Record it. Fix it when the work touches that code anyway.
- **Cosmetic or historical**: style, naming, a check whose purpose has been met, a
  leftover that nothing reads. Leave it, or remove it only if removal is the simplest
  way to tidy the area you are already changing.

Calibration rules:

- A check whose baseline no longer exists is a **maintenance** note, not a failure,
  unless the check guards a current result. Ask what the check was for before deciding.
- Do not raise the severity of a finding to justify a change. If nothing is broken,
  say so.
- Do not treat a long function, a duplicated block, or an old file as a problem by
  default. Ask whether it causes a real cost (a bug that hides, a change that cannot be
  made safely, a result that cannot be reproduced).
- **No change is a valid outcome.** Report "nothing needs changing here" when true.
- Do not recommend next steps to fill a list. Recommend only what pays off, and say
  "nothing urgent" when that is the honest answer.

## 1. Explore

1. Read the project's entry points and documentation. Do not create missing files.
2. Prioritise actively changed paths: `git log --oneline -30` and
   `git log --name-only --format='' -30`. Widen if history is thin.
3. Trace one representative workflow from raw input through cleaning and modelling to a
   final figure or table. Record the real dependency order and every side effect.
4. Record a **baseline** before touching anything:
   - commit hash and `git status`;
   - R version, and whether `renv.lock` matches the installed packages;
   - the entry commands and the order they actually need;
   - checksums or `identical()`-ready copies of key outputs (fits, bootstrap samples,
     prepared datasets, tables, figures);
   - random seeds and where they are set;
   - which inputs are raw, which are derived, and which are external.
   If R or the data is unavailable, say so and limit the claims accordingly.

### Friction to look for

Look for proven problems, not aesthetic ones:

- steps that only run in a particular order, or depend on objects left in the session;
- `setwd()`, `attach()`, `assign()`, `<<-`, `options()` changes, `.RData` loading;
- cleaning or join rules repeated across scripts and drifting apart;
- hard-coded absolute paths, or external data with no documented location;
- one script doing ingestion, cleaning, fitting, diagnostics and publication figures,
  so one step cannot be rerun alone;
- derived files written into the raw-data folder;
- variant pipelines (tags, versions, sensitivity runs) duplicated as separate functions
  when one parameter would do, and variants kept alive in the main path;
- wrappers that only forward calls. Apply the **deletion test**: removing the wrapper
  should concentrate complexity, not just move it;
- randomness without a recorded seed; outputs overwritten with no record of their inputs;
- expensive stages that rerun unnecessarily;
- scripts that were executed but never checked in a fresh session.

## 2. Recommend 2–5 candidates

Each candidate must cite specific files and call sites, and state:

- **Current friction**: the observable symptom and what it costs (reproducibility,
  maintenance, correctness, run time).
- **Proposed change**: what moves, what is simplified, what the new interface is.
- **Before / after**: a short text diagram of the workflow (or a self-contained HTML
  report if the environment supports it; never require a CDN to read it).
- **Scientific invariants**: what must not change (row counts, IDs, factor levels, joins,
  units, ordering, CRS, time zones, seeds, thresholds, model formulas, figure content).
- **Verification**: the equivalence test that will be used (see §4).
- **Cost and risk**: effort, run time, disruption, whether the baseline is reproducible.
- **Strength**: `Strong`, `Worth exploring` or `Speculative`, with the evidence.

Rank by benefit for code that changes often, by how well it isolates dependencies, and
by how feasible verification is. Recommend one to start with. If nothing is consequential,
say so and recommend no change. In review-only mode, stop
here and let the user choose.

## 3. Choose the smallest effective structure

Options, not orthodoxy:

- **`.Rproj` and project-relative paths.** Use `here::here()` or paths relative to the
  project root. Required before anything else is portable.
- **Raw and derived data.** `data/raw/` is read-only. Derived products go to
  `data/processed/` with the stage in the name. Large or sensitive data may live outside
  the repository, with a manifest and access instructions.
- **Folders.** `R/` for reusable functions, `scripts/` for executable steps, `outputs/`
  or `output/` for results, `reports/` for Quarto. Keep names already in use if clear.
  An `R/` folder does not make the project a package.
- **`renv`** when package drift harms collaboration or reproducibility. Snapshot the
  packages the code actually uses, exclude archives and data with `.renvignore`, and do
  not commit the local library.
- **`targets`** only for a real multi-stage, expensive graph where selective rerunning
  saves time. Not for a handful of straightforward scripts.
- **testthat** for stable functions and scientific invariants. A short end-to-end smoke
  run may be enough.
- **Package structure** only for reusable software with a public interface.

## 4. Refactor incrementally (implementation mode)

One coherent change at a time. For each change:

1. **Keep a baseline copy.** Save the old file and the old outputs outside the repo
   before editing. Work in a sandbox copy of the committed code when the real run is
   expensive.
2. **Move, then simplify.** Behaviour-preserving moves first, with callers updated in the
   same change. Then change internals.
3. **Update every reference** in the same change: `source()` calls, paths, job scripts,
   README and methods text, comments, CI.
4. **Check.** Parse every changed R file. Syntax-check every changed shell script. Run the
   affected entry points in a fresh session.
5. **Compare with the baseline** (§5). Inspect differences; do not accept a passing script
   as sufficient.
6. **On a discrepancy**, stop. Diagnose, then fix or revert. Do not move on.
7. Only then commit. Delete legacy entry points, large outputs and logs after consumers
   are confirmed, and say what was deleted.

## 5. Verification: equivalence appropriate to the result

| Output | Check |
|---|---|
| Stored R objects (lists, tibbles, fits) | `identical()`, including attributes. Watch `NULL` versus `character(0)` for empty attributes |
| CSV tables | `cmp` or byte comparison against the stored file |
| Derived datasets rebuilt from raw data | byte comparison, or `identical()` after reading |
| Fitted model coefficients | agreed tolerance, documented, plus identical IDs and term names |
| Stochastic steps | the same seed on both sides; identical output, or a distributional summary when the algorithm changed |
| Figures | rasterise and compare pixels, or inspect side by side. Set seeds for jitter first |
| Spatial or time data | CRS, geometry count, extent, time zone, aggregation window |

Use a **reduced-size run** (for example, fewer bootstraps) to test that a whole pipeline
is wired correctly. Say plainly that the numbers from a reduced run cannot be compared
with the full results. Compare full results only against the stored full-size outputs.

Compare **old function against new function on the same inputs** before replacing the
old one. A small set of representative cases (different taxa, with and without random
effects, with and without a predictor list) is usually enough for a model-fitting change.

## Lessons from practice

These came up in real refactors and are worth checking for every project:

- **Superassignment hides state.** `<<-` inside a `map` can quietly collect results.
  Compute such results in a pure helper, and attach them explicitly.
- **Empty values differ.** `NULL` removes an attribute, `character(0)` sets one. Make the
  empty case match the old code exactly before comparing.
- **Line-level regex edits.** Never use multiline-spanning regex flags for line
  replacements. A `.*` with the dotall flag can delete the rest of the file. Check the
  result before you write it.
- **Shell quoting.** Writing R code inside nested `ssh` and shell quotes fails in
  confusing ways. Write the script to a file and run that file.
- **Rebuilt versus original.** Byte equality of rebuilt derived data is strong evidence
  that a cleaning step is unchanged. Store the old version before rebuilding.
- **Lockfiles on compute nodes.** `renv::snapshot()` fails if a package in the code is
  not installed. Packages that need compilation can fail on nodes without a compiler.
  Record that limit, and do not claim the lockfile restores cleanly unless it was tested.
- **Archived code** should be excluded from `renv` scanning and from active checks.
- **Deleting logs and outputs** needs a look first: count them, date them, check what
  reads them. Delete with a stated reason.

## 6. Deliver

1. **What changed**, with paths and the reason for each change.
2. **Before / after** workflow, and the entry commands.
3. **Verification evidence**: commands run, comparisons made, outcomes, tolerances.
4. **What was not verified** and why (for example, slow model fits, missing compiler).
5. **Remaining risks** and one next high-leverage step.

If review only: the ranked candidates and the recommended starting point. Keep the user in
control of substantial structural changes.

## Completion gate

Before finishing:

- the code was audited before any change, and every structural change has a justification
  tied to purpose and consequence (see "Judge findings by purpose and consequence");
- findings were classified as consequential, maintenance or cosmetic, and no
  cosmetic or historical item was presented as a failure;
- PASS findings were left alone unless broader cleanup was requested;
- architecture and scientific changes were kept separate;
- raw data was not modified, and derived data is distinguishable from it;
- every reference to a moved file or renamed function was updated;
- the changed files parse, and any changed shell scripts pass a syntax check;
- stored outputs were compared with the baseline, and the result is reported;
- anything not verified is stated explicitly.

## Conditional references

- `references/principles.md` for the sources and the boundary between published guidance
  and this skill's judgement.
- `r-human-code` for line-level readability, error handling and function extraction.
