# External resources

Practical references for R maps, layouts, colour, and publication export.
Deep notes: [layouts-and-colour.md](layouts-and-colour.md). Copy-paste map
patterns: [r-recipes.md](r-recipes.md).

## Start here

1. [patchwork](https://patchwork.data-imaginist.com/) — multi-panel composition
2. [Wilke — Color basics](https://clauswilke.com/dataviz/color-basics.html) + [pitfalls](https://clauswilke.com/dataviz/color-pitfalls.html)
3. [ggplot2 book — colour scales](https://ggplot2-book.org/scales-colour.html) + [arranging plots](https://ggplot2-book.org/arranging-plots.html)
4. This skill’s [layouts-and-colour.md](layouts-and-colour.md) for decision trees

## ggplot2 + sf maps

- [r-spatial: ggplot2 and sf (parts 1–3)](https://r-spatial.org/r/2018/10/25/ggplot2-sf.html) — `geom_sf`, themes, layers, `ggspatial`, insets
- [Geocomputation with R — Advanced map making](https://r.geocompx.org/adv-map) — modern map grammar; ggplot/`ggspatial` alternatives
- [ggplot2 book](https://ggplot2-book.org/) — scales, themes, coords that maps inherit
- [ggspatial](https://paleolimbot.github.io/ggspatial/) — scale bars, north arrows
- [tidyterra](https://dieghernan.github.io/tidyterra/articles/welcome) — SpatRaster in ggplot
- [maptiles](https://cran.r-project.org/package=maptiles) — basemap tiles
- [rnaturalearth](https://docs.ropensci.org/rnaturalearth/) — land vectors
- [Geocompx inset maps](https://geocompx.org/post/2019/ggplot2-inset-maps/) · [UPGo beautiful maps](https://upgo.lab.mcgill.ca/2019/12/13/making-beautiful-maps/)

## Layouts (multi-panel)

- [patchwork Layout](https://patchwork.data-imaginist.com/articles/guides/layout.html) · [Annotation](https://patchwork.data-imaginist.com/articles/guides/annotation.html)
- [Wilke — Multi-panel figures](https://clauswilke.com/dataviz/multi-panel-figures.html)
- [cowplot — Drawing with/on plots](https://wilkelab.org/cowplot/articles/drawing_with_on_plots.html) · [Shared legends](https://wilkelab.org/cowplot/articles/shared_legends.html)
- [ggh4x Facets](https://teunbrand.github.io/ggh4x/articles/Facets.html) — nested facets
- [aplot](https://yulab-smu.top/aplot/) — axis-locked side panels
- Workshops: [NIH CCR Lesson 6](https://bioinformatics.ccr.cancer.gov/docs/data-visualization-with-r/Lesson6/) · [FMI combining panels](https://fmicompbio.github.io/intermediate_ggplot2/5_combining_plot_panels.html)

## Colour palettes

- [Paul Tol schemes (PDF)](https://sronpersonalpages.nl/~pault/data/colourschemes.pdf) · [khroma](https://packages.tesselle.org/khroma/articles/tol.html)
- [colorspace HCL](https://colorspace.r-forge.r-project.org/articles/hcl_palettes.html) · [HCL Wizard](https://hclwizard.org/)
- [Crameri Scientific Colour Maps](https://www.fabiocrameri.ch/colourmaps/) · [scico](https://github.com/thomasp85/scico)
- [viridis intro](https://cran.r-project.org/web/packages/viridis/vignettes/intro-to-viridis.html)
- [ColorBrewer 2.0](https://colorbrewer2.org/) · [rcartocolor](https://jakubnowosad.com/rcartocolor/)
- [Wilke — Redundant coding](https://clauswilke.com/dataviz/redundant-coding.html)
- [Scherer ggplot tutorial](https://www.cedricscherer.com/2019/08/05/a-ggplot2-tutorial-for-beautiful-plotting-in-r/) · [Heiss colour notes](https://datavizf24.classes.andrewheiss.com/resource/colors.html)
- [r-statistics.co ggplot2 colours](https://r-statistics.co/ggplot2-Colours.html)

## Themes and export

- [Publication-quality figures checklist](https://r-statistics.co/Publication-Quality-Figures-in-R.html)
- [Quent 2026 — publication-ready ggplot2](https://jaquent.github.io/2026/02/creating-actually-publication-ready-figures-for-journals-using-ggplot2/)
- [Journal size / DPI / font guide](https://scholarviz.com/blog/journal-target-size-dpi-font-decision-tree)
- [CCT publication ggplot workshop](https://cct-datascience.quarto.pub/crafting-publication-quality-data-visualizations-with-ggplot2/)

## Optional teaching

- [ggplot2 Uncharted — spatial modules](https://www.ggplot2-uncharted.com/)
- [Geospatial 101 workbook — publication maps](https://geospatial.101workbook.org/Visualizations/GRWG_Maps_R.html)

## Sibling skills

- `figure-design` — claim, integrity, accessibility, caption QA
- `ggplot-maps` — R map recipes (this skill)
