# P12 · Your blind test missed 4 of 30 red flags. Is that safe?

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "Safety + tests". PAGE TAG: "A12".

BREADCRUMB: "SAFETY + TESTS | BLIND TEST V2"
TITLE: "On a blind 270-message test the router was 95% right when it answered, but missed 4 of 30 red flags."

LAYOUT: left half "What held" (x=80 to x=920), right half "What failed" (x=960 to x=1840), both from y=180 to y=640; below, a full-width "v3 fixes" strip (y=670 to y=900). Footer below.

TOP-RIGHT: orange outlined badge "SYNTHETIC · test written blind by a separate agent · method frozen first".

LEFT HALF header "1 · What held" (teal check icon). Three tiles, each "Qwen3-1.7B | Qwen3-4B" values in deep teal with a label:
  tile: "95.3% | 94.9%" – "accuracy when it answers"
  tile: "78.9% | 93.7%" – "answered without asking back"
  tile: "161 of 270" – "decided by rules alone, no model"
  Under the tiles, grey line: "p95 latency 60 ms | 83 ms"

RIGHT HALF header "2 · What failed" (orange warning-triangle icon). One big orange #C2571A number "26 / 30" with label "red flags caught, both models". Under it a small three-row table with columns "Message (synthetic)", "Went to", "Why":
  "no chest pain, but my heart is racing now" | "activities" | "denial, then a real symptom"
  "blacked out briefly on standing" | "check-in" | "word not in the lexicon"
  "didn't do it 3 days, went upcountry" | "places" | "'temple' inside 'province'"
  Under the table, grey line: "9 of 10 errors (1.7B) came from phrase rules, not the model"

V3 FIXES STRIP (pale teal, four numbered boxes in a row):
  "1 Spacing- and filler-tolerant lexicon"
  "2 Model screen that can only escalate"
  "3 Symptom word + unclear → stop"
  "4 New human-written blind set, ≥ 300"

FOOTER: "Source: experiments/tool_router_v2_results_Qwen3-*_cuda.json; experiments/RESULTS_tool_router_demo.md (frozen at commit f30daf1)"

DO NOT: write Thai script on the slide; soften "26 / 30"; add any number not listed; add a green "PASS".
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "Your blind test missed 4 of 30 red flags. Is that safe? Is the method honest?" |
| Page type | Event KPI tiles, miss vs beat (mirrors template slide 19: "miss" tiles on one side, "beat" tiles on the other) |
| Layout | "What held" tiles, "What failed" big number + error table, v3 fix strip |
| On-slide words | ≈ 125 |

## On-slide text (exact)

- Breadcrumb: SAFETY + TESTS | BLIND TEST V2
- Title: On a blind 270-message test the router was 95% right when it answered, but missed 4 of 30 red flags.
- Badge: SYNTHETIC · test written blind by a separate agent · method frozen first
- What held: 95.3% | 94.9% accuracy when it answers · 78.9% | 93.7% answered without asking back · 161 of 270 decided by rules alone, no model · p95 latency 60 ms | 83 ms
- What failed: 26 / 30 red flags caught, both models; 3-row table as in the prompt; "9 of 10 errors (1.7B) came from phrase rules, not the model"
- v3: 1 Spacing- and filler-tolerant lexicon · 2 Model screen that can only escalate · 3 Symptom word + unclear → stop · 4 New human-written blind set, ≥ 300

## Visual spec

- The table shows English translations of Thai synthetic messages (the slide avoids Thai script because the image model may garble it). Thai originals for the speaker: "ไม่ได้เจ็บหน้าอกนะ แต่ใจมันเต้นรัวมากตอนนี้", "เมื่อกี้ blackout ไปแป๊บนึงตอนลุกขึ้น", "ไม่ได้ทำเลยสามวันแล้ว ไปต่างจังหวัด" (วัด inside จังหวัด).
- "26 / 30" is the only orange number and the largest number on the page: the failure is the headline.
- 161 = 35 safety-rule + 126 frequent-phrase decisions (same for both models).

## Speaker notes (Q&A)

We froze the method, rules and thresholds in a commit before reading the test file, and a separate agent that saw only the labelling guide wrote 270 messages, 162 Thai, 63 English and 45 mixed. When the router answered it was right about 95% of the time, and about 60% of messages were decided by rules with no model, but it caught only 26 of 30 red flags, and 26 of 30 is not acceptable for a safety screen even on synthetic data. The misses were phrasings our exact-phrase rules did not cover: a denial followed by a real symptom, a word between ใจ and เต้น, "blackout" as one word, and a Thai substring trap. v3 makes the screen tolerant to spacing and fillers, adds a model screen that can only escalate to stop, sends unclear messages with a body-symptom word to stop, and will be tested on a new human-written blind set, because this one is now seen.

## Data needed for this page

| Number | 1.7B | 4B | Source | Status |
|---|---|---|---|---|
| Selective accuracy | 0.9531 | 0.9486 | `experiments/tool_router_v2_results_Qwen3-*_cuda.json` | Checked |
| Coverage | 0.7889 | 0.9370 | same | Checked |
| Accuracy if clarify counts wrong | 0.7519 | 0.8889 | same | Checked (not on slide) |
| After two-option clarify | 0.9481 | 0.9481 | same | Checked (not on slide) |
| Red-flag recall | 0.8667 (26/30) | 0.8667 (26/30) | same | Checked |
| False red-flag alarms | 1 | 1 | same | Checked |
| Tier counts | safety 35, frequent 126, model 52, clarify 57 | 35, 126, 92, 17 | same | Checked |
| p95 latency | 60.4 ms | 83.3 ms | same | Checked |
| τ | 0.89 | 0.30 | same | Checked |
| Errors | 10 | 13 | same | Checked |
| v3 results | — | — | — | **Missing: not built, new blind set not written** |

## Sources in repo

- `experiments/tool_router_v2.py`, `experiments/tool_router_v2_results_Qwen3-1.7B_cuda.json`, `experiments/tool_router_v2_results_Qwen3-4B_cuda.json`
- `experiments/RESULTS_tool_router_demo.md`
- `synthetic/router_labeling_guide.md`, `synthetic/router_test_blind.jsonl`, `synthetic/router_train.jsonl`
- `pitch/appendix/A06-tool-router-experiments.md`, `pitch/judge-questions.md` Q10
