# researchskills

**AI agent skills for scientific research workflows.** Manuscript writing,
DOCX↔Markdown roundtrip, scientific figure design, submission packaging,
evidence-grounded literature reviews, project-wide research red teaming,
AIC/AICc model selection, OpenAlex discovery,
PROTOCOL.md walkthroughs, PDF finding, Scite CLI, Zotero, and research-project
operations. Works with Claude Code, Codex, Cursor, and any Agent Skills host.

Packaged like [marketingskills](https://github.com/coreyhaines31/marketingskills) /
[makerskills](https://github.com/coreyhaines31/makerskills):
documentation-first skills, backends optional and out of band.

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
3. Try **figure design**: ask `/figure-design` to plan or audit a scientific figure.
4. Try **research red teaming**: ask `/research-red-team` to challenge a project from premise through reproducibility.
5. Try **manuscript submission**: ask `/manuscript-submission` to inspect a target journal or run preflight.
6. Try **literature review**: ask `/literature-review` to orient around a provisional research question.
7. For direct discovery, use `/discover-papers` with a brain-dump question.
8. When you need a reproducible review, let literature-review route to `/protocol` and locked discovery.

## Which skill when?

| I want to… | Skill |
|------------|--------|
| Unsure which skill | [`researchskills`](./skills/researchskills/SKILL.md) |
| Draft, revise, storyboard, or audit a research manuscript | [`manuscript-writing`](./skills/manuscript-writing/SKILL.md) |
| Roundtrip Word DOCX ↔ Markdown (**default** MD↔Word path) | [`manuscript-markdown`](./skills/manuscript-markdown/SKILL.md) |
| CriticMarkup collab / strip agent comments / export Word for coauthors | [`manuscript-collab`](./skills/manuscript-collab/SKILL.md) |
| Plan, create, revise, or audit a scientific figure | [`figure-design`](./skills/figure-design/SKILL.md) |
| Build R/ggplot2 maps (`sf`, polar CRS, basemaps, rasters) | [`ggplot-maps`](./skills/ggplot-maps/SKILL.md) |
| Critically stress-test an entire research project | [`research-red-team`](./skills/research-red-team/SKILL.md) |
| AIC/AICc model selection (Δ, weights, nested near-ties) | [`aic-model-selection`](./skills/aic-model-selection/SKILL.md) |
| Adapt a manuscript to a journal or prepare its submission package | [`manuscript-submission`](./skills/manuscript-submission/SKILL.md) |
| Manage a preliminary, methods, or formal literature workflow | [`literature-review`](./skills/literature-review/SKILL.md) |
| Scaffold / audit / hand off a research project | [`research-project-ops`](./skills/research-project-ops/SKILL.md) |
| Set up / doctor R in Cursor or VS Code (packages, Air, radian) | [`r-editor-setup`](./skills/r-editor-setup/SKILL.md) |
| Quarto `.qmd` authoring (external) | `npx skills add posit-dev/skills@quarto-authoring -g` |
| Find papers (OpenAlex) | [`discover-papers`](./skills/discover-papers/SKILL.md) |
| Build a PROTOCOL.md from a research question | [`protocol`](./skills/protocol/SKILL.md) (soft-hidden; literature-review or discover can invoke it) |
| Get a PDF by DOI | [`find-pdf`](./skills/find-pdf/SKILL.md) |
| Scite Smart Citations / literature search CLI | [`pp-scite`](./skills/pp-scite/SKILL.md) |
| Zotero library day-to-day (MCP if present, else local API) | [`zotero`](./skills/zotero/SKILL.md) |
| Install/configure [54yyyu Zotero MCP](https://github.com/54yyyu/zotero-mcp) | [`zotero-mcp`](./skills/zotero-mcp/SKILL.md) |
| Semantic search in Zotero ([ZotSeek](https://github.com/introfini/ZotSeek) plugin) | [`zotseek`](./skills/zotseek/SKILL.md) |

## Architecture

Skills are workflow docs. Engines and CLIs (UsefulPapers, OpenAlex, Unpaywall,
institutional fetch, and Zotero MCP) stay on your machine. See
[INSTALL.md](./INSTALL.md).

```text
/literature-review       ← review-state router + evidence gates
     ├─ /protocol        ← durable scope and locked search
     ├─ /discover-papers ← external candidate discovery
     ├─ /find-pdf        ← authorised full-text retrieval
     ├─ /pp-scite        ← Smart Citations / Scite CLI
     └─ /zotero · /zotero-mcp · /zotseek · UsefulPapers
/research-project-ops    ← project artifacts, state, and handoff
/r-editor-setup          ← R env doctor: extensions, packages, Air
/research-red-team       ← independent project-wide challenge register
/aic-model-selection ← AIC/AICc ranking, near-ties, primary inference
/manuscript-writing      ← manuscript argument, prose, and audit
/manuscript-markdown     ← DOCX ↔ Markdown roundtrip (CLI + extension)
/figure-design           ← scientific figure design and QA
/ggplot-maps             ← R/ggplot2 + sf map recipes (companion)
/manuscript-submission   ← journal compliance and submission package
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
