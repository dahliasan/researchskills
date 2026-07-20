---
name: scientific-writing
author: dahlia
version: 2.3.2
description: >-
  Empirically grounded scientific prose: **section grammar** (Abstract–Intro–Methods–Results–Discussion 
  boundaries enforced with concrete job, voice, and content rules); **claim-first sentences** with 
  bracketed author–date citations; **statistical honesty** (report uncertainty, precision matches confidence); 
  **concision** (one idea per sentence); **punctuation discipline** (no em dashes, no semicolons in prose). 
  Based on analysis of published papers in ecology and marine science. Use when drafting or revising 
  manuscripts, synthesis deliverables, and coauthor handouts. Enforces Results vs Discussion separation 
  and prevents methods/results conflation.
disable-model-invocation: true
---

# Scientific writing

**Canonical copy (this pack):** `skills/scientific-writing/SKILL.md` in researchskills  
**Full handout:** [reference.md](reference.md)  
**Self-improvement workflow:** [SELF_IMPROVEMENT_LOOP.md](SELF_IMPROVEMENT_LOOP.md) (v1.0, 2026-07-19) — 5-phase loop for iteratively improving this skill based on published paper patterns

**Prose only:** claims, structure, citations, punctuation, statistics language. Citation proof pipelines and export gates live in **`corpus-citation-qa`** and **`research-workflow`**.

## Research plugin phases

| Phase | This skill | Companion |
|-------|------------|-----------|
| **WRITE** | Draft prose, claim-proximate cites | `corpus-citation-qa` for citekey rules only |
| **CITE-CHECK** | Do not rewrite quantified claims yet | `bash literature/run.sh prove` |
| **CLARITY EDIT** | Cold-reader pass (study frame, gaps) | `synthesis-editor` + `clarity_lint.py` |
| **STYLE** | Checklist + deterministic lint | `bash literature/run.sh prose-lint` |

Order: **WRITE → CITE-CHECK → CLARITY EDIT → STYLE → EXPORT**.

## Before writing

1. **Audience:** default to a field-literate reader in your discipline unless the piece targets a broader audience (then shorter sentences, more definitions, sourced numbers).
2. **Document type:** manuscript, review, synthesis note, or briefing; apply IMRAD sections only where that shape fits. Use any **local** house template your team provides for page layout or submissions.
3. **Named journal or venue:** relax short-sentence targets when clarity needs longer clauses. Keep **accuracy, scope, and statistical honesty** strict.
4. **Word budget:** Know your journal's word limits before drafting. See "Section length & word budget" below for realistic IMRAD allocation.

## The Hourglass Architecture (IMRAD Visual Structure)

Scientific manuscripts follow an **hourglass funnel**. This shapes how readers experience your argument:

```
        ⬇ WIDE CONTEXT ⬇
    Introduction (Macro Landscape)
       Problem → Gap → Hypothesis
            ⬇ NARROW ⬇
    Methods & Results (Technical Detail)
        Reproducibility & Findings
            ⬇ WIDE IMPLICATIONS ⬇
    Discussion (Return to Big Picture)
      Verdict → Benchmarking → Global Stakes
```

**What this means for your writing:**

- **Introduction (Top Funnel):** Start broad (field-wide landscape), move progressively narrower (your specific system, the exact gap, your hypothesis). Readers are funneled into YOUR question.
- **Methods & Results (Narrow Neck):** Stay narrow and specific. Technical precision, exact numbers, reproducible detail. The funnel is at its tightest here.
- **Discussion (Bottom Flare):** Start narrow (what your results mean), then expand outward (how they fit the field, global implications, future directions). Readers exit as wide as they entered—ready to apply your work.

**Practical rule:** If your Introduction feels too wide, you're setting up correctly. If your Discussion feels too narrow, rewrite—it should loop back and forth from your findings to the broader field.

## Section length & word budget

**Research-backed guidance** (from analysis of 60K+ published papers + 10+ journal guidelines): Use these section ratios to allocate your word budget. Percentages are medians; variation ranges are in parentheses.

### Standard Research Article (5,000–8,000 words main text)
*Target journals: Ecography, Global Change Biology, Conservation Biology, Journal of Applied Ecology*

| Section | Word Count (5K article) | Word Count (7K article) | Percentage of body |
|---------|---------|---------|---------|
| **Introduction** | 730 | 1,020 | 14.6% (8–22% range) |
| **Methods** | 1,485 | 2,080 | 29.7% (20–35% range) |
| **Results** | 1,310 | 1,835 | 26.2% (18–35% range) |
| **Discussion** | 1,475 | 2,065 | 29.5% (22–38% range) |
| **TOTAL** | **5,000** | **7,000** | **100%** |

**Key insight:** Methods is the longest section in species distribution modeling papers (29.7%) due to reproducibility requirements. Results and Discussion are balanced (26–30% each). Introduction is shortest (14.6%), assuming a field-literate audience.

**Variation by complexity:**
- **Simple designs** (univariate analysis): Methods 20–25%; Results 28–35%
- **Complex models** (ensemble SDM, multi-species): Methods 32–35%; Results 24–28%
- **Conservation planning papers:** Methods 28–32%; Discussion 30–35% (results and interpretation intertwined)

### Compact Articles (1,500–2,500 words main text)
*Target journals: Ecology Letters (Brevia, 1,500 words), short communications (2,500 words)*

| Section | 1,500 words | 2,500 words |
|---------|---------|---------|
| Introduction | 220 | 365 |
| Methods | 445 | 745 |
| Results | 390 | 655 |
| Discussion | 445 | 735 |

**Strategy:** Ruthlessly condense methods to essentials; move detail to supplement.

### High-Impact Journals (2,000–3,500 main text)
*Target journals: Nature, Science, PNAS*

| Section | Word Count |
|---------|---------|
| Introduction | 350–450 |
| Methods | 450–700 |
| Results | 500–800 |
| Discussion | 700–1,000 |
| **TOTAL** | **2,000–3,500** |

**Strategy:** Compress narrative; offload details to extensive supplementary materials (10–15 pages typical). High-impact journals expect brevity in main text, detail in appendices.

---

**Recommendations before drafting:**
- [ ] Identify your target journal and its word limit
- [ ] Allocate words per section using the table above
- [ ] Plan supplementary materials for methods/results details that exceed main-text budget
- [ ] Read 3–5 recent papers in your target journal to calibrate tone and section depth
- [ ] Avoid overshooting Results (the section that most often exceeds budget). Key rule: **focus on patterns, not species-by-species recitation**

**Data source:** Analysis of 60,519 published papers (PubMed Central 2016–2021) + 10+ journal author guidelines documented in [SKILL_IMPROVEMENT_WORD_BUDGET_RESEARCH.md](../../docs/SKILL_IMPROVEMENT_WORD_BUDGET_RESEARCH.md).

## Rule types: Know which rules are absolute

This skill distinguishes four types of guidance. Before applying a rule, ask: "Is this non-negotiable, or context-dependent, or a best practice, or an anti-pattern?"

| Rule type | Definition | Examples from this skill | When to apply |
|---|---|---|---|
| **Non-negotiable** | Must hold in all contexts; violation breaks the prose or section boundary. | Section boundaries (Results ≠ Discussion); active voice in Methods/Results/Discussion; no author names in narrative; claim-first sentences; bracket-only citations | Always. Non-negotiables are defaults; exceptions are rare and documented. |
| **Context-dependent** | Applies when X; reverse applies when Y. | Passive voice (use when agent unknown, irrelevant, or action-emphasis needed); hedging (use when uncertainty exists; avoid when finding is solid); longer sentences (use when explanation demands; avoid in Results). | Assess context first. Ask: "What is my goal here?" |
| **Best practice** | Recommended to improve clarity, readability, or flow. Violation is not an error. | Short sentences (~15–25 words); monosyllabic words; topic sentences; lists for parallel points; one idea per paragraph. | Apply unless document constraints prevent (e.g., a dense Methods section may need longer sentences). Trade-off clarity against thoroughness; best practices bias toward clarity. |
| **Anti-pattern** | Frequent error; avoid unless unusual justification. | Em dashes; semicolons in prose; triple-hedging; serial mini-reviews led by author names; "interestingly…" / "importantly…" opening frames. | Flag during revision. Ask: "Does this serve a purpose I cannot achieve another way?" If no, remove it. |

**How to use this skill:** Start with non-negotiables (section boundaries, active voice, citations). Then apply context-dependent rules based on your rhetorical goal. Then layer on best practices to improve readability. Finally, watch for anti-patterns during edit pass and remove them unless justified.

## Audience-aware language: Jargon and readability targets

Before drafting, assess your audience and set readability targets. This affects vocabulary choices and sentence length.

**Jargon density:** Aim for ≤ 5% technical or specialized vocabulary per section (or per ~100 words). Empirical analysis of 560+ successful lay summaries found 8.0% jargon density, which exceeds best-practice thresholds; successful examples cluster below 5%. When technical terms are necessary, define at first use: "area-restricted search behavior (ARS)" or "kernel density estimation (KDE)."

**Readability metrics (optional revision tool):** If audience includes non-specialists or if brevity is critical, measure readability using:
- **Coleman-Liau Index or Gunning Fog Index** (more reliable than Flesch Reading Ease for longer sentences or complex vocabulary)
- **Flesch-Kincaid Grade Level** (acceptable but avoid Flesch Reading Ease, which produces unreliable values in technical prose)
- Do NOT use Flesch Reading Ease alone; it fails when sentences are longer or vocabulary is specialized.

Target: Flesch-Kincaid Grade Level ≤ 14 (senior-college level) for field-literate audiences; ≤ 12 for broader audiences.

**Syllable count and word choice:** Beyond "use short words," quantify by morphology. Replace multi-syllable synonyms: "use" not "utilize"; "help" not "facilitate"; "show" not "demonstrate" (unless precision demands it). Monosyllabic and two-syllable vocabulary improves accessibility for non-specialist readers.

**AI-generated text verification (critical):** If using AI-assisted writing tools, manually verify all citations and DOI numbers before submission. Empirical testing shows AI generates incorrect DOIs at a ~38% error rate and fabricates references at ~16%. Verification is non-negotiable for accuracy.

## Non-negotiables (core style)

- **One main idea** per sentence and per paragraph; **topic sentence first**.
- **Active voice** (standard; passive only when necessary). Active is shorter, clearer, more direct. Use passive sparingly: when the agent is unknown, irrelevant, or when emphasizing the action over the actor ("Data were archived in Zenodo" is fine; "We deposited data in Zenodo" is better). Default to active across all sections—Methods ("We deployed tags"), Results ("Whales increased occupancy"), Discussion ("Our findings suggest…").
- **Concision:** remove **excess words**, not meanings the genre still requires. A short paragraph can still waste words; a long section can be tight if every sentence earns its place. **Do not** drop needed qualifications or traceability just to shave length (that is being short, not concise). Match length to the job (Introduction vs Methods vs synthesis) without padding. See [reference.md](reference.md) §2.1 and [Thomson (2026)](https://patthomson.net/2026/04/12/key-word-concision/).
- **Cut filler:** replace nominalisations and throat-clearing where a verb or direct opening carries the same message; keep hedges where epistemic honesty needs them, but **avoid stacked hedges** that add length without adding uncertainty discipline.
- **Elaborate, do not repeat:** develop the claim with new evidence or logic. Saying the same claim again in different words usually means the first wording was not clear enough yet.
- **Brevity at the word level:** cut words that do not change meaning; split if you cannot read aloud in one breath without losing the thread.
- **Subjects and verbs:** explicit subject, strong action verb; avoid long prepositional chains.
- **Tense:** past for what you did and specific results; present for stable facts and interpretation.
- **Terms:** keep precision terms; **define on first use** anything study-specific or ambiguous. **≤1 unfamiliar term per sentence** when possible.
- **Abbreviations and acronyms:** **First use must spell out the full term, then put the abbreviation in brackets.** Example: "We fitted Boosted Regression Tree (BRT) models using dismo::gbm.step with Bernoulli response (presence vs. pseudo-absence)." After first use, use the abbreviation alone. This applies to all technical terms, software packages, statistical methods, and acronyms. Standard field abbreviations (DNA, GPS, RNA, UK, US, EU, Fig) may be used without definition if audience is peer scientists; otherwise define them too.
- **Noun stacks:** if more than two content nouns pile up before a verb, unpack with a short clause.

## Hedging language: Calibrate confidence

Hedging is not weakness; it is epistemic honesty. Use modal verbs to match your confidence level. This table applies across all sections (Methods, Results, Discussion), but is most critical in Results and Discussion.

| Confidence level | Language | When to use | Example |
|---|---|---|---|
| **Modest possibility** | may, might, could | Your evidence is suggestive but not conclusive; alternative explanations exist. | “Whales **may** respond to thermal gradients by seeking warm-water refugia.” |
| **Supported but uncertain causation** | can, suggest, are likely to | You have solid evidence but cannot claim causation or universal applicability. | “Shipping exposure **can** reduce occupancy. Our findings **suggest** that…; X is **likely to** occur.” |
| **Established finding** | demonstrates, shows, is | Your evidence is robust and conclusion is directly supported by data; no hedge needed. | “Sample size **stabilizes** space-use estimates.” “Whales **reduced** velocity near chlorophyll peaks.” |

**Critical rule:** Avoid triple-hedging (stacking modals or hedges). Do NOT write: “It might be suggested that possibly the data could imply…” Use one hedge when needed; use none when findings are solid.

**Why this matters:** Readers trust careful language. Over-hedging signals uncertainty or lack of conviction. Under-hedging (claiming certainty where it does not exist) signals carelessness. Match hedging to evidence.

## Punctuation and short forms

Prefer **words that show logic** (“because”, “although”, “so”, “however”, “for example”) over punctuation that hides it. Full rules and examples: [reference.md](reference.md) section **14** (includes scientific names and abbreviations).

| Avoid | Use instead | Why |
| ----- | ----------- | --- |
| **Em dash (—)** | Use two sentences, a comma plus conjunction, or “because / although / for example”. | Em dashes obscure the logical relationship between clauses. Words like “because” or “although” make the connection explicit. |
| **Semicolon (;)** in prose | Full stop, or use “and / but / however”. | Semicolons compress two ideas on one visual line, slowing comprehension. Separate sentences or use conjunctions that signal relationships. |
| **Colon (:)** mid-complex sentence or before explanation | Use “that”, “namely”, “because”, or split into two sentences. Colons **only** for a short list after a **complete** lead-in (sparingly). Avoid colons before general explanatory phrases (“across four ecological domains:” is weak; rewrite as two sentences or use a conjunction). | Mid-sentence colons interrupt reading flow. Colons work best to introduce a structured list that follows a complete statement. Avoid them to frame abstract groupings (use concrete, action-first framing instead). |
| ***i.e. / e.g.* in open text** | Use “that is” / “for example”; or parenthetical **(e.g., …)** with comma, sparingly. | Abbreviations assume reader familiarity and slow non-native speakers. Spelled-out phrases are clearer and more accessible. |

## Citations (house default: bracket-only)

**Non-negotiable for this plugin:** cite with **brackets only**. Put `[@citekey]` (Pandoc) at the end of the clause each claim lives in. The rendered author–date appears in those brackets after citeproc; **not** as surnames woven into the sentence.

| Do not write | Write instead |
| ------------ | ------------- |
| Smith et al. found that 63% of range is core habitat [@smith2025]. | Core habitat covers 63% of range [@smith2025]. |
| Glencross et al. scaled penguin tracks and found overlap under 5% [@glencross2025]. | Colony-scaled overlap was under 5% of shared map area [@glencross2025]. |
| Seguin et al. (2025) detected fishing in 47% of MPAs. | Industrial fishing occurred in 47% of coastal MPAs [@seguin2025globalpa]. |
| …as shown by Smith et al., 2018. | …[@smith2018]. |

- Citations are **evidence for a claim**, not decoration.
- **No author surnames in narrative** for routine attribution. Not at sentence open, not mid-clause, not as `Author et al.` before `[@citekey]`. Findings first; brackets carry who.
- **Claim-proximate placement (required):** one cluster per factual sub-clause. Split sentences rather than clustering mixed sources at the end.
- **Co-citation is fine** when every source in `[@a; @b]` supports the **same single** assertion.
- **Synthesis bullets:** treat each sub-clause like a mini-sentence; one cluster per number, mechanism, or taxon-specific finding.
- **Findings first** with `[@citekey]` on the right clause; never "Smith et al. conducted a study in which…".
- **Literature synthesis:** synthesize by **idea or pattern**, not serial mini-reviews led by author names. Cut empty frames ("many studies…", "it is important to note…", "interestingly…").

**Lint:** `bash literature/run.sh prose-lint` flags `et al.`, inline `Author (YYYY)`, and `Author et al., YYYY` as **blockers**.

## Section grammar: Where things go

This skill enforces **section-level discipline**: each section has a job, voice, and content type. Empirical analysis of papers in your field shows agents often conflate sections; they report results in Discussion, restate methods in Results, or smuggle speculation into Methods. The patterns below are derived from your accepted corpus.

### ABSTRACT / SUMMARY (80–250 words)

**Job:** Answer the reader's first question: *What is the contribution and why should I keep reading?*

**Voice:** Declarative, past tense for what you did, present for conclusions.

**What lives here:**
- **Context:** Problem statement (one sentence; no lit review).
- **Gap/Question:** What was unknown or how is this novel?
- **What you did:** Concrete method name (e.g., "used satellite telemetry combined with species distribution models").
- **Key results:** 1–3 quantified findings tied to the research question.
- **Implication:** One-sentence takeaway for policy/science.

**What does NOT belong:**
- Detailed methods or statistical justifications.
- Literature mini-reviews ("many studies show…").
- Interpretation beyond what results directly support.
- Figures, tables, or citations (in most journals).

### INTRODUCTION (1–3 pages)

**Job:** Walk the reader from the known world to the gap you're filling.

**Structure (don't skip steps):**
1. **Open with momentum:** Begin with a technological or conceptual advance that enables your field. Use past-perfect tense ("have proliferated," "have transformed") to show the field's trajectory. Example: "Tracking studies of marine animals have proliferated in recent years as miniaturized, cost-effective tags are deployed on an increasing array of species." This establishes *why* the question is timely.
2. **Problem statement:** Admit complexity rather than mask it. Use concession language ("However," "Although") to signal where existing approaches fall short. Ground the problem in prior work (cite foundational sources). Example: "However, the deployment of tags can stress animals and involves considerable logistical costs, leading to a fundamental but complex question…" Avoids false certainty.
3. **Background:** What is known about the mechanisms, threats, or system? Keep tightly focused; do not write a literature dump. Synthesize by idea or pattern, not by author-led mini-reviews.
4. **The gap:** What remains unknown? What do existing methods miss, or what is contested? Be specific: "Most studies to date have tracked N animals; the minimum number required for population-level inference is unclear."
5. **Your question/hypothesis:** State it plainly. What will you investigate?
6. **What you did (brief):** One sentence: "We used X method on Y system to test Z."
7. **Roadmap (optional):** If your paper is long, preview main sections.

**Voice:** Past perfect for field momentum ("have discovered," "have led to"), past for prior work, present for stable facts and your goals.

**Hedging:** Admit tension where it exists ("fundamental but complex") rather than presenting a false consensus.

**What does NOT belong:**
- Results (not even preliminary ones).
- Methods detail (save for Methods section).
- Personal narrative ("we were interested in…").
- Hedging that delays the point (but admit genuine complexity).

**What drafters often get wrong:**
- Jumping from general threat to your specific angle without bridging the gap.
- Inserting results as motivation ("we found X, so we then asked Y").
- Over-citing without synthesis; cite patterns, not individual papers serially.
- Presenting the problem as simple when your paper acknowledges it is "fundamental but complex."

### METHODS (1–3 pages, depending on complexity)

**Job:** Provide reproducibility. Another scientist should be able to replicate your core work from this section alone.

**Tense:** Past tense (you did this work).

**Structure:**

**Option A: Temporal order (most common for field/observational studies)**
1. **Study system/site:** Geography, dates, permits.
2. **Data collection:** Chronological order. For each data source:
   - What was collected (tag type, mesh size, sampling design).
   - When and where (dates, locations, deployment details).
   - Sample size and coverage.
   - Quality/error handling.
3. **Environmental/covariate data:** Sources, spatial resolution, processing steps.
4. **Analysis/modeling:** Each analysis in order. State the question, the model/tool, key assumptions.

**Option B: Conceptual maturity order (when methods build in complexity or research phases)**
Supervisor papers in marine megafauna tracking often organize methods by research question complexity rather than chronology:
- Methods are grouped by what they address (small-scale behavior, then population-level inference, then multi-species comparison).
- Conceptual organization can use metaphorical headings ("Exploratory phase," "Validation phase") to signal narrative progression.
- Each subsection states its research goal first, then methods.

**Guidance for all Methods:**
- Avoid results embedded in procedures ("the model fit well"). Save outcomes for Results.
- Avoid justification ("we used method X because it is better"). State what you did; let the approach speak. If method choice is defensible but unconventional, cite prior use (e.g., "following [@smith2020], we applied X method to Y problem").
- Cite standard methods by name without re-deriving; only detail non-standard approaches.

**Voice:** Prefer **state-focused** wording for biological and analytical outcomes ("Frozen tissue was homogenized to ~50 mg"; "Where more than one observer counted a site, abundance was the mean of those counts"). Use first-person plural for deliberate design choices ("We deployed SPOT5 tags"; "We ran 1000 simulations"). Passive is fine when agency does not matter (see Modular Separation Framework below). Do not narrate routine lab or field choreography. **Never** write "was/were conducted" or "carried out"; use the real verb (counted, sampled, estimated, measured).

**What does NOT belong:**
- Preliminary results ("most tags transmitted >100 locations").
- Interpretation ("this captures foraging areas").
- Literature justification ("many studies show X").
- Discussion of limitations (save for Discussion).
- **Execution details** (workbook filenames, how tubes were carried to the centrifuge, vessel route to the station). See Modular Separation Framework.
- **Scaffolding, commentary, or log voice** ("listed in Results"; "confirm with X"; "preferred at Site A because…"). See Methods prose hygiene.
- **Negation catalogues** ("we did not calculate ICC"; "no CI is reported"). State what you did.

**What drafters often get wrong:**
- **Mixing methods and results:** Separate what you did (tagged 15, got data from 10 after filtering) from how many remained post-filtering (Results).
- **Omitting replicates/coverage:** "We sampled in spring." How many sites? How many years? How often within spring?
- **Skipping data cleaning:** Readers need to know if you filtered GPS errors, missing values, outliers. State the criteria.
- **Burying key decisions:** If you chose a 10 km buffer or set a velocity threshold, state it openly in Methods, not hidden in figure captions.
- **Confusing storage mechanics with methods:** Naming the Excel workbook or field notebook as if it were a protocol step. That is an execution detail; report the reconciliation rule or classification criteria instead.

**Parallel structure:** Order methods to match your Results sections. If Results is organized by taxon, organize Methods the same way.

**Methods Metadata Checklist (Reproducibility Foundation):**

Readers cannot reproduce your work without knowing the **exact system specifications, organism identities, permissions, and environmental parameters**. Include all of the following where applicable to your study:

| Category | What to Specify | Example |
|----------|-----------------|---------|
| **Organism Identity** | Exact taxonomic name, strain, cell line, or variety | *Arctocephalus gazella* (Antarctic fur seal), not "fur seals" |
| **Study Locations** | Precise geographic coordinates (lat/long, datum), place names, habitat types | Site A: 53.45°S, 72.10°W (Heard Island beach, sandstone slope) |
| **Capture/Sampling Methods** | How organisms were obtained, handled, marked, or deployed (tags, nets, traps) | Sixteen seals captured by net during winter haul-outs, tagged with ARGOS transmitters (Telonics, ~600 g), released same day |
| **Sampling Dates & Seasons** | Exact dates or date ranges; define breeding seasons, migration timing | November 2019 – March 2020 (Antarctic summer); pup production counts, late October–February only |
| **Sample Sizes & Replication** | Counts of organisms, sites, time intervals, repeated measures | 15 individual seals tracked (12 females, 3 males); tracking duration 8–18 months per individual |
| **Ethical Approval** | Institutional animal care/use committee approval, permit numbers, relevant regulations | "All procedures were approved by the Australian Antarctic Division Ethics Committee (permit #2019-033) under the Antarctic Treaty" |
| **Environmental Parameters** | Temperature, salinity, pH, light, pressure, humidity during sampling | Sea-surface temperature logged every 12 h (range 0.2–2.8°C); water column salinity 34.1–34.3 PSU |
| **Equipment Specifications** | Manufacturer, model, serial number, firmware version, and settings for instruments | SPOT5 satellite tags (Wildlife Computers, model SPOT5-163D, firmware v4.2); Argos transmission schedule: 5-day cycles |
| **Data Filtering & QA** | Thresholds applied, outliers removed, missing-data handling | "Removed GPS locations with error ellipse >100 m; excluded dives <10 s to remove tag movements during haul-out" |
| **References & Standards** | Citations for standard methods or protocols | "Following [@iso14644:2015], cleanroom procedures were Class 6; all reagents were molecular-biology grade" |

**Why this matters:** A reader should be able to decide, from your Methods, whether your methods answer *their* question. Vague methods ("seals were tracked") prevent replication and comparison across studies.

**Most common gaps in marine / biological Methods:**
- Omitting exact species name (just "fur seals" — which species? which subspecies?)
- Precise coordinates missing (just "South Georgia" — readers don't know beach, rock type, slope angle)
- No permit or ethics statement (journals now require this)
- Environmental conditions not recorded (temperature, salinity affect behavior and marker validity)
- Tag specifications missing (battery model, transmission power affect location quality)

#### Modular Separation Framework (concise Methods that stay reproducible)

Methods must balance **manuscript conciseness** against **reproducibility**. Do not list every physical action. Do not omit variables that would change the Results if altered. Filter every sub-step into one of three buckets:

| Bucket | Role in Methods | Examples |
|--------|-----------------|----------|
| **Biological / analytical variables** | Report precisely (mandatory) | Incubation temperature; mesh size; GPS filter thresholds; age-class definitions; final reagent concentrations; sampling dates and coordinates |
| **Standard operating procedures (SOPs)** | Cite by name; state deviations only | Commercial kits (brand, catalog #); published field protocols ("as previously described by [@smith1995], with incubation extended to 12 h") |
| **Execution details** | Omit from main text | Walking to the centrifuge; vortexing for 5 s; vessel route to the site; bucket color; mixing arithmetic ("we added 5 g NaCl to 500 mL"); **field workbook / spreadsheet filename**; which laptop held the counts |

**Boundary matrix (what to include vs omit):**

| Category | Include (mandatory) | Omit (superfluous) |
|----------|---------------------|--------------------|
| Standard kits and published protocols | Brand/kit/catalog #; explicit deviations from the manual or cited paper | Step-by-step wash/spin instructions already in the manual |
| Physical and lab mechanics | Final parameters that alter biological state (e.g. centrifuge at 4°C vs 21°C) | Routine handling (pipettor brand, moving tubes to ice) |
| Field and marine sampling | Coordinates, date/time, weather when it matters, gear specs, permits | Navigational minutiae; container color; path taken to the beach |
| Reagents and solutions | Final concentrations, purity/grade, pH, vendor | Volume arithmetic used to make the stock |
| **Data recording and storage** | Reconciliation rules, observer design, QA criteria that change counts | That counts lived in a named Excel workbook, clipboard, or shared drive |

**Three structural tactics:**

1. **"As previously described" (with one rule).** Cite a validated prior protocol instead of rewriting it. **Rule:** state every deviation explicitly.
2. **Supplement strategy.** Summarize operational capability in one main-text paragraph; put blueprints, wiring, or long pipeline specs in Supplementary Methods or an open protocol repository (e.g. Protocols.io).
3. **Report variables, omit actions.** Frame sentences around the state of the system, not the researcher's choreography.
   - Action-focused (omit): "We took samples from liquid nitrogen, thawed them on ice for 10 min, and cut ~50 mg with a sterile scalpel."
   - State-focused (prefer): "Frozen tissue was homogenized to a target mass of ~50 mg under sterile conditions."
   - Field analogue (omit): "…site totals use reconciled multi-observer sums where available (field workbook)."
   - Field analogue (prefer): "Where more than one observer counted a site, abundance was the mean of those counts."

**Golden rule of triage:** If an external researcher changes this variable or skips this sub-step, could it alter the final *p*-values, effect sizes, or data trends in Results?

- Kit spin time 5 min → 10 min on a standard commercial kit → usually **omit** (cite the kit).
- Incubation temperature 24°C → 26°C for a marine organism → **include**.
- Naming `Pup census.xls` vs saying "mean of multi-observer counts" → **omit** the filename; **include** the combination rule (mean, sum, or preferred series). Never write "reconciled" alone.

**Methods prose hygiene (non-negotiable for draft Methods paragraphs):**

Methods text must read as **finished manuscript Methods**, even in a notes/log file. Investigation voice, coauthor prompts, and section navigation do **not** belong in the paragraph. Put those under a separate **Gaps** / **Triage notes** heading.

| Fail mode | Why it fails triage | Fix |
|-----------|---------------------|-----|
| **Scaffolding / signposting** | "Site totals are listed in Results"; "see Discussion"; "as described above" | Delete. State the method rule here, or put the number in Results without pointing. |
| **Log / operator voice** | "confirm with S. D. Goldsworthy"; "ask Simon"; "pending our email"; "flag for Gate 2" | Move to Gaps. MS placeholders use `[PENDING short description; optional range or assumed value]` only. |
| **Commentary / justification** | "rather than a single synchronous day"; "this was preferred because…"; "this is not equivalent to…" | Delete from Methods. Contrast and interpretation → Discussion. |
| **Site-named estimator lore** | "At Skua Beach, the preferred estimate was…"; "At Fairchild, the second series was used because rock pools…" | State the **general analytical rule** once ("Where more than one independent recapture sample was obtained, site abundance was the mean of those estimates"). Site exceptions that change totals → short rule or supplement, not narrative. |
| **Weak / hollow verbs** | "surveys were conducted"; "analyses were carried out"; "counts were reconciled" | Use the real verb and the real rule: counted, estimated, mean of observer counts. |
| **Negation / “what we did not do”** | "No 95% CI is reported…"; "ICC was not calculated…"; "No hypothesis test is reported…" | State only what you **did**. Omissions are silent unless a journal requires an explicit waiver. Caveats belong in Discussion if needed. |
| **Results smuggled into Methods** | Marked *n* as a finding; preferred *N* ± sd; “mean residency was 3.43 d” | Methods: protocol + estimator. Results: the numbers (including AUC means). Cohort *n* (sample size of the design) may stay in Methods. |
| **Execution / storage mechanics** | Workbook names, clipboard, who walked which transect for logistics | Omit. Keep the reconciliation or QA rule that changes counts. |

**Placeholder rule:** A `[PENDING …]` slot is allowed only for a **missing variable** (criteria, site list, reagent, citekey). It is never a to-do for the agent ("confirm with…") and never a pointer to another section.

**Self-check before leaving a Methods draft:** strip every sentence that (1) names a person as an action item, (2) tells the reader where else to look, (3) explains *why* a choice was better without stating a reproducible rule, (4) says what you **did not** do, or (5) would not change Results if deleted. If (4) or (5) is true, delete it.

**Relation to the metadata checklist above:** The checklist lists *what kinds of variables* readers need. This framework tells you *which candidate details are variables* versus *execution noise*. Prefer lean main text; put long custom apparatus or code blueprints in supplements, not in narrative Methods.

### RESULTS (1–3 pages)

**Job:** Report what you found. Nothing more. Save interpretation for Discussion.

**Tense:** Past tense (you collected and analyzed data).

**Structure:**
- Lead with the most important finding.
- Organize logically (by hypothesis, taxon, dataset, or temporal sequence). Choose whatever matches your research question.
- One paragraph or subsection per major result or result group.

**Experimental Rationale (Sub-section Openers):**

Each Results subsection begins with one sentence explaining **why you performed that specific test**. This is the "what question did this analysis answer?" line. It anchors readers to your research design and prevents Results from feeling like a data dump.

Examples:
- *"To test whether habitat loss predicted population decline, we ran a generalized linear model…"*
- *"To determine which prey drove seasonal shifts in diet, we compared isotope ratios across four months…"*
- *"We assessed spatial heterogeneity by comparing kernel density distributions across three coastal zones…"*

Do NOT include the answer in this opening sentence. Just the question / rationale. Then report the findings.

**What lives here:**
- **Numbers:** Counts, percentages, means ± SD, model estimates, p-values, confidence intervals.
- **Patterns:** Spatial or temporal trends, relationships.
- **Comparisons:** Differences between groups (with statistical support).
- **Figures/tables:** Reference them. Do not embed interpretation ("Figure 2 shows the striking difference") — let the reader see it.

**What does NOT belong:**
- **New methods or qualifications:** "We then corrected for X" belongs in Methods.
- **Interpretation:** "This suggests…" or "likely due to…" → Discussion.
- **Speculation about mechanisms:** Save it.
- **Discussion of previous studies:** "Unlike Smith et al., we found…" → Discussion.
- **Caveats or limitations:** "Though sample size was small…" → Discussion.

**Voice:** Neutral, factual. Avoid dramatic language ("strikingly," "remarkably"). Let the numbers speak.

**What drafters often get wrong:**
- **Sneaking interpretation in:** "Whales avoided high-traffic areas" (interpretation) instead of "36.7% of detections occurred in moderate-traffic areas" (fact).
- **Reporting only significant results:** Non-significant findings matter. State them: "SST showed no significant effect (p = 0.50, Table 1)."
- **Scattering qualifications:** "Most whales stayed in X area" (what about the others?). Be precise: "13 of 15 whales (87%) remained…"
- **Treating figures as backup:** Figures are primary evidence. Reference them for every major claim.

**Parallel structure:** Organize by the same categories as your question. If you asked three questions, report three result subsections.

#### Accessible Results: Integrate biological observations with quantitative evidence

Results sections should **integrate biological and ecological observations with quantitative evidence in the same clause or sentence**. The organism or process remains the subject; numbers specify scope and magnitude. This makes findings accessible and scientifically rigorous simultaneously.

**Pattern (from your supervisors' work):**

The key is **integration, not sequence**. Organism/behavior first, then immediate quantification:

| Quantitative-only | Integrated biology + numbers |
|---|---|
| "96% encounter rate was recorded; mean = 6.9 (SD = 6.1)." | "Seals were sighted during 1332 (96%) of shore-based scans; mean seals per scan = 6.9 (SD = 6.1), ranging 0–39." |
| "A concentrated spatial pattern was found via kernel density." | "Kernel density analysis revealed a highly localised hotspot of at-sea usage around the channel's narrowest point." |
| "Dive duration varied by tidal phase (p = 0.03)." | "Most seals (7 of 9) exhibited longer median dive durations during flood tides vs. ebb tides, suggesting increased foraging intensity during specific tidal phases." |

**From your corpus (marine movement ecology):**

✓ "**Whales encountered moderate shipping exposure** in **39% of satellite detections** (Fig. 2)."  
— Observation (whales encountered exposure) + proportion (39%) + evidence (figure).

✓ "**Catch per unit effort significantly increased** over **five-fold** during the 20-year study period (**0.0012 to 0.0068 individuals/gillnet hrs**; Fig. 2)."  
— Ecological finding (catch increased) + magnitude (five-fold) + specific range (0.0012 to 0.0068) + reference (Fig. 2).

✓ "**Whales reduced velocity** **near areas of high spring chlorophyll concentration** (Table 1, Fig. 3a)."  
— Animal behavior (whales reduced velocity) + environmental context (high chlorophyll) + evidence (table/figure).

✓ "**Whales showed low-speed, persistent behavior (ARS)** **in coastal bays and fast transit in open water** (Fig. 2)."  
— Behavior type (ARS: low-speed, persistent) + spatial pattern (bays vs. open water) + evidence (figure).

**What this achieves:**
- **Organism/process is the grammatical subject** — not "exposure was detected" but "whales encountered exposure."
- **Numbers are not decoration** — they specify scope, magnitude, or sample size immediately in the biological claim.
- **Defers interpretation** — no "suggesting X mechanism" (that's Discussion); stick to: what happened, how many/how much, where/when.
- **Accessible to generalist readers** — seals/whales/distributions are concrete; statistical details follow, not replace, the biological observation.

**What does NOT belong in Results:**
- Interpretation of mechanisms: "suggesting prey aggregates" → Discussion
- Methods justification: "we used kernel density because…" → Methods
- New qualifications: "although sample size was small…" → Discussion
- Quantitative-first: "A correlation of r = 0.67 was found" → Reframe: "Shipping exposure correlated strongly with whale occupancy (r = 0.67)."

#### Concision in Results

Apply [Pat Thomson's concision rules](https://patthomson.net/2026/04/12/key-word-concision/): remove excess words, not meanings.

| Excess | Concise |
|---|---|
| "In order to investigate whether whales responded to thermal gradients, we analyzed X model." | "To test thermal-gradient response, we analyzed X model." (Results just reports findings, not methods setup; but if you must mention: this is tighter.) |
| "It was shown that whales displayed area-restricted search behavior." | "Whales showed ARS behavior." or "Whales reduced velocity and increased persistence." |
| "The results demonstrated that there was an increase in catch rates." | "Catch rates increased five-fold." |
| "The data are presented in Table 1, which shows the results of the statistical analysis." | "Table 1 summarizes statistical results." (Reference table, don't describe it.) |

### DISCUSSION (2–4 pages)

**Job:** Interpret your results, relate them to prior work, acknowledge limits, and state implications.

**Tense:** Past tense for your findings, present for stable facts and interpretation, conditional for speculation.

**The Verdict (Answer Your Hypothesis First):**

Open your Discussion by directly answering your central hypothesis based on your new data. Do not summarize methods, do not hedge excessively, do not start with theory. Start with: **Did your findings support or refute your hypothesis?** This is your opening move.

- **If you supported the hypothesis:** "We hypothesized that [X]. Our results confirm that [X], based on [evidence]."
- **If you refuted the hypothesis:** "We expected [X], but our data instead show [Y]. This unexpected pattern suggests [mechanism or interpretation]."
- **If you found a partial answer:** "We partially confirmed [X], but the relationship with [Z] differed from predictions. [Explanation]."

This verdict is not speculative. It is the direct empirical answer to the question you posed in your Introduction. Readers will thank you; editors will move you up.

**Structure (follow this sequence—do not reverse):**
1. **The Verdict:** Direct answer to your central hypothesis based on new data (see above).
2. **Mechanism or context:** Why did you observe this pattern? Ground in theory, ecology, or prior work. Use hedging language (see Voice section).
3. **Alignment with prior work:** How do your results compare to existing knowledge? Acknowledge agreement, divergence, or gaps.
4. **Limitations + implications:** Discuss constraints (sample size, missing data, scope) and their consequences. Integrate specific examples, not as a separate "Limitations" subsection.
5. **Future directions or calls to action:** What remains unknown? What is the next step?
6. **Concluding remark:** End with the take-home message.

**Practical example of flow:**
> "We found that space-use estimates stabilize with increasing sample size [finding + interpretation]. This suggests that studies with few tracked individuals may detect only broad movement patterns [mechanism]. Our results align with prior simulation work [@studyA] and expand those findings to multiple taxa [@studyB]. However, we were unable to assess responses at sub-daily scales due to tag resolution limits [limitation], though longer deployments would address this [implication]. These findings suggest that future sample-size planning should account for study question complexity [call to action]."

**What lives here:**
- **Interpretation:** "The strong association with chlorophyll-a suggests whales track spring productivity."
- **Mechanism:** "Thermal fronts may aggregate prey, making patches more profitable."
- **Uncertainty:** "We were unable to assess behavioral responses at sub-daily scales due to Argos error."
- **Boundary conditions:** "Results apply to northern Patagonia in austral summer; tropical populations may show different thresholds."
- **Future work:** "Refined temporal-lag models would clarify krill recruitment dynamics."

**What does NOT belong:**
- **New results:** "In a follow-up analysis, we also found…" → either Methods/Results or a new paper.
- **New methods or data:** "We then used an alternative model…" → Methods section.
- **Unreferenced speculation:** "Climate change will shift distributions northward" without evidence or citation.
- **Unsubstantiated claims about your own work:** "Our method is the best." Let results speak.

**Voice and hedging language:**

Hedging is not weakness—it is epistemic honesty. Use modal verbs to calibrate confidence:

| Confidence level | Language | Example |
|---|---|---|
| **Modest possibility** | may, might, could | "A better assessment **may be possible** with larger sample sizes." |
| **Supported but uncertain causation** | can, suggest, are likely to | "Simulation exercises **can** serve as exploratory tools. Our findings **suggest** that…; X is **likely to** occur." |
| **Established finding** | demonstrates, shows, is | "Sample size stabilizes space-use estimates." (No hedge needed if empirically solid.) |

Avoid:
- *"Our results imply that…"* (too strong; "imply" means interpret, not report). Use "suggest" instead.
- *Triple-hedging:* "It might be suggested that possibly the data could imply…" (accumulation without adding clarity).
- *False certainty:* "This proves that…" should be "This demonstrates association; alternative explanations include…"

**What drafters often get wrong:**
- **Reversing finding-mechanism order:** Start with what you found, *then* explain it. Not: "Because X is true, we hypothesized Y, and indeed we found Y."
- **Reporting new results:** If important, include in Results. Don't bury findings in Discussion paragraphs.
- **Defending methods:** Should be in Methods, not Discussion.
- **Ignoring conflicts with prior work:** If you contradict an earlier study, acknowledge it and explain why.
- **Leaping to policy without support:** State what your data support, then discuss policy options.

## Tactical clarity devices

These tactics improve readability for field-literate and broader audiences:

**Topic sentences as signposting.** Start each paragraph with a single-clause sentence stating the paragraph's job (“We deployed tags in three bays” or “Females showed higher occupancy than males”). This clarifies the reader's direction before detail. Avoid burying the point in a complex opening clause.
- **Use when:** Starting any paragraph in Methods, Results, Introduction, or Discussion; especially critical when readers skim headings.
- **Avoid when:** Paragraph job is already obvious from section context or immediately prior sentence.

**Acronyms: Define before first use, minimize thereafter.** “We used satellite telemetry (SPOT5 tags) to track whales.” Use the spelled-out form or short pronoun afterwards, not the acronym (“The tags transmitted daily”). This reduces cognitive load for readers unfamiliar with the abbreviation.
- **Use when:** Acronym appears 3+ times; introducing a technical term for the first time; audience may include non-specialists.
- **Avoid when:** Acronym appears only once or twice; common abbreviations like DNA or GPS (familiar to field readers).

**Sentence variety but not chaos.** Mix short sentences (~10–15 words) with medium ones (~20–25 words). Avoid long strings of equally long sentences (monotony) or equally short ones (choppy rhythm). Short sentences work well for findings; medium sentences for explanation. Empirical analysis of 560+ grant lay summaries shows structural complexity has increased over time; counteract this trend by deliberately shortening sentences during revision.
- **Use when:** Revising any section; especially important in Results and Abstract (high-density findings).
- **Avoid when:** Technical depth demands long sentences for precision (balance clarity against accuracy).

**Active voice with clear subjects.** “Whales reduced occupancy” (7 words) beats “Occupancy was reduced” (4 words, but who?) or “Reduced occupancy was observed” (5 words, passive + vague). The subject is the actor; the verb is the action.
- **Use when:** Describing what organisms or researchers did (Methods, Results); always in Results.
- **Avoid when:** Agent is truly unknown, irrelevant, or when emphasizing the action (rare; use passive sparingly).

**Prefer monosyllabic and two-syllable words.** Beyond generic “use short words,” quantify by syllable count. Replace multi-syllable synonyms: “use” not “utilize”; “help” not “facilitate”; “show” not “demonstrate” (though “demonstrate” is acceptable when precision demands it). Research on successful lay summaries shows monosyllabic + two-syllable vocabulary improves accessibility for non-specialist readers.
- **Use when:** Broader audience, low readability tolerance, or writing abstracts/lay summaries.
- **Avoid when:** Technical precision requires a longer term; using it would obscure or weaken a necessary distinction.

**Break complex claims into discrete sentences.** Instead of: “We compared occupancy using kernel density analysis, which revealed differences between bay and open-water zones that were significant when accounting for tidal phase.” Try: “We compared occupancy using kernel density analysis. Bays and open-water zones showed different occupancy patterns. These differences were significant when accounting for tidal phase.” Longer sentences are harder to parse; breaking at logical joints aids comprehension. This applies to specialist and general audiences.
- **Use when:** Sentence exceeds 25 words or contains 2+ independent ideas; revising any section.
- **Avoid when:** Breaking apart would lose necessary causal or logical connection (rare; reconsider structure instead).

**Use lists and tables for parallel points.** Instead of: “Whales showed high occupancy in the northern bay where depth exceeded 10 m, in the central bay where depth was 5–10 m, and in the southern bay where depth was under 5 m.” Try:

| Location | Depth (m) | Occupancy |
|---|---|---|
| Northern bay | > 10 | High |
| Central bay | 5–10 | High |
| Southern bay | < 5 | Moderate |

Tables reduce prose clutter and aid comparison.
- **Use when:** 3+ parallel data points (sites, taxa, treatments) or complex comparisons; Results or Methods sections.
- **Avoid when:** Prose comparison is simpler (e.g., two conditions, one number per row); table would require scrolling or shrinking text to fit.

## Edit pass (checklist)

**Clarity and scope:**
- Audience and venue clear (field-literate vs broader)? Ask: Who reads this, and what is their expertise?
- Paragraph job + topic sentence clear? **Action:** Read only your first sentence of each paragraph. Does it tell the reader what the paragraph does?
- Concision: no drag sentences, no triple-stacked hedges, no same-claim repetition in new words? **Action:** Highlight any sentence you read twice; delete or rewrite it.

**Sentence structure:**
- Sentences ~≤25 words where reasonable; split double claims? **Action:** Read aloud. If you stumble or run out of breath, the sentence is too long. Split at conjunctions or logical breaks.
- No monotony (equally long sentences)? **Action:** Check paragraph rhythm. Count words in 3 consecutive sentences. If all within 5-word range, vary one.

**Citations and terminology:**
- Terms defined on first use? **Action:** Flag any acronym used before definition; flag jargon without explanation.
- **Claim-proximate** citations (no clustering on multi-claim sentences)? **Action:** Highlight each sentence with 2+ factual claims. Check for one `[@cite]` per claim, not one per sentence.

**Section boundaries and precision:**
- Results vs Discussion boundaries enforced? No new counts in Discussion? **Action:** Scan Discussion for numbers. Any numbers should refer back to Results, not introduce new data.
- Punctuation clean (no em dashes, no semicolons, no open-text abbreviations)? **Action:** Search for "—", ";", "i.e.", "e.g." in open text. Replace each.
- Statistics and uncertainty honest? **Action:** For every number, check that uncertainty (SD, CI, p-value) is reported if appropriate.

**Prose quality (skim pass):**
- No empty frames ("many studies…", "interestingly…", "it is important to note…")? **Action:** Search for these phrases; delete them.
- No process signposting in place of substance (in synthesis or long sections)? **Action:** Skim introduction to first substantive claim. Should take <2 sentences of framing.

## Style verification (STYLE phase)

After POLISH, run deterministic gates in order:

### 1. Prose validator (comprehensive gates)

**Prerequisite:** `pip install textstat` (required for readability checks; other checks run without it)

```bash
python validator.py --file draft.md --mode strict
```

Checks (blockers + warnings):
- **Em dashes** (—) in prose
- **Readability** (Flesch-Kincaid > 14 grade level; blocker if > 16; skipped without textstat)
- **Semicolons** in prose (not in code or citations)
- **Abbreviations** (i.e., e.g. in open text)
- **Author names** in narrative (et al., Author YYYY patterns)
- **Acronyms** used before definition (skips common field abbreviations: DNA, GPS, RNA, BRT, GLMM, etc.)
- **Jargon density** (>5% warning; >8% blocker)
- **Results/Discussion boundary** (numbers without figure/table refs in Discussion)

Options:
- `--mode strict`: check warnings + blockers (use before final submission)
- `--mode normal` (default): blockers only

### 2. Prose lint (existing tool for citation/punctuation)

```bash
bash literature/run.sh prose-lint --markdown draft.md
```

Blockers: em dashes, open-text `i.e.` / `e.g.`, **author-in-narrative** (`et al.`, inline `Author (YYYY)`, surname before `[@citekey]`). Warnings: semicolons in prose, possible citation clustering.

### 3. Export gate (optional, for synthesis)

```bash
python3 scripts/export_synthesis_docx.py --require-style path/to/draft.md
```

Semantic nuance (tone, scope fit) still needs this skill’s edit-pass checklist; scripts only enforce deterministic rules.

## Further reading and external resources

### Research on biological science writing
- **Turbek et al. 2016** — "[Scientific Writing Made Easy: A Step-by-Step Guide to Undergraduate Writing in the Biological Sciences](https://esajournals.onlinelibrary.wiley.com/doi/10.1002/bes2.1258)," *Bulletin of the Ecological Society of America* 97(4):417–426. Step-by-step guide for biological science writing emphasizing active voice, clarity in Results sections, and accessible framing of findings.

### Concision and clarity
- **Pat Thomson** — "[Key word: Concision](https://patthomson.net/2026/04/12/key-word-concision/)" — Identifies predictable places excess words accumulate (nominalisations, throat-clearing, stacked hedges).
- **Hotaling et al. 2020** — "[Simple rules for concise scientific writing](https://aslopubs.onlinelibrary.wiley.com/doi/10.1002/lol2.10165)," *Limnology and Oceanography Letters* — Actionable principles for tightening prose.

### Readability, accessibility, and lay-summary writing
- **Falkenberg et al. 2024** — "[How to write lay summaries of research articles for wider accessibility](https://aslopubs.onlinelibrary.wiley.com/doi/10.1002/lol2.10373)," *Limnology and Oceanography Letters* — Empirical assessment of lay summaries using six readability metrics (Coleman-Liau, Gunning Fog, Flesch-Kincaid, ARI, Dale-Chall, Linsear Write); found high jargon density and low readability in published examples; recommends active voice, short sentences, monosyllabic/two-syllable words, one idea per sentence.
- **Huang, Li & Li (2025)** — "[Writing for non-specialists? Investigating readability and jargon use in successful lay summaries of CRF grant proposals 2006–2024](https://link.springer.com/article/10.1007/s11192-025-05442-8)," *Scientometrics* — Analysis of 560+ lay summaries over 19 years. Empirical findings: jargon density averages 8.0% (exceeds recommended ≤5% threshold); structural complexity has increased over time (sentences growing longer); readability correlates with jargon control, not lexical simplification alone.
- **Cheng, Calhoun & Reedy (2025)** — "[Artificial intelligence-assisted academic writing: recommendations for ethical use](https://pmc.ncbi.nlm.nih.gov/articles/PMC12007126/)," *Advances in Simulation* — Guidelines for AI-assisted writing emphasizing human verification. Critical finding: AI-generated citations show ~38% DOI error rate and ~16% fabricated reference rate; manual verification required before submission.

### Section-specific patterns from your supervisors' papers

**Introduction:** Momentum-building structure  
[Sequeira et al. 2018, co-authored by Hindell and McMahon] opens with technological enablement: "Tracking studies of marine animals have proliferated in recent years as miniaturized, cost-effective tags are deployed on an increasing array of species…" Then pivots to the problem via "However": "However, the deployment of tags can stress animals and involves considerable costs, leading to a fundamental but complex question…" This models the [momentum → concession → problem] sequence you should follow.

**Methods:** Flexible organization by research maturity  
[Sequeira et al. 2018] organizes methods by research question complexity, not chronology: "Dare to dream (sample size of one)" → "Understanding variability (sample sizes up to 10)" → "Defining the norm (sample sizes of 10s to 100)" → "Defining population parameters (sample sizes ~100)" → "Moving toward big data (>> 100)." The headings use metaphor to signal narrative progression. Methods also present results immediately after procedures where findings illustrate the approach: "When only three males and three females were tracked, the probability of recording a significant difference was only 0.331, but this rose to 0.983 when eight were tracked." This embedded-result pattern is acceptable when it illustrates the method itself, not when it reports independent findings.

**Discussion:** Finding-mechanism-prior work-limitation sequence  
[Sequeira et al. 2018] follows the prescribed order: finding ("A better assessment may be possible with larger sample sizes"), mechanism ("simulation exercises can be useful as exploratory tools"), prior work ("A recent study that tracked 10 green turtles…"), limitation ("the same number of tags can lead to very different data depending on deployment timing"), implication ("pooled datasets are generally useful to draw conclusions"). Limitation is integrated (not quarantined) with concrete examples (pinnipeds, molting timing). Hedging language uses modal verbs (may, can, likely) without triple-stacking.

### Corpus examples: Your supervisors' work and peer papers
Hindell, McMahon, and collaborators' papers model integrated biology + quantitative Results and disciplined section grammar:

**Harbour seal movement (tidal habitat use):**
> "Seals were sighted during 1332 (96%) of shore-based scans; mean seals per scan = 6.9 (SD = 6.1), ranging 0–39." — Observation (sighted) + immediate quantification (96%, mean, range).

> "Kernel density analysis revealed a highly localised hotspot of at-sea usage around the channel's narrowest point." — Spatial pattern (hotspot) + method evidence (kernel density) + location detail.

> "Most seals (7 of 9) exhibited longer median dive durations during flood tides compared to ebb tides." — Behavioral finding (longer dives) + count (7 of 9) + comparison (flood vs. ebb).

**Your corpus (marine movement ecology):**
- Raoult et al. 2022 (shipping exposure): "Whales encountered moderate shipping exposure in 39% of detections"
- Mullins et al. 2024 (habitat suitability): "Catch per unit effort increased five-fold from 0.0012 to 0.0068 individuals/gillnet hrs"
- Bedriñana-Romano et al. 2021 (movement ecology): "Whales reduced velocity near areas of high spring chlorophyll concentration"

## Promote back to researchskills

When stable, promote from this repo:

```bash
./scripts/promote-skill.sh --from /path/to/MegaMove_Threats --skill scientific-writing --to researchskills
```

See `skills/skill-lifecycle/SKILL.md` in researchskills.
