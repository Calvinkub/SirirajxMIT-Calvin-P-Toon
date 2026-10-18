# P16 · The AI costs about US$0.78 a patient-month on our estimate; people and licences are the real cost

## Key message

On an estimated budget of 7,800 input and 1,050 output tokens per patient-day, Heartstep's model calls cost about US$0.78 per patient-month at Claude Sonnet 5.5 list prices, or US$2.11 on one rented H100 shared by 1,000 patients. That is roughly 5–15% of a 499 THB (≈ US$14) monthly price, so AI inference does not decide whether the business works. The lines that do decide it, clinician sign-off time and the IRIS for Health licence, are not priced yet, and the token budget itself has not been measured.

## Why this matters to the judges

- **Real-world impact.** A recommender that a hospital or insurer cannot afford to run never reaches Somchai. Judges will ask "what does one patient cost you?" and this page answers with a number, its arithmetic and what it leaves out.
- **Technical coherence.** The cost follows from the design: rules decide most messages for free, the recommender ranks a closed catalogue instead of writing prose, and models return short JSON ids. Cost is low because the architecture keeps models on a short leash, not because of a pricing trick.
- **Use of InterSystems technology.** The IRIS licence is a real line in our budget, and we say so. Most of the heavy lifting (FHIR storage, SQL projection, vector search) runs in IRIS, not in a GPU, which is one reason model cost stays small.

## Full detail

### What we are costing

Heartstep is "Netflix for a healthy heart": a chat coach that recommends activities and community groups a patient will enjoy, inside limits a doctor signed. Per active patient per day, the estimated model load is one recommendation or mission call, two short chat or voice check-ins, and a share of a weekly clinician summary. We estimated that load at about **7,800 input tokens and 1,050 output tokens per patient-day** (`docs/pitch/faq-appendix/slides/cost.html`). This is an estimate. We have not logged a single real patient-day, so every number on this page inherits that uncertainty.

Over a 30-day month that is 234,000 input tokens (0.234 M) and 31,500 output tokens (0.0315 M) per patient.

### The arithmetic, line by line

| Step | Calculation | Result |
|---|---|---|
| Monthly input tokens | 7,800 × 30 | 0.234 M |
| Monthly output tokens | 1,050 × 30 | 0.0315 M |
| Claude Sonnet 5.5 (US$2 in, US$10 out per M) | 0.234 × 2 + 0.0315 × 10 = 0.468 + 0.315 | **US$0.78** |
| Claude Opus 5.5 (US$4 in, US$20 out per M) | 0.234 × 4 + 0.0315 × 20 = 0.936 + 0.630 | **US$1.57** |
| Claude Haiku 5.5 (US$0.10 in, US$0.50 out per M, ≤ 100K-token tier as listed) | 0.234 × 0.10 + 0.0315 × 0.50 = 0.0234 + 0.0158 | **≈ US$0.04** |
| Sonnet 5.5 if 80% of input is a cached prefix (cache read US$0.10 per M; cache-write cost ignored) | 0.234 × (0.2 × 2 + 0.8 × 0.10) + 0.315 = 0.112 + 0.315 | **≈ US$0.43** (scenario) |
| One H100, 24/7, at ≈ US$2.89/h | 2.89 × 730 h | **≈ US$2,110 a month** |
| Per patient at 1,000 patients | 2,110 / 1,000 | **US$2.11** |
| Per patient at 10,000 patients (only if one GPU holds the load) | 2,110 / 10,000 | **US$0.21** |
| Break-even, one H100 vs Sonnet 5.5 | 2,110 / 0.783 | **≈ 2,700 patients** |
| Break-even, one H100 vs Opus 5.5 | 2,110 / 1.566 | **≈ 1,350 patients** |
| Price | 499 THB / 35 THB per US$ (assumed rate) | **≈ US$14.26** |
| AI share of price | 0.78 / 14.26 (Sonnet); 1.57 / 14.26 (Opus); 2.11 / 14.26 (H100 at 1,000) | **5.5%; 11%; 15%** |

Two lines are new in this version. The Haiku 5.5 line and the cache-read scenario come from the price page we opened on 2026-10-18 (claude.com/pricing). They show that the API bill can fall another order of magnitude if a smaller model is good enough for check-ins and if the long, fixed part of each prompt (patient limits, guideline passages, tool list) is cached. Neither has been tested for quality. Haiku-class output on Thai chat is unmeasured, and the 80% cached share is an assumption chosen to show the size of the effect, not a measurement.

### Why we still plan to self-host the patient-facing models

At pilot size, self-hosting is **more expensive**: US$2.11 per patient-month at 1,000 patients against US$0.78 on the Sonnet API. We plan to self-host anyway, for three reasons:

1. **Data residency under PDPA.** Health data is sensitive personal data under PDPA Section 26 (see P20). Keeping patient-identifying model calls on a server in Thailand avoids a cross-border transfer question that still needs a lawyer's answer.
2. **Thai speech.** The Thai speech-in and speech-out candidates (Qwen3-ASR; Typhoon2-Audio or JaiTTS to test) are open-weight and run on our own GPU.
3. **Cost that stops growing per token.** A rented GPU is a fixed monthly bill. Past about 2,700 active patients it is cheaper than the Sonnet API on our budget, if one GPU can carry the load. That capacity is the biggest unknown on this page.

A hybrid is the realistic pilot setup: de-identified, non-patient work (for example drafting guideline summaries for clinician review) on an API, and anything carrying patient data on our own model. That split needs the consent design in P20 first.

### Why the load is small by design

- **Rules decide most messages without any model.** In router v2 on a blind synthetic set, 161 of 270 messages (35 safety, 126 frequent-phrase) were decided by rules: 59.6% with zero model cost (`experiments/tool_router_v2_results_Qwen3-*_cuda.json`, tier counts).
- **The recommender ranks, it does not write.** Somchai's catalogue of 100 activities is filtered by rules to 67, then ranked by nearest-neighbour similarity to what he enjoys. That ranking is arithmetic on vectors in IRIS, not token generation.
- **Models return ids, not essays.** The choice step returns a short JSON id from the allowed set. Router v2 also caches a 617-token prompt prefix (`prefix_tokens_cached: 617`), which is the same idea as the cache-read scenario above.
- **Constraint-pruned decoding** may cut the output side further (P17). Not benchmarked.

### Worked example: Somchai's month

Somchai, 58, used to play tennis and now has hypertension. In a typical month he sends a few dozen chat messages, gets a weekly plan (badminton Tuesday and Friday, a walking day), answers symptom taps after each session, and his clinician gets one summary a week. On our budget his month costs about 78 US cents on the Sonnet API. If he switched his phone to Thai voice, ASR and TTS compute would be added, and we have not modelled it. If he reported chest tightness, the stop path runs in rules and costs nothing in tokens. The expensive minutes in his month are human: the cardiologist who signed his limit (≤ 5.9 METs, heart rate under 110, RPE 11–13 in the synthetic demo record) and who reads his weekly flags.

### What the R&D itself cost

The measured experiments behind this deck were cheap. All Colab T4 runs used about **0.21 compute units in total**; the v1 three-model run is recorded at about 0.14 units (`experiments/RESULTS_tool_router_demo.md`), so the v2 blind test used roughly the remainder. Local runs used an Apple Silicon Mac. This matters for credibility, not for unit economics: the team can afford to re-run every number on the slide.

### What is NOT in these numbers

| Cost line | Why it matters | Status |
|---|---|---|
| Clinician time: signing limits, reviewing flags and weekly summaries | Every exercising user needs a signed limit (safety rule 6). Likely the largest line | **To price with Siriraj** |
| InterSystems IRIS for Health licence and hosting | Production licence; development uses the kit's Community edition | **To price with InterSystems** |
| Thai speech (ASR, TTS), embeddings, storage, push notifications | Real compute, not modelled | Not modelled |
| Second GPU for redundancy | A single GPU is a single point of failure; doubling it doubles the GPU line | Not modelled |
| Customer acquisition and insurer sales cycle | Unknown; no Thai data (P19) | Unknown |
| Wearables | Patients use their own watch; no kit is shipped (unlike Movn) | Assumed zero |

## Visualizations

### Chart 1 · Bar chart: AI cost per patient-month by serving option (estimate)

- **Type:** vertical bar chart, one bar per option.
- **Title:** "AI cost per patient-month (US$), estimated token budget"
- **X axis:** serving option. **Y axis:** US$ per patient-month, 0 to 2.5.
- **Data:**

| Option | US$ per patient-month | Basis | Status |
|---|---|---|---|
| Claude Haiku 5.5 API | 0.04 | US$0.10 / 0.50 per M (≤ 100K tier) | estimate; quality untested |
| Sonnet 5.5, 80% cached input | 0.43 | cache read US$0.10 per M | scenario |
| Claude Sonnet 5.5 API | 0.78 | US$2 / 10 per M | estimate |
| Claude Opus 5.5 API | 1.57 | US$4 / 20 per M | estimate |
| 1 H100, 1,000 patients | 2.11 | US$2.89/h × 730 h / 1,000 | estimate |
| 1 H100, 10,000 patients | 0.21 | same / 10,000 | estimate; capacity not measured |

- **Annotations:** a thin line above the bars, "Assumes 7,800 input + 1,050 output tokens per patient-day (not measured)". Dashed outline on the 10,000-patient bar and the cached-Sonnet bar with footnotes "capacity not measured" and "scenario".
- **What the reader should notice:** every option is under US$2.20 a month, and the choice between API and own GPU is driven by data residency and scale, not by price at pilot size.

### Chart 2 · Line chart: cost per patient vs number of patients (break-even)

- **Type:** line chart, log-scale X axis.
- **Title:** "One rented GPU gets cheaper than the API at about 2,700 patients"
- **X axis:** active patients (log scale). **Y axis:** US$ per patient-month (log scale).
- **Data:**

| Active patients | 1 H100 at US$2.89/h | Sonnet 5.5 API | Opus 5.5 API |
|---|---|---|---|
| 100 | 21.10 | 0.78 | 1.57 |
| 250 | 8.44 | 0.78 | 1.57 |
| 500 | 4.22 | 0.78 | 1.57 |
| 1,000 | 2.11 | 0.78 | 1.57 |
| 1,350 | 1.56 | 0.78 | 1.57 |
| 2,000 | 1.06 | 0.78 | 1.57 |
| 2,700 | 0.78 | 0.78 | 1.57 |
| 5,000 | 0.42 | 0.78 | 1.57 |
| 10,000 | 0.21 | 0.78 | 1.57 |

- **Annotations:** markers at the crossings, "≈ 1,350 (vs Opus)" and "≈ 2,700 (vs Sonnet)". Shade the region right of 2,700 lightly with the label "only if one GPU holds this load (not measured)".
- **What the reader should notice:** the GPU line is a fixed bill spread over patients; the API lines are flat. The crossing point moves if GPU capacity per patient turns out lower than one H100 for 10,000 patients.

### Chart 3 · Bar chart: sensitivity of the monthly GPU bill to the hourly rate

- **Type:** horizontal bar chart.
- **Title:** "H100 rental prices vary ±40% between providers (getdeploying.com, data dated 14 Sept 2026)"
- **X axis:** US$ per month for one H100 at 730 h. **Y axis:** listed provider rate.
- **Data:**

| Hourly rate (US$) | Source label | US$ per month (× 730 h) | Per patient at 1,000 | Break-even vs Sonnet (patients) |
|---|---|---|---|---|
| 1.78 | Lowest listed (Lium) | 1,299 | 1.30 | ≈ 1,660 |
| 2.89 | Rate used in this deck (brief, Sept 2026) | 2,110 | 2.11 | ≈ 2,700 |
| 3.19 | Runpod, on-demand, as listed 2026-10-18 | 2,329 | 2.33 | ≈ 2,970 |
| 3.49 | Highest listed (Jarvislabs) | 2,548 | 2.55 | ≈ 3,250 |

- **What the reader should notice:** the conclusion (AI is a small share of price; self-hosting pays off only in the low thousands of patients) holds across the whole listed range.

### Diagram · Where the money goes (known vs unknown)

A simple two-column block diagram. Left column "Priced (estimate)": model inference US$0.04–2.11. Right column "Not priced yet" with five boxes: clinician time, IRIS licence and hosting, Thai speech and storage, redundancy GPU, customer acquisition. An arrow labelled "likely largest" points at clinician time. No numbers on the right column.

## Numbers and claims ledger

| Claim | Value | Source | Status |
|---|---|---|---|
| Token budget per patient-day | 7,800 in + 1,050 out | `docs/pitch/faq-appendix/slides/cost.html` | estimate (not measured) |
| Sonnet 5.5 list price | US$2 in / US$10 out per M tokens | https://claude.com/pricing (opened 2026-10-18; anthropic.com/pricing redirects there) | checked |
| Opus 5.5 list price | US$4 in / US$20 out per M tokens | same | checked |
| Haiku 5.5 list price | US$0.10 in / US$0.50 out per M (≤ 100K tokens); US$0.50 / 2.50 above | same | checked (tier meaning to verify) |
| Sonnet 5.5 cache read | US$0.10 per M | same | checked |
| H100 rate used | ≈ US$2.89/h | team brief; `docs/pitch/faq-appendix/slides/sources.html` (getdeploying.com, Sept 2026) | to verify: page shows other rates today |
| H100 listed range | US$1.78 to 3.49/h; Runpod US$3.19/h; data "last updated on Sept. 14, 2026" | https://getdeploying.com/gpus/nvidia-h100-vs-nvidia-l4 (opened 2026-10-18) | checked |
| Sonnet cost per patient-month | US$0.78 | arithmetic above | estimate |
| Opus cost per patient-month | US$1.57 | arithmetic above | estimate |
| H100 per patient at 1,000 / 10,000 | US$2.11 / 0.21 | arithmetic above | estimate; capacity not measured |
| Break-even vs Sonnet / Opus | ≈ 2,700 / ≈ 1,350 patients | arithmetic above | estimate |
| Price | 499 THB a month | spec §2b; `research/pitch-claims-check.md` ("unvalidated") | hypothesis |
| Exchange rate | 35 THB per US$ | `cost.html` | assumption |
| Messages decided by rules (router v2) | 161 of 270 (59.6%) | `experiments/tool_router_v2_results_Qwen3-1.7B_cuda.json` tier counts | synthetic |
| Cached prompt prefix | 617 tokens | same, `meta.prefix_tokens_cached` | checked |
| Catalogue filter for Somchai | 100 → 67 activities | `demo/agent-flow-demo.html` (computed from RAW and LIMIT) | synthetic |
| Colab compute for all T4 runs | ≈ 0.21 units (v1 ≈ 0.14) | team brief; `experiments/RESULTS_tool_router_demo.md` | checked (v1); total from team |

## Limits and open questions

- The token budget is the foundation of every number and it is unmeasured. A one-week log of real or concierge-pilot sessions would replace it.
- GPU capacity per patient is unknown: how many concurrent chats, ASR streams and choice calls one H100 serves at an acceptable p95 latency. The 10,000-patient figure is a ceiling, not a forecast.
- Haiku-class quality on Thai chat and on the choice step is untested. A cheaper model is only cheaper if it is still safe and correct.
- The 2.89 US$/h rate in the brief does not match what the comparison page lists today (Runpod US$3.19/h). Chart 3 shows the conclusion survives either way.
- Clinician time per patient, the IRIS licence, speech compute and acquisition cost are all missing, so we cannot state a gross margin and do not.
- 499 THB is a price hypothesis with no Thai willingness-to-pay data (P19).

## Likely judge questions

1. **"Why not just call Claude for everything? It is cheaper."** At pilot size it is, by about US$1.33 per patient-month against one H100 at 1,000 patients. We self-host patient-identifying calls because of data residency under PDPA and Thai speech, and we would use an API for de-identified work. The crossover is around 2,700 patients if one GPU holds the load.
2. **"How sure are you about 7,800 tokens a day?"** Not sure; it is an estimate built from one recommendation call, two check-ins and a weekly summary share. The first pilot week will log real token counts, and the cost slide will be redone from that log.
3. **"What is your biggest cost then?"** Almost certainly clinician time, because every exercising user needs a signed limit and someone must read flags. We have not priced it and will do so with Siriraj.
4. **"Does IRIS add cost?"** Yes, a production licence and hosting, still to price with InterSystems. It also removes cost: FHIR storage, the SQL projection the rules engine reads, and vector search all live in one platform instead of three services.
5. **"Could a cheaper model run the check-ins?"** Possibly. Haiku 5.5 list prices would put the API line near US$0.04 a month, but we have not tested its Thai quality or its behaviour on our safety scenarios, so it is not in the plan yet.

## Sources

Repo files:
- `docs/pitch/faq-appendix/slides/cost.html` (token budget, original table, speaker notes)
- `docs/pitch/faq-appendix/slides/sources.html` (price sources)
- `pitch/appendix/A08-cost-structure.md`, `pitch/appendix-deck/P14-cost-structure.md`
- `experiments/tool_router_v2_results_Qwen3-1.7B_cuda.json`, `experiments/tool_router_v2_results_Qwen3-4B_cuda.json` (tier counts, cached prefix)
- `experiments/RESULTS_tool_router_demo.md` (Colab cost of v1)
- `demo/agent-flow-demo.html` (catalogue, synthetic limit record)
- `docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md` §2b (price), §5 (rules 6, 11)
- `research/pitch-claims-check.md` ("Premium from 499: unvalidated")

External (opened 2026-10-18):
- Claude API pricing: https://claude.com/pricing
- GPU prices, H100 vs L4: https://getdeploying.com/gpus/nvidia-h100-vs-nvidia-l4

## Image-generation prompt

Design one 16:9 information slide on a white background. Put the key message first as the title: "On our estimate, the AI costs about US$0.78 a patient-month; people and licences are the real cost." Make the main visual the bar chart "AI cost per patient-month (US$)" with exactly these bars: Haiku 5.5 API 0.04, Sonnet 5.5 cached 0.43 (dashed, "scenario"), Sonnet 5.5 API 0.78, Opus 5.5 API 1.57, 1 H100 at 1,000 patients 2.11, 1 H100 at 10,000 patients 0.21 (dashed, "capacity not measured"), with the note "Assumes 7,800 input + 1,050 output tokens per patient-day (not measured)". Beside it show three quoted numbers: "≈ US$14 price (499 THB, hypothesis)", "≈ 2,700 patients: GPU = Sonnet API cost", "≈ 6% AI share of price". Add a small box "Not priced yet: clinician time, IRIS licence, Thai speech, redundancy GPU, acquisition". Add a small "ESTIMATE" badge. No logos, no invented numbers, no margin or profit figures. ChatGPT chooses the design.
