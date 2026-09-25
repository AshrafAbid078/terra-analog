# CLAUDE.md — Terra Analog

Coding standards for this repo. `AGENTS.md` says what you're allowed to compute; this file says how to write it once you're in bounds. Read both before starting. Named `CLAUDE.md` per convention, but applies to Antigravity (the primary coding tool for this project) just the same, and to any code written by hand.

## Python (`src/acquire`, `src/compute`, `src/ai`, `src/api`)

- Type hints on every function signature — this is a data pipeline, and a wrong shape three functions downstream is much harder to debug than a wrong type caught at the call site.
- Docstrings on every public function: one line of purpose, then what it returns, in the style already used in `similarity.py`.
- `src/compute/` functions must be pure: no I/O, no randomness, no network calls, no hidden global state. Same input, same output, every time — this isn't a style preference here, it's the thing the whole project's Validity claim rests on.
- Prefer `numpy`/vectorized operations over Python loops for anything touching the predictor grid — the grid is ~360×720 cells, loop-per-cell code will be visibly slow in a live demo.
- Formatting: `black` + `ruff`, default settings. Run before committing, don't hand-format.
- Error handling in `src/acquire/`: if a raw file is missing or malformed, raise a clear error naming the expected path — don't silently skip a source or fabricate a fallback value. Silent gaps here become silent gaps in `data_confidence` later, which defeats the point of that metric.

## TypeScript / React (`web/`)

- Functional components with hooks only — no class components.
- One component per file, filename matches the component name, matching the layout already fixed in `structure.md`.
- Colors always via the CSS variables defined in `DESIGN.md` (`--bg-page`, `--accent-primary`, `--score-high`, etc.) — never a raw hex in a component file. See `.agent/skills/frontend-tokens/SKILL.md` for the full list and per-page rules.
- The client-side mirror of `similarity()` (for live slider re-rank) lives in one shared file (e.g. `web/src/lib/similarity.ts`), not copy-pasted into whichever component needs it — one file to keep in sync with the Python original, not several.
- Data fetching goes through `web/src/lib/api.ts` — components don't call `fetch` directly.

## Testing

- `src/compute/similarity.py` and `src/compute/confidence.py` need a small golden-test file (a handful of hand-checked site/target pairs with expected output) — this is the regression check that catches drift if the formula changes mid-build, and it's also what the JS mirror in `web/src/lib/similarity.ts` should be tested against, so both implementations are checked against the same fixture rather than against each other.
- Don't write tests for `src/ai/insight.py` or `compare_verdict.py` that assert on exact LLM output text — assert on the shape of the response and the graceful-failure path instead (page still renders if the call fails).

## Commits

- Small, one logical change per commit. A commit that touches both `src/compute` and `web/` at once is usually a sign the change should have been two commits.
- Commit messages: imperative mood, what changed and why in one line — `"add slope/roughness derivation from DEM"`, not `"updates"`.

## Comments

- Comment *why*, not *what* — the code already says what it does. A comment earns its place by explaining a non-obvious choice (e.g. why a particular normalization range was picked) or citing a source (e.g. the formula's origin), not by restating the line above it.
- No commented-out code left in commits — delete it, git history has it if it's needed again.

## When in doubt

If a task in `plan.md`, `FEATURES.md`, or a skill file conflicts with something in this file, the task-specific document wins for *what* to build; this file still governs *how* to write it.
