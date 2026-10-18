# Pitch folder: Heartstep (CVD Mission Coach)

MIT GrandHack 2026 · InterSystems challenge, "Best Use of GenAI or FHIR using InterSystems technology" · team Calvin, P and Toon.

Judging criteria: Innovation · Real-world impact · Use of InterSystems technology · Technical coherence.

## Structure

The pitch is 3 minutes, then Q&A backed by an appendix.

| Part | Time | What it does | File |
|---|---|---|---|
| Minute 1 | 0:00–1:00 | Pain and problem: one patient, three sourced numbers, why a chatbot is not enough | [main-3min.md](main-3min.md), slides 1–2 |
| Minute 2 | 1:00–2:00 | Solution: IRIS for Health at the centre, live demo of the agent trace, measured router results (synthetic) | [main-3min.md](main-3min.md), slide 3, live demo, slide 4 |
| Minute 3 | 2:00–3:00 | Business: insurers (B2B2C) and freemium (B2C), why now, the ask | [main-3min.md](main-3min.md), slides 5–6 |
| Q&A | after | Jump to the appendix file that answers the question | [judge-questions.md](judge-questions.md) → [appendix/](appendix/) |

Spoken words: 133 / 148 / 147 per minute (428 total), at about 140 words per minute.

## Who presents what

| Part | Speaker | Backup |
|---|---|---|
| Minute 1: problem | [NAME 1] | [NAME 2] |
| Minute 2: solution and slide 4 | [NAME 2] | [NAME 3] |
| Live demo clicks | [NAME 3] (driver, at the laptop) | [NAME 1] |
| Minute 3: business and ask | [NAME 3] | [NAME 1] |
| Q&A: InterSystems, FHIR, agent, experiments | [NAME, technical lead] | |
| Q&A: clinical safety and limits | [NAME, clinical lead] | |
| Q&A: business, insurers, regulation | [NAME, business lead] | |

Suggestion: whoever built the router experiments answers the AI questions, because judges will probe the numbers.

## How to use this folder

1. **Rehearse from [main-3min.md](main-3min.md).** Read each spoken block aloud with a timer. If a block runs long, cut words; do not speed up.
2. **Rehearse the demo clicks** in [`demo/agent-flow-demo.html`](../demo/agent-flow-demo.html). The page auto-runs the football-to-golf message on load. On stage, click preset 1, wait for the trace, pick "Golf, walking with a pull cart", then "Start gently: 2 sessions", then click preset 4 (the chest-tightness message). Keep a screen recording as backup.
3. **Before Q&A, read [judge-questions.md](judge-questions.md).** Each answer names the appendix file to open.
4. **Appendix files** live in [appendix/](appendix/) (A01–A13). They are written separately; this folder only links to them:
   - [A01 Why not ChatGPT](appendix/A01-why-not-chatgpt.md)
   - [A02 System architecture](appendix/A02-system-architecture.md)
   - [A03 FHIR data model](appendix/A03-fhir-data-model.md)
   - [A04 Agentic harness](appendix/A04-agentic-harness.md)
   - [A05 InterSystems Vector Search and geo](appendix/A05-intersystems-vector-search-and-geo.md)
   - [A06 Tool-router experiments](appendix/A06-tool-router-experiments.md)
   - [A07 Safety and evaluation](appendix/A07-safety-and-evaluation.md)
   - [A08 Cost structure](appendix/A08-cost-structure.md)
   - [A09 Speed R&D (katgpt-rs)](appendix/A09-speed-rnd-katgpt.md)
   - [A10 Clinical evidence](appendix/A10-clinical-evidence.md)
   - [A11 Market and business](appendix/A11-market-and-business.md)
   - [A12 Regulatory and PDPA](appendix/A12-regulatory-pdpa.md)
   - [A13 Roadmap to MVP](appendix/A13-roadmap-mvp.md)

## Before the event: open items

- [ ] Fill in the [NAME] placeholders and the insurer [PRICE] on slide 5.
- [ ] Confirm whether the 8 synthetic FHIR bundles are loaded into the kit's IRIS FHIR server (`synthetic/load_to_iris.py`). This decides whether the demo is described as "running on IRIS" or "designed for IRIS". Today the demo page is scripted and in-browser.
- [x] PMC12990137 full text checked (2026-10-17): it states 93% of Italian GPs prescribe activity and 15% give it in writing. [ ] Optional: open the original Italian survey (its ref 13).
- [ ] Ask the organizers whether a pitch slide may show a live IRIS Management Portal window during Q&A.

## Rules for everything said on stage

- No invented statistics. Every number traces to a file in this repo; the source table is at the end of [main-3min.md](main-3min.md).
- Synthetic results are always called synthetic.
- Never say "proven", "optimal", "clinically validated", or that the app reduces readmissions.
- The AI never sets or raises an exercise limit. A clinician does.
- Red flags are handled by rules only. No model sees them first.
- Use 93% / 15% (Italian GPs), not the old 80% / 15%.
