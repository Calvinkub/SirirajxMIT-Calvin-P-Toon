# P14 · What does the AI cost per patient?

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "Cost + speed". PAGE TAG: "A14".

BREADCRUMB: "COST + SPEED | COST PER PATIENT"
TITLE: "On our estimate, AI inference costs about US$0.78–2.11 per patient-month, against a ~US$14 price."

LAYOUT: left a bar chart (x=80 to x=1080, y=180 to y=860); right a column of three KPI tiles (x=1120 to x=1840, y=180 to y=640) and below them a "Not in these numbers" box (y=670 to y=860). Footer below.

TOP-RIGHT: orange outlined badge "ESTIMATE · token budget not measured".

BAR CHART title: "AI cost per patient-month (US$)". Four vertical flat bars, value printed above each bar, label under each bar, no gridlines, no y-axis numbers:
  "Sonnet 5.5 API" 0.78 (teal)
  "Opus 5.5 API" 1.57 (teal)
  "1 H100, 1,000 patients" 2.11 (deep teal)
  "1 H100, 10,000 patients*" 0.21 (light teal with dashed outline)
  Under the chart, grey footnote: "* only if one GPU holds the load: not measured"
  Above the bars, a thin grey line reading "Assumes 7,800 input + 1,050 output tokens per patient-day"

KPI TILES (light grey, big number + label):
  "≈ US$14" – "price: 499 THB a month at 35 THB/US$"
  "≈ 2,700" – "patients where 1 rented GPU = Sonnet API cost"
  "≈ 6%" – "AI share of the price (Sonnet case)"

BOX "Not in these numbers" (white with orange #C2571A border), five short lines each with a small orange dot:
  "Clinician time (likely the largest)"
  "IRIS for Health licence"
  "Thai speech, embeddings, storage"
  "Second GPU for redundancy"
  "Customer acquisition"

FOOTER: "Source: docs/pitch/faq-appendix/slides/cost.html; Anthropic API list prices; H100 ≈ US$2.89/h (getdeploying.com, Sept 2026). 499 THB is a price hypothesis"

DO NOT: draw Anthropic, NVIDIA or cloud logos; add any revenue, margin or profit number; add numbers not listed.
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "What does it cost to run? Why self-host?" |
| Page type | Two-trend chart page (mirrors template slide 13: drawn bar chart with legend that labels estimates, plus "our view" tiles) |
| Layout | 4-bar chart, 3 KPI tiles, "not included" box |
| On-slide words | ≈ 100 |

## On-slide text (exact)

- Breadcrumb: COST + SPEED | COST PER PATIENT
- Title: On our estimate, AI inference costs about US$0.78–2.11 per patient-month, against a ~US$14 price.
- Badge: ESTIMATE · token budget not measured
- Chart: AI cost per patient-month (US$); Sonnet 5.5 API 0.78; Opus 5.5 API 1.57; 1 H100, 1,000 patients 2.11; 1 H100, 10,000 patients* 0.21; "* only if one GPU holds the load: not measured"; "Assumes 7,800 input + 1,050 output tokens per patient-day"
- Tiles: ≈ US$14 price: 499 THB a month at 35 THB/US$ · ≈ 2,700 patients where 1 rented GPU = Sonnet API cost · ≈ 6% AI share of the price (Sonnet case)
- Box: Not in these numbers: Clinician time (likely the largest) · IRIS for Health licence · Thai speech, embeddings, storage · Second GPU for redundancy · Customer acquisition

## Visual spec

- Calculations (for the speaker): monthly tokens 0.234 M in, 0.0315 M out; Sonnet 0.234 × 2 + 0.0315 × 10 = 0.78; Opus 0.234 × 4 + 0.0315 × 20 = 1.57; H100 2.89 × ~730 h ≈ 2,110 a month; /1,000 = 2.11; /10,000 = 0.21; break-even 2,110 / 0.78 ≈ 2,700; share 0.78 / 14 ≈ 6%.
- The 10,000-patient bar is dashed because GPU capacity per patient is unmeasured.

## Speaker notes (Q&A)

On an estimated budget of about 7,800 input and 1,050 output tokens per patient-day, which we have not measured, inference is about US$0.78 a patient-month on Claude Sonnet 5.5 list prices or about US$2.11 on one rented H100 at 1,000 patients. At pilot size self-hosting is more expensive; we self-host for data residency under PDPA, open-weight Thai speech, and cost that stops growing per token past roughly 2,700 patients. Load is already low: in router v2 about 60% of decisions used no model, and MedGemma returns a short JSON id, not prose. The big lines are people and licences, clinician sign-off time and the IRIS licence, and both are still to price.

## Data needed for this page

| Number | Value | Source | Status |
|---|---|---|---|
| Token budget | 7,800 in + 1,050 out per patient-day | `cost.html`, A08 | **Estimate, not measured** |
| Sonnet 5.5 / Opus 5.5 prices | US$2/10 and 4/20 per M tokens | Anthropic API list, via `sources.html` | List prices; re-check before quoting |
| H100 rate | ≈ US$2.89/h | getdeploying.com (RunPod), Sept 2026 | List price |
| Price | 499 THB, 35 THB/US$ | spec §2b, A08 | **Price hypothesis; exchange rate assumed** |
| GPU capacity per patient | — | — | **Missing: not measured** |
| Clinician time, IRIS licence | — | — | **Missing: to price with Siriraj and InterSystems** |

## Sources in repo

- `pitch/appendix/A08-cost-structure.md`
- `docs/pitch/faq-appendix/slides/cost.html`, `docs/pitch/faq-appendix/slides/sources.html`, `docs/pitch/faq-appendix/README.md`
- `experiments/tool_router_v2_results_Qwen3-*_cuda.json` (tier counts)
- `research/pitch-claims-check.md` ("Premium from 499: unvalidated")
