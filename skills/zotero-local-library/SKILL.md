---
name: zotero-local-library
description: >-
  Lists items in a named Zotero collection and resolves local PDF/file paths.
  Default backend is the Zotero 7+ local HTTP API (Web API v3 on localhost); optional
  SQLite reads zotero.sqlite when the app is closed or on older Zotero. Use when
  the user names a collection (e.g. "nz sea lion"), wants references from that
  collection, or needs paths to stored Zotero PDFs.
---

# Local Zotero library and collections

## What this enables

- List items in a **collection by name** (exact match first; otherwise substring match on the collection name).
- Read **titles**, **item keys**, and **resolved file paths** for attachments (PDFs and other linked/stored files).
- Open or read PDFs on disk using those absolute paths (e.g. with the Read tool where supported).

## Default: Zotero 7+ local API

Zotero serves a **read-only Web API v3** on **localhost** (same port family as the Connector, default base `http://127.0.0.1:23119`). The script uses:

- `GET /api/users/0/collections` (paginated)
- `GET /api/users/0/collections/{collectionKey}/items/top` (paginated)
- `GET /api/users/0/items/{itemKey}/children` for attachments

**Requirements**

1. **Zotero is running** (Zotero 7 or later with local API support).
2. **Local app access enabled**: Settings → Advanced → allow other applications on this computer to communicate with Zotero (wording may vary slightly by version).

**Optional env**

- `ZOTERO_LOCAL_API_BASE` — override API base URL (default `http://127.0.0.1:23119`).
- `ZOTERO_DATA_DIR` — data directory used only to **resolve files** under `storage/` and linked paths (default `~/Zotero` on macOS).

## Fallback: SQLite backend

Use when Zotero 6, the app is closed, or the local API is disabled:

```bash
python3 ~/.cursor/skills/zotero-local-library/query_collection.py "nz sea lion" --backend sqlite --json
```

While Zotero is running, `zotero.sqlite` is often **locked**. Prefer the default API backend, or run SQLite mode **without** `--no-copy` so the script copies the DB to a temp file. Do not write to `zotero.sqlite` from tooling.

## Agent workflow

1. Resolve the data directory if resolving paths: `ZOTERO_DATA_DIR` or `~/Zotero`.
2. Run (API default):

```bash
python3 ~/.cursor/skills/zotero-local-library/query_collection.py "nz sea lion" --json
```

3. Interpret JSON:
   - `backend`: `"api"` or `"sqlite"`
   - **API**: `matchedCollections`, `matchedCollectionKeys`, `items[].collectionKey`, `items[].itemKey`, `items[].itemVersion` (no numeric `itemID`)
   - **SQLite**: `matchedCollectionIDs`, `items[].itemID`, `items[].itemKey`
   - `items[].pdfPaths`, `items[].attachments` (`pathInDb`, `contentType`, `linkMode`, `resolvedPath`)

## Linked vs stored files

- **Stored** (`imported_file`): `{dataDir}/storage/{attachmentKey}/…`
- **Saved from the web** (`imported_url`): Zotero often still saves a copy under the same `storage/{attachmentKey}/` tree (e.g. PDF or HTML). The script resolves a local PDF there when the API omits `path` or marks URL import.
- **Linked** (`linked_file`): path on disk (absolute or relative to the data directory in some setups)

## Limitations

- **Python 3**, stdlib only (`urllib`, `json`, `sqlite3`).
- Local API requires a **compatible Zotero version** and correct preference; otherwise use `--backend sqlite`.
- Does not replace Zotero sync or the cloud Web API for remote-only libraries.

## Script

`query_collection.py` (same folder as this skill) — flags: `--backend api|sqlite`, `--api-base`, `--timeout`, `--zotero-dir`, `--no-copy` (SQLite), `--json`.
