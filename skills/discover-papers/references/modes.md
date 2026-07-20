# discover-papers modes

| Mode | PROTOCOL.md | OpenAlex input |
|------|-------------|----------------|
| quick | not required | ad hoc queries from brain dump |
| protocol | created via `/protocol` | then locked |
| locked | required | `search.queries[]` or PCC fallback |

Query resolution matches UsefulPapers: explicit `search.queries[]` wins; else concatenate question PCC fields; else review `name`.
