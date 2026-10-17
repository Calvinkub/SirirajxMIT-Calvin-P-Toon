# P01 · Why not just ask ChatGPT or Claude?

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "Why us". PAGE TAG: "A01".

BREADCRUMB (top-left): "WHY US | VS A GENERAL CHATBOT"
TITLE (top-left, two lines max): "A chatbot answers when asked. Our agent acts first, inside the doctor's signed limits."

LAYOUT: two side-by-side panels in the upper two thirds (y=190 to y=640), then a row of three number tiles (y=670 to y=880), then the footer.

LEFT PANEL (x=80 to x=700, light grey fill #F3F5F6, header "General chatbot" in 26 px deep teal, small grey speech-bubble icon in lineal colour style next to the header). Inside, a vertical chain of three rounded boxes joined by grey arrows pointing down:
  box 1: "Patient asks"
  box 2: "Model decides facts, safety and tone"
  box 3: "Answer"

RIGHT PANEL (x=760 to x=1840, white fill with a 3 px teal #1B7F7A border, header "Heartstep" in 26 px deep teal, small heart-with-shield icon in lineal colour style). Inside, a horizontal chain of five rounded boxes joined by teal arrows pointing right:
  box 1: "Scheduler or message"
  box 2: "Red-flag screen" with a small teal badge under it reading "RULES ONLY"
  box 3: "Allowed set from signed CarePlan" with a small teal badge "FHIR"
  box 4: "Model picks ONE id" with a small grey badge "MODEL"
  box 5: "Task + Provenance in IRIS" with a small teal badge "FHIR"
  From box 2 a short orange #C2571A arrow goes down to an orange-outlined pill reading "Stop · call 1669".

ROW OF THREE TILES (equal width, light grey fill, rounded). Above the row, a small orange outlined badge reading "SYNTHETIC TEST · n = 36 per run".
  tile 1: big number "4 of 4" in orange #C2571A; label "red flags missed when the model writes the tool call"
  tile 2: big number "0 of 4" in deep teal; label "missed with the rules in front"
  tile 3: big word "PM2.5" in deep teal; label "small model said 'currently high' without calling the tool"

TAKEAWAY STRIP (y=895 to y=950, pale teal fill #CDEBE8, deep teal text): "Not a smarter model. A bounded one."

FOOTER SOURCE LINE (bottom-left, y=972): "Source: experiments/RESULTS_tool_router_demo.md (Qwen3 0.6B/1.7B/4B, synthetic); OpenAI 'Launching Health in ChatGPT' (US, Jul 2026)"

DO NOT: draw any OpenAI, Anthropic, ChatGPT or Claude logo; add any other numbers or percentages; add extra text or captions; use photos.
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "Why not just ask ChatGPT or Claude?" |
| Page type | Variant perception (mirrors template slide 12: "market view" chain on the left vs "our view" on the right, KPI tiles under it) |
| Layout | Two panels (chatbot chain vs our chain) + three KPI tiles + takeaway strip |
| On-slide words | ≈ 85 |

## On-slide text (exact)

- Breadcrumb: WHY US | VS A GENERAL CHATBOT
- Title: A chatbot answers when asked. Our agent acts first, inside the doctor's signed limits.
- Left panel "General chatbot": Patient asks → Model decides facts, safety and tone → Answer
- Right panel "Heartstep": Scheduler or message → Red-flag screen [RULES ONLY] → Allowed set from signed CarePlan [FHIR] → Model picks ONE id [MODEL] → Task + Provenance in IRIS [FHIR]; branch: Stop · call 1669
- Badge: SYNTHETIC TEST · n = 36 per run
- Tile 1: 4 of 4 · red flags missed when the model writes the tool call
- Tile 2: 0 of 4 · missed with the rules in front
- Tile 3: PM2.5 · small model said "currently high" without calling the tool
- Takeaway: Not a smarter model. A bounded one.
- Source line as in the prompt.

## Visual spec

- Left chain is grey and vertical (passive); right chain is teal and horizontal (a pipeline). The contrast is the message.
- The only orange items: tile 1 number and the "Stop · call 1669" pill.
- Tiles report v1 config A vs config C. "4 of 4" holds for every model size tested (0.6B Mac and T4, 1.7B T4, 4B T4). The PM2.5 example is Qwen3-0.6B.

## Speaker notes (Q&A)

General models are strong reasoners, and both OpenAI and Anthropic now connect health records for US users, so we do not claim a smarter model. Our claim is that the model is bounded: limits come from a clinician-signed FHIR `CarePlan`, rules decide safety before any model runs, the app pushes one or two missions at a time the patient chose, it works in Thai, and the care team sees flags and an audit trail. In our synthetic router test, a plain small model writing the tool call missed all 4 red-flag messages at every size and once invented a PM2.5 answer; with the rules gate in front, 0 of 4 were missed. That shows the failure mode, not real-world accuracy.

## Data needed for this page

| Number or claim | Value | Source | Status |
|---|---|---|---|
| Red flags missed, config A | 4 of 4 (all models) | `experiments/tool_router_demo_results_*.json` (`red_flag_missed` = 4) | Checked |
| Red flags missed, config C | 0 of 4 | same files | Checked |
| Test size | n = 36 per run | same files (`n`: 36) | Checked |
| PM2.5 invented answer | Qwen3-0.6B, "currently high" | `experiments/RESULTS_tool_router_demo.md`, A01 | From write-up |
| ChatGPT Health US-only | OpenAI, July 2026 | `docs/pitch/faq-appendix/slides/chatbot.html` | **To verify** before quoting (A01 "limits of this answer") |
| Missing | — | — | None blocking |

## Sources in repo

- `pitch/appendix/A01-why-not-chatgpt.md`
- `docs/pitch/faq-appendix/slides/chatbot.html`
- `experiments/RESULTS_tool_router_demo.md`, `experiments/tool_router_demo_results_Qwen3-*_cuda.json`, `experiments/tool_router_demo_results_Qwen3-0.6B_mps.json`
- `pitch/judge-questions.md` Q6
