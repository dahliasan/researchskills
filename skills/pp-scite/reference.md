# scite search v2 filters

Endpoint: `GET /search/v2` via `scite search` and `scite search facets`.

## Common flags

| Flag | Example |
|------|---------|
| `--mode` | `all`, `papers`, `citations`, `question-answering` |
| `--term` | Cross-field query |
| `--limit` | Up to 1000 |
| `--offset` | Pagination |
| `--sort` | `date`, `total_cited`, `total_supported`, `total_contrasted`, `total_mentioned`, `total_citing_publications` |
| `--sort-order` | `asc`, `desc` |
| `--date-from` / `--date-to` | `YYYY` or `YYYY-MM-DD` |
| `--paper-type` / `--paper-types` | `review`, `article`, `preprint`, … |
| `--has-retraction` | `true` / `false` |
| `--has-concern` | editorial concerns |
| `--has-correction` / `--has-erratum` / `--has-withdrawn` | `true` / `false` |
| `--has-tally` | smart citations present |
| `--citation-types` | `supporting`, `contrasting`, `mentioning` |
| `--supporting-from` / `--supporting-to` | min/max supporting statements |
| `--mentioning-from` / `--mentioning-to` | min/max mentioning |
| `--contrasting-from` / `--contrasting-to` | min/max contrasting |
| `--citing-publications-from` / `--to` | distinct citing pubs |
| `--author` / `--authors` | author filter |
| `--journal` / `--journals` | journal filter |
| `--publisher` | publisher |
| `--section` / `--sections` | `results`, `discussion`, `methods`, `introduction`, `conclusion` |
| `--affiliation` / `--affiliations` | affiliation |
| `--topic` / `--topics` | research topic |
| `--title` / `--abstract` | field-specific text |

## Facets

```bash
scite search facets "<query>" --aggregations journals,topics --json --agent
```

## Examples

```bash
scite search "animal tracking climate" --date-from 2021 --date-to 2026 \
  --paper-type review --has-tally true --sort date --limit 50 --json --agent
```
