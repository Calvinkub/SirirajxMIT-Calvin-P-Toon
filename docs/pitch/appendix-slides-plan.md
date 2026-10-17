# Appendix slides plan — InterSystems challenge judges

Status: **plan v0.1, 2026-10-18. Not built yet.** For team review before the slides are drafted.

## Who reads these slides

The InterSystems challenge at MIT GrandHack 2026: "Best Use of GenAI or FHIR using InterSystems technology" ([challenge page](https://developer.intersystems.com/intersystems-challenge-mit-grandhack-2026/)). Teams must use **InterSystems IRIS Vector Search**, the **InterSystems FHIR Server**, or both.

Judging criteria, verbatim: Innovation · Real-world impact · Use of InterSystems technology · Technical coherence. Their extra guidance: "clear problem in healthcare; smart use of GenAI (Vector Search) and/or FHIR; thoughtful data model and system design; realistic path to MVP or startup; clear explanation of impact."

Assumption: these slides are an appendix behind the main pitch, opened during Q&A or read after the session. Each slide must stand alone and answer one judge question.

## What changes in our architecture for this audience

Our current design has a generic "patient state store". For this challenge it becomes **InterSystems IRIS for Health**:

- **FHIR Server (R4)** holds all patient data as standard resources: watch readings, the clinician limit record, missions, symptom taps, red-flag events, consent and audit.
- **FHIR SQL Builder** projects those resources into SQL tables, which the rules-only mission engine and the weekly analytics query directly.
- **IRIS Vector Search** grounds MedGemma (RAG) over the clinician-approved content library and guideline snippets. It also powers semantic search of community activities.
- **MCP server over FHIR**: the agent reads and writes FHIR only through typed MCP tools. The InterSystems hackathon kit already uses FastMCP and LangChain.

The hackathon kit ([FHIR-AI-Hackathon-Kit](https://github.com/intersystems-community/FHIR-AI-Hackathon-Kit)) provides a Docker template of IRIS for Health with a FHIR server, `intersystems-irispython`, FHIR SQL Builder and vector-search tutorials. We build on it rather than from scratch.

## Slide list

| # | Title (the claim the slide makes) | Judge question it answers | Main visual | Criterion |
|---|---|---|---|---|
| A1 | IRIS for Health is the single source of truth between the watch, the agents and the clinician | "Where does InterSystems sit in your system?" | Layered architecture diagram, IRIS for Health in the centre | Use of InterSystems tech, technical coherence |
| A2 | Every fact the agent uses is a standard FHIR R4 resource | "Is your data model thoughtful and interoperable?" | FHIR resource map with references (table below) | Thoughtful data model |
| A3 | A daily mission is a FHIR round trip with rules before and after the model | "How does the agentic workflow actually run?" | Sequence diagram, swimlanes: Scheduler, FHIR Server, SQL Builder, Mission engine, MedGemma, Vector Search, Push | Technical coherence |
| A4 | Vector Search keeps MedGemma grounded in clinician-approved content only | "What is your smart use of GenAI?" | RAG diagram: what is embedded, the query, the grounding check | Smart use of GenAI |
| A5 | Safety and trust are written into FHIR, not just into prompts | "How do you stop the AI from harming a heart patient?" | Red-flag path plus Provenance, AuditEvent and Consent on one diagram | Real-world impact, coherence |
| A6 | Open models, each with one job | "Which models, and why these?" | Condensed model-stack table from the agentic plan | Innovation |
| A7 | From hackathon demo to hospital pilot | "Is there a realistic path to MVP?" | Roadmap with gates: demo, clinician review, usability, IRB/Thai FDA, supervised pilot, insurer pilot | Realistic path to MVP |

## A2 FHIR resource map (draft)

| Our concept | FHIR R4 resource | Key fields | Who writes it |
|---|---|---|---|
| Patient | `Patient` | demographics, language | Onboarding |
| Diagnosis, risk factors | `Condition` (post-MI), `Observation` (LVEF) | code, onset, value | Clinician (or MedGemma extraction, then clinician confirmation) |
| Discharge note | `DocumentReference` | attachment, type | Patient upload |
| Medicines, beta-blocker flag | `MedicationStatement` | medication, status | Clinician-confirmed |
| Clinician limit record | `CarePlan` + `Goal`, signed via `Provenance` | activity limits (HR ceiling, effort target, activity types), period = review-by date | Named clinician only |
| Watch data | `Observation` (vital-signs category), `Device` | heart rate (LOINC 8867-4), step count (LOINC 55423-8, to verify), effective time | Health data bridge |
| Daily mission | `Task` linked to the `CarePlan` | status (requested, completed), executionPeriod, reason codes | Mission engine (MedGemma's pick, validated) |
| Symptom tap, check-in | `QuestionnaireResponse` | answers | Patient |
| Red-flag event | `Flag` (or `DetectedIssue`) + `Communication` to the clinician | status, code, period | Red-flag rules |
| Consent | `Consent` | scope, provision (insurer access denied by default) | Patient |
| Every agent action | `AuditEvent` + `Provenance` | agent (model id + version), entity, outcome | Every node |

Open choices for the team: `Task` vs `CarePlan.activity` for missions; `Flag` vs `DetectedIssue` for red flags. LOINC codes must be checked against the official LOINC site before the slide ships.

## A3 Daily mission sequence (draft steps)

1. Scheduler fires at the patient's chosen time. No model is involved.
2. Mission engine queries FHIR SQL Builder tables: the active `CarePlan` limits, the last 7 days of heart-rate and step `Observation`s, and recent `QuestionnaireResponse`s.
3. Rules give the allowed set (mission template ids).
4. The router (Qwen3-4B) calls environment tools: heat index, PM2.5 and nearby places.
5. Vector Search returns approved explanation snippets for the candidate missions.
6. MedGemma returns `{mission_id, reason_codes}` as JSON. The validator checks it against the allowed set.
7. A FHIR `Task` is created, with a `Provenance` record naming the model and version.
8. Thai phrasing and fact check, then push to phone and watch.
9. Completion and the symptom taps write back as a `Task` status update and a `QuestionnaireResponse`.

## A4 Vector Search content (draft)

| Embedded collection | Source | Used for |
|---|---|---|
| Mission library explanations | Written by the team, approved by a clinician | Grounding MedGemma's "why this mission" text |
| Patient education snippets | Clinician-approved, each with its source | Answers to plan questions in the coach chat |
| Guideline snippets | Reconciled table (`research/guidelines/RECONCILE-for-clinician.md`), after clinician sign-off | Clinician summary references |
| Community activities | Curated, intensity-tagged list | "Find a quiet morning walk near me" semantic search |
| Discharge notes | `DocumentReference` text | Onboarding extraction support |

Grounding rule: the patient sees an answer only if it cites retrieved snippets. Otherwise the reply is a fixed "ask your care team" message. Thai search needs a multilingual embedding model (candidate: BGE-M3); its Thai retrieval quality must be tested.

## A5 Safety and trust in FHIR (draft)

- **Red-flag path:** rules only; creates a `Flag` plus a `Communication` to the clinician; coaching pauses until the clinician clears it.
- **Provenance** on every `Task`: which model, which version, which allowed set.
- **AuditEvent** for every agent turn and tool call.
- **Consent** enforced on every read by the MCP layer; insurer access off by default.
- **Clinician access:** SMART on FHIR app with scoped OAuth (to confirm what the IRIS FHIR Server supports).
- **Hospital link (later):** a discharge summary from the hospital system arrives as HL7v2 or CDA and is converted to FHIR by InterSystems transformation tools. This is listed on the challenge page as a supported pattern; not in the demo.

## Look

Same visual system as `diagramtemplate.pptx` and the backend diagram: teal ground, white panel, five column colours, Prompt font. Diagram slides use the existing backend diagram as the base for A1. Language is English, with Thai labels only where they show a Thai input.

## Honesty rules for these slides

- Mark everything not built as "planned". At this point the only built part is the Heartstep UI prototype with rules-only safety checks.
- No efficacy or readmission numbers.
- Model numbers are quoted from model cards with the source on the slide footer.

## Decisions needed before drafting

1. Is the InterSystems challenge the target (FHIR + Vector Search), or are there other GrandHack tracks too?
2. How many appendix slides do you want (7 proposed)?
3. Slides format: Claude Slides deck (exports to .pptx or PDF), or built into your .pptx template directly?
