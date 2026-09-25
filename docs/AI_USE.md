# AI_USE.md — Terra Analog

Mandatory AI-use disclosure. **Update this continuously as you build — add a row the same day you do the work, not from memory afterward.** Names every AI tool used, what it was asked to do, and what it produced versus what a person wrote or decided.

## Tools in use on this project

| Tool | Role |
|---|---|
| Claude (Anthropic) | Documentation only — planning docs, `FEATURES.md`, `DESIGN.md`, `structure.md`, `plan.md`, `AGENTS.md`, `CLAUDE.md`, this file. No implementation code. |
| Antigravity (Gemini) | Coding help — implementation across acquisition loaders, compute functions, API, frontend |
| Human (you) | Some code written directly, without an AI tool — log which files below |

## What AI generated vs. what a person decided — the boundary

Consistent with `AGENTS.md`: the similarity score, data confidence score, and any terrain tag are **always deterministic code**, never AI output, regardless of which tool wrote the surrounding code. The only place an LLM's *output* appears in the running application itself is the two files in `src/ai/` — the site-detail rationale text and the compare-page verdict text. Everything else described in this log is AI used as a *development tool* (writing code, drafting docs, planning), which is a different thing from AI being part of the shipped product's runtime behavior — both are disclosed below, but they answer different questions.

## Runtime AI use (in the shipped app)

| File | What the model is given | What it returns | Fails gracefully? |
|---|---|---|---|
| `src/ai/insight.py` | One site's 6 computed scores + raw values | 2–3 paragraphs: why it matches / why it doesn't | Yes — page renders scores, bars, radar chart, table without this text if the call fails |
| `src/ai/compare_verdict.py` | 2–3 sites' already-computed scores | Short "best for X use case" recommendation | Yes — comparison table and radar overlay render without it |

## Development log (add rows as you go)

| Date | Tool | Task | AI-generated vs. human-written |
|---|---|---|---|
| _fill in_ | Claude | Challenge scoping, target/criteria selection, architecture decisions, `FEATURES.md`, `DESIGN.md`, `structure.md`, `plan.md`, `AGENTS.md`, `CLAUDE.md`, this file | Drafted by Claude from the team's decisions in conversation; all decisions (targets, criteria, cuts, tech choices) made by the team, Claude wrote the resulting documents. No implementation code from Claude. |
| _fill in_ | Antigravity (Gemini) | _fill in — e.g. "wrote src/acquire/load_power.py"_ | _fill in — e.g. "AI-generated from AGENTS.md + nasa-acquisition skill, reviewed and edited by [name]"_ |
| _fill in_ | Human, no AI tool | _fill in — which file(s) written directly_ | Human-written, no AI assistance |

Keep this table growing — a judge reading it should be able to tell, file by file, which tool touched it (or that no tool did) and how much of the result is AI output versus human decision-making.
