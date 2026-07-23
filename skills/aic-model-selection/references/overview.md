# AIC/AICc selection — overview

Working notes for the parent skill. Not a textbook.

## Criteria

| Criterion | Typical use |
|-----------|-------------|
| AIC | Large *n* relative to *K* |
| AICc | Small-sample correction (default in many ecology GLMMs) |
| QAICc | Overdispersion quasi-likelihood settings |

Lower is better **within a comparable model set**.

## Δ and rough support bands

Common ecology shorthand (Burnham and Anderson style; not sacred cutoffs):

| ΔAICc | Rough reading |
|------:|---------------|
| 0–2 | Substantial support / competitive zone — **then** check nesting |
| 4–7 | Considerably less support |
| >10 | Essentially no support relative to the best |

Never stop at Δ alone for nested models; run the uninformative-parameters module.

## Akaike weights

Weights renormalize relative support **within the reported set**. Flat weights
among nested near-ties usually mean shared support for a **core structure**, not
license to narrate every extra term.

Do not write weights as Bayesian posterior probabilities unless that is
explicitly your framework.

## Cross-family rule

Do **not** compare absolute AICc between different likelihoods (e.g. binomial
GLMM vs beta-binomial). Rank within family; if family itself changed for
diagnostics, say so and keep selection tables separate or clearly labeled.

## Min-AICc vs primary inference

| Rule | When to use |
|------|-------------|
| Min-AICc alone | Clear separation (no nested Δ ≤ 2 with weak extras) |
| Parsimony among Δ ≤ 2 nested | Simpler nested model within Δ ≤ 2; extras uninformative or weakly justified (Arnold) |
| Multi-model / averaging | Large exploratory sets or deliberate multi-model inference |

Always **name which rule** produced the reported coefficients and figures.

## Related reading

- Burnham, K. P., and Anderson, D. R. (2002). *Model selection and multimodel
  inference* (2nd ed.). Springer. Especially nested Δ 0–2 boxed warning.
- Arnold, T. W. (2010). Uninformative parameters and model selection using
  Akaike’s Information Criterion. *Journal of Wildlife Management*, 74,
  1175–1178. https://doi.org/10.2193/2009-367
