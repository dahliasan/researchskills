# R map recipes

Minimal patterns. Adapt CRS, colours, and paths to the project. Prefer project
helpers when they already exist.

## 1. Grey-land polar track map

```r
library(ggplot2)
library(sf)
library(rnaturalearth)

target_crs <- "+proj=laea +lat_0=-90 +lon_0=170 +datum=WGS84 +units=km"

tracks_sf <- st_transform(tracks_sf, target_crs)
world <- ne_countries(scale = "medium", returnclass = "sf") |>
  st_crop(xmin = -180, xmax = 180, ymin = -90, ymax = -30) |>
  st_transform(target_crs)

ggplot() +
  geom_sf(data = world, fill = "grey80", colour = "grey60", linewidth = 0.1) +
  geom_sf(data = fronts_sf, linetype = "dashed", colour = "grey20", linewidth = 0.3) +
  geom_sf(data = tracks_sf, aes(colour = group), linewidth = 0.5, alpha = 0.6) +
  geom_sf(data = colony_sf, shape = 17, size = 3, colour = "#D44D5C") +
  coord_sf(crs = target_crs, expand = FALSE) +
  theme_bw() +
  theme(panel.grid = element_blank())
```

## 2. Satellite polar overview with ggrepel

```r
library(ggplot2)
library(sf)
library(ggrepel)
library(maptiles)
library(ggspatial)
library(terra)
library(rnaturalearth)

target_crs <- paste0(
  "+proj=stere +lat_0=-90 +lon_0=0 +lat_ts=-71 ",
  "+x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
)

bbox_ll <- st_bbox(c(xmin = -180, xmax = 180, ymin = -90, ymax = -28), crs = 4326)
tiles <- get_tiles(bbox_ll, provider = "Esri.WorldImagery", zoom = 3, crop = TRUE)
r_proj <- project(rast(tiles), target_crs, method = "bilinear", res = 20000)

world <- ne_countries(scale = "medium", returnclass = "sf") |>
  st_crop(xmin = -180, xmax = 180, ymin = -90, ymax = -28) |>
  st_transform(target_crs)

pts <- st_transform(pts_ll, target_crs)
xy <- st_coordinates(pts)
pts$X <- xy[, 1]
pts$Y <- xy[, 2]

ggplot() +
  theme_void() +
  layer_spatial(r_proj) +
  geom_sf(data = world, fill = NA, colour = "white", linewidth = 0.12) +
  geom_point(data = pts, aes(X, Y, size = n), shape = 21,
             fill = "#1a5fb4", colour = "#0d3b7a", stroke = 0.35, alpha = 0.88) +
  geom_text_repel(
    data = pts, aes(X, Y, label = map_label),
    size = 3, colour = "white", bg.color = "#000000d0", bg.r = 0.1,
    seed = 42, max.overlaps = 50
  ) +
  coord_sf(expand = FALSE, crs = target_crs, datum = target_crs)
```

If tiles fail, drop `layer_spatial` and fill `world` with a light blue-grey.

## 3. Raster surface with tidyterra

```r
library(ggplot2)
library(tidyterra)
library(terra)

r <- rast("habitat.tif")  # already in display CRS, or project() first

ggplot() +
  geom_spatraster(data = r) +
  scale_fill_viridis_c(option = "inferno", na.value = "transparent") +
  geom_sf(data = land_sf, fill = "grey85", colour = NA) +
  coord_sf(expand = FALSE) +
  theme_void()
```

## 4. Ice or enviro contours (stars)

Useful when a continuous ice legend is hard to read:

```r
library(stars)
library(ggplot2)

ice_c <- ice_stars |>
  st_contour(breaks = c(5, 20, 40, 60, 80, Inf))

ggplot() +
  geom_sf(data = ice_c, aes(fill = as.factor(Min)), colour = NA) +
  scale_fill_manual(values = RColorBrewer::brewer.pal(9, "Blues")[3:9], name = "Sea ice") +
  geom_sf(data = tracks_sf, colour = "white", linewidth = 0.4) +
  coord_sf(crs = target_crs, expand = FALSE) +
  theme_minimal()
```

## 5. Scale bar

```r
library(ggspatial)

# ... after geoms ...
annotation_scale(location = "bl", width_hint = 0.25) +
  # annotation_north_arrow(location = "tl", style = north_arrow_minimal()) # only if needed
  coord_sf(crs = target_crs, expand = FALSE)
```

## 6. Export

```r
ggsave("figure_map.png", plot = last_plot(), width = 180, height = 120,
       units = "mm", dpi = 300, bg = "white")

ggsave("figure_map.pdf", plot = last_plot(), width = 180, height = 120,
       units = "mm", device = cairo_pdf, bg = "white")
```

## 7. Extent buffer recipe

```r
sp_ex <- sf::st_bbox(tracks_sf) |>
  sf::st_as_sfc() |>
  sf::st_buffer(50) |>   # units follow the CRS (km or m)
  sf::st_bbox()
```

Use the buffered bbox to crop rasters and set `coord_sf` limits consistently.
