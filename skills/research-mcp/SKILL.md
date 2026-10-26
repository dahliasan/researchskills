---
name: research-mcp
description: >-
  Local MCP aggregator (Zotero + ZotSeek + PaperKit + pp-scite) exposed to ChatGPT and
  other MCP clients through a private OpenAI tunnel or Cloudflare OAuth. Use when connecting a remote MCP
  client to Scite, private Zotero, or ZotSeek search, or when the user says
  my-research-library / research-mcp / ChatGPT research connector.
---

# Research MCP (local aggregator)

The server runs **on the machine that hosts Zotero** — no SSH tunnel to a
second machine. It is an MCP **aggregator**: on startup it connects to native
Zotero, ZotSeek and PaperKit MCP servers, re-exposes their tools namespaced by
source (`zotero_*`, `zotseek_*`, `paperkit_*`), and adds its own tools
(`scite_*`) that shell out to the unofficial **pp-scite** CLI — never the
official Scite MCP.

Use Zotero tools to manage and look up references. Use ZotSeek for semantic
library discovery and similar-paper searches. Use PaperKit when an answer needs
PDF body text: search passages, read the relevant passage/section/pages, then
check exact wording with `paperkit_verify_quotes` before citing it. Search
snippets and abstracts are navigation aids, not evidence. PaperKit's indexed
copy reflects PDFs synced into its index; after adding PDFs to Zotero, run
`paper sync-zotero --all` on the host to refresh its whole-library index, or
pass a project name to limit PaperKit to that project.

`paperkit_get_paper` can acquire and index a paper by DOI or Zotero key; it may
attach the downloaded PDF to Zotero. It is enabled separately by default even
while Zotero's other write tools remain hidden.

For private OpenAI access, `tunnel-client` runs the aggregator over stdio through
Secure MCP Tunnel. This route has no public HTTP listener and uses OpenAI tunnel
permissions instead of Cloudflare OAuth. Keep the client running for discovery
and tool calls. Verify a real ChatGPT tool call before retiring an existing route.

For clients using the public HTTPS route, a Cloudflare named tunnel forwards to
the local HTTP service. FastMCP's OIDC proxy authenticates MCP requests through a
dedicated Cloudflare Access SaaS OIDC application. The public route retains OAuth
when the separate private stdio route is enabled.

Private host wiring (paths, hostnames, tokens) lives outside this public pack:

```text
researchskills/.private/my-research-library/
```

## Operator

```bash
cd <researchskills-root>/.private/my-research-library
bin/doctor          # check Zotero / ZotSeek / PaperKit / scite reachability
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
- A `READONLY` flag (default on) hides upstream Zotero write tools.
  `paperkit_get_paper` is separately controlled by `PAPERKIT_ALLOW_GET`
  (default on); it acquires/indexes papers and may attach a PDF to Zotero.
- Upstream-down failures are surfaced as actionable tool errors ("open
  Zotero", "install/enable ZotSeek"), never silent/empty results.
- The Cloudflare OIDC app must enable refresh tokens and the connector must
  advertise/request `offline_access`; after changing provider metadata, refresh
  or recreate the ChatGPT app and authorize again.
- Do not put hostnames, tokens, team domains, or Access AUDs in this public
  skill — those stay in `.private/my-research-library/.env` (gitignored).
