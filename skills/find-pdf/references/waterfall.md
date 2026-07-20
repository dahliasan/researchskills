# PDF waterfall

Order for **waterfall** mode:

| # | Mode | Backend |
|---|------|---------|
| 1 | direct | `oa_url` / publisher PDF URL from metadata |
| 2 | unpaywall | Unpaywall API v2 with mailto |
| 3 | zotero_native | Zotero Attachments.addAvailableFile / plugin |
| 4 | institutional | Optional library CLI + HITL SSO |
| 5 | scihub | Optional Sci-Hub CLI (throttled) |
| 6 | browser_hitl | Agent browser for JS/paywall gates |

**Policy:** never block accept/discover if all modes fail. Reject HTML stub "PDFs". Prefer legal OA paths before Sci-Hub.

Extracted from UsefulPapers D24 (`off | unpaywall | zotero_first | usefulpapers_only`) and MegaMove literature PDF auth HITL docs — generalized for public use.
