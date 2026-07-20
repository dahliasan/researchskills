# Scientific Writing Skill — Self-Improvement Loop Workflow

**Version:** 1.0  
**Date Created:** 2026-07-19  
**Purpose:** Reusable workflow for iteratively improving the scientific-writing skill by drafting real sections, validating, and refining guidance based on published paper patterns.

---

## Overview

This workflow describes how to use the scientific-writing skill as a **self-improving system**:

1. **Research** published papers to identify real patterns
2. **Update the skill** with new guidance based on patterns
3. **Draft** manuscript sections using the skill
4. **Validate** with deterministic checks (validator.py)
5. **Iterate** until output matches published standards
6. **Refine the skill** again based on what worked/didn't work

The loop treats the skill document itself as a **living specification** that evolves as agents encounter real writing challenges.

---

## When to Use This Workflow

- Writing a new IMRAD section (abstract, introduction, methods, results, discussion)
- Extending the skill to cover new genres (review, synthesis, commentary)
- Discovering patterns in published papers that aren't yet documented in the skill
- When agent drafts fail validator checks repeatedly
- When supervisor feedback suggests the skill is incomplete

## The 5-Phase Loop

### Phase 1: Research Real Papers

**Goal:** Understand how published papers in your field structure this section.

**Steps:**
1. Identify 3–5 published papers in your field/area
   - Preference: papers from project supervisors, recent high-impact journals
   - Collect full-text PDFs or summaries (abstracts + figure captions)
2. Read the target section in each paper (e.g., all 5 Results sections)
3. Document patterns observed:
   - **Logical structure**: ordered by species? taxonomy? methods? findings importance?
   - **Opening/closing**: how does it start? how does it wrap up?
   - **Citation placement**: where do citations appear? claim-proximate or clustered?
   - **Quantitative reporting**: means ± SD? confidence intervals? p-values shown?
   - **Hedging language**: how confident are claims? "suggests", "indicates", "demonstrates"?
   - **Jargon density**: technical terms per sentence? domain-specific abbreviations?
   - **Readability**: sentence length, paragraph structure, transitions?
   - **Active voice**: present or past tense? passive constructions?
   - **Result-specific patterns**: (for Results only) biology + numbers integrated? separate?
4. Create a **pattern document** (markdown or notes) summarizing findings
   - Example: `PATTERN_STUDY_RESULTS_2026_07_19.md`
5. **Compare patterns against current skill guidance**
   - What's already documented? ✅
   - What's missing? ❌
   - What contradicts current guidance? ⚠️

**Output:**
- Pattern study document (persisted for future reference)
- List of skill gaps to address

---

### Phase 2: Update Skill Guidance

**Goal:** Add or refine skill.md based on Phase 1 findings.

**Steps:**
1. Open `.agents/skills/scientific-writing/SKILL.md`
2. For each gap/pattern found:
   - Add section-specific guidance (if not already present)
   - Update examples to match published patterns
   - Refine hedging language table, citation rules, punctuation
3. Test new guidance against Phase 1 papers:
   - Would this guidance help reproduce published patterns?
   - Are examples clear enough for agents to follow?
4. Add or update validator checks if needed:
   - New punctuation rules? → add to validator.py
   - New hedging patterns? → document in SKILL.md with examples
   - New acronym rules? → update validator skip-list
5. **Document what changed**:
   - Commit message should reference Phase 1 findings
   - Example: "refactor(skill): add Results-specific guidance for integrated biology+numbers pattern"

**Output:**
- Updated SKILL.md (section-specific or general)
- Updated validator.py (if deterministic checks changed)
- Updated validator-README.md (if new checks documented)
- Commit with clear rationale

---

### Phase 3: Draft & Validate

**Goal:** Write a section using the updated skill, then run deterministic validator.

**Steps:**
1. **Brief agents** with:
   - SKILL.md (core guidance)
   - Phase 1 pattern study (examples)
   - Data sources (cv_all.json, tables, figures)
   - Success criteria (0 blockers, ≤14 Flesch-Kincaid, ≤5% jargon)
2. **Orchestrate sub-agents** to draft section
   - Preference: parallel variants (3 different approaches) to compare
3. **Run validator** on each draft:
   ```bash
   python validator.py --mode strict --input paper1-04-results-v1.0.md
   ```
4. **Record results**:
   - Blockers found (em-dashes, semicolons, author-narrative citations)
   - Warnings (jargon, readability, acronym definitions)
   - Metrics (word count, Flesch-Kincaid, %jargon)
5. **Fix blockers immediately**:
   - 0 blockers is non-negotiable
   - Re-run validator after each fix
   - Iterate with agents until passing

**Output:**
- Draft section file (paper1-XX-{section}-v1.0.md)
- Validator output log (saved in commit message)
- 0-blocker status achieved

---

### Phase 4: Cold-Read & Human Review

**Goal:** Verify the draft matches real published papers and answers the research question.

**Steps:**
1. **Cold-read** the draft fresh (start to end, no context)
   - Does it make sense?
   - Are there logical gaps?
   - Does it flow?
2. **Check scope**:
   - Does it answer the Methods research questions?
   - Is it at the right grain (per species? per taxon? overall)?
   - Any missing patterns or edge cases?
3. **Check boundaries** (IMRAD enforcement):
   - No Methods re-explanation? ✅
   - No Discussion/implications? ✅
   - Results-only findings? ✅
4. **Check biological integration** (Results-specific):
   - Are numbers + context in the same clause/sentence?
   - Could a non-statistician understand the findings?
   - Are patterns explained, not just reported?
5. **Compare against Phase 1 papers**:
   - Does the structure match published papers?
   - Are citations placed similarly (claim-proximate)?
   - Is the tone/voice consistent with supervisor papers?
6. **Identify gaps** for agents to revise:
   - Mark sentences for rewrite
   - Note missing species/taxa coverage
   - Flag ambiguous phrasing
7. **Supervisor approval** (final gate):
   - Does this match Hindell/McMahon/Sequeira style?
   - Would you publish this as-is?

**Output:**
- Cold-read notes (gaps, strengths, flow issues)
- Supervisor feedback (approved or needs revision)
- List of revisions for Phase 3b (iterate)

---

### Phase 3b: Iterate (Loop if Needed)

**Goal:** Fix human feedback and re-validate.

**If cold-read found issues:**
1. **Brief agents** with supervisor feedback
2. **Re-draft** problematic sections
3. **Re-run validator** (must maintain 0 blockers)
4. **Return to Phase 4** cold-read (repeat until approved)

**Success exit:** Supervisor approves + 0 blockers + ≤14 Flesch-Kincaid

---

### Phase 5: Proof & Export

**Goal:** Verify citations and finalize for manuscript assembly.

**Steps:**
1. **Run proof checks**:
   ```bash
   bash literature/run.sh prove  # if using literature pipeline
   ```
2. **Audit citations**:
   - Every citekey `[@citekey]` exists in references.bib? ✅
   - Evidence is accurate (claim matches cited paper)? ✅
   - Data citations traceable (cv_all.json, species_funnel.md)? ✅
3. **Export** (if integrating into full manuscript):
   ```bash
   python export_synthesis_docx.py --require-audit
   ```
4. **Final cold-read** for publication readiness
5. **Mark section "done"**:
   - Tag commit with "ready for manuscript"
   - Update status table in WRITING_WORKFLOW.md

**Output:**
- Proof audit log (citations verified)
- Exported .docx if needed
- Commit message: "chore(paper1-04): proof and export gate"

---

## Validator.py Checklist

Deterministic checks that **must pass**:

| Check | Blocker? | Target |
|-------|----------|--------|
| Em-dashes (—) | ✅ YES | 0 occurrences |
| Semicolons in prose | ✅ YES | 0 occurrences |
| Author-narrative citations | ✅ YES | 0 (use `[@citekey]` only) |
| Readability (Flesch-Kincaid) | ✅ YES >16 | ≤14 |
| Jargon density | ✅ YES >8% | ≤5% |
| Verbose words | ⚠️ WARNING | minimize (e.g., conducted→did) |
| Acronym definitions | ⚠️ WARNING | all defined on first use |
| IMRAD boundary | ⚠️ WARNING | Results = findings only |

---

## Quick Reference: 5 Phases in 30 Seconds

1. **Phase 1 (Research):** Read 3+ papers. Document patterns.
2. **Phase 2 (Update Skill):** Add patterns to SKILL.md + validator.
3. **Phase 3 (Draft):** Agents write section using skill. Validate (0 blockers).
4. **Phase 4 (Review):** Cold-read + supervisor approval.
5. **Phase 5 (Proof):** Citation audit + export.

Loop = Phases 1–5. Repeat for each new section.

---

**Status:** Template ready for reuse  
**Owner:** Scientific-writing skill stewards  
**Last Updated:** 2026-07-19

Start with **Phase 1** → **Phase 5**. Loop back to **Phase 1** when new sections/genres emerge.
