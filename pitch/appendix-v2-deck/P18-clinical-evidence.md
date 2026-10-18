# P18 · A clinician sets the limit from CPET or another accepted test; the recommender only ranks what fits inside it

## Key message

Cardiology guidelines already accept several ways to set a safe exercise intensity: CPET is the most precise, and a symptom-limited ECG stress test, a 6-minute walk test, perceived effort (Borg RPE) and the talk test are accepted when there is no CPET. They also say who may exercise unsupervised: clinician-confirmed low-risk patients only. Heartstep makes none of these decisions; a clinician signs the limit and the risk class into a FHIR `CarePlan`, and the recommender ranks only activities whose published intensity (2024 Adult Compendium METs) fits inside it, which is why tennis singles (8.0 METs) is out for Somchai and social badminton (5.5), table tennis (4.0) and bowling (3.8) are in.

## Why this matters to the judges

- **Real-world impact.** A coach that recommends the wrong intensity to a heart patient is dangerous. Judges will ask "where do the limits come from when there is no CPET?" and "who is not allowed to use this?". This page answers both from guidelines, not from the model.
- **Technical coherence.** Every clinical input has a home in FHIR: the limit and its source test in `CarePlan` extensions, the risk class as an `Observation`, the signer in `Provenance`. The rules engine reads them through FHIR SQL Builder (P06), so clinical evidence and code are the same chain.
- **Innovation, honestly bounded.** The recommender (taste, people like you, near you) is the new part. The clinical part is deliberately not new: it reuses accepted practice so that the novelty never sits in the safety-critical path.

## Full detail

### Status of the evidence

The clinical parameters come from first-pass research built with NotebookLM over 55 sources on 2026-10-17 (`research/README.md`). That research is machine-generated and contradicts itself in 12 places (`research/guidelines/RECONCILE-for-clinician.md`). The rule in the repo is explicit: **"DO NOT IMPLEMENT numbers from `guidelines/` yet."** For this page we opened two primary or near-primary sources ourselves: the 2024 Adult Compendium sports table (MET values used in the demo, checked for 8 activities) and a report of the ACC scientific statement on exercise of 15 October 2026. We confirmed that the ESC 2020 sports cardiology guideline has a section 4.2.3 on hypertension but could not retrieve its text; the four lines we use are a NotebookLM paraphrase and are marked "to verify".

### Where the limit comes from

The clinician sets the limit; the `CarePlan` records the source test in a `limit-source` extension, the signer, the date and a review-by date. With no signed, in-date record, the app shows only non-exertional content (spec rule 6).

| Source of the limit | What it gives | Accepted by (per research file, to verify) | Heartstep use | Synthetic patients |
|---|---|---|---|---|
| **CPET** | Ventilatory thresholds; HR at VT1 can be the hard upper bound | Main precise source; described as "significantly underutilized" (cost, training, equipment) | Best case | p01, p05, p07, p08 |
| Symptom-limited ECG stress test | Peak HR and HR reserve, measured on usual medication | IACR (Irish, 2025), AACVPR, ESC 2020, GERS-P 2022, EAPC | Accepted | p03 (`exercise-ecg`) |
| 6-minute walk test | Submaximal capacity for a low-to-moderate start | IACR, GERS-P, EAPC | Accepted | p02 (`6mwt`) |
| Resting HR + 20–30 bpm | Early outpatient target when no test exists | AACVPR, ACSM | Not in v1 | — |
| Borg RPE 11–14 (6–20 scale) | Perceived effort | ESC, EAPC, AACVPR, IACR, ACSM | Always paired with HR; v1 uses 11–13 | all |
| Talk test | "Can still talk" | ESC, EAPC, IACR, AACVPR | Primary for beta-blocked patients | all |

**Beta-blockers** blunt the heart-rate response, so age-predicted maximum heart rate (220 − age) is unreliable. The research files disagree on the correction (K = 0.8 in the Karvonen formula; subtract 10 bpm; or "overestimates by 20–40 bpm"). The proposed v1 rule therefore avoids any formula: **no %HRR calculation; use the clinician's HR ceiling plus RPE 11–13 and the talk test.** No resistance missions in v1.

### From a limit to a recommendation: the MET bridge

A recommender needs a common intensity scale for 100 different activities. We use **METs** (metabolic equivalents) from the 2024 Adult Compendium of Physical Activities, the standard reference table of activity intensities. In the demo catalogue 44 of 100 activities carry a Compendium code; the other 56 are team estimates marked "to verify" in the page footer. We re-checked eight of the coded values against the Compendium sports table on 2026-10-18 and all eight match.

The clinician's limit is expressed as a MET ceiling plus a heart-rate ceiling, an RPE band and an avoid-list. For Somchai's synthetic record (`CarePlan/cmc-p09-limits`, "Dr. Narin R. (synthetic)"): up to 5.9 METs, heart rate under 120 bpm, RPE 11–13, avoid heavy straining and breath-holding. The rules engine drops everything above the MET ceiling and everything flagged for contact, heavy straining or vigorous bursts. Only then does the recommender rank by taste.

**A caveat we say out loud:** MET values are population averages for an activity, not a measurement of how hard Somchai will play. Social badminton at 5.5 METs sits close to his 5.9 ceiling, so the plan pairs it with the heart-rate ceiling, the talk test and a symptom tap after each session. The 5.9 figure itself is synthetic; a real clinician would set it, and whether METs are the right unit for a limit record is one of the questions for the reviewing physician.

### The guideline lines the agent retrieves for hypertension

The demo retrieves four paraphrased lines from the ESC 2020 sports cardiology guideline, section 4.2.3 (hypertension), from an approved-content collection in IRIS Vector Search. They are shown to the patient as context, never used to set the limit:

1. At least 30 minutes of moderate dynamic aerobic exercise (walking, cycling, swimming) 5–7 days a week.
2. Resistance training 2–3 days a week is also advised.
3. Avoid heavy weightlifting with static (isometric) effort and breath-holding (Valsalva).
4. If blood pressure is uncontrolled (SBP > 160), no high-intensity exercise until it is controlled.

Line 3 is why "heavy weight lifting", "plank holds" and "push-ups to failure" carry the breath-holding flag and drop out for Somchai. Line 4 is a candidate hard-block rule for the rules engine once a clinician confirms it; it needs a recent blood-pressure `Observation`, which the synthetic bundles contain (two BP panels per patient).

### What the October 2026 ACC statement adds

A scientific statement published in JACC on 15 October 2026 (writing-committee chair Jonathan N. Myers, as reported by News-Medical) supports the direction of the product without validating it:

- "Cardiac rehabilitation remains first-line treatment; individualized prescriptions should be provided when formal rehab is unavailable."
- Exercise testing "is not routinely required before starting exercise for asymptomatic or stable individuals."
- 5,000 to 7,000 steps per day produce clinically important improvements.
- "Digital tools and home-based programs may enhance adherence when combined with structured programs."
- Chair's quote: "The most important message is that some activity is better than none."

We read this as support for two of our design choices: Heartstep supports and extends rehab rather than replacing it, and a clinician-signed limit from an accepted non-CPET source is reasonable for stable patients. We have read a news report of the statement, not the full JACC text; the exact wording is to verify.

### Who may use the app: risk classes

| Class (AACVPR-style, per research file) | Example criteria | Suitability (per research file) | Heartstep v1 behaviour | Synthetic patient |
|---|---|---|---|---|
| Low | LVEF ≥ 50% (bands conflict), uncomplicated event, ≥ 7 METs measured, no complex arrhythmia, no clinical depression | Unsupervised home or digital rehab | Recommendations, once a clinician confirms the class | p01, p02, p05, p07, p08 |
| Moderate | LVEF about 35/40–49%, symptoms only at higher effort | Hybrid home rehab after 3–6 supervised sessions | Supervised sessions first | p03 (LVEF 42%) |
| High | LVEF below 35/40%, cardiac-arrest survivor, complex arrhythmia, ICD (one source), symptoms at low effort | Not suitable for unsupervised exercise | Blocked + referral `Flag` | p04 (LVEF 30%, ICD) |
| Unknown | No class entered | — | Treated as blocked | p06 (draft limit) |

The simulated panel found a catch that shaped the design: "low risk" requires ≥ 7 METs **measured**, so a user with no test cannot classify themselves as low risk. That is why the class must be entered by a clinician (spec rule 7) and why "unknown" means blocked.

### Hypertension is not yet a scoped population

Somchai, the demo patient, has hypertension. The synthetic FHIR bundles and the clinical research focus on **post-MI** patients (the synthetic p01 is also called Somchai, but is a low-risk post-MI patient on a beta-blocker). The spec says "heart failure and high-risk hypertension are out of v1 scope until a clinician defines their rules." So the demo shows the recommender mechanism on a hypertension story, while the eligibility rules a clinician has to sign are written for post-MI. Closing that gap, either with hypertension rules signed by a clinician or a post-MI demo patient, is an open item.

### Contradictions a clinician must settle

`RECONCILE-for-clinician.md` lists 12 questions. Grouped by what they affect:

| Group | Rows | Example |
|---|---|---|
| Intensity targets | 1, 2, 4 | 50–70% HRR vs VT1 at about 39–45% HRR post-MI; beta-blocker corrections; talk test "full sentences" vs "short phrases" |
| Eligibility | 5, 6, 7 | LVEF ≥ 50 vs > 50; overlapping MET bands; ICD as high risk |
| Dose and progression | 3, 8, 9 | resistance start after CABG 12 weeks vs 4–6 weeks; session length; 5–10% per week vs a 10% cap |
| Home safety and environment | 10, 11, 12 | lab stop criteria not adapted for home; Thai heat not covered; safety-evidence wording |

Safe wording for home-rehab safety, if asked: **"no significant difference in trials of screened low- and moderate-risk patients; the intervals include a possible increase in serious events."** The research file's serious-adverse-event risk ratio of 1.30 (95% CI 0.63–2.67) does not support "non-inferior".

### The Thai gap, briefly (detail on P02 and P19)

Per the research files, to verify against primary sources: Thai post-ACS recommendations (2020) say to offer rehab no later than 10 days after discharge; one single-site study reported phase-2 uptake after CABG of 12.5%, with 83.3% of those patients saying they were never told about it. A Thai LINE-based home-rehab study (n = 54, 27 vs 27) reported better 6-minute walk, DASI and SF-36 scores than controls. The team checked PMC12990137 on 2026-10-17: 93% of Italian GPs prescribe activity and 15% give it in writing.

## Visualizations

### Chart 1 · Bar chart: Somchai's options against his limit

- **Type:** horizontal bar chart with a vertical reference line.
- **Title:** "Published intensity (METs) of the activities Somchai mentioned, against his signed limit (synthetic)"
- **X axis:** METs, 0 to 9. **Y axis:** activity.
- **Data (2024 Adult Compendium, checked 2026-10-18):**

| Activity | Compendium code | METs | Flag in catalogue | Result for Somchai |
|---|---|---|---|---|
| Tennis, singles | 15690 | 8.0 | vigorous bursts | Out (above cap) |
| Badminton, competitive | 15020 | 7.0 | vigorous bursts | Out (above cap) |
| Tennis, doubles | 15680 | 6.0 | — | Out (above cap) |
| Badminton, social | 15030 | 5.5 | — | In, offered |
| Golf, walking and carrying clubs | 15265 | 4.3 | — | In |
| Table tennis, social | 15660 | 4.0 | — | In, offered |
| Bowling | 15092 | 3.8 | — | In, offered |
| Walking football | 15615 | 3.5 | — | In |

- **Annotations:** vertical dashed line at 5.9 labelled "Signed limit: ≤ 5.9 METs, HR < 120, RPE 11–13 (synthetic record)". Colour bars above the line grey with "out", the three offered options teal.
- **What the reader should notice:** the cut is made by a published table and a clinician's number, not by the model. Social badminton sits close to the line, so it is paired with heart-rate and talk-test checks.

### Chart 2 · Stacked bar: what the rules remove from the 100-activity catalogue

- **Type:** single stacked bar (or waterfall).
- **Title:** "100 activities → 67 inside Somchai's limits"
- **Data:**

| Segment | Count |
|---|---|
| Kept (≤ 5.9 METs, no contact, straining or burst flag) | 67 |
| Removed: above 5.9 METs | 29 |
| Removed: within METs but flagged (power yoga, digging the garden, plank holds, Muay Thai bag work) | 4 |
| **Total** | **100** |

Secondary data for a small inset (catalogue intensity mix):

| MET band | Activities |
|---|---|
| under 3.0 | 13 |
| 3.0–5.9 | 58 |
| 6.0–8.9 | 25 |
| 9.0 and above | 4 |

- **What the reader should notice:** two-thirds of the catalogue stays available, so a limit narrows the choice without leaving the patient with "just walk".

### Chart 3 · Bar chart: open clinical questions by area

- **Type:** horizontal bar chart.
- **Title:** "12 contradictions in our research, waiting for a rehab physician"
- **Data:**

| Area | Number of reconcile rows |
|---|---|
| Intensity targets | 3 |
| Eligibility and risk bands | 3 |
| Dose and progression | 3 |
| Home safety and environment | 3 |

- **What the reader should notice:** the open questions sit exactly where the rules engine would need numbers, which is why nothing from the research file is coded.

### Diagram · Who decides what

Three lanes left to right. Lane 1 "Clinician (human)": test (CPET / stress ECG / 6MWT) → limit (METs, HR, RPE, avoid-list) → risk class → signs `CarePlan` + `Provenance`. Lane 2 "Rules engine (deterministic)": reads limit via FHIR SQL Builder → filters catalogue → blocks unknown or high risk → red-flag stop path. Lane 3 "Recommender and chat (model)": ranks only the allowed set by taste, people like you, near you → asks the patient → writes FHIR `Task`s. A bold arrow from lane 1 to lane 2 only; no arrow from lane 3 back to the limit.

## Numbers and claims ledger

| Claim | Value | Source | Status |
|---|---|---|---|
| MET values for 8 activities | as in Chart 1 | https://pacompendium.com/sports/ (opened 2026-10-18); `demo/agent-flow-demo.html` | checked |
| Activities with a Compendium code in demo | 44 of 100 | `demo/agent-flow-demo.html` footer and RAW table | checked (others are estimates) |
| Somchai limit | ≤ 5.9 METs, HR < 120, RPE 11–13, avoid straining and breath-holding | `demo/agent-flow-demo.html` `LIMIT` | synthetic |
| Catalogue filter | 100 → 67 (29 above cap, 4 flagged) | computed from demo file | synthetic |
| ESC 2020 §4.2.3 hypertension lines | 30 min moderate aerobic 5–7 days/week; resistance 2–3 days/week; avoid isometric and Valsalva; no high intensity if SBP > 160 until controlled | team brief; demo `GUIDE` (paraphrased via NotebookLM); section existence seen at https://academic.oup.com/eurheartj/article/42/1/17/5898937 | to verify (text not retrieved) |
| ACC statement, JACC, 15 Oct 2026 | rehab first-line; testing not routinely required; 5,000–7,000 steps; digital tools may help with structured programs | https://www.news-medical.net/news/20261015/New-scientific-statement-urges-doctors-to-prescribe-exercise-for-heart-health.aspx | checked (news report, not the paper) |
| Accepted non-CPET sources | stress ECG, 6MWT, HRR, RHR + 20–30, RPE, talk test | `research/guidelines/app-parameters-qa.md` §1 | machine-generated, to verify |
| CPET "significantly underutilized" | quote | `research/pitch-claims-check.md` | to verify |
| Risk classes and suitability | as in table | `app-parameters-qa.md` §4 | machine-generated, conflicting |
| 12 contradictions | rows 1–12 | `research/guidelines/RECONCILE-for-clinician.md` | checked (unresolved) |
| SAE RR | 1.30 (95% CI 0.63–2.67) | `app-parameters-qa.md:135` | to verify |
| Thai rehab start | ≤ 10 days after discharge | `app-parameters-qa.md` §7 | to verify |
| Phase-2 uptake after CABG; never told | 12.5%; 83.3% | `research/README.md`; PMC11456183 (page blocked by captcha when opened) | to verify |
| LINE home-rehab study | n = 54 (27 vs 27) | `app-parameters-qa.md` §7 | to verify |
| GP exercise prescription | 93% prescribe, 15% in writing (Italian GPs) | `pitch/README.md` (PMC12990137 checked 2026-10-17) | checked by team |
| Synthetic patient classes and limit sources | as in tables | `synthetic/README.md`, `synthetic/profiles.json` | synthetic |

## Limits and open questions

- No real clinician has signed any value. Gate G-B (P21) is the fix: a cardiologist and a rehab physician review the limit library in writing.
- Primary guidelines (ESC 2020 full text, EAPC, AACVPR editions, IACR 2025, Thai 2020 post-ACS) were not opened for this page. The ESC hypertension lines are paraphrases.
- 56 of 100 catalogue MET values are team estimates.
- MET values describe typical effort, not an individual's; whether a MET ceiling belongs in the limit record is for the clinician.
- Hypertension is the demo story but post-MI is the researched, scoped population.
- Beta-blocker handling, drug classes beyond beta-blockers (nitrates, anticoagulants, diuretics, antiarrhythmics, diabetes drugs), Thai heat rules and the Thai red-flag phrase list all need a clinician.
- Wrist heart-rate accuracy during exercise, in arrhythmia or on beta-blockers is not assessed.

## Likely judge questions

1. **"Who sets the limit if there is no CPET?"** A clinician, from an accepted alternative: a symptom-limited ECG stress test, a 6-minute walk, perceived effort and the talk test. The `CarePlan` records which test, who signed and when to review; without it, no exercise recommendations at all.
2. **"Why is tennis out but badminton in?"** Tennis singles is 8.0 METs in the 2024 Compendium and social badminton is 5.5; Somchai's synthetic limit is 5.9. The cut is made by rules from those numbers; the model only ranks what is left.
3. **"What about beta-blockers?"** No heart-rate formula in v1. The clinician's heart-rate ceiling plus RPE 11–13 and the talk test, which guidelines in our research prefer for beta-blocked patients.
4. **"Is home exercise safe?"** For screened low- and moderate-risk patients, trials show no significant difference from centre-based rehab, but the intervals include a possible increase in serious events. That is why only clinician-confirmed low-risk patients get unsupervised recommendations, and red flags stop everything.
5. **"Doesn't the new ACC statement make this unnecessary?"** It says cardiac rehab is first-line and individualised prescriptions should be given when rehab is unavailable. Heartstep is a way to deliver the clinician's individual limits day to day; it supports rehab, it does not replace it.

## Sources

Repo files:
- `research/README.md`; `research/guidelines/app-parameters-qa.md`; `research/guidelines/RECONCILE-for-clinician.md`; `research/pitch-claims-check.md`
- `evaluation/reviews/2026-10-17-document/SYNTHESIS.md` (R4, R6, R18; simulated panel)
- `docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md` §5 (rules 1–11), §8
- `demo/agent-flow-demo.html` (catalogue, `LIMIT`, `GUIDE`)
- `synthetic/README.md`, `synthetic/profiles.json`, `synthetic/generate_fhir.py`
- `pitch/README.md` (PMC12990137 check); `pitch/appendix/A10-clinical-evidence.md`; `pitch/appendix-deck/P16-clinical-evidence.md`

External (opened 2026-10-18):
- 2024 Adult Compendium, sports: https://pacompendium.com/sports/
- ACC statement report (News-Medical, 15 Oct 2026): https://www.news-medical.net/news/20261015/New-scientific-statement-urges-doctors-to-prescribe-exercise-for-heart-health.aspx
- ESC 2020 sports cardiology guideline (section list only retrieved): https://academic.oup.com/eurheartj/article/42/1/17/5898937

## Image-generation prompt

Design one 16:9 information slide on a white background. Title, the key message: "A clinician sets the limit; the recommender only ranks what fits inside it." Main visual: a horizontal bar chart "METs (2024 Adult Compendium) vs Somchai's signed limit (synthetic)" with bars Tennis singles 8.0, Badminton competitive 7.0, Tennis doubles 6.0, Badminton social 5.5, Golf walking 4.3, Table tennis 4.0, Bowling 3.8, Walking football 3.5, and a dashed line at 5.9 labelled "Signed limit ≤ 5.9 METs · HR < 120 · RPE 11–13". Bars above the line grey "out"; Badminton social, Table tennis and Bowling highlighted "offered". Beside it a small four-row panel "Who may use it": Low – recommendations after clinician confirms; Moderate – supervised first; High – blocked + referral; Unknown – blocked. A small strip: "12 research contradictions sent to a rehab physician · ESC 2020 hypertension lines retrieved, never used to set limits". Badge: "Synthetic patient · first-pass research". No logos, no other numbers. ChatGPT chooses the design.
