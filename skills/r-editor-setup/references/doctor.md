# Doctor — R environment checks

Run these from the project or home directory. Report a pass/fail table.

## Shell checks

```bash
command -v R && R --version | head -1
command -v Rscript
command -v air && air --version
command -v radian || true
command -v quarto || true
# Cursor or VS Code:
cursor --list-extensions 2>/dev/null | grep -E 'reditorsupport\.r|posit\.air-vscode|rdebugger\.r-debugger|quarto\.quarto' \
  || code --list-extensions 2>/dev/null | grep -E 'reditorsupport\.r|posit\.air-vscode|rdebugger\.r-debugger|quarto\.quarto'
```

## R package doctor

```bash
Rscript - <<'RS'
pkgs <- c(
  # Tier A — editor (vscode-R / VS Code docs)
  "languageserver", "httpgd", "rmarkdown", "lintr",
  # Air / project helpers
  "usethis",
  # Debugger (optional; often GitHub)
  "vscDebugger",
  # Tier B — research baseline
  "tidyverse", "here", "renv", "pak", "remotes",
  "broom", "patchwork", "scales", "knitr", "jsonlite"
)
status <- vapply(pkgs, function(p) {
  if (requireNamespace(p, quietly = TRUE)) "OK" else "MISSING"
}, character(1))
print(data.frame(package = pkgs, status = unname(status), row.names = NULL))
cat("\nR_HOME=", R.home(), "\n", sep = "")
cat("libPaths:\n")
writeLines(paste0("  ", .libPaths()))
RS
```

Adjust the package list if the user asked for editor-only (Tier A) or a
domain Tier C set from [packages.md](packages.md).

## Project file checks

```bash
test -f air.toml -o -f .air.toml && echo "air.toml: OK" || echo "air.toml: MISSING"
test -f .vscode/settings.json && echo "settings.json: OK" || echo "settings.json: MISSING"
test -f .vscode/extensions.json && echo "extensions.json: OK" || echo "extensions.json: MISSING"
grep -q 'Posit.air-vscode' .vscode/settings.json 2>/dev/null \
  && echo "Air defaultFormatter: OK" || echo "Air defaultFormatter: MISSING"
```

## Interactive verify (ask the user, or guide them)

From [VS Code R docs](https://code.visualstudio.com/docs/languages/r) and
[Datanovia](https://www.datanovia.com/learn/tools/r-in-vscode/setting-up-r-environment-in-vscode.html):

| Check | How | Pass looks like |
|-------|-----|-----------------|
| Terminal | Command Palette → `R: Create R terminal` | R or radian prompt |
| Session | Status bar | `R: <pid>` after sending code (`r.sessionWatcher`) |
| Completions | Type `mean(` in an `.R` file | Signature / help hover |
| Plot pane | `plot(1:10)` with `r.plot.useHttpgd` | Plot in VS Code / Cursor panel |
| Format | Save a messy one-liner `.R` file | Air rewrites layout |
| Baseline pkgs | `library(tidyverse); library(here)` | No error |
| Quarto (optional) | `quarto --version` + extension if `.qmd` | Semver + `quarto.quarto` listed |

## Quarto companion skill (external)

Not part of this pack. If the user writes `.qmd`, after CLI/extension pass:

```bash
npx skills add posit-dev/skills@quarto-authoring -g
```

Missing `quarto-authoring` is **not** an r-editor-setup doctor failure.

## Common failures → fix

| Symptom | Fix pointer |
|---------|-------------|
| R not found | Install CRAN R; set `r.rpath.*` / `r.rterm.*` |
| No completions | `install.packages("languageserver")`; reload window |
| No plot pane | `httpgd` + `"r.plot.useHttpgd": true` + session watcher |
| radian missing | `pip install -U radian`; set `r.rterm.*`; `r.bracketedPaste` |
| Save does not format | Install `Posit.air-vscode`; set workspace formatter; reload |
| Works until `renv::init()` | Add scaffolding libs per vscode-R renv wiki |
| Windows compile errors | Install Rtools, retry |
| Quarto not found | Install Quarto CLI + `quarto.quarto`; authoring skill stays upstream |
