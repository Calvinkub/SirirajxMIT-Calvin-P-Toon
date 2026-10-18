# P09 · Walk us through what the agent actually does.

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "Agent". PAGE TAG: "A09".

BREADCRUMB: "AGENT | ONE REQUEST, EIGHT STEPS"
TITLE: "Eight steps from one message to a week of FHIR Tasks; the patient chooses, rules bound each step."

LAYOUT: a patient message bubble at the top-left (y=170 to y=240); an eight-step horizontal timeline across the middle (y=270 to y=640); a big funnel number and a result strip below (y=670 to y=900). Footer below.

TOP-RIGHT: an orange outlined badge "SCRIPTED DEMO · SYNTHETIC DATA".

MESSAGE BUBBLE (pale grey, with a small patient icon): "I like golf and football. Plan something for my blood pressure."

TIMELINE: a teal horizontal line with eight numbered circles. Above each circle a short bold name; below each circle one grey line and one coloured tag pill. Tags: teal "RULES", grey "MODEL", teal "FHIR", teal "VECTOR", grey "KNN", orange-outline "PATIENT".
  1 "Safety screen" – "clear · ≈0.1 ms · no model" – tag "RULES"
  2 "Goal" – "likes golf, football; blood pressure" – tag "MODEL"
  3 "Limits + guideline" – "≤ 5.9 METs · HR < 110 · RPE 11–13" – tags "FHIR" and "VECTOR"
  4 "Filter" – "no contact, no breath-holding, no bursts" – tag "RULES"
  5 "Match" – "nearest to what he enjoys, k = 5" – tag "KNN"
  6 "Community" – "groups near home, cool hours" – tag "FHIR"
  7 "Similar users" – "still active at week 4" – tag "KNN"
  8 "Choice + save" – "he picks; Tasks + Provenance" – tags "PATIENT" and "FHIR"

BELOW LEFT: big funnel figure: "100" in deep teal, a teal arrow, "67" in orange #C2571A, with label under it "activities → allowed by the signed limits".

BELOW RIGHT: a strip with two short result lines, each with a small icon:
  red-cross icon: "Football: out (contact, bursts)"
  green-check icon: "Walking golf: in"
  and under them in grey: "Similar-user numbers are invented for the demo"

FOOTER: "Source: demo/agent-flow-demo.html (catalogue and filter counted); patient cmc-p01 is one of the 8 synthetic bundles"

DO NOT: show a real person's face; add percentages for similar users; add numbers not listed; add any step beyond the eight.
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "What does the agent actually do, step by step? Where is the AI?" |
| Page type | Timeline (mirrors template slide 8 milestone timeline) + funnel number (template slide 11 callout "7.6×") |
| Layout | Message bubble, 8-step timeline with technology tags, 100 → 67 funnel, result strip |
| On-slide words | ≈ 110 |

## On-slide text (exact)

- Breadcrumb: AGENT | ONE REQUEST, EIGHT STEPS
- Title: Eight steps from one message to a week of FHIR Tasks; the patient chooses, rules bound each step.
- Badge: SCRIPTED DEMO · SYNTHETIC DATA
- Bubble: I like golf and football. Plan something for my blood pressure.
- Steps 1–8 with lines and tags exactly as in the prompt
- Funnel: 100 → 67 · activities → allowed by the signed limits
- Results: Football: out (contact, bursts) · Walking golf: in · Similar-user numbers are invented for the demo

## Visual spec

- Only two "MODEL"/"KNN"-type steps involve learned or similarity computation; four steps are rules or FHIR reads; the patient makes the decision in step 8.
- 100 → 67 is computed from the demo file: 100 activities; kept if METs ≤ 5.9 and no contact (x), heavy-straining/breath-holding (h) or vigorous-burst (v) flag. Of the 33 removed, 4 are removed by METs alone (walking uphill, tennis doubles, leisurely swimming, recreational trampoline); flags: 6 contact, 7 straining, 25 bursts (overlapping).
- The 3-minute pitch uses the tennis preset (tennis → badminton, bowling, table tennis); this page uses the golf + football preset. Both are in the demo.

## Speaker notes (Q&A)

Rules screen the message for warning symptoms first, in about 0.1 ms with no model; a small router then extracts the goal. The agent reads the signed limits from the FHIR `CarePlan` and four approved ESC 2020 hypertension lines from Vector Search, and rules filter 100 activities down to 67, so football is excluded and the patient is told why. A nearest-neighbour match finds allowed activities closest to golf and football, FHIR finds groups near home at a cool time of day, and the patient picks one option and how often, which is saved as FHIR Tasks with Provenance. Be exact: this is scripted JavaScript, the KNN runs on hand-made 11-dimension tag vectors, MET values are partly estimates, and the similar-user cohort is invented.

## Data needed for this page

| Number | Value | Source | Status |
|---|---|---|---|
| Catalogue size | 100 | `demo/agent-flow-demo.html` `RAW` (counted 2026-10-18) | Checked |
| Allowed | 67 | same, filter `met ≤ 5.9` and no `h/x/v` flag | Checked. **A04 says 99 → 66 (older version of the demo): update A04 or say 100 → 67 consistently** |
| Limits | 5.9 METs, HR 110, RPE 11–13 | `LIMIT` in demo | Synthetic (`cmc-p01`) |
| Screen time | ≈ 0.1 ms | demo trace text; router v2 median 0.1 ms | Demo label; v2 measured median |
| KNN | k = 5, cosine, 11-dim tag vectors | demo code | Hand-made features, not embeddings |
| Similar users | n = 52, percentages | demo `COHORT` | **Invented: never quote as data** |
| Live run against IRIS | — | — | **Not done: scripted in browser** |

## Sources in repo

- `demo/agent-flow-demo.html` (`RAW`, `LIMIT`, `GUIDE`, `COMMUNITY`, `COHORT`, `plan()`)
- `pitch/appendix/A04-agentic-harness.md` (demo flow, honesty notes)
- `pitch/main-3min.md` (demo slide), `pitch/README.md` (click script)
