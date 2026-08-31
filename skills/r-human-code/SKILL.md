---
name: r-human-code
description: >-
  Use when writing or refactoring scientific R analysis scripts, when output
  looks over-engineered (helper files, CLI parsing, purrr nests, all-namespaced
  tidyverse), or when the user asks for /r-human-code, humanize R, or deslop R.
metadata:
  version: 1.2.0
---

# /r-human-code — readable R, not agent slop

**Core principle:** One script, read top to bottom — paths → loads → transform →
model/plot → write. Match how a coauthor writes R.

## When to use

- New analysis script or major refactor of `.R` / `.Rmd` / `.qmd`
- Script has `source()` helpers, `parse_cli()`, or one-function wrappers
- All-namespaced tidyverse despite a load block, or bare masked verbs with no load

**When NOT:** repo paths/conventions → `AGENTS.md`. HPC → `dayhoff-slurm`. Maps → `ggplot-maps`.

## Script shape

```r
input_csv <- "..."; out_dir <- "..."
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

library(dplyr); library(readr); library(ggplot2)

dat <- read_csv(input_csv, show_col_types = FALSE) |>
  filter(!is.na(n_months), n_months >= 1)

write_csv(dat, file.path(out_dir, "out.csv"))
```

| Slot | Rule |
|------|------|
| Paths | Plain variables at top — no `commandArgs()` / `optparse` |
| Loads | One block after paths; `library()` for packages used throughout |
| Body | Linear; no `source()` / `lib_*.R`; no fn used once |
| Split | Only for separate deliverables |

Use `|>` (or `%>%` if file already does). Prefer tidyverse; `data.table` only for large I/O.

## Packages: load default, namespace exceptions

`library()` + bare verbs is normal when the load block is visible.

**Bare call** — package in load block, name unambiguous.

**`pkg::fun()`** — ANY true:

| Predicate | Example |
|-----------|---------|
| Not in load block | `ncdf4::nc_open()`, `glmmTMB::glmmTMB()` |
| Single call only | `janitor::clean_names(dat)` |
| Masked, wrong semantics | `stats::filter()`, `base::union()` |
| Source unclear | `terra::extract()` without `library(terra)` |

Watch: `filter`, `select`, `rename`, `lag`, `intersect`, `union`, `setdiff`, `count`, `first`, `last`.

**Editing:** match file's existing load/namespace style.

## Built-ins over wrappers

| Need | Use |
|------|-----|
| Clean names (once) | `janitor::clean_names()` |
| Standardize | `scale()` / `mutate(across(...))` |
| Drop NAs | `drop_na()` |
| Reshape | `pivot_longer()` / `pivot_wider()` |

Base R bare: `mean()`, `c()`, `file.path()`, `for`, `if`. Local fn OK only for
domain rules used repeatedly (taxon lookup, `theme_pub`).

## Common mistakes

| Symptom | Fix |
|---------|-----|
| `dplyr::filter()` with tidyverse loaded | Bare after `library()` |
| Bare `filter()`, no load | `library(dplyr)` or `stats::filter()` |
| `library(ncdf4)` for one open | `ncdf4::nc_open()` |
| `source("lib_*.R")`, narrating `# filter rows` | Inline; delete comment |
| `purrr`+`nest` for taxon loop | `for` |

## Rationalizations

| Excuse | Reality |
|--------|---------|
| "Namespaces always clearer" | Humans load dplyr, call `filter()` |
| "Masking makes library() unsafe" | Qualify the rare conflict only |
| "Helper keeps it clean" | One-off helpers force hunting |
| "CLI makes it reusable" | Plain vars; SLURM wrapper for HPC |

## Companions

`r-editor-setup` · `ggplot-maps` · `aic-model-selection` · `figure-design` ·
`dayhoff-slurm` · `rules/r-human-code.mdc`

Not: `r-style-guide`, `tidyverse-patterns`, `r-tidyverse-style`.
