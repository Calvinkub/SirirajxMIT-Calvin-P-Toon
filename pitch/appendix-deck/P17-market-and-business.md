# P17 · Who pays, and who else does this?

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "Clinic + business". PAGE TAG: "A17".

BREADCRUMB: "CLINIC + BUSINESS | WHO PAYS"
TITLE: "Insurers pay for recovery and patients can start free; both are hypotheses we will test."

LAYOUT: three columns (y=180 to y=880): left "Who pays" cards (x=80 to x=680), middle "Why Thailand" tiles (x=720 to x=1300), right "Others and gaps" (x=1340 to x=1840). Footer below.

COLUMN 1 header "1 · Who pays". Three stacked cards, each with a lineal-colour icon, a bold name, two short lines, and a status tag:
  (umbrella icon) "Insurer (B2B2C)" – "per-member fee, to negotiate" / "aggregate reports only" – orange tag "UNVERIFIED IN THAILAND"
  (phone icon) "Patient (B2C)" – "1 free week, then from 499 THB a month" / "free week = no exercise without signed limits" – orange tag "PRICE HYPOTHESIS"
  (hospital icon) "Hospital" – "enrols and signs limits" / "enabler, not payer yet" – grey tag "CHANNEL"

COLUMN 2 header "2 · Why Thailand". Three tiles, big number + label + tiny grey caveat:
  "10 days" – "Thai recommendation: start rehab by then" – caveat "guideline statement"
  "12.5%" – "phase-2 rehab uptake after bypass" – caveat "single site"
  "83.3%" – "of them never told about rehab" – caveat "same study"
  Under the tiles: "No public fee code for digital therapeutics: private payers first"

COLUMN 3 header "3 · Others and gaps".
  Small table "Name", "Where", "Note":
    "Movn Health" | "US" | "clinician-led virtual rehab"
    "Cardihab" | "Australia" | "app + clinician portal"
    "EAPC EXPERT" | "Europe" | "tool for clinicians"
  Then an orange-bordered box "Gaps" with three lines:
    "No insurer spoken to yet"
    "No Thai willingness-to-pay data"
    "No market size shown"

TAKEAWAY STRIP (pale teal, full width): "Cheapest next test: a concierge pilot with 8–10 clinician-enrolled patients over LINE."

FOOTER: "Source: research/README.md; research/market/notebooklm-deep-report.md (machine-generated, corrections block); research/pitch-claims-check.md. Vendor figures not used"

DO NOT: draw Movn, Cardihab, AIA, LINE or insurer logos; show a TAM/SAM/SOM; add readmission-reduction claims or any number not listed.
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "Who pays? Who are the competitors? Why Thailand, why now?" |
| Page type | Segment cards + why (mirrors template slide 9: segment cards, evidence tiles, numbered "why" list and key takeaway) |
| Layout | Payer cards, Thailand evidence tiles, competitor table + gaps box, takeaway |
| On-slide words | ≈ 135 |

## On-slide text (exact)

- Breadcrumb: CLINIC + BUSINESS | WHO PAYS
- Title: Insurers pay for recovery and patients can start free; both are hypotheses we will test.
- Column 1: 1 · Who pays; Insurer (B2B2C) – per-member fee, to negotiate / aggregate reports only [UNVERIFIED IN THAILAND]; Patient (B2C) – 1 free week, then from 499 THB a month / free week = no exercise without signed limits [PRICE HYPOTHESIS]; Hospital – enrols and signs limits / enabler, not payer yet [CHANNEL]
- Column 2: 2 · Why Thailand; 10 days – Thai recommendation: start rehab by then (guideline statement); 12.5% – phase-2 rehab uptake after bypass (single site); 83.3% – of them never told about rehab (same study); No public fee code for digital therapeutics: private payers first
- Column 3: 3 · Others and gaps; Movn Health US clinician-led virtual rehab; Cardihab Australia app + clinician portal; EAPC EXPERT Europe tool for clinicians; Gaps: No insurer spoken to yet · No Thai willingness-to-pay data · No market size shown
- Takeaway: Cheapest next test: a concierge pilot with 8–10 clinician-enrolled patients over LINE.

## Visual spec

- Vendor claims (Movn "20–30% fewer readmissions", Cardihab "21% → 63%") are deliberately not on the slide; they are vendor-reported.
- "No market size shown" is a stated gap, not an omission.
- The insurer pitch wording for the speaker: "designed to improve rehab adherence, which is linked to fewer readmissions" (never "proven to reduce").

## Speaker notes (Q&A)

Two routes: an insurer offers the program as a recovery benefit next to critical-illness cover, and patients can start with a free week and then pay from 499 baht a month; Thailand's public schemes have no fee code for digital therapeutics, so private payers and self-pay come first. Both are hypotheses: we have not spoken to an insurer and have no Thai willingness-to-pay data, so we propose a concierge pilot over LINE with 8 to 10 clinician-enrolled patients, after ethics review, to test adherence and price before building the full stack. Clinician-led virtual rehab exists abroad, Movn in the US and Cardihab in Australia; we have not found a Thai-language, patient-first, daily-mission product, but that is not a proven absence. The Thai numbers come from first-pass research and a single-site study and must be checked against the primary sources before quoting.

## Data needed for this page

| Number | Value | Source | Status |
|---|---|---|---|
| Rehab start | ≤ 10 days after discharge | Thai post-ACS recommendations 2020, via `research/README.md` | **To verify against primary** |
| Phase-2 uptake after CABG | 12.5% | single-site study, via `research/README.md`, used in `main-3min.md` | **To verify** |
| Never told | 83.3% | same | **To verify** |
| Price | 499 THB/month | spec §2b | **Hypothesis** |
| Insurer fee | — | — | **Missing (pitch README: "[PRICE]" placeholder on slide 5)** |
| TAM/SAM/SOM | — | A11 | **Not presented: Thai post-MI incidence and private-cover data unverified** |
| Insurer and patient interviews | 3–5 each | A11 | **Not done** |

## Sources in repo

- `pitch/appendix/A11-market-and-business.md`
- `research/README.md`, `research/market/notebooklm-deep-report.md`, `research/pitch-claims-check.md`
- `evaluation/reviews/2026-10-17-document/SYNTHESIS.md` R12, R13, R16, R17 (simulated)
- `pitch/main-3min.md` (business slide)
