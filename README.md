# SirirajxMIT — CVD Mission Coach

Team: Calvin, P, Toon.

An app for patients who were just diagnosed with cardiovascular disease. An AI agent reads the patient's smartwatch data and turns it into tiny daily missions, such as "walk 10 min, keep it easy", delivered to the phone and watch. The missions stay inside clinician-set safety limits.

- Start here: [HANDOFF.md](HANDOFF.md)
- Design draft: [docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md](docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md)

## IRIS database demo

Run `docker compose up -d --build`, then open http://127.0.0.1:8000. This mode stores fictional patient details, clinician limits, simulated watch summaries, mission completions, and symptom pauses in IRIS for Health. It also initializes a FHIR R4 server. See [setup, verification, and limitations](docs/intersystems-setup.md).

Run `npm run test:iris` to verify the running database integration. The browser-only prototype remains available below.

## Browser-only prototype

**Heartstep** is the working UI name. Run with Node.js 22 or later (no dependency installation required):

```sh
npm run dev
```

Open http://127.0.0.1:5173. The responsive prototype includes Today, My plan, My coach, Community, and My profile. Try completing a walk, setting a goal, checking in, or starting new-patient onboarding from My profile. Use “Reset demo data” in My profile to restore the sample patient.

```sh
npm test
```

This is a local interactive demo with fictional data and scripted coach replies. Watch connections, notifications, clinical approvals, and AI services are not connected. Use sample details only. Dates and weekly history are illustrative fixtures.

See the [document review and UI decisions](docs/initial-ui-review.md) for requirement mapping, assumptions, unresolved questions, and verification limits.
