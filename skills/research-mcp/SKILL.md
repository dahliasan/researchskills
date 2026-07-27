---
name: research-mcp
description: >-
  Start the ChatGPT research MCP tunnel (pp-scite + Zotero/ZotSeek). Use when
  connecting ChatGPT web Developer Mode to Scite CLI or private Zotero, or when
  the user says research-mcp-tunnel / ChatGPT Zotero MCP.
---

# Research MCP (ChatGPT)

Private host wiring lives outside the public pack. On Dennis the implementation is:

```text
researchskills/.private/research-mcp/
```

## Operator

```bash
cd "$(git -C ~/Developer/researchskills rev-parse --show-toplevel)/.private/research-mcp"
./bin/research-mcp-tunnel --bg
```

Then paste `mcp_url` + Bearer token from `~/.config/research-mcp/` into ChatGPT
Developer Mode → Connectors.

Full card: `.private/research-mcp/README.md`  
Design: `docs/superpowers/specs/2026-07-27-chatgpt-research-mcp-tunnel-design.md`  
Issue: https://github.com/dahliasan/researchskills/issues/10

## Rules

- Uses **pp-scite**, never official Scite MCP
- Zotero via local SSH tunnel skill **zotero-private** (read-only in v1)
- Do not put hostnames, tokens, or WebDAV secrets in this public skill
