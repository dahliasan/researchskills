# Citation primitives — tool map

Use this when choosing APIs/MCP tools. Prefer the left column when available.

## Find relevant citations

| Need | Prefer | Fallback |
|------|--------|----------|
| “Papers like this claim” in *my* library | ZotSeek `search` (`hybrid`/`semantic`) | `zotero_semantic_search` |
| More like a known item | ZotSeek `find_similar` | semantic query with title+abstract terms |
| Exact author / title / DOI | `zotero_search_items` or BBT citekey | SQLite DOI index (read-only) |
| Prior “use in intro” curation | Zotero tags / collections | — |
| Nothing good in library | `discover-papers` (OpenAlex) | Crossref / scite search |
| Add missing DOI to library | `zotero_add_by_doi` | `zotero_add_by_url` (weaker for reports) |

### Query design

- Encode: **process + system/taxon + purpose** (e.g. “tracking data bias species distribution models marine”).
- Avoid mega-queries; run several short ones.
- After hits: curate keep / maybe / skip against the claim and nearby already-used keys.

## Verify existing citations

| Need | Prefer | Fallback |
|------|--------|----------|
| Resolve cite → item | DOI in Zotero / BBT key | Crossref / OpenAlex |
| Full-text support | Zotero PDF / ZotSeek passages | scite full-text excerpts |
| How others cite this paper | scite Smart Citations / tallies | — |
| Year/author sanity | metadata `date` + creators | publisher page |

### Verdict rubric

| Verdict | Meaning |
|---------|---------|
| supported | Passage/result matches the claim as written |
| partially-supported | Same direction but narrower/broader scope → reword |
| unsupported | Topic overlap only, or contradicts |
| source-unavailable | No accessible full text / abstract-only when full text required |

## Summarise studies

| Need | Prefer | Fallback |
|------|--------|----------|
| Bibliographic facts | `zotero_get_item_metadata` | Crossref |
| Claim-tied reading | ZotSeek passages / PDF pages | scite `term` excerpts on DOI |
| Quick orientation | Abstract only — **label as abstract-only** | — |

## Backend smoke checks

```bash
# Zotero local API / ZotSeek family
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:23119/

# ZotSeek MCP (if plugin enabled)
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:23119/zotseek/mcp
```

If Zotero runs on another machine, tunnel `23119` first (see `zotseek` / `zotero-private`).

## What not to use these tools for

| Task | Wrong tool | Right skill |
|------|------------|-------------|
| Rewrite intro argument | citation-ops alone | `manuscript-writing` |
| DOCX live fields | citation-ops alone | `manuscript-markdown` |
| Systematic review corpus | citation-ops alone | `literature-review` |
| Install Zotero MCP | citation-ops | `zotero-mcp` |
