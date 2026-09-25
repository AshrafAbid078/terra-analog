---
name: frontend tokens
description: Design tokens and per-page visual rules for the frontend.
---

# Skill: frontend tokens

Applies to any work inside `web/`. Trigger on: building or editing a page/component, styling, adding a chart or map, touching `web/src/styles/tokens.css`.

## Always pull colors from tokens, never invent new ones

Reference `DESIGN.md` and `web/src/styles/tokens.css` for every color decision. Do not introduce a new hex value for a "just this once" case — extend the token file instead if something is genuinely missing.

- `--bg-void` / `--bg-surface` / `--bg-surface-2` — the only three background layers
- `--accent-teal` — primary CTA, active nav, links (Earth)
- `--accent-blue` — Moon target badges only
- `--accent-coral` — Mars target badges only
- `--score-high` / `--score-medium` / `--score-low` — match score only, always this 3-step scale, never a gradient between them
- `--confidence-full` / `--confidence-limited` / `--confidence-missing` — data confidence only

**Never reuse `--accent-blue` or `--accent-coral` for score or confidence meaning.** Those two colors mean "this is Moon" / "this is Mars" — nothing else. Mixing them into the score scale makes a judge misread a Moon-tagged badge as a match-quality signal.

## Typography

- UI, nav, headings: Inter or Sora (sans-serif)
- Data readouts — match %, coordinates, the data table, the score-breakdown card: JetBrains Mono or IBM Plex Mono
- AI insight prose paragraphs: sans-serif, not monospace — readability matters more than console aesthetic there

## Page-to-component map

Match each page to the shared components in `structure.md` rather than building one-off variants:

- `SiteDetail.tsx` and `Compare.tsx` both use `MatchScoreCard.tsx` and `ConfidenceIndicator.tsx` — same components, not parallel implementations, since both read the identical 6-criteria + confidence array from `src/compute`.
- `SelectTarget.tsx` uses `TargetToggleCard.tsx` for exactly the 4 canonical targets (Shackleton crater rim, South pole plateau site, Jezero crater, Gale crater) — no free-text target entry, no additional targets.
- Dashboard's ranked list and map both color by the same `--score-high/medium/low` scale — if one changes, the other must too.

## Building UI

When generating a new component, check `DESIGN.md` and `structure.md` first rather than starting from a blank layout — the page structure and component names are already decided, this skill exists to keep new code matching what's already speced rather than drifting into a different visual language mid-build.
