---
name: zotero-mcp
description: >-
  Install, configure, and operate the 54yyyu Zotero MCP server (zotero-mcp-server).
  Use when the user asks for Zotero MCP, zotero-mcp, richer Zotero agent tools
  (annotations, DOI add, semantic search extras), or how to connect Zotero to
  Cursor/Claude via MCP. Upstream: https://github.com/54yyyu/zotero-mcp.
  Not a Zotero .xpi plugin; not ZotSeek. For day-to-day library routing see zotero;
  for ZotSeek semantic plugin see zotseek.
metadata:
  version: 0.1.0
---

# Zotero MCP (54yyyu)

Agent skill for the **Python MCP server** that exposes a rich Zotero tool set to
Cursor, Claude, and other MCP hosts.

**Upstream (install from here):** [github.com/54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp)

This pack does **not** vendor that code. Prefer the upstream README when install
flags change. This skill is the researchskills entry point: install, detect,
route, and boundaries.

## What it is / is not

| | |
|--|--|
| **Is** | Optional MCP server package `zotero-mcp-server` (CLI `zotero-mcp`) |
| **Is not** | A Zotero Desktop `.xpi` plugin |
| **Is not** | [introfini/ZotSeek](https://github.com/introfini/ZotSeek) (separate plugin + MCP; skill `zotseek`) |
| **Is not** | The pack’s local-API CLIs (`skills/zotero/scripts/`) — those are the thin fallback |

Day-to-day library work still goes through skill **`zotero`** (router: prefer MCP
tools when connected, else local scripts). Load **this** skill when installing,
debugging MCP connection, or choosing MCP-only capabilities.

## Install

Recommended:

```bash
uv tool install zotero-mcp-server
zotero-mcp setup   # auto-configure where supported (e.g. Claude Desktop)
```

Also fine: `pip install zotero-mcp-server` or `pipx install zotero-mcp-server`,
then `zotero-mcp setup`.

Optional extras (see upstream):

| Extra | Adds |
|-------|------|
| `[semantic]` | Vector semantic search (Chroma / embeddings) |
| `[pdf]` | PDF outline / heavier PDF helpers |
| `[scite]` | Scite tallies / retraction helpers |

GUI-oriented community installer (optional): [ehawkin/zotero-mcp-setup](https://github.com/ehawkin/zotero-mcp-setup).

Full docs: [54yyyu/zotero-mcp README](https://github.com/54yyyu/zotero-mcp#readme).

## Harness config (local read-first)

Local mode needs **Zotero Desktop running** with local HTTP access enabled
(Settings → Advanced).

Minimal env: `ZOTERO_LOCAL=true`.

**Remote library on another host:** MCP still uses `127.0.0.1:23119` on the
Cursor machine. SSH-forward that port to the Zotero host, then keep
`ZOTERO_LOCAL=true`. If skill **`zotero-private`** is installed, follow it for
host-specific tunnel aliases and MCP paths (do not put those in public skills).

**Cursor** — MCP settings (stdio). Prefer absolute path if the GUI cannot see `PATH`:

```json
"zotero": {
  "command": "zotero-mcp",
  "env": {
    "ZOTERO_LOCAL": "true"
  }
}
```

Find the binary with `which zotero-mcp` or `zotero-mcp setup-info`.

**Claude Code** — e.g. in `~/.claude.json` `mcpServers`:

```json
"zotero": {
  "command": "zotero-mcp",
  "env": {
    "ZOTERO_LOCAL": "true"
  }
}
```

### Hybrid writes (optional)

Local API is largely **read-only** for library membership. For MCP writes
(add by DOI, update items, notes, attach PDF, etc.), set a Zotero Web API key +
library id
([Zotero → Settings → Security → Applications](https://www.zotero.org/settings/security#applications)):

- Keep `ZOTERO_LOCAL=true` for fast local reads
- Add `ZOTERO_API_KEY` and `ZOTERO_LIBRARY_ID` (numeric userID; for groups also
  `ZOTERO_LIBRARY_TYPE=group`)

Confirm with the user before any write.

**Where to store the API key (hosts):** prefer
`~/.config/zotero-mcp/config.json` → `client_env` (upstream loads this on
`serve`). Host overlays like **`zotero-private`** document the local helpers
`zotero-mcp-set-key` / `zotero-mcp-cred-status`. Do not commit keys.

**PDF file sync vs Zotero Storage:** MCP attachment uploads follow the library’s
Desktop sync settings. To avoid burning Zotero’s free file quota, configure
**Settings → Sync → File Syncing → WebDAV** (or turn file sync off). Host-specific
WebDAV / attach policy belongs in skill **`zotero-private`** when present — do not
put credentials in public skills.
See [WebDAV services](https://www.zotero.org/support/kb/webdav_services).

Web-only remote mode: `zotero-mcp setup --no-local --api-key … --library-id …`
(see upstream).

## Detect in-session

Look for harness MCP tools named `zotero_*`, for example:

- Search: `zotero_search_items`, `zotero_advanced_search`, `zotero_semantic_search`
- Read: `zotero_get_item_metadata`, `zotero_get_item_fulltext`, `zotero_get_collection_items`, `zotero_get_attachment_path`
- Annotations / notes: `zotero_get_annotations`, `zotero_create_note`, …
- Write: `zotero_add_by_doi`, `zotero_update_item`, `zotero_create_collection`, …

If present → use them (skill `zotero` already prefers this path).
If absent → install/configure per this skill, or fall back to `zotero` local scripts
and say MCP is not connected.

## When to prefer MCP vs siblings

| Goal | Use |
|------|-----|
| Annotations, DOI/URL/ISBN add, collection manage, rich search | **This MCP** (`zotero_*` tools) |
| BibTeX + insert cite into TeX/Markdown draft | Skill `zotero` scripts (`zotero.py cite`) even if MCP is up |
| Collection name → disk PDF paths without MCP | `zotero` → `query_collection.py` |
| Local semantic passages + `zotero://` page links | Skill `zotseek` ([ZotSeek](https://github.com/introfini/ZotSeek) plugin) |
| Scite from CLI outside MCP | Skill `pp-scite` |

54yyyu `[semantic]` and ZotSeek are **different** stacks. Prefer `zotseek` when the
user already runs the ZotSeek plugin; use MCP semantic only if that extra is
installed and indexed.

## Agent workflow

1. Confirm upstream link: https://github.com/54yyyu/zotero-mcp
2. Check whether `zotero_*` MCP tools are already available.
3. If not: give install + harness snippet; do not pretend tools exist.
4. If yes: call the matching MCP tool; confirm before writes.
5. For manuscript cite wiring, still use `zotero` / `zotero.py cite` as needed.

## Related skills

- `zotero` — session router (MCP if present, else local-API scripts)
- `zotseek` — ZotSeek plugin semantic MCP
- `pp-scite` — Scite CLI outside this MCP
- `find-pdf` — PDF waterfall when the item is not already in Zotero
