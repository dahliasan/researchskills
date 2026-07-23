# Install — system, extensions, radian, Air

Agents must flag failures instead of claiming the IDE is ready.

## 1. R

- Install from [CRAN](https://cloud.r-project.org/) (R ≥ 3.4; prefer current release).
- Windows: enable **Write R version to registry** so vscode-R can find R
  ([VS Code docs](https://code.visualstudio.com/docs/languages/r)).
- Confirm: `R --version` and `Rscript -e "cat(R.home())"`.

If the extension cannot find R, set `r.rpath.mac` / `r.rpath.linux` /
`r.rpath.windows` (path to `R`), distinct from `r.rterm.*` (console /
radian).

## 2. Extensions (Cursor / VS Code)

| Extension | ID | Role |
|-----------|----|------|
| R | `REditorSupport.r` | Terminal, viewers, LSP client (~3M Marketplace installs) |
| Air | `Posit.air-vscode` | Formatter (+ bundled binary) |
| R Debugger | `RDebugger.r-debugger` | Breakpoints (needs `vscDebugger`) |
| Quarto | `quarto.quarto` | `.qmd` |
| Tombi | `tombi-toml.tombi` | `air.toml` editing |

```bash
cursor --install-extension REditorSupport.r
cursor --install-extension Posit.air-vscode
cursor --install-extension RDebugger.r-debugger   # optional
cursor --install-extension quarto.quarto            # optional
# VS Code: code --install-extension …
```

Reload window after first install.

## 3. radian (recommended console)

From [vscode-R wiki](https://github.com/REditorSupport/vscode-R/wiki/Installation:-macOS)
and [VS Code R docs](https://code.visualstudio.com/docs/languages/r):

```bash
pip install -U radian
# or: pipx install radian
which radian   # macOS/Linux
```

**User** settings (machine-specific — usually do **not** commit):

```json
{
  "r.rterm.mac": "/path/from/which/radian",
  "r.bracketedPaste": true,
  "r.sessionWatcher": true,
  "r.plot.useHttpgd": true,
  "r.alwaysUseActiveTerminal": true
}
```

Use `r.rterm.linux` / `r.rterm.windows` on other OSes. Wiki may also set
`terminal.integrated.env.osx` `R_HOME` / `R_BIN` when radian needs them.

## 4. Air CLI (agents / CI)

Extension alone is enough for in-editor format. CLI helps agents and hooks
([Air CLI](https://posit-dev.github.io/air/cli.html)):

```bash
# macOS Homebrew
brew install air
# or official installer
curl -LsSf https://github.com/posit-dev/air/releases/latest/download/air-installer.sh | sh
air --version
```

Windows: use the PowerShell installer from the same docs page.

## 5. Quarto (optional tooling — not the authoring skill)

When the project uses `.qmd` or the user wants Quarto reports:

1. Install **Quarto CLI**: https://quarto.org/docs/get-started/
   - macOS: `brew install --cask quarto` (or official installer)
2. Install extension `quarto.quarto` (see §2).
3. Optional R package: `install.packages("quarto")`.

Confirm:

```bash
quarto --version
cursor --list-extensions | grep -i quarto || code --list-extensions | grep -i quarto
```

**Do not** copy or fork `posit-dev/skills@quarto-authoring` into researchskills.
That skill stays upstream. After CLI/extension are OK, tell the user:

```bash
npx skills add posit-dev/skills@quarto-authoring -g
```

See [INSTALL.md](../../../INSTALL.md) (Optional companion skills).

## 6. Pandoc

Needed for rich R help / R Markdown. Often present via RStudio or Quarto CLI.
If help is plain-text only: install Pandoc or Quarto.

## 7. Project Air config

Prefer:

```r
install.packages("usethis")
usethis::use_air()
```

This creates empty `air.toml`, workspace format-on-save, and
`.vscode/extensions.json` recommending `Posit.air-vscode`
([tidyverse Air 0.7 blog](https://tidyverse.org/blog/2025/06/air-0-7-0/),
[use_air](https://usethis.r-lib.org/reference/use_air.html)).

Manual templates: [templates.md](templates.md).

## Upstream links

- https://code.visualstudio.com/docs/languages/r
- https://github.com/REditorSupport/vscode-R/wiki
- https://posit-dev.github.io/air/
- https://marketplace.visualstudio.com/items?itemName=REditorSupport.r
- https://marketplace.visualstudio.com/items?itemName=Posit.air-vscode
- https://quarto.org/docs/get-started/
- https://skills.sh/posit-dev/skills/quarto-authoring
