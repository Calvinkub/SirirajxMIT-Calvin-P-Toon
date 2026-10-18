# Heartstep UI vs agentic workflow plan

Checked 2026-10-18 against the [Agentic AI Workflow Plan](https://claude.ai/artifact/TeeFMYw4faY4HCZ6rM3yyM) and design doc §5 rules 6–11. UI version: merge of PR #1 (`93a745a`). `npm test`: 6/6 pass.

## Summary

The UI already gets the core safety behaviour right: exercise stays locked without clinician limits, chat runs the red-flag check before any reply, and a stop persists. The biggest gap is the red-flag phrase list. Common Thai and English ways of describing chest symptoms are missed (see below). Second: the walk is fixed at 12:30 PM, which conflicts with the plan's "patient-chosen time, avoid midday heat" rule.

## Red-flag screen probe (`safety.js` `hasRedFlag`)

Run with `node --input-type=module -e "import {hasRedFlag} from './safety.js'; ..."`.

| Phrase | Meaning | Result | Expected |
|---|---|---|---|
| แน่นหน้าอก | chest tightness | MISS | stop |
| เจ็บแน่นหน้าอก | chest pain and tightness | MISS (regex needs เจ็บหน้าอก contiguous) | stop |
| เหนื่อยหอบ | breathless, panting | MISS | stop |
| หน้ามืด | blacking out, faint | MISS | stop |
| ใจเต้นแรง / ใจเต้นผิดจังหวะ | pounding / irregular heartbeat | MISS | stop |
| chest pressure / my chest hurts | chest symptoms | MISS | stop |
| I can't breathe | breathlessness | MISS | stop |
| light-headed / I passed out | dizziness / fainting | MISS | stop |
| pain in my left arm and jaw | radiating pain | MISS | stop |
| ไม่เจ็บหน้าอก / no chest pain today | negation | STOP | stop is acceptable (fail closed), but it will annoy patients; the plan says negation handling needs a clinician-written list |

These phrases are a starting test set only. The final list must be written and signed off by a Thai-speaking clinician. Adding phrases only increases stops, so it is a safe change to make now.

## Workflow mapping

| Plan workflow | What the UI does now | Gap | Where the agentic piece plugs in |
|---|---|---|---|
| W1 Onboarding | Name, age, diagnosis, goal form. Exercise locked until `clinicianApproved`, `maxHR`, `rpe`, walking allowed | No ICD, LVEF, beta-blocker or surgery-date questions; no discharge-note upload; no risk-class gate | Discharge-note photo → MedGemma 1.5 4B extraction → clinician confirm screen |
| W2 Daily loop | Two mission cards (walk, evening medication), done/undo, safe-limit row | Walk fixed at **12:30 PM** (midday heat); no symptom tap before and after the walk; no warm-up or cool-down text; no heat or PM2.5 context | Mission engine allowed set → MedGemma pick → Thai phrasing; environment tool for heat and PM2.5 |
| W3 Check-in / coach | Scripted replies; `hasRedFlag` runs before any reply; "raise my limit" refused | Phrase misses above; no voice; place and activity questions get no tool results | Router (Qwen3-4B) + places and community MCP; Qwen3-ASR for voice |
| Community | Static "little-walk club", join/leave, no leaderboard | No intensity tag, distance or time; not filtered by the patient's limits | `search_activities(intensity_max, …)` over the curated list |
| W4 Weekly review | Check-in modal; limits stay the same | No clinician summary or bounded progression proposal | MedGemma weekly summary → clinician queue |
| W5 Red flag | Stop banner, `tel:1669`, coaching paused, persists across reload | No caregiver alert, no clinician flag, no pre-recorded audio | Fixed audio files; clinician-queue `flag()` |

## Matches the plan

- Rule 6 (no exercise without a signed record): enforced in `canExercise` and tested.
- Rule 8 (symptoms before LLM): chat checks first; the symptom picker exists. Coverage is the issue, not the order.
- Rule 9 (no medication advice): medication card says "exactly as prescribed"; no dose wording.
- No streak guilt: weekly copy is "You're showing up. That's what matters."

## Suggested next changes (for the UI owner)

1. Extend `hasRedFlag` with the missed phrases and add them to `tests/safety.test.mjs`. Keep the clinician sign-off note.
2. Let the patient pick the walk time in onboarding; default to morning or evening, not midday.
3. Add a symptom tap before and after the walk, plus warm-up and cool-down lines on the walk card.
4. Add ICD / LVEF / beta-blocker / surgery-date fields to onboarding (as "ask your clinician" if unknown), and block exercise on unknown or high risk.
5. Tag community groups with intensity and show only those within the patient's limits.
