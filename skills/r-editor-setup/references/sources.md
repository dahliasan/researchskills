# Sources — inspiration and authority

This skill synthesizes public setup guidance. Prefer these over chat memory
when behavior is unclear.

## Official / primary

| Source | Used for |
|--------|----------|
| [VS Code: R](https://code.visualstudio.com/docs/languages/r) | Required stack: R, `languageserver`, extension; recommends radian + httpgd; lintr; debugger |
| [REditorSupport/vscode-R](https://github.com/REditorSupport/vscode-R) + wiki | OS install, radian env, httpgd repos, debugger, renv scaffolding |
| [posit-dev/air](https://github.com/posit-dev/air) docs | Formatter, workspace vs user settings, CLI, CI |
| [`usethis::use_air()`](https://usethis.r-lib.org/reference/use_air.html) | Canonical project Air + `.vscode` wiring |
| [tidyverse Air posts](https://tidyverse.org/blog/2025/02/air/) | Product intent; format-on-save; styler comparison |

## Strong secondary guides

| Source | Used for |
|--------|----------|
| [Datanovia: Setting up R in VS Code](https://www.datanovia.com/learn/tools/r-in-vscode/setting-up-r-environment-in-vscode.html) | Ordered install, verify checklist (terminal / workspace / help / plots), settings bundle |
| [R-bloggers / VS Code + AI tooling (2025)](https://www.r-bloggers.com/2025/06/setting-up-vscode-for-r-and-generative-ai-tools/) | Practical Cursor-adjacent tips; httpgd CRAN flakiness; radian + bracketed paste |
| [InfoWorld: Run R in VS Code](https://www.infoworld.com/article/2267616/how-to-run-r-in-visual-studio-code.html) | Older but durable radian / languageserver narrative |
| [RStudio vs VS Code vs Positron](https://r-statistics.co/RStudio-vs-VSCode-vs-Positron.html) | IDE comparison framing |

## Newer Posit / tidyverse stack (2025–2026)

See [modern-tooling.md](modern-tooling.md) for the live catalog. Highlights:

| Project | Used for |
|---------|----------|
| [Positron](https://github.com/posit-dev/positron) + [Ark](https://github.com/posit-dev/ark) | Alternative IDE; native R (no vscode-R) |
| [Air](https://github.com/posit-dev/air) | Formatter (already core to this skill) |
| [ellmer](https://github.com/tidyverse/ellmer), [btw](https://github.com/posit-dev/btw), [mcptools](https://github.com/posit-dev/mcptools) | LLM + MCP bridge to live R |
| [gander](https://github.com/simonpcouch/gander) / [chores](https://github.com/simonpcouch/chores) | IDE chat assistants |
| [duckplyr](https://github.com/tidyverse/duckplyr), [mirai](https://github.com/r-lib/mirai) | Performance / async |
| [`posit-dev/skills`](https://github.com/posit-dev/skills) | Quarto authoring skill companion |

## Skills ecosystem (find-skills)

Searched via `npx skills find` (R vscode, air, lintr, radian, tidyverse,
environment setup, positron, quarto). **No** high-quality dedicated “R + VS Code
environment doctor” skill found. Closest patterns:

- `flutter/skills@flutter-environment-setup-*` — doctor → install → re-check
- `posit-dev/skills@quarto-authoring` — Quarto writing (complement)
- Tiny R pattern skills (`ab604/claude-code-r-skills`, etc.) — coding style,
  not environment bootstrap

This skill adopts the **flutter-style doctor loop** and the **vscode-R + Air
official package/extension lists**, plus research Tier B and opt-in AI Tier D.

## Deliberate exclusions

- Do not vendor UsefulPapers / Sci-Hub / institutional PDF tools here
  (researchskills pack rule).
- Do not replace `ggplot-maps` or `research-project-ops`.
