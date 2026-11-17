# Publication figure sizing

Official guidance checked 17 November 2026. Journal rules take precedence over
these examples. They differ and should not be combined into one mandatory range.

| Venue | Physical size | Figure lettering / export |
|---|---|---|
| [Nature Communications](https://www.nature.com/ncomms/submit/how-to-submit) | 88 mm single, 180 mm double column | Consistent sans-serif; vector PDF/EPS/AI for charts; bitmap images at least 300 dpi; nonvector line art 1,200 dpi |
| [Nature Communications submission guide](https://www.nature.com/documents/ncomms-submission-guide.pdf) | Prepare at expected print size | Older official brief suggests 5–8 pt; use current journal instructions when they differ |
| [Nature final submission](https://www.nature.com/nature/for-authors/final-submission) | 89 / 183 mm; full depth 247 mm | 5–7 pt other text; 8 pt bold panel labels; Helvetica/Arial; strokes 0.25–1 pt |
| [Ecology Letters](https://onlinelibrary.wiley.com/page/journal/14610248/homepage/forauthors.html) | 82, 110 or 173 mm | Smallest practicable final size; allow for reduction; vector PDF/EPS preferred; raster line/combination 600 dpi, photographs 300 dpi |
| [PLOS Biology](https://journals.plos.org/plosbiology/s/figures) | 6.68–19.05 cm wide (13.2 cm to match the text column); height up to 22.23 cm, which fills the page and pushes the caption elsewhere | Arial, Times or Symbol, 8–12 pt; use its required submission formats |

Nature's formatting and final-artwork pages give different dimensions. The values
above are from final submission; do not silently mix specifications from pages.

Nature Communications also has a [formatting PDF](https://www.nature.com/documents/ncomms-formatting-instructions.pdf)
which limits each figure to an A4-sized 179 × 260 mm area. Its web page describes
180 mm double-column placement. Record which instruction a submission follows;
do not describe column widths as universal maxima. Typography-only revisions
should preserve dimensions and panel layout where practical. Retune point size,
point-range fattening and stroke width independently when changing physical size.

## Height and layout

Journals fix the width (the column) and cap the height (the page), but they do
not fix the aspect ratio. Set the width first, set type for that width, then let
the height grow until nothing is crowded:

- The journal scales a figure to its column width, so export at that width and
  type sizes stay as set. Height changes spacing, not type size.
- A main-text figure usually shares its page with the caption; keep it about
  200 mm or less. Supplementary figures can use the full page.
- Put tick labels and axis titles only on the outer edges of a panel grid: the
  first column and the bottom row. A spare grid cell can hold the legend.
- When panels are assembled with cowplot, `rel_widths` and `rel_heights` share
  space by proportion, so a column with y-axis labels gets narrower plotting
  areas. Measure the label space instead: build one panel with and without the
  labels, convert each `ggplotGrob()` width or height that is not a `null` unit
  to mm, take the difference, and add it to the first column and the bottom row.

## R settings

[ggsave](https://ggplot2.tidyverse.org/reference/ggsave.html) defaults to inches.
Always specify physical units explicitly:

```r
p <- p + theme_bw(base_size = 8, base_family = "Helvetica") +
  theme(axis.text = element_text(size = 7),
        strip.text = element_text(size = 8),
        legend.text = element_text(size = 7))
ggsave("figure.pdf", p, width = 180, height = 150, units = "mm",
       device = cairo_pdf, bg = "white")
```

[ggplot2 text sizing](https://ggplot2.tidyverse.org/articles/faq-customising.html):
`element_text(size=...)` uses points; `geom_text` and text annotations historically
use millimetres. Use `size = 7 / .pt` for 7 pt, or `size.unit = "pt"` where the
installed version supports it. Cowplot label sizes use points. Relative theme
sizes can make tick labels smaller than the base size, so inspect them explicitly.

Vector text should remain editable with fonts embedded. DPI applies to raster
layers, not vector lettering. Preserve the existing export formats unless the
brief or journal calls for a change. A successful render does not establish
legibility: inspect representative dense panels and the full export.
