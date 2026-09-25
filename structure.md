# structure.md — Terra Analog repo layout

Follows the shared build-kit architecture (frontend never talks to NASA directly, `src/compute` stays deterministic, offline-first). Trimmed of the parts that don't apply to this challenge — no `src/agents` orchestrator loop, no runtime MCP server config, no `.claude/skills/` folder (Antigravity's own `.agent/skills/` format is used instead). Data acquisition is manual-download-based, not live-fetch — see `plan.md` section 2.

```
terra-analog/
├── AGENTS.md                      # the AI boundary — what the model may/may never compute, read every session
├── CLAUDE.md                      # coding standards — how to write the code, once it's in bounds
├── plan.md                        # master plan — re-read at the start of each build session
├── README.md
├── DESIGN.md                      # dual light/dark tokens, typography, per-page visual treatment, chart specs
├── FEATURES.md                    # page-by-page spec, canonical targets + criteria
│
├── .agent/
│   └── skills/                    # Antigravity's task-triggered skill format
│       ├── nasa-acquisition/SKILL.md      # loading + normalizing data/raw/, citation rules
│       ├── compute-boundary/SKILL.md      # similarity.py / confidence.py formulas, the AI boundary in practice
│       └── frontend-tokens/SKILL.md       # DESIGN.md tokens, per-page visual rules
│
├── docs/
│   ├── AI_USE.md                  # mandatory disclosure log — updated continuously, not at the end
│   └── DATA_SOURCES.md            # full citation list (dataset, product, URL, accessed date), feeds /about page
│
├── data/
│   ├── raw/                       # gitignored — manual downloads, untouched, as exported from each portal
│   │   ├── power/                 # + a .source.txt per file: portal URL + access date
│   │   ├── dem/
│   │   ├── modis_lst/
│   │   └── targets/                # Moon Trek / Mars Trek / PDS exports for the 4 target sites
│   └── targets.json                # 4 target vectors (Shackleton rim, South pole plateau,
│                                    # Jezero, Gale), each value with a source_url
│
├── cache/                         # gitignored — normalized/resampled layers, output of src/acquire
│   ├── power/
│   ├── dem/
│   └── modis_lst/
│
├── demo_fixtures/                 # COMMITTED — exact bytes the demo depends on
│   ├── predictor_stack.zarr/      # trimmed copy of the global grid, enough for the demo
│   ├── site_scores.json           # precomputed scores for the 5–8 demo candidate sites
│   └── insights_cache.json        # pre-generated LLM insight text, used if the live call fails
│
├── src/
│   ├── acquire/                   # LOADS data/raw/ and normalizes it — no live API calls, ever
│   │   ├── load_power.py
│   │   ├── load_dem.py
│   │   ├── load_modis_lst.py
│   │   └── safe.py                # try cache → fall back to fixture, never raises mid-demo
│   │
│   ├── compute/                   # deterministic only — no LLM calls anywhere in this folder
│   │   ├── similarity.py          # weighted distance over the 6 criteria (CRITERIA list, locked)
│   │   ├── confidence.py          # coverage-weight formula from plan.md / FEATURES.md
│   │   └── terrain_tag.py         # optional, cut-if-needed — rule-based terrain label
│   │
│   ├── ai/                        # the only two places an LLM is called
│   │   ├── insight.py             # site-detail "why it matches / why it doesn't"
│   │   └── compare_verdict.py     # /compare page "best for X use case"
│   │
│   ├── api/
│   │   ├── main.py                # FastAPI app
│   │   └── routes/
│   │       ├── sites.py           # GET ranked sites for a target
│   │       ├── site_detail.py     # GET one site's full breakdown
│   │       └── compare.py         # POST 2–3 site ids → verdict
│   │
│   └── tests/
│       ├── golden_similarity.json # hand-checked site/target pairs — Python AND JS mirror both test against this
│       ├── test_similarity.py
│       └── test_confidence.py
│
└── web/
    ├── src/
    │   ├── pages/
    │   │   ├── Landing.tsx        # Page 1  /
    │   │   ├── SelectTarget.tsx   # Page 2  /select-target
    │   │   ├── Dashboard.tsx      # Page 3  /dashboard
    │   │   ├── SiteDetail.tsx     # Page 4  /site/:id
    │   │   ├── Compare.tsx        # Page 5  /compare
    │   │   └── About.tsx          # Page 6  /about
    │   ├── components/
    │   │   ├── Navbar.tsx          # includes the light/dark theme toggle
    │   │   ├── MatchScoreCard.tsx  # breakdown bars + radar chart, shared by Page 4 & 5
    │   │   ├── ConfidenceIndicator.tsx
    │   │   ├── TargetToggleCard.tsx
    │   │   ├── SiteListCard.tsx
    │   │   └── WorldMap.tsx
    │   ├── styles/
    │   │   └── tokens.css         # light (default) + [data-theme="dark"] overrides, from DESIGN.md
    │   └── lib/
    │       ├── api.ts             # thin fetch wrapper to src/api
    │       └── similarity.ts      # JS mirror of similarity.py, for client-side live re-rank —
    │                               # tested against src/tests/golden_similarity.json, same as the Python version
    └── public/
        └── images/                # committed, real imagery only if/when curated — never hotlinked
```

## Notes

- `src/compute` and `src/ai` are kept as separate top-level folders on purpose — it should be visually obvious which files may never call an LLM (`compute`) and which two are allowed to (`ai`), matching the boundary in `AGENTS.md`.
- `data/raw/` is gitignored and untouched as downloaded; `src/acquire/` loads and normalizes it into `cache/` (also gitignored); `demo_fixtures/` is the only data folder committed to git — the exact bytes the demo needs, so it never depends on `data/raw/` or `cache/` being present.
- No `src/agents/` folder and no runtime MCP server config — this challenge has no live agent tool-calling loop; both LLM calls in `src/ai/` are plain one-shot API calls with the computed numbers already in the prompt. (A dev-time MCP server for granule search is registered globally in Antigravity's own config, not in this repo — see `plan.md` section 7.)
- `src/tests/golden_similarity.json` is shared on purpose — one fixture, checked by both the Python `similarity.py` and the TypeScript `similarity.ts`, so the server-computed initial rank and the client-side slider re-rank can never silently drift apart.
