# my-research-library MCP — Implementation Plan

> **Status (2026-09-19): SHIPPED & live.** All tasks done. T3's auth changed
> during build: ChatGPT's OAuth mode rejects a self-hosted Access app, so auth is
> now FastMCP `OIDCProxy` serving native MCP OAuth with a Cloudflare Access **SaaS
> OIDC** app as upstream login (policy: only `dahliafoo@gmail.com`). Tunnel + DNS +
> OIDC app provisioned via CF API; both launchd services loaded; endpoint verified
> (OAuth discovery 200, `/mcp` 401 without token). Remaining: final ChatGPT connect
> smoke-test (T6) by the operator. See the spec's "Resolved" section.


**Spec:** `docs/superpowers/specs/2026-09-19-my-research-library-mcp-design.md`
**Date:** 2026-09-19
**Deliverable:** a local MCP **aggregator** on Dahlia's Mac, exposed at
`https://research-library.dahlia.foo/mcp` behind Cloudflare Access
(single identity: `dahliafoo@gmail.com`), bundling native tools from
54yyyu `zotero-mcp` + ZotSeek MCP + pp-scite into one ChatGPT connector.

## Guardrails

- pp-scite only — never register `https://api.scite.ai/mcp` (AGENTS.md #1/#8).
- Private wiring lives in `researchskills/.private/my-research-library/`; public
  skills stay scrubbed of host paths, tokens, hostnames (AGENTS.md #6).
- Secrets never committed. `.private/` and creds are gitignored.

## Tasks

### T1 — Scaffold the aggregator package (grunt)
`.private/my-research-library/` with:
- `pyproject.toml` / `requirements.txt` (`fastmcp`, `httpx`, `pyjwt[crypto]`).
- `.venv`, `.env.example` (no secrets), `.gitignore`.
- `src/my_research_library/`:
  - `server.py` — FastMCP streamable-HTTP app at `/mcp`.
  - `aggregator.py` — connect upstream MCPs, list+namespace+re-expose tools.
  - `access.py` — Cloudflare Access JWT middleware (stub in T3).
  - `scite_tools.py` — pp-scite subprocess tools.
  - `status.py` — `research_status` health tool.
- `bin/serve`, `bin/doctor`.
**Accept:** `bin/serve` boots, `/mcp` responds to MCP `initialize` locally.

### T2 — Upstream aggregation (grunt)
- On startup connect: 54yyyu `zotero-mcp serve` (stdio, `ZOTERO_LOCAL=true`) and
  ZotSeek MCP (`http://127.0.0.1:23119/zotseek/mcp`).
- `tools/list` merges upstream tools, prefixed `zotero_*` / `zotseek_*`; `scite_*`
  are local. `tools/call` routes by prefix to the right upstream / handler.
- Upstream-down → tool returns actionable error, never empty (fail loud).
**Accept:** local MCP client lists tools from all three sources; a `zotero_*` and a
`zotseek_*` and a `scite_*` call each return real data with Zotero+ZotSeek running.

### T3 — Cloudflare Access verification (grunt)
- Middleware: require `Cf-Access-Jwt-Assertion`; verify sig via
  `https://<team>.cloudflareaccess.com/cdn-cgi/access/certs`, check `iss`, `aud`,
  and identity email == `dahliafoo@gmail.com`. Reject 401 otherwise.
- `READONLY` env flag: when true, hide/deny upstream write tools.
- Config via env: `ACCESS_TEAM_DOMAIN`, `ACCESS_POLICY_AUD`, `ALLOWED_EMAIL`.
**Accept:** request without a valid JWT → 401; forged/other-email JWT → 401; a valid
`dahliafoo@gmail.com` assertion → tools work. Unit test with a mock JWKS.

### T4 — Tunnel + Access provisioning (operator, needs Dahlia's CF account)
- `cloudflared tunnel create research-library`; DNS route to
  `research-library.dahlia.foo`; ingress → `http://127.0.0.1:<port>`.
- New Access application on that hostname; single allow policy `dahliafoo@gmail.com`.
- Record team domain + AUD into `.env` (gitignored).
**Accept:** `curl https://research-library.dahlia.foo/mcp` → Access challenge; after
Access login the MCP handshake succeeds.

### T5 — launchd services (grunt)
- Plists for `cloudflared` and the aggregator; auto-start on login; restart on
  crash; logs to `~/.config/my-research-library/logs/`.
**Accept:** after `launchctl load` + reboot, endpoint is up with no manual steps.

### T6 — ChatGPT connector + smoke (operator)
- Add remote MCP connector: URL `https://research-library.dahlia.foo/mcp`, name
  `my-research-library`, complete Access login as `dahliafoo@gmail.com`.
- Smoke: a scite search, a Zotero lookup, a ZotSeek semantic search from ChatGPT.
**Accept:** all three tool families return results in ChatGPT web.

### T7 — Docs (grunt)
- `.private/my-research-library/README.md`: start/stop, ChatGPT connect, teardown.
- Update public skill `research-mcp/SKILL.md` to describe the new local-aggregator
  model (no tunnel-to-Dennis), scrubbed of host paths.
**Accept:** README lets operator reconnect after reboot without re-reading the spec.

## Open questions to resolve during build
1. ChatGPT connector ↔ Access login handshake (native vs OAuth-discovery shim). [T3/T6]
2. Same-named tools across upstreams → source prefix. [T2]
3. Writes on-by-default vs `READONLY` default. [T3]

## Delegation
- **Grunt (delegate to subagent):** T1, T2, T3, T5, T7 — code, config templates,
  tests, docs. No secrets, no live CF/ChatGPT.
- **Operator (Dahlia, with agent assist):** T4, T6 — anything touching the live
  Cloudflare account, DNS, Access app, and the ChatGPT connector UI.
</content>
