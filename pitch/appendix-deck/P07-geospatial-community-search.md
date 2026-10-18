# P07 · How do you find real places and groups near the patient?

## Image-generation prompt

```text
STYLE: Render ONE presentation slide, 16:9, exactly 1920×1080 px, flat vector look. Clean white background (#FFFFFF), no gradients, no textures, no photos, no 3D, no drop shadows except a very soft 4 px shadow under panels. Palette: deep teal #12363B for the title and main text; teal #1B7F7A for accents, arrows, lines and the active tab; orange #C2571A for at most two highlights per slide (one key number or one warning); soft greys #F3F5F6 (panel fills), #D9DEE0 (panel borders, 2 px, 16 px rounded corners), #6B7780 (small text). Title font: modern geometric sans like "Prompt", semibold; body font: clean sans like "Inter", regular. Icons: flat "lineal colour" style, thick black outlines (about 3 px), pastel fills (pale teal #CDEBE8, pale orange #F8DCC8, pale grey #E6EAEC), simple and friendly, like a hand-drawn doctor icon. Fixed frame: (1) breadcrumb top-left at x=80, y=44, 20 px, letter-spaced caps, grey #6B7780; (2) title at x=80, y=80, max width 1760 px, 44 px semibold deep teal, one or two lines; (3) footer source line at x=80, y=972, 15 px grey; (4) bottom navigation strip from y=1010 to y=1060 across the full width: six tabs "Why us", "IRIS + FHIR", "Agent", "Safety + tests", "Cost + speed", "Clinic + business", 16 px, grey text, with the active tab filled teal #1B7F7A and white text; (5) page tag bottom-right inside the strip, e.g. "A01", 16 px. Spell every piece of text exactly as quoted. Do not add any text, numbers, logos, watermarks or captions that are not listed.

ACTIVE TAB: "IRIS + FHIR". PAGE TAG: "A07".

BREADCRUMB: "IRIS + FHIR | COMMUNITY NEAR HOME"
TITLE: "Groups come from FHIR places near home, filtered by rules before anything is ranked."

LAYOUT: a five-step horizontal flow (y=180 to y=470); below it, left a small stylised map panel (x=80 to x=760, y=500 to y=900) and right a data-source table (x=800 to x=1840, y=500 to y=900). Footer below.

FIVE-STEP FLOW (numbered rounded boxes, teal arrows; each box has a small lineal-colour icon, a bold name and one grey line):
  "1 Service area" – "home district, not address" (house icon)
  "2 FHIR candidates" – "Location + HealthcareService" (teal badge "FHIR")
  "3 Safety filter" – "intensity ≤ limit · open · heat" (teal badge "RULES ONLY")
  "4 Rank" – "patient's own words" (teal badge "VECTOR")
  "5 Three choices" – "sent with the mission"

MAP PANEL (flat, pale grey background, no real street names): a dark dot labelled "Home district" at the centre, a soft teal circle around it labelled "≈ 15-minute walk", and three orange #C2571A pins inside the circle with small labels "park", "temple", "mall". Under the map a monospace line: "HealthcareService?location.near=13.67|100.60|5|km" and an orange text tag after it: "near on IRIS: to confirm".

DATA-SOURCE TABLE (header row teal text, thin grey lines), columns "Data", "Source", "Stored as":
  "Parks, temples, malls" | "OpenStreetMap" | "Location"
  "Walking groups, tai chi" | "Curated list" | "HealthcareService"
  "Heat" | "TMD or Open-Meteo" | "tool result"
  "PM2.5" | "Air4Thai" | "tool result"
  Under the table, a small orange outlined badge "SYNTHETIC: 8 Locations, 7 HealthcareServices".

TAKEAWAY STRIP (pale teal): "The model never invents a place or a group."

FOOTER: "Source: pitch/appendix/A05; docs/pitch/faq-appendix/slides/geo.html; synthetic/fhir/00_shared_reference_data.json"

DO NOT: draw a real Bangkok street map or real place names; add logos of OpenStreetMap or any agency; add distances other than "≈ 15-minute walk"; add extra pins.
```

## Page spec

| Field | Value |
|---|---|
| Judge question | "How do you find real places near the patient? Is it private?" |
| Page type | Value-chain flow (mirrors template slide 16) + a data table (template slide 7 matrix, small) |
| Layout | 5-step flow, stylised map, source table, takeaway |
| On-slide words | ≈ 100 |

## On-slide text (exact)

- Breadcrumb: IRIS + FHIR | COMMUNITY NEAR HOME
- Title: Groups come from FHIR places near home, filtered by rules before anything is ranked.
- Flow: 1 Service area (home district, not address) → 2 FHIR candidates (Location + HealthcareService) [FHIR] → 3 Safety filter (intensity ≤ limit · open · heat) [RULES ONLY] → 4 Rank (patient's own words) [VECTOR] → 5 Three choices (sent with the mission)
- Map: Home district; ≈ 15-minute walk; park; temple; mall; `HealthcareService?location.near=13.67|100.60|5|km`; near on IRIS: to confirm
- Table: 4 rows as in the prompt; badge SYNTHETIC: 8 Locations, 7 HealthcareServices
- Takeaway: The model never invents a place or a group.

## Visual spec

- The order matters and must read left to right: rules filter (step 3) comes before vector ranking (step 4).
- The map is a diagram, not geography. No real streets.
- Synthetic examples for the speaker: "Air-conditioned mall walkers club" (light, indoor, good on hot or smoky days), "Supervised cardiac rehab class" (moderate, needs referral), "Evening walking circle, Community Track".

## Speaker notes (Q&A)

Places and groups are FHIR `Location` and `HealthcareService` resources with coordinates, opening hours, an indoor flag and an intensity tag. The patient's home is stored as a district with a district-level position, not an exact address, for PDPA reasons. Rules first remove anything above the limit, closed at the mission time, or outdoors on a hot or smoky day; only then does Vector Search rank what is left against the patient's own words, such as "quiet, near a temple, with friends". No public API lists Thai community exercise groups, so v1 uses a curated list, and we still need to confirm that the IRIS FHIR server supports `near` and the chained form; the fallback is projecting `Location.position` with SQL Builder and filtering by distance in SQL.

## Data needed for this page

| Item | Value | Source | Status |
|---|---|---|---|
| Synthetic places and groups | 8 Locations, 7 HealthcareServices | counted from `synthetic/fhir/00_shared_reference_data.json` | Checked |
| Demo near-search call | `13.67|100.60|5|km` | `demo/agent-flow-demo.html` | Scripted, not live |
| "≈ 15-minute walk" service area | from OSM routing | `docs/pitch/faq-appendix/slides/geo.html`, A05 | Design, not built |
| `near` support on IRIS FHIR | — | A05 | **Missing: check `/fhir/r4/metadata` or ask mentors** |
| Real Thai group list | — | A05 | **Missing: no public API; curated list not started** |

## Sources in repo

- `pitch/appendix/A05-intersystems-vector-search-and-geo.md` (geo section)
- `docs/pitch/faq-appendix/slides/geo.html`
- `synthetic/generate_fhir.py`, `synthetic/fhir/00_shared_reference_data.json`
- `demo/agent-flow-demo.html` (`COMMUNITY`, near-search call)
