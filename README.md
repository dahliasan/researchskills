# researchskills

**AI agent skills for scientific research workflows.** Scientific prose, evidence-grounded literature reviews, OpenAlex discovery, PROTOCOL.md walkthroughs, PDF finding, Zotero, and research-project operations. Works with Claude Code, Codex, Cursor, and any Agent Skills host.

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
2. Try **scientific writing**: ask your agent to revise a Results paragraph with `/scientific-writing`.
3. Try **literature review**: ask `/literature-review` to orient around a provisional research question.
4. For direct discovery, use `/discover-papers` with a brain-dump question.
5. When you need a reproducible review, let literature-review route to `/protocol` and locked discovery.

## Which skill when?

| I want to… | Skill |
|------------|--------|
| Unsure which skill | [`researchskills`](./skills/researchskills/SKILL.md) |
| Scaffold / audit / hand off a research project | [`research-project-ops`](./skills/research-project-ops/SKILL.md) |
| Manage a preliminary, methods, or formal literature workflow | [`literature-review`](./skills/literature-review/SKILL.md) |
| Draft/revise scientific prose | [`scientific-writing`](./skills/scientific-writing/SKILL.md) |
| Find papers (OpenAlex) | [`discover-papers`](./skills/discover-papers/SKILL.md) |
| Build a PROTOCOL.md from a research question | [`protocol`](./skills/protocol/SKILL.md) (soft-hidden; literature-review or discover can invoke it) |
| Get a PDF by DOI | [`find-pdf`](./skills/find-pdf/SKILL.md) |
| Search / cite from Zotero | [`zotero`](./skills/zotero/SKILL.md) |
| Semantic search in Zotero | [`zotseek`](./skills/zotseek/SKILL.md) |
| List a Zotero collection + PDF paths | [`zotero-local-library`](./skills/zotero-local-library/SKILL.md) |

## Architecture

Skills are workflow docs. Engines and CLIs (UsefulPapers, OpenAlex, Unpaywall, institutional fetch, and Zotero MCP) stay on your machine. See [INSTALL.md](./INSTALL.md).

```text
/literature-review       ← review-state router + evidence gates
     ├─ /protocol        ← durable review plan → PROTOCOL.md
     ├─ /discover-papers ← external candidate discovery
     ├─ /find-pdf        ← full-text waterfall router
     └─ /zotero · /zotseek · UsefulPapers
/research-project-ops    ← project artifacts, state, and handoff
/scientific-writing      ← manuscript prose SOT
```

## Docs

- [INSTALL.md](./INSTALL.md) — env vars and optional backends
- [ARCHITECTURE.md](./ARCHITECTURE.md) — public pack vs private backends
- [EXAMPLES.md](./EXAMPLES.md) — what you say → what happens
- [CONTRIBUTING.md](./CONTRIBUTING.md)

## Related

- [usefulpapers](https://github.com/dahliasan/usefulpapers) — optional Zotero adapter + literature pipeline engine

## License

MIT — see [LICENSE](./LICENSE).
