# plan.md — Terra Analog

NASA Space Apps Challenge 2026 — Earth Locations that Analog Moon and Mars Bases. Master plan, ties together `FEATURES.md`, `DESIGN.md`, `structure.md`, and the `.agent/skills/` set into one build order. This is the file to re-read at the start of each build session.

## 1. What we're building

A similarity search over Earth. Pick a target (Moon or Mars site), and the tool scores every Earth grid cell against it on 6 physical criteria, ranks the best analogues, and shows the rationale criterion by criterion — with visible, adjustable weights, never a model's opinion of similarity.

## 2. Data sources (locked) — acquisition mode: manual download, not live scripts

Downloads are happening by hand now, straight into the IDE workspace, in whatever format each portal exports (CSV, GeoTIFF, NetCDF, etc.) — not via a live-fetch script hitting an API at build time. This changes what `src/acquire` actually does: it's a **loader/normalizer**, not a **fetcher**. Land every manual download in `data/raw/<source>/` exactly as downloaded, untouched; `src/acquire/load_*.py` reads from there, resamples to the common ~0.5° grid, and writes the normalized layer into the cache — it never calls a NASA endpoint itself.

| Source | Provides | Criteria keys | Raw folder |
|---|---|---|---|
| NASA POWER | Global climate normals, on a regular grid | `aridity`, `temp_range_c` | `data/raw/power/` |
| DEM (USGS 3DEP or Earthdata) | Elevation, from which slope + roughness are derived | `elevation_m`, `slope_deg`, `roughness` | `data/raw/dem/` |
| MODIS land surface temperature | Diurnal range — the dimension that makes deserts and polar deserts behave like other worlds | `lst_diurnal_c` | `data/raw/modis_lst/` |
| Moon Trek, Mars Trek, PDS | Target-side characteristics for the planetary site being matched | feeds `data/targets.json` | `data/raw/targets/` |

`CRITERIA = ["aridity", "temp_range_c", "elevation_m", "slope_deg", "roughness", "lst_diurnal_c"]` — this exact list and key naming is now canonical across `src/compute`, `data/targets.json`, and the frontend. Use these key names everywhere, not the display labels ("Aridity", "Temperature", etc.) — keep raw keys and display labels in separate places so a rename of one doesn't silently break the other.

**Keep the exact download source noted somewhere per file** (a sibling `.source.txt` next to each raw file, or a running note) — the portal URL and access date, not just the filename — since `docs/DATA_SOURCES.md` and every `source_url` in `data/targets.json` need to trace back to something real, and that's much harder to reconstruct after the fact than to jot down now while downloading.

## 3. Similarity engine (locked, as given)

```python
import numpy as np

CRITERIA = ["aridity", "temp_range_c", "elevation_m", "slope_deg",
            "roughness", "lst_diurnal_c"]

def similarity(earth_stack, target_vector, weights, ranges):
    """Weighted normalised distance. Returns a 0-1 score per cell plus the
    per-criterion contribution, so the interface can explain any result."""
    contrib = {}
    total = np.zeros(earth_stack[CRITERIA[0]].shape)
    wsum = sum(weights[c] for c in CRITERIA)
    for c in CRITERIA:
        lo, hi = ranges[c]
        d = np.abs(earth_stack[c] - target_vector[c]) / (hi - lo)
        contrib[c] = np.clip(1 - d, 0, 1)
        total += weights[c] * contrib[c]
    return total / wsum, contrib
```

Lives in `src/compute/similarity.py` exactly as-is. `ranges[c]` (the `lo, hi` normalization bounds per criterion) still needs concrete values — pull them from the actual data distribution once the Earth predictor stack is built, not guessed ahead of time. `data_confidence` (the separate coverage-weight formula from `FEATURES.md`) is a sibling function in the same file, not part of `similarity()` itself.

## 4. Targets (locked, 4 total)

- Shackleton crater rim (Moon)
- South pole plateau site (Moon)
- Jezero crater (Mars) — primary demo target
- Gale crater (Mars)

Each needs a `target_vector` with all 6 `CRITERIA` keys plus a `source_url` per value in `data/targets.json`, sourced from Moon Trek / Mars Trek / PDS.

## 5. Architecture (see `structure.md` for the full tree)

- `data/raw/` — manually downloaded files, exactly as exported from each portal, gitignored (too large / not the point of the repo), one subfolder per source
- `src/acquire/` — loads and normalizes `data/raw/` into the common grid, resamples, writes to `cache/`; no live API calls
- `src/compute/` — `similarity.py`, `confidence.py`, deterministic only, no LLM ever
- `src/ai/` — `insight.py`, `compare_verdict.py`, the only two files allowed to call an LLM, both take already-computed numbers and return prose only
- `src/api/` — FastAPI, reads `cache/`/`demo_fixtures/`, never calls NASA at request time
- `web/` — React + Vite, 6 routes, client-side re-rank on slider drag (mirrors `similarity()` in JS — see open item below)
- `cache/` gitignored, `demo_fixtures/` committed

## 6. Design (see `DESIGN.md` for full tokens)

Light theme default (warm off-white, terracotta/forest-teal accent), dark theme available via `data-theme` toggle (original navy/teal console look). Radar chart (6 axes, fixed criteria order) on site detail; overlaid radar + full comparison table on compare; illustrated flat SVG imagery instead of stock photos, matching the theme's own tokens.

## 7. Tooling and project docs

- `AGENTS.md` at repo root — the AI boundary: what the model may and may never compute. Antigravity reads this every session.
- `CLAUDE.md` at repo root — coding standards: how to write the code, once it's allowed to. Complements `AGENTS.md` rather than repeating it.
- `docs/DATA_SOURCES.md` — every dataset cited, feeds the `/about` page directly.
- `docs/AI_USE.md` — the living AI-disclosure log, updated through the build, not written the night before submission.
- `.agent/skills/nasa-acquisition/`, `.agent/skills/compute-boundary/`, `.agent/skills/frontend-tokens/` — task-triggered skills, already written. (`nasa-acquisition` should be re-read now that acquisition is manual-download-based, not live-fetch — its acquisition rules still hold, only the mechanism changed.)
- One MCP server (`datalayer/earthdata-mcp-server`) registered in `~/.gemini/antigravity/mcp_config.json` — dev-time only, for real granule search while writing loader scripts, never called at runtime by the deployed app

## 8. AI-layer boundary (for judging disclosure)

Similarity scoring and confidence scoring are code, not AI — `docs/AI_USE.md` should say this explicitly. The only two LLM calls in the whole project are the site-detail rationale and the compare-page verdict, both narrating numbers they didn't produce. Both degrade gracefully; the dashboard, radar chart, bars, and data table never block on them.

## 9. Open items (decide before or during build, not after)

- **`ranges[c]` normalization bounds** — compute these once the raw downloads are loaded and normalized; don't hardcode placeholder numbers into the demo.
- **JS mirror of `similarity()`** for the client-side live re-rank — write a small golden-test fixture (a few hand-checked site/target pairs) that both the Python and JS versions must pass, so a later edit to one doesn't silently desync from the other.
- **Terrain type tags** on the dashboard filter — cut-if-needed; only build if a simple threshold rule on the 6 computed values gets written, not a hand-labeled list.
- **Per-file source note** — confirm each `data/raw/<source>/` folder actually has its `.source.txt` (portal URL + access date) before moving on to loading scripts; missing this now means guessing it later for `docs/DATA_SOURCES.md`.

## 10. Build order (48 hours, cut-list if behind)

1. Finish manual downloads into `data/raw/`, one `.source.txt` per file — already underway
2. Loader/normalizer scripts (`src/acquire/load_*.py`) + `data/targets.json` (all 4 targets, cited) — nothing else can start meaningfully until this exists, even as a small trimmed version
3. `src/compute/similarity.py` + `confidence.py`, tested against a handful of real site/target pairs
4. `src/api` serving the computed scores from `demo_fixtures/`
5. Frontend: Dashboard + Site Detail first (these two carry the killer demo), Select Target next, Compare and About last
6. `src/ai/insight.py` and `compare_verdict.py` — wired last, since every page must work with these absent or failing

If behind schedule, cut in this order: Compare page → terrain tags → satellite/illustrated imagery polish → second Moon/Mars target (demo on Jezero + Shackleton rim only) — never cut the confidence formula or the source citations, since those are what the judging rubric is actually checking for.
