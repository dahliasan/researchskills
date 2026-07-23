---
name: r-editor-setup
description: >-
  Use when setting up, doctoring, or repairing an R environment for Cursor or
  VS Code: install/check R, extensions, radian, httpgd, Air, languageserver,
  lintr, baseline research packages (tidyverse, renv, …), project air.toml /
  .vscode settings, or when the user says "/r-editor-setup" / "set up R".
  Does not teach statistics or map recipes (use ggplot-maps).
metadata:
  version: 0.2.2
---

# /r-editor-setup — R environment for Cursor / VS Code

Get a machine **ready for typical research R work**: interpreter, editor IDE
features, formatter, and a sensible package baseline. Doctor first; install
only what is missing; verify with concrete checks.

Inspired by (and prefer linking to) official sources over ad-hoc memory:

- [VS Code: R](https://code.visualstudio.com/docs/languages/r)
- [vscode-R wiki (macOS)](https://github.com/REditorSupport/vscode-R/wiki/Installation:-macOS) (+ Windows/Linux siblings)
- [vscode-R + renv](https://github.com/REditorSupport/vscode-R/wiki/Working-with-renv-enabled-projects)
- [Air editors / VS Code](https://posit-dev.github.io/air/editor-vscode.html), [CLI](https://posit-dev.github.io/air/cli.html)
- [`usethis::use_air()`](https://usethis.r-lib.org/reference/use_air.html)
- Community setup patterns: [Datanovia R in VS Code](https://www.datanovia.com/learn/tools/r-in-vscode/setting-up-r-environment-in-vscode.html)
- Newer stack catalog: [references/modern-tooling.md](references/modern-tooling.md)
  (Positron/Ark, btw/ellmer/mcptools, duckplyr, …)

Skill-ecosystem note: `npx skills find` has **no** strong R+VS Code env skill
(flutter/`environment-setup` patterns are the closest analogues; tiny R pattern
skills exist but are not install/doctor playbooks). This skill fills the
env-doctor gap. Quarto **authoring** stays upstream
(`posit-dev/skills@quarto-authoring`); this skill only installs/checks Quarto
CLI + `quarto.quarto` when needed — do **not** vendor or fork that skill here.

## Modes

| Signal | Mode |
|--------|------|
| "set up R / ready to code / install what I need" | **full-setup** |
| "is my R env OK? / doctor" | **doctor** |
| "install packages / tidyverse / missing pkgs" | **packages** |
| "Air / format on save / air.toml" | **air-project** |
| "format this file/folder" | **format** |
| "R MCP / btw / ellmer / connect agent to R" | **ai-bridge** |
| "Positron vs VS Code / Cursor" | **ide-advice** (point at modern-tooling; no forced migrate) |

Default: **doctor** → install gaps → **packages** (core + research baseline) →
**air-project** if a project folder is open → re-**doctor** until green.
Offer Tier D / Positron only when relevant.

## Step 0 — Doctor (always)

Run the checks in [references/doctor.md](references/doctor.md). Print a
pass/fail table. Do **not** claim the environment is ready until:

1. `Rscript -e 'R.version.string'` works
2. Extensions `REditorSupport.r` and `Posit.air-vscode` are installed (Cursor)
3. R packages `languageserver` and `httpgd` load
4. At least one verify check from doctor.md succeeds (terminal / plot / format)

## Step 1 — Install missing system + editor pieces

Order matters ([Datanovia](https://www.datanovia.com/learn/tools/r-in-vscode/setting-up-r-environment-in-vscode.html),
[VS Code docs](https://code.visualstudio.com/docs/languages/r)):

1. **R** on PATH (CRAN; Windows: write version to registry)
2. **Extensions**: `REditorSupport.r`, `Posit.air-vscode`
3. Optional extensions: `RDebugger.r-debugger`, `quarto.quarto`, Tombi
4. **Air CLI** (agents/CI) — see [references/install.md](references/install.md)
5. **radian** (`pip`/`pipx`) + point `r.rterm.*` + `r.bracketedPaste`
6. Editor settings: `r.sessionWatcher`, `r.plot.useHttpgd`

Details and OS notes: [references/install.md](references/install.md).

## Step 2 — Install / check R packages

Use the tiers in [references/packages.md](references/packages.md).

1. Run the package doctor script (missing vs installed).
2. Install **Tier A** (editor) without asking if the user asked for setup.
3. Install **Tier B** (research baseline) unless the user asked for editor-only.
4. Offer **Tier C** (domain: geo, mixed models, pipelines, duckplyr/mirai) —
   only what matches the open project or an explicit ask.
5. Offer **Tier D** (ellmer / btw / mcptools) only for **ai-bridge** or an
   explicit ask; never silent-install API-key tooling.
6. Prefer `pak::pak()` when `pak` is available; else `install.packages()`.
7. On Windows, if compile fails, tell the user to install **Rtools**.
8. If the user prefers Positron: follow
   [modern-tooling.md](references/modern-tooling.md) (skip vscode-R; Air is
   bundled).

If the project uses **renv**, declare IDE deps in a scaffolding file per the
[vscode-R renv wiki](https://github.com/REditorSupport/vscode-R/wiki/Working-with-renv-enabled-projects)
(`languageserver`, `httpgd`, optional `vscDebugger`) so they enter the lockfile
/ cache — do not leave the language server broken inside `renv`.

## Step 3 — Wire the project (Air + workspace)

Prefer **workspace** config (checked in) over user-global Air settings
([Air VS Code guide](https://posit-dev.github.io/air/editor-vscode.html)).

In the project root:

1. Prefer `usethis::use_air()` when `usethis` is available (creates `air.toml`,
   `.vscode/settings.json`, `.vscode/extensions.json`).
2. Else write templates from [references/templates.md](references/templates.md).
3. Ask before `air format` on a whole tree (large diffs).
4. Optional CI: `usethis::use_github_action(url = "https://github.com/posit-dev/setup-air/blob/main/examples/format-check.yaml")`.

## Step 4 — Verify (show, don't assume)

Walk the user (or run) the verify checklist in [references/doctor.md](references/doctor.md):

- `R: Create R terminal` works (radian if configured)
- Completions / hover work (`languageserver`)
- `plot(1:10)` appears in the httpgd pane
- Saving an `.R` file formats with Air
- `library(tidyverse)` (or Tier B) loads

## Air vs lintr vs Prettier

| Tool | Role |
|------|------|
| **Air** | Formatter (layout). Default width 80. Extension ships its own binary. |
| **lintr** | Linter via `languageserver`. Does not reformat. |
| **Prettier** | Not for `.R`. |
| **styler** | Legacy R formatter; prefer Air for new setups. |

Air usually does **not** wrap long `#` comments. Keep Air `line-width` and
lintr `line_length_linter` aligned when both are used.

## Rules

1. Doctor before installing; install only gaps; re-doctor after.
2. Workspace Air settings + `air.toml` for projects; avoid user-global
   format-on-save unless the user insists.
3. Scrub personal absolute paths from committed settings (use
   `${workspaceFolder}` or omit machine-specific `r.rterm` from the repo —
   keep radian path in **user** settings).
4. Do not mass-format without confirmation.
5. Route map code to `ggplot-maps`; project scaffold to `research-project-ops`.
6. Cite upstream docs in the exit summary when something non-obvious was fixed.
7. Quarto: install/check **CLI + extension** only. For `.qmd` authoring help,
   recommend `npx skills add posit-dev/skills@quarto-authoring -g`. Never copy
   that skill into researchskills unless the user explicitly asks for an
   attributed in-house fork.

## Exit

Report: mode, doctor table, packages installed, files written, verify results,
whether **Reload Window** is needed, and (if Quarto is in play) whether the
user should install the upstream `quarto-authoring` companion skill.
