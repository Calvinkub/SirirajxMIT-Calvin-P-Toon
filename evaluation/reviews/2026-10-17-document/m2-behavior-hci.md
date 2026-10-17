# m2-behavior-hci review — document — 2026-10-17

> Simulated review by a language-model role-play. Not a real clinician or institution.

**Artifacts read:** docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md (design), docs/pitch-script-draft1.md (pitch), HANDOFF.md, research/README.md, research/pitch-claims-check.md; skimmed research/market/notebooklm-deep-report.md (market).
**Gate result (my view):** FAIL (G4 fails in the pitch script as written; G1, G3, G5, G6 are NOT-DEFINED)

Line references for the design file use the numbering of the file itself.

## Safety gates
| Gate | Status (PASS / FAIL / NOT-DEFINED) | Evidence (path:line) |
|---|---|---|
| G1 Limits | NOT-DEFINED | Intent is stated (design:71, :74), but the limit schema covers only HR, RPE and activity type (design:71). Duration and progression are not bounded, yet the weekly check-in lets the patient choose "keep 10 min or try 12?" (design:101). Nothing proves the AI cannot raise load. |
| G2 Red flags | PASS (design only) | Deterministic, no LLM, "Stop now and call 1669" (design:73, :94). Caveat: the symptom intake that triggers it is undefined. The Today screen is "one-tap done" (design:85) and has no symptom prompt. The pitch is silent. |
| G3 Eligibility | NOT-DEFINED | The risk-class gate exists only in research/README.md:18. It is not in design §5 or §6, and the target user list includes heart failure and high-risk hypertension (design:46). The pitch is silent. |
| G4 Claims | FAIL (pitch); PASS (design) | Pitch: "optimal, exact plan" (pitch:17), "proven tool to reduce readmission rates" (pitch:25), 80%/15% (pitch:7). The design review table already flags these (design:35-39) but the script has not been revised. |
| G5 Accountability | NOT-DEFINED | "Confirm with Siriraj clinical mentor" (design:70). No named limit owner. Open question 8 asks whether the clinician sees anything (design:117). No consent design for wearable data or insurer access. |
| G6 Failure mode | NOT-DEFINED | Nothing on what happens when watch data, network or model is down, or when the patient goes silent for several days. |

## Scores (0-4)

### Track A (design and system)
| Dimension | Score | One-line reason |
|---|---|---|
| Clinical validity | 2 | Rules are sensible (RPE, beta-blocker caution) but are an unverified draft (design:70). |
| Patient safety | 2 | Known paths are covered (red flag, no self-raising of limits), but there is no hazard analysis and no streak/pressure hazard review. |
| Evidence and sourcing | 2 | The design is honest about UNSOURCED and guess items. There is no behavior-change evidence at all for the core "brainless micro-mission" bet. |
| Feasibility | 2 | There is no code (HANDOFF:11). The limit source for the demo is open (design:111). The Thai-language agent and wearable bridge are unproven. |
| Regulatory and privacy | 1 | SaMD risk is noted (design:75) and PDPA is mentioned only in the market report. There is no consent or data-flow design. |
| Behavior and adherence | 1 | Several plausible ideas (one-tap, streak, weekly summary) but no retention logic, no dropout assumptions, no test plan, and an undefined peer feature. |
| Agent safety and evaluation | 1 | The architecture split is good (design:97). There is no scenario suite, adversarial test or regression plan. |
**Track A average: 1.57 (needs major work)**

### Track B (pitch)
| Dimension | Score | One-line reason |
|---|---|---|
| Problem clarity | 2 | There is a clear patient moment ("leave the clinic", pitch:5), but the gap statistic is mis-framed (pitch-claims-check:5) and the "5-minute consult" is unsourced. |
| Solution credibility | 1 | "Optimal, exact ... with ease" and CPET-centered inputs contradict the "no CPET / brainless" reality. The "brainless" angle and the micro-missions are absent from the script. |
| Evidence | 1 | Headline numbers are wrong or unsourced. "Proven" is unsupported. No limits are stated. |
| Market and business | 1 | The 499 THB price has no Thai willingness-to-pay data (pitch-claims-check:11). Insurer demand is unverified in Thailand (pitch-claims-check:10). |
| Differentiation | 1 | The script names no competitor. EXPERT, Movn, Cardihab and LINE programs appear only in the design and research. |
| Team and feasibility | 1 | No demo and no named clinical partner (HANDOFF:11). |
| Impact and ethics | 1 | Safety, data handling and equity (older, rural, low-income users) are not mentioned. |
**Track B average: 1.14 (not ready)**

**Combined average: 1.36 (not ready).**

## Findings (most severe first)

### F1 [S1] The paywall lands at day 7, before any habit can form
- **What is wrong:** Freemium gives "one-time 1-week schedule", then Premium (pitch:27). Habit formation in the literature takes weeks to months (Lally et al. 2010 reported a median of about 66 days, with wide variation; recalled from memory, verify the citation). The user decides to pay before the behavior is automatic, and during the post-MI period of fear and low mood. If the free week is the only experience, week-4 retention is mostly a conversion question.
- **Evidence:** pitch:27; design:101-105 (no habit-support or lapse-recovery logic beyond a streak). No dropout or conversion data anywhere in the repo, so any retention number is `UNSOURCED`.
- **Failure scenario:** The patient completes 6 of 7 walks, is shown a paywall, lacks a reason to pay, and drops. Or an insurer-sponsored patient never sees it, so B2C funnel data tells you nothing about B2B2C engagement.
- **Fix:** Make the free tier the first 4 weeks of core missions and gate the extras (peer group, caregiver reports, adaptation) instead. Alternatively, test paywall timing as an experiment arm (see the experiment below).
- **Needs real expert?** yes (behavioral scientist / pricing).

### F2 [S1] The "brainless" promise conflicts with the chat-first, form-heavy onboarding for 55-75-year-olds
- **What is wrong:** The journey needs demographics, medications, clinician limits "entered or scanned from discharge note" (design:83), then a free-text goal conversation with an LLM (design:16, :82), all before the first mission. The design never says who types what, in which language (open question 7, design:115), or at what reading level. Older, low-literacy or rural users (market:39, :115) are the people the pitch says are underserved.
- **Evidence:** design:14-17, :83, :115. No accessibility requirements (font size, voice, caregiver-assisted setup) appear in any artifact.
- **Failure scenario:** A 68-year-old post-MI patient is asked to chat in Thai about goals with a bot. They give up at step 3, or a family member fills it in with guessed limits (a safety problem, not only an engagement one).
- **Fix:** Time-to-first-mission target (for example under 3 minutes). The clinic or a caregiver does limit entry. Replace goal chat with 3 tap-choices in v1. Keep chat optional. Write Thai-first accessibility requirements.
- **Needs real expert?** yes (Thai geriatric nurse / HCI researcher; see S3).

### F3 [S1] Streaks and "tap Done" can push post-MI patients to exercise through symptoms, and self-report is the adherence signal
- **What is wrong:** Streak and completion framing (design:104) are standard engagement levers, but for this population a broken streak is a reason to walk when unwell, tired, or after a skipped red-flag symptom. Daily symptom check-in is not part of the mission card. The watch "confirms the walk" (design:103) but a heart rate trace does not confirm RPE or symptoms.
- **Evidence:** design:73, :85, :103-104. G2 trigger input is undefined.
- **Failure scenario:** Day 12 of a streak, patient feels dizzy, does not want to lose the streak, taps Done anyway. The app logs success and the weekly summary praises adherence.
- **Fix:** Pair every exercise card with a 2-option symptom/RPE tap ("fine / not fine") that gates the Done button. Use "restart without penalty" language and a weekly (not daily) consistency measure. Have S1/S2 review the copy. Never reward intensity.
- **Needs real expert?** yes (cardiologist, rehab physician).

### F4 [S1] Pitch makes unsupported claims that judges will probe, and the script omits the behavior layer that is the actual product
- **What is wrong:** "Optimal, exact plan", "proven tool", and 80%/15% (pitch:7, :17, :25) are unsupported or wrong (pitch-claims-check:5, :9). The script never says "tiny daily missions", which is the differentiator in the design (design:29, "Brainless missions alone sounds unsafe" and "Precise prescription alone sounds like a document"), so the script sells a prescription document generator.
- **Evidence:** pitch:7, :17, :25; design:30, :35-39; pitch-claims-check:5-9.
- **Failure scenario:** A judge asks "proven how?" or "how is this different from a PDF plan?" and the team has no behavior-change answer.
- **Fix:** Apply design:37-39 rewrites, cite 93%/15% (Italian GPs) with source or cut it, and add one sentence of the mission mechanic with a patient-moment example.
- **Needs real expert?** no.

### F5 [S2] Peer-community feature is undesigned, and the evidence cited for it is the wrong kind
- **What is wrong:** The pitch says peer communities ensure adherence (pitch:17). The repo support is a Thai cross-sectional association of social support with readmission (beta = -0.225; market:11; README:21). That is correlational, about support in general, and not a trial of peer groups. Risks not addressed: peers advising "push harder", moderation, PDPA for a group sharing health data, shame comparisons.
- **Evidence:** pitch:17; pitch-claims-check:8 ("Plausibly supported", not a trial); market:189 (family caregiver via LINE is the stronger-evidence route the report itself proposes). Peer-group effect size on adherence: `UNSOURCED`.
- **Failure scenario:** A 60-year-old is added to a group where a faster peer posts 5 km walks. The patient exceeds their limit to keep up.
- **Fix:** Reframe as family/caregiver summaries via LINE for v1 (lower risk, aligned with the Thai evidence). Defer open peer groups until moderation and limits-in-peer-view are designed. Say "supports", not "ensures".
- **Needs real expert?** yes (cardiac nurse; lawyer for PDPA).

### F6 [S2] Notification and just-in-time design is fixed-time, not adaptive, and has no fatigue plan
- **What is wrong:** An anti-goal is "mute within a week" (design:65), but the only mitigation is "1-2 missions per day". Pushes are fixed at 12:30 and 20:00 (design:102-103). There is no rule for missed days, "do not disturb", heat or rain, context (already walked), or escalating down to silence. Meds reminder and exercise ping are two distinct pushes at a time when the patient already has many pills and appointments. The week adapts weekly (design:17), not daily, so this is not yet a just-in-time adaptive intervention.
- **Evidence:** design:65, :102-103. No dropout assumptions or notification rate caps.
- **Failure scenario:** Patient misses 3 days, app continues the same two pings, patient mutes the app on day 9.
- **Fix:** Add a lapse protocol (after 2 misses, 1 gentle low-bar mission; after 5, ask "what got in the way?" with 3 taps; after 10, notify the caregiver or clinician if consent exists). Add a rate cap and quiet hours. Let the patient choose time slots at onboarding.
- **Needs real expert?** no for the design; yes for clinical escalation rules.

### F7 [S2] No evidence is cited for the micro-mission / implementation-intention approach, and no engagement metrics are defined
- **What is wrong:** The whole bet rests on small cued daily tasks. The design uses the right shape ("walk 10 min after lunch" is an if-then cue, design:53), but no behavior-change source is cited (for example implementation-intention or digital cardiac-rehab engagement literature), and no target such as week-4 active rate is defined.
- **Evidence:** `UNSOURCED` across design, HANDOFF and research. Cardihab completion figures 25-40% to 70-85% are vendor data (market:61-62; README:32).
- **Failure scenario:** Insurer asks "what retention do you expect at 12 weeks?" and the only answer is a vendor's marketing number.
- **Fix:** Add a short evidence note for 2-3 real behavior-change sources and flag them as unverified until checked. Define metrics: day-28 retention, missions completed per active week, time to first mission, mute rate.
- **Needs real expert?** yes (behavioral scientist, to confirm the literature).

### F8 [S3] "Brainless" is a risky word for the pitch and for the patient
- **What is wrong:** It sounds like removing patient understanding. It conflicts with patient autonomy, trust and clinical review, even if the intention is "no data interpretation".
- **Evidence:** design:10, :30.
- **Fix:** Use "effortless" or "one clear step a day" in public copy. Keep "brainless" internal.
- **Needs real expert?** no.

## Biggest threat to week-4 retention and cheapest experiment

**Threat:** The combination of F1 and F2 and F6: a heavy first-run, a paywall at day 7 before habit forms, and a fixed-schedule ping stream with no lapse recovery. Post-MI fear and low mood (the cardiac nurse's area, S3) amplify all three. This is my judgement, not measured.

**Cheapest experiment (no app, no code, about 2-3 weeks to run):** A concierge/Wizard-of-Oz pilot. Recruit a small convenience sample of post-MI patients from the Siriraj rehab clinic, with clinician-set limits entered by staff (NEEDS REAL EXPERT and IRB/ethics check before any real patient contact). Deliver one tap-style mission a day through LINE, written by a human from a fixed library inside the limits. Randomize between two arms: (A) fixed 12:30 ping, with streak; (B) patient-chosen time, symptom tap, and the lapse protocol of F6. Measure day-28 active rate, mission completion, time-to-first-mission and "would you pay" at week 4 and after the free week. This tests feasibility and engagement signal only. It will not prove efficacy, and the sample is too small for statistical claims; do not report it as such.

## What I could not verify
- All guideline and clinical thresholds (NEEDS REAL EXPERT: S1, S2).
- Whether the cited Thai studies (PMC10353658, PMC8894994, PMC11456183) say what the market report claims. I read the report, not the sources.
- The Lally habit-formation figure and any behavior-change literature I name. They are from memory and not in the repo.
- The market report's competitor rows and any dropout benchmark for digital cardiac rehab. None is sourced in the repo (README:33).
- Whether LINE can legally and technically carry health content and PDPA-compliant consent (NEEDS REAL EXPERT: lawyer).
