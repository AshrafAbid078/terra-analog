# FEATURES.md
## Project: Terra Analog — Earth-Moon-Mars Analog Site Finder
### NASA Space Apps Challenge 2026 — "Identify Earth Locations that Analog the Permanent Moon Base Locations and Mars"

**v3.** This is the page-by-page spec. For the master build plan, the locked `similarity()` code, and the build order, see `plan.md`. For the AI boundary rule, see `AGENTS.md`. For colors and per-page visual treatment (charts, illustrations, tables), see `DESIGN.md`.

**v2 note (kept for history):** Three things were inconsistent across the app-flow diagram, the match-score mockup, and the original FEATURES.md draft; that version made one canonical decision for each and applied it everywhere below.

| Item | Was (inconsistent across docs) | Now (canonical) |
|---|---|---|
| Targets | 2 in the flow diagram, 6 in the old FEATURES.md draft | **4 total** — 2 Moon, 2 Mars (list below) |
| Match criteria | 6 in the score-card mockup, but "mineral similarity" + "radiation exposure" in the old FEATURES.md draft | **6 only**: aridity, temperature range, elevation, slope, roughness, thermal behaviour |
| Data confidence | Shown as a bare 91% with no defined source | **Deterministic coverage formula** (below) — computed in `src/compute`, never asserted by the model |

Structure: 6 separate full pages/routes (unchanged).

---

## Canonical target list

Four targets total. No open-ended "Mare regions" / "Highlands" / "Utopia Planitia" style categories — those are broad regions, not point locations, so they can't produce a single cited target vector inside a 48-hour build. Each of the four below needs one row in `data/targets.json` with a `source_url` per value.

- 🌙 **Shackleton crater rim** (Moon) — permanently-lit ridge candidate, near-permanent shadow in the crater itself
- 🌙 **South pole plateau site** (Moon) — the broader flat highland candidate near Shackleton–de Gerlache ridge
- 🔴 **Jezero crater** (Mars) — Perseverance landing site, the challenge's own "killer demo" target
- 🔴 **Gale crater** (Mars) — Curiosity landing site, chosen as the second Mars target because its geology contrasts with Jezero enough to make the ranking interesting

---

## Canonical match criteria (6, no more)

Aridity, temperature range, elevation, slope, surface roughness, thermal (diurnal) behaviour. Sourced entirely from NASA POWER (aridity, temperature range), a DEM (elevation → derived slope and roughness), and MODIS LST (thermal behaviour) — see Data Sources below.

**Display name → raw key** (the raw keys are what `similarity.py`, `data/targets.json`, and `web/src/lib/similarity.ts` actually use — never the display names):

| Display name | Raw key |
|---|---|
| Aridity | `aridity` |
| Temperature range | `temp_range_c` |
| Elevation | `elevation_m` |
| Slope | `slope_deg` |
| Roughness | `roughness` |
| Thermal behaviour | `lst_diurnal_c` |

"Mineral similarity" and "radiation exposure," present in the original FEATURES.md draft, are **cut**. Neither has an acquisition script, a cached dataset, or a target-vector value defined anywhere in this project, so building them into the radar chart or the breakdown bars now would mean either fabricating numbers (fatal for the Validity score) or a late scramble for a 7th and 8th data source. If there's time left after the core 6 are solid, mineral similarity (via PDS mineral maps) is the more plausible stretch addition of the two — but it does not appear in any Must-have page below.

---

## Data confidence — deterministic formula

Not a single opaque percentage. Each of the 6 criteria gets a coverage weight for the given Earth grid cell, computed in `src/compute` alongside `similarity.py`:

- **1.0 (full)** — native data resolution matches or exceeds the analysis grid, no gaps in that cell
- **0.5 (limited)** — data available but coarser than the grid, interpolated, or partial temporal coverage (e.g. MODIS LST cloud gaps)
- **0.0 (missing)** — no valid data for that criterion at that cell

```
data_confidence = mean(coverage_weight across the 6 criteria) × 100
```

Example matching the mockup: 5 criteria at full coverage (1.0 each) + thermal behaviour limited (0.5) → (5 × 1.0 + 0.5) / 6 = 91.7% ≈ **91%**. Same numbers that drive the per-criterion checklist (✓ / ⚠ / ✗) also drive the headline percentage — they can never disagree, because they come from the same array.

---

## PAGE 1: `/` — Landing Page

**Purpose:** First impression, looks good in demo video

- Hero section: project name + one-line tagline ("Find Earth's twin for the next Moon base")
- Background visual: Earth/Moon/Mars imagery or subtle animation
- Primary CTA button: "Explore Analog Sites" → navigates to `/select-target`
- Stats bar: "X candidate sites analyzed", "Y datasets used"
- Footer: NASA/data source attribution (short), team name

---

## PAGE 2: `/select-target` — Target Selector (Onboarding)

**Purpose:** User decides what they're searching for

- Two large toggle cards: 🌙 Moon / 🔴 Mars
- On selection, a list of exactly the targets defined above (2 per body) — no free-text or open-ended region picker
- Preview card showing selected target's basic info (temp range, elevation, known conditions) — same 6 values that drive the match score, so the preview and the results page are never showing different numbers for the same target
- "Find Matches" button → navigates to `/dashboard` with target pre-applied as filter

---

## PAGE 3: `/dashboard` — Explore / Main Results Page

### 3.1 Left Sidebar — Filters
- Minimum match score slider
- Sort by: Highest match / Alphabetical / Region
- Terrain type tags (Desert, Polar, Volcanic, Cave, Arid) — see note below; treat as **cut-if-needed**, not core, since it needs its own derivation rule

### 3.2 Center — Interactive Map
- World map (Leaflet/Mapbox)
- Markers for each candidate Earth site, color-coded by match score (green = high, yellow = medium, red = low)
- Hover: tooltip with name + score%
- Click: navigates to `/site/:id` (Page 4)

### 3.3 Right Sidebar — Ranked List
- Scrollable card list, each card shows:
  - Site name + country
  - Match score (prominent %)
  - Thumbnail image (if available)
  - One-line AI-generated summary
  - "View Details" button → navigates to `/site/:id`
  - Checkbox: "Add to Compare" → adds to selection for Page 5

### 3.4 Empty / Error States
- "No matches found for these filters" message
- Loading skeleton/spinner while data or AI insight is being fetched

**Note on terrain type tags:** these aren't in any dataset yet. If kept, derive them with a simple deterministic rule from the same 6 computed values (e.g. aridity above a threshold + low roughness → "Desert"; elevation + roughness above thresholds → "Volcanic") rather than hand-labeling sites — otherwise it's a 7th, un-cited "factor" competing with the six that are actually sourced.

---

## PAGE 4: `/site/:id` — Site Detail Page

**Purpose:** Deep analysis of one specific site

- Header: site name, coordinates (lat/long), overall match score (large, prominent) + data confidence score, shown side by side
- **Radar/Spider chart**: the 6 canonical criteria only — aridity, temperature range, elevation, slope, roughness, thermal behaviour
- **Match Score Breakdown**: same 6 criteria as percentage bars, so the radar chart and the bars are always the same underlying array rendered two ways, never two separate computations
- **Data Confidence / Quality Indicator**: headline % (formula above) plus the per-criterion checklist (✓ full / ⚠ limited / ✗ missing) driving it
- **AI Insight box**: LLM-generated 2–3 paragraph explanation, split into two labeled sections:
  - **Why it matches** — strongest similarities, referencing the actual computed scores
  - **Why it doesn't** — meaningful differences and limitations, so the site is presented as an analog for specific characteristics, not an exact stand-in for the Moon/Mars environment
- **Data table**: raw values side by side (Earth vs. target), each row links to its `source_url`
- Satellite imagery / reference photo (if available)
- Button: "Add to Compare" → navigates to `/compare` with this site included
- Weight sliders (one per criterion, 6 total) with live re-rank, matching the shared architecture's similarity engine

---

## PAGE 5: `/compare` — Comparison Page

**Purpose:** Compare 2–3 sites side by side

- Table/grid: columns = each selected site, rows = the 6 criteria + overall score + data confidence
- Combined radar chart (overlay of selected sites)
- Short AI verdict text: which site is best for which use case (e.g. "best for thermal extremes")
- Option to remove a site from comparison or add another from `/dashboard`

---

## PAGE 6: `/about` — About / Data Sources Page

**Purpose:** Transparency (boosts validity score in judging)

- Full list of NASA/space agency datasets used: NASA POWER, a DEM source, MODIS LST, plus wherever the four target vectors were sourced (e.g. Solar System Treks)
- Methodology explanation: how the similarity score and the data confidence score are calculated (plain-language version of the formula above)
- Team info + link to the official challenge statement
- `docs/AI_USE.md` disclosure, linked or summarized here — kept live during the build, not written the night before submission

---

## Global Elements (present on all pages)
- Top navbar: Logo, Home, Explore, Compare, About — visible/accessible from every page
- Consistent loading states (skeleton/spinner) wherever data or AI calls are in flight
- Responsive layout (mobile-friendly)
- Consistent error handling (failed API calls show a retry option, not a blank screen)
- Every live external call wrapped in the shared `safe.py` pattern: try live → fall back to cache → fall back to a committed fixture in `demo_fixtures/`, so nothing can go blank on stage

---

## Feature Priority (for time-constrained build)

### Must-have (core demo)
- Landing page (Page 1)
- Target Selector (Page 2) — exactly the 4 canonical targets
- Dashboard: map + ranked list + sort/score-slider (Page 3), filter sidebar without terrain tags
- Site Detail: radar chart + breakdown bars + data confidence + AI insight (Page 4), using the 6 canonical criteria only
- At least 5–8 real candidate sites with computed scores against Jezero (the primary demo target)

### Cut-if-needed (nice-to-have)
- Comparison page (Page 5) — can be demoed manually by describing two sites if time is short
- Terrain type tags on the dashboard filter — only add once a simple derivation rule exists (see note above)
- Satellite imagery on Site Detail
- Separate About page (Page 6) — can shrink to a footer/modal if time runs out
- Second Moon and second Mars target (Gale crater, second Moon site) — if behind schedule, demo on Jezero + Shackleton rim only and mention the other two as "supported, not yet populated"

---

## AI Layer — where AI is actually used (for judging the "AI-powered" claim)

This section is corrected from the original draft, which mislabeled the similarity scoring itself as "AI." Per the shared architecture's rule, **the model may narrate, never compute.** Concretely:

1. **Similarity scoring — NOT AI.** Feature-vector comparison (Earth site vs. target) is a deterministic weighted-distance function in `src/compute/similarity.py`. It runs the same way every time on the same inputs. No LLM call.
2. **Data confidence — NOT AI.** The coverage-weight formula above is likewise plain code in `src/compute`, alongside `similarity.py`.
3. **Insight generation — this is the actual AI use.** One LLM call per site takes the already-computed scores and raw factor values and writes the "Why it matches / Why it doesn't" prose. The model is given the numbers; it does not decide them.
4. **Compare verdict — also actual AI use.** One LLM call takes 2–3 sites' already-computed scores and writes a short "best for X use case" recommendation.
5. **Explainable scoring display** and **limitations-aware insight** (separating matches from non-matches) are UI/prompt requirements on top of #3 and #4, not separate AI features.

Both LLM calls (#3, #4) degrade gracefully — the dashboard, radar chart, breakdown bars, and data table all render from computed scores alone; only the prose blocks are missing if the LLM call fails or is slow. Nothing on the core dashboard blocks on the AI layer.
