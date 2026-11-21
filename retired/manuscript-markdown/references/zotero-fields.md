# Live Zotero Word fields (MD → DOCX)

Manuscript Markdown can emit real Word fields (`ADDIN ZOTERO_ITEM`), not only
plain author–year text. Use this when the user wants Zotero Refresh / style
changes in Word.

Upstream: [jbearak/manuscript-markdown](https://github.com/jbearak/manuscript-markdown)
(Zotero roundtrip docs in that repo).

## Requirements

1. YAML frontmatter names a CSL file, e.g. `csl: conservation-letters.csl`.
   Prefer the **target journal** style (cover letter / submission plan), not an
   arbitrary leftover CSL.
2. In-text cites use Pandoc form `[@citekey]` or `[@a; @b]`. Bare narrative
   `@citekey` may stay plain text unless bracketed.
3. Each cited BibTeX entry has **`zotero-key`** and **`zotero-uri`** so the
   Word plugin can bind to the library item:

```bibtex
@article{exampleKey2024,
  ...
  zotero-key = {ABCD1234},
  zotero-uri = {http://zotero.org/users/USERID/items/ABCD1234},
}
```

Without those two fields, export may still format cites via CSL, but fields
are not reliably live.

Optional YAML: `zotero-notes: in-text`, `locale: en-GB` (or the journal locale).

## CriticMarkup conflict (literal citekeys)

Cites **inside** `{++…++}` or `{--…--}` are **not** turned into Zotero fields.
They appear in Word as literal `[@citekey]`.

| Deliverable | What to do |
|-------------|------------|
| Track-change review pack | Export source MD with CM as-is; expect few/no fields in inserts |
| Live Zotero + human comments | **Export-only** preprocess: accept `{++}` / drop `{--}`; keep `{>>}` / `{==}`; then run CLI. Do not silently rewrite the review source MD |
| Clean submission / Refresh | Export live MD with no add/del marks |

See also [criticmarkup.md](criticmarkup.md).

## Bare `@key` → `[@key]` (safe)

Only convert bare `@key` when the key exists in the project `.bib`.

**Protect** existing clusters first (`[@a; @b]`). Naive replace turns
`[@a; @b]` into `[@a; [@b]]` or splits into `[@a; @b]; [@c]`.

Pattern: stash `\[@[^\]]+\]` → convert remaining bib keys → restore clusters.
Then merge accidental `[@a; @b]; [@c]` back to one cluster if needed.

## styleID after export

Embedded Zotero prefs may set:

`http://www.zotero.org/styles/<filename>.csl`

Zotero expects the CSL `<id>` **without** a trailing `.csl`, e.g.:

`http://www.zotero.org/styles/conservation-letters`

After MD→DOCX, if Refresh fails to resolve the style, patch
`docProps/custom.xml` `styleID` to match the CSL file’s `<id>` element.

## Verify

In the DOCX (`word/document.xml` / custom props):

- `ZOTERO_ITEM` count ≈ bracket citation clusters outside add/del marks
- Visible result text like `(Author Year)`, not `[@citekey]`
- `styleID` matches CSL `<id>`
- Bibliography field (`ZOTERO_BIBL`) may still be missing; insert via Zotero
  in Word if needed, then Refresh

## Citekey alignment with Better BibTeX

Manuscript citekeys should match the BBT export keys in the Zotero collection
`.bib`. Prefer renaming MD/`refs.bib` keys to BBT over trying to pin Zotero
items to old keys via the local API (local API is read-only for those writes).
Collection membership changes that local cannot do → cloud Web API with an
API key (see `zotero` skill).
