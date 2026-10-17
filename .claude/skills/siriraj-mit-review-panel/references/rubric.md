# Rubric

## Severity

| Level | Meaning | Example |
|---|---|---|
| S0 Blocker | Could harm a patient, or makes a core claim false | Mission can exceed clinician limit; red-flag path goes through the LLM |
| S1 Major | Likely fails review or pilot; fix before next gate | Unsourced headline statistic; no plan for patients without CPET |
| S2 Moderate | Weakens the case; fix soon | Vague retention plan |
| S3 Minor | Polish | Wording, formatting |

## Hard safety gates (any FAIL = overall FAIL)

| Gate | Pass condition |
|---|---|
| G1 Limits | Every mission is provably inside clinician-set (or guideline-default) limits; AI cannot raise limits |
| G2 Red flags | Red-flag handling is deterministic (no LLM in the path) and tells the patient to stop and seek emergency care |
| G3 Eligibility | App blocks or escalates patients outside its safe population (e.g. high-risk class, ICD, unstable symptoms) |
| G4 Claims | No unsupported efficacy, safety, or "proven" claim; no diagnose/treat wording |
| G5 Accountability | A named clinical owner for limits is defined, and patient consent covers data and use |
| G6 Failure mode | When data, network, or model is unavailable, the app degrades to a safe default (no new intensity) |

Gate status per artifact: `PASS`, `FAIL`, or `NOT-DEFINED` (the artifact is silent). `NOT-DEFINED` counts as FAIL for the `pilot-gate` mode and as a finding (S1) for other modes.

## Track A — design and system (score each 0–4)

| Dimension | 0 | 2 | 4 |
|---|---|---|---|
| Clinical validity | Contradicts guidelines | Mostly consistent, gaps | Traceable to guidelines, edge cases covered |
| Patient safety | Unsafe path exists | Known paths covered | Hazard analysis done and tested |
| Evidence and sourcing | Claims unsourced | Mixed | Every number traceable, vendor data flagged |
| Feasibility | Not buildable as described | Buildable with unknowns | Plan, owners, and demo path clear |
| Regulatory and privacy | Unaddressed | Identified, unresolved | Classified, consent and data flow designed |
| Behavior and adherence | No retention logic | Plausible, untested | Evidence-based with a test plan |
| Agent safety and evaluation | No test plan | Some tests | Scenario suite, adversarial tests, regression |

## Track B — pitch (score each 0–4)

| Dimension | 4 means |
|---|---|
| Problem clarity | One patient, one moment, one measurable gap, with source |
| Solution credibility | Mechanism is clear and safe; no overclaims |
| Evidence | Numbers sourced; limits stated |
| Market and business | Payer, price, and path to first revenue defensible |
| Differentiation | Clear versus Movn, Cardihab, hospital programs, LINE programs |
| Team and feasibility | Demo works; clinical partner named |
| Impact and ethics | Equity, safety, and data handling addressed |

## Score reading

Average of dimensions: 0–1.4 not ready; 1.5–2.4 needs major work; 2.5–3.4 promising, fix gaps; 3.5–4 strong. A strong score never overrides a gate failure.

## Gate result

- **PASS:** no gate FAIL, no S0 open, average ≥ 2.5
- **CONDITIONAL:** no gate FAIL, S0 none, but S1 findings open or average < 2.5
- **FAIL:** any gate FAIL or any S0 open
