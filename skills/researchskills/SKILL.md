---
name: researchskills
description: >-
  Pack router for researchskills. Use when the user is unsure which research
  skill to run, asks for research help generally, or says "/researchskills".
  Routes to manuscript-writing, manuscript-markdown, manuscript-collab,
  figure-design, manuscript-submission, literature-review, research-red-team,
  discover-papers, protocol, find-pdf, pp-scite, research-project-ops, zotero,
  zotseek, or zotero-local-library. Does not reimplement those skills.
metadata:
  version: 0.1.6
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
| Critically stress-test a whole research project, simulate reviewer 2, or run a replication pre-mortem | `research-red-team` |
| Adapt a manuscript to a journal or prepare a submission package | `manuscript-submission` |
| Literature workflow, synthesis, citation check | `literature-review` |
| Find papers / OpenAlex / brain-dump search | `discover-papers` |
| Build or refine PROTOCOL.md from a research question | `protocol` |
| Get a PDF for a DOI or paper | `find-pdf` |
| Scite Smart Citations, search, tallies, assistant, reference-check | `pp-scite` |
| Scaffold / audit / hand off a research repo (PROJECT.md, METHODS.md, STATUS.md) | `research-project-ops` |
| Zotero search, BibTeX, cite into draft | `zotero` |
| Semantic search over Zotero PDFs | `zotseek` |
| List items in a named Zotero collection + PDF paths | `zotero-local-library` |

## Rules

1. Prefer `literature-review` for review-shaped work; prefer `discover-papers` for one-off search.
2. Use `research-red-team` for an opposing project-wide scientific lens; use `manuscript-writing` audit mode for manuscript-only coherence and prose checks.
3. Do not invent a second prose skill; always `manuscript-writing`.
4. **Default** MD↔DOCX conversion to `manuscript-markdown` (never pandoc first; never as a prose twin).
5. Use `figure-design` for visual design; keep analytical decisions with the analysis owner.
6. Use `manuscript-submission` for venue rules, reporting compliance, declarations, and package preflight. For Word file emit during packaging, invoke `manuscript-markdown`.
7. If Zotero MCP is unavailable, say so and continue with non-Zotero paths where possible.

## Exit

Name the chosen skill and invoke it.
