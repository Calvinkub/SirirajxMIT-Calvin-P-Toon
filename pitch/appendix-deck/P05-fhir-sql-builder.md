# P05 · How does the rules engine read FHIR? (FHIR SQL Builder)

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "IRIS + FHIR". PAGE TAG: "A05".

BREADCRUMB: "IRIS + FHIR | FHIR SQL BUILDER"
TITLE: "FHIR SQL Builder turns the signed limits into SQL the rules engine can gate on."

LAYOUT: a five-step horizontal flow across the top (y=180 to y=330); below it two panels side by side (y=370 to y=860): left a table of projected tables, right a code box. Footer below.

Top-right of the title area: a grey dashed badge "PLANNED · kit tutorial 3.5".

FIVE-STEP FLOW (rounded boxes joined by teal arrows, each box has a number circle and a 1–2 word name, with one tiny grey line under it):
  "1 Credentials" – "FHIR-SQL user"
  "2 Repository" – "/fhir/r4"
  "3 Analysis" – "sample of resources"
  "4 Transform spec" – "pick the columns"
  "5 Projection" – "SQL package CMC" (this box has a teal border)

LEFT PANEL header "Projected tables (proposed)" – a clean table with 3 columns "Table", "From", "Columns", 6 rows, thin grey lines:
  "CMC.LimitRecord" | "CarePlan" | "status, review-by, HR ceiling, RPE"
  "CMC.AllowedActivity" | "CarePlan extension" | "activity code"
  "CMC.Vital" | "Observation" | "LOINC, time, value"
  "CMC.Mission" | "Task" | "mission id, status, time"
  "CMC.SymptomCheck" | "QuestionnaireResponse" | "item, answer"
  "CMC.Place" | "Location + HealthcareService" | "lat, lon, hours, intensity"

RIGHT PANEL header "Gate 1 in SQL" – a dark-text monospace code box on very light grey, exactly these 4 lines:
  "SELECT TOP 1 HrCeiling, RpeLow, RpeHigh"
  "FROM CMC.LimitRecord"
  "WHERE Subject = 'Patient/cmc-p01'"
  "  AND Status = 'active' AND PeriodEnd > NOW"
  Under the code box, a big orange #C2571A statement in 30 px: "No row = no exercise missions"

TAKEAWAY STRIP (pale teal): "Same namespace holds VECTOR columns: one query can filter FHIR columns and rank by similarity."

FOOTER: "Source: FHIR-AI-Hackathon-Kit tutorial 3.5 (projecting FHIR data in SQL); pitch/appendix/A03. Table names depend on the final transform spec"

DO NOT: show a screenshot of a real management portal; add logos; add more SQL lines; add numbers.
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "Are you using more than the FHIR REST API? Where does SQL Builder fit?" |
| Page type | Value-chain flow (mirrors template slide 16: left-to-right boxes) + a table panel, with a big statement as the "Team view" (template slide 4) |
| Layout | 5-step flow, projected-table table, SQL code box, takeaway strip |
| On-slide words | ≈ 120 (matrix-style page) |

## On-slide text (exact)

- Breadcrumb: IRIS + FHIR | FHIR SQL BUILDER
- Title: FHIR SQL Builder turns the signed limits into SQL the rules engine can gate on.
- Badge: PLANNED · kit tutorial 3.5
- Flow: 1 Credentials (FHIR-SQL user) → 2 Repository (/fhir/r4) → 3 Analysis (sample of resources) → 4 Transform spec (pick the columns) → 5 Projection (SQL package CMC)
- Table: 6 rows as in the prompt
- Code: 4 lines as in the prompt; statement "No row = no exercise missions"
- Takeaway: Same namespace holds VECTOR columns: one query can filter FHIR columns and rank by similarity.

## Visual spec

- The code is illustrative and simplified for the slide (`NOW` stands for `CURRENT_TIMESTAMP`; IRIS uses `SELECT TOP`, not `LIMIT`). The full version with the 7-day vitals query is in A03 for the speaker.
- "No row = no exercise missions" is the one orange element: it is spec rule 6 expressed in SQL.

## Speaker notes (Q&A)

The kit's tutorial 3.5 projects FHIR resources into SQL tables through the FHIR management portal in five steps: credentials, repository, analysis, transform specification and projection. We would define one package, `CMC`, with tables for the limit record, allowed activities, vitals, missions, symptom checks and places, so the rules engine gates on plain SQL: no active, unexpired, signed limit row means no exercise mission. Because Vector Search lives in the same namespace, one statement can filter projected columns such as intensity and opening hours and then rank by `VECTOR_COSINE`. This is planned, not run; the open technical question is whether SQL Builder projects our extension values and repeating extensions as columns.

## Data needed for this page

| Item | Source | Status |
|---|---|---|
| Five SQL Builder steps | `FHIR-AI-Hackathon-Kit/Tutorials/3-fhir/markdown/3.5-projecting-fhir-data-in-sql.md` | In repo |
| Proposed tables and gate query | `pitch/appendix/A03-fhir-data-model.md` | In repo (proposal) |
| Can SQL Builder project custom and repeating extensions? | — | **Missing: to test on IRIS or ask InterSystems mentors** |
| Projection actually built | — | **Not done** (engineering step 2 in A13) |

## Sources in repo

- `pitch/appendix/A03-fhir-data-model.md` (SQL Builder section)
- `FHIR-AI-Hackathon-Kit/Tutorials/3-fhir/markdown/3.5-projecting-fhir-data-in-sql.md`
- `FHIR-AI-Hackathon-Kit/skills/iris-sql-python/SKILL.md` (`SELECT TOP`)
- `pitch/appendix/A13-roadmap-mvp.md` engineering track step 2
