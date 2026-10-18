# P08 · What runs inside the agent harness, and why those models?

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "Agent". PAGE TAG: "A08".

BREADCRUMB: "AGENT | MODELS, ONE JOB EACH"
TITLE: "Open models each do one narrow job; fixed rules decide what is safe."

LAYOUT: a matrix table on the left (x=80 to x=1430, y=180 to y=880) and a narrow KPI column on the right (x=1470 to x=1840, y=180 to y=880). Footer below.

MATRIX: 4 columns with header row in deep teal on pale teal: "Job", "Model", "How we use it", "Known limit". 7 rows, alternating white and very light grey, each row starts with a small lineal-colour icon in the "Job" cell:
  row 1 (ear icon): "Hear" | "Qwen3-ASR 1.7B" | "Thai + English speech to text" | "Older Thai speakers: to test"
  row 2 (signpost icon): "Route" | "Qwen3-4B or 1.7B" | "score a closed tool list" | "writing calls missed red flags"
  row 3 (target icon): "Choose" | "MedGemma 27B" | "one English JSON turn, closed choice" | "card: not for direct clinical decisions"
  row 4 (document icon): "Read notes" | "MedGemma 1.5 4B" | "draft extraction" | "clinician confirms every field"
  row 5 (speech-bubble icon): "Thai phrasing" | "Qwen3-8B or Typhoon 2" | "fact-checked against the mission" | "to choose"
  row 6 (speaker icon): "Speak" | "Qwen3-TTS" | "English voice" | "no Thai: Typhoon2-Audio or JaiTTS, to test" (this last cell in orange #C2571A)
  row 7 (shield icon, row filled pale teal): "Safety" | "No model" (teal badge "RULES ONLY") | "red flags, limits, allowed set, output filter" | "Thai phrase list needs a clinician"

KPI COLUMN: four stacked small tiles (light grey), each a big value in 40 px deep teal and a one-line label:
  "85.3" – "MedQA, MedGemma 27B card"
  "69.1" – "MedQA, MedGemma 1.5 4B card"
  "119" – "languages incl. Thai, Qwen3"
  "10" – "TTS languages, Thai not one"

FOOTER: "Source: model cards checked Oct 2026 (docs/pitch/faq-appendix/slides/sources.html); pitch/appendix/A04. Model-card scores, not our measurements"

DO NOT: draw Qwen, Google, Gemma or Typhoon logos; add parameter counts or scores not listed; add a robot mascot.
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "What runs inside your harness, and why those models?" |
| Page type | Matrix (mirrors template slide 7: drawn grid of capabilities × options + KPI column + takeaway) |
| Layout | 7-row × 4-column matrix, 4-tile KPI column |
| On-slide words | ≈ 135 (matrix page) |

## On-slide text (exact)

- Breadcrumb: AGENT | MODELS, ONE JOB EACH
- Title: Open models each do one narrow job; fixed rules decide what is safe.
- Matrix header: Job · Model · How we use it · Known limit
- Rows 1–7 exactly as in the prompt
- KPI column: 85.3 MedQA, MedGemma 27B card · 69.1 MedQA, MedGemma 1.5 4B card · 119 languages incl. Thai, Qwen3 · 10 TTS languages, Thai not one

## Visual spec

- The "Safety" row is visually different (pale teal) to show that the most important job has no model.
- The only orange cell is the Thai TTS gap: it is a real limitation, shown on purpose.
- KPI tiles are model-card figures, labelled as such in the footer.

## Speaker notes (Q&A)

Each open model gets one narrow job with a typed input and output. Qwen3-ASR hears Thai and English; a small Qwen3 router scores a closed list of tools instead of writing the call, because writing calls was slow and missed every red flag in our test; MedGemma 27B gets one English JSON request and may only choose a mission id from the set the rules allowed, because its card says it is not for direct clinical decisions, not optimised for multi-turn chat and red-teamed mainly in English. MedGemma 1.5 4B drafts fields from a discharge note and a clinician confirms each one. Qwen3-TTS open weights do not cover Thai, so Thai voice needs a second engine we still have to test, and safety audio such as the stop message is pre-recorded, never synthesised live.

## Data needed for this page

| Item | Value | Source | Status |
|---|---|---|---|
| MedGemma 27B MedQA | 85.3 | MedGemma model card, via A04 and `sources.html` | Checked against card Oct 2026 (per repo) |
| MedGemma 1.5 4B MedQA | 69.1, 128K context | same | Same |
| Qwen3 languages | 119 incl. Thai | Qwen3 release, via A04 | Same |
| Qwen3-TTS languages | 10, not Thai | Qwen3-TTS card, via A04 | Same |
| Thai phrasing model choice | Qwen3-8B or Typhoon 2 | A04, `HANDOFF.md` | **Not chosen** |
| Thai TTS choice | Typhoon2-Audio or JaiTTS | A04 | **Not tested** |
| Qwen3-ASR on older Thai speakers | — | A04 | **Not tested** |
| Any model actually served in the harness | — | — | **Not built** (router ran in Colab experiments only) |

## Sources in repo

- `pitch/appendix/A04-agentic-harness.md` (models table)
- `docs/pitch/faq-appendix/slides/harness.html`, `docs/pitch/faq-appendix/slides/sources.html`
- `HANDOFF.md` (agentic workflow plan, model stack)
- `experiments/RESULTS_tool_router_demo.md` (why route by scoring)
