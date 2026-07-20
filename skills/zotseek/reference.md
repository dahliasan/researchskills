# ZotSeek reference

## Endpoint

| Field | Value |
|-------|-------|
| MCP URL | `http://localhost:23119/zotseek/mcp` |
| Host process | Zotero desktop + ZotSeek plugin |
| Bind | Typically `127.0.0.1:23119` (not LAN-exposed) |

## Remote Zotero (optional)

If ZotSeek runs on another machine and listens on loopback only:

```bash
ssh -fN -o ExitOnForwardFailure=yes -L 23119:127.0.0.1:23119 your-zotero-host
```

Clients then use `localhost:23119` after the tunnel is up.

Probe:

```bash
curl -sS -X POST http://localhost:23119/zotseek/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"0"}}}'
```

Expect `serverInfo.name` = `zotseek`.

## Harness registration

### Cursor — use stdio bridge (recommended)

HTTP Streamable MCP connects, then Cursor opens `GET` SSE on the same URL. ZotSeek may return `400 Endpoint does not support method` → MCP status **failed**.

```json
"zotseek": {
  "command": "/usr/bin/python3",
  "args": [
    "/ABSOLUTE/PATH/TO/researchskills/skills/zotseek/scripts/zotseek_stdio_mcp.py"
  ]
}
```

Script: `skills/zotseek/scripts/zotseek_stdio_mcp.py` (proxies to REST `/zotseek/search|similar|stats`). Reload MCP after edits.

### Claude Code

Prefer the same stdio entry if HTTP shows SSE Bad Request. Otherwise:

```bash
claude mcp add --transport http --scope user zotseek http://localhost:23119/zotseek/mcp
claude mcp list
```

## Tool schemas (v1.18+)

### `index_status`

No arguments. Returns JSON: `ready`, `indexedPapers`, `totalChunks`, `modelId`, `coverage`, `lastIndexed`, `storageUsedBytes`.

### `search`

| Arg | Type | Default | Notes |
|-----|------|---------|-------|
| `query` | string | required | Natural language |
| `max_results` | int 1–100 | 10 | |
| `mode` | `hybrid` \| `semantic` \| `keyword` | `hybrid` | |
| `min_similarity` | 0–1 | ZotSeek pref (~0.3) | Semantic floor |
| `granularity` | `papers` \| `passages` | `papers` | |
| `library_key` | string | all | `user` or `group:<id>` |

Each hit: `itemKey`, `title`, `authors`, `year`, `score`, `matchedChunk` (snippet, page), `links` (`select`, `openPdf`, `selectHttp`, `openPdfHttp`).

### `find_similar`

| Arg | Type | Default |
|-----|------|---------|
| `item_key` | string (8-char) | required |
| `library_key` | string | `user` |
| `max_results` | int 1–100 | 10 |

## Boundaries vs other Zotero tooling

| Need | Use |
|------|-----|
| Semantic / passage search | ZotSeek |
| Collection membership, disk PDF paths | `zotero-local-library` |
| Export bib, cite into tex/md | `zotero` skill CLI |
| Find new papers (OpenAlex) | `discover-papers` |

ZotSeek does **not** replace project-level screening or citation-proof pipelines.
