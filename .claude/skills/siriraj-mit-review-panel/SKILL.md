---
name: siriraj-mit-review-panel
description: Run a simulated expert review of the CVD Mission Coach project (SirirajxMIT) by a panel of domain-expert subagents — Siriraj clinical side (cardiologist, cardiac-rehab/exercise physiologist, nurse/pharmacist, regulatory/ethics) and MIT-style committee side (AI safety, digital-health/behavior-change, venture/market) — then synthesize a scored report. Also holds the system evaluation framework (safety scenario tests, agent evals, pilot stage-gates). Use whenever the user wants the design, pitch script, research, prototype, or a code change evaluated, asks for "the panel", "committee review", "Siriraj/MIT judges", "red-team the idea", "score this against the rubric", "is this safe/ready", or wants to define or run the evaluation tests for the app.
---

# Siriraj × MIT review panel

Simulated reviewers for a cardiac-patient exercise-coaching app. Goal: find the flaws a real Siriraj clinician or MIT judge would find, **before** the real ones do.

## Honesty rules (non-negotiable)

1. Personas are role-plays by a language model. They are **not** real Siriraj or MIT staff, do not speak for either institution, and never count as clinical validation, ethics approval, or endorsement. Never write "Siriraj approved" or "MIT judges said". Write "simulated Siriraj cardiologist panel flagged".
2. Reviewers may only cite evidence found in the repo (`research/`, `docs/`) or fetched with a source link. A number without a source is marked `UNSOURCED`. No invented statistics, guideline clauses, or Thai regulations. If unsure of a clinical fact, say "needs verification by a real clinician".
3. The panel finds problems. It does not certify safety. Safety-gate failures always escalate to a human clinician decision.
4. Assumption: "MIT committee" means a judging panel for an MIT-affiliated health-innovation event. If the team names a different format (e.g. MIT Hacking Medicine, Sloan venture judges), update `references/personas.md` §MIT before running.

## When to run

| Trigger | Mode | Reviewers |
|---|---|---|
| New or changed design doc, pitch script, or research | `document` | all 7 |
| Code or prompt change touching missions, limits, red-flag path, or the agent | `system` | clinical 4 + AI safety |
| Before pitch / submission | `pitch` | all 7, scored on `references/rubric.md` track B |
| Before any real-patient pilot | `pilot-gate` | all 7 + a **human** clinician sign-off (panel cannot replace this) |

## How to run

1. **Pick mode and artifacts.** List exact files the reviewers must read. Default set: `docs/superpowers/specs/*design.md`, `HANDOFF.md`, `research/README.md`, `research/pitch-claims-check.md`, and the pitch script if present.
2. **Dispatch reviewers in parallel**, one Agent call per persona in a single message. Use persona prompts verbatim from `references/personas.md`. Give each agent: the artifact paths, the mode, `references/rubric.md`, and the output template from `references/report-template.md`. Tell each agent: read-only, no background jobs, no waiting on other agents, write its review to `evaluation/reviews/<date>-<mode>/<persona-id>.md` and return a 10-line summary.
3. **Do not share reviews between reviewers.** Independence is the point.
4. **Dispatch the chair** after all reviewers finish. The chair reads every review, de-duplicates, resolves conflicts, runs the safety-gate check, and writes `evaluation/reviews/<date>-<mode>/SYNTHESIS.md`.
5. **Verify before reporting.** Spot-check the 3 highest-severity findings against the artifact yourself. Drop findings that misread the artifact.
6. **Report to the user:** gate result (PASS / CONDITIONAL / FAIL), top 5 findings ranked by severity, scores per persona, disagreements, and what only a real clinician can decide.
7. **Commit** the review folder if the user asked for teammate handoff.

## System evaluation framework

The product-level tests live in `references/system-eval.md`: safety scenario suite, limit-adherence property tests, agent adversarial evals, data-quality checks, adherence and clinical metrics, and pilot stage-gates. Run `system` mode whenever those tests change or fail. When code exists, the panel's AI-safety reviewer must run the scenario suite, not just read about it.

## Files

- `references/personas.md` — the 7 reviewer prompts plus the chair prompt
- `references/rubric.md` — scoring scales, hard safety gates, severity definitions
- `references/system-eval.md` — system evaluation framework
- `references/report-template.md` — output format for reviewers and the chair
