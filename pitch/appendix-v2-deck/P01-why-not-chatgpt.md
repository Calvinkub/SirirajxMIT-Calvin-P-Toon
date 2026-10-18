# P01 · A general chatbot answers what you ask; Heartstep recommends what you will enjoy, only inside the limits your doctor signed.

## Key message

General assistants such as ChatGPT and Claude are strong reasoners and can now read health records and phone health data, but they answer from the conversation and give advice, not a bounded plan. Heartstep is "Netflix for a healthy heart": a chat coach that ranks activities and community groups by three signals (your taste, people like you, near you), and only after fixed rules have removed everything outside a clinician-signed limit record held as FHIR in InterSystems IRIS for Health. In our demo the rules keep 67 of 100 catalogue activities for Somchai, the ranker turns "I used to play tennis" into bowling, table tennis and badminton, and in our synthetic router test a plain small model missed 4 of 4 red-flag messages while the rules-first setup missed 0 of 4.

## Why this matters to the judges

- **Innovation.** The question every judge will ask first is "why can't I just use ChatGPT?". The answer is not "our model is smarter". It is a different product shape: a recommender (ranking a closed, safe catalogue) instead of a generator (writing free advice), with a clinical hard filter in front of the ranker.
- **Real-world impact.** People keep doing what they enjoy and what they do with others. A patient who loved tennis is more likely to keep playing badminton with a club 1.9 km away than to follow "30 minutes of moderate exercise, 5 days a week" (see P02).
- **Use of InterSystems technology.** The bound on the model is data, not a prompt: the limit record is a FHIR `CarePlan` + `Goal` with a `Provenance` naming the clinician as attester, the groups are FHIR `HealthcareService` + `Location`, every plan becomes FHIR `Task`s with a `Provenance` naming the AI as assembler. IRIS Vector Search ranks; FHIR SQL Builder feeds the rules (P03, P06, P07).
- **Technical coherence.** One rule runs through the system: rules decide what is allowed, models decide what is preferred, the patient decides what is chosen, FHIR records who did what.

## Full detail

### 1. Be fair to general chatbots first

General models are not the straw man. In January 2026 Anthropic announced "Claude for Healthcare" at the J.P. Morgan Healthcare Conference, with connectors including electronic health records, HealthEx ("lets people bring their health records into a conversation with Claude and ask important questions in everyday language") and Apple Health and Android Health Connect "rolling out in beta" in the Claude iOS and Android apps (Clinical Trials Arena, opened 2026-10-18). OpenAI launched "Health in ChatGPT"; our earlier appendix says it launched for US users in July 2026, but the OpenAI page returned HTTP 403 when we tried to re-open it on 2026-10-18, so the launch date and country scope are **to verify** before they are said on stage. The Clinical Trials Arena article does not state that Claude's health connectors are US-only; it is US-oriented (CMS coverage database, ICD-10), so "US-focused" is the safe phrasing, not "US-only".

So the honest framing is: general assistants can already read your data and reason about it. What they do not do, by design, is (a) hold a limit record that a named clinician signed and refuse anything outside it, (b) take safety decisions out of the model's hands, (c) start the conversation at a time the patient chose, and (d) rank real, nearby, intensity-tagged community groups instead of describing exercise in general.

### 2. Three differences that matter

**Difference 1: advice versus a bounded recommendation.** A chatbot writes an answer token by token. Any activity, intensity or place can appear in that answer, including ones the patient's doctor ruled out. Heartstep never writes an activity. It filters a fixed catalogue (100 activities in the demo, each with a MET value and safety flags) against the signed limit record, then ranks only what is left. The model's job shrinks from "decide what is safe and good" to "pick one id from an allowed list" (spec §6: "the agent can only pick from missions that the rules engine marks as allowed").

**Difference 2: memory versus record.** A chatbot knows the patient's limits only if the patient types them in, and it cannot tell a typed limit from a signed one. In Heartstep the limit is a FHIR `CarePlan` with extensions `hr-ceiling`, `rpe-target`, `limit-source` and `allowed-activity`, and a `Provenance` whose agent type is `attester` and whose `who` is the clinician. HL7 defines an attester as "An agent (verifier) who attests to the accuracy of the entity" (HL7 terminology, provenance-participant-type, opened 2026-10-18). Spec rule 6: no signed, unexpired limit record, no exercise mission.

**Difference 3: the model decides safety versus rules decide safety.** In a chatbot, "my chest feels tight while walking" goes to the model, which decides what to say. In Heartstep a deterministic Thai/English screen runs before any model. The demo's screen is a regular expression covering phrases such as "chest pain/tight/pressure", "dizz", "faint", "palpitat", "เจ็บหน้าอก", "แน่นหน้าอก", "หน้ามืด", "ใจสั่น", "หายใจไม่ทัน" (`demo/agent-flow-demo.html`, `RED`). A match stops coaching, shows "stop and call 1669" (number to confirm with the clinician) and writes a FHIR `Flag` + `Communication` to the care team.

### 3. Why "Netflix for a healthy heart" is the right analogy and where it stops

Netflix does not ask you to describe the film you want; it shows rows: "Because you watched…", "Popular with people like you", "Trending near you". Heartstep shows three equivalent rows:

| Netflix-style row | Heartstep signal | How it is computed today | Data status |
|---|---|---|---|
| "Because you loved tennis" | Your taste | Cosine nearest neighbours on 11 activity tags (outdoor, indoor, team, ball, aim, competitive, social, water, rhythm, mind-body, walking) among allowed activities | Real code, demo catalogue |
| "Popular with people like you" | People like you | Share still active at week 4 in a similar cohort | **Synthetic** (n = 52, invented percentages) |
| "Groups near you this week" | Near you | FHIR `HealthcareService?location.near=…` | **Synthetic** places, scripted call |

Where the analogy stops: Netflix can show you anything; Heartstep can show you only what the clinician's limits allow. A film recommender's worst error is a boring evening; ours is an unsafe exertion, which is why the safety filter is not a ranking feature but a hard gate that runs first.

### 4. Worked example: Somchai, 58, used to play tennis, now has high blood pressure

Somchai types (demo preset 1): "I used to play tennis every weekend, but now I have hypertension and my doctor says I must lower the intensity. Maybe badminton or bowling? Can you recommend a plan?"

1. **Safety screen (rules, about 0.1 ms, no model).** No red-flag phrase. Continue.
2. **Understand the goal (small model).** Router output: intent `build_activity_plan`; likes = tennis, badminton, bowling; condition = hypertension.
3. **Read limits (FHIR).** `GET /fhir/r4/CarePlan?patient=cmc-p01&status=active` returns a synthetic signed limit: up to about 5.9 METs, heart rate under 110, RPE 11–13, avoid heavy straining and breath-holding. Guideline lines come from `vector_search("hypertension exercise", collection="approved_guidelines", k=4)` (four paraphrased ESC 2020 §4.2.3 lines, P07).
4. **Filter (rules).** 100 activities → 67 allowed. Tennis singles (8.0 METs, flagged "vigorous bursts") is removed. The patient is told why: too intense with his blood pressure for now.
5. **Match taste (KNN).** The mean of tennis, badminton and bowling tag vectors is compared with every allowed activity. Top three, all cosine 0.945: bowling (3.8 METs), table tennis, social (4.0), badminton, social (5.5).
6. **Near you (FHIR, synthetic).** Seniors' bowling league 3.2 km (Wed 10:00); community table-tennis room 0.9 km (daily 16:00–20:00); social badminton club 1.9 km (Tue and Fri 18:30).
7. **People like you (synthetic).** Still active at week 4: badminton 57%, table tennis 52%, bowling 49% (invented cohort).
8. **Ask, then save.** Somchai picks one and "2 sessions" or "3 sessions". The week is written as FHIR `Task`s, each with a `Provenance` (assembler = AI model, reason "picked-from-allowed-set").

A general chatbot given the same message would very likely suggest badminton or bowling too. The difference is not the suggestion; it is that Heartstep could not have suggested tennis, squash or a 5 km run, could not have invented the badminton club, and leaves a FHIR audit trail a clinician can read.

### 5. What we measured about the failure mode (synthetic)

Our tool-router experiment (`experiments/RESULTS_tool_router_demo.md`, 36 synthetic test messages per run, 4 of them red flags) compared a plain small model writing its own tool call (config A) with a rules gate in front (config C). With Qwen3-0.6B, 1.7B and 4B, config A missed 4 of 4 red flags in every run; with rules in front, 0 of 4. Config A on Qwen3-0.6B also answered "is PM2.5 high today?" with "currently high" without calling the air-quality tool: an invented fact. On a later blind test (270 synthetic messages, v2), rules plus a Qwen3 router still missed 4 of 30 red flags (P14). That second number matters: rules are necessary, but phrase lists alone are not enough, which is why v3 adds a second screen that can only escalate, never clear.

### 6. Alternatives we rejected

- **Prompt a general model with the limits.** Rejected: a prompt is a request, not a constraint; the model can still output any activity, and there is no signed record.
- **Fine-tune a model on exercise prescriptions.** Rejected for v1: no labelled Thai data, and a model that writes prescriptions moves toward medical-device territory (A12). We keep the AI as a scheduler inside clinician limits.
- **Pure rules app with no chat.** Rejected: the patient's goal ("I loved tennis") is free text in Thai or English; a small model is the cheapest way to turn it into slots.

## Visualizations

### Chart 1 · Funnel: from catalogue to three choices (demo, synthetic limit)

- **Type:** horizontal funnel (or descending bar).
- **Title:** "100 activities → 67 inside the signed limit → 3 offered"
- **Axis / units:** count of activities.

| Stage | Activities | What removes the rest | Who decides |
|---|---|---|---|
| Demo catalogue | 100 | — | Team-curated list (44 with a 2024 Adult Compendium code) |
| Above 5.9 METs | −29 | MET value > limit | Rules |
| At or below 5.9 METs but flagged contact, heavy straining or vigorous bursts | −4 | Safety flags `x`, `h`, `v` | Rules |
| Allowed set | 67 | — | Rules |
| Ranked by taste (cosine) | 67 ranked | — | KNN (no LLM) |
| Offered to Somchai | 3 | Top 3 | Ranker; patient chooses |

Annotation: "Tennis singles (8.0 METs) removed before ranking." **What the reader should notice:** the model never sees the 33 removed activities, so no ranking error can bring one back. Of the 29 over-limit activities, 25 also carry a safety flag; the flags alone remove 4 more that are within the MET limit. Source: computed from `demo/agent-flow-demo.html` `RAW`, `LIMIT` and `plan()` on 2026-10-18.

### Chart 2 · Bar: taste similarity of the top 10 allowed activities for Somchai

- **Type:** horizontal bar, sorted.
- **Title:** "Closest to tennis + badminton + bowling, among allowed activities"
- **Axis:** cosine similarity of 11-tag vectors (0–1).

| Rank | Activity | METs | Cosine | 2024 Compendium code |
|---|---|---|---|---|
| 1 | Bowling | 3.8 | 0.945 | 15092 |
| 2 | Table tennis, social | 4.0 | 0.945 | 15660 |
| 3 | Badminton, social | 5.5 | 0.945 | 15030 |
| 4 | Petanque | 3.3 | 0.850 | 15465 (closest listed) |
| 5 | Bocce | 3.3 | 0.850 | 15465 |
| 6 | Croquet | 3.3 | 0.850 | 15160 |
| 7 | Golf with a power cart | 3.5 | 0.850 | 15290 |
| 8 | Miniature golf | 3.5 | 0.850 | 15270 |
| 9 | Pickleball | 4.5 | 0.850 | none (team estimate) |
| 10 | Putting practice | 2.3 | 0.764 | none (team estimate) |

Annotation: ties are broken by lower METs. **Notice:** the top three tie at 0.945 because 11 binary tags are coarse; a real system needs richer features and the cohort and distance signals (P09). Source: same computation.

### Chart 3 · Grouped bar: red-flag messages missed (synthetic router test v1)

- **Title:** "Rules in front catch the red flags a plain model misses"
- **Axis:** red-flag messages missed, of 4 (lower is better).

| Model | A. Model writes the tool call | C. Rules first, then one-pass scoring |
|---|---|---|
| Qwen3-0.6B | 4 | 0 |
| Qwen3-1.7B | 4 | 0 |
| Qwen3-4B | 4 | 0 |

Annotation: "Synthetic messages, n = 36 per run, 4 red flags. Blind v2 test: 4 of 30 still missed (P14)." **Notice:** model size does not fix the safety gap; the architecture does, and even the architecture needs a better screen.

### Diagram · Two pipelines side by side

Left, "General chatbot": Patient asks → model decides facts, safety and tone → answer. Right, "Heartstep": message → red-flag screen [RULES] → (match → stop, call 1669, FHIR Flag + Communication) / (clear → read signed CarePlan [FHIR] → filter catalogue [RULES] → rank by taste, people like you, near you [KNN + VECTOR] → patient chooses → Task + Provenance [FHIR]).

## Numbers and claims ledger

| Claim | Value | Source | Status |
|---|---|---|---|
| Catalogue size | 100 | `demo/agent-flow-demo.html` `RAW` (counted) | checked |
| Allowed after filter | 67 | computed from `RAW` with `met <= 5.9` and no `h/x/v` flag | checked (synthetic limit) |
| Removed by MET / by flag only | 29 / 4 | computed | checked |
| Activities with 2024 Compendium code | 44 (1 "closest listed") | `RAW` (counted) | checked; MET values to verify by clinician |
| Top 3 for Somchai | Bowling, table tennis, badminton, cosine 0.945 | computed from `plan()` | checked |
| Group distances | 3.2 km, 0.9 km, 1.9 km | `COMMUNITY` in demo | synthetic |
| Week-4 activity shares | 57%, 52%, 49% (n = 52) | `COHORT` in demo | synthetic |
| Demo limit | ≤ 5.9 METs, HR < 110, RPE 11–13 | `LIMIT` (patient `cmc-p01`) | synthetic |
| Red flags missed, model writes call | 4 of 4 (0.6B, 1.7B, 4B) | `experiments/RESULTS_tool_router_demo.md` | simulated (synthetic) |
| Red flags missed, rules first | 0 of 4 | same | simulated (synthetic) |
| Blind v2 red flags caught | 26 of 30 | same, v2 section | simulated (synthetic) |
| Invented PM2.5 answer | Qwen3-0.6B, config A | same | checked (synthetic) |
| Claude for Healthcare, JPM 2026, Apple Health and Health Connect beta | as quoted | Clinical Trials Arena (link below) | checked |
| Health in ChatGPT, US, July 2026 | — | OpenAI page returned 403 | to verify |
| "Attester" definition | as quoted | HL7 terminology JSON | checked |

## Limits and open questions

- The comparison with general chatbots is architectural, not a head-to-head test. We have not run ChatGPT or Claude on the same 36 or 270 messages; doing so (with the same rules scoring) would turn an argument into a measurement.
- The "people like you" and "near you" rows are invented data in the demo. Only the taste ranking is real code.
- Resolved (2026-10-18): the demo patient is now bundle `cmc-p01` (Somchai, 58, Bang Na, high blood pressure and an MI this year, HR < 110, ≤ 5.9 METs). See README "Changes after the pages were written".
- The 11-tag taste vector is coarse (three-way tie at the top).
- Red-flag rules were written by the same person who wrote the test messages; the blind v2 test still missed 4 of 30.
- "1669" as the patient-facing number must be confirmed by the clinical mentor.

## Likely judge questions

1. **"ChatGPT already reads Apple Health. Why build this?"** Reading data is not the gap. The gap is a signed limit that the system cannot cross, safety decided outside the model, and real local groups. We keep the model, but bounded by FHIR records in IRIS.
2. **"Couldn't you just put the limits in a system prompt?"** A prompt is a request. Our model never outputs an activity it was not given; the allowed set is computed by rules from a signed `CarePlan`, and a validator rejects any id outside it.
3. **"Is your model better than GPT at exercise advice?"** We do not claim that. Our small models do narrow jobs (routing, picking an id). Quality comes from the clinician's limits and the curated catalogue, not from model knowledge.
4. **"What happens if the patient says 'chest tight' in slang?"** Rules first; in our blind synthetic test 4 of 30 phrasings slipped through, so v3 adds spacing-tolerant lexicons and a second screen that can only escalate to the stop path.
5. **"Why Netflix?"** Because the hard part of exercise after a diagnosis is not knowing that exercise helps; it is finding something you enjoy, with people, near home, that your doctor allows. That is a recommendation problem with a safety constraint.

## Sources

Repo:
- `demo/agent-flow-demo.html` (`RAW`, `LIMIT`, `GUIDE`, `COMMUNITY`, `COHORT`, `RED`, `plan()`, `PRESETS`)
- `experiments/RESULTS_tool_router_demo.md`
- `docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md` §5–6
- `pitch/appendix/A01-why-not-chatgpt.md`, `pitch/appendix-deck/P01-why-not-chatgpt.md`, `docs/pitch/faq-appendix/slides/chatbot.html`
- `synthetic/fhir/p01_Somchai_Kaewmanee.json`

External (opened 2026-10-18):
- Clinical Trials Arena, "JPM26: Anthropic advances healthcare presence with new AI toolkit": https://www.clinicaltrialsarena.com/news/jpm26-anthropic-advances-healthcare-presence-with-new-ai-toolkit-2/
- HL7 terminology, Provenance participant type code system: https://terminology.hl7.org/CodeSystem-provenance-participant-type.json
- OpenAI, "Health in ChatGPT": https://openai.com/index/health-in-chatgpt/ (**returned 403; not re-read; to verify**)

## Image-generation prompt

Design one 16:9 information slide on a white background. Put the key message first as the title: "A general chatbot answers what you ask; Heartstep recommends what you will enjoy, only inside the limits your doctor signed." Make the main visual a funnel "100 activities → 67 inside the signed limit → 3 offered" with the three offered activities labelled Bowling, Table tennis, Badminton, and a small side panel contrasting "General chatbot: model decides facts, safety and tone" with "Heartstep: rules filter first, recommender ranks, patient chooses, FHIR records". Add a small bar pair "Red flags missed (synthetic test): model alone 4 of 4, rules first 0 of 4". Mark synthetic data as synthetic. No logos, no invented numbers; choose the design freely.
