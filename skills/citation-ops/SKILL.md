---
name: citation-ops
description: >-
  Day-to-day citation primitives playbook: find relevant papers for a claim,
  verify that existing citations actually support the wording, and summarise
  studies relative to a manuscript use. Prefer ZotSeek/semantic search, Zotero
  MCP, scite/pp-scite, and discover-papers over memory or keyword-only search.
  Use when the user asks to find cites, check a citation, diversify intro cites,
  summarise a paper for a sentence, or fix claim–citation fit. Does not draft
  long manuscript prose (manuscript-writing) or own DOCX roundtrip
  (manuscript-markdown). Heavier review corpora stay in literature-review.
metadata:
  version: 0.1.0
---

# /citation-ops — find · verify · summarise

Teach the agent to use **library and literature APIs correctly**, not to invent
cites from memory.

## Contract

| Guarantee | Detail |
|-----------|--------|
| Tool-first | Prefer live Zotero / ZotSeek / scite / OpenAlex over recalled DOIs |
| Claim-scoped | Every find/verify/summarise is anchored to an exact sentence or claim |
| Honest fit | Topical relatedness ≠ support; say when wording must change |
| No spam | Prefer diverse, claim-matched cites; avoid reusing the same keys across adjacent sentences |

## Modes (pick one)

| User need | Mode | First tools |
|-----------|------|-------------|
| “Find me a cite for this sentence / paragraph” | `find` | ZotSeek → Zotero tags → discover-papers if library empty |
| “Does this cite support the claim?” / year-author check | `verify` | resolve item → full text / scite → classify support |
| “Summarise this study” (for a claim or shortlist) | `summarise` | metadata + abstract → full-text excerpts if available |

If the user wants a full review corpus, synthesis matrix, or protocolled search,
hand off to **`literature-review`**. If they want prose rewritten after evidence
is clear, hand off to **`manuscript-writing`**. If they want live Zotero fields in
Word, hand off to **`manuscript-markdown`**.

---

## Shared preflight

1. Restate the **exact claim** (quote the sentence). Split multi-claim sentences.
2. Probe backends (do not pretend they work):
   - Zotero MCP tools (`zotero_*`) and/or skill **`zotero`**
   - ZotSeek (`zotseek` skill / MCP) for semantic library search
   - scite MCP or **`pp-scite`** for Smart Citations / support snippets
   - **`discover-papers`** only when the library is thin or user wants *new* papers
3. If a backend is down, say so and continue with the next-best path.

Load sibling install/config skills only when needed: **`zotero-mcp`**, **`zotseek`**.

Tool routing detail: [references/tool-map.md](references/tool-map.md).

---

## Mode `find`

**Goal:** shortlist papers that could *support* the claim, ranked for manuscript use.

### Steps

1. **Quote the claim.** Note constraints: taxon, scale, method, already-used keys in nearby paragraphs.
2. **Semantic search first** (ZotSeek `search`, or Zotero `zotero_semantic_search` if that is what the harness exposes).
   - One claim → one focused query (process + taxon/system + purpose).
   - Run 2–3 queries with different phrasings if the first set is weak.
3. **Do not rely on long-phrase keyword search** that silently collapses to one word.
   Keyword search is for exact author/title/DOI only.
4. **Use library tags** when present (e.g. `action: P1: Cite in Intro`) as prior curation signals — confirm relevance, do not auto-cite.
5. **Curate 2–4 candidates.** For each: title, year, DOI/item key, *why it fits this claim*, and reuse risk (already cited nearby?).
6. If the library lacks a good match, run **`discover-papers`** (OpenAlex), then offer to add via Zotero DOI tools.
7. Propose **APA in-text** + recommend wording only if the best paper needs a slight claim narrow.

### Anti-patterns

- Dumping 10 semantic hits without curation
- Recommending a paper already used in the previous sentence for a different claim
- Preferring a famous lab paper over a claim-matched one
- Citing from memory without resolving an item key / DOI

---

## Mode `verify`

**Goal:** classify whether the cited work supports the *specific* wording.

### Steps

1. Extract claim + citation (author, year, or citekey).
2. **Resolve identity** in Zotero (DOI → item key). Flag year/author mismatches (e.g. cited 2021, published 2020).
3. Open evidence in order of strength:
   - PDF / Zotero full text / ZotSeek passage
   - scite excerpts or Smart Citation snippets for that DOI
   - abstract only → mark evidence level `abstract-only` (not full verification)
4. Classify: `supported` | `partially-supported` | `unsupported` | `source-unavailable`.
5. If partial/unsupported: propose **narrower wording** and/or a **replacement cite** (run `find` on the corrected claim).
6. Report the supporting passage location when available (section / paraphrase carefully; no fabricated quotes).

### Anti-patterns

- Treating “same topic” as supported
- Verifying from title + abstract when the claim is methodological or quantitative
- Leaving a wrong year in the manuscript after noticing it

---

## Mode `summarise`

**Goal:** a claim-useful summary, not a generic abstract rewrite.

### Steps

1. Confirm target paper (DOI / item key) and the **use** (which manuscript claim or decision).
2. Pull metadata via Zotero; abstract via Zotero/scite/OpenAlex.
3. Prefer full-text excerpts for methods/results if the use depends on them.
4. Write a short summary with fixed slots:

```text
Paper: Author et al. (year). Title. Journal. DOI
What they did: …
What they found: …
Why it matters for [claim]: …
Limits / mismatch: …
Cite as: (Author et al., year) | Zotero key: …
```

5. If summarising a shortlist, keep each to ≤6 lines and compare *relative to the claim*.

### Anti-patterns

- Long unstructured dumps
- Hiding that you only read the abstract
- Summarising without tying back to the user’s sentence

---

## Output formats

### `find`

```text
Claim: "…"
Candidates (best first):
1. Author et al. (year) — why fit — DOI / key — reuse note
2. …
Recommend: #1 [+ optional wording tweak]
Evidence level: semantic library | OpenAlex | tagged prior
```

### `verify`

```text
Claim: "…"
Citation: Author et al. (year) → resolved DOI / key
Verdict: supported | partially-supported | unsupported | source-unavailable
Evidence: [passage / section / abstract-only]
Action: keep | reword | replace → …
```

### `summarise`

Use the slot template above.

---

## Related skills

| Skill | When |
|-------|------|
| `zotseek` | Semantic / passage search over library PDFs |
| `zotero` / `zotero-mcp` | Resolve items, tags, DOI add, metadata |
| `pp-scite` / scite MCP | Smart Citations, support snippets, tallies |
| `discover-papers` | New papers outside the library (OpenAlex) |
| `find-pdf` | Need the PDF for verification |
| `literature-review` | Protocolled review / citation-check corpus |
| `manuscript-writing` | Revise prose after evidence is settled |
| `manuscript-markdown` | Embed live Zotero fields in DOCX |

## Exit

Return the mode output. If the user next wants prose or Word fields, name the
handoff skill and stop inventing a parallel workflow.
