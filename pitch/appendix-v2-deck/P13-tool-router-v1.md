# P13 · Rules first, then one forward pass: about 18× faster and 36 points more accurate than letting the model write the tool call.

## Key message

On 36 synthetic Thai messages, Qwen3-1.7B writing a native tool call picked the right tool 42% of the time at 1,272 ms median and missed all 4 red flags; with red-flag and medication rules first and then one forward pass that scores the option letters, the same model picked the right tool 78% of the time at 71 ms and missed none. The pattern held at three model sizes: plain tool calling missed 4 of 4 red flags every time, the rules gate missed 0. The numbers come from synthetic data with n = 36, so they show the mechanism, not real-world accuracy, and they are why we ran a blind v2 next (P14).

## Why this matters to the judges

- **Technical coherence.** We measured our own architecture choice rather than asserting it, with provenance (script, data, hardware, date) and pre-written caveats.
- **Innovation.** "Decide, don't generate": scoring a closed tool list in one forward pass behind a rules gate. Routing from a frozen model is prior art; the combination with a rules-only safety gate and FHIR tools in Thai is our contribution.
- **Real-world impact.** A coach that answers in 71 ms instead of 1.3 s feels conversational on a phone, and a gate that stops symptoms before any model is a safety property, not a speed trick.
- **Use of InterSystems technology.** The eight labels are the MCP tools over IRIS for Health (places, activities, heat, PM2.5, limits, recent activity, check-in, none); routing well is what makes FHIR data reachable by voice or chat.

## Full detail

### 1. The question

Most patient messages need one of a few tools or no tool. A tool call such as `{"name":"search_places","arguments":{"type":"park"}}` is mostly decided, not written: only a few tokens carry information. Hypothesis (from `RESULTS_tool_router_demo.md`): "Picking the tool from one forward pass, behind a rules-only safety gate, is much faster than letting a small LLM write the tool call, without losing tool-selection accuracy."

### 2. Setup and provenance

- **Script:** `experiments/tool_router_demo.py` (173 lines).
- **Data:** `synthetic/tool_router_utterances.jsonl`, 72 messages written by the team's assistant, 9 labels × 8: `search_places`, `search_activities`, `get_heat_index`, `get_pm25`, `get_patient_limits`, `get_recent_activity`, `log_checkin`, `none`, `red_flag`.
- **Split by id:** even ids = test (36), odd ids = calibration (36, used only by config D). Counting the file shows the test split is **all Thai** (36 th) and the calibration split **all English** (36 en), with 32 of 36 adjacent pairs sharing the same label and arguments. So config D learned its centroids from English messages and was scored on Thai ones on parallel topics. This is not stated in the results file; we report it here.
- **Decoding:** greedy, float16, Qwen3 thinking disabled; two warm-up calls before timing.
- **Hardware:** Apple Silicon Mac 24 GB, PyTorch 2.8.0, MPS (0.6B); Google Colab Tesla T4, PyTorch 2.11, transformers 5.18 (0.6B, 1.7B, 4B). Cost of the Colab run: about 0.14 compute units.
- **Sanity check:** the baseline parser was checked by hand on 3 messages; low baseline accuracy is model behaviour, not a parser bug. The 0.6B accuracies are identical on Mac and T4, which suggests the harness is deterministic across devices.

### 3. The four configurations

- **A. LLM writes the tool call.** Native Qwen3 tool calling with the 7 tools in the chat template, up to 64 new tokens; the parser reads the `name` field. Missing call = "none".
- **B. One forward pass, score option letters.** The message plus a lettered menu (A–H) in one prompt; the model's next-token logits over the 8 letters pick the tool. No decoding.
- **C. Rules, then B.** A red-flag regex (Thai and English) and a medication regex run first; a red-flag match returns `red_flag`, a medication question returns `none` (it must go to the clinician path, never to tool use). Otherwise B.
- **D. Rules, then nearest centroid.** Same rules; then the mean-pooled last hidden state of the message alone (no menu) is compared with per-tool centroids built from the calibration split.

### 4. Results

Qwen3-1.7B on T4 (the best setting): A 15 of 36 correct (41.7%) at 1,271.7 ms median; B 23 of 36 (63.9%) at 70.8 ms; C 28 of 36 (77.8%) at 71.2 ms; D 13 of 36 (36.1%) at 53.5 ms. A generated 34.2 tokens per call on average; B, C and D used one forward pass (0.9 on average for C and D, because rules decided some messages with no model).

Speed-ups of C over A on the same machine: 17.9× (1.7B T4), 18.5× (0.6B T4), 9.2× (4B T4), 6.4× (0.6B Mac). Accuracy gains of C over A: +36.1 points (1.7B), +19.5 (0.6B), +8.3 (4B).

Red flags: A missed 4 of 4 at every size; B missed 4 of 4 (no rules); C and D missed 0 of 4.

One failure in A shows why the rules-first design exists: asked "วันนี้ฝุ่น PM2.5 เยอะไหม" (is PM2.5 high today?), Qwen3-0.6B answered "currently high" without calling the air-quality tool. That is an invented fact about the patient's environment.

### 5. Reading the results honestly

- **C is the consistent winner.** It was the best or tied-best configuration at 1.7B and 4B and beat A at every size.
- **Bigger is not always better for scoring.** 4B writing calls (61.1%) beat 4B scoring without rules (58.3%); with rules, 4B C reached 69.4%, below 1.7B C (77.8%). With n = 36, differences under about 3 points per message are noise; the 95% interval for 1.7B C is 61.9–88.3% (Wilson) and for 1.7B A 27.1–57.8%, so the C-vs-A gap at 1.7B is larger than the noise but the 1.7B-vs-4B gap for C is not established.
- **D only won at 0.6B** (66.7%) and got worse with size (36.1% at 1.7B, 50.0% at 4B). Mean-pooling the last layer is a weak feature, and the English-calibration / Thai-test split (section 2) makes D a cross-lingual test it was not designed for. D is not the method to pitch.
- **D's speed is not like-for-like.** It reads the message alone, with no tool menu or system prompt, so part of its speed-up is a shorter input.
- **The rules were written by the same person who wrote the messages**, so 0 missed red flags in C and D is optimistic. This was written down before v2, and v2 confirmed it (26 of 30 on a blind set).
- **Only the tool is chosen.** Argument filling (e.g. `{"type":"park"}`) is not implemented or measured.

### 6. What the experiment did and did not test against the pre-registered plan

The plan (`docs/research/neurosymbolic-tool-router-plan.md`) set a bar for the full cascade: tool accuracy within 1 point of the baseline, argument exact-match within 2 points, 100% schema-valid output, 0 red-flag messages reaching any model, ≥ 3× faster median. v1 reached rung 1 of the ladder (frozen-model probe, no training) on synthetic data only. It met the speed bar (C at 6–18× faster) and exceeded the baseline's accuracy rather than merely matching it, but argument filling, schema validity, BFCL sanity runs, neuron pruning and the ≥ 300 human-written domain messages were not done.

### 7. Prior art

Routing tools from a frozen model's own states is published: "The Router Within: Eliciting Native Skill Routing from a Frozen LLM" (Chen et al., arXiv 2609.15982, Sept 2026) uses two trainable linear maps on a frozen LLM's internal states; OATS (Chen et al., arXiv 2603.13426, March 2026) interpolates tool embeddings toward the centroid of queries where each tool succeeded, without LLM inference at serving time. Our contribution is not the routing trick but the combination: a rules-only safety gate in front, allowed-set constraints behind, FHIR tools on IRIS, Thai patients. A formal novelty check is still to do.

### 8. Worked example: Somchai asks about dust

Somchai types "วันนี้ฝุ่น PM2.5 เยอะไหม". In config A the small model may answer from nothing ("currently high"). In config C the red-flag and medication rules do not match, one forward pass scores the 8 options, `get_pm25` wins, and the answer comes from the air-quality tool for his district. If he had typed "เหนื่อยหอบ" (panting), the rules would stop before any model in C and D; in A and B no component knows what a red flag is.

## Visualizations

### Chart 1 · Grouped bar: tool accuracy by configuration and model (synthetic, n = 36 per bar)

- Type: grouped vertical bar; x = configuration A–D; groups = model/device; y = tool accuracy (%). Title: "Rules + one-pass scoring (C) wins at every size".

| Model · device | A writes call | B one-pass | C rules + one-pass | D rules + centroid |
|---|---|---|---|---|
| Qwen3-0.6B · Mac MPS | 22.2 | 30.6 | 41.7 | 66.7 |
| Qwen3-0.6B · T4 | 22.2 | 30.6 | 41.7 | 66.7 |
| Qwen3-1.7B · T4 | 41.7 | 63.9 | **77.8** | 36.1 |
| Qwen3-4B · T4 | 61.1 | 58.3 | 69.4 | 50.0 |

- Annotation: "One message ≈ 2.8 points"; "D calibrated on English, tested on Thai".

### Chart 2 · Bar (log scale): median latency per decision

| Model · device | A (ms) | B (ms) | C (ms) | D (ms) | p95 A (ms) | p95 C (ms) |
|---|---|---|---|---|---|---|
| Qwen3-0.6B · Mac MPS | 2,044.4 | 336.1 | 317.6 | 66.3 | 5,331.0 | 344.8 |
| Qwen3-0.6B · T4 | 991.3 | 53.8 | 53.5 | 53.0 | 2,946.8 | 67.0 |
| Qwen3-1.7B · T4 | 1,271.7 | 70.8 | 71.2 | 53.5 | 3,200.6 | 85.1 |
| Qwen3-4B · T4 | 1,502.2 | 163.6 | 163.8 | 74.9 | 4,655.2 | 168.4 |

- What to notice: writing a call costs 28–34 generated tokens and has a long tail (p95 3–5 s); one-pass scoring is flat.

### Chart 3 · Scatter: accuracy vs median latency (one point per model × config)

Use the two tables above. x = median ms (log), y = accuracy. Highlight 1.7B C (71.2 ms, 77.8%) and 1.7B A (1,271.7 ms, 41.7%) with an arrow "17.9× faster, +36 points".

### Chart 4 · Bar: red flags missed (of 4)

| Config | 0.6B | 1.7B | 4B |
|---|---|---|---|
| A writes call | 4 | 4 | 4 |
| B one-pass, no rules | 4 | 4 | 4 |
| C rules + one-pass | 0 | 0 | 0 |
| D rules + centroid | 0 | 0 | 0 |

- Annotation: "Rules and messages written by the same person (optimistic); blind v2: 26 of 30 (P14)".

### Chart 5 · Bar: speed-up and accuracy gain of C over A

| Model · device | Speed-up (median A / median C) | Accuracy gain (points) |
|---|---|---|
| Qwen3-0.6B · Mac MPS | 6.4× | +19.5 |
| Qwen3-0.6B · T4 | 18.5× | +19.5 |
| Qwen3-1.7B · T4 | 17.9× | +36.1 |
| Qwen3-4B · T4 | 9.2× | +8.3 |

## Numbers and claims ledger

| Claim | Value | Source | Status |
|---|---|---|---|
| Data | 72 messages, 9 labels × 8, test 36 / calibration 36 | `synthetic/tool_router_utterances.jsonl` (counted) | synthetic |
| Test split all Thai, calibration all English; 32/36 pairs share label + args | — | same, counted with python3 | checked (new finding) |
| 1.7B T4 accuracy A/B/C/D | 41.7 / 63.9 / 77.8 / 36.1% | `experiments/tool_router_demo_results_Qwen3-1.7B_cuda.json` | synthetic |
| 1.7B T4 medians A/B/C/D | 1,271.7 / 70.8 / 71.2 / 53.5 ms | same | synthetic |
| 0.6B MPS and T4, 4B T4 values | Charts 1–2 | `…0.6B_mps.json`, `…0.6B_cuda.json`, `…4B_cuda.json` | synthetic |
| Tokens per call in A | 28.3–34.2 | same files | checked |
| Speed-ups and gains | Chart 5 | our arithmetic from the JSON files | checked |
| Wilson 95% intervals | C 1.7B 61.9–88.3%; A 1.7B 27.1–57.8% | our computation | checked |
| Red flags missed A vs C | 4 vs 0 of 4 | all v1 JSON files | synthetic |
| PM2.5 invented answer | Qwen3-0.6B "currently high" | `experiments/RESULTS_tool_router_demo.md` | checked (as reported) |
| Colab cost | ~0.14 compute units | same | as reported |
| Prior art | arXiv 2609.15982, 2603.13426 | abstract pages opened | checked |
| Accuracy on real patient messages | — | — | not shown |

## Limits and open questions

- Synthetic data, n = 36, single author for messages and rules.
- Test split is Thai only and calibration English only; no English test result for v1.
- Only tool selection; argument filling and schema validity not measured.
- No BFCL sanity run, no neuron pruning, no production GPU or vLLM measurement.
- Results do not transfer to MedGemma, which is not the router in this design.
- Novelty check not done.

## Likely judge questions

**Q: 78% is not good enough for patients, is it?**
No, and we do not claim it is. What v1 shows is a comparison on identical messages: the same model is faster and more accurate when it picks rather than writes, and only the rules gate catches red flags. v2 then tested a frozen cascade on a blind set (P14).

**Q: Why is the 4B model worse than 1.7B with scoring?**
With 36 messages one message is about 3 points, so we cannot rank 1.7B and 4B on v1. Both are far faster with scoring than with writing; v2 uses both.

**Q: Isn't this just prompt engineering?**
The speed comes from not decoding: one forward pass and a softmax over 8 letters instead of 28–34 generated tokens. The safety comes from code that runs before the model. Both are architectural, not wording.

**Q: Who else does this?**
Routing from a frozen model's states is published (The Router Within; OATS). We combine it with a deterministic clinical safety gate and FHIR tools for Thai patients.

## Sources

Repo:
- `experiments/tool_router_demo.py`
- `experiments/tool_router_demo_results_Qwen3-0.6B_mps.json`, `…_Qwen3-0.6B_cuda.json`, `…_Qwen3-1.7B_cuda.json`, `…_Qwen3-4B_cuda.json`
- `experiments/RESULTS_tool_router_demo.md`
- `synthetic/tool_router_utterances.jsonl` (counts only)
- `docs/research/neurosymbolic-tool-router-plan.md`
- `pitch/appendix/A06-tool-router-experiments.md`, `pitch/appendix-deck/P11-tool-router-v1.md`

External (opened):
- Chen R. et al. The Router Within: Eliciting Native Skill Routing from a Frozen LLM. arXiv 2609.15982. https://arxiv.org/abs/2609.15982
- Chen H. et al. Outcome-Aware Tool Selection for Semantic Routers (OATS). arXiv 2603.13426. https://arxiv.org/abs/2603.13426
- Qwen3 blog (tool calling, sizes): https://qwenlm.github.io/blog/qwen3/

## Image-generation prompt

A 16:9 information slide on a white background. Key message as title: "Rules first, then one forward pass: about 18× faster and 36 points more accurate." Main chart: a scatter or paired bar for Qwen3-1.7B comparing "model writes the tool call: 41.7% at 1,272 ms" with "rules + one-pass scoring: 77.8% at 71 ms", with an arrow labelled "17.9× faster, +36 points". Secondary small chart: red flags missed of 4, "writes call: 4 at every size" vs "rules first: 0". Footer badge: "synthetic messages, n = 36, Colab T4". Use only these numbers, no logos, no invented figures; ChatGPT chooses the design.
