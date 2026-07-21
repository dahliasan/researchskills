---
name: zotseek
description: >-
  Semantic search over a Zotero library via ZotSeek MCP (search, find_similar,
  index_status). Use when the user asks for ZotSeek, semantic Zotero search,
  related papers from embeddings, manuscript citation curation from the library,
  or PDF-page snippets with zotero:// deep links. Prefer this over keyword-only
  Zotero search when relevance ranking or passage evidence matters. Not a
  substitute for project RAG or for listing a named collection
  (use zotero-local-library for collection membership and PDF paths).
metadata:
  version: 0.1.0
---

# ZotSeek (semantic Zotero MCP)

ZotSeek is a **Zotero plugin** that embeds library PDFs locally and exposes MCP tools
at `http://localhost:23119/zotseek/mcp` (same port family as the Zotero Connector).

## When to use

| Goal | Tooling |
|------|---------|
| Natural-language / semantic paper find | **ZotSeek** `search` |
| More like this paper | **ZotSeek** `find_similar` |
| Items in a named collection + PDF paths | `zotero-local-library` |
| BibTeX / cite / write collections | `zotero` |
| OpenAlex discovery (new papers) | `discover-papers` |

## Preconditions

1. **Zotero is running** with ZotSeek installed and indexed.
2. MCP registered in the harness (see [reference.md](reference.md)).
3. ZotSeek reachable on localhost:23119 (or tunneled there). If Zotero runs on another machine:

```bash
ssh -fN -L 23119:127.0.0.1:23119 your-zotero-host
# Check: lsof -i :23119
```

Smoke test: `curl -sS http://localhost:23119/zotseek/mcp` should not connection-refuse.

## Agent workflow

0. Ensure port 23119 is listening (tunnel if remote).
1. **`index_status`** — confirm `ready`, coverage, `lastIndexed`. If not ready, stop and tell the user to index in ZotSeek.
2. **`search`** — write a concrete scholarly query (species + place + process), not a single vague keyword.
3. Present results with **title, authors, year, snippet + page**, and clickable links:
   - Prefer `links.selectHttp` / `links.openPdfHttp` in clients that do not linkify `zotero://`.
4. For expansion from a known hit, call **`find_similar`** with that `itemKey`.
5. **Curate**, do not dump: mark keep / maybe / skip against the user's section goal.
6. Collection membership is **not** in ZotSeek results — cross-check with `zotero-local-library` when needed.

### Query tips

- One claim or section theme per query; run several targeted queries rather than one mega-query.
- Default `mode`: `hybrid`. Use `semantic` for paraphrase recall; `keyword` for exact author/title.
- `granularity: passages` when drafting and you need page-level quotes; `papers` for shortlists.

### Tools (names)

| Tool | Required args | Notes |
|------|---------------|-------|
| `index_status` | — | Call first |
| `search` | `query` | Optional: `max_results`, `mode`, `min_similarity`, `granularity`, `library_key` |
| `find_similar` | `item_key` | Optional: `library_key`, `max_results` |

`library_key`: omit for all indexed libraries; `user` for personal; `group:<id>` for a group.

## MCP fallback (no harness tool)

If the `zotseek` MCP server is not loaded but port 23119 is up, call JSON-RPC over HTTP (initialize → `tools/call`). Full recipe: [reference.md](reference.md).

## Setup (once per harness)

**Prefer stdio bridge in Cursor** when HTTP MCP shows SSE errors. Point at this pack's bridge script:

```json
"zotseek": {
  "command": "/usr/bin/python3",
  "args": ["/ABSOLUTE/PATH/TO/researchskills/skills/zotseek/scripts/zotseek_stdio_mcp.py"]
}
```

Use an absolute path (expand `~`). The bridge calls REST `GET /zotseek/*` on `127.0.0.1:23119`.

HTTP transport still works in clients that do not require SSE GET:

```bash
claude mcp add --transport http --scope user zotseek http://localhost:23119/zotseek/mcp
```

Details: [reference.md](reference.md).

## Related skills

- `zotero-local-library` — collection list + PDF paths
- `zotero` — local CLI / API inventory and bibtex
- `manuscript-writing` — how cites land in prose
- `discover-papers` — find new papers outside the library
