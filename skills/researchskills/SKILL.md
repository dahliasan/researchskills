---
name: researchskills
description: >-
  Pack router for researchskills. Use when the user is unsure which research
  skill to run, asks for research help generally, or says "/researchskills".
  Routes to manuscript-writing, literature-review, discover-papers, protocol,
  find-pdf, research-project-ops, zotero, zotseek, or zotero-local-library.
  Does not reimplement those skills.
metadata:
  version: 0.1.1
---

# /researchskills — pack router

Pick the narrowest sibling skill. Then load and follow that skill.

## Route

| Intent | Skill |
|--------|--------|
| Draft, revise, or audit manuscript prose | `manuscript-writing` |
| Literature workflow, synthesis, citation check | `literature-review` |
| Find papers / OpenAlex / brain-dump search | `discover-papers` |
| Build or refine PROTOCOL.md from a research question | `protocol` |
| Get a PDF for a DOI or paper | `find-pdf` |
| Scaffold / audit / hand off a research repo (PROJECT.md, METHODS.md, STATUS.md) | `research-project-ops` |
| Zotero search, BibTeX, cite into draft | `zotero` |
| Semantic search over Zotero PDFs | `zotseek` |
| List items in a named Zotero collection + PDF paths | `zotero-local-library` |

## Rules

1. Prefer `literature-review` for review-shaped work; prefer `discover-papers` for one-off search (it can offer `protocol`).
2. Do not invent a second prose skill; always `manuscript-writing`.
3. If Zotero MCP is unavailable, say so and continue with non-Zotero paths where possible.

## Exit

Name the chosen skill and invoke it.
