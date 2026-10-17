# Q&A appendix deck · Heartstep (CVD Mission Coach) · Calvin, P, Toon

MIT GrandHack 2026 · InterSystems challenge "Best Use of GenAI or FHIR using InterSystems technology" (Innovation · Real-world impact · Use of InterSystems technology · Technical coherence).

20 slide specs, one per file. Each file is self-contained: it opens with an **image-generation prompt** (paste the whole fenced block into ChatGPT image generation to render a 1920×1080 slide), then the exact on-slide text, the visual spec, speaker notes for Q&A, the data each number depends on, and the repo sources. The detailed answers behind these pages are in [`../appendix/`](../appendix/) (A01–A13); these pages reuse their facts.

- Structure learned from the team's earlier deck: [TEMPLATE-ANALYSIS.md](TEMPLATE-ANALYSIS.md)
- Shared look (palette, fonts, icons, frame, badges): [STYLE-GUIDE.md](STYLE-GUIDE.md)

**Read first.** All patient data is **synthetic**. The review panel is **simulated** (language-model reviewers). Costs are **estimates** on an unmeasured token budget. The agent demo is **scripted in the browser**, not a live IRIS run. The AI never sets an exercise limit; red flags are handled by rules only.

## Index

| Page | Judge question it answers | Page type (template slide) | Data on the page |
|---|---|---|---|
| [P01](P01-why-not-chatgpt.md) | Why not just ask ChatGPT or Claude? | Variant perception (12) | Red flags missed 4 of 4 (model writes call) vs 0 of 4 (rules first); PM2.5 invented answer; n = 36 synthetic |
| [P02](P02-architecture-iris-for-health.md) | Where does InterSystems sit? Is IRIS just a vector store? | Stack + value chain (8, 16) | FHIR Server, SQL Builder, Vector Search, Interop; built vs planned badges |
| [P03](P03-fhir-resource-map.md) | Why FHIR? Show the data model | Column map (2) | 19 resource types, 383 resources, 9 PUT bundles; LOINC 8867-4, 41950-7, 18842-5; SNOMED CT, ATC; Consent insurer deny |
| [P04](P04-synthetic-fhir-bundles.md) | What data did you build, what does it test? | KPI snapshot (3) | 8 patients; per-bundle counts 20/52/50/51/29/52/28/52/49; 143 Observations; 8 test paths |
| [P05](P05-fhir-sql-builder.md) | How does the rules engine read FHIR? | Value-chain flow + table (16, 4) | SQL Builder 5 steps; 6 proposed CMC tables; Gate 1 query; "no row = no exercise" |
| [P06](P06-vector-search-grounding.md) | What do you embed? How do you stay grounded? Thai? | Two-panel chart (13) | 4 ESC 2020 §4.2.3 lines (paraphrased); 100 activities, 44 with 2024 Compendium code, 56 estimates; 5.9 MET demo limit; grounding rule |
| [P07](P07-geospatial-community-search.md) | How do you find places and groups near home? | Value-chain flow + table (16, 7) | 5-step geo flow; 8 Locations, 7 HealthcareServices (synthetic); near-search call; data sources |
| [P08](P08-agent-harness-models.md) | What runs in the harness, why those models? | Matrix (7) | 7 jobs × model; MedQA 85.3 / 69.1 (cards); Qwen3 119 languages; Qwen3-TTS 10 languages, no Thai |
| [P09](P09-agent-flow-8-steps.md) | Walk us through what the agent does | Timeline + callout (8, 11) | 8 steps with tech tags; 100 → 67 activities; ≤ 5.9 METs, HR < 120, RPE 11–13; football out, walking golf in |
| [P10](P10-safety-by-construction.md) | How do you stop the AI harming a patient? | Matrix + flow (7) | Rules-only red-flag flow, fail closed; gates G1–G6 status from simulated panel and fixes |
| [P11](P11-tool-router-v1.md) | Did you measure anything? | Event KPI tiles + bar chart (19, 20, 3) | 71 vs 1,272 ms; 78% vs 42%; 0 vs 4 red flags missed; A/B/C/D bars; A → C at 0.6B, 1.7B, 4B |
| [P12](P12-tool-router-v2-blind.md) | You missed 4 of 30 red flags. Is that safe? | Miss vs beat tiles (19) | 95.3% / 94.9% selective accuracy; 78.9% / 93.7% coverage; 161 of 270 by rules; 26/30 red flags; 3 error cases; v3 fixes |
| [P13](P13-evaluation-and-review-panel.md) | How do you evaluate it? Who reviewed it? | Four numbered panels (17) | Layers L0–L6; panel FAIL 1.39 / 4, 7 of 7 FAIL, 0 of 18 scenarios; 5 S0 fixes; rule of three ≈ 14% |
| [P14](P14-cost-structure.md) | What does the AI cost per patient? | Chart + tiles (13) | US$0.78 / 1.57 / 2.11 / 0.21 per patient-month; ≈ US$14 price; ≈ 2,700 break-even; ≈ 6% share; excluded costs |
| [P15](P15-speed-rnd-katgpt.md) | Can it run faster and cheaper? | Evolution flow + matrix (11, 7) | Draft → Prune → Tree → Verify; 3 benchmark arms; cascade T0–T4 measured yes/no; "no MedGemma number yet" |
| [P16](P16-clinical-evidence.md) | What is the clinical basis? No CPET? Beta-blockers? | Matrix (7) | 6 limit sources with synthetic patients; 4 risk classes; 12 contradictions; beta-blocker rule |
| [P17](P17-market-and-business.md) | Who pays? Who else does this? | Segment cards + why (9) | Insurer / patient / hospital routes; 499 THB; 10 days, 12.5%, 83.3% (to verify); Movn, Cardihab, EXPERT; gaps |
| [P18](P18-regulatory-pdpa.md) | Is it a medical device? PDPA? | Three-pillar columns (4, 5) | Wording do/avoid; 4 SaMD features → design; 5 consents, insurer OFF; lawyer list |
| [P19](P19-roadmap-to-pilot.md) | Is there a realistic path to a pilot? | Timeline + stack (8) | Gates G-A to G-F with owners and status; 9 engineering steps; MVP in/out |
| [P20](P20-team-built-vs-reused.md) | What did you build vs reuse? Who are you? | Column map (2, 1) | Built / reused / planned lists; 6/6 UI tests; the ask; team roles (to fill) |

Page-type mix (mirrors the template's mix): 2 variant-perception/argument pages, 4 matrix pages, 5 flow/timeline pages, 4 KPI/number pages, 3 chart pages, 2 column maps. No divider pages: in Q&A each page is opened on its own.

## Data gaps that block or weaken a page

| Gap | Pages affected | Owner / how to close |
|---|---|---|
| Are the 9 bundles loaded and accepted by the kit's IRIS FHIR server (custom extensions)? | P02, P04, P19, P20 | Run `synthetic/load_to_iris.py`; until then say "designed for IRIS" |
| Does SQL Builder project custom and repeating extensions? | P05 | Test on IRIS or ask InterSystems mentors |
| Does IRIS FHIR support `near` / chained `location.near`? | P07 | Check `/fhir/r4/metadata` or ask mentors |
| Thai embedding quality (BGE-M3), score threshold | P06 | Run the A05 test plan on a blind set |
| Team roles | P20 | Team fills `[ROLE]` (and `[NAME]` in `pitch/README.md`) |
| Named clinical owner; clinician-signed red-flag phrase list; 1669 confirmation | P10, P13, P16, P19 | Siriraj mentor |
| Primary-source check of guideline numbers and Thai statistics (10 days, 12.5%, 83.3%, ESC 2020 lines, Compendium METs) | P06, P09, P16, P17 | Open primary guidelines and studies |
| Insurer fee, Thai willingness to pay, market size | P17 | 3–5 insurer and patient interviews |
| Measured token budget, GPU capacity per patient, clinician time, IRIS licence price | P14 | Pilot logging; quotes from Siriraj and InterSystems |
| MedGemma speed benchmark | P15 | Run the 3-arm benchmark |
| Router v3 + new human-written blind set | P12 | Build v3; write ≥ 300 new messages |
| Scenario suite SC-01…18, panel re-run | P13 | Build L1/L2 tests; re-run panel |
| Legal review (Thai FDA, PDPA, OIC), IRB | P18 | Regulatory and privacy lawyers, hospital IRB |

## Consistency notes for the team

- **Demo catalogue:** the current `demo/agent-flow-demo.html` has 100 activities and keeps 67 (counted 2026-10-18). `pitch/appendix/A04` still says 99 → 66; `main-3min.md` already says 100 → 67. Update A04 before Q&A.
- **Compendium codes:** the demo footer says "about 40" activities use 2024 Compendium codes; the file has 44 (one marked "closest listed").
- **"Rules engine built":** the 3-minute tech slide says the rules engine was built here; what exists is the UI rules (`safety.js`) and the router rules. P20 uses the narrower wording.
- **Doctor statistic:** A10 says to use neither the 81%/11% nor 93%/15% figure; `pitch/README.md` says PMC12990137 was checked and supports 93%/15% (Italian GPs). No appendix-deck page uses either figure.
- **Rendering:** image models misspell long text. Check every rendered slide against the "On-slide text (exact)" section, and fix text in an editor if needed. Thai script is kept off the slides on purpose.
