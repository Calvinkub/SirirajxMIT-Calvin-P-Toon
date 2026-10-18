# Handoff — SirirajxMIT (Calvin, P, Toon)

_Last updated: 2026-10-17 by Calvin (with Claude). Pitch script Draft 1 folded into design doc §2b._

## Research (added 2026-10-17)

See [research/README.md](research/README.md) (guidelines and Thai market, from NotebookLM) and [research/pitch-claims-check.md](research/pitch-claims-check.md). Machine-generated: verify before quoting.

## Agentic AI workflow plan (added 2026-10-18)

For AI-expert judges: [CVD Mission Coach — Agentic AI Workflow Plan](https://claude.ai/artifact/TeeFMYw4faY4HCZ6rM3yyM) (Claude Doc, private until Calvin shares it). Model stack: Qwen3-ASR (speech in), Qwen3-4B (router and tool calls), MedGemma 27B / 1.5 4B (reasoning, discharge-note reading), Qwen3-8B or Typhoon 2 (Thai phrasing), Qwen3-TTS (English only; Thai TTS still to choose). Backend diagram: [docs/diagrams/](docs/diagrams/).

## Where we are

- The idea is defined at the problem level and a first design draft is written. An initial browser UI is now implemented on `feature/initial-ui` (17 October 2026).
- Run `npm run dev` and open http://127.0.0.1:5173. No dependency installation is needed. See [UI review and assumptions](docs/initial-ui-review.md).
- The browser-only prototype uses fictional local data and scripted conversation. On branch `intersystems`, `docker compose up -d --build` runs a Python API and IRIS for Health demo at http://127.0.0.1:8000 with SQL persistence and a seeded FHIR R4 server. See [IRIS setup](docs/intersystems-setup.md). Username-only login and full patient-record onboarding are implemented; `somchai` opens the existing sample. New records are available through `/api/me/context` for future agent tools. Real AI/MCP, watch connection, notifications, verified authentication, and a clinician approval workflow are not implemented.
- Design draft: [docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md](docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md)

## The idea in one paragraph

After a CVD diagnosis, patients have to change their behavior. For example, they often need to exercise *less* hard than before. Many already have a smartwatch full of data, but they don't know what to actually do. Our app lets them run on autopilot: they declare goals in a chat with an AI agent, and the agent reads watch data through MCP. The agent then pushes 1–2 tiny, safe missions per day to the phone and watch. Safety limits come from the clinician, never from the AI.

## Journey

Open app → demographics → goal declaration (AI agent + MCP to watch data, weekly/daily missions) → personalized plan → daily push missions → weekly check-in.

## What we need from each teammate

Please read the design draft and answer **Section 8: Open questions** directly in the file, or in the group chat. The most important ones are:

1. Does every user need a CPET result? (Draft 1 script picked post-MI as the lead user.)
2. What does the hackathon require us to deliver, and by when?
3. Which smartwatch or phone can we demo on?

## Decisions so far

| Decision | By | Note |
|---|---|---|
| Missions delivered as phone push, mirrored to watch | Claude's call, change if you disagree | Avoids building a watch app |
| Rules engine owns safety; LLM only owns conversation | Claude's call, change if you disagree | Red-flag path is hard-coded |
| Positioned as adherence support, not diagnosis | Claude's call, change if you disagree | Thai FDA SaMD exposure |

## InterSystems challenge angle (added 2026-10-17)

Source: exploration of the [FHIR-AI-Hackathon-Kit](https://github.com/intersystems-community/FHIR-AI-Hackathon-Kit) and the [GrandHack 2026 challenge page](https://developer.intersystems.com/intersystems-challenge-mit-grandhack-2026/). The design doc does not use IRIS yet. Not verified against the Siriraj 2026 rules.

**What the kit offers.** InterSystems IRIS for Health in Docker (FHIR server, SQL, Vector Search), plus tutorials for LangChain agents (5.1) and MCP servers (5.2). The kit's data is synthetic only (about 5 Synthea patients). It has no image or audio handling.

**Judging, as relayed by Calvin.** InterSystems judges on how interesting and innovative the use of their technology is. A chatbot over PDFs with IRIS as a plain vector store is the weak version. The stronger version uses several IRIS models together.

**Ways to fit the CVD Mission Coach to IRIS (proposals, not decisions):**
- Store watch summaries and missions as FHIR `Observation` and `Task` or `CarePlan` resources. The agent writes them back (kit tutorials 3.3 and 3.4).
- Keep the clinician safety limits in IRIS as FHIR data. The rules engine reads them from there.
- Hybrid query: SQL filter on FHIR-projected tables (3.5) plus vector similarity, for example "post-MI patients with similar activity patterns".
- Expose the coach's data access as an MCP server (5.2).
- Name each IRIS feature on one architecture slide.

**Open questions for the organizers** (email: sea.query@intersystems.com). The first three change the plan most:
1. Is the provided data real or synthetic, and can we bring our own?
2. Are LLM or embedding API credits provided, and may we use a model other than OpenAI?
3. How deep must IRIS use be (vector only, or FHIR as well)?
4. Is there a written rubric for "innovation"?
5. Is there a mentor from InterSystems at the event, and when?

**Caveats.** Any demo data is synthetic and must be labelled so in the pitch. The LLM never makes clinical decisions, which matches the decision table above.

## Next steps

1. The team answers the open questions.
2. We finalize the design doc.
3. Review the initial UI and confirm the assumptions in `docs/initial-ui-review.md`.
4. Plan and implement the approved clinical/data integrations after the team settles the open questions.
