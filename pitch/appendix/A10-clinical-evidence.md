# A10 · What is the clinical basis?

**One-line answer:** Cardiac rehab guidelines already accept several ways to set a safe exercise intensity, with CPET as the most precise and others when there is no CPET. They also say who is safe for unsupervised home exercise. Our app does not make those decisions. A clinician sets the limit and the risk class, and the app only schedules small missions inside them. Our guideline research is machine-generated and contradicts itself in places, so a real rehab physician must reconcile it before any number is coded.

> **Status of the evidence:** first-pass research built with NotebookLM from 55 sources (2026-10-17). We have not yet opened the primary guidelines (ESC 2020, EAPC, AACVPR editions, the Thai 2020 recommendations) to check each number. Every value below is **to verify**, and nothing here is a claim that the app works.

## Where the limit comes from

The clinician sets the limit, and the source test is recorded in the FHIR `CarePlan` (`limit-source` extension).

| Source of the limit | What it gives | Guidelines that accept it (per research file) | Our use |
|---|---|---|---|
| **CPET** | Ventilatory thresholds. HR at VT1 can be the hard upper bound | Main source in the pitch. The review we found calls CPET "significantly underutilized" (cost, training, equipment) | Best case. Synthetic p01, p05, p07, p08 |
| Symptom-limited ECG stress test | Peak HR and HR reserve, measured on usual medication | IACR (Irish, 2025), AACVPR, ESC 2020, GERS-P 2022, EAPC | p03 (`exercise-ecg`) |
| 6-minute walk test | Submaximal capacity for a low-to-moderate start | IACR, GERS-P, EAPC | p02 (`6mwt`) |
| Resting HR + 20–30 bpm | Early outpatient target when there is no test | AACVPR, ACSM (per research file) | Not in v1 (needs clinician sign-off) |
| Borg RPE 11–14 (6–20 scale) | Perceived effort | ESC, EAPC, AACVPR, IACR, ACSM | **Always paired** with HR |
| Talk test | "Can still talk" | ESC, EAPC, IACR, AACVPR | **Primary for beta-blocked patients** |

**Beta-blockers** blunt heart rate, so formulas based on age-predicted maximum HR are unreliable. Proposed v1 rule, waiting for clinician confirmation: **no %HRR calculation. Use the clinician's HR ceiling plus RPE 11–13 and the talk test.** No resistance missions in v1.

## Who is suitable (risk classes, to reconcile)

| Class (AACVPR-style, per research file) | Examples of criteria | Suitability for home or app use (per research file) | v1 app behaviour |
|---|---|---|---|
| Low | LVEF ≥ 50% (bands conflict, see below), uncomplicated event, ≥ 7 METs measured, no complex arrhythmia, no depression | Suitable for unsupervised home or digital rehab | App missions, **once a clinician confirms the class** |
| Moderate | LVEF about 35/40–49%, symptoms only at higher effort | Hybrid home rehab after 3–6 supervised sessions | Supervised sessions first (synthetic p03) |
| High | LVEF below 35/40%, cardiac-arrest survivor, complex arrhythmia, ICD (listed in one source, to confirm), symptoms at low effort | **Not suitable** for unsupervised exercise | Blocked + referral `Flag` (synthetic p04) |
| Unknown | No class entered | — | **Treated as blocked** |

Note: synthetic patient cmc-p07 was regenerated with LVEF 53% so its "low risk" label matches these bands.

A catch the panel found: "low risk" needs ≥ 7 METs **measured**, so a user with no test cannot be classed as low risk. That is why the app requires a clinician-entered class.

## Contradictions a clinician must settle (from `RECONCILE-for-clinician.md`)

| # | Question | Source A | Source B |
|---|---|---|---|
| 1 | Moderate-intensity target after MI | 50–70% HRR | VT1 is about 39–45% HRR post-MI, so 50–70% may exceed VT1 |
| 2 | Beta-blocker adjustment | K 0.6 → 0.8; subtract 10 bpm | Age-predicted max overestimates by 20–40 bpm (uncited) |
| 3 | Resistance start | Post-MI 1–4 weeks; upper body 12 weeks after CABG | 2–4 weeks post-PCI; 4–6 weeks post-CABG |
| 4 | Talk test | Full sentences | Short phrases at moderate intensity |
| 5–6 | Risk bands and MET thresholds | LVEF ≥ 50; moderate 35–49 or 40–49 | > 50; 40–49. Overlapping MET bands |
| 7 | ICD as high risk | Listed | Not stated |
| 8 | Session length | 20–60 min | ≥ 40 min continuous + 10 + 10 |
| 9 | Weekly progression | 5–10% per week | Our eval caps at 10% |
| 10 | Stop criteria | Lab test-termination list | Not adapted for home (no BP cuff) |
| 11 | Thai heat | Not covered | Not covered |
| 12 | Home-safety wording | SAE risk ratio 1.30 (95% CI 0.63–2.67) read as "non-inferior" | That interval does **not** support non-inferiority |

Safe wording for home-rehab safety, if asked: "no significant difference in trials of screened low- and moderate-risk patients; the intervals include a possible increase in serious events."

## The Thai gap (why this matters locally)

| Finding (per research file, to verify against the primary source) | Caveat |
|---|---|
| Thai post-ACS recommendations (2020): offer cardiac rehab no later than **10 days** after discharge | Guideline statement |
| Phase-2 outpatient rehab uptake after CABG: **12.5%**. **83.3%** of those patients said they were never told about it | Single-site study |
| Thai LINE-based home rehab study (n = 54, 27 vs 27): better 6-minute walk, DASI and SF-36 scores than controls | Small trial. Supports LINE as a channel |
| Social support predicted readmission in Thai cardiac cohorts (β = −0.225) | Correlational. Not a trial of peer groups |
| Doctors recommend exercise but rarely give it in writing | **Unresolved:** the repo has two conflicting figures (about 81%/11% for cardiologists vs 93%/15% for Italian GPs, PMC12990137). **Use neither** until someone opens the primary source |

Do **not** quote "88% of post-MI patients are readmitted". That figure almost certainly describes patients who were readmitted at least once.

## What still needs a real clinician

| Who | Decision |
|---|---|
| Cardiologist (named owner of the limit library) | Default for a user with no limit record. Hard-block list. Thai red-flag phrase list including negation (e.g. "ไม่เจ็บหน้าอก"). Whether 1669 is the right number to show. Drug-class rules beyond beta-blockers (nitrates, anticoagulants, diuretics, antiarrhythmics, diabetes drugs). Whether discharge notes carry exercise limits |
| Cardiac rehab physician or CPET lab | The 12 rows above. Warm-up, cool-down, weekly volume and progression caps. Thai heat thresholds. CPET availability in Thailand |
| Clinical pharmacist | Medication reminder text. The "agent never advises on drugs" rule |
| Cardiac nurse, Thai health-literacy specialist | Usability for patients aged 55–75. Caregiver role. Fasting timing. Thai naming of "mission" |
| Psychologist | Depression and fear-of-exercise screen (a Thai-validated instrument) |

## Sources / evidence in repo

- `research/README.md`: what the research changes, the "DO NOT IMPLEMENT" warning, Thai gap
- `research/guidelines/app-parameters-qa.md`: intensity without CPET, beta-blockers, stop criteria, risk classes, FITT, home safety, Thai studies (machine-generated, verbatim NotebookLM output)
- `research/guidelines/RECONCILE-for-clinician.md`: the 12 contradictions
- `research/pitch-claims-check.md`: doctor-statistic conflict, CPET underuse
- `evaluation/reviews/2026-10-17-document/SYNTHESIS.md` R4, R6, R18 and the "needs a real expert" table (simulated panel)
- `docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md` §2b, §5, §8
- `synthetic/generate_fhir.py`: limit sources and risk classes of the 8 synthetic patients
