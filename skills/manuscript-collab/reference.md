# manuscript-collab — reference

## Agent author allowlist

Stripped on collaborator export (case-insensitive):

| Canonical | Also matched |
|-----------|----------------|
| Claude | `claude`, `@Claude` |
| Cursor | `cursor`, `@Cursor`, **Composer** |
| Codex | `codex`, `@Codex` |
| ChatGPT | `chatgpt`, `@ChatGPT`, `GPT`, `Chat GPT` |

Humans (e.g. `@Ada Lee`) are never stripped.

## Preferred comment form

```markdown
{>>@Claude | short note<<}
{>>@Claude (2026-07-21 14:00) | note with timestamp<<}
```

Also accepted by the stripper (legacy / informal):

```markdown
{>>Claude (2026-07-21) | Provenance: …<<}
```

## Strip rule (export)

When removing an agent comment:

1. Delete `{>>…<<}`.
2. If a `{==text==}` or `==text==` highlight immediately precedes that comment,
   unwrap to bare `text`.
3. Leave human comments alone.
4. Leave `{++}` / `{--}` / `{~~}` alone (v1).

Script:

```bash
python3 skills/manuscript-collab/scripts/strip_agent_criticmarkup.py \
  --in paper.md --out /tmp/paper.stripped.md --stats
```

## Snapshot + export

```bash
bash skills/manuscript-collab/scripts/export_for_collaborators.sh \
  paper.md share.docx --force [--archive-dir DIR] [--ensure-cli]
```

Archive default:

1. `--archive-dir` if set
2. Else walk parents for `docs/manuscript/_archive`
3. Else `<source-dir>/_archive`

Snapshot filename: `<stem>-YYYY-MM-DD-HHMM.md` with a SNAPSHOT banner.

## Address replies

Append after the human comment (do not mutate the human body):

```markdown
…prose…{>>@Ada Lee | Please expand.<<}{>>@Claude | Expanded the Methods paragraph on …<<}
```

## HTML comments

`<!-- agent-only note -->` stays invisible in Manuscript Markdown Word export.
Use for notes that should never surface as Word comments even in internal
DOCX roundtrips.

## Upstream

- Converter: [jbearak/manuscript-markdown](https://github.com/jbearak/manuscript-markdown) CLI
- Install: `skills/manuscript-markdown/references/install.md`
- Ensure helper: `scripts/ensure_manuscript_markdown_cli.sh`
