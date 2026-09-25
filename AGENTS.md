# AGENTS.md — Terra Analog

Read this before touching any file. It defines what you're allowed to do, not how to write it — for coding style and conventions, see `CLAUDE.md`. For the full build plan, see `plan.md`.

## The one rule that overrides everything else

**The model may narrate. The model may never compute.**

Concretely:

- You may write prose that explains, summarizes, or compares numbers that already exist.
- You may never produce a similarity score, a terrain tag, or a data confidence value yourself — not as a fallback, not as a placeholder, not "just this once to unblock the build." These are computed by deterministic code in `src/compute/`, full stop.
- If a task seems to require you to estimate, guess, or "use your judgment" for a similarity score, a match percentage, a confidence percentage, or a terrain category — stop and flag it instead of producing a number. The fix is almost always "write the missing function in `src/compute`," not "approximate it here."

This rule exists because the project's Validity score at judging depends on every number being traceable to real data through deterministic code — not asserted by an LLM. Breaking this boundary once, even in a throwaway test file, undermines the whole premise of the build.

## Where the boundary actually lives in the repo

| Folder | May call an LLM? | What goes here |
|---|---|---|
| `src/compute/` | **Never** | `similarity.py`, `confidence.py`, `terrain_tag.py` — pure functions, same input always gives same output |
| `src/ai/` | **Only these two files** | `insight.py` (site-detail "why it matches / why it doesn't"), `compare_verdict.py` (compare-page recommendation) — both take already-computed numbers as input, return prose only |
| `src/acquire/` | Never | Loads and normalizes manually-downloaded raw data from `data/raw/` — no computation of scores, no LLM |
| `src/api/`, `web/` | Never directly | Reads/displays what `src/compute` and `src/ai` already produced |

If you're writing a file in `src/compute/` and find yourself wanting to call an LLM for "just a quick judgment call" — that's the signal you're in the wrong folder. If you're writing `src/ai/insight.py` and find yourself computing a new number instead of using one that was passed in — same signal, wrong direction.

## Data acquisition is manual right now

NASA data (POWER, DEM, MODIS LST, target vectors) is being downloaded by hand into `data/raw/<source>/`, not fetched live by a script. `src/acquire/` loads and normalizes what's already on disk — never calls a NASA API at build or runtime. Every value that reaches `data/targets.json` or a cached predictor layer needs a traceable source (portal URL + access date) — don't invent or guess a plausible-looking one.

## Targets and criteria are locked — don't add or rename

Four targets only: Shackleton crater rim, South pole plateau site (Moon), Jezero crater, Gale crater (Mars). Six criteria only, these exact keys: `aridity`, `temp_range_c`, `elevation_m`, `slope_deg`, `roughness`, `lst_diurnal_c`. Don't add "mineral similarity," "radiation exposure," or additional targets/regions on your own initiative — they were deliberately cut because no acquisition pipeline exists for them. If a task seems to call for a 7th criterion or a 5th target, flag it rather than inventing the data behind it.

## Skills

Task-scoped detail lives in `.agent/skills/`:
- `nasa-acquisition/SKILL.md` — loading and normalizing `data/raw/`
- `compute-boundary/SKILL.md` — the formulas themselves (similarity, confidence)
- `frontend-tokens/SKILL.md` — design tokens, per-page visual treatment

Read the relevant one before starting work in its area — this file is the boundary, those are the how.
