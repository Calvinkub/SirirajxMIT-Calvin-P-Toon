# Remote monitoring: from episodic care to value-based care

This branch (`feat/remote-monitoring-dashboard`) moves Heartstep from occasional visits to continuous, patient-reported monitoring.

## What it does

| Piece | File | What |
|---|---|---|
| Patient diary (PROM) | `app.js` (Diary tab), `styles.css` | Daily BP, resting heart rate, morning weight, one question ("coffee in the last 30 minutes?"), a warning-symptom box, and a weekly PROM (how do you feel, 1-5) and PREM (felt listened to, 1-5). |
| Rules engine | `monitor.js` | Plain rules turn the diary into a zone: green, amber or red, with a reason and a next step. No model decides the zone. |
| Care-network dashboard | `dashboard.html` | Doctor, nurse and coach views. Triage list sorted red first, trend lines, PROM and PREM averages. |
| Red-zone tracker | `dashboard.html` | Each red zone opens a case: open, acknowledged, called, resolved, with a log. Coach cannot act on cases. |
| Tests | `tests/monitor.test.mjs` | Rules, coffee note, input checks, seed cohort. |

The Somchai row on the dashboard is LIVE: it reads the diary saved by the patient app in the same browser. The other six patients are synthetic.

## Rules (prototype defaults, a clinician sets them per patient)

- Weight: amber at +1.0 kg in 2 days or +1.5 kg in 7 days. Red at +2.0 kg in 3 days or +2.5 kg in 7 days.
- Blood pressure: red at 180/110 or higher, or top number under 90. Amber at 160/100 or higher, under 100, or 140/90 or higher for three readings in a row.
- Resting heart rate: red above 120 or under 45. Amber above 100 or under 50.
- Coffee "yes" adds a "recheck in 30 minutes" note to amber BP and heart rate. It never lowers a red zone.
- A reported warning symptom is red. Two days with no diary is amber.

### Where the thresholds come from (checked 2026-10-18)

| Rule | Source | Status |
|---|---|---|
| Weight gain over 2 kg in 3 days: tell the care team | ESC Heart Failure Association patient site: https://www.heartfailurematters.org/warning-signs/rapid-weight-gain/ | Verified page |
| More than 2-3 lb a day or 5 lb a week | Hospital patient-education pages citing AHA-style advice, e.g. https://healthlibrary.methodisthealthsystem.org/when-call-doctor-heart-failure | Rule of thumb, not AHA primary |
| Home BP 135/85 or higher is hypertension; 180/110 or higher is urgent | 2024 ESC hypertension guideline: https://academic.oup.com/eurheartj/article/45/38/3912/7741010 | Numbers confirmed from search summaries, not the page text |
| BP above 180 and/or 120 is a crisis (AHA) | https://www.heart.org/en/health-topics/high-blood-pressure/understanding-blood-pressure-readings/monitoring-your-blood-pressure-at-home | Page returned 403; unverified |
| Heart-rate cut-offs (120, 100, 50, 45) | none found | **Unverified. Team choice. A clinician must set these.** |
| 2 kg rule for self-care and daily weights | 2021 ESC HF guideline, section 9.3: https://academic.oup.com/eurheartj/article/42/36/3599/6358045 | Exact kg figure not seen on the page |
| The BP "sustained 3 readings" and weight "+1 kg in 2 days" amber levels | none | **Team choices, to review with a clinician** |

## Reference projects on GitHub

All URLs below were opened on 2026-10-18. No open-source project was found that does the whole job (diary, rules, care-team dashboard), so these are building blocks.

| Repo | What it does | Licence | Idea we borrow |
|---|---|---|---|
| https://github.com/hapifhir/hapi-fhir | Java FHIR R4/R5 server and API | Apache-2.0 | Store each reading as an Observation; raise a Flag or Communication |
| https://github.com/medplum/medplum | FHIR repository, auth, React components, server-side Bots | Apache-2.0 | Bots as the rule engine; React care-team panel |
| https://github.com/openmhealth/schemas | Open mHealth data-point schemas | Apache-2.0 | Shapes for BP, weight, heart-rate points (names not confirmed) |
| https://github.com/openmhealth/omh-dsu-ri | Reference data store with OAuth2 | Apache-2.0 | Patient-owned store with scoped clinician access |
| https://github.com/openmhealth/shimmer | Pulls Withings, iHealth, Fitbit data into Open mHealth format | Apache-2.0 | Later: import BP and weight automatically |
| https://github.com/HL7/phd | FHIR Personal Healthcare Devices guide (scales, BP cuffs) | not confirmed | Mark device vs patient-entered readings |
| https://github.com/hl7-be/patient-monitoring | Belgian FHIR guide for remote patient monitoring | not confirmed | Exchange of monitoring outcomes |
| https://github.com/openmrs/openmrs-esm-patient-chart | OpenMRS 3 patient chart, Vitals and Biometrics widget | not confirmed | Vitals trend widgets in a clinician view |
| https://github.com/aehrc/smart-forms | React renderer for FHIR Questionnaires | Apache-2.0 | Diary and PROM/PREM as a Questionnaire |
| https://github.com/cqframework/clinical-reasoning | CQL and decision-support engine on FHIR | Apache-2.0 | Write "weight up 2 kg in 3 days" as CQL or PlanDefinition |

FHIR mapping when we move the diary into IRIS: BP panel LOINC 85354-9 (systolic 8480-6, diastolic 8462-4) and heart rate 8867-4 are verified at https://hl7.org/fhir/R4/bp.html and https://hl7.org/fhir/R4/heartrate.html. Body weight 29463-7 is the standard code but its LOINC page returned 403, so confirm it. A red zone maps to a `Flag` plus a `Communication` to the nurse; the case log maps to `Task` and `Provenance`.

## Limits

- Diary and cases live in the browser (`localStorage`). They are not yet written to IRIS or FHIR.
- The rules are simple thresholds. They do not use age, medicines, baseline weight or the clinician's signed limits yet.
- PROM and PREM here are two single questions, not validated instruments.
- Not medical advice. Synthetic data.
