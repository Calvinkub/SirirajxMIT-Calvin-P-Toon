> NotebookLM answer (2026-10-17) from the 55-source notebook, saved verbatim. Bracketed numbers are NotebookLM citation indices, not our own. Machine-generated: confirm against the primary guideline before any value goes into the rules engine. Clinician (Siriraj) must sign off on all thresholds.

# Exercise parameters for a post-MI home-exercise app

Here are the evidence-based guidelines and exact numerical parameter recommendations for designing a post-MI home exercise scheduling app, grounded directly in the clinical guidelines and studies in your notebook.

---

### **(1) Exercise Intensity Prescription Without CPET**

When Cardiopulmonary Exercise Testing (CPET) with gas exchange analysis is unavailable, guidelines recommend deriving target intensity from a symptom-limited ECG exercise stress test (EST), functional walking tests, or validated subjective scales [1-3].

* **Symptom-Limited ECG Exercise Stress Test (Treadmill or Cycle Ergometer):**
  * **Method:** Uses peak heart rate (\\(\text{HR}_{\text{peak}}\\)) or Heart Rate Reserve (\\(\text{HRR} = \text{HR}_{\text{peak}} - \text{HR}_{\text{rest}}\\)) obtained from a maximal/symptom-limited test on standard cardiovascular medications [4-6].
  * **Endorsing Guidelines:** Endorsed as the primary non-CPET alternative by the **IACR (2025)** [2, 3, 6], **AACVPR** [7], **ESC Guidelines on Sports Cardiology (2020)** [4, 8], **French Society GERS-P (2022)** [1, 9], and **EAPC** [10, 11].
* **6-Minute Walk Test (6MWT) / Functional Walk Tests:**
  * **Method:** Used to assess submaximal functional capacity and guide initial low-to-moderate exercise prescription when treadmill/cycle testing is unavailable or unsafe [1, 2, 12].
  * **Endorsing Guidelines:** Endorsed by **IACR (2025)** [2, 3], **French Society GERS-P** [1], and **EAPC Position Statements** [13].
* **Percentage of Heart Rate Reserve (%HRR) / Karvonen Formula:**
  * **Formula:** \\(\text{Target HR} = \text{HR}_{\text{rest}} + \%HRR \times (\text{HR}_{\text{peak}} - \text{HR}_{\text{rest}})\\) [5, 9, 14].
  * **Target Range:** **40%–80% HRR** (standard moderate intensity is **50%–70% HRR**; **40%–50%** for deconditioned or high-risk patients) [7, 15-17]. French GERS-P uses \\(K = 0.6\\) for standard patients or \\(K = 0.8\\) for those on beta-blockers [9, 18].
  * **Endorsing Guidelines:** **AACVPR** [7], **IACR (2025)** [16, 17], **ESC (2020)** [14, 19], **French GERS-P** [9, 18], and **AHA/AACVPR** (defining moderate intensity as **40%–59% HRR**) [20, 21].
* **Resting HR + 20–30 bpm (\\(\text{RHR} + 20\text{--}30\\)):**
  * **Formula:** \\(\text{Target HR} = \text{Resting HR} + 20 \text{ to } 30 \text{ bpm}\\) [22, 23].
  * **Endorsing Guidelines:** Endorsed by **AACVPR** and **ACSM** for early outpatient Phase II / early post-MI mobilization or when no baseline stress test has been conducted [22, 24, 25].
* **Borg Rating of Perceived Exertion (RPE):**
  * **Target Range:** **11–14 / 12–14** on the 6–20 Borg scale ("fairly light" to "somewhat hard") or **3–4** on the 0–10 Modified Borg scale [15, 16, 26-28].
  * **Endorsing Guidelines:** **ESC (2020)** [19], **EAPC** [10], **AACVPR** [7], **IACR (2025)** [16, 27], and **ACSM** [29].
* **Talk Test:**
  * **Method:** Maintain exertion at a level where the patient can converse in full sentences comfortably without gasping ("can talk while exercising") [10, 19, 28, 30].
  * **Endorsing Guidelines:** Endorsed by **ESC (2020)** [19], **EAPC** [10, 31], **IACR (2025)** [32], and **AACVPR** [30] as an adjunct tool, especially for home-based cardiac rehabilitation [30, 31].

---

### **(2) Exercise Intensity on Beta-Blockers**

Beta-blockers attenuate peak heart rate and chronotropic response, making age-predicted maximal HR equations (\\(220 - \text{age}\\)) inaccurate [14, 19, 33, 34].

1. **Test On-Medication:** Stress testing MUST be performed while the patient is taking their prescribed beta-blocker dose to capture true peak HR [6, 19, 33].
2. **HRR Karvonen Adjustment:** In the Karvonen equation (\\(\text{Exercise HR} = \text{HR}_{\text{rest}} + K \times \text{HRR}\\)), adjust the multiplier \\(K\\) from \\(0.6\\) to **\\(0.8\\)** for patients on beta-blocker therapy [9, 18].
3. **Age-Predicted Fallback Deduction:** If an exercise test is unavailable and age-predicted max HR must be used, deduct **10 bpm** from the estimated max HR before applying target HR ranges [33].
4. **Dose Modification Adjustment:** If beta-blocker dosage changes during rehabilitation, reset target HR by measuring steady-state HR after \\(\ge 5 \text{ minutes}\\) of exercise at the patient's prior workload [35].
5. **Primary Reliance on RPE & Talk Test:** Subjective monitoring via **Borg RPE 11–14** and the **Talk Test** should be prioritized alongside HR monitoring to ensure clinical safety and avoid under- or over-exercising [19, 36-38].

---

### **(3) Criteria to Stop Exercise Immediately & Seek Emergency Care**

The app should instruct patients to cease exercise and alert emergency care if any of the following develop [39-42]:

* **Angina or Ischemic Symptoms:** Chest pain, pressure, tightness, heaviness, or pain radiating to the jaw, neck, back, or arm [41-43].
* **Severe Dyspnea:** Sudden or extreme shortness of breath disproportionate to exertion level [41-43].
* **Central Nervous System Symptoms:** Dizziness, lightheadedness, confusion, ataxia, or syncope/fainting [41-43].
* **Arrhythmias / Palpitations:** Sudden very rapid, pounding, or irregular heartbeat [39, 41, 42].
* **Hemodynamic Criteria:**
  * Drop in Systolic Blood Pressure (SBP) \\(> 10\text{--}15 \text{ mmHg}\\) below baseline despite increasing workload [39, 41].
  * SBP surge \\(> 250 \text{ mmHg}\\) or Diastolic Blood Pressure (DBP) \\(> 115 \text{ mmHg}\\) (or SBP increase \\(> 40 \text{ mmHg}\\) above rest) [41, 44].
* **Heart Rate Drop:** Drop in HR \\(> 10 \text{ bpm}\\) during exercise or chronotropic failure to rise with effort [39, 41].
* **ECG Red Flags (if connected via telemetry):** ST-segment depression \\(\ge 2 \text{ mm}\\) or new ST elevation [39, 43, 45].

*App Virtual Emergency Protocol:* Require location confirmation at session start; if red flags occur, trigger immediate session termination, local EMS notification, and provider escalation [40].

---

### **(4) AACVPR Risk Stratification & Unsupervised Home CR Suitability**

#### **AACVPR Risk Classes [81–83, 109, 159–161, 281–285]:**
* **LOW RISK (ALL factors must be present):**
  * Left Ventricular Ejection Fraction (LVEF) \\(\ge 50\%\\) [43, 46-48].
  * Uncomplicated MI, CABG, or PCI without CHF or post-event ischemia [46, 49-51].
  * Normal ECG and hemodynamics during exercise and recovery; no complex resting/exercise dysrhythmias [43, 46-49].
  * Asymptomatic (no angina, dizziness, dyspnea) [46-49].
  * Measured functional capacity \\(\ge 7.0 \text{ METs}\\) [46, 49-51].
  * Absence of clinical depression [46, 49-51].
* **MODERATE RISK (ANY 1 present, or not meeting Low/High):**
  * LVEF \\(35\% \text{ to } 49\%\\) (or \\(40\%\text{--}49\%\\)) [47-49].
  * Angina or ischemic symptoms occurring only at moderate-to-high exertion (\\(\ge 5\text{--}7 \text{ METs}\\)) [47, 52, 53].
  * Mild to moderate silent ischemia (ST depression \\(< 2 \text{ mm}\\)) [52, 53].
  * Functional capacity \\(< 5.0 \text{ METs}\\) [53].
* **HIGH RISK (ANY 1 present):**
  * LVEF \\(< 35\%\\) or \\(< 40\%\\) [39, 47, 54].
  * Survivor of cardiac arrest or sudden death [39, 50, 54].
  * Complex dysrhythmias at rest or exercise [39, 47, 55].
  * Post-event shock, CHF, or post-procedure ischemia [39, 50, 54].
  * Abnormal exercise hemodynamics (flat/decreasing SBP, severe hypotension) [39, 54].
  * Silent ischemia \\(\ge 2 \text{ mm}\\) ST depression [43, 55].
  * Symptoms at low exertion (\\(< 5.0 \text{ METs}\\)) [43, 47, 55].
  * Functional capacity \\(\le 3.0 \text{ METs}\\) [54].
  * Presence of an ICD or clinical depression [43, 50, 54].

#### **Suitability for Unsupervised Home-Based or Digital Rehabilitation:**
* **Low-Risk Patients:** **Fully suitable** for unsupervised home-based CR, digital mobile health (mHealth) applications, and virtual telerehabilitation [56-60].
* **Moderate-Risk Patients:** **Eligible for teleguided/telemonitored hybrid home CR** after completing an initial supervised center-based orientation (3–6 sessions) [57, 59, 61-63].
* **High-Risk Patients:** **NOT suitable** for unsupervised home exercise; require direct medical supervision with continuous telemetry monitoring for at least 18–36 sessions [64-66].

---

### **(5) Recommended FITT & Progression Rules for Phase II/III**

#### **Aerobic Training FITT:**
* **Frequency:** **3–5 days/week** (progressing to 6–7 days/week for light/moderate activity) [7, 15, 28, 67, 68].
* **Intensity:** **40%–80% HRR** (standard post-MI target **50%–70% HRR**), Borg RPE **12–14** (6–20 scale) or **3–4** (0–10 scale) [7, 15, 16, 27, 28].
* **Time (Duration):** **20–60 minutes/session** (20–45 min conditioning phase + 5–10 min warm-up and cool-down) [7, 9, 15, 69].
* **Type:** Rhythmic, continuous dynamic exercise engaging large muscle groups (walking, stationary cycling, treadmill) [7, 15, 67].

#### **Resistance Training FITT:**
* **Initiation Timing:**
  * **Post-MI:** Initiated **1–4 weeks** post-event, following at least 1–2 weeks of well-tolerated aerobic exercise [70-72].
  * **Post-CABG / Open-Heart Surgery:** Upper-body resistance postponed for **3 months (12 weeks)** to ensure full sternal healing [70, 71, 73-75].
* **Frequency:** **2–3 days/week** (with \\(\ge 48\text{ hours}\\) rest between same muscle groups) [15, 28, 67, 71, 76].
* **Intensity:**
  * Upper body: **30%–70% 1-RM** [15, 67, 76].
  * Lower body: **40%–80% 1-RM** [15, 67, 76].
  * Perceived exertion: OMNI-RES **3–5/10** initially up to **5–8/10**, or Borg RPE **11–13** up to **13–15** [15, 18, 28, 77].
* **Time/Volume:** **1–3 sets**, **8–15 repetitions** per exercise; session duration **20–30 minutes** [15, 28, 68, 76].
* **Type:** Light dumbbells (1–3 lbs / 0.5–1.5 kg initially), resistance bands, weight machines, or bodyweight [70, 73, 76]. **Avoid Valsalva maneuvers** [28, 78, 79].

#### **Progression Rules:**
1. **Duration Before Intensity:** Always increase session duration before increasing exercise intensity [79-83].
2. **Single Variable Increment:** Adjust only ONE FITT parameter at a time [81, 82].
3. **5%–10% Weekly Rate:** Increase duration or intensity by **5%–10% per week** [81].
4. **Interval-to-Continuous Transition:** Deconditioned patients begin with short interval bouts (3–5 min work with active rest) and gradually decrease rest periods until 30 minutes of continuous exercise is maintained [25, 83, 84].
5. **Resistance Phase Progression:** Phase 1 (technique): 10–15 reps at 20%–30% 1-RM \\(\rightarrow\\) Phase 2 (endurance): 12–25 reps at 30%–40% 1-RM \\(\rightarrow\\) Phase 3 (strength): 8–15 reps at 40%–60% 1-RM across 3–4 weeks [77, 85].

---

### **(6) Safety Evidence for Home-Based & Telemonitored CR (Event Rates)**

* **Center-Based Event Rates:**
  * Cardiac arrest rate: **1 per 116,906 patient-hours** [86].
  * Fatal cardiac event rate: **1 per 752,081 patient-hours** [86].
* **Home-Based / Telemonitored CR Safety Meta-Analyses:**
  * Systematic reviews (Cochrane Review by Taylor et al., Huang et al., Li et al. 2025) demonstrate **no statistically significant differences in all-cause mortality or serious adverse events (SAEs)** between home-based/telemonitored CR and center-based CR in low-to-moderate risk CAD/post-MI patients [61, 87-90].
  * **Mortality Risk Ratio:** \\(\text{RR} = 1.06\\) (95% CI: 0.76–1.49) [89].
  * **Serious Adverse Events Risk Ratio:** \\(\text{RR} = 1.30\\) (95% CI: 0.63–2.67) [89].
* **Consensus Conclusion:** Home-based telemonitored CR is clinically safe and non-inferior to center-based CR when low-to-moderate risk criteria and emergency protocols are maintained [61, 87, 88, 90, 91].

---

### **(7) Thailand-Specific Context & Studies**

* **Thai Post-ACS Recommendations (2020 Steering Committee Guidelines):**
  * All post-ACS patients in Thailand should be offered cardiac rehabilitation as early as possible and **no later than 10 days post-discharge** [92, 93].
  * Emphasizes establishing standardized post-discharge secondary prevention protocols to reduce the **14%–25% 1-year post-discharge mortality rate** in Thai ACS patients [94, 95].
* **Cardiac Rehab Uptake in Thailand:**
  * Center-based CR utilization in Thailand remains low (\\(\sim 20\%\\)) due to travel distances, cost, and geographical barriers [92, 94, 96, 97].
  * **Phatthalung Hospital Study (Salinpramote 2022):** Evaluated 113 post-MI working-age patients following CR. **88.49%** of patients successfully returned to work [12, 92]. Return-to-work success was significantly correlated with 6MWT distance, DASI scores, LVEF, and CR participation (\\(p < 0.05\\)) [12].
* **LINE App Home-Based CR Study Results (MDPI 2025 / Ramathibodi & Rajavithi Hospitals, Mahidol University):**
  * **Study Design:** 54 open-heart surgery / CAD patients (27 intervention via LINE app vs. 27 standard care control), completing a 12-week program with 10 digital touchpoints (video calls, e-handbook, exercise videos, self-care logs) [98-100].
  * **Functional Capacity Outcome:** The LINE app intervention group achieved **statistically significantly higher functional capacity** on both the 6MWT and the Duke Activity Status Index (DASI) compared to controls (\\(p < 0.05\\)) [98].
  * **Quality of Life (SF-36) Outcome:** The LINE app group demonstrated significantly higher overall Quality of Life (\\(p < 0.05\\)), with marked improvements in physical functioning, emotional roles, vitality, mental health, social functioning, and general health (\\(p < 0.05\\)) [98].
  * **Clinical Utility:** Using ubiquitous smartphone messaging tools like LINE removes travel barriers in Thailand, promotes self-efficacy under Orem's self-care framework, and provides a feasible, scalable model for home digital CR [97, 98, 101].

---
