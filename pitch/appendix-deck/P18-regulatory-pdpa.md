# P18 · Is this a medical device? What about PDPA?

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "Clinic + business". PAGE TAG: "A18".

BREADCRUMB: "CLINIC + BUSINESS | REGULATORY AND PDPA"
TITLE: "Positioned as adherence support inside clinician limits; device and privacy questions go to lawyers first."

LAYOUT: three equal numbered columns (y=180 to y=800), then a full-width "Needs a real lawyer" strip (y=830 to y=930). Footer below.

TOP-RIGHT: orange outlined badge "NOT LEGAL ADVICE · TO VERIFY".

COLUMN 1 header "1 · What we say" (speech-bubble icon). Two-part list, left label "We say" in teal, right label "We avoid" in grey with strike-through:
  "inside your clinician's safe limits" | "optimal, exact plan"
  "designed to improve rehab adherence" | "proven to reduce readmissions"
  "stop now and call 1669" | "symptom interpretation"
  "ask your doctor or pharmacist" | "drug or dose advice"

COLUMN 2 header "2 · Thai FDA software question" (scale icon). Four rows "Feature → our design":
  "Exercise intensity" → "AI picks from a clinician-set list"
  "Red-flag message" → "fixed text, rules only"
  "Discharge-note reading" → "draft; clinician confirms"
  "Weekly progression" → "proposal to the clinician queue"
  Under the rows, orange #C2571A tag: "Classification: open question"

COLUMN 3 header "3 · PDPA consents in FHIR" (padlock icon). Five small rows with toggle icons:
  "App + clinician care" – toggle ON (teal)
  "Wearable data import" – toggle ON (teal)
  "AI processing" – toggle ON (teal)
  "Caregiver summary" – toggle "optional" (grey)
  "Insurer, aggregate only" – toggle OFF (orange)
  Under the rows: "Home district, not address · hosted in Thailand (planned)"

STRIP (white with orange border): "Needs a real lawyer: device classification · lawful basis and controller roles · cross-border transfer · insurer access"

FOOTER: "Source: pitch/appendix/A12; design spec §2b, §4, §5; synthetic Consent resources (insurer = deny)"

DO NOT: draw Thai FDA, OIC or government logos or seals; cite section numbers of any law; add numbers other than 1669; use the words "approved" or "compliant".
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "Is this a medical device? What about PDPA and insurer access?" |
| Page type | Three-pillar columns (mirrors template slide 4/5: three numbered columns with a full-width takeaway, here "needs a real lawyer") |
| Layout | Wording do/don't, SaMD feature table, consent toggles, lawyer strip |
| On-slide words | ≈ 125 |

## On-slide text (exact)

- Breadcrumb: CLINIC + BUSINESS | REGULATORY AND PDPA
- Title: Positioned as adherence support inside clinician limits; device and privacy questions go to lawyers first.
- Badge: NOT LEGAL ADVICE · TO VERIFY
- Column 1: 1 · What we say; 4 pairs as in the prompt
- Column 2: 2 · Thai FDA software question; 4 rows as in the prompt; Classification: open question
- Column 3: 3 · PDPA consents in FHIR; App + clinician care ON; Wearable data import ON; AI processing ON; Caregiver summary optional; Insurer, aggregate only OFF; Home district, not address · hosted in Thailand (planned)
- Strip: Needs a real lawyer: device classification · lawful basis and controller roles · cross-border transfer · insurer access

## Visual spec

- Toggles in column 3 show the default state of the five consents in the design; insurer access is the one orange "OFF".
- In the synthetic data today each `Consent` has scope `patient-privacy`, category LOINC 59284-0, policy OPTIN, a permit for TREAT and a nested deny for role `PAYOR` (code to verify). The five separate consents are the design; the synthetic set has one Consent per patient.

## Speaker notes (Q&A)

We position v1 as rehab-adherence support: a clinician sets the limits and the AI schedules small missions inside them; it does not diagnose, set limits, change medication or replace cardiac rehab. Whether Thai FDA would still treat it as software as a medical device is an open question that we will put to a regulatory lawyer or Thai FDA in writing, with a draft intended-use statement and feature list, before any real patient. Under PDPA, consents are separate and stored as FHIR `Consent`, the MCP layer checks consent on every read, the home is stored as a district, models are self-hosted so data stays in Thailand, and insurers see aggregate adherence only, never patient-level data and never for underwriting. Nothing here has been checked by a lawyer yet.

## Data needed for this page

| Item | Source | Status |
|---|---|---|
| Wording rules | A12, `pitch/README.md` rules, spec §2b | In repo |
| SaMD feature table | A12 | In repo; **classification unknown** |
| Consent design (5 consents) | A12 | Design; synthetic data has 1 Consent per patient with insurer deny |
| `PAYOR` role code | A03, A12 | **To verify** |
| Legal review (Thai FDA, PDPA, OIC) | — | **Missing: no lawyer consulted** |
| IRB route | A12 | **Missing: hospital IRB not contacted** |

## Sources in repo

- `pitch/appendix/A12-regulatory-pdpa.md`
- `docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md` §2b, §4, §5
- `synthetic/generate_fhir.py` (Consent with PAYOR deny, district-only address)
- `evaluation/reviews/2026-10-17-document/SYNTHESIS.md` R3, R8, R10 (simulated)
- `pitch/judge-questions.md` Q14
