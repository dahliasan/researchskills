# EXAMPLES.md

One worked example per skill: what you say → what happens.

## research-project-ops

**You:** Scaffold this new analysis repo so an agent can resume next week.

**Agent:** Mode **scaffold** → creates minimum PROJECT.md / STATUS.md / METHODS.md / DECISIONS.md / AGENTS.md as needed; does not invent results.

## scientific-writing

**You:** Revise this Results paragraph; keep Discussion claims out.

**Agent:** Loads `scientific-writing`, rewrites claim-first sentences with uncertainty, runs `validator.py` on the draft.

## discover-papers (quick)

**You:** Find papers on Antarctic fur seal census methods at Heard Island.

**Agent:** Mode **quick** → `openalex_search.py --query … --json` → triage table (title, year, DOI, OA URL). Offers protocol save / find-pdf / zotero.

## discover-papers (locked)

**You:** Search using our PROTOCOL.md

**Agent:** Mode **locked** → reads `search.queries[]` → one OpenAlex pass per query → deduped candidates.

## protocol

**You:** /protocol — I need a scoping review on shipping exposure for baleen whales 2015–2026.

**Agent:** Settled ground → draft PCC → include/exclude bullets for reaction → draft OpenAlex queries → writes PROTOCOL.md → offers `/discover-papers`.

## find-pdf

**You:** Get the PDF for 10.1038/nature12373

**Agent:** Waterfall: OA URL → Unpaywall → Zotero native → optional institutional/Sci-Hub → browser HITL. Reports path or `pdf_unavailable` without aborting.

## zotero / zotseek / zotero-local-library

**You:** What's in my "synthesis-2026" collection? / Semantically search for tidal habitat use in seals.

**Agent:** `zotero-local-library` for collection+PDF paths; `zotseek` for semantic hits; `zotero` for BibTeX/cite.
