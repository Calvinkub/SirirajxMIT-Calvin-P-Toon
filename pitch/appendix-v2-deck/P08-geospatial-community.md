# P08 · Groups and places come from FHIR resources near the patient's home district, filtered by rules for intensity, opening hours, heat and PM2.5 before anything is ranked.

## Key message

The "near you" signal is built from FHIR `Location` (position, opening hours, indoor flag) and `HealthcareService` (the group or class, its intensity, a free-text description) resources, searched around the patient's home district rather than a street address. Rules remove anything above the signed limit, closed at the mission time, or outdoors when it is hot or smoky; only then does ranking run, so the model never invents a place or a group. Live public data already works for the environment checks (Open-Meteo forecast and Air4Thai PM2.5, both pulled on 2026-10-18 for all 8 synthetic homes), but no public source lists Thai community exercise groups, and IRIS support for the FHIR `near` search is still to confirm.

## Why this matters to the judges

- **Real-world impact:** the evidence in P02 says patients drop out because of distance (31% of Thai CABG non-attenders cited transport) and loneliness (social support beta −0.22). A group 0.9 km away, open in the evening, is the practical answer.
- **Use of InterSystems technology:** places and groups are FHIR resources in IRIS for Health; filters run on FHIR SQL Builder projections (P06); ranking uses IRIS Vector Search (P07). The chosen group becomes a `Task` that references the `HealthcareService`.
- **Technical coherence:** the same order as everywhere else: rules filter, then rank, then the patient chooses.
- **Privacy by design:** district-level location is a deliberate PDPA data-minimisation choice.

## Full detail

### 1. The five steps

1. **Service area.** The patient's home is stored as `Patient.address.district` plus a district-centroid extension `home-district-position` (latitude, longitude), not a street address. The design target is about a 15-minute walk or a short ride, from OpenStreetMap routing (design, not built). The demo uses a 5 km radius.
2. **Candidates from FHIR.** `HealthcareService` resources whose `location` is near the centroid. FHIR R4 defines the `near` search on `Location`: "Search for locations where the location.position is near to, or within a specified distance of, the provided coordinates expressed as [latitude]|[longitude]|[distance]|[units] (using the WGS84 datum …). If the units are omitted, then kms should be assumed." `HealthcareService` has a `location` reference search parameter, so the chained form is `HealthcareService?location.near=13.67|100.60|5|km`; the R4 search page says reference parameters "may be 'chained' by appending them with a period", and notes the R4 `near` format "now supports both" the multiple separator and chaining.
3. **Safety filter (rules only).** Keep a service only if its `activity-intensity` fits the limit (light for app-only patients; moderate only if the clinician allowed it or it is supervised), the `Location.hoursOfOperation` covers the mission time, and, if the heat or PM2.5 check fails at that time, the `Location` is indoor (`indoor` extension = true) or the mission moves to a cooler time.
4. **Rank.** What is left is ranked by taste (P07), by "people like you" (P09) and by distance; the patient's own words ("quiet, near a temple, with friends") are matched to `HealthcareService.comment` with IRIS Vector Search.
5. **Three choices, sent with the mission.** Each choice is a reference to a real `HealthcareService`; the patient's pick becomes a `Task`.

### 2. Data sources and what each one gives

| Data | Source | How it enters | Status |
|---|---|---|---|
| Parks, temples, malls, tracks | OpenStreetMap via Overpass API | Curated into FHIR `Location` (position, hours, indoor) | Design; Overpass not yet queried |
| Walking groups, tai chi, mall walkers, rehab classes | Curated list (no public API found for Thai community exercise groups) | FHIR `HealthcareService` with `activity-intensity`, `comment` | 7 synthetic services |
| Heat (feels-like temperature) | Open-Meteo forecast API (Thai Meteorological Department as alternative) | Tool result at mission time, not stored per patient | Live API called 2026-10-18 |
| PM2.5 | Air4Thai (Pollution Control Department) JSON service | Tool result at mission time | Live API called 2026-10-18 |

**OpenStreetMap / Overpass.** The OSM wiki describes Overpass as "a database engine to query the OpenStreetMap data". The public instance is fine for "less than 10,000 queries per day and download less than 1 GB data per day", and for regular applications "these numbers should be divided by 100". So places should be harvested once into FHIR `Location`s and refreshed occasionally, never queried per patient request.

**Open-Meteo.** Endpoint `https://api.open-meteo.com/v1/forecast`; an API key is "Only required to commercial use"; `apparent_temperature` is "the perceived feels-like temperature combining wind chill factor, relative humidity and solar radiation"; `timezone=auto` or a named zone; up to 16 forecast days. Commercial use needs a paid licence, which matters for a paid product.

**Air4Thai.** `https://air4thai.pcd.go.th/services/getNewAQI_JSON.php` returned 173 stations on 2026-10-18; 159 had a reading dated that day (158 at 07:00). Bangkok had 79 stations, 77 with a valid reading that morning. One station we tested (10t, Bang Kapi) still reported a reading from 2023-10-12, so the tool must check the reading's timestamp and fall back to the next station.

### 3. Worked example: Somchai's groups (demo) and the real environment that morning

In the demo, Somchai's three choices come with synthetic groups: seniors' bowling league 3.2 km (Wed 10:00), community table-tennis room 0.9 km (daily 16:00–20:00), social badminton club 1.9 km (Tue and Fri 18:30). The heat tool says "afternoon hot, prefer morning/evening".

Real data for the same day: Open-Meteo's forecast for central Bangkok (grid point 13.743, 100.496, used for Bang Rak) gives a feels-like temperature of 31.5 °C at 07:00, rising to 38.9 °C at 12:00, 37.8 °C at 14:00 and 33.7 °C at 18:00. Air4Thai's nearest station to Bang Rak (Bangrak Lovely Plaza, 0.5 km away) reported PM2.5 21.2 at 07:00 (AQI 41). Both checks would let an evening badminton session through and push a midday outdoor mission indoors or to the evening. The heat and PM2.5 cut-offs are **not yet defined**; they must be set with the clinician.

### 4. What the synthetic places show, and two gaps they exposed

The shared bundle has 8 fictional Bangkok-area `Location`s and 7 `HealthcareService`s (5 light, 2 moderate). Measuring great-circle distance from each patient's district centroid:

- Every synthetic patient has at least one place within 5 km, but only 1 to 3 places; patients in outer districts (Bang Kapi, Min Buri) have one each.
- **Gap 1: the demo's near-search finds nothing in the FHIR data.** The scripted call `location.near=13.67|100.60|5|km` is about 10.9 km from the nearest synthetic `Location`; the three groups in the demo come from a separate in-browser list, not from the FHIR bundle. The demo and the bundle need one shared place list.
- **Gap 2: an hours inconsistency.** "Air-conditioned mall walkers club" says "Indoor walking loop before shops open", but its `Location` opens at 10:00. A rules engine reading `hoursOfOperation` would never offer it before 10:00. Services need their own `availableTime`.

### 5. If IRIS does not support `near`

Whether the IRIS for Health FHIR server supports `near` on `Location` (and the chained form on `HealthcareService`) is **to confirm** via `GET /fhir/r4/metadata` (the capability statement) or the InterSystems mentors. FHIR says servers "SHOULD ignore unknown or unsupported parameters", and the kit warns "Unknown search params are silently ignored (verified: 200 with all results). A typo'd param looks like 'no filter', not an error." An unsupported `near` would silently return every place in Bangkok. Two safeguards: send `Prefer: handling=strict` and check the capability statement at start-up; and, as a fallback, project `Location.position` with FHIR SQL Builder and filter distance in SQL.

### 6. Privacy and design decisions

- **District, not address:** enough to find groups within a short trip; does not reveal where someone lives.
- **Weather and PM2.5 are not stored per patient;** they are tool results used at decision time and logged only as the reason for a change.
- **Model never invents places:** choices are references to curated `HealthcareService`s; the router only calls tools.
- **Rejected:** live GPS tracking (unnecessary and sensitive); scraping social media for groups (unverifiable intensity, consent issues); letting the model describe "a good park near you" (hallucination risk, as the PM2.5 failure in P01 showed).

## Visualizations

### Chart 1 · Line: feels-like temperature through the day, central Bangkok, 18 Oct 2026 (Open-Meteo forecast)

- **Type:** line, hourly.
- **Title:** "Midday is the wrong time for an outdoor mission"
- **Axes:** x = hour (Asia/Bangkok); y = °C. Two lines: apparent temperature and air temperature.

| Hour | Apparent temp (°C) | Air temp (°C) | Relative humidity (%) |
|---|---|---|---|
| 00 | 31.2 | 25.6 | 95 |
| 03 | 31.0 | 25.0 | 96 |
| 06 | 31.0 | 24.9 | 98 |
| 07 | 31.5 | 25.4 | 96 |
| 08 | 32.9 | 26.6 | 91 |
| 09 | 34.5 | 28.4 | 81 |
| 10 | 35.8 | 29.6 | 75 |
| 11 | 37.9 | 30.5 | 73 |
| 12 | 38.9 | 31.2 | 69 |
| 13 | 36.9 | 30.9 | 70 |
| 14 | 37.8 | 30.7 | 74 |
| 15 | 33.7 | 27.7 | 85 |
| 16 | 32.7 | 27.0 | 88 |
| 17 | 33.9 | 27.4 | 88 |
| 18 | 33.7 | 27.3 | 90 |
| 19 | 34.2 | 27.3 | 91 |
| 20 | 34.1 | 27.3 | 90 |
| 21 | 33.9 | 27.0 | 92 |

Annotations: shade 10:00–14:00 "hottest hours"; mark 06:30 (synthetic walking group) and 18:30 (synthetic badminton club). Note: "Forecast, grid point 13.743 N, 100.496 E, pulled 2026-10-18. Heat cut-off not yet set by a clinician." **What to notice:** feels-like temperature is above 31 °C all day; the rule should pick the relatively cooler hours and favour indoor places, not promise "cool".

### Chart 2 · Bar: PM2.5 at the nearest Air4Thai station to each synthetic home, 07:00, 18 Oct 2026

- **Title:** "Air quality varies across the city on the same morning"
- **Axis:** PM2.5 value as reported by Air4Thai (µg/m³ assumed; to verify).

| Patient home (district) | Nearest station | Distance (km) | PM2.5 | AQI |
|---|---|---|---|---|
| p01 Bang Rak | Bangrak Lovely Plaza | 0.5 | 21.2 | 41 |
| p02 Phra Nakhon | Phra Nakhon District Office | 1.1 | 23.1 | 45 |
| p03 Chatuchak | Chatuchak Park | 0.4 | 18.0 | 33 |
| p04 Thon Buri | Thonburi Power Sub-Station | 0.3 | 25.1 | 51 |
| p05 Huai Khwang | Huai Khwang District Office | 1.3 | 17.2 | 31 |
| p06 Bang Kapi | Bang Kapi District Office | 0.2 | 16.2 | 29 |
| p07 Lat Phrao | Ladphrao District Office | 2.1 | 19.5 | 37 |
| p08 Min Buri | Chaloem Phrakiat Rama 9 Park, Min Buri | 0.4 | 18.4 | 34 |

Context: across the 77 Bangkok stations reporting that morning, PM2.5 ranged from 15.0 to 32.7 (median 20.5). **Notice:** a station is within 2.1 km of every synthetic home, so a district-level check is realistic; this was a clean-air morning, so the chart shows the mechanism, not a smoky day.

### Chart 3 · Grouped bar: synthetic places within reach of each home

- **Title:** "Every synthetic patient has 1–3 places within 5 km; the demo query has none"
- **Axis:** number of synthetic `Location`s within 5 km (great-circle from district centroid).

| Home | Within 5 km | Nearest place (km) |
|---|---|---|
| p01 Bang Rak | 2 | Riverside Community Park 0.9 |
| p02 Phra Nakhon | 3 | Wat Demo Walking Courtyard 0.3 |
| p03 Chatuchak | 3 | Northern Green Park 0.6 |
| p04 Thon Buri | 3 | Riverside Community Park / Wat Demo 3.4 |
| p05 Huai Khwang | 2 | Cool Air Mall 0.5 |
| p06 Bang Kapi | 1 | Eastside Mall 0.9 |
| p07 Lat Phrao | 2 | Wat Lat Phrao Demo Grounds 0.4 |
| p08 Min Buri | 1 | Community Sports Track 0.6 |
| Demo query 13.67, 100.60 | 0 | Cool Air Mall 10.9 |

**Notice:** the FHIR place data and the demo's place list are not yet the same data (Gap 1).

### Chart 4 · Table-chart: the 7 synthetic groups and the filter fields

| HealthcareService | Location (type, indoor) | Intensity | Location hours | Description (`comment`, used for vector ranking) |
|---|---|---|---|---|
| Morning walking group, Riverside Park | park, outdoor | light | 06:00–20:00 | Easy 20-minute group walk, talk-test pace, every weekday 06:30 |
| Temple courtyard slow walk | temple, outdoor | light | 06:00–18:00 | Quiet slow walk with older adults after morning prayers |
| Air-conditioned mall walkers club | indoor mall, indoor | light | 10:00–22:00 | Indoor walking loop before shops open, good on hot or smoky days |
| Supervised cardiac rehab class | rehab gym, indoor | moderate | 08:00–16:00 | Monitored exercise class with ECG telemetry, needs referral |
| Tai chi for beginners, Northern Green Park | park, outdoor | light | 05:00–21:00 | Gentle tai chi, 30 minutes, Saturday and Sunday 07:00 |
| Evening walking circle, Community Track | track, outdoor | light | 05:00–20:00 | Easy evening walk after sunset, friendly for fasting days |
| Stationary cycling, low resistance | indoor mall, indoor | moderate | 10:00–22:00 | Instructor-led low-resistance cycling, 25 minutes |

### Diagram · Five-step flow

Home district (not address) → FHIR candidates (`Location` + `HealthcareService`) [FHIR] → safety filter: intensity ≤ limit, open at mission time, heat/PM2.5 → indoor or another time [RULES ONLY] → rank by taste, people like you, distance, patient's words [VECTOR] → three choices with the mission; the pick becomes a `Task`. Side inputs: Open-Meteo and Air4Thai as tool calls into step 3.

## Numbers and claims ledger

| Claim | Value | Source | Status |
|---|---|---|---|
| FHIR `near` definition, km default | quoted | hl7.org/fhir/R4/location.html | checked |
| Chaining syntax; servers SHOULD ignore unknown parameters; `Prefer: handling=strict` | quoted | hl7.org/fhir/R4/search.html | checked |
| `HealthcareService` `location` search parameter | reference | hl7.org/fhir/R4/healthcareservice.html | checked |
| Unknown params silently ignored on the kit server | quoted | `FHIR-AI-Hackathon-Kit/skills/iris-fhir/SKILL.md` | checked (kit) |
| IRIS supports `near` / chained near | — | — | to verify (`/fhir/r4/metadata`) |
| Overpass public limits | < 10,000 queries/day, < 1 GB/day; ÷100 for apps | OSM wiki | checked |
| Open-Meteo endpoint, key only for commercial, apparent temperature definition | quoted | open-meteo.com/en/docs | checked |
| Hourly forecast values | as Chart 1 | Open-Meteo API call, 2026-10-18 | checked (forecast, not observation) |
| Air4Thai stations / fresh / Bangkok | 173 / 159 / 79 (77 valid) | Air4Thai JSON, 2026-10-18 07:00 | checked |
| PM2.5 per home | as Chart 2 | same | checked; unit to verify |
| Stale station example | 10t, last reading 2023-10-12 | same | checked |
| Synthetic places / services | 8 / 7 (5 light, 2 moderate) | `synthetic/fhir/00_shared_reference_data.json` | synthetic |
| Distances | as Chart 3 | haversine computed by us | checked, synthetic places |
| Demo groups and distances | 3.2, 0.9, 1.9 km | `COMMUNITY` in demo | synthetic |
| Heat and PM2.5 cut-offs | — | — | missing: clinician to set |
| Public list of Thai community exercise groups | none found | A05, geo slide | gap |

## Limits and open questions

- No real group data. A curated list (district health offices, hospital rehab programmes, senior clubs, temples, malls) must be built and kept current; partner sources are a business question (P19).
- `near` support on IRIS is unconfirmed; an unsupported parameter would silently return all places.
- Demo places and FHIR places are different lists; the demo near-search returns no FHIR place.
- Heat and PM2.5 thresholds, and whether to use apparent temperature or a heat index, need a clinician decision.
- Open-Meteo's free tier is non-commercial; a paid product needs a licence or Thai Meteorological Department data.
- Group intensity tags are our guesses; a real group's intensity varies by session and members.
- Moderation and safety of community groups (P12) are not designed in detail.

## Likely judge questions

1. **"Where do the groups come from?"** A curated list stored as FHIR `HealthcareService` + `Location`. No public Thai API exists; building that list with district and hospital partners is part of the pilot.
2. **"How do you protect location privacy?"** We store the home district and its centroid, not the address, and do not track GPS. Weather and air quality are looked up per district at decision time.
3. **"What if it is 39 °C or smoky?"** The rules move the mission to a cooler time or an indoor place (mall walkers, indoor cycling) before ranking; cut-offs will be set by the clinician. On 18 Oct 2026 the feels-like forecast peaked at 38.9 °C at noon.
4. **"Does IRIS do geo search?"** FHIR R4 defines `near` on `Location`; we will confirm IRIS support in the capability statement. Fallback: project positions with SQL Builder and filter distance in SQL.
5. **"Could the model suggest a place that doesn't exist?"** No. The model only calls tools; every choice is a reference to a stored `HealthcareService`.

## Sources

Repo:
- `pitch/appendix/A05-intersystems-vector-search-and-geo.md`, `pitch/appendix-deck/P07-geospatial-community-search.md`, `docs/pitch/faq-appendix/slides/geo.html`
- `synthetic/generate_fhir.py` (`PLACES`, `SERVICES`, `PROFILES` coordinates), `synthetic/fhir/00_shared_reference_data.json`, `synthetic/fhir/p0*_*.json`
- `demo/agent-flow-demo.html` (`COMMUNITY`, near-search and heat calls)
- `FHIR-AI-Hackathon-Kit/skills/iris-fhir/SKILL.md`, `skills/iris-environment/SKILL.md`

External (opened or called 2026-10-18):
- HL7 FHIR R4 Location (positional searching, `near`): https://hl7.org/fhir/R4/location.html
- HL7 FHIR R4 HealthcareService (search parameters): https://hl7.org/fhir/R4/healthcareservice.html
- HL7 FHIR R4 Search (chaining, unknown parameters): https://hl7.org/fhir/R4/search.html
- OpenStreetMap wiki, Overpass API: https://wiki.openstreetmap.org/wiki/Overpass_API
- Open-Meteo API documentation: https://open-meteo.com/en/docs; forecast call: https://api.open-meteo.com/v1/forecast?latitude=13.7279&longitude=100.5241&hourly=apparent_temperature&timezone=Asia%2FBangkok&forecast_days=1
- Air4Thai AQI JSON service (Pollution Control Department): https://air4thai.pcd.go.th/services/getNewAQI_JSON.php

## Image-generation prompt

Design one 16:9 information slide on a white background. Lead with the key message as the title: "Groups and places come from FHIR resources near the home district, filtered by rules before anything is ranked." Make the main chart a line of feels-like temperature in central Bangkok on 18 Oct 2026 (Open-Meteo forecast) with exactly these points: 07:00 31.5 °C, 10:00 35.8 °C, 12:00 38.9 °C, 14:00 37.8 °C, 18:00 33.7 °C, with the midday band shaded "hottest hours". Beside it, a five-step flow (home district → FHIR Location + HealthcareService → rules: intensity, opening hours, heat, PM2.5 → rank → three choices) and a small bar of PM2.5 at the nearest Air4Thai station for three homes (Bang Rak 21.2, Thon Buri 25.1, Bang Kapi 16.2). Mark places and groups as synthetic. No logos, no invented numbers; choose the design freely.
