# s1-cardiologist review — document — 2026-10-17

> Simulated review by a language-model role-play. Not a real clinician or institution.

**Artifacts read:** `docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md`, `docs/pitch-script-draft1.md`, `HANDOFF.md`, `research/README.md`, `research/pitch-claims-check.md`, `research/guidelines/app-parameters-qa.md`. Targeted reads of `research/guidelines/notebooklm-deep-report.md` (lines 49, 131-154) and `research/market/notebooklm-deep-report.md` (lines 9-23, 57-64, 109).
**Gate result (my view):** FAIL (G4 FAIL, plus an S0 open; G1, G3, G5, G6 NOT-DEFINED). Paths are cited as `spec` = design doc, `script` = pitch script, `qa` = app-parameters-qa.

## Safety gates
| Gate | Status | Evidence |
|---|---|---|
| G1 Limits | NOT-DEFINED | The principle is stated (`spec:71`, `spec:74`). Enforcement is not. Limit source in the demo is open (`spec:111`). The free tier gives a schedule with no clinician limits (`script:27`, `spec:108`). The weekly check-in lets the patient choose "try 12?" with no clinician cap on duration or progression (`spec:101`). The stored limit fields are only HR, RPE and activity type (`spec:71`). |
| G2 Red flags | PASS at design level (with S1 F4) | Hard-coded, no LLM, "Stop now and call 1669" (`spec:73`, `spec:93`, `HANDOFF.md:35`). The trigger input is undefined. Symptoms arrive through a free-text LLM chat (`spec:16`, `spec:48`, `script:15` "daily symptoms"). |
| G3 Eligibility | NOT-DEFINED | The risk-class gate exists only in the research notes (`research/README.md:18`). The design target user includes heart failure and high-risk hypertension (`spec:46`). No exclusions are listed for ICD, LVEF, unstable angina, recent CABG or valve disease. No intake procedure. |
| G4 Claims | FAIL | The script is still unamended: "proven tool to reduce readmission" (`script:25`), "optimal, exact plan ... with ease" (`script:17`), "vital to your survival" (`script:5`), "80% / 15%" (`script:7`). `research/pitch-claims-check.md:5-9` and `spec:35-38` flag these, but the script was not changed. The market report still says "Proven" (`research/market/notebooklm-deep-report.md:63`). |
| G5 Accountability | NOT-DEFINED | "Clinician" is generic. There is no named owner, no consent design, and the B2C path has no clinician at all. Siriraj mentor sign-off is requested but not recorded (`spec:69`, `qa:1`). |
| G6 Failure mode | NOT-DEFINED | No behaviour for missing watch HR, no network, or LLM down. No "no new intensity" default. `spec:97` covers only agent-vs-rules split. |

## Scores (Track A: design and system)
| Dimension | Score | One-line reason |
|---|---|---|
| Clinical validity | 2 | Right skeleton (limits from clinician, RPE with HR, hard-coded stop). Beta-blocker K=0.8 (`qa:40`) and the %HRR range up to 80% (`qa:21`) are unsafe to load as-is. Drug list is incomplete. |
| Patient safety | 1 | No hazard analysis. Free-tier path with no limits. Real-time HR ceiling unenforceable. Heat not considered. |
| Evidence and sourcing | 2 | Research is cited, but machine-generated and self-flagged as unverified (`research/README.md:4`). Doc-to-doc numbers disagree (81/11 vs 93/15). |
| Feasibility | 2 | Buildable stack. Eligibility and limit-entry flows undefined. |
| Regulatory and privacy | 1 | SaMD risk named (`spec:75`). No classification, consent, or data-flow design. (Defer detail to S4.) |
| Behavior and adherence | 1 | Peer community and brainless missions asserted with no test plan. (Defer to M2.) |
| Agent safety and evaluation | 1 | Architecture split is good. No scenario suite or adversarial tests. (Defer to M1.) |
| **Track A average** | **1.43** | Not ready. |

## Scores (Track B: pitch script)
| Dimension | Score | One-line reason |
|---|---|---|
| Problem clarity | 2 | Clear patient moment. The only number is mis-sourced (Italian GPs, not Thai cardiologists) and "5-minute consult" is unsourced. |
| Solution credibility | 1 | "Optimal, exact, with ease", "complex health conditions". It promises a prescription while the design cannot gate who is eligible. |
| Evidence | 1 | Headline stat wrong. "Proven" readmission claim has no data from this product. |
| Market and business | 2 | Payer and price named. Insurer willingness and 499 THB are unvalidated (`pitch-claims-check.md:10-11`). |
| Differentiation | 1 | Movn, Cardihab and the EAPC EXPERT tool are not mentioned in the script. LINE programmes absent. |
| Team and feasibility | 1 | No code, no clinical partner named, no demo path (`HANDOFF.md:11`). |
| Impact and ethics | 1 | No safety, equity, or data handling statement in the pitch. |
| **Track B average** | **1.29** | Not ready. |

**Combined average:** 1.36 (0-1.4 band, not ready).

## Findings (most severe first)

### F1 [S0] The free "1-week schedule" is the no-limits population
- **What is wrong:** The B2C funnel gives every new user a free week of exercise missions, but the design requires limits to come from a clinician (or a test) and says Premium users are the ones with ongoing tracking. Freemium users mostly have no CPET or stress test (`spec:40`, `spec:108`).
- **Evidence:** `script:27`, `spec:71`, `spec:74`, `spec:108`, `qa:11-31`.
- **Failure scenario:** A 58-year-old, 12 days post-MI with an EF of 35%, downloads the app, enters "post-MI" and has no limits on file. The agent falls back to "Resting HR + 20-30 bpm" or age-predicted HR. He is given a daily walk in the first week, the highest-risk week after discharge.
- **Fix:** No exercise mission without a clinician-signed limit record (any source tagged "who set it"). With no record, the free week contains only non-exertional content (meds reminder, education, "ask your cardiologist for your limits" with a limit-request form). Put this in the script and the spec.
- **Needs real expert?** Yes (cardiologist, to sign the default no-record behaviour).

### F2 [S1] Eligibility gate is circular and absent from the design
- **What is wrong:** The research's "low risk, app-only" class requires measured capacity of at least 7 METs and a normal exercise ECG (`qa:70-74`). A patient without a stress test cannot be classed low risk, so the no-CPET answer to open question 0 (`spec:108`) quietly puts those users in an unclassifiable group. Spec §3 names heart failure as a target user (`spec:46`), and the Q&A says high risk (LVEF below 35-40%, ICD, complex arrhythmia, depression) is not suitable (`qa:80-94`).
- **Evidence:** `qa:70-94`, `research/README.md:18`, `spec:46`; the design has no gate.
- **Failure scenario:** ICD patient self-reports as "post-MI, no limits", receives HR-ceiling missions based on a rate the ICD shock threshold ignores. ICD therapy threshold vs target HR is not addressed in any artifact. NEEDS REAL EXPERT.
- **Fix:** Add an onboarding hard block list (ICD or pacemaker, EF below 40% or unknown, unstable or recent-onset angina, decompensated HF, uncontrolled arrhythmia incl. AF with fast rate, severe valve disease, CABG or sternotomy under 12 weeks for upper-body missions, SBP above 200 or DBP above 110 at rest per `deep-report:49`, cardiac arrest survivor). Unknown means blocked. Requires a clinician-entered class, not self-report. Reconcile "unsupervised moderate risk" with the supervised-sessions rule (`qa:93`).
- **Needs real expert?** Yes (cardiologist and cardiac rehab physician).

### F3 [S1] The pitch script is unamended and fails G4
- **What is wrong:** The unsafe wording the team's own checks flagged is still verbatim in the script.
- **Evidence:** `script:5,7,17,25`; checks at `pitch-claims-check.md:5-9`; `spec:35-39`.
- **Failure scenario:** A judge asks "proven how?" and the first 60 seconds fall apart; or an insurer reads "proven tool". "Optimal, exact ... with ease" plus "complex health conditions" tells patients with HF or ICD that the app is for them.
- **Fix:** Replace with the spec's own suggested wording (`spec:36-38`). Change "survival" to "recovery". Drop the "80/15" numbers unless the cited source matches: `spec:35` says 81%/11% cardiologists, `pitch-claims-check.md:5` says 93%/15% Italian GPs. These two repo documents conflict; check the primary source (PMC12990137, per `pitch-claims-check.md:5`) before using either. I did not verify the PMC source myself: UNVERIFIED. Drop "5-minute consult" unless a Siriraj figure exists.
- **Needs real expert?** No for wording; yes (Siriraj mentor) for the local consult-time figure.

### F4 [S1] Red-flag path has no deterministic input, and delays care in chat
- **What is wrong:** Detection of symptoms is not defined. The design relies on a hard-coded handler, but the patient reports symptoms in free text to an LLM chat, or taps a mission "Done". The watch cannot detect chest pain. "Daily symptoms" is a stated input (`script:15`).
- **Evidence:** `spec:16`, `spec:73`, `spec:93`, `spec:104`.
- **Failure scenario:** At 02:00 the patient types "แน่นหน้าอกนิดหน่อย" ("slight chest tightness") into the chat. The LLM replies with a reassuring explanation, or asks a follow-up question, instead of "call 1669". The patient waits for the answer. This is the single most likely harm path of a correctly-used app.
- **Fix:** (a) Symptom check-in is a fixed-choice form before every exercise mission, not free text. (b) A deterministic pre-filter on every chat message (Thai and English keywords for chest, breath, faint, palpitation, sweating) runs before the LLM and short-circuits to the stop-and-call message. (c) A persistent footer: "This app is not for emergencies. Chest pain: call 1669." (d) Triage tiers: the research list is all "call emergency" (`qa:49-61`); tiering mild palpitation versus ongoing chest pain is a clinical decision. NEEDS REAL EXPERT. (e) Log every trigger.
- **Needs real expert?** Yes (cardiologist for tiers and wording; Thai-language review).

### F5 [S1] HR ceiling and progression are not enforceable as described
- **What is wrong:** The example mission "stay below 110 bpm" (`spec:53`) needs real-time HR. The bridge is HealthKit / Health Connect (`spec:84`), which batches data. The patient only sees the notification. Nothing says what happens when HR exceeds the ceiling mid-walk. The example 110 bpm is not derived from any limit record: UNSOURCED. The check-in lets the patient pick a longer duration (`spec:101`) with no clinician cap, against rule 4 (`spec:74`).
- **Evidence:** `spec:53`, `spec:84`, `spec:101`, `spec:71`.
- **Failure scenario:** The wrist sensor reads low or lags during an arrhythmia; the patient trusts the "Done" tick and keeps walking.
- **Fix:** Make RPE or talk test the primary in-session control (`spec:72`), with HR as a secondary after-the-fact check. Limit record to include max duration, max sessions per week, max weekly increment and days since event. Progression only within caps (5-10% per week is in `qa:122`, a research figure to be signed off). Drop numeric HR from examples until a limit record exists. Missing or implausible HR means no progression and show RPE only (G6).
- **Needs real expert?** Yes (rehab physician for the caps; S2 will overlap).

### F6 [S1] Drug and environment interactions are incomplete
- **What is wrong:** The design covers only beta-blockers (`spec:72`). The deep report has vasodilator and nitrate cool-down of 10 minutes or more (`deep-report:137`) and anticoagulant fall risk (`deep-report:133`), none of which enters the design or the Q&A. Not addressed anywhere: antiarrhythmics or ivabradine and HR blunting, diuretics and dehydration, diabetes medication and hypoglycaemia, sublingual nitrate carrying, and Thai heat and humidity. The example mission is a walk at 12:30 (`spec:103`), at peak heat.
- **Evidence:** `spec:72`, `spec:103`; `research/guidelines/notebooklm-deep-report.md:131-137`. Heat, diabetes and antiarrhythmic effects: not in the artifacts at all.
- **Failure scenario:** Patient on a nitrate and an ACE inhibitor stops walking abruptly in a hot afternoon market, with a drop in BP, and faints. Or an insulin-treated patient walks fasting.
- **Fix:** Medication intake as structured drug-class checkboxes feeding rules (not free text to the LLM). Mandatory cool-down in every mission. Time-of-day and heat-aware scheduling (early morning or indoor). Carry-your-nitrate prompt where prescribed. NEEDS REAL EXPERT for each rule, particularly diabetes.
- **Needs real expert?** Yes (cardiologist, clinical pharmacist).

### F7 [S1] Research parameters that would go straight into the rules engine need expert correction
- **What is wrong:** `qa:40` says to raise the Karvonen K from 0.6 to 0.8 for beta-blocked patients. Read literally, that raises the target rate for the group with the least reliable HR. I cannot confirm this from the GERS-P source and I suspect a misreading by the model. `qa:21` offers 40-80% HRR, which is too high for unsupervised early post-MI. `qa:43` makes RPE and talk test primary, which I agree with. BP-based stop criteria (`qa:56-57`) need a cuff the app does not assume.
- **Evidence:** `qa:21`, `qa:40`, `qa:56-57`; `qa:1` (self-flagged: confirm before use).
- **Failure scenario:** A developer implements `qa:40` as written and a beta-blocked patient is told to walk at a higher HR.
- **Fix:** Do not implement any `qa:` number until a clinician signs it. Cap initial unsupervised intensity at RPE 11-13 and low-end %HRR (clinician to confirm). Remove the K=0.8 instruction from implementation notes, or have it verified against the primary source.
- **Needs real expert?** Yes (cardiologist, rehab physician).

### F8 [S1] Peer community is a clinical-advice channel nobody owns
- **What is wrong:** The script adds peer communities (`script:17`); the design has nothing on moderation, advice rules or privacy. Support evidence is correlational Thai data (`research/README.md:20`, β = -0.225) and not a trial of peer groups (`pitch-claims-check.md:8`).
- **Evidence:** `script:17`, `pitch-claims-check.md:8`.
- **Failure scenario:** A peer replies "I had that pain too, it was nothing", and the member does not call 1669.
- **Fix:** v1 peer feature limited to shared activity-count goals (no free text), or moderated with a hard "no medical advice, call 1669" rule.
- **Needs real expert?** Yes (S3 and S4 overlap).

### F9 [S1] Accountability and consent are blank for B2C and insurer data
- **What is wrong:** No named clinical owner of limits, no clinician view in v1 (`spec:116`), and no consent for wearable data or insurer visibility. The B2B2C model sends outcome data to insurers (`script:25`).
- **Evidence:** `spec:116`, `script:25`, `HANDOFF.md:35`.
- **Failure scenario:** An adverse event in a B2C user and nobody holds the limit record; or the insurer sees exercise or symptom data used for underwriting.
- **Fix:** Name the Siriraj clinical owner (a real person, once confirmed) and a limit-entry sign-off record. Write a one-page consent. NEEDS REAL EXPERT (lawyer, S4).
- **Needs real expert?** Yes.

### F10 [S2] The research notes contradict themselves on the Thai readmission figure
- **What is wrong:** `research/README.md:34` says the "88% had 1-2 readmissions" figure is not a population rate, but the market report still presents it as "high readmission rate (88% within 12 months)" for the insurer pitch (`market/notebooklm-deep-report.md:109`). The Movn "proven" 20-30% is vendor data (`research/README.md:32`, `market/notebooklm-deep-report.md:63`).
- **Fix:** Correct line 109; flag vendor data in the table row.
- **Needs real expert?** No.

### F11 [S2] Missing-data, depression and fear after MI are not designed
- **What is wrong:** Depression is a high-risk marker in the research (`qa:89`), yet no screen is proposed. Sudden notification pressure on a frightened patient is not discussed. Fear after MI can lead to over- or under-exertion. (S3 will cover detail.)
- **Fix:** A PHQ-2 at onboarding with escalation to a clinician; the app never says "you failed".
- **Needs real expert?** Yes (S3 and psychiatrist or psychologist).

### F12 [S3] Resistance-training sternal rule is in research only
- **What is wrong:** The 12-week upper-body rule after CABG (`qa:109`) is not in the spec's mission library plan.
- **Fix:** Exclude resistance missions in v1, or carry the rule as a hard block.
- **Needs real expert?** Yes.

## What I could not verify
- The primary sources behind the 80/15, 81/11 and 93/15 figures (PMC12990137 not opened); NotebookLM citation indices.
- The GERS-P K=0.6/0.8 statement, the exact AACVPR class definitions, and the 10 bpm deduction (`qa:41`); I treat all as UNSOURCED until a clinician checks them.
- The Thai post-ACS 10-day recommendation, the 12.5% phase-2 uptake and the LINE-based study results.
- Whether the Siriraj mentor has seen any of this. Nothing in the artifacts shows sign-off.
- Wrist HR accuracy in arrhythmia, beta-blocker, or AF patients: UNSOURCED, NEEDS REAL EXPERT.
- Anything about code behaviour: no code exists (`HANDOFF.md:11`).
