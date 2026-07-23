# EXAMPLES.md

One worked example per skill: what you say → what happens.

## research-project-ops

**You:** Scaffold this new analysis repo so an agent can resume next week.

**Agent:** Mode **scaffold** → creates minimum PROJECT.md / STATUS.md / METHODS.md / DECISIONS.md / AGENTS.md as needed; does not invent results.

## r-editor-setup

**You:** /r-editor-setup — get this machine ready for R research in Cursor.

**Agent:** Mode **doctor** → installs missing R/extensions/radian/Air → installs
Tier A+B packages (languageserver, httpgd, tidyverse, …) → `use_air()` /
workspace settings → re-doctors and verify checklist; asks before Tier C or
mass-format. If `.qmd` is in play: Quarto CLI + `quarto.quarto` only, then
recommends `npx skills add posit-dev/skills@quarto-authoring -g` (does not
vendor that skill).

## manuscript-writing

**You:** Revise this Results paragraph; keep Discussion claims out.

**Agent:** Loads `manuscript-writing` → chooses `revise` → reads `modes/revise.md` only (plus Results in `reference.md`), rewrites claim-first sentences with uncertainty, runs `skills/manuscript-writing/validator.py` on the draft.

**You:** Fix this one coauthor comment surgically.

**Agent:** Chooses `surgical-edit` → reads `modes/surgical-edit.md` only; does not load Intro/Discussion hourglasses or the full revision-pass stack.

## manuscript-markdown

**You:** /manuscript-markdown — convert this coauthor Word outline to Markdown and keep comments.

**Agent:** Step 0 checks `manuscript-markdown` on PATH (flags install if missing) → DOCX→MD with CriticMarkup preserved → places MD in the manuscript tree with provenance; does not rewrite scientific prose.

## research-red-team

**You:** /research-red-team analysis — is our two-stage model selection defensible?

**Agent:** Evidence-tiered challenge register; may run bounded reanalysis; recommends keep / change / disclose without defaulting to sunk cost.

## aic-model-selection

**You:** /aic-model-selection — cold spell × rain wins AICc by 0.3 over cold spell alone; what is the primary model?

**Agent:** Ranks within family; classifies nested near-tie; applies Arnold uninformative-parameter check; recommends primary inference model (often the simpler nested model) and softens Abstract claims.

## literature-review

**You:** Orient me on shipping exposure for migratory whales and build a core reading set.

**Agent:** Mode **orient** → applies evidence gates → routes to `discover-papers` / `find-pdf` as needed → returns candidates with access level, not invented full-text detail.

## discover-papers (quick)

**You:** Find papers on Antarctic fur seal census methods at Heard Island.

**Agent:** Mode **quick** → `openalex_search.py --query … --json` → triage table (title, year, DOI, OA URL). Offers protocol save / find-pdf / zotero.

## discover-papers (locked)

**You:** Search using our PROTOCOL.md

**Agent:** Mode **locked** → reads `search.queries[]` → one OpenAlex pass per query → deduped candidates.

## protocol

**You:** /protocol — I need a scoping review on shipping exposure for baleen whales 2015–2026.

**Agent:** Settled ground → draft PCC → include/exclude bullets for reaction → draft OpenAlex queries → writes PROTOCOL.md → offers `/discover-papers`.

## find-pdf

**You:** Get the PDF for 10.1038/nature12373

**Agent:** Waterfall: OA URL → Unpaywall → Zotero native → optional institutional/Sci-Hub → browser HITL. Reports path or `pdf_unavailable` without aborting.

## zotero / zotero-mcp / zotseek

**You:** What's in my "synthesis-2026" collection? / Install Zotero MCP / Semantically search for tidal habitat use in seals.

**Agent:** `zotero` for session work (prefer MCP tools if connected, else local scripts); `zotero-mcp` for [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp) install/config; `zotseek` for semantic hits.
