---
name: compute boundary
description: Definition and instructions for the deterministic AI boundary formulas.
---

# Skill: compute boundary

Applies to any work inside `src/compute/` or `src/ai/`. Trigger on: writing or editing `similarity.py`, `confidence.py`, `terrain_tag.py`, `insight.py`, `compare_verdict.py`, or anything that computes or explains a match score.

## The one rule that matters

**`src/compute/` never calls an LLM. `src/ai/` never computes a score.** These are two separate folders on purpose. If a change would blur that line — e.g. asking a model to "estimate" a similarity score, or letting `insight.py` adjust a number instead of just narrating it — stop and flag it instead of writing it.

## `src/compute/similarity.py`

- Weighted distance function over exactly 6 criteria: aridity, temperature range, elevation, slope, roughness, thermal behaviour.
- Weights are the user-facing sliders — the function takes them as parameters, live re-rank calls this same function again with new weights, never a different code path.
- Same inputs always produce the same output. No randomness, no model call, no "AI-adjusted" fudge factor.

## `src/compute/confidence.py`

Per-criterion coverage weight, computed from actual data availability at that grid cell — not asserted, not estimated by a model:

- `1.0` (full) — native resolution ≥ grid resolution, no gaps in that cell
- `0.5` (limited) — coarser than grid, interpolated, or partial temporal coverage
- `0.0` (missing) — no valid data

```
data_confidence = mean(coverage_weight across the 6 criteria) × 100
```

The per-criterion checklist shown in the UI (✓ / ⚠ / ✗) and the headline percentage must read from this same array — never compute them separately.

## `src/compute/terrain_tag.py` (cut-if-needed)

If built at all: a simple threshold rule on the same 6 computed values (e.g. high aridity + low roughness → "Desert"). Not a hand-labeled lookup table, not a 7th uncited factor.

## `src/ai/insight.py` and `src/ai/compare_verdict.py`

These are the only two files in the project allowed to call an LLM. Both take already-computed numbers as input and return prose only:

- `insight.py`: given one site's 6 scores + raw values, write "why it matches" / "why it doesn't" — must explicitly name at least one meaningful difference, not just similarities.
- `compare_verdict.py`: given 2–3 sites' scores, write a short "best for X use case" line.

Both must degrade gracefully — if the call fails or times out, the page still renders the scores, bars, radar chart, and data table with no prose block, never a blocked or blank page.
