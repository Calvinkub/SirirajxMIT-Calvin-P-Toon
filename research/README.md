# Research folder

Built 2026-10-17 with NotebookLM (notebook "SirirajxMIT — CVD Mission Coach (market + guidelines)", 55 sources, owner: Calvin's Google account).
Everything here is **machine-generated first-pass research**. Check each number against its source before it goes in the pitch.

| File | What it is |
|---|---|
| [guidelines/app-parameters-qa.md](guidelines/app-parameters-qa.md) | Exercise intensity without CPET, beta-blockers, stop criteria, risk classes, FITT, home-CR safety, Thai context |
| [guidelines/notebooklm-deep-report.md](guidelines/notebooklm-deep-report.md) | Long deep-research report on post-MI exercise guidelines |
| [guidelines/sources.md](guidelines/sources.md) | Guideline source links |
| [market/notebooklm-deep-report.md](market/notebooklm-deep-report.md) | Thai burden, CR uptake, competitors, insurers, wearables, GTM |
| [market/sources.md](market/sources.md) | Market source links |
| [pitch-claims-check.md](pitch-claims-check.md) | Which pitch-script numbers are supported, and which are not |

## What this changes in the design

1. **Open question 0 (no CPET) has an answer.** Guidelines accept other ways to set intensity: symptom-limited ECG stress test, 6-minute walk test, % heart-rate reserve, resting HR + 20–30 bpm, Borg RPE 11–14, talk test. On beta-blockers, use RPE and talk test first. The app should accept these as inputs, flagged by "who set the limit".
2. **Only some patients suit unsupervised home use.** AACVPR low risk (e.g. LVEF ≥ 50%, uncomplicated, ≥ 7 METs, no depression) are suitable for app-only. Moderate risk need a few supervised sessions first. High risk (e.g. LVEF < 35–40%, ICD, complex arrhythmia) are **not** suitable. The app needs a risk-class gate at onboarding.
3. **Stop rules are concrete** (chest pain, severe breathlessness, dizziness or fainting, palpitations). See Q&A section 3. These stay hard-coded, never LLM-generated.
4. **Thai gap is real.** Thai post-ACS recommendations say start rehab within 10 days of discharge. Phase-2 outpatient uptake after CABG was reported at 12.5%, and 83.3% of those patients said they were never told about it (single-site study). A Thai LINE-based home-CR study (n = 54) showed better 6-minute-walk and quality-of-life scores than controls. LINE is a delivery channel worth considering next to push notifications.
5. **Social support predicts readmission in Thai cohorts** (reported β = −0.225). This supports the peer-community feature in the pitch script.

## Market in short (verify before use)

- Insurer entry point: critical-illness cover (Muang Thai Life reported > 70% CI premium growth), AIA Vitality as a wearable-linked wellness channel.
- Public schemes (UCS, CSMBS, SSS) have no fee code for digital therapeutics, so private insurers and self-pay come first.
- Closest competitors: Movn Health (US, 12-week virtual CR with watch and BP kit) and Cardihab (Australia). Both are clinician-led. We have not found a Thai-language, patient-first, daily-mission competitor, but that is **not** a proven absence.
- The report suggests Thai self-pay tiers of 299–599 THB per month (basic) and 1,500–3,500 THB per month (clinical). Our 499 starting price sits in the basic tier. This is a model suggestion, not survey data.

## Known weak spots in the research

- Company-sourced claims (Movn 20–30% fewer readmissions, Cardihab 21% → 63% uptake) are vendor data, not independent trials.
- Competitor rows for Kaia, Sword, Hinge, Vivira, Welldoc come from model background knowledge, not cited pages. They are MSK or diabetes products, not cardiac.
- Thai readmission figures: the "88% had 1–2 readmissions" line almost certainly describes patients who were readmitted at least once, not all post-MI patients. Do not quote it as a population rate.
- No Thai willingness-to-pay data was found. A short patient and insurer interview round is the gap to close.
