# Appendix v2 — information-first pages

Purpose: Q&A appendix for MIT GrandHack 2026, InterSystems challenge ("Best Use of GenAI or FHIR using InterSystems technology"; criteria: Innovation, Real-world impact, Use of InterSystems technology, Technical coherence). These pages are **content, not design**: each file holds everything a judge could ask about one topic, with sources and chart data. ChatGPT image generation will design the slide from the file.

Positioning (use everywhere): **Heartstep is like Netflix for a healthy heart** — a chat coach that recommends activities and community groups each patient will enjoy (signals: your taste, people like you, near you) and builds a care plan, only inside the limits a doctor signed. Built on InterSystems IRIS for Health (FHIR Server, FHIR SQL Builder, IRIS Vector Search). Safety by construction: red-flag symptoms are handled by rules, never by a model. Demo example: Somchai, 58, used to play tennis, now has hypertension → badminton, bowling, table tennis.

## Page template (every file follows it, in this order)

1. `# Pxx · <claim title>` — the title is a sentence the judge should remember.
2. `## Key message` — 2–3 declarative sentences. No hedging, but every claim sourced below.
3. `## Why this matters to the judges` — which criterion it serves and why.
4. `## Full detail` — long, specific explanatory text (typically 800–1,500 words) in short subsections: how it works, design decisions and alternatives rejected, worked example with Somchai, numbers in context. Text first; no layout talk.
5. `## Visualizations` — at least one real chart (bar, line, stacked, scatter, funnel, waterfall, Sankey, timeline) and a diagram where it helps. For each: chart type, title, axes and units, **the full data table in Markdown**, annotations, and "what the reader should notice". Only real or clearly labelled synthetic/estimated data.
6. `## Numbers and claims ledger` — table: claim · value · source (repo path or URL actually opened) · status (checked / synthetic / estimate / simulated / to verify).
7. `## Limits and open questions` — what this page does not prove and what is missing.
8. `## Likely judge questions` — 3–5 questions with 2–4 sentence answers.
9. `## Sources` — repo files and external sources, each external one a link you opened.
10. `## Image-generation prompt` — one short paragraph at the end: 16:9 information slide, white background, put the main chart and the key message first, include the quoted key numbers, no logos, no invented numbers; ChatGPT chooses the design.

## Honesty rules
No invented statistics or citations. Every number traces to a repo file or an external page you opened. Label synthetic data, the simulated review panel and estimates. Mark unchecked items "to verify". Never "proven", "optimal" or "clinically validated". The AI never sets exercise limits. Red flags are rules-only.

## Pages

| Page | Topic |
|---|---|
| P01 | Why not ChatGPT/Claude: recommender chat coach vs general advice |
| P02 | Problem evidence: one guideline for everyone; no clue, no friends, no trust in data |
| P03 | System architecture on IRIS for Health |
| P04 | FHIR R4 resource map, codes and extensions |
| P05 | Synthetic FHIR bundles: 8 patients, counts, what each tests |
| P06 | FHIR SQL Builder: from resources to the rules engine |
| P07 | IRIS Vector Search grounding: guideline and activity retrieval |
| P08 | Geospatial community search: service area, groups, weather |
| P09 | The recommender: Netflix-style signals, ranking, cold start, evaluation |
| P10 | Agent harness: models, roles, typed contracts |
| P11 | The 8-step agent flow (demo) from message to FHIR Tasks |
| P12 | Safety by construction: rules, gates G1–G6 |
| P13 | Tool-router experiment v1 (speed and accuracy) |
| P14 | Tool-router v2 blind test and red-flag misses |
| P15 | Evaluation framework and simulated review panel |
| P16 | Cost structure and unit economics |
| P17 | Speed R&D: constraint-pruned speculative decoding (katgpt-rs) |
| P18 | Clinical evidence: guidelines, CPET and non-CPET intensity, risk classes |
| P19 | Market, competitors and business model |
| P20 | Regulatory, PDPA and accountability |
| P21 | Roadmap to pilot: six gates |
| P22 | Team: built at the event vs reused vs planned |
