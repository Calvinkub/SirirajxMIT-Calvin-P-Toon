# Template analysis: statisTISC_Presentation_VRT01.pptx (slides 1–20)

Source: `/Users/admin/Downloads/statisTISC_Presentation_VRT01.pptx` (86 slides, 16:9, 20 × 11.25 in). Analysed with python-pptx 1.0.2, first 20 slides only. Content belongs to a different project (equity research on Vertiv, Thai Intercollegiate Stock Challenge 2026); only structure is used here.

**How the counts were made.** "Text boxes" = shapes that carry text (groups walked recursively). "Words" = English/number tokens + Thai characters ÷ 6 (Thai has no spaces, so a plain split undercounts). "Drawn shapes" = freeform + auto shapes. No slide in 1–20 contains a native picture, chart or table object: **every chart, table and diagram is drawn from freeform shapes plus small text boxes** (bars, axis ticks and data labels are separate text boxes). The background comes from the master.

## Shared frame on every content slide

| Element | Position | Content pattern |
|---|---|---|
| Breadcrumb | top-left, small (~17 pt) | `Section | Sub-topic` (e.g. "Investment Thesis 1 | Power Density & Capacity") |
| Headline | full width under breadcrumb, ~22 pt, one line | **A claim sentence**, not a topic label (e.g. "Q2 revenue miss reflects timing, not demand destruction") |
| Body | 2–4 panels | Each panel has its own small header (13–18 pt) |
| Takeaway box | bottom band or right column | "Key Takeaway:" / "Our view:" / "What the market may miss" |
| Source line | bottom-left, ~10–11 pt | "Source: …; Team calculations" |
| Section nav bar | bottom strip | Overview · Thesis 1 · Thesis 2 · Thesis 3 · Valuation · Risk, current one highlighted |
| Page number | bottom-right | plain number |

## Slide-by-slide

| # | Title (paraphrased, structure only) | Slide's job (question it answers) | Layout | Text boxes | Words (est.) | Drawn shapes | Pics / charts / tables | Density |
|---|---|---|---|---|---|---|---|---|
| 1 | Company + recommendation cover | What is the call? | Cover: company name, one big recommendation block (Buy, target, upside, revenue), team names along the bottom | 8 | 36 | 12 | 0 / 0 / 0 | Very light |
| 2 | Business overview: main products | What does the company sell? | 4 product columns (header, sub-line, 3 bullets each) + revenue-split bar at bottom (Products 79.6% vs Services 20.4%) | 34 | 138 | 31 | 0 / 0 / 0 (bar drawn) | Medium |
| 3 | Snapshot + Q2 results + key drivers | How big and how fast? | 3 zones: 2×3 big-number KPI tiles (number + label + context line), drawn revenue bar chart with CAGR arrow, regional split map, right column of 3 drivers with numbers | 62 | 169 | 45 | 0 / 0 / 0 (chart drawn) | High (≈20 numbers) |
| 4 | Competitive advantage | Why does it win? | Top: 3 exposure KPIs + "results that support it" KPIs + "Team View" box. Bottom: two panels (power vs thermal) each with a big label and 1–2 lines | 39 | 209 | 41 | 0 / 0 / 0 | Medium-high |
| 5 | Sustainability of returns | Can growth fund itself? | 3 equal columns, each: numbered header, one claim, mini drawn chart, "what the market misses" note; full-width Key Takeaway at bottom | 70 | 318 | 44 | 0 / 0 / 0 (3 charts drawn) | Dense |
| 6 | Industry macro factors | What external trend drives demand? | Two trend panels: left bar chart (GW per year, estimate bars labelled), right timeline (years to grid-ready); bottom 3 levers + one big revenue-per-MW figure; "what the market may miss" line | 59 | 209 | 64 | 0 / 0 / 0 | High |
| 7 | Industry structure and competitive position | Who are the competitors and where do we stand? | Left: numbered customer list. Right: drawn matrix (4 capability rows × 3 competitors) + KPI column (#1 rankings, 5,300 engineers). Key Takeaway box | 41 | 208 | 42 | 0 / 0 / 0 (table drawn) | Medium-high |
| 8 | Key success factor | What must go right, and when? | Top-left YoY growth comparison bars; top timeline (2026 → 2028, 5 milestones); 3-tier architecture stack with labels; "collaboration spotlight" panel | 58 | 355 | 57 | 0 / 0 / 0 | Very dense |
| 9 | Trend opportunity | Which customer segment grows fastest, and why? | 3 columns: segment cards with market size + CAGR; drawn market chart with KPI tiles above it and an estimate legend; "why it keeps growing" list of 3 numbered reasons + Key Takeaway | 99 | 379 | 88 | 0 / 0 / 0 | Densest in the set |
| 10 | Investment framework (divider) | What are the 3 pillars of the argument? | Section divider: title + 3 numbered pillars, each 2–3 lines + one number + "[THESIS n]" tag | 9 | 75 | 8 | 0 / 0 / 0 | Light |
| 11 | Thesis 1: power density | What is changing technically? | Drawn bar chart (rack kW by generation, labelled 30–50 → 1,000+, "7.6×" callout) + adoption S-curve with labelled phases + "our view" line | 36 | 130 | 27 | 0 / 0 / 0 | Medium |
| 12 | Thesis 1: variant perception | Where does the market's view differ from ours? | Split: left "market view" causal chain (AI demand → MW → revenue); right "our view" equation (Revenue = MW × content/MW) + 3 KPI tiles (15+, 2.3 MW, 4 layers) | 37 | 149 | 24 | 0 / 0 / 0 | Medium |
| 13 | Thesis 1: revenue driver | What number moves, and by how much? | Two drawn charts side by side (range bars old vs new; share line 8% → 33%), each with an "Our view" box under it; chart legend says "range endpoints, not realised revenue" | 70 | 193 | 55 | 0 / 0 / 0 | High |
| 14 | (Build of 13) | Same as 13 | Animation build: one "our view" box removed | 65 | 159 | 53 | 0 / 0 / 0 | High |
| 15 | Framework divider (repeat) | Where are we in the argument? | Same as 10, next pillar highlighted | 9 | 75 | 8 | 0 / 0 / 0 | Light |
| 16 | Thesis 2: value chain | Where in the chain is value created? | Horizontal value chain of 8 boxes, "new via acquisition" vs "existing core" brackets; top row customer challenges → outcomes | 42 | 182 | 33 | 0 / 0 / 0 | Medium |
| 17 | Thesis 2: market view vs our view | Why is this more than it looks? | 4 numbered panels: how the market sees it / our view / evidence and valuation (2 KPI tiles) / financial impact; interpretation footnote | 29 | 304 | 30 | 0 / 0 / 0 | Dense (paragraphs) |
| 18 | Framework divider (repeat) | Where are we in the argument? | Same as 10 | 9 | 75 | 8 | 0 / 0 / 0 | Light |
| 19 | Thesis 3: event analysis | Was the bad number a real problem? | Left: drawn line chart vs benchmark + 3 "miss" KPI tiles (−3.1%, −17.2%, −15.7 ppts). Right: 3 "beat" KPI tiles (value, vs consensus) + 3 balance-sheet tiles (before → after) | 47 | 203 | 23 | 0 / 0 / 0 | High |
| 20 | Thesis 3: margin expansion | Is the improvement broad and repeatable? | Left: drawn margin-by-region chart + explanation; right: two drivers, each with an "A +17% VS B +24%" comparison tile | 23 | 146 | 16 | 0 / 0 / 0 | Medium |

## Page types found

| Type | Template slides | What it carries |
|---|---|---|
| T1 Cover / verdict | 1 | One verdict block with 3–5 numbers |
| T2 Column map | 2 | 3–4 parallel columns of short items + one summary bar |
| T3 KPI snapshot | 3 | 4–6 big-number tiles (number · label · context) + one chart + drivers column |
| T4 Three-pillar columns | 4, 5 | 3 numbered columns, each claim + number or mini-chart + note; full-width takeaway |
| T5 Two-trend charts | 6, 13 | 2 drawn charts side by side, each with its own "our view" box |
| T6 Matrix | 7 | Drawn grid (rows = capabilities, columns = options) + KPI column + takeaway |
| T7 Timeline + stack | 8 | Milestone timeline + layered stack diagram + spotlight panel |
| T8 Segment cards + why | 9 | Cards with size/growth, chart, numbered "why" list |
| T9 Framework divider | 10, 15, 18 | 3 pillars, ~75 words, repeated with highlight |
| T10 Evolution chart | 11 | One labelled bar progression + callout multiple ("7.6×") |
| T11 Variant perception | 12, 17 | "Market view" vs "our view", equation or numbered panels |
| T12 Value-chain flow | 16 | Left-to-right boxes, bracketed groups, outcomes row |
| T13 Event KPI tiles | 19, 20 | "Miss" tiles vs "beat" tiles, "A vs B" comparison tiles, before → after |

## Rules we take from it

1. **Words per page:** content pages sit at about 130–210 words (median ≈ 200 incl. Thai); the densest go to ~380. Dividers ~75, cover ~35. For an English Q&A appendix read from a screen, we would cap at ≈ 170 on-slide words. **Because our slides are rendered by an image model (which misspells long text), we cap on-slide text at ≈ 110 words, ≈ 140 for matrix pages,** and move the rest into speaker notes.
2. **Headline = a claim**, one sentence, full width, under a `Section | Sub-topic` breadcrumb. The question the page answers is never the headline.
3. **Numbers as tiles:** each key number gets its own tile, big (27–52 pt), with a one-line label and a one-line context ("$4.4bn → $10.2bn (FY20–FY25)"). Comparisons are shown as "A vs B" or "before → after" inside the tile. A typical content page carries 6–20 numbers.
4. **Charts are drawn and labelled directly:** every bar carries its own data label, there is no gridline reading; estimates are marked on the chart itself ("light bars = calculated from CAGR, not published", "range endpoints, not realised revenue"). We do the same for **synthetic**, **simulated** and **estimate**.
5. **Diagrams are labelled boxes with arrows and brackets** (value chain, stack, timeline). Each box has a 1–3-word name plus a one-line description. Groups are bracketed ("new via UIG" vs "existing core"); we use "rules only" vs "model" and "built" vs "planned" brackets.
6. **Every content page ends with a takeaway box** ("Key Takeaway", "Our view", "What the market may miss") and a **source line** bottom-left; page number bottom-right; section nav bar along the bottom.
7. **Page-type mix:** in 20 slides: 1 cover, 3 dividers, ~5 KPI/number pages, ~4 chart pages, ~3 diagram/flow pages, ~2 matrix/table pages, ~2 view-vs-view pages. No page is text-only; no page is image-only. A divider repeats the framework so the audience knows where they are.
8. **Panels are numbered (1, 2, 3)** when they form an argument, so a speaker can say "point 2".
9. **One build page** (13 → 14) is used to reveal a takeaway; we do not need builds in a Q&A appendix.
