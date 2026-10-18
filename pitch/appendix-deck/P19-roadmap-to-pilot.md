# P19 · Is there a realistic path to an MVP and a pilot?

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "Clinic + business". PAGE TAG: "A19".

BREADCRUMB: "CLINIC + BUSINESS | ROADMAP TO PILOT"
TITLE: "Six gates to a pilot, each passed by a named human; the critical path is people, not code."

LAYOUT: a six-gate horizontal timeline (y=180 to y=520); below it, left an engineering-steps list (x=80 to x=1100, y=550 to y=900) and right an MVP-scope box (x=1140 to x=1840, y=550 to y=900). Footer below.

TIMELINE: a teal line with six gate circles. Above each circle the gate name; below each circle "Passed by" and a status tag.
  "G-A Prototype" – "team" – teal tag "IN PROGRESS"
  "G-B Clinician review" – "cardiologist + rehab physician" – orange tag "OWNER NOT NAMED"
  "G-C Usability" – "≥ 8 Thai users aged 55–75" – grey tag "NOT STARTED"
  "G-D IRB, Thai FDA, PDPA" – "IRB + lawyers" – grey tag "NOT STARTED"
  "G-E Supervised pilot" – "clinician + statistician" – grey tag "NOT STARTED"
  "G-F Insurer pilot" – "insurer + statistician" – grey tag "NOT STARTED"
  The first circle is filled teal; the second circle is outlined orange #C2571A; the others grey.

LEFT LIST header "Engineering, cheapest first". Nine numbered short lines in two columns, each with a small status dot (teal = has code, grey = not yet):
  "1 Load bundles into IRIS" (teal dot, label "loader written")
  "2 SQL Builder projection" (grey)
  "3 Rules engine + 18 scenarios" (grey)
  "4 Vector tables + Thai embedding test" (grey)
  "5 MCP server, typed tools" (grey)
  "6 Router v3 on new blind set" (grey)
  "7 MedGemma choice + validator" (grey)
  "8 Thai TTS listening test" (grey)
  "9 Decoding benchmark" (grey)

RIGHT BOX header "MVP scope". Two columns "In" (teal header) and "Out" (grey header):
  In: "Low-risk post-MI, clinician-enrolled" · "Walking missions" · "Rules-only stop path" · "FHIR on IRIS for Health"
  Out: "Heart failure, high risk" · "Resistance training" · "Free-text peer community" · "Insurer patient-level data"

FOOTER: "Source: .claude/skills/siriraj-mit-review-panel/references/system-eval.md (gates G-A to G-F); pitch/appendix/A13. No dates committed"

DO NOT: add dates, months or durations; add a budget; add any company or hospital logo; add numbers not listed.
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "Is there a realistic path from this demo to real patients?" |
| Page type | Timeline + stack (mirrors template slide 8: milestone timeline with a spotlight panel) |
| Layout | 6-gate timeline with owners and status, 9-step engineering list, MVP in/out box |
| On-slide words | ≈ 130 |

## On-slide text (exact)

- Breadcrumb: CLINIC + BUSINESS | ROADMAP TO PILOT
- Title: Six gates to a pilot, each passed by a named human; the critical path is people, not code.
- Gates: G-A Prototype – team – IN PROGRESS; G-B Clinician review – cardiologist + rehab physician – OWNER NOT NAMED; G-C Usability – ≥ 8 Thai users aged 55–75 – NOT STARTED; G-D IRB, Thai FDA, PDPA – IRB + lawyers – NOT STARTED; G-E Supervised pilot – clinician + statistician – NOT STARTED; G-F Insurer pilot – insurer + statistician – NOT STARTED
- Engineering, cheapest first: 9 lines as in the prompt (step 1 "loader written")
- MVP scope: In – Low-risk post-MI, clinician-enrolled · Walking missions · Rules-only stop path · FHIR on IRIS for Health; Out – Heart failure, high risk · Resistance training · Free-text peer community · Insurer patient-level data

## Visual spec

- Only G-A is active. The orange G-B circle marks the real blocker: no named clinical owner.
- No dates on purpose; the repo has no committed timeline.

## Speaker notes (Q&A)

The path is six gates, each with a named human who passes it: our prototype gate (rules and red-flag tests plus all 18 scenarios), a written review of limits, stop rules and the Thai red-flag list by a real cardiologist and rehab physician, a moderated usability test with at least 8 Thai users aged 55 to 75, IRB plus written Thai FDA and PDPA answers, a supervised low-risk pilot with pre-written stop rules, and only then an insurer pilot with pre-registered outcomes. The engineering is cheapest first on the InterSystems kit, starting with loading our bundles into IRIS and projecting them with SQL Builder. The critical path is people: we need a named Siriraj clinical owner, and our 12-question reconcile table is ready to send. A small pilot cannot show safety by "zero events", so a statistician sets its size and states what bound it supports.

## Data needed for this page

| Item | Source | Status |
|---|---|---|
| Gates G-A to G-F, exit criteria | `system-eval.md` stage gates, A13 | In repo |
| Current state per gate | A13 "Where we are" | In repo |
| Engineering steps 1–9 | A13 | In repo |
| MVP in/out | A13 | In repo |
| Named clinical owner | — | **Missing (blocks G-B)** |
| Bundles loaded in IRIS (step 1 done?) | `pitch/README.md` open item | **Missing: team to confirm** |
| Dates, budget, pilot size | — | **Missing: not committed; pilot size needs a statistician** |

## Sources in repo

- `pitch/appendix/A13-roadmap-mvp.md`
- `.claude/skills/siriraj-mit-review-panel/references/system-eval.md`
- `research/guidelines/RECONCILE-for-clinician.md`
- `synthetic/load_to_iris.py`, `FHIR-AI-Hackathon-Kit/Tutorials/3-fhir/markdown/3.5-projecting-fhir-data-in-sql.md`
