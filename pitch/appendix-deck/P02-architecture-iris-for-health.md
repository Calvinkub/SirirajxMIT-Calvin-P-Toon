# P02 · Where does InterSystems sit? How is it built?

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "IRIS + FHIR". PAGE TAG: "A02".

BREADCRUMB: "IRIS + FHIR | SYSTEM ARCHITECTURE"
TITLE: "IRIS for Health is the single source of truth; agents reach it only through typed tools."

LAYOUT: a three-column architecture diagram from y=180 to y=840, then a takeaway strip, then the footer.

LEFT COLUMN "Edge" (x=80 to x=470). Column header "Edge" 24 px grey. Four stacked rounded boxes, each with a small lineal-colour icon on the left:
  "Heartstep app" (phone icon) – second line "missions · symptom tap · Thai voice"
  "Smartwatch" (watch icon) – second line "HealthKit / Health Connect"
  "Clinician web" (doctor icon) – second line "signs limits · reviews flags"
  "Local data" (map-pin icon) – second line "places · heat · PM2.5"

CENTRE COLUMN (x=560 to x=1260): one large rounded box with a 3 px teal #1B7F7A border and pale teal header band reading "InterSystems IRIS for Health". Inside it, four sub-boxes stacked:
  "FHIR Server R4" – second line "every fact as a standard resource" – small badge "BUILT: synthetic bundles"
  "FHIR SQL Builder" – second line "tables for the rules engine" – small grey dashed badge "PLANNED"
  "Vector Search" – second line "approved text + activity ranking" – small grey dashed badge "PLANNED"
  "Interoperability" – second line "HL7v2 / CDA → FHIR" – small grey dashed badge "LATER"
  A thin teal arrow from "FHIR Server R4" down to "FHIR SQL Builder".

RIGHT COLUMN "Agent harness" (x=1350 to x=1840). Column header "Agent harness". Three stacked rounded boxes:
  "Rules engine" with a teal badge "RULES ONLY" – second line "red flags · limit gate · allowed set · output filter"
  "MCP server" – second line "typed tools · no tool writes limits"
  "Open models" with a grey badge "MODEL" – second line "one job each"

ARROWS (teal, each with a small label):
  Smartwatch → FHIR Server R4: "Observations"
  Clinician web → FHIR Server R4: "signed CarePlan + Provenance"
  Local data → FHIR Server R4: "Location / HealthcareService"
  FHIR SQL Builder → Rules engine: "SQL"
  Rules engine → Open models: "allowed set"
  Open models → MCP server: "tool calls"
  MCP server → FHIR Server R4: "FHIR REST"
  MCP server → Vector Search: "SQL + vector"
  Rules engine → FHIR Server R4: "Task + Provenance"
  Heartstep app → Rules engine: "taps, check-ins"

TAKEAWAY STRIP (pale teal, y=870 to y=940): "Rules engine owns safety. Agent owns conversation. No tool can write a limit."

FOOTER: "Source: docs/diagrams/backend-architecture.dc.html; pitch/appendix/A02; FHIR-AI-Hackathon-Kit (IRIS for Health Docker)"

DO NOT: draw the InterSystems logo or any vendor logo; add boxes not listed; add numbers; add cloud-provider icons.
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "Where exactly does InterSystems sit? Is IRIS just your vector store?" |
| Page type | Stack + value-chain diagram (mirrors template slide 8 architecture stack and slide 16 value chain with "new" vs "existing" brackets; here "built" vs "planned" badges) |
| Layout | Three columns: edge → IRIS for Health → agent harness, labelled arrows, takeaway strip |
| On-slide words | ≈ 110 |

## On-slide text (exact)

- Breadcrumb: IRIS + FHIR | SYSTEM ARCHITECTURE
- Title: IRIS for Health is the single source of truth; agents reach it only through typed tools.
- Edge: Heartstep app (missions · symptom tap · Thai voice); Smartwatch (HealthKit / Health Connect); Clinician web (signs limits · reviews flags); Local data (places · heat · PM2.5)
- IRIS for Health: FHIR Server R4 (every fact as a standard resource) [BUILT: synthetic bundles]; FHIR SQL Builder (tables for the rules engine) [PLANNED]; Vector Search (approved text + activity ranking) [PLANNED]; Interoperability (HL7v2 / CDA → FHIR) [LATER]
- Agent harness: Rules engine [RULES ONLY] (red flags · limit gate · allowed set · output filter); MCP server (typed tools · no tool writes limits); Open models [MODEL] (one job each)
- Arrow labels: Observations; signed CarePlan + Provenance; Location / HealthcareService; SQL; allowed set; tool calls; FHIR REST; SQL + vector; Task + Provenance; taps, check-ins
- Takeaway: Rules engine owns safety. Agent owns conversation. No tool can write a limit.

## Visual spec

- The IRIS box is the visual centre and the largest object; all arrows touch it.
- "BUILT" badge only on FHIR Server R4, and it says what is built (synthetic bundles validated, loader written), not that IRIS is running live.
- No arrow from any model directly to FHIR: models reach data only via MCP.

## Speaker notes (Q&A)

IRIS for Health is the single source of truth: the FHIR R4 server holds the patient, the clinician-signed limit record, watch observations, missions, symptom answers, red flags, consent and provenance. FHIR SQL Builder will give the rules engine SQL tables, and Vector Search grounds the model in approved content and ranks nearby activities, so IRIS is far more than a vector store. Agents touch data only through typed MCP tools (the kit's FastMCP pattern), and no tool writes a limit. Today the synthetic bundles and the loader exist; SQL Builder, Vector tables and MCP are planned, and we say so.

## Data needed for this page

| Item | Source | Status |
|---|---|---|
| Five-layer design, safe default, tooling layer | `docs/diagrams/backend-architecture.dc.html` | In repo |
| Built vs planned split | `pitch/appendix/A02-system-architecture.md` "Built vs planned" | In repo |
| Whether bundles are loaded into a running IRIS | `pitch/README.md` open item; `judge-questions.md` Q4 `[CONFIRM]` | **Missing: team must confirm** before the badge can say "running on IRIS" |
| SMART on FHIR for clinician web | A02 | **To confirm** (left off the slide) |

## Sources in repo

- `pitch/appendix/A02-system-architecture.md`
- `docs/diagrams/backend-architecture.dc.html`, `docs/pitch/faq-appendix/slides/architecture.html`
- `FHIR-AI-Hackathon-Kit/README.md` (tutorials 3.x FHIR, 4.1 Vector Search, 5.1 agents, 5.2 MCP), `FHIR-AI-Hackathon-Kit/skills/iris-ai-agents/SKILL.md`
- `synthetic/load_to_iris.py`
