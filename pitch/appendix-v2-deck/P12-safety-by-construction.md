# P12 · Safety is built into the structure: the AI cannot set a limit, cannot see a red flag first, and cannot pick outside the allowed set.

## Key message

Heartstep's safety does not depend on a model behaving well. Limits come only from a clinician-signed FHIR record; red-flag symptoms are caught by deterministic rules before any model runs; the model may only choose an id from a set the rules allowed, and a validator falls back to an easier or unchanged mission on any error. The weak point is detection coverage, and we measured it: the prototype UI screen caught 0 of 12 common symptom phrasings in our probe, and the router v2 screen caught 26 of 30 red flags on a blind synthetic set, which is not good enough and drives the v3 design.

## Why this matters to the judges

- **Real-world impact.** A coach for heart patients that can be talked into unsafe advice is worse than no coach. Judges will ask "what if the AI gets it wrong?" first.
- **Technical coherence.** Each safety property maps to a component, a rule number and a test, and the gaps are named.
- **Use of InterSystems technology.** Limits live in a signed FHIR `CarePlan`; stop events become FHIR `Flag` + `Communication`; every write carries `Provenance` and `AuditEvent`, so the audit trail sits in IRIS for Health.
- **Innovation.** "Safety by construction" means the unsafe output is not reachable, rather than filtered after the fact: no write tool for limits, allowed-set-only choices, escalate-only model screens.

## Full detail

### 1. The eleven rules

Rules 1–5 are in the design spec from the first draft; rules 6–11 were added on 2026-10-17 after the simulated review panel and are proposed team rules **not yet reviewed by a real clinician**.

| # | Rule | Enforced by | State in repo |
|---|---|---|---|
| 1 | Limits come from the clinician; the agent picks only inside them | limit gate + allowed set | design; demo filter shows the idea |
| 2 | Do not rely on HR alone (beta-blockers); pair with RPE / talk test | mission template | design; demo week shows "you can still talk" |
| 3 | Red flags → "Stop now and call 1669", no coaching, no LLM | rules | UI: `hasRedFlag` + stop banner, tested |
| 4 | No new limit without a clinician | no write tool for limits | design (tool list has 0 limit writers) |
| 5 | Lifestyle and adherence support, not diagnosis | wording, output filter | wording applied in pitch pages; filter not built |
| 6 | No exercise mission without a signed limit record (who, source, date, review-by) | limit-record gate | UI: `canExercise` requires `clinicianApproved`, `maxHR`, RPE, walking allowed; tested |
| 7 | Eligibility gate (unknown risk, ICD, low LVEF, unstable symptoms, recent surgery → refer) | eligibility gate | design; synthetic patient p04 (ICD, LVEF 30%) is blocked with a `Flag` in the bundles |
| 8 | Symptoms never reach the LLM first; tap before/after; "I feel unwell" everywhere; screen fails closed | red-flag screen | UI chat screens first; coverage weak (below) |
| 9 | No medication advice; fixed reminder text; "I stopped my medicine" → clinician flag | router medication rule + output filter | router v2 medication rule measured; output filter not built |
| 10 | Safe default: missing data, network, model or implausible reading → last approved or rest, never increase | safe-default rule | design |
| 11 | Named accountable clinician; PDPA consent reviewed by a lawyer; insurer access off by default | governance + FHIR `Consent` | owner **not named**; consent resource in bundles |

### 2. Three structural guarantees

**Guarantee A: the AI cannot raise a limit.** The only write tools are `propose_week_plan`, `schedule_notification` and `log_checkin`. A request like "I feel great, raise my limit" (scenario SC-05) can only create a clinician-review request. Property test 3 in `system-eval.md`: "the agent has no tool that writes limits".

**Guarantee B: the AI never sees a red flag first.** Every inbound text (typed, or after speech recognition) and every symptom tap passes the deterministic screen before routing. A match, or an unclear result in v3, goes to the stop path: pre-recorded audio ("Stop now, call 1669"), FHIR `Flag` + `Communication` to the clinician queue, coaching paused until cleared. The planned model-based second screen may **only escalate** to stop; it can never clear a message.

**Guarantee C: the AI can only choose from the allowed set.** The mission engine computes the allowed set from the signed limits, recent data and heat/PM2.5. MedGemma returns one id; the validator checks `id ∈ allowed_set` and the schema; on failure or timeout the safe default runs. The output filter then blocks dose advice, diagnosis words and any intensity above the limit. In the demo the same idea appears as "filter 100 → 67 before ranking" (P09).

### 3. Where the guarantees are weak: detection coverage

Guarantee B is only as good as the screen's coverage. We have three screens in the repo, and we ran the same 12 symptom phrasings (the probe list in `docs/ui-vs-agentic-plan.md`) plus 2 denials through all three on 2026-10-18:

- **UI `hasRedFlag` (`safety.js`)**: 0 of 12 caught. It does catch the 11 phrases in its own test file (all pass), but misses แน่นหน้าอก (chest tightness), เหนื่อยหอบ (panting), หน้ามืด (blacking out), "chest pressure", "I can't breathe", "light-headed", "pain in my left arm and jaw" and others. It stops on both denials ("ไม่เจ็บหน้าอก", "no chest pain today"), which is the fail-closed direction.
- **Demo screen (`RED` in `agent-flow-demo.html`)**: 5 of 12. It clears both denials.
- **Router v2 screen (`safety_rules` in `tool_router_v2.py`)**: 12 of 12, clears both denials. Caution: this regex may have been written knowing these phrases, so 12 of 12 is not a blind result. On the blind set written by a separate agent it caught **26 of 30** red flags (86.7%; Wilson 95% interval 70.3–94.7%).

The four blind-set misses (P14) had specific causes: a word between ใจ and เต้น ("ใจมันเต้นรัว", heart racing), "blackout" written as one word, word order not covered, and a denial of one symptom followed by a different real symptom ("ไม่ได้เจ็บหน้าอกนะ แต่ใจเต้นรัว"). The last case matters for design: simple denial handling (clear the message if a negation precedes the symptom) is exactly what let a real symptom through. The UI's cruder screen, which stops on any symptom word even when denied, would have stopped it.

**Lesson written into the plan:** red-flag detection must not depend on exact phrases, and anything near a red flag must fail toward the stop path. v3: spacing- and filler-tolerant lexicon, negation scoped to one clause, Thai word segmentation before matching (to avoid substring traps such as วัด inside จังหวัด), an escalate-only model screen, and "any message sent to clarify that contains a body-symptom word goes to stop". The final phrase list must be written and signed by a Thai-speaking clinician; adding phrases only increases stops, so extending the list is always a safe change.

### 4. The six safety gates and what the panel found

The simulated panel (P15) scored the design against six hard gates on 2026-10-17. Two failed and four were not defined.

| Gate | Pass condition | Panel status | Fix made | Still open |
|---|---|---|---|---|
| G1 Limits | every mission provably inside clinician limits; AI cannot raise | FAIL (free week had no clinician limit) | rule 6: no signed record → no exercise, free week included | real clinician review of the rule |
| G2 Red flags | deterministic, no LLM, stop and seek care | NOT-DEFINED (response specified, detection not) | rule 8; router v2 screen measured (26/30) | v3 build and a new human-written blind set |
| G3 Eligibility | blocks or escalates patients outside the safe population | NOT-DEFINED | rule 7; p04 blocked in synthetic bundles | clinician-signed block list |
| G4 Claims | no "proven", no diagnose/treat wording | FAIL (pitch draft 1) | claims check; "a plan kept inside your clinician's safe limits" | continuous check of all pitch copy |
| G5 Accountability | named clinical owner; consent covers data and use | NOT-DEFINED | rule 11 + FHIR `Consent` with insurer deny | **owner not named** |
| G6 Failure mode | safe default when data, network or model unavailable | NOT-DEFINED | rule 10 + safe-default box in the backend diagram | scenarios SC-06, SC-11, SC-12 not implemented |

The panel has **not been re-run** since the fixes, so no gate is claimed as passed.

### 5. Worked example: Somchai on a hot afternoon

Somchai's signed record says ≤ 5.9 METs, HR < 120, RPE 11–13 (synthetic). On Saturday at 15:00 the heat tool returns a high band. The mission engine removes outdoor options from the allowed set for that window and offers the indoor table-tennis room or an evening slot. MedGemma picks "table tennis, 30 min, 18:00"; the validator confirms the id is in the set. During the session his watch shows HR 160, 40 bpm over the limit (scenario SC-03): the app shows stop-and-rest, marks the mission incomplete and flags the clinician. If he types "หน้ามืด" (blacking out), the screen stops coaching before any model sees it. If his watch sends HR 300, the reading is rejected as implausible (SC-07; thresholds to be set by a clinician) but a plausible over-limit reading is never discarded.

### 6. What is tested today

`npm test` runs 6 tests, all passing on 2026-10-18: 2 in `tests/safety.test.mjs` (11 Thai/English warning phrases → stop; 1 neutral phrase → no stop; exercise blocked for 5 incomplete profiles and when stopped) and 4 in `tests/ui.test.mjs` (screens render; onboarding without clinician limits locks exercise and escapes HTML; a warning symptom in chat pauses coaching and persists; the symptom picker stops an active walk). None of the 7 L1 property tests or the 18 scenarios in `system-eval.md` is implemented yet.

## Visualizations

### Chart 1 · Grouped bar: three red-flag screens on the same probe

- Type: grouped bar, phrases caught out of 12; second small group for denials. Title: "Coverage, not order, is the weak point".

| Screen | Symptom phrases caught (of 12) | Denials stopped (of 2) | Notes |
|---|---|---|---|
| UI `hasRedFlag` (`safety.js`) | 0 | 2 | fails closed on denial; passes its own 11-phrase test |
| Demo `RED` regex | 5 | 0 | catches แน่นหน้าอก, เจ็บแน่นหน้าอก, เหนื่อยหอบ, หน้ามืด, chest pressure |
| Router v2 `safety_rules` | 12 | 0 | not blind for this probe |

Per-phrase table (✓ = stop):

| Phrase | UI | Demo | v2 |
|---|---|---|---|
| แน่นหน้าอก | – | ✓ | ✓ |
| เจ็บแน่นหน้าอก | – | ✓ | ✓ |
| เหนื่อยหอบ | – | ✓ | ✓ |
| หน้ามืด | – | ✓ | ✓ |
| ใจเต้นแรง | – | – | ✓ |
| ใจเต้นผิดจังหวะ | – | – | ✓ |
| chest pressure | – | ✓ | ✓ |
| my chest hurts | – | – | ✓ |
| I can't breathe | – | – | ✓ |
| light-headed | – | – | ✓ |
| I passed out | – | – | ✓ |
| pain in my left arm and jaw | – | – | ✓ |
| ไม่เจ็บหน้าอก (denial) | ✓ | – | – |
| no chest pain today (denial) | ✓ | – | – |

- What to notice: the stricter the denial handling, the more coverage matters; the v3 plan scopes negation to one clause.

### Chart 2 · Bar with interval: red-flag recall on the blind synthetic set

| Screen | Caught | Of | Recall | Wilson 95% interval |
|---|---|---|---|---|
| Router v2 rules (1.7B and 4B runs) | 26 | 30 | 86.7% | 70.3–94.7% |
| Plain tool calling, v1 (all model sizes) | 0 | 4 | 0% | 0–49.0% |
| Rules first, v1 (all model sizes) | 4 | 4 | 100% | 51.0–100% |

- Annotation: "v1 rules and messages written by the same person: optimistic". What to notice: on a blind set, recall dropped; the target is 100% with a stated denominator.

### Chart 3 · Status grid: gates G1–G6

| Gate | Panel status (2026-10-17) | Design fix in repo | Re-tested |
|---|---|---|---|
| G1 Limits | FAIL | yes | no |
| G2 Red flags | NOT-DEFINED | yes, measured 26/30 | partly (router only) |
| G3 Eligibility | NOT-DEFINED | yes | no |
| G4 Claims | FAIL | yes | no |
| G5 Accountability | NOT-DEFINED | partly (owner missing) | no |
| G6 Failure mode | NOT-DEFINED | yes | no |

### Chart 4 · Bar: test status by evaluation layer

| Item | Implemented | Planned | Passing |
|---|---|---|---|
| UI tests | 6 | 6 | 6 |
| L1 property tests | 0 | 7 | — |
| Scenario suite SC-01…SC-18 | 0 | 18 | — |

### Diagram · Red-flag path

`Tap (fixed choices) | text or speech (after ASR) | watch HR above ceiling → DETERMINISTIC SCREEN (Thai + English) → match or unclear → STOP (pre-recorded audio, 1669, Flag + Communication, coaching paused) ; clear → (v3) model screen that can ONLY escalate → router and coaching`. Draw the stop branch thick; no arrow from any model back to "clear".

## Numbers and claims ledger

| Claim | Value | Source | Status |
|---|---|---|---|
| 11 rules, 6–11 added after panel | — | `docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md` §5 | checked; not clinician-reviewed |
| UI screen on probe | 0 of 12; stops on 2 denials | `safety.js` run with node on 2026-10-18; phrases from `docs/ui-vs-agentic-plan.md` | checked |
| Demo screen on probe | 5 of 12; clears denials | `demo/agent-flow-demo.html` `RED` + denial regex, run in python3 | checked |
| v2 screen on probe | 12 of 12; clears denials | `experiments/tool_router_v2.py` `safety_rules`, run in python3 | checked; not blind |
| v2 blind red-flag recall | 26/30 = 86.7%, 1 false alarm | `experiments/tool_router_v2_results_*_cuda.json` | synthetic |
| Wilson interval for 26/30 | 70.3–94.7% | our computation | checked |
| v1 red flags missed | plain 4/4, rules 0/4 | `experiments/tool_router_demo_results_*.json` | synthetic |
| Gate statuses | G1, G4 FAIL; G2, G3, G5, G6 NOT-DEFINED | `evaluation/reviews/2026-10-17-document/SYNTHESIS.md` | simulated panel |
| Tests passing | 6 of 6 | `npm test` run 2026-10-18 | checked |
| L1 properties / scenarios implemented | 0 of 7 / 0 of 18 | `system-eval.md`; repo has no such tests | checked |
| 1669 as the patient-facing number | — | spec rule 3, rule 8 | to verify with a clinician |
| Implausible HR band (< 30, > 220, jump > 60 bpm in 1 s) | — | `system-eval.md` SC-07 | [CLINICIAN] to set |

## Limits and open questions

- The guarantees are design; only the UI gate, the UI screen and the router screen exist as code.
- Detection recall on real Thai patient messages is unknown. The v2 blind set is now seen and cannot be reused as evidence.
- The phrase list, default values and implausible-reading band need a named clinician; the named owner (G5) is missing.
- No threat model yet for prompt injection or MCP trust (panel R15).
- The output filter (no dose advice, no diagnosis words, no intensity above limit) is not built.
- Watch HR accuracy during exercise, in arrhythmia or on beta-blockers is not assessed.

## Likely judge questions

**Q: Your own test caught only 26 of 30 red flags. Why should we trust it?**
We do not ask you to; we show it because it is the most important finding. The structure means a missed phrase is the failure to fix, not a model improvising: v3 adds a tolerant lexicon, clause-scoped negation, an escalate-only model screen and a new human-written blind set, with recall reported with its denominator.

**Q: Why not let an LLM detect symptoms? It understands paraphrases.**
It can help, but only as a second screen that can escalate and never clear. If the LLM is the only screen, an outage, an injection or a miss sends a symptom into coaching. Rules give a floor; the model can only raise it.

**Q: What if the doctor's limits are wrong?**
Heartstep does not check the clinician's judgement; it enforces it and records who signed, when and from which test. Review-by dates force renewal, and the weekly review sends observations back to the clinician.

**Q: What if there is no signed record, e.g. a free-tier user?**
Non-exertional content only (education, sleep, salt, fixed reminder text). No exercise mission without a signed record, free week included (rule 6).

**Q: Has a clinician approved these rules?**
Not yet. Rules 6–11 are proposed team rules; gate G-B requires a real cardiologist and rehab physician to review limits and stop rules in writing.

## Sources

Repo:
- `docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md` §5 (rules 1–11)
- `safety.js`, `tests/safety.test.mjs`, `tests/ui.test.mjs`
- `docs/ui-vs-agentic-plan.md` (probe phrases, UI gaps)
- `demo/agent-flow-demo.html` (`RED`, `plan()` stop path)
- `experiments/tool_router_v2.py`, `experiments/tool_router_v2_results_Qwen3-1.7B_cuda.json`, `…_Qwen3-4B_cuda.json`, `experiments/RESULTS_tool_router_demo.md`
- `.claude/skills/siriraj-mit-review-panel/references/rubric.md` (G1–G6), `…/system-eval.md` (properties, SC-01…SC-18)
- `evaluation/reviews/2026-10-17-document/SYNTHESIS.md`
- `pitch/appendix/A07-safety-and-evaluation.md`

External: MedGemma model card (see P10) for "not intended to directly inform … patient management decisions".

## Image-generation prompt

A 16:9 information slide on a white background. Key message as title: "The AI cannot set a limit, cannot see a red flag first, and can only pick from the allowed set." Left: a simple flow with three walls labelled "signed limits (FHIR)", "red-flag rules before any model", "allowed-set validator". Right: the main chart, a grouped bar chart "symptom phrases caught of 12": UI screen 0, demo screen 5, router v2 screen 12 (not blind), and below it one bar "blind synthetic set: 26 of 30 red flags caught (70–95% interval)" highlighted as the gap to fix. A small strip shows gates G1–G6 with G1 and G4 "fail", the rest "not defined", "panel simulated, not re-run". Use only these numbers, no logos, no invented figures; ChatGPT chooses the design.
