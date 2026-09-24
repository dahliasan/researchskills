---
name: r-human-code
description: >-
  Use when writing, refactoring, or reviewing scientific R analysis code, especially
  when generated code is over-engineered, too CLI-like, over-factored, branch-heavy,
  hard to inspect interactively, or unlike code a human R researcher would maintain.
metadata:
  version: "2.3.4"
---

# Coauthor R

Write R for the scientist who reads it next.

Scientific R is often both a program and a working analysis document. Preserve a
human's ability to open a script, run meaningful sections, inspect intermediate
objects, and still execute the complete analysis cleanly in a fresh session.

## Design language

- **Reveal intent.** Names and top-level structure expose the analysis rather than the
  mechanics.
- **Do one thing.** A function or section has one coherent analytical responsibility.
- **One level of abstraction.** Do not casually mix scientific decisions with file
  plumbing, plotting, export mechanics, or execution infrastructure.
- **Extract concepts, not chunks.** Functions should name meaningful operations,
  remove real duplication, isolate consequential logic, or simplify the caller.
- **Keep decisions visible.** Name dense scientific conditions. Inspect repeated or
  deeply nested branches for a missing concept, lookup table, or responsibility.
- **Keep side effects visible.** File writes, plotting, global state, environment
  changes, and by-reference mutation should not be surprising.
- **Comments explain why.** Preserve rationale, units, assumptions, exclusions,
  thresholds, source corrections, and non-obvious choices. Do not narrate syntax.

Read [references/clean-code.md](references/clean-code.md) only when a design choice is
ambiguous.


## Identify the R context

Before auditing structure, identify what kind of R code you are reading. Do not apply
package conventions mechanically to an analysis script.

- **Analysis script** — favour readable top-level stages, visible settings, inspectable
  intermediate objects, and interactive execution. Functions should earn their
  abstraction.
- **Package or helper library** — favour stable function interfaces, explicit inputs and
  outputs, tests for reusable behaviour, and minimal reliance on global state. Top-level
  analysis work usually does not belong here.
- **Pipeline or orchestrator** — keep orchestration readable and move substantial reusable
  computation into functions when that makes dependencies and testing clearer. Preserve
  the pipeline framework's established interface.

If the file legitimately mixes roles, judge each part by its actual responsibility rather
than forcing the whole file into one category.

## Audit before editing

When reviewing existing code, audit first and edit second. Do not refactor merely
because another style is possible. The burden of proof is on the refactor.

Classify findings as:

- **PASS** — clear, correct, and maintainable enough; no change needed.
- **REVIEW** — a plausible smell or trade-off that requires judgement; explain the
  concern before changing it.
- **FAIL** — an objective problem such as a parse error, deterministic checker failure,
  broken behaviour, or violated project interface. Fix it.

Change code only when there is a demonstrated reason, such as a deterministic failure,
clear readability or maintenance problem, harmful duplication, mixed responsibilities,
excessive or opaque branching, hidden state, or an explicitly requested structural
change. Prefer the smallest change that resolves the identified issue. Do not perform
adjacent cleanup unless it is required for that fix.

## Script and execution model

Prefer a readable top-level analysis with packages, visible settings, substantive
stages, and outputs in execution order. Use `# Section name ----` only for real stages.
Preserve established project headers; do not invent metadata bureaucracy for style.

Treat interactive readability and whole-script reproducibility as compatible:

- ordinary analysis settings are plain assignments near the top;
- researchers can run meaningful sections and inspect intermediate objects;
- the complete file should run in a fresh project session when practical;
- `Rscript script.R` does **not** imply a CLI.

Prefer the simplest interface first: keep settings as plain assignments near the top of
the script when that is enough for collaborators. Add a human-editable configuration
file only when a repeatable set of choices has outgrown that simple interface; read
[references/configuration.md](references/configuration.md) before designing it.

Use no command-line interface by default. Add `docopt` only when a documented Bash,
HPC, or pipeline caller genuinely needs one. Otherwise, collaborators edit top-level
settings, or an established configuration, and source the analysis. Add `main()` only
when an existing interface requires it.

When `docopt` is needed, expose one argument that selects the configuration file rather
than duplicating every setting as a flag.

During audit, treat command-line interfaces as follows:

- **PASS** when a documented Bash, HPC, or pipeline caller uses `docopt` to select a
  configuration file;
- **REVIEW** when `commandArgs()` is used, or when a CLI exposes ordinary analysis
  settings that collaborators could edit in the configuration;
- never remove an existing interface automatically without checking callers and
  preserving it.

A script can still run non-interactively with `Rscript script.R` while keeping analysis
settings as ordinary assignments. Non-interactive execution does not itself justify a
CLI.

## Functions

Keep simple transformations inline. Extract when at least one is true:

- logic is genuinely repeated;
- the block represents a coherent analytical operation with a clear name;
- extraction keeps the caller at one level of abstraction;
- the logic is consequential enough to verify independently;
- the operation stays the same while inputs vary.

Line count alone does not qualify. Do not wrap ordinary package calls or one-off
expressions merely to appear modular. Use verb-based domain names, explicit inputs, stable outputs, and unsurprising side
effects. Prefer R's implicit final return for ordinary functions. Use explicit `return()`
mainly for early exits or when it materially improves control-flow clarity.

## Conditions and iteration

`if` is not a smell by itself. Prefer conditions whose scientific meaning is obvious.
Name dense predicates rather than forcing the reader to decode Boolean mechanics.
Repeated category branches may belong in data, a lookup table, or a dedicated
function; do not introduce S3/R6 solely to eliminate an `if`. When nesting makes a
function hard to follow, consider an early return or guard clause to flatten the control
flow. Do not introduce early returns mechanically when the existing branch is clearer.

Use `for` when it clearly expresses I/O, skipping, resuming, mutation, or uneven work.
Use `map` for homogeneous transformations when it is clearer. Flatten nested mapping
when a loop exposes control flow better.

## Scientific behaviour

Preserve raw inputs, types, missing-value semantics, identifiers, units, seeds,
thresholds, exclusions, and statistical assumptions. Do not change scientific
meaning while performing style cleanup.

### Error handling: let R fail

**Do not add error handling that R already provides.** Missing files, bad paths,
empty filters that leave nothing to plot, and missing columns already stop with a
traceback. Extra `stopifnot()`, `stop()`, `tryCatch()`, or empty-data guards are
noise unless they earn their keep.

**Default:** call the reader or plotter and let failure surface.

| Smell | Prefer |
|---|---|
| `stopifnot(file.exists(path))` then `st_read(path)` / `read_csv(path)` | Just read; missing path fails in the reader |
| `if (!file.exists(path)) stop(...)` before I/O | Just read |
| `if (!nrow(x)) stop("empty")` after a filter you expect to keep rows | Let the next step fail or plot nothing |
| `if (nrow(x) > 0) geom_sf(data = x)` for required layers | Plot; empty or missing data fails or draws nothing |
| `if ("col" %in% names(d))` for columns the script requires | Use `d$col`; missing column errors |
| Blanket `tryCatch` / purrr `safely` / `possibly` around ordinary steps | Let the error stop the script |

**Add a check only when it earns its keep:**

- a real failure already burned time and still recurs;
- an **expected** gap that should skip (`if (!file.exists(nc)) next`, resume if
  output exists);
- one item in a batch must fail without killing the rest (`try()` on that item,
  log which one, continue).

**Order of preference:** fix the root cause → verify the upstream step by looking
at outputs → skip known gaps → `stop()` only after that miss has happened →
`try()` / `tryCatch` only for per-item batch continuation.

Do not invent prerequisite theatre (`if (n_files < 90) stop(...)`) because an
upstream step was not inspected. Open the folder or log instead.

## Deterministic gate

If the project has `scripts/check_r_code.R`, run:

```bash
Rscript scripts/check_r_code.R
```

Fix deterministic failures. Review complexity warnings rather than mechanically
refactoring to satisfy a number.

If the project does not have the checker, at minimum parse every changed R file and run
known affected entry points in fresh sessions where practical. Use `r-tooling-setup`
when the user wants the project-level checker installed.

## Conditional references

- Read [references/smells.md](references/smells.md) during refactoring or generated-code
  cleanup.
- Read [references/performance.md](references/performance.md) for performance, memory,
  parallelism, iteration strategy, or `data.table` mutation.
- Read [references/environment.md](references/environment.md) for packages, `renv`,
  credentials, or environment setup.
- Read [references/configuration.md](references/configuration.md) when collaborators
  need to change recurring analysis settings, or when connecting a configuration file
  to HPC or shell automation.
- Read [references/sources.md](references/sources.md) when reconciling this skill with
  external style advice.

## Completion gate

Before finishing:

- existing code was audited before refactoring, and every structural change has a
  specific justification;
- PASS findings were left alone unless the user explicitly requested broader cleanup;
- REVIEW findings were not mechanically rewritten solely to satisfy a heuristic;
- the code was judged in the correct context: analysis script, package/helper library,
  or pipeline/orchestrator;
- the analysis reads top to bottom at an appropriate level;
- abstractions earn their existence;
- any CLI or sourced interface touched has its real callers accounted for;
- scientific assumptions did not change accidentally;
- the project checker passes when present;
- relevant outputs or entry points were exercised after structural changes;
- anything that could not be verified is stated explicitly.
