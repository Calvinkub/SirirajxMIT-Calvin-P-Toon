# A06 · Did you measure anything? (tool-router experiments)

**One-line answer:** Yes, on synthetic messages only. Putting rules first and then letting a small Qwen3 model score the options in one forward pass was about 18× faster than letting the same model write the tool call (71 ms vs 1,272 ms median) and more accurate (78% vs 42%). On a blind 270-message set, the v2 router was 95% accurate on the messages it answered. **But it caught only 26 of 30 red flags**, and that miss is the most important finding. v3 fixes it with a new blind set.

> **Every number here comes from synthetic messages written for this project.** They show how the mechanism behaves. They are not evidence of accuracy on real patient messages, and they are not a clinical result.

## Why a router at all

Most patient messages need one of a few tools (places, groups, heat, PM2.5, limits, recent activity, check-in) or no tool. A tool call is mostly **decided**, not **written**. So we score a closed list in one forward pass instead of generating JSON token by token, and fixed rules handle red flags and medication questions before any model runs.

Labels: `search_places`, `search_activities`, `get_heat_index`, `get_pm25`, `get_patient_limits`, `get_recent_activity`, `log_checkin`, `none`, and `red_flag` (**rules only, never scored by a model**).

## v1: four configurations, three model sizes

**Provenance.** Script `experiments/tool_router_demo.py`. Data `synthetic/tool_router_utterances.jsonl`: 72 Thai and English messages, 9 labels, 8 per label. Split by id: even = test (36), odd = calibration (36, used only by config D). Greedy, float16, thinking disabled. Mac run: Apple Silicon, 24 GB, PyTorch 2.8.0, MPS. Colab runs: Tesla T4, PyTorch 2.11, transformers 5.18. Two warm-up calls before timing. The parser was hand-checked on 3 messages. Cost of the Colab run: about 0.14 compute units.

Configs: **A** = the LLM writes the tool call (native tool calling). **B** = one forward pass, score the option letters. **C** = red-flag and medication rules, then B. **D** = rules, then nearest-centroid on hidden states.

| Model · device | Config | Tool accuracy | Red flags missed (of 4) | Median ms | p95 ms | Tokens or passes per call |
|---|---|---|---|---|---|---|
| Qwen3-0.6B · Mac MPS | A | 22% | 4 | 2,044 | 5,331 | 28.4 tokens |
| Qwen3-0.6B · Mac MPS | B | 31% | 4 | 336 | 378 | 1 |
| Qwen3-0.6B · Mac MPS | C | 42% | **0** | 318 | 345 | 0.9 |
| Qwen3-0.6B · Mac MPS | D | 67% | **0** | 66 | 521 | 0.9 |
| Qwen3-0.6B · T4 | A | 22% | 4 | 991 | 2,947 | 28.3 tokens |
| Qwen3-0.6B · T4 | D | 67% | **0** | 53 | 58 | 0.9 |
| Qwen3-1.7B · T4 | A | 42% | 4 | 1,272 | 3,201 | 34.2 tokens |
| Qwen3-1.7B · T4 | B | 64% | 4 | 71 | 77 | 1 |
| **Qwen3-1.7B · T4** | **C** | **78%** | **0** | **71** | **85** | 0.9 |
| Qwen3-1.7B · T4 | D | 36% | **0** | 54 | 61 | 0.9 |
| Qwen3-4B · T4 | A | 61% | 4 | 1,502 | 4,655 | 32.1 tokens |
| Qwen3-4B · T4 | C | 69% | **0** | 164 | 168 | 0.9 |
| Qwen3-4B · T4 | D | 50% | **0** | 75 | 85 | 0.9 |

What v1 showed:

- **Config C won consistently.** Qwen3-1.7B went from 42% at 1,272 ms (A) to 78% at 71 ms (C): about 18× faster and +36 points.
- **Plain tool calling missed every red flag** (4 of 4) at every size. With the rules gate in front, 0 were missed.
- **The plain model invented a fact.** Asked "วันนี้ฝุ่น PM2.5 เยอะไหม", Qwen3-0.6B said "currently high" without calling the air-quality tool.
- The 0.6B accuracies match exactly between Mac and T4, which suggests the harness is deterministic across devices.
- D (hidden-state centroid) only won at 0.6B and got worse with bigger models. It is not the method to pitch.

**Too-good-to-be-true checks (written in the results file):** D's speed partly comes from a much shorter input (no tool menu), so it is not a like-for-like kernel comparison. The red-flag rules and the messages were written by the same person, so 0 misses was optimistic. With n = 36, one message moves accuracy by about 3 points.

## v2: blind test, frozen method

**Protocol.**
1. Method, rules and thresholds were frozen in commit `f30daf1` **before the test file was read**.
2. The test set (`synthetic/router_test_blind.jsonl`) was written by a **separate agent that saw only the labelling guide**, not the rules, training set or code.
3. 270 messages: 30 per label. 162 Thai, 63 English, 45 mixed. Colloquial particles, typos, code-mixing, elderly phrasing and boundary cases were requested.
4. Training: `router_train.jsonl` (225) + v1's 72 = 297 rows. The threshold τ was chosen on cross-validated training predictions only: the smallest τ with ≥ 99.5% selective accuracy (1.7B: τ = 0.89; 4B: τ = 0.30).
5. Errors were read **only after** the run.

**Cascade.** Tier 0 safety rules (red flag, medication) → Tier 1 frequent-phrase rules (fire only if exactly one label matches) → one forward pass that gives both letter probabilities and hidden-state features (617-token prompt prefix cached once) → a logistic-regression probe → **answer only if the LLM and the probe agree and the confidence is ≥ τ**, otherwise ask the patient a two-option question.

| Model (Colab T4) | Accuracy when it answers | Coverage (answers itself) | Accuracy if every clarify counts as wrong | Accuracy after a two-option question | Red flags caught (of 30) | False red-flag alarms | p95 latency |
|---|---|---|---|---|---|---|---|
| Qwen3-1.7B | 95.3% | 78.9% | 75.2% | 94.8% | **26** | 1 | 60 ms |
| Qwen3-4B | 94.9% | 93.7% | 88.9% | 94.8% | **26** | 1 | 83 ms |

Where decisions were made (both models): safety rules 35, frequent-phrase rules 126, model 52 (1.7B) or 92 (4B), clarify 57 (1.7B) or 17 (4B). **About 60% of messages (161 of 270) were decided without any model**, so the median latency is about 0.1 ms.

### What went wrong (read after the run)

| Error | Message (synthetic) | Gold → predicted | Cause |
|---|---|---|---|
| Red flag missed | "ไม่ได้เจ็บหน้าอกนะ แต่ใจมันเต้นรัวมากตอนนี้" (no chest pain, but my heart is racing now) | red_flag → search_activities | Denial of one symptom followed by a real one. "ใจมันเต้น" has a word between ใจ and เต้น, so the regex missed it and the "เต้น" (dance) group rule fired |
| Red flag missed | "เมื่อกี้ blackout ไปแป๊บนึงตอนลุกขึ้น" (blacked out briefly on standing) | red_flag → log_checkin | "blackout" as one word was not in the lexicon |
| Red flag missed (4B) | "ปวดหลังร้าวขึ้นมาจากหน้าอก เป็นอยู่ตอนนี้ค่ะ" (back pain spreading from the chest, now) | red_flag → none | Word order not covered. The model then chose "none" |
| Red flags to clarify (1.7B) | 2 messages | red_flag → clarify | Not answered wrongly, but they did not reach the stop path |
| False alarm | "เจ็บหน้าอกแบบไหนที่ต้องรีบไปโรงพยาบาล" (what kind of chest pain needs hospital?) | none → red_flag | General question read as a report. Acceptable direction for safety |
| Medication question misrouted | "หมอให้ยาใหม่มา กินพร้อมยาเดิมได้ไหมคะ" (new drug, can I take it with my old one?) | none → get_patient_limits | Medication rule missed "ยาใหม่". The "หมอ…ให้" (doctor allowed) limits rule fired. A medication question must go to the clinician path |
| Thai substring trap | "ไม่ได้ทำเลยสามวันแล้ว ไปต่างจังหวัด" (didn't do it for 3 days, went upcountry) | log_checkin → search_places | Our reading: "วัด" (temple) matched inside "จังหวัด" (province). Thai has no spaces between words |

**9 of the 10 errors with Qwen3-1.7B came from the frequent-phrase rules, not the model.** Single keywords are too blunt for mixed intents.

## The key lesson

> Red-flag detection must not depend on exact phrases. Anything near a red flag must fail toward the stop path.

26 of 30 is **not acceptable** for a safety screen, even on synthetic data. The v2 blind set is now seen and **cannot be reused as evidence**.

## v3 plan (new blind set)

1. Frequent-phrase rules accept only when the model agrees. Disagreement goes to the model or to the clarify question.
2. Red-flag screen: a symptom lexicon that tolerates spacing and filler words, negation scoped to one clause, and a **model-based second screen that can only escalate to the stop path, never clear a message**.
3. Any message sent to "clarify" that contains a body-symptom word goes to the stop path instead.
4. Thai word segmentation before keyword matching, to avoid substring traps like จังหวัด (our addition after reading the errors).
5. A new blind set, written by people (team, mentors, ideally patients), ≥ 300 Thai and English messages split 50/50 into calibration and test. Red-flag recall is reported with its denominator.

Pre-registered bar for the full cascade (from the plan): tool accuracy within 1 point of the baseline, argument exact-match within 2 points, 100% schema-valid output, **0 red-flag messages reaching any model**, and ≥ 3× faster median than the baseline on the same machine.

## What this does and does not show

| Shown (synthetic) | Not shown |
|---|---|
| The rules-first, one-pass mechanism runs end to end and is much faster per decision | Any accuracy on real patient messages |
| A plain small LLM can invent answers instead of calling tools | Argument filling (only the tool is chosen) |
| Plain tool calling has no concept of red flags | Neuron pruning, production GPU speed, MedGemma behaviour |
| Exact-phrase red-flag rules miss real-world phrasing patterns | That 26 of 30 or any later number is clinically sufficient |

**Prior art:** routing tools from a frozen model's own hidden states is published ("The Router Within", arXiv 2609.15982; OATS centroid tool selection, arXiv 2603.13426). Our contribution is the combination: a rules-only safety gate, allowed-set constraints and FHIR tools in a Thai clinical setting. It is not the routing trick itself. A proper novelty check is still to do.

## Sources / evidence in repo

- `experiments/RESULTS_tool_router_demo.md`: full write-up, provenance, checks, v3 plan
- `experiments/tool_router_demo.py`, `experiments/tool_router_v2.py`: code (v2 rules and τ selection are in the file)
- `experiments/tool_router_demo_results_Qwen3-0.6B_mps.json`, `…_Qwen3-0.6B_cuda.json`, `…_Qwen3-1.7B_cuda.json`, `…_Qwen3-4B_cuda.json`: v1 raw results
- `experiments/tool_router_v2_results_Qwen3-1.7B_cuda.json`, `…_Qwen3-4B_cuda.json`: v2 raw results, tier counts, error list
- `synthetic/router_labeling_guide.md`, `synthetic/router_test_blind.jsonl`, `synthetic/router_train.jsonl`, `synthetic/tool_router_utterances.jsonl`
- `docs/research/neurosymbolic-tool-router-plan.md`: hypothesis, pre-registered bar, ladder
