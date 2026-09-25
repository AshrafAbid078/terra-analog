# build-prompt.md — Terra Analog

Paste this into Antigravity to start or resume a build session. It assumes `AGENTS.md`, `CLAUDE.md`, `plan.md`, `FEATURES.md`, `DESIGN.md`, `structure.md`, `docs/DATA_SOURCES.md`, `docs/AI_USE.md`, and `.agent/skills/` already exist in the repo — read them, don't ask me to repeat their content.

---

**You are building Terra Analog**, an Earth-Moon-Mars analog site finder for NASA Space Apps Challenge 2026 (challenge: "Earth Locations that Analog Moon and Mars Bases"). A similarity search over Earth: pick a target site (Moon or Mars), score every Earth grid cell against it on 6 physical criteria, rank the best analogues, and show the rationale criterion by criterion with visible, adjustable weights.

## Before writing anything

Read, in this order: `AGENTS.md` (what you may never compute), `plan.md` (the full plan and current build-order position), `FEATURES.md` (page-by-page spec), `DESIGN.md` (tokens and per-page visual treatment), `structure.md` (exact file tree), and the relevant file(s) in `.agent/skills/` for whatever you're about to touch. `CLAUDE.md` governs how you write code once you're in bounds.

## Hard rules — non-negotiable, repeated here because they matter most

1. **Never compute a similarity score, confidence score, or terrain tag with an LLM.** These live only in `src/compute/`, as deterministic functions. If you can't compute something, say so — don't approximate it.
2. **Only `src/ai/insight.py` and `src/ai/compare_verdict.py` may call an LLM**, and only to narrate numbers already computed elsewhere.
3. **Targets are locked at exactly 4**: Shackleton crater rim, South pole plateau site (Moon), Jezero crater, Gale crater (Mars). **Criteria are locked at exactly 6**, these raw keys: `aridity`, `temp_range_c`, `elevation_m`, `slope_deg`, `roughness`, `lst_diurnal_c`. Don't add, rename, or substitute any of these without being asked.
4. **Data acquisition is manual-download-based.** `src/acquire/` loads and normalizes files already sitting in `data/raw/<source>/` — it never calls a NASA API. If a raw file is missing, raise a clear error naming the expected path; don't invent a value or skip the source silently.
5. **Every number needs a real source.** A value in `data/targets.json` or a cached layer with no traceable `source_url` / entry in `docs/DATA_SOURCES.md` doesn't go in.
6. **`src/api` and `web/` never call NASA or the live LLM provider directly outside the two `src/ai/` files** — everything else reads from `cache/` or `demo_fixtures/`.
7. **Colors only from `DESIGN.md` tokens.** No raw hex in component files. Both light (default) and dark themes must work for anything you style.

## Build order — work through this in sequence, don't jump ahead

Check `plan.md` section 10 for the current position; broadly:

1. Loader/normalizer scripts in `src/acquire/` reading `data/raw/`, plus `data/targets.json` with all 4 targets cited
2. `src/compute/similarity.py` (exact formula already given in `plan.md`) and `src/compute/confidence.py`, both with tests in `src/tests/` against `src/tests/golden_similarity.json`
3. `src/api/` serving computed scores from `demo_fixtures/`
4. `web/` — Dashboard and Site Detail first (these carry the demo), then Select Target, then Compare and About
5. `web/src/lib/similarity.ts` — JS mirror of `similarity.py`, tested against the same golden fixture, used only for the client-side live-slider re-rank
6. `src/ai/insight.py` and `src/ai/compare_verdict.py` — last, and every page above must already work correctly with these absent or failing

## After each phase

- Update `docs/AI_USE.md` with what you (Antigravity) generated in that phase — don't wait until the end.
- Update `docs/DATA_SOURCES.md` if a new dataset detail (URL, access date, product ID) became concrete.
- Run whatever tests exist in `src/tests/` before moving to the next phase.
- Tell me explicitly if something in `FEATURES.md` or `plan.md` conflicts with what you're finding in the actual data — don't silently resolve the conflict by cutting scope or fabricating a value.

## What NOT to do, specifically (past drift we've already caught)

- Don't add "mineral similarity" or "radiation exposure" as criteria — no acquisition pipeline exists for them, they were deliberately cut.
- Don't build the terrain-type filter tags unless you also write the simple threshold rule for them — no hand-labeled lookup table.
- Don't let the data-confidence percentage and the per-criterion checklist (✓/⚠/✗) be computed separately — they must read from the same array, or they'll disagree.
- Don't hardcode `ranges[c]` normalization bounds with placeholder numbers — compute them from the actual loaded data once it exists.
