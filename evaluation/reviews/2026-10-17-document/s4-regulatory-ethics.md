# s4-regulatory-ethics review — document — 2026-10-17

> Simulated review by a language-model role-play. Not a real clinician or institution.

**Artifacts read:** `docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md`, `docs/pitch-script-draft1.md`, `HANDOFF.md`, `research/README.md`, `research/pitch-claims-check.md`. Skimmed: `research/` (grep for PDPA, FDA, SaMD, consent, OIC, sandbox, privacy, liability, IRB, ethics), `research/guidelines/app-parameters-qa.md` (stop criteria, risk classes).
**Gate result (my view):** FAIL (G1, G4 fail; G3, G5, G6 not defined; two S0 open)

Scope note: I cite no Thai statute, clause or FDA classification rule. Anything that depends on one is marked UNSOURCED or NEEDS REAL EXPERT. The repo contains no regulatory or PDPA research at all; the grep above returned only a US FDA mention about a competitor and a Thailand 4.0 policy paragraph.

## Safety gates
| Gate | Status (PASS / FAIL / NOT-DEFINED) | Evidence (path:line) |
|---|---|---|
| G1 Limits | FAIL | The design intent is right (`design.md:71`, `:74`, `:97`). But limits can be "entered or scanned from discharge note" (`design.md:81`), so the patient may type them in. Nothing says who verifies them. B2C no-CPET users have no clinician-set limit path (`design.md:108`, `research/README.md:17`, which only says "flagged by who set the limit"). The pitch has the AI "designs an optimal, exact plan" (`pitch-script-draft1.md:17`). Provably inside clinician limits is not met. |
| G2 Red flags | PASS (design level, with caveats) | Deterministic handler, no LLM, "Stop now and call 1669" (`design.md:73`, `:93`, `HANDOFF.md:35`). Caveats: how symptoms are captured is not defined (free-text chat would route through the LLM). The 1669 number needs verification (NEEDS REAL EXPERT, Thai EMS). |
| G3 Eligibility | NOT-DEFINED | The risk-class gate is only a research suggestion (`research/README.md:18`). The spec's target user lists heart failure and high-risk hypertension (`design.md:46`) and has no ICD or low-EF exclusion. Open question 0 is unresolved (`design.md:108`). |
| G4 Claims | FAIL | "proven tool to reduce readmission rates" (`pitch-script-draft1.md:25`, flagged unsupported at `pitch-claims-check.md:9`). "optimal, exact plan … with ease" (`pitch-script-draft1.md:17`). The core framing is an AI-built "exercise prescription" (`design.md:22`, `pitch-script-draft1.md:9`). The design doc corrects these (`design.md:36-39`), but the pitch script is unchanged. |
| G5 Accountability | NOT-DEFINED | No named clinical owner for limits. Whether the clinician sees anything in v1 is open (`design.md:116`). No consent text, no PDPA treatment, and no insurer data-sharing design in any artifact. |
| G6 Failure mode | NOT-DEFINED | No text on missing watch data, network outage, or model outage. "Safe default, no new intensity" is not stated anywhere (grep of the design doc and `HANDOFF.md`). |

## Scores (0–4, track A or B)

### Track A — design and system
| Dimension | Score | One-line reason |
|---|---|---|
| Clinical validity | 2 | Rules are consistent with rehab practice in outline (`design.md:67-75`), but they are explicitly unconfirmed by a clinician. |
| Patient safety | 2 | Red-flag and no-self-raise rules exist (`design.md:73-74`). There is no hazard analysis, no exclusion enforcement, and no degraded mode. |
| Evidence and sourcing | 2 | The claims check is honest and flags vendor data (`research/README.md:30-35`). The research is machine-generated and not yet verified. |
| Feasibility | 2 | The architecture is plausible (`design.md:79-95`). There is no code and the team has no named clinical owner. |
| Regulatory and privacy | 1 | SaMD risk is identified (`design.md:39`, `:75`) and nothing is resolved. PDPA, consent, data residency and insurer sharing are absent. The LLM vendor as a data processor is not mentioned. |
| Behavior and adherence | 2 | Plausible (micro-missions, peer community). Untested and not my focus. |
| Agent safety and evaluation | 1 | The rules/LLM split is stated (`design.md:97`). There is no scenario suite and no test plan. |
Track A average: 12/7 = 1.71

### Track B — pitch
| Dimension | Score | One-line reason |
|---|---|---|
| Problem clarity | 2 | There is one patient and one moment, but 80/15 is mis-sourced (`pitch-claims-check.md:5`) and "5-minute consult" is unsourced (`:6`). |
| Solution credibility | 1 | "Optimal, exact", AI "designs" the plan, and nothing on safety limits or clinician involvement in the script. |
| Evidence | 1 | Headline stat is wrong and "proven" is false. Limits are not stated. |
| Market and business | 2 | Payer and price are named. Insurer willingness and 499 are unvalidated (`pitch-claims-check.md:10-11`). |
| Differentiation | 1 | No competitor is named in the script. The EXPERT-tool contrast sits only in the design doc (`design.md:42`). |
| Team and feasibility | 1 | No clinical partner named in the script and no demo exists. |
| Impact and ethics | 1 | The script says nothing on safety, consent, data, or equity. Older, low-income and rural patients are not addressed. |
Track B average: 9/7 = 1.29

**Overall average (A and B): 1.5 (needs major work)**

## Findings (most severe first)

### F1 [S0] Pitch script makes false and diagnose/treat-adjacent claims
- **What is wrong:** The script says "proven tool to reduce readmission rates", "optimal, exact plan", and frames the product as an AI-designed "exercise prescription". The "proven" claim is false for this product, and "prescription" is clinician-practice wording that supports a medical-function reading.
- **Evidence:** `docs/pitch-script-draft1.md:9`, `:17`, `:25`; `research/pitch-claims-check.md:9`; `design.md:36-39`.
- **Failure scenario:** A judge, an insurer's legal team or the Thai FDA reads "proven" and "prescription". The team is then asked for trial data it does not have, or the pitch becomes the evidence of intended use in any regulatory discussion. How "intended use" is judged under Thai rules is UNSOURCED.
- **Fix:** Replace with the design doc's wording: "keeps missions inside your clinician's safe limits, adjusted each week", and "designed to support rehab adherence, which is linked to fewer readmissions" with a cited rehab source. Drop "prescription" from patient-facing and judge-facing copy, or say "clinician-set exercise limits".
- **Needs real expert?** yes (Thai FDA / regulatory lawyer, for the wording and intended-use question)

### F2 [S0] Limits provenance is open for the B2C freemium path
- **What is wrong:** The business model is a self-serve free week, and most of those users have no CPET. The spec allows limits to be "entered", with no rule that a clinician verifies them. Any self-entered number becomes an unreviewed exercise limit applied to a post-MI patient.
- **Evidence:** `design.md:81`, `:108`; `research/README.md:17`; `pitch-script-draft1.md:27`.
- **Failure scenario:** A post-MI patient with an ICD or low EF skips the clinician and types "130 bpm". The app issues missions at that intensity. This is a patient-harm path and a liability path, because the product enabled it.
- **Fix:** Rule: no mission is generated until limits carry a clinician identity and date (e.g. a signed discharge limit sheet). Without it, the app offers only non-exercise content (education, meds reminders, walking-as-tolerated text approved by a clinician) and no heart-rate-bounded missions. Write this rule into spec §5.
- **Needs real expert?** yes (cardiologist / rehab physician, to approve the default content)

### F3 [S1] No PDPA, consent or data-flow design anywhere
- **What is wrong:** The product ingests heart-rate data, diagnosis, medications and symptoms, and the business model is to share it with insurers. None of the five artifacts covers consent, purpose limitation, retention, cross-border transfer (the LLM and backend location is undefined), or a rule on what insurers see.
- **Evidence:** `design.md:6-122` (no privacy section); `HANDOFF.md:30-36`; grep of `research/` found no PDPA content.
- **Failure scenario:** An insurer partner or hospital IRB asks "what does the insurer see, and did the patient agree separately?" and nobody can answer. A patient later finds that premium or claims decisions used app data (insurer use of this data for underwriting is a major ethics risk).
- **Fix:** Add a one-page data-flow diagram and a consent matrix. Include separate opt-in for insurer sharing, which is aggregate-only by default and never feeds underwriting. Name a controller. State where the LLM is called and what is sent (de-identified summaries, not raw identity). Health data is treated as sensitive under Thai PDPA (UNSOURCED here; clause details NEEDS REAL EXPERT).
- **Needs real expert?** yes (Thai privacy lawyer / hospital DPO)

### F4 [S1] SaMD classification is flagged but treated as "later"
- **What is wrong:** `design.md:75` says "check before any real-patient pilot" and `HANDOFF.md:36` calls positioning as adherence support a decision. A positioning label does not decide classification. An agent that selects exercise intensity from physiological data may be read as more than a lifestyle tool. I cannot say which way Thai FDA would rule. The "no diagnose, no detect" rule does not address the treatment or management side.
- **Evidence:** `design.md:39`, `:75`; `HANDOFF.md:36`.
- **Failure scenario:** The team builds a pilot, then learns it needs registration or a different pilot route. Months are lost against the funding window.
- **Fix:** Before building, send a short written intended-use statement and feature list to a Thai FDA consultation channel or lawyer. Keep the feature set in line with the answer (e.g. mission library fixed and clinician-approved, agent only schedules and phrases).
- **Needs real expert?** yes (Thai FDA / regulatory lawyer)

### F5 [S1] No named accountable clinician or incident process
- **What is wrong:** Who owns the limits, who reviews flagged "could do more" cases, and who receives adverse events are all undefined. Open question 8 asks whether the clinician sees anything at all.
- **Evidence:** `design.md:74`, `:116`.
- **Failure scenario:** The app flags "patient could do more", and nobody receives it. Or a patient is hurt and there is no incident record, no reporting route, and unclear liability between the hospital, the startup and the insurer.
- **Fix:** Name a Siriraj clinical owner (or state none yet and block patient use). Define a minimal incident log, a flag inbox with a response time, and a pilot-agreement liability clause drafted by a lawyer.
- **Needs real expert?** yes (hospital clinical safety committee, lawyer)

### F6 [S1] Eligibility gate is not in the spec, and the target user list is too wide
- **What is wrong:** The target group includes heart failure and high-risk hypertension (`design.md:46`). The research says high-risk patients (ICD, low EF) are "not suitable" for unsupervised use (`research/README.md:18`), but onboarding has no screening step and the app has no way to verify answers.
- **Evidence:** `design.md:46`, `:108`; `research/README.md:18`.
- **Failure scenario:** A heart-failure patient with an ICD downloads the free week.
- **Fix:** Narrow v1 to post-MI, low-risk class, clinician-enrolled. Add a hard eligibility screen with exclusion and "ask your doctor first" screens. Self-declaration alone is weak, so prefer enrolment through the hospital or insurer.
- **Needs real expert?** yes (cardiologist, for the class definitions)

### F7 [S1] Failure and degraded modes undefined
- **What is wrong:** No behavior is specified for missing watch data, a model or network outage, or spoofed or noisy heart rate data.
- **Evidence:** G6 row above. Not mentioned in `design.md` or `HANDOFF.md`.
- **Failure scenario:** The model times out and a stale previous mission, or a default one, is pushed at higher intensity.
- **Fix:** One rule in §5: when data is missing or stale, push only the last approved mission at or below its previous level, or a rest or check-in message. Never increase.
- **Needs real expert?** no (engineering), with clinician sign-off on the default

### F8 [S2] Insurer B2B2C raises an ethics issue the pitch does not touch
- **What is wrong:** Selling to insurers while holding patient health data creates a conflict. Patients may fear that adherence or HR data affects cover or premiums.
- **Evidence:** `pitch-script-draft1.md:25`; `research/README.md:25`.
- **Failure scenario:** A judge asks "will my insurer see I skipped walks?"
- **Fix:** Add a sentence and a design rule: insurer sees opt-in aggregate engagement only. No individual data without separate consent. Whether this is even permitted in Thai insurance practice is NEEDS REAL EXPERT (OIC rules, UNSOURCED).
- **Needs real expert?** yes (insurance lawyer)

### F9 [S2] Peer-community feature has no safeguards
- **What is wrong:** Peer groups let patients see each other's data and talk about health. There is no moderation plan, no rule against peer medical advice, and no privacy rule for shared activity goals. It is also not in the design doc's architecture.
- **Evidence:** `pitch-script-draft1.md:17`; `design.md:24` (named, not designed); `pitch-claims-check.md:8` (support is indirect only).
- **Failure scenario:** A member tells another to "push through" chest tightness.
- **Fix:** Defer to a later phase, or design it with a moderated, scripted, pseudonymous format and a safety message in every thread.
- **Needs real expert?** yes (clinical, privacy)

### F10 [S2] Unverified sources still feed the pitch
- **What is wrong:** The research is labelled machine-generated. The claims check corrects 80/15 to 93/15 (Italian GPs), but the script still carries 80/15 and the fix is not applied.
- **Evidence:** `research/README.md:4`; `research/pitch-claims-check.md:5`; `pitch-script-draft1.md:7`.
- **Failure scenario:** A judge checks the stat and finds it wrong.
- **Fix:** Apply the corrected figure with its citation, or cut it. Verify the PMC reference directly (I did not open it).
- **Needs real expert?** no

### F11 [S3] Minor wording
- "Stop now and call 1669" should be reviewed as patient copy in Thai by a clinician (`design.md:73`). Emoji in the med reminder (`design.md:103`) is fine, but make sure reminders never show drug names on a lock screen without the patient opting in (privacy).

## What I could not verify
- Whether Thai FDA would classify this as SaMD, and at what class (UNSOURCED, NEEDS REAL EXPERT).
- The exact PDPA obligations (sensitive-data basis, explicit consent form, DPO duty, cross-border rules), also OIC rules on insurer data use (UNSOURCED, NEEDS REAL EXPERT).
- The IRB route for a pilot, the hospital's own approval path, and who holds liability. NEEDS REAL EXPERT (Siriraj IRB, lawyer).
- Whether 1669 is the correct emergency number for the patient copy (NEEDS REAL EXPERT).
- The PMC12990137 source and all machine-generated research figures. I did not open them.
- Whether any code exists. HANDOFF says none, so I did not run an evaluation.
