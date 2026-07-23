# Modern tooling — projects, extensions, packages (2025–2026)

Catalog of **newer or high-leverage** tools worth knowing when setting up R.
Offer these; do not force-install everything. Prefer official Posit / tidyverse
sources. Stars below are approximate GitHub signals at research time (mid-2026).

## IDEs and kernels

| Project | What it is | When to mention |
|---------|------------|-----------------|
| [Positron](https://github.com/posit-dev/positron) (~4k★) | Posit’s next data-science IDE (Code OSS). Native R+Python panes; **Air bundled**. Do **not** install `REditorSupport.r` in Positron (incompatible; built-in R). | User wants RStudio-like panes + VS Code editing |
| [Ark](https://github.com/posit-dev/ark) | Jupyter-compatible R kernel + LSP/DAP used by Positron | Positron users; not a Cursor install step |
| Cursor / VS Code + vscode-R | Still the polyglot/AI-assistant path | Default for this skill |

Migration note: [Positron ← VS Code](https://positron.posit.co/migrate-vscode.html).

## Formatters and editor extensions

| Tool | Role |
|------|------|
| [Air](https://github.com/posit-dev/air) (~400★) + `Posit.air-vscode` | **Current** R formatter; prefer over styler for new setups |
| `REditorSupport.r` (~3.3M Marketplace installs) | Required for Cursor/VS Code R |
| `RDebugger.r-debugger` + `vscDebugger` | Breakpoints |
| `quarto.quarto` | Quarto authoring |
| Tombi | `air.toml` schema help |
| `usethis::use_air()` | Canonical project Air + `.vscode` wiring |

## AI / agent bridge (opt-in Tier D)

Posit’s 2025–2026 LLM stack for R (offer when the user uses Cursor/Claude with live R sessions):

| Package | Role | Install hint |
|---------|------|--------------|
| [ellmer](https://github.com/tidyverse/ellmer) (~600★) | Unified LLM APIs from R | CRAN |
| [btw](https://github.com/posit-dev/btw) (~130★) | Session/docs context for LLMs; `btw_mcp_server()`; `use_btw_md()` | CRAN / posit-dev r-universe |
| [mcptools](https://github.com/posit-dev/mcptools) (~180★) | MCP server/client so agents can talk to **running** R sessions | CRAN / GitHub |
| [gander](https://github.com/simonpcouch/gander) (~130★) | Env-aware coding assistant (RStudio/Positron chat) | CRAN |
| [chores](https://github.com/simonpcouch/chores) (~140★) | LLM assistants for common R chores | CRAN |
| [vitals](https://github.com/tidyverse/vitals) | LLM evaluation harness | optional |

For Cursor: prefer **btw + mcptools** so the agent can inspect the live session
(`btw::btw_mcp_server()` / `mcptools::mcp_session()`). See
[btw](https://posit-dev.github.io/btw/) and
[mcptools server vignette](https://posit-dev.github.io/mcptools/articles/server.html).

Ask before installing Tier D (needs API keys / MCP config).

## Performance / modern data

| Package | Role |
|---------|------|
| [duckplyr](https://github.com/tidyverse/duckplyr) (~400★) | dplyr API + DuckDB engine for larger data |
| [mirai](https://github.com/r-lib/mirai) (~300★) + nanonext | Modern async / parallel (pairs well with `crew` / targets) |
| `pak` | Prefer for installs (already Tier B) |

## Quality-of-life (safe Tier B add-ons)

| Package | Role |
|---------|-----|
| `conflicted` | Explicit function conflicts (tidyverse-friendly) |
| `cli` / `rlang` | Usually come with tidyverse; ensure present for scripts |

## Publishing / skills companions

| Project | Role |
|---------|------|
| Quarto CLI + `quarto` R pkg | Manuscripts / slides (already Tier C) |
| [`posit-dev/skills@quarto-authoring`](https://skills.sh/posit-dev/skills/quarto-authoring) (~900 installs) | Keep **upstream**; `npx skills add posit-dev/skills@quarto-authoring -g` — do not vendor into researchskills |
| R-multiverse | Dual community/production package repo (advanced reproducibility; mention only if asked) |

## What not to chase

- Random “Top 40 new CRAN packages” for monthly niche domains — only add when
  the open project needs them.
- Installing vscode-R **inside Positron**.
- Replacing Air with styler on greenfield projects.
- Forcing gander in Cursor (it targets RStudio/Positron chat UX); use btw/MCP instead.
- **Forking** `quarto-authoring` into researchskills by default (compose via
  `npx skills add`; in-house copy only with `references/attribution.md` if
  pack-specific Quarto rules are required).

## skills.sh search notes

`npx skills find` (R / positron / quarto / environment): no competing full R
env-doctor skill. Useful companions: `posit-dev/skills` (Quarto), Positron
internal QA skills (not for end users).
