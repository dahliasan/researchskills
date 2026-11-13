# Analysis outputs: raw results, summaries and names

Read this whenever an analysis writes results to disk or prints a table someone will read.

## 1. Save the raw results first

The primary saved output is the result as the analysis produces it: the model output
after `summary()`, or the `broom` tidy/glance tables with every field the function
reports. Save all of it in a tidy form (one row per model, draw, group or term). Do not
trim fields because you think they are unimportant. A reader can then check any number
against the source without rerunning anything.

- Keep the same layout as the project's existing raw results, so results can be
  compared directly.
- Keep identifiers (draw, model, taxon, term) and units.

## 2. Summaries are interpretation

A summary is a second layer over raw results. Make one only when the question needs
several results combined, or when the raw output lacks a quantity the question needs.

- Add a quantity only when it is standard and needed to read the result, for example a
  95% confidence interval for a proportion, or a mean and its interval. Do not add
  columns just in case.
- Whenever a summary reports a mean, also report its standard deviation (SD).
- Keep the summary to the rows and columns the request asks for. Extra summaries,
  block splits, per-draw tables or diagnostics are not saved as official outputs unless
  requested. If they are useful for checking, keep them in a clearly separate scratch
  location outside the official output folder.

## 3. Use the community's standard terms

Use the names that the statistics literature and the packages already use. Do not invent
a plainer-sounding word for them. Examples:

| Avoid | Use |
|---|---|
| share, fraction, rate (for a proportion) | proportion |
| typical, central value | mean, median |
| spread, range | confidence interval, standard deviation |
| delta, gap, difference (when it has a defined form) | the defined form, e.g. AIC null minus full |
| score (for an information criterion) | AIC, BIC |
| goodness, fit (for a log-likelihood) | logLik |
| n, count of rows (for observations) | nobs |
| estimate, error, p-value (from a model) | estimate, std.error, p.value (broom names) |

This applies to any analysis, not only proportions. Before naming a quantity, check
whether a package or textbook already names it. If one does, use that name.

## 4. Name columns with the metric and unit

- Put the metric in the name, and the unit where it is not obvious.
- Name differences by their operands and direction, e.g. `aic_null_minus_full`, so the
  sign is readable without a note.
- Do not use generic labels such as `full`, `null`, `set`, `block1` as column names
  when they are model or group names. Use `aic_full`, `aic_null`, or the group's
  descriptive name.
- Keep names short. Do not repeat the table or file name inside a column name.

## 5. Keep tables readable

- Row labels are plain words a reader would say aloud, e.g. "Production", "New run".
- Show proportions as proportions (0.165) in data files, and as percentages in
  people-facing tables.
- Round to what the analysis supports, but keep full precision in saved raw results.
- State the sign convention of any difference once, in the table note or caption, when
  the column name alone does not make it obvious.
- Do not add flags such as `full_better` unless they are reported. Compute the
  quantity directly, e.g. `mean(aic_full < aic_null)`.

## 6. Round to the precision the metric supports

Round at presentation, never inside a calculation. Saved raw results keep full precision.
Summary tables are people-facing and are rounded.

- Round the uncertainty first (to 1 or 2 significant figures), then give the estimate and
  its interval the same number of decimal places.
- AIC, BIC, logLik, deviance: 1 decimal place. Differences between models are often 1 to 2
  units, so whole numbers hide them.
- Proportions: 2 or 3 decimal places (0.17), or percentages to 1 decimal place (16.5%).
- Means and medians of a metric: the metric's own precision (above).
- Coefficient estimates and standard errors: 2 to 3 significant figures, matched to the
  standard error.
- p-values: 3 significant figures, or `< 0.001`.
- Counts and sample sizes: integers.

## Checklist

- [ ] The raw results are saved as the analysis produced them, in tidy form.
- [ ] Any summary adds only quantities that are standard and needed.
- [ ] Only the requested tables, rows and columns are saved to official outputs.
- [ ] Terms match the literature and package names.
- [ ] Column names state the metric, and the unit where needed.
- [ ] No column needs a footnote to be understood.
- [ ] Flags and helper columns are absent unless they are reported.
- [ ] Summary values are rounded to the metric's precision; raw results are not.
- [ ] Every reported mean has its SD next to it.
