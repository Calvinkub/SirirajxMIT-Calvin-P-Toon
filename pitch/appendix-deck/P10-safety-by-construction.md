# P10 · How do you stop the AI from harming a heart patient?

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "Safety + tests". PAGE TAG: "A10".

BREADCRUMB: "SAFETY + TESTS | SAFETY BY CONSTRUCTION"
TITLE: "Red flags and limits are fixed code; no model can set a limit or clear a symptom."

LAYOUT: left panel with the red-flag flow (x=80 to x=880, y=180 to y=880); right panel with a gate table (x=920 to x=1840, y=180 to y=880). Footer below.

LEFT PANEL header "1 · Red flags: rules only, fail closed" with a small shield icon.
  Three input boxes stacked on the left, each with a lineal-colour icon:
    "Symptom tap" (finger-tap icon)
    "Typed or spoken text" (speech-bubble icon)
    "Watch HR above ceiling" (watch icon)
  All three arrows go into one diamond: "Deterministic screen" with teal badge "RULES ONLY" and grey line "Thai + English lexicon".
  From the diamond, two orange #C2571A arrows labelled "match" and "unclear" go to a large orange-outlined STOP box with a stop-hand icon and three lines:
    "Pre-recorded audio: stop now, call 1669"
    "Flag + Communication to clinician"
    "Coaching paused"
  From the diamond, one teal arrow labelled "clear" goes to a grey box "Router and coaching".
  Under the flow, small grey text: "1669 to confirm with a clinician"

RIGHT PANEL header "2 · Panel gates after the first review" – table with 3 columns "Gate", "Status found", "Fix made", 6 rows:
  "G1 Limits" | "FAIL" (orange text) | "No signed limit → no exercise"
  "G2 Red flags" | "NOT DEFINED" (orange text) | "Pre-model screen, measured"
  "G3 Eligibility" | "NOT DEFINED" (orange text) | "ICD, low LVEF → blocked"
  "G4 Claims" | "FAIL" (orange text) | "Claims check, safe wording"
  "G5 Accountability" | "NOT DEFINED" (orange text) | "Consent; owner not yet named"
  "G6 Failure mode" | "NOT DEFINED" (orange text) | "Safe default: last approved or rest"
  Under the table, an orange outlined badge "SIMULATED PANEL · not re-run · no gate claimed as passed".

TAKEAWAY STRIP (pale teal, full width): "The model can only pick from what the rules allow. Missing data means rest, never more."

FOOTER: "Source: design spec §5 rules 1–11; .claude/skills/siriraj-mit-review-panel/references/system-eval.md; evaluation/reviews/2026-10-17-document/SYNTHESIS.md"

DO NOT: use a red cross medical logo or ambulance photo; change any gate status; add percentages; add the word "proven".
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "How do you stop the AI harming a heart patient? Can a bad model output hurt someone?" |
| Page type | Matrix + flow (mirrors template slide 7 grid with a diagram panel; gate statuses as matrix cells) |
| Layout | Red-flag flow on the left, G1–G6 gate table on the right, takeaway strip |
| On-slide words | ≈ 135 (matrix page) |

## On-slide text (exact)

- Breadcrumb: SAFETY + TESTS | SAFETY BY CONSTRUCTION
- Title: Red flags and limits are fixed code; no model can set a limit or clear a symptom.
- Left: 1 · Red flags: rules only, fail closed; inputs Symptom tap / Typed or spoken text / Watch HR above ceiling; Deterministic screen [RULES ONLY] Thai + English lexicon; match / unclear → Pre-recorded audio: stop now, call 1669 · Flag + Communication to clinician · Coaching paused; clear → Router and coaching; "1669 to confirm with a clinician"
- Right: 2 · Panel gates after the first review; 6 rows as in the prompt; badge SIMULATED PANEL · not re-run · no gate claimed as passed
- Takeaway: The model can only pick from what the rules allow. Missing data means rest, never more.

## Visual spec

- "unclear" goes to STOP, same as "match": fail closed is the visible point of the left diagram.
- The gate table shows the honest starting state found by the simulated panel and the fix we made; there is no "PASS" column on purpose.
- Backup list for the speaker (spec §5, rules 1–11): clinician-only limits; RPE/talk test paired with HR; red flags → stop, no LLM; no new limit without a clinician; adherence support, not diagnosis; no exercise without a signed record (free week included); eligibility gate; symptoms never reach the LLM first; no medication advice; safe default; named clinician, PDPA consent, insurer off.

## Speaker notes (Q&A)

The model never writes free arguments and never sets a limit: it returns one mission id, and the server checks that id against the allowed set before any FHIR `Task` is created. Red flags from a tap, typed or spoken text, or the watch go through a deterministic Thai and English screen before any model, and both a match and an unclear result go to the stop path with pre-recorded audio and a clinician flag. Missing data, no network, a model outage or an implausible reading fall back to the last approved mission or rest, never an increase. Our own simulated panel found G1 and G4 failing and four gates undefined; we fixed each in the spec, but the panel has not been re-run and no gate is claimed as passed. A full prompt-injection and MCP threat model is still open.

## Data needed for this page

| Item | Source | Status |
|---|---|---|
| Gate statuses G1–G6 | `evaluation/reviews/2026-10-17-document/SYNTHESIS.md` gate table | In repo (simulated) |
| Fixes per gate | `pitch/appendix/A07-safety-and-evaluation.md` | In repo; rules 6–11 **not yet reviewed by a real clinician** |
| 1669 as the number to show | A01, A07 | **To confirm with a clinician** |
| Thai red-flag phrase list | — | **Missing: must be written and signed by a Thai-speaking clinician** |
| Named clinical owner (G5) | — | **Missing** |
| Threat model (prompt injection, MCP trust) | SYNTHESIS R15 | **Missing** |

## Sources in repo

- `pitch/appendix/A07-safety-and-evaluation.md`
- `docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md` §5
- `.claude/skills/siriraj-mit-review-panel/references/system-eval.md`, `.claude/skills/siriraj-mit-review-panel/references/rubric.md`
- `evaluation/reviews/2026-10-17-document/SYNTHESIS.md`
- `safety.js`, `tests/safety.test.mjs`, `docs/diagrams/backend-architecture.dc.html`
