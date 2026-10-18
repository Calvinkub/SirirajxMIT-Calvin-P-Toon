# P05 · Eight synthetic patients, each built to push one path through the safety rules, in 9 idempotent FHIR transaction bundles.

## Key message

We generated 9 FHIR R4 transaction bundles (1 shared reference bundle + 8 patients) holding 383 resources of 19 types, every one tagged `data-origin = synthetic`, every entry a `PUT Type/id` so reloading updates instead of duplicating. Each patient is a test case for one rule: a normal low-risk patient, a 71-year-old with a 6-minute-walk limit, a moderate-risk patient, a high-risk ICD patient who is blocked, a post-bypass patient with a restriction, a new user with only a draft limit, a red flag on day 5, and a low-adherence evening exerciser. The data proves the record shape and the rules' paths, not accuracy or clinical value.

## Why this matters to the judges

- **Technical coherence:** a judge can open any bundle and see the safety rules expressed as data (no `CarePlan` for the ineligible patient, a `draft` `CarePlan` with no `Task`s for the new user, `cancelled` `Task`s after the red flag).
- **Use of InterSystems technology:** the bundles follow the kit's FHIR loading pattern (transaction bundle POSTed to `/fhir/r4/`), fixed for idempotency, ready for the IRIS for Health FHIR server and then for FHIR SQL Builder (P06).
- **Honesty:** synthetic data is labelled in the data itself (`meta.tag`), so it cannot be mistaken for evidence later.

## Full detail

### 1. How the bundles are built

`synthetic/generate_fhir.py` (390 lines, seed 42, demo week 2026-10-11 to 2026-10-17, Asia/Bangkok +07:00) builds every resource from a `PROFILES` table, wraps each in an entry with `request.method = PUT` and `request.url = Type/id`, and runs `Bundle.model_validate(b)` with `fhir.resources` R4B models before writing ("raises on invalid FHIR"). The kit uses the same library. Two kit lessons are built in:

- **Idempotency.** The kit's FHIR skill warns: "POSTing the same bundle twice creates duplicates." The kit's own setup re-POSTs Synthea bundles on restart and duplicates patients. Our entries use `PUT` with stable ids (`cmc-p01-limits`, `cmc-p01-task-1`…), which the kit's tutorial 3.4 describes as "insert new or replace existing".
- **Attachments.** FHIR `attachment.data` is base64; the kit's 3.1 notebook encodes notes as hex, "which the server accepts but does not match the spec". Our discharge notes are base64 UTF-8.

A transaction is all-or-nothing: kit tutorial 3.4 says resources in a transaction "are processed together, meaning if one of the resources errors, the rest of the bundle is not saved". That is what we want for a patient: either the whole record loads or none of it.

`synthetic/load_to_iris.py` (28 lines) POSTs the shared bundle first (patient bundles reference its practitioners, model device, questionnaire, places and services), then each patient bundle, to `http://localhost:52773/fhir/r4/` with the kit's local demo credentials, prints any `OperationOutcome` issue and stops on the first error.

### 2. The eight patients and what each one tests

| Id | Synthetic person | Case | Rule exercised | Expected system behaviour | What the bundle contains |
|---|---|---|---|---|---|
| cmc-p01 | Somchai K., male, b. 1964, Bang Rak | Low risk after MI, LVEF 55%, CPET limit, bisoprolol | Normal path; beta-blocker → RPE paired with HR | Daily missions | Active CarePlan (HR ≤ 110, RPE 11–13, walking + stationary cycling), 7 Tasks all completed, 7 symptom checks |
| cmc-p02 | Malee S., female, b. 1955 (71), Phra Nakhon | Low risk, no CPET, limit from 6-minute walk | Non-CPET limit source | Simpler missions, caregiver help | HR ≤ 100, RPE 11–12, walking only; 4 of 7 completed |
| cmc-p03 | Anan T., male, b. 1968, Chatuchak | Moderate risk, LVEF 42%, exercise-ECG limit | Risk-class gate | Supervised sessions before app-only | HR ≤ 105, walking only; 5 of 7 completed |
| cmc-p04 | Prasert W., male, b. 1959, Thon Buri | High risk, LVEF 30%, ICD, heart failure | Eligibility gate (spec rule 7) | **Blocked**; referred | `Flag` `app-ineligible`; no Goal, CarePlan, Task or Provenance |
| cmc-p05 | Wanida C., female, b. 1962, Huai Khwang | 6 weeks after CABG, LVEF 50% | Restriction text | Walking only | `restriction` "No upper-body resistance until 12 weeks after CABG"; 6 of 7 completed |
| cmc-p06 | Kittisak B., male, b. 1971, Bang Kapi | New sign-up, risk unknown, no LVEF | Signed-limit gate (spec rule 6) | **No exercise missions** | `CarePlan` status `draft` without limit extensions; no Tasks |
| cmc-p07 | Siriporn J., female, b. 1966, Lat Phrao | Low risk, chest tightness on day 5 | Red-flag stop (spec rule 3, 8) | Stop, flag to clinician, pause | Symptom check with chest-pain = yes; `Flag` `red-flag-chest-symptom` + `Communication`; Task 5 failed, Tasks 6–7 cancelled |
| cmc-p08 | Abdul R., male, b. 1960, Min Buri | MI, HTN, T2DM, AF; low adherence; fasting days | Missed missions, evening schedule | 19:00 missions, many missed | All 7 Tasks at 19:00; 1 completed, 6 requested |

### 3. What every patient bundle holds

Patient (Thai preferred language, district, district-centroid extension) · Condition (1–4, SNOMED CT) · MedicationStatement (4–5, ATC; all 8 patients on a beta-blocker) · DocumentReference (synthetic discharge note, LOINC 18842-5, base64) · Device (watch) · Observation × 17–18 (LVEF where known, risk class, 7 daily resting HR, 7 daily step counts, 2 BP panels) · Consent (insurer access denied) · and, where the rules allow, Goal + CarePlan + attester Provenance, 7 Tasks + 7 assembler Provenances, and one QuestionnaireResponse per finished or failed mission.

### 4. The data in numbers

Totals: 383 resources (shared 20, patients 28–52 each). The shared bundle holds 1 Organization ("Demo Cardiac Rehab Clinic (synthetic)"), 2 Practitioners (a cardiologist and a rehab physiotherapist), 1 AI-model Device, 1 symptom-check Questionnaire, 8 Locations and 7 HealthcareServices (P08). File sizes range from 27 KB (shared) to 83 KB (p01).

### 5. What the data does not do

It does not simulate physiology: resting HR (63–76 bpm means) and steps (633–4,587 a day means) are drawn around a per-patient target with a fixed seed. It does not contain any model output: the mission `Provenance` names the MedGemma device, but no model ran. It is not Synthea: Synthea would give population realism but not the precise edge cases the safety rules need. A Synthea background population plus our eight edge cases is the right next step for SQL Builder testing at scale.

### 6. Consistency fixes already made and still open

- Fixed: cmc-p07 was first generated with LVEF 48% and risk class "low", inconsistent with the low-risk band (LVEF ≥ 50%); now LVEF 53% (A03).
- Resolved (2026-10-18): the demo patient is now bundle `cmc-p01` (Somchai, 58, Bang Na, high blood pressure and an MI this year, HR < 110, ≤ 5.9 METs); `cmc-p01` was removed. See README "Changes after the pages were written".
- Open: `allowed-activity` codes are only `walking` and `stationary-cycling`; the demo catalogue's 100 activities are not yet represented as codes in any `CarePlan`.

## Visualizations

### Chart 1 · Stacked bar: resources per bundle by type group

- **Type:** stacked vertical bar, one bar per bundle.
- **Title:** "Blocked paths are visibly shorter: no plan, no missions"
- **Axis:** number of resources.

| Bundle | Observation | Task | Provenance | QuestionnaireResponse | MedicationStatement | Condition | Plan (Goal + CarePlan) | Flag + Communication | Other (Patient, Device, DocRef, Consent; shared: Org, Practitioner, Device, Questionnaire, Location, HealthcareService) | Total |
|---|---|---|---|---|---|---|---|---|---|---|
| shared | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 20 | 20 |
| p01 | 18 | 7 | 8 | 7 | 4 | 2 | 2 | 0 | 4 | 52 |
| p02 | 18 | 7 | 8 | 4 | 5 | 2 | 2 | 0 | 4 | 50 |
| p03 | 18 | 7 | 8 | 5 | 5 | 2 | 2 | 0 | 4 | 51 |
| p04 | 18 | 0 | 0 | 0 | 4 | 2 | 0 | 1 | 4 | 29 |
| p05 | 18 | 7 | 8 | 6 | 4 | 3 | 2 | 0 | 4 | 52 |
| p06 | 17 | 0 | 0 | 0 | 4 | 1 | 2 | 0 | 4 | 28 |
| p07 | 18 | 7 | 8 | 4 | 5 | 2 | 2 | 2 | 4 | 52 |
| p08 | 18 | 7 | 8 | 1 | 5 | 4 | 2 | 0 | 4 | 49 |
| **Total** | 143 | 42 | 48 | 27 | 36 | 18 | 14 | 3 | 52 | **383** |

Annotation on p04 and p06: "Rules block: no Tasks written." **Notice:** the shape of the data is the safety logic: the two patients who must not exercise have no missions, and the red-flag patient carries the only `Communication`.

### Chart 2 · Stacked bar: mission status by patient (the week of 2026-10-11)

- **Title:** "What the clinician would see after one week"
- **Axis:** Tasks (of 7).

| Patient | Completed | Requested (not done) | Failed | Cancelled | Generator adherence setting |
|---|---|---|---|---|---|
| p01 | 7 | 0 | 0 | 0 | 0.85 |
| p02 | 4 | 3 | 0 | 0 | 0.60 |
| p03 | 5 | 2 | 0 | 0 | 0.75 |
| p05 | 6 | 1 | 0 | 0 | 0.80 |
| p07 | 3 | 1 | 1 | 2 | 0.70 (red flag day 5) |
| p08 | 1 | 6 | 0 | 0 | 0.45 |
| p04, p06 | — | — | — | — | blocked |

**Notice:** p07 shows the stop path in data: the failed day-5 mission is followed by two cancellations, not by more coaching. Adherence settings are generator parameters, not measurements.

### Chart 3 · Dot plot: week means of the watch data per patient (synthetic)

| Patient | Mean resting HR (bpm) | Mean steps/day | BP panels (mmHg) | Symptom-check RPE values |
|---|---|---|---|---|
| p01 | 63.0 | 4,587 | 140/82, 140/80 | 12, 12, 12, 11, 11, 12, 13 |
| p02 | 69.0 | 2,680 | 129/77, 124/82 | 12, 11, 11, 11 |
| p03 | 72.7 | 3,403 | 131/81, 120/78 | 11, 11, 12, 11, 11 |
| p04 | 75.7 | 633 | 137/78, 124/86 | — |
| p05 | 68.7 | 4,110 | 140/82, 119/75 | 12, 13, 12, 13, 12, 13 |
| p06 | 65.7 | 2,148 | 133/79, 124/85 | — |
| p07 | 69.0 | 3,783 | 136/83, 135/72 | 12, 11, 11, 13 |
| p08 | 72.4 | 2,330 | 122/86, 129/86 | 12 |

**Notice:** every recorded RPE is inside 11–13, the range the limit records allow; out-of-range RPE is a test case we have not generated yet.

### Diagram · Eight paths through the gates

A decision tree: Eligibility gate → (high risk: p04 blocked) → Signed-limit gate → (draft: p06 no missions) → Risk class → (moderate: p03 supervised first) → Daily missions (p01, p02, p05 with restriction, p08 evening) → Symptom check → (chest pain: p07 stop, flag, cancel).

## Numbers and claims ledger

| Claim | Value | Source | Status |
|---|---|---|---|
| Bundles, all `transaction`, all `PUT` | 9 | counted from `synthetic/fhir/*.json` | checked |
| Resources / types | 383 / 19 | counted | checked, synthetic |
| Per-bundle totals | 20, 52, 50, 51, 29, 52, 28, 52, 49 | counted | checked |
| Task status per patient | as Chart 2 | counted | checked, synthetic |
| HR / steps / BP / RPE | as Chart 3 | computed from bundles | checked, synthetic |
| Validation | `Bundle.model_validate` (R4B) | `synthetic/generate_fhir.py` line 376 | checked (code); re-run not done here |
| "POSTing the same bundle twice creates duplicates" | quote | `FHIR-AI-Hackathon-Kit/skills/iris-fhir/SKILL.md` | checked |
| Transaction all-or-nothing | quote | kit tutorial 3.4 | checked |
| File sizes | 27–83 KB | `ls -l` | checked |
| Loaded into a live IRIS (HTTP 200 per bundle) | — | `synthetic/load_to_iris.py` exists | to verify (not run) |

## Limits and open questions

- Not yet loaded into a running IRIS for Health server. IRIS validates more strictly than `fhir.resources` (kit note), especially references and unknown extensions.
- No out-of-range cases yet: HR above the ceiling during a mission, RPE above 13, expired `CarePlan`, implausible watch readings, missing watch days, consent withdrawn.
- Eight patients cannot test SQL Builder performance or population analytics; add a Synthea background.
- `AuditEvent` not generated.
- The demo's Somchai and the bundle's Somchai differ (see 6).

## Likely judge questions

1. **"Is this real patient data?"** No. Every resource carries the `synthetic` tag; names, places and clinic are invented.
2. **"Why not Synthea?"** Synthea gives realistic populations but not the exact edge cases our rules must handle (draft limits, ICD exclusion, red flag on day 5). We will add Synthea as background.
3. **"What happens if you load twice?"** Nothing new: every entry is `PUT Type/id`, so IRIS updates the same resources.
4. **"Did IRIS accept your extensions?"** Not tested yet; it is the first thing the loader will tell us, and the fallback is to publish `StructureDefinition`s.
5. **"What does p07 show?"** That after a chest-pain tap the record contains a `Flag`, a `Communication` to the clinician and cancelled missions: the stop path is visible to an auditor.

## Sources

Repo:
- `synthetic/generate_fhir.py`, `synthetic/load_to_iris.py`, `synthetic/README.md`, `synthetic/profiles.json`
- `synthetic/fhir/00_shared_reference_data.json`, `synthetic/fhir/p01…p08_*.json` (all counts computed with python3 on 2026-10-18)
- `pitch/appendix/A03-fhir-data-model.md`, `pitch/appendix-deck/P04-synthetic-fhir-bundles.md`
- `FHIR-AI-Hackathon-Kit/skills/iris-fhir/SKILL.md`, `skills/iris-environment/SKILL.md`, `Tutorials/3-fhir/markdown/3.1-load-fhir-data.md`, `3.3-create-fhir-resources.md`, `3.4-create-transaction-bundles.md`
- `demo/agent-flow-demo.html` (`LIMIT`, patient `cmc-p01`)

External (opened 2026-10-18):
- HL7 FHIR R4 Task (status, basedOn): https://hl7.org/fhir/R4/task.html

## Image-generation prompt

Design one 16:9 information slide on a white background. Lead with the key message as the title: "Eight synthetic patients, each built to push one path through the safety rules." Make the main chart a stacked bar "Resources per bundle" with exactly these totals: shared 20, p01 52, p02 50, p03 51, p04 29, p05 52, p06 28, p07 52, p08 49, highlighting p04 and p06 as "blocked: no missions". Next to it, a compact eight-row list pairing each patient with the rule it tests (normal, 6-minute-walk limit, moderate risk, blocked ICD, post-bypass restriction, draft limit, red flag day 5, low adherence evenings), and the badge "383 resources · 9 PUT transaction bundles · SYNTHETIC". No logos, no invented numbers; choose the design freely.
