# ZotSeek reference

## Endpoint

| Field | Value |
|-------|-------|
| MCP URL | `http://localhost:23119/zotseek/mcp` |
| Host process | Zotero desktop + ZotSeek plugin |
| Bind | Typically `127.0.0.1:23119` (not LAN-exposed) |

## Remote Zotero (Dahlia)

ZotSeek on Dahlia listens on loopback only. From another Mac:

```bash
# One-shot tunnel (background)
ssh -fN -o ExitOnForwardFailure=yes -L 23119:127.0.0.1:23119 dahlia

# Or durable SSH host alias (add to ~/.ssh/config):
# Host dahlia-zotseek
#   HostName <dahlia-tailscale-or-lan>
#   User dahlia
#   LocalForward 23119 127.0.0.1:23119
#   ExitOnForwardFailure yes
#   ServerAliveInterval 30
ssh -fN dahlia-zotseek
```

Claude and Cursor both use `localhost:23119` **after** the tunnel is up.

Probe:

```bash
curl -sS -X POST http://localhost:23119/zotseek/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"0"}}}'
```

Expect `serverInfo.name` = `zotseek`.

## Harness registration

### Cursor — use stdio bridge (required)

HTTP Streamable MCP connects, then Cursor opens `GET` SSE on the same URL. ZotSeek returns `400 Endpoint does not support method` → MCP status **failed**.

```json
"zotseek": {
  "command": "/usr/bin/python3",
  "args": [
    "/Users/dennis/Developer/dahlias-skills/skills/zotseek/scripts/zotseek_stdio_mcp.py"
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

### Codex

Add an HTTP MCP entry pointing at the same URL in `~/.codex/config.toml` (see Codex MCP docs for current `http` / `url` syntax). Restart Codex.

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

## HTTP fallback (`tools/call`)

When the harness has no MCP tool but localhost answers:

```python
import json, urllib.request

URL = "http://localhost:23119/zotseek/mcp"

def rpc(method, params=None, id=1):
    body = {"jsonrpc": "2.0", "id": id, "method": method}
    if params is not None:
        body["params"] = params
    req = urllib.request.Request(
        URL,
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())

rpc("initialize", {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "agent", "version": "0"},
})
# optional: notifications/initialized
out = rpc("tools/call", {"name": "search", "arguments": {"query": "…", "max_results": 10}}, id=2)
# parse out["result"]["content"][0]["text"] as JSON string of results
```

## Boundaries vs other Zotero tooling

| Need | Use |
|------|-----|
| Semantic / passage search | ZotSeek |
| Collection membership, disk PDF paths | `zotero-local-library` |
| Export bib, cite into tex/md | `zotero` skill CLI |
| Screening + project RAG + prove | `project-corpus` |

ZotSeek does **not** replace accepted-corpus policy or citation-proof (`prove`) pipelines.
