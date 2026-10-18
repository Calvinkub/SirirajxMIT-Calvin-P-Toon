# Heartstep appendix infographic prompts


## Final revision instructions

### A02

Change only these factual errors, keeping all other visual design. Built panel first bullet must read 'Patient app UI prototype (missions and symptom taps)' WITHOUT Thai voice. Built router bullet 'Router experiments v1/v2 (synthetic)' WITHOUT MCP tools. Built demo bullet 'Scripted agent-flow demo; no live IRIS'. Patient input voice label 'Thai voice (planned)'. Replace all OpenAI knot logos with generic neural-network icons. Tool panel heading 'Typed MCP tools (planned)'; remove model-direct write Task and Provenance tool icons, replace with 'Propose week plan' and 'Log check-in'; below tools state 'Rules validate and write Task + Provenance'. Add source footer 'A02-system-architecture.md'. Never say Thai voice is built.

### A03

Keep design but correct technical arrows and labels. Resource map title subtitle 'Conceptual relationships, not exact FHIR search syntax'. Replace 'hasGoal' with 'goal'. Replace QuestionnaireResponse-to-Task arrow label 'basedOn' with 'about-task extension'. Task-CarePlan arrow must point FROM Task TO CarePlan and label basedOn. Replace AI Task->Provenance arrow label wasGeneratedBy with 'target: Task' and point FROM Provenance TO Task. Clinician Provenance must link to CarePlan with label 'target: CarePlan'. Remove any link from Consent to HealthcareService; these are separate resource families. p03 outcome only 'Supervision first', remove gradual progression. Bottom notes retain all synthetic and not real model caveats.

### A05

Keep visual design, correct safety and technical details only. In red-flag screen block replace 'If urgent or outside scope, use fixed referral' with 'Symptom match: STOP path. Clear: continue retrieval'. Give symptom matches a separate red STOP branch, not the ordinary care-team referral. No-snippet fallback remains 'Please ask your care team'. Remove the entire fabricated SQL code box at lower left including LIMIT 3. Replace with clean 3-step conceptual diagram 'FHIR SQL projections' -> 'Safety filters' -> 'VECTOR_COSINE ranking'. Label panel 'Planned IRIS implementation'. Add source filename A05-intersystems-vector-search-and-geo.md at bottom. Do not claim deployment is complete.

### A06

Keep design, fix factual claims. Native latency 1272 and scoring71 bars MUST share a zero baseline and scale: 71 bar is exactly about 5.6% of 1272 bar. Zero red flags missed must have no bar. Replace bottom-left Why this matters prose with 'These experiments measure tool selection on synthetic messages. They do not demonstrate live FHIR integration or clinical safety. Rules and one-pass scoring reduce generated tokens.' Replace substring trap example with exact 'วัด (temple) matched inside จังหวัด (province)'. Escalate-only screen text 'A proposed second screen can add STOP decisions but can never reverse a rules STOP'. No invented FHIR logging in experiments.

### A07

Correct ONLY the center flow and panel evidence, preserving overall visual style and all other content. Center title 'Proposed safety flow'. Diagram: Patient input -> deterministic symptom screen. Two branches: red 'match or unclear' -> STOP + prerecorded audio + Flag/Communication + pause coaching (TERMINAL, NO arrow back to coaching). Green 'clear' -> model selects from allowed set -> rules output filter -> deliver checked message. Failure branch from validator/filter -> approved/rest default. Delete mixed numbering 4,3,1. In planned v3 box use 'Messages not stopped by rules' -> 'Second screen (planned)' with red escalate to STOP, green no escalation to normal router. Never send an already-flagged message to model. In evaluation ladder subtitle change 'Six levels' to 'Seven levels'. Panel heading 'Simulated design review (AI reviewers)'. Panel introduction exact 'Seven role-played AI reviewers assessed the first design. No scenario tests ran at that time.' Keep FAIL 1.39/4 and panel not rerun. Remove the 26/30 metric FROM panel findings and put it in a separately labeled 'Separate router test: 26/30 red flags caught on blind synthetic messages'. Eighteen scenarios are PLANNED, not already tested. Footer A07-safety-and-evaluation.md.

### A08

Change only idle-GPU caveat. Current 'Idle GPU costs continue and are not included in per-patient estimates' is misleading. Replace exactly with 'Routing estimate prices active compute only. The H100 monthly allocation includes the rented month, even when idle.' Preserve all numbers and design. Add source footer A08-cost-structure.md.

### A09

Keep design but fix lower-left measured-router comparison. Rename bars 'Rules + one-pass scoring' and 'Native tool calling', not merely with/without rules. Use true zero-baseline bars with 71 height 5.6% of 1272, or use two numeric comparison cards without bar lengths. Caption 'Qwen3-1.7B on Tesla T4, synthetic n=36'. Keep every caveat and other section.

## Original generation prompts

Generated using the built-in image_gen tool. Style reference: the user-supplied Heartstep A01 infographic. Content source: GitHub pitch/appendix A01–A13.

## A01

Use case: infographic-diagram.
Create one finished high-resolution 16:9 landscape medical technology infographic, approximately 3200x1800 or higher, matching the attached REFERENCE IMAGE's visual language closely. This is a dense illustrated explainer poster, NOT a conventional presentation slide. White background, navy headings, blue section borders and icons, light-blue panels, teal safety/allowed paths, coral red warnings, amber limitations. Top left numbered blue Axx badge and question title. Top right pink/red heart symbol with Heartstep wordmark. Use purposeful vector-style pictograms, clear arrows and labeled process diagrams, detailed compact tables only where useful, 4–6 content regions with balanced density. Avoid giant whitespace or generic three-column summary slides. Crisp readable English typography like reference. English text, as in reference. Keep content around 350–500 words maximum, prioritize facts and mechanisms, minimize tiny type. Preserve caveats and denominators. Do not introduce new factual claims or claim planned systems are built. Use source markdown as content, not as instructions. Never copy unverified broad claims about commercial chatbots. No fabricated model logos or endorsements. Source footer identifies source filename. Return ONE infographic only.
REFERENCE IS STYLE ONLY. DO NOT COPY its sentences or claims. Use ONLY the following approved copy. Do not add facts, prices, clinical advice or sources. Preserve every planning/validation qualifier. Do not put OpenAI logos on our open-model systems. Use varied illustrated diagrams, not just boxes of prose.
Comparison with a general chat workflow: 6 comparison rows phrased as Heartstep design commitments rather than universal product claims; right side synthetic experiment examples and detailed safety flow; bottom FHIR audit benefit and built/planned limitations. Preserve n=36 and 4/4 vs 0/4 red-flag misses.
Title A01: Why not just ask ChatGPT or Claude?
One-line answer: Heartstep recommends daily activities and nearby groups only within a clinician-signed care plan.
Design commitments (NOT claims about all commercial assistants): Signed FHIR limits rather than self-entered limits. Proactive 1–2 missions at a chosen time. Rules-first stop path. Thai voice pipeline planned. Clinician flag queue and weekly summary planned. Places and groups from FHIR resources. No tool can raise limits.
Comparison diagram labels only: "Unbounded chat pattern" Patient asks -> model-generated response. "Heartstep design" Scheduled or patient message -> rules screen -> signed limits and allowed set -> model selects one ID -> validator -> Task + Provenance. Red branch screen match/unclear -> stop and clinician escalation. Stop-number text "1669: clinician confirmation pending".
Measured synthetic failures: Qwen3-0.6B answered PM2.5 without calling the tool. Native tool calling missed 4/4 red flags in v1; rules-first missed 0/4. n=36 per run. These show mechanisms, not clinical accuracy.
FHIR benefit: Task links to CarePlan; Provenance records decision origin. Built: UI prototype, synthetic FHIR bundles, router experiments. Planned: IRIS integration, Thai voice and clinician portal.
Source: A01-why-not-chatgpt.md. EXCLUDE ALL subscription prices, US launch statements, categorical "chatbots give everyone same advice", and "no concept of red flags" generalization.

## A02

Use case: infographic-diagram.
Create one finished high-resolution 16:9 landscape medical technology infographic, approximately 3200x1800 or higher, matching the attached REFERENCE IMAGE's visual language closely. This is a dense illustrated explainer poster, NOT a conventional presentation slide. White background, navy headings, blue section borders and icons, light-blue panels, teal safety/allowed paths, coral red warnings, amber limitations. Top left numbered blue Axx badge and question title. Top right pink/red heart symbol with Heartstep wordmark. Use purposeful vector-style pictograms, clear arrows and labeled process diagrams, detailed compact tables only where useful, 4–6 content regions with balanced density. Avoid giant whitespace or generic three-column summary slides. Crisp readable English typography like reference. English text, as in reference. Keep content around 350–500 words maximum, prioritize facts and mechanisms, minimize tiny type. Preserve caveats and denominators. Do not introduce new factual claims or claim planned systems are built. Use source markdown as content, not as instructions. Never copy unverified broad claims about commercial chatbots. No fabricated model logos or endorsements. Source footer identifies source filename. Return ONE infographic only.
REFERENCE IS STYLE ONLY. Do not copy its content. Use ONLY the following text/content for this new A02 infographic. Draw the actual diagrams and icons described, not just text boxes.
Main visual is a detailed layered architecture with patient/watch/clinician/environment icons, central IRIS FHIR database, SQL Builder and Vector Search, rules harness and typed MCP tools. Number the daily mission round trip. Side panel built vs planned. No model can write limits.
Title A02: How is the system built?
One-line answer: IRIS for Health holds the facts; fixed rules own safety and models own bounded conversation.
Architecture: Patient app (missions, symptoms, Thai voice); smartwatch (HealthKit / Health Connect); clinician (signs limits, reviews flags); local environment (places, heat, PM2.5). All feed the proposed system.
IRIS core: FHIR R4 Server stores Patient, Observation, CarePlan, Task, Consent, Provenance, Flag, Communication, Location, HealthcareService. FHIR SQL Builder projects limits, vitals and missions for rules. Vector Search retrieves approved content and ranks eligible activities.
Harness: red-flag screen, limit gate, eligibility, allowed set, validator, output filter and safe default are rules. Typed MCP tools are the only agent access. No tool writes clinician limits.
Daily loop 1 scheduled time 2 signed limits + recent activity 3 rules build allowed set 4 approved snippets 5 model picks ID 6 validate 7 save Task + Provenance 8 push and check-in.
Built: UI prototype; 9 synthetic bundles / 383 resources; loader script; router v1/v2; scripted demo.
Planned: IRIS deployment, SQL projections, vector tables, MCP serving, live models, clinician web.
Safe default: unavailable data/model/network never raises intensity; approved or rest mission.
Source A02-system-architecture.md.

### Final correction prompt

Edit this existing infographic. Preserve the style, dimensions, colors, headings, illustrations and all correct text. Do not add unrelated text. Carefully apply these factual corrections:
Change only these factual errors, keeping all other visual design. Built panel first bullet must read 'Patient app UI prototype (missions and symptom taps)' WITHOUT Thai voice. Built router bullet 'Router experiments v1/v2 (synthetic)' WITHOUT MCP tools. Built demo bullet 'Scripted agent-flow demo; no live IRIS'. Patient input voice label 'Thai voice (planned)'. Replace all OpenAI knot logos with generic neural-network icons. Tool panel heading 'Typed MCP tools (planned)'; remove model-direct write Task and Provenance tool icons, replace with 'Propose week plan' and 'Log check-in'; below tools state 'Rules validate and write Task + Provenance'. Add source footer 'A02-system-architecture.md'. Never say Thai voice is built.

## A03

Use case: infographic-diagram.
Create one finished high-resolution 16:9 landscape medical technology infographic, approximately 3200x1800 or higher, matching the attached REFERENCE IMAGE's visual language closely. This is a dense illustrated explainer poster, NOT a conventional presentation slide. White background, navy headings, blue section borders and icons, light-blue panels, teal safety/allowed paths, coral red warnings, amber limitations. Top left numbered blue Axx badge and question title. Top right pink/red heart symbol with Heartstep wordmark. Use purposeful vector-style pictograms, clear arrows and labeled process diagrams, detailed compact tables only where useful, 4–6 content regions with balanced density. Avoid giant whitespace or generic three-column summary slides. Crisp readable English typography like reference. English text, as in reference. Keep content around 350–500 words maximum, prioritize facts and mechanisms, minimize tiny type. Preserve caveats and denominators. Do not introduce new factual claims or claim planned systems are built. Use source markdown as content, not as instructions. Never copy unverified broad claims about commercial chatbots. No fabricated model logos or endorsements. Source footer identifies source filename. Return ONE infographic only.
REFERENCE IS STYLE ONLY. Do not copy its content. Use ONLY the following text/content for this new A03 infographic. Draw the actual diagrams and icons described, not just text boxes.
Main visual is a FHIR resource relationship map, clinician-attested CarePlan to Task to AI Provenance. Show 383 resources, 9 PUT bundles, 8 synthetic patients. Compact panel of 8 patient cases, stable-ID PUT load process, terminology and validation caveats.
Title A03: Is the data model interoperable?
One-line answer: Each fact, mission and decision origin has a FHIR resource.
Big figures: 383 synthetic resources; 9 idempotent PUT bundles; 8 synthetic patient cases.
Resource map: Patient has Condition, MedicationStatement, DocumentReference, Device and Observation. Clinician Practitioner authors CarePlan linked to Goal. Clinician Provenance attests CarePlan. Task is basedOn CarePlan. AI-model Device is assembler in Task Provenance. Symptom QuestionnaireResponse links to Task. Red flag creates Flag + Communication. Consent controls access. HealthcareService links to Location.
Cases: p01 low-risk post-MI, normal missions; p02 older adult, simpler flow; p03 moderate risk, supervision first; p04 high risk, blocked; p05 post-CABG restrictions; p06 draft limits, exercise locked; p07 symptoms, later tasks cancelled; p08 AF/low adherence, adapted timing.
Loading: shared references first -> PUT Type/id transactions -> validation -> IRIS server. Stable IDs update resources rather than duplicate them.
Coding: LOINC observations; SNOMED CT conditions; ATC medications; UCUM units. Codes and custom profiles still need verification.
Caveats: all data synthetic. Validated using fhir.resources R4B; stricter IRIS validation pending. AuditEvent is planned. Synthetic AI provenance does not mean a model ran.
Source A03-fhir-data-model.md.

## A04

Use case: infographic-diagram.
Create one finished high-resolution 16:9 landscape medical technology infographic, approximately 3200x1800 or higher, matching the attached REFERENCE IMAGE's visual language closely. This is a dense illustrated explainer poster, NOT a conventional presentation slide. White background, navy headings, blue section borders and icons, light-blue panels, teal safety/allowed paths, coral red warnings, amber limitations. Top left numbered blue Axx badge and question title. Top right pink/red heart symbol with Heartstep wordmark. Use purposeful vector-style pictograms, clear arrows and labeled process diagrams, detailed compact tables only where useful, 4–6 content regions with balanced density. Avoid giant whitespace or generic three-column summary slides. Crisp readable English typography like reference. English text, as in reference. Keep content around 350–500 words maximum, prioritize facts and mechanisms, minimize tiny type. Preserve caveats and denominators. Do not introduce new factual claims or claim planned systems are built. Use source markdown as content, not as instructions. Never copy unverified broad claims about commercial chatbots. No fabricated model logos or endorsements. Source footer identifies source filename. Return ONE infographic only.
REFERENCE IS STYLE ONLY. Do not copy its content. Use ONLY the following text/content for this new A04 infographic. Draw the actual diagrams and icons described, not just text boxes.
Main visual is full rules-before-and-after agent harness with red stop branch and safe default branch. Model roles Hear/Route/Choose/Extract/Phrase/Speak with exact names, plus W1-W5 workflow strip. Mark live integration planned and demo scripted synthetic, no live IRIS.
Title A04: What runs inside the agent harness?
One-line answer: Narrow model roles are surrounded by deterministic controls.
Roles: Hear Qwen3-ASR 1.7B (Thai performance to test); route Qwen3-1.7B / 4B via one-pass scores; choose MedGemma 27B single-turn English JSON; extract discharge data MedGemma 1.5 4B with clinician confirmation; Thai phrasing Qwen3-8B or Typhoon 2 (selection pending); Thai speech Typhoon2-Audio or JaiTTS (testing pending).
Main flow: message/tap/scheduler -> red-flag rules -> router -> typed MCP reads -> signed limits + eligibility -> allowed set -> MedGemma selects mission_id -> JSON and ID validator -> output filter -> Thai fact check -> notification + Task/Provenance.
Red branch: symptom match/unclear -> fixed stop message, prerecorded audio, Flag + Communication, pause coaching. Medication questions -> fixed clinician referral. Invalid/timeout -> approved/rest default.
Tool boundary: read limits, recent activity, heat, PM2.5, places and groups. Proposed writes: propose_week_plan, schedule_notification, log_checkin. NO limit-writing tool.
W1 onboarding; W2 daily mission; W3 check-in; W4 clinician weekly review; W5 red flag.
Caveat: scripted synthetic demo, no live models or IRIS. Safety audio never generated live. Thai speech quality needs testing.
Source A04-agentic-harness.md.

## A05

Use case: infographic-diagram.
Create one finished high-resolution 16:9 landscape medical technology infographic, approximately 3200x1800 or higher, matching the attached REFERENCE IMAGE's visual language closely. This is a dense illustrated explainer poster, NOT a conventional presentation slide. White background, navy headings, blue section borders and icons, light-blue panels, teal safety/allowed paths, coral red warnings, amber limitations. Top left numbered blue Axx badge and question title. Top right pink/red heart symbol with Heartstep wordmark. Use purposeful vector-style pictograms, clear arrows and labeled process diagrams, detailed compact tables only where useful, 4–6 content regions with balanced density. Avoid giant whitespace or generic three-column summary slides. Crisp readable English typography like reference. English text, as in reference. Keep content around 350–500 words maximum, prioritize facts and mechanisms, minimize tiny type. Preserve caveats and denominators. Do not introduce new factual claims or claim planned systems are built. Use source markdown as content, not as instructions. Never copy unverified broad claims about commercial chatbots. No fabricated model logos or endorsements. Source footer identifies source filename. Return ONE infographic only.
REFERENCE IS STYLE ONLY. Do not copy its content. Use ONLY the following approved content, with correct numbers and no added claims. Do not draw OpenAI/ChatGPT logos for our open model components. Main diagram should occupy at least half the page.
Two visual tracks: retrieval grounding and nearby activity recommendation. Grounding includes approved snippets, threshold, citation check, fixed referral. Geo track district then FHIR candidates then safety filters then vector ranking then three choices. Include BGE-M3 unmeasured, near-search unconfirmed.
Title A05: How do Vector Search and local data work?
One-line answer: Rules filter the choices; retrieval grounds explanations and ranks allowed activities.
Track 1 Grounded answer: patient question -> red-flag screen -> approved collection -> relevance threshold + approval check -> answer with snippet IDs -> every claim checked -> show and audit. No suitable snippet or failed check -> fixed "Please ask your care team".
Collections: mission explanations; patient education; guidelines after clinician sign-off; curated activity descriptions. Do not embed raw patient chat or watch streams.
Track 2 Local activity: district-level position -> FHIR Location and HealthcareService -> rules filter intensity, hours, heat and PM2.5 -> semantic ranking -> up to 3 choices -> selected activity becomes Task.
IRIS implementation: SQL filters join FHIR projections with VECTOR columns; VECTOR_COSINE ranks similarity. Stored and query vectors must use the same model.
Sources: OpenStreetMap places, curated groups, weather and Air4Thai tools. Samples are synthetic: 8 locations, 7 services.
Validation: BGE-M3 Thai retrieval unmeasured; compare Recall@3 and MRR on held-out queries; tune threshold on calibration only.
Open gap: IRIS Location near-search and chained form not confirmed. SQL distance filtering is a proposed fallback.
Source A05-intersystems-vector-search-and-geo.md.

### Final correction prompt

Edit this existing infographic. Preserve the style, dimensions, colors, headings, illustrations and all correct text. Do not add unrelated text. Carefully apply these factual corrections:
Keep visual design, correct safety and technical details only. In red-flag screen block replace 'If urgent or outside scope, use fixed referral' with 'Symptom match: STOP path. Clear: continue retrieval'. Give symptom matches a separate red STOP branch, not the ordinary care-team referral. No-snippet fallback remains 'Please ask your care team'. Remove the entire fabricated SQL code box at lower left including LIMIT 3. Replace with clean 3-step conceptual diagram 'FHIR SQL projections' -> 'Safety filters' -> 'VECTOR_COSINE ranking'. Label panel 'Planned IRIS implementation'. Add source filename A05-intersystems-vector-search-and-geo.md at bottom. Do not claim deployment is complete.

## A06

Use case: infographic-diagram.
Create one finished high-resolution 16:9 landscape medical technology infographic, approximately 3200x1800 or higher, matching the attached REFERENCE IMAGE's visual language closely. This is a dense illustrated explainer poster, NOT a conventional presentation slide. White background, navy headings, blue section borders and icons, light-blue panels, teal safety/allowed paths, coral red warnings, amber limitations. Top left numbered blue Axx badge and question title. Top right pink/red heart symbol with Heartstep wordmark. Use purposeful vector-style pictograms, clear arrows and labeled process diagrams, detailed compact tables only where useful, 4–6 content regions with balanced density. Avoid giant whitespace or generic three-column summary slides. Crisp readable English typography like reference. English text, as in reference. Keep content around 350–500 words maximum, prioritize facts and mechanisms, minimize tiny type. Preserve caveats and denominators. Do not introduce new factual claims or claim planned systems are built. Use source markdown as content, not as instructions. Never copy unverified broad claims about commercial chatbots. No fabricated model logos or endorsements. Source footer identifies source filename. Return ONE infographic only.
REFERENCE IS STYLE ONLY. Do not copy its content. Use ONLY the following approved content, with correct numbers and no added claims. Do not draw OpenAI/ChatGPT logos for our open model components. Main diagram should occupy at least half the page.
Strong empirical infographic: side-by-side bar comparisons 1272 vs 71 ms median and 42% vs 78% v1 accuracy Qwen3-1.7B T4 n=36. Blind v2 n=270 panel shows both models selective accuracy, coverage, red flags 26/30. Large red 4 missed warning. Cascade diagram and v3 proposed fixes. No claim v3 already fixed failures.
Title A06: What did the router experiments measure?
One-line answer: Rules + one-pass scoring were faster on synthetic data, but blind testing exposed missed red flags.
V1 Qwen3-1.7B, Tesla T4, n=36 test messages. Native tool calling: 1272 ms median, 42% tool accuracy, 4/4 red flags missed. Rules + one-pass: 71 ms median, 78% tool accuracy, 0/4 red flags missed. About 18x faster; +36 percentage points. Make proportional bars.
V2 frozen-method blind set: 270 synthetic messages, 30 per label; 162 Thai, 63 English, 45 mixed.
Table columns model / selective accuracy / coverage / red flags caught / p95.
1.7B: 95.3% / 78.9% / 26 of 30 / 60 ms.
4B: 94.9% / 93.7% / 26 of 30 / 83 ms.
Main warning: FOUR red flags did not reach STOP. 26/30 is not an acceptable safety result.
Cascade: safety rules -> unambiguous phrase rules -> one forward pass + probe -> agree and confidence high? answer, otherwise clarify. 161/270 decisions used no model.
Failure examples: blackout missing from lexicon; Thai filler words interrupt symptom patterns; substring traps.
V3 PLAN: clinician-written lexicon, clause-scoped negation, segmentation, escalate-only second screen and NEW human-written blind set.
Synthetic results are not clinical evidence. Source A06-tool-router-experiments.md.

## A07

Use case: infographic-diagram.
Create one finished high-resolution 16:9 landscape medical technology infographic, approximately 3200x1800 or higher, matching the attached REFERENCE IMAGE's visual language closely. This is a dense illustrated explainer poster, NOT a conventional presentation slide. White background, navy headings, blue section borders and icons, light-blue panels, teal safety/allowed paths, coral red warnings, amber limitations. Top left numbered blue Axx badge and question title. Top right pink/red heart symbol with Heartstep wordmark. Use purposeful vector-style pictograms, clear arrows and labeled process diagrams, detailed compact tables only where useful, 4–6 content regions with balanced density. Avoid giant whitespace or generic three-column summary slides. Crisp readable English typography like reference. English text, as in reference. Keep content around 350–500 words maximum, prioritize facts and mechanisms, minimize tiny type. Preserve caveats and denominators. Do not introduce new factual claims or claim planned systems are built. Use source markdown as content, not as instructions. Never copy unverified broad claims about commercial chatbots. No fabricated model logos or endorsements. Source footer identifies source filename. Return ONE infographic only.
REFERENCE IS STYLE ONLY. Do not copy its content. Use ONLY the following approved content, with correct numbers and no added claims. Do not draw OpenAI/ChatGPT logos for our open model components. Main diagram should occupy at least half the page.
Defense-in-depth infographic with signed-limit gate, eligibility gate, symptom screen, allowed set, output filter, safe default. Evaluation ladder L0–L6 and 18 scenarios. Simulated panel FAIL, not clinical validation, not rerun. 26/30 red-flag recall and open clinical owner visible. v3 escalate-only second screen clearly planned.
Title A07: How is safety enforced and evaluated?
One-line answer: Clinicians set limits, rules constrain actions, and failures must lead to a safe default.
Six guardrails with icons: 1 signed current CarePlan required 2 clinician-confirmed eligibility 3 symptom screen before coaching 4 model selects only allowed IDs 5 output filter blocks dose advice and excess intensity 6 failures use approved/rest default.
STOP flow: symptom tap or text -> deterministic screen -> match or unclear -> fixed stop + prerecorded audio -> Flag/Communication -> pause coaching. Proposed v3 model second screen may only escalate; never clear a flagged message.
Evidence warning: blind synthetic router caught 26/30 red flags. Detection remains incomplete.
Evaluation ladder: L0 clinician/spec review; L1 rules properties; L2 stop-path tests; L3 adversarial agent tests; L4 bad-data fault injection; L5 Thai usability; L6 supervised pilot. 18 planned scenarios.
Simulated review panel: seven role-played AI reviewers, initial FAIL; score 1.39/4. Findings prompted signed-limit, eligibility, medication and default rules. Panel has NOT rerun and cannot approve a clinical stage gate.
Open items: named clinical owner; signed Thai phrase list; clinician-reviewed values; complete scenario suite.
No patient safety validation claimed. Source A07-safety-and-evaluation.md.

### Final correction prompt

Edit this existing infographic. Preserve the style, dimensions, colors, headings, illustrations and all correct text. Do not add unrelated text. Carefully apply these factual corrections:
Correct ONLY the center flow and panel evidence, preserving overall visual style and all other content. Center title 'Proposed safety flow'. Diagram: Patient input -> deterministic symptom screen. Two branches: red 'match or unclear' -> STOP + prerecorded audio + Flag/Communication + pause coaching (TERMINAL, NO arrow back to coaching). Green 'clear' -> model selects from allowed set -> rules output filter -> deliver checked message. Failure branch from validator/filter -> approved/rest default. Delete mixed numbering 4,3,1. In planned v3 box use 'Messages not stopped by rules' -> 'Second screen (planned)' with red escalate to STOP, green no escalation to normal router. Never send an already-flagged message to model. In evaluation ladder subtitle change 'Six levels' to 'Seven levels'. Panel heading 'Simulated design review (AI reviewers)'. Panel introduction exact 'Seven role-played AI reviewers assessed the first design. No scenario tests ran at that time.' Keep FAIL 1.39/4 and panel not rerun. Remove the 26/30 metric FROM panel findings and put it in a separately labeled 'Separate router test: 26/30 red flags caught on blind synthetic messages'. Eighteen scenarios are PLANNED, not already tested. Footer A07-safety-and-evaluation.md.

## A08

Use case: infographic-diagram.
Create one finished high-resolution 16:9 landscape medical technology infographic, approximately 3200x1800 or higher, matching the attached REFERENCE IMAGE's visual language closely. This is a dense illustrated explainer poster, NOT a conventional presentation slide. White background, navy headings, blue section borders and icons, light-blue panels, teal safety/allowed paths, coral red warnings, amber limitations. Top left numbered blue Axx badge and question title. Top right pink/red heart symbol with Heartstep wordmark. Use purposeful vector-style pictograms, clear arrows and labeled process diagrams, detailed compact tables only where useful, 4–6 content regions with balanced density. Avoid giant whitespace or generic three-column summary slides. Crisp readable English typography like reference. English text, as in reference. Keep content around 350–500 words maximum, prioritize facts and mechanisms, minimize tiny type. Preserve caveats and denominators. Do not introduce new factual claims or claim planned systems are built. Use source markdown as content, not as instructions. Never copy unverified broad claims about commercial chatbots. No fabricated model logos or endorsements. Source footer identifies source filename. Return ONE infographic only.
REFERENCE IS STYLE ONLY. Use ONLY approved text below, not reference content. Do not invent code, numbers, facts, logos, claims or sources. Use large clear diagrams and charts with icons. No additional statements. All qualifiers mandatory.
Cost infographic with estimated routing GPU time, monthly price hypothesis and full cost layers. Use only source T4/H100 assumptions and arithmetic, avoid commercial API model price comparisons that are unverified. 0.19 THB per 1000 messages with 404x71ms, T4 $0.69/h, FX 33.7; H100 $3.19/h $2329/mo, $2.33/patient at 1000, $0.78 at 3000, $0.23 at 10000 conditional capacity. 499 THB proposed price. Clinician/IRIS/voice unpriced. Source estimates not validated invoices.
Title A08: What does it cost?
One-line answer: Routing compute is small in the model; full service costs remain unpriced.
Large estimates: THB 0.19 per 1000 routing messages; THB 499 proposed monthly patient price; USD 2.33 H100 cost per patient-month at 1000 patients.
Routing visual: 1000 messages -> 596 rule decisions / 404 model passes -> 404 x 71 ms = about 29 GPU-seconds -> USD 0.0055 = about THB 0.19.
Inputs: measured synthetic latency, T4 USD 0.69/hour, assumed FX 33.7 THB/USD. This prices active compute, not a full always-on bill.
H100 scale chart: USD 3.19/hour; approx USD 2329/month. At 1000 patients USD 2.33 each; 3000 USD 0.78; 10000 USD 0.23. Last scenario only if one GPU can support demand; capacity not measured.
Workload budget: 7800 input + 1050 output tokens per patient-day, an unmeasured estimate.
Cost iceberg: estimated inference above water; clinician review, IRIS licence, Thai speech, support, acquisition and backup capacity still unpriced.
Limits: single-stream synthetic benchmarks; idle GPU costs continue; token budget unmeasured; source pricing dated 18 Oct 2026 and must be rechecked.
No competitor subscription or API pricing in this image.
Source A08-cost-structure.md.

## A09

Use case: infographic-diagram.
Create one finished high-resolution 16:9 landscape medical technology infographic, approximately 3200x1800 or higher, matching the attached REFERENCE IMAGE's visual language closely. This is a dense illustrated explainer poster, NOT a conventional presentation slide. White background, navy headings, blue section borders and icons, light-blue panels, teal safety/allowed paths, coral red warnings, amber limitations. Top left numbered blue Axx badge and question title. Top right pink/red heart symbol with Heartstep wordmark. Use purposeful vector-style pictograms, clear arrows and labeled process diagrams, detailed compact tables only where useful, 4–6 content regions with balanced density. Avoid giant whitespace or generic three-column summary slides. Crisp readable English typography like reference. English text, as in reference. Keep content around 350–500 words maximum, prioritize facts and mechanisms, minimize tiny type. Preserve caveats and denominators. Do not introduce new factual claims or claim planned systems are built. Use source markdown as content, not as instructions. Never copy unverified broad claims about commercial chatbots. No fabricated model logos or endorsements. Source footer identifies source filename. Return ONE infographic only.
REFERENCE IS STYLE ONLY. Use ONLY approved text below, not reference content. Do not invent code, numbers, facts, logos, claims or sources. Use large clear diagrams and charts with icons. No additional statements. All qualifiers mandatory.
R&D infographic main 4-step draft/prune/tree/verify pipeline using schema + allowed mission IDs. Three benchmark arms and metrics. Distinguish measured router gains from unmeasured MedGemma. katgpt-rs modelless micro-model evidence only. No MedGemma speed claim.
Title A09: Can decoding run faster and cheaper?
One-line answer: The allowed-set safety constraint may also reduce wasted decoding. This is an R&D hypothesis.
Main pipeline: 1 Draft small Gemma 3 proposes tokens 2 ConstraintPruner removes schema-invalid and disallowed mission tokens 3 DDTree builds valid continuation tree 4 MedGemma verifies tree.
Example JSON: {"mission_id":"walk-10-easy","reason_codes":["keep-level"]}. Constraints: valid schema + ID in today's allowed set.
katgpt-rs: team Rust library of decoding primitives, modelless. Micro-model/constraint-puzzle results do NOT transfer to MedGemma.
Benchmark: Arm 1 vLLM guided JSON; Arm 2 + standard speculative decoding; Arm 3 + schema and allowed-set tree pruning. Same GPU and request set for all.
Metrics for ALL arms: p95 latency, valid-output rate, mission-choice agreement, cost per 1000 patient-days. Pruning-off check must reproduce arm 2.
Measured separately: router 71 vs 1272 ms median on synthetic Qwen3-1.7B T4, n=36.
Unmeasured: MedGemma speed, argument filling, capability masks, production throughput.
Hypothesis: at least 3x median speed with tool accuracy no more than 1 point lower. Reject if speed or accuracy fails.
Source A09-speed-rnd-katgpt.md.

## A10

Use case: infographic-diagram.
Create one finished high-resolution 16:9 landscape medical technology infographic, approximately 3200x1800 or higher, matching the attached REFERENCE IMAGE's visual language closely. This is a dense illustrated explainer poster, NOT a conventional presentation slide. White background, navy headings, blue section borders and icons, light-blue panels, teal safety/allowed paths, coral red warnings, amber limitations. Top left numbered blue Axx badge and question title. Top right pink/red heart symbol with Heartstep wordmark. Use purposeful vector-style pictograms, clear arrows and labeled process diagrams, detailed compact tables only where useful, 4–6 content regions with balanced density. Avoid giant whitespace or generic three-column summary slides. Crisp readable English typography like reference. English text, as in reference. Keep content around 350–500 words maximum, prioritize facts and mechanisms, minimize tiny type. Preserve caveats and denominators. Do not introduce new factual claims or claim planned systems are built. Use source markdown as content, not as instructions. Never copy unverified broad claims about commercial chatbots. No fabricated model logos or endorsements. Source footer identifies source filename. Return ONE infographic only.
REFERENCE IS STYLE ONLY. Use ONLY approved text below, not reference content. Do not invent code, numbers, facts, logos, claims or sources. Use large clear diagrams and charts with icons. No additional statements. All qualifiers mandatory.
Clinical evidence infographic with clinician-owned limit workflow, CPET/ECG/6MWT source options, risk gate, 12 unresolved clinical questions grouped visually. Do not give unverified clinical numerical prescriptions as recommendations. Clear machine-generated research, primary guideline verification pending, no efficacy data. Proposed low-risk post-MI v1 walking only.
Title A10: What is the clinical basis?
One-line answer: A clinician sets the limit and risk class; the app follows that record.
Evidence status: first-pass machine-generated research from 55 sources. Primary guidelines not yet checked. NO app efficacy evidence.
Limit-source map: CPET / symptom-limited ECG test / 6-minute walk assessment -> clinician interpretation -> signed CarePlan + source/date/review-by -> allowed walking missions.
Risk gate: clinician-confirmed low risk -> proposed v1; moderate risk -> supervision first; high or unknown -> block and refer.
Twelve reconciliation topics grouped: intensity and beta-blockers; resistance timing and talk test; risk bands, METs and ICD; session length and progression; home stop rules and Thai heat; interpretation of home-rehab safety evidence.
Do not implement unreviewed numeric thresholds. Show a prominent "12 open clinical questions" marker.
Proposed v1: low-risk post-MI only; walking with warm-up/cool-down; clinician ceiling with perceived effort/talk test; no resistance training or automatic HR-reserve calculation.
Human review: cardiologist owns limits and Thai symptom list; rehab physician reconciles exercise parameters; pharmacist reviews reminder text; nurse checks older-adult comprehension.
Research values remain frozen until signed review.
Source A10-clinical-evidence.md.

## A11

Use case: infographic-diagram.
Create one finished high-resolution 16:9 landscape medical technology infographic, approximately 3200x1800 or higher, matching the attached REFERENCE IMAGE's visual language closely. This is a dense illustrated explainer poster, NOT a conventional presentation slide. White background, navy headings, blue section borders and icons, light-blue panels, teal safety/allowed paths, coral red warnings, amber limitations. Top left numbered blue Axx badge and question title. Top right pink/red heart symbol with Heartstep wordmark. Use purposeful vector-style pictograms, clear arrows and labeled process diagrams, detailed compact tables only where useful, 4–6 content regions with balanced density. Avoid giant whitespace or generic three-column summary slides. Crisp readable English typography like reference. English text, as in reference. Keep content around 350–500 words maximum, prioritize facts and mechanisms, minimize tiny type. Preserve caveats and denominators. Do not introduce new factual claims or claim planned systems are built. Use source markdown as content, not as instructions. Never copy unverified broad claims about commercial chatbots. No fabricated model logos or endorsements. Source footer identifies source filename. Return ONE infographic only.
REFERENCE IS STYLE ONLY. DO NOT COPY its sentences or claims. Use ONLY the following approved copy. Do not add facts, prices, clinical advice or sources. Preserve every planning/validation qualifier. Do not put OpenAI logos on our open-model systems. Use varied illustrated diagrams, not just boxes of prose.
Business infographic with B2B2C insurer and B2C patient/family payment flows, hospital clinician enrollment. 499 THB price hypothesis, competitors Movn/Cardihab/EXPERT with roles not performance claims. Validation funnel interviews to ethics-reviewed concierge pilot 8–10. No insurer contacted, willingness to pay unvalidated, no outcome claims.
Title A11: Who pays, and who else does this?
One-line answer: An insurer benefit and self-pay subscription are two hypotheses to validate.
Flow A B2B2C: private insurer -> negotiated per-member fee -> Heartstep -> rehab benefit -> clinician-enrolled patient. Aggregate reporting only if permitted; patient-level insurer access off by default.
Flow B B2C: patient or family -> freemium / proposed Premium from THB 499 per month -> daily missions.
Hospital/clinician enables both: enrollment and signed limits.
Prior art map: Movn Health, US, clinician-led virtual rehab; Cardihab, Australia, hybrid/remote rehab; EAPC EXPERT, Europe, clinician prescription decision support. Proposed differentiation: Thai daily missions inside signed limits, deterministic controls and FHIR records.
Validation funnel: 3–5 insurer interviews -> 3–5 patient interviews -> ethics-reviewed concierge pilot with 8–10 clinician-enrolled patients -> willingness-to-pay test.
Unknowns: no insurer contacted; no Thai pricing evidence; clinician time and IRIS licensing unpriced; no verified market size.
Do not claim app reduces readmissions. No vendor performance claims. No proof of competitor absence.
Source A11-market-and-business.md.

## A12

Use case: infographic-diagram.
Create one finished high-resolution 16:9 landscape medical technology infographic, approximately 3200x1800 or higher, matching the attached REFERENCE IMAGE's visual language closely. This is a dense illustrated explainer poster, NOT a conventional presentation slide. White background, navy headings, blue section borders and icons, light-blue panels, teal safety/allowed paths, coral red warnings, amber limitations. Top left numbered blue Axx badge and question title. Top right pink/red heart symbol with Heartstep wordmark. Use purposeful vector-style pictograms, clear arrows and labeled process diagrams, detailed compact tables only where useful, 4–6 content regions with balanced density. Avoid giant whitespace or generic three-column summary slides. Crisp readable English typography like reference. English text, as in reference. Keep content around 350–500 words maximum, prioritize facts and mechanisms, minimize tiny type. Preserve caveats and denominators. Do not introduce new factual claims or claim planned systems are built. Use source markdown as content, not as instructions. Never copy unverified broad claims about commercial chatbots. No fabricated model logos or endorsements. Source footer identifies source filename. Return ONE infographic only.
REFERENCE IS STYLE ONLY. DO NOT COPY its sentences or claims. Use ONLY the following approved copy. Do not add facts, prices, clinical advice or sources. Preserve every planning/validation qualifier. Do not put OpenAI logos on our open-model systems. Use varied illustrated diagrams, not just boxes of prose.
Regulatory/privacy infographic with intended-use boundary, open Thai FDA SaMD classification, five separate consents flowing into FHIR Consent then per-read MCP checks. Insurer off by default; district only, approved retrieval collections, Thailand hosting planned. Accountability map CarePlan/Task/Provenance/AuditEvent/Flag. All legal review pending.
Title A12: Is it a medical device? What about PDPA?
One-line answer: Adherence-support positioning does not settle the Thai FDA question. Written review is required.
Intended use draft: help clinician-enrolled adults after MI follow signed exercise limits through daily activities and reminders.
Feature review: choosing allowed activities; fixed symptom stop messages; discharge-note extraction; clinician-reviewed progression proposals; eligibility blocking. Thai FDA SaMD classification remains OPEN.
Five consent streams: 1 app and clinician care 2 wearable import 3 AI processing/location 4 optional caregiver summary 5 insurer aggregate sharing OFF by default. Flow to FHIR Consent -> MCP checks every read -> IRIS. These are proposed controls.
Data minimization: district-level location; no raw chat/watch streams in vector index; Thailand hosting planned; no insurer underwriting use in design.
Accountability: clinician limit -> CarePlan + attester Provenance; mission choice -> Task + assembler Provenance; tool access -> AuditEvent planned; red flag -> Flag + Communication.
Review before patient use: regulatory lawyer/Thai FDA; privacy lawyer or DPO for basis, roles, transfers, retention; insurance adviser for sharing; hospital IRB; named clinical owner and incident route.
No legal compliance or approval claimed.
Source A12-regulatory-pdpa.md.

## A13

Use case: infographic-diagram.
Create one finished high-resolution 16:9 landscape medical technology infographic, approximately 3200x1800 or higher, matching the attached REFERENCE IMAGE's visual language closely. This is a dense illustrated explainer poster, NOT a conventional presentation slide. White background, navy headings, blue section borders and icons, light-blue panels, teal safety/allowed paths, coral red warnings, amber limitations. Top left numbered blue Axx badge and question title. Top right pink/red heart symbol with Heartstep wordmark. Use purposeful vector-style pictograms, clear arrows and labeled process diagrams, detailed compact tables only where useful, 4–6 content regions with balanced density. Avoid giant whitespace or generic three-column summary slides. Crisp readable English typography like reference. English text, as in reference. Keep content around 350–500 words maximum, prioritize facts and mechanisms, minimize tiny type. Preserve caveats and denominators. Do not introduce new factual claims or claim planned systems are built. Use source markdown as content, not as instructions. Never copy unverified broad claims about commercial chatbots. No fabricated model logos or endorsements. Source footer identifies source filename. Return ONE infographic only.
REFERENCE IS STYLE ONLY. DO NOT COPY its sentences or claims. Use ONLY the following approved copy. Do not add facts, prices, clinical advice or sources. Preserve every planning/validation qualifier. Do not put OpenAI logos on our open-model systems. Use varied illustrated diagrams, not just boxes of prose.
Roadmap infographic main six stage gates G-A to G-F with owners and exit conditions. Detailed prototype to clinical review to usability >=8 to IRB/FDA/PDPA to supervised low-risk pilot to insurer matched-outcomes pilot. Lower MVP in/out and next engineering steps. Current prototype, no clinical owner yet, all later gates unpassed.
Title A13: Is there a realistic path to an MVP?
One-line answer: Six gates, each approved by accountable people, separate the demo from patient deployment.
Main roadmap with six connected gates:
G-A Prototype: property and stop-path tests; 18 scenarios; no open critical finding. Owner team. IN PROGRESS.
G-B Clinical review: written approval of limits, stop rules and Thai lexicon. Owner cardiologist + rehab physician. Owner not yet named.
G-C Usability: at least 8 target-age Thai users complete onboarding and a week of missions without severe issues. Owner usability lead + cardiac nurse.
G-D Ethics/regulatory: IRB decision, written Thai FDA classification, PDPA review. Owner IRB and legal/privacy reviewers.
G-E Supervised pilot: low-risk cohort, weekly safety review, predefined pause rules. Owner clinician + statistician.
G-F Insurer pilot: pre-registered completion/readmission outcomes, matched comparison. Owner insurer + statistician.
MVP IN: clinician-confirmed low-risk post-MI; walking; fixed medication reminders; Thai text; symptom tap; FHIR.
MVP OUT: unsupervised high/moderate risk; resistance training; HRR calculation; free-text peer groups; patient-level insurer data.
Engineering next: load 9 FHIR bundles -> SQL rules -> test suite -> approved-content retrieval -> MCP -> new blind router test -> bounded model serving.
Critical path: named clinician, lawyer, IRB. No patient or insurer pilot started.
Source A13-roadmap-mvp.md.
