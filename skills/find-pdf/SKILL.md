---
name: find-pdf
description: >-
  Router for obtaining a paper PDF by DOI or URL. Modes — open access / publisher
  URL, Unpaywall, Zotero native Find Available PDF, institutional library CLI
  (optional), Sci-Hub fallback, browser human-in-the-loop. Triggers on
  "/find-pdf", "get the PDF", "download full text", "Unpaywall", "fetch PDF for
  DOI". Never blocks a parent accept/discover job if PDF fails. Does not replace
  discover-papers or zotero library search.
metadata:
  version: 0.1.0
---

# /find-pdf — PDF waterfall router

skillify-shaped: detect mode (or run the full waterfall), call the right backend, report success/failure. **Never fail the parent job** solely because a PDF is missing.

See [references/waterfall.md](references/waterfall.md).

## Step 0 — Detect mode

| Signal | Mode |
|--------|------|
| User already has an `oa_url` / PDF URL | **direct** |
| "Unpaywall" / need legal OA resolve | **unpaywall** |
| Item already in Zotero; "Find Available PDF" | **zotero_native** |
| Institutional library / EZproxy / campus proxy | **institutional** (optional CLI) |
| OA + library miss; user accepts Sci-Hub risk | **scihub** |
| Publisher JS gate / paywall needing browser | **browser_hitl** |
| "get the PDF" with only a DOI | **waterfall** (try in order) |

## Waterfall order (default)

1. Direct OA URL from OpenAlex / metadata  
2. Unpaywall API (`mailto` required — reuse `RESEARCHSKILLS_MAILTO`)  
3. Zotero native attach (if item exists in Zotero)  
4. Institutional CLI if installed (Primo/LibKey/EZproxy pattern) — HITL login without asking for DevTools  
5. Sci-Hub CLI if installed and user/policy allows — polite rate limit  
6. Browser HITL for publisher-specific gates  

Stop at first real PDF (validate file magic / size; reject HTML stubs).

## Unpaywall

```bash
curl -sL "https://api.unpaywall.org/v2/${DOI}?email=${RESEARCHSKILLS_MAILTO}" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print((d.get('best_oa_location') or {}).get('url_for_pdf') or '')"
```

## Zotero native

If the parent item is in Zotero, prefer Zotero's Find Available PDF, or a local `zotero_first` PDF mode when a batch engine plugin is present. Otherwise use `zotero` skill + manual attach.

## Institutional / Sci-Hub

Documented as optional. Detect CLI on PATH. If missing, skip the mode and continue. For institutional SSO: open the library login in the agent browser and ask the user only to sign in — agents harvest session tokens; never ask users to paste DevTools JavaScript.

- Institutional (Primo/LibKey/EZproxy pattern): see [references/institutional-proxy.md](references/institutional-proxy.md)
- Sci-Hub: see [references/scihub.md](references/scihub.md) — canonical CLI: [dahliasan/scihub-pp-cli](https://github.com/dahliasan/scihub-pp-cli)

## Browser HITL

Use when HTTP clients get HTML interstitial pages. Prefer Cursor/agent browser; save PDF to the path the user named.

## Exit criteria

Report: mode used, output path or Zotero attachment status, or explicit `pdf_unavailable` without aborting the caller.

## Composes with

- `discover-papers` — candidates often include `oa_url`
- `zotero` — attach or locate existing PDFs (MCP or local scripts)
- optional local batch engine — PDF-on-accept modes when installed
