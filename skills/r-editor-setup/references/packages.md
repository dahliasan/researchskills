# Packages — tiers for a usable research R setup

Install **missing** packages only. Prefer `pak::pak(pkgs)` when `pak` is
installed; otherwise `install.packages(pkgs)`.

Sources for Tier A: [VS Code R](https://code.visualstudio.com/docs/languages/r),
[REditorSupport marketplace](https://marketplace.visualstudio.com/items?itemName=REditorSupport.r),
[vscode-R wiki](https://github.com/REditorSupport/vscode-R/wiki/Installation:-macOS).

## Tier A — editor (always for Cursor / VS Code R)

| Package | Why |
|---------|-----|
| `languageserver` | Completions, diagnostics, hover, outline ([required by vscode-R](https://code.visualstudio.com/docs/languages/r)) |
| `httpgd` | Interactive plot viewer (`r.plot.useHttpgd`) |
| `lintr` | Linting surfaced through the language server |
| `rmarkdown` | Formatted help / Rmd; pair with Pandoc |
| `jsonlite` | Often pulled by languageserver / vscode-R tooling |
| `usethis` | `use_air()`, project helpers |
| `vscDebugger` | R Debugger extension backend (often `remotes::install_github("ManuelHentschel/vscDebugger")`) |

```r
install.packages(c(
  "languageserver", "httpgd", "lintr", "rmarkdown", "jsonlite", "usethis"
))
# If httpgd is missing from CRAN mirrors, try r-universe (vscode-R wiki):
# install.packages("httpgd", repos = c("https://nx10.r-universe.dev", "https://cloud.r-project.org"))
```

## Tier B — research baseline (default for “set up R for research”)

Enough for most analysis / manuscript prep without domain extras:

| Package | Why |
|---------|-----|
| `tidyverse` | dplyr, ggplot2, readr, tidyr, purrr, stringr, tibble, forcats |
| `here` | Project-relative paths |
| `renv` | Project libraries / lockfiles |
| `pak` | Fast, reliable installs |
| `remotes` | GitHub / remote installs |
| `broom` | Tidy model summaries |
| `patchwork` | Compose ggplot panels |
| `scales` | Axis / legend helpers |
| `knitr` | Reports / Quarto engine piece |
| `conflicted` | Make masked-function conflicts explicit |

```r
install.packages(c(
  "tidyverse", "here", "renv", "pak", "remotes",
  "broom", "patchwork", "scales", "knitr", "conflicted"
))
```

## Tier C — domain (offer; install on match)

Install when the open project or user request matches:

| Domain | Packages |
|--------|----------|
| Spatial / maps | `sf`, `terra`, `stars`, `ggrepel`, `rnaturalearth` (+ `ggplot-maps` skill) |
| Mixed models | `lme4`, `glmmTMB`, `broom.mixed`, `performance`, `DHARMa`, `MuMIn` |
| Bayesian | `brms`, `cmdstanr` (ask first; heavy) |
| Pipelines / async | `targets`, `tarchetypes`, `crew`, `mirai` |
| Larger dplyr workloads | `duckplyr` (DuckDB-backed dplyr) |
| Tables | `gt`, `gtsummary`, `flextable` |
| Quarto pubs | `quarto` R package; CLI `quarto` separately |
| Quarto authoring skill | **External** — `npx skills add posit-dev/skills@quarto-authoring -g` (do not vendor) |
| Dev / packages | `devtools`, `testthat`, `roxygen2`, `pkgload` |

## Tier D — AI / agent bridge (opt-in)

Only when the user wants LLM tools talking to a **live** R session, or
RStudio/Positron chat assistants. Details:
[modern-tooling.md](modern-tooling.md).

| Package | Why |
|---------|-----|
| `ellmer` | LLM APIs from R |
| `btw` | Session/docs context; MCP-friendly tools; `use_btw_md()` |
| `mcptools` | MCP server so Cursor/Claude can use running R |
| `gander` / `chores` | IDE chat assistants (strongest in RStudio/Positron) |

```r
install.packages(c("ellmer", "btw", "mcptools"))
# optional: install.packages(c("gander", "chores"))
```

## What not to force

- Do not install every Tier C/D package “just in case”.
- Prefer **Air** over **styler** for new formatter setups (styler remains fine
  in legacy repos that already standardize on it).
- Do not commit a bloated user library into git; use `renv` for project pins.
- Do not install `REditorSupport.r` inside **Positron** (native R; extension conflicts).

## renv + vscode-R

If `renv` is active, add a project scaffolding script that names IDE deps so
they are snapshotted / cached
([wiki](https://github.com/REditorSupport/vscode-R/wiki/Working-with-renv-enabled-projects)):

```r
# scaffolding.R — declare only; need not be sourced in analysis
library(languageserver)
library(httpgd)
# library(vscDebugger)
```

Then `renv::snapshot()` after installs.
