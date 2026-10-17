# m3-venture-market review — document — 2026-10-17

> Simulated review by a language-model role-play. Not a real clinician or institution.

**Artifacts read (fully):** docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md, docs/pitch-script-draft1.md, HANDOFF.md, research/README.md, research/pitch-claims-check.md, research/market/notebooklm-deep-report.md, research/market/sources.md
**Gate result (my view):** FAIL (G4 fails on the pitch script; one S0 open; several gates NOT-DEFINED)

Path prefix below: `spec` = docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md, `script` = docs/pitch-script-draft1.md, `mkt` = research/market/notebooklm-deep-report.md, `src` = research/market/sources.md, `chk` = research/pitch-claims-check.md, `rd` = research/README.md. Safety gates are outside my specialty. I mark what the text shows and add NEEDS REAL EXPERT where a clinician or lawyer must decide.

## Safety gates
| Gate | Status | Evidence (path:line) |
|---|---|---|
| G1 Limits | NOT-DEFINED | Intent is stated (`spec:72`, `spec:75`, `spec:98`). No mechanism makes it provable, and the script says the AI "designs an optimal, exact plan" (`script:17`), which contradicts "limits come from the clinician". NEEDS REAL EXPERT (safety engineer). |
| G2 Red flags | PASS (design only) | Hard-coded, no LLM (`spec:74`, `spec:95`). The pitch does not mention it. Untested. |
| G3 Eligibility | NOT-DEFINED | The spec has no risk-class gate. `rd:18` recommends one, and `spec:109` mentions it only inside an open question. B2C freemium sells to anyone (`script:27`). NEEDS REAL EXPERT (cardiologist). |
| G4 Claims | FAIL | `script:25` "proven tool to reduce readmission rates". `script:17` "optimal, exact plan". `script:7` 80%/15% is wrong versus the closest source (`chk:5`). The fixes exist only as notes (`spec:36-41`), not in the script. |
| G5 Accountability | NOT-DEFINED | No named clinical owner for limits. No consent design for wearable data or insurer access. `spec:117` asks whether the clinician sees anything. The insurer channel needs insurer data-sharing consent. NEEDS REAL EXPERT (lawyer). |
| G6 Failure mode | NOT-DEFINED | The spec is silent on data, network or model outage. |

## Scores (0–4)

### Track A — design and system
| Dimension | Score | One-line reason |
|---|---|---|
| Clinical validity | 2 | Design rules are sensible. The no-CPET path is a research note, not yet a design (`spec:109`). |
| Patient safety | 2 | Red-flag and no-self-raise rules exist (`spec:73-74`). No hazard analysis. |
| Evidence and sourcing | 2 | `(guess)` tags and the weak-spots list are honest (`rd:30-35`). Headline market numbers still rest on vendor and non-primary citations. |
| Feasibility | 2 | Buildable, but "No code yet" (`HANDOFF.md:11`). Demo path, watch and deliverable are open questions (`spec:112-113`). |
| Regulatory and privacy | 1 | SaMD and PDPA are flagged (`spec:75`) but not resolved. Insurer data flow is unaddressed. |
| Behavior and adherence | 1 | Peer community is asserted, with no mechanism or test plan. Social-support evidence is correlational (`chk:8`). |
| Agent safety and evaluation | 1 | No scenario suite or test plan. |
**Track A average: 1.57 (needs major work)**

### Track B — pitch (includes `script`)
| Dimension | Score | One-line reason |
|---|---|---|
| Problem clarity | 2 | One patient and one gap, but the 80/15 and "5-minute" numbers are unsourced or mis-sourced (`chk:5-6`). |
| Solution credibility | 1 | "Optimal, exact … with ease" (`script:17`) overclaims. CPET is the headline input, yet most users won't have one (`spec:40`). |
| Evidence | 1 | No evidence the product works. Only borrowed vendor claims. |
| Market and business | 1 | Payer named, price named, but no willingness-to-pay data, no insurer contact, no CAC or unit economics. See F2-F7. |
| Differentiation | 0 | The script never mentions Movn, Cardihab, AIA Vitality, hospital programs, or LINE programs. |
| Team and feasibility | 1 | No demo. No named clinical partner in the pitch. |
| Impact and ethics | 1 | Rural and low-income equity gap is in the research (`mkt:39`, `mkt:45`) but the 499 THB product ignores it. Safety and data handling are absent from the pitch. |
**Track B average: 1.00 (not ready)**
**Overall average (A and B): 1.29 (not ready)**

## Findings (most severe first)

### F1 [S0] "Proven tool to reduce readmission rates" is a false core claim
- **What is wrong:** The business pitch's central insurer claim is stated as proven. We have zero data, and the borrowed 20-30% is vendor data from a different product.
- **Evidence:** `script:25`; `chk:9` ("Not supported for us"); `mkt:63` labels the 20-30% "Proven across commercial payer populations", an overstatement of its own sources.
- **Failure scenario:** A judge or insurer asks "proven by whom, on whom?" in the first minute of Q&A. Credibility for the whole pitch collapses, and it is a G4 failure.
- **Fix:** Replace with "designed to improve rehab adherence, which cardiac-rehab evidence links to fewer readmissions", as `spec:39` already suggests. Add "pilot will measure this". Edit the script itself, not only the notes.
- **Needs real expert?** yes (regulatory lawyer on claim wording).

### F2 [S1] The 20-30% readmission reduction and $1,377 cost are vendor sourced
- **What is wrong:** The figures are from Movn's own materials or payer marketing. The report cites a trial-registry listing, a health-plan marketing blog, and Movn's own blog.
- **Evidence:** `mkt:57`, `mkt:63-64`, `mkt:85`, cites [18] WithPower listing, [19] MVP Health Care blog, [20] Movn blog (`mkt:216-218`; `src:17-19`). `rd:32` concedes "vendor data, not independent trials". No Thai or Asian cost basis. The $14,000 readmission cost is US.
- **Failure scenario:** An insurer actuary asks for the peer-reviewed effect size and a Thai claim cost. We have neither, so the insurer ROI story has no input.
- **Fix:** Label every Movn number "vendor-reported, US" wherever it appears. Search for independent RCTs and meta-analyses of digital or home-based CR on readmission. Build a Thai ROI from Thai claim costs (NEEDS REAL EXPERT: insurer actuary). Do not use a US cost as a Thai cost.
- **Needs real expert?** yes (insurer actuary).

### F3 [S1] The "88% readmitted 1-2 times" statistic is misused as a population rate
- **What is wrong:** `rd:34` correctly says it likely describes readmitted patients only. The market report still uses it as "the high readmission rate (88% within 12 months)" in the insurer rationale and conclusion.
- **Evidence:** `mkt:9`, `mkt:109`, `mkt:195`; caveat at `rd:34`. The same report gives a 11-14% 30-day post-AMI readmission rate (`mkt:20`), which contradicts the 88% reading. The cited cohorts ([5], [6]) are single or multi-hospital readmission-factor studies, not population incidence.
- **Failure scenario:** If 88% reaches a slide, any clinician judge will know it is impossible. The pitch loses the audience.
- **Fix:** Strike 88% from all pitch material. Use the pooled 30-day 11-14% (`mkt:20`, primary source [4] is a meta-analysis, though non-Thai) and say it is global. Fix `mkt:109` and `mkt:195` or mark them "do not quote".
- **Needs real expert?** no.

### F4 [S1] The insurer wedge relies on a mis-attributed citation
- **What is wrong:** "Muang Thai Life >70% CI premium growth" is cited to [23], which is a Facebook post about Bangkok Life Assurance's "bla goodlife keeper" product, not Muang Thai Life. `rd:25` repeats it as a market fact.
- **Evidence:** `mkt:103`, `mkt:221`, `src:34`. AIA Vitality (`mkt:102`) is cited to [25], an Asia Trusted Life Agents awards page (`mkt:223`, `src:35`), not an AIA source. Allianz, Krungthai-AXA and Thai Life rows carry no direct source (`mkt:124-125`).
- **Failure scenario:** Someone checks the footnote, finds Facebook and the wrong company, and doubts every insurer claim. UNSOURCED until a primary Muang Thai Life or OIC source is found.
- **Fix:** Mark ">70% CI premium growth" UNSOURCED and remove it from `rd:25`. Pull the figure from Muang Thai Life annual reports or OIC statistics. Source AIA Vitality from AIA's own page.
- **Needs real expert?** yes (insurer).

### F5 [S1] No Thai insurer evidence at all; payer logic is untested and the sales cycle is ignored
- **What is wrong:** "Insurers pay for rehab packages" is unverified in Thailand (`chk:10`). The report's own data shows private insurance and self-pay are only 0.3-2.5% of inpatient cardiac admissions and public schemes cover over 95% (`mkt:13`, `mkt:96`). So the paying market is a small slice, and the report never sizes it (no TAM/SAM/SOM anywhere). Insurer sales cycles, OIC filing and who owns the budget (claims, product, or wellness) are not covered. The US reimbursement codes (CPT, `mkt:66`) do not transfer.
- **Evidence:** `chk:10`; `mkt:13`, `mkt:96-98`; `rd:26`. The "Critical Illness rider" path (`mkt:109`) is the report's inference, not sourced fact. Sales-cycle length: UNSOURCED, none given.
- **Failure scenario:** A judge asks "which insurer, which budget line, how many lives, how long until money?". The team has only a plausible story.
- **Fix:** Run 3-5 insurer and 3-5 patient interviews before the next gate. State TAM/SAM/SOM from Thai AMI incidence times private-insured share, with each input sourced. Name a first-revenue path: for example, a paid pilot with one hospital or one insurer's CI claimants, scoped in months.
- **Needs real expert?** yes (insurer product or claims lead; Thai health-insurance regulator expertise).

### F6 [S1] The 499 THB price and the freemium funnel have no support, and the price may be mismatched to the tier
- **What is wrong:** "Starting at 499" has no unit stated (per month? per plan?) and no Thai willingness-to-pay data (`chk:11`, `rd:35`). The "299-599 THB/month" tier is defined in the report as a smartphone computer-vision exercise coaching tier, which is not this product (`mkt:116`). The 1,500-3,500 THB/month tier is cited to a US health-plan blog, an APACMed policy paper and a hypertension marketing blog (`mkt:117`, cites [19], [22], [28]), none of which is Thai pricing data. The report itself notes 64.8% of one Thai cohort earns at most 10,000 THB/month (`mkt:45`, `mkt:115`), so 499/month is about 5% of that income. There is no CAC, conversion, churn or LTV anywhere.
- **Evidence:** `script:27`; `spec:27` ("499 (THB assumed)"); `mkt:115-117`; `rd:28` ("model suggestion, not survey data").
- **Failure scenario:** A judge asks "what share of free users convert and what does it cost to acquire one?". There is no answer, and the one-week free trial may end before the habit forms.
- **Fix:** State price unit. Present 499 as a hypothesis with a fake-door or interview test. Add a back-of-envelope CAC and conversion model with every input marked ASSUMPTION. Consider a free first week anchored to the first clinic visit, not to download.
- **Needs real expert?** no for the test design; yes for pricing (health-economics advisor).

### F7 [S1] Differentiation is absent from the pitch, and the research understates incumbents
- **What is wrong:** The script never names a competitor. The research says no Thai-language patient-first daily-mission competitor was found, then notes this is not a proven absence (`rd:27`). Competitor rows for Kaia, Sword, Hinge, Vivira, Welldoc are model background knowledge, not cited pages, and are MSK or diabetes products (`rd:33`; `mkt:78-81`, `mkt:87-90` carry no `[cite]` tags). Kardia/HeartBuddy (`mkt:74`) also carry no cite. The Thai LINE-based home-CR study (`rd:20`) and AIA Vitality are direct local alternatives that the script ignores. The EAPC EXPERT tool is acknowledged (`spec:42`). Defensibility is not argued: a large insurer or hospital could copy a mission-pusher built on a general LLM and the phone's HealthKit.
- **Evidence:** `script:1-27` (no competitor); `rd:27,33`; `mkt:74-90`.
- **Failure scenario:** "How is this different from AIA Vitality plus a hospital LINE OA?". No prepared answer.
- **Fix:** Add one differentiation line to the script with a defensible moat: clinician-set limits with a deterministic safety layer, patient-first daily missions, Thai language, and later, local outcome data. Verify or delete the uncited competitor rows. Search for Thai cardiac apps, hospital apps and LINE programs directly.
- **Needs real expert?** no.

### F8 [S1] Several report claims are vendor-market-research or low-quality sources
- **What is wrong:** Smartwatch market figures (USD 85.7M to 137.5M, CAGR 9.5%, 46% share) and device price ranges come from a smartwatch ODM's marketing blog and paid-report landing pages (6Wresearch, Persistence, MarketDataForecast). Completion rates of 70-85% vs 25-40% come from a vendor blog (Carda Health). Cardihab 21% to 63% comes from a trade news item (pharmaphorum) about a vendor product. "Smartwatches ... 46% of wearables" is cited to [31], a global report.
- **Evidence:** `mkt:55`, `mkt:131`, `mkt:139-149`; cites [16] [29] [30] [31] (`mkt:214`, `mkt:227-229`); `src:22`, `src:28-30`, `src:37`.
- **Failure scenario:** The pitch states smartwatch penetration to justify the product. A judge asks for the source and gets a vendor teaser page. Note also that the spec targets patients aged 45-75 with a watch (`spec:46-47`). No data is given on the share of Thai post-MI patients who own a smartwatch (UNSOURCED). The key "who has a watch" premise rests on that.
- **Fix:** Tag each as "vendor or market-research estimate". Do not put them on slides. Replace with Thai national surveys (NSO, ETDA) for device ownership in the target age band. Verify Cardihab's result in the JMIR Cardio paper itself.
- **Needs real expert?** no.

### F9 [S2] Thai burden and CR-uptake numbers are sourced to real papers, but need one verification pass and have a population mismatch
- **What is wrong:** The 12.5% Phase-2 uptake and 83.3% "never informed" are from a single-site post-CABG study (`rd:20` says single-site) and the pitch is post-MI. Phase-1 67.4% is from tertiary urban centers (`mkt:33`). These are reasonable primary sources (`src:7`, `src:5-6`) and the best market evidence in the pack, but the 12.5% is post-CABG only. Rural travel claims (90-180 min) are from a different paper and are not specific to Siriraj patients.
- **Evidence:** `mkt:33-35`, `src:7`; `rd:20`.
- **Failure scenario:** The team says "12.5% of MI patients get rehab" and a cardiologist corrects it to "of CABG patients, one site".
- **Fix:** Quote as "post-CABG, one Thai center" or find a post-MI Thai figure. Ask the Siriraj mentor for local numbers (referral rate, CR capacity, average consult time). This also fixes the unsourced "5-minute consultation" (`chk:6`).
- **Needs real expert?** yes (Siriraj cardiology or rehab mentor).

### F10 [S2] The Premium offer silently assumes a clinician-set limit, yet B2C buyers mostly have none; this breaks both the safety and the business story
- **What is wrong:** The product's safety depends on clinician limits (`spec:72`). B2C freemium users will mostly lack CPET (`spec:40`). The business model has no cost line for clinician sign-off, and no answer to who pays the clinician. A nurse-oversight tier is priced at 1,500-3,500 THB (`mkt:117`) but the pitch offers only 499.
- **Evidence:** `spec:40`, `spec:109`; `script:27`; `mkt:117`.
- **Failure scenario:** Unit economics are impossible if every free user needs a clinician review, and unsafe if they don't.
- **Fix:** State in the pitch that Premium requires a clinician-signed limit via hospital or insurer. Move B2C to "referred by hospital" first. Model clinician-time cost per member.
- **Needs real expert?** yes (cardiologist; actuary).

### F11 [S2] Peer-community claim is supported only by correlation, and adds moderation, safety and cost burden
- **What is wrong:** Social support predicted readmission in cross-sectional Thai studies (β = -0.225). That is not evidence that app peer groups raise adherence (`chk:8`). The same social-support finding favors family and caregiver involvement (`mkt:189`), which the script does not feature. The community feature adds moderation, privacy (health data among strangers) and PDPA exposure with no cost line.
- **Evidence:** `chk:8`; `mkt:11`, `mkt:23`, `mkt:189`; `spec:24`.
- **Failure scenario:** A judge says the claim is correlation, and asks who moderates 1,000 post-MI strangers sharing activity.
- **Fix:** Say "supported by observational data". Consider a LINE family-caregiver loop first. Defer open communities.
- **Needs real expert?** yes (behavior scientist; lawyer for PDPA).

### F12 [S2] No pilot design that produces insurer-grade evidence
- **What is wrong:** The next-steps list (`HANDOFF.md:38-43`) goes from questions to design to build. No pilot design, outcome measure, comparison group, sample size or timeline. There is no success metric an insurer would accept (readmission needs large n; adherence or CR attendance is a feasible proxy).
- **Evidence:** `HANDOFF.md:38-43`; `spec:111-117`.
- **Failure scenario:** Insurer says "come back with data". The team has no plan to generate it.
- **Fix:** Draft a one-page pilot: 30-50 post-MI patients at Siriraj, primary outcome = CR attendance and mission adherence at 12 weeks, with safety events recorded. Sample size and readmission power: NEEDS REAL EXPERT (statistician).
- **Needs real expert?** yes (statistician; Siriraj clinician; IRB).

### F13 [S3] Smaller items
- `mkt:63` header "12-Month Readmission Reduction" row compares to "Baseline" with no number; the table implies a head-to-head trial that does not exist.
- `mkt:182` proposes smartphone computer vision form tracking (Kaia-like). That is not the product in the spec, and it imports scope creep and a separate regulatory burden.
- `mkt:178` "eliminates physician oversight" for EMR triggers is an overclaim.
- Report mixes "Siriraj" as both partner and EMR-integration target (`mkt:172`) without any evidence of integration feasibility. UNSOURCED.
- `chk:5` says 93% of Italian GPs; the script and `spec:36` quote cardiologists at about 81% and 11%. Pick one source and cite the paper.

## What I could not verify
- I did not open any URL, so I could not check whether the cited pages say what the report claims. The mismatches in F4 are inferred from the page titles in `src` and the report's footnote list, not from reading the pages. Treat them as "title does not match claim", not as proven errors.
- Muang Thai Life CI premium growth (>70%), any insurer's willingness to bundle, and OIC filing requirements: UNSOURCED, NEEDS REAL EXPERT (insurer, OIC-literate lawyer).
- Thai smartwatch ownership among post-MI patients aged 45-75: UNSOURCED.
- Thai willingness to pay, CAC, conversion, churn, insurer sales-cycle length: UNSOURCED; none exists in the pack.
- Cardihab 21% to 63% and 11-14% 30-day readmission: sources exist but I did not read the primary papers. Partly verifiable only by a real reader.
- Clinical safety gates G1, G3, G5, G6 are outside my specialty. NEEDS REAL EXPERT (cardiologist, safety engineer, lawyer).
