# Synthetic demo data

**Everything here is invented.** No real patient, clinician, clinic or place. Every resource carries the meta tag `data-origin = synthetic`. Do not use any of it as clinical or model-accuracy evidence.

## What is here

| Path | What |
|---|---|
| `generate_fhir.py` | Builds FHIR R4 transaction bundles (seed 42), validated with `fhir.resources` R4B models as in the FHIR-AI-Hackathon-Kit |
| `fhir/00_shared_reference_data.json` | Organization, 2 Practitioners, AI model Device, symptom-check Questionnaire, 8 Locations (Bangkok-area coordinates, fictional names), 7 HealthcareServices (activities with an intensity tag) |
| `fhir/p01…p08_*.json` | One bundle per patient |
| `profiles.json` | One line per patient: risk and story |
| `tool_router_utterances.jsonl` | 72 Thai and English messages, 8 per label, for the tool-router demo |
| `load_to_iris.py` | Loads the bundles into the kit's IRIS for Health FHIR server (`http://localhost:52773/fhir/r4/`) |

Regenerate: `.venv/bin/python synthetic/generate_fhir.py` (needs `fhir.resources` 8.x, Python 3.10+).

## The 8 patients (each a different case the app must handle)

| Id | Case | What the app should do |
|---|---|---|
| cmc-p01 | **Demo patient.** Somchai, 58, Bang Na; high blood pressure and MI this year; low risk, CPET limit (HR < 110, ≤ 5.9 METs), beta-blocker; used to play tennis | Normal daily missions; Netflix-style picks: bowling, table tennis, badminton |
| cmc-p02 | Aged 71, limit from 6-minute walk, low tech comfort | Simple missions, caregiver help |
| cmc-p03 | Moderate risk, LVEF 42% | Supervised sessions first |
| cmc-p04 | High risk, LVEF 30%, ICD | Blocked; `Flag` "not eligible" |
| cmc-p05 | 6 weeks after bypass surgery | Walking only, upper-body restriction |
| cmc-p06 | New sign-up, limit record in draft | No exercise missions yet |
| cmc-p07 | Chest tightness reported on day 5 | Red-flag `Flag` + `Communication` to clinician; later missions cancelled |
| cmc-p08 | Several conditions incl. AF, low adherence, fasting days | Evening missions, many missed |

## Resources per patient (about 5–10 rows of each kind)

Patient · Condition (2–4) · MedicationStatement (4–5) · DocumentReference (synthetic discharge note) · Device (watch) · Observation (LVEF, risk class, 7 days of resting heart rate and steps, 2 blood-pressure panels) · Consent (insurer access denied) · Goal + CarePlan (the limit record, as extensions) + Provenance (clinician attests) · Task (7 daily missions) + Provenance (AI model assembled it from the allowed set) · QuestionnaireResponse (symptom check per finished mission) · Flag / Communication where relevant.

## Codes

- LOINC: 8867-4 heart rate, 41950-7 steps in 24 h, 85354-9 / 8480-6 / 8462-4 blood pressure, 10230-1 LVEF, 18842-5 discharge summary, 59284-0 consent. SNOMED CT for conditions, ATC for medicines.
- Our own concepts (risk class, mission ids, limit extensions, activity intensity) use the placeholder system `https://cvd-mission-coach.example/fhir/...`.
- **Check before any real use:** every code above against the official LOINC, SNOMED CT and ATC browsers; the `PAYOR` role code in Consent; whether the IRIS FHIR server accepts the custom extensions without profiles.
