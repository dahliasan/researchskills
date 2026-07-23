---
name: researchskills
description: >-
  Pack router for researchskills. Use when the user is unsure which research
  skill to run, asks for research help generally, or says "/researchskills".
  Routes to manuscript-writing, manuscript-markdown, manuscript-collab,
  figure-design, ggplot-maps, manuscript-submission, literature-review,
  research-red-team, aic-model-selection, discover-papers, protocol,
  find-pdf, pp-scite, research-project-ops, r-editor-setup, zotero, zotero-mcp,
  or zotseek. Does not reimplement those skills.
metadata:
  version: 0.2.0
---

# /researchskills — pack router

Pick the narrowest sibling skill. Then load and follow that skill.

## Route

| Intent | Skill |
|--------|--------|
| Draft, revise, storyboard, or audit manuscript prose | `manuscript-writing` |
| Roundtrip DOCX ↔ Markdown (default MD↔Word path) | `manuscript-markdown` |
| CriticMarkup collab, address review comments, or export Word without agent comments | `manuscript-collab` |
| Plan, create, revise, or audit a scientific figure | `figure-design` |
| Build R/ggplot2 maps (`sf`, polar CRS, basemaps, rasters) | `ggplot-maps` |
| Critically stress-test a whole research project, simulate reviewer 2, or run a replication pre-mortem | `research-red-team` |
| AIC/AICc model selection, Δ/weights, nested near-ties, primary inference | `aic-model-selection` |
| Adapt a manuscript to a journal or prepare a submission package | `manuscript-submission` |
| Literature workflow, synthesis, citation check | `literature-review` |
| Find papers / OpenAlex / brain-dump search | `discover-papers` |
| Build or refine PROTOCOL.md from a research question | `protocol` |
| Get a PDF for a DOI or paper | `find-pdf` |
| Scite Smart Citations, search, tallies, assistant, reference-check | `pp-scite` |
| Scaffold / audit / hand off a research repo (PROJECT.md, METHODS.md, STATUS.md) | `research-project-ops` |
| Install / doctor R env in Cursor or VS Code (packages, Air, radian, httpgd) | `r-editor-setup` |
| Zotero library day-to-day (prefer MCP if present, else local API) | `zotero` |
| Install/configure 54yyyu Zotero MCP | `zotero-mcp` |
| Semantic search over Zotero PDFs (ZotSeek plugin) | `zotseek` |

## Rules

1. Prefer `literature-review` for review-shaped work; prefer `discover-papers` for one-off search.
2. Use `research-red-team` for an opposing project-wide scientific lens; use `manuscript-writing` audit mode for manuscript-only coherence and prose checks.
3. Use `aic-model-selection` for AIC/AICc tables, Δ/weights, nested near-ties, and primary inference choice; do not expand it into a general stats skill.
4. Do not invent a second prose skill; always `manuscript-writing`.
5. **Default** MD↔DOCX conversion to `manuscript-markdown` (never pandoc first; never as a prose twin).
6. Use `figure-design` for visual design QA; use `ggplot-maps` for R map recipes. Keep analytical decisions with the analysis owner.
7. Use `manuscript-submission` for venue rules, reporting compliance, declarations, and package preflight. For Word file emit during packaging, invoke `manuscript-markdown`.
8. Zotero: `zotero` for session work; `zotero-mcp` for [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp) install/config; `zotseek` for ZotSeek semantic. If backends are down, say so and continue without Zotero where possible.
9. Use `r-editor-setup` for R + Air editor tooling; do not bury that in `ggplot-maps` or analysis scripts.

## Exit

Name the chosen skill and invoke it.
