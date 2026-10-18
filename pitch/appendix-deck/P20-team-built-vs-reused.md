# P20 · What did you build here, what did you reuse, and who are you?

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "Why us". PAGE TAG: "A20".

BREADCRUMB: "WHY US | TEAM AND WHAT EXISTS"
TITLE: "What you saw is exactly what exists: built here, reused, and still planned."

LAYOUT: a team row at the top (y=170 to y=320); three columns below (y=350 to y=830); an "ask" strip (y=850 to y=940). Footer below.

TEAM ROW: three equal cards side by side, each with a simple friendly lineal-colour person icon (no real faces), a name in 26 px deep teal and a role line in 18 px grey:
  "Calvin" – "[ROLE]"
  "P" – "[ROLE]"
  "Toon" – "[ROLE]"

COLUMN 1 header "Built here" with a teal-filled badge "BUILT". Six lines, each with a small teal check:
  "FHIR data model + generator"
  "383 synthetic resources, 9 bundles"
  "Loader for the kit's IRIS server"
  "Heartstep UI, rules-only checks (6/6 tests)"
  "Tool-router experiments v1 + v2"
  "Scripted 8-step agent demo"

COLUMN 2 header "Reused" with a grey badge "REUSED". Five lines, each with a small grey recycle-arrow icon:
  "InterSystems FHIR-AI Hackathon Kit"
  "IRIS for Health Docker + tutorials"
  "Open weights: Qwen3, MedGemma"
  "fhir.resources (R4B validation)"
  "katgpt-rs (team's own prior library)"

COLUMN 3 header "Planned" with a grey dashed badge "PLANNED". Six lines, each with a small grey empty circle:
  "Live IRIS run of the demo"
  "SQL Builder projection"
  "Vector tables, Thai embeddings"
  "MCP server over FHIR"
  "Model serving, Thai TTS"
  "Clinician web app"

ASK STRIP (pale teal, three items with small icons separated by dots): "Our ask: InterSystems mentorship to run fully on IRIS · a cardiologist to sign the limit library · a small supervised pilot"

FOOTER: "Source: pitch/deck-3min/slides/tech.html (built vs reused); pitch/appendix/A02; npm test run 2026-10-18 (6 pass)"

DO NOT: draw photos or realistic faces; invent job titles, universities or degrees; add logos; add numbers other than those listed.
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "What did you build during the event, and what did you reuse? Who is on the team?" |
| Page type | Column map (mirrors template slide 2 columns; team row like the cover's names, slide 1) |
| Layout | Team row, three columns (built / reused / planned), ask strip |
| On-slide words | ≈ 110 |

## On-slide text (exact)

- Breadcrumb: WHY US | TEAM AND WHAT EXISTS
- Title: What you saw is exactly what exists: built here, reused, and still planned.
- Team: Calvin – [ROLE]; P – [ROLE]; Toon – [ROLE]
- Built here: FHIR data model + generator · 383 synthetic resources, 9 bundles · Loader for the kit's IRIS server · Heartstep UI, rules-only checks (6/6 tests) · Tool-router experiments v1 + v2 · Scripted 8-step agent demo
- Reused: InterSystems FHIR-AI Hackathon Kit · IRIS for Health Docker + tutorials · Open weights: Qwen3, MedGemma · fhir.resources (R4B validation) · katgpt-rs (team's own prior library)
- Planned: Live IRIS run of the demo · SQL Builder projection · Vector tables, Thai embeddings · MCP server over FHIR · Model serving, Thai TTS · Clinician web app
- Ask: Our ask: InterSystems mentorship to run fully on IRIS · a cardiologist to sign the limit library · a small supervised pilot

## Visual spec

- Replace each "[ROLE]" before rendering (e.g. technical lead, clinical lead, business lead per `pitch/README.md` speaker table). If roles are not filled, render without the role line rather than with placeholder text.
- If the bundles are confirmed loaded in IRIS before the event, move "Live IRIS run of the demo" wording to "Bundles loaded in IRIS" under "Built here".

## Speaker notes (Q&A)

At the event we built the FHIR data model and generator, 383 synthetic resources in nine idempotent PUT bundles with a loader for the kit's IRIS server, the Heartstep UI with rules-only safety checks, the two router experiments, and the scripted agent demo. We reused the InterSystems FHIR-AI Hackathon Kit for IRIS for Health and its tutorials, open Qwen3 and MedGemma weights, and katgpt-rs, a decoding library the team wrote before the event. SQL Builder, Vector tables, the MCP server, model serving and the clinician app are planned, and the demo is scripted in the browser, so we describe it as designed for IRIS until a live run is confirmed. Our ask is mentorship to run fully on IRIS, a cardiologist to sign the limit library, and a small supervised pilot.

## Data needed for this page

| Item | Source | Status |
|---|---|---|
| Built vs reused list | `pitch/deck-3min/slides/tech.html` footer, A02 "Built vs planned" | In repo |
| UI tests | `tests/*.mjs`, `npm test` run 2026-10-18: 6 tests, 6 pass | Checked |
| Team roles | `pitch/README.md` has `[NAME]` placeholders only | **Missing: team to fill** |
| "Rules engine" built? | tech slide says "rules engine" built; A02 says UI rules (`safety.js`) + router rules exist, SQL-based engine planned | **Inconsistent: this page uses the narrower wording** |
| Bundles loaded in IRIS | `pitch/README.md` open item | **Missing: confirm** |
| The ask | `pitch/main-3min.md` closing slide | In repo |

## Sources in repo

- `pitch/deck-3min/slides/tech.html`, `pitch/main-3min.md`, `pitch/README.md`, `pitch/pitch-techniques.md` ("say what was built at the event versus reused")
- `pitch/appendix/A02-system-architecture.md`
- `FHIR-AI-Hackathon-Kit/README.md`
- `safety.js`, `tests/safety.test.mjs`, `tests/ui.test.mjs`, `synthetic/`, `experiments/`, `demo/agent-flow-demo.html`
