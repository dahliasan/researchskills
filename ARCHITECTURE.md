# Architecture

## Public pack + private backends

```text
┌─ researchskills (this repo) ─────────────────────────────┐
│  skills/*/SKILL.md   workflow docs + thin helpers         │
│  No API keys. No personal vaults. No PDF libraries.       │
└───────────────────────────┬───────────────────────────────┘
                            │ invokes
┌───────────────────────────▼───────────────────────────────┐
│  Your machine                                              │
│  OpenAlex HTTP · Zotero/ZotSeek · Unpaywall · optional    │
│  UsefulPapers / institutional full-text tools              │
│  RESEARCHSKILLS_MAILTO in env                              │
└────────────────────────────────────────────────────────────┘
```

Same idea as makerskills `second-brain`: the skill is the workflow; the data and heavy engines stay out of git.

## Skill families

| Family | Skills | Pattern |
|--------|--------|---------|
| Pack routing | `researchskills` | Intent → sibling |
| Project operations | `research-project-ops` | Project artifacts, state, dependencies, handoff |
| Literature workflow | `literature-review` | Review mode → evidence gate → sibling/backend |
| Prose | `manuscript-writing` | Artifact-driven draft/revise/audit + lint |
| Document roundtrip | `manuscript-markdown` | **Default** DOCX ↔ Markdown (CLI/extension; not pandoc) |
| Discovery | `discover-papers`, `protocol` | Search front door + durable protocol walk |
| Full text | `find-pdf` | Waterfall router |
| Library | `zotero`, `zotseek`, `zotero-local-library` | Assume Zotero MCP/API |

## Literature workflow

```text
research-project-ops
        │ project question, methods, status
        ▼
literature-review
        ├─ protocol          durable scope and locked search
        ├─ discover-papers   OpenAlex candidates
        ├─ find-pdf          authorised full-text retrieval
        ├─ zotero/zotseek    existing project library
        └─ UsefulPapers      optional batch engine and Zotero adapter
                │
                ▼
       verified evidence artifacts
                │
                ├─ research-project-ops updates project SOT
                └─ manuscript-writing uses evidence for prose
```

`literature-review` is not the parent of project operations or manuscript writing. It is a specialist router that produces verified evidence artifacts. `research-project-ops` owns project state. `manuscript-writing` owns manuscript prose.

## Evidence gates

```text
metadata        → discovery
abstract        → initial screening
full text       → methods/results extraction
exact location  → citation verification
```

A missing PDF may leave a paper in the corpus, but it cannot be promoted to full-text verified evidence.

## discover-papers modes

```text
quick ──► OpenAlex (no PROTOCOL.md)
protocol ──► /protocol ──► locked
locked ──► PROTOCOL.md search.queries[] (else PCC concat)
```

## Composes with (optional)

- [usefulpapers](https://github.com/dahliasan/usefulpapers) — PROTOCOL.md consumer, screening pipeline, and Zotero adapter
- Institutional full-text tools — only if available and authorised

## Maintainer loop (edit → live)

```text
~/Developer/researchskills/skills/<name>/   ← edit here
        ▲
        │  ./scripts/link-global.sh  (symlink once)
        ▼
~/.agents/skills/<name>  →  ~/.cursor|claude|codex/skills/<name>
```

File edits are live. Re-run `link-global.sh` only when adding a new skill name to `skills/sets/global.txt`.

Consumers who use `npx skills add` get **copies**; they refresh with `npx skills update`, not live symlinks.

## Versioning

- Pack: `CHANGELOG.md` + `.claude-plugin/*.json` version
- Per-skill: `metadata.version` in SKILL.md frontmatter
