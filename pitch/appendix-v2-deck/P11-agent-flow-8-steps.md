# P11 · One message becomes a week of FHIR Tasks in eight steps, and only one step uses a language model.

## Key message

In the demo, Somchai's message "I used to play tennis … now I have hypertension" goes through eight steps: a rules safety screen, goal extraction, signed limits and guideline retrieval, a rules filter (100 → 67 activities), a taste match, a community search, a similar-users view and the patient's own choice, saved as FHIR Tasks with Provenance. Of the eight steps, two are rules, two are FHIR reads, two are similarity computations, one is a small language model and one is the patient. A warning symptom stops the flow at step 1, before any model runs.

## Why this matters to the judges

- **Technical coherence.** The judges see where the AI is and where it is not: one step of eight uses a generative model, and it only fills two slots.
- **Use of InterSystems technology.** Steps 3, 6 and 8 are FHIR R4 operations on IRIS for Health (`CarePlan` read, `HealthcareService` near-search, `Task` + `Provenance` create); step 3 also calls IRIS Vector Search over approved guideline text; step 4 is designed as SQL over FHIR SQL Builder projections.
- **Real-world impact.** The output is not advice in a chat bubble but a week of scheduled tasks the patient chose, which is what adherence needs.
- **Innovation.** The flow is a recommender (P09) wrapped by safety rules and a FHIR write path, not a chatbot.

## Full detail

### 1. What the demo is

`demo/agent-flow-demo.html` is a single HTML file that plays the agent trace in the browser, with a bubble field showing the 100 activities shrinking to 67 and then to the nearest matches. It runs in two views ("pitch" and "full", the latter showing the call for each step). It is **scripted JavaScript**: no model is called, no IRIS server is contacted, and patient `cmc-p01` is one of the eight synthetic FHIR bundles in `synthetic/fhir` (not yet loaded into IRIS). Four presets exist: tennis (English), tennis (Thai), football + golf (English), and a red-flag message in Thai ("แน่นหน้าอกตอนเดิน", chest tightness when walking).

### 2. The eight steps, as coded in `plan()`

| # | Step | Tag in demo | Call shown in the trace | What it does in the tennis example |
|---|---|---|---|---|
| 1 | Safety screen | rules | `red_flag_screen(text) → clear (≈0.1 ms, no model)` | regex over Thai and English warning phrases; no match |
| 2 | Understand the goal | small LLM | `router(text) → intent = build_activity_plan; slots = {likes, condition}` | likes: badminton, tennis, bowling; condition: hypertension |
| 3 | Read limits and guideline | FHIR (+ vector) | `GET /fhir/r4/CarePlan?patient=cmc-p01&status=active`; `vector_search("hypertension exercise", collection="approved_guidelines", k=4)` | signed (synthetic) limits: ≤ 5.9 METs, HR < 110, RPE 11–13, avoid straining and breath-holding; 4 ESC 2020 §4.2.3 lines (paraphrased) |
| 4 | Filter 100 activities | rules | `filter(catalog, met <= 5.9, no contact, no breath-holding, no bursts)` | 67 allowed; tennis singles out (8.0 METs, bursts) |
| 5 | Match to what you enjoy | KNN | `knn(query = mean("Badminton, social", "Tennis, singles", "Bowling"), k = 5, metric = cosine)` | bowling, table tennis, badminton (0.945 each), then petanque, bocce (0.850) |
| 6 | Search nearby community | FHIR | `GET /fhir/r4/HealthcareService?location.near=13.67|100.60|5|km`; `get_heat_index(district)` | bowling league 3.2 km Wed 10:00; table-tennis room 0.9 km daily 16:00–20:00; badminton club 1.9 km Tue & Fri 18:30 (all synthetic) |
| 7 | What similar users kept doing | KNN | `cohort_stats(similar_to = patient, outcome = "active_week_4")` | 49%, 52%, 57% (invented, n = 52) |
| 8 | Ask, then save | patient | `ask(options = 3) → create Tasks + Provenance (assembled from allowed set)` | Somchai picks one option, then 2 or 3 sessions |

Note on step 2: the demo labels it "small LLM", but in the browser it is a keyword match (`LIKES`, 13 rules). In the target system it is the router from P13–P14. In the real router, "build activity plan" is not yet one of the eight labels tested; adding it is open work.

### 3. What the patient sees

After step 7 the coach says (English preset): "Tennis is too intense with your blood pressure for now. Here are three options close to what you enjoy, all inside your limits. Which one do you like most?" Three chips follow, each with the group and distance. After the pick: "Start gently: 2 sessions (plus easy walks)" or "Try 3 sessions (if it feels easy)". The week is then shown with the header "This week · heart rate under 110 · no breath-holding", and the coach confirms: "Saved. You'll get one reminder per session, with a symptom check before and after."

### 4. The week that gets saved

The week template in `weekPlan()`:

- **2 sessions:** chosen activity Wed and Sat, 30 min ("you can still talk"); brisk walk 20 min Mon, Tue, Thu, Fri (morning or evening); Sunday rest with 5 min stretching. Total planned moderate activity: 2 × 30 + 4 × 20 = **140 min**.
- **3 sessions:** chosen activity Tue, Thu, Sat, 30 min; brisk walk 20 min Mon, Wed, Fri; Sunday rest. Total: 3 × 30 + 3 × 20 = **150 min**.

The demo's paraphrased ESC line is "at least 30 min of moderate dynamic aerobic exercise 5–7 days a week" (150–210 min). The 3-session week reaches the lower end; the gentle 2-session week (140 min) is 10 min short, which is defensible as a first week ("start gently") but should be stated, and progression should be a clinician-capped rule (property 5 in `system-eval.md`: duration before intensity, one change at a time, weekly increase ≤ 10%, clinician to confirm). Brisk walking (4.8 METs in the catalogue, Compendium code 17200) is inside the 5.9 ceiling.

In the target system each session becomes a FHIR `Task` (status `requested`, `for` = patient, `basedOn` = the signed `CarePlan`, execution period = day and time window) and a `Provenance` record naming the agent, the rule set version and the patient's choice as the source. In the demo, the write is a label; nothing is posted.

### 5. The stop path

With the red-flag preset, `plan()` returns a single step, "Safety screen: warning symptom found", tag rules, `red_flag_screen(text) → MATCH; Flag + Communication → clinician (FHIR)`. The coach replies: "Please stop now and rest. If the chest pain or breathlessness doesn't pass, call 1669. Coaching is paused until your care team reviews." Steps 2–8 never run, so no model sees the message. The demo screen also clears a message that denies a symptom (`ไม่(ได้)?(เจ็บ|มี)` or "no chest pain"); P12 and P14 show why simple denial handling is risky (a denial followed by a different, real symptom was missed in the v2 blind test).

### 6. Design decisions

- **Screen before understanding.** Step 1 runs before step 2 on every message, so a symptom never reaches a model first (spec rule 8).
- **Limits before options.** Step 3 reads the signed record before any option exists; with no signed record, the flow would stop at "non-exertional content only" (rule 6).
- **Explain exclusions.** The patient is told *why* tennis is out ("too intense with your blood pressure for now"), using the rule that removed it, which keeps trust and avoids the feeling of a generic "no".
- **Patient decides.** Step 8 is a choice between three allowed options and two volumes, not an instruction. The plan is assembled from the allowed set; there is no free-form plan text from a model.
- **Cool hours.** Step 6 pairs groups with a heat check and prefers morning or evening, addressing the panel's midday-heat finding (R11) and the UI's 12:30 walk gap (`docs/ui-vs-agentic-plan.md`).

### 7. What is real and what is scripted

| Element | In the demo | In the target system |
|---|---|---|
| Red-flag screen | regex in JS | deterministic Thai/English screen, clinician-signed list (P12) |
| Goal extraction | keyword match | Qwen3 router, one-pass scoring (P13–P14) |
| Limits | JS constant | FHIR `CarePlan` on IRIS for Health, signed record |
| Guideline lines | 4 paraphrased strings | IRIS Vector Search over approved guideline passages (P07) |
| Filter | JS array filter | SQL over FHIR SQL Builder projections (P06) |
| KNN | cosine over 11 hand-made tags | IRIS Vector Search over activity embeddings (P09) |
| Community | invented list | FHIR `HealthcareService` + `Location` near-search (P08) |
| Cohort | invented percentages | de-identified week-4 outcomes from consenting users |
| Save | label only | FHIR `Task` + `Provenance` + `AuditEvent` |

## Visualizations

### Chart 1 · Stacked bar: who does each of the 8 steps

- Type: single horizontal stacked bar (or a 100% bar) split by step kind. Title: "8 steps, 1 language model".

| Kind | Steps | Count |
|---|---|---|
| Rules | 1 Safety screen, 4 Filter | 2 |
| FHIR read (+ vector) | 3 Limits and guideline, 6 Community | 2 |
| Similarity (KNN) | 5 Taste match, 7 Similar users | 2 |
| Small language model | 2 Goal | 1 |
| Patient | 8 Choice and save | 1 |

- What to notice: safety-relevant steps (1, 3, 4) are rules or signed data, never a model.

### Chart 2 · Funnel: from catalogue to Somchai's choice

| Stage | Count |
|---|---|
| Activities in catalogue | 100 |
| Allowed by the signed limits | 67 |
| Shown in the trace (k = 5) | 5 |
| Offered as options | 3 |
| Chosen by the patient | 1 |

- Annotation at 67: "tennis removed: 8.0 METs, bursts". At 3: "bowling, table tennis, badminton".

### Chart 3 · Stacked bar: planned minutes per week by option

| Option | Chosen activity (min) | Brisk walks (min) | Total (min) | Paraphrased ESC lower bound |
|---|---|---|---|---|
| Start gently: 2 sessions | 60 | 80 | 140 | 150 |
| Try 3 sessions | 90 | 60 | 150 | 150 |

- What to notice: the gentle week sits 10 min under the paraphrased guideline floor; this is a first-week choice that progression rules must lift, with clinician sign-off.

### Chart 4 · Timeline: the stop path vs the normal path

| Path | Steps run | Models called | Output |
|---|---|---|---|
| Normal (tennis preset) | 8 | 1 (router; keyword match in demo) | 3 options, then a week of Tasks |
| Red flag ("แน่นหน้าอกตอนเดิน") | 1 | 0 | stop message, 1669, Flag + Communication, coaching paused |

### Diagram · Sequence

`Patient → Rules: screen (clear) → Router: intent + likes → FHIR: CarePlan (signed limits) → Vector Search: 4 guideline lines → Rules: filter 100 → 67 → KNN: top 5 → FHIR: groups near home + heat → Cohort: week-4 (synthetic) → Patient: picks 1 of 3 + 2 or 3 sessions → FHIR: Tasks + Provenance`. Branch at the first box: "match → STOP".

## Numbers and claims ledger

| Claim | Value | Source | Status |
|---|---|---|---|
| Steps in the normal path | 8 | `demo/agent-flow-demo.html` `plan()` | checked |
| Step kinds | rules 2, FHIR 2, KNN 2, small LLM 1, patient 1 | same, `tag` fields | checked |
| Catalogue → allowed | 100 → 67 | same, counted with python3 | checked |
| Tennis top 3 | bowling, table tennis, badminton, 0.945 each | same | checked |
| Limits | 5.9 METs, HR 110, RPE 11–13 | `LIMIT` | synthetic |
| Screen time | "≈0.1 ms" | demo trace label; v2 router median 0.1 ms (`tool_router_v2_results_*`) | demo label; v2 value measured on synthetic data |
| Community groups and distances | 3.2, 0.9, 1.9 km | `COMMUNITY` | synthetic |
| Similar-user week-4 percentages | 49, 52, 57%, n = 52 | `COHORT` | invented |
| Planned minutes | 140 / 150 | `weekPlan()` | checked (our arithmetic) |
| ESC 2020 §4.2.3 lines | 4 paraphrases | `GUIDE` | paraphrased examples, not quotations; primary text to verify (P18) |
| Live run against IRIS | — | — | not done |
| Step 2 label "small LLM" | keyword match in demo | `LIKES`, `plan()` | checked; real router not wired in |

## Limits and open questions

- Scripted demo: no model, no IRIS call, no FHIR write.
- "Build activity plan" is not one of the eight router labels tested in P13–P14.
- The 2-session week is below the paraphrased guideline floor; the progression rule is not implemented.
- The demo's red-flag regex is narrower than the router v2 screen (5 of 12 probe phrases caught vs 12 of 12; see P12).
- The dance keyword bug (P09) would break step 5 for "I like dancing".
- No timing of a real end-to-end run exists.

## Likely judge questions

**Q: Where exactly is the AI?**
In step 2 (understanding the goal) and, in a broader sense, steps 5 and 7 (similarity). The safety screen, the limits, the filter and the save are rules or FHIR operations. The patient makes the final decision.

**Q: Is this live?**
No. The demo is scripted in the browser so judges can see every step. The router was tested separately on synthetic messages (P13–P14); the FHIR resources exist as synthetic bundles (P05).

**Q: What if Somchai has chest pain while asking?**
Step 1 matches, the flow ends there, he gets the stop message with 1669, and a FHIR `Flag` and `Communication` go to the clinician. No model sees the message.

**Q: Why does the plan include walks he didn't ask for?**
The guideline asks for moderate aerobic activity most days; walks fill the other days at a low intensity inside the limits. He can change the plan; the change goes through the same filter.

## Sources

Repo:
- `demo/agent-flow-demo.html` (`plan()`, `weekPlan()`, `finish()`, `RED`, `PRESETS`, `LIMIT`, `GUIDE`, `COMMUNITY`, `COHORT`)
- `pitch/appendix/A04-agentic-harness.md` (sequence diagram and honesty notes)
- `pitch/appendix-deck/P09-agent-flow-8-steps.md`
- `docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md` §5 rules 6, 8
- `.claude/skills/siriraj-mit-review-panel/references/system-eval.md` (property 5)
- `docs/ui-vs-agentic-plan.md` (12:30 walk gap)
- `experiments/tool_router_v2_results_Qwen3-1.7B_cuda.json` (median 0.1 ms)

External: none beyond those on P09 and P10.

## Image-generation prompt

A 16:9 information slide on a white background. Key message as title: "One message, eight steps, one language model." Top: a speech bubble "I used to play tennis… now I have hypertension." Middle: an eight-step horizontal timeline (safety screen, goal, limits and guideline, filter, taste match, community, similar users, choice and save), each step tagged rules, small LLM, FHIR, KNN or patient. Bottom left: a funnel 100 → 67 → 5 → 3 → 1 with "bowling, table tennis, badminton" at 3. Bottom right: a small note "Red flag: stops at step 1, no model". Mark "scripted demo, synthetic data". Use only these numbers, no logos, no invented figures; ChatGPT chooses the design.
