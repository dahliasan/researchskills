---
name: r-human-code
description: >-
  Use when writing or refactoring scientific R analysis scripts, when output
  looks over-engineered (Sys.getenv paths, helper files, CLI parsing, purrr nests,
  one-off local functions, all-namespaced tidyverse), or when the user asks for
  /r-human-code, humanize R, or deslop R.
metadata:
  version: 1.10.1
---

# /r-human-code — readable R, not agent slop

**Core principle:** One script, read top to bottom — paths → loads → transform →
model/plot → write. Match how a coauthor writes R.

**Trust what you verified.** Humans build pipeline scripts iteratively: run step N,
watch the output, then write step N+1 assuming N worked. Do **not** paper over
unchecked upstream work with speculative `stop()` / count gates / “just in case”
branches. If you need those, you did not finish verifying the previous step.

## Hard rules (check before every edit)

1. **Plain string paths** in step scripts. `animal_dir <- "/path/to/data"`.
   No `Sys.getenv`, no `unset`, no `nzchar(Sys.getenv(...))` unless the file
   is shared `config.R` that already centralises paths for many tags/machines.
2. **No one-off local functions.** Inline the body. Allowed only if the **same
   file** calls it from **≥2 distinct source locations**. A loop body called
   1000 times at runtime is still **one** call site.
3. **No `source()` of helper scripts** for logic used in one pipeline step.
   Exception: shared `R/` modules for path constants and multi-step pipeline
   functions (see Function gate).
4. **No narrating comments** (`# filter rows`). Brief **why** comments are OK
   for non-obvious steps (date formats, file naming, missing-value codes).
5. **No skill/agent/internal refs** in comments.
6. **Tidy inside `for` is fine** — do not extract to a one-off function.
7. **No preemptive error handling.** Do not add `tryCatch`, `try()`, `withCallingHandlers`,
   purrr adverbs (`safely`, `possibly`, `quietly`, `insistently`), or extra `stop()`/`warning()`
   unless there is a concrete reason (see below). R's normal errors are enough for most scripts.
   Agents add this by default — don't.
8. **No premature guards / fake tests.** Don't wrap steps in `if (nrow(d) > 0)`,
   `if ("col" %in% names(d))`, `if (!is.null(x))`, `if (n_files < 90)`, or other
   conditions for failures you have **not** seen in a real run. Soft counts and
   sentinel checks in orchestrators are the same smell: they hide that prepare /
   config / paths were not checked. Fix or verify the upstream step; only add a
   guard after a real failure or for a known expected case (resume,
   missing netCDF month, optional upstream file).
9. **No hypothetical config branches.** Don't add `Sys.getenv` + `if (x != "")` (or `nzchar`) for
   debug limits, subset modes, or alternate methods you haven't run in production. Edit the script
   or the shell for a one-off; delete the branch when the experiment ends.
10. **No defensive scripts as a substitute for babysitting.** If step N was run and the
    outputs look right, step N+1 should assume that and stay simple. Adding gates
    “so the cluster job is safe” without having inspected N is agent slop — go look
    at the files / logs instead.

### Function gate

**Step scripts** (numbered pipeline scripts, one-off exports run via `Rscript`):

| Question | If no → |
|----------|---------|
| Called from ≥2 places in this file? | Inline |
| Shared across scripts? | Only if repo already has that shared file |
| Extracting because loop is long? | Keep loop; use `\|>` inline |

**Shared `R/` modules** (library files under `R/`):
different bar — these replace shell scripts or keep orchestration graphs readable.

| Question | If no → |
|----------|---------|
| Multi-step logic (loop + I/O + summary)? | Inline in caller only if caller stays short |
| Thin one-liner alias? | Inline at call site |
| Called from ≥2 scripts or targets graphs? | Strong keep |
| One call site but ~30+ lines of pipeline work? | **OK in `R/`** — don't bloat the orchestrator |

**Wrong:** `fill_threats_from_nc()` — one call site inside one step script.  
**Wrong:** `sidecar_json_path()` — one-liner path used once; inline `file.path(...)`.  
**Wrong:** `packs_output_dir()` — `file.path(run_dir, "packs")` used once.  
**Wrong:** `Sys.getenv("APR2026_OUT", unset = "output/foo")` in a step script.  
**Wrong:** `tryCatch(fread(f), error = function(e) NULL)` around every file read.  
**Wrong:** `map(files, safely(read_csv))` when any failure should stop the job.  
**Wrong:** `if (nrow(d) > 0) { d <- d |> filter(...) }` on every step — empty data is rare; if it happens, let the pipe fail.  
**Wrong:** `if (n_prepare < 90) stop(...)` in the fit orchestrator when prepare was not inspected — fake test.  
**Right:** `out_dir <- "output/track_duration"` at the top; edit the string.  
**Right:** Confirm prepare outputs, then fit script assumes they exist.  
**Right:** `build_model_packs()` in `R/` — unit loop, serialized read/write, summary table; one orchestrator call but real pipeline step.  
**Right:** `write_metrics_table()` in `R/` — same pattern as a former standalone export script.  
**Right:** Let `fread()` fail; fix the path. `try()` / `safely()` only when one model/species
failing must not stop the rest — prefer plain `try()` over `safely()` for readability.

### Shared path constants and helpers

Many repos keep one file (`R/paths.R`, `config.R`) for paths reused across
orchestration, exports, and shell wrappers. That is **not** the same as sprinkling
`Sys.getenv` overrides through step scripts.

| Kind | When to add | When to inline |
|------|-------------|----------------|
| **`OUTPUT_*` constant** (`OUTPUT_METRICS`, `OUTPUT_MAPS`) | Same workstream path in ≥2 scripts | Used in one file only |
| **Path helper with logic** (`run_label()`, `report_path()`) | Non-trivial derivation (run stamp → folder name) **and** ≥2 call sites | One-liner or one call site |
| **Plain `file.path` in step script** | Default when path is local to one script | — |

**Wrong:** `sidecar_json_path(run)` — `paste0("meta_", run, ".json")` used in one script.  
**Right:** `prepared_data_dir(config)` — used in fit step, prepare script, shell runners.  
**Right:** `file.path(ROOT, OUTPUT_MAPS)` — shared constant, not a one-off function.  
**Right:** Step script top: `out_dir <- "output/track_duration"` when nothing else needs that path.

Step scripts may `source()` the shared path file for `OUTPUT_*` constants; they still
should not grow env-var path overrides (orchestrators set env once if needed).

### Serialized R objects vs tabular exports

| Artifact | Usual format | Why |
|----------|--------------|-----|
| Fitted models, attributed lists | `saveRDS` / `qs2` | Full R object; metadata attrs matter |
| Report / QC / validation tables | CSV / JSON | Human-readable, traceable, diff-friendly |
| Numbers cited in prose | CSV / JSON only | Don't bury reportable values in binary blobs |

Binary serialization is fine for heavy pipeline intermediates on HPC. Don't migrate
to Parquet/CSV for model blobs unless you have a concrete interoperability need.

**Wrong:** Saving evaluation metrics only in RDS/qs2 with no CSV export.  
**Right:** Fit → serialized model file; report → `metrics_by_unit.csv` + summary JSON.

## When to use

- New analysis script or major refactor of `.R` / `.Rmd` / `.qmd`
- Script has `source()` helpers, `parse_cli()`, `Sys.getenv` paths, or one-function wrappers

**When NOT:** repo paths/conventions → `AGENTS.md`. HPC → `dayhoff-slurm`. Maps → `ggplot-maps`.

## Naming: artifacts, not intent

Name folders, scripts, config keys, and pipeline lanes after **what is stored or
produced**, not **why you made it** (paper, dashboard, experiment).

| Intent name (avoid) | Artifact name (prefer) | Why |
|---------------------|------------------------|-----|
| `sample`, `analysis_subset` | `training_data` | Tables that feed modelling |
| `cv` | `validation` | Holdout / cross-validation metric tables |
| vague `models`, `results` | `fit/`, `maps/` (or similar) | Fit artifacts vs spatial outputs |
| `active_retrain`, `current_version` | `run_id` | Stamp on a fit tree (`20260315`) |
| `deploy_version`, `prod_copy` | `frozen_run` | Frozen ops cohort — only if you truly have two lifecycles |
| `manuscript`, `paper1/` | workstream folders + `build_*` | Paper is a consumer, not a path |
| `diagnostics` | `qc` | Pipeline QA artifacts |

**Run IDs:** one stamp per lifecycle. If experimental fit and frozen deploy differ,
use two keys (e.g. `run_id` + `frozen_run`) — don't mirror the same stamp under
`current_version`, `latest_version`, and nested config blocks.

**Pipeline lanes** (fit → report → derived data → render):

```text
pipeline/fit.*          # or _targets.R — heavy compute
pipeline/report.*       # metrics summary JSON/CSV
pipeline/build_data.*   # derived inputs before render
scripts/build_tables.R  # formatted tables
scripts/build_figures.R # figure PDFs
```

Use **`build_data`**, not `build_results`, for the pre-render lane:

| Name | Use when |
|------|----------|
| **`build_data`** | Producing **inputs** to render: metric CSVs, derived rasters, summary tables — things `build_tables` / `build_figures` read. Pairs with `build_*`. |
| **`build_results`** | Avoid as a folder or targets graph name — too vague (figures are also "results") and sounds like the whole paper output. |
| **`results`** | OK in prose ("Results section") or one-off filenames; not for `output/` workstreams or `{targets}` graphs. |

**Orchestration graphs** (e.g. `{targets}` files under `pipeline/`): name by
role (`report`, `build_data`), not by paper or experiment. Keep them separate from
numbered step scripts (`scripts/02_prepare.R`, etc.).

**Orchestrators** (pipeline graph files, shell wrappers) may set env vars once
before `Rscript`; **step scripts** still use plain path strings at the top (see
hard rules). Docs and SLURM job names can say "manuscript regen"; repo paths
cannot.

## Script shape

```r
animal_dir <- "/data/gridded"
out_dir    <- "output/track_duration"
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

library(dplyr); library(readr)

dat <- read_csv(file.path(out_dir, "in.csv"), show_col_types = FALSE) |>
  filter(!is.na(n_months))

write_csv(dat, file.path(out_dir, "out.csv"))
```

| Slot | Rule |
|------|------|
| Paths | Plain strings at top; comment "edit here if paths move" |
| Loads | One block after paths; `library()` for packages used throughout |
| Body | Linear; no one-call-site functions |
| Split | Only for separate deliverables |

Use `|>`. Prefer tidyverse; `data.table` only for large I/O (`fread`/`fwrite`).

## Tidyverse by default

Reach for tidyverse packages when they read clearer than base R — not for purity.

| Task | Prefer | Not |
|------|--------|-----|
| Dates / year-month | `lubridate` (`ym`, `ymd`, `year`, `month`) | `substr` + `grepl` on date strings |
| Reshape / join / filter | `dplyr`, `tidyr` | `aggregate`, nested `[` indexing |
| Strings (when non-trivial) | `stringr` | `grep`/`sub` chains |
| Small/medium CSV I/O | `readr` (`read_csv`, `write_csv`) | `read.csv` |
| Large CSV I/O | `data.table` (`fread`/`fwrite`) then `as.data.frame()` + dplyr | — |

After `fread`, piping with dplyr is fine — speed where it matters (read), readability
where it matters (transform).

## Pipes vs intermediate values

**Default:** pipe with `|>`. A coauthor should read one transform chain top to bottom.

**Save an intermediate** when it genuinely helps:

| Situation | Example |
|-----------|---------|
| Reused downstream | `months <- d \|> distinct(year, month)` then loop over it |
| Heavy step worth inspecting | `d <- fread(...)` before a long mutate chain |
| Loop with side effects | `d` built once, mutated per month inside `for` |
| Pipe too long to scan | Split after a natural stage (load → clean → enrich) |

Do not split every line into a named variable — that is the opposite of readable.

## `for` loops vs `purrr::map`

Both are fine. Pick for **readability first**; efficiency rarely differs unless
the inner work is pure computation at scale (not typical in this repo's I/O-heavy scripts).

**Prefer `for`** when:

- Side effects: `fwrite`, `nc_open`, `message`, `next`/`break`, resume skips
- Imperative steps are the story ("for each species file, …")
- You mutate an object built outside the loop (`d[row_idx, t] <- vals`)
- Early exit or uneven work per iteration

**Prefer `purrr::map` / `map_dfr`** when:

- Homogeneous transform: each element → one output, no side effects
- Result is a new list or stacked tibble (`map_dfr(files, read_csv)`)
- The whole point is "apply this function to each X" with no extra narrative

**Avoid:** `purrr::walk` + one-off anonymous function when a plain `for` with
`message()` reads the same and is easier to debug. Nested `map` inside `map`
is a smell — use a `for` or flatten the logic.

```r
# Readable for this repo: explicit file loop with skip + I/O
for (i in seq_along(species_files)) {
  if (file.exists(out_file)) next
  d <- fread(species_files[i]) |> filter(presence == 1)
  ...
}

# Readable map: stack many similar CSVs with no per-file logic
all <- map_dfr(files, \(f) read_csv(f, show_col_types = FALSE))
```

## Packages: load default, namespace exceptions

`library()` + bare verbs when the load block is visible. Include `lubridate` when
parsing or extracting date parts.

**`pkg::fun()`** when: not loaded, single call, masked name (`stats::filter`), or unclear source (`ncdf4::nc_open`).

## Error handling: fix first, guard sparingly

**Do not add error handling "just in case".** If you haven't hit the failure in real
runs and can't fix the root cause, you probably don't need `tryCatch` yet.

**Default:** let R fail with its normal error. A missing column or bad path already
stops the script with a traceback — that is enough for interactive work and for most
of a SLURM script too. Do not prepend `stopifnot(file.exists(path))` or
`if (!file.exists(path)) stop(...)` before `read_csv` / `st_read` / `rast`; the
reader already fails.

**How humans write these scripts:** run prepare → confirm ~95 inputs exist → write
fit assuming prepare is done. The fit script does not re-prove prepare with
`if (n < 90) stop(...)`. Soft thresholds and duplicate sentinel checks are **fake
tests**: they were not earned by a failure you saw; they compensate for not looking.

Add checks only when they earn their keep:

| When | What | Example |
|------|------|---------|
| **You already burned time on a real miss** | One `stop()` / `next` for that exact miss | Wrong prepare dir once → fix the path; only then a top check if it keeps recurring |
| **Expected partial failure** | Skip or record, don't wrap everything | `if (file.exists(out_file)) next` (resume); `if (!file.exists(nc_path)) next` (gap in threat months) |
| **Per-item failure, job should continue** | `try()` or `tryCatch` on *that* step only | Model won't converge for one species → `NA` + log, fit the rest |
| **Never by default** | Blanket `tryCatch`, count gates (`n >= 90`), `safely` / `possibly` around loops, `stopifnot(file.exists(...))` / `stop()` before `read_*` / `st_read` / `rast` | Hides bugs; papers over unverified upstream steps; readers already fail on missing paths |

**Interactive vs SLURM:** same script. Prefer **verify upstream in the session /
logs** over encoding fear into the next script. A cluster job that fails in 30s
on a bad path is fine — that is R working. Inventing prerequisite theatre because
an agent did not open the prepare folder is not.

**Order of preference:**

1. Fix the root cause (wrong path, bad column name, empty filter)
2. Verify the previous step’s outputs (list files, spot-check a CSV) before writing the next script
3. Skip expected gaps (`next`, `if (!file.exists(...))`)
4. Resume/checkpoint (write per-species files; skip if done)
5. `stop()` only after that miss has actually happened (or clearly recurs)
6. `try()` / `tryCatch` only when one item failing must not kill the batch — prefer `try()` over `safely()`; log which item failed

**Purrr adverbs** (`safely`, `possibly`, `quietly`, `insistently`) are `tryCatch` for `map` —
same rules. `possibly(read_csv, tibble())` swallowing read errors is almost always wrong.
`insistently()` (retry) is rare; fix flaky I/O instead.

```r
# Good: fail fast before looping 111 species
if (length(species_files) == 0) stop("No species CSVs found")

# Good: expected gap — not every month has a netCDF
if (!file.exists(nc_path)) next

# Good: long job — resume without reprocessing
if (file.exists(out_file) && file.info(out_file)$size > 0) next

# Smell: swallow errors everywhere
for (f in files) {
  tryCatch(process(f), error = function(e) message(e))
}

# Smell: guard every step for problems that don't exist yet
if (nrow(d) > 0 && "YearMon" %in% names(d) && !all(is.na(d$YearMon))) {
  d <- d |> mutate(year = year(ym(YearMon)))
}
```

## Code smells (checklist)

Smells are not bugs — patterns that often make scripts harder to read or debug.
**Not smells:** long but linear code, a `for` with dplyr inside, named intermediates
when reused, or a shared function genuinely called from ≥2 places.

### Custom functions

| Smell | Better |
|-------|--------|
| One-off helper used once **in a step script** | Inline in loop or pipe |
| Helper extracted because loop is long | Keep `for`; pipe inside it |
| Tiny wrapper (`read_my_csv <- function(f) fread(f)`) | Call `fread()` directly |
| Helper for "reuse" but only one call site in one script | Inline (loop ≠ multiple call sites) |
| One-liner path helper used once (`foo_path(config)`) | Inline `file.path(...)` |
| **OK:** same function called ≥2 times in one step script | Keep it |
| **OK:** multi-step pipeline fn in `R/` with one orchestrator call | Keep in `R/` (`build_model_packs`, `write_metrics_table`) |

### Paths & config

| Smell | Better |
|-------|--------|
| `Sys.getenv(..., unset = ...)` in step script | Plain string at top |
| `if (nzchar(Sys.getenv("X")))` path override | Plain string at top |
| `nzchar(Sys.getenv("X"))` to test unset | `x != ""` or `Sys.getenv("X", "default")` — `getenv` always returns length-1 |
| `if (limit != "")` / debug env hooks never used in prod | Delete; edit script for one-offs |
| `if (subdir_env != "")` discover-all vs subset | One discover path; subset by editing `src_dirs` |
| `if (nzchar(Sys.getenv("SLURM_CPUS_PER_TASK")))` | `max(1L, as.integer(Sys.getenv("SLURM_CPUS_PER_TASK", "1")))` |
| Paths scattered through the file | All paths in first ~15 lines |
| `source("helpers.R")` for one pipeline step | Inline, or existing shared `config.R` only |
| `OUTPUT_FOO` constant defined but never used | Delete, or wire scripts that still hardcode the path |
| Path helper that is only `file.path(OUTPUT_X, "sub")` once | Inline at call site |
| **OK:** `OUTPUT_METRICS` used in fit + figures + tables | Keep constant in shared path file |
| **OK:** `prepared_data_dir(config)` — stamp logic + many call sites | Keep helper |

### Tidyverse & style

| Smell | Better |
|-------|--------|
| `substr` + `grepl` on dates | `lubridate` (`ym`, `year`, `month`) |
| `dplyr::` on every verb with dplyr loaded | `library()` + bare verbs |
| `read.csv()` on normal-sized files | `read_csv()` |
| 15-step pipe, nothing reused | One intermediate at a natural break |
| Split every pipe step into a named variable | Pipe; name only when reused or hard to scan |

### Loops & iteration

| Smell | Better |
|-------|--------|
| Nested `map` inside `map` | `for` with clear steps |
| `purrr::walk` + I/O / `next` / mutation | Plain `for` |
| `map` when you mutate something outside the loop | `for` |
| **OK:** `map_dfr(files, read_csv)` — same transform, no side effects | Keep `map` |

### Error handling & guards

| Smell | Better |
|-------|--------|
| `tryCatch` / `safely` / `possibly` around every read or loop | Fix cause; per-item `try()` only if batch must continue |
| `stop()` after every `read_csv` | Trust the read; `stop()` on missing *upstream* outputs only |
| `if (nrow(d) > 0)` around every dplyr step | Only where empty data is realistic; else let pipe fail |
| `if ("col" %in% names(d))` before every mutate | Fix column names; check once at load if truly optional |
| Soft count / sentinel gates (`n < 90`, “expected ≥N”) with no real miss | Verify upstream; delete the gate |
| Orchestrator re-checks what the previous script already produced | Trust verified outputs; keep the next script thin |
| Long `if/else` for hypothetical edge cases | Fix root cause; add guard only after real failure |
| `insistently()` retry without a known flaky step | Fix I/O; retries hide real problems |
| **OK:** `stop()` if file list empty before 10-hour loop | Keep |
| **OK:** `if (!file.exists(nc_path)) next` for known gaps | Keep |
| **OK:** `if (file.exists(out_file)) next` for resume | Keep |

### Naming

| Smell | Better |
|-------|--------|
| `output/sample/`, `output/manuscript/` | `output/training_data/`, flat workstreams |
| `active_retrain`, `current_version` + nested version keys | `run_id` (+ `frozen_run` only if needed) |
| `targets/_manuscript.R`, `build_results.R` | `targets/_build_data.R` (pre-render derived data) |
| Nested `output/paper1/cv/` | `output/validation/` at repo root |
| Config key named for a one-off task | Key named for the artifact stamp or folder |

### Comments & structure

| Smell | Better |
|-------|--------|
| `# filter rows` (states the obvious) | Delete, or explain **why** |
| `# === STEP 3 ===` banners | Short `# why` comment or nothing |
| Roxygen `#'` in a one-off script | Plain `#` or nothing |
| Comments mentioning skills, agents, internal paths | Delete |

### Data handling

| Smell | Better |
|-------|--------|
| Magic numbers (`-999`) without comment | Brief `# why` (e.g. netCDF missval) |
| Copy-paste same 20-line block 3× with tiny diffs | Accept repetition, or extract only if ≥2 real call sites |
| Defensive `tryCatch` around every I/O call | Let I/O fail; fix path or add resume/skip |
| Reportable metrics only in RDS / qs2 | Export CSV/JSON for reports and QC |
| Parquet migration for attributed prepared inputs "for purity" | Keep binary R blobs; CSV for evidence |
| **OK:** serialized model file + summary JSON sidecar | Keep — compute vs evidence split |

### Modelling & stats

| Smell | Better |
|-------|--------|
| Giant `if/else` tree per species | Loop over species with clear skip rule |
| Saving 12 near-identical objects | Named list + one export step |
| Fitting models inside a long pipe chain | Pipes for load/clean; `for` or `try()` for fits |
| **OK:** `try(glmmTMB(...), silent = TRUE)` when some taxa won't converge | Keep; log failures |

### The pattern

A smell usually means: **indirection** (helper, env var, nested `map`), **wrong tool**
(`map` where `for` tells the story), **false generality** (abstracted but used once), or
**noise** (guards/comments that don't help a coauthor read top to bottom).

## Common mistakes

| Symptom | Fix |
|---------|-----|
| `Sys.getenv(..., unset = ...)` in step script | Plain string variable |
| `if (nzchar(Sys.getenv("X")))` path override | Plain string variable |
| `nzchar(Sys.getenv(...))` | `getenv(..., "default")` or `x != ""` |
| `if (limit != "")`, unused `METHOD`/`SUBDIRS` env branches | Delete until needed; edit script instead |
| Helper fn, one call site **in a step script** | Inline |
| Path helper fn, one call site, one-liner body | Inline `file.path(...)` |
| 90-line pipeline block inlined into orchestrator | Extract to `R/*.R` even if one call |
| `dplyr::filter()` with tidyverse loaded | Bare `filter()` |
| `substr(YearMon, 1, 4)` for dates | `year(ym(YearMon))` |
| `purrr::map` over files with `fwrite`/`next` | Plain `for` loop |
| Pipe 15 steps with no reuse | One intermediate at a natural break |
| `tryCatch` / `safely` around whole loop / every `fread` | Fix cause; `next` or per-item `try()` only if batch must continue |
| `stop()` on every row/column check | Let dplyr fail; `stop()` only after a real recurring miss |
| `if (n_prep < 90)` / soft “expected N” gates | Confirm prepare yourself; don't encode unchecked fear |
| `if (nrow(d) > 0)` before every mutate/filter | Only where empty is realistic; else let pipe fail |
| `if ("x" %in% names(d))` on every step | Fix colnames once; don't guard hypotheticals |
| `#'` roxygen, `# ===` banners | Delete or one-line `#` |

## Rationalizations

| Excuse | Reality |
|--------|---------|
| "Env vars make it portable" | Edit 2–3 strings at top; SLURM `cd`s to repo root |
| "Helper keeps it clean" | One-off helpers in step scripts force hunting — top failure mode |
| "Called inside a loop so it's reused" | Loop ≠ multiple call sites |
| "Every path needs a helper in paths.R" | Constants/helpers only when shared or non-trivial; inline one-offs |
| "One call site → must inline" | True for one-liners in step scripts; false for 30+ line pipeline steps in `R/` |
| "binary blobs are wrong, use CSV for models" | CSV can't store fitted model objects; export CSV for metrics, RDS/qs2 for fits |
| "unset is beginner-friendly" | Plain strings are clearer than getenv semantics |
| "purrr is more idiomatic" | `for` is clearer for I/O, skips, and mutation |
| "substr is fine for YYYY-MM" | `lubridate` states intent; verify format once on real data |
| "One giant pipe is always best" | Name intermediates when reused or the chain is hard to scan |
| "Defensive tryCatch makes HPC robust" | No — it hides bugs. Catch only known per-item failures |
| "stop() helps debugging" | Only after that miss was real — not speculative counts / sentinels |
| "Need n >= 90 so the job is safe" | You should have checked prepare; the gate is a fake test |
| "safely() is the tidyverse way" | It's still hiding errors — use only for known per-item failure |
| "Need if (nrow > 0) to be safe" | Empty-after-filter is a bug to fix, not wrap at every step |
| "Check column exists before mutate" | Wrong name should fail loudly — don't paper over typos |
| "Scripts should handle all errors" | Fix the cause; R's traceback is the handler |
| "I didn't watch the last step, so I'll guard this one" | Go look at outputs; don't compensate in code |
| "`manuscript` folder is clear for the paper" | Paper is intent; paths are workstreams + `build_*` |
| "`build_results` covers everything we export" | Too broad — `build_data` = pre-render tables/rasters; `build_figures` = PDFs |
| "We need current_version and run_id" | One stamp per lifecycle; duplicate keys drift |
| "Need subset via env for flexibility" | Edit `src_dirs` or shell for a one-off; don't keep an R branch you never take |


## Companions

`r-editor-setup` · `ggplot-maps` · `dayhoff-slurm`

Not: `r-style-guide`, `tidyverse-patterns`, `r-tidyverse-style`.
