# P04 · Every fact is a standard FHIR R4 resource, including the clinician's signature on the limits and the AI's own provenance.

## Key message

Heartstep's whole state fits 19 standard FHIR R4 resource types: who the patient is, what the clinician allowed, what the watch measured, what the AI scheduled, what the patient felt and who may see it. The limit record is a `Goal` + `CarePlan` signed through a `Provenance` with agent type `attester`; every AI-chosen mission is a `Task` based on that `CarePlan` with its own `Provenance` (agent type `assembler`), so an auditor can read what the model chose without trusting the model. All 8 LOINC, 6 SNOMED CT and 9 ATC codes in the synthetic data resolve to the intended concepts in the official terminology services (checked 2026-10-18); 10 custom extensions still need published profiles.

## Why this matters to the judges

- **Use of InterSystems technology:** IRIS for Health's FHIR server is the system of record. A data model built from standard resources is what lets FHIR SQL Builder, FHIR search and Vector Search work on the same data (P06–P08).
- **Technical coherence:** each design rule from P03 ("only clinicians write limits", "the model picks from an allowed set", "red flags go to a human") is visible as a resource, a reference or an agent type, not as a comment in code.
- **Real-world impact:** a hospital can receive a patient's plan, adherence and red-flag events as FHIR without a custom integration.

## Full detail

### 1. The map in five groups

| Group | Resources | Role in Heartstep |
|---|---|---|
| Who | `Patient`, `Practitioner`, `Organization`, `Device` | Patient (Thai as preferred language, district only, no street); the signing clinician; the clinic; the watch and the AI model as devices |
| Clinical facts | `Condition`, `MedicationStatement`, `Observation`, `DocumentReference` | Diagnoses (SNOMED CT), medicines (ATC, beta-blocker flag), HR, steps, BP, LVEF, risk class, discharge note |
| Limit record | `Goal`, `CarePlan`, `Provenance` (attester) | What the clinician allows, until when, and who signed |
| Daily loop | `Task`, `Provenance` (assembler), `Questionnaire`, `QuestionnaireResponse`, `Flag`, `Communication` | Each mission, who chose it, symptom taps, red flags to the care team |
| Places and consent | `Location`, `HealthcareService`, `Consent` | Parks, temples, malls, rehab gym; groups and classes; who may see the data |

### 2. The limit record, element by element

The `CarePlan` (`status = active` when signed, `draft` while waiting; `intent = plan`; `period.end` = review-by date; `author` = the clinician) carries five custom extensions under `https://cvd-mission-coach.example/fhir/StructureDefinition/`:

| Extension | FHIR type | Example (cmc-p01) | Used by |
|---|---|---|---|
| `hr-ceiling` | Quantity, UCUM `/min` | 110 /min | Mission engine, watch check |
| `rpe-target` | Range | 11–13 (Borg 6–20) | Mission text, symptom check |
| `limit-source` | code | `cpet` (others: `6mwt`, `exercise-ecg`) | Clinician summary, audit |
| `allowed-activity` | code, repeating | `walking`, `stationary-cycling` | Catalogue filter |
| `restriction` | string | p05: "No upper-body resistance until 12 weeks after CABG" | Catalogue filter, mission text |

A separate `Provenance` targets the `CarePlan` with agent type `attester` and `who` = `Practitioner/pr-cardio-1`. HL7 defines attester as "An agent (verifier) who attests to the accuracy of the entity". Spec rule 6 is then a data rule: no `active` `CarePlan` inside its period with an attester `Provenance` means no exercise mission.

Why not `Goal` alone or `CarePlan.activity`? `Goal` expresses a desired state ("an expressed desired health state to be achieved", HL7 R4); the limit is a constraint on the plan, so it sits on the `CarePlan`. HL7 R4 describes `CarePlan` as "one of the request resources in the FHIR workflow specification", which is what lets each `Task` point at it with `basedOn`.

### 3. The daily loop and the AI's accountability

Each mission is a `Task` with `intent = plan`, `basedOn` → the limit `CarePlan`, `code` = mission id (`walk-10-easy`, `walk-12-easy`, `cycle-10-easy`, `rest-day`), `executionPeriod` = the patient's chosen time, and a lifecycle `status` (requested, completed, failed, cancelled). HL7 R4: a Task "describes an activity that can be performed and tracks the state of completion of that activity", and `basedOn` "refers to a higher-level authorization that triggered the creation of the task … such as a … CarePlan".

Each `Task` has its own `Provenance`: agent type `assembler`, `who` = `Device/dev-medgemma` ("MedGemma 27B mission picker (demo config)"), reason `picked-from-allowed-set`. HL7 defines assembler as "A device that operates independently of an author using algorithms for data extraction of existing information for purpose of generating a new entity." That is an accurate description of what the model is allowed to do: assemble a mission from an allowed set, not author a prescription. In production the `Provenance` will also record the model version and the allowed set.

After each mission the patient answers a fixed `Questionnaire` (`symptom-check|1.0`: chest pain, breathless, dizzy, palpitations as booleans; RPE as integer). The `QuestionnaireResponse` points to its `Task` through the extension `about-task`. Any "yes" becomes a `Flag` (category `clinical`, local code `red-flag-chest-symptom`) and a `Communication` to the clinician (`about` → the `Flag`), and remaining `Task`s become `cancelled` (patient cmc-p07).

Ineligible patients get a different `Flag` (`app-ineligible`, authored by the clinician) and no `CarePlan` at all (cmc-p04, LVEF 30%, ICD).

### 4. Codes, checked against the terminology services

| System | Code | Our meaning | Official display (looked up 2026-10-18) |
|---|---|---|---|
| LOINC | 8867-4 | Resting heart rate (daily, 06:30) | Heart rate |
| LOINC | 41950-7 | Steps per day | Number of steps in 24 hour Measured |
| LOINC | 85354-9 | BP panel | Blood pressure panel with all children optional |
| LOINC | 8480-6 / 8462-4 | Systolic / diastolic | Systolic blood pressure / Diastolic blood pressure |
| LOINC | 10230-1 | LVEF | Left ventricular Ejection fraction |
| LOINC | 18842-5 | Discharge note | Discharge Summary |
| LOINC | 59284-0 | Consent category | **Consent Document** (our generator writes the display "Patient Consent": fix) |
| SNOMED CT | 22298006 | MI | Myocardial infarction |
| SNOMED CT | 38341003 | Hypertension | Hypertensive disorder |
| SNOMED CT | 44054006 | T2DM | Type 2 diabetes mellitus |
| SNOMED CT | 49436004 | AF | Atrial fibrillation |
| SNOMED CT | 84114007 | Heart failure | Heart failure |
| SNOMED CT | 232717009 | "CABG (history)" | Coronary artery bypass graft (a **procedure** concept used in a `Condition`: a clinician-informatician should choose between a `Procedure` resource or a history/situation concept) |
| ATC | C07AB07, C07AB02 | Beta-blockers | bisoprolol, metoprolol |
| ATC | B01AC06, B01AC04, B01AC24 | Antiplatelets | acetylsalicylic acid, clopidogrel, ticagrelor |
| ATC | C10AA05, C09AA05, A10BA02, C01DA02 | Statin, ACE inhibitor, metformin, nitrate | atorvastatin, ramipril, metformin, glyceryl trinitrate |

Consent: `scope` = `patient-privacy`, `policyRule` = `OPTIN`, provision `permit` for purpose `TREAT` ("To perform one or more operations on information for provision of health care", HL7 v3 ActReason), with a nested `deny` for actor role `PAYOR`. HL7 v3 RoleClass defines `PAYOR` as "invoice payor": "an organization that undertakes to accept claims invoices, assess the coverage or payments due … and pay". An insurer that underwrites rather than pays claims fits `UNDWRT` (underwriter); denying both is safer (open item).

### 5. Design choices and the alternatives

| Choice | Chosen | Alternative | Reason |
|---|---|---|---|
| Mission | `Task` | `CarePlan.activity` | Each mission needs its own status, time and `Provenance` |
| Red flag | `Flag` + `Communication` | `DetectedIssue` | HL7: `DetectedIssue` is for "Potential allergy or drug interaction to planned therapy"; a `Flag` is "a warning or notification … presented to the user"; the `Communication` gets it to a named clinician |
| AI accountability | `Provenance` per `Task` | `AuditEvent` only | `Provenance` is attached to the record and travels with it; `AuditEvent` (planned) logs every tool call |
| Home | `Patient.address.district` + district centroid extension | Full address | PDPA data minimisation (P08) |
| Loading | `PUT Type/id` in transaction bundles | `POST` | The kit warns "POSTing the same bundle twice creates duplicates"; PUT is idempotent (P05) |

HL7 maturity, as shown on the R4 pages we opened: `Task` maturity 2 and `Flag` maturity 1, both Trial Use. These resources may change in later FHIR versions; the map would need a migration plan for R5/R6.

### 6. Worked example: what an auditor sees for Somchai's first mission

`Task/cmc-p01-task-1`: completed, 2026-10-11 18:00–18:30, "10-minute easy walk, warm-up and cool-down included", `basedOn` `CarePlan/cmc-p01-limits`. `Provenance/cmc-p01-task-1-prov`: assembler `Device/dev-medgemma`, reason "Mission id chosen from the rules engine's allowed set". `QuestionnaireResponse/cmc-p01-task-1-check`: no chest pain, no breathlessness, no dizziness, no palpitations, RPE 12. `CarePlan/cmc-p01-limits`: HR ≤ 110, RPE 11–13, CPET, walking + stationary cycling, signed by `Practitioner/pr-cardio-1`, valid 2026-10-04 to 2026-11-29. Four resources answer "what did the AI do, under whose authority, and how did the patient feel?" (Synthetic.)

## Visualizations

### Chart 1 · Bar: synthetic resources by FHIR type (all 9 bundles)

- **Type:** horizontal bar, sorted, coloured by group.
- **Title:** "383 synthetic resources across 19 FHIR R4 types"
- **Axis:** number of resources.

| Resource type | Count | Group |
|---|---|---|
| Observation | 143 | Clinical facts |
| Provenance | 48 | Limit record + daily loop |
| Task | 42 | Daily loop |
| MedicationStatement | 36 | Clinical facts |
| QuestionnaireResponse | 27 | Daily loop |
| Condition | 18 | Clinical facts |
| Device | 9 | Who |
| Patient | 8 | Who |
| DocumentReference | 8 | Clinical facts |
| Consent | 8 | Places and consent |
| Location | 8 | Places and consent |
| Goal | 7 | Limit record |
| CarePlan | 7 | Limit record |
| HealthcareService | 7 | Places and consent |
| Practitioner | 2 | Who |
| Flag | 2 | Daily loop |
| Organization | 1 | Who |
| Questionnaire | 1 | Daily loop |
| Communication | 1 | Daily loop |
| **Total** | **383** | |

**Notice:** 48 `Provenance` = 6 signed limit records + 42 mission records: every AI decision in the data has a provenance record. Observations dominate because each patient has 7 days of HR and steps. Source: counted with python3 from `synthetic/fhir/*.json` on 2026-10-18.

### Chart 2 · Bar: custom extension instances in the synthetic data

| Extension | Instances | On resource |
|---|---|---|
| `about-task` | 27 | QuestionnaireResponse |
| `indoor` | 8 | Location |
| `home-district-position` | 8 | Patient |
| `beta-blocker` | 8 | MedicationStatement |
| `allowed-activity` | 8 | CarePlan (repeating) |
| `activity-intensity` | 7 | HealthcareService |
| `hr-ceiling` | 6 | CarePlan |
| `rpe-target` | 6 | CarePlan |
| `limit-source` | 6 | CarePlan |
| `restriction` | 1 | CarePlan |

**Notice:** 10 extensions, all unprofiled; five sit on the limit record, which makes "will IRIS accept and project them?" the top technical risk (P06). The draft `CarePlan` (cmc-p06) has none of the limit extensions, so 6 of 7 CarePlans carry `hr-ceiling`.

### Diagram · Resource graph

Patient at the centre. Condition, MedicationStatement, DocumentReference, Observation, Consent → Patient. Observation → Device (watch). CarePlan → Patient, Goal, author Practitioner; Provenance (attester) → CarePlan, who Practitioner. Task basedOn → CarePlan; Provenance (assembler) → Task, who Device (AI model). QuestionnaireResponse about-task → Task. Flag → Patient; Communication about → Flag, recipient → Practitioner. HealthcareService → Location. Highlight the limit record (Goal + CarePlan + attester Provenance) with a border.

## Numbers and claims ledger

| Claim | Value | Source | Status |
|---|---|---|---|
| Resource types / resources | 19 / 383 | `synthetic/fhir/*.json` | checked, synthetic |
| Provenance = 6 limit + 42 mission | 48 | counted (6 active CarePlans, 42 Tasks) | checked |
| Extension instances | as table | counted | checked |
| LOINC displays | as table | NLM Clinical Tables LOINC API | checked |
| SNOMED CT displays | as table | tx.fhir.org `$lookup` (SNOMED International 2025-02-01) | checked |
| ATC names | as table | WHOCC ATC/DDD index | checked |
| 59284-0 display mismatch | "Consent Document" vs "Patient Consent" | NLM API vs `generate_fhir.py` | checked, fix needed |
| PAYOR definition | "invoice payor" | HL7 v3 RoleClass JSON | checked |
| Attester / assembler definitions | quoted | HL7 provenance-participant-type JSON | checked |
| Task / Flag definitions and maturity | quoted; FMM 2 and 1, Trial Use | hl7.org/fhir/R4 task.html, flag.html | checked |
| IRIS accepts unprofiled extensions | — | — | to verify (live load) |

## Limits and open questions

- Extensions use a placeholder domain (`cvd-mission-coach.example`) and have no `StructureDefinition`s; a real deployment needs published profiles, ideally aligned with a Thai Core IG if one applies.
- `Condition` with a procedure code for CABG history should be remodelled with a clinician.
- `AuditEvent` is designed but not generated.
- Risk class is a local code (`aacvpr-risk-class`); there may be a better standard representation.
- `Flag` is maturity 1 (Trial Use); `DetectedIssue` or a `Communication`-only design may be preferred by the hospital.
- In the synthetic data the mission `Provenance` names MedGemma, but no model ran; the generator writes the shape of the record.

## Likely judge questions

1. **"Why FHIR at all?"** Because the outputs (plans, flags, provenance) must be readable by the hospital and auditable without our app, and IRIS for Health stores and projects FHIR natively.
2. **"Where is the clinician's signature?"** A `Provenance` targeting the `CarePlan` with agent type `attester` and `who` = the `Practitioner`. No attested, unexpired `CarePlan`, no exercise mission.
3. **"How do you know what the AI did?"** Every `Task` has a `Provenance` with agent type `assembler` pointing at the model `Device` and the reason "picked-from-allowed-set".
4. **"Are your codes real?"** All 23 codes resolve in the official LOINC, SNOMED CT and ATC services; one display string and one modelling choice (CABG history) need fixing.
5. **"Why `Task` and not `CarePlan.activity`?"** Each mission needs its own status, time window and provenance; `Task` gives all three and links back with `basedOn`.

## Sources

Repo:
- `synthetic/generate_fhir.py`, `synthetic/fhir/00_shared_reference_data.json`, `synthetic/fhir/p01…p08_*.json`, `synthetic/README.md`
- `pitch/appendix/A03-fhir-data-model.md`, `pitch/appendix-deck/P03-fhir-resource-map.md`
- `FHIR-AI-Hackathon-Kit/skills/iris-fhir/SKILL.md`
- `docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md` §5

External (opened 2026-10-18):
- HL7 FHIR R4 Task: https://hl7.org/fhir/R4/task.html
- HL7 FHIR R4 Flag: https://hl7.org/fhir/R4/flag.html
- HL7 FHIR R4 CarePlan, Goal, Provenance, Consent, QuestionnaireResponse, Communication: https://hl7.org/fhir/R4/careplan.html, https://hl7.org/fhir/R4/goal.html, https://hl7.org/fhir/R4/provenance.html, https://hl7.org/fhir/R4/consent.html, https://hl7.org/fhir/R4/questionnaireresponse.html, https://hl7.org/fhir/R4/communication.html
- HL7 terminology, provenance participant type: https://terminology.hl7.org/CodeSystem-provenance-participant-type.json
- HL7 terminology, v3 RoleClass and ActReason: https://terminology.hl7.org/CodeSystem-v3-RoleClass.json, https://terminology.hl7.org/CodeSystem-v3-ActReason.json
- NLM Clinical Tables LOINC API (e.g. https://clinicaltables.nlm.nih.gov/api/loinc_items/v3/search?terms=8867-4&sf=LOINC_NUM&df=LOINC_NUM,LONG_COMMON_NAME)
- HL7 terminology server SNOMED lookup (e.g. https://tx.fhir.org/r4/CodeSystem/$lookup?system=http://snomed.info/sct&code=22298006)
- WHOCC ATC/DDD index (e.g. https://atcddd.fhi.no/atc_ddd_index/?code=C07AB07)

## Image-generation prompt

Design one 16:9 information slide on a white background. Lead with the key message as the title: "Every fact is a standard FHIR R4 resource, including the clinician's signature and the AI's own provenance." Make the main visual a resource map in five groups (Who; Clinical facts; Limit record; Daily loop; Places and consent) with the limit record (Goal + CarePlan + Provenance "attester = clinician") outlined, and the daily loop showing Task → Provenance "assembler = AI model". Add a sorted bar chart "383 synthetic resources across 19 FHIR types" using exactly the counts Observation 143, Provenance 48, Task 42, MedicationStatement 36, QuestionnaireResponse 27, Condition 18, others 69, and a small note "23 codes checked against LOINC, SNOMED CT and ATC". Label the data synthetic. No logos, no invented numbers; choose the design freely.
