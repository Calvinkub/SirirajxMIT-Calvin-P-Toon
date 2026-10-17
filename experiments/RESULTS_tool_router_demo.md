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
