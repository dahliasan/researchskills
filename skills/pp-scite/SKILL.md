---
name: pp-scite
description: "Unofficial Scite CLI for Smart Citations, literature search, assistant Q&A, and reference-check. Triggers: scite search, scite assistant, smart citations, citation tally, use scite, pp-scite."
author: "dahlia"
license: "Apache-2.0"
argument-hint: "<command> [args]"
allowed-tools: "Read Bash"
metadata:
  openclaw:
    requires:
      bins:
        - scite-pp-cli
---

# Scite — Printing Press CLI

Unofficial Scite client for agents and citation pipelines. Not affiliated with
Scite. Use your own credentials and follow [Scite's terms](https://scite.ai/terms).

Built from Printing Press run `20260612-141029` plus hand-coded commands for
search filters, assistant, reference-check, and optional MCP OAuth token reuse.

## Install

```bash
git clone https://github.com/dahliasan/scite-pp-cli.git
cd scite-pp-cli
go build -o scite ./cmd/scite-pp-cli
mkdir -p ~/.local/bin
ln -sf "$(pwd)/scite" ~/.local/bin/scite

scite doctor --json
```

Binary names: `scite` (symlink) or `scite-pp-cli` (module default).

## Auth

Prefer your own Scite credential:

1. `export SCITE_BEARER_AUTH="<your-token>"`
2. Or `scite auth set-token` → `~/.config/scite-pp-cli/config.toml`
3. Optional fallback: if you already authenticated Scite MCP via `mcp-remote`,
   the CLI may reuse that OAuth access token from `~/.mcp-auth/`

Search, tallies, and papers often work without auth. Assistant and
reference-check typically need a paid/subscription credential.

## Core capabilities

### Literature search with filters

```bash
scite search "polar bear range shift" --date-from 2021 --paper-type review \
  --has-retraction false --limit 20 --json --agent
```

`GET /search/v2` (~60/min). Filter reference: [`reference.md`](reference.md).

### Facet discovery

```bash
scite search facets "marine megafauna" --aggregations journals,topics --json --agent
```

### Assistant

```bash
scite assistant ask "What is CRISPR?" --wait --json --agent
scite assistant poll <task-id> --wait --json --agent
```

Prefer `scite assistant` over `api-partner … assistant` when your subscription
token returns 403 on partner routes.

### Reference check

```bash
scite reference-check submit --pdf manuscript.pdf --json --agent
scite reference-check wait <task-id> --json --agent
scite reference-check report-url <task-id> --json --agent
```

### Tallies / papers

```bash
scite tallies get-tally-doi-get 10.1038/s41586-020-2012-7 --json --agent
scite papers get-doi-get 10.1038/s41586-020-2012-7 --json --agent
```

## Agent mode

`--agent` → `--json --compact --no-input --no-color --yes`

Use `--select field1,field2` to shrink large search responses.

## Command routing

| User intent | Command |
|-------------|---------|
| Search literature | `scite search "<q>"` or `scite scite-search --term "<q>"` |
| Filtered / facet search | flags on `search` or `search facets` |
| Smart citation counts | `scite tallies get-tally-doi-get <doi>` |
| Paper metadata | `scite papers get-doi-get <doi>` |
| Research Q&A | `scite assistant ask "<q>" --wait` |
| Audit manuscript refs | `scite reference-check submit --pdf <path>` |
| Health / auth | `scite doctor --json` |

## Search filters (summary)

See [`reference.md`](reference.md) in this repo.

Key flags: `--date-from`, `--date-to`, `--paper-type`, `--has-retraction`,
`--supporting-from`, `--citation-types`, `--sort`, `--mode`.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Auth errors (exit 4) | Set `SCITE_BEARER_AUTH` or run `scite auth set-token` |
| Assistant 403 on api-partner | Use `scite assistant ask` with your subscription token |
| Reference-check auth | Paid license + `scite auth set-token` or MCP login |
| Search 429 | Throttle to ~60 requests/minute |

## Exit codes

0 success · 2 usage · 3 not found · 4 auth · 5 API · 7 rate limit · 10 config

## Direct use workflow

1. `which scite` — install if missing (see above)
2. Match intent to table above
3. Run with `--agent`
4. Parse JSON `.results` or envelope from `--json` output
