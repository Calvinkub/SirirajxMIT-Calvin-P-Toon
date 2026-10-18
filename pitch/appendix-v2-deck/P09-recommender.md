# P09 · The recommender filters for safety first, then ranks by taste: Netflix for a healthy heart, inside the doctor's limits.

## Key message

Heartstep recommends activities the way Netflix recommends films, with one difference: a rules filter removes everything outside the doctor-signed limits **before** any ranking runs, so no score can bring an unsafe activity back. In the demo, the filter keeps 67 of 100 activities, and a content-based nearest-neighbour match on tag vectors turns "I used to play tennis" into badminton, bowling and table tennis (cosine 0.945 each). Today only the taste signal ranks; the "people like you" and "near you" signals are shown with invented data, and collaborative filtering, exploration and diversity re-ranking are the planned next steps once real users exist.

## Why this matters to the judges

- **Innovation.** Most patient apps hand out one generic plan. Heartstep treats exercise as a recommendation problem ("what will *this* person enjoy and keep doing?"), constrained by a clinical hard filter. Combining a recommender with a clinician-signed constraint set is the core idea behind the "Netflix for a healthy heart" line.
- **Real-world impact.** The panel's behaviour reviewer named week-4 retention as the main threat (`SYNTHESIS.md` R16). People keep doing what they enjoy; a recommender aims at enjoyment and lets us measure acceptance and retention directly.
- **Use of InterSystems technology.** The catalogue, limits and community groups are designed to live in IRIS for Health: limits in a FHIR `CarePlan`, groups as FHIR `HealthcareService` + `Location`, activity vectors in IRIS Vector Search, the filter as SQL over FHIR SQL Builder projections (see P06–P08).
- **Technical coherence.** The safety filter and the ranker are separate components with a one-way dependency: the ranker only ever sees the allowed set. This is the same "rules decide what is allowed, models decide what is preferred" split used across the system (P12).

## Full detail

### 1. What "Netflix-style" means here, and what it does not mean

Netflix describes its recommender as a set of algorithms (a personalised ranker, a video-to-video similarity algorithm that drives "Because You Watched" rows, page generation) that together influence "choice for about 80% of hours streamed", with the remaining 20% from search (Gomez-Uribe and Hunt 2015, §2.8). Its point about choice is relevant to us: members lose interest "after perhaps 60 to 90 seconds of choosing, having reviewed 10 to 20 titles (perhaps 3 in detail)". Heartstep borrows three ideas:

1. **Item-to-item similarity ("Because you liked tennis").** Netflix's "sims" algorithm is unpersonalised item similarity; personalisation comes from which anchors are chosen. Our demo works the same way: the anchor is what the patient says they enjoyed, and similarity is computed over item features.
2. **A short list, not a catalogue.** We show **3 options**, matching the "perhaps 3 in detail" observation, and the patient picks one.
3. **Evaluate on retention, not clicks.** Netflix chose member retention and streaming hours as A/B metrics (§4.1). Our equivalent is week-4 activity, which is already metric E-1 (day-7, day-28 active rate) in our evaluation plan (`system-eval.md`).

What we do **not** borrow: Netflix optimises engagement without a safety constraint. In Heartstep, engagement is optimised only *inside* a set that a clinician signed. More watching is fine for films; more exertion is not automatically fine for a hypertensive 58-year-old.

### 2. The pipeline as implemented in `demo/agent-flow-demo.html`

The demo is scripted JavaScript running in the browser. It does not call a model, IRIS or a database. Everything below was counted from the file with Python on 2026-10-18.

**Step A: catalogue.** 100 activities in a `RAW` table, each with an English and Thai name, a MET value, a tag string, a flag string and an optional 2024 Adult Compendium code. 44 have a Compendium code (one marked `*` = "closest listed activity"); the other 56 MET values are team estimates, and the demo footer says a clinician must check them. The catalogue mixes Western and Thai activities: golf, petanque, sepak takraw, ram mai phlong (stick dance), ramwong, ruesi dat ton (Thai self-stretching), walking meditation at a temple, senior walking groups.

**Step B: tags become a vector.** 11 binary dimensions: `o` outdoor, `i` indoor, `t` team, `b` ball, `a` aim/skill, `s` social, `c` competitive, `w` water, `r` rhythm, `m` mind-body, `k` walking-based. Badminton (social) is `ibas` → (0,1,0,1,1,0,1,0,0,0,0). Three safety flags are kept separate from the taste vector: `x` contact, `h` heavy straining or breath-holding, `v` vigorous bursts.

**Step C: hard filter (rules, before ranking).** `allowed = ACTS.filter(a => a.met <= LIMIT.maxMet && !/[hxv]/.test(a.flags))`. With the synthetic signed limit of 5.9 METs, 67 activities remain. The 33 removed break down as: 4 by MET alone (walking uphill 6.0, tennis doubles 6.0, leisurely swimming 6.0, recreational trampoline 6.3), 4 by flag alone (power yoga, digging the garden, plank holds: `h`; Muay Thai bag work: `x v`), and 25 by both. Across the catalogue, 6 activities carry `x`, 7 carry `h` and 25 carry `v`; every flagged activity is removed. The flag rules mirror the paraphrased ESC 2020 hypertension lines in the demo ("avoid heavy weightlifting with static effort and breath-holding"; "no high-intensity exercise until blood pressure is controlled").

**Step D: taste query.** Liked activities are detected with 13 keyword rules (`LIKES`, Thai and English). The query is the mean of their tag vectors. Liked activities that are *not* allowed still contribute to the query: tennis singles (8.0 METs, `v`) is excluded from the recommendations but still tells the ranker "this person likes ball and aim sports". This is the key to the tennis example: the taste comes from the past, the options come from the allowed present.

**Step E: content-based KNN.** `ranked = allowed.map(a => ({a, s: cos(q, a.vec)})).sort((x, y) => y.s - x.s || x.a.met - y.a.met)`. Cosine similarity, k = 5 shown in the trace, top 3 offered. Ties are broken by **lower MET first**, a conservative choice: when two activities are equally similar, the easier one ranks higher.

**Step F: community and cohort (displayed, not ranked).** For each of the top 3, a keyword maps the activity to an invented community group with distance and time (e.g. "Community table-tennis room (synthetic) · 0.9 km · daily 16:00–20:00"). An invented cohort table gives "share of similar users still active after 4 weeks (synthetic cohort, n = 52)". **Neither number changes the ranking.** They are shown to illustrate the "people like you" and "near you" signals.

**Step G: patient choice.** The patient taps one of 3 options, then "2 sessions" or "3 sessions". The week is assembled from fixed templates (30 min of the chosen activity, 20-min brisk walks on other days, Sunday rest) and labelled "heart rate under 120 · no breath-holding".

### 3. Worked example: Somchai, 58, used to play tennis, now has hypertension

Preset message: "I used to play tennis every weekend, but now I have hypertension and my doctor says I must lower the intensity. Maybe badminton or bowling? Can you recommend a plan?"

- Keyword rules detect three liked activities: **badminton, social** (`ibas`, 5.5 METs), **tennis, singles** (`obac`, 8.0 METs, flag `v`) and **bowling** (`iabs`, 3.8 METs). The Thai version of the preset detects the same three.
- Query vector (mean): outdoor 0.33, indoor 0.67, ball 1.00, aim/skill 1.00, competitive 0.33, social 0.67, all others 0.
- Tennis singles fails the filter (8.0 > 5.9 METs and `v`), so the patient is told: "Tennis is too intense with your blood pressure for now."
- Top 3 among the 67 allowed: **bowling (3.8 METs), table tennis social (4.0), badminton social (5.5)**, all at cosine 0.945; the MET tie-break orders them.
- Community (synthetic): seniors' bowling league 3.2 km Wed 10:00; table-tennis room 0.9 km daily 16:00–20:00; social badminton club 1.9 km Tue & Fri 18:30.
- Cohort (synthetic, invented): 49%, 52%, 57% still active at week 4. Not data.

The second preset ("I usually played football … my lifestyle goal is to play golf") gives walking football, golf walking and carrying clubs, golf with a pull cart (cosine 0.894 each), and football is excluded for contact and bursts.

### 4. Why filter before ranking (and not "rank, then check")

If the ranker ran over all 100 activities, the tennis query's top 10 would include **badminton, competitive** (7.0 METs, `v`) at rank 4; the football + golf query's top 5 would include **football, casual** and **football, competitive** at ranks 4–5 (cosine 0.894, tied with the top 3). A "rank then check" design would need the check to be perfect and would leak unsafe items into explanations, logs, cohort statistics and any learned model trained on impressions. Filtering first means:

- the ranker never sees an unsafe item, so a future learned ranker cannot learn to push one;
- the safety property is a set-membership test that can be property-tested (`mission.intensity <= patient.limits.max`, L1 property 1 in `system-eval.md`);
- the explanation "too intense for now" comes from the rule that removed the item, not from a model.

Rejected alternatives: (a) a soft penalty for high-MET items in the score (an unsafe item could still win with a strong enough taste match); (b) letting an LLM pick from the whole catalogue and validating afterwards (generative choice of an unsafe item is exactly what the panel's S0 findings warn about); (c) one global "heart-healthy" list (that is the one-guideline-for-everyone problem from P02).

### 5. What the current ranker gets wrong (measured on the demo)

The tag vector is hand-made and coarse. That is acceptable for a demo and a cold-start fallback, but its weaknesses are measurable:

- **Many ties.** Among the 67 allowed activities the tennis query produces only 18 distinct cosine values; the golf + football query produces 13. The top 3 in the tennis case are tied exactly, so the MET tie-break, not taste, sets the order.
- **Low diversity.** Intra-list diversity (mean pairwise 1 − cosine between the 3 options) is **0.000** for the tennis case (bowling, table tennis and badminton have identical tag sets) and **0.133** for golf + football (two of three options are golf variants).
- **Odd neighbours for sparse tags.** Single-like queries expose the problem: "jogging" (tag `o` only) → fishing from the bank, light gardening, horse riding at a walk (all cosine 1.0); "Muay Thai" (tag `i` only) → general housework, light stationary bike, light resistance bands. These are allowed but are not what a jogger or boxer wants.
- **Narrow coverage.** Over 12 single-like queries (one per working keyword rule), only **23 of the 67** allowed activities ever appear in a top 3.
- **A bug.** The `LIKES` rule for dance maps to "Line dancing", but the catalogue entry is "Line dancing, moderate". `ACTS.find` returns `undefined`, so any message mentioning dance (เต้น, รำ, "dance") breaks the plan. Found by this count; not yet fixed (this page does not edit the demo).

### 6. How the recommender evolves (plan, not built)

The direction follows the standard recommender literature, with the safety filter fixed in front of every stage.

**Stage 1 (now): content-based, cold start by design.** Koren, Bell and Volinsky (2009) describe content filtering as building a profile of each item and user, and note that collaborative filtering, while "generally more accurate", "suffers from what is called the cold start problem", where content filtering "is superior". A new hospital programme has no interaction history, so content-based ranking is the right first stage. Improvements before any user data: richer item features (Compendium MET, impact, upper-body load, heat exposure, cost, equipment, Thai availability), multilingual text embeddings of activity descriptions in IRIS Vector Search instead of 11 binary tags, and an onboarding "taste" question ("which of these did you enjoy?").

**Stage 2: hybrid with collaborative filtering once real users exist.** Implicit feedback (accepted, completed, repeated, skipped) feeds a matrix-factorisation or item-item collaborative filter. Koren et al. note that implicit feedback can be gathered "regardless of the user's willingness to provide explicit ratings", which matters for older patients who will not rate things. The De Croon et al. (2021) systematic review of 73 health recommender systems for laypersons found hybrid designs most common (44%, 32/73), knowledge-based 22%, content-based 10% and collaborative filtering alone 4%: our "rules + content, then hybrid" path matches the field.

**Stage 3: proximity and cohort signals enter the score.** Proposed score over the allowed set only: `score = w_taste·content + w_cf·collaborative + w_near·proximity(time, distance, heat) + w_keep·cohort_retention`. Weights are not set; they would be fitted on pilot data. Cohort retention would come from real de-identified week-4 outcomes, never from the invented demo numbers.

**Stage 4: diversity and exploration.** Re-rank the top candidates with Maximal Marginal Relevance (Carbonell and Goldstein 1998), which trades relevance against similarity to items already chosen, so the 3 options differ (e.g. one ball sport, one walking group, one mind-body class). Exploration with a contextual bandit (Li et al. 2010 reported a 12.5% click lift over a context-free bandit on Yahoo! news) can test new activities on a small share of slots, again **only among allowed items**.

**Constant: the safety filter.** Every stage takes the allowed set from the rules engine as its input. No learned weight can change the MET ceiling or the flags, and the server re-validates the chosen activity before a FHIR `Task` is written (P12).

### 7. How we would evaluate it

Offline (on logged data): hit rate and precision at 3 against what patients later chose; catalogue coverage (today 23 of 67 across 12 single-like queries); intra-list diversity (today 0.000 and 0.133 for the two presets). Online (pilot): acceptance rate (one of the 3 options picked), week-1 completion, **week-4 retention** (E-1 day-28 active), mission completion (E-2), mute or opt-out rate (E-3). Safety: allowed-set violations = 0, checked by construction and by property test. De Croon et al. found only 53% (39/73) of health recommender studies evaluated with users and only 8% (6/73) used an RCT, and only 12% reported ethics approval; we plan user evaluation behind an IRB decision (gate G-D).

## Visualizations

### Chart 1 · Stacked bar: what the safety filter keeps, by category

- Type: horizontal stacked bar (kept vs removed) per category; title "100 activities → 67 allowed by the signed limits".
- Axis: number of activities. Categories as defined by the demo's `cat()` function (water > rhythm/dance > mind-body > ball/aim > walking > other, first match wins).

| Category | In catalogue | Kept (≤ 5.9 METs, no x/h/v) | Removed |
|---|---|---|---|
| Ball and aim sports | 30 | 21 | 9 |
| Walking-based | 12 | 11 | 1 |
| Dance and rhythm | 8 | 6 | 2 |
| Water | 7 | 6 | 1 |
| Mind-body | 9 | 8 | 1 |
| Other (cycling, gym, garden, misc.) | 34 | 15 | 19 |
| **Total** | **100** | **67** | **33** |

- Annotation: "Removed: 4 by METs only, 4 by flags only, 25 by both".
- What to notice: gym-style and vigorous items carry most of the removals; ball sports keep 21 options, which is why a former tennis player still gets ball-sport choices.

### Chart 2 · Horizontal bar: top 12 allowed matches for the tennis example

- Type: horizontal bar, cosine similarity (0–1) on x; label each bar with METs. Title: "Liked: tennis, badminton, bowling → nearest allowed activities".

| Rank | Activity | Tags | METs | Compendium 2024 code | Cosine |
|---|---|---|---|---|---|
| 1 | Bowling | iabs | 3.8 | 15092 | 0.945 |
| 2 | Table tennis, social | ibas | 4.0 | 15660 | 0.945 |
| 3 | Badminton, social | ibas | 5.5 | 15030 | 0.945 |
| 4 | Petanque | oabs | 3.3 | 15465 (closest) | 0.850 |
| 5 | Bocce | oabs | 3.3 | 15465 | 0.850 |
| 6 | Croquet | oabs | 3.3 | 15160 | 0.850 |
| 7 | Golf with a power cart | oabs | 3.5 | 15290 | 0.850 |
| 8 | Miniature golf | oabs | 3.5 | 15270 | 0.850 |
| 9 | Pickleball | obas | 4.5 | estimate | 0.850 |
| 10 | Putting practice | oab | 2.3 | estimate | 0.764 |
| 11 | Darts | ias | 2.5 | 15180 | 0.764 |
| 12 | Billiards | ias | 2.5 | 15080 | 0.764 |

- Annotation: bracket ranks 1–3 "offered to Somchai"; note "ties broken by lower MET".
- What to notice: the offered three are tied; tennis itself (8.0 METs) is absent because it was filtered out before ranking.

### Chart 3 · Side-by-side table: rank without the filter vs with the filter

| Query | Rank 4 if ranking ran on all 100 | Rank 4 with filter first |
|---|---|---|
| Tennis + badminton + bowling | Badminton, competitive (7.0 METs, bursts), cosine 0.850 | Petanque (3.3 METs), cosine 0.850 |
| Football + golf | Football, casual (7.0 METs, contact + bursts), cosine 0.894; rank 5 Football, competitive | Volleyball, recreational (3.0 METs), cosine 0.875 |

- What to notice: unsafe items score as high as safe ones on taste; only the filter keeps them out.

### Chart 4 · Grouped bar: MET bands before and after the filter

| MET band | In catalogue | Allowed |
|---|---|---|
| < 3.0 | 13 | 13 |
| 3.0–3.9 | 27 | 26 |
| 4.0–4.9 | 15 | 14 |
| 5.0–5.9 | 16 | 14 |
| ≥ 6.0 | 29 | 0 |

- What to notice: nothing at or above 6.0 METs survives; 14 allowed items sit within 0.9 MET of the ceiling (5.0–5.9), so MET accuracy matters most there (badminton social 5.5 is one of them).

### Chart 5 · Bar: diversity and coverage of the current ranker

| Measure | Value |
|---|---|
| Distinct cosine values among 67 allowed, tennis query | 18 |
| Distinct cosine values, football + golf query | 13 |
| Intra-list diversity of offered 3, tennis | 0.000 |
| Intra-list diversity of offered 3, football + golf | 0.133 |
| Allowed activities ever in a top 3 (12 single-like queries) | 23 of 67 |

- What to notice: the content ranker works for the demo but is coarse; this is the measured case for embeddings, MMR re-ranking and collaborative filtering.

### Diagram · Signal pipeline

`Patient message → red-flag screen (rules) → liked activities (keyword rules) → signed limits (FHIR CarePlan) → HARD FILTER 100 → 67 (rules) → taste rank: cosine KNN (implemented) → [near you: community groups (synthetic, shown)] → [people like you: week-4 cohort (invented, shown)] → 3 options → patient picks → FHIR Tasks + Provenance`. Mark the filter box as a wall: arrows pass only through it. Mark the two bracketed signals "displayed only in demo".

## Numbers and claims ledger

| Claim | Value | Source | Status |
|---|---|---|---|
| Catalogue size | 100 | `demo/agent-flow-demo.html` `RAW`, counted with python3 | checked |
| Activities with a 2024 Compendium code | 44 (1 "closest listed") | same | checked; codes not re-verified against pacompendium.com |
| Allowed after filter | 67 | same, `met ≤ 5.9` and no `h/x/v` | checked |
| Removal reasons | 4 MET only, 4 flag only, 25 both | same | checked |
| Flag counts | x 6, h 7, v 25 | same | checked |
| Category before/after | see Chart 1 | same, demo `cat()` | checked |
| Tennis top 3 cosine | 0.945 each | same, `cos()` reimplemented in python3 | checked |
| Football + golf top 3 cosine | 0.894 each | same | checked |
| Distinct scores, ILD, coverage | 18 / 13; 0.000 / 0.133; 23 of 67 | same | checked (our computation) |
| Dance keyword bug | "Line dancing" not in catalogue | same | checked |
| Signed limit 5.9 METs, HR 120, RPE 11–13 | — | `LIMIT` in demo | synthetic |
| Community groups and distances | e.g. 0.9 km table tennis | `COMMUNITY` in demo | synthetic |
| Week-4 cohort percentages, n = 52 | e.g. 49%, 52%, 57% | `COHORT` in demo | synthetic, invented; never quote as data |
| Netflix: recommendations influence ~80% of hours streamed | ~80% | Gomez-Uribe & Hunt 2015, §2.8 | checked (PDF opened) |
| Netflix: 60–90 s, 10–20 titles, ~3 in detail | — | same, §1 | checked |
| CF more accurate but suffers cold start | — | Koren, Bell, Volinsky 2009 | checked (PDF opened) |
| HRS review: 73 studies; hybrid 44%; CB 10%; CF 4%; users in 53%; RCT 8%; ethics 12% | — | De Croon et al. 2021 (PMC8278303) | checked |
| Contextual bandit 12.5% click lift | 12.5% | Li et al. 2010, arXiv 1003.0146 | checked (abstract) |
| 2024 Adult Compendium covers adults 19–59; separate Older Adult Compendium exists | — | pacompendium.com (older-adult compendium listed); age range from search abstract | older-adult compendium checked; 19–59 range to verify |
| Recommender raises adherence or retention for cardiac patients | — | — | not shown; to test in pilot |

## Limits and open questions

- **Only one signal ranks today.** Taste (content cosine) is implemented; "near you" and "people like you" are displayed with invented data and do not change the order. The "Netflix" claim is about the design direction, not about a trained model.
- **MET values.** 56 of 100 are estimates. The 2024 Adult Compendium was built for adults aged 19–59 (to verify); the target users are 45–75, and pacompendium.com lists a separate Older Adult Compendium that should be checked for patients aged 60 and over. A clinician must review every value near the ceiling.
- **MET is not the only safety dimension.** Heat, PM2.5, beta-blocker effect on heart rate, orthopaedic limits and fall risk are not in the filter yet.
- **Tag vectors are hand-made** and produce ties and odd neighbours (section 5).
- **No user data, no offline evaluation, no A/B test.** Acceptance rate and week-4 retention are planned metrics with no values.
- **Fairness and access.** Proximity and cost signals could favour patients near Bangkok facilities; not analysed.
- **Demo bug** in the dance keyword (section 5).

## Likely judge questions

**Q: Isn't this just a lookup table with cosine similarity?**
Today, yes, and we say so: a content-based KNN over 11 hand-made tags is the cold-start stage. The design choice that matters is where it sits: after a clinician-signed hard filter, so any later learned ranker inherits the same guarantee. Collaborative filtering and bandit exploration need real users, and we will not fake them.

**Q: Where do the "people like you" numbers come from?**
In the demo they are invented and labelled synthetic (n = 52). In a pilot they would be de-identified week-4 outcomes from real users with consent, and they would only re-order activities that already passed the filter.

**Q: What stops the recommender from suggesting something dangerous if the model learns badly?**
The ranker never sees unsafe items: the rules engine passes it only the allowed set (67 of 100 in the demo), and the server re-checks the chosen item against the signed limits before writing a FHIR `Task`. A learned weight cannot change a MET ceiling or a contact flag.

**Q: How will you know the recommendations are good?**
Acceptance rate of the 3 options, week-1 completion and week-4 retention in a supervised pilot, plus offline coverage and diversity. Netflix's lesson is to judge a recommender by retention in controlled tests, not by clicks.

**Q: Why 3 options?**
Choice fatigue: Netflix's consumer research points to about 3 titles looked at in detail. For older patients, fewer options with a reason each is easier; the number is a design choice to test.

## Sources

Repo:
- `demo/agent-flow-demo.html` (`RAW`, `DIMS`, `LIMIT`, `GUIDE`, `COMMUNITY`, `COHORT`, `LIKES`, `plan()`, `weekPlan()`)
- `pitch/appendix/A04-agentic-harness.md` (demo flow and honesty notes)
- `pitch/appendix-deck/P09-agent-flow-8-steps.md` (earlier 100 → 67 count)
- `.claude/skills/siriraj-mit-review-panel/references/system-eval.md` (E-1, E-2, E-3, L1 property 1)
- `evaluation/reviews/2026-10-17-document/SYNTHESIS.md` (R16 retention)

External (opened):
- Gomez-Uribe CA, Hunt N. The Netflix recommender system: algorithms, business value, and innovation. ACM TMIS 6(4), 2015. https://gwern.net/doc/reinforcement-learning/exploration/2015-gomezuribe.pdf
- Koren Y, Bell R, Volinsky C. Matrix factorization techniques for recommender systems. IEEE Computer, Aug 2009. https://datajobs.com/data-science-repo/Recommender-Systems-%5BNetflix%5D.pdf
- De Croon R, Van Houdt L, Htun NN, Štiglic G, Verbert K. Health recommender systems: systematic review. JMIR 2021;23(6):e18035. https://pmc.ncbi.nlm.nih.gov/articles/PMC8278303
- Carbonell J, Goldstein J. The use of MMR, diversity-based reranking for reordering documents and producing summaries. SIGIR 1998. https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf
- Li L, Chu W, Langford J, Schapire RE. A contextual-bandit approach to personalized news article recommendation. 2010. https://arxiv.org/abs/1003.0146
- Compendium of Physical Activities (Adult, Older Adult and Wheelchair compendia; citation Herrmann et al., J Sport Health Sci 2024;13(1):6–12). https://pacompendium.com/

## Image-generation prompt

A 16:9 information slide on a white background. Put the key message first as the title: "Safety filter first, then taste: Netflix for a healthy heart." Main visual on the left: a funnel from "100 activities" to "67 allowed by the signed limits", with a short note "removed: 4 by METs, 4 by flags, 25 by both". Main chart on the right: a horizontal bar chart of the top matches for "used to play tennis", with bowling, table tennis and badminton highlighted at 0.945 and petanque, bocce, croquet at 0.850, each bar labelled with its METs. A small strip at the bottom lists the four signals: "your taste (live)", "near you (synthetic)", "people like you (synthetic)", "you choose". Use only these numbers, no logos, no invented figures; ChatGPT chooses the design.
