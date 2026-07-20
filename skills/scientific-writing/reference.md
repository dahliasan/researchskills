# Scientific writing style guide

Companion to [SKILL.md](SKILL.md). **Portable:** no repository paths or project tooling; local overlays for tools and templates live in project docs (see §24).

## 1. Purpose and audience

- Write to make the reader’s job **easy**, not to show how smart you are.
- Assume a scientifically literate reader in your field:
  - Do not explain standard, textbook concepts.
  - Do define study-specific terms, ambiguous concepts, and non-standard uses (e.g. exactly what you mean by “foraging effort”).
- For public or policy pieces: lower the assumed background, use plainer language, but keep key technical terms when they carry real precision.

## 2. Core style principles

- Clear, simple, precise, meaningful. Plain language where possible, technical language where necessary.
- One main idea per sentence; one main idea per paragraph.
- Aim for brevity at the **word** level: remove words that don’t change meaning.

**Rule of thumb:** if you can’t read a sentence aloud in one breath while keeping the thread, rewrite it.

### 2.1 Concision vs brevity (genre and meaning)

Concision is **not** the same as low total word count. A short abstract can still waste words, and a long Methods or theory section can stay meaningful to the last sentence if each unit does work for that genre ([Thomson, 2026](https://patthomson.net/2026/04/12/key-word-concision/)). **Concision** means clarity about what you mean and stripping **excess** wording. **Being short** can mean deleting qualifications or steps the reader still needs, which hurts meaning.

- **Work inside the genre.** An article Introduction must establish context, gap, and contribution efficiently because readers skim for relevance. A Methods chapter may need to show reasoning behind design choices. A theoretical section may need staged definitions. Each has a different legitimate length; concision still applies so the piece does not run **past** what that job requires (for example, repeating the same point across consecutive paragraphs in different words).
- **Cut excess words, not required meanings.** Prefer strong verbs over nominalisations when the process does not need to be treated as an object (“investigate” rather than “conduct an investigation into”; “contribute to” rather than “make a contribution to”), but keep nominalisations when the discipline routinely uses them as stable terms.
- **Throat-clearing:** drop openings that delay the claim (“It is important to note that…”, “In order to understand this, it is first necessary to…”) unless the sentence truly orients a reader who needs extra context (for example mixed-audience briefings).
- **Hedging:** hedges are often necessary for honest uncertainty, but **stacked** hedges (“It could perhaps be argued that in some cases there may be a tendency for…”) usually add length without sharpening what is and is not known. Prefer one calibrated hedge tied to evidence.
- **Repetition vs elaboration:** elaboration adds a new angle, contrast, or evidence. Repetition restates the **same** claim in new words and often signals the writer has not settled the clearest single formulation yet. Fix the underlying meaning, then say it once well (pedagogical or informal pieces may deliberately repeat for accessibility; dense research prose usually should not).
- **Long documents:** excess wears readers down more in a thesis or long synthesis than in a paragraph, because there is more of it. Showing reasoning and tracing methods can be **legitimate** length; padding is not.
- **Revision habit:** reread with **impatience**. Where does the prose drag? Which sentence duplicates the previous one? What is the sentence **before** your key claim doing, and can it go if it overshoots the job?

## 3. Sentences and paragraphs

- Prefer simple or moderately complex sentences; keep most under 25 words.
- Use explicit subjects and strong verbs; avoid long strings of prepositional phrases.
- Start each paragraph with a clear topic sentence; everything after should support or develop that idea.
- Avoid tangents and repetition; say each important thing once, as clearly as possible.

**Revision checklist:**

- Split sentences that contain more than one core idea.
- Shorten or remove redundant phrases and repeated points.

## 4. Verbs, voice, and tense

- Prefer **active voice** when it doesn’t distort meaning (“We measured dive depth…”, “Females foraged primarily along the shelf break…”).
- Use precise action verbs; avoid relying on “is, has, occurs, appears, seems” where a stronger verb exists.
- **Past tense** for methods and specific results (“we collected”, “we found”); **present tense** for general truths and interpretations (“fur seals typically forage at…”).
- Replace patterns like “is characterized by” with direct verbs (“shows”, “consists of”).

## 5. Technical terms and jargon

- Use domain-specific terms when they add real precision; do not replace them with vague synonyms just to sound “simple”.
- Briefly define non-standard or ambiguous terms on first use (especially key ones like “foraging trips”, “foraging effort”, “foraging habitat”, “foraging success”), e.g. “We define foraging effort as the time spent in dives classified as search and capture behavior based on X criteria.”
- Avoid decorative jargon and unexplained acronyms: spell out on first use (“boosted regression tree (BRT)”, “sea-surface temperature (SST)”), then use the abbreviation consistently.

**Heuristic:** no more than one potentially unfamiliar term per sentence for your intended reader.

## 6. Noun stacks and abstractions

- Avoid long noun strings like “Indian Ocean sector process questions.” Prefer clauses: “questions about ecosystem processes in the Indian Ocean sector.”
- Use concrete subjects where possible (“The study region influences regional management…” vs “The influence of the study region on regional management…”).
- If you see more than two nouns in a row, consider rewriting.

## 7. Structure of a paper or section

IMRAD roles at a glance: **§19** (table). Each section has one job; do not repeat the same content across sections (no results smuggled into Introduction, no new primary results in Discussion).

## 8. Citations: general principles

- Citations are **evidence**, not decoration. Use them to support specific claims, methods, or contrasts.
- Every substantive claim that depends on prior work should have a citation placed as close as possible to that claim.
- Cite only what you have actually read and used; don’t pad reference lists.

## 9. How to place citations

### 9.1 Brackets only (no author-in-narrative)

**House convention (this plugin):** the **only** acceptable in-text form is bracketed author–date at the end of the clause — in Pandoc deliverables, `[@citekey]` (citeproc renders author–year).

**Do not** weave surnames into prose for attribution:

- Not “Smith et al. showed…”
- Not “Smith (2020) found…” or “Smith et al., 2018” inline without citekeys
- Not “Smith et al. [@smith2020]” (redundant author before bracket)

State the finding; let the bracket carry the source.

**Examples (Pandoc markdown):**

- **Good:** “Core habitat covers 63% of combined range [@sequeira2025globaltr].”
- **Bad:** “Sequeira et al. found that core habitat covers 63% of range [@sequeira2025globaltr].”
- **Bad:** “Core habitat covers 63% of range (Sequeira et al., 2025).” — use `[@sequeira2025globaltr]` instead.

`bash literature/run.sh prose-lint` enforces this deterministically where patterns allow; semantic misfits still need human or POLISH pass review.

### 9.2 Claim-proximate citation placement (required)

**Standard name:** *claim-proximate citation placement* (also: claim-specific attribution, granular in-text citation).

**Anti-patterns to avoid:** *citation clustering*, *umbrella citations*, *reference stacking* (several sources piled at the end of a compound sentence or bullet so the reader cannot tell which paper supports which clause).

- Place citation(s) immediately after the statement they support, before the period in name-year styles.
- When a sentence or bullet contains **multiple distinct claims**, split the sentence or attach **separate citation clusters** to each relevant clause.
- **Executive summaries and synthesis bullets:** each number, mechanism, taxon-specific point, or governance claim gets its own cluster unless every co-cited source supports that exact assertion.

**Better:** “Krill dominates female diets at some subantarctic archipelagos [@smith2018], whereas females at the comparison site take a more mixed diet [@jones2020].”

**Worse:** “Smith et al. (2018) showed krill dominates female diets at some archipelagos, whereas Jones and Lee (2020) found a more mixed diet at the comparison site.”

**Also worse:** “Krill dominates female diets at some subantarctic archipelagos, whereas females at the comparison site take a more mixed diet [@smith2018; @jones2020].”

The better version makes it obvious which study supports which statement.

### 9.3 Grouping citations (co-citation)

- Group multiple sources in one set of brackets only when they **all** support the **same** claim or pattern.
- Do not dump a large mixed list after several different claims; that forces readers to guess which paper supports what.
- If you need to show different types of support (e.g. diet vs movement), use separate clauses or sentences with their own citation clusters.

**Guiding idea:** never make the reader guess which paper justifies which assertion.

## 10. Study-level scaffolding and integrating prior work

- Use scaffolding phrases only when they genuinely orient the reader (“In this study, we test whether…”, “Here, we extend previous work by…”).
- Avoid vague or empty scaffolding (“Many studies have been conducted regarding…”, “It is important to note that…”).
- When bringing in prior work, use simple, informative verbs: neutral (“showed”, “reported”, “found”, “documented”); comparative (“contrasted with”, “extended”, “refined”, “challenged”).

**Example:** “Previous work shows female fur seals at krill-rich archipelagos rely heavily on krill [@smith2018; @brown2019]. Here, we test whether females at our study site show a similarly krill-dominated diet.”

## 11. Don’t over-scaffold: prioritize findings

- Lead with the **finding**, not the study story. Most of the time, readers want the result, not the recruitment details.
- **Avoid:** “Smith et al. (2018) conducted a study in which they examined X and found that…”
- **Prefer:** “X occurs more frequently in Y than Z [@smith2018].”

Include brief study details only when they change what the result **means** for your argument (method affects interpretation; system/time period is crucially different; you are explicitly comparing methods or systems across studies).

**Heuristic:** delete any extra study description that you could remove without changing your argument; if nothing breaks, keep it out.

## 12. Background and literature: enough, not everything

- Keep background and literature review tightly aligned with your research question and hypotheses.
- Group studies by idea or pattern, not as one-by-one mini-summaries: “Several studies report krill-dominated female diets in subantarctic archipelagos A; B; C, whereas others describe mixed diets in more diverse prey fields D; E.”
- Avoid information overload: synthesize what matters for **this** study, not catalogue the entire field.

## 13. Drafting guardrails (collaborators and writing assistants)

Assistants should follow **§§8–12** (citations and literature), **§18** (lint), and **§17** (keep process or contributor signposting out of the article body). No extra rules beyond those sections.

---

## 14. Punctuation: em dashes, colons, semicolons

Prefer words that show logical links (“because”, “although”, “so”, “however”, “for example”) over em dashes, colons, and semicolons in body prose (titles may use colons more freely; see §14.2).

### 14.1 Em dashes (—)

- **Do not use em dashes** in prose that follows this guide. That includes clause glue **and** so-called emphasis. There is no “one per page” exception.
- They hide the logical link and encourage long, wandering sentences. Use two sentences, a comma plus conjunction, or “because”, “although”, “so”, “for example”, as the sense requires.

**Examples**

- Instead of: “Foraging effort increased in winter—conditions likely reduced prey availability.”  
Prefer: “Foraging effort increased in winter, likely because conditions reduced prey availability.”
- Instead of: “These results are encouraging—they show that…”  
Prefer: “These results are encouraging because they show that…”

### 14.2 Colons (:)

- **Default:** avoid colons in running text almost always.
- Do not use a colon where “because”, “such as”, “for example”, or “namely” would make the relationship clearer.
- **Acceptable (sparingly):** before a **short** list only when the lead-in is a **complete sentence** and the list is easy to scan. Prefer rewording if the sentence is already dense.
- Titles and headings may use colons for punchy clarification more freely than body prose.

**Examples**

- Instead of: “The main point is this: trend estimates are heterogeneous.”  
Prefer: “The main point is that trend estimates are heterogeneous.”
- For “three drivers” lists, prefer plain glue, not a colon in the middle of a long clause:  
“We focus on three key drivers, namely prey availability, competition, and climate.”  
or two sentences: “We focus on three key drivers. They are prey availability, competition, and climate.”

**House convention:** no colons in the middle of **complex** sentences; use conjunctions or split the sentence.

### 14.3 Semicolons (;)

- **Default:** avoid semicolons in prose. They are easy to misuse and lengthen sentences.
- Prefer two sentences, or connect with “and”, “but”, or “however”.

**Examples**

- Instead of: “Pup counts increased at site A; they decreased at site B.”  
Prefer: “Pup counts increased at site A, but they decreased at site B.”  
or: “Pup counts increased at site A. They decreased at site B.”
- Instead of: “We tested three models; the first performed best.”  
Prefer: “We tested three models, and the first performed best.”

### 14.4 *i.e.* and *e.g.*

**General principle**

- These abbreviations often make sentences feel choppy. Most of the time, replace them with plain words or rewrite.

**House conventions**

- In running text, prefer **“that is”** instead of *i.e.* and **“for example”** instead of *e.g.*
- If you use *i.e.* or *e.g.* (rarely): **inside parentheses only**, with a comma after: “(e.g., shelf-break habitats)”. Do not chain long lists after them.

**Examples**

- Instead of: “We focus on three key drivers, i.e. prey availability, competition, and climate.”  
Prefer: “We focus on three key drivers, namely prey availability, competition, and climate.”  
or: “We focus on three key drivers (that is, prey availability, competition, and climate).”
- Instead of: “Seals used a range of habitats, e.g. shelf break and frontal zones.”  
Prefer: “Seals used a range of habitats, for example shelf-break and frontal zones.”  
or: “Seals used a range of habitats (e.g., shelf-break and frontal zones).”

**Short rule**

- Avoid *i.e.* and *e.g.* in the main sentence flow; prefer “that is” and “for example”.
- Parenthetical *e.g.*/*i.e.* only, with comma, sparingly; when in doubt, rewrite into a clear clause.

### 14.5 Scientific names and abbreviations

- *Italicise* genus and species (*Homo sapiens*, *Escherichia coli*) unless the target venue specifies otherwise.
- Spell out abbreviations at **first use** if they recur (e.g. global positioning system (GPS)), unless the venue defines a standard list.

---

## 15. Out of scope for this document

- **Page and wiki templates** (Purpose blocks, runbooks, scan-first hubs): define per project or in a separate layout skill.
- **Repository layout**, compiled literature notes, reference-manager automation: document locally; do not embed paths here.

## 16. Calibrate from your field and venue

Read **Introduction** and **Discussion** paragraphs from papers in your **target journal or funder style**, not from generic “plain English” templates. Mirror discipline-specific density, hedging norms, and how claims meet citations.

**Introduction moves (typical).**

- Open with **problem importance** and **taxon or system**, then support with citations (often clusters in journal prose).
- State **gap or uncertainty** (“However,” “Despite,” “It remains unclear whether …”).
- State **aim** (“Here we …”, “The objectives were …”, numbered aims when the paper uses them).

**Methods:** past tense; passive acceptable when agency does not matter; replicable *n*, gear, indices, software where relevant. Apply the **Modular Separation Framework** in `SKILL.md` (Methods): report biological/analytical variables; cite SOPs and state deviations; omit execution details (including workbook filenames and routine handling). Prefer state-focused sentences over action choreography. Triage: would changing this step alter Results trends or *p*-values? Also apply **Methods prose hygiene**: no scaffolding ("listed in Results"), no log voice ("confirm with…"), no site-named estimator lore, no commentary contrasts; `[PENDING …]` only for missing variables.

**Results:** data-forward; cite figures/tables; report point estimates **with uncertainty** when the source does.

**Discussion:** calibrated language (“consistent with,” “suggests”); separate mechanism from correlation; flag alternatives.

**Note-first workflows:** wiki-style links or literature-database notes are fine while drafting; convert to the venue’s citation format for submission.

## 17. How long synthesis drafts often drift (and fixes)


| Tendency                                                     | Why it weakens science prose        | Fix                                                                          |
| ------------------------------------------------------------ | ----------------------------------- | ---------------------------------------------------------------------------- |
| Rhetorical bold / slogan openers                             | Reads editorial                     | Neutral syntax; state the implication plainly                                |
| Em dashes (any use)                                          | Hides logic; not allowed under §14  | Same rules as §14                                                            |
| Horizontal rules between every subsection                    | OK in notes; heavy for manuscript   | Use headings or merge for submission drafts                                  |
| Meta-disclaimers (“this note is written to…”)                | Process, not content                | Delete or move to email or contributor guide                                 |
| Meta-scaffolding (“in this section…”, “as mentioned above…”) | Hides claims                        | Delete or one direct fact sentence; link or restate instead of “above/below” |
| Methods scaffolding (“listed in Results”, “see Discussion”)  | Navigation, not method              | Delete; put the rule or the number in the right section                      |
| Methods log voice (“confirm with…”, “ask Simon”)             | Operator note in MS prose           | Move to Gaps; use `[PENDING variable; context]` only                         |
| Methods commentary (“preferred because…”, “rather than…”)  | Justification / contrast            | State the reproducible rule once, or move contrast to Discussion             |
| Methods negation (“was not calculated”, “no CI is reported”) | Lists absences instead of methods | State only what was done; Discussion for why not if a reviewer needs it      |
| Site-named estimator lore in Methods                         | Anecdote instead of rule            | One general analytical rule; exceptions only if they change totals           |
| Contributor or tool signposting inside the article body      | Reads like a runbook                | Delete from the article; move to supplement, README, or internal wiki        |
| Second-person imperatives to the reader                      | Wrong voice for IMRAD-style reports | Third person or “we” + indicative                                            |
| Sparse citations on quantitative sentences                   | Evidence gap                        | Cite on the same sentence                                                    |
| Parallel metaphor overload                                   | Ambiguous referents                 | Literal verbs per clause                                                     |
| Noun stacks, bare comparatives, vague “global” shorthand     | Misread risk                        | Unpack clauses; add *than what*; name taxon, stage, or metric                |
| Bullets as the only argument in Discussion-style drafts      | No prose chain                      | Unspool into paragraphs with topic sentences                                 |
| Hype intensifiers without stats                              | Unscientific tone                   | Magnitude, scope, or statistics                                              |
| Claims without where/when/stage                              | Over-generalisation                 | Lead with scope and design limits                                            |


**List-style index pages** that are intentionally bibliographies or methods inventories should **not** be forced into IMRAD.

## 18. Prose clarity lint (repeatable pass)

Use on literature syntheses, Discussion sections, and drafts. Assume **domain experts** unless the user asks for a general-audience or policy piece.

**Sentences:** one main idea; roughly 10–25 words when density allows; ≤1 unfamiliar term per sentence unless the second is defined in the same sentence.

**Verbs:** active when agency is clear; swap weak “is/has/occurs” predicates for specific verbs; replace “is characterized by” with direct verb + object.

**Noun stacks:** avoid 2 content nouns in a row before a verb; unpack with a short clause.

**Metaphors:** do not repeat the same non-literal verb across parallel clauses; split or name the referent.

**Comparatives:** “more/less/higher” needs an explicit standard (“than at the reference site”, “than in males”, “than in the control year”, etc.).

**Terms with several operational meanings** (for example behaviour counts, effort indices, habitat use, inferred success): on first substantive use in a section, state which meaning you use, then stay consistent.

**Paragraphs:** topic sentence first; 3–5 sentences for article-like blocks; each paragraph advances argument, method, or interpretation.

**Quick self-lint:** strip filler (“in order to,” “it is important to note that”); apply the one-breath rule (§2).

## 19. IMRAD section focus


| Section          | Focus                                                                                                                        |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **Title**        | Informative; species/system when relevant; avoid empty novelty                                                               |
| **Abstract**     | Background (1–2), gap/aim, methods sketch, key quantitative results, interpretation in scope; 150–250 words unless specified |
| **Introduction** | Context + citations → gap → aims; no detailed results                                                                        |
| **Methods**      | Replicable; past tense; passive OK; subheadings normal                                                                       |
| **Results**      | Patterns in logical order (often vs aims); minimal interpretation                                                            |
| **Discussion**   | Interpret vs prior work and limits; no new primary results; mark speculation explicitly if used                              |


## 20. Statistical and quantitative reporting

When the source has **p-values**, **CIs**, ***n***, or **model comparison**:

- Report **uncertainty** with point estimates when available.
- Distinguish **biological** vs **statistical** importance.
- **Consistent rounding**; do not over-precision beyond data or model.
- Name **software** when reproducibility depends on it.

If the draft omits uncertainty the primary table had, **flag** it; do not invent intervals.

## 21. Few-shot tighten patterns (Methods / Results)

Adapt density to how specialist the reader is (journal-style vs general-audience summary).

**Thresholds — weak:** “We selected this range because the upper value approximates the pooled 50th percentile …”

**Stronger:** “We tested 0, 1, 2, and 3 °C. We chose this range to keep thresholds meaningful and usable. The highest value (3 °C) is near the long-term median (about 3.3 °C). Lower values yield fewer qualifying days. Values below 0 °C produced no cold-spell days, so they were excluded.”

**Model — weak:** “Daily deaths conditional on pups at risk were modelled as Binomial(n, pi) using a two-column response formulation.”

**Stronger:** “For each day, deaths were modelled as Binomial(*n*, pi), where *n* is pups at risk, using the two-column response (deaths, survivors).”

**Selection — weak:** “Models with delta-AICc = 2 were treated as a confidence set and the most parsimonious model was retained.”

**Stronger:** “Models with delta-AICc ≤ 2 were treated as similarly supported, and we retained the model with fewer parameters.”

## 22. Editing workflow

1. Confirm **audience**, **venue**, and any **local** layout or submission template (outside this guide).
2. **Structure:** IMRAD boundaries; topic sentences; Results vs Discussion.
3. **Evidence:** citation placement; numbers traced to sources; scope explicit.
4. **Voice:** cut filler and meta-scaffolding; run §**18** lint; fix §**17** patterns if upgrading to manuscript tone.
5. **Mechanics:** abbreviations, species italics, §**14** punctuation, §**20** stats language.
6. **Preserve substance:** do not invent results, *n*, or citations; flag gaps.

## 23. Conflicts with user instructions

If the user asks for **dramatic** or **marketing** prose, follow tone choice but keep facts, scope, and statistics accurate. If they ask for **denser specialist** text, lean into journal-style density and relax short-sentence targets while keeping definitions a generalist reviewer might need.

## 24. Portable use vs project overlays

Keep this guide **venue-agnostic**. Record paths, citation tools, and ingest pipelines in a local README or agent rule instead of forking this file. The repeatable clarity pass is §**18** only.

## 25. Session orchestration (optional)

For a **session-level** checklist when combining literature pulls, fulltext passes, and manuscript drafting (sources -> plan -> implement -> verify -> capture -> log), see the **academic writing plugin** in the dbrain repo: `plugins/academic-writing/README.md`. It points to which skills support each step; it does **not** replace this guide's prose rules.

## 26. Further reading (optional)

- [Thomson (2026) — concision vs brevity, genre, nominalisation, hedges, repetition](https://patthomson.net/2026/04/12/key-word-concision/) (blog)
- [Don’t torture your readers](https://conservationbytes.com/2009/02/09/dont-torture-your-readers/) (ConservationBytes)
- [Australian Government Style Manual — colons](https://www.stylemanual.gov.au/grammar-punctuation-and-conventions/punctuation/colons)
- [CDC clear writing guide (PDF)](https://www.cdc.gov/nceh/clearwriting/docs/clear-writing-guide-508.pdf)
- [Colorado College — concise academic writing (PDF)](https://www.coloradocollege.edu/dotAsset/f543ad6e-f606-4738-97d9-7945986705b0.pdf)
- [PMC — IMRAD structure and reader burden](https://pmc.ncbi.nlm.nih.gov/articles/PMC6199843/)
- [NIH plain language](https://www.nih.gov/nih-style-guide/plain-language) (useful for general-audience summaries)