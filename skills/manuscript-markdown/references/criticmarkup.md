# CriticMarkup in Manuscript Markdown

Upstream detail: [CriticMarkup docs](https://github.com/jbearak/manuscript-markdown/blob/HEAD/docs/criticmarkup.md).

Word comments / track changes / highlights import as CriticMarkup in the `.md`.

| Mark | Syntax | Meaning |
|------|--------|---------|
| Addition | `{++text++}` | Inserted |
| Deletion | `{--text--}` | Removed |
| Substitution | `{~~old~>new~~}` | Replaced |
| Comment | `{>>text<<}` | Note; attributed form `{>>@Author (date) \| text<<}` |
| Highlight | `{==text==}` | Attention |

Combined: `{==span==}{>>comment<<}`.

## Agent handling

- **Keep** marks when the deliverable is a working review draft or coauthor
  handoff.
- **Strip** marks when feeding a clean outline into `manuscript-writing`
  (unless the user wants the comment text promoted into `[TBC]` / TODO notes).
- Do not invent CriticMarkup the DOCX did not contain.

## Preview caveat

Multi-line CriticMarkup only renders cleanly in Markdown preview when the
pattern starts at the beginning of a line. Import/export and navigation still
work for mid-line marks.
