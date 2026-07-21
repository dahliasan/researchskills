---
name: manuscript-markdown
description: >-
  Roundtrip DOCX ↔ Manuscript Markdown with Word comments, track changes,
  highlights, tables, equations, and Zotero citations via the Manuscript
  Markdown CLI and VS Code extension. Default converter for any research
  Markdown↔Word work. Use when converting .docx ↔ .md, exporting Word for
  coauthors, importing Word drafts, preserving CriticMarkup, comparing to
  pandoc, or the user says "/manuscript-markdown". Does not draft scientific
  prose (use manuscript-writing). Requires Manuscript Markdown tooling —
  stop and flag install if missing.
metadata:
  version: 0.1.1
---

# /manuscript-markdown — DOCX ↔ Markdown roundtrip

**Default** for research Markdown↔Word conversion in this pack. Convert with
**roundtrip** fidelity (comments, track changes, highlights, Zotero fields).
Do not reach for pandoc first.

**Not prose.** Argument, storyboard, and audit stay in `manuscript-writing`.

## Step 0 — Install gate (always)

Completion criterion: CLI is on `PATH` **or** you have stopped and told the
user what to install. Do not convert with a substitute without saying so.

```bash
command -v manuscript-markdown
manuscript-markdown --version
```

| Check | If missing |
|-------|------------|
| `manuscript-markdown` CLI | **Flag:** Manuscript Markdown CLI is required. Install steps → [references/install.md](references/install.md) |
| VS Code / Cursor extension `jbearak.manuscript-markdown` (human editing) | **Flag:** Extension recommended for annotations UI and right-click Export. Same install doc |

If the user only needs agent conversion, CLI alone unblocks Step 1. Still note
when the extension is absent so they can install it for editor roundtrip.

**Do not silently fall back to pandoc.** Pandoc drops Word comments and
highlights. If the user accepts pandoc after the flag, say so explicitly and
label the output as pandoc (not Manuscript Markdown).

## Step 1 — Detect mode

| Signal | Mode |
|--------|------|
| Input ends in `.docx` | **import** (DOCX → MD) |
| Input ends in `.md` | **export** (MD → DOCX) |
| "preserve comments / track changes / CriticMarkup" | **import** (or export if editing MD marks) |
| "compare to pandoc" | **compare** after import |
| "install / setup / doctor" | stop after Step 0 + [references/install.md](references/install.md) |

## Step 2 — Convert

Default CLI (direction from extension):

```bash
manuscript-markdown path/to/paper.docx --force --output path/to/paper
manuscript-markdown path/to/paper.md --force --output path/to/paper.docx
```

- DOCX → MD writes `paper.md` and, when Zotero/citation fields need export,
  `paper.bib`.
- Prefer `--force` only when overwriting is intended.
- Citation key format (DOCX → MD): `--citation-key-format authorYearTitle`
  (default) | `authorYear` | `numeric`.

Flags and edge cases → [references/cli.md](references/cli.md).
CriticMarkup marks → [references/criticmarkup.md](references/criticmarkup.md).

Completion criterion: output file exists; report path(s); if annotations were
present, mention that CriticMarkup was preserved (or that none were found).

## Step 3 — Place the artifact (when in a research repo)

- Put converted MD beside the project's manuscript tree (follow existing
  naming: e.g. `paperN-00-outline-vX.Y.md`).
- Keep a one-line provenance comment or YAML `title`/`author` from the
  converter; do not invent scientific content.
- Strip or keep CriticMarkup per user intent: **keep** for coauthor review
  history; **strip** for a clean outline fed to `manuscript-writing`.

Completion criterion: path stated; provenance noted; CriticMarkup keep/strip
decision recorded.

## Step 4 — Compare (optional)

When the user asks how this differs from pandoc: convert with both, then
diff. Typical delta: Manuscript Markdown keeps `{>>comments<<}` and
`{==highlights==}`; pandoc does not. Body prose is usually the same after
normalizing whitespace.

## Composes with

- `manuscript-writing` — draft/revise after a clean Markdown outline exists
- `manuscript-submission` — venue DOCX packaging (separate from roundtrip edit)
- `zotero` — library search; MM owns field-code roundtrip when present in DOCX

## Upstream

- Repo: [jbearak/manuscript-markdown](https://github.com/jbearak/manuscript-markdown)
- Marketplace: [Manuscript Markdown](https://marketplace.visualstudio.com/items?itemName=jbearak.manuscript-markdown)
