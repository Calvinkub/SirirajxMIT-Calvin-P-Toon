# Neuro-symbolic tool router — experiment plan

Status: **plan v0.1, 2026-10-18. Nothing run yet.** No number in this file is a result.

## Hypothesis (testable)

On CVD Mission Coach tool calls, a cascade of rules, an embedding router, a single-forward-pass tool classifier and grammar-constrained argument filling, with optional activation-based neuron pruning, is:

- **at least 3× faster** per tool call (median wall-clock, same hardware), and
- **non-inferior** in tool-selection accuracy (no more than 1 percentage point worse) and argument exact-match,

compared with the same small LM doing plain native tool calling. Schema-valid output must be 100%.

**Falsified if:** accuracy drops by more than 1 point at every speed setting that reaches 3×, or the speed-up is under 3× at equal accuracy.

## Why this can work (the core idea)

A tool call is mostly *decided*, not *written*. In `{"name":"search_places","arguments":{"type":"park","radius_m":1000,"open_now":true}}` only a few value tokens carry information. Everything else is forced by the schema. So:

1. **Never decode what rules can decide.** The red-flag screen and unambiguous intents are pure rules (microseconds).
2. **Pick the tool in one forward pass, not by generating its name.** Score the closed tool list from the model's next-token distribution (or an embedding router) and stop.
3. **Emit schema tokens without the model** ("jump-forward" over tokens the grammar forces), and mask every non-allowed token for enum arguments (the katgpt-rs `ConstraintPruner` idea: the safety allowed-set *is* the decoding constraint).
4. **Copy, don't generate, free-text arguments** where the value is in the user's words (prompt-lookup speculative decoding: the draft comes from the input text, the model verifies).
5. **Run a smaller network for this one job.** Keep only the MLP neurons that fire on tool-routing prompts (activation statistics on a calibration split), the katgpt-rs `SubstrateGate` "per-capability MLP mask" idea, and check what accuracy it costs.

Honest caveats, written down before running:

- Qwen3 uses SwiGLU (SiLU), not ReLU. Activation sparsity is weaker than in ReLU models, so neuron pruning needs thresholding and may cost accuracy.
- **Unstructured** sparsity gives no speed on MPS or GPU without special kernels. Only **structured** pruning (removing whole neuron rows and columns, so the matmuls get smaller) gives a real speed-up we can measure in PyTorch.
- Tokens/second inflates when the grammar forces tokens. We report **forward passes per tool call** and **wall-clock per call** as primary metrics; tok/s only as secondary, labelled.
- Parts 3 and 4 are known techniques (SGLang jump-forward, XGrammar, prompt-lookup decoding); parts 2 and 5 have prior art too (semantic routers, early exit, Wanda/TEAL-style pruning). The possible novelty is the **combination**: safety rules, allowed-set constraints and a capability-masked model in one deterministic cascade for clinical tool use. A proper novelty check is still to do.

## The cascade (what gets built)

| Tier | What | Cost per call (expected order) | Deterministic? |
|---|---|---|---|
| T0 Rules | Red-flag screen (always first) + keyword/regex router for unambiguous intents | microseconds | yes |
| T1 Embedding router | Multilingual encoder + nearest-centroid over tool exemplars, with a confidence margin gate | ~ms | yes (fixed weights, argmax) |
| T2 One-pass classifier | Small LM, one forward pass, score each tool's name tokens; greedy | 1 forward pass | yes (greedy) |
| T3 Argument filler | Grammar from the tool's JSON schema; jump-forward on forced tokens; allowed-set masks on enums; prompt-lookup drafts for copied text | a few forward passes | yes (greedy) |
| T4 Capability mask | Structured MLP pruning of the T2/T3 model, from activation statistics on the calibration split | smaller forward passes | yes |

A query escalates to the next tier only when the current tier is not confident. Thresholds are tuned on the calibration split only.

## Eval data (the blocker)

| Set | Source | Use |
|---|---|---|
| BFCL v3 `simple` and `multiple` | Public, English, real | General sanity: does the cascade break normal tool calling? |
| **Domain set** | ≥ 300 Thai and English utterances **written by people** (team, mentors, ideally patients), each labelled with tool + arguments; split 50% calibration / 50% test, test never touched during tuning | The real evidence |
| LLM-generated utterances | Synthetic | Plumbing only. Never reported as evidence |

Tools in scope: `search_places`, `search_activities`, `get_heat_index`, `get_pm25`, `get_patient_limits`, `get_recent_activity`, `log_checkin`, plus "no tool" (chit-chat) and "red flag" (must never reach a model).

## Ladder (cheapest first)

| Rung | Run | Hardware | Exit criterion |
|---|---|---|---|
| 0 Baseline | Qwen3-1.7B and Qwen3-4B native tool calling on BFCL simple and the domain test set: tool accuracy, argument exact-match, schema-valid rate, forward passes per call, median and p95 wall-clock | Local Mac (Apple Silicon, MPS, 24 GB) | Baseline reproduces roughly the published BFCL level for that model; harness no-op check passes |
| 1 Frozen cascade | Add T0, T1, T2, T3 one at a time; measure each | Local | Know which tier buys the speed and what it costs |
| 2 Local sweep | T4 sparsity 0 / 25 / 50 / 70%; cascade thresholds; model size 0.6B / 1.7B / 4B | Local | Pareto curve of accuracy vs latency |
| 3 Recover | LoRA on the calibration split to recover pruned accuracy, Thai especially | Rented GPU | Only if Rung 2 shows a gap worth closing |
| 4 Real system | Port to vLLM structured output or katgpt-rs runtime; benchmark on target GPU | Rented GPU | Real latency and throughput numbers for the cost slide |

## Harness correctness check (before any number)

With every tier switched off, the cascade must reproduce the baseline model's tool calls exactly (same greedy outputs) on 50 domain examples. If it does not, the harness has a bug.

## Pre-registered success bar

- Tool-selection accuracy on the domain test set: within 1 point of the baseline.
- Argument exact-match: within 2 points.
- Schema-valid output: 100%.
- Red-flag utterances reaching any model: 0.
- Median wall-clock per tool call: ≥ 3× faster than baseline on the same machine.

## What this will not prove

- No clinical claim of any kind.
- A Mac MPS speed-up is not a production GPU speed-up (that is Rung 4).
- Results on Qwen3 small models do not carry over to MedGemma automatically; MedGemma is not the tool caller in this design.

## Decisions needed from the team

1. Who writes the ≥ 300 domain utterances, and in which language mix?
2. OK to download Qwen3-0.6B, 1.7B and 4B (about 13 GB together) on this Mac for Rungs 0–2?
3. Run the novelty check now, or after Rung 1?
