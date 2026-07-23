# Layouts and colour (R / ggplot2)

Curated deep-research notes for publication figures. Prefer package docs and
Wilke over Medium/listicle posts. Pair with [resources.md](resources.md) URLs
and sibling `figure-design` for integrity QA.

## Start here (short path)

1. **Compose** — [patchwork](https://patchwork.data-imaginist.com/) Getting Started → Layout → Annotation; [ggplot2 book §9](https://ggplot2-book.org/arranging-plots.html).
2. **Colour** — [Wilke colour basics](https://clauswilke.com/dataviz/color-basics.html) + [pitfalls](https://clauswilke.com/dataviz/color-pitfalls.html); then [ggplot2 colour scales](https://ggplot2-book.org/scales-colour.html).
3. **Size** — Design at journal column width (`ggsave(..., units = "mm")`); greyscale + CVD check before submit.

Default stack: **ggplot2 + patchwork + viridis/scico + Okabe–Ito/Tol**.

---

## Multi-panel layouts

### Best sources

| Resource | Why |
|---|---|
| [patchwork site](https://patchwork.data-imaginist.com/) | Canonical composer; replaces `grid.arrange` for ggplot |
| [Layout guide](https://patchwork.data-imaginist.com/articles/guides/layout.html) | `plot_layout()`, design strings, fixed-aspect / `coord_sf` |
| [Annotation guide](https://patchwork.data-imaginist.com/articles/guides/annotation.html) | A/B/C tags, titles without `ggdraw` hacks |
| [ggplot2 book — Arranging plots](https://ggplot2-book.org/arranging-plots.html) | Official patchwork + `inset_element` |
| [Wilke — Multi-panel figures](https://clauswilke.com/dataviz/multi-panel-figures.html) | Design: small multiples vs compound; shared scales |
| [cowplot — Drawing with/on plots](https://wilkelab.org/cowplot/articles/drawing_with_on_plots.html) | Freeform insets (`ggdraw` + `draw_plot`) |
| [ggh4x Facets](https://teunbrand.github.io/ggh4x/articles/Facets.html) | Nested facets inside one ggplot |
| [aplot](https://yulab-smu.top/aplot/) | Axis-locked side panels (heatmap + dendrogram style) |

Practical workshop (not primary doctrine): [NIH CCR Lesson 6](https://bioinformatics.ccr.cancer.gov/docs/data-visualization-with-r/Lesson6/), [FMI intermediate ggplot2 combining panels](https://fmicompbio.github.io/intermediate_ggplot2/5_combining_plot_panels.html).

### Recurring layout tips

```r
# Operators
p1 | p2          # side by side
p1 / p2          # stacked
(p1 | p2) / p3   # nested

# Shared legend + tags
(p1 | p2) +
  plot_layout(guides = "collect") +
  plot_annotation(tag_levels = "A") &
  theme(legend.position = "bottom")

# Irregular grid
design <- "
AAA#
BBCC
"
wrap_plots(A = p1, B = p2, C = p3, design = design)

# Map + chart: let map keep aspect
p_map + p_ts + plot_layout(widths = c(NA, 1))
```

- Prefer `guides = "collect"` over manual `cowplot::get_legend()`.
- Fixed-aspect maps (`coord_sf`): use `NA` widths/heights so patchwork does not squash them.
- Same units across panels → fixed scales; different ranges → `scales = "free_y"` or ggh4x per-panel scales.
- Insets: `inset_element()` first; cowplot `draw_plot()` when placement must be freeform.
- Apply theme to all panels with `& theme(...)`.

### Skip or demote

| Approach | Why |
|---|---|
| `gridExtra::grid.arrange` as default | Works, but weak guide/axis collection vs patchwork |
| Manual legend extraction as default | Brittle; patchwork collects guides |
| `egg` as default composer | Stale; niche `set_panel_size()` only |
| Assembling figures only in PowerPoint | Fine for last-mile; bad primary workflow |
| ggh4x / aplot as patchwork replacements | Wrong layer (facets / axis-lock vs page layout) |

---

## Colour palettes

### Best sources

| Resource | Why |
|---|---|
| [Wilke — Color basics](https://clauswilke.com/dataviz/color-basics.html) | Qual vs seq vs div vs highlight |
| [Wilke — Color pitfalls](https://clauswilke.com/dataviz/color-pitfalls.html) | Okabe–Ito default; CVD; avoid rainbow |
| [Wilke — Redundant coding](https://clauswilke.com/dataviz/redundant-coding.html) | Shape/linetype when marks are thin |
| [Paul Tol schemes (PDF)](https://sronpersonalpages.nl/~pault/data/colourschemes.pdf) | Citeable qualitative/diverging/sequential |
| [khroma Tol vignette](https://packages.tesselle.org/khroma/articles/tol.html) | R wrappers + CVD diagnostics |
| [colorspace HCL palettes](https://colorspace.r-forge.r-project.org/articles/hcl_palettes.html) | Theory + `hclwizard()` |
| [Crameri Scientific Colour Maps](https://www.fabiocrameri.ch/colourmaps/) | Map-safe sequential/diverging; B&W readable |
| [scico](https://github.com/thomasp85/scico) | ggplot2 bindings for Crameri |
| [ggplot2 colour scales](https://ggplot2-book.org/scales-colour.html) | viridis / distiller / fermenter / steps |
| [ColorBrewer 2.0](https://colorbrewer2.org/) | Map-first; CVD + print filters |
| [viridis intro](https://cran.r-project.org/web/packages/viridis/vignettes/intro-to-viridis.html) | Why rainbow fails; CVD demos |
| [Scherer ggplot tutorial](https://www.cedricscherer.com/2019/08/05/a-ggplot2-tutorial-for-beautiful-plotting-in-r/) | Practical package tour |

Also useful: [r-statistics.co ggplot2 colours](https://r-statistics.co/ggplot2-Colours.html), [Andrew Heiss colour notes](https://datavizf24.classes.andrewheiss.com/resource/colors.html).

### Decision tree

```
Colour encodes…
├─ Categories (unordered) → QUALITATIVE
│   n ≤ 5–8: Okabe–Ito or Tol bright/muted
│   n > 8: facet / grey+highlight / shapes — do not invent 12 hues
├─ Ordered magnitude, no centre → SEQUENTIAL
│   continuous maps/rasters: viridis/cividis/magma OR scico batlow/tokyo
│   binned choropleths: scale_*_fermenter / scale_*_steps
└─ Meaningful midpoint (0, anomaly) → DIVERGING
    scico vik/berlin OR Brewer PuOr/RdBu via distiller/fermenter
    fix midpoint explicitly
```

**Maps / large areas:** Brewer, CARTO (`rcartocolor` CVD-friendly), scico/Crameri, viridis.  
**Thin points/lines:** Okabe–Ito / Tol bright (Brewer pastels often wash out).

### Default stack (ecology / tracking)

```r
# Qualitative
scale_colour_manual(values = unname(palette.colors(n, "Okabe-Ito")))
# or khroma::scale_colour_okabeito() / scale_colour_bright()

# Sequential continuous
scale_fill_viridis_c(option = "cividis")   # or "magma" / "inferno" for habitat
# scale_fill_scico(palette = "batlow")

# Diverging
scale_fill_scico(palette = "vik", midpoint = 0)

# Binned map legend
scale_fill_fermenter(palette = "YlGnBu", n.breaks = 6)
```

### Accessibility checklist

- [ ] Palette type matches data type; diverging midpoint is real
- [ ] ≤ ~8 categorical hues; redundant shape/linetype for thin marks
- [ ] CVD check (deut + prot); greyscale/print proof
- [ ] No red–green-only encoding
- [ ] NA = explicit grey, not a data hue
- [ ] Soft-proof CMYK if the journal cares
- [ ] Cite Tol/Crameri/Okabe–Ito in Methods when non-default

### Risky / overhyped for papers

| Habit | Risk |
|---|---|
| Rainbow / jet / `topo.colors` | False edges; CVD and greyscale fail |
| turbo as primary science map | Better than jet; still rainbow-like |
| WesAnderson / NatParks as default | Pretty; not CVD-designed |
| MetBrewer unchecked | Only some schemes are CVD-safe |
| Default ggplot hue cycle | Poor greyscale; prefer Okabe–Ito |
| Viridis for unordered categories | Implies order |
| Interpolating Tol qualitative | Use discrete stops as published |

---

## Themes, fonts, export

### Best sources

| Resource | Why |
|---|---|
| [Publication-quality figures checklist](https://r-statistics.co/Publication-Quality-Figures-in-R.html) | Theme + ggsave + panel tags checklist |
| [Quent 2026 — actually publication-ready](https://jaquent.github.io/2026/02/creating-actually-publication-ready-figures-for-journals-using-ggplot2/) | `theme_journal()`, geom defaults, journal widths |
| [Journal size / DPI / font guide](https://scholarviz.com/blog/journal-target-size-dpi-font-decision-tree) | Nature/Science/Cell column widths |
| [CCT publication ggplot workshop](https://cct-datascience.quarto.pub/crafting-publication-quality-data-visualizations-with-ggplot2/) | Themes + vector vs raster |

### Recurring export tips

- Set `width` / `height` / `units` / `dpi` explicitly; never rely on the open device.
- Design at final print width (often ~80–90 mm single, ~170–183 mm double).
- Fonts: sans (Arial/Helvetica equivalents); size for *printed* width, not the IDE pane.
- Line art → PDF/SVG (`cairo_pdf` if fonts drop); photos/rasters → PNG/TIFF ≥300 dpi.
- Panel tags via `plot_annotation(tag_levels = "A")` (or journal-specific `a`/`A`).
- Shared project theme helper beats one-off `theme()` edits per figure.

```r
ggsave("fig1.pdf", fig, width = 173, height = 120, units = "mm",
       device = cairo_pdf, bg = "white")
ggsave("fig1.png", fig, width = 173, height = 120, units = "mm",
       dpi = 300, bg = "white")
```
