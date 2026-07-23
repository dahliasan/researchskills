# Module: uninformative parameters (nested near-ties)

Primary paper: Arnold (2010). Full source notes:
[arnold-2010.md](arnold-2010.md).

## Idea

AIC adds about **+2 per extra parameter**. A nested richer model can sit within
ΔAIC ≤ 2 of a simpler model even when fit barely improves. Those extras are
**uninformative** and should not be sold as ecological effects.

Same warning is boxed in Burnham and Anderson (2002:131).

## Decision checks

### A. Nesting

1. Write both formulas.
2. Are fixed effects of A a subset of B (shared RE policy)?
3. If no → treat as alternative structures, not Arnold’s nested trap.

### B. Fit vs penalty

```text
penalty ≈ 2 × (K_complex − K_simple)
Δdeviance ≈ 2 × (logL_complex − logL_simple)
```

- Fit fails to beat penalty → uninformative.
- Fit barely beats penalty (simpler Δ ≪ 2 behind min-AICc) → weakly supported;
  default **parsimony for primary inference** unless strong a priori biology and
  clear CIs argue otherwise.

### C. Coefficients (corroboration)

For contested extras: do intervals include zero? Plausible a priori?
CI-includes-zero is not the whole rule (Arnold notes AIC/CI mismatch) but helps
when already near-tied.

### D. Weights

Flat weights among nested near-ties → shared support for the core structure
(e.g. “cold spell”), not unique support for every interaction term.

## Output template

```markdown
## AIC near-tie decision
- Min-AICc model:
- Nested simpler within Δ ≤ 2:
- ΔAICc (simpler vs min):
- Extra parameters:
- Nesting: yes/no
- Fit vs penalty: uninformative / weakly supported / clearly supported
- Primary inference model:
- Rule used: parsimony among Δ≤2 nested | min-AICc alone | other (state)
- Claims to soften or drop:
- Cite: Arnold 2010; Burnham & Anderson 2002 as needed
```
