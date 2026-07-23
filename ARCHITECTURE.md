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
│  project code, data readers, runtimes, and generated files │
│  RESEARCHSKILLS_MAILTO in env                              │
└────────────────────────────────────────────────────────────┘
```

Same idea as makerskills `second-brain`: the skill is the workflow; the data and heavy engines stay out of git.

## Skill families

| Family | Skills | Pattern |
|--------|--------|---------|
| Pack routing | `researchskills` | Intent → sibling |
| Project operations | `research-project-ops` | Project artifacts, state, dependencies, handoff |
| Editor tooling | `r-editor-setup` | Doctor/install R + Cursor/VS Code + packages + Air |
| Project challenge | `research-red-team` | Evidence tier → argument map → challenge register |
| AIC model selection | `aic-model-selection` | AICc ranking, near-ties, primary inference; Arnold module for nested junk params |
| Literature workflow | `literature-review` | Review mode → evidence gate → sibling/backend |
| Prose | `manuscript-writing` | Artifact-driven draft/revise/audit + lint; modes under `modes/` |
| Document roundtrip | `manuscript-markdown` | **Default** DOCX ↔ Markdown (CLI/extension; not pandoc) |
| Discovery | `discover-papers`, `protocol` | Search front door + durable protocol walk |
| Full text | `find-pdf` | Waterfall router |
| Library | `zotero`, `zotero-mcp`, `zotseek` | `zotero` day-to-day router; `zotero-mcp` = [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp) install/config; `zotseek` = [ZotSeek](https://github.com/introfini/ZotSeek) plugin |

## Peer research workflows

```text
research-project-ops
    owns project state, decisions, dependencies, and handoff

literature-review
    owns review workflow and verified literature evidence

research-red-team
    reads across the project and records evidence-linked challenges

aic-model-selection
    owns AIC/AICc ranking, near-ties, and primary inference choice

manuscript-writing
    owns manuscript argument, prose, revision, and audit
    (thin SKILL.md + modes/*.md + reference.md; one skill, not prose twins)

figure-design
    owns scientific figure planning, creation, and visual QA
```

`research-red-team` is not a parent router and does not own the artifacts it
challenges. It can hand accepted findings to peer skills:

```text
research-red-team
    ├─ project state or decision      → research-project-ops
    ├─ novelty or citation challenge  → literature-review
    ├─ figure-integrity challenge     → figure-design
    └─ manuscript wording challenge   → manuscript-writing
```

## Red-team evidence tiers

```text
Tier 1  project documentation and manuscript
Tier 2  + code, configuration, outputs, logs, history, full text
Tier 3  + data, model objects, runtime, bounded recomputation
```

The skill must state the tier used. A documentation review cannot claim to have
verified implementation or data correctness.

Default truth hierarchy:

```text
authoritative source data
→ executed outputs and logs
→ code and configuration used for the run
→ versioned generated summaries
→ verified full-text literature
→ project documentation and decisions
→ manuscript prose
→ agent memory or convention
```

Conflicts are reported rather than silently resolved.

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
- Project runtimes and data readers — used by research-red-team only when available and proportionate

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
