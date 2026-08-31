---
name: r-human-code
description: >-
  Human-readable R analysis scripts — linear top-to-bottom flow, pkg::fun()
  namespacing (no library() masking), no CLI parsing, no one-off helpers or AI
  slop. Use when writing or refactoring scientific R scripts, or when the user
  asks for /r-human-code, "humanize R", or "deslop R". Complements
  r-editor-setup (environment), ggplot-maps (maps), dayhoff-slurm (HPC jobs).
metadata:
  version: 1.0.0
---

# /r-human-code — readable R, not agent slop

Write R a coauthor can read by scrolling down once. One script per job where
possible. Inspired by anti-slop hygiene (no speculative helpers, no narrating
comments) — adapted for R analysis, not Python web apps.

## Shape

1. **One script.** Paths and constants at the top, then load → transform →
   model/plot → write. Split only when outputs are genuinely separate
   deliverables.
2. **Linear.** No indirection — the reader should not hunt for helpers in other
   files.
3. **No CLI in the script.** No `commandArgs()`, `optparse`, or `parse_cli()`.
   Set dataset tag, paths, and options as plain variables at the top (or read
   env vars once at the top). SLURM wrappers live in a separate `.sh` file — see
   `dayhoff-slurm`.
4. **No custom functions** unless the same non-trivial chunk repeats in that
   script. A named list for domain lookup (taxon → predictors) or a `theme_pub`
   used several times is fine.

## Namespacing — always `pkg::fun()`

Call non-base R functions with an explicit namespace. Do **not** `library(dplyr)`
then bare `filter()` — masks are opaque and look like agent slop.

| Do | Don't |
|----|-------|
| `dplyr::filter(dat, !is.na(x))` | `library(dplyr); filter(dat, …)` |
| `readr::read_csv(path, show_col_types = FALSE)` | `library(readr); read_csv(…)` |
| `ggplot2::ggplot(dat, ggplot2::aes(x, y))` | `library(ggplot2); ggplot(…)` |
| `trip::speedfilter(…)` | `library(trip); speedfilter(…)` |

**Base R stays bare:** `mean()`, `c()`, `file.path()`, `list()`, `for`, `if`.

**Legacy scripts:** if a file already uses `library()` consistently, match that
file when editing — do not half-convert. New scripts default to namespaced calls.

## Preferred packages

| Role | Prefer |
|------|--------|
| Tables | `dplyr`, `tidyr`, `tibble` |
| I/O | `readr` |
| Names | `janitor` |
| Plots | `ggplot2` |
| Strings | `stringr` when needed |
| Models | domain packages (`glmmTMB`, `ncdf4`, …) with tidy prep around them |

Use native `|>` (or `%>%` if the project already does). Prefer tidyverse for
ordinary scripts. Use `data.table` only for large HPC I/O where it clearly wins
— keep that block local and still linear.

## Use built-ins instead of wrappers

| Need | Use |
|------|-----|
| Standardize | `scale()` / `dplyr::mutate(dplyr::across(..., ~ as.numeric(scale(.x))))` |
| Drop incomplete rows | `tidyr::drop_na()` or `stats::complete.cases()` |
| Clean names | `janitor::clean_names()` |
| Reshape | `tidyr::pivot_longer()` / `tidyr::pivot_wider()` |
| Bind | `dplyr::bind_rows()` |
| Formulas | `stats::reformulate()` |
| Smooth on plots | `ggplot2::geom_smooth()` |
| Labels | `dplyr::case_when()` / `base::cut()` |

## When a local function is OK

Only if it encodes **domain rules** or unavoidable repetition:

- Taxon → predictor inclusion table (named list)
- Year windows for monthly raster / netCDF extracts
- A single plot theme reused in one script (`theme_pub`)

Not OK: one-line wrappers around `scale`, `drop_na`, `glmmTMB`, path getters,
or bespoke z-score / complete-case helpers.

## Anti-slop (R-adapted)

Borrowed from code-humanizer / deslop patterns — structural debt, not formatting:

| Pattern | Fix |
|---------|-----|
| `lib_*.R` or `source()` for one-off helpers | Inline or delete |
| `purrr`/`nest` acrobatics when a `for` over taxa is clearer | Use `for` |
| Reimplementing `janitor`, `scale`, `drop_na`, `geom_smooth` | Use the package |
| Pretty-label maps when raw column names are fine | Drop the map |
| Narrating comments (`# filter rows`) | Delete — code should speak |
| `try(..., silent = TRUE)` swallowing real errors | Let it fail or narrow the catch |
| `parse_cli()` / `optparse` in analysis scripts | Plain variables at top |
| Multiple small functions each used once | Inline |

## Sketch

```r
input_csv <- "input/endloc_database_alltaxa_aug2026reextract.csv"
out_dir <- "output/end_locations/location_exports/v2_aug2026reextract"
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

dat <- readr::read_csv(input_csv, show_col_types = FALSE) |>
  dplyr::filter(!is.na(n_months), n_months >= 1)

# ... transform, model, plot ...

readr::write_csv(dat, file.path(out_dir, "endloc_alltaxa.csv"))
```

## Companions

| Need | Skill / rule |
|------|----------------|
| R + editor setup | `r-editor-setup` |
| Map figures | `ggplot-maps` |
| AIC / model choice | `aic-model-selection` |
| Figure design QA | `figure-design` |
| SLURM jobs on ANU Dayhoff | `dayhoff-slurm` |
| Cursor auto-nudge when editing `.R` files | `rules/r-human-code.mdc` via `./scripts/link-cursor-rules.sh` |

Do not use generic `r-style-guide`, `tidyverse-patterns`, or `r-tidyverse-style`
skills for analysis scripts.
