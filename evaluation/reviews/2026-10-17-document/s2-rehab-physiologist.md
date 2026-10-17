# s2-rehab-physiologist review — document — 2026-10-17

> Simulated review by a language-model role-play. Not a real clinician or institution.

**Artifacts read:** docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md (spec), docs/pitch-script-draft1.md (pitch), HANDOFF.md, research/README.md, research/pitch-claims-check.md, research/guidelines/app-parameters-qa.md (QA), research/guidelines/notebooklm-deep-report.md (DEEP). Line numbers below are the file's own line numbers.
**Gate result (my view):** FAIL (G1 and G4 FAIL; two S0 findings open)

Conventions: where I say a guideline value differs from what I know, I give my recollection and mark it NEEDS REAL EXPERT where I cannot verify it. I have not opened the primary guidelines in this review.

## Safety gates
| Gate | Status | Evidence (path:line) |
|---|---|---|
| G1 Limits | FAIL | Intent is right (spec:71, :74). But (a) the pitch says AI "designs an optimal, exact plan" (pitch:17); (b) the free 1-week plan has no clinician-set limit (pitch:27, spec:108); (c) "limits" are defined only as HR, RPE and activity type (spec:71), so duration, frequency and weekly progression are unbounded; (d) the spec's own example offers 10 -> 12 min (spec:101), a 20% jump, against the 5-10%/week rule in QA:121. Nothing makes "inside limits" provable. |
| G2 Red flags | PASS (design intent only) | Deterministic, no LLM, "Stop now and call 1669" (spec:73, :95). Pitch is silent. The symptom list is a test-termination list (QA:49-61), not a home list; see F6. |
| G3 Eligibility | NOT-DEFINED | The risk-class gate exists only in research/README.md:18 and spec:108. §5 safety rules and §3 target user include HF and "hypertension with high risk" (spec:46), with no ICD/EF/unstable-angina exclusion. QA:94 says high-risk is NOT suitable, so the spec's own target user list conflicts with it. |
| G4 Claims | FAIL | "optimal, exact" (pitch:17), "proven tool to reduce readmission rates" (pitch:25), unsourced 80/15 (pitch:7). The spec and claims-check flag these (spec:35-39, claims-check:5, :9), but the script text is unchanged. |
| G5 Accountability | NOT-DEFINED | "Confirm with the Siriraj clinical mentor" (spec:70) is not a named owner of limits. No consent design. No definition of who signs the limit for B2C users. |
| G6 Failure mode | NOT-DEFINED | Nothing on watch, network or LLM down. Nothing on "no data -> repeat last safe mission or rest". |

## Scores (Track A: design and system)
| Dimension | Score | One-line reason |
|---|---|---|
| Clinical validity | 2 | Skeleton is sound (RPE plus talk test with beta-blockers, no self-raised limits, duration before intensity). The numeric parameter set is internally contradictory (F2, F3) and the sources are weak. |
| Patient safety | 1 | No hazard analysis. A single HR cap, no warm-up/cool-down, a midday-heat example mission, no pre-exercise check, and the eligibility gate is not in the spec. |
| Evidence and sourcing | 2 | Honest "machine-generated, verify" labels. But sources include Aetna, Docsity, a congenital-HD paper and an Irish guideline presented as "IACR"; vendor and single-site data are flagged. |
| Feasibility | 2 | Buildable. Unknown who produces limits and how risk class is learned (F4). |
| Regulatory and privacy | 2 | SaMD risk identified (spec:75). Unresolved. Outside my lens. NEEDS REAL EXPERT (S4). |
| Behavior and adherence | 2 | Plausible but untested. Peer goals add an over-exertion hazard (F8). |
| Agent safety and evaluation | 1 | Architecture split is correct (spec:97). No scenario suite or test plan exists. No code. |
**Track A average: 12/7 = 1.7**

## Scores (Track B: pitch script)
| Dimension | Score | One-line reason |
|---|---|---|
| Problem clarity | 2 | One patient (post-MI) and a real gap. The 80/15 numbers are wrong or unsourced, and "5-minute consult" has no source. |
| Solution credibility | 1 | "Optimal, exact, with ease" contradicts the clinician-limit design. CPET is presented as the input, but most B2C users will not have one. |
| Evidence | 1 | Headline stat unsourced. The corrected 93%/15% (claims-check:5) refers to Italian GPs, not Thai cardiologists. |
| Market and business | 2 | Payer and price are stated. WTP and insurer payment are unverified (claims-check:10-11). Outside my lens. |
| Differentiation | 1 | The pitch never names Movn, Cardihab, LINE programs or the EAPC EXPERT tool (the EXPERT tool is only in spec:42). |
| Team and feasibility | 1 | No demo ("No code yet", HANDOFF:11). No clinical partner named in the pitch. |
| Impact and ethics | 1 | Silent on safety, eligibility and who is accountable. |
**Track B average: 9/7 = 1.3**   **Overall average: 21/14 = 1.5 (needs major work)**

## Findings (most severe first)

### F1 [S0] Free-tier / no-clinician plan breaks the app's own safety rule 1
- **What is wrong:** The pitch gives every new user a free 1-week schedule (pitch:27) and says AI designs the plan (pitch:17). The spec requires limits from a clinician (spec:71), and says B2C users mostly have no CPET (spec:40, :108). No artifact says who signs a limit for a self-installed user.
- **Evidence:** pitch:17, :27; spec:71, :108; QA:94.
- **Failure scenario:** A 62-year-old, 3 weeks post-MI, downloads the app, types "metoprolol", and gets "10 min walk, RPE 12-14" with no EF, no stress test and no release to exercise. If he has LVEF 30% or residual ischemia, he is high-risk and unsuitable for unsupervised exercise (QA:94).
- **Fix:** No exercise mission is issued until a limit record exists with `set_by` (clinician name or ID, source test, date). Freemium users get education, medication and walking-as-usual content only. Alternatively, the free week is a clinician-onboarded trial. Change the pitch to match.
- **Needs real expert?** yes (cardiac rehab physician at Siriraj).

### F2 [S0] The intensity parameters in QA conflict with DEEP, and the defaults could place patients above VT1/VT2
- **What is wrong:** QA presents 50-70% HRR as "standard post-MI" (QA:21, :102) and K = 0.8 for beta-blocked patients (QA:21, :40). DEEP states that in post-MI cohorts VT1 sits at about 39-45% HRR and about 63-68% HRpeak, and that 60-75% HRR formulas "frequently" push high-risk patients above VT2 (DEEP:69). Phase II start should be at or below VT1, RPE 12-13 (DEEP:98). Applying 80% HRR to a beta-blocked patient is not consistent with that. I recall GERS-P K values of this kind only for patients with a measured, on-drug peak. I cannot verify the K = 0.8 claim.
- **Evidence:** QA:21, :40, :102; DEEP:69, :98, :127.
- **Failure scenario:** The rules engine implements QA:21 literally. A beta-blocked patient with HRpeak 120 and HRrest 55 gets a "target" of 55 + 0.8 x 65 = 107 bpm, which may sit above his VT1 or VT2. He is told "stay below 110".
- **Fix:** Rules engine v1 uses an upper HR cap taken from the clinician (ideally the HR at VT1 or the on-drug test), RPE 11-13 and "full sentences", and does not compute %HRR itself. The app may store the formula output only as a suggestion to the clinician, never as a limit. Reconcile QA and DEEP in writing before any number is coded.
- **Needs real expert?** yes (CPET lab / rehab physician).

### F3 [S1] Internal numeric contradictions between QA and DEEP (all would need to be resolved before hard-coding)
- **What is wrong:** Listed with my recollection where I have one.
  1. Resistance start: QA:108-109 says post-MI 1-4 weeks (after 1-2 weeks of aerobic) and post-CABG upper body 3 months. DEEP:110 says 2-4 weeks post-PCI or 4-6 weeks post-CABG. The sternal precaution gap (4-6 weeks vs 12 weeks) is the dangerous one. I recall most programs holding upper-body loading much longer after sternotomy than 4-6 weeks. NEEDS REAL EXPERT.
  2. Session length: QA:103 says 20-60 min including 5-10 min warm-up and cool-down. DEEP:100 says at least 40 min continuous plus "mandatory" 10 + 10 min, which is more than 60 min, so it contradicts DEEP's own "20-60".
  3. Beta-blocker HR adjustment: QA:41 says subtract 10 bpm from predicted max. DEEP:127 says age formulas overestimate by "up to 20-40 bpm" (UNSOURCED in the file). The safe answer is to not use age-predicted HRmax at all.
  4. Talk test: QA:30 says full sentences comfortably. DEEP:86 says moderate intensity means "short phrases but not sing", which is a higher intensity than a VT1-anchored target (DEEP:98).
  5. AACVPR EF: QA:69 says LVEF >= 50% for low risk. DEEP:32 says > 50%. Moderate band 35-49 (QA:76) vs 40-49 (DEEP:33). High: < 35 or < 40 (QA:81). I recall the AACVPR scheme uses >= 50 / 40-49 / < 40. Verify.
  6. Functional capacity: QA lists < 5.0 METs under both moderate (QA:79) and high (QA:87), plus <= 3.0 in high (QA:88). DEEP:33-34 repeats the overlap. The bands do not partition. I recall the AACVPR sheet showing moderate at about 5-7 METs and high at < 5 METs. Verify.
  7. ICD as a high-risk marker (QA:89): I cannot confirm this is in the AACVPR scheme itself. It is a sensible app exclusion regardless.
- **Evidence:** as above.
- **Failure scenario:** The engineer picks one value per row. The wrong choice (CABG at 4-6 weeks; moderate-band overlap) goes into the mission library.
- **Fix:** One reconciled parameter table, with a column for primary source, version, page and "signed by". Keep thresholds in a clinician-editable config, not code.
- **Needs real expert?** yes.

### F4 [S1] The "no CPET" answer is a list of options, not a rule; limits cannot realistically come from a discharge note
- **What is wrong:** README:17 and spec:108 list stress test, 6MWT, %HRR, RHR + 20-30, RPE and talk test as accepted inputs. But the eligibility criteria that make an app-only user "low risk" (EF >= 50%, >= 7 METs measured, no depression; QA:68-74) themselves require echo, a stress test and a depression screen. Spec:81 imagines limits "scanned from discharge note". My expectation is that discharge letters typically say "exercise as tolerated" and contain no HR or RPE limits (not verifiable here; NEEDS REAL EXPERT). RHR + 20-30 bpm (QA:24-25) is an early-phase rule for supervised or early mobilization, not a self-served limit. Also, 6MWT does not yield a training HR on its own.
- **Evidence:** QA:68-74, :24-25; spec:81; README:17-18.
- **Failure scenario:** Hospital cannot or does not fill in limits. The team falls back to RHR + 20 for everyone. A patient with a resting HR of 90 from anxiety or anemia gets a 120 cap without any clinician review.
- **Fix:** v1 demo and pilot: a clinician form with these fields only: date of release, risk class, HR ceiling, RPE ceiling, max minutes per session, max sessions per week, resistance allowed (Y/N and from date), exclusions. If the form is empty, no exercise mission.
- **Needs real expert?** yes.

### F5 [S1] A "tiny daily mission" cannot carry a complete prescription: warm-up, cool-down, FITT volume and resistance are missing
- **What is wrong:** The sample mission is "Walk 10 min after lunch, stay below 110 bpm" (spec:53). Guidance in the files calls for warm-up and cool-down of 5-10 min each (QA:103), cool-down >= 10 min with vasodilators (DEEP:137), 3-5 days/week and 150-300 min/week target (DEEP:102; HAT >= 150 min, DEEP:174), and resistance 2-3 days/week (QA:110). A 10-min walk with one HR cap provides none of these. No target for weekly volume is stated anywhere.
- **Evidence:** spec:53, :102; QA:101-115; DEEP:100-102, :137.
- **Failure scenario:** Patient on nitrates or an ACEi stops a brisk walk abruptly at the corner, sits down, becomes pre-syncopal. Or after 12 weeks he is still doing 10 minutes and the insurer's "rehab package" has delivered a fraction of a rehab dose.
- **Fix:** Each mission template includes: warm-up (e.g. 3-5 min easy), main block, cool-down, an RPE check prompt, an explicit "stop if" line and a weekly volume target set by the clinician. Say honestly in the pitch that v1 is "a bridge to and between rehab", not "a rehab package" (see F9).
- **Needs real expert?** yes (rehab physician for the template parameters).

### F6 [S1] Red-flag list and handling are copied from test-termination criteria, and miss home-relevant signals
- **What is wrong:** QA:49-61 mixes patient symptoms with in-lab criteria the app cannot measure (SBP > 250, ST depression >= 2 mm, HR drop > 10 bpm). The "virtual emergency protocol" with EMS notification and location confirmation (QA:61) is not designed anywhere in the spec. Missing for a home user: symptoms occurring at rest or after exercise (delayed), nitrate use (what to do when chest pain is relieved by rest or nitroglycerin and the patient wants to carry on), rapid weight gain or leg swelling, new orthopnea, fever or acute illness, a pre-exercise "not today" check (the resting BP threshold appears in DEEP:50 but nothing in the spec asks for a BP). Also a PPG-based HR is an unreliable trigger, especially with motion and arrhythmia. I am not certain of the best Thai wording; NEEDS REAL EXPERT (S1 cardiologist).
- **Evidence:** QA:49-61; spec:73; DEEP:50.
- **Failure scenario:** Patient reports chest tightness the evening after a walk. The Today screen still shows tomorrow's mission. Or the app triggers "call 1669" from a PPG HR spike during arm swing.
- **Fix:** Separate lists: (a) in-session stop symptoms, (b) after-session or rest symptoms and "do not exercise today" triggers, (c) data-driven cautions that only ever generate "stop and rest, then ask your clinician". All three are deterministic, Thai-language, and pre-approved by the clinician.
- **Needs real expert?** yes (cardiologist).

### F7 [S1] The home-safety evidence is stretched: supervised event rates and a wide-CI meta-analysis are read as "clinically safe and non-inferior"
- **What is wrong:** The cardiac arrest and fatal event rates (QA:130-131) come from supervised, ECG-monitored centers and say nothing about unsupervised app users. The SAE RR of 1.30 (0.63-2.67) and mortality RR of 1.06 (0.76-1.49) (QA:134-135) show no significant difference, but the interval for SAE is far too wide to claim "non-inferior" (QA:136). Those trials enrolled screened low-to-moderate risk patients, many with a supervised start (QA:93). DEEP:147-154 adds conditions the app lacks: real-time audiovisual tele-supervision, a caregiver trained in emergencies, a safe home environment, complete revascularization. I recall the rates as being close to Franklin 1998 but cannot confirm the exact figures; verify before quoting.
- **Evidence:** QA:129-136; DEEP:147-154.
- **Failure scenario:** The pitch or insurer deck says "home-based CR is as safe as center-based", and the first adverse event in the pilot is blamed on an unsupervised patient who was outside those trials' populations.
- **Fix:** Say "no significant difference in trials of screened low- and moderate-risk patients; confidence intervals include a possible increase in serious events". Add "caregiver contact" and "emergency plan" to onboarding.
- **Needs real expert?** yes (biostatistician or cardiologist).

### F8 [S1] Peer communities with shared activity goals have no intensity guard
- **What is wrong:** Pitch:17 adds peer groups for adherence. Nothing prevents a leaderboard or "my group walked 30 minutes" from pushing a post-MI patient past his own limit. Claims-check:8 only shows that social support predicts readmission, not that peer goals raise exercise safely.
- **Evidence:** pitch:17; claims-check:8; README:21.
- **Failure scenario:** Patient on a beta-blocker who feels "fine" matches a friend's pace in the group and ignores his own RPE cap.
- **Fix:** Peer goals are about frequency and consistency only (sessions completed), never speed, distance or HR. Group chat does not show anyone's intensity.
- **Needs real expert?** no for the rule; yes (behavior reviewer) for design.

### F9 [S1] "Rehab package" and "replaces nothing" are in conflict; app must not stand in for supervised CR
- **What is wrong:** The pitch sells a "specialized rehabilitation package" to insurers (pitch:25). The spec says non-goal "replacing cardiac rehab" (spec:59). DEEP:174 notes that daily household activities must not replace formal exercise-based CR (Thai guideline wording, per the file). Thai phase-2 uptake is low (README:20), so the temptation is for the app to become the rehab.
- **Evidence:** pitch:25; spec:59; DEEP:174.
- **Failure scenario:** An insurer enrolls moderate-risk patients "instead of" the 3-6 supervised orientation sessions (QA:93).
- **Fix:** Position as "supports and extends rehab; enrollment requires referral and, for moderate risk, completed supervised orientation".
- **Needs real expert?** yes.

### F10 [S2] Example mission is set at noon in Thailand, and uses HR ceiling without RPE
- **What is wrong:** "Daily push at 12:30: 10-min easy walk" (spec:102) is the hottest, most humid part of the day in most of Thailand. Heat and humidity raise HR and strain for the same pace, and some cardiac medicines (diuretics) add dehydration risk. The spec:72 rule says pair HR with RPE, but the example text shows only "You should still be able to talk".
- **Evidence:** spec:53, :102, :72.
- **Fix:** Schedule defaults to early morning or evening or indoors; add heat and rain "indoor alternative" logic. NEEDS REAL EXPERT for the Thai-climate thresholds.
- **Needs real expert?** yes.

### F11 [S2] Progression is described only loosely, and the "ask the patient" step could slip a limit change
- **What is wrong:** QA:119-123 gives the right rules (duration before intensity, one variable, 5-10%/week). The spec's example lets the patient pick 10 or 12 min (spec:101). Rule 4 (spec:74) says no new limit without a clinician but "limit" is not defined to include duration or weekly volume (spec:71).
- **Fix:** Put max duration, frequency and a weekly cap on progression into the clinician record; the agent may offer only steps within the rule table. Flag stalled progress or two missed weeks to the clinician, not to the AI.
- **Needs real expert?** no.

### F12 [S2] Source quality and labelling in the research folder
- **What is wrong:** DEEP:178 gives "DASI > 34.7 METs". DASI is a questionnaire score, not METs; the unit is wrong. QA:146 and DEEP:178 give figures (about 20% CR utilization, 14-25% one-year mortality, QA:144) that I cannot trace (UNSOURCED here). "IACR (2025)" in QA is an Irish guideline (DEEP ref 22, iacronline.ie) but reads as an international body. Several citations are weak: Aetna payer bulletin used for remote-CR eligibility (DEEP ref 9), Docsity for the AACVPR table (ref 15), a congenital-heart-disease paper for wearable guidance (ref 21), and a 2012 AACVPR algorithm file. The deep report lists "Thai return to work 88.5%" correctly as a single site.
- **Evidence:** DEEP:178, refs 9, 15, 21, 22; QA:144, :146.
- **Fix:** Cite primary documents (ESC 2020, EAPC 2021 position statement, AACVPR guidelines, HAT). Mark every number with the primary source or `UNSOURCED`.
- **Needs real expert?** no.

### F13 [S2] "Without CPET" concerns for pitch wording: CPET as headline input
- **What is wrong:** Pitch:15 makes CPET the input. Claims-check:7 notes CPET is underutilized. In Thailand, access to CPET is unverified here (UNSOURCED). A judge or cardiologist will ask what the app does for the typical patient who has no CPET.
- **Fix:** Pitch line: "uses the limits your clinician sets, from CPET where available or from a stress test or walk test otherwise".
- **Needs real expert?** yes (Thai CPET availability).

### F14 [S3] Hygiene
- DEEP:150, "Complete revascularization" is listed as a remote-CR criterion; the spec's target user list (spec:46) includes patients without it. DEEP:70, the summary "prescribing 60-75% HRR ... frequently" is attributed to a single review; flag as one source.

## Checks of NOTEBOOKLM numbers (summary)
| Item | My read |
|---|---|
| Class I, Level A for exercise-based CR post-MI/CCS (DEEP:7) | Consistent with my recollection of ESC guidance. Verify class and level per document. |
| VT1 at 39-45% HRR, 63-68% HRpeak post-MI (DEEP:69) | Plausible and important. Single-study; verify source (DEEP ref 7). |
| Borg 11-14 / 12-14 for HR-limited patients (QA:27) | Consistent with common practice. Two ranges given; pick one (RPE 11-13 for v1). |
| Karvonen K = 0.6 / 0.8 (QA:21) | Cannot verify; conflicts with DEEP:69. See F2. |
| RHR + 20-30 bpm (QA:24) | Known early-phase rule (I recall ACSM figures of +20 for MI and +30 for surgery). Not for self-service use. |
| 5-10% weekly increase, duration before intensity (QA:119-121) | Consistent with common practice. |
| Resistance start timings (QA:108-109 vs DEEP:110) | Conflicting. See F3. |
| Valsalva avoidance, 1-3 sets x 8-15 reps, 2-3 d/week, 48 h (QA:110-116) | Consistent with common practice. Starting load by %1RM is not a home-novice instruction. |
| AACVPR risk classes (QA:67-89; DEEP:32-34) | Partly inconsistent between files. See F3. |
| Event rates (QA:130-131) | Close to a figure I recall (Franklin 1998). Supervised only. See F7. |
| DASI in METs (DEEP:178) | Unit error. |
| 1-year Thai ACS mortality 14-25% (QA:144) | UNSOURCED here. |

## What I could not verify
- Primary-guideline wording (ESC 2020, EAPC 2021, AACVPR 5th/6th ed., HAT 2020, IACR 2025). I worked from the extracts and from memory.
- K = 0.8 for beta-blocked patients; ICD as AACVPR high-risk; CABG upper-body timing; the exact Franklin figures; the DASI cut-offs.
- Whether Thai discharge letters carry exercise limits, and CPET availability in Thailand.
- Anything on regulation, consent or data (S4), safety of LLM-controlled flows (M1), and market numbers (M3).
- No code exists, so the rule engine, scenario suite and mission library could not be inspected.

## Cheapest fixes from my side (ordered)
1. Block exercise missions until a clinician-signed limit record exists (F1, F4).
2. Reconcile QA and DEEP into one signed parameter table; remove %HRR and K = 0.8 from the rules engine (F2, F3).
3. Rewrite pitch lines: "inside your clinician's limits", not "optimal, exact" or "proven"; fix 80/15 with a named source (F13, claims-check).
4. Add warm-up, cool-down and a weekly-volume target to the mission template (F5).
5. Split red-flag lists and add "do not exercise today" checks (F6).
