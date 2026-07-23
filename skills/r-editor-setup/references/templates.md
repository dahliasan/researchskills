# Templates — workspace files

Merge into existing JSON; do not delete unrelated keys. Prefer
`usethis::use_air()` when available — it writes these for you.

Machine-specific paths (`r.rterm.*`, absolute `R_HOME`) belong in **user**
settings, not the repo.

## `air.toml`

Empty file is a valid signal. Explicit defaults:

```toml
[format]
line-width = 80
indent-width = 2
indent-style = "space"
line-ending = "auto"
persistent-line-breaks = true
assignment-style = "arrow"
```

## `.vscode/settings.json` (from `use_air()` / Air docs)

```json
{
  "[r]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "Posit.air-vscode"
  },
  "[quarto]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "quarto.quarto"
  },
  "r.sessionWatcher": true,
  "r.plot.useHttpgd": true,
  "r.bracketedPaste": true,
  "r.alwaysUseActiveTerminal": true
}
```

Omit Quarto block if the project has no `.qmd`. Keep radian `r.rterm.*` in
user settings.

## `.vscode/extensions.json`

```json
{
  "recommendations": [
    "REditorSupport.r",
    "Posit.air-vscode"
  ]
}
```

Optional recommendations: `RDebugger.r-debugger`, `quarto.quarto`.

## Optional `.lintr`

Only if the project already uses lintr or the user wants matching width:

```r
linters: linters_with_defaults(
  line_length_linter(80L)
)
```

## Optional `scaffolding.R` (renv + vscode-R)

```r
# Declare IDE dependencies for renv snapshot/cache (need not be sourced).
library(languageserver)
library(httpgd)
```
