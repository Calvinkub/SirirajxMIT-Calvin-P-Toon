# P11 · Did you measure anything? (tool-router v1)

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "Safety + tests". PAGE TAG: "A11".

BREADCRUMB: "SAFETY + TESTS | TOOL-ROUTER EXPERIMENT V1"
TITLE: "Choosing the tool in one forward pass was about 18× faster and more accurate than writing the call."

LAYOUT: a row of three KPI tiles on top (y=180 to y=380); below, left a bar chart (x=80 to x=1080, y=410 to y=900) and right a small comparison table (x=1120 to x=1840, y=410 to y=900). Footer below.

TOP-RIGHT: orange outlined badge "SYNTHETIC · 36 test messages · Colab T4".

KPI TILES (light grey, rounded; each tile shows "A vs B" with the better value in deep teal and the worse in grey, and a one-line label):
  tile 1: "71 ms" vs "1,272 ms" – label "median time per decision, Qwen3-1.7B"
  tile 2: "78%" vs "42%" – label "tool accuracy, same 36 messages"
  tile 3: "0" vs "4" – label "red flags missed, of 4" (the "4" in orange #C2571A)

BAR CHART title: "Qwen3-1.7B on T4: accuracy by method". Four vertical flat bars, value printed above each bar, a second grey line under each bar label with median time:
  "A · model writes the call" 42% – under it "1,272 ms" (bar grey)
  "B · one-pass scoring" 64% – "71 ms" (bar light teal)
  "C · rules, then one-pass" 78% – "71 ms" (bar teal #1B7F7A, outlined, the highlight)
  "D · rules, then centroid" 36% – "54 ms" (bar light grey)
  No gridlines, no y-axis numbers.

COMPARISON TABLE title: "Same pattern at every size (A → C)". Columns "Model", "Accuracy", "Median ms". Rows:
  "0.6B · Mac" | "22% → 42%" | "2,044 → 318"
  "1.7B · T4" | "42% → 78%" | "1,272 → 71"
  "4B · T4" | "61% → 69%" | "1,502 → 164"

TAKEAWAY STRIP (pale teal): "Decide, don't write: rules first, then one pass. One message moves accuracy by about 3 points."

FOOTER: "Source: experiments/tool_router_demo_results_Qwen3-*.json; experiments/RESULTS_tool_router_demo.md. Not evidence of accuracy on real patient messages"

DO NOT: add error bars or confidence intervals; add numbers not listed; call the result "proven" or "state of the art"; add model logos.
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "Did you measure anything? Is 78% good enough?" |
| Page type | Event KPI tiles + bar chart (mirrors template slide 19 "A vs B" tiles and slide 20 "X vs Y" comparison, with a drawn bar chart like slide 3) |
| Layout | 3 "A vs B" tiles, 4-bar chart, 3-row comparison table |
| On-slide words | ≈ 110 |

## On-slide text (exact)

- Breadcrumb: SAFETY + TESTS | TOOL-ROUTER EXPERIMENT V1
- Title: Choosing the tool in one forward pass was about 18× faster and more accurate than writing the call.
- Badge: SYNTHETIC · 36 test messages · Colab T4
- Tiles: 71 ms vs 1,272 ms (median time per decision, Qwen3-1.7B) · 78% vs 42% (tool accuracy, same 36 messages) · 0 vs 4 (red flags missed, of 4)
- Chart: A · model writes the call 42% (1,272 ms); B · one-pass scoring 64% (71 ms); C · rules, then one-pass 78% (71 ms); D · rules, then centroid 36% (54 ms)
- Table: 0.6B · Mac 22% → 42%, 2,044 → 318; 1.7B · T4 42% → 78%, 1,272 → 71; 4B · T4 61% → 69%, 1,502 → 164
- Takeaway: Decide, don't write: rules first, then one pass. One message moves accuracy by about 3 points.

## Visual spec

- 18× = 1,271.7 / 71.2 ≈ 17.9, rounded to "about 18×".
- The 0.6B row is the Mac MPS run (the 0.6B T4 run gives the same accuracies: 22% A, 42% C; medians 991 and 54 ms).
- D got worse as models grew (67% at 0.6B, 36% at 1.7B, 50% at 4B); it is shown but not pitched.

## Speaker notes (Q&A)

No, 78% is not good enough, and every message is synthetic; what we stand behind is the comparison on the same 36 messages. When Qwen3-1.7B wrote the tool call it was right 42% of the time at 1,272 ms median and missed all 4 red flags; with red-flag and medication rules first and then one forward pass scoring the option letters, it was right 78% of the time at 71 ms and missed none. Caveats written before we saw results: the same person wrote the rules and the messages, so 0 misses was optimistic, and with n = 36 one message moves accuracy by about 3 points. That is why we ran a blind v2 next. Routing from a frozen model is prior art ("The Router Within", OATS); our contribution is the rules-only gate, allowed-set constraints and FHIR tools in a Thai clinical setting.

## Data needed for this page

| Number | Value | Source | Status |
|---|---|---|---|
| 1.7B T4 A/B/C/D accuracy | 41.7 / 63.9 / 77.8 / 36.1% | `experiments/tool_router_demo_results_Qwen3-1.7B_cuda.json` | Checked |
| 1.7B T4 medians | 1,271.7 / 70.8 / 71.2 / 53.5 ms | same | Checked |
| 0.6B Mac A→C | 22.2% → 41.7%, 2,044.4 → 317.6 ms | `…Qwen3-0.6B_mps.json` | Checked |
| 4B T4 A→C | 61.1% → 69.4%, 1,502.2 → 163.8 ms | `…Qwen3-4B_cuda.json` | Checked |
| Red flags missed A vs C | 4 vs 0 (of 4) | all v1 files | Checked |
| Data | 72 messages, 9 labels, 36 test / 36 calibration | `synthetic/tool_router_utterances.jsonl`, A06 | In repo |
| Novelty check | — | A06 | **Missing: formal novelty check not done** |

## Sources in repo

- `experiments/tool_router_demo.py`, `experiments/tool_router_demo_results_Qwen3-0.6B_mps.json`, `…0.6B_cuda.json`, `…1.7B_cuda.json`, `…4B_cuda.json`
- `experiments/RESULTS_tool_router_demo.md`
- `pitch/appendix/A06-tool-router-experiments.md`, `pitch/judge-questions.md` Q8
