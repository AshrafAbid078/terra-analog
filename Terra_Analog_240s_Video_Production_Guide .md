# Terra Analog — 240-Second Prescreening Video Production Guide

## 1. Purpose

This guide defines the recommended workflow for producing the **NASA Space Apps 2026 240-second prescreening video** for **Terra Analog — Earth-Moon-Mars Analog Site Finder**.

The goal is to create a video that feels like a real NASA Space Apps project pitch—not a generic AI-generated slideshow.

The recommended production pipeline is:

> **NotebookLM → Story/Visual Draft → Canva/Figma Graphics → Product/UI Recording → Voiceover → CapCut/Premiere → Final Video**

---

## 2. Prescreening Requirements

According to the provided Space Apps 2026 guide, the 1 October prescreening video is:

- **Maximum duration:** 240 seconds
- **Deadline:** 1 October, 11:59 PM
- Must introduce:
  - Team name
  - Every team member by name
  - Problem / challenge statement
  - Solution approach as a concept
- The video is concept-focused because the full challenge statements and datasets are expected to publish later.
- The same core pitch can later be adapted for the local judging video with a working demo.

### Important

Do not present unfinished functionality as already implemented.

If a UI, map, score, or feature is still a concept/mockup, label or present it clearly as a concept.

---

# 3. Recommended Tool Strategy

## A. NotebookLM — Story and Visual Draft

Use NotebookLM as a **planning and visualization tool**, not as the final video editor.

### Give NotebookLM:

- `Terra_Analog_240s_Prescreening_Video_Guide.md`
- `FEATURES.md`
- `plan.md`
- `DESIGN.md`
- Relevant NASA challenge/source material

### Use NotebookLM for:

- Understanding the project story
- Creating a visual overview
- Exploring how the problem and solution connect
- Generating an initial video concept
- Identifying important sections that should appear visually

### Do NOT rely on NotebookLM for:

- Final scientific claims
- Final project numbers
- Final NASA dataset descriptions
- Final UI representation
- Final narration without review

The project documents remain the source of truth.

---

## B. Gemini Pro — Custom Visual Generation

Use Gemini Pro for **custom cinematic and conceptual visuals** that support the story.

### Recommended Gemini visuals

- Earth → Moon → Mars opening
- Lunar and Martian exploration environments
- Earth analog environments
- Research / field-testing concepts
- Planetary environment comparison concepts
- Conceptual NASA-data / planetary-data backgrounds
- Final Earth → other worlds impact scene

### Do NOT use Gemini to generate

- Fake scientific measurements
- Fake similarity scores
- Fake confidence values
- Fake NASA dataset results
- Fake maps presented as real analysis
- Fake Terra Analog UI presented as the actual application

If Gemini generates a conceptual scientific visual, treat it as **illustration**, not evidence.

### Recommended visual style

Keep Gemini-generated visuals consistent:

> Scientific + cinematic + realistic + futuristic, but not overly sci-fi.

Avoid excessive fantasy effects or visuals that make the project look like a fictional space movie.

### Prompt principle

Keep prompts focused on:

- Environment
- Composition
- Lighting
- Scientific/documentary tone
- Aspect ratio
- Absence of unwanted text/logos

Use actual project UI, diagrams, and verified data for anything that represents a real Terra Analog computation.

---

# 4. Canva / Figma — Professional Visual Assets

Create the main visual assets separately so the final video has a consistent visual identity.

Prepare:

### Opening

- Terra Analog logo/title
- Earth → Moon → Mars visual transition
- Tagline if finalized

### Team

- Team name
- Five member names
- Optional headshots/team photo

### Problem

Use simple visual cards showing:

- Earth analog environments
- Moon/Mars exploration
- Distributed environmental information
- Need for systematic comparison

### Solution

Create a simple flow:

```text
Select Planetary Target
        ↓
Build Environmental Profile
        ↓
Compare With Earth Locations
        ↓
Calculate Similarity
        ↓
Explore Candidate Sites
```

### Six Criteria

Show exactly:

1. Aridity
2. Temperature Range
3. Elevation
4. Slope
5. Surface Roughness
6. Thermal Behaviour

Do not add old/cut criteria such as mineral similarity or radiation exposure.

### NASA Data

Show the planned data sources:

- NASA POWER
- Elevation / DEM data
- MODIS Land Surface Temperature
- Moon Trek
- Mars Trek
- Planetary Data System (PDS)

---

# 5. Product / UI Recording

When the application is available, record short clips of:

1. Landing page
2. Target selection
3. Dashboard
4. Earth candidate map
5. Site detail
6. Criterion-by-criterion comparison
7. Compare page
8. AI insight section

The interface should demonstrate that the reasoning behind a match is visible rather than hiding everything behind one number.

---

# 6. Voiceover Strategy

## Preferred Option — Human Voice

Use one team member as the narrator for the entire 240-second video.

Advantages:

- More authentic
- Stronger team identity
- More natural presentation
- Less generic than AI-generated narration

Record in a quiet room with:

- Phone/laptop microphone or external microphone
- Minimal background noise
- Consistent microphone distance
- Slow and confident delivery

Record several takes and choose the cleanest one.

## Alternative — AI Voice

If the narrator's recording quality is poor, an AI voice can be used.

However:

- Keep the voice natural
- Avoid overly dramatic delivery
- Do not use a robotic-sounding voice
- Review every pronunciation
- Keep the narration synchronized with visuals

### Important

The voiceover should follow the approved script. Do not let an AI voice introduce unsupported claims.

---

# 7. Final Editing — CapCut / Premiere

Use the editor to combine:

```text
Narration
   +
Visuals
   +
UI recordings
   +
NASA data labels
   +
Subtitles
   +
Transitions
```

Recommended editing principles:

- Keep cuts fast enough to maintain attention.
- Avoid excessive transitions.
- Use readable text.
- Keep subtitles synchronized.
- Use the project's DESIGN tokens for visual consistency.
- Do not introduce random colors that conflict with the project's design system.
- Keep important information on screen long enough to read.

---

# 8. Recommended 240-Second Storyboard

## 00:00–00:12 — Hook

### Voice

> “What if we could find places on Earth that closely resemble environments on the Moon and Mars?
> This is Terra Analog.”

### Visual

Earth → Moon → Mars.

Show Terra Analog title.

---

## 00:12–00:32 — Team

### Voice

> “We are [TEAM NAME], a five-member team working on Terra Analog.
> Our team members are [MEMBER 1], [MEMBER 2], [MEMBER 3], [MEMBER 4], and [MEMBER 5].”

### Visual

Team name + five member names.

Optional team photo/headshots.

---

## 00:32–01:05 — Problem

### Voice

> “Future lunar and Martian exploration requires environments where technologies, instruments, operations, and human activities can be tested under challenging conditions.
>
> Earth already contains locations with environmental characteristics that can resemble aspects of extraterrestrial environments.
>
> However, finding suitable analog sites is difficult when relevant information is distributed across different datasets and environmental characteristics.
>
> Researchers and mission planners need a more systematic way to compare these conditions.”

### Visual

Earth analog environments → fragmented datasets → researcher → comparison problem.

---

## 01:05–01:35 — Solution

### Voice

> “Terra Analog addresses this challenge with an interactive platform for discovering and comparing potential Earth analog sites.
>
> A user selects a lunar or Martian target.
>
> Terra Analog then represents that target through measurable environmental characteristics and compares them with candidate locations on Earth.
>
> The goal is to make analog-site discovery more structured, transparent, and accessible.”

### Visual

Show the product flow and UI concept.

---

## 01:35–02:00 — How It Works

### Voice

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

Target selection → data → computation → candidate sites.

---

## 02:00–02:25 — Six Criteria

### Voice

> “Our comparison is based on six environmental characteristics:
> aridity, temperature range, elevation, slope, surface roughness, and thermal behaviour.
>
> Together, these characteristics form the basis for comparing a planetary target with potential Earth analog locations.”

### Visual

Six animated criterion cards.

---

## 02:25–02:48 — NASA Data

### Voice

> “The platform is designed around NASA and partner datasets.
>
> The planned data pipeline uses NASA POWER for climate characteristics, elevation data for terrain-derived features, MODIS land surface temperature for thermal behaviour, and planetary sources such as Moon Trek, Mars Trek, and PDS for target-side information.
>
> These inputs are normalized into a consistent structure before comparison.”

### Visual

NASA data sources → normalization → Terra Analog pipeline.

---

## 02:48–03:20 — User Experience

### Voice

> “From the user's perspective, Terra Analog brings this analysis into one interface.
>
> Users can select a target, explore candidate Earth locations on a map, inspect similarity and confidence information, view criterion-by-criterion comparisons, and compare selected sites.
>
> The interface is designed to make the reasoning behind a match visible rather than hiding everything behind a single number.”

### Visual

Record actual UI where possible.

Show:

- Target selection
- Map
- Site cards
- Similarity
- Confidence
- Comparison

---

## 03:20–03:40 — AI Role

### Voice

> “AI has a specific role in Terra Analog.
>
> The scientific similarity and confidence calculations are handled by deterministic computation, not by an AI model.
>
> Once the results are calculated, the AI layer can help explain those results in clear language and generate useful insights from the computed evidence.”

### Visual

Show:

```text
NASA / Earth Data
       ↓
Deterministic Computation
       ↓
Similarity + Confidence
       ↓
AI Narration / Insights
```

Clearly separate computation from AI.

---

## 03:40–03:52 — Impact

### Voice

> “By connecting planetary environments with real locations on Earth, Terra Analog aims to support analog-site discovery for research, field testing, education, and future exploration planning.
>
> It connects Earth data with the environments of other worlds.”

### Visual

Research → field testing → education → exploration.

---

## 03:52–04:00 — Closing

### Voice

> “This is Terra Analog.
> Finding Earth. Preparing for Other Worlds.
> Thank you.”

### Visual

Terra Analog logo + tagline.

---

# 9. Critical Accuracy Rules

Before exporting the video, verify:

### Project Scope

- Exactly **4 planetary targets**
- Exactly **6 comparison criteria**

### Targets

- Shackleton crater rim
- South pole plateau site
- Jezero crater
- Gale crater

### Criteria

- Aridity
- Temperature range
- Elevation
- Slope
- Surface roughness
- Thermal behaviour

### AI Boundary

AI must not be presented as the system that calculates:

- Similarity
- Confidence
- Terrain classification

AI is used to narrate/explain already computed evidence.

### Data

Do not invent:

- Scientific measurements
- Similarity scores
- Confidence percentages
- Candidate rankings
- NASA dataset results

unless they actually exist in the project.

---

# 10. What NOT To Do

Avoid:

- Making the whole video with NotebookLM and submitting it directly.
- Using an AI voice without reviewing pronunciation and timing.
- Claiming the application is fully implemented if it is still a concept.
- Showing fake scientific results.
- Inventing NASA data values.
- Adding removed criteria.
- Overusing cinematic effects.
- Using unrelated stock footage for important scientific claims.
- Making AI appear responsible for deterministic scientific calculations.

---

# 11. Final Production Workflow

## Phase 1 — Now

### Lock

- Project name
- Team name
- Five member names
- Narrator
- Script
- Storyboard
- Visual style

### Create

- Logo/title
- Team card
- Problem graphics
- Solution flow
- Six-criteria graphics
- NASA data pipeline
- Architecture/AI boundary graphic

---

## Phase 2 — NotebookLM

Use NotebookLM to:

1. Review the project sources.
2. Generate a visual understanding of the concept.
3. Identify useful visual storytelling ideas.
4. Check whether the narrative clearly connects problem → solution → impact.

Do not treat generated content as the final source of truth.

---

## Phase 3 — Recording

Record:

- Narration
- Team introduction
- Any available product footage
- Optional team footage

Keep the narrator consistent throughout.

---

## Phase 4 — Editing

Combine:

1. Voiceover
2. Visual assets
3. UI recordings
4. NASA data visuals
5. Subtitles
6. Transitions
7. Final branding

Target approximately **235–238 seconds** during editing so the exported video safely remains under the 240-second limit.

---

# 12. Final Quality Checklist

Before submission:

- [ ] Video is ≤ 240 seconds
- [ ] Team name is included
- [ ] All five members are named
- [ ] Problem is clearly explained
- [ ] Solution concept is clearly explained
- [ ] Exactly 4 targets are used
- [ ] Exactly 6 criteria are used
- [ ] NASA/partner data sources are named accurately
- [ ] AI role is accurately explained
- [ ] No unsupported scientific results are shown
- [ ] No fake scores/rankings are shown
- [ ] Subtitles are readable
- [ ] Audio is clear
- [ ] Visuals match the Terra Analog design
- [ ] Concept/mockups are not presented as completed functionality
- [ ] Final video has a clear ending and project identity

---

# 13. Recommended Final Stack

| Task | Recommended Tool |
|---|---|
| Project source review | NotebookLM |
| Story/visual exploration | NotebookLM |
| Graphics | Canva / Figma |
| UI prototype | Existing Terra Analog frontend |
| Screen recording | OBS / built-in recorder |
| Voice | Human narrator preferred |
| AI voice fallback | AI TTS |
| Video editing | CapCut / Premiere Pro |
| Subtitles | CapCut / Premiere |
| Final review | Full team |

## Bottom Line

**Use NotebookLM to understand and visualize the story, not to replace the entire production process.**

The strongest workflow for Terra Analog is:

> **NotebookLM for concept → Gemini Pro for custom visuals → Canva/Figma for polished graphics → Terra Analog UI for product proof → human voice for authenticity → CapCut/Premiere for final editing.**

This keeps the video professional, authentic, technically accurate, and aligned with the current Terra Analog project architecture.
