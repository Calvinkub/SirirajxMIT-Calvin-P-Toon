# Tool router demo — Results (synthetic, hackathon mock-up)

> Every number below comes from **synthetic** messages written for this demo. It shows how the mechanism behaves, not how well it works for real patients.

## Hypothesis

Picking the tool from one forward pass, behind a rules-only safety gate, is much faster than letting a small LLM write the tool call, without losing tool-selection accuracy.

## Ladder rung reached

Rung 1 (frozen-model probe, no training), on synthetic data only. Stopped here by choice: hackathon time box, no real labelled messages yet.

## Provenance

- **Model**: `Qwen/Qwen3-0.6B`, float16, thinking disabled, greedy
- **Data**: `synthetic/tool_router_utterances.jsonl`, 72 Thai and English messages, 9 labels (7 tools, "none", "red_flag"). Split by id: even ids = test (36), odd ids = calibration (36, used only by config D)
- **Command**: `python3 experiments/tool_router_demo.py`; raw output in `experiments/tool_router_demo_results.json`
- **Hardware**: Apple Silicon Mac, 24 GB, PyTorch 2.8.0 on MPS
- **Date**: 2026-10-18

## Sanity check

- Baseline output parsing was checked by hand on 3 messages: the parser reads `<tool_call>` JSON correctly. Low baseline accuracy is the model's behaviour, not a parser bug.
- Two warm-up calls before timing.

## Results (test split, n = 36)

| Config | Tool accuracy | Accuracy excl. red flags | Red flags missed (of 4) | Median ms | p95 ms | Forward passes or tokens per call |
|---|---|---|---|---|---|---|
| A. LLM writes the tool call (native tool calling) | 22% | 25% | 4 | 2,044 | 5,331 | 28.4 generated tokens |
| B. One forward pass, score option letters | 31% | 34% | 4 | 336 | 378 | 1 |
| C. Red-flag and medication rules, then B | 42% | 34% | 0 | 318 | 345 | 0.9 |
| D. Rules, then nearest-centroid on the model's hidden states | 67% | 63% | 0 | 66 | 521 | 0.9 |

Notable failure in A: asked "วันนี้ฝุ่น PM2.5 เยอะไหม" (is PM2.5 high today?), the plain model **answered "currently high" without calling the air-quality tool**, which is an invented fact. This is the behaviour the rules-first design is meant to block.

## Update: three model sizes on a Colab T4 (2026-10-18)

Same script and data, run on Google Colab, Tesla T4, float16, PyTorch 2.11, transformers 5.18. Raw output: `experiments/tool_router_demo_results_Qwen3-*_cuda.json`. The 0.6B accuracies match the Mac run exactly, which suggests the harness is deterministic across devices.

| Model | Config | Tool accuracy | Red flags missed (of 4) | Median ms | p95 ms |
|---|---|---|---|---|---|
| Qwen3-0.6B | A. LLM writes the call | 22% | 4 | 991 | 2,947 |
| Qwen3-0.6B | D. Rules + hidden-state centroid | 67% | 0 | 53 | 58 |
| **Qwen3-1.7B** | A. LLM writes the call | 42% | 4 | 1,272 | 3,201 |
| **Qwen3-1.7B** | **C. Rules + one-pass letter scoring** | **78%** | **0** | **71** | **85** |
| Qwen3-1.7B | D. Rules + hidden-state centroid | 36% | 0 | 54 | 61 |
| Qwen3-4B | A. LLM writes the call | 61% | 4 | 1,502 | 4,655 |
| Qwen3-4B | C. Rules + one-pass letter scoring | 69% | 0 | 164 | 168 |
| Qwen3-4B | D. Rules + hidden-state centroid | 50% | 0 | 75 | 85 |

Best setting on this mock-up: **Qwen3-1.7B with rules + one-pass scoring: 78% at 71 ms median, against 42% at 1,272 ms for the same model writing the tool call (about 18× faster, +36 points).** The hidden-state centroid router (D) only won at 0.6B and got worse with bigger models: mean-pooling the last layer is a weak feature, so D is not the method to pitch. The one-pass letter scoring (C) is the consistent winner.

Cost of this run: about 0.14 Colab compute units.

## Too-good-to-be-true check

- D's ~31× median speed-up partly comes from a much shorter input (the message alone, with no tool menu or system prompt). That is a real property of the design, but it is not a like-for-like kernel comparison.
- The rules (red-flag, medication) were written by the same person who wrote the messages, so C and D's red-flag result is optimistic. Real phrasing will be messier.
- D learns from the calibration split, which comes from the same synthetic writer as the test split. The 67% is likely higher than real-world.
- n = 36: one message moves accuracy by about 3 points.

## Interpretation

On this mock-up, deciding the tool in one forward pass is 6–30× faster than writing the tool call, and routing on hidden states with a few labelled examples is more accurate than both asking the 0.6B model to write the call and asking it to pick a letter. The rules gate catches all red flags here, while the plain model catches none (it has no concept of them). Accuracy is still far too low for real use: a 0.6B model's Thai is weak, and 67% is not good enough.

## What this does and does NOT prove

- **Shown:** the mechanism works end to end on a laptop and is much faster per decision; a plain small LLM can invent answers instead of calling tools.
- **NOT proven:** any accuracy on real patient messages; any result for larger models; argument filling (not implemented here: the demo only picks the tool); neuron pruning (not run); production GPU speed.
- **Prior art:** routing tools from a frozen model's own hidden states is published ("The Router Within", arXiv 2609.15982; OATS centroid tool selection, arXiv 2603.13426). Our contribution is the combination with a rules-only safety gate, allowed-set argument constraints and FHIR tools in a Thai clinical setting, not the routing trick itself.
- **Next rung:** 300+ real Thai and English messages written by people; Qwen3-1.7B / 4B; constrained argument filling; measure on a GPU.

## Router v2 on a blind test set (2026-10-18)

Method frozen in commit `f30daf1` before the test file was read. Test set: 270 synthetic messages (30 per label; 162 Thai, 63 English, 45 mixed) written by a separate agent that saw only the labelling guide. Run on Colab T4. Raw output: `experiments/tool_router_v2_results_Qwen3-*_cuda.json`.

| Model | Accuracy when it answers | Answers itself (coverage) | Accuracy after a two-option question | Red flags caught (of 30) | False red-flag alarms | p95 latency |
|---|---|---|---|---|---|---|
| Qwen3-1.7B | 95.3% | 78.9% | 94.8% | 26 | 1 | 60 ms |
| Qwen3-4B | 94.9% | 93.7% | 94.8% | 26 | 1 | 83 ms |

Median latency is ~0.1 ms because the rules decide 60% of messages without any model.

**Not 99%.** What went wrong (read only after the run):
- 9 of 10 errors with 1.7B come from the frequent-phrase rules, not the model. Example: "อยากไปเดินสวนแต่กลัวจะหนักเกินไปสำหรับหัวใจ" was sent to places by the word "สวน", but it asks about limits. Single keywords are too blunt for mixed intents.
- **4 red flags were not caught** (2 routed wrongly, 2 sent to the clarify question). Phrasings the rules did not cover: "ใจมันเต้นรัว" (a word between ใจ and เต้น), "blackout" as one word, and a denial of one symptom followed by a different real symptom ("ไม่ได้เจ็บหน้าอกนะ แต่ใจเต้นรัว"). **This is the most important finding:** red-flag detection must not depend on exact phrases, and anything near a red flag must fail toward the stop path.
- 1 false alarm: a general question ("เจ็บหน้าอกแบบไหนที่ต้องรีบไปโรงพยาบาล") was treated as a symptom report. For safety that error direction is acceptable.

**Next (v3), with a NEW blind set** (this one is now seen and cannot be reused as evidence):
1. Frequent-phrase rules only accept when the model agrees; disagreement goes to the model or the clarify question.
2. Red-flag screen: symptom lexicon with spacing and filler tolerance, negation scoped to one clause, and a model-based second screen that can only escalate to the stop path, never clear it.
3. Any message sent to "clarify" that contains a body-symptom word goes to the stop path instead.
