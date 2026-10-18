# P17 · The rule that keeps Somchai safe can also make decoding faster; we have measured the router, not MedGemma

## Key message

Heartstep's models never write free advice: they pick an id from a set the rules already allowed, so most output tokens are forced and the few real choices come from a short list. That safety constraint is also a decoding constraint, which is the basis of our R&D track: constraint-pruned speculative decoding with the team's own Rust library, katgpt-rs. The cheap end of this idea is measured on synthetic data (one-pass tool choice: 71 ms vs 1,272 ms median on a T4); the MedGemma end is not benchmarked, and katgpt-rs is modelless, so none of its published numbers apply to MedGemma.

## Why this matters to the judges

- **Innovation.** Most teams treat safety and speed as a trade-off. Here one mechanism, the allowed set from the rules engine, gives both: a model that cannot emit an out-of-limit activity also wastes no compute considering one.
- **Technical coherence.** The R&D track is not a side project. It plugs into the same allowed set the IRIS-backed rules engine computes from FHIR (P06, P12), and into the cost model on P16.
- **Honesty under questioning.** Technical judges will ask "how much faster?". The answer on this page separates measured router numbers (synthetic data, small Qwen3 models) from an unrun MedGemma benchmark, and says what would falsify the idea.

## Full detail

### The idea: decide, don't write

In Heartstep the agent's model output is short and structured. For Somchai the choice step returns something like `{"activity_id": "badminton-social", "reason_codes": ["like-tennis", "within-limits"]}`. The braces, keys, quotes and commas are fixed by a JSON schema. The only free tokens are the values, and those values must come from sets the system already knows:

- `activity_id` must be one of the **67 activities** that passed the rules filter for Somchai (100 in the catalogue; 29 dropped for exceeding his synthetic 5.9 MET cap and 4 for contact or breath-holding flags; computed from `demo/agent-flow-demo.html`).
- `reason_codes` must come from a fixed code list.

A normal decoder still runs the full model over the full vocabulary for every one of those tokens, including the ones that have only one legal value. Constrained decoding (for example vLLM guided JSON) removes illegal tokens but still spends one forward pass per token. Our proposal goes one step further: let a small draft model propose several tokens ahead, throw away every draft branch that breaks the schema or leaves the allowed set, and ask the large model to verify the surviving tree in one pass.

### The four-step pipeline

| Step | What happens | Component |
|---|---|---|
| 1 Draft | A small Gemma 3 model proposes the next few tokens (same family as MedGemma; tokenizer match still to verify) | draft model |
| 2 Prune | Drop every drafted token that breaks the JSON schema or names an activity outside today's allowed set | katgpt-rs `ConstraintPruner`; `spec_pruner` compiles a spec into a token constraint |
| 3 Tree | Build a tree of valid continuations only | katgpt-rs `DDTree` |
| 4 Verify | MedGemma scores the tree in one forward pass and accepts the longest valid prefix it agrees with | target model |

The katgpt-rs README describes exactly this core pipeline: "LLM drafts logits → ConstraintPruner filters invalid → DDTree builds valid-only tree → Target verifies". For us the "specification" handed to the pruner is the JSON schema plus Somchai's allowed set, which the rules engine computed from his signed `CarePlan` limit record in IRIS.

**Why it fits this product and not every product:** our outputs are short, mostly forced, and already constrained for safety. A chatbot writing long free text gains little from this; a recommender picking one id from 67 can gain a lot. Whether it does is the benchmark.

### What katgpt-rs is, and what it is not

katgpt-rs is the team's own MIT-licensed Rust library of decoding primitives, started on 2026-05-04 (first commit in its own repository) and therefore **reused prior work, not built at this event** (P22). Its README lists primitives we would use: the `ConstraintPruner` trait, `DDTree` best-first draft trees, speculative decoding, `SubstrateGate` ("Inference-time capability substrate routing via MLP masks"), and `spec_pruner` ("Modelless spec-to-constraint O(1) RoaringBitmap compilation").

The README is also explicit that "katgpt-rs is modelless (no model loader)". Its headline results come from micro-models (the reference architecture has a 27-token vocabulary, 16-dimensional embeddings and one layer) and constraint puzzles such as Sudoku. **We quote none of those numbers for Heartstep.** They are evidence that the primitives work as algorithms, not that MedGemma 27B runs faster. A real-model result would come from a port into a serving stack (vLLM structured output or a katgpt-rs runtime) on a rented GPU.

### What is already measured: the cheap end of the same idea

The tool router is the same principle at small scale: choose from a closed list in one forward pass instead of generating the choice token by token. These runs are real measurements on **synthetic** messages.

**Router v1** (72 synthetic Thai and English messages, test n = 36, Colab Tesla T4, float16, greedy; `experiments/RESULTS_tool_router_demo.md`):

| Model | Config | Tool accuracy | Median ms | p95 ms | Red flags missed (of 4) |
|---|---|---|---|---|---|
| Qwen3-0.6B | A. LLM writes the tool call | 22% | 991 | 2,947 | 4 |
| Qwen3-0.6B | D. Rules + hidden-state centroid | 67% | 53 | 58 | 0 |
| Qwen3-1.7B | A. LLM writes the tool call | 42% | 1,272 | 3,201 | 4 |
| Qwen3-1.7B | C. Rules + one-pass letter scoring | 78% | 71 | 85 | 0 |
| Qwen3-4B | A. LLM writes the tool call | 61% | 1,502 | 4,655 | 4 |
| Qwen3-4B | C. Rules + one-pass letter scoring | 69% | 164 | 168 | 0 |

The best setting, Qwen3-1.7B with rules plus one-pass scoring, was about 18× faster at the median (1,272 / 71) and 36 points more accurate than the same model writing the call. The plain model also invented an answer ("currently high") to a PM2.5 question instead of calling the air-quality tool, which is the failure the rules-first design blocks.

**Router v2** (method frozen in commit `f30daf1` before the blind set was read; 270 synthetic messages written by a separate agent; T4): rules decided 161 of 270 messages without any model, median latency about 0.1 ms, p95 60 ms (1.7B) and 83 ms (4B), selective accuracy 95.3% and 94.9%. It also missed 4 of 30 red flags, which is why red-flag handling moves to a fail-closed lexicon in v3 (P14).

### The full cascade plan, and what has been measured

| Tier | What | Measured? |
|---|---|---|
| T0 Rules | Red-flag screen first, then keyword rules for unambiguous intents | Yes (v1, v2) |
| T1 Embedding router | Multilingual encoder + nearest centroid with a margin gate | No |
| T2 One-pass classifier | Score the closed tool list from one forward pass | Yes (v1 config C, v2) |
| T3 Argument filler | Grammar from the tool schema; jump-forward over forced tokens; allowed-set masks on enums; prompt-lookup drafts for copied text | No |
| T4 Capability mask | Structured MLP pruning from activation statistics (the `SubstrateGate` idea) | No |

**Pre-registered hypothesis** (`docs/research/neurosymbolic-tool-router-plan.md`): the cascade is at least 3× faster per tool call (median wall-clock, same hardware) and non-inferior on tool accuracy (no more than 1 point worse), with 100% schema-valid output and 0 red-flag messages reaching any model. **Falsified if** accuracy drops by more than 1 point at every setting that reaches 3×, or the speed-up is under 3× at equal accuracy.

### The MedGemma benchmark (designed, not run)

| Arm | Setup | Purpose |
|---|---|---|
| 1 | vLLM with guided JSON (grammar-constrained decoding) | The fair baseline: already constrained |
| 2 | Arm 1 + standard speculative decoding with a small Gemma 3 draft | Isolates the gain from speculation |
| 3 | Arm 2 + constraint-pruned trees (schema + allowed set, katgpt-rs style) | Isolates the gain from pruning |

Metrics: **p95 latency** per choice call; **valid-output rate** (must be 100% for arm 3 by construction, measured for all arms); **agreement with arm 1's choice**; **forward passes per call**; **US$ per 1,000 patient-days**, which feeds P16; tokens per second only as a secondary, labelled number, because forced tokens inflate it.

Harness check before any number is reported: with pruning switched off, arm 3 must reproduce arm 2's greedy outputs exactly. If it does not, the harness has a bug and no number is published.

### Design decisions and alternatives we rejected

- **Let the model write free text and filter afterwards.** Rejected: post-hoc filtering wastes compute on illegal outputs and fails open if the filter misses something. Constraint at decode time cannot emit an illegal id.
- **Grammar-constrained decoding alone.** Kept as arm 1: it is the honest baseline. It guarantees validity but does not reduce forward passes.
- **Unstructured weight sparsity for speed.** Rejected for now: it gives no speed-up on GPU or Apple MPS without special kernels. Only structured pruning (removing whole rows and columns) is measurable in PyTorch.
- **Claim katgpt-rs speed-ups.** Rejected: wrong model class, wrong scale. We say "no MedGemma number yet".

### Prior art and where novelty might be

Almost every part has prior art: grammar-constrained decoding (XGrammar, SGLang jump-forward), prompt-lookup decoding, speculative decoding with draft trees, semantic routers, Wanda- and TEAL-style activation pruning, and tool routing from a frozen model's hidden states ("The Router Within", arXiv 2609.15982; OATS, arXiv 2603.13426). The possible novelty is the **combination** in a clinical setting: a deterministic safety layer, allowed-set constraints derived from a FHIR limit record, and capability masking in one cascade. A formal novelty check has not been done.

## Visualizations

### Chart 1 · Grouped bar chart: writing the tool call vs deciding it in one pass (measured, synthetic)

- **Type:** grouped horizontal bars, log-scale X axis.
- **Title:** "Deciding beats writing: median latency per tool decision, Colab T4 (synthetic test set, n = 36)"
- **X axis:** median milliseconds (log scale). **Y axis:** model size, two bars each.
- **Data:**

| Model | A. LLM writes the call: median ms | Best one-pass config: median ms | Best config | Accuracy A → best |
|---|---|---|---|---|
| Qwen3-0.6B | 991 | 53 | D (rules + hidden-state centroid) | 22% → 67% |
| Qwen3-1.7B | 1,272 | 71 | C (rules + one-pass scoring) | 42% → 78% |
| Qwen3-4B | 1,502 | 164 | C (rules + one-pass scoring) | 61% → 69% |

- **Annotations:** label the 1.7B pair "≈ 18× faster, +36 points". Footnote: "Synthetic messages written by the team; config D's input is shorter than A's, so its speed-up is not a like-for-like kernel comparison."
- **What the reader should notice:** at every model size the one-pass decision is an order of magnitude faster and more accurate on this mock-up, and red flags missed fall from 4 to 0 because rules see them first.

### Chart 2 · Stacked bar chart: who decides each message in router v2 (blind synthetic set)

- **Type:** 100% stacked horizontal bar, one bar per model.
- **Title:** "60% of messages never reach a model"
- **X axis:** share of 270 messages. **Y axis:** model.
- **Data:**

| Model | Safety rules | Frequent-phrase rules | Model (one pass) | Two-option clarify question | Total |
|---|---|---|---|---|---|
| Qwen3-1.7B | 35 | 126 | 52 | 57 | 270 |
| Qwen3-4B | 35 | 126 | 92 | 17 | 270 |

- **Annotations:** bracket over the first two segments, "161 / 270 = 59.6% decided by rules, median ≈ 0.1 ms". Side labels: p95 60.4 ms (1.7B), 83.3 ms (4B).
- **What the reader should notice:** the cheapest model call is the one you never make; the larger model mainly converts clarify questions into direct answers.

### Chart 3 · Funnel: Somchai's allowed set, the constraint the decoder would enforce

- **Type:** funnel.
- **Title:** "The decoder may only name one of 67 activities"
- **Data:**

| Stage | Count | What removes items |
|---|---|---|
| Activities in catalogue | 100 | — |
| After MET cap (≤ 5.9 METs, synthetic limit) | 71 | 29 above the cap |
| After contact / breath-holding / burst flags | 67 | 4 flagged (power yoga, digging, plank holds, Muay Thai bag work) |
| Top-5 by similarity to tennis | 5 | ranking |
| Options offered to Somchai | 3 | badminton (social), bowling, table tennis |

- **What the reader should notice:** the same 67-item set that keeps Somchai inside his limits is the vocabulary constraint for decoding.

### Diagram · Constraint-pruned speculative decoding

Four boxes left to right with arrows: "1 Draft (small Gemma 3)" → "2 Prune (ConstraintPruner: schema + allowed set)" → "3 Tree (DDTree, valid branches only)" → "4 Verify (MedGemma, one pass)" → pill "Valid by construction". Above box 2, a dotted arrow from a cylinder "IRIS for Health: CarePlan limits → rules engine → allowed set (67 ids)". Under the diagram, a grey strip: "Benchmark: 3 arms, not run. No MedGemma speed number yet."

### Matrix · Measured vs planned

Five-row table (T0–T4) with a "Measured?" column: Yes, No, Yes, No, No (as in the cascade table above).

## Numbers and claims ledger

| Claim | Value | Source | Status |
|---|---|---|---|
| One-pass vs writing, Qwen3-1.7B, median | 71 ms vs 1,272 ms | `experiments/RESULTS_tool_router_demo.md`; `tool_router_demo_results_Qwen3-1.7B_cuda.json` | synthetic |
| Same, accuracy | 78% vs 42% (n = 36) | same | synthetic |
| 0.6B and 4B rows | as in Chart 1 | same | synthetic |
| Plain model invented a PM2.5 answer | "currently high" without a tool call | same | synthetic (Mac run) |
| Router v2 tier counts | 35 / 126 / 52 / 57 (1.7B); 35 / 126 / 92 / 17 (4B) | `experiments/tool_router_v2_results_Qwen3-*_cuda.json` | synthetic, blind |
| Router v2 p95 | 60.4 ms (1.7B), 83.3 ms (4B) | same | synthetic |
| Router v2 selective accuracy | 95.3% (1.7B), 94.9% (4B) | same | synthetic |
| Red flags caught, v2 | 26 of 30 | same | synthetic |
| Method frozen before test | commit `f30daf1` | git log | checked |
| Somchai allowed set | 100 → 67 | `demo/agent-flow-demo.html` | synthetic |
| katgpt-rs pipeline wording | "LLM drafts logits → ConstraintPruner filters invalid → DDTree builds valid-only tree → Target verifies" | `/Users/admin/Project/katgpt-rs/README.md` | checked |
| katgpt-rs is modelless | "katgpt-rs is modelless (no model loader)" | same | checked |
| katgpt-rs start date | first commit 2026-05-04 | katgpt-rs git log | checked |
| Cascade hypothesis | ≥ 3× faster, ≤ 1 point accuracy loss, 100% schema-valid | `docs/research/neurosymbolic-tool-router-plan.md` | plan |
| MedGemma speed-up | none | — | **not measured** |
| Gemma 3 drafter shares MedGemma tokenizer | — | — | to verify |

## Limits and open questions

- No MedGemma latency, throughput, p95 or cost number exists. The three-arm benchmark needs a rented GPU and a request set.
- All router numbers are on synthetic messages written by the team or by another agent; n = 36 in v1 means one message moves accuracy by about 3 points.
- Tokenizer compatibility between a small Gemma 3 drafter and MedGemma must be checked; without it, step 1 needs a different drafter.
- The choice step's output is so short that speculative decoding might add overhead rather than save time. Arm 2 vs arm 1 will show this; if it does, the honest result is "grammar-constrained decoding is enough".
- Qwen3 uses SwiGLU, so activation sparsity for T4 masks is weaker than in ReLU models; pruning may cost accuracy.
- A Mac MPS speed-up is not a production GPU speed-up.
- No formal novelty check has been run.

## Likely judge questions

1. **"How much faster is MedGemma with your method?"** We do not know yet, and we will not guess. The router, the cheap end of the same idea, was about 18× faster at the median on a synthetic set; MedGemma needs the three-arm benchmark, starting from guided JSON as the baseline.
2. **"Isn't this just constrained decoding?"** Arm 1 is exactly that, and it is our baseline. The extra step is drafting several tokens and pruning the draft tree against the schema and the patient's allowed set before the big model verifies, which can cut forward passes, not just illegal tokens.
3. **"What is katgpt-rs?"** Our own MIT-licensed Rust library of decoding primitives, written before this event. It has no model loader, so its published numbers come from micro-models and puzzles and do not transfer to MedGemma.
4. **"What would prove you wrong?"** For the router cascade: more than 1 point of accuracy lost at every setting that reaches 3×, or under 3× at equal accuracy. For MedGemma: arm 3 not beating arm 1 on p95 latency at equal choices.
5. **"Why does speed matter for a coach?"** Voice check-ins need fast turns for 55–75-year-old users, and fewer forward passes per patient-day lowers the GPU bill on P16, which decides when self-hosting in Thailand pays off.

## Sources

Repo files:
- `docs/pitch/faq-appendix/slides/speed.html` (pipeline, benchmark plan)
- `docs/research/neurosymbolic-tool-router-plan.md` (cascade, hypothesis, falsification, caveats)
- `experiments/RESULTS_tool_router_demo.md`; `experiments/tool_router_demo_results_Qwen3-*_cuda.json`; `experiments/tool_router_v2_results_Qwen3-*_cuda.json`
- `demo/agent-flow-demo.html` (catalogue and synthetic limit)
- `pitch/appendix/A09-speed-rnd-katgpt.md`, `pitch/appendix-deck/P15-speed-rnd-katgpt.md`
- katgpt-rs README, team's own repository: `/Users/admin/Project/katgpt-rs/README.md` (outside this repo)

External: none opened for this page. Prior-art arXiv ids are as recorded in `experiments/RESULTS_tool_router_demo.md` and were not re-opened (to verify).

## Image-generation prompt

Design one 16:9 information slide on a white background. Put the key message first as the title: "The rule that keeps patients safe can also speed up decoding. Router measured; MedGemma not yet." Main visual: a grouped bar chart "Median ms per tool decision, Colab T4, synthetic n = 36" with pairs Qwen3-0.6B 991 vs 53, Qwen3-1.7B 1,272 vs 71 (label "≈ 18× faster, 78% vs 42%"), Qwen3-4B 1,502 vs 164, legend "LLM writes the call" and "decided in one pass". Below it a four-step flow: "1 Draft (small Gemma 3)" → "2 Prune (schema + allowed set)" → "3 Tree (valid only)" → "4 Verify (MedGemma, one pass)" → "Valid by construction". Add a clear orange tile: "No MedGemma speed number yet". Small footer: "katgpt-rs is the team's own modelless Rust library; its micro-model results are not MedGemma results." No logos, no other numbers, no invented speed-ups. ChatGPT chooses the design.
