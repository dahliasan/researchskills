# my-research-library MCP — Zotero + pp-scite for ChatGPT (easy, hardened tunnel)

**Status:** ready-for-agent
**Repo:** researchskills (private overlay owns machine wiring)
**Date:** 2026-09-19
**Supersedes:** `2026-07-27-chatgpt-research-mcp-tunnel-design.md` (torn down 2026-09-19)
**Related skills:** `pp-scite`, `zotero`, `zotseek`, `zotero-mcp`
**Connector name (in ChatGPT):** `my-research-library`

## Problem Statement

We want Scite (via **pp-scite**, never official Scite MCP), Zotero keyword/collection
lookup, and ZotSeek semantic search available in **ChatGPT web and phone** — plus
desktop clients — with a setup that is **easy** (stable URL, auto-starting, nothing
to re-paste after reboot) and **safe** (a public endpoint that a leaked URL alone
cannot read).

The previous `research-mcp` failed on both counts: it ran on Dennis (not the Zotero
host, so it needed an SSH forward), used a Cloudflare **quick** tunnel whose URL
**rotated on every restart**, had four fragile moving parts, and left an
account-linked App-SDK connector that was hard to delete.

## Decisions (locked)

| Question | Decision |
|----------|----------|
| Reach from | **ChatGPT web + phone**, and desktop clients |
| Where the server runs | **On the Zotero host** (Dahlia's Mac) — no SSH forward |
| Tunnel | **Cloudflare *named* tunnel** (stable hostname), run as a service |
| Hostname | `research-library.dahlia.foo` (your Cloudflare zone) |
| Security | **OAuth via FastMCP OIDCProxy**, upstream = Cloudflare Access SaaS OIDC, single email |
| Tool surface | **Aggregate all native MCP tools** from ZotSeek + Zotero MCP + pp-scite |
| Connector name | `my-research-library` |

### Auth — OAuth (OIDCProxy) over Cloudflare Access OIDC

**As-built note:** the first cut used a self-hosted Access application that gates at
the edge and injects `Cf-Access-Jwt-Assertion`. That works for a browser but
**ChatGPT's remote-connector OAuth mode rejects it** ("MCP server does not implement
OAuth") because a self-hosted app 302-redirects the OAuth discovery requests instead
of serving JSON. The self-hosted app was created then **deleted**; the shipped design
is OAuth-native:

- **Server implements MCP OAuth** via FastMCP's `OIDCProxy`: it serves
  `/.well-known/oauth-authorization-server`, `/.well-known/oauth-protected-resource`,
  `/authorize`, `/token`, `/register` (dynamic client registration) and
  `/auth/callback`, and gates `/mcp` on the token it issues. These discovery/registration
  endpoints are public JSON (no edge gate in front) so ChatGPT can complete the flow.
- **Upstream login = Cloudflare Access SaaS (OIDC) application.** OIDCProxy delegates
  the actual login to it, so authentication still runs through Cloudflare Access and
  is restricted by an Access **policy allowing only `dahliafoo@gmail.com`**.
- **Team domain:** `dfoo.cloudflareaccess.com`. The SaaS app exposes standard OIDC
  discovery/authorize/token/jwks under `…/cdn-cgi/access/sso/oidc/<client_id>/…`.
- **Redirect:** the SaaS app's redirect URI is `https://research-library.dahlia.foo/auth/callback`
  (OIDCProxy's default `redirect_path`). ChatGPT/Claude connector callbacks are
  allowed via `allowed_client_redirect_uris`.
- **Independent:** its own app, client_id/secret, and policy — shares nothing with
  Nowhere/Selva.

## Architecture

```
ChatGPT (web / phone / desktop)
        │  MCP OAuth: discovery → DCR → /authorize → login → /token → Bearer
        ▼
Cloudflare named tunnel (stable hostname research-library.dahlia.foo)
        ▼
cloudflared (launchd service, on Dahlia's Mac)
        │  localhost
        ▼
my-research-library MCP server  (HTTP /mcp, localhost only)
        │  ├── OIDCProxy: serves /.well-known/*, /authorize, /token, /register,
        │  │   /auth/callback; login delegated upstream to Cloudflare Access SaaS
        │  │   OIDC (policy: only dahliafoo@gmail.com); gates /mcp on issued token
        │  │
        │  AGGREGATOR — merges upstream native MCP tool lists + own tools:
        ├── scite_*     → own tools, shell out to `scite` / `scite-pp-cli`
        ├── zotero…     → proxy 54yyyu zotero-mcp (native tools, as-is)
        └── zotseek…    → proxy ZotSeek MCP  127.0.0.1:23119/zotseek/mcp (native, as-is)
```

The server is an **MCP aggregator/gateway**: it starts/connects the upstream native
MCP servers, exposes their tools under one connector (namespaced to avoid
collisions), and adds its own pp-scite tools. Everything from the server inward is
`localhost` on the Zotero host — no SSH, no second machine. The only public surface
is one Cloudflare hostname, gated by Access.

## Why this is *easy*

- **Stable URL.** A *named* tunnel has a fixed hostname
  (`research-library.dahlia.foo`). It never rotates, so the ChatGPT connector is configured **once**
  and survives reboots. (Quick `trycloudflare.com` tunnels — the thing that broke
  last time — are banned by this spec.)
- **Auto-start.** `cloudflared` and the MCP server both run as **launchd** agents
  on login; nothing to remember to start. Health survives reboot and Zotero
  restarts (server reconnects to `:23119` on demand).
- **One-time ChatGPT setup.** Add the connector URL + auth once. No re-paste ever.

## Why this is *safe*

**OAuth login through Cloudflare Access, scoped to exactly one identity:**

1. **Single-identity Access policy.** No token is issued unless the caller logs in
   through the Cloudflare Access SaaS OIDC app, whose policy allows only
   `dahliafoo@gmail.com`. No one else — not even other emails on the account — can
   authenticate.
2. **Tokens gate the tools.** `/mcp` requires a valid OIDCProxy-issued Bearer token;
   the public endpoints are only the OAuth discovery/registration metadata.
3. **Secrets stay on the host.** Scite/Zotero credentials never leave the Mac;
   ChatGPT only ever sees tool results.
4. **Kill switch.** Stop `cloudflared`, delete the tunnel, or disable the SaaS OIDC
   app / its policy → access is severed instantly.

**Trade-offs accepted:**
- Cloudflare named tunnel terminates TLS at the Cloudflare edge (CF can see
  plaintext) — chosen deliberately for the stronger Access identity gate over
  Tailscale Funnel's E2E passthrough.
- **Aggregating all native tools includes Zotero writes** (see below). Because the
  gate is a single-email Access policy on a read/write personal library, the risk is
  bounded to *your own* authenticated access. An optional `READONLY=true` server
  flag can hide write tools if you want to re-tighten later.

## Tool Surface — all native tools, aggregated

Per decision, the connector exposes **every native MCP tool** from the upstream
servers, merged under one endpoint (names namespaced per source to avoid
collisions), plus the pp-scite tools:

- **pp-scite (own tools):** `scite_search`, `scite_paper`, `scite_tally` (+
  credential-gated `scite_assistant`, `scite_reference_check`).
- **Zotero (54yyyu `zotero-mcp`, native, as-is):** full toolset — search, collection
  items, item metadata, attachment paths, annotations, notes, add-by-DOI/URL, etc.
  (This is where the **write** tools come from.)
- **ZotSeek MCP (native, as-is):** semantic `search`, `find_similar`,
  `index_status`, PDF-page snippets with `zotero://` deep links.

All tool results are passed through; large payloads are truncated/limited so ChatGPT
context is not flooded.

## Implementation Decisions

- **Server = MCP aggregator/gateway.** Python (`fastmcp` streamable-HTTP at `/mcp`).
  On startup it launches/connects the upstream native MCP servers, lists their tools,
  and re-exposes them (namespaced) alongside its own pp-scite tools. Prefer a proven
  MCP-proxy/aggregation lib over hand-rolled routing; silence the FastMCP banner.
- **Auth = FastMCP `OIDCProxy`** (in `auth_provider.py`, wired as `FastMCP(auth=…)`).
  `config_url` = the SaaS OIDC discovery URL, `client_id`/`client_secret` from the
  SaaS app, `base_url` = the public host, `redirect_path=/auth/callback`,
  `allowed_client_redirect_uris` = ChatGPT/Claude callbacks. `DEV_SKIP_ACCESS=true`
  disables auth for local dev only.
- **Scite backend:** wrap **pp-scite** only (`scite … --agent --json`). Do **not**
  register `https://api.scite.ai/mcp`. Token in `~/.config/scite-pp-cli/`.
- **Zotero backend:** proxy the 54yyyu **`zotero-mcp`** (already installed at
  `~/.local/bin/zotero-mcp`, `ZOTERO_LOCAL=true` → `127.0.0.1:23119`). Reuse its
  native tools rather than reimplementing.
- **ZotSeek backend:** proxy `127.0.0.1:23119/zotseek/mcp`; if absent, its tools
  surface a clear "install/enable ZotSeek" error (skill `zotseek`), never empty.
- **Location:** private overlay `researchskills/.private/my-research-library/` on
  Dahlia's Mac. Public skills stay scrubbed of host paths / tokens / hostnames
  (AGENTS.md non-negotiable #6).
- **Named tunnel:** remotely-managed `cloudflared` tunnel `research-library`, ingress
  → `http://127.0.0.1:8731`, DNS CNAME `research-library.dahlia.foo` → the tunnel.
  Run via `bin/cloudflared-run` (token in `~/.config/my-research-library/tunnel-token`,
  chmod 600 — kept out of the plist).
- **Access:** a **dedicated Cloudflare Access SaaS (OIDC)** app as the OAuth upstream,
  with a single allow policy for `dahliafoo@gmail.com`. Independent of Nowhere/Selva.
- **Services:** launchd plists for both `cloudflared` and the aggregator; a
  `research_status` tool reports tunnel, Access, Scite binary, Zotero, ZotSeek, and
  each upstream MCP connection separately.
- **No cloud App-SDK connector.** Register in ChatGPT as a standard remote MCP
  connector (URL + Access), not a published "App" — teardown stays one click.

## Setup Flow (one time)

1. Create the remotely-managed tunnel + ingress + DNS CNAME to
   `research-library.dahlia.foo` (via CF API); save the tunnel token (600).
2. Create the Cloudflare Access **SaaS OIDC** app (redirect
   `https://research-library.dahlia.foo/auth/callback`) + a policy allowing only
   `dahliafoo@gmail.com`; put client_id/secret/discovery URL in `.env`.
3. Drop launchd plists for `cloudflared` and the aggregator; load them.
4. In ChatGPT → Settings → Connectors (Developer mode) → add remote MCP
   (Connection = **Server URL**, not Tunnel): URL
   `https://research-library.dahlia.foo/mcp`, name `my-research-library`,
   Authentication = **OAuth**; complete the Cloudflare login as `dahliafoo@gmail.com`.
5. Done — reboots and Zotero restarts need no re-setup.

## Preconditions

1. Zotero Desktop open on this Mac; local API + ZotSeek AI Agent Access on.
2. External library drive mounted (if the library lives there).
3. `scite` / `scite-pp-cli` and 54yyyu `zotero-mcp` on PATH.
4. `cloudflared` installed; `dahlia.foo` on this Cloudflare account
   (single-level subdomain → covered by Universal SSL, no ACM needed).

## Failure Modes (fail loud)

Upstream Zotero / ZotSeek tools must surface an actionable error — "open Zotero",
"mount the library drive", "install/enable ZotSeek", "upstream MCP not connected" —
instead of empty results, so a half-up environment is obvious. This is the specific
regression from the old stack we are fixing.

## Non-Goals (v1)

- Zotero **Web API** (cloud) backend — local API is richer (ZotSeek, PDF paths) and
  needs no key; revisit only for off-Mac unattended access.
- Running the server on any host other than the Zotero host.
- Publishing a cloud App-SDK connector.
- Multi-user access — policy is single-email by design.

## Resolved (during build)

1. **ChatGPT connector handshake — RESOLVED.** A self-hosted Access app fails
   ChatGPT OAuth ("does not implement OAuth"); replaced with FastMCP `OIDCProxy`
   serving native MCP OAuth, upstream login via Cloudflare Access SaaS OIDC.
2. **Namespacing — RESOLVED.** Zotero mounted un-namespaced (already `zotero_*`,
   bare `search`/`fetch` renamed to `zotero_search`/`zotero_fetch`); ZotSeek mounted
   under `zotseek`; scite tools are local `scite_*`.
3. **Write-tool posture — RESOLVED.** Shipped `READONLY=true` default (write tools
   hidden); flip `READONLY=false` in `.env` to expose them.

## Open Questions

1. **Refresh tokens:** the SaaS OIDC app was created with `authorization_code` only
   (Cloudflare required extra refresh-token options); sessions re-auth on expiry.
   Add the `refresh_tokens` grant later if re-login frequency is annoying.
2. **`allowed_client_redirect_uris`:** currently a wildcard list for ChatGPT/Claude;
   tighten to exact callback URLs once confirmed from a live connect.
