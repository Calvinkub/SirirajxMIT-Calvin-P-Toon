# P07 · IRIS Vector Search ranks only what the rules allowed and answers only from clinician-approved text: no approved snippet, no answer.

## Key message

Heartstep uses IRIS Vector Search for two jobs, both behind the rules: ranking the allowed activities and groups by similarity to what the patient enjoys, and retrieving clinician-approved text so the coach can explain a mission without inventing medicine. Because IRIS stores `VECTOR` and `EMBEDDING` columns "alongside other data in a relational table", one SQL statement can filter by the signed limit and rank by `VECTOR_COSINE`. In the demo the ranking runs in the browser on 100 activities (67 allowed) and turns tennis into bowling, table tennis and badminton; the IRIS tables, the Thai embedding model and the score threshold are planned and untested.

## Why this matters to the judges

- **Use of InterSystems technology:** this is the "smart use of Vector Search" question. The weak version is "a chatbot over PDFs with IRIS as a vector store" (team note, `HANDOFF.md` via A05). Ours sits behind FHIR-based rules, ranks FHIR resources (`HealthcareService/…`), and logs which approved snippets an answer used.
- **Innovation:** the same vector machinery powers the "Netflix" part (taste similarity) and the grounding part (approved explanations), in the same namespace as the clinical record.
- **Technical coherence:** filter first (SQL `WHERE` on projected FHIR columns), rank second (`ORDER BY VECTOR_COSINE … DESC`), answer third (only with a cited snippet above a threshold).

## Full detail

### 1. What IRIS Vector Search provides (InterSystems documentation)

From "Using Vector Search" (IRIS 2025.1 documentation, opened 2026-10-18):

- "InterSystems IRIS SQL supports a dedicated VECTOR type that leverages SIMD CPU instructions to efficiently perform distance computations and an EMBEDDING type that … simplifies the conversion of a string value from a source field in the same table … into an embedding vector."
- "As VECTOR and EMBEDDING are standard SQL data types, you can store them alongside other data in a relational table, converting a SQL database transparently into a hybrid vector database."
- Similarity functions: `VECTOR_DOT_PRODUCT` and `VECTOR_COSINE`; "The larger the value of these functions, the more similar the vectors are", so queries use `ORDER BY … DESC`.
- Approximate nearest neighbour index: HNSW, created with `CREATE INDEX … AS HNSW(Distance='Cosine')`, optional `M` (default 16) and `efConstruction` (default 64). Requirements include a fixed-length VECTOR or EMBEDDING field "of type double or decimal". With Cosine distance, "all-zero vectors stored in a table are silently omitted from the index".
- Embedding configurations live in `%Embedding.Config`; IRIS ships two embedding classes, `%Embedding.OpenAI` and `%Embedding.SentenceTransformers`, and other sources need a class extending `%Embedding.Interface`.

The kit's pattern (`skills/iris-vector-search/SKILL.md`) uses `VECTOR(DOUBLE, 1536)` with OpenAI `text-embedding-3-small`, inserts with `TO_VECTOR(?)`, searches with `SELECT TOP k … ORDER BY VECTOR_COSINE(Embedding, TO_VECTOR(?, DOUBLE)) DESC`, notes that "Query and stored vectors must come from the same model", and shows combining with normal filters: `WHERE Source LIKE '%Retinopathy%' ORDER BY VECTOR_COSINE(...) DESC`.

### 2. Job 1 · Ranking activities and groups (the recommender's taste signal)

**What runs in the demo.** Each of the 100 catalogue activities has 11 binary tags: outdoor, indoor, team, ball, aim/skill, social, competitive, water, rhythm, mind-body, walking-based. The patient's liked activities (from the router's slots) are averaged into a query vector; the allowed activities are ranked by cosine similarity (`demo/agent-flow-demo.html`, `knn(query = mean(...), k = 5, metric = cosine)`).

**How it maps to IRIS.** The same computation is one statement:

```sql
CREATE TABLE CMC.Activity (
  Code VARCHAR(60), NameEn VARCHAR(100), NameTh VARCHAR(100),
  Met DOUBLE, Flags VARCHAR(5), CompendiumCode VARCHAR(10),
  Tags VECTOR(DOUBLE, 11),            -- taste features (demo)
  TextEmb VECTOR(DOUBLE, 1024)        -- later: description embedding; dim = model output
);

-- filter by the signed limit (rules), then rank by taste (vector)
SELECT TOP 5 a.Code, a.NameEn, a.Met,
       VECTOR_COSINE(a.Tags, TO_VECTOR(?, DOUBLE)) AS Score
  FROM CMC.Activity a
 WHERE a.Met <= ?                        -- from CMC.LimitRecord (P06)
   AND a.Flags NOT LIKE '%h%' AND a.Flags NOT LIKE '%x%' AND a.Flags NOT LIKE '%v%'
 ORDER BY Score DESC, a.Met ASC;
```

For 100 rows an exact scan is enough; an HNSW index pays off for groups and places across a city. Tags are a placeholder for richer features: text embeddings of activity descriptions and `HealthcareService.comment` ("Quiet slow walk with older adults after morning prayers"), and later co-occurrence from real users (P09).

**Somchai's result (demo, synthetic limit).** Query = mean(tennis singles, badminton social, bowling). Among the 67 allowed activities the top scores are bowling, table tennis and badminton (0.945 each), then six at 0.850 (petanque, bocce, croquet, golf with a power cart, miniature golf, pickleball). Tennis itself (8.0 METs, vigorous bursts) is never scored because the `WHERE` clause removed it.

### 3. Job 2 · Grounding the coach in approved text

**What we embed** (A05): mission-library explanations (team-written, clinician-approved); patient-education snippets (clinician-approved, each with its source); guideline snippets from the reconciled table, **only after clinician sign-off**; community activities (`HealthcareService.comment`); discharge-note text for onboarding extraction. We do **not** embed raw patient chat or watch streams.

**Table and query (planned):**

```sql
CREATE TABLE CMC.ApprovedContent (
  Collection VARCHAR(40),        -- mission | education | guideline | activity
  SourceRef  VARCHAR(200),       -- e.g. HealthcareService/svc-mall-walk, or guideline id + section
  ApprovedBy VARCHAR(100),       -- clinician who approved it
  Lang       VARCHAR(5),         -- th | en
  Text       VARCHAR(10000),
  Embedding  VECTOR(DOUBLE, 1024)   -- dim must equal the embedding model's output
);
SELECT TOP 4 SourceRef, Text, VECTOR_COSINE(Embedding, TO_VECTOR(?, DOUBLE)) AS Score
  FROM CMC.ApprovedContent
 WHERE Collection = 'guideline' AND ApprovedBy IS NOT NULL
 ORDER BY Score DESC;
```

**The grounding rule.** Question → red-flag screen (rules) → vector search over approved collections only → if the top score is below a threshold or the snippet is not approved, a fixed reply ("please ask your care team") → otherwise the model writes a reply citing snippet ids → an output filter checks every claim maps to a cited snippet and that there is no drug, dose or diagnosis wording → the cited ids are logged (planned `AuditEvent`). The threshold is to be tuned on a labelled calibration split, not guessed.

**What the demo shows.** For Somchai, `vector_search("hypertension exercise", collection="approved_guidelines", k=4)` returns four lines labelled "ESC 2020 sports cardiology, §4.2.3 Hypertension (paraphrased)": at least 30 minutes of moderate dynamic aerobic exercise 5–7 days a week; resistance training 2–3 days a week; avoid heavy static lifting and breath-holding; no high-intensity exercise while SBP > 160. These are hard-coded in the demo and paraphrased; the primary guideline text has not been re-checked, and `research/README.md` warns that guideline numbers must not be implemented until a rehab physician reconciles the two research summaries.

### 4. Thai: the embedding model is the open risk

The kit's model (`text-embedding-3-small`, 1536 dimensions) is called over the OpenAI API. For Thai patient-side text we need (1) good Thai retrieval and (2) embedding inside Thailand for PDPA reasons (P20). IRIS's `%Embedding.SentenceTransformers` class means a self-hosted multilingual model can be configured in `%Embedding.Config` and used through the `EMBEDDING` type. Our candidate is BGE-M3 (named in the team plan); its Thai retrieval quality on our content is **not measured**, and its output dimension must be confirmed from the model card before the column is created (the 1024 above is a placeholder to verify).

**Test plan (not run):** Thai, English and mixed queries in the style of our router set (colloquial, elderly phrasing, typos), each labelled with correct snippet ids; arms: self-hosted BGE-M3 vs the kit's `text-embedding-3-small`; metrics: Recall@3, MRR, and the share of "no good answer" queries correctly sent to the fixed reply; threshold picked on a calibration split; report on a held-out split written by someone else (the router v2 blind protocol).

### 5. Alternatives rejected

- **Let the model answer from its own knowledge.** Rejected: no audit trail and no guarantee the advice matches the clinician's limits.
- **Retrieval without a threshold (always answer with the nearest snippet).** Rejected: the nearest snippet to an off-topic or risky question is still wrong.
- **Rank first, filter after.** Rejected: a high similarity score could push an unsafe activity into the top k before filtering, and the top k would then be short. Filtering in the `WHERE` clause makes the unsafe set unreachable.
- **External vector database.** Rejected: duplicate content, separate access control, and no join with FHIR projections.

## Visualizations

### Chart 1 · Histogram: demo catalogue by intensity, allowed versus removed

- **Type:** stacked vertical bar by MET band.
- **Title:** "The signed limit removes everything above 5.9 METs before ranking"
- **Axis:** x = MET band; y = number of activities.

| MET band | Allowed | Removed | Total | With 2024 Compendium code |
|---|---|---|---|---|
| < 3 | 13 | 0 | 13 | 2 |
| 3–3.9 | 26 | 1 | 27 | 13 |
| 4–4.9 | 14 | 1 | 15 | 7 |
| 5–5.9 | 14 | 2 | 16 | 10 |
| 6–6.9 | 0 | 7 | 7 | 3 |
| 7–7.9 | 0 | 8 | 8 | 4 |
| ≥ 8 | 0 | 14 | 14 | 5 |
| **Total** | **67** | **33** | **100** | **44** |

Annotation: "4 activities under the limit removed by safety flags: power yoga and plank holds (straining), digging the garden (straining), Muay Thai bag work (contact, bursts)." Vertical line at 5.9 METs labelled "synthetic limit, cmc-p01". **What to notice:** the filter uses two kinds of rule (intensity and movement type); only 31 of the 67 allowed activities have a Compendium code, so 36 MET values are team estimates a clinician must check.

### Chart 2 · Histogram: similarity scores of the 67 allowed activities for Somchai

- **Title:** "Only a handful of allowed activities are close to what Somchai enjoys"
- **Axis:** x = cosine band; y = activities.

| Cosine band | Activities | Examples |
|---|---|---|
| ≥ 0.90 | 3 | bowling, table tennis (social), badminton (social) |
| 0.70–0.89 | 14 | petanque, bocce, croquet, miniature golf, pickleball, putting practice |
| 0.50–0.69 | 6 | — |
| 0.30–0.49 | 16 | — |
| 0.10–0.29 | 25 | — |
| 0 | 3 | — |

**Notice:** the head is short and tied, which is why "people like you" and "near you" are needed as tie-breakers (P09), and why richer embeddings should replace 11 binary tags.

### Chart 3 · Bar (planned evaluation, empty): Thai retrieval quality

- **Title:** "Thai retrieval: to be measured before launch"
- Columns: model (BGE-M3 self-hosted; text-embedding-3-small); Recall@3; MRR; correct "no answer" rate. **All values: not yet measured.** Draw as an empty frame with "TO MEASURE" so nobody reads it as a result.

### Diagram · Grounding flow

Question → Red-flag screen [RULES] → (match → stop path) / (clear → Vector Search over approved collections [VECTOR]) → score ≥ threshold and approved? → (no → fixed reply "please ask your care team") / (yes → reply cites snippet ids → claim check and output filter [RULES] → reply shown, ids logged).

## Numbers and claims ledger

| Claim | Value | Source | Status |
|---|---|---|---|
| VECTOR / EMBEDDING types, hybrid relational storage | quotes | InterSystems "Using Vector Search" (IRIS 2025.1 docs) | checked |
| HNSW syntax, M default 16, efConstruction default 64, double/decimal requirement | as quoted | same | checked |
| Built-in embedding classes | `%Embedding.OpenAI`, `%Embedding.SentenceTransformers` | same | checked |
| Kit model and dimension | text-embedding-3-small, 1536 | `skills/iris-vector-search/SKILL.md` | checked (kit) |
| Catalogue / allowed / removed | 100 / 67 / 33 | computed from `demo/agent-flow-demo.html` | checked |
| Compendium-coded (all / allowed) | 44 / 31 | computed | checked; values to verify by clinician |
| Score distribution for Somchai | as Chart 2 | computed | checked (demo) |
| Top 3 cosine | 0.945 | computed | checked |
| Guideline lines | 4, ESC 2020 §4.2.3, paraphrased | `GUIDE` in demo | primary text to verify |
| BGE-M3 dimension and Thai quality | — | — | to verify / not measured |
| Score threshold | — | — | to tune on labelled data |
| Live IRIS vector table | — | — | not built |

## Limits and open questions

- Everything in the demo runs in the browser; no IRIS vector table exists yet.
- Approved content does not exist yet beyond four paraphrased lines; it needs a clinician owner (spec rule 11).
- 36 of 67 allowed activities have estimated MET values.
- No Thai retrieval measurement; no threshold; no measurement of how often the fixed reply fires.
- The claim check ("every claim maps to a cited snippet") is a design, not an implemented checker.

## Likely judge questions

1. **"What is smart about your Vector Search use?"** It ranks only what the signed limit allows, in the same SQL statement, and the ranked items are FHIR resources the patient can book; answers must cite approved snippets or the coach says "ask your care team".
2. **"Does it work in Thai?"** Not measured yet. IRIS supports self-hosted SentenceTransformers models; BGE-M3 is the candidate, tested against the kit's OpenAI model on a blind Thai set (Recall@3, MRR).
3. **"Why not a bigger LLM instead of retrieval?"** A bigger model knows more but is not bounded by what this clinician approved; retrieval with a threshold is.
4. **"Do you embed patient chats?"** No. Only approved content and activity descriptions.
5. **"Is 11-tag cosine really 'Netflix'?"** It is the content-based starting point; real users add collaborative signals (P09).

## Sources

Repo:
- `demo/agent-flow-demo.html` (`RAW`, `DIMS`, `GUIDE`, `plan()`, `knn` and `vector_search` calls)
- `pitch/appendix/A05-intersystems-vector-search-and-geo.md`, `pitch/appendix-deck/P06-vector-search-grounding.md`
- `FHIR-AI-Hackathon-Kit/skills/iris-vector-search/SKILL.md`, `skills/iris-ai-agents/SKILL.md`
- `research/README.md`, `research/guidelines/RECONCILE-for-clinician.md`
- `docs/superpowers/specs/2026-10-17-cvd-mission-coach-design.md` §5 (rule 11)

External (opened 2026-10-18):
- InterSystems IRIS documentation, "Using Vector Search": https://docs.intersystems.com/iris20251/csp/docbook/DocBook.UI.Page.cls?KEY=GSQL_vecsearch

## Image-generation prompt

Design one 16:9 information slide on a white background. Lead with the key message as the title: "IRIS Vector Search ranks only what the rules allowed and answers only from clinician-approved text." Make the main chart a stacked histogram of the demo catalogue by MET band with exactly these values (allowed/removed): <3: 13/0; 3–3.9: 26/1; 4–4.9: 14/1; 5–5.9: 14/2; 6–6.9: 0/7; 7–7.9: 0/8; ≥8: 0/14, a line at 5.9 METs labelled "synthetic signed limit", and the callout "100 → 67 allowed → top 3: bowling, table tennis, badminton". Add a small flow "rules filter → VECTOR_COSINE rank → cite approved snippet or 'ask your care team'". Mark Thai retrieval as "to measure". No logos, no invented numbers; choose the design freely.
