---
name: figure-design
description: >-
  Plan, create, revise, and audit scientific figures from verified data and
  manuscript claims. Use for chart selection, multi-panel figure architecture,
  maps, statistical graphics, legends, annotations, colour and accessibility,
  journal sizing, source-data traceability, and figure-caption coordination.
  Does not invent data, choose an analysis after seeing a preferred visual, or
  treat visual polish as evidence.
metadata:
  version: 0.1.0
---

# Figure design

Turn verified scientific results into accurate, readable figures.

## Scope

This skill owns visual design and figure-level quality control. It does not own:

- statistical analysis or result selection
- manuscript argument or prose
- data cleaning without an authoritative specification
- literature discovery
- image manipulation that changes scientific content

Use companion workflows when available:

- `research-project-ops` for result IDs, source data, generating code, and output manifests
- `analysis-design` for unresolved analytical choices
- `manuscript-writing` for the claim, figure order, and caption role
- `ggplot-maps` for R/ggplot2 + `sf` map stacks, polar CRS, basemaps, and `ggsave` recipes
- a chart, GIS, notebook, or graphics tool for rendering

## Router

| Mode | Use when | Output |
|---|---|---|
| `plan` | A result needs a visual | Figure brief and panel plan |
| `create` | Verified data and claim are available | Reproducible draft figure and caption inputs |
| `revise` | An existing figure needs improvement | Revised figure plus material changes |
| `audit` | Checking scientific and visual integrity | Prioritised figure QA report |
| `journal-adapt` | Resizing or reformatting for a venue | Venue-compliant export without changed meaning |

## Evidence gate

Before designing, locate:

- the question or claim the figure must support
- authoritative source data
- result IDs or analysis output
- units, sample, groups, and uncertainty definition
- generating code or workflow when available
- intended manuscript section and figure order
- target medium, dimensions, and file format when known

Keep these statuses visible:

- `verified source data`
- `project result`
- `derived for display`
- `manual annotation`
- `[TBC]`

If a visual choice would require a new analysis, transformation, exclusion, or
aggregation, stop and route that decision to the analysis owner.

## Integrity gate

Never:

- alter values or omit inconvenient observations for visual effect
- truncate an axis in a way that exaggerates a pattern without clear justification
- connect observations that are not ordered or meaningfully continuous
- show uncertainty without defining it
- imply paired, temporal, spatial, or causal structure that the design does not support
- use area, volume, or colour intensity inconsistently with the encoded values
- hide overplotting, missingness, exclusions, or small samples when material
- export only a raster image when editable or reproducible source is required

## Workflow

1. Identify mode, audience, medium, and venue constraints.
2. Load the verified claim, result, source data, and current figure if present.
3. Complete the figure brief.
4. Select the visual form from the analytical question and data structure.
5. Plan panels and shared visual encodings before styling.
6. Build or revise the figure reproducibly where practical.
7. Check scientific integrity, legibility, accessibility, and manuscript fit.
8. Test the final-size export rather than only the working-size view.
9. Save or report source data, code, export, caption inputs, and unresolved items.

## Figure brief

Record:

| Field | Question |
|---|---|
| Purpose | Why must this figure exist? |
| Question | What exact question does it answer? |
| Claim | What result should the reader understand? |
| Evidence | Which result IDs and source data support it? |
| Boundary | What must the figure not imply? |
| Audience | Specialist, broad scientific, policy, or public? |
| Medium | Manuscript, presentation, poster, web, or report? |
| Constraints | Size, panels, colours, format, resolution, or journal rules? |

Use [assets/figure-brief.md](assets/figure-brief.md) when the project has no
existing figure specification.

## Choose the visual form

Choose based on the comparison, not habit.

| Need | Common starting point |
|---|---|
| Compare distributions | dot, interval, box, violin, or raincloud plot |
| Show estimates and uncertainty | coefficient or forest plot |
| Show change through time | line or point-interval plot |
| Show association | scatterplot with justified model summary |
| Show composition | aligned bars or small multiples; avoid hard-to-compare angles |
| Show spatial pattern | map with projection, scale, extent, and uncertainty considered |
| Show model performance | observed-predicted, calibration, residual, or validation plot |
| Show many repeated units | small multiples or transparent individual trajectories |
| Explain a process | schematic that clearly separates evidence from conceptual elements |

Read [references/design-guidance.md](references/design-guidance.md) when
selecting a chart, designing multiple panels, or resolving accessibility issues.

## Multi-panel contract

Every panel should contribute a necessary step in the figure's argument.

Check:

- panels follow the reading order
- repeated encodings mean the same thing
- shared axes are genuinely comparable
- panel labels are unambiguous
- legends are shared where possible
- redundant panels are removed
- detailed diagnostics move to supplementary material when they do not support the main claim
- the complete figure has one primary takeaway

Do not combine panels merely because they were produced by the same analysis.

## Statistical display

- Show raw observations when they are informative and legible.
- Define whether intervals are SD, SE, confidence, credible, prediction, or another quantity.
- Keep denominators and analytical units visible where needed.
- Distinguish observed data from fitted values and projections.
- Show transformations or non-linear scales clearly.
- Use consistent precision between the figure, caption, table, and prose.
- Avoid significance symbols as the only description of evidence.

## Maps

For spatial figures, verify:

- coordinate reference system and projection
- geographic extent and inset context
- scale bar and north arrow only where useful
- land, coast, bathymetry, or boundaries have a documented source
- colour scales match the data type and scientific question
- missing, unsampled, masked, and zero values are visually distinct
- spatial resolution is not presented as biological precision
- sensitive locations are generalised when required

## Colour and accessibility

- Do not rely on colour alone to distinguish important groups.
- Use colourblind-safe, perceptually ordered palettes.
- Use a diverging palette only around a meaningful midpoint.
- Keep categorical colours stable across figures.
- Check grayscale and common colour-vision deficiencies when relevant.
- Maintain sufficient contrast for text, lines, and symbols.
- Avoid decorative gradients, shadows, and three-dimensional effects.

## Labels and annotations

- Use units on axes or directly in labels.
- Prefer direct labels when they reduce legend lookup.
- Define abbreviations.
- Annotate only values or events needed to interpret the result.
- Separate statistical annotations from interpretive claims.
- Keep type size readable at final dimensions.
- Use consistent terminology with the manuscript.

## Caption handoff

Provide manuscript-writing with:

- what is shown
- population, period, and analytical sample
- panel descriptions
- visual encodings and units
- uncertainty and statistical summaries
- abbreviations
- source or attribution where required
- any display-only transformation

The caption may be drafted by either skill, but the figure and caption must be
checked together.

## Audit

Classify findings:

- `BLOCKER`: data mismatch, misleading encoding, missing provenance, or scientifically wrong label
- `MAJOR`: unclear claim, unsuitable chart, hidden uncertainty, illegible final size, or inconsistent panels
- `MINOR`: local label, spacing, legend, or ordering problem
- `EDITORIAL`: cosmetic preference with no material effect

Check:

1. figure values match authoritative outputs
2. encodings match the variable types and comparisons
3. uncertainty, sample, units, and transformations are defined
4. axes, legends, labels, and annotations are accurate
5. palettes and symbols remain accessible
6. panels form one coherent argument
7. final-size export is legible
8. figure, caption, Results prose, and tables agree
9. source data and generating code are recoverable

## Output contract

For planning:

1. figure brief
2. recommended visual form and reason
3. panel plan
4. source-data and analysis requirements
5. unresolved scientific decisions

For creating or revising:

1. figure or exact generating changes
2. source-data and code paths
3. caption inputs
4. material scientific or accessibility issues

For audit:

```markdown
## Readiness
READY | READY WITH GAPS | NOT READY

## Findings
- [severity] panel or location: issue and required action

## Highest-value next action
...
```
