# ChatGPT research MCP tunnel (pp-scite + Zotero private)

**Status:** ready-for-agent  
**Repo:** researchskills (private overlay for machine wiring)  
**Related:** Litbase remote MCP (`heardislandafs` `./bin/litbase-tunnel`), skills `pp-scite`, `zotero-private`

## Problem Statement

ChatGPT web (Developer Mode connectors) can only call remote HTTPS MCP servers. Today Scite access for agents is the local `pp-scite` CLI, and Zotero/ZotSeek run as stdio MCP on Dennis over an SSH tunnel to Dahlia. Neither path is reachable from ChatGPT, so literature search and library lookup stay stuck in Cursor/Claude.

The operator does **not** want ChatGPT wired to the official Scite hosted MCP (`https://api.scite.ai/mcp`). Behavior and auth must go through the Printing Press Scite CLI (`pp-scite` / `scite-pp-cli`).

## Solution

Ship one remote research MCP facade on Dennis, exposed via Cloudflare tunnel (same operator pattern as Litbase), that ChatGPT connects to as `{PUBLIC_URL}/mcp`.

The facade:

- Invokes **pp-scite** for literature search, tallies, papers, and optional assistant/reference-check
- Proxies **read** Zotero and ZotSeek tools through the existing Dahlia SSH forward (`127.0.0.1:23119`)
- Leaves Cursor/Claude stdio MCP configs unchanged

Operator flow: ensure Dahlia Zotero is up → `ssh -fN dahlia-zotseek` → start research tunnel → paste MCP URL into ChatGPT Developer Mode.

## User Stories

1. As a researcher on ChatGPT web, I want to search literature via pp-scite filters, so that I get the same agent-oriented Scite results I use in Cursor without using official Scite MCP.
2. As a researcher on ChatGPT web, I want citation tallies and paper metadata by DOI via pp-scite, so that I can inspect Smart Citation balance in chat.
3. As a researcher on ChatGPT web, I want optional Scite assistant Q&A via pp-scite when credentials allow, so that subscription features work from ChatGPT the same as the CLI.
4. As a researcher on ChatGPT web, I want to search my Zotero library by keyword/collection/tag, so that I can find items already in my private library.
5. As a researcher on ChatGPT web, I want ZotSeek semantic search over my library, so that passage-level retrieval works without leaving ChatGPT.
6. As a researcher on ChatGPT web, I want clear errors when Dahlia Zotero or the SSH tunnel is down, so that I know to open Zotero / re-run the tunnel instead of assuming empty results.
7. As an operator on Dennis, I want one start command that brings up the HTTP MCP + Cloudflare public URL, so that ChatGPT setup is copy-paste.
8. As an operator on Dennis, I want the Dahlia SSH forward checked (or started) before advertising healthy Zotero tools, so that half-up tunnels fail loudly.
9. As an operator, I want Cursor and Claude stdio MCP entries left alone, so that local agent workflows do not regress.
10. As an operator, I want Scite credentials to stay on Dennis (`SCITE_BEARER_AUTH` / pp-scite config), so that ChatGPT never stores my Scite token.
11. As an operator, I want Zotero WebDAV and local-API secrets to stay on Dahlia/Dennis, so that ChatGPT only receives tool results over the authenticated tunnel.
12. As an operator, I want v1 tools to be read-first (no PDF attach / no library writes), so that ChatGPT write mistakes cannot corrupt the library.
13. As an operator, I want a health endpoint that reports tunnel, Scite binary, and Zotero reachability separately, so that debugging is fast.
14. As an operator, I want rate limits and compact JSON on Scite tools, so that ChatGPT context is not flooded by large search payloads.
15. As an agent implementer, I want the facade to shell out to `scite … --agent` rather than reimplement Scite HTTP, so that CLI and ChatGPT stay in lockstep.
16. As an agent implementer, I want Zotero tools to reuse zotero-mcp / zotseek bridge behavior, so that tool names and semantics match Cursor.
17. As a security-conscious operator, I want ChatGPT auth that matches Developer Mode constraints (OAuth, no-auth, or mixed — not “paste bearer in UI”), so that the connector actually connects.
18. As a security-conscious operator, I want ephemeral or rotating public URLs plus auth, so that a leaked trycloudflare URL alone is not enough to read my library.
19. As a documentation consumer, I want a short operator card (start, ChatGPT connect steps, stop), so that I can reconnect after reboot without re-reading the design.
20. As a skill maintainer, I want public `pp-scite` / `zotero` docs scrubbed of hostnames while private `zotero-private` owns Dahlia wiring, so that researchskills stays publishable.
21. As a future implementer, I want optional OpenAPI Actions export as a fallback like Litbase, so that Custom GPT Actions work if MCP connectors misbehave.
22. As a researcher, I want collection-scoped Zotero search for manuscript collections (e.g. NZSL), so that ChatGPT can stay inside one project bibliography.
23. As a researcher, I want DOI lookup that returns whether the paper is already in Zotero, so that I can avoid duplicate adds later.
24. As an operator, I want logs for facade tool calls without dumping fulltext PDFs into logs, so that debugging stays safe.
25. As an operator, I want the facade to refuse Zotero Storage-oriented attach flows, so that WebDAV policy from zotero-private is preserved even if write tools are added later.

## Implementation Decisions

- **Single seam:** one HTTP MCP facade process on Dennis (`research-mcp` or similar name). ChatGPT talks only to `{PUBLIC_URL}/mcp`. Tests and operator docs treat this as the only product boundary.
- **Scite backend:** wrap **pp-scite** / `scite-pp-cli` only. Do **not** proxy or register official `https://api.scite.ai/mcp`. Tool surface maps CLI intents: search, search facets, tallies by DOI, papers by DOI; optional assistant and reference-check behind feature flags / credential checks.
- **Zotero backend:** keep `ZOTERO_LOCAL=true` path via existing `dahlia-zotseek` SSH LocalForward to `127.0.0.1:23119`. Facade calls existing zotero-mcp / zotseek bridge logic (subprocess or in-process adapter), not a new Zotero Web API client for reads.
- **Transport:** streamable HTTP MCP at `/mcp`, modeled on Litbase `serve_remote` + `cloudflared tunnel --url`. Prefer reuse of Litbase tunnel script patterns (token file under `~/.config/…`, `--bg`, deploy JSON with `mcp_url`) rather than inventing a second tunnel style.
- **Auth for ChatGPT:** Developer Mode supports OAuth / no-auth / mixed, not a first-class “API key” field. Implement either (a) a minimal OAuth shim that issues tokens matching a local shared secret, or (b) mixed auth with public `initialize`/`list` and protected tools — document the chosen option. Curl/local health checks may still use Bearer for operator convenience.
- **Default tool policy v1:** read-only. Expose search/metadata/collections/tags/ZotSeek. Do not expose attach, create item, merge, or batch write. Writes stay out of scope until a later ticket.
- **Home for code:** private-capable packaging under researchskills (e.g. `.private/` or a small sibling module referenced by `zotero-private`), with a scrubbed public operator skill pointing at the start command. Do not put Dahlia hostnames or tokens in public skill bodies.
- **Cursor compatibility:** do not change `~/.cursor/mcp.json` stdio entries as part of this work; ChatGPT is an additional consumer.
- **Health:** `/health` returns structured status for `scite_bin`, `scite_auth_configured`, `zotero_port`, `zotseek`, `tunnel` without leaking secrets.
- **Companion skills (optional install, not blockers):** `openai/skills@chatgpt-apps`, `mcp-use/mcp-use@chatgpt-app-builder`; existing `mcp-builder` for server shape.

## Testing Decisions

- Good tests assert **external behavior** at the facade: HTTP status, tool list, tool result shapes, and failure modes — not internal CLI argv construction details beyond contract snapshots.
- **Modules under test:** the research MCP facade (primary); tunnel start script (smoke); adapters that call pp-scite and Zotero bridges (contract tests with fixtures / recorded CLI JSON).
- **Prior art:** Litbase remote MCP health + ChatGPT connector checklist in heardislandafs Litbase remote plan; pp-scite `--agent` JSON envelopes; zotero-private tunnel probe (`zotero.py status --json`).
- **Acceptance checks:**
  1. With tunnel up and Scite credential present, ChatGPT (or MCP inspector) can run a pp-scite search and get JSON hits.
  2. With Dahlia Zotero + SSH forward up, ChatGPT can run a Zotero search and get library hits.
  3. With SSH forward down, Zotero tools return an actionable error; Scite tools still work.
  4. Official Scite MCP URL is not referenced in config, docs, or code paths for this facade.
  5. Cursor stdio zotero/zotseek/scite continue to work unchanged after facade install.

## Out of Scope

- Wiring ChatGPT to official Scite MCP
- Zotero write/attach tools (WebDAV attach policy deferred)
- Moving the Zotero library onto Dennis or into cloud Zotero Storage
- Replacing Litbase / corpus MCP (separate product)
- Publishing a public ChatGPT plugin / App Store listing
- VPS hosting of the facade (Dennis + cloudflared is the v1 deploy)
- Changing Scite.terms compliance beyond “use your own credential”

## Further Notes

- Quick Cloudflare URLs rotate; operator docs should say “re-copy URL after restart” unless a named tunnel is added later.
- pp-scite doctor currently reports auth not configured until `SCITE_BEARER_AUTH` or `scite auth set-token` is set; ChatGPT assistant/reference-check tools should degrade gracefully when auth is missing.
- If ChatGPT OAuth friction blocks first connect, temporary no-auth on an ephemeral URL is acceptable for personal use only — document the risk.
- Next workflow after this spec: `/to-tickets` into tracer bullets (tunnel script, scite tools, zotero tools, ChatGPT auth, operator docs).
