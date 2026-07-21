# Scientific figure design guidance

Load this reference when selecting a visual form, designing multiple panels,
or auditing accessibility. Project and journal rules take priority.

## Start from the analytical question

A figure should reveal a comparison, pattern, distribution, relationship,
uncertainty, or process. State that purpose before choosing geometry or style.

Ask:

1. What are the observational or analytical units?
2. Which variable is the outcome?
3. Which comparisons matter?
4. Is order meaningful?
5. Which uncertainty must remain visible?
6. What would a reader incorrectly infer from this design?

## Match encodings to variables

- Position on a common scale is usually easiest to compare.
- Length is useful when bars begin at a meaningful baseline.
- Area and volume are difficult to compare precisely.
- Hue is suitable for categories.
- Lightness or a sequential scale is suitable for ordered magnitude.
- A diverging scale requires a scientifically meaningful centre.
- Shape and line type can provide redundant encoding for accessibility.

## Common chart decisions

### Distributions

Prefer individual observations, intervals, or distribution summaries that show
sample structure. Box or violin plots should not hide very small samples.

### Time series

Use connected lines only when observations belong to an ordered sequence.
Distinguish repeated individuals, group summaries, fitted values, and forecasts.

### Associations

Show observations and avoid implying that a fitted relationship is causal.
Display model uncertainty only when it is meaningful for the intended inference.

### Estimates

Coefficient or forest plots support comparison of estimates and uncertainty.
Use a clear null or reference line and retain units or transformations.

### Composition

Prefer aligned positions or lengths. Use pie charts only when approximate
part-to-whole comparison is sufficient and there are few categories.

### Maps

Match projection to purpose. Use equal-area projections for area comparison.
Distinguish unsampled locations from measured zeros. Do not imply that smooth
interpolation or a coarse grid represents observed fine-scale conditions.

## Multi-panel architecture

A multi-panel figure should read as a sequence:

```text
context or setup → primary comparison → supporting explanation or validation
```

Other sequences are valid when they reflect the scientific argument. Maintain
consistent group order, palette, units, and terminology across panels.

Use small multiples when repeated panels share a comparison. Avoid squeezing
unrelated analyses into one figure to save a figure number.

## Main versus supplementary figures

Keep a panel in the main figure when it is necessary to understand or verify the
central result. Move it to supplementary material when it mainly documents
diagnostics, robustness, secondary groups, or implementation detail.

## Accessibility checks

Review the final export for:

- readable text at intended dimensions
- contrast in print and on screen
- meaning retained without colour
- distinguishable lines and symbols
- no label collisions or clipped content
- sensible reading order
- descriptive alternative text when the medium supports it

## Export checks

Retain:

- source data
- generating code or editable source
- exact dimensions
- colour profile when required
- vector export for line art where supported
- raster resolution appropriate to the venue
- versioned final export linked to the manuscript
