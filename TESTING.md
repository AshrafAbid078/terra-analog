# TESTING.md — Terra Analog

Step-by-step checks, phased to match the build order in `plan.md`. Run the checks for a phase before moving to the next one — catching a bad source URL or a broken fallback early is much cheaper than catching it during a demo rehearsal.

## Phase 1 — Data acquisition (manual downloads + loaders)

- [ ] Every file in `data/raw/<source>/` has a sibling `.source.txt` with the portal URL and access date
- [ ] `data/targets.json` has all 4 targets, each with all 6 criteria keys (`aridity`, `temp_range_c`, `elevation_m`, `slope_deg`, `roughness`, `lst_diurnal_c`) and a `source_url` per value — no missing keys, no placeholder numbers
- [ ] `src/acquire/load_power.py`, `load_dem.py`, `load_modis_lst.py` each run standalone and write a normalized layer to `cache/` without errors
- [ ] Deleting one raw file and re-running its loader raises a clear error naming the missing path — doesn't silently produce empty/zero data
- [ ] The three normalized layers (POWER, DEM-derived, MODIS LST) are all on the same ~0.5° grid — spot-check the shape/resolution of each cached array matches

## Phase 2 — Compute layer (`src/compute/`)

- [ ] `src/tests/golden_similarity.json` exists with at least 3–5 hand-checked site/target pairs and their expected scores
- [ ] `test_similarity.py` passes against the golden fixture
- [ ] `test_confidence.py` passes — spot-check one cell with known full coverage (all 6 criteria = 1.0 → 100%) and one with a deliberately missing criterion (should drop proportionally, e.g. 5/6 full → ~83%, or matches the documented weighted example → 91%)
- [ ] Re-running `similarity()` twice with identical inputs gives bit-identical output (confirms no hidden randomness/state)
- [ ] Changing one weight and re-running actually changes the ranking order for at least one pair of sites (confirms the weights aren't silently ignored)
- [ ] `ranges[c]` normalization bounds are pulled from real loaded data, not hardcoded placeholders — check the values in code against the actual min/max of the cached layers

## Phase 3 — API (`src/api/`)

- [ ] `GET` ranked sites for each of the 4 targets returns a non-empty, correctly-sorted list
- [ ] `GET` one site's detail returns all 6 per-criterion scores + the confidence breakdown, matching what `similarity()`/`confidence()` compute directly for the same inputs
- [ ] `POST` compare with 2–3 site ids returns a table with the same 6-criteria + overall-score shape for each
- [ ] Kill network access (or point `cache/`/`demo_fixtures/` paths at a temp empty dir) and confirm the API still returns `demo_fixtures/` data via `safe.py` rather than erroring
- [ ] No endpoint in `src/api/` calls a NASA URL or an LLM provider directly — grep for `requests.get`/`fetch` outside `src/acquire/` and `src/ai/` and confirm there's nothing

## Phase 4 — Frontend, page by page

- [ ] **Landing** — loads with no console errors, CTA navigates to `/select-target`, stats bar numbers aren't hardcoded to stale values
- [ ] **Select Target** — exactly 4 targets shown (2 Moon, 2 Mars), no 5th/6th option, preview panel updates on selection, "Find matches" carries the target through to `/dashboard`
- [ ] **Dashboard** — map markers color correctly by `--score-high/medium/low` (verify at least one site in each band if the demo data allows), ranked list matches map marker order, min-match slider actually filters
- [ ] **Site Detail** — radar chart's 6 axes are in the fixed order (aridity, temperature, elevation, slope, roughness, thermal), breakdown bars match the radar chart's own numbers exactly, confidence checklist (✓/⚠/✗) matches the headline confidence %, weight sliders re-rank live using `similarity.ts` and match what the server originally returned before any slider was touched
- [ ] **Compare** — overlay radar chart's legend colors match the table's column header colors, "Overall" row is bolded and correctly colored by score band
- [ ] **About** — data source list matches `docs/DATA_SOURCES.md` exactly, not a separate hand-written summary that could drift from it
- [ ] Every page tested in **both light and dark theme** — no invisible text, no token left unstyled in one mode
- [ ] Every page tested at a narrow (mobile) width — no horizontal overflow, no clipped chart

## Phase 5 — AI layer (`src/ai/`)

- [ ] `insight.py` output explicitly contains at least one "why it doesn't" point, not only strengths — confirm this isn't just prompted for but actually present in a few real outputs
- [ ] Force `insight.py` to fail (bad API key, timeout) and confirm Site Detail still renders scores/bars/radar/table with no broken UI where the prose would be
- [ ] Same graceful-failure check for `compare_verdict.py` on `/compare`
- [ ] Spot-check 2–3 generated insights against the actual computed numbers for that site — confirm the prose isn't inventing a criterion or contradicting the displayed percentage

## Phase 6 — Full offline demo rehearsal (do this before judging, not the morning of)

- [ ] Disconnect from the network entirely
- [ ] Walk through all 6 pages in order, using only `demo_fixtures/` — nothing blank, nothing stuck on a loading spinner
- [ ] Time the full walkthrough — confirm it fits inside the demo video length you're targeting
- [ ] Confirm the "killer demo" moment (pick Jezero → map lights up → top result's breakdown appears) works smoothly and fast, since this is the single highest-value moment in the whole build

## Judging-alignment spot checks

- [ ] Every score-bearing page traces back to `docs/DATA_SOURCES.md` — could you click through from any percentage on screen to a real citation?
- [ ] `docs/AI_USE.md` has been updated at least once per work session, not left for a final pass
- [ ] The challenge name, a public repo link, and the project page are all confirmed ready — the three cheap points teams throw away
