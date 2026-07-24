# Changelog

## 0.2.10 — 2026-07-23

- Own paper-card extraction in-repo: `schemas/paper-extraction.v1.schema.json`
  (`researchskills.extraction.v1`). PROTOCOL template and literature-review
  extract mode use the in-repo schema. Field shape matches the former external
  `*.extraction.v3` card for migration.
- Scrub product-name coupling to an external batch literature engine from
  skills and pack docs; keep optional-engine language only.
- Add PROTOCOL-templated extraction prompt
  (`skills/literature-review/references/extraction-prompt.md`) plus
  `render_extraction_prompt.py` and `validate_extraction.py`.

## 0.2.9 — 2026-07-23

- Restructure `manuscript-writing` for progressive disclosure: thin `SKILL.md`
  (gates + router), mode files under `modes/`, scaffolding examples in
  `scaffolding.md`, section contracts SSOT in `reference.md`. Same skill, not
  split into prose twins. Skill version 3.6.0.

## 0.2.8 — 2026-07-23

- Rename/expand `aic-uninformative-parameters` → `aic-model-selection`: broader
  AIC/AICc selection concept (Δ, weights, cross-family rule, primary inference
  choice) with Arnold (2010) uninformative-parameters as a module under
  `references/`.

## 0.2.7 — 2026-07-23

- Add AIC near-tie concept skill (initially `aic-uninformative-parameters`;
  superseded by `aic-model-selection` in 0.2.8).
- Wire into pack router, `global.txt`, README, ARCHITECTURE, EXAMPLES,
  validation.

## 0.2.6 — 2026-07-23

- Add `zotero-mcp` skill: install/config reference for
  [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp) (does not vendor the
  server). Wire into pack router, `global.txt`, README, INSTALL, ARCHITECTURE.
- `zotero` router points install/debug at `zotero-mcp`.

## 0.2.5 — 2026-07-23

- Collapse Zotero into one router skill: remove `zotero-local-library`; move
  `query_collection.py` under `skills/zotero/scripts/`.
- `zotero` prefers [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp) when
  connected, else local-API scripts; suggests MCP/ZotSeek install once if missing.
- Keep `zotseek` for [introfini/ZotSeek](https://github.com/introfini/ZotSeek).

## 0.2.4 — 2026-07-23

- Add `r-editor-setup`: Cursor/VS Code R environment skill (doctor → install →
  packages → Air project wiring), grounded in VS Code / vscode-R / Air /
  `usethis::use_air()` docs plus Datanovia-style verify checks.
- Package tiers: editor (languageserver, httpgd, …), research baseline
  (tidyverse, renv, conflicted, …), domain (incl. duckplyr/mirai), opt-in AI
  (ellmer, btw, mcptools); Positron/Ark noted in `modern-tooling.md`.
- Quarto policy: env skill installs/checks CLI + extension only; Quarto
  authoring stays upstream (`npx skills add posit-dev/skills@quarto-authoring -g`);
  documented in INSTALL.md companion skills (no in-pack fork by default).
- Wire into pack router, `skills/sets/global.txt`, and validation.
- Link Zotero download targets: [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp),
  [introfini/ZotSeek](https://github.com/introfini/ZotSeek) releases.

## 0.2.3 — 2026-07-22

- Add `ggplot-maps` companion skill: R/ggplot2 + `sf` map stacks, polar CRS, basemaps, rasters, and export recipes.
- Wire `ggplot-maps` into pack router, `figure-design` companions, `skills/sets/global.txt`, and validation.
- Add deep-research reference `layouts-and-colour.md` (patchwork layouts, Okabe–Ito/Tol/viridis/scico, journal export).

## 0.2.2 — 2026-07-21

- Add `manuscript-markdown` for DOCX ↔ Markdown roundtrip via the Manuscript Markdown CLI/extension (install gate; CriticMarkup references).
- Make `manuscript-markdown` the **default** MD↔DOCX path (AGENTS + pack router; pandoc only opt-in).
- Route table, README, ARCHITECTURE, EXAMPLES, and pack validation updated.

## 0.2.1 — 2026-07-21

- Remove deprecated `scientific-writing` skill; `manuscript-writing` is the only prose skill.

## 0.2.0 — 2026-07-21

- Add `literature-review` router with evidence gates and artifact contracts.
- Add `manuscript-writing` as the manuscript prose/audit source of truth.
- Point pack validation at `skills/manuscript-writing/validator.py`.
- Update pack router, README, ARCHITECTURE, and EXAMPLES for the peer skill layout.

## 0.1.1 — 2026-07-21

- Add `research-project-ops` (scaffold/audit/handoff research repos).
- Add `./scripts/link-global.sh` for live maintainer installs across harnesses.

## 0.1.0 — 2026-07-21

- Initial public pack: researchskills router, scientific-writing, discover-papers, protocol (soft-hidden), find-pdf, zotero, zotseek, zotero-local-library.
- Validate gate: frontmatter, required scripts, plugin JSON, scrub check, offline tests.
- Docs: ARCHITECTURE.md, EXAMPLES.md.
