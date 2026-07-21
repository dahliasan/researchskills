# CLI reference — Manuscript Markdown

Upstream: [docs/cli.md](https://github.com/jbearak/manuscript-markdown/blob/HEAD/docs/cli.md).

## Direction

Inferred from the input extension:

| Input | Output |
|-------|--------|
| `.docx` | `.md` (+ `.bib` when citation fields export) |
| `.md` | `.docx` (loads sibling `.bib` when present) |

```bash
manuscript-markdown paper.docx
manuscript-markdown paper.md
manuscript-markdown paper.docx --force --output /tmp/draft
```

`--output` for DOCX→MD is a **base path** (derives `.md` / `.bib`). For MD→DOCX
it is the literal `.docx` path.

## Common flags

| Flag | Direction | Notes |
|------|-----------|-------|
| `--force` | both | Overwrite existing outputs |
| `--citation-key-format` | DOCX→MD | `authorYearTitle` (default), `authorYear`, `numeric` |
| `--bib` | MD→DOCX | Explicit BibTeX path |
| `--template` | MD→DOCX | Style template DOCX |
| `--no-template` | MD→DOCX | Do not reuse existing DOCX styles |
| `--author` | MD→DOCX | Document author (default: OS user) |
| `--always-use-comment-ids` | DOCX→MD | ID-based overlapping comments |
| `--pipe-table-max-line-width` | DOCX→MD | Default 120; `0` forces HTML tables |
| `--grid-table-max-line-width` | DOCX→MD | Default 120 |

## What this preserves (vs pandoc)

| Feature | Manuscript Markdown | Typical pandoc |
|---------|---------------------|----------------|
| Body headings / lists | Yes | Yes |
| Word comments | CriticMarkup `{>>…<<}` | Usually dropped |
| Highlights | `{==…==}` | Usually dropped |
| Track changes | CriticMarkup add/del/sub | Limited / lost |
| Zotero fields | Roundtrip + optional `.bib` | Citekeys only if already text |
| Equations | LaTeX ↔ OMML | Varies |

Use Manuscript Markdown as the **default** MD↔DOCX path. Use pandoc only when
the user opts in after the install/compare flag (and label that output as
pandoc).
