# P02 · Patients get one guideline for everyone: no clue what fits them, no friends to move with, and no way to trust their own data.

## Key message

Exercise advice after a heart diagnosis is written for everyone and rarely written down for anyone: in an Italian GP survey 93% regularly prescribed physical activity but only 15% gave it in writing. Thai patients fall out of rehabilitation before it starts: in a Bangkok CABG cohort only 12.5% joined phase-2 cardiac rehab, 61.9% of non-attenders did not know it existed, and 31% cited transport. Social support was the only significant predictor of readmission in 321 Thai coronary patients (beta = −0.22), which is why Heartstep recommends people and places, not just exercises.

## Why this matters to the judges

- **Real-world impact** is a judging criterion. This page shows the gap is real, local and measured, and names exactly which numbers come from which study, so the judge can tell evidence from our hypothesis.
- **Innovation** only matters if it targets the real failure. The evidence points to three failures (personal fit, awareness and access, social support) that a generic chatbot or a generic guideline does not address, and one (trust in watch data) that we infer but have not yet measured.
- **Technical coherence:** each pain point maps to one design element: signed limits + catalogue filter (fit), proactive missions at a chosen time (awareness), FHIR `HealthcareService` near home + cohort signal (friends), plain-language missions instead of raw numbers (trust).

## Full detail

### 1. The story we tell (demo/problem-story.html)

Somchai is 58 and has high blood pressure. He receives the standard sheet: 30 minutes a day, 5 days a week, "moderate" intensity, avoid heavy lifting. The same sheet goes to a 35-year-old runner. He has three questions the sheet cannot answer: How hard is "moderate" for me? Can I still play tennis? Is today safe? His tennis group now plays too hard for him, so he exercises alone, or not at all. His watch shows 128 bpm and 6,214 steps but not whether 128 is too high. So nothing changes: "Advice without a personal plan rarely becomes a habit." The story ends: "One guideline for everyone. No plan for Somchai. He needs a plan made for him: his limits, his interests, his neighbourhood."

The story is illustrative. The rest of this page is the evidence behind each scene, with the strength of each piece marked.

### 2. Pain 1 · One guideline for everyone

Guidelines are population advice by design. The 2020 ESC sports cardiology guideline section on hypertension, paraphrased in our demo, recommends "at least 30 min of moderate dynamic aerobic exercise (walking, cycling, swimming) 5–7 days a week", resistance training 2–3 days a week, avoiding heavy isometric lifting and breath-holding, and no high-intensity exercise while systolic pressure is above 160 (`demo/agent-flow-demo.html`, `GUIDE`; paraphrase, primary text not re-checked). That is correct and useless to a patient who wants to know whether his Saturday tennis is still allowed.

Personalisation is supposed to come from the clinician, but it rarely arrives in a usable form. A 2026 review of exercise prescription in clinical populations (Komici et al., *Frontiers in Sports and Active Living*) reports an Italian standardized survey of general practitioners: "only 24% of GPs perform or prescribe physical capacity evaluations. Despite 93% of the GPs regularly prescribed physical activity and exercise, only 15% provided recommendations in writing." The same review says CPET, the most precise basis for an individual intensity, "remains significantly underutilized in contemporary clinical practice" because of technical complexity, insufficient training and poor understanding among referring physicians. These are Italian GPs, not Thai cardiologists; we use them as the best-documented example of the advice-to-plan gap, not as a Thai statistic.

Our earlier pitch line "up to 80% of doctors recommend exercise, only 15% give detailed guidance" mixed two studies and is retired (`research/pitch-claims-check.md`). The "5-minute consultation" line has no source and is also retired.

### 3. Pain 2 · No clue what fits, and no clue rehab exists

The clearest Thai evidence is about cardiac rehabilitation (CR), the structured programme that should translate guidelines into a personal plan. Rangkla et al. (2024, *Health Services Insights*, King Chulalongkorn Memorial Hospital, Bangkok) studied patients after coronary bypass surgery (CABG) who completed in-hospital phase-1 CR between October 2016 and September 2018:

- "The rate of participation in phase-2 CR was only 12.5%."
- Of the 42 non-attenders interviewed by phone, "Did not know that there was phase-2 CR" was the most common reason (61.9%), followed by "Transportation problems" (31%), "Unable to take leave due to work schedule" (19%) and "Did not participate due to chronic diseases and complications" (14.3%).
- 66.7% "reported not having been invited to participate in phase-2 CR or having the program explained to them", and "The majority of the patients (83.3%) reported not being informed about phase 2 CR during a follow-up appointment."
- Half the interviewed patients lived in Bangkok (54.8%); the authors note that tertiary hospitals offering CR are concentrated in Bangkok and provincial city centres, and that most patients return to local hospitals for follow-up.

This is one hospital, one procedure and 42 interviews. It is still the most direct Thai evidence we have that the failure is information and access, not unwillingness.

Globally the picture is the same. The International Council of Cardiovascular Prevention and Rehabilitation audit, reported by the World Heart Federation (5 July 2019), found that "just one in 12 ischemic heart disease patients globally can get rehab", that over 18 million additional rehabilitation spots are needed each year, that "almost half of countries in the globe have absolutely no rehab programs", and that home-based CR was "only offered in 38 countries".

### 4. Pain 3 · No friends to move with

Polsook and Aungsuroch (2021, *Journal of Research in Nursing*) recruited 321 coronary artery disease patients from tertiary hospitals across all regions of Thailand. In multiple regression, "The coefficient for social support (beta = −0.22) was found to be significant (p < 0.05), whereas comorbidity, symptom severity, depression and quality of life were not significant." The authors conclude that nurses "should promote social support interventions". Our research notes quote this as −0.225; the PubMed abstract we opened says −0.22, and we use that.

Two cautions keep us honest. First, this is a cross-sectional association, not a trial of peer groups. Second, a companion study by the same group in 200 Thai MI patients (Polsook and Aungsuroch, *Belitung Nursing Journal*) found the opposite emphasis: its model explained only 4% of readmission variance (R² = 0.04) and "Symptom severity was the most influential factor". In that study 88% of participants "were readmitted only 1 or 2 times within 12 months", which describes readmitted patients, not a population readmission rate; the "88% of post-MI patients are readmitted" line in our market research is wrong and must not be used.

So the defensible claim is: social support is associated with fewer readmissions in one large Thai CAD sample, and exercise is easier to keep up with others. That is enough to justify a "people like you" and "groups near you" signal; it is not evidence that our groups reduce readmissions.

### 5. Pain 4 · No trust in the data

Many patients already wear a watch. The watch shows numbers (128 bpm, 6,214 steps) but not what is safe for this person. Beta-blockers, common after MI, blunt the heart-rate response, so a generic HR zone can mislead; guidelines therefore pair HR with perceived exertion and the talk test (`research/guidelines/app-parameters-qa.md` §2, machine-generated summary, to verify). In our synthetic bundles 8 of 8 patients take a beta-blocker (bisoprolol or metoprolol).

We have **not** found a study measuring Thai cardiac patients' trust in or understanding of their watch data. "No trust in the data" is a team hypothesis from the problem brief ("the data exists, but nobody turns it into action", design spec §1). It is the first thing patient interviews should test.

### 6. From pain to design

| Pain | Evidence strength | Design answer | Where |
|---|---|---|---|
| One guideline for everyone | Moderate (Italian GP survey; guideline text) | Clinician signs a limit record; rules filter the catalogue to what fits | P04, P06 |
| No clue rehab exists / what to do | Strong for Thai CABG (single site) | App starts the conversation at a chosen time; 1–2 missions a day | P11 |
| No friends to move with | Moderate (cross-sectional, n = 321) | "People like you" + groups near home from FHIR `HealthcareService` | P08, P09 |
| No trust in watch data | Hypothesis only | Missions in plain words ("you can still talk"), RPE check, HR only as a ceiling | P12 |
| Transport and work | Single-site (31%, 19%) | Home-district groups, evening and weekend slots | P08 |

## Visualizations

### Chart 1 · Bar: why Thai CABG patients missed phase-2 rehab

- **Type:** horizontal bar, sorted descending.
- **Title:** "Not knowing, not being told, not getting there"
- **Axis:** % of the 42 interviewed non-attenders (more than one reason allowed).

| Reason (patient-reported) | % | Approx. n of 42 (derived) |
|---|---|---|
| Did not know phase-2 CR existed | 61.9 | 26 |
| Transportation problems | 31.0 | 13 |
| Could not take leave from work | 19.0 | 8 |
| Chronic disease or complications | 14.3 | 6 |

Annotation: "Phase-2 participation: 12.5% · 83.3% not told at follow-up · single hospital, Bangkok, 2016–2018." **What to notice:** the top barrier is information, the second is distance; both are things an app plus local groups can change, unlike the comorbidity barrier. Counts are derived by us (percentage × 42) and rounded.

### Chart 2 · Funnel: from advice to a written plan (Italian GPs)

- **Type:** three-step funnel.
- **Title:** "Almost every GP recommends exercise; few write it down or measure capacity"

| Step | % of GPs |
|---|---|
| Regularly prescribe physical activity and exercise | 93 |
| Perform or prescribe a physical-capacity evaluation | 24 |
| Give recommendations in writing | 15 |

Annotation: "Italian standardized GP survey, cited in Komici et al. 2026." **Notice:** the drop is not about motivation to recommend; it is about turning advice into a personal, written plan. Not Thai data.

### Chart 3 · Waffle or icon array: global access to cardiac rehab

- **Title:** "1 in 12 heart patients worldwide can get rehab"
- **Data:** 12 icons, 1 filled. Side facts: about half of countries have no programme; 18 million more spots needed a year; home-based CR offered in 38 countries (ICCPR audit via World Heart Federation, 2019).

### Chart 4 · Coefficient bar: predictors of readmission in Thai CAD patients

| Predictor | Result in Polsook & Aungsuroch 2021 (n = 321) |
|---|---|
| Social support | beta = −0.22, p < 0.05 (significant) |
| Comorbidity | not significant |
| Symptom severity | not significant |
| Depression | not significant |
| Quality of life | not significant |

Draw one bar for social support and grey "n.s." markers for the others (the abstract does not give their coefficients). Footnote: "Companion MI study (n = 200) found symptom severity most influential; model R² = 0.04." **Notice:** the evidence for "friends" is real but modest.

### Diagram · Four scenes to four design answers

Four panels from the problem story (sheet for everyone; "Can I still play tennis?"; exercising alone; "Is 128 too high?") each with an arrow to its Heartstep answer (signed limit + filter; recommendation from what you loved; groups near you; plain-words mission with RPE check).

## Numbers and claims ledger

| Claim | Value | Source | Status |
|---|---|---|---|
| GPs regularly prescribing exercise | 93% | Komici et al. 2026, PMC12990137 (citing Italian survey) | checked |
| GPs giving it in writing | 15% | same | checked |
| GPs doing capacity evaluation | 24% | same | checked |
| CPET "significantly underutilized" | quote | same | checked |
| Phase-2 CR participation after CABG | 12.5% | Rangkla et al. 2024, PMC11456183 | checked |
| Did not know phase-2 CR existed | 61.9% | same | checked |
| Transport / work / comorbidity | 31% / 19% / 14.3% | same | checked |
| Not informed at follow-up | 83.3% | same | checked |
| Not invited during admission | 66.7% | same | checked |
| Interviewed non-attenders | 42 | same | checked |
| IHD patients with access to rehab | 1 in 12 | World Heart Federation, ICCPR audit, 2019 | checked |
| Additional rehab spots needed per year | > 18 million | same | checked |
| Countries with home-based CR | 38 | same | checked |
| Social support beta, Thai CAD | −0.22 (n = 321) | PubMed 35251254 abstract | checked (repo said −0.225) |
| MI model R² | 0.04 | PMC10353658 | checked |
| "88% readmitted 1–2 times" | among readmitted patients only | PMC10353658 Table 1 | checked; not a population rate |
| ESC 2020 hypertension lines | 4 lines | `demo/agent-flow-demo.html` `GUIDE` | paraphrase; primary text to verify |
| Synthetic patients on a beta-blocker | 8 of 8 | `synthetic/fhir/*.json` (counted) | synthetic |
| Thai patients do not trust watch data | — | design spec §1 | hypothesis, to verify |
| "5-minute consultation" | — | none | unsupported, retired |

## Limits and open questions

- No Thai post-MI (as opposed to post-CABG) phase-2 uptake figure was opened. Thai nationwide CR uptake (rehabmed.or.th PDF cited in the market report) is not yet re-read.
- No Siriraj-specific numbers. The Siriraj mentor is the best source for consultation length and local referral rates.
- "No trust in data" has no source; patient interviews (10–15 post-MI patients) are needed.
- The GP survey is Italian; a Thai cardiologist survey would be much stronger.
- The social-support evidence is associational and mixed across the two Thai studies.

## Likely judge questions

1. **"Is this a Thai problem or a global one?"** Both: globally 1 in 12 heart patients can get rehab; in a Bangkok CABG cohort only 12.5% joined phase-2 rehab and 61.9% of non-attenders did not know it existed.
2. **"Where does '80% recommend, 15% detail' come from?"** It did not survive checking. The sourced figures are 93% of Italian GPs prescribe exercise, 15% in writing, 24% assess capacity.
3. **"Do peer groups reduce readmission?"** We do not claim that. One Thai study (n = 321) found social support was the only significant predictor of readmission (beta −0.22); another (n = 200) did not. We use it to motivate the feature, and adherence is what a pilot will measure.
4. **"Why not just send patients to hospital rehab?"** Because the top reasons they miss it are not knowing, distance and work. Home-district groups and phone missions address those; supervised rehab stays the path for moderate and high risk (P05, P18).
5. **"How do you know patients don't trust their watch?"** We don't yet; it is a hypothesis from the brief and the first interview question.

## Sources

Repo:
- `demo/problem-story.html`, `demo/agent-flow-demo.html` (`GUIDE`)
- `research/pitch-claims-check.md`, `research/README.md`, `research/market/notebooklm-deep-report.md` (with team corrections), `research/guidelines/app-parameters-qa.md`
- `docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md` §1, §2b
- `synthetic/fhir/*.json`

External (opened 2026-10-18; PMC pages read through the Europe PMC full-text service):
- Rangkla S. et al., "Exploring the Impediments: Investigating Barriers to Participation in Phase-2 Cardiac Rehabilitation Following Coronary Artery Bypass Graft Among Thai Patients", Health Services Insights 2024, doi:10.1177/11786329241287397: https://pmc.ncbi.nlm.nih.gov/articles/PMC11456183/
- Komici K. et al., "Practical guidelines for exercise prescription in different clinical populations", Front Sports Act Living 2026, doi:10.3389/fspor.2026.1649549: https://pmc.ncbi.nlm.nih.gov/articles/PMC12990137/
- Polsook R., Aungsuroch Y., "A cross-sectional study of factors predicting readmission in Thais with coronary artery disease", J Res Nurs 2021 (abstract): https://pubmed.ncbi.nlm.nih.gov/35251254/
- Polsook R., Aungsuroch Y., "Factors influencing readmission among Thais with myocardial infarction", Belitung Nurs J, doi:10.33546/bnj.1234: https://pmc.ncbi.nlm.nih.gov/articles/PMC10353658/
- World Heart Federation, ICCPR global CR survey news (5 July 2019): https://world-heart-federation.org/news/international-council-of-cardiovascular-prevention-and-rehabilitation-iccpr-carries-out-first-ever-survey-of-cardiac-rehabilitation-around-the-globe/

## Image-generation prompt

Design one 16:9 information slide on a white background. Lead with the key message as the title: "Patients get one guideline for everyone: no clue what fits them, no friends to move with, and no way to trust their own data." Make the main chart a horizontal bar chart "Why Thai CABG patients missed phase-2 rehab" with exactly these values: Did not know it existed 61.9%, Transportation 31%, Could not take leave 19%, Chronic disease 14.3%, and the callouts "Phase-2 participation 12.5%" and "83.3% not told at follow-up". Add two small supporting figures: "93% of Italian GPs prescribe exercise, 15% in writing" and "1 in 12 heart patients worldwide can get rehab". Footnote the sources (Rangkla 2024; Komici 2026; ICCPR/WHF 2019). No logos, no invented numbers; choose the design freely.
