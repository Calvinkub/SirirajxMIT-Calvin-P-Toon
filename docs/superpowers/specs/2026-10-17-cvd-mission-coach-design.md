# CVD Mission Coach — Design Draft

Status: **DRAFT v0.1, 2026-10-17.** Brainstorm in progress. Anything tagged *(guess)* is a working assumption and has not been confirmed by the team. Statements without a tag come from Calvin's problem brief.

## 1. Problem (from Calvin's brief)

- A patient gets a diagnosis of a cardiovascular disease (CVD). They now have to change how they live. For example, their exercise intensity often has to be *lower* than before, not higher.
- Most of these patients already know they are at risk. Many already wear a smartwatch that collects data.
- They do **not** know what to do day to day. The data exists, but nobody turns it into action.
- Goal: let the patient act **"brainless"**. They get small, easy tasks as notifications on the watch or phone. They do the task and tick it off. They never have to interpret the data.

## 2. Customer journey (from brief)

1. **Open app.**
2. **Demographics.** Age, sex, diagnosis, medications, and so on.
3. **Goal declaration.** The patient talks with an AI agent. The agent connects to the smartwatch app through MCP and agrees weekly and daily missions with the patient, as a conversation.
4. **Personalized plan and recommendations.** Missions are pushed to the watch or phone, and the plan adapts each week.

## 2b. What the Draft 1 pitch script settles (team input, 2026-10-17)

- **Lead example user:** a patient recovering from a myocardial infarction (MI). We no longer need to guess the lead user for the pitch.
- **Core framing:** the app delivers an AI-built *exercise prescription*. The gap it fills: doctors recommend exercise, but a 5-minute consult leaves no time to write a detailed plan.
- **Inputs:** cardiac, pulmonary, and metabolic risk factors; daily symptoms; lifestyle habits; and **CPET results**. CPET is the main source of the safe-intensity limits. This fits safety rule 1 well: thresholds from the test (e.g. HR at VT1) become the hard bounds on every mission.
- **Adherence:** peer communities with shared activity goals. This is a new feature that was not in the first brief.
- **Business model:**
  - B2B2C: sell to insurers as a rehab package. The pitch is fewer readmissions and lower long-term cost.
  - B2C: freemium. Users get one free 1-week schedule, then Premium at 1, 3, or 12 months, starting at 499 (THB assumed).

**How the script and Calvin's brief fit together:** CPET supplies the *precise* limits. The "brainless" mission layer turns those limits into tiny daily tasks. The pitch should say both halves clearly. "Precise prescription" alone sounds like a document. "Brainless missions" alone sounds unsafe.

### Script review notes

| Line in script | Issue | Suggested fix |
|---|---|---|
| "Up to 80% of doctors recommend exercise, but only 15% provide detailed guidance" | We could not find a source with exactly 80/15. The closest found: ~81% of cardiologists prescribe exercise, but only ~11% give it in writing, and intensity, type, and duration are stated in less than half of cases (EAPC/EXPERT-related survey work). | Cite a real paper and use its exact numbers, or cut the numbers. |
| "5-minute consultation" | Needs a Thai or Siriraj source, or soften the wording ("a short outpatient visit"). | Ask the Siriraj mentor for the local number. |
| "designs an optimal, exact plan … with ease" | This is an overclaim. "Optimal" and "exact" invite judges to ask "proven how?" | Say "a plan kept inside your clinician's safe limits, adjusted each week." |
| "proven tool to reduce readmission rates" (insurer pitch) | Not proven yet, since we have no data. | Say "designed to improve rehab adherence, which is linked to fewer readmissions". Then cite cardiac-rehab evidence, not our app. |
| AI writes an "exercise prescription" | Likely puts the app in Thai FDA SaMD territory. | Frame it as "clinician-approved limits → AI schedules within them". |
| Who generates the plan when there is no CPET? | B2C freemium users mostly won't have a CPET. The script doesn't say what happens to them. | See open question 0. |

**Prior art to know:** the EAPC **EXPERT tool** is a digital decision-support tool that helps clinicians write exercise prescriptions for CVD patients. It targets clinicians. Our difference: it is patient-facing, adapts daily from the watch, and runs as a conversation.

## 3. Target user *(guess, to confirm)*

- Thai adult, roughly 45–75 years old, discharged after a CVD event or diagnosis. Examples: post-MI, stable angina, heart failure with stable EF, hypertension with high risk.
- Owns a smartphone and often a smartwatch: Apple Watch, Samsung Galaxy Watch, Garmin, Huawei, or Xiaomi.
- Siriraj Hospital cardiology or cardiac rehab is the context, because the project is SirirajxMIT.

## 4. Goals / non-goals / anti-goals

**Goals**
- Turn watch data plus the clinician's limits into **one or two tiny missions per day**. Examples: "Walk 10 min after lunch, stay below 110 bpm" or "Take evening meds", with one tap to complete.
- Use conversation, not forms, to set goals. Weekly check-in with the agent.
- Stay safe by default. Missions never go beyond the clinician-set limits.

**Non-goals (v1)**
- Diagnosis or risk prediction.
- Replacing cardiac rehab or the cardiologist.
- Building our own watch firmware or watch-face app. We use the phone's push notifications, which mirror to the watch.

**Anti-goals (failure even if it "works")**
- A mission pushes a patient above a safe heart rate or exertion level.
- The patient has to read charts or numbers to know what to do.
- Notification fatigue that makes the patient mute the app within a week.

## 5. Clinical safety rules (must hold in any build)

These rules come from standard cardiac-rehab practice. Confirm them with the Siriraj clinical mentor.

1. **Exercise limits come from the clinician, not from the AI.** Store the limits per patient: max HR or HR range, Borg RPE target, and allowed activity types. The agent may only choose missions *inside* those limits.
2. **Do not rely only on heart rate.** Beta-blockers blunt HR. Pair every exercise mission with an RPE ("talk test") check.
3. **Red-flag symptoms override everything.** Chest pain, unusual breathlessness, dizziness, fainting, and palpitations all trigger one response: "Stop now and call 1669." The app sends no coaching in that case. The LLM must not handle this path. Use hard-coded logic.
4. **No new limit without a clinician.** If the data suggests the patient could do more, the app flags this for the clinician. It never raises the patient's limit by itself.
5. **Regulatory framing.** Position v1 as a lifestyle/adherence support tool, not as a diagnostic tool. Avoid wording like "diagnose" or "detect". Check this against Thai FDA SaMD rules before any real-patient pilot.

*Added 2026-10-17 after the first simulated panel run (see `evaluation/reviews/2026-10-17-document/SYNTHESIS.md`). These are proposed team rules, not yet reviewed by a real clinician:*

6. **No exercise mission without a signed limit record.** A limit record holds: who set it (named clinician or rehab team), source (stress test, CPET, 6-minute walk, or clinician judgement), date, and review-by date. If the record is missing, expired, or self-entered, the app shows only non-exertional content (education, medication-reminder text from a clinician-approved library, sleep, salt). This applies to the free week too. "Entered or scanned from discharge note" is only a way to *capture* a record, and a clinician must confirm it before missions start.
7. **Eligibility gate at sign-up.** Block exercise missions and refer to a clinician when: risk class is unknown, the patient reports an ICD, LVEF below the clinician's cut-off, unstable or new symptoms, or surgery inside the clinician's restriction window. Only guideline low-risk patients (clinician-confirmed) get app-only missions in v1. Heart failure and high-risk hypertension are out of v1 scope until a clinician defines their rules.
8. **Symptoms never go through the LLM first.** Every mission card has a symptom tap (fixed choices) before and after exercise, and every screen has an "I feel unwell" control. Any free text in chat or check-ins passes a deterministic Thai and English screen first; if it matches a symptom phrase or is unclear, the app shows the stop-and-call message and logs the event. The phrase list is written with a Thai-speaking clinician. Confirm 1669 as the patient-facing number.
9. **No medication advice.** The agent never advises on starting, stopping, or changing a drug or dose, and never comments on side effects beyond "tell your doctor or pharmacist". Medication reminders use fixed clinician-approved text. A missed-dose or "I stopped my medicine" message is routed to a clinician flag, not answered by the LLM.
10. **Safe default when anything is missing.** No watch data, no network, an LLM outage, or an implausible reading means: show the last approved mission or a rest/light-activity mission, and never increase intensity. No new data is ever invented.
11. **Named owner and consent.** v1 needs a named accountable clinician who owns the limit library, and a written consent flow (what data, who sees it, whether an insurer ever sees it, where the LLM processes it) reviewed by a lawyer under PDPA before any real patient. Insurer access to patient-level data is **off** by default.

## 6. Architecture sketch *(guess, builder's call within these lines)*

```
Patient phone app (React Native / Expo, guess)
  ├─ Onboarding: demographics + clinician limits (entered or scanned from discharge note)
  ├─ Chat screen: goal declaration with AI agent
  ├─ Today screen: 1–2 mission cards, one-tap done
  └─ Health data bridge: Apple HealthKit / Android Health Connect
          │   (covers most watches indirectly; Garmin/Huawei via their own APIs later)
          ▼
Backend
  ├─ Mission engine (rules): clinician limits + recent data → candidate missions
  ├─ AI agent (Claude) with MCP tools:
  │     get_recent_activity(days), get_heart_rate_summary(days),
  │     get_patient_limits(), propose_week_plan(missions),
  │     schedule_notification(mission, time), log_checkin(text)
  ├─ Red-flag handler (deterministic, no LLM)
  └─ Notification scheduler → phone push → mirrored to watch
```

Key split: **the rules engine owns safety and the agent owns conversation.** The agent can only pick from missions that the rules engine marks as allowed.

## 7. Example week *(illustrative)*

- **Mon:** Agent check-in: "Last week you did 4/7 walks. Want to keep 10 min or try 11?" The patient picks one option. *(An increase never exceeds the clinician's weekly progression cap, and never raises intensity and duration together.)*
- **Daily push, time chosen by the patient (default early morning or evening, not midday heat):** "10-min easy walk, with a 3-min warm-up and cool-down. You should still be able to talk." Before starting: symptom tap. After: symptom tap, then Done. The watch HR confirms the walk and flags any reading above the clinician's ceiling.
- **Daily push at 20:00:** "Evening meds 💊." The patient taps Done.
- **Sun:** Summary of the week as one sentence. No charts unless the patient asks. No guilt wording after missed days; missing days gets an easier mission, not a streak warning, because streaks can push people to exercise through symptoms.

## 8. Open questions (team must answer — most important first)

0. **Does every user need a CPET result to get a plan?** If not, where do the safe limits come from for users without one (e.g. B2C freemium)? This is now the biggest open question. **Research answer (see [research/README.md](../../../research/README.md)):** guidelines accept stress test, 6-minute walk, % HR reserve, resting HR + 20–30 bpm, Borg RPE 11–14, talk test. The app needs a risk-class gate (low risk: app-only; moderate: a few supervised sessions first; high: not suitable). Clinician still signs off.
1. ~~Which diagnosis group first?~~ Draft 1 script leads with post-MI. Confirm that the v1 mission library is post-MI only.
2. **Where do the clinician limits come from in the demo?** Options are manual entry, a mock discharge note, or a clinician web portal.
3. **What does the hackathon require us to deliver?** A working demo, a clickable prototype, or a pitch deck? What is the deadline?
4. **Which watch do we demo on?** Apple Watch via HealthKit is the easiest for a demo. Do we have one?
5. **What does "MCP to the smartwatch app" mean for us?** (a) Our agent reads watch data through MCP tools, or (b) the agent talks into an existing watch app such as Samsung Health or Garmin. This draft assumes (a).
6. **Mission scope beyond exercise.** Do we include meds, diet (salt), sleep, BP self-measurement, and smoking? (Rule 9 limits medication to fixed reminder text.)
7. **Language.** Thai first, English, or both?
8. **Escalation to the clinician.** Does the clinician see anything in v1, or is the app patient-only?

## 8b. Open items raised by the panel (2026-10-17)

- Which clinician is the named owner of the limit library (rule 11)?
- What exactly does the free week contain for a user with no signed limit record: education only, or a clinician-booked first session (rule 6)?
- Real rehab physician to reconcile guideline numbers: see [research/guidelines/RECONCILE-for-clinician.md](../../../research/guidelines/RECONCILE-for-clinician.md).
- Caregiver role (LINE summary for family), no-watch mode, and large-text accessibility for 55–75-year-olds.
- Peer community: moderation and an intensity guard for shared goals; consider caregiver summaries first.
- Paywall timing: day 7 is early for habit formation. Test a longer free period.

## 9. Left to the builder

- Stack choice inside the sketch above.
- Notification copy style, provided it stays short and action-first.
- Mission library format: a JSON list of mission templates with parameters and safety bounds is suggested.
