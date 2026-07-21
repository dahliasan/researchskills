# Changelog

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
