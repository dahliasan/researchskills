# researchskills

**AI agent skills for scientific research workflows.** Manuscript writing, OpenAlex discovery, PROTOCOL.md walkthroughs, PDF finding, Zotero, and research project operations. Works with Claude Code, Codex, Cursor, and any Agent Skills host.

Packaged like [marketingskills](https://github.com/coreyhaines31/marketingskills) / [makerskills](https://github.com/coreyhaines31/makerskills): documentation-first skills, backends optional and out of band.

## Install

```bash
# CLI (recommended)
npx skills add dahliasan/researchskills

# Claude Code plugin
/plugin marketplace add dahliasan/researchskills
/plugin install researchskills@researchskills
```

Optional env for OpenAlex polite pool:

```bash
export RESEARCHSKILLS_MAILTO="you@example.com"
```

## 5-minute path

1. Install the pack.
2. Try **manuscript writing**: ask your agent to revise a Results paragraph with `/manuscript-writing`.
3. Try **discovery**: `/discover-papers` with a brain-dump question (no PROTOCOL.md required).
4. When you want a durable review, let discover offer the **protocol** walk, or run `/protocol`.

## Which skill when?

| I want to… | Skill |
|------------|--------|
| Draft, revise, or audit a research manuscript | [`manuscript-writing`](./skills/manuscript-writing/SKILL.md) |
| Find papers (OpenAlex) | [`discover-papers`](./skills/discover-papers/SKILL.md) |
| Build a PROTOCOL.md from a research question | [`protocol`](./skills/protocol/SKILL.md) |
| Scaffold, audit, or hand off a research project | [`research-project-ops`](./skills/research-project-ops/SKILL.md) |
| Get a PDF by DOI | [`find-pdf`](./skills/find-pdf/SKILL.md) |
| Search or cite from Zotero | [`zotero`](./skills/zotero/SKILL.md) |
| Semantic search in Zotero | [`zotseek`](./skills/zotseek/SKILL.md) |
| List a Zotero collection and PDF paths | [`zotero-local-library`](./skills/zotero-local-library/SKILL.md) |

`scientific-writing` remains only as a deprecated compatibility alias.

## Architecture

Skills are workflow docs. Engines and CLIs (UsefulPapers, Unpaywall, institutional fetch, Sci-Hub, Zotero MCP) stay on your machine. See [INSTALL.md](./INSTALL.md).

```text
/discover-papers          ← discovery front door
     └─ /protocol         ← optional formal scope → PROTOCOL.md
/find-pdf                 ← retrieval waterfall
/manuscript-writing       ← manuscript prose and audit
/research-project-ops     ← project state and artifact router
/zotero · /zotseek · …    ← library backends
```

## Docs

- [INSTALL.md](./INSTALL.md)
- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [EXAMPLES.md](./EXAMPLES.md)
- [CONTRIBUTING.md](./CONTRIBUTING.md)

## Related

- [usefulpapers](https://github.com/dahliasan/usefulpapers) — optional Zotero adapter and literature pipeline engine

## License

MIT — see [LICENSE](./LICENSE).
