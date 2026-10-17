# P06 · What do you embed in IRIS Vector Search, and how do you keep the model grounded?

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "IRIS + FHIR". PAGE TAG: "A06".

BREADCRUMB: "IRIS + FHIR | VECTOR SEARCH GROUNDING"
TITLE: "Vector Search answers only from clinician-approved text: no snippet, no answer."

LAYOUT: two panels side by side (y=180 to y=640), then a full-width grounding-rule flow (y=670 to y=900), then the footer.

LEFT PANEL (x=80 to x=940, light grey) header "1 · Approved guideline lines" with a small book icon. Under the header, a monospace grey line: "vector_search(\"hypertension exercise\", k = 4)". Then four numbered white cards, each one line:
  "1  30 min moderate aerobic, 5–7 days a week"
  "2  Resistance training 2–3 days a week"
  "3  Avoid heavy static lifting and breath-holding"
  "4  SBP above 160: no high intensity until controlled"
  Under the cards, small grey text: "ESC 2020 sports cardiology, §4.2.3 hypertension · paraphrased"

RIGHT PANEL (x=980 to x=1840, light grey) header "2 · Activity catalogue: intensity" with a small running-shoe icon. A single horizontal stacked bar, full panel width, split in two parts with the count printed inside each part:
  teal part "44" labelled below "with a 2024 Compendium code"
  light grey part "56" labelled below "team estimates · to verify"
  Above the bar: big number "100" with label "activities, MET value each".
  Under the bar, one line: "Limit in the demo: up to 5.9 METs (synthetic)"

GROUNDING FLOW (full width, rounded boxes, teal arrows left to right):
  "Question" → "Red-flag screen" (teal badge "RULES ONLY") → "Vector Search" (teal badge "VECTOR", second line "approved collections only") → diamond "Score ≥ threshold and approved?"
  From the diamond, an orange #C2571A arrow labelled "no" goes to an orange-outlined box "Fixed reply: please ask your care team".
  From the diamond, a teal arrow labelled "yes" goes to a box "Reply cites snippet ids" then to a box "ids logged for audit".

FOOTER: "Source: demo/agent-flow-demo.html (GUIDE, catalogue); FHIR-AI-Hackathon-Kit skill iris-vector-search; Thai embedding (BGE-M3) not yet tested"

DO NOT: write the guideline lines as quotations or add quotation marks around them; add any other guideline numbers; add an ESC logo; add a similarity score number.
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "What is your smart use of Vector Search? Does it work in Thai?" |
| Page type | Two-panel chart page (mirrors template slide 13: two side-by-side panels, each with its own figure and caption) + a flow strip |
| Layout | Guideline retrieval panel, activity-catalogue bar, grounding-rule flow |
| On-slide words | ≈ 120 |

## On-slide text (exact)

- Breadcrumb: IRIS + FHIR | VECTOR SEARCH GROUNDING
- Title: Vector Search answers only from clinician-approved text: no snippet, no answer.
- Left: 1 · Approved guideline lines; `vector_search("hypertension exercise", k = 4)`; lines 1–4 as in the prompt; "ESC 2020 sports cardiology, §4.2.3 hypertension · paraphrased"
- Right: 2 · Activity catalogue: intensity; 100 activities, MET value each; 44 with a 2024 Compendium code; 56 team estimates · to verify; Limit in the demo: up to 5.9 METs (synthetic)
- Flow: Question → Red-flag screen [RULES ONLY] → Vector Search [VECTOR] (approved collections only) → Score ≥ threshold and approved? → no: Fixed reply: please ask your care team / yes: Reply cites snippet ids → ids logged for audit

## Visual spec

- The guideline lines are the four paraphrased lines in the demo's `GUIDE` array, shortened for the slide. They must stay labelled "paraphrased".
- 44 = activities in the demo catalogue with a 2024 Adult Compendium code (one of them marked "closest listed activity"); 56 = no code, team estimate. The demo footer says "about 40"; the exact count from the file is 44.
- Embedded collections (for speaker, not on slide): mission explanations, patient-education snippets, guideline snippets (blocked until clinician sign-off), community activities (`HealthcareService.comment`), discharge-note text. No raw chat or watch streams are embedded.

## Speaker notes (Q&A)

We embed only clinician-approved content: guideline and education snippets, mission explanations and an intensity-tagged list of community activities. The patient sees an answer only if it cites a retrieved, approved snippet above a threshold; otherwise a fixed "please ask your care team" message, and the cited ids go into the audit log. In the demo, the four ESC 2020 hypertension lines are paraphrased examples and the 100 activity MET values are partly from the 2024 Compendium and partly our estimates, so a clinician must check them. For Thai we need a multilingual embedding model hosted in Thailand; BGE-M3 is the candidate, its Thai retrieval is not measured yet, and the test plan is Recall@3 and MRR on a blind held-out set against the kit's `text-embedding-3-small` baseline.

## Data needed for this page

| Number or item | Value | Source | Status |
|---|---|---|---|
| Guideline lines | 4, ESC 2020 §4.2.3, paraphrased | `demo/agent-flow-demo.html` `GUIDE` | In repo; **primary guideline text not re-checked** |
| Catalogue size | 100 | `demo/agent-flow-demo.html` `RAW` (counted) | Checked |
| Compendium-coded | 44 (1 "closest listed") | counted from `RAW` | Checked; **each MET value to verify by clinician** |
| Demo limit | 5.9 METs, HR 120, RPE 11–13 | `LIMIT` in demo (patient `cmc-p09`, not in the 8 bundles) | Synthetic |
| Score threshold | — | A05 | **Missing: to tune on a labelled set** |
| Thai retrieval quality (BGE-M3) | — | A05 | **Missing: test not run** |
| Live IRIS vector table | — | — | **Not built** (demo is scripted in-browser) |

## Sources in repo

- `pitch/appendix/A05-intersystems-vector-search-and-geo.md`
- `demo/agent-flow-demo.html` (`GUIDE`, `RAW`, `LIMIT`, footer)
- `FHIR-AI-Hackathon-Kit/skills/iris-vector-search/SKILL.md` (`VECTOR`, `TO_VECTOR`, `VECTOR_COSINE`)
- `pitch/judge-questions.md` Q3
