# P04 · What data did you build, and what does each patient test?

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "IRIS + FHIR". PAGE TAG: "A04".

BREADCRUMB: "IRIS + FHIR | SYNTHETIC BUNDLES"
TITLE: "Eight synthetic patients, each built to test one path through the safety rules."

LAYOUT: left zone (x=80 to x=1000) with a row of four KPI tiles on top (y=180 to y=360) and a bar chart below (y=390 to y=880); right zone (x=1060 to x=1840) with an eight-row path list (y=180 to y=880). Footer below.

Top-right corner of the left zone: a small orange outlined badge "SYNTHETIC · data-origin = synthetic".

KPI TILES (light grey, rounded, big number 72 px deep teal, label 18 px grey):
  "8" – "patients"
  "383" – "FHIR R4 resources"
  "9" – "PUT transaction bundles"
  "143" – "Observations"

BAR CHART (vertical flat bars, teal #1B7F7A, value printed above each bar, category label under each bar, no gridlines, no y-axis numbers). Chart title above it: "Resources per bundle".
  "shared" 20
  "p01" 52
  "p02" 50
  "p03" 51
  "p04" 29  (this bar orange #C2571A)
  "p05" 52
  "p06" 28  (this bar orange #C2571A)
  "p07" 52
  "p08" 49
  Under the chart a one-line note in 18 px grey: "Orange = blocked paths: no Tasks written"

RIGHT ZONE: header "What each patient tests" (24 px). Eight rows, each row = small round id chip on the left (teal outline) + one line of text:
  "p01" – "Low risk after MI, CPET limit → normal missions"
  "p02" – "Age 71, 6-minute-walk limit → simple missions"
  "p03" – "LVEF 42%, moderate risk → supervised first"
  "p04" – "LVEF 30%, ICD → blocked, Flag" (chip orange)
  "p05" – "6 weeks after bypass → walking only"
  "p06" – "Limits in draft → no exercise" (chip orange)
  "p07" – "Chest tightness day 5 → red flag, Tasks cancelled" (chip orange)
  "p08" – "AF, fasting days → evening missions"

FOOTER: "Source: synthetic/fhir/*.json (counted 2026-10-18); synthetic/README.md. Invented data: not clinical or accuracy evidence"

DO NOT: show real patient photos or faces; add names other than the ids; add numbers not listed; add a y-axis scale.
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "Show us the data. Is it realistic? What does it test?" |
| Page type | KPI snapshot (mirrors template slide 3: 2×N big-number tiles + drawn bar chart + drivers column) |
| Layout | 4 KPI tiles, bar chart of resources per bundle, 8-row path list |
| On-slide words | ≈ 110 |

## On-slide text (exact)

- Breadcrumb: IRIS + FHIR | SYNTHETIC BUNDLES
- Title: Eight synthetic patients, each built to test one path through the safety rules.
- Badge: SYNTHETIC · data-origin = synthetic
- Tiles: 8 patients · 383 FHIR R4 resources · 9 PUT transaction bundles · 143 Observations
- Chart title: Resources per bundle; bars shared 20, p01 52, p02 50, p03 51, p04 29, p05 52, p06 28, p07 52, p08 49; note "Orange = blocked paths: no Tasks written"
- Path list (8 rows) as in the prompt.

## Visual spec

- Bars p04 and p06 are short because the rules leave them without missions: p04 has no CarePlan, Goal, Task or Provenance (a `Flag` instead); p06 has a `draft` CarePlan and no Tasks. p07 is full length but its later Tasks are `cancelled` and it carries a `Flag` + `Communication`.
- Per-type totals for a backup table: Observation 143, Provenance 48, Task 42, MedicationStatement 36, QuestionnaireResponse 27, Condition 18, Device 9, Patient 8, DocumentReference 8, Consent 8, Location 8, Goal 7, CarePlan 7, HealthcareService 7, Practitioner 2, Flag 2, Organization 1, Questionnaire 1, Communication 1.

## Speaker notes (Q&A)

All eight patients are invented and every resource is tagged `data-origin = synthetic`; they exist to exercise the rules, not to show accuracy. Each patient is one path: a normal low-risk case, an older patient with a 6-minute-walk limit, a moderate-risk case that needs supervision, a high-risk ICD patient who is blocked, a post-bypass patient with an upper-body restriction, a new sign-up whose limits are still in draft, a red flag on day 5, and a low-adherence patient who fasts. The bundles use `PUT Type/id` with stable ids, so reloading updates instead of duplicating, which is a known issue with POSTed Synthea bundles in the kit. They were validated with `fhir.resources` R4B; IRIS validates more strictly, so a live load is the next check.

## Data needed for this page

| Number | Value | Source | Status |
|---|---|---|---|
| Per-bundle counts | 20, 52, 50, 51, 29, 52, 28, 52, 49 | counted from `synthetic/fhir/*.json` | Checked 2026-10-18 |
| Totals | 383 resources, 143 Observations, 9 bundles | counted | Checked |
| Patient cases | 8 rows | `synthetic/README.md`, `synthetic/profiles.json` | In repo |
| p07 LVEF regenerated 48% → 53% | — | A03 | Not on slide |
| Live load into IRIS (200 per bundle, extensions accepted) | — | `synthetic/load_to_iris.py` | **Missing: not run / not confirmed** |

## Sources in repo

- `synthetic/fhir/*.json`, `synthetic/README.md`, `synthetic/profiles.json`, `synthetic/generate_fhir.py`, `synthetic/load_to_iris.py`
- `pitch/appendix/A03-fhir-data-model.md`
