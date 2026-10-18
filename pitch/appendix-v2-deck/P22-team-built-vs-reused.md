# P22 · What you saw is exactly what exists: built here in one night, reused with credit, or still planned

## Key message

Everything in Heartstep's repository was committed in one 7 h 26 min window, from 20:28 on 17 October to 03:54 on 18 October 2026 (Bangkok time): 28 commits, about 31,800 inserted lines, including the FHIR data model and generator, 383 synthetic FHIR resources in 9 bundles, a UI whose 6 tests pass, two router experiments on a T4, and the scripted recommender demo. We reused the InterSystems FHIR-AI Hackathon Kit, open model weights, and katgpt-rs, a Rust library the team started in May 2026; the live IRIS run, SQL Builder, Vector Search tables, the MCP server and model serving are still planned, and we built with AI coding assistants, which the commit history records openly.

## Why this matters to the judges

- **Technical coherence and honesty.** Hackathon judges are asked to separate what was built during the event from what was brought in. This page gives the evidence: the git history, file by file, with timestamps.
- **Use of InterSystems technology.** We show precisely how far we got on IRIS for Health (data model and loader for the kit's FHIR server) and what the InterSystems mentorship we ask for would unlock (live load, SQL Builder, Vector Search, MCP).
- **Team and feasibility.** A judge deciding whether this team can carry the project forward wants to see velocity, discipline (method frozen before a blind test) and a clear ask.

## Full detail

### The team

Calvin, P and Toon (`README.md`, `pitch/README.md`). Roles are not yet filled in the repo; the pitch folder has placeholders for a technical lead, a clinical lead and a business lead. **Team to fill before the event; this page invents no titles, universities or degrees.** The git history shows two authors: commits by "Admin" (26 commits, from the machine whose handoff notes are signed by Calvin; team to confirm) and by "suteekarn" / "SuteekarnPhasugmool" (the initial Heartstep UI commit and the merge of pull request #1 from `Calvinkub/feature/initial-ui`).

### How we know what was built here: the git log

The repository's first commit is `35f0a9a` at 2026-10-17 20:28 +07:00 ("add CVD mission coach design draft and team handoff"); the last is `0d9e34e` at 2026-10-18 03:54 ("reposition as 'Netflix for a healthy heart' recommender chat coach"). There is no earlier history. Whether that window lies entirely inside the official event period is for the team to confirm against the GrandHack schedule.

Commits by hour (start of hour, +07:00) and by kind:

| Hour | Commits | Docs, research, evaluation | Code and demo | Data and experiments | Pitch | Lines inserted |
|---|---|---|---|---|---|---|
| 20:00 | 3 | 3 | 0 | 0 | 0 | 938 |
| 21:00 | 4 | 3 | 1 | 0 | 0 | 2,077 |
| 23:00 | 1 (merge) | 0 | 0 | 0 | 0 | 0 |
| 00:00 | 5 | 4 | 0 | 0 | 1 | 493 |
| 01:00 | 6 | 0 | 1 | 5 | 0 | 23,741 |
| 02:00 | 5 | 0 | 3 | 0 | 2 | 2,239 |
| 03:00 | 4 | 0 | 2 | 0 | 2 | 2,348 |
| **Total** | **28** | **10** | **7** | **5** | **5** | **31,836** |

The 01:00 spike is mostly generated data: commit `3c06d2c` alone inserted 22,177 lines, nearly all of it the nine synthetic FHIR bundles written by `synthetic/generate_fhir.py`. Line counts measure volume, not effort, and generated JSON inflates them; we show them only to make the timeline concrete.

### Built at the event (with evidence)

| What | Evidence | Commit | Check |
|---|---|---|---|
| Design spec with 11 safety rules, eligibility gate and failure defaults | `docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md` | `35f0a9a`, `c7923f7` | read |
| First-pass guideline and market research (NotebookLM, 55 sources) and a pitch-claims check | `research/` | `415511d` | machine-generated, labelled |
| Review-panel skill, evaluation framework (layers, 18 scenarios, six gates), first simulated panel run | `.claude/skills/siriraj-mit-review-panel/`, `evaluation/reviews/2026-10-17-document/` | `ea5cf30` | simulated, labelled |
| Clinician reconcile table (12 questions) | `research/guidelines/RECONCILE-for-clinician.md` | `c7923f7` | read |
| Heartstep UI with rules-only safety checks | `index.html`, `app.js`, `safety.js`, `tests/` | `3f37a61` | `npm test` on 2026-10-18: 6 tests, 6 pass |
| FHIR R4 data model and generator; 383 synthetic resources in 9 bundles (shared reference data + 8 patients) | `synthetic/generate_fhir.py`, `synthetic/fhir/*.json` | `3c06d2c` | counted: 20 + 52 + 50 + 51 + 29 + 52 + 28 + 52 + 49 = 383 |
| Loader for the kit's IRIS for Health FHIR server | `synthetic/load_to_iris.py` | `3c06d2c` | written; live load to confirm |
| Router v1: three Qwen3 sizes on a Mac and a Colab T4 | `experiments/tool_router_demo.py`, results JSON, `RESULTS_tool_router_demo.md` | `3c06d2c`, `aad3538` | synthetic data |
| Router v2: method frozen before a blind 270-message test written by a separate agent | `experiments/tool_router_v2.py`; `synthetic/router_test_blind.jsonl` | `f30daf1` (freeze 01:48) → `7d906b3` (test 01:49) → `490c821` (results 01:55) | order verified in git |
| Recommender agent demo: 100-activity catalogue, rules filter to 67, KNN by taste, nearby groups, synthetic cohort, FHIR Tasks; GIF recording | `demo/agent-flow-demo.html`, `demo/media/` | `c6d8536` to `54769c8` | runs in browser, scripted |
| Problem-story animation | `demo/problem-story.html` | `11ea4b0` | — |
| 3-minute pitch, 13-part Q&A appendix, appendix deck specs, repositioning as "Netflix for a healthy heart" | `pitch/` | `6e1110b`, `0bb3195`, `696653f`, `0d9e34e` | — |

The order of the three router v2 commits is worth stating: the rules and method were committed at 01:48, the blind test set at 01:49, and results at 01:55. That is the evidence that the v2 numbers on P14 were not tuned on the test set. The test set is now seen and cannot be reused as evidence; v3 needs a new one.

### Reused (with credit)

| What | What we used it for | Origin |
|---|---|---|
| InterSystems FHIR-AI Hackathon Kit | IRIS for Health in Docker (FHIR server, SQL, Vector Search), tutorials (FHIR SQL projection 3.5, LangChain agents 5.1, MCP servers 5.2), the `fhir.resources` validation pattern | github.com/intersystems-community/FHIR-AI-Hackathon-Kit; cloned locally, not committed to our repo |
| Open model weights | Qwen3-0.6B, 1.7B, 4B for the router experiments; MedGemma and Qwen3 family in the planned harness | model cards cited in `docs/pitch/faq-appendix/slides/sources.html` |
| `fhir.resources` (R4B models) | Validating every generated resource | Python package, as in the kit |
| 2024 Adult Compendium of Physical Activities | MET values for 44 of 100 catalogue activities | pacompendium.com |
| ESC 2020 sports cardiology guideline §4.2.3 | Paraphrased hypertension lines retrieved in the demo | via NotebookLM; to verify against full text |
| katgpt-rs | Planned decoding primitives (`ConstraintPruner`, `DDTree`, `spec_pruner`) for the R&D track (P17) | The team's own MIT-licensed Rust library; first commit 2026-05-04, 2,706 commits before the event; modelless |
| NotebookLM | First-pass research over 55 sources | Google tool; output labelled machine-generated |
| AI coding assistants | Drafting docs, code, data generators and pitch material | 26 of 26 commits by "Admin" carry a Claude co-author trailer (23 Claude Opus 5.5, 3 Claude Sonnet 5.5); the UI commit by suteekarn carries none |

We disclose AI assistance because judges increasingly ask, and because it explains the volume of documentation in one night. The judgment calls (positioning, safety rules, what to measure and what not to claim) are the team's, and the honesty rules in `pitch/README.md` apply to everything regardless of who typed it.

### Planned (not built yet)

| What | Why it matters | Blocker |
|---|---|---|
| Live IRIS run: bundles loaded and served by the kit's FHIR server | Turns "designed for IRIS" into "running on IRIS" | Confirm load; custom extensions accepted |
| FHIR SQL Builder projection for the rules engine | Rules read signed limits as SQL | Kit tutorial 3.5 |
| IRIS Vector Search tables for guideline passages and the activity catalogue | Grounded retrieval and KNN inside IRIS instead of the browser | Thai embedding test |
| MCP server over FHIR with a typed tool list | Agent reads and writes FHIR only through audited tools | Kit FastMCP pattern |
| Model serving (Qwen3 router, MedGemma choice step) and Thai TTS | Real agent instead of scripted trace | GPU, Thai TTS choice |
| Clinician web app (sign limits, review flags) | A clinician owns every limit | Named clinical owner |
| Router v3 and red-flag v3 on a new blind set | Fix the 4 missed red flags | Human-written test set |

### What the demo is, precisely

The demo page is scripted and runs in the browser. Its catalogue, limit record, groups and cohort numbers are synthetic and labelled so on the page. It shows the intended agent flow (rules check → read limits and guideline → filter 100 to 67 → KNN match → nearby groups → similar users → patient chooses → FHIR Tasks) with the FHIR calls it would make. Until the bundles are confirmed loaded in IRIS, we describe it as "designed for IRIS for Health", not "running on IRIS".

### Our ask

From the 3-minute pitch: **InterSystems mentorship to run fully on IRIS, a cardiologist to sign the limit library, and a small supervised pilot.** Each maps to a gate on P21: mentorship to engineering steps 1–5 inside G-A, the cardiologist to G-B, the pilot to G-E.

## Visualizations

### Chart 1 · Timeline bar chart: commits per hour, stacked by kind

- **Type:** stacked vertical bar chart over time.
- **Title:** "28 commits in 7 h 26 min (17–18 Oct 2026, +07:00)"
- **X axis:** hour (20:00 to 03:00). **Y axis:** commits.
- **Data:**

| Hour | Docs, research, evaluation | Code and demo | Data and experiments | Pitch | Merge |
|---|---|---|---|---|---|
| 20:00 | 3 | 0 | 0 | 0 | 0 |
| 21:00 | 3 | 1 | 0 | 0 | 0 |
| 22:00 | 0 | 0 | 0 | 0 | 0 |
| 23:00 | 0 | 0 | 0 | 0 | 1 |
| 00:00 | 4 | 0 | 0 | 1 | 0 |
| 01:00 | 0 | 1 | 5 | 0 | 0 |
| 02:00 | 0 | 3 | 0 | 2 | 0 |
| 03:00 | 0 | 2 | 0 | 2 | 0 |

- **Annotations:** markers "01:48 method frozen → 01:49 blind test → 01:55 results"; "21:14 UI with tests"; "01:16 383 FHIR resources".
- **What the reader should notice:** the order of work: safety design and evaluation framework first, then data and experiments, then demo and pitch.

### Chart 2 · Line chart: cumulative lines inserted

- **Type:** step line chart.
- **Title:** "Cumulative lines in the repository (generated JSON included)"
- **X axis:** hour. **Y axis:** cumulative lines inserted.
- **Data:**

| End of hour | Cumulative lines inserted |
|---|---|
| 20:00 | 938 |
| 21:00 | 3,015 |
| 23:00 | 3,015 |
| 00:00 | 3,508 |
| 01:00 | 27,249 |
| 02:00 | 29,488 |
| 03:00 | 31,836 |

- **Annotation:** at 01:00, "22,177 lines in one commit: generated synthetic FHIR bundles".
- **What the reader should notice:** volume is not effort; the jump is generated data, flagged as such.

### Chart 3 · Three-column status chart: built, reused, planned

- **Type:** categorical column map (three columns of items with icons).
- **Data:**

| Built here | Reused | Planned |
|---|---|---|
| FHIR data model + generator | InterSystems FHIR-AI Hackathon Kit | Live IRIS run of the demo |
| 383 synthetic resources, 9 bundles | IRIS for Health Docker + tutorials | SQL Builder projection |
| Loader for the kit's IRIS server | Open weights: Qwen3, MedGemma | Vector tables, Thai embeddings |
| Heartstep UI, rules-only checks (6/6 tests) | `fhir.resources` (R4B validation) | MCP server over FHIR |
| Router v1 + v2 (blind, frozen method) | 2024 Compendium METs | Model serving, Thai TTS |
| Scripted 8-step recommender demo | katgpt-rs (team's own, since May 2026) | Clinician web app |

- **What the reader should notice:** every claim on the main slides maps to one of these columns.

### Chart 4 · Bar chart: who and what wrote the commits

- **Type:** horizontal bar chart.
- **Title:** "Commit authorship and AI assistance, as recorded in git"
- **Data:**

| Author (git name) | Commits | With Claude co-author trailer |
|---|---|---|
| Admin | 26 | 26 |
| suteekarn / SuteekarnPhasugmool | 2 (1 commit + 1 merge) | 0 |

- **What the reader should notice:** AI assistance is disclosed, not hidden.

## Numbers and claims ledger

| Claim | Value | Source | Status |
|---|---|---|---|
| First and last commit | 2026-10-17 20:28 +07:00; 2026-10-18 03:54 +07:00 | `git log` | checked |
| Window inside event period | — | GrandHack schedule | to verify |
| Commits | 28 (26 Admin, 2 suteekarn incl. merge) | `git log` | checked |
| Lines inserted | 31,836 total; 22,177 in `3c06d2c` | `git log --shortstat` | checked |
| Router v2 order | freeze 01:48, test 01:49, results 01:55 | `git log` | checked |
| Synthetic resources | 383 in 9 bundles | `synthetic/fhir/*.json` | checked (synthetic) |
| UI tests | 6 of 6 pass | `npm test`, 2026-10-18 | checked |
| Claude co-author trailers | 26 (23 Opus 5.5, 3 Sonnet 5.5) | `git log --format=%B` | checked |
| katgpt-rs history | first commit 2026-05-04; 2,706 commits; MIT; modelless | katgpt-rs git log and README | checked |
| Compendium-coded activities | 44 of 100 | `demo/agent-flow-demo.html` | checked |
| Kit reused, not committed | `FHIR-AI-Hackathon-Kit/` untracked | `git status` | checked |
| Team roles | — | `pitch/README.md` placeholders | missing |
| Bundles loaded in IRIS | — | `pitch/README.md` open item | to confirm |

## Limits and open questions

- Team roles, backgrounds and who maps to which git name are not in the repo; the team must fill them.
- Whether all commits fall inside the official event window is not verified.
- Line counts overstate effort because of generated JSON; commit counts understate pair work.
- The demo is scripted; no part of it calls IRIS or a model live yet.
- AI assistants drafted much of the text and code; the team should be ready to explain any file on request.

## Likely judge questions

1. **"What did you build during the event?"** The design and safety rules, the FHIR data model and 383 synthetic resources with a loader for IRIS, the UI with passing tests, two router experiments with a frozen-then-blind method, and the recommender demo, all in a git history that starts at 20:28 on 17 October.
2. **"What did you reuse?"** The InterSystems FHIR-AI Hackathon Kit and its IRIS for Health setup, open Qwen3 and MedGemma weights, the Compendium MET table, and katgpt-rs, our own decoding library from before the event, which is R&D only and not in the demo.
3. **"Is it running on IRIS?"** Not yet live in the demo: the data model and loader are built for the kit's FHIR server, and the demo is scripted in the browser. That is exactly what we are asking InterSystems mentorship for.
4. **"Did AI write this?"** AI coding assistants helped a lot, and the git history says so on every commit from the main machine. The decisions on safety, scope and what not to claim are ours, and every number traces to a file.
5. **"Who are you and what do you need?"** Calvin, P and Toon. We need InterSystems mentorship to run fully on IRIS, a cardiologist to sign the limit library, and a small supervised pilot.

## Sources

Repo files and commands:
- `git log` (dates, authors, `--shortstat`, commit bodies), `git status`
- `README.md`, `HANDOFF.md`, `pitch/README.md`, `pitch/main-3min.md`, `pitch/deck-3min/slides/tech.html`
- `synthetic/README.md`, `synthetic/fhir/*.json`, `synthetic/generate_fhir.py`, `synthetic/load_to_iris.py`
- `tests/safety.test.mjs`, `tests/ui.test.mjs` (`npm test` run 2026-10-18)
- `experiments/` (router v1, v2)
- `demo/agent-flow-demo.html`, `demo/problem-story.html`
- `pitch/appendix/A02-system-architecture.md`, `pitch/appendix-deck/P20-team-built-vs-reused.md`
- katgpt-rs repository: `/Users/admin/Project/katgpt-rs/README.md` and its git log (outside this repo)

External:
- FHIR-AI Hackathon Kit (as linked in `docs/pitch/faq-appendix/slides/sources.html`): https://github.com/intersystems-community/FHIR-AI-Hackathon-Kit (not re-opened for this page)
- 2024 Adult Compendium, sports (opened 2026-10-18): https://pacompendium.com/sports/

## Image-generation prompt

Design one 16:9 information slide on a white background. Title, the key message: "What you saw is exactly what exists: built here in one night, reused with credit, or still planned." Top: a stacked bar timeline "28 commits, 20:00 on 17 Oct to 03:54 on 18 Oct (+07:00)" with hours 20:00 3, 21:00 4, 23:00 1, 00:00 5, 01:00 6, 02:00 5, 03:00 4, coloured by docs/research, code/demo, data/experiments, pitch, with a marker "01:48 method frozen → 01:49 blind test → 01:55 results". Below: three columns "Built here" (FHIR data model + generator; 383 synthetic resources, 9 bundles; IRIS loader; UI, 6/6 tests; router v1 + v2; recommender demo), "Reused" (InterSystems FHIR-AI Hackathon Kit; IRIS for Health Docker; Qwen3, MedGemma weights; 2024 Compendium METs; katgpt-rs, team's own since May 2026), "Planned" (live IRIS run; SQL Builder; Vector tables; MCP server; model serving, Thai TTS; clinician app). Footer strip: "Our ask: InterSystems mentorship · a cardiologist to sign the limit library · a small supervised pilot". Small note: "Built with AI coding assistants, disclosed in git." Team names Calvin, P, Toon with no titles. No photos, no logos, no other numbers. ChatGPT chooses the design.
