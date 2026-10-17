# Parameters to reconcile — questions for the Siriraj rehab physician / cardiologist

Status: **do not implement any value from `app-parameters-qa.md` or `notebooklm-deep-report.md` until this table is filled in by a real clinician.** Both files are machine-generated and contradict each other. Citation line numbers are from the 2026-10-17 repo.

For each row, please give: the value to use in v1, the source (guideline, version, page), and your name and date.

| # | Question | Source A says | Source B says | Why it matters |
|---|---|---|---|---|
| 1 | Standard moderate-intensity target after MI | `app-parameters-qa.md:21` 50–70% HRR | `notebooklm-deep-report.md:69` VT1 is about 39–45% HRR post-MI, so 50–70% may exceed VT1 | A patient could be capped above their first ventilatory threshold |
| 2 | Beta-blocker adjustment | `qa:40` raise K from 0.6 to 0.8; `qa:41` subtract 10 bpm from age-predicted max | `deep:127` age-predicted max overestimates by 20–40 bpm (uncited) | Over-prescription in the largest patient group. Proposal: v1 drops %HRR and uses a clinician HR ceiling plus RPE 11–13 and talk test |
| 3 | Resistance training start | `qa:108-109` post-MI 1–4 weeks; upper body 12 weeks after CABG | `deep:110` 2–4 weeks post-PCI; 4–6 weeks post-CABG | Sternal healing. Proposal: v1 has no resistance missions |
| 4 | Talk test definition | `qa:30` full sentences | `deep:86` short phrases at moderate intensity | The main safety check for a beta-blocked patient |
| 5 | Risk class bands | `qa:69` low = LVEF ≥ 50; moderate 35–49 or 40–49; high < 35 or < 40 | `deep:32-33` low > 50; moderate 40–49 | Who is eligible for app-only use |
| 6 | MET thresholds across classes | overlapping bands in `qa` | see `deep:32-33` | Same |
| 7 | ICD as high-risk marker | `qa:89` lists ICD under high risk | not stated | Is that in the AACVPR scheme or a local rule? |
| 8 | Session length | `qa` 20–60 min | `deep` "minimum 40 min continuous" plus 10 + 10 warm-up and cool-down | Starting duration for a deconditioned patient |
| 9 | Weekly progression | `qa:121` 5–10% per week | system-eval property 5 caps at 10% | Cap value |
| 10 | Stop criteria | `qa` §3 is a laboratory test-termination list | not adapted for home | Which items are valid for a patient at home with no BP cuff? What rest, delayed-symptom or "not today" rules apply? |
| 11 | Thai heat | not covered | not covered | Outdoor walking limits by time and temperature |
| 12 | Home-safety evidence | `qa` §6 event rates are from supervised centres; serious-adverse-event RR 1.30 (0.63–2.67) read as non-inferior | — | Wording of any safety claim |

Also needed from the clinician: default behaviour for a user with no limit record; the Thai red-flag phrase list (with negation, e.g. "ไม่เจ็บหน้าอก"); drug-interaction rules beyond beta-blockers (nitrates, anticoagulants, diabetes drugs, diuretics); and whether 1669 is the right number to show.
