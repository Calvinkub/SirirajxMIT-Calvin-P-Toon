# Initial UI: document review and implementation

Reviewed all four original repository documents on 17 October 2026: `README.md`, `HANDOFF.md`, the CVD Mission Coach design draft, and `track.txt`.

## Product interpretation

The central problem is the gap between a cardiac diagnosis and knowing what to do today. The initial UI makes the next action prominent, with two simple mission cards instead of a health analytics dashboard. The lead sample patient is recovering after MI, consistent with the pitch additions in §2b. “Heartstep” is a provisional UI name, not an agreed brand.

The broader cardiovascular innovation brief in `track.txt` provides context, but does not expand v1 into stroke diagnosis, risk prediction, or emergency detection. The design document's narrower recovery and adherence scope governs this prototype.

## Screen mapping

| Screen | Document requirement | Prototype behavior |
| --- | --- | --- |
| Today | One or two tiny daily missions | Easy walking and prescribed medication; completion, undo, browser-local persistence |
| My plan | Personalized schedule and weekly check-in | Illustrative seven-day plan; check-in saved without increasing limits |
| My coach | Conversational goals and support | Scripted replies and goal selection; explicitly labeled as a demo |
| Community | Shared goals from pitch draft | Sample walking group, local join/leave, no competition or health sharing |
| My profile | Demographics, goals, clinician limits | Sample profile, new-patient form, read-only safety plan, demo reset |
| Symptom dialog | Hard-coded red-flag override | Direct selection or keyword detection pauses exercise and coaching; displays the specified emergency action |

## Working assumptions

- A responsive browser prototype is the fastest reviewable first UI. It uses plain HTML, CSS, and JavaScript without dependencies. React Native / Expo remains a possible production decision.
- English is used for this initial review. Thai symptom keywords are recognized, but this is not a translated UI.
- The default patient has clearly labeled illustrative CPET-derived limits: easy walking, below 110 bpm, paired with a talk test. These numbers come from the design document's example and are not general patient advice.
- New-patient onboarding does not invent safe limits. Exercise stays unavailable without clinician approval, a positive numeric ceiling, allowed walking, and effort guidance. The prototype deliberately has no patient control to raise safety limits.
- The displayed day and weekly progress are fixed demo fixtures for 17 October 2026. This is not a live scheduler.
- Medication completion records a patient action against an existing prescription; the prototype does not recommend a drug or dose.
- Community is included because the pitch adds it. Pricing is deferred: currency and package details are not settled, and a recovery demo does not require a checkout.

## Decisions still needed

1. Decide how clinicians supply and approve limits, including the path for patients without CPET results.
2. Confirm post-MI-only mission scope and validate mission copy, red flags, effort scale, and emergency behavior with the clinical mentor.
3. Choose the demo device, HealthKit / Health Connect bridge, permissions, MCP tool contracts, and push notification delivery.
4. Confirm Thai-first versus bilingual support and accessibility requirements with intended patients.
5. Confirm hackathon deadline, required delivery format, clinician escalation, and whether medication missions are in scope.
6. Validate pitch statistics and claims before using them externally. The original spec flags unresolved citations; no unverified statistics or readmission claims are displayed here.

## Technical and clinical limits

All patient details and watch readings are fictional. Local storage is for demonstration only, not real patient data. There is no backend, authentication, AI model, clinical approval workflow, live watch connection, notification scheduler, emergency dispatch, or real community.

The deterministic symptom check is a prototype safeguard, not a clinically validated symptom classifier. It conservatively routes matching phrases to the stop path and cannot interpret all language. The original clinical safety requirements still need clinical validation before any patient use. A symptom stop persists across navigation and reload; only resetting the whole fictional demo clears it.

## Validation

Run `npm test` for clinician-limit gating, English/Thai red-flag detection, all screen renders, mission persistence, input escaping, onboarding lockout, symptom override, and demo reset. UI tests run the real application code against a small DOM harness; they do not substitute for visual browser testing. Browser automation was unavailable in this environment, so desktop/mobile appearance and physical device behavior still need manual review.
