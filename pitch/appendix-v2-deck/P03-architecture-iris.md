# P03 · IRIS for Health is the single source of truth; rules own safety, models own conversation, and agents reach data only through typed tools.

## Key message

Every fact Heartstep uses lives as a standard FHIR R4 resource in one InterSystems IRIS for Health namespace: the FHIR server holds the record, FHIR SQL Builder projects it into tables for the rules engine, and IRIS Vector Search ranks approved content and activities in the same database. Models never touch the database directly and no tool can write a clinician limit; they call typed tools, and every AI decision is written back as a FHIR `Task` with a `Provenance`. Today the FHIR data (9 bundles, 383 synthetic resources), the loader, the scripted demo and the router experiments exist; the live IRIS deployment, SQL projection, vector tables and MCP server are planned, and we say so.

## Why this matters to the judges

- **Use of InterSystems technology** (criterion 3): IRIS is not used as a vector store bolted onto a chatbot. Three IRIS for Health capabilities carry weight and share one namespace: FHIR Server (record), FHIR SQL Builder (rules input), Vector Search (grounding and ranking). Interoperability (HL7v2/CDA to FHIR) is the route into hospitals later.
- **Technical coherence** (criterion 4): one data model end to end; one direction of authority (clinician → signed limit → rules → model → patient choice → FHIR record).
- **Real-world impact:** a FHIR-native record is what a hospital can accept. A clinician, auditor or EHR can read what the AI did without trusting the AI.

## Full detail

### 1. The five layers

The backend design (`docs/diagrams/backend-architecture.dc.html`, summarised in `pitch/appendix/A02-system-architecture.md`) has five layers. Only one contains a language model.

| Layer | What it does | Model inside? | Main IRIS piece |
|---|---|---|---|
| 1. Inputs | App chat and taps, watch data (HealthKit / Health Connect), clinician limit record, discharge note, consent | No | FHIR Server (writes) |
| 2. Ingestion and safety gates | Red-flag screen, data bridge (drop implausible HR, dedupe, fix timezone), limit-record gate, eligibility gate | **No, rules only** | FHIR SQL Builder tables |
| 3. Agent harness | Coach agent with typed tools; mission engine (rules) builds the allowed set; recommender ranks | Agent yes, mission engine no | Vector Search, FHIR REST |
| 4. Output control and audit | Output filter (no drug/dose advice, no diagnosis wording, nothing above the limit), scheduler, clinician flag queue, audit | **No, rules only** | FHIR `Task`, `Provenance`, `Flag`, `Communication` |
| 5. Apps | Today screen, push mirrored to the watch, clinician web, weekly summary | No | FHIR REST (SMART on FHIR, to confirm) |

**Safe default:** with no watch data, no network, a model outage or an implausible reading, the app shows the last approved mission or a rest/light mission. Intensity never goes up (spec rule 10).

### 2. Why IRIS for Health, concretely

The InterSystems FHIR-AI Hackathon Kit runs IRIS for Health Community Edition in Docker with a FHIR R4 server. From the kit (`FHIR-AI-Hackathon-Kit/skills/iris-environment/SKILL.md` and tutorial 3.0):

| Item | Value in the kit |
|---|---|
| FHIR base URL | `http://localhost:52773/fhir/r4` |
| Capability statement | `http://localhost:52773/fhir/r4/metadata` |
| Namespace (FHIR data, SQL tables, vectors) | `FHIRSERVER` |
| Python SQL driver port (superserver) | 1972, package `intersystems-irispython` |
| FHIR storage strategy installed by the kit | `HS.FHIRServer.Storage.JsonAdvSQL.InteractionsStrategy` |
| FHIR metadata package | `hl7.fhir.r4.core@4.0.1` |
| FHIR SQL Builder portal | `/csp/fhir-management` |
| Agent / MCP pattern | LangChain `create_agent` with Python tools; FastMCP servers over streamable HTTP or stdio |

The key fact for our design is the shared namespace: the FHIR repository, the SQL projections of it and any table with a `VECTOR` column all sit in `FHIRSERVER`, so the rules engine and the ranker read the same data the clinician signed, with no copy job in between (P06, P07).

### 3. Who may write what

| Writer | May write | May never write |
|---|---|---|
| Clinician (clinician web) | `CarePlan` + `Goal` limit record, `Provenance` (attester), eligibility confirmation | — |
| Patient (app) | Goal in their own words, mission status, `QuestionnaireResponse` (fixed symptom taps), `Consent` | Limits |
| Watch bridge | `Observation` (HR, steps), `Device` | Anything else |
| Rules engine | Allowed set (in memory), `Task`, `Flag`, `Communication`, `Provenance` | Limits |
| Models (via tools) | Nothing directly. They return an id or text to the rules engine | Limits, flags, any resource |
| Curators (team, later partners) | `Location`, `HealthcareService` | Patient data |

The kit's own warning shapes this: its MCP example only allows `SELECT` statements and notes "A prefix check is not real protection. For anything beyond a local demo, connect as an IRIS user with SELECT-only privileges." We will use a read-only IRIS user for the model-facing tools and a separate service user for the rules engine.

### 4. Models: one narrow job each

| Job | Model (planned) | Why a model at all | Guard |
|---|---|---|---|
| Hear Thai/English speech | Qwen3-ASR | Older users speak more easily than type | Transcript passes the same red-flag rules |
| Route the message to a tool | Qwen3-1.7B or 4B, one-pass scoring | Free text to one of a closed list of tools | Rules decide about 60% of messages first (v2) |
| Pick one mission id / explain it | MedGemma 27B (English JSON in, JSON out) | Short explanation grounded in approved snippets | Must pick from the allowed set; validator rejects others |
| Draft fields from a discharge note | MedGemma 1.5 4B | Saves clinician typing | Clinician confirms every field |
| Rank activities and groups | No LLM: cosine KNN + IRIS Vector Search | Similarity, not generation | Runs only on the allowed set |
| Safety | **No model** | — | Rules only |

Model facts are in P10. The point here is architectural: the most important decision (is this safe?) has no model in it.

### 5. One recommendation as a round trip (Somchai)

1. App → rules: Somchai's message. Red-flag screen clear (about 0.1 ms).
2. Router (small model) → intent `build_activity_plan`, likes tennis, badminton, bowling.
3. Rules → FHIR SQL Builder tables: is there an active, unexpired, attested `CarePlan`? Read the MET limit, HR ceiling, RPE range, exclusions.
4. Rules → catalogue: 100 → 67 allowed.
5. Ranker → IRIS Vector Search / KNN: rank the 67 by taste; FHIR search for `HealthcareService` near the home district; cohort statistic.
6. Rules → app: three choices, each a reference to a FHIR `HealthcareService`.
7. Patient chooses; rules → FHIR: `PUT Task` × sessions, each `basedOn` the `CarePlan`, plus `Provenance` (assembler = the model `Device`, reason "picked-from-allowed-set").
8. Later: watch → `Observation`; app → `QuestionnaireResponse` per session; any symptom tap → `Flag` + `Communication` to the clinician.

### 6. Alternatives considered

- **Patient data in a general database, FHIR only as an export.** Rejected: two sources of truth, and the audit trail would not be in a standard a hospital can read.
- **Separate vector database.** Rejected: it would need its own copy of approved content and activity metadata and its own access control. IRIS stores `VECTOR` columns next to relational columns in the same namespace.
- **Rules inside the LLM prompt.** Rejected (P01, P12).
- **One large model doing everything.** Rejected: slower (P13: writing a tool call took a median 1,272 ms on Qwen3-1.7B versus 71 ms for one-pass scoring) and no notion of red flags.

## Visualizations

### Chart 1 · Stacked bar: what is built today versus planned, by IRIS capability

- **Type:** stacked horizontal bar, one bar per component, segments "built", "planned", "later".
- **Title:** "Built at the event: the FHIR record and the rules. Planned: the live IRIS services."

| Component | Status | Evidence |
|---|---|---|
| FHIR R4 data model + 9 transaction bundles (383 resources) | Built (synthetic) | `synthetic/fhir/*.json`, validated with `fhir.resources` R4B |
| Loader for the kit's FHIR server | Built, **not yet run against a live server (to confirm)** | `synthetic/load_to_iris.py` |
| Rules-only safety checks in the UI prototype | Built | `safety.js`, `npm test` 6/6 (A02) |
| Scripted agent-flow demo (filter, KNN, scripted FHIR calls) | Built | `demo/agent-flow-demo.html` |
| Tool-router experiments v1, v2 | Built (synthetic) | `experiments/` |
| IRIS for Health deployment with our data | Planned | — |
| FHIR SQL Builder projection (package CMC) | Planned | P06 |
| Vector tables + Thai embedding | Planned | P07 |
| MCP server over FHIR | Planned | kit 5.2 pattern |
| Clinician web, SMART on FHIR | Planned | to confirm |
| HL7v2 / CDA → FHIR interoperability | Later | — |

Chart data (counts): Built 5 · Planned 5 · Later 1. **What to notice:** the hardest-to-change part (the data model and who-writes-what) is done; the remaining work is standard IRIS configuration that the kit already demonstrates.

### Chart 2 · Bar (log scale): time per decision on the message path

- **Title:** "Rules first keeps the common path fast"
- **Axis:** milliseconds, log scale. Synthetic messages, Colab T4.

| Step | Time | Source |
|---|---|---|
| Red-flag rules (median message, v2) | ~0.1 ms (median; rules decide 60% of messages) | `experiments/RESULTS_tool_router_demo.md` v2 |
| Router, Qwen3-1.7B, one-pass scoring (v1 median) | 71 ms | same, v1 T4 table |
| Router, Qwen3-1.7B, v2 p95 | 60 ms | same, v2 table |
| Same model writing the tool call (v1 median) | 1,272 ms | same |

**Notice:** the model is only on the path when the rules cannot decide, and even then it scores a closed list instead of writing free text.

### Diagram · Three columns

Left "Edge": Heartstep app; smartwatch (HealthKit / Health Connect); clinician web; local data (OpenStreetMap places, Open-Meteo heat, Air4Thai PM2.5). Centre "InterSystems IRIS for Health, namespace FHIRSERVER": FHIR Server R4 → FHIR SQL Builder (arrow), Vector Search, Interoperability (later). Right "Agent harness": Rules engine [RULES ONLY], typed tools / MCP [read-mostly, no tool writes limits], open models [one job each]. Arrows: watch → FHIR "Observations"; clinician → FHIR "signed CarePlan + Provenance"; local data → FHIR "Location / HealthcareService"; SQL Builder → rules "SQL"; rules → models "allowed set"; models → tools "tool calls"; tools → FHIR "FHIR REST"; tools → Vector Search "SQL + vector"; rules → FHIR "Task + Provenance". No arrow from a model directly to FHIR.

## Numbers and claims ledger

| Claim | Value | Source | Status |
|---|---|---|---|
| FHIR base URL, namespace, ports | as in table | `FHIR-AI-Hackathon-Kit/skills/iris-environment/SKILL.md` | checked (kit) |
| Storage strategy and FHIR package | `JsonAdvSQL.InteractionsStrategy`, `hl7.fhir.r4.core@4.0.1` | kit tutorial 3.0 | checked (kit) |
| "A prefix check is not real protection" | quote | `skills/iris-ai-agents/SKILL.md` | checked |
| Bundles / resources / types | 9 / 383 / 19 | `synthetic/fhir/*.json` (counted with python3) | checked, synthetic |
| UI safety tests | 6/6 pass | `pitch/appendix/A02-system-architecture.md` | not re-run here, to verify |
| Rules decide share of messages | 60% | `experiments/RESULTS_tool_router_demo.md` v2 | simulated (synthetic) |
| Router median, 1.7B one-pass | 71 ms | same, v1 T4 | simulated |
| Router median, 1.7B writes call | 1,272 ms | same | simulated |
| Router p95 v2, 1.7B | 60 ms | same | simulated |
| Bundles loaded into a running IRIS | — | `pitch/appendix-deck/P02` data table | to verify (team) |
| Built / planned / later counts | 5 / 5 / 1 | this page's component list | estimate (our classification) |

## Limits and open questions

- We have not shown the bundles loading into a live IRIS for Health instance; until we do, "running on IRIS" must not be said. The loader stops on any `OperationOutcome` error, so the first run will tell us whether IRIS accepts our unprofiled extensions.
- SMART on FHIR support and scopes for the clinician web are to confirm with InterSystems mentors.
- The harness models are named but none serves real traffic; latency figures are from synthetic router tests on a Colab T4.
- `AuditEvent` (every agent turn and tool call) is designed but not generated.
- No load test or cost per user yet (P16).

## Likely judge questions

1. **"Is IRIS just your vector store?"** No. IRIS for Health holds the clinical record as FHIR, projects it to SQL for the safety rules, and stores the vectors in the same namespace, so the ranker can only see what the signed record allows.
2. **"Can the AI change a patient's limit?"** No tool writes a `CarePlan`. A "do more" request becomes a clinician flag (spec rule 4).
3. **"What runs today?"** The FHIR bundles, the loader script, the scripted demo and two router experiments. IRIS deployment, SQL Builder, vectors and MCP are planned.
4. **"Why FHIR and not your own schema?"** Because the output (plans, flags, provenance) must be readable by the hospital and auditable without our app; FHIR R4 is what IRIS for Health and hospital systems already speak.
5. **"What if the model is down?"** Safe default: last approved or a rest/light mission; intensity never increases.

## Sources

Repo:
- `pitch/appendix/A02-system-architecture.md`, `pitch/appendix-deck/P02-architecture-iris-for-health.md`, `docs/pitch/faq-appendix/slides/architecture.html`
- `docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md` §5–6
- `FHIR-AI-Hackathon-Kit/README.md`, `skills/iris-environment/SKILL.md`, `skills/iris-ai-agents/SKILL.md`, `skills/iris-fhir/SKILL.md`, `Tutorials/3-fhir/markdown/3.0-setup-fhir-server.md`
- `synthetic/load_to_iris.py`, `synthetic/fhir/*.json`
- `experiments/RESULTS_tool_router_demo.md`
- `demo/agent-flow-demo.html`

External (opened 2026-10-18):
- InterSystems IRIS documentation, "Using Vector Search" (VECTOR and EMBEDDING types stored "alongside other data in a relational table"): https://docs.intersystems.com/iris20251/csp/docbook/DocBook.UI.Page.cls?KEY=GSQL_vecsearch
- InterSystems FHIR-AI Hackathon Kit (local clone of https://github.com/intersystems-community/FHIR-AI-Hackathon-Kit)

## Image-generation prompt

Design one 16:9 information slide on a white background. Lead with the key message as the title: "IRIS for Health is the single source of truth; rules own safety, models own conversation." Make the main visual a three-column architecture diagram (Edge → InterSystems IRIS for Health with FHIR Server R4, FHIR SQL Builder and Vector Search in one namespace → Agent harness with a "rules only" safety engine, typed tools and small models), with no arrow from any model straight to the database. Beside it, a small stacked bar "Built 5 · Planned 5 · Later 1" and the quoted numbers "9 FHIR bundles · 383 synthetic resources". Label synthetic data. No logos, no invented numbers; choose the design freely.
