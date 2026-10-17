# Style guide: Heartstep Q&A appendix deck (P01–P20)

Every page file starts with an "Image-generation prompt" that already contains this style block, so a page can be pasted into ChatGPT image generation on its own. This file is the master copy. If you change the style, change it here and in the `STYLE` paragraph of every page.

## Shared style block (pasted at the start of every page prompt)

> Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

## Tokens

| Token | Value | Use |
|---|---|---|
| `--title` | #12363B | Title, main text, table headers |
| `--accent` | #1B7F7A | Arrows, outlines of key boxes, active tab, "rules only" tags |
| `--highlight` | #C2571A | One key number, warnings ("missed", "to verify", "not yet") |
| `--panel` | #F3F5F6 | Panel and tile fill |
| `--border` | #D9DEE0 | Panel borders, table lines |
| `--muted` | #6B7780 | Breadcrumb, footer, small labels |
| Pastels for icons | #CDEBE8, #F8DCC8, #E6EAEC | Icon fills only |

## Type scale (1920×1080)

| Element | Size | Weight |
|---|---|---|
| Title | 44 px | Semibold, geometric sans (Prompt-like) |
| Panel header | 26 px | Semibold |
| Body | 20–22 px | Regular |
| Big number in a tile | 64–88 px | Bold, deep teal (or orange for the one highlight) |
| Tile label | 18 px | Regular |
| Breadcrumb, footer, nav | 15–20 px | Regular, grey |

## Tags and badges (used across pages)

| Badge text | Fill | Meaning |
|---|---|---|
| "RULES ONLY" | teal outline, pale teal fill | Deterministic code, no model |
| "MODEL" | grey outline, pale grey fill | An open model does this step |
| "FHIR" / "VECTOR" / "SQL" | teal fill, white text | IRIS for Health capability |
| "SYNTHETIC" | orange outline, white fill, orange text | Synthetic data |
| "SIMULATED" | orange outline | Language-model review panel |
| "ESTIMATE" | orange outline | Not measured |
| "PLANNED" | grey dashed outline | Not built yet |
| "BUILT" | teal fill | Exists in the repo |
| "TO VERIFY" | orange text | Unchecked fact |

## Page frame (from the template)

1. Breadcrumb `SECTION | TOPIC` → title as a claim → 2–4 numbered panels → takeaway box → source line → nav strip → page tag.
2. Each key number sits in its own tile: big number, one-line label, one-line context.
3. Charts are flat bars with the value printed on or above each bar; no gridlines; estimates and synthetic data are labelled on the chart itself.
4. Diagrams are rounded boxes with a 1–3-word name and one short line, connected by teal arrows; groups get a bracket with a badge.
5. At most ≈ 110 words of on-slide text (≈ 140 on matrix pages). Everything else goes to speaker notes.

## Nav tab per page

| Tab | Pages |
|---|---|
| Why us | P01, P20 |
| IRIS + FHIR | P02–P07 |
| Agent | P08, P09 |
| Safety + tests | P10–P13 |
| Cost + speed | P14, P15 |
| Clinic + business | P16–P19 |

## Never on any slide

Company or product logos (InterSystems, Qwen, Google, OpenAI, Anthropic, Apple, Samsung), photos of real people, real hospital names other than in a source line, invented numbers, decorative stock charts, the words "proven", "optimal", "clinically validated", "prescription", "diagnose".
