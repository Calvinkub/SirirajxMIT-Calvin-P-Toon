# P14 · On a blind test the router was 95% right when it answered, but it caught only 26 of 30 red flags, and that miss is our most important finding.

## Key message

We froze the router's rules and thresholds in a commit before reading a 270-message test set written blind by a separate agent. When it answered, the router was right 95.3% (Qwen3-1.7B) and 94.9% (Qwen3-4B) of the time, rules alone decided 161 of 270 messages, and the 95th-percentile latency was 60–83 ms on a T4. But the safety rules caught only 26 of 30 red-flag messages, 2 of them reached the model tier, and 9 of the 10 errors with Qwen3-1.7B came from keyword rules rather than the model. Red-flag detection must not depend on exact phrases, and the v3 design changes the screen accordingly.

## Why this matters to the judges

- **Technical coherence.** A pre-registered, frozen, blind evaluation with errors read only after the run is unusual at a hackathon; it shows we can tell a demo from evidence.
- **Real-world impact.** The page reports the failure that matters for patients (missed red flags) rather than the headline accuracy, and turns it into design changes.
- **Innovation.** A four-tier cascade (safety rules → frequent-phrase rules → one forward pass giving both letter scores and hidden-state features → agree-or-ask) that answers only when two signals agree and otherwise asks the patient a two-option question.
- **Use of InterSystems technology.** The tools being routed are the MCP tools over IRIS for Health; a router that knows when to ask instead of guess keeps wrong FHIR queries out of the conversation.

## Full detail

### 1. Protocol

1. Method, rules and thresholds frozen in commit `f30daf1` **before the test file was read**.
2. Test set `synthetic/router_test_blind.jsonl` written by a **separate agent that saw only the labelling guide** (`synthetic/router_labeling_guide.md`), not the rules, training data or code. The guide asked for colloquial particles, typos, missing tone marks, Thai–English code-mixing, elderly phrasing, very short and long rambling messages, and boundary cases.
3. 270 messages: 30 per label for 9 labels; 162 Thai, 63 English, 45 mixed.
4. Training: `router_train.jsonl` (225 rows: 135 Thai, 54 English, 36 mixed; 25 per label) plus the 72 v1 messages = 297 rows.
5. Threshold τ chosen on cross-validated **training** predictions only: the smallest τ with ≥ 99.5% selective accuracy (1.7B: τ = 0.89; 4B: τ = 0.30).
6. Errors read only after the run. Hardware: Colab Tesla T4; 617-token prompt prefix cached once and reused per message.

### 2. The cascade (`experiments/tool_router_v2.py`)

- **Tier 0, safety rules.** A wider Thai and English red-flag regex (chest pain, pressure, breathlessness, dizziness, fainting, palpitations, radiating pain, cold sweat), a denial check on the 12 characters before the match, a "general question about symptoms" exception, and a medication rule that sends any medicine question to `none` (the clinician path) unless it is a report of having taken it.
- **Tier 1, frequent-phrase rules.** One regex per label; fires only when exactly one label matches.
- **Tier 2, one forward pass.** A few-shot prompt (2 examples per label) gives letter probabilities over 8 labels, and the same pass gives hidden-state features (mean of 3 layers over the message tokens).
- **Tier 3, probe and agreement.** A logistic-regression probe on the hidden states; the router answers only if the LLM's top label, the probe's top label and their average agree and the averaged confidence is ≥ τ. Otherwise it asks the patient a two-option question built from the top two labels.
- `red_flag` is **never** scored by a model; only Tier 0 can return it.

### 3. Results

| Measure | Qwen3-1.7B | Qwen3-4B |
|---|---|---|
| Accuracy when it answers (selective) | 95.3% (203/213) | 94.9% (240/253) |
| Coverage (answers itself) | 78.9% (213/270) | 93.7% (253/270) |
| Accuracy if every clarify counts as wrong | 75.2% | 88.9% |
| Clarify questions whose 2 options contain the right answer | 93.0% (53/57) | 94.1% (16/17) |
| Accuracy after the two-option question | 94.8% (256/270) | 94.8% (256/270) |
| Red flags caught | 26/30 | 26/30 |
| False red-flag alarms | 1 | 1 |
| Median latency | 0.1 ms | 0.1 ms |
| p95 latency | 60.4 ms | 83.3 ms |
| Errors (answered wrongly) | 10 | 13 |

Wilson 95% intervals: selective accuracy 1.7B 91.6–97.4%, 4B 91.4–97.0%; red-flag recall 70.3–94.7%.

### 4. Where decisions were made

Both models share Tiers 0–1, which decided 161 of 270 messages (60%) with no model: 35 by safety rules and 126 by frequent-phrase rules. We re-ran Tiers 0–1 locally (no model needed) and reproduced the 35 / 126 / 109 split exactly.

- Safety tier: 35 decisions, 34 correct: 26 red flags, 8 medication questions sent to `none`, 1 false alarm (a general question about which chest pain needs hospital care, read as a report; acceptable direction).
- Frequent-phrase tier: 126 decisions, 117 correct (92.9%); **all 9 remaining errors of the 1.7B run are here**, and the same 9 recur in the 4B run.
- Model tier: 1.7B answered 52 and got all 52 right but asked 57 clarify questions; 4B answered 92 (89 right) and asked 17.

The difference between the two models is therefore a coverage trade-off: 1.7B with τ = 0.89 is cautious and asks often; 4B with τ = 0.30 answers more and makes 3 more mistakes. After the two-option question both reach 256 of 270.

### 5. The red flags

Of 30 red-flag messages: 26 caught by Tier 0; 2 slipped to the frequent-phrase tier and were routed wrongly (one to `search_activities` because the Thai word for "dance", เต้น, appeared in "ใจมันเต้นรัว", heart racing; one to `log_checkin` because "blackout" was written as one word); 2 reached the model tier. With 1.7B both of those went to the clarify question; with 4B one went to clarify and one was answered `none` (a word order the regex did not cover). Either way **2 red-flag messages reached a model**, which breaks the pre-registered bar of "0 red-flag messages reaching any model".

The case that changes the design is "ไม่ได้เจ็บหน้าอกนะ แต่ใจเต้นรัว" (no chest pain, but my heart is racing): the patient denies one symptom and reports another. Negation handling that clears the whole message is unsafe; negation must be scoped to one clause, and a cruder screen that stops on any symptom word (like the UI's) would have been safer here.

### 6. The other errors

By gold → predicted label (1.7B): limits → places (2), check-in → places (1), check-in → PM2.5 (1), recent activity → places (1), limits → activities (1), none → limits (1), red flag → activities (1), red flag → check-in (1), none → red flag (1, false alarm). Causes we identified after the run:

- **Single keywords are too blunt for mixed intents.** "อยากไปเดินสวนแต่กลัวจะหนักเกินไปสำหรับหัวใจ" (I want to walk in the park but fear it is too hard for my heart) asks about limits, but "สวน" (park) fired the places rule.
- **Thai has no spaces between words.** วัด (temple) matched inside จังหวัด (province), sending a check-in about a trip upcountry to `search_places`.
- **A medication question missed by the medication rule** went to `get_patient_limits` because a "the doctor allowed" phrase fired; a medication question must always reach the clinician path.

Errors were concentrated in Thai: 8 of 10 (1.7B) and 10 of 13 (4B), against a 60% Thai share of the test set. Error rates per language for 1.7B: Thai 4.9% (8/162), English 1.6% (1/63), mixed 2.2% (1/45).

### 7. What v3 changes (new blind set required)

1. Frequent-phrase rules accept only when the model agrees; disagreement goes to the model or the clarify question.
2. Red-flag screen: symptom lexicon tolerant of spacing and filler words, negation scoped to one clause, Thai word segmentation before matching, and a model-based second screen that can **only escalate** to stop.
3. Any message sent to clarify that contains a body-symptom word goes to stop instead.
4. A new blind set written by people (team, mentors, ideally patients), ≥ 300 Thai and English messages, split 50/50 into calibration and test; red-flag recall reported with its denominator. The v2 set is now seen and cannot be reused as evidence.

### 8. Worked example: Somchai, two messages

"ร้อนมั้ย" (is it hot?) → the heat rule fires alone → `get_heat_index` in about 0.1 ms with no model. "อยากไปเดินสวนแต่กลัวจะหนักเกินไปสำหรับหัวใจ" → in v2 the park keyword sends him a list of parks, which is wrong; in v3 the keyword rule must agree with the model, which reads "fear it is too hard for my heart" as a limits question, so he gets his signed limits instead. If he had added a symptom ("ใจเต้นรัว"), v3 sends the whole message to stop.

## Visualizations

### Chart 1 · Funnel or waterfall: where 270 messages were decided (Qwen3-1.7B, with 4B alongside)

| Tier | Qwen3-1.7B | Qwen3-4B | Correct (1.7B) | Correct (4B) |
|---|---|---|---|---|
| Safety rules | 35 | 35 | 34 | 34 |
| Frequent-phrase rules | 126 | 126 | 117 | 117 |
| Model answers (agree + τ) | 52 | 92 | 52 | 89 |
| Clarify (two-option question) | 57 | 17 | 53 contain the answer | 16 contain the answer |
| **Total** | **270** | **270** | | |

- Annotation: "161 of 270 decided with no model → median 0.1 ms". What to notice: errors live in the keyword tier, not the model tier.

### Chart 2 · Sankey: the 30 red-flag messages

| From | To | 1.7B | 4B |
|---|---|---|---|
| Red-flag messages | Safety rules → STOP | 26 | 26 |
| Red-flag messages | Keyword rule → wrong tool | 2 | 2 |
| Red-flag messages | Model tier → clarify | 2 | 1 |
| Red-flag messages | Model tier → `none` | 0 | 1 |

- What to notice: 4 misses, 2 of which reached a model; target is 30 of 30 with nothing reaching a model.

### Chart 3 · Bar: coverage vs selective accuracy (the τ trade-off)

| Model | τ | Coverage | Selective accuracy | Accuracy after clarify |
|---|---|---|---|---|
| Qwen3-1.7B | 0.89 | 78.9% | 95.3% | 94.8% |
| Qwen3-4B | 0.30 | 93.7% | 94.9% | 94.8% |

### Chart 4 · Stacked bar: tier by gold label (both models; Tiers 0–1 identical)

| Gold label | Safety | Frequent | Model or clarify |
|---|---|---|---|
| red_flag | 26 | 2 | 2 |
| none | 9 | 7 | 14 |
| get_pm25 | 0 | 25 | 5 |
| search_places | 0 | 21 | 9 |
| get_heat_index | 0 | 20 | 10 |
| search_activities | 0 | 17 | 13 |
| log_checkin | 0 | 15 | 15 |
| get_recent_activity | 0 | 10 | 20 |
| get_patient_limits | 0 | 9 | 21 |

- What to notice: concrete topics (dust, heat, places) are caught by keywords; "what am I allowed to do" questions need the model.

### Chart 5 · Bar: errors by language (Qwen3-1.7B)

| Language | Test messages | Errors | Error rate |
|---|---|---|---|
| Thai | 162 | 8 | 4.9% |
| English | 63 | 1 | 1.6% |
| Mixed | 45 | 1 | 2.2% |

(4B: Thai 10, mixed 2, English 1 of 13 errors.)

## Numbers and claims ledger

| Claim | Value | Source | Status |
|---|---|---|---|
| Test set | 270; 30/label; 162 th, 63 en, 45 mix | `synthetic/router_test_blind.jsonl` (counted) | synthetic, blind to method |
| Train set | 225 + 72 = 297 | `synthetic/router_train.jsonl`, v1 file, JSON `meta` | synthetic |
| Frozen before test read | commit `f30daf1` | `experiments/RESULTS_tool_router_demo.md` | as reported (commit not re-inspected here) |
| τ | 0.89 / 0.30 | JSON `meta` | checked |
| Selective accuracy, coverage, clarify, recall, false alarms, latency | §3 table | `experiments/tool_router_v2_results_Qwen3-1.7B_cuda.json`, `…_4B_cuda.json` | synthetic |
| Correct counts 203/213, 240/253, 53/57, 16/17 | — | derived from JSON rates × counts | checked |
| Tier 0–1 split 35 / 126 / 109 | — | re-run locally with the frozen rules | checked (reproduced) |
| Frequent tier 117/126 correct; safety 34/35 | — | same local re-run | checked |
| Red-flag routing (26 / 2 / 2) | — | local re-run + JSON error list | checked |
| Errors by language | 1.7B th 8, en 1, mix 1 | JSON error ids × test file `lang` | checked |
| Wilson intervals | §3 | our computation | checked |
| Pre-registered bar "0 red flags reach a model" | not met (2) | `docs/research/neurosymbolic-tool-router-plan.md` + above | checked |
| v3 results | — | — | not built |

## Limits and open questions

- Synthetic messages, even if blind: written by a language model from a guide, not by patients.
- Argument filling still not implemented.
- The blind set is now used; any v3 claim needs a new set written by people.
- Latency is a T4 measurement with a cached prefix, not production serving.
- No per-dialect or age analysis is possible with this data.
- The clarify question's real-world acceptability for older users is untested.

## Likely judge questions

**Q: 95% sounds good. Why lead with the 26 of 30?**
Because a missed chest-pain message is the error that hurts a patient, and accuracy on weather questions does not offset it. The 4 misses tell us exactly what to change: phrase-tolerant matching, clause-scoped negation and an escalate-only model screen.

**Q: Was the test really blind?**
The rules and thresholds were committed before the test file was read, and the test was written by a separate agent that saw only the labelling guide. It is still synthetic; real blind evidence needs messages written by people.

**Q: Why ask the patient a question instead of guessing?**
When the two signals disagree, a two-option question ("weather or places?") contains the right answer 93–94% of the time and costs one tap. Guessing wrong sends the wrong FHIR query and erodes trust.

**Q: Why are the errors in the rules, not the model?**
Keyword rules are fast and transparent, but Thai has no spaces and patients mix intents. v3 makes keyword rules advisory: they accept only when the model agrees.

## Sources

Repo:
- `experiments/tool_router_v2.py`
- `experiments/tool_router_v2_results_Qwen3-1.7B_cuda.json`, `experiments/tool_router_v2_results_Qwen3-4B_cuda.json`
- `experiments/RESULTS_tool_router_demo.md` (quoted messages are those already quoted there)
- `synthetic/router_labeling_guide.md`, `synthetic/router_test_blind.jsonl`, `synthetic/router_train.jsonl` (counts only)
- `docs/research/neurosymbolic-tool-router-plan.md` (pre-registered bar)
- `pitch/appendix/A06-tool-router-experiments.md`, `pitch/appendix-deck/P12-tool-router-v2-blind.md`

External: see P13 (prior art) and P10 (Qwen3 model facts).

## Image-generation prompt

A 16:9 information slide on a white background. Key message as title: "95% right when it answers, but only 26 of 30 red flags caught." Main chart: a waterfall of 270 blind synthetic messages: 35 safety rules, 126 keyword rules, 52 model, 57 clarify (Qwen3-1.7B), labelled "161 decided with no model". Second chart: a small Sankey of 30 red-flag messages: 26 to STOP, 2 to the wrong tool, 2 reaching the model tier, with the misses in orange. A short line: "9 of 10 errors came from keyword rules, not the model." Footer badge: "frozen before reading; synthetic; Colab T4; p95 60–83 ms". Use only these numbers, no logos, no invented figures; ChatGPT chooses the design.
