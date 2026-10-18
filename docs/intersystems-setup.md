# Local IRIS for Health setup

This setup uses the [FHIR-AI-Hackathon-Kit V2](https://github.com/intersystems-community/FHIR-AI-Hackathon-Kit/tree/V2) approach: IRIS for Health Community, the external Python driver, SQL tables, and a FHIR R4 repository. It adds a small FastAPI backend for Heartstep. No LLM key is required.

## Run

Start Docker Desktop, then from the repository root:

```sh
docker compose up -d --build
docker compose logs -f api
```

On the first run the images download, IRIS initializes, and the API installs FHIR and seeds fictional data. Wait for `Application startup complete` in the API logs.

- App: http://127.0.0.1:8000
- API documentation: http://127.0.0.1:8000/docs
- Database health: http://127.0.0.1:8000/api/health
- IRIS portal: http://127.0.0.1:52773/csp/sys/UtilHome.csp
- FHIR R4 metadata: http://127.0.0.1:52773/fhir/r4/metadata
- FHIR sample patient: http://127.0.0.1:52773/fhir/r4/Patient/demo-somchai

Local demo login: `SuperUser` / `SYS`. Namespace: `FHIRSERVER`. Native SQL port: `1972`.

All published ports bind to loopback. This is a username-only development app. Usernames identify profiles and do not verify identity. Anyone who knows a username can open that profile. Keep it local and use sample data. Verified authentication, limited database roles, and deployment security are future work. Session cookies scope requests to the selected profile; they do not make username-only login secure. `IRIS_PASSWORD` configures the API connection; changing it alone does not change the database password. If you change the IRIS password through the portal, set the matching value in an ignored `.env` file and recreate the API container.

Optional configuration: copy `.env.example` to `.env`. `APP_PORT` changes the app's host port. `IRIS_IMAGE` selects the base IRIS image; rebuild after changing it. The default follows the kit's `latest-cd` image, so upgrades should be tested against a backup of the data volume.

## Username entry and onboarding

At http://127.0.0.1:8000 enter `somchai` to open the existing sample patient, or choose a new username (3–32 ASCII letters, numbers, dots, underscores, or hyphens; case-insensitive). A returning session restores its home page on reload. Sign out to switch users.

New usernames open five steps:

1. Name, age, sex, patient-record number, clinic, medical history, allergies, and recovery goal.
2. Repeatable diagnosis and medication entries. Missing medication information is distinguished from reporting no current medications.
3. Repeatable measurements with a value, unit, and timestamp: heart rate, systolic/diastolic BP, weight, height, oxygen saturation, or blood glucose. Input times use the browser's local timezone and are saved as ISO timestamps.
4. Optional doctor-provided CPET: date, doctor/care team, peak VO₂ (mL/kg/min), HR at VT1 (bpm), peak HR (bpm), and report notes. Skip this step if unavailable. Report files are not uploaded in this version.
5. Review and save. Registration writes the account and all clinical context in one SQL transaction; exercise approval is never created from these inputs.

New profiles open their own home page with no invented sample watch readings, history, or missions. My profile shows the saved records. Clinician limits remain separate. The form draft stays in memory until Save; reload before saving discards the draft.

`GET /api/me/context` returns patient-scoped structured context for future agent tools: patient details, diagnoses, medications, measurements, optional CPET, provenance, and current safety status. CPET is explicitly marked unverified. This is an API foundation; no agent or LLM is connected yet. New onboarding data is stored in SQL; automatic FHIR mapping/synchronization is not implemented.

Login uses an opaque HttpOnly, SameSite cookie and a hashed session token stored in IRIS (seven-day expiry). Patient IDs are resolved from the session, not accepted from the browser. Local UI preferences are keyed per patient. This remains a prototype with username-only identity selection, not production authentication.

## What is connected

The Python server serves the existing frontend and enables its IRIS mode via `/runtime.js`. `npm run dev` still serves the browser-only demo on port 5173.

IRIS tables under schema `Heartstep`:

| Table | Contents |
|---|---|
| Patient | Fictional profile and persisted symptom-stop state |
| ClinicalLimit | Server-owned sample limits, approver, source, and review date |
| Completion | Dated walk and medication completion records |
| ActivitySummary | Simulated steps and resting heart rate |
| Account | Normalized username linked to a patient |
| UserSession | Hashed session token and expiry |
| PatientRecord | Demographics, history, allergies, goal, and medication-information status |
| Diagnosis / Medication / Measurement | Repeatable structured, patient-scoped records with provenance |
| CPET | Optional doctor-report values entered by the patient; unverified |

FHIR contains `Patient/demo-somchai` and `Observation/demo-resting-hr`. The UI reads the SQL data; FHIR is seeded and available for the next hospital integration step. The observation and SQL watch summary are illustrative fixtures, not an automatic synchronization pipeline.

Completing or undoing a mission saves through the API. Weekly walk counts come from the completion table. Symptom reports pause the UI immediately and persist to IRIS; a failed stop write is reported and retried on reload from browser-local state. Failed reads/writes disable exercise until reload/reconnection. The server also rejects walk completions after a symptom stop or with missing/expired approval. It never accepts new clinician limits from the browser.

The onboarding goal is stored in IRIS. Later goal edits in the scripted coach, chat, check-ins, and community choices remain browser-local. The browser-only demo retains its original simplified onboarding; full database-backed onboarding is on port 8000. No watch, notifications, real clinician workflow, AI, MCP, or vector search is connected.

Somchai’s displayed sample week is fixed at 12–18 October 2026. New profiles use the current Bangkok date. Seeded approval expires on 17 November 2026, checked against the current Bangkok date. After expiry, a developer must update the fictional seed limit in SQL for continued demo use; restarting does not silently renew approval. `POST /api/demo/reset` clears only the sample day's completions and symptom pause. It is a demo reset, not a clinical clearance flow.

## Verify

```sh
npm ci
npm test
npm run test:iris
```

The IRIS smoke test requires the stack running and resets today's fictional progress. It tests real SQL reads/writes, duplicate completion, undo, symptom pause, and rejection of browser-supplied clinical fields.

Optional Python boundary tests:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.txt
.venv/bin/python -m unittest discover -s tests/backend
```

## Stop and restart

```sh
docker compose down
docker compose up -d
```

The `heartstep_iris-data` named volume preserves records. Setup is idempotent and retains existing records, completions, and symptom pauses. Do not delete the volume to troubleshoot ordinary startup issues.

For diagnostics use `docker compose ps` and `docker compose logs --tail=100 iris api`. If port 8000 is occupied, set `APP_PORT=8001` in `.env`; native/FHIR port conflicts require changing the host side of the corresponding ports in `compose.yaml`.

### Full onboarding integration check

```sh
docker compose exec -T api python < scripts/smoke-onboarding.py
```

This creates two temporary synthetic accounts, checks returning login, record persistence, optional CPET, account isolation, and locked exercise, then removes only those test-created records. Frontend tests include in-memory DOM tests for the complete forms, back navigation, CPET skipping, and sign-out.
