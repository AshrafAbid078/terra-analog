# Terra Analog — 240-Second Prescreening Video Guide

## Purpose

A complete 4-minute concept video plan for the **1 October 2026 NASA Space Apps prescreening**.

According to the provided build guide, the 1 October video must include:

- Team name
- Every team member by name
- The problem and challenge statement
- The proposed solution approach as a concept

The full challenge statements are scheduled for **28 October 2026**, so this video should present the concept rather than pretend the final implementation is already complete.

---

# 1. Project Facts Used in This Script

- **Project:** Terra Analog — Earth-Moon-Mars Analog Site Finder
- **Challenge:** “Earth Locations that Analog Moon and Mars Bases”
- **Canonical targets:** 4 total
  - Shackleton crater rim — Moon
  - South pole plateau site — Moon
  - Jezero crater — Mars
  - Gale crater — Mars
- **Canonical criteria:** 6
  - Aridity
  - Temperature range
  - Elevation
  - Slope
  - Roughness
  - Thermal behaviour
- **Planned data sources:**
  - NASA POWER
  - DEM
  - MODIS LST
  - Moon Trek / Mars Trek / PDS
- **Core concept:** Compare Earth locations with a selected lunar or Martian target using deterministic similarity analysis.
- **AI boundary:** AI explains/narrates already-computed results; it does not calculate similarity or confidence.

---

# 2. 240-Second Timeline

| Time | Section | What to Show |
|---|---|---|
| 00:00–00:12 | Hook | Earth → Moon → Mars + Terra Analog title |
| 00:12–00:32 | Team | Team name + all 5 members |
| 00:32–01:05 | Problem | Why analog-site discovery is difficult |
| 01:05–01:35 | Solution | Terra Analog concept |
| 01:35–02:00 | How It Works | Target → profile → candidates → similarity → sites |
| 02:00–02:25 | Six Criteria | The six environmental criteria |
| 02:25–02:48 | NASA Data | Planned NASA/partner data pipeline |
| 02:48–03:20 | User Experience | Target selection → map → details → comparison |
| 03:20–03:40 | AI Role | Deterministic computation → AI explanation |
| 03:40–03:52 | Impact | Research, testing, education, exploration |
| 03:52–04:00 | Closing | Logo + tagline + team name |

---

# 3. Full Narration + Visual Directions

## 00:00–00:12 — HOOK

### Narration

> “What if we could find places on Earth that closely resemble environments on the Moon and Mars?
>
> This is Terra Analog.”

### Visual

- **0:00–0:04:** Earth from space
- **0:04–0:08:** Earth → Moon → Mars transition
- **0:08–0:12:** Terra Analog logo/title

### On-screen text

```text
TERRA ANALOG
Finding Earth. Preparing for Other Worlds.
```

---

## 00:12–00:32 — TEAM INTRODUCTION

### Narration

> “We are [TEAM NAME], a five-member team working on Terra Analog.
>
> Our team members are [MEMBER 1], [MEMBER 2], [MEMBER 3], [MEMBER 4], and [MEMBER 5].
>
> Together, we are exploring a data-driven way to identify Earth locations that can serve as analog environments for lunar and Martian exploration.”

### Visual

Show:

```text
[TEAM NAME]

[MEMBER 1]
[MEMBER 2]
[MEMBER 3]
[MEMBER 4]
[MEMBER 5]
```

Use team photos/headshots if available.

**Important:** One person is the only narrator. The five members do not need separate speaking parts.

---

# 00:32–01:05 — PROBLEM

### Narration

> “Future lunar and Martian exploration requires environments where technologies, instruments, operations, and human activities can be tested under challenging conditions.
>
> Earth already contains locations with environmental characteristics that can resemble aspects of extraterrestrial environments.
>
> However, finding suitable analog sites is difficult when relevant information is distributed across different datasets and environmental characteristics.
>
> Researchers and mission planners need a more systematic way to compare these conditions.”

### Visual

Start with:

```text
Earth
Moon
Mars
```

Then show separate data cards:

```text
Temperature
Elevation
Slope
Roughness
Aridity
Thermal Behaviour
```

Then:

```text
Multiple datasets
        ↓
Difficult comparison
        ↓
Difficult analog-site discovery
```

---

# 01:05–01:35 — SOLUTION

### Narration

> “Terra Analog addresses this challenge with an interactive platform for discovering and comparing potential Earth analog sites.
>
> A user selects a lunar or Martian target.
>
> Terra Analog then represents that target through measurable environmental characteristics and compares them with candidate locations on Earth.
>
> The goal is to make analog-site discovery more structured, transparent, and accessible.”

### Visual

Show a polished concept UI.

Show:

```text
SELECT
   ↓
ANALYZE
   ↓
COMPARE
   ↓
DISCOVER
```

Then show Moon/Mars target selection.

---

# 01:35–02:00 — HOW IT WORKS

### Narration

> “The workflow is simple.
>
> First, the user selects a target site on the Moon or Mars.
>
> Next, its environmental profile is compared with Earth data.
>
> The system evaluates candidate Earth locations using a deterministic similarity process.
>
> Finally, the most comparable locations can be explored through the interface.”

### Visual

```text
Lunar / Martian Target
          ↓
Environmental Profile
          ↓
Earth Candidate Locations
          ↓
Similarity Analysis
          ↓
Ranked Candidate Sites
```

Use animated arrows.

---

# 02:00–02:25 — SIX CRITERIA

### Narration

> “Our comparison is based on six environmental characteristics:
>
> aridity, temperature range, elevation, slope, surface roughness, and thermal behaviour.
>
> Together, these characteristics form the basis for comparing a planetary target with potential Earth analog locations.”

### Visual

Show six cards:

```text
ARIDITY

TEMPERATURE RANGE

ELEVATION

SLOPE

ROUGHNESS

THERMAL BEHAVIOUR
```

### Important

Do **not** add old criteria such as:

- Mineral similarity
- Radiation exposure

The current project specification locks the comparison to six criteria.

---

# 02:25–02:48 — NASA DATA

### Narration

> “The platform is designed around NASA and partner datasets.
>
> The planned data pipeline uses NASA POWER for climate characteristics, elevation data for terrain-derived features, MODIS land surface temperature for thermal behaviour, and planetary sources such as Moon Trek, Mars Trek, and PDS for target-side information.
>
> These inputs are normalized into a consistent structure before comparison.”

### Visual

Show:

```text
NASA POWER
DEM
MODIS LST
Moon Trek
Mars Trek
PDS
```

Then:

```text
RAW DATA
    ↓
NORMALIZATION
    ↓
ENVIRONMENTAL FEATURES
    ↓
SIMILARITY
```

Do not display made-up measurements or scientific results.

---

# 02:48–03:20 — USER EXPERIENCE

### Narration

> “From the user's perspective, Terra Analog brings this analysis into one interface.
>
> Users can select a target, explore candidate Earth locations on a map, inspect similarity and confidence information, view criterion-by-criterion comparisons, and compare selected sites.
>
> The interface is designed to make the reasoning behind a match visible rather than hiding everything behind a single number.”

### Visual Sequence

### Screen 1 — Landing

```text
TERRA ANALOG
Explore Analog Sites
```

### Screen 2 — Target Selection

```text
SELECT YOUR TARGET

Moon
Mars

Shackleton crater rim
South pole plateau site
Jezero crater
Gale crater
```

### Screen 3 — Dashboard

```text
Earth Map
+
Candidate Site List
+
Similarity Information
```

### Screen 4 — Site Detail

```text
Site
Similarity
Confidence

Aridity
Temperature
Elevation
Slope
Roughness
Thermal Behaviour
```

### Screen 5 — Compare

```text
Site A | Site B | Site C

6 Criteria
Overall Score
Confidence
```

If these screens are not implemented yet, present them as **concept/mockup visuals**.

Do not present invented scores as real results.

---

# 03:20–03:40 — AI ROLE

### Narration

> “AI has a specific role in Terra Analog.
>
> The scientific similarity and confidence calculations are handled by deterministic computation, not by an AI model.
>
> Once the results are calculated, the AI layer can help explain those results in clear language and generate useful insights from the computed evidence.”

### Visual

```text
DATA
  ↓
DETERMINISTIC COMPUTATION
  ↓
SIMILARITY + CONFIDENCE
  ↓
AI EXPLANATION
```

Labels:

```text
Scientific calculation
     Deterministic
```

and:

```text
AI
Narration / Explanation
```

---

# 03:40–03:52 — IMPACT

### Narration

> “By connecting planetary environments with real locations on Earth, Terra Analog aims to support analog-site discovery for research, field testing, education, and future exploration planning.
>
> It connects Earth data with the environments of other worlds.”

### Visual

```text
Earth Analog Sites
        ↓
Research
        ↓
Field Testing
        ↓
Education
        ↓
Future Exploration
```

---

# 03:52–04:00 — CLOSING

### Narration

> “This is Terra Analog.
>
> Finding Earth. Preparing for Other Worlds.
>
> Thank you.”

### Visual

```text
TERRA ANALOG

Finding Earth.
Preparing for Other Worlds.

[TEAM NAME]
```

Keep the final frame clean.

---

# 4. Required Visual Assets

Prepare these before editing:

- [ ] Terra Analog logo/title card
- [ ] Team name card
- [ ] Five-member team card
- [ ] Earth → Moon → Mars opening visual
- [ ] Problem/data-fragment visual
- [ ] Solution architecture animation
- [ ] Six-criteria cards
- [ ] NASA/partner data-source visual
- [ ] Target-selection concept screen
- [ ] Dashboard/map concept screen
- [ ] Site-detail concept screen
- [ ] Comparison concept screen
- [ ] AI boundary diagram
- [ ] Final logo/tagline card

---

# 5. Editing Rules

1. One person narrates the entire video.
2. Keep the narration continuous and natural.
3. Use subtitles throughout if possible.
4. Do not claim that the final software is already implemented.
5. Do not invent scientific scores, measurements, candidate-site results, or NASA findings.
6. Keep terminology consistent with the current project specification.
7. Use exactly the current 4 targets and 6 criteria.
8. If a UI screen is only a concept, label it as a concept/mockup or avoid implying that it is already functional.
9. Do not add mineral similarity or radiation exposure as criteria.
10. Target approximately **235–238 seconds** during editing so the final export stays safely under 240 seconds.
11. Use the current Terra Analog files as the source of truth and ignore older project drafts.

---

# 6. Final Recording Structure

```text
00:00  Hook
00:12  Team
00:32  Problem
01:05  Solution
01:35  How It Works
02:00  Six Criteria
02:25  NASA Data
02:48  User Experience
03:20  AI Role
03:40  Impact
03:52  Closing
04:00  END
```

---

# 7. Information Still Needed Before Final Recording

Only these project-specific details still need to be filled:

- Final team name
- Five member names
- Final tagline, if different from the working tagline
- Available team photos/headshots
- Any existing footage or visual assets
- Whether the four target names should all appear on screen

The rest of the script is based on the current Terra Analog project documentation.
