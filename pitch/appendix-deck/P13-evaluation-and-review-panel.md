# P13 · How will you evaluate it, and who has reviewed it?

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "Safety + tests". PAGE TAG: "A13".

BREADCRUMB: "SAFETY + TESTS | EVALUATION AND REVIEW"
TITLE: "Our own simulated review panel failed the first design, and we fixed what it found."

LAYOUT: four numbered panels in a 2 × 2 grid (each about 860 × 340 px, y=180 to y=900). Footer below.

TOP-RIGHT: orange outlined badge "SIMULATED: language-model reviewers, not clinicians".

PANEL 1 (top-left) header "1 · Seven test layers". A vertical ladder of seven thin stacked bars, each with a code and a short label:
  "L0 Spec vs guidelines"
  "L1 Rules: property tests"
  "L2 Red-flag path"
  "L3 Agent stays in allowed set"
  "L4 Bad watch data"
  "L5 Usability, age 55–75"
  "L6 Staged pilot"
  Bars L1 and L2 are teal with a small badge "RULES ONLY"; the others light grey.

PANEL 2 (top-right) header "2 · Panel result, 17 Oct". Big orange #C2571A word "FAIL" and next to it big number "1.39 / 4" in deep teal with label "combined score, 'not ready' band". Under it three small facts:
  "7 of 7 reviewers: FAIL"
  "0 of 18 scenarios run (no code yet)"
  "Reviewers: cardiology, rehab, nurse, regulatory, AI safety, HCI, market"

PANEL 3 (bottom-left) header "3 · Five S0 findings → fixes" – five rows, arrow between finding and fix:
  "No limit in free week" → "No signed limit, no exercise"
  "Red-flag detection undefined" → "Pre-model screen, measured"
  "Unsupported claims" → "Claims check, safe wording"
  "Guideline numbers conflict" → "12 questions for a clinician"
  "No medication safety" → "Medication → clinician queue"

PANEL 4 (bottom-right) header "4 · Why passing runs is not proof". Big number "20 / 20" with a teal arrow to big orange number "≈ 14%" and the label "a zero-failure run of 20 still allows up to ≈ 14% true failure (95% bound)". Under it one line: "So safety must come from the rules layers."

FOOTER: "Source: evaluation/reviews/2026-10-17-document/SYNTHESIS.md; .claude/skills/siriraj-mit-review-panel/references/system-eval.md. The panel informs; it cannot pass a gate"

DO NOT: draw human reviewer photos or faces; add scores per reviewer; add a "PASS" badge; add numbers not listed.
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "How do you evaluate an agent in a safety setting? Has anyone reviewed this?" |
| Page type | Four numbered panels, market view vs our view (mirrors template slide 17: 4 numbered panels with an evidence panel and big-number tiles) |
| Layout | 2 × 2 grid: layers, panel result, findings → fixes, rule of three |
| On-slide words | ≈ 135 |

## On-slide text (exact)

- Breadcrumb: SAFETY + TESTS | EVALUATION AND REVIEW
- Title: Our own simulated review panel failed the first design, and we fixed what it found.
- Badge: SIMULATED: language-model reviewers, not clinicians
- Panel 1: 1 · Seven test layers; L0 Spec vs guidelines; L1 Rules: property tests; L2 Red-flag path; L3 Agent stays in allowed set; L4 Bad watch data; L5 Usability, age 55–75; L6 Staged pilot
- Panel 2: 2 · Panel result, 17 Oct; FAIL; 1.39 / 4 combined score, "not ready" band; 7 of 7 reviewers: FAIL; 0 of 18 scenarios run (no code yet); Reviewers: cardiology, rehab, nurse, regulatory, AI safety, HCI, market
- Panel 3: 3 · Five S0 findings → fixes; five rows as in the prompt
- Panel 4: 4 · Why passing runs is not proof; 20 / 20 → ≈ 14%; a zero-failure run of 20 still allows up to ≈ 14% true failure (95% bound); So safety must come from the rules layers.

## Visual spec

- "FAIL" is shown proudly: it is evidence of a process that looks for problems.
- Rule of three: 3 / 20 = 0.15; the eval file states "about 14%" (exact 95% upper bound for 0 of 20 is 1 − 0.05^(1/20) ≈ 13.9%).
- Track scores for the speaker: design 1.55, pitch 1.22, combined 1.39 of 4.

## Speaker notes (Q&A)

We test in seven layers; the two that matter most, the rules engine and the red-flag path, are deterministic and get property tests and an 18-scenario suite on every commit, such as "chest feels tight" in Thai and English, HR 40 bpm over the limit, "raise my limit", three days without watch data, and a prompt injection from a partner app. We also ran a simulated panel of seven language-model reviewers on 17 October; all seven returned FAIL with a combined 1.39 of 4, and we fixed each of the five S0 findings in the spec, research notes and pitch wording. This is not clinical validation: no real clinician reviewed it, the panel has not been re-run, and by the rule of three even 20 clean agent runs still allow about a 14% failure rate, so safety has to come from code the agent cannot bypass.

## Data needed for this page

| Number or item | Value | Source | Status |
|---|---|---|---|
| Combined score | 1.39 of 4 ("not ready" band 0–1.4) | `SYNTHESIS.md` line 5 | In repo (simulated) |
| Reviewers | 7, all FAIL | `SYNTHESIS.md`, reviewer files `s1…s4`, `m1…m3` | In repo |
| Scenarios run | 0 of 18 | A07 | In repo |
| S0 findings R1–R5 and fixes | 5 | `SYNTHESIS.md`, A07 | In repo |
| Rule of three ≈ 14% | — | `system-eval.md` | In repo |
| L1/L2 tests and SC-01…18 implemented | — | — | **Missing: scenario suite not built; only 6 UI tests exist (6/6 pass, run 2026-10-18)** |
| Panel re-run after fixes | — | — | **Missing** |
| Real clinician review | — | — | **Missing (gate G-B)** |

## Sources in repo

- `evaluation/reviews/2026-10-17-document/SYNTHESIS.md` and the seven reviewer files in the same folder
- `.claude/skills/siriraj-mit-review-panel/references/system-eval.md`
- `pitch/appendix/A07-safety-and-evaluation.md`
- `tests/safety.test.mjs`, `tests/ui.test.mjs`
