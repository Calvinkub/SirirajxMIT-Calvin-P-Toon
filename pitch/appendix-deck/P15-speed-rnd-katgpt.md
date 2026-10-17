# P15 · Can it run faster and cheaper? (R&D track)

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "Cost + speed". PAGE TAG: "A15".

BREADCRUMB: "COST + SPEED | DECODING R&D"
TITLE: "The rule that keeps patients safe can also speed up decoding. We have no MedGemma number yet."

LAYOUT: a four-step pipeline across the top (y=180 to y=430); below it, left a benchmark-plan table (x=80 to x=1000, y=470 to y=900) and right a cascade-status table (x=1040 to x=1840, y=470 to y=900). Footer below.

TOP-RIGHT: a large orange #C2571A outlined tile reading "No MedGemma speed number yet".

PIPELINE (four rounded boxes joined by teal arrows, each with a number, a name and one grey line), then a final teal-filled pill:
  "1 Draft" – "small Gemma 3 proposes tokens"
  "2 Prune" – "drop tokens that break the schema or allowed set"
  "3 Tree" – "valid continuations only"
  "4 Verify" – "MedGemma checks the tree in one pass"
  final pill (white text on teal): "Valid by construction"
  Under the pipeline, grey line: "katgpt-rs: the team's own Rust decoding library (ConstraintPruner, DDTree)"

LEFT TABLE header "Benchmark plan (not run)". Columns "Arm", "Setup". Rows:
  "1" | "vLLM with guided JSON"
  "2" | "+ standard speculative decoding"
  "3" | "+ constraint-pruned trees"
  Under the table: "Measure: p95 latency · valid-output rate · US$ per 1,000 patient-days"

RIGHT TABLE header "Router cascade: measured?" Columns "Tier", "What", "Measured". Rows:
  "T0" | "Rules first" | "Yes" (teal)
  "T1" | "Embedding router" | "No" (grey)
  "T2" | "One-pass classifier" | "Yes" (teal)
  "T3" | "Grammar argument filler" | "No" (grey)
  "T4" | "Capability mask" | "No" (grey)
  Under the table: "Hypothesis: ≥ 3× faster, ≤ 1 point accuracy loss, 100% schema-valid"

FOOTER: "Source: docs/research/neurosymbolic-tool-router-plan.md; docs/pitch/faq-appendix/slides/speed.html. katgpt-rs results come from micro-models, not MedGemma"

DO NOT: show any speed-up multiple or tokens-per-second figure; draw a Rust or Google logo; add numbers not listed.
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "Can this run fast and cheap on your own GPUs? What is technically new?" |
| Page type | Evolution/flow + matrix (mirrors template slide 11 progression diagram with a callout, and slide 7 grid for the status table) |
| Layout | 4-step pipeline + "valid by construction" pill, benchmark-plan table, cascade-status table, orange "no number yet" tile |
| On-slide words | ≈ 120 |

## On-slide text (exact)

- Breadcrumb: COST + SPEED | DECODING R&D
- Title: The rule that keeps patients safe can also speed up decoding. We have no MedGemma number yet.
- Tile: No MedGemma speed number yet
- Pipeline: 1 Draft (small Gemma 3 proposes tokens) → 2 Prune (drop tokens that break the schema or allowed set) → 3 Tree (valid continuations only) → 4 Verify (MedGemma checks the tree in one pass) → Valid by construction; "katgpt-rs: the team's own Rust decoding library (ConstraintPruner, DDTree)"
- Benchmark plan (not run): 1 vLLM with guided JSON; 2 + standard speculative decoding; 3 + constraint-pruned trees; Measure: p95 latency · valid-output rate · US$ per 1,000 patient-days
- Router cascade: T0 Rules first Yes; T1 Embedding router No; T2 One-pass classifier Yes; T3 Grammar argument filler No; T4 Capability mask No; Hypothesis: ≥ 3× faster, ≤ 1 point accuracy loss, 100% schema-valid

## Visual spec

- The orange "No MedGemma speed number yet" tile is deliberate: the page's honesty is the point.
- No numbers from the katgpt-rs README appear anywhere on the slide.

## Speaker notes (Q&A)

MedGemma's output is a short JSON object where almost every token is forced by the schema and the few real choices must come from the allowed set, so the safety constraint is also a decoding constraint. The plan is constraint-pruned speculative decoding: a small Gemma 3 drafts, katgpt-rs's ConstraintPruner drops tokens that break the schema or the allowed set, DDTree builds a tree of valid continuations, and MedGemma verifies in one pass. katgpt-rs is our own modelless Rust library and its published results come from micro-models, so no number transfers to a 27B medical model; we will benchmark three arms on the same GPU and first check that, with pruning switched off, arm 3 reproduces arm 2's outputs exactly. On the router side, rules first and one-pass scoring are measured; the embedding router, grammar argument filler and capability masks are not, and most parts have prior art, so any novelty is in the combination and a formal novelty check is still to do.

## Data needed for this page

| Item | Source | Status |
|---|---|---|
| Pipeline description | `docs/pitch/faq-appendix/slides/speed.html`, katgpt-rs README (outside this repo) | In repo (slide); README not in repo |
| Cascade tiers and measured status | `docs/research/neurosymbolic-tool-router-plan.md`, A09 | In repo |
| Pre-registered hypothesis and falsification rule | same | In repo |
| Gemma 3 drafter tokenizer match with MedGemma | — | **To verify** |
| Any MedGemma latency, p95 or cost per 1,000 patient-days | — | **Missing: benchmark not run** |
| Novelty check | — | **Missing** |

## Sources in repo

- `pitch/appendix/A09-speed-rnd-katgpt.md`
- `docs/research/neurosymbolic-tool-router-plan.md`
- `docs/pitch/faq-appendix/slides/speed.html`, `docs/pitch/faq-appendix/slides/sources.html`
- `experiments/RESULTS_tool_router_demo.md` (measured T0 and T2)
