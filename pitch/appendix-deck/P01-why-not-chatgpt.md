# P01 · Why not just ask ChatGPT or Claude?

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "Why us". PAGE TAG: "A01".

BREADCRUMB (top-left): "WHY US | VS A GENERAL CHATBOT"
TITLE (top-left, two lines max): "A general chatbot gives advice. Heartstep recommends what you will enjoy, inside your doctor's care plan."

LAYOUT: two side-by-side panels in the upper two thirds (y=190 to y=640), then a row of three number tiles (y=670 to y=880), then the footer.

LEFT PANEL (x=80 to x=640, light grey fill #F3F5F6, header "General chatbot" in 26 px deep teal, small grey speech-bubble icon in lineal colour style next to the header). Inside, a vertical chain of three rounded boxes joined by grey arrows pointing down:
  box 1: "You ask a question"
  box 2: "Model writes advice from memory"
  box 3: "Same tips for everyone"

RIGHT PANEL (x=700 to x=1840, white fill with a 3 px teal #1B7F7A border, header "Heartstep: like Netflix for a healthy heart" in 26 px deep teal, small heart icon with a play-button triangle in lineal colour style). Inside, three horizontal "Netflix-style" rows of small rounded activity cards (each card a pastel rectangle with a tiny lineal icon and a one-word label), each row with a row title on its left:
  row 1 title: "Because you loved tennis" — cards: "Badminton", "Table tennis", "Bowling"
  row 2 title: "Popular with people like you" — cards: "Walking group", "Tai chi", "Petanque"
  row 3 title: "Groups near you this week" — cards: "Badminton club 1.9 km", "Bowling league 3.2 km"
  Under the three rows, a thin teal bar with a small shield icon reading "Only activities inside your signed care plan · warning symptoms stop by rules".

ROW OF THREE TILES (equal width, light grey fill, rounded):
  tile 1: big text "100 → 67" in deep teal; label "activities in the catalogue that fit the care plan"
  tile 2: big text "3 signals" in deep teal; label "your taste · people like you · near you"
  tile 3: big text "0 of 4" in orange #C2571A; label "red flags missed with rules in front (synthetic test)"

TAKEAWAY STRIP (y=895 to y=950, pale teal fill #CDEBE8, deep teal text): "Recommendations you enjoy, a community to join, inside a safe plan."

FOOTER SOURCE LINE (bottom-left, y=972): "Source: demo/agent-flow-demo.html (synthetic patient and places); experiments/RESULTS_tool_router_demo.md (synthetic)"

DO NOT: draw any OpenAI, Anthropic, ChatGPT, Claude or Netflix logo; use Netflix red or its typeface; add any other numbers or percentages; add extra text or captions; use photos.
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "Why not just ask ChatGPT or Claude?" |
| Page type | Variant perception (template slide 12: "market view" on the left vs "our view" on the right, KPI tiles under it) |
| Layout | Two panels (general chatbot chain vs Netflix-style recommendation rows) + three KPI tiles + takeaway strip |
| On-slide words | ≈ 100 |

## On-slide text (exact)

- Breadcrumb: WHY US | VS A GENERAL CHATBOT
- Title: A general chatbot gives advice. Heartstep recommends what you will enjoy, inside your doctor's care plan.
- Left panel "General chatbot": You ask a question → Model writes advice from memory → Same tips for everyone
- Right panel "Heartstep: like Netflix for a healthy heart":
  - Because you loved tennis: Badminton · Table tennis · Bowling
  - Popular with people like you: Walking group · Tai chi · Petanque
  - Groups near you this week: Badminton club 1.9 km · Bowling league 3.2 km
  - Bar: Only activities inside your signed care plan · warning symptoms stop by rules
- Tile 1: 100 → 67 · activities in the catalogue that fit the care plan
- Tile 2: 3 signals · your taste · people like you · near you
- Tile 3: 0 of 4 · red flags missed with rules in front (synthetic test)
- Takeaway: Recommendations you enjoy, a community to join, inside a safe plan.

## Visual spec

- Left: grey, vertical, generic. Right: teal frame with three horizontal rows of cards, like a streaming app's home screen, but in the deck's palette (no Netflix branding or red).
- Orange only on tile 3.
- The recommendation rows map to the demo's signals: KNN on the patient's liked activities ("Because you loved…"), the similar-user cohort ("Popular with people like you"), and FHIR `HealthcareService` near home ("Groups near you").

## Speaker notes (Q&A)

We are a chat coach too, but a general chatbot answers from memory and gives everyone the same tips. Heartstep works like a recommender: it starts from a catalogue of 100 activities, keeps only the 67 that fit the doctor's signed care plan, then ranks them by what you enjoyed, what people like you kept doing, and what groups meet near you. The patient chooses, and the plan is saved as FHIR. Safety stays outside the model: in our synthetic test, rules in front caught all 4 red-flag messages that a plain small model missed.

## Data needed for this page

| Number or claim | Value | Source | Status |
|---|---|---|---|
| Catalogue and filter | 100 → 67 | `demo/agent-flow-demo.html` (catalogue + filter MET ≤ 5.9, no contact/straining/bursts) | Checked (synthetic limits) |
| Top picks for the tennis example | Bowling, table tennis, badminton | headless run of the demo (preset 1) | Checked |
| Group distances | 1.9 km, 3.2 km | `demo/agent-flow-demo.html` COMMUNITY (synthetic) | Synthetic |
| Red flags, rules in front | 0 of 4 | `experiments/tool_router_demo_results_*.json` | Checked (synthetic) |
| "Popular with people like you" items | Walking group, tai chi, petanque | illustrative; cohort numbers are synthetic | Label as example |
| Missing | real cohort data for collaborative filtering | — | Needed for a pilot |

## Sources in repo

- `demo/agent-flow-demo.html`
- `pitch/appendix/A01-why-not-chatgpt.md`, `pitch/appendix/A04-agentic-harness.md`
- `experiments/RESULTS_tool_router_demo.md`
