# researchskills

**AI agent skills for scientific research workflows.** Scientific prose, OpenAlex discovery, PROTOCOL.md walkthroughs, PDF finding, and Zotero. Works with Claude Code, Codex, Cursor, and any Agent Skills host.

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
3. Try **discovery**: `/discover-papers` with a brain-dump question (no PROTOCOL.md required).
4. When you want a durable review, let discover offer the **protocol** walk, or run `/protocol`.

## Which skill when?

| I want to… | Skill |
|------------|--------|
| Unsure which skill | [`researchskills`](./skills/researchskills/SKILL.md) |
| Draft/revise scientific prose | [`scientific-writing`](./skills/scientific-writing/SKILL.md) |
| Find papers (OpenAlex) | [`discover-papers`](./skills/discover-papers/SKILL.md) |
| Build a PROTOCOL.md from a research question | [`protocol`](./skills/protocol/SKILL.md) (soft-hidden; discover can invoke it) |
| Get a PDF by DOI | [`find-pdf`](./skills/find-pdf/SKILL.md) |
| Search / cite from Zotero | [`zotero`](./skills/zotero/SKILL.md) |
| Semantic search in Zotero | [`zotseek`](./skills/zotseek/SKILL.md) |
| List a Zotero collection + PDF paths | [`zotero-local-library`](./skills/zotero-local-library/SKILL.md) |

## Architecture

Skills are workflow docs. Engines and CLIs (UsefulPapers, Unpaywall, institutional fetch, Sci-Hub, Zotero MCP) stay on your machine. See [INSTALL.md](./INSTALL.md).

```text
/discover-papers          ← front door (quick | protocol | locked)
     └─ /protocol         ← soft-hidden walk → PROTOCOL.md
/find-pdf                 ← waterfall router
/scientific-writing       ← prose SOT
/zotero · /zotseek · …    ← assume Zotero MCP / local API
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
