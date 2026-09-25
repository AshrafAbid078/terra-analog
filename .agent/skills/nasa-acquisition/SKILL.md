---
name: NASA data acquisition
description: Rules and guidelines for fetching, normalizing, and caching NASA data.
---

# Skill: NASA data acquisition

Applies to any work inside `src/acquire/`. Trigger on: fetching POWER, DEM, or MODIS LST data; writing anything that calls a NASA API; populating `data/targets.json`; touching `cache/` or `demo_fixtures/`.

## Hard rules

1. **Batch, not live.** Every acquisition script in this folder runs once, pre-event, to disk. Nothing in `src/api` or `web/` may call a NASA endpoint directly at request time — it reads from `cache/` or `demo_fixtures/` only.
2. **Every value gets a `source_url`.** When writing a value into `data/targets.json` or a cached predictor layer, record the exact dataset/granule/API endpoint it came from. A number with no traceable source is not allowed in this project — it directly costs Validity points at judging.
3. **Grid resolution is ~0.5°** (POWER's native climate grid). Resample DEM (finer, e.g. SRTM 30m) and MODIS LST down to this grid — don't leave layers at mismatched native resolutions. Finer than 0.5° for the final analysis grid is false precision.
4. **Cache everything, re-fetch nothing.** First successful pull writes to `cache/<source>/`. Every subsequent run reads the cache. Never re-hit a NASA endpoint for data you already have on disk.
5. **`safe.py` wraps every live call**: try live → fall back to `cache/` → fall back to `demo_fixtures/`. Never let a fetch failure raise during acquisition or during a demo rehearsal.

## Data sources in scope for this project

| Source | Provides | Notes |
|---|---|---|
| NASA POWER | Aridity, temperature range | Native ~0.5° grid — this sets the project's resolution |
| A DEM (SRTM / USGS 3DEP via Earthdata) | Elevation → derive slope + roughness | Derive slope/roughness yourself with numpy gradient ops after resampling |
| MODIS LST | Thermal / diurnal behaviour | Needs day/night compositing; expect cloud gaps — feed directly into the confidence formula in `compute-boundary`, don't paper over gaps |
| Solar System Treks (Moon Trek / Mars Trek) or PDS | The 4 target vectors | Shackleton crater rim, South pole plateau site, Jezero crater, Gale crater — exactly these 4, no others |

Do not add mineral or radiation data sources — those criteria were cut from FEATURES.md because no acquisition pipeline exists for them in this project.

## When exploring what's available

If an MCP server for CMR/PDS search is connected, use it to find real granule IDs and confirm dataset URLs before writing them into `targets.json` — don't recall a plausible-looking URL from memory. If no MCP server is connected, use `earthaccess`/CMR search directly in a script rather than guessing endpoint paths.
