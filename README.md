# 🌍 Terra Analog

### Earth-Moon-Mars Analog Site Finder
**NASA Space Apps Challenge 2026**

---

> *Which places on Earth most closely resemble the surface conditions of a lunar or Martian base site?*

Terra Analog answers that question with real NASA data. Pick one of four planetary targets — a crater rim on the Moon or a landing site on Mars — and the tool scores every Earth grid cell against it on six physical criteria, ranks the best analogues, and explains *why* each site matched, criterion by criterion.

---

## 🔭 How It Works

```
Earth Data (POWER, DEM, MODIS LST)
        ↓
   Normalize to ~0.5° grid
        ↓
   Score against planetary target vectors
        ↓
   Rank → Visualize → Explain
```

1. **Select a Target** — Choose from Shackleton crater rim (Moon), South pole plateau (Moon), Jezero crater (Mars), or Gale crater (Mars).
2. **Explore the Dashboard** — See ranked Earth sites on an interactive map, colored by match quality.
3. **Dive into Details** — View per-criterion breakdowns with radar charts, confidence indicators, and AI-generated insights explaining *why* a site matches or doesn't.
4. **Compare Sites** — Place 2–3 candidates side-by-side with overlaid radar charts and a full comparison table.

---

## 📊 Six Criteria

| Criterion | Source | Key |
|---|---|---|
| Aridity | NASA POWER | `aridity` |
| Temperature Range | NASA POWER | `temp_range_c` |
| Elevation | DEM (SRTM) | `elevation_m` |
| Slope | Derived from DEM | `slope_deg` |
| Roughness | Derived from DEM | `roughness` |
| Diurnal Thermal Range | MODIS LST | `lst_diurnal_c` |

All weights are adjustable via sliders — the ranking updates live in the browser using the same deterministic formula as the server.

---

## 🏗️ Architecture

```
src/
├── acquire/        # Loads & normalizes raw NASA data → cache/
├── compute/        # Deterministic scoring (similarity + confidence) — no LLM, ever
├── ai/             # Two LLM calls only: site insight + compare verdict (prose only)
├── api/            # FastAPI backend, reads cache/demo_fixtures
└── tests/          # Golden fixtures shared by Python & TypeScript

web/                # React + Vite frontend, 6 pages
```

**Key boundary:** `src/compute/` is purely deterministic — same inputs always produce the same output. `src/ai/` takes already-computed numbers and returns prose only. Every number on screen is traceable to real data through code, never asserted by an LLM.

---

## 🗂️ Data Pipeline

| Layer | Path | Git Status |
|---|---|---|
| Raw downloads (as exported from portals) | `data/raw/` | Gitignored |
| Normalized/resampled layers | `cache/` | Gitignored |
| Demo-ready fixtures (exact bytes for the demo) | `demo_fixtures/` | **Committed** |
| Planetary target vectors with source URLs | `data/targets.json` | **Committed** |

Data acquisition is manual-download-based, not live-fetch. See [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md) for the complete citation list.

---

## 🌐 Pages

| # | Route | Page |
|---|---|---|
| 1 | `/` | Landing |
| 2 | `/select-target` | Select Target |
| 3 | `/dashboard` | Dashboard (map + ranked list) |
| 4 | `/site/:id` | Site Detail (radar chart + insight) |
| 5 | `/compare` | Compare (side-by-side) |
| 6 | `/about` | About (citations + methodology) |

---

## 📚 Documentation

| File | Purpose |
|---|---|
| [`plan.md`](plan.md) | Master build plan — re-read at each session |
| [`FEATURES.md`](FEATURES.md) | Page-by-page specification and canonical targets |
| [`DESIGN.md`](DESIGN.md) | Design tokens, typography, and visual treatment |
| [`AGENTS.md`](AGENTS.md) | AI boundary — what the model may and may never compute |
| [`CLAUDE.md`](CLAUDE.md) | Coding standards and conventions |
| [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md) | Full citation list of datasets |
| [`docs/AI_USE.md`](docs/AI_USE.md) | Mandatory AI disclosure log |

---

## 🤖 AI Disclosure

Similarity scoring and confidence scoring are **deterministic code**, not AI. The only two LLM calls in the entire project are:

1. **Site-detail insight** — narrates why a site matches or doesn't
2. **Compare verdict** — recommends which site is best for a use case

Both take already-computed numbers as input, return prose only, and degrade gracefully if unavailable. Full disclosure is maintained in [`docs/AI_USE.md`](docs/AI_USE.md).

---

## 👥 Team

Built for the NASA Space Apps Challenge 2026.

---

*"The model may narrate. The model may never compute."*
