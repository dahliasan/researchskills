---
name: zotero
description: >-
  Router for Zotero library work: prefer 54yyyu Zotero MCP tools when present,
  otherwise use the pack's local-API CLI (status, search, BibTeX, cite, collection
  PDF paths). Use when the user mentions Zotero, citations, references.bib,
  BibTeX, localhost:23119, collections, or library PDFs. For semantic/passage
  search hand off to zotseek. For install/config of 54yyyu MCP, see zotero-mcp.
  Does not replace ZotSeek.
metadata:
  version: 0.2.1
---

# Zotero (router)

One skill for day-to-day Zotero work. **Probe backends first**, then pick the
strongest path that exists in this session.

- Install / debug **54yyyu Zotero MCP** → load sibling **`zotero-mcp`**
  ([github.com/54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp)).
- Semantic / embedding search via **ZotSeek plugin** → sibling **`zotseek`**
  ([introfini/ZotSeek](https://github.com/introfini/ZotSeek)).

## Route (every session)

0. **Host-private overlay** — if skill **`zotero-private`** is installed (personal
   harness), load it first. It owns tunnel / remote-library wiring for this
   machine. Public skills stay scrubbed of host paths.
1. **Detect Zotero MCP** — look for harness MCP tools whose names start with
   `zotero_` (from [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp)),
   e.g. `zotero_search_items`, `zotero_get_collection_items`,
   `zotero_get_attachment_path`, `zotero_get_item_metadata`.
2. **If MCP is present → prefer it** for library search, collection listing,
   attachment paths, metadata, annotations, DOI/URL add, notes, and other rich
   ops the MCP exposes. Do not reinvent those with shell if the MCP tool fits.
3. **If MCP is absent → use the local-API scripts** below (default path). State
   the limitations briefly when they matter.
4. **On first miss of MCP in this conversation** — tell the user once that a
   richer backend exists; point them at skill **`zotero-mcp`** and
   https://github.com/54yyyu/zotero-mcp (see [Suggest upgrades](#suggest-upgrades)).
   Then continue with the local-API fallback. Do not nag every turn.
5. **Semantic / “find by meaning” / PDF passages** → load and follow `zotseek`
   (separate plugin + MCP). Do not fake semantic search with keyword local API.

## What the scripts are for

Pack CLIs under `skills/zotero/scripts/`. Stdlib Python only. They talk to
**Zotero Desktop’s native local HTTP API** (`http://127.0.0.1:23119`) and the
connector where needed. They are the **fallback** when 54yyyu MCP is not
installed or not connected to this harness — not a full substitute for that MCP.

| Script | Role |
|--------|------|
| `zotero.py` | Enable/probe local API; inventory; keyword search; BibTeX export; insert citekeys into TeX/Markdown; children/fulltext/file-url; connector BibTeX/RIS import |
| `query_collection.py` | Resolve a **collection by name** and list items with **disk PDF paths** (API default; SQLite if app closed) |

Resolve `<researchskills-root>` as the pack root that contains `skills/`.

```bash
python3 <researchskills-root>/skills/zotero/scripts/zotero.py status --json
python3 <researchskills-root>/skills/zotero/scripts/query_collection.py "collection name" --json
```

**Not the scripts’ job:** semantic search (→ `zotseek`), Scite tallies (→ `pp-scite`
or MCP `[scite]` extra), or cloud-only libraries with no Desktop local access.

## Local-API limitations (fallback)

When using scripts only:

- Library/collection **membership writes** via local `POST` often return **501**;
  use Zotero Web API + API key (confirm with user) or MCP write tools if available.
- Keyword / metadata search only — not embedding search.
- No annotation CRUD, DOI ingest cascade, or Scite enrichment unless MCP (or
  another skill) provides them.
- Zotero Desktop must be running with local app access enabled (Settings → Advanced),
  except `query_collection.py --backend sqlite` when the app is closed.

## Prefer MCP when available (examples)

| Goal | Prefer MCP tool (if present) | Else script |
|------|------------------------------|-------------|
| Search library | `zotero_search_items` / `zotero_advanced_search` | `zotero.py search …` |
| Collection items | `zotero_get_collection_items` / `zotero_search_collections` | `query_collection.py "Name" --json` |
| PDF / attachment path | `zotero_get_attachment_path` | `query_collection.py` or `zotero.py children` / `file-url` |
| Metadata / full text | `zotero_get_item_metadata` / `zotero_get_item_fulltext` | `zotero.py` inventory/search/fulltext |
| Add by DOI / notes / annotations | MCP write/annotation tools | Say MCP (or Web API) needed; do not fake it |
| Attach PDF (binary) | MCP write only if hybrid + user OK; prefer Desktop UI | File sync may be WebDAV — follow `zotero-private` when present; do not assume Zotero Storage |
| BibTeX + insert into draft | MCP export if handy, then still wire draft | `zotero.py cite` / `export-bibtex` (skill specialty) |
| Semantic passages | **Not MCP-54yyyu by default** — use `zotseek` | — |

Manuscript citekey insertion and `references.bib` sync remain a first-class
local-script workflow even when MCP exists (`zotero.py cite`).

## Suggest upgrades

If MCP tools were **not** detected, mention once (plain language):

1. **Richer library MCP (optional):** skill **`zotero-mcp`** → install from
   [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp)
   (`uv tool install zotero-mcp-server` then `zotero-mcp setup` / harness config).
2. **Semantic search plugin (optional):** [introfini/ZotSeek](https://github.com/introfini/ZotSeek)
   — download `.xpi` from [Releases](https://github.com/introfini/ZotSeek/releases),
   install in Zotero, enable AI Agent Access; use skill `zotseek`.

Prerequisite for local scripts and for most MCP local modes: **Zotero Desktop**
running with local HTTP access allowed.

## Fast starts (local fallback)

```bash
python3 <researchskills-root>/skills/zotero/scripts/zotero.py status --json
python3 <researchskills-root>/skills/zotero/scripts/zotero.py enable --restart
python3 <researchskills-root>/skills/zotero/scripts/zotero.py search "transformer" --json
python3 <researchskills-root>/skills/zotero/scripts/zotero.py export-bibtex --out references.bib
python3 <researchskills-root>/skills/zotero/scripts/zotero.py cite --query "Attention Is All You Need" --tex paper.tex --bib references.bib --marker '<cite>'
python3 <researchskills-root>/skills/zotero/scripts/query_collection.py "nz sea lion" --json
```

## Workflow checklist

1. Route per [Route](#route-every-session) (MCP → scripts → suggest once → `zotseek` if semantic).
2. If using scripts and local API is down: `status --json`; `enable --restart` only when the user asked to operate Zotero.
3. Confirm before any library **write** (import, MCP add/update/delete, Web API collection membership).
4. **Better BibTeX:** when draft `[@keys]` disagree with BBT export, prefer renaming manuscript + `.bib` to match BBT over pinning items via writes the local API cannot do.
5. **Live Word fields (Manuscript Markdown):** enrich BibTeX with `zotero-key` / `zotero-uri`. See `skills/manuscript-markdown/references/zotero-fields.md`.

## Common local commands

```bash
python3 <researchskills-root>/skills/zotero/scripts/zotero.py status --json
python3 <researchskills-root>/skills/zotero/scripts/zotero.py probe --json
python3 <researchskills-root>/skills/zotero/scripts/zotero.py inventory
python3 <researchskills-root>/skills/zotero/scripts/zotero.py collections
python3 <researchskills-root>/skills/zotero/scripts/zotero.py search "BERT"
python3 <researchskills-root>/skills/zotero/scripts/zotero.py export-bibtex --item-key PXW99EKT
python3 <researchskills-root>/skills/zotero/scripts/zotero.py children PXW99EKT --json
python3 <researchskills-root>/skills/zotero/scripts/zotero.py cite --item-key PXW99EKT --markdown notes.md --bib references.bib --marker '<cite>'
python3 <researchskills-root>/skills/zotero/scripts/query_collection.py "Heard Island AFS" --json
```

## Output standards

- Prefer title, creators, year, Zotero item key, and BibTeX key when available.
- Zotero item keys (`PXW99EKT`) ≠ BibTeX keys (`vaswani_attention_2023`).
- Name the backend used: `mcp`, `local-api`, or `sqlite`.
- For blockers: MCP missing (suggested), Zotero app missing, local API disabled, port closed, no match, write not confirmed, or local API **501**.

## Related

- `zotero-private` — optional host overlay (remote library tunnel); load when present
- `zotero-mcp` — install/config for 54yyyu MCP
- `zotseek` — semantic / passage search

## Route details

Endpoint map for the fallback CLI: `references/local-api-routes.md`.
Cloud writes: official Web API (`https://api.zotero.org`) with an API key — not local `/api/` membership POSTs.
