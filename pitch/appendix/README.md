# Q&A appendix · CVD Mission Coach (Calvin, P, Toon)

MIT GrandHack 2026 · InterSystems challenge: "Best Use of GenAI or FHIR using InterSystems technology". Each file stands alone and answers one judge question. It opens with a one-line answer, then gives detail, a diagram where useful, and the repo evidence behind every number.

**Read this first:**
- All patient data is **synthetic** (tagged `data-origin = synthetic`). The review panel is **simulated** (language-model reviewers). Neither is clinical evidence.
- Built today: Heartstep UI prototype with rules-only checks, 383 synthetic FHIR R4 resources in PUT transaction bundles, tool-router experiments v1/v2 on Colab T4, and a scripted agent-flow demo. Everything else is **planned**.
- The AI never sets a limit. Red flags are handled by rules only.

| File | Judge question it answers | One-line answer |
|---|---|---|
| [A01](A01-why-not-chatgpt.md) | Why not just ask ChatGPT or Claude? | A chatbot answers when asked. We act first, inside a clinician-signed FHIR limit record, with rules deciding safety before any model, in Thai, with the care team in the loop |
| [A02](A02-system-architecture.md) | Where does InterSystems sit? How is it built? | IRIS for Health is the single source of truth: FHIR Server for every fact, SQL Builder for the rules engine, Vector Search for grounding, and typed MCP tools as the only way in |
| [A03](A03-fhir-data-model.md) | Is the data model thoughtful and interoperable? | Every fact is a standard FHIR R4 resource, from watch readings to the signed limit `CarePlan` to each mission `Task` and its AI `Provenance`. 9 idempotent PUT bundles, 383 resources, validated |
| [A04](A04-agentic-harness.md) | What runs inside the agent harness? | Open models with one job each (Qwen3-ASR, Qwen3 router, MedGemma 27B / 1.5 4B, Thai TTS), wrapped by rules before and after. The model only picks an id from the allowed set. Workflows W1–W5 and the full demo flow |
| [A05](A05-intersystems-vector-search-and-geo.md) | What is your smart use of GenAI / Vector Search? | Vector Search grounds answers in clinician-approved content only (no snippet, no answer) and ranks real FHIR places and groups near home after the rules filter them |
| [A06](A06-tool-router-experiments.md) | Did you measure anything? | Yes, on synthetic data. Rules + one-pass scoring was ~18× faster and more accurate than LLM tool calling (Qwen3-1.7B: 71 vs 1,272 ms, 78% vs 42%). Blind v2: 95% when it answers, but 26/30 red flags. v3 fixes that |
| [A07](A07-safety-and-evaluation.md) | How do you stop the AI harming a heart patient? | Limits from a signed record, rules-only red flags, eligibility gate, output filter, safe default. Tested by properties, 18 scenarios and stage gates. Our simulated panel failed v0.1 and we fixed what it found |
| [A08](A08-cost-structure.md) | What does the AI cost per patient? | About US$0.78/patient-month on Sonnet 5.5 or US$2.11 on one H100 at 1,000 patients (unmeasured token budget), against a ~US$14 price. People and the IRIS licence are the big lines, still to price |
| [A09](A09-speed-rnd-katgpt.md) | Can it run faster and cheaper? | Probably: the safety constraint doubles as a decoding constraint (constraint-pruned speculative decoding, katgpt-rs). No MedGemma speed number yet. Benchmark plan stated |
| [A10](A10-clinical-evidence.md) | What is the clinical basis? | Guidelines accept CPET and non-CPET intensity methods and define who is safe for home exercise. A clinician sets limits and class. Our research conflicts in 12 places and needs a rehab physician |
| [A11](A11-market-and-business.md) | Who pays, and who else does this? | Insurer B2B2C and B2C freemium from 499 THB. Movn and Cardihab are clinician-led and not Thai. Insurer willingness and price are unvalidated, with weak spots listed |
| [A12](A12-regulatory-pdpa.md) | Is it a medical device? What about PDPA? | Positioned as adherence support inside clinician limits. The Thai FDA SaMD question is open for a lawyer. Separate PDPA consents in FHIR `Consent`, insurer off by default |
| [A13](A13-roadmap-mvp.md) | Is there a realistic path to an MVP? | Six gates with named humans: demo → clinician review → usability → IRB/Thai FDA → supervised pilot → insurer pilot. The critical path is people, not code |

Mermaid diagrams render on GitHub and in most Markdown viewers.

## Sources / evidence in repo

Each file ends with its own list. The main ones: `docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md`, `docs/pitch/appendix-slides-plan.md`, `docs/pitch/faq-appendix/slides/*.html`, `docs/diagrams/backend-architecture.dc.html`, `synthetic/`, `experiments/`, `research/`, `evaluation/reviews/2026-10-17-document/SYNTHESIS.md`, `.claude/skills/siriraj-mit-review-panel/references/system-eval.md`, `FHIR-AI-Hackathon-Kit/`.
