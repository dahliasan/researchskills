---
name: ggplot-maps
description: >-
  Use when building or revising scientific maps and spatial figures in R with
  ggplot2, sf, ggspatial, tidyterra, maptiles, or rnaturalearth; when choosing
  polar projections, basemaps, track overlays, raster fills, scale bars, or
  ggsave/cairo export for marine or Southern Ocean maps. Companion to
  figure-design for R recipes. Does not choose analyses or invent data.
metadata:
  version: 0.1.0
---

# ggplot maps (R)

R/ggplot recipes for accurate, readable scientific maps. Pair with
`figure-design` for claim, integrity, accessibility, and caption QA.

## Scope

This skill owns:

- ggplot2 + `sf` map stacks and layer order
- projection and extent choices in R
- basemap, annotation, label, and raster patterns
- panel composition and export conventions for R figures

It does not own:

- figure purpose, claim framing, or integrity audit (`figure-design`)
- manuscript prose or captions as final copy (`manuscript-writing`)
- analysis design, filtering, or new aggregations

## Workflow

1. Confirm the map claim and source data with `figure-design` evidence gate.
2. Choose stack from the table below.
3. Fix CRS, crop, and layer order before styling.
4. Add labels, scale, and legend only where they help the claim.
5. Export at final journal size; then audit with `figure-design`.

## Stack chooser

| Need | Prefer |
|---|---|
| Vector tracks, points, polygons on a clean land mask | `ggplot2` + `sf` + `rnaturalearth` + `geom_sf` |
| Labelled site map with satellite context | `maptiles` + `ggspatial::layer_spatial` + coast `geom_sf` + `ggrepel` |
| Continuous raster (habitat, ice, SST, chl) | `terra` + `tidyterra` (`geom_spatraster`) or stars contours |
| Distance / orientation cues | `ggspatial::annotation_scale` (+ north arrow only if orientation is unclear) |
| Multi-panel maps or map + inset | `patchwork` (maps) or `cowplot` (mixed panels / insets) |
| Southern Ocean fronts context | `orsifronts` (or equivalent) as dashed `geom_sf` under tracks |
| Quick diagnostic (not manuscript) | base `plot` / `basf` is fine; do not ship it as the pub figure |

Prefer `terra`/`tidyterra` for new raster work. Treat legacy `raster` +
`rasterToPoints` pipelines as migrate-when-touched.

## Layer contract

Build bottom → top. Skip layers the claim does not need.

1. Basemap or land fill
2. Soft coast / land outline
3. Management regions or fronts (thin, dashed, low contrast)
4. Raster surface or contours (if primary)
5. Tracks / effort lines
6. Focal points (sightings, colonies, sites)
7. Labels (`ggrepel`)
8. Scale bar / north (if needed)
9. Legend and panel tags

Keep land quieter than data. Do not let satellite imagery overpower points or
tracks: thin white/light coasts, modest point stroke, high-contrast labels.

## Projection and extent

- Set one target CRS early; transform every layer into it before plotting.
- Southern Ocean defaults that work well:
  - **LAEA polar** for equal-area track/particle maps  
    `+proj=laea +lat_0=-90 +lon_0=<study> +datum=WGS84 +units=km`
  - **Polar stereographic** for Antarctic overview / imagery panels  
    `+proj=stere +lat_0=-90 +lat_ts=-71 +lon_0=0 +datum=WGS84 +units=m`
- Choose `lon_0` (or study meridian) so the focal region sits near the centre.
- Crop in lon/lat only when still in geographic CRS; after projection, use
  projected bbox + optional buffer (`st_bbox` → `st_as_sfc` → `st_buffer`).
- Plot with `coord_sf(crs = target, expand = FALSE)`. Use `datum = NA` when
  graticules add noise; keep them when readers need absolute lat/lon.

Helper pattern for lon/lat tables → polar `sf`:

```r
convert2polarsf <- function(data,
                            crs = "+proj=laea +lat_0=-90 +lon_0=170 +datum=WGS84 +units=km",
                            proj = 4326,
                            remove_coords = TRUE) {
  sf::st_as_sf(data, coords = c("lon", "lat"), crs = proj, remove = remove_coords) |>
    sf::st_transform(crs)
}
```

## Basemaps

| Situation | Approach |
|---|---|
| Manuscript track / dispersal map | Grey Natural Earth land (`ne_countries`) |
| Study-site overview, presentation, wiki | Esri World Imagery via `maptiles::get_tiles`, then project |
| Offline / tile failure | Fall back to Natural Earth fill; say so in caption |
| Ice / enviro context | Contours or semi-transparent raster over land, not under it |

Attribute imagery providers in the caption. Do not imply satellite pixels are
your analysis grid.

## Colour and legends

- Tracks / categories: fixed named colours stable across figures.
- Continuous surfaces: viridis family (`inferno` / `magma` common for habitat);
  CVD-safe; `na.value` transparent or explicitly masked.
- Ice / sequential fills: light→dark sequential (e.g. Blues); bin with contours
  when a continuous legend is noisy.
- Diverging only with a real midpoint (anomaly, residual).
- Prefer direct labels over large legends when there are few groups.

## Labels and annotations

- Use `ggrepel` for site and landmark labels; set a seed for stable layouts.
- On dark imagery, light text with dark halo (`bg.color` / `bg.r`) reads better.
- Keep landmark labels schematic; do not invent precise centroids as data.
- Scale bar after `coord_sf`. Skip north arrow on polar maps when orientation is
  obvious from the projection.

## Themes and titles

- Maps: `theme_void()` or a heavily stripped `theme_bw` / `theme_minimal`.
- Non-map companion panels: small shared theme helper (e.g. minimal base 10,
  no minor grid, bottom legend).
- Prefer caption / manuscript figure title over large in-plot `ggtitle` for
  journal deliverables when the project bans plot titles.

## Export

- Set `width` / `height` for the final column or page width, not the IDE pane.
- Raster maps / photos: PNG or TIFF ≥300 dpi (`bg = "white"`).
- Line maps: PDF or SVG; use `cairo_pdf` if fonts drop out.
- Save the generating script beside the export; keep CRS and data paths in
  comments at the top.

## Integrity reminders (R-specific)

Hand these to `figure-design` audit, but check while coding:

- Every `geom_sf` layer shares the plot CRS.
- Masked / NA / unsampled cells are visually distinct from zero.
- Contours and projected rasters state the source resolution.
- Management polygons cite their source (e.g. CCAMLR, EEZ gazetteer).
- Particle or simulated tracks are styled differently from observed tracks.

## Caption handoff

Give `manuscript-writing` / `figure-design`:

- projection name and why it was chosen
- basemap or land source
- what each layer is (observed vs simulated vs management)
- colour / size encodings and units
- date or period of imagery or enviro layers
- any display-only buffers or generalizations

## References

- [references/r-recipes.md](references/r-recipes.md) — copy-paste map patterns
- [references/layouts-and-colour.md](references/layouts-and-colour.md) — multi-panel layouts, palettes, export
- [references/resources.md](references/resources.md) — curated external tutorials
- Sibling: `figure-design` for plan / audit / journal adapt
