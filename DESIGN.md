# DESIGN.md — Terra Analog

Two themes, one token set. Light is the default (warm, editorial SaaS look); dark keeps the original mission-console look from the first draft. Every component reads only the token names below — never a raw hex — so the toggle is a one-line attribute flip, not a rebuild.

## Theme switch mechanism

```css
:root { /* light values, default */ }
[data-theme="dark"] { /* dark overrides */ }
```

```js
// toggle
document.documentElement.setAttribute('data-theme', next); // 'light' | 'dark'
localStorage.setItem('theme', next); // remember choice
```

Default: respect `prefers-color-scheme` on first visit, then remember whatever the person picks via the navbar toggle. Both themes must always be readable — never ship a component styled for only one.

## Tokens — light (default)

| Token | Hex | Use |
|---|---|---|
| `--bg-page` | `#FAF7F2` | Page background — warm off-white, not stark white |
| `--bg-surface` | `#FFFFFF` | Cards, panels |
| `--bg-surface-2` | `#F5EDE1` | Raised elements, hover, stat strips |
| `--border` | `#E0DACD` | Card borders, dividers, table rules |
| `--text-primary` | `#1A1A18` | Headings, primary values |
| `--text-secondary` | `#6B6B63` | Labels, captions, body copy |
| `--text-muted` | `#A39C8C` | Placeholder, disabled |

## Tokens — dark

| Token | Hex | Use |
|---|---|---|
| `--bg-page` | `#0B0F1A` | Page background |
| `--bg-surface` | `#121826` | Cards, panels |
| `--bg-surface-2` | `#1B2436` | Raised elements, hover |
| `--border` | `#2A3346` | Card borders, dividers |
| `--text-primary` | `#F5F7FA` | Headings, primary values |
| `--text-secondary` | `#9AA5B8` | Labels, captions |
| `--text-muted` | `#5C6B85` | Placeholder, disabled |

## Accent triad — Earth / Moon / Mars

| Token | Light | Dark | Use |
|---|---|---|---|
| `--accent-primary` | `#C1440E` (terracotta) | `#2DD4BF` (teal) | Primary CTA, active nav, links |
| `--accent-moon` | `#3E6B99` | `#5B8DEF` | Moon target badges only |
| `--accent-mars` | `#9C3B12` | `#E8674F` | Mars target badges only — kept a shade off `--accent-primary` in light mode so "brand color" and "this is Mars" don't read as the same signal |

## Semantic — match score (same 3-step meaning, both themes)

| Token | Light | Dark |
|---|---|---|
| `--score-high` | `#3F7D52` | `#4ADE80` |
| `--score-medium` | `#C98A1D` | `#FBBF24` |
| `--score-low` | `#B23A2E` | `#F87171` |

## Semantic — data confidence

| Token | Light | Dark | Coverage weight |
|---|---|---|---|
| `--confidence-full` | `#1A6B5C` | `#2DD4BF` | 1.0 (✓) |
| `--confidence-limited` | `#C98A1D` | `#FBBF24` | 0.5 (⚠) |
| `--confidence-missing` | `#A39C8C` | `#64748B` | 0.0 (✗) |

## Typography (unchanged across themes)

- **UI / headings / nav**: Inter or Sora, sans-serif
- **Data readouts**: JetBrains Mono or IBM Plex Mono — match %, coordinates, data table, score breakdown
- **AI insight prose**: sans-serif, not monospace

## Component notes

- Radar chart, score bars, and confidence checklist all read `--score-*` / `--confidence-*` — never a hardcoded hex, so they flip themes automatically.
- No drop shadows in either theme — depth comes from `--border` + the surface/surface-2 step, not shadow.
- `--accent-moon` / `--accent-mars` are reserved for target-body identity only, in both themes — never reused for score or confidence meaning.
- Illustrated landscape strips (hero image area, site-detail terrain graphic) are flat SVG, not photos, and should swap their fill colors to the theme's own palette rather than staying fixed — e.g. the sun/mountain illustration uses `--accent-mars` and `--accent-primary` fills, which already differ correctly between the two themes.

## Overall visual direction

Not a generic dashboard template. Warm, editorial, a real point of view — closer to a well-designed product page than a data-dense admin panel, even though the underlying content is scientific. Generous whitespace, bold headline type on the landing page, restraint everywhere else. If a page feels flat or default, it's wrong — every page should feel like it was designed for this project specifically, not dropped in from a component library with the colors swapped.

## Per-page visual treatment

Not every page gets the same richness — match the treatment to what that page is actually for.

| Page | Background / image | Chart | Table |
|---|---|---|---|
| `/` Landing | Illustrated flat background (starfield + orbit rings, or landscape silhouette + sun) behind the hero — see Illustrated imagery below | — | — |
| `/select-target` | Plain surface, no illustration needed — this page is a quick decision, not a moment to linger on | — | — |
| `/dashboard` | Map is the visual centerpiece (color-coded markers by score) | — | — |
| `/site/:id` | Illustrated landscape strip at the top (site terrain) | **Radar chart**, 6 axes — see spec below | **Earth vs. target** data table, each row linking to its source |
| `/compare` | — | **Overlaid radar chart**, one polygon per site, color-keyed to the site names | **Full comparison table** — criterion rows × site columns, overall score row bolded at the bottom |
| `/about` | — | — | Data source list (dataset name → what it provides), not a comparison table |

## Illustrated imagery (not stock photos)

Real photography needs licensing, hosting, and an offline-safe asset pipeline — none of which fits a 48-hour build cleanly. Use flat, theme-aware SVG illustrations instead, in the same spirit as the landing-page starfield and the site-detail landscape strip already built:

- Flat fills only, from the theme's own token palette — no gradients, no photographic detail
- Landing hero: soft starfield (small dots, `--border` color) plus 1–2 faint orbit rings, optionally two small solid circles suggesting Moon/Mars
- Site detail: a simple layered-silhouette landscape (2–3 flat shapes suggesting terrain) using `--accent-mars` / `--accent-primary` at low opacity, not a literal drawing of the specific site
- If real site photography becomes available later (e.g. public-domain NASA/USGS imagery), it belongs in a committed `web/public/images/` folder — downloaded once, never hotlinked or fetched live — swapped in behind the same layout, not appended alongside the illustration

## Radar chart spec

6 axes, one per criterion, in this fixed order (clockwise from top): aridity, temperature, elevation, slope, roughness, thermal behaviour. Regular hexagon grid at 1/3, 2/3, and full radius for scale reference. Plot polygon color = `--accent-mars` (single-site view) or one color per site keyed to a small legend (compare view). Fill the polygon at low opacity (≈15–18%), stroke at full opacity, 2px. Axis labels in `--text-secondary`, 11px, positioned just outside the outer hexagon vertex on each axis.

## Comparison table spec (`/compare`)

Rows = the 6 criteria in the same fixed order as the radar chart, plus an `Overall` row last, bolded, in `--score-high/medium/low` per its own value. Columns = one per selected site (2–3), each column header colored to match that site's radar-chart legend color. Hairline row dividers (`--border`), no zebra striping, no shadows.
