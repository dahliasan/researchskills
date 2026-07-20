---
name: discover-papers
description: >-
  Find candidate papers via OpenAlex. Front door for literature discovery.
  Modes — quick (brain dump, no PROTOCOL.md), protocol (hand off to /protocol
  then search), locked (read existing PROTOCOL.md search.queries). Triggers on
  "/discover-papers", "search OpenAlex", "find papers on", "literature search",
  "brain dump search". Does not fetch PDFs (use find-pdf) and does not replace
  Zotero semantic search (use zotseek).
metadata:
  version: 0.1.0
---

# /discover-papers — OpenAlex discovery

## Step 0 — Detect mode

| Signal | Mode |
|--------|------|
| Brain dump / one question / "just search" / no protocol file | **quick** |
| "set up a review" / "write a protocol" / wants durable Methods | **protocol** → run `protocol` skill, then continue as **locked** |
| User points at PROTOCOL.md / `search.queries` already exist | **locked** |
| Ambiguous | Ask once: quick search vs full protocol |

## Env

```bash
export RESEARCHSKILLS_MAILTO="you@example.com"   # or OPENALEX_MAILTO
```

Without mailto, the helper still sends a generic User-Agent; polite identity is strongly preferred.

## Helper script

From the researchskills root (or installed skill folder):

```bash
python3 skills/discover-papers/scripts/openalex_search.py \
  --query "Antarctic fur seal population census" \
  --mailto "${RESEARCHSKILLS_MAILTO:-}" \
  --per-page 25 \
  --max-pages 1 \
  --json
```

Or from a protocol file:

```bash
python3 skills/discover-papers/scripts/openalex_search.py \
  --protocol PROTOCOL.md \
  --json
```

## Mode: quick

1. Parse the user's brain dump into one or more search strings (confirm if ambiguous).
2. Run OpenAlex via the helper (or HTTP equivalent).
3. Present a triage table: title, year, DOI, OA landing URL, cited_by_count.
4. Offer: save as PROTOCOL.md (`protocol` skill), fetch PDFs (`find-pdf`), or add to Zotero (`zotero`).

## Mode: protocol

1. Invoke `protocol` until PROTOCOL.md exists.
2. Continue as **locked**.

## Mode: locked

1. Read PROTOCOL.md YAML.
2. Prefer `search.queries[]`. Else concatenate `question.population|concept|context` (UsefulPapers rule).
3. Apply `date_range` filters when present.
4. Run one OpenAlex search per query string; dedupe by DOI.
5. Report candidates + which query produced each hit.

## Output shape

Each candidate should include at least: `title`, `doi`, `year`, `oa_url` (if any), `openalex_id`, `cited_by_count`.

## Composes with

- `protocol` — durable review design
- `find-pdf` — full text for chosen DOIs
- `zotero` / `zotseek` — library ops after triage
- UsefulPapers engine (optional) — batch discover when installed

## Notes

- Discovery only; not citation proof or RAG.
- Never require PROTOCOL.md for quick mode.
- Respect OpenAlex rate limits; back off on HTTP 429.
