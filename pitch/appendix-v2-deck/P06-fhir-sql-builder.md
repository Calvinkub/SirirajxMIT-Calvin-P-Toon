# P06 · FHIR SQL Builder turns the signed FHIR record into SQL tables, so every safety gate is a plain query: no row, no exercise.

## Key message

The rules engine should not page through FHIR REST calls to decide whether a patient may exercise today; it should ask one SQL question of the same data the clinician signed. InterSystems FHIR SQL Builder projects FHIR resources into SQL tables inside IRIS for Health in five steps (credentials, repository, analysis, transform specification, projection), and the kit shows it can be scripted from Python. Run against our 8 synthetic patients, four SQL gates leave 5 patients with missions, 1 of them supervised-first, and block 3 (ineligible, unsigned, red flag); this is planned work, and the open risk is whether our custom extensions project as columns.

## Why this matters to the judges

- **Use of InterSystems technology:** FHIR SQL Builder is an IRIS for Health feature most teams skip. We use it for the part that must be most reliable: the safety gates.
- **Technical coherence:** the gate logic is auditable SQL over a standard record, not code buried in an agent. The same projected tables feed weekly clinician summaries and, in the same namespace, the vector ranker (P07).
- **Real-world impact:** hospitals already have analysts who speak SQL. Projections let them check adherence and red-flag rates without learning FHIR search.

## Full detail

### 1. What FHIR SQL Builder is

InterSystems' documentation describes the FHIR SQL Builder as "a sophisticated projection tool used to create custom SQL schemas using data in an InterSystems IRIS for Health FHIR repository without moving the data to a separate SQL repository" (quoted from the InterSystems docs page as returned by web search; the page itself did not render for us, so the wording is **to verify**). The kit's tutorial 3.5 says it is "particularly powerful for looking at data at the population level, rather than querying individual patients or resources", and its FHIR skill advises: "For population-level analytics prefer projecting FHIR to SQL (FHIR SQL Builder) … over paging through REST."

### 2. The five steps (kit tutorial 3.5)

| Step | What you define | Our setting (planned) |
|---|---|---|
| 1. Credentials | A user for the Builder ("If you are not using a superuser with %All resources, the user will need the FSB_Administrator resource") | Dedicated FSB user, not SuperUser |
| 2. Repository configuration | Host, internal web port 52773, then "Discover FHIR Repositories", pick `/fhir/r4` | `/fhir/r4` on our IRIS for Health |
| 3. Analysis | A sample of the repository ("selectivity percentage"); the kit uses 100% on a small server | 100% for the 383 synthetic resources |
| 4. Transform specification | Which resource elements become columns, with names; histograms help pick elements; exportable as JSON | Spec "CMC" below |
| 5. Projection | Analysis + spec + SQL package name; SQL access per user | Package `CMC` |

Portal: `http://localhost:52773/csp/fhir-management/index.html`. The kit also shows a programmatic path with the experimental community library `iris-fhirsql`: `FHIRSQLClient`, `client.credentials.create(...)`, `client.repositories.create(..., fhir_url="/fhir/r4")`, `client.analysis.create(..., selectivity_percentage=100)`, a `TransformSpecBuilder` with `add_field("Patient", "Patient.gender", "String", name="PatientGender", length=10, index=True)`, then `client.projections.create(..., package_name=...)`. Scripting matters for us: the projection can live in version control next to `generate_fhir.py` instead of being clicked together before the demo.

After projection, tables are queried like any IRIS SQL table, e.g. the kit's `SELECT … FROM FHIRSQLTables.Condition` joined to `PatientNames` on `ConditionSubjectReference = 'Patient/' || pn.Patient`. Note two IRIS details: `SELECT TOP n`, not `LIMIT`; and the Python driver autocommits by default.

### 3. The CMC transform specification (proposal)

| Projected table | From | Columns the rules need | Gate it serves |
|---|---|---|---|
| `CMC.LimitRecord` | `CarePlan` | id, subject, status, period.start, period.end, author, `hr-ceiling` value, `rpe-target` low/high, `limit-source`, `restriction` | G2 signed and current limit |
| `CMC.LimitAttestation` | `Provenance` where agent type = attester | target, agent who, recorded | G2 (who signed) |
| `CMC.AllowedActivity` | `CarePlan.extension[allowed-activity]` (repeating) | careplan id, activity code | Catalogue filter |
| `CMC.Eligibility` | `Flag` code `app-ineligible`; `Observation` `aacvpr-risk-class` | subject, status, risk class | G1 eligibility, supervised-first |
| `CMC.RedFlag` | `Flag` code `red-flag-chest-symptom` | subject, status, period | G3 unresolved red flag |
| `CMC.Vital` | `Observation` (8867-4, 41950-7, 85354-9 components) | subject, code, effective, value, unit, device | Context, weekly summary, plausibility |
| `CMC.Mission` | `Task` | id, subject, basedOn, code, status, executionPeriod.start | Adherence, progression cap |
| `CMC.SymptomCheck` | `QuestionnaireResponse` | subject, `about-task`, authored, linkId, answer | Post-mission screen |
| `CMC.Place` | `Location` + `HealthcareService` | id, type, latitude, longitude, opening, closing, indoor, intensity | Geo filter (P08) |

### 4. The gates as SQL (illustrative; final names depend on the spec)

```sql
-- G1 eligibility: an active 'app-ineligible' flag blocks everything
SELECT COUNT(*) FROM CMC.Eligibility e
 WHERE e.Subject = ? AND e.FlagCode = 'app-ineligible' AND e.Status = 'active';

-- G2 signed, current limit: no row = no exercise missions
SELECT TOP 1 l.ID, l.HrCeiling, l.RpeLow, l.RpeHigh, l.LimitSource
  FROM CMC.LimitRecord l
  JOIN CMC.LimitAttestation a ON a.Target = 'CarePlan/' || l.ID
 WHERE l.Subject = ? AND l.Status = 'active'
   AND l.PeriodStart <= CURRENT_TIMESTAMP AND l.PeriodEnd > CURRENT_TIMESTAMP;

-- G3 unresolved red flag: any active row stops coaching
SELECT COUNT(*) FROM CMC.RedFlag r WHERE r.Subject = ? AND r.Status = 'active';

-- Context for the allowed set and the weekly summary
SELECT v.Code, AVG(v.Value) AS Mean7d, COUNT(*) AS N
  FROM CMC.Vital v
 WHERE v.Subject = ? AND v.Effective >= DATEADD('dd', -7, CURRENT_TIMESTAMP)
 GROUP BY v.Code;
```

Values are always bound with `?` placeholders (kit: "never f-string values into SQL"). The gates run in the rules engine under a service user; the model-facing tools get a SELECT-only user and never see these tables' write path.

### 5. Worked example: the gates on 2026-10-18 for the 8 synthetic patients

| Patient | G1 eligible? | G2 active, attested, in period? | G3 red flag? | Risk class | Result |
|---|---|---|---|---|---|
| p01 Somchai | yes | yes (to 2026-11-29) | no | low | Missions |
| p02 Malee | yes | yes | no | low | Missions |
| p03 Anan | yes | yes | no | **moderate** | Supervised sessions first |
| p04 Prasert | **no** (`app-ineligible`) | no CarePlan | no | high | **Blocked** |
| p05 Wanida | yes | yes, with restriction | no | low | Missions (walking only) |
| p06 Kittisak | yes | **no** (`draft`, no attester) | no | unknown | **No exercise missions** |
| p07 Siriporn | yes | yes | **yes** (active) | low | **Stopped**, clinician review |
| p08 Abdul | yes | yes | no | low | Missions (19:00) |

Result: 8 → 7 (G1) → 6 (G2) → 5 (G3), of which 1 is supervised-first. This is the logic the generator encoded, re-derived by reading the bundles; it has not been run as SQL on IRIS.

### 6. Design decisions

- **SQL for gates, FHIR REST for writes.** Reads that decide safety go through projections; writes (`Task`, `Flag`, `Provenance`) go through the FHIR API so they are validated and versioned as FHIR.
- **Freshness.** A gate is only as good as the projection's freshness. If a clinician signs a `CarePlan` at 09:15, the 09:30 mission must see it. Whether projections update with each FHIR write or need a refresh is **to verify** with InterSystems. Fallback: the rules engine double-checks G2 and G3 with a direct FHIR read (`CarePlan?patient=…&status=active`, `Flag?patient=…&status=active`) before writing any `Task`; SQL stays the fast path for analytics and context.
- **Fail closed.** If the projection is unavailable, the gates return "no row", which means no exercise mission (spec rule 10, safe default).
- **Rejected alternatives:** paging FHIR search per patient (slow and verbose for weekly summaries); copying FHIR into our own tables with an ETL job (a second source of truth that can drift from what was signed).

## Visualizations

### Chart 1 · Funnel: synthetic patients through the SQL gates

- **Type:** funnel (vertical).
- **Title:** "Four gates, eight patients: five get missions, three are stopped by data"
- **Axis:** number of synthetic patients.

| Stage | Patients remaining | Removed | Who |
|---|---|---|---|
| All synthetic patients | 8 | — | — |
| G1 not flagged ineligible | 7 | 1 | p04 (LVEF 30%, ICD) |
| G2 active, attested, in-period limit | 6 | 1 | p06 (draft) |
| G3 no active red flag | 5 | 1 | p07 (chest tightness day 5) |
| of which app-only | 4 | 1 supervised-first | p03 (moderate risk) |

**Notice:** every removal is caused by a FHIR resource a clinician or a rule wrote, never by a model output. Synthetic data; derived from bundle contents, not from a SQL run.

### Chart 2 · Bar: columns to project per proposed table, split by source kind

- **Title:** "Most gate-critical columns come from our own extensions"
- **Axis:** number of columns.

| Table | Columns from standard FHIR elements | Columns from custom extensions | Total |
|---|---|---|---|
| CMC.LimitRecord | 6 (id, subject, status, period.start, period.end, author) | 5 (hr-ceiling, rpe low, rpe high, limit-source, restriction) | 11 |
| CMC.AllowedActivity | 1 (careplan id) | 1 (allowed-activity, repeating) | 2 |
| CMC.SymptomCheck | 4 (subject, authored, linkId, answer) | 1 (about-task) | 5 |
| CMC.Place | 6 (id, type, latitude, longitude, opening, closing) | 2 (indoor, intensity) | 8 |
| CMC.Mission | 6 | 0 | 6 |
| CMC.Vital | 6 | 0 | 6 |
| CMC.RedFlag | 4 (subject, code, status, period) | 0 | 4 |

**Notice:** across all tables only 9 of 42 proposed columns come from extensions, but in the two tables the limit gate and the catalogue filter depend on (`LimitRecord`, `AllowedActivity`) it is 6 of 13, and those are exactly the columns nobody has projected yet. This is the single most important technical test before the pitch. (Column counts are our proposal.)

### Diagram · Five-step projection flow

Credentials (FSB user) → Repository (`/fhir/r4`) → Analysis (100%) → Transform spec "CMC" → Projection (package `CMC`) → rules engine queries (G1–G3) → `Task` + `Provenance` written back through FHIR REST. Badge: PLANNED.

## Numbers and claims ledger

| Claim | Value | Source | Status |
|---|---|---|---|
| Five steps and portal URL | as listed | `FHIR-AI-Hackathon-Kit/Tutorials/3-fhir/markdown/3.5-projecting-fhir-data-in-sql.md` | checked (kit) |
| `FSB_Administrator` resource needed for non-superusers | quote | same | checked |
| Programmatic library `iris-fhirsql` (experimental) | as listed | same | checked (kit text); not run |
| "without moving the data to a separate SQL repository" | quote | InterSystems docs (KEY=AFSB) via search result | to verify (page did not render) |
| Prefer SQL Builder over paging REST for population analytics | quote | `skills/iris-fhir/SKILL.md` | checked |
| `SELECT TOP`, not `LIMIT`; autocommit default | as stated | `skills/iris-sql-python/SKILL.md` | checked |
| Gate outcomes for 8 patients | 8 → 7 → 6 → 5 (1 supervised) | derived from `synthetic/fhir/*.json` | checked, synthetic |
| Proposed columns | as Chart 2 | this proposal (from A03) | estimate |
| Extensions project as columns, incl. repeating | — | — | to verify on IRIS |
| Projection freshness after a FHIR write | — | — | to verify with InterSystems |
| Projection actually built | — | — | not done |

## Limits and open questions

- Not run. No projection exists yet; gate results are derived from the data, not executed.
- Can the transform specification select an extension by URL (FHIRPath like `CarePlan.extension.where(url='…/hr-ceiling').valueQuantity.value`) and a repeating extension into a child table? To test or ask mentors.
- Projection freshness and refresh cost are unknown.
- Access control for projected tables (per-user SQL access in step 5) must match PDPA roles (P20).
- `Provenance` agent-type filtering (attester only) may need its own table.

## Likely judge questions

1. **"Why not just call the FHIR API?"** We do for writes and as a final double-check. For gates and weekly summaries, SQL over projections is simpler, faster to audit and what hospital analysts already use.
2. **"Is the projection a copy that can go stale?"** InterSystems describes it as a projection without moving data; the refresh behaviour after a write is the question we will confirm. Until then, the rules engine re-reads `CarePlan` and `Flag` via FHIR before writing a mission.
3. **"Will it handle your custom extensions?"** Not yet tested; it is our top technical risk. Fallback: model the limit values as `Goal.target` or `CarePlan.activity.detail` elements that project natively.
4. **"Show me the rule 'no signed limit, no exercise'."** G2 above: no active, in-period `CarePlan` with an attester `Provenance` returns no row, and no row means no exercise mission.
5. **"Can you build it in code?"** The kit's experimental `iris-fhirsql` client creates credentials, repository, analysis, spec and projection from Python.

## Sources

Repo:
- `FHIR-AI-Hackathon-Kit/Tutorials/3-fhir/markdown/3.5-projecting-fhir-data-in-sql.md`
- `FHIR-AI-Hackathon-Kit/skills/iris-fhir/SKILL.md`, `skills/iris-sql-python/SKILL.md`, `skills/iris-ai-agents/SKILL.md`, `skills/iris-environment/SKILL.md`
- `pitch/appendix/A03-fhir-data-model.md` (SQL Builder section), `pitch/appendix-deck/P05-fhir-sql-builder.md`
- `synthetic/fhir/*.json`, `synthetic/generate_fhir.py`
- `docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md` §5 (rules 6, 7, 10)

External (opened 2026-10-18):
- InterSystems documentation, "The FHIR SQL Builder" (KEY=AFSB): https://docs.intersystems.com/components/csp/docbook/Doc.View.cls?KEY=AFSB (opened; the server returned "Version Not Available", the quoted sentence comes from the search-result summary of this page: to verify)
- HL7 FHIR R4 Task: https://hl7.org/fhir/R4/task.html

## Image-generation prompt

Design one 16:9 information slide on a white background. Lead with the key message as the title: "FHIR SQL Builder turns the signed FHIR record into SQL tables, so every safety gate is a plain query: no row, no exercise." Make the main chart a funnel of synthetic patients through the gates with exactly these numbers: All 8 → not ineligible 7 → signed current limit 6 → no active red flag 5 (1 of them supervised first). Beside it, show the five projection steps (Credentials → Repository /fhir/r4 → Analysis → Transform spec → Projection, package CMC) with a "PLANNED" badge, and a short SQL snippet labelled "illustrative". Label data as synthetic. No logos, no invented numbers; choose the design freely.
