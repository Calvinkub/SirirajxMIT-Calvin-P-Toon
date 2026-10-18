# P21 · Six gates to a pilot, each passed by a named human; the critical path is people, not code

## Key message

Heartstep reaches real patients only through six gates: prototype, clinician review, usability, ethics and regulatory, supervised pilot, insurer pilot. Each gate has written exit criteria, and four of the six can only be passed by named humans (clinicians, an IRB, lawyers, a statistician, an insurer); our simulated review panel can inform a gate but never pass one. We are inside gate G-A today, the engineering steps run cheapest-first on the InterSystems kit, and the real blocker is that no Siriraj clinical owner is named yet.

## Why this matters to the judges

- **Real-world impact.** Judges want to know whether this can leave the hackathon. A path with named owners, exit criteria and stop rules is more credible than a timeline with dates nobody has agreed.
- **Use of InterSystems technology.** The first five engineering steps are on IRIS for Health: load the FHIR bundles, project them with FHIR SQL Builder, build vector tables, expose FHIR through an MCP server. The InterSystems mentorship we ask for shortens exactly these steps.
- **Technical coherence.** The gates reuse the evaluation framework (P15): property tests, the 18-scenario suite, red-flag recall with a denominator, and pilot stop rules. The roadmap is the evaluation plan in time order.

## Full detail

### The six gates

| Gate | Entry needs | Exit needs (from `system-eval.md`) | Who passes it | Where we are (2026-10-18) |
|---|---|---|---|---|
| **G-A Prototype** | Design approved by the team | L1 property tests and L2 red-flag tests pass; scenarios SC-01…SC-18 pass (SC-16…18 checked by a person); no open S0 in the last panel run (the panel informs, it cannot pass a gate) | Team | **In progress.** UI with rules-only checks (6/6 tests pass). 383 synthetic FHIR resources in 9 bundles. Router v1 and v2 run on a T4. Scripted 8-step recommender demo. Not yet: bundles confirmed in IRIS, SQL Builder, Vector Search, MCP, scenario suite |
| **G-B Clinician review** | G-A done; limit library written | A real cardiologist and rehab physician review limits, stop rules and the Thai red-flag phrase list **in writing** | Named Siriraj clinicians | 12-question reconcile table ready to send. **Owner not named** |
| **G-C Usability** | G-B done | ≥ 8 target-age Thai users complete onboarding and a week of recommendations in a moderated test; no S0/S1 usability issue | Usability lead + cardiac nurse | Not started |
| **G-D Ethics and regulatory** | G-C done | IRB decision; Thai FDA classification confirmed in writing; PDPA consent flow reviewed by a lawyer | IRB, regulatory lawyer, privacy lawyer or DPO | Intended-use draft and consent design (P20) |
| **G-E Supervised pilot** | G-D done | Small low-risk cohort with a named clinician, weekly safety review, pre-written stop rules (any intensity violation or serious event pauses enrolment) | Clinician + statistician | Not started |
| **G-F Insurer pilot** | G-E clean | Pre-registered outcomes, matched comparison, statistician sign-off | Insurer + statistician | No insurer contacted |

The concierge pilot (human-sent recommendations over LINE to 8–10 clinician-enrolled patients, P19) is not a seventh gate. It is a cheap market and behaviour test that can run alongside G-B and G-C, but only after an IRB decision, so in practice it waits for the ethics part of G-D.

### Gate G-A in detail: what "done" means and what is missing

| G-A exit criterion | Status | Evidence |
|---|---|---|
| L1 property tests (7 properties: never above limit; no recommendation if risk high or missing; no limit-writing tool; no exercise after unresolved red flag; progression caps; beta-blocker uses RPE; post-CABG restriction) | Not written as tests | `system-eval.md` L1 |
| L2 red-flag deterministic test | Partial: UI tests cover English and Thai red flags; a probe found 9 groups of common Thai and English phrasings missed (e.g. "แน่นหน้าอก", "chest pressure", "I can't breathe") | `tests/safety.test.mjs`; `docs/ui-vs-agentic-plan.md` |
| Router red-flag recall on a blind set | 26 of 30 caught (86.7%) on synthetic data; 4 misses | `experiments/tool_router_v2_results_*` |
| Scenarios SC-01…SC-15 automated | 0 run | `SYNTHESIS.md`: "0 of 18 scenarios run" |
| SC-16…SC-18 checked by a person | 0 run | same |
| No open S0 in the last panel run | 5 S0 findings at the 2026-10-17 run; design fixes since (rules 6–11, consent, intended use) not re-reviewed | `SYNTHESIS.md` |

So G-A is roughly a third done in spirit and not passed in letter. The most important item is the red-flag lexicon: the router v2 misses ("ใจมันเต้นรัว", "blackout", a denial followed by a real symptom) and the UI probe misses point the same way. Version 3 uses spacing- and filler-tolerant matching, one-clause negation scope, and a model screen that can only escalate to the stop path, never clear it, and it must be tested on a **new** human-written blind set.

### Engineering track (cheapest first)

| # | Step | Uses | Done when | Status |
|---|---|---|---|---|
| 1 | Load the 9 synthetic bundles into the kit's IRIS for Health FHIR server | `synthetic/load_to_iris.py` | All bundles return 200; custom extensions accepted | Loader written; run to confirm |
| 2 | FHIR SQL Builder projection for limits, vitals, tasks, symptom checks, places | Kit tutorial 3.5 | Rules engine reads limits from SQL | Not started |
| 3 | Rules engine + L1 property tests + scenario suite SC-01…18 | `system-eval.md` | L1, L2 and all scenarios green | UI rules only |
| 4 | Vector tables for approved guideline passages and the activity catalogue; Thai embedding test | Kit vector skill; BGE-M3 candidate | Recall@3 on a held-out Thai set | Not started (demo ranks in-browser) |
| 5 | MCP server over FHIR with the typed tool list | Kit FastMCP pattern | Tool-scope audit: no extra write tools | Not started |
| 6 | Router v3 + red-flag v3 on a new human-written blind set | `docs/research/neurosymbolic-tool-router-plan.md` | Red-flag recall reported with its denominator; 0 red flags reach a model | v1, v2 done |
| 7 | MedGemma choice step with validator; safe default on any failure | vLLM guided JSON | 100% of outputs in the allowed set (by validation) | Not started |
| 8 | Thai TTS choice (Typhoon2-Audio vs JaiTTS); pre-recorded safety audio | — | Listening test with target-age users | Not started |
| 9 | Decoding benchmark (three arms) | P17 | p95 latency and US$ per 1,000 patient-days measured | Not started |

Steps 1–5 are where InterSystems mentorship matters most. Steps 6–9 can run in parallel with G-B, because they do not touch patients.

### What "MVP" means here

| In the MVP (G-A to G-E) | Out of the MVP |
|---|---|
| Clinician-enrolled, clinician-confirmed low-risk post-MI patients | Heart failure, high-risk hypertension, moderate or high risk without supervision |
| Recommendations from the walking-type and social-sport catalogue inside the signed limit, with warm-up and cool-down | Resistance training; any %HRR calculation |
| Nearby real-world groups (clubs, parks, courts) recommended from district location | Free-text peer community inside the app |
| Symptom tap + rules-only stop path; clinician flag queue | Insurer access to patient-level data |
| Thai text first; Thai voice once a Thai TTS passes testing | Hospital HL7v2/CDA integration (after the pilot) |
| FHIR on IRIS for Health; SQL Builder rules; Vector Search grounding | — |

Note the gap between the demo and the MVP: the demo tells Somchai's hypertension story, but the MVP population is low-risk post-MI, because that is the population our clinical research and synthetic bundles cover. Hypertension enters scope only when a clinician writes its rules (P18).

### Why a small pilot cannot prove safety

A supervised pilot will be small. If it has zero serious events, that does **not** show the event rate is zero. The exact one-sided 95% upper bound on the rate after 0 events in n patients is 1 − 0.05^(1/n), close to the "rule of three" (3/n):

| Patients with 0 events (n) | Exact 95% upper bound | Rule of three (3/n) |
|---|---|---|
| 10 | 25.9% | 30.0% |
| 20 | 13.9% | 15.0% |
| 30 | 9.5% | 10.0% |
| 50 | 5.8% | 6.0% |
| 100 | 3.0% | 3.0% |
| 300 | 1.0% | 1.0% |
| 1,000 | 0.3% | 0.3% |

So safety must rest on the deterministic layers (signed limits, rules filter, red-flag stop path, property tests), and the pilot's job is to check that those layers behave as designed with real people. A statistician sets the pilot size and states what bound it supports; the same arithmetic applies to the "20 runs, 0 failures" smoke tests in the agent evaluation, which bound the failure rate at about 14%.

### Risks that could stop us

| Risk | Mitigation |
|---|---|
| No named clinical owner | Ask the Siriraj mentor now, with the reconcile table. Without an owner: no patient use |
| Thai FDA classes it as SaMD (Class 2–4) | Keep features fixed and clinician-approved; plan for a review period of up to about 250–300 days (secondary source, P20) |
| Red-flag recall not good enough on real Thai phrasing | Fail toward the stop path; clinician-written lexicon; escalate-only model screen; new blind set |
| Recommender suggests activities people do not enjoy or cannot reach | Concierge pilot measures uptake per recommended activity and group before automation |
| Insurers do not pay | B2C and hospital routes; interviews and the concierge pilot test willingness to pay early |
| A pilot cannot show safety statistically | Statistician sets size and bound; safety rests on deterministic layers |

### Worked example: Somchai through the gates

Today Somchai exists only as synthetic FHIR and a scripted demo (G-A). At G-B, a Siriraj cardiologist decides whether a 5.9 MET ceiling, a heart rate under 110 and RPE 11–13 are a sensible kind of limit record for someone like him, and signs the Thai phrases that must stop him. At G-C, eight people his age try to onboard and pick badminton or bowling without help. At G-D, an IRB and lawyers approve the consent text and the device position. At G-E, real low-risk post-MI patients use it with weekly safety review. Only at G-F does an insurer see aggregate results, against outcomes written down in advance.

## Visualizations

### Chart 1 · Timeline (no dates): six gates with owners and status

- **Type:** horizontal milestone timeline, evenly spaced, no time axis.
- **Title:** "Six gates to a pilot; each passed by a named human"
- **Data:**

| Order | Gate | Passed by | Status |
|---|---|---|---|
| 1 | G-A Prototype | Team | In progress |
| 2 | G-B Clinician review | Cardiologist + rehab physician | Blocked: owner not named |
| 3 | G-C Usability | ≥ 8 Thai users aged 55–75; usability lead + nurse | Not started |
| 4 | G-D IRB, Thai FDA, PDPA | IRB + lawyers | Not started |
| 5 | G-E Supervised pilot | Clinician + statistician | Not started |
| 6 | G-F Insurer pilot | Insurer + statistician | Not started |

- **Annotations:** G-A filled, G-B outlined in the warning colour with "owner not named", the rest grey. A bracket over G-B to G-F: "needs named humans". No dates.
- **What the reader should notice:** the next blocker is a person, not a feature.

### Chart 2 · Line chart: what zero events can and cannot show

- **Type:** line chart, log X axis.
- **Title:** "Zero serious events in a small pilot still allows a high true rate"
- **X axis:** patients with zero events (log). **Y axis:** 95% upper bound on the event rate (%).
- **Data:** the table in "Why a small pilot cannot prove safety" (exact and rule-of-three columns as two lines).
- **Annotations:** point at n = 20, "0/20 → up to ≈ 14%"; point at n = 300, "≈ 1%".
- **What the reader should notice:** safety has to be built in, not inferred from a pilot.

### Chart 3 · Stacked bar: engineering steps by status

- **Type:** single horizontal stacked bar (or nine-cell status strip).
- **Title:** "Nine engineering steps, cheapest first"
- **Data:**

| Status | Steps | Count |
|---|---|---|
| Partly done (code exists, not yet confirmed or complete) | 1 loader; 3 UI rules; 6 router v1/v2 | 3 |
| Not started | 2, 4, 5, 7, 8, 9 | 6 |
| Done | — | 0 |

- **What the reader should notice:** the prototype is real but early; most of the IRIS integration is the next work, which is where mentorship helps.

### Chart 4 · Bar chart: red-flag evidence so far

- **Type:** grouped bars.
- **Title:** "Red-flag detection is the first G-A item to fix"
- **Data:**

| Test | Caught | Total | Note |
|---|---|---|---|
| Router v1 rules (synthetic) | 4 | 4 | same writer wrote rules and messages |
| Router v2 rules, blind synthetic set | 26 | 30 | 4 misses: unusual Thai spacing, "blackout", negation then symptom |
| Plain LLM writing the tool call (v1) | 0 | 4 | no concept of red flags |

- **What the reader should notice:** rules beat the model, but phrase-matching rules are not enough; v3 must fail closed.

## Numbers and claims ledger

| Claim | Value | Source | Status |
|---|---|---|---|
| Gates G-A to G-F and exit criteria | as in table | `.claude/skills/siriraj-mit-review-panel/references/system-eval.md` | checked (proposal v0.1) |
| Panel cannot pass a gate | quote | same | checked |
| UI tests | 6 of 6 pass (run 2026-10-18) | `npm test`; `tests/*.mjs` | checked |
| UI red-flag probe misses | 9 phrase groups | `docs/ui-vs-agentic-plan.md` | checked |
| Router v2 red flags | 26 of 30; 1 false alarm | `experiments/tool_router_v2_results_*` | synthetic |
| Scenarios run | 0 of 18 (as of panel run) | `evaluation/reviews/2026-10-17-document/SYNTHESIS.md` | checked |
| S0 findings at panel run | R1–R5 | same | simulated |
| Synthetic data | 383 resources, 9 bundles | `synthetic/fhir/*.json` (counted) | synthetic |
| Bundles loaded in IRIS | — | `pitch/README.md` open item | to confirm |
| Zero-event bounds | as in table | arithmetic | checked |
| Concierge pilot size | 8–10 patients | `SYNTHESIS.md` R16 | simulated panel suggestion |
| Usability gate size | ≥ 8 users aged 55–75 | `system-eval.md` | proposal |
| Dates, budget, pilot size | — | — | not committed |

## Limits and open questions

- No dates or budget: the repo has no committed timeline and we do not invent one.
- No named clinical owner, IRB contact, lawyer or insurer.
- G-A exit criteria have themselves been criticised by the simulated panel (for example, adding SC-19 onward for tool-boundary rejection, stored prompt injection, Thai negation, medication changes); the scenario list will grow.
- Whether the 9 bundles load cleanly into IRIS with our custom extensions is unconfirmed.
- The demo population (hypertension) and the MVP population (low-risk post-MI) differ.
- Pilot size, stop rules and outcome measures need a statistician.

## Likely judge questions

1. **"What happens the week after the hackathon?"** Two things in parallel: send the 12-question reconcile table to a Siriraj clinician and ask them to own the limit library (G-B), and load our bundles into IRIS and build the SQL Builder projection (engineering steps 1–2).
2. **"When can a patient use it?"** After G-D at the earliest, meaning a clinician review, a usability test, an IRB decision and written Thai FDA and PDPA answers. We have not put dates on that because none of those people have agreed to anything yet.
3. **"How will you know it is safe?"** Mostly by construction: signed limits, a rules filter, a rules-only stop path and property tests. A pilot checks that this works with real people; a pilot of 20 with zero events still allows a rate of up to about 14%, so it cannot prove safety alone.
4. **"What would make you stop?"** In the pilot, any intensity violation or serious adverse event pauses enrolment. Before that, failing the red-flag recall target on a new blind set or a Thai FDA answer we cannot meet with fixed, clinician-approved features.
5. **"Why should InterSystems help?"** Because the next five engineering steps are IRIS for Health work (FHIR load, SQL Builder, Vector Search, MCP over FHIR), and doing them right is what turns the scripted demo into a running system.

## Sources

Repo files:
- `.claude/skills/siriraj-mit-review-panel/references/system-eval.md` (layers, scenarios, metrics, stage-gates)
- `evaluation/reviews/2026-10-17-document/SYNTHESIS.md` (findings, scenario count, cheapest actions; simulated)
- `docs/ui-vs-agentic-plan.md` (UI status, red-flag probe)
- `tests/safety.test.mjs`, `tests/ui.test.mjs`, `safety.js`
- `experiments/RESULTS_tool_router_demo.md`, `experiments/tool_router_v2_results_*`
- `docs/research/neurosymbolic-tool-router-plan.md`
- `research/guidelines/RECONCILE-for-clinician.md`
- `synthetic/load_to_iris.py`; `FHIR-AI-Hackathon-Kit/Tutorials/3-fhir/markdown/3.5-projecting-fhir-data-in-sql.md`
- `pitch/README.md` (open items); `pitch/appendix/A13-roadmap-mvp.md`; `pitch/appendix-deck/P19-roadmap-to-pilot.md`

External: none needed; the bound table is arithmetic.

## Image-generation prompt

Design one 16:9 information slide on a white background. Title, the key message: "Six gates to a pilot, each passed by a named human; the critical path is people, not code." Main visual: a horizontal timeline with six gate circles and no dates: "G-A Prototype – team – IN PROGRESS" (filled), "G-B Clinician review – cardiologist + rehab physician – OWNER NOT NAMED" (orange outline), "G-C Usability – ≥ 8 Thai users aged 55–75", "G-D IRB, Thai FDA, PDPA – IRB + lawyers", "G-E Supervised pilot – clinician + statistician", "G-F Insurer pilot – insurer + statistician" (grey, "NOT STARTED"). Below, a small line chart "Zero events still allows a high true rate": 10 patients 25.9%, 20 patients 13.9%, 50 patients 5.8%, 100 patients 3.0%, 300 patients 1.0%. A side box "Next week: send 12-question reconcile table to Siriraj · load 9 FHIR bundles into IRIS · SQL Builder projection". No dates, no budget, no logos, no other numbers. ChatGPT chooses the design.
