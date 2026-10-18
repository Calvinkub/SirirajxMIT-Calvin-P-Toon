# Tool-router labelling guide

One label per message. Messages come from Thai heart patients (mostly aged 45–80) using a phone app, typed or spoken, in Thai, English, or mixed. Precedence: if two labels seem to fit, use the first one in this list that fits.

| # | Label | Use when the patient… | Not this label when… |
|---|---|---|---|
| 1 | `red_flag` | reports a warning symptom happening now or just now: chest pain/pressure/tightness, unusual breathlessness, dizziness, light-headedness, fainting or near-fainting, racing/pounding/irregular heartbeat, pain spreading to arm/jaw/back, cold sweat with chest discomfort | the symptom is clearly denied ("no chest pain today") or is a general question about symptoms ("what are heart attack signs?" → `none`) |
| 2 | `none` | greets, thanks, small talk, asks about the app, asks anything about medicines (stop, skip, double, side effects, forgot a dose), asks general medical questions | — |
| 3 | `log_checkin` | reports how a finished or skipped mission or activity went, or that they did/didn't do it, or that they took their medicine | they ask to SEE past data (→ `get_recent_activity`) |
| 4 | `get_recent_activity` | asks to see their own past steps, heart rate, minutes, missions done, progress | — |
| 5 | `get_patient_limits` | asks what they are allowed to do: heart-rate ceiling, how hard, which activities, lifting, cycling, swimming, when they can do more | — |
| 6 | `get_pm25` | asks about air quality, dust, smoke, haze, PM2.5, masks because of dust | — |
| 7 | `get_heat_index` | asks about temperature, heat, sun, whether it is too hot or cool enough, rain/weather for going out | the question is only about dust/smoke (→ `get_pm25`) |
| 8 | `search_activities` | wants a group, class, club, people to exercise with, an event or a supervised session | they only want a place to go on their own (→ `search_places`) |
| 9 | `search_places` | wants a place or route to walk or exercise on their own: park, temple grounds, mall, track, shaded path | — |

## Output format (JSONL, one object per line)

`{"id": "<prefix><number>", "lang": "th" | "en" | "mix", "text": "<message>", "tool": "<label>"}`

## Variety wanted

Colloquial Thai (ครับ/ค่ะ/นะ/จ้า, dropped subjects), spoken-style run-ons, typos and missing tone marks, Thai–English code-mixing ("วันนี้ PM สูงมั้ย"), elderly phrasing, very short messages ("ร้อนมั้ย"), long rambling ones, indirect requests ("อยากออกไปข้างนอกแต่กลัวฝุ่น"), and hard cases near the label boundaries above.
