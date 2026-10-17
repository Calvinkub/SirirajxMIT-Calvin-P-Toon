# P03 · Is the data model thoughtful and interoperable?

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "IRIS + FHIR". PAGE TAG: "A03".

BREADCRUMB: "IRIS + FHIR | DATA MODEL"
TITLE: "Every fact is a standard FHIR R4 resource, including the AI's own provenance."

LAYOUT: five equal columns from y=190 to y=800 (each about 330 px wide, 20 px gaps), a summary bar at y=820 to y=900, then the footer.

Each column is a light grey rounded panel with a header in 24 px deep teal, a small lineal-colour icon above the header, and 3 to 4 white "resource cards" inside. Each card shows the resource name in 20 px semibold deep teal and one short grey line under it.

COLUMN 1 header "Who" (person icon):
  card "Patient" – "language th · district only"
  card "Practitioner" – "signs the limits"
  card "Device" – "AI model + watch"

COLUMN 2 header "Clinical facts" (clipboard icon):
  card "Condition" – "SNOMED CT"
  card "MedicationStatement" – "ATC · beta-blocker flag"
  card "Observation" – "LOINC 8867-4 HR · 41950-7 steps"
  card "DocumentReference" – "LOINC 18842-5 discharge note"

COLUMN 3 header "Limit record" (shield icon), with a 3 px teal border around the whole column:
  card "Goal + CarePlan" – "HR ceiling · RPE 11–13 · limit source"
  card "Provenance" – "attester = clinician"
  Under the cards, a small teal badge "CLINICIAN ONLY"

COLUMN 4 header "Daily loop" (calendar icon):
  card "Task" – "one mission, basedOn CarePlan"
  card "Provenance" – "assembler = AI model"
  card "QuestionnaireResponse" – "symptom tap"
  card "Flag + Communication" – "red flag to clinician" (this card has an orange #C2571A left edge)

COLUMN 5 header "Places + consent" (map-pin icon):
  card "Location" – "position · opening hours"
  card "HealthcareService" – "groups · intensity"
  card "Consent" – "insurer = deny"

SUMMARY BAR (full width, pale teal fill, three big numbers side by side with labels):
  "19" – "resource types"
  "383" – "synthetic resources"
  "9" – "PUT transaction bundles"
  At the right end of the bar a small orange outlined badge "SYNTHETIC".

FOOTER: "Source: synthetic/generate_fhir.py; synthetic/fhir/*.json (counted); codes to verify against LOINC, SNOMED CT and ATC browsers"

DO NOT: add a HL7 or FHIR logo; add resources not listed; add extra code numbers; draw connecting spaghetti lines between all cards.
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "Why FHIR? Show us the data model." |
| Page type | Column map (mirrors template slide 2: parallel product columns + one summary bar) |
| Layout | 5 columns of resource cards, limit-record column outlined, summary bar of 3 numbers |
| On-slide words | ≈ 105 |

## On-slide text (exact)

- Breadcrumb: IRIS + FHIR | DATA MODEL
- Title: Every fact is a standard FHIR R4 resource, including the AI's own provenance.
- Who: Patient (language th · district only); Practitioner (signs the limits); Device (AI model + watch)
- Clinical facts: Condition (SNOMED CT); MedicationStatement (ATC · beta-blocker flag); Observation (LOINC 8867-4 HR · 41950-7 steps); DocumentReference (LOINC 18842-5 discharge note)
- Limit record: Goal + CarePlan (HR ceiling · RPE 11–13 · limit source); Provenance (attester = clinician); CLINICIAN ONLY
- Daily loop: Task (one mission, basedOn CarePlan); Provenance (assembler = AI model); QuestionnaireResponse (symptom tap); Flag + Communication (red flag to clinician)
- Places + consent: Location (position · opening hours); HealthcareService (groups · intensity); Consent (insurer = deny)
- Summary: 19 resource types · 383 synthetic resources · 9 PUT transaction bundles · SYNTHETIC

## Visual spec

- Column 3 (limit record) is the only outlined column: it is the object the whole safety design depends on.
- The red-flag card is the only orange element.
- Optional detail for a backup build (not on the image): extension URLs `hr-ceiling`, `rpe-target`, `limit-source`, `allowed-activity`, `restriction`; BP 85354-9 (8480-6/8462-4); LVEF 10230-1; Consent category LOINC 59284-0, policy OPTIN, nested deny for role `PAYOR`.

## Speaker notes (Q&A)

The limit record is a `Goal` plus `CarePlan` carrying custom extensions for the HR ceiling, RPE range, limit source and allowed activities, signed through a `Provenance` that names the clinician as attester. Each mission is a `Task` based on that CarePlan, with its own `Provenance` naming the AI model as assembler, so an auditor can read what the model chose without trusting it. Red flags are a `Flag` plus a `Communication` to the clinician, and consent denies insurer access by default. Open choices we will discuss: `Task` vs `CarePlan.activity`, `Flag` vs `DetectedIssue`, and whether IRIS accepts our extensions without published profiles.

## Data needed for this page

| Number | Value | Source | Status |
|---|---|---|---|
| Resource types | 19 | counted from `synthetic/fhir/*.json` | Checked 2026-10-18 |
| Resources | 383 | counted from `synthetic/fhir/*.json` | Checked |
| Bundles | 9 (all `transaction`, all entries `PUT`) | counted | Checked |
| LOINC / SNOMED CT / ATC codes | as listed | `synthetic/generate_fhir.py`, `synthetic/README.md` | **To verify** against official browsers |
| `PAYOR` role code | — | A03 | **To verify** |
| `AuditEvent` | in design, not generated | A03 | Not on slide on purpose |

## Sources in repo

- `pitch/appendix/A03-fhir-data-model.md`
- `synthetic/generate_fhir.py`, `synthetic/README.md`, `synthetic/fhir/00_shared_reference_data.json`, `synthetic/fhir/p01…p08_*.json`
- `FHIR-AI-Hackathon-Kit/skills/iris-fhir/SKILL.md`
