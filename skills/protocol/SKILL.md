---
name: protocol
description: >-
  Guided walkthrough from a research question to a PROTOCOL.md (YAML + prose).
  Soft-hidden: prefer discover-papers as the front door; use this when the user
  wants a durable review protocol, Methods-ready search strategy, or says
  "/protocol". Staged react-to-drafts walk (not a blank form). Extraction schema
  is researchskills.extraction.v1 (in-repo). Triggers on "/protocol", "write a
  PROTOCOL.md", "define my review protocol", "lock my search strategy",
  "PICO/PCC for this review".
metadata:
  version: 0.2.0
---

# /protocol — research question → PROTOCOL.md

Soft-hidden sibling of `discover-papers`. Produce a reproducible protocol file. Do **not** invoke explore-unknowns; borrow only the interaction pattern: settled ground → react to concrete drafts → ship an artifact.

## Mental model

```text
question → scope drafts → eligibility → OpenAlex queries → seeds → screening prefs
                                ↓
                         PROTOCOL.md (YAML + prose)
```

Template: [references/protocol-template.md](references/protocol-template.md).  
Paper-card schema: [../../schemas/paper-extraction.v1.schema.json](../../schemas/paper-extraction.v1.schema.json) (`researchskills.extraction.v1`).

## Step 0 — Settled ground

Restate what you already know from the chat (topic, taxa, years, must-include/exclude). Flag assumptions. Ask **one** clarifying question only if a load-bearing gap blocks drafting.

## Step 1 — Question framework

Default **PCC** (population / concept / context) unless the user prefers PICO. Show a filled draft table for reaction (not empty fields).

## Step 2 — Eligibility

Show draft include/exclude bullets. Ask the user to steal/skip/edit. Do not proceed until they react.

## Step 3 — Search queries

Propose 3–8 OpenAlex `search.queries[]` strings. Prefer explicit queries over concatenating PCC alone. User reacts; revise.

## Step 4 — Seeds and extras

Ask for 0–N seed DOIs (optional). Note snowball / additional sources as optional PROTOCOL fields.

## Step 5 — Screening prefs

Propose defaults (AI triage on title/abstract; human confirm policy as the user prefers). Keep YAML keys stable across projects.

## Step 6 — Write the file

Write `PROTOCOL.md` at the path the user chooses (default: project root or `literature/PROTOCOL.md`). Include YAML front matter + prose Overview / Question / Eligibility / Search sections suitable for Methods. Set `extraction.schema` to `researchskills.extraction.v1`. Declare review-specific card fields under `extraction.extra_fields` (rendered into the extract prompt).

## Step 7 — Offer next step

Offer `/discover-papers` in **locked** mode on this file. Do not start an external literature-engine run unless the user asks and that tool is available.

## Composes with

- `discover-papers` — run OpenAlex from locked protocol or return here from protocol mode
- `literature-review` — extract using the in-repo paper-card schema
- `find-pdf` — after candidates are accepted
- `zotero` — export Accepted items later

## Notes

- Never require PROTOCOL.md for a one-off search — that is `discover-papers` **quick** mode.
- Quality over completeness: a short locked protocol beats an unfinished mega-protocol.
