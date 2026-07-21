# Institutional library CLI reference (find-pdf institutional mode)

Backs the **institutional** mode of [find-pdf](../SKILL.md). Generic pattern for
academic libraries running **Primo** (discovery layer), **LibKey** (article-level
full-text linking), and **EZproxy** (off-campus authenticated proxying) — a
common stack across many university libraries, not ANU-specific.

Canonical implementation used by the author: `anulib` (ANU Library), built on
this pattern. Adapt the constants below to your own institution's Primo VID,
LibKey library ID, and EZproxy host pattern.

## Why this needs a CLI at all

Primo VE is a single-page app — the initial HTML rarely contains the LibKey
full-text link. A CLI needs to either drive a browser session or use
publisher-specific proxy-URL rewriting instead of scraping Primo's landing HTML.

## Auth workflow

**Use a real logged-in browser session**, not a bare HTTP client — institutional
SSO (Shibboleth/SAML) needs an authenticated cookie jar. Cookie import reads
from your browser's cookie store (path depends on browser/OS).

### One-time / session setup

```bash
<cli> auth setup                    # guided; picks a supported browser profile
<cli> auth setup --browser <browser> --no-wait   # re-import after login
<cli> auth status --json
```

### Login URLs to visit first (in the same browser profile the CLI reads cookies from)

1. Your institution's Primo home, e.g. `https://<vid-host>.primo.exlibrisgroup.com/discovery/search?vid=<VID>`
2. A known LibKey-linked DOI search, to confirm a **Download PDF** button appears
3. A known open-publisher DOI, to confirm the institutional access banner appears

### EZproxy token (often required separately from cookie import)

Many EZproxy deployments set a proxy session cookie (e.g. `ezproxy=...`) that
lives only in browser memory and is **not** persisted to the on-disk cookie
store — so a plain cookie-file import is not sufficient for EZproxy-proxied
publishers (e.g. Wiley, Elsevier).

On any `*.virtual.<institution>.edu` (or equivalent EZproxy host) page, in the
same browser profile, read the proxy cookie via the browser's DevTools/console
and hand it to the CLI:

```bash
<cli> auth ezproxy <token>
```

Re-run when EZproxy-proxied publisher probes return `proxy_login_required`
(the token typically expires within hours).

**Human-in-the-loop, not DevTools-for-the-user:** an agent driving a browser
should harvest this token itself via CDP/automation and ask the human only to
sign in — never ask the user to open DevTools and paste JavaScript themselves.

## Core commands

```bash
<cli> access --doi <doi> --json
<cli> fetch <doi> -o paper.pdf --json
```

Always use `--json` in agent pipelines.

## Resolution order (typical implementation)

1. Primo HTML search (usually SPA shell only — rarely yields LibKey links directly)
2. Publisher-specific candidate URLs + EZproxy host rewrite (`publisher.com` → `publisher-com.virtual.<institution>.edu`)
3. Publisher-specific full-text patterns (e.g. Wiley `/doi/pdfdirect/{doi}?download=true` on the proxied host)
4. Publishers exposing a direct `citation_pdf_url` meta tag (no proxy needed)
5. `doi.org` resolution last (often blocked for bots — a 403 here doesn't necessarily mean login failure if the publisher-specific path works)

## Error codes (typical taxonomy)

| Code | Meaning | Fix |
|------|---------|-----|
| `available` | Probe found PDF URL | — |
| `proxy_login_required` | EZproxy/Shibboleth gate hit; no proxy cookie in store | Click a LibKey link in the authenticated browser, then re-run `auth ezproxy <token>` |
| `login_expired` | Publisher session cookies stale | Re-run `auth setup` |
| `not_subscribed` | No institutional path for this title | Fall back to Sci-Hub / Unpaywall |
| `vpn_maybe_required` | Interstitial suggests VPN-gated access | Connect institutional VPN (rare if EZproxy already works) |
| `no_pdf_found` | Landing HTML has no PDF link | Check publisher page manually |

## Pitfalls

| Mistake | Reality |
|---------|---------|
| Assuming any logged-in browser works | Institutional SSO often only completes in one specific browser profile — confirm cookies actually import |
| Expecting Primo HTML scrape to work | Primo VE is an SPA; LibKey links aren't in the initial HTML |
| Treating a `doi.org` 403 as an auth failure | Often bot-blocking; check whether the publisher-specific + proxy path succeeds instead |
| Assuming cookie import alone gives full access | EZproxy-proxied publishers (Wiley, Elsevier, etc.) typically need the separate `auth ezproxy` token too |
| Merging this with a Sci-Hub-style CLI | Keep separate — cookie/proxy semantics vs. mirror semantics are different failure domains |

## Constants you'll need from your own institution

- Primo VID (institution code in the Primo URL)
- LibKey library ID (if your library uses LibKey)
- EZproxy host pattern (e.g. `{host-with-dots-as-dashes}.virtual.<institution>.edu`)

## When to use

- User is affiliated with an institution running Primo/LibKey/EZproxy, with legitimate subscription access
- Institutional pass before falling back to Sci-Hub

## When not to use

- Unpaywall / an open-access URL already resolves the PDF
- User has no affiliation with the institution the CLI is configured for
- Batch runs without periodic EZproxy token refresh
