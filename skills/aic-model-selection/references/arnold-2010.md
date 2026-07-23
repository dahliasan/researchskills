# Arnold (2010) — source notes

**Citation:** Arnold, T. W. (2010). Uninformative parameters and model selection
using Akaike’s Information Criterion. *Journal of Wildlife Management*, 74(6),
1175–1178. https://doi.org/10.2193/2009-367

**Role in this skill:** Source for the nested ΔAIC ≤ 2 “junk parameter” module
inside `/aic-model-selection`. See also
[uninformative-parameters.md](uninformative-parameters.md).

## Core claim

Adding one parameter costs **+2 AIC units**. A model that is within ΔAIC ≤ 2 of
a better (often simpler) model may look “competitive” only because the fit did
**not** improve enough to beat that penalty. Those extra parameters are
**uninformative**: they should not be interpreted as having an ecological effect.

Burnham and Anderson (2002:131) already boxed this: models within about 0–2 of
the best that differ by one parameter and have essentially the same maximized
log-likelihood are not truly competitive; the larger model is close only because
of the +2K penalty.

## What Arnold is *not* saying

- Not “always pick the simplest model in the entire candidate set.”
- Not “ΔAIC ≤ 2 means models are equal in every sense.”
- Not a replacement for a priori biology when designing the candidate set.

## Five remedies Arnold reviews

1. **Report all, dismiss uninformative** — preferred for small a priori sets.
2. **Model averaging** — can shrink junk influence; does not fix bad narrative
   alone.
3. **95% CIs** — flag terms that include zero; can also discard terms that AIC
   still supports (mismatch risk).
4. **All-subsets + variable weights** — for large / exploratory sets.
5. **Cull nested expansions** — hierarchical or sequential dropping so
   “best + junk” models do not steal weight or table space.

Arnold’s recommendation emphasis: for limited a priori sets, report models but
explain that near-top scores may not be competitive once deviance/log-likelihood
is considered. Move from ranking ritual to interpretation.

## Practical translation for nested AICc tables

| Observation | Practical call |
|-------------|----------------|
| Complex = simpler + 1–2 params; logL almost unchanged; Δ(complex) ≤ 2 | Treat extras as uninformative; do not invent effects |
| Complex is min-AICc by ≪ 2; simpler nested within Δ ≤ 2 | Prefer simpler for primary inference unless extras clearly earn their keep |
| Two non-nested models both within Δ ≤ 2 | Both are structural competitors; report both |

## Attribution

Distilled for agent use from the published article. Copyright remains with the
publisher/authors. Do not paste long copyrighted excerpts into manuscripts;
cite the paper.
