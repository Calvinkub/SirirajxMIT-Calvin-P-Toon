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

All published ports bind to loopback. This is an unauthenticated, single-fictional-patient development app. Keep it local and use sample data. Authentication, patient authorization, limited database roles, and deployment security are future work. `IRIS_PASSWORD` configures the API connection; changing it alone does not change the database password. If you change the IRIS password through the portal, set the matching value in an ignored `.env` file and recreate the API container.

Optional configuration: copy `.env.example` to `.env`. `APP_PORT` changes the app's host port. `IRIS_IMAGE` selects the base IRIS image; rebuild after changing it. The default follows the kit's `latest-cd` image, so upgrades should be tested against a backup of the data volume.

## What is connected

The Python server serves the existing frontend and enables its IRIS mode via `/runtime.js`. `npm run dev` still serves the browser-only demo on port 5173.

IRIS tables under schema `Heartstep`:

| Table | Contents |
|---|---|
| Patient | Fictional profile and persisted symptom-stop state |
| ClinicalLimit | Server-owned sample limits, approver, source, and review date |
| Completion | Dated walk and medication completion records |
| ActivitySummary | Simulated steps and resting heart rate |

FHIR contains `Patient/demo-somchai` and `Observation/demo-resting-hr`. The UI reads the SQL data; FHIR is seeded and available for the next hospital integration step. The observation and SQL watch summary are illustrative fixtures, not an automatic synchronization pipeline.

Completing or undoing a mission saves through the API. Weekly walk counts come from the completion table. Symptom reports pause the UI immediately and persist to IRIS; a failed stop write is reported and retried on reload from browser-local state. Failed reads/writes disable exercise until reload/reconnection. The server also rejects walk completions after a symptom stop or with missing/expired approval. It never accepts new clinician limits from the browser.

Goals, scripted chat, check-ins, and community choices remain browser-local. Onboarding is available in the browser-only demo. No watch, notifications, real clinician workflow, AI, MCP, or vector search is connected.

The displayed week is fixed at 12–18 October 2026. Seeded approval expires on 17 November 2026, checked against the current Bangkok date. After expiry, a developer must update the fictional seed limit in SQL for continued demo use; restarting does not silently renew approval. `POST /api/demo/reset` clears only the sample day's completions and symptom pause. It is a demo reset, not a clinical clearance flow.

## Verify

```sh
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
