# P16 · What is the clinical basis? Who sets limits without a CPET?

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "Clinic + business". PAGE TAG: "A16".

BREADCRUMB: "CLINIC + BUSINESS | CLINICAL BASIS"
TITLE: "A clinician sets the limit from CPET or another accepted test; the app only schedules inside it."

LAYOUT: left a matrix of limit sources (x=80 to x=1080, y=180 to y=760); right four risk-class cards stacked (x=1120 to x=1840, y=180 to y=760); bottom a two-part callout strip (y=790 to y=920). Footer below.

TOP-RIGHT: orange outlined badge "FIRST-PASS RESEARCH · TO VERIFY".

LEFT MATRIX header "1 · Where the limit comes from". Columns "Source", "Gives", "Synthetic patient". Six rows, thin grey lines, each row with a small lineal-colour icon:
  (lungs icon) "CPET" | "HR at first ventilatory threshold" | "p01, p05, p07, p08"
  (ECG icon) "Symptom-limited ECG test" | "peak HR on usual medicines" | "p03"
  (footsteps icon) "6-minute walk test" | "submaximal capacity" | "p02"
  (heart icon) "Resting HR + 20–30 bpm" | "early target, no test" | "not in v1"
  (gauge icon) "Borg RPE 11–14" | "perceived effort" | "always paired"
  (speech icon) "Talk test" | "can still talk" | "first on beta-blockers"
  The CPET row has a teal left edge; the "not in v1" cell is grey.

RIGHT CARDS header "2 · Who may use the app". Four cards, each a coloured left bar, a class name and one line:
  teal bar: "Low" – "app missions, once a clinician confirms"
  light teal bar: "Moderate" – "supervised sessions first (p03)"
  orange #C2571A bar: "High" – "blocked + referral Flag (p04)"
  grey bar: "Unknown" – "treated as blocked"

CALLOUT STRIP (pale teal, two halves):
  left half: big number "12" in orange + label "contradictions in our research, sent to a rehab physician"
  right half: "Beta-blockers: no %HRR formula. Clinician HR ceiling + RPE 11–13 + talk test."

FOOTER: "Source: research/guidelines/app-parameters-qa.md and RECONCILE-for-clinician.md (NotebookLM, 55 sources, machine-generated); synthetic/generate_fhir.py"

DO NOT: write any LVEF cut-off or %HRR number; draw guideline-society logos; call anything "proven" or "validated"; add numbers not listed.
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "Who sets limits for patients without CPET? Who is eligible? What about beta-blockers?" |
| Page type | Matrix (mirrors template slide 7: grid on the left, KPI/ranking column on the right, takeaway box) |
| Layout | 6-row limit-source matrix, 4 risk-class cards, callout strip |
| On-slide words | ≈ 125 |

## On-slide text (exact)

- Breadcrumb: CLINIC + BUSINESS | CLINICAL BASIS
- Title: A clinician sets the limit from CPET or another accepted test; the app only schedules inside it.
- Badge: FIRST-PASS RESEARCH · TO VERIFY
- Matrix: 1 · Where the limit comes from; 6 rows as in the prompt
- Cards: 2 · Who may use the app; Low – app missions, once a clinician confirms; Moderate – supervised sessions first (p03); High – blocked + referral Flag (p04); Unknown – treated as blocked
- Callout: 12 contradictions in our research, sent to a rehab physician · Beta-blockers: no %HRR formula. Clinician HR ceiling + RPE 11–13 + talk test.

## Visual spec

- LVEF bands are deliberately left off the slide because the sources conflict (≥ 50 vs > 50; moderate 35–49 vs 40–49); they are row 5–6 of the reconcile table.
- Synthetic-patient column ties each limit source to a FHIR `CarePlan` `limit-source` value (`cpet`, `exercise-ecg`, `6mwt`).

## Speaker notes (Q&A)

A clinician always sets the limit, and the `CarePlan` records who set it, from which test, when, and when it must be reviewed. Guidelines in our first-pass research accept CPET as the most precise source and also a symptom-limited stress test, a 6-minute walk, heart-rate-based targets, Borg effort and the talk test; on beta-blockers we do not compute any heart-rate formula and rely on the clinician's ceiling plus effort and talk test. Only clinician-confirmed low-risk patients get app missions; moderate risk starts supervised, high risk and unknown are blocked. Our research is machine-generated and contradicts itself in 12 places, for example 50–70% HRR vs a first ventilatory threshold around 39–45% HRR after MI, so nothing is coded until a rehab physician reconciles it. If asked about home-rehab safety: no significant difference in trials of screened low- and moderate-risk patients, and the intervals include a possible increase in serious events.

## Data needed for this page

| Item | Source | Status |
|---|---|---|
| Accepted limit sources | `research/guidelines/app-parameters-qa.md`, A10 | Machine-generated; **primary guidelines (ESC 2020, EAPC, AACVPR, IACR, Thai 2020) not opened** |
| Synthetic limit sources per patient | `synthetic/generate_fhir.py`, A03/A10 | In repo |
| 12 contradictions | `research/guidelines/RECONCILE-for-clinician.md` | In repo, **unresolved** |
| Risk-class criteria and LVEF bands | A10 | **Conflicting: to reconcile** |
| Clinician sign-off of any value | — | **Missing (gate G-B)** |

## Sources in repo

- `pitch/appendix/A10-clinical-evidence.md`
- `research/README.md`, `research/guidelines/app-parameters-qa.md`, `research/guidelines/RECONCILE-for-clinician.md`
- `research/pitch-claims-check.md` (CPET underused)
- `synthetic/generate_fhir.py`, `pitch/judge-questions.md` Q11–Q13
