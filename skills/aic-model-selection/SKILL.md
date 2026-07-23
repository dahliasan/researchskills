---
name: aic-model-selection
description: >-
  Information-theoretic model selection with AIC/AICc/QAICc: rank candidates,
  interpret Δ and weights, separate nested vs non-nested near-ties, detect
  uninformative parameters (Arnold 2010), and choose a primary inference model
  when min-AICc and parsimony disagree. Use when building or auditing model
  selection tables, debating ΔAICc ≤ 2, asking whether an interaction earns
  its keep, or citing Burnham and Anderson / Arnold. Triggers on
  "/aic-model-selection", "AICc table", "Akaike weights", "uninformative
  parameters", "ΔAICc less than 2", "parsimony vs lowest AICc", "Arnold AIC".
  Not a general statistics textbook; not one-paper-only.
metadata:
  version: 0.2.0
---

# /aic-model-selection — AIC/AICc ranking and inference choice

Judgment framework for **information-theoretic model selection** in ecology and
related observational work. Covers ranking, near-ties, nested traps, and what to
report as the primary inference model.

**Concept skill** (not one paper = one skill; not a catch-all stats dump).
Core sources: Burnham and Anderson (2002); Arnold (2010) for uninformative
parameters.

References:

- [references/overview.md](references/overview.md) — Δ, weights, cross-family rules
- [references/uninformative-parameters.md](references/uninformative-parameters.md) —
  Arnold module + decision checks
- [references/arnold-2010.md](references/arnold-2010.md) — source notes

## When to use

- Building or revising an AIC/AICc/QAICc candidate table
- Choosing which model owns coefficients, figures, and Abstract effects
- Nested near-ties (e.g. main effect vs interaction)
- Reviewer / red-team risk on over-claiming weights or “clearly best”

## When not to use

- Choosing likelihood **family** (binomial vs beta-binomial, etc.) as the main
  question — decide family first, then select **within** family
- Experimental design, DHARMa recipes, or GLMM coding tutorials
- General statistics tutoring unrelated to IT model selection

## Hard rules

1. Compare AICc **within the same likelihood family** only. Absolute AICc is not
   comparable across binomial vs beta-binomial (or other families).
2. **Δ ≤ 2 is not automatic endorsement** of every near-top model.
3. For nested models, apply the **uninformative-parameters** module before
   narrating extra terms as ecological effects.
4. Name an explicit rule for the **primary inference model** (min-AICc alone vs
   parsimony among Δ ≤ 2 nested). Do not leave it implicit.
5. Do not silently change the user’s estimand or research question.
6. Prefer plain language for managers/coauthors after the technical call.

## Workflow

### 1. Confirm the selection universe

- Same response, same random-effect structure policy, same data rows.
- Same likelihood family for all ranked models.
- Candidate set is a priori (or label exploratory clearly).

### 2. Rank and inventory

From the AICc (or AIC/QAICc) table, record for each model: formula, K/df,
log-likelihood or deviance, AICc, Δ, weight. Identify:

- **Min-AICc** model
- Models with **Δ ≤ 2** (and optionally Δ ≤ 4 for a wider set)

### 3. Classify near-ties

| Pattern | Call |
|---------|------|
| Non-nested, both Δ ≤ 2 | Structural competitors — report both; do not pretend one is unique |
| Nested; larger almost same logL; Δ(larger) ≈ 0–2 | Extras likely **uninformative** (Arnold) |
| Nested; larger is min-AICc by a hair; simpler Δ ≤ 2 | Extras **weakly supported** — default toward parsimony for primary inference unless biology + CIs clearly earn the extras |

Detail: [references/uninformative-parameters.md](references/uninformative-parameters.md).

### 4. Choose the primary inference model

Default for **small a priori sets** when a nested simpler model sits within
Δ ≤ 2 of min-AICc and extras are uninformative or only weakly justified:

→ Prefer the **simpler nested model** for coefficients, predictions, and Abstract.

Keep min-AICc as primary only when:

- extras clearly beat the parameter penalty, **and**
- there is an a priori biological case, **and**
- you still disclose the near-tie in the table and prose.

State the rule used in Methods / `DECISIONS.md`.

### 5. Reporting

**Do:**

- Show the full (or SI) ranked table with Δ and weights
- Disclose nested near-ties and whether extras were treated as uninformative
- Soften “clearly best” language when weights are flat

**Do not:**

- Interpret junk nested extras as proven mechanisms
- Compare raw AICc across likelihood families
- Equate Akaike weight with posterior probability in prose

### 6. Hand off

- Decision log → `research-project-ops` / project `DECISIONS.md`
- Project-wide challenge → `research-red-team`
- Prose → `manuscript-writing`

## Exit checklist

- [ ] Selection universe and likelihood family stated
- [ ] Min-AICc and Δ ≤ 2 set listed
- [ ] Nested vs non-nested classified
- [ ] Uninformative / weakly supported extras called (if any)
- [ ] Primary inference model + explicit rule named
- [ ] Claim-language risk flagged for Abstract/Results
- [ ] Cite Burnham and Anderson 2002; Arnold 2010 when nested near-ties matter

## Companions

| Need | Skill |
|------|--------|
| Whole-project challenge | `research-red-team` |
| Manuscript wording | `manuscript-writing` |
| Project decision log | `research-project-ops` |
