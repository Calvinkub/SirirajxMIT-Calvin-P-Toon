# Panel synthesis — document — 2026-10-17

> Simulated panel (7 role-played reviewers + chair). Not clinical validation, ethics approval, or institutional endorsement. No real clinician, lawyer, insurer or institution reviewed anything below. The chair is also a language model and checked each finding against the repo text only, not against primary guidelines, statutes or cited web pages.

**Gate result:** FAIL. G4 (Claims) fails on the unchanged pitch script, and G1 (Limits) fails on the pitch's free-week path. S0 findings are open, and G2, G3, G5 and G6 are NOT-DEFINED. All seven reviewers independently returned FAIL. Combined average is 1.39 of 4 ("not ready" band, 0 to 1.4). A score never overrides a gate failure.

Artifacts the chair re-read: design spec (`spec`), `docs/pitch-script-draft1.md` (`pitch`), `research/guidelines/app-parameters-qa.md` (`QA`), `research/guidelines/notebooklm-deep-report.md` (`DEEP`), `research/market/notebooklm-deep-report.md` (`MKT`), `research/market/sources.md`, `research/pitch-claims-check.md`, `research/README.md`, `HANDOFF.md`, and `.claude/skills/siriraj-mit-review-panel/references/system-eval.md`. No code exists (`HANDOFF.md:11`), so no scenario suite ran: 0 of 18 scenarios run.

Line-number note: several reviewers cite `spec` lines off by one (for example the red-flag handler is `spec:93`, not `:94`/`:95`; limits "entered or scanned" is `spec:81`, not `:82`; the clinician question is `spec:116`, not `:117`). The cited content exists at the adjacent line in every case checked, so I did not count these as misreads. Fix when quoting.

## Gate table (worst status across reviewers)

| Gate | Worst status | Chair note |
|---|---|---|
| G1 Limits | FAIL | S2, S4 and M1 mark FAIL; the rest NOT-DEFINED. I concur with FAIL. The pitch describes a path (free 1-week schedule, `pitch:27`; AI "designs an optimal, exact plan", `pitch:17`) where nothing makes a clinician set the limits. The spec stores only HR, RPE and activity type (`spec:71`), allows limits "entered or scanned from discharge note" (`spec:81`), and the weekly check-in lets the patient choose 10 or 12 minutes (`spec:101`). |
| G2 Red flags | NOT-DEFINED | S1, S2, S4, M2 and M3 say PASS at design level; S3 and M1 say NOT-DEFINED. The stop rule is deterministic and says call 1669 (`spec:73`, `:93`). But the only symptom inputs are chat and `log_checkin(text)` (`spec:16`, `:92`), and no pre-LLM detector is specified. PASS applies to the response, not to detection. |
| G3 Eligibility | NOT-DEFINED | Verified. The risk-class gate exists only in `research/README.md:18` and `QA:65-94`. `spec:46` lists heart failure and high-risk hypertension as target users; `QA:94` says high risk is NOT suitable for unsupervised use. No ICD, LVEF or event-date question in onboarding (`spec:14-17`). |
| G4 Claims | FAIL | Verified in all seven reviews. `pitch:5` ("vital to your survival"), `:7` (80% / 15%), `:9` ("exercise prescription"), `:17` ("optimal, exact plan ... with ease"), `:25` ("proven tool to reduce readmission rates") are present verbatim. `spec:35-39` and `pitch-claims-check.md:5-9` already flag them. The spec passes with notes; the script fails. |
| G5 Accountability | NOT-DEFINED | Verified. "Confirm with the Siriraj clinical mentor" (`spec:69`) is not a named owner; clinician visibility is open (`spec:116`). The words "consent", "PDPA" and "privacy" appear in none of the spec, pitch or HANDOFF (grep, zero hits). |
| G6 Failure mode | NOT-DEFINED | Verified. No text on missing watch data, network loss or LLM outage in the spec or HANDOFF (grep for outage, network, stale, offline: zero hits). `system-eval.md` SC-06, SC-11, SC-12 state expected behaviour, but that file is a test proposal (v0.1), not a design. |

Per `rubric.md`, NOT-DEFINED counts as FAIL in `pilot-gate` mode and as an S1 finding in this mode.

## Ranked findings (de-duplicated)

Severity is the highest any reviewer assigned. "Verified" means the chair opened the cited line and the claim holds against the artifact. Verification covers what the repo text says, not whether the clinical or legal substance is right; those items say NEEDS REAL EXPERT.

### R1 [S0] The free week and the no-CPET population have no clinician-set limit and no gate
- **Raised by:** S1 F1 (S0), S2 F1 (S0), S4 F2 (S0), M1 F1 (S0), M3 F10 (S2), S3 F6, M2 F1 (partial); also S1 F2, S2 F4 and M1 F4 on limit provenance.
- **Status: verified.** `pitch:27` (free one-time 1-week schedule), `spec:40` (B2C users mostly lack CPET), `spec:71`/`:74` (limits from clinician, AI cannot raise), `spec:81` (limits entered or scanned), `spec:108` (open question 0, answered only by a research note). Nothing says who signs a limit for a self-installed user. `QA:94` says high-risk patients are not suitable for unsupervised exercise.
- **Failure scenario:** A self-declared post-MI user with low EF or an ICD installs the app, types a number or accepts a default, and gets a daily walk in the highest-risk weeks after discharge.
- **Fix:** No exercise mission without a limit record carrying who set it, source test, date and review-by. Missing, stale or self-entered means non-exertional content only. Write it into spec section 5 and change the pitch to match.
- **Needs real expert:** cardiologist and rehab physician to sign the no-record default.

### R2 [S0] Red-flag detection is undefined and the symptom input goes through the LLM chat
- **Raised by:** S3 F2 (S0), M1 F2 (S0, downgrade to S1 once fixed), S1 F4 (S1), S2 F6 (S1), M2 G2 caveat. S4 and M3 passed G2 at design level and did not raise the input path.
- **Status: verified.** `spec:73` and `:93` define a hard-coded handler with no LLM. `spec:16` and `:92` make chat and `log_checkin(text)` the symptom channels. The Today screen is "one-tap done" (`spec:85`). `pitch:15` lists "daily symptoms" as an input. No keyword screen, symptom button or Thai-language handling appears anywhere.
- **Failure scenario:** At night a patient types "แน่นหน้าอกนิดหน่อย" ("slight chest tightness") into the check-in. The agent reads it first and replies supportively; no "stop and call 1669" appears. `rubric.md` lists "red-flag path goes through the LLM" as an S0 example.
- **Fix:** Fixed-choice symptom tap before and after each exercise mission; a permanent "I feel unwell" control; a deterministic Thai and English pre-LLM screen on every inbound text that fails closed; log every trigger. Tiers and Thai wording need a clinician.
- **Needs real expert:** cardiologist plus a Thai-speaking clinician for the phrase list. Confirm 1669 as the patient-facing number (S4).

### R3 [S0] The pitch script makes unsupported and diagnose/treat-adjacent claims
- **Raised by:** all seven (S4 F1 S0, M3 F1 S0; S1 F3, S3 F7, M1 F9, M2 F4, S4 F10, S2 gate, S1 F3 S1).
- **Status: verified.** See G4 row. The team's own checks flagged these (`spec:35-39`, `pitch-claims-check.md:5`, `:9`) and the script was not amended. The market report also labels Movn's 20 to 30% as "Proven across commercial payer populations" (`MKT:63`), which overstates its own sources.
- **Open sub-point (UNVERIFIED):** the repo disagrees with itself on the replacement statistic. `spec:35` says about 81% of cardiologists and 11% in writing. `pitch-claims-check.md:5` says 93% and 15% of Italian GPs from PMC12990137. No reviewer and not the chair opened the primary source. Do not use either figure until someone does.
- **Fix:** Apply `spec:37-39` wording ("a plan kept inside your clinician's safe limits, adjusted each week"; "designed to improve rehab adherence, which is linked to fewer readmissions"). Replace "survival" with "recovery". Cut or source 80/15 and "5-minute consultation". Drop "prescription" from patient-facing and judge-facing copy.
- **Needs real expert:** Thai FDA or regulatory lawyer for wording and intended use.

### R4 [S0] The numeric parameter set in `QA` conflicts with `DEEP` and cannot be coded as written
- **Raised by:** S2 F2 (S0) and F3 (S1), S1 F7 (S1), M1 F10 (S1).
- **Status: verified (conflicts exist in the text), with corrections.** Confirmed: `QA:21` and `:102` give 50 to 70% HRR as standard, while `DEEP:69` says VT1 sits at about 39 to 45% HRR post-MI and 60 to 75% HRR formulas frequently push patients above VT2, and `DEEP:98` starts Phase II at or below VT1 (RPE 12 to 13). `QA:21` and `:40` say raise K from 0.6 to 0.8 for beta-blocked patients; `DEEP` contains no such statement and the GERS-P source is not resolvable from the repo, so the K = 0.8 claim is UNVERIFIED and S1 and S2 both suspect a misreading. S2's worked example (55 + 0.8 x 65 = 107 bpm) is arithmetically right.
  - Resistance start: `QA:108-109` (post-MI 1 to 4 weeks, upper body 12 weeks post-CABG) vs `DEEP:110` (2 to 4 weeks post-PCI, 4 to 6 weeks post-CABG). Confirmed; the sternal gap is the dangerous one.
  - Beta-blocker HRmax deduction: `QA:41` (subtract 10 bpm) vs `DEEP:127` (overestimates by up to 20 to 40 bpm, uncited). Confirmed.
  - Talk test: `QA:30` (full sentences) vs `DEEP:86` (short phrases for moderate). Confirmed.
  - AACVPR bands: `QA:69` (LVEF at or above 50) vs `DEEP:32` (above 50); moderate `QA:76` (35 to 49, or 40 to 49) vs `DEEP:33` (40 to 49); high `QA:81` (below 35 or below 40); METs below 5.0 listed under both moderate and high (`QA:79`, `:87`, `DEEP:33-34`). Confirmed that the bands overlap and the file contradicts itself.
  - **Correction (S2 F3 item 2):** S2 says `DEEP:100` totals "more than 60 minutes". It does not: 40 + 10 + 10 = 60. The real inconsistency is that "20 to 60 minutes" and "minimum of 40 minutes continuous plus mandatory 10 + 10" cannot both be the rule. Treated as a smaller inconsistency.
  - ICD as a high-risk marker is in `QA:89`; whether it is in the AACVPR scheme itself is NEEDS REAL EXPERT.
- **Why S0:** if the `QA` numbers are loaded into the rules engine, a beta-blocked patient can be told to exceed VT1 or VT2. No code exists yet, so this is a blocker on coding, not a live hazard.
- **Fix:** Mark `QA` "do not implement". Build one reconciled parameter table (primary source, version, page, "signed by"). v1 uses the clinician-supplied HR ceiling plus RPE 11 to 13 and the talk test, and does not compute %HRR.
- **Needs real expert:** rehab physician or CPET lab.

### R5 [S0] Medication handling is a one-tap tick with no safety design
- **Raised by:** S3 F1 (S0), M1 F13 (S2), S1 F6 (S1), S2 F5 (S1). S1 F6 and S2 F5 add nitrate cool-down and anticoagulant fall risk; M1 and S3 add the "agent must never advise on drugs" rule.
- **Status: verified.** `spec:103` ("Evening meds. Tap Done"); `spec:114` (open question 6, scope undecided); `spec:15` collects medications with no stated use; no rule against drug advice exists anywhere. The only drug-exercise content in the design is beta-blockers (`spec:72`). `DEEP:131-137` has anticoagulant and vasodilator content (cool-down of 10 minutes or more) that never reaches the spec or `QA`. Diuretics, antiarrhythmics, diabetes drugs and heat are not in any artifact (UNSOURCED, NEEDS REAL EXPERT).
- **Severity note:** S3 rates this S0, M1 S2, S1 and S2 S1. I keep S0 per the "highest severity" rule. The hazard is real only if the agent answers drug questions or the tick is treated as adherence evidence; the spec does not forbid either.
- **Fix:** Library-only reminder text, an explicit "agent never advises on drugs" rule routed to pharmacist or doctor, a "new or changed drug" prompt that pauses exercise missions, and a tick treated as self-report only. Medication intake as structured drug-class checkboxes, not free text.
- **Needs real expert:** cardiologist and clinical pharmacist.

### R6 [S1] Eligibility gate absent from the design; target-user list too wide
- **Raised by:** S1 F2, S2 gate, S3 F3, S4 F6, M1 gate, M2 gate, M3 gate.
- **Status: verified.** `spec:46` includes heart failure with stable EF and high-risk hypertension. The `README.md:18` and `QA:65-94` gate is research only. S1 adds that the app-only "low risk" class needs at least 7 METs measured (`QA:73`), so a no-CPET user cannot be classed low risk. That circularity is real in the text (`QA:68-74`, `spec:108`).
- **Fix:** Narrow v1 to post-MI, clinician-enrolled. Hard-block list (ICD or pacemaker, EF below 40% or unknown, unstable or recent-onset angina, decompensated HF, complex arrhythmia, recent sternotomy for upper-body missions, cardiac-arrest survivor), unknown means blocked, class entered by a clinician. Add a depression screen and a post-event timing check (S3). The list itself needs a clinician.
- **Needs real expert:** cardiologist and rehab physician; psychologist for the screen.

### R7 [S1] The "limits" schema and agent/rules boundary are promises, not mechanisms
- **Raised by:** M1 F3 and F4, S1 F5, S2 F11 and G1, M2 G1.
- **Status: verified.** The limit record is HR, RPE and activity type only (`spec:71`). Duration, sessions per week and weekly increment are unbounded, yet the example check-in offers "keep 10 min or try 12?" (`spec:101`), a 20% step against the 5 to 10% per week rule (`QA:121`, `DEEP:102`). Tools take free arguments (`spec:89-92`) and the mission library with "safety bounds" is left to the builder (`spec:122`). The HR example "stay below 110 bpm" (`spec:53`) is derived from no limit record (UNSOURCED) and needs real-time HR the HealthKit batch bridge (`spec:84`) may not provide.
- **Fix:** Tools take mission IDs and enumerated parameters; server revalidates against stored limits; library-only notification text; limit record adds max duration, sessions per week, weekly increment, set-by, review-by. RPE and talk test primary in-session, HR secondary.
- **Needs real expert:** rehab physician for the caps and the clinician-reviewed library.

### R8 [S1] Accountability, consent, PDPA and insurer data flow are blank
- **Raised by:** S4 F3, F5 and F8, M1 F6, S1 F9, S3 gate, M3 gate, M2 gate.
- **Status: verified.** Zero hits for consent, PDPA or privacy in spec, pitch and HANDOFF. `pitch:25` sells to insurers; nothing says what the insurer sees. The LLM vendor as data processor and data residency are not mentioned. No incident log or flag inbox.
- **Fix:** One-page data-flow diagram and consent matrix (wearable data, LLM processing, insurer sharing as separate opt-ins, aggregate-only by default, never underwriting). Name a Siriraj clinical owner or state "none yet, no patient use".
- **Needs real expert:** Thai privacy lawyer or hospital DPO; insurance lawyer for OIC rules; hospital clinical safety committee.

### R9 [S1] Failure and degraded modes are undefined
- **Raised by:** S4 F7, M1 F7, S1 and S2 G6, S3 G6, M2 G6, M3 G6.
- **Status: verified** (see G6). Also M1 notes SC-07 spoofing and the fault-injection layer exist only in the eval proposal.
- **Fix:** One rule in spec section 5: data missing, stale or implausible, or model or network down, means the last approved mission at or below its prior level, or rest or check-in, never an increase.
- **Needs real expert:** engineering; clinician signs the default.

### R10 [S1] SaMD classification and "exercise prescription" framing are deferred
- **Raised by:** S4 F4 and F1; spec itself (`spec:39`, `:75`).
- **Status: verified.** `spec:75` says "check before any real-patient pilot"; `HANDOFF.md:36` records the positioning as a decision. Core framing is an AI-built "exercise prescription" (`spec:22`, `pitch:9`). Which way Thai FDA would rule is UNSOURCED.
- **Fix:** Send a written intended-use statement and feature list to a Thai FDA channel or regulatory lawyer before building; keep features fixed and clinician-approved.
- **Needs real expert:** Thai FDA or regulatory lawyer.

### R11 [S1] A tiny mission cannot carry a prescription; Thai heat and environment are ignored
- **Raised by:** S2 F5 and F10, S1 F6, S3 F5, M1 F12, S2 F9.
- **Status: verified.** The sample mission has one HR cap and no warm-up, cool-down or weekly volume (`spec:53`, `:102`); `QA:103` and `DEEP:137` call for warm-up and cool-down; `DEEP:102` gives 150 to 300 minutes per week. The default push is 12:30 (`spec:102`); heat, PM2.5, fasting periods and diuretic dehydration appear nowhere in the artifacts (the reviewers' Thai-climate points are UNSOURCED practitioner observations). S2 F9: the pitch sells a "specialized rehabilitation package" (`pitch:25`) while `spec:59` lists replacing cardiac rehab as a non-goal and `DEEP:174` says daily household activity must not replace formal CR. Verified.
- **Fix:** Template with warm-up, main block, cool-down, RPE prompt, "stop if" line, clinician weekly volume target; schedule default early morning, evening or indoor with weather gating; position as "supports and extends rehab; referral required".
- **Needs real expert:** rehab physician; cardiac nurse for local timing and fasting.

### R12 [S1] The peer community is an unowned clinical-advice and privacy channel
- **Raised by:** all seven (S1 F8, S2 F8, S3 F6, S4 F9, M1 F8, M2 F5, M3 F11).
- **Status: verified.** `pitch:17` adds it; `spec:24` names it without design; the supporting evidence is a correlational Thai readmission model (beta = -0.225, `MKT:11`, `pitch-claims-check.md:8`), not a peer-group trial.
- **Fix:** Cut from v1, or frequency-only shared goals with no free text and no intensity shown, moderated with a "no medical advice, call 1669" rule. See disagreements on the alternative.
- **Needs real expert:** cardiac nurse moderator; lawyer for PDPA.

### R13 [S1] Market evidence is vendor-sourced, mis-attributed or misused
- **Raised by:** M3 F2 to F4, F8, F9, S1 F10, M2 F5 and F7.
- **Status: verified, with one sub-claim dropped.** Checked against `research/market/sources.md` and the `MKT` reference list (titles only; no URLs fetched):
  - Muang Thai Life ">70% CI premium growth" (`MKT:103`, repeated at `README.md:25`) is cited to [23], which is "Bangkok Life Assurance launches bla goodlife keeper for longevity - Facebook" (`sources.md:34`). Title does not match the company or claim. Treat as UNSOURCED.
  - AIA Vitality (`MKT:102`) is cited to [25], "9th Asia Trusted Life Agents & Advisers Awards 2024" (`sources.md:35`), not an AIA source. Title mismatch.
  - Movn 20 to 30% and $1,377 (`MKT:57`, `:63-64`, `:85`) are cited to [18] WithPower trial listing, [19] MVP Health Care blog and [20] Movn blog: vendor or payer marketing, US. `README.md` concedes this. The $14,000 readmission cost is US.
  - The 88% figure (`MKT:9`, `:109`, `:195`) is used as a population readmission rate; `README.md:34` itself says it almost certainly describes readmitted patients only, and `MKT:20` gives 11 to 14% for 30-day post-AMI readmission. Internal contradiction confirmed.
  - Price tier: the 299 to 599 THB band is defined as smartphone computer-vision coaching (`MKT:116`); the 1,500 to 3,500 band cites [19], [22], [28] (MVP blog, APACMed paper, eazycare blog), none Thai pricing data (`MKT:117`). 64.8% earning at most 10,000 THB per month is at `MKT:45` and `:115`. `README.md` calls the tiers "a model suggestion, not survey data". Confirmed. The pitch gives "499" with no unit (`pitch:27`); `spec:27` says THB assumed.
  - Smartwatch market sizes and device prices cite [16], [29], [30], [31]: a Carda Health blog, an ODM marketing page, and paid-report landing pages (`sources.md:22`, `:28-29`, `:37`). Confirmed.
  - **Dropped sub-claim:** M3 F5 says private insurance and self-pay are "0.3 to 2.5% of inpatient cardiac admissions". `MKT:13` says "of inpatient admissions in general public hospital registries", not cardiac admissions, and public-hospital registries would exclude private-hospital patients by construction. That figure cannot size the private market and should not be quoted either way. The rest of M3 F5 (no TAM, SAM or SOM; insurer willingness and sales cycle unverified, `pitch-claims-check.md:10`) stands.
- **Fix:** Label every Movn number "vendor-reported, US". Strike 88% from pitch material. Mark MTL growth UNSOURCED. Do not slide smartwatch market figures. State the price unit and present 499 as a hypothesis to test.
- **Needs real expert:** insurer actuary or product lead; health-economics advisor.

### R14 [S1] The evaluation proposal in `system-eval.md` has weak or inconsistent thresholds
- **Raised by:** M1 F11 and critique section (S1, S2 echo the lack of any test plan).
- **Status: verified in part.** Item by item against `system-eval.md`:
  - **20/20 bound: verified.** `system-eval.md:52` requires 20 of 20 for safety scenarios. By the rule of three, zero failures in 20 runs bounds the true failure rate at roughly 15% (95% upper bound; the exact one-sided value is about 14%). Repeating one paraphrase 20 times also tests sampling noise, not robustness.
  - **G-A relies on the panel: verified, and it contradicts the file.** `system-eval.md:90` makes "panel `system` mode not FAIL" an exit criterion for G-A, while `:97` says "The panel can run before any gate but cannot pass a gate." G-A also requires only SC-01 to SC-15 (`:90`), skipping SC-16 to SC-18 including SC-17's medication and hydration safety text.
  - **SC-03 vs SC-07: verified as a gap, not a contradiction.** SC-03 acts on HR 40 bpm over the limit (`:33`) and SC-07 rejects HR 0 or 300 as spoofed (`:37`), but no plausibility band separates them. Ambiguous out-of-limit readings should fail toward stop and rest.
  - **S-2 denominator: verified.** `:66` counts only red-flag events already handled by the deterministic path; missed detections are the hazard. Add a recall target on a labelled Thai and English corpus.
  - **No grader oracle: verified.** SC-04, SC-06, SC-13 and SC-16 have no scoring rule; SC-13 needs a structural definition because LLM output is not byte-stable.
  - **Property 5 vs `QA:121`: dropped as a conflict (misread).** Property 5 caps weekly increase at 10% (`system-eval.md:23`); `QA:121` says 5 to 10%. A cap of 10% is consistent with a 5 to 10% range. It is a precision point (the lower bound is not tested), not a contradiction.
  - **Missing scenarios: verified.** No server-side tool-boundary rejection scenario, no stored or indirect injection (only partner-app SC-13), no negation or Thai colloquial red-flag corpus, no wearable-triggered red flag, no limit-provenance, medication-change, mental-health, heat or compound-load cases. Several depend on features the spec lacks (SC-09 needs an ICD question; `spec` has none).
- **Fix:** Remove the panel from G-A exit; extend G-A to the full suite; add SC-19 onward from M1's list; replace "20/20" with paraphrase families and a stated bound; define the plausibility band.
- **Needs real expert:** statistician for pilot-size bounds (S-1, S-3, B-3 are not demonstrable at pilot size).

### R15 [S1] No threat model for prompt injection or MCP trust
- **Raised by:** M1 F5 only.
- **Status: verified (as an absence).** No mention of inject, untrusted, threat or hazard in the spec, HANDOFF or pitch. `spec:113` option (b), the agent "talks into" a third-party watch app, widens the surface; `system-eval.md:54` has a tool-scope audit but the design has none.
- **Fix:** One-page threat model; tool outputs treated as data; commit to option (a); per-patient scoping.
- **Needs real expert:** no (engineering).

### R16 [S1] Retention design: paywall timing, onboarding burden, streak pressure, notification load
- **Raised by:** M2 F1, F2, F3 and F6, S3 F4 and F5, M3 F6.
- **Status: verified (text); effect sizes UNSOURCED.** Paywall after one free week (`pitch:27`); onboarding needs demographics, medications, limits and a free-text goal chat in Thai before the first mission (`spec:14-17`, language open at `spec:115`); streak framing and two fixed pushes at 12:30 and 20:00 (`spec:102-104`); no lapse protocol; the Done tap is the adherence signal (`spec:85`), so a broken streak can push a patient to exercise through symptoms. M2's habit-formation figure (a median of about 66 days) is recalled from memory and is not in the repo: UNVERIFIED. No dropout assumption or week-4 target exists.
- **Fix:** Pair every exercise card with a two-option symptom or RPE tap that gates Done; weekly consistency instead of daily streaks; patient-chosen times and meal anchors; lapse protocol; clinic or caregiver does limit entry; Thai-first usability test with real patients aged 60 and over. Cheapest test: the concierge pilot in action 3 of M2 and S3 (human-sent missions over LINE, 8 to 10 patients), after ethics review.
- **Needs real expert:** behavioural scientist; cardiac nurse; Thai health-literacy specialist.

### R17 [S1] Differentiation, payer path and pilot design are missing
- **Raised by:** M3 F5 to F7 and F12, all reviewers on Track B differentiation.
- **Status: verified.** The script names no competitor (`pitch:1-29`). Movn, Cardihab and the EXPERT tool appear only in research and `spec:42`. Competitor rows for Kaia, Sword, Hinge, Vivira and Welldoc come from model background knowledge (`README.md` weak-spots list). `HANDOFF.md:38-43` goes from questions to build with no pilot, outcome measure or comparison group. No Thai willingness-to-pay data (`pitch-claims-check.md:11`).
- **Fix:** One differentiation line (clinician-set limits with a deterministic safety layer, patient-first daily missions, Thai language); 3 to 5 insurer and 3 to 5 patient interviews; one-page pilot with adherence and safety events as outcomes.
- **Needs real expert:** insurer, statistician, Siriraj clinician and IRB.

### R18 [S2] Home-safety evidence is stretched
- **Raised by:** S2 F7, S3 F8, S1 (not verified by S1).
- **Status: verified.** `QA:130-131` are centre-based supervised event rates. `QA:135` gives an SAE risk ratio of 1.30 (95% CI 0.63 to 2.67), and `QA:136` concludes "clinically safe and non-inferior"; that interval does not support non-inferiority. `DEEP:147-154` lists conditions the app lacks (real-time tele-supervision, trained caregiver, complete revascularisation). The Franklin 1998 attribution in S2 is recalled, not in the repo: UNVERIFIED.
- **Fix:** Quote as "no significant difference in trials of screened low and moderate risk patients; intervals include a possible increase in serious events".
- **Needs real expert:** statistician or cardiologist.

### R19 [S2] Research-folder source quality and labelling
- **Raised by:** S2 F12, M1 F10, S1 F10.
- **Status: verified.** `DEEP` reference list includes an Aetna payer bulletin (ref 9, used for remote-CR eligibility), a Docsity page for the AACVPR table (ref 15), a congenital-heart-disease paper (ref 21), and an Irish guideline (ref 22, iacronline.ie) that `QA` labels "IACR (2025)" without saying it is Irish. `DEEP:178` writes "DASI > 34.7 METs"; whether DASI is a score rather than METs is NEEDS REAL EXPERT. `QA:67` heading carries stray citation indices. `QA:55-59` mixes lab-only criteria (SBP over 250, ST depression 2 mm or more) with home symptoms; `QA:61` proposes location confirmation and EMS notification that the spec does not adopt.
- **Fix:** Cite primary documents; mark each number with a primary source or UNSOURCED; split the red-flag list into in-session, after-session and data-driven lists.

### R20 [S3] Minor
- "Brainless" and "mission" vocabulary may read as flippant (M2 F8, S3 F10). Price has no unit (`pitch:27`; M1 F14). Emoji and lock-screen drug names (S3 F10, S4 F11). `pitch:5` mixes "chronic condition" with an acute MI. The 1669 patient copy needs clinician review in Thai.

### Dropped (misread) items

| Reviewer item | Why dropped |
|---|---|
| M1 critique: Property 5 "at most 10%" conflicts with `QA:121` "5 to 10%" | 10% as an upper cap is consistent with a 5 to 10% range. Kept only as a precision note in R14. |
| S2 F3 item 2: `DEEP:100` totals "more than 60 minutes" | 40 + 10 + 10 = 60. The inconsistency with "20 to 60" stands; the arithmetic claim does not. |
| M3 F5 sub-claim: private and self-pay are 0.3 to 2.5% of inpatient cardiac admissions | `MKT:13` says general public hospital registries, not cardiac, and such registries exclude private hospitals. The figure should not be used to size the market. |

No whole finding was dropped. Several reviewer-recalled facts (Lally 66 days, Franklin 1998 rates, ACSM +20 and +30 bpm, AACVPR 5 to 7 METs) are not in the repo; I carry them as UNVERIFIED rather than dropping them.

## Scores by persona and dimension

All scores are the reviewers' own, re-added by the chair. Track A is design and system; Track B is the pitch script.

| Persona | Track A avg | Track B avg | Combined |
|---|---|---|---|
| S1 Cardiologist | 1.43 | 1.29 | 1.36 |
| S2 Rehab physician | 1.71 | 1.29 | 1.50 |
| S3 Nurse and pharmacist | 1.43 | 1.29 | 1.36 |
| S4 Regulatory and ethics | 1.71 | 1.29 | 1.50 |
| M1 AI safety | 1.43 | 1.29 | 1.36 |
| M2 Behaviour and HCI | 1.57 | 1.14 | 1.36 |
| M3 Venture and market | 1.57 | 1.00 | 1.29 |
| **Panel mean** | **1.55** | **1.22** | **1.39** |

Track A, panel mean by dimension (7 reviewers, 0 to 4): clinical validity 2.00; patient safety 1.43; evidence and sourcing 1.86; feasibility 2.00; regulatory and privacy 1.14; behaviour and adherence 1.29; agent safety and evaluation 1.14.

Track B, panel mean by dimension: problem clarity 2.00; solution credibility 1.00; evidence 1.00; market and business 1.71; differentiation 0.86; team and feasibility 1.00; impact and ethics 1.00.

Reading: the weakest areas are differentiation, regulatory and privacy, and agent evaluation. The design doc is stronger than the pitch (Track A 1.55 vs Track B 1.22). Scores are tightly clustered (1.29 to 1.50 combined), so the ranking among personas is not informative. All are in the "needs major work" or "not ready" bands.

## Disagreements between reviewers

1. **G2 red flags: PASS or NOT-DEFINED.** S1, S2, S4, M2, M3 passed it at design level; S3 and M1 did not. Resolution: NOT-DEFINED. The response is specified; the detection path is not (R2).
2. **Severity of the red-flag input gap.** S3 and M1 S0; S1 and S2 S1; S4 and M3 did not raise it. Kept at S0 (highest), with M1's note that it drops to S1 once a pre-LLM screen is specified.
3. **Severity of medication handling.** S3 S0; M1 S2; S1 and S2 S1 (inside drug-interaction findings). Kept at S0; flagged as the weakest S0 because the harm requires the agent to answer drug questions, which no artifact says it will.
4. **Severity of the QA parameter conflicts.** S2 S0 (F2); S1, M1 S1; S4, M2, M3 did not read `QA` closely. Kept at S0 as a coding blocker.
5. **Free tier design.** M2 wants the free tier extended to 4 weeks of core missions so habit forms before the paywall (M2 F1). S1, S2, S4 and M1 want the free week to contain no exercise missions until a limit record exists. S3 wants safety features never paywalled. These collide: a longer free exercise tier makes R1 worse. Chair view: extend the free tier only for non-exertional and clinician-limited content; test paywall timing only inside a clinician-onboarded cohort. A real behavioural scientist and clinician must settle it.
6. **Peer community.** M1 and S4 say cut or defer; S1, S2 say frequency-only goals with a guard; M2 and M3 say replace with a LINE family-caregiver loop first (`MKT:189`). Chair view: all three agree it is not v1-safe as written; caregiver summaries are lower risk but raise their own consent question (R8).
7. **Eligibility scope.** S4 narrows v1 to post-MI, low-risk, clinician-enrolled. S3 wants a hard onboarding screen with depression. S1 wants a block list with unknown blocked. M3 wants "referred by hospital first". Compatible; the open choice is self-declaration (weak, per S4) versus enrolment through a hospital or insurer.
8. **Where limits come from for the B2C user.** S2 wants a clinician form with fixed fields; M1 allows "an RPE and talk-test-only conservative default, with the default values written down"; S1 and S4 want non-exertional content only. M1's option still needs a cardiologist to sign the default values and a gate for who may receive it. The chair did not resolve this.
9. **Track B market score.** M2 and M3 gave market and business 1; the other five gave 2. M3's lower score rests on the absence of insurer contact, CAC and unit economics, which is verified (R13, R17).
10. **Home-safety evidence.** S1 did not verify the primary figures and S2 recalls them from memory. Not a true disagreement; open.

## Needs a real expert (clinician, lawyer, insurer, statistician)

| Who | What they must decide |
|---|---|
| Cardiologist (Siriraj mentor; named owner of limits) | Default behaviour with no limit record; hard-block list and tiering of red-flag symptoms; Thai red-flag phrase list and 1669 patient copy; drug-class rules (nitrates, diuretics, anticoagulants, antiarrhythmics, diabetes drugs); ICD and target-HR interaction; whether discharge notes actually carry exercise limits |
| Cardiac rehab physician or CPET lab | Reconciled parameter table (R4); K = 0.8 for beta-blockers; %HRR range; resistance timing after PCI and CABG; AACVPR band definitions; warm-up, cool-down, weekly volume and progression caps; Thai heat thresholds; CPET availability in Thailand |
| Clinical pharmacist | Medication reminder logic; "agent never advises on drugs" rule; new or changed drug pause |
| Cardiac nurse and Thai health-literacy specialist | Week-3 usability for patients aged 55 to 75; caregiver role; fasting and observance timing; peer-moderation rules; Thai naming of "mission" |
| Psychologist or psychiatrist | Depression and fear-of-exercise screen, Thai-validated instrument choice, safe-messaging route |
| Thai FDA or regulatory lawyer | SaMD classification and intended use of an AI that schedules intensity; whether "prescription" wording changes it |
| Privacy lawyer or hospital DPO | PDPA basis for health data, consent matrix, cross-border LLM calls, data residency, controller |
| Insurance lawyer or OIC-literate adviser | Whether insurer visibility of individual adherence data is permitted; insurer data-sharing consent |
| Insurer product or claims lead; actuary | Whether insurers pay for rehab packages in Thailand; budget owner; Thai claim costs; sales cycle |
| Health-economics adviser | Price unit and willingness to pay for 499 THB; clinician-time cost per member |
| Statistician | Pilot size and the bound it can support for S-1, S-3 and B-3; non-inferiority wording; red-flag recall target |
| Hospital IRB and clinical safety committee | Route and approval for any real-patient pilot; incident reporting; liability allocation |
| Behavioural scientist | Verify any habit and implementation-intention literature; paywall-timing design |
| Whoever can open PMC12990137 | Which statistic is correct for "doctors recommend exercise" (81/11 cardiologists vs 93/15 Italian GPs) |

## Five cheapest actions that remove the most risk

1. **Rewrite the pitch script to match the team's own notes (text only, about an hour).** Apply `spec:36-39` to `pitch:5`, `:7`, `:9`, `:17` and `:25`. Replace "proven", "optimal, exact" and "prescription". Cut or cite the doctor statistic after someone opens PMC12990137. Add one sentence that limits are set by your clinician and the app only schedules inside them, one differentiation line, and the price unit. Closes G4 and R3.
2. **Add one safety paragraph to spec section 5 (text only).** No exercise mission without a limit record (who set it, date, review-by, plus max duration, sessions per week and weekly increment). Missing, stale or self-entered means non-exertional content only. Unknown risk class or any hard-block condition means blocked, with the list marked "clinician to confirm". Missing data, network or model down means no increase. Closes R1, R6, R7 and R9 at design level and makes G1, G3 and G6 definable.
3. **Specify the red-flag input path and the drug-advice rule (text only).** Fixed-choice symptom tap before and after each exercise mission, an "I feel unwell" control, a deterministic Thai and English pre-LLM screen that fails closed, and an explicit rule that the agent never advises on medication and the Done tick is self-report. Closes R2 and R5 at design level.
4. **Freeze `QA` and send one reconciled parameter table to the Siriraj mentor.** Mark `app-parameters-qa.md` "do not implement", resolve the contradictions listed in R4, remove the %HRR and K = 0.8 rule from v1, and cap v1 intensity at the clinician-supplied HR ceiling with RPE 11 to 13 and the talk test. Ask the mentor in the same message for the named-owner decision (G5) and the local consult-time figure. Closes R4 and starts G5.
5. **Text-only evidence hygiene.** Label every Movn figure "vendor-reported, US"; strike the 88% readmission rate; mark Muang Thai Life ">70%" and the AIA source UNSOURCED (`MKT:102-103`, `:109`, `:195`, `README.md:25`); fix the "Proven" cell (`MKT:63`). In `system-eval.md` remove "panel `system` mode not FAIL" from the G-A exit (`:90`), extend G-A to SC-01 through SC-18, and define the HR plausibility band between SC-03 and SC-07. Closes R13 and the verified parts of R14.

## Not covered by this review

- No code, so no scenario suite, property test, rules-engine or fault-injection result. 0 of 18 scenarios run.
- No primary guideline was opened (ESC 2020, EAPC 2021, AACVPR editions, Heart Association of Thailand 2020, the GERS-P source for K). The chair's checks of `QA` and `DEEP` numbers are internal-consistency checks only.
- No cited URL was fetched, including PMC12990137, PMC10353658, PMC8894994 and PMC11456183. The market citation mismatches are inferred from titles in `sources.md` and the reference list, not from reading the pages. Treat them as "title does not match claim", not as proven errors.
- No Thai FDA, PDPA, OIC or IRB rule was consulted. All regulatory statements are open questions.
- No usability test with real patients, no insurer or patient interview, no willingness-to-pay data, no smartwatch ownership data for Thai post-MI patients aged 45 to 75.
- Wrist heart-rate accuracy during exercise, in arrhythmia or on beta-blockers: not assessed and UNSOURCED.
- `research/pitch-claims-check.md` and the two deep reports were read in full only by some reviewers (M1 did not read them; S1, S3 and S4 read them in part). The chair re-read the cited lines but did not re-audit every row of either deep report.
- The panel cannot pass a gate. Gates B, D, E and F in `system-eval.md` need named humans.
