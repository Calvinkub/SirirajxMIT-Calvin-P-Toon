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

- **Mon:** Agent check-in: "Last week you did 4/7 walks. Want to keep 10 min or try 12?" The patient picks one option.
- **Daily push at 12:30:** "10-min easy walk. You should still be able to talk." The patient taps Done, and the watch HR confirms the walk.
- **Daily push at 20:00:** "Evening meds 💊." The patient taps Done.
- **Sun:** Summary of the week as one sentence plus a streak. No charts unless the patient asks for them.

## 8. Open questions (team must answer — most important first)

1. **Who is the user, exactly?** Which diagnosis group do we start with: post-MI, heart failure, or hypertension? This choice changes the mission library and the safety limits.
2. **Where do the clinician limits come from in the demo?** Options are manual entry, a mock discharge note, or a clinician web portal.
3. **What does the hackathon require us to deliver?** A working demo, a clickable prototype, or a pitch deck? What is the deadline?
4. **Which watch do we demo on?** Apple Watch via HealthKit is the easiest for a demo. Do we have one?
5. **What does "MCP to the smartwatch app" mean for us?** (a) Our agent reads watch data through MCP tools, or (b) the agent talks into an existing watch app such as Samsung Health or Garmin. This draft assumes (a).
6. **Mission scope beyond exercise.** Do we include meds, diet (salt), sleep, BP self-measurement, and smoking?
7. **Language.** Thai first, English, or both?
8. **Escalation to the clinician.** Does the clinician see anything in v1, or is the app patient-only?

## 9. Left to the builder

- Stack choice inside the sketch above.
- Notification copy style, provided it stays short and action-first.
- Mission library format: a JSON list of mission templates with parameters and safety bounds is suggested.
