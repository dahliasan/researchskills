---
name: research-mcp
description: >-
  Local MCP aggregator (Zotero + ZotSeek + pp-scite) exposed to ChatGPT and
  other MCP clients behind Cloudflare Access. Use when connecting a remote MCP
  client to Scite, private Zotero, or ZotSeek search, or when the user says
  my-research-library / research-mcp / ChatGPT research connector.
---

# Research MCP (local aggregator)

The server runs **on the machine that hosts Zotero** — no SSH tunnel to a
second machine. It is an MCP **aggregator**: on startup it connects to the
native Zotero MCP server and the ZotSeek MCP server, re-exposes their tools
namespaced by source (`zotero_*`, `zotseek_*`), and adds its own tools
(`scite_*`) that shell out to the unofficial **pp-scite** CLI — never the
official Scite MCP.

The only public surface is a single Cloudflare **named** tunnel hostname,
gated by a dedicated Cloudflare Access application (single allowed identity).
The tunnel hostname never rotates, so a remote client (e.g. ChatGPT Developer
Mode → Connectors) is configured once and survives reboots.

Private host wiring (paths, hostnames, tokens) lives outside this public pack:

```text
researchskills/.private/my-research-library/
```

## Operator

```bash
cd "$(git -C ~/Developer/researchskills rev-parse --show-toplevel)/.private/my-research-library"
bin/doctor          # check Zotero / ZotSeek / scite / upstream MCP reachability
bin/serve --bg       # start the aggregator locally
```

Full setup, launchd services, and ChatGPT connect steps:
`.private/my-research-library/README.md`
Design: `docs/superpowers/specs/2026-09-19-my-research-library-mcp-design.md`
Plan: `docs/superpowers/plans/2026-09-19-my-research-library-mcp.md`

## Rules

- Uses **pp-scite**, never official Scite MCP.
- Zotero and ZotSeek are proxied as native MCP tools (not reimplemented) —
  local Zotero API only, no Zotero Web API key needed.
- A `READONLY` flag (default on) hides upstream write tools (Zotero
  add/create/update/delete/merge). Flip deliberately, not by default.
- Upstream-down failures are surfaced as actionable tool errors ("open
  Zotero", "install/enable ZotSeek"), never silent/empty results.
- Do not put hostnames, tokens, team domains, or Access AUDs in this public
  skill — those stay in `.private/my-research-library/.env` (gitignored).
