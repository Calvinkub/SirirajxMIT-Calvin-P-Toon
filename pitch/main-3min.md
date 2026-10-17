# Main pitch: 3 minutes

**Heartstep (CVD Mission Coach)** · team Calvin, P and Toon · MIT GrandHack 2026 · InterSystems challenge, "Best Use of GenAI or FHIR using InterSystems technology"

Pace: about 140 spoken words per minute. Word counts cover the spoken lines only, not the stage directions in [brackets].

| Minute | Slides | Job | Spoken words |
|---|---|---|---|
| 0:00–1:00 | 1–2 | Pain and problem | 133 |
| 1:00–2:00 | 3, live demo, 4 | Solution, live demo, measured results | 148 |
| 2:00–3:00 | 5–6 | Business, why now, the ask | 147 |
| **Total** | | | **428** |

Judging criteria to hit: Innovation · Real-world impact · Use of InterSystems technology · Technical coherence. Each slide below names the criterion it serves.

---

## Minute 1: pain and problem (0:00–1:00)

### Slide 1 · 0:00–0:20 · "After a heart attack, the plan stops at the clinic door"

Criterion: real-world impact.

**On screen.** A photo-style illustration of a 58-year-old Thai man on his front step, smartwatch on his wrist. One line of text: "Exercise, but gently." Small corner label: "Somchai is a synthetic persona."

**Spoken script (44 words)**

> Meet Somchai. He is fifty-eight. He used to play football every week. Now he has high blood pressure, and his doctor says: exercise, but gently. Then he goes home. His watch is full of data. But nobody tells him what to do tomorrow morning.

**Speaker:** [NAME 1]

---

### Slide 2 · 0:20–1:00 · "Doctors say 'exercise'. Almost nobody gets the plan in writing."

Criterion: real-world impact (a clear problem in healthcare).

**On screen.** Three large numbers, each with its source in small type underneath:

- **93% → 15%**: Italian GPs who regularly prescribe physical activity, against those who give it in writing. *(Italian GP survey, cited in Komici et al., Front. Sports Act. Living 2026, PMC12990137.)*
- **12.5%**: patients attending outpatient cardiac rehab after bypass surgery. **83%** said nobody told them about it. *(Single-site Thai study, PMC11456183.)*
- **About 80,000** Thai deaths a year from cardiovascular disease. *(GrandHack track brief.)*

Bottom strip: "A chatbot does not know your doctor's limits."

**Spoken script (89 words)**

> Somchai is not rare. Cardiovascular disease causes about eighty thousand deaths a year in Thailand.
>
> Doctors do recommend exercise. In one survey of Italian GPs, ninety-three percent prescribed physical activity. Only fifteen percent wrote it down.
>
> Cardiac rehab should fill that gap. But in one Thai hospital, only twelve point five percent of bypass patients attended. Eighty-three percent said nobody had told them about it.
>
> So the advice exists. The daily plan does not. And a general chatbot cannot safely make one. It does not know the doctor's limits.

**Speaker:** [NAME 1]

**Do not say:** "80% of doctors", "a 5-minute consultation", "88% are readmitted". These are unsourced or misread (see `research/pitch-claims-check.md` and `evaluation/reviews/2026-10-17-document/SYNTHESIS.md`, R3 and R13).

---

## Minute 2: solution and live demo (1:00–2:00)

### Slide 3 · 1:00–1:13 · "The clinician sets the limits. The agent plans inside them. IRIS holds the truth."

Criteria: use of InterSystems technology, technical coherence.

**On screen.** The architecture diagram from `docs/pitch/faq-appendix/slides/architecture.html`, simplified to one row:

`Smartwatch → InterSystems IRIS for Health [FHIR R4 Server · FHIR SQL Builder · Vector Search] ⇄ Agent harness (small open models) ⇄ Rules engine` with a "Clinician signs limits" arrow into IRIS.

A red bar under the rules engine: "Red flags: rules only. No model ever sees them."

**Spoken script (33 words)**

> Heartstep is an agentic coach. A clinician signs the limits. They live as FHIR resources in InterSystems IRIS for Health, next to the watch data. The agent works only through those records. Watch.

**Speaker:** [NAME 2]

---

### Live demo · 1:13–1:42 · `demo/agent-flow-demo.html`

Criteria: innovation, use of InterSystems technology, technical coherence.

**On screen.** The demo page, full screen. Left: the patient's phone chat. Right: "What the AI is doing", a trace that lights up step by step. Header label on the page: "Scripted demo · synthetic patient, places and statistics · not medical advice". Leave it visible.

**Before going on stage (driver: [NAME 3])**

1. Open `demo/agent-flow-demo.html` in a browser, zoom so both panels fit.
2. The page auto-runs the football-to-golf message on load. Leave it in the default **Pitch flow** view (4 trace steps). Use **Full trace** only if a judge asks to see the calls (it shows the `GET /fhir/r4/CarePlan…`, `vector_search(…)`, `knn(…)` and `create Tasks + Provenance` lines).
3. Check that the four preset buttons sit under the chat.

**Click-by-click beats**

| Time | Driver clicks | Trace on the right shows | Speaker says |
|---|---|---|---|
| 1:13 | Preset 1: "I usually played football, but now I have hypertension…" | Chat clears, message appears | "Somchai tells the coach his goal." |
| 1:16 | Nothing (the trace animates, about 3 s) | **Read my limits and guideline** (FHIR): signed limit, about 5.9 METs, heart rate under 120 · **Filter 100 activities**: funnel 100 → 67, "Not allowed for now: Football, casual game" · **Match to what you enjoy** (KNN): bars for golf and walking football · **Ask you, then save the plan** | Lines 2–4 below |
| 1:29 | Chip **"Golf, walking with a pull cart"**, then **"Start gently: 2 sessions"** | Week plan appears in chat: "heart rate under 120 · no breath-holding" | Line 5 |
| 1:36 | Preset 4: "แน่นหน้าอกตอนเดิน" ("chest tightness when walking") | One red step: **Safety screen: warning symptom found** (rules). Chat: "Please stop now and rest… call 1669." | Line 6 |

**Spoken script (70 words)**

> Somchai tells the coach his goal.
>
> The agent reads his signed limits from FHIR, and the hypertension guideline through IRIS Vector Search.
>
> Rules cut a hundred activities to sixty-seven. Football is out. Too intense.
>
> A nearest-neighbour match finds what is closest to football and golf.
>
> It asks him. He picks golf. The week is saved as FHIR Tasks, with Provenance.
>
> He types "chest tightness". Rules stop it. No model sees it.

**Speaker:** [NAME 2] · **Driver:** [NAME 3]

**Honesty note for the speaker.** The page is a scripted, in-browser demo on synthetic data. The trace shows the FHIR and Vector Search calls the build makes; it is not calling a live IRIS server on stage. [CONFIRM before the event: whether `synthetic/load_to_iris.py` has loaded the 8 synthetic bundles into the kit's IRIS FHIR server. If yes, a judge can be shown the resources in IRIS during Q&A. If no, say "designed for" rather than "running on".] The "similar users" numbers (Full trace only) are a synthetic cohort, n = 52.

**If the demo fails:** go straight to Slide 4 and say, "The demo page is in our repo; we will show it in Q&A." Keep a screen recording of the run as backup.

---

### Slide 4 · 1:42–2:00 · "Safety by construction is also faster. We measured it."

Criteria: technical coherence, innovation.

**On screen.** One small table, with a big "SYNTHETIC DATA" label:

| Tool router, Qwen3-1.7B, Colab T4 (36 synthetic test messages) | Tool accuracy | Median latency | Red flags missed |
|---|---|---|---|
| Model writes the tool call | 42% | 1,272 ms | 4 of 4 |
| Rules first, then one forward pass | **78%** | **71 ms** | **0 of 4** |

Under it, one line: "Blind synthetic test set (270 messages): 95% accurate when it answers, 26 of 30 red flags caught. Not good enough yet. v3: anything near a red flag goes to stop."

Footer: "Source: `experiments/RESULTS_tool_router_demo.md`. Synthetic messages only. Not evidence of accuracy on real patients."

**Spoken script (45 words)**

> We measured our router on synthetic messages. Rules first, then one forward pass: seventy-eight percent correct, in seventy-one milliseconds. A model writing the call: forty-two percent, over a second. A blind test still missed four of thirty red flags. So version three fails toward stop.

**Speaker:** [NAME 2]

---

## Minute 3: business (2:00–3:00)

### Slide 5 · 2:00–2:33 · "Insurers already pay when the heart attack happens. We help that money buy recovery."

Criterion: real-world impact (realistic path to a business).

**On screen.** Two columns.

- **B2B2C, insurers (lead channel).** Critical-illness cover pays out after a heart attack. Heartstep is a recovery benefit for those policyholders. Price: **[PRICE PER MEMBER PER MONTH, THB, to set after insurer interviews]**. Insurer sees no patient-level data unless the patient consents; off by default.
- **B2C, freemium.** Free starter week (education, no exercise missions until a clinician signs limits). Premium: 1, 3 or 12 months, **[499 THB a month, a hypothesis to test]**.

Bottom line, small type: "AI inference estimate: about US$0.78 per patient-month at Claude Sonnet 5.5 list prices. Token budget not yet measured. (Appendix A08.)"

**Spoken script (81 words)**

> Who pays? First, insurers. Critical-illness cover pays out after a heart attack. So insurers care what happens next. We sell Heartstep to them as a recovery benefit for those policyholders.
>
> Second, patients directly. A free starter week, then Premium. We will test about four hundred ninety-nine baht a month.
>
> Exercise missions only start after a clinician signs the limits. Insurers see no patient data unless the patient agrees.
>
> And AI cost is small: our estimate is under one dollar per patient-month.

**Speaker:** [NAME 3]

---

### Slide 6 · 2:33–3:00 · "Why now, and what we need from you"

Criteria: innovation, real-world impact.

**On screen.** Left, "Why now" (3 bullets):
- Open speech models now list Thai (Qwen3-ASR, Apache-2.0).
- One InterSystems engine holds FHIR, SQL and Vector Search, so the agent has one source of truth.
- Health in ChatGPT launched for US users only (OpenAI, July 2026).

Right, "The ask" (3 bullets):
- A Siriraj rehab clinician to own and sign the limit library.
- One insurer for a pilot with pre-agreed adherence and safety outcomes.
- InterSystems mentorship to run IRIS for Health for a Thai pilot.

Closing line, large: "The doctor sets the limits. Heartstep turns them into one safe step a day."

**Spoken script (66 words)**

> Why now? Open speech models now understand Thai. And InterSystems IRIS gives us FHIR, SQL and vector search in one engine.
>
> Our ask: a Siriraj rehab clinician to sign our limit library. One insurer for a pilot, with outcomes agreed up front. And InterSystems help to run IRIS for a Thai pilot.
>
> The doctor sets the limits. Heartstep turns them into one safe step a day.

**Speaker:** [NAME 3]

---

## Every number on these slides, and where it comes from

| Number | Where it is in the repo | Label on slide |
|---|---|---|
| About 80,000 Thai CVD deaths a year | `track.txt` (GrandHack track brief) | "GrandHack track brief" |
| 93% prescribe, 15% in writing (Italian GPs) | `research/pitch-claims-check.md` (PMC12990137). Primary text checked on 2026-10-17 via the Europe PMC full text of PMC12990137 (the review quotes the Italian GP survey: 93% prescribe, 15% in writing); the survey itself (ref 13) is not opened | Source on slide |
| 12.5% attend outpatient CR after CABG; 83% never told | `docs/pitch-script-draft2-proposed.md`, `research/README.md` (PMC11456183) | "Single-site Thai study" |
| 100 activities → 67 allowed | `demo/agent-flow-demo.html` (activity list and filter `met <= 5.9`, no contact, breath-holding or bursts) | Demo is labelled synthetic |
| 78% vs 42%, 71 ms vs 1,272 ms, 0 vs 4 of 4 red flags missed | `experiments/RESULTS_tool_router_demo.md`, Colab T4 table, Qwen3-1.7B | "Synthetic" |
| 95% when it answers; 26 of 30 red flags caught | Same file, "Router v2 on a blind test set", Qwen3-1.7B: 95.3%, coverage 78.9% | "Synthetic" |
| About US$0.78 per patient-month | `docs/pitch/faq-appendix/slides/cost.html` (list prices, unmeasured token budget) | "Estimate" |
| 499 THB | `docs/pitch-script-draft1.md`; unvalidated (`research/pitch-claims-check.md`) | "Hypothesis to test" |
| Health in ChatGPT, US only, July 2026 | `docs/pitch/faq-appendix/slides/chatbot.html` | Source on slide |

## Words we never use on stage

"proven", "optimal", "exact plan", "clinically validated", "exercise prescription" (for what the AI does), "diagnose", "detect", "reduces readmissions" (for our app). The AI never sets or raises a limit; a clinician does. Red flags are rules only.
