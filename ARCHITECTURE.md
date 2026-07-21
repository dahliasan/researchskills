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
│  UsefulPapers / institutional / Sci-Hub CLIs               │
│  RESEARCHSKILLS_MAILTO in env                              │
└────────────────────────────────────────────────────────────┘
```

Same idea as makerskills `second-brain`: the skill is the workflow; the data and heavy engines stay out of git.

## Skill families

| Family | Skills | Pattern |
|--------|--------|---------|
| Router | `researchskills` | Intent → sibling |
| Prose | `scientific-writing` | Standalone + validator |
| Discovery | `discover-papers`, `protocol` | Front door + soft-hidden walk |
| Full text | `find-pdf` | skillify-style mode router |
| Library | `zotero`, `zotseek`, `zotero-local-library` | Assume Zotero MCP/API |

## discover-papers modes

```text
quick ──► OpenAlex (no PROTOCOL.md)
protocol ──► /protocol ──► locked
locked ──► PROTOCOL.md search.queries[] (else PCC concat)
```

## Composes with (optional)

- [usefulpapers](https://github.com/dahliasan/usefulpapers) — PROTOCOL.md consumer / Zotero adapter
- Institutional PDF CLIs — only if on PATH

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
