# s3-nurse-pharmacist review — document — 2026-10-17

> Simulated review by a language-model role-play. Not a real clinician or institution.

**Artifacts read:** `docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md` (spec), `docs/pitch-script-draft1.md` (pitch), `HANDOFF.md`, `research/README.md`, `research/pitch-claims-check.md`, `research/guidelines/app-parameters-qa.md` (qa), `research/market/notebooklm-deep-report.md` (skimmed for Thai patient barriers; grep plus targeted reads, not read in full).
**Gate result (my view):** FAIL. G4 fails on the pitch script. Several other gates are NOT-DEFINED, which counts as an S1 finding in document mode. S0 findings are open (F1, F2).

## Safety gates
| Gate | Status | Evidence |
|---|---|---|
| G1 Limits | NOT-DEFINED (intent stated, not provable) | Spec rule 1 and rule 4 say limits come from the clinician and the AI never raises them (spec:71, spec:74). But the source of limits in the demo is open (spec:110, Q2). Onboarding says limits are "entered or scanned from discharge note" (spec:82), so it is unclear who enters them. No-CPET users have no defined limit source beyond the README suggestion (README:17). Mission-level bound checking is not specified. |
| G2 Red flags | NOT-DEFINED (partial PASS on the LLM split) | Deterministic handler and "Stop now and call 1669" are stated (spec:73, spec:94, HANDOFF:35). Not defined: how a symptom is reported (button, free-text chat, daily check-in), what happens if the patient is not looking at the phone, and whether red-flag words typed into the chat bypass the LLM. qa:61 suggests location confirmation and EMS notification, and the spec does not adopt it. |
| G3 Eligibility | NOT-DEFINED in the design | The risk-class gate exists only in research (README:18, qa:65-94). The spec journey (spec:14-17) has no screening step. Depression and ICD are high-risk exclusions in qa:89, but onboarding has no depression screen, no ICD question and no LVEF question. The target-user list includes heart failure and high-risk hypertension (spec:46) without a gate. |
| G4 Claims | FAIL (pitch); PASS-with-notes (spec) | The pitch says "optimal, exact plan ... with ease" (pitch:17) and "proven tool to reduce readmission rates" (pitch:25). The team's own claims check marks the "proven" claim "Not supported for us" (pitch-claims-check:9). The 80%/15% numbers are wrong (pitch:7 vs pitch-claims-check:5). The spec flags these (spec:35-40) but the script is still the verbatim draft. |
| G5 Accountability | NOT-DEFINED | No named clinical owner for limits. "Confirm with the Siriraj clinical mentor" (spec:69) is not an owner. Whether the clinician sees anything in v1 is open (spec:116). No consent for wearable data, insurer access, or use. The words "consent" and "PDPA" do not appear in the spec. |
| G6 Failure mode | NOT-DEFINED | Nothing on watch disconnect, no HR data, or the LLM being down. The example week assumes "watch HR confirms the walk" (spec:102). A patient who taps Done with no watch data, or a patient whose watch is off, has no defined behavior. |

## Scores (0-4)

### Track A — design and system
| Dimension | Score | One-line reason |
|---|---|---|
| Clinical validity | 2 | Rules 1-4 are sound in direction. Meds, depression and the risk gate are missing from the design itself. |
| Patient safety | 1 | The red-flag intent is good, but there is no hazard analysis, and reporting, missed-dose and no-data paths are undefined. |
| Evidence and sourcing | 2 | The claims check is honest. Vendor data is flagged. Home-CR safety (qa:127-136) covers supervised or telemonitored low-to-moderate-risk CR, not an unsupervised LLM app. |
| Feasibility | 2 | A buildable sketch, but the limit source, watch, and language are open. |
| Regulatory and privacy | 1 | SaMD is identified (spec:75). Consent, PDPA and data flow are not designed. This is outside my lane (NEEDS REAL EXPERT: S4). |
| Behavior and adherence | 1 | "Brainless" is asserted. There is no week-3 plan, no tests, and no handling of fear or depression. |
| Agent safety and evaluation | 1 | No scenario suite or adversarial tests. Outside my lane. |

Track A average: 10/7 = 1.43

### Track B — pitch
| Dimension | Score | One-line reason |
|---|---|---|
| Problem clarity | 2 | Good patient moment (pitch:5). The headline stat is wrong and "5-minute" is unsourced. |
| Solution credibility | 1 | "Optimal, exact ... with ease" (pitch:17) conflicts with the spec's own safety framing. |
| Evidence | 1 | The only numbers are 80/15 (wrong) and "proven" (not supported). |
| Market and business | 2 | Two channels are named. Pricing is unvalidated (pitch-claims-check:11). The insurer claim is unverified in Thailand (pitch-claims-check:10). |
| Differentiation | 1 | No mention of Movn, Cardihab, hospital programs or LINE programs. |
| Team and feasibility | 1 | No demo, no code (HANDOFF:11), no named clinical partner. |
| Impact and ethics | 1 | No mention of older, rural or low-income users, safety limits, or data handling. |

Track B average: 9/7 = 1.29. Combined average: 19/14 = 1.36 (not ready).

## Findings (most severe first)

### F1 [S0] Medication handling is a one-tap tick, with no safety design
- **What is wrong:** The only medication content is "Evening meds. Tap Done" (spec:103). There is no handling of missed doses, dose changes, polypharmacy, or the rule that the LLM must not give medication advice. The missions also assume the patient takes the same drugs at the same time every day.
- **Evidence:** spec:103; spec:114 (Q6, scope open); spec:15 (medications collected, but no stated use). The only drug-exercise content is beta-blockers (qa:35-43). Nitrates, diuretics, antiplatelets, anticoagulants and BP drugs are not addressed in any artifact (`UNSOURCED`, `NEEDS REAL EXPERT`).
- **Failure scenario:** A patient ticks "meds done" without taking them. The app records adherence and the insurer sees a false signal. Or the patient asks the chat "can I skip my aspirin today?" and the LLM answers. Or a diuretic dose is changed, the patient is dehydrated or hypotensive on a walk, and the app pushes the same mission.
- **Fix:** Make meds an out-of-scope or tightly scripted feature in v1. Add an explicit rule that the agent never advises on drugs and always routes drug questions to the pharmacist or doctor. Treat a tick as self-report only. Add a "dose changed or new drug" prompt that pauses exercise missions and flags the clinician.
- **Needs real expert?** yes (cardiology plus a clinical pharmacist).

### F2 [S0] Red-flag path stops at "show a message"; no way to tell the patient reliably
- **What is wrong:** The design says the app sends no coaching and says call 1669 (spec:73). It does not say how a symptom reaches the app. If the patient is mid-walk with a phone in a pocket, or an older patient is typing into a chatbot, the stop message may never be seen. The same chat could also let a patient describe chest pain and get a conversational reply.
- **Evidence:** spec:73, spec:94; the check-in is conversational (spec:16, spec:101). The qa:61 EMS and location protocol is not adopted.
- **Failure scenario:** A 66-year-old patient types "my chest feels a bit tight but I'll finish the walk" into the weekly check-in. A text-based trigger is not specified, so the LLM replies supportively.
- **Fix:** Put a permanent "I feel unwell" button on every mission card and the watch notification. Define a keyword and phrase list (Thai and English) that pre-empts the LLM in any chat turn. The first response must say "stop, sit down, call 1669". Test it with Thai colloquial phrasing ("แน่นหน้าอก", "ใจสั่น", "เหนื่อยผิดปกติ"). The Thai word list is my suggestion and needs a native-speaking clinician to validate.
- **Needs real expert?** yes (cardiologist; Thai clinical language).

### F3 [S1] Eligibility gate exists only in research; depression and fear are not screened
- **What is wrong:** Depression is a high-risk criterion in qa:89, and low risk requires "absence of clinical depression" (qa:74). The spec's onboarding has no depression screen, no LVEF or ICD question, and no explicit post-event timing check. The "brainless" framing does nothing for post-MI fear of exertion, which in my experience is a main reason patients stop moving (practitioner observation, `UNSOURCED`).
- **Evidence:** spec:14-17; README:18; qa:74, qa:89. Social support and depression are tied to Thai readmission outcomes in the market report (market report line 11), single-source, unverified.
- **Failure scenario:** A depressed, frightened post-MI patient is enrolled, mutes the app in week 1, and nobody notices. Or a patient with an ICD joins through the free B2C route and receives a walking mission.
- **Fix:** Add a hard onboarding gate with LVEF, ICD, recent event or procedure date, and a short validated depression screen. Choose the instrument with a clinician, and I will not name one as Thai-validated (`NEEDS REAL EXPERT`). Outside the safe class, show "please ask your cardiology team first" and stop. Add one fear-of-exercise reassurance mission in week 1.
- **Needs real expert?** yes (cardiologist, rehab, psychiatrist or psychologist).

### F4 [S1] Week-3 reality for a 55-75-year-old Thai user: onboarding and chat design assume too much
- **What is wrong:** The journey begins with demographics forms plus an AI chat that agrees goals "as a conversation" (spec:15-16). Limits may be "scanned from discharge note" (spec:82). The user is assumed to own a smartphone and often a smartwatch (spec:47). Thai language is an open question (spec:115, Q7). Older and rural patients are not mentioned anywhere in the spec. The market report says rural patients have lower education and income (market report line 39) and 64.8% earn <=10,000 THB/month (market report line 115, source not checked).
- **Evidence:** spec:14-17, 47, 82, 115; market report lines 39, 115, 189.
- **Failure scenario:** The patient's daughter sets up the app. In week 2 the daughter is not around. The patient cannot restart a lost notification setting, does not trust a chatbot with medication questions, and quietly stops. The family never hears about it.
- **Fix:** Make Thai the primary language and test the wording with real patients aged 60+. Offer a caregiver role (set-up, one weekly summary, an alert if the patient has been silent N days). The market report already proposes LINE caregiver alerts (market report line 189) and the spec leaves them out. Add a no-watch mode (phone only, RPE and talk test, per qa:26-31). Run a 5-patient "use it alone on day 14" test before building more.
- **Needs real expert?** no for the usability test; yes (Thai health-literacy specialist) for wording.

### F5 [S1] Notification and mission load has no design; two daily pushes plus streaks can backfire
- **What is wrong:** Notification fatigue is listed as an anti-goal (spec:65) but the example week already has two pushes a day (spec:102-103) plus streak framing (spec:104). Nothing says what happens after a missed day or a bad-week streak break, which can discourage a frightened patient. Nothing covers quiet hours, Buddhist observance days, Ramadan or other fasting (evening-meds timing at 20:00 can clash with fast-breaking times), or Thai heat and PM2.5, which bear on a "12:30 walk" (spec:102). All of this is my practitioner observation, `UNSOURCED`, `NEEDS REAL EXPERT`.
- **Evidence:** spec:65, 101-105.
- **Failure scenario:** The patient mutes the app on day 9 after one missed walk and a "streak lost" message. A Muslim patient is told to take evening meds and walk at a time that conflicts with fasting.
- **Fix:** Let the patient choose the walk time and meal-linked anchors ("after breakfast" instead of a clock time). Replace streaks with a non-punitive "welcome back" message. Add a weather and heat check that skips or shifts the mission. Define a mute-detection rule that tells the caregiver or clinician. Test the plan against fasting periods with a real patient.
- **Needs real expert?** yes (cardiac nurse; cultural advisor).

### F6 [S1] Freemium timing and peer communities do not fit the clinical course
- **What is wrong:** One free week and then a paywall (pitch:27) puts the first and riskiest unsupervised week behind a free preview, then asks an older patient to pay 499 THB while the Thai guideline says start rehab within 10 days (qa:143) and programs run about 12 weeks (qa:149 for the LINE study). The peer-community feature (pitch:17) is not in the spec's design at all (only spec:24). No moderation, privacy, or risk-class matching is defined. Peers can give drug or exercise advice, and shared-goal comparison can push a frail patient to overreach. The "social support" evidence is a correlational readmission model, not a peer-group trial (pitch-claims-check:8).
- **Evidence:** pitch:17, 27; spec:24; pitch-claims-check:8, 11; qa:143.
- **Failure scenario:** A week-2 patient hits the paywall, has no plan, and drifts back to no exercise. Or a group chat tells a patient on blood thinners to "just walk it off".
- **Fix:** Decide what is free for safety (at minimum the safe limits, the red-flag button and the eligibility gate). Do not make safety features a paid tier. Hold the peer feature out of v1, or run it as a moderated, risk-class-matched, no-advice group with a clinician or nurse moderator.
- **Needs real expert?** yes (insurer or pricing advisor; nurse moderator).

### F7 [S1] Pitch overclaims and a wrong headline stat (G4)
- **What is wrong:** The pitch still contains "optimal, exact plan ... with ease", "proven tool to reduce readmission rates", and 80%/15%. Each is already flagged by the team (spec:35-40, pitch-claims-check:5-9).
- **Evidence:** pitch:7, 17, 25; pitch-claims-check:5, 9.
- **Failure scenario:** A judge asks "proven how?" and the team has no answer. A nurse on the panel hears "exact plan" and thinks this is unsafe.
- **Fix:** Apply the suggested rewrites in spec:37-38. Use "93% / 15%, Italian GPs" with citation (pitch-claims-check:5) or cut the numbers. Drop "with ease". Add one sentence: "limits are set by your cardiologist, the app only schedules inside them". The "Italian GP survey" number is the team's claim from the review cited there. I have not checked the primary source.
- **Needs real expert?** no.

### F8 [S2] The "5-minute consultation" and the home-safety evidence are carrying more weight than they can
- **What is wrong:** "5-minute consultation" is unsourced (pitch-claims-check:6). The safety meta-analysis (qa:127-136) is for supervised or telemonitored CR in low-to-moderate-risk patients, and the SAE interval (RR 1.30, 95% CI 0.63-2.67, qa:135) is wide. It does not show that an unsupervised, LLM-mediated app is safe. The spec's rule 5 says "confirm with mentor" (spec:69, 75), and no one is named.
- **Evidence:** pitch:7; qa:127-136; pitch-claims-check:6.
- **Fix:** Cite the evidence as "supervised or telemonitored, low-to-moderate risk" and say so aloud. Ask the Siriraj mentor for the local consult length.
- **Needs real expert?** yes (cardiologist, statistician for the interval).

### F9 [S2] Cheapest retention experiment is missing
- **What is wrong:** No test plan for week-3 use. A rehab nurse would run this cheaply before any build.
- **Fix:** Take 8-10 post-MI patients (outpatient clinic, with ethics approval and mentor sign-off). Run a 3-week Wizard-of-Oz version: a nurse sends the same 1-2 missions through LINE. Measure daily replies, day-14 and day-21 drop-off, and what patients say when they stop. This also gives the Thai willingness-to-pay data that is missing (README:35).
- **Needs real expert?** yes (ethics review before any real patient).

### F10 [S3] Minor
- Pitch says "chronic cardiovascular condition, like recovering from a myocardial infarction" (pitch:5), mixing a chronic condition with an acute event. The "mission" and "brainless" vocabulary may read as flippant to patients after a life-threatening event. Test Thai naming. The 💊 emoji in the example (spec:103) is fine for the demo but may confuse low-vision or older users, so use text too.

## What I could not verify
- Every guideline value in qa (HRR ranges, RPE 11-14, 7 METs, LVEF cut-offs, SBP stop thresholds). I did not check them against primary guidelines and they are labeled machine-generated (qa:1). That is S2's job.
- The Italian GP survey and all Thai statistics (12.5%, 83.3%, beta = -0.225, 64.8%). I only have the team's citations.
- Whether Thai-validated depression, health-literacy or fear-of-exercise instruments exist and which to use (`NEEDS REAL EXPERT`).
- Drug-exercise interactions beyond beta-blockers (nitrates, diuretics, anticoagulants, antiarrhythmics).
- Thai FDA SaMD status, PDPA, insurer data-sharing (S4's lane).
- Whether the Thai red-flag phrase list in F2 is clinically adequate.
- The market report was skimmed with targeted reads. Its LINE and caregiver text (line 189) is a model suggestion, not evidence.
