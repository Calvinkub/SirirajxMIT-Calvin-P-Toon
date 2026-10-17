# Likely judge questions (15)

Judges: InterSystems engineers, AI experts and clinicians. Answer in two or three sentences, then offer the appendix file. If you do not know, say so and say how you would find out.

## InterSystems and FHIR

### 1. Where exactly does InterSystems sit? Is IRIS just your vector store?
IRIS for Health is the single source of truth. The FHIR R4 server holds the patient, the clinician-signed limit record, watch observations, missions, symptom answers, red-flag events, consent and audit. FHIR SQL Builder gives the rules engine SQL tables, and Vector Search grounds the agent in approved content and ranks nearby activities.
→ [A02 System architecture](appendix/A02-system-architecture.md)

### 2. Why FHIR? Show us the data model.
The limit record is a `CarePlan` plus `Goal`, signed through `Provenance` naming the clinician. A mission is a `Task` with its own `Provenance` naming the model and the allowed set it chose from, and a red flag is a `Flag` plus a `Communication` to the clinician. Our synthetic generator builds 8 patients as FHIR R4 bundles, validated with `fhir.resources`; open choices are `Task` vs `CarePlan.activity`, and whether IRIS accepts our custom extensions without profiles.
→ [A03 FHIR data model](appendix/A03-fhir-data-model.md)

### 3. What do you embed in IRIS Vector Search, and does it work in Thai?
We embed clinician-approved guideline and education snippets, mission explanations, and an intensity-tagged list of community activities. A patient sees an explanation only if it cites a retrieved snippet; otherwise they get a fixed "ask your care team" message. The candidate multilingual embedding model is BGE-M3, and we have not tested its Thai retrieval yet.
→ [A05 Vector Search and geo](appendix/A05-intersystems-vector-search-and-geo.md)

### 4. Was the demo running against a live IRIS server?
No. The demo page is a scripted, in-browser run on synthetic data, and the trace shows the FHIR and Vector Search calls the build makes. What exists today: the synthetic FHIR bundles, a loader for the hackathon kit's IRIS FHIR server, the router experiments and the Heartstep UI prototype. [CONFIRM: say whether the bundles are loaded in IRIS, and show them if so.]
→ [A02 System architecture](appendix/A02-system-architecture.md), [A13 Roadmap](appendix/A13-roadmap-mvp.md)

### 5. How do you find real places near the patient?
Places and groups are FHIR `Location` and `HealthcareService` resources with coordinates. Rules filter them for intensity, opening time, heat and PM2.5, and then Vector Search ranks what is left against the patient's own words. No public API lists Thai community exercise groups, so v1 uses a curated list, and we still need to confirm that IRIS supports FHIR `near` search.
→ [A05 Vector Search and geo](appendix/A05-intersystems-vector-search-and-geo.md)

## Agentic AI

### 6. Why not just use ChatGPT or Claude?
We are a chat coach too, but a recommender, not a general advice bot: like Netflix, it ranks a catalogue of activities and real groups by your taste, people like you and what is near you, and only from what your doctor’s care plan allows. General models are strong reasoners; ours is also bounded. Limits come from a signed record, rules decide safety before any model runs, the app acts first instead of waiting for a question, it works in Thai, and the care team is in the loop. Health in ChatGPT also launched for US users only (OpenAI, July 2026).
→ [A01 Why not ChatGPT](appendix/A01-why-not-chatgpt.md)

### 7. What runs inside your agent harness, and why those models?
Each open model has one narrow job with typed input and output. Qwen3-ASR handles speech in, a small Qwen3 router calls MCP tools over FHIR, and MedGemma picks one mission id from the allowed set as JSON. MedGemma's model card says it is not for direct clinical decisions, which is why it only chooses from options the rules already allow.
→ [A04 Agentic harness](appendix/A04-agentic-harness.md)

### 8. Your router numbers: is 78% good enough, and is the method new?
No, 78% is not good enough, and every message in that test is synthetic. The result we stand behind is the comparison on the same 36 messages: rules plus one forward pass was 78% at 71 ms median, against 42% at 1,272 ms when Qwen3-1.7B wrote the call. Routing from a frozen model is published prior art ("The Router Within", OATS); what we add is the rules-only safety gate, allowed-set constraints and FHIR tools in a Thai clinical setting.
→ [A06 Tool-router experiments](appendix/A06-tool-router-experiments.md)

### 9. Can a prompt injection or a bad model output hurt the patient?
In our design, the model never writes free arguments. It returns a mission id, and the server checks that id against the allowed set before any FHIR `Task` is created. Red flags, medication questions and missing data are handled by rules, and any failure falls back to the last approved mission or rest. A full threat model for MCP and prompt injection is still open work.
→ [A04 Agentic harness](appendix/A04-agentic-harness.md), [A07 Safety and evaluation](appendix/A07-safety-and-evaluation.md)

### 10. Your blind test missed 4 of 30 red flags. Is that safe?
Not yet, and that is why we ran a blind test. The misses were phrasings our rules did not cover, such as a word inside "ใจเต้นรัว" or a denial of one symptom followed by a real one, and all of these are synthetic messages. Version 3 tolerates spacing and filler words, adds a model screen that can only escalate to stop, never clear, and sends any unclear message with a body-symptom word to the stop path. It will be tested on a new blind set.
→ [A07 Safety and evaluation](appendix/A07-safety-and-evaluation.md), [A06 Tool-router experiments](appendix/A06-tool-router-experiments.md)

## Clinical

### 11. Who sets the limits for patients without a CPET?
A clinician, always. Guidelines accept other sources: a stress test, a 6-minute walk, heart-rate reserve, Borg effort 11–14 and the talk test. The limit record stores who set it, the source, the date and a review-by date. With no signed record, the app shows only education and other non-exercise content, and that includes the free week.
→ [A10 Clinical evidence](appendix/A10-clinical-evidence.md)

### 12. Heart rate is blunted on beta-blockers. How can you trust it?
We don't rely on heart rate alone. Effort rating and the talk test come first during a session, and heart rate is a secondary check against the clinician's ceiling. Our research notes give conflicting beta-blocker adjustments, so we do not compute any; a rehab physician must reconcile them first.
→ [A10 Clinical evidence](appendix/A10-clinical-evidence.md)

### 13. Who is eligible? Your demo patient has hypertension.
The first version is for clinician-enrolled, guideline low-risk patients with a signed limit record. An ICD, unknown risk class, low ejection fraction, new symptoms or recent surgery blocks exercise missions and sends the patient to a clinician. Heart failure and high-risk hypertension stay out until a clinician writes their rules. The demo patient is synthetic and has a signed limit in the demo data.
→ [A07 Safety and evaluation](appendix/A07-safety-and-evaluation.md), [A10 Clinical evidence](appendix/A10-clinical-evidence.md)

## Business and regulation

### 14. Is this a medical device? What about PDPA?
We position v1 as adherence support inside clinician-set limits, not diagnosis or treatment, and we avoid the words "diagnose", "detect" and "prescription". We must check Thai FDA software-as-a-medical-device rules and have the consent flow reviewed under PDPA before any real patient. Insurer access to patient-level data is off by default, and we plan to host the system in Thailand.
→ [A12 Regulatory and PDPA](appendix/A12-regulatory-pdpa.md)

### 15. Will insurers pay, and what does it cost you to run?
We have no outcome data of our own yet. Published readmission numbers from Movn Health are vendor-reported and from the US, so we propose a pilot with adherence and safety outcomes agreed in advance. On cost, our estimate is about US$0.78 per patient-month for inference at Claude Sonnet 5.5 list prices, or about US$2.11 on one rented H100 at 1,000 patients, and our token budget is not measured yet. The larger costs are clinician sign-off time and the IRIS licence, both still to price.
→ [A11 Market and business](appendix/A11-market-and-business.md), [A08 Cost structure](appendix/A08-cost-structure.md), [A09 Speed R&D](appendix/A09-speed-rnd-katgpt.md), [A13 Roadmap](appendix/A13-roadmap-mvp.md)
