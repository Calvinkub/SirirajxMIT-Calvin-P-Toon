# Report templates

## Reviewer report

```markdown
# <persona id> review — <mode> — <date>

> Simulated review by a language-model role-play. Not a real clinician or institution.

**Artifacts read:** <paths>
**Gate result (my view):** PASS | CONDITIONAL | FAIL

## Safety gates
| Gate | Status (PASS / FAIL / NOT-DEFINED) | Evidence (path:line) |
|---|---|---|
| G1 Limits | | |
| G2 Red flags | | |
| G3 Eligibility | | |
| G4 Claims | | |
| G5 Accountability | | |
| G6 Failure mode | | |

## Scores (0–4, track A or B)
| Dimension | Score | One-line reason |
|---|---|---|

## Findings (most severe first)
### F1 [S0|S1|S2|S3] <short title>
- **What is wrong:** <one sentence>
- **Evidence:** `path:line` or URL, or `UNSOURCED`
- **Failure scenario:** <concrete patient / judge / insurer moment>
- **Fix:** <specific and cheap>
- **Needs real expert?** yes/no (who)

## What I could not verify
<list>
```

## Chair synthesis (`SYNTHESIS.md`)

```markdown
# Panel synthesis — <mode> — <date>

> Simulated panel (7 role-played reviewers + chair). Not clinical validation, ethics approval, or institutional endorsement.

**Gate result:** PASS | CONDITIONAL | FAIL — <one-line reason>

## Gate table (worst status across reviewers)
## Ranked findings (de-duplicated; reviewers who raised each; verified by chair yes/no)
## Scores by persona and dimension
## Disagreements between reviewers
## Needs a real expert (clinician, lawyer, insurer, statistician)
## Five cheapest actions that remove the most risk
## Not covered by this review
```
