# Handoff — SirirajxMIT (Calvin, P, Toon)

_Last updated: 2026-10-17 by Calvin (with Claude). Pitch script Draft 1 folded into design doc §2b._

## Research (added 2026-10-17)

See [research/README.md](research/README.md) (guidelines and Thai market, from NotebookLM) and [research/pitch-claims-check.md](research/pitch-claims-check.md). Machine-generated: verify before quoting.

## Where we are

- The idea is defined at the problem level and a first design draft is written. **No code yet.**
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

## Next steps

1. The team answers the open questions.
2. We finalize the design doc.
3. We write the implementation plan.
4. We build the demo.
