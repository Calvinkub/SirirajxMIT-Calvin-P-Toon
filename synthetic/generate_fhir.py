"""Generate SYNTHETIC FHIR R4 transaction bundles for CVD Mission Coach demos.

Every person, place, note and number here is invented. Nothing is clinical
evidence. Follows the FHIR-AI-Hackathon-Kit pattern (transaction bundles,
fhir.resources validation) but uses PUT with stable ids, so reloading the
bundles updates resources instead of duplicating them.

Usage:
    .venv/bin/python synthetic/generate_fhir.py      # writes synthetic/fhir/*.json
"""

import base64
import json
import random
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from fhir.resources.R4B.bundle import Bundle

OUT = Path(__file__).parent / "fhir"
SEED = 42
DAY0 = date(2026, 10, 11)  # first day of the 7-day demo window
DAYS = 7
TZ = timezone(timedelta(hours=7))  # Asia/Bangkok

LOCAL = "https://cvd-mission-coach.example/fhir"
CS_LOCAL = f"{LOCAL}/CodeSystem/cmc"
EXT = f"{LOCAL}/StructureDefinition"
SYNTH_TAG = {"system": f"{LOCAL}/CodeSystem/data-origin", "code": "synthetic", "display": "Synthetic demo data"}

LOINC = "http://loinc.org"
SNOMED = "http://snomed.info/sct"
ATC = "http://www.whocc.no/atc"
UCUM = "http://unitsofmeasure.org"

MEDS = {
    "bisoprolol": ("C07AB07", "Bisoprolol 2.5 mg once daily", True),
    "metoprolol": ("C07AB02", "Metoprolol succinate 47.5 mg once daily", True),
    "aspirin": ("B01AC06", "Aspirin 81 mg once daily", False),
    "clopidogrel": ("B01AC04", "Clopidogrel 75 mg once daily", False),
    "ticagrelor": ("B01AC24", "Ticagrelor 90 mg twice daily", False),
    "atorvastatin": ("C10AA05", "Atorvastatin 40 mg at night", False),
    "ramipril": ("C09AA05", "Ramipril 5 mg once daily", False),
    "metformin": ("A10BA02", "Metformin 500 mg twice daily", False),
    "nitroglycerin": ("C01DA02", "Nitroglycerin 0.4 mg sublingual as needed", False),
}

CONDITIONS = {
    "mi": ("22298006", "Myocardial infarction"),
    "htn": ("38341003", "Hypertensive disorder"),
    "t2dm": ("44054006", "Type 2 diabetes mellitus"),
    "af": ("49436004", "Atrial fibrillation"),
    "hf": ("84114007", "Heart failure"),
    "cabg": ("232717009", "Coronary artery bypass graft (history)"),
}

# One row per patient archetype: the variety the demo and the tool router need.
PROFILES = [
    dict(id="p01", given="Somchai", family="Kaewmanee", gender="male", birth="1964-03-12", district="Bang Rak",
         lat=13.7279, lon=100.5241, conds=["mi", "htn"], meds=["bisoprolol", "aspirin", "ticagrelor", "atorvastatin"],
         lvef=55, risk="low", limit=dict(source="cpet", hr=110, rpe=(11, 13), acts=["walking", "stationary-cycling"]),
         rest_hr=64, steps=5200, adherence=0.85, story="Low risk after MI, CPET done, on a beta-blocker, keen walker."),
    dict(id="p02", given="Malee", family="Srisuk", gender="female", birth="1955-07-30", district="Phra Nakhon",
         lat=13.7563, lon=100.4930, conds=["mi", "htn"], meds=["metoprolol", "aspirin", "clopidogrel", "atorvastatin", "ramipril"],
         lvef=52, risk="low", limit=dict(source="6mwt", hr=100, rpe=(11, 12), acts=["walking"]),
         rest_hr=70, steps=2800, adherence=0.6, story="Aged 71, no CPET (limit from 6-minute walk), low tech comfort, daughter helps."),
    dict(id="p03", given="Anan", family="Thongdee", gender="male", birth="1968-11-02", district="Chatuchak",
         lat=13.8000, lon=100.5530, conds=["mi", "t2dm"], meds=["bisoprolol", "aspirin", "ticagrelor", "atorvastatin", "metformin"],
         lvef=42, risk="moderate", limit=dict(source="exercise-ecg", hr=105, rpe=(11, 12), acts=["walking"]),
         rest_hr=72, steps=3900, adherence=0.75, story="Moderate risk (LVEF 42%): needs supervised sessions before app-only use."),
    dict(id="p04", given="Prasert", family="Wongsa", gender="male", birth="1959-01-19", district="Thon Buri",
         lat=13.7250, lon=100.4850, conds=["mi", "hf"], meds=["metoprolol", "aspirin", "atorvastatin", "ramipril"],
         lvef=30, risk="high", icd=True, limit=None,
         rest_hr=76, steps=1500, adherence=0.0, story="High risk (LVEF 30%, ICD): blocked from app missions, referred to supervised rehab."),
    dict(id="p05", given="Wanida", family="Chaiyaporn", gender="female", birth="1962-05-08", district="Huai Khwang",
         lat=13.7660, lon=100.5740, conds=["cabg", "htn", "t2dm"], meds=["bisoprolol", "aspirin", "atorvastatin", "metformin"],
         lvef=50, risk="low", cabg_weeks=6, limit=dict(source="cpet", hr=108, rpe=(11, 13), acts=["walking"]),
         rest_hr=68, steps=4100, adherence=0.8, story="Six weeks after bypass surgery: walking only, no upper-body resistance yet."),
    dict(id="p06", given="Kittisak", family="Boonmee", gender="male", birth="1971-09-25", district="Bang Kapi",
         lat=13.7650, lon=100.6470, conds=["mi"], meds=["bisoprolol", "aspirin", "clopidogrel", "atorvastatin"],
         lvef=None, risk="unknown", limit=None, draft_limit=True,
         rest_hr=66, steps=3300, adherence=0.0, story="New sign-up: no clinician-signed limit yet, so no exercise missions."),
    dict(id="p07", given="Siriporn", family="Jaidee", gender="female", birth="1966-12-14", district="Lat Phrao",
         lat=13.8160, lon=100.5930, conds=["mi", "htn"], meds=["bisoprolol", "aspirin", "ticagrelor", "atorvastatin", "nitroglycerin"],
         lvef=53, risk="low", limit=dict(source="cpet", hr=105, rpe=(11, 12), acts=["walking"]),
         rest_hr=69, steps=3600, adherence=0.7, red_flag_day=4,
         story="Reported chest tightness on day 5: stop path fired, coaching paused for clinician review."),
    dict(id="p08", given="Abdul", family="Rahman", gender="male", birth="1960-04-03", district="Min Buri",
         lat=13.8130, lon=100.7280, conds=["mi", "htn", "t2dm", "af"], meds=["metoprolol", "clopidogrel", "atorvastatin", "metformin", "ramipril"],
         lvef=50, risk="low", limit=dict(source="cpet", hr=100, rpe=(11, 12), acts=["walking", "stationary-cycling"]),
         rest_hr=74, steps=2500, adherence=0.45, fasting=True,
         story="Several conditions incl. AF, misses missions often, prefers evening; observes fasting days."),
]

MISSIONS = [
    ("walk-10-easy", "10-minute easy walk, warm-up and cool-down included"),
    ("walk-12-easy", "12-minute easy walk, warm-up and cool-down included"),
    ("cycle-10-easy", "10-minute easy stationary cycling"),
    ("rest-day", "Rest day: gentle stretching only"),
]

# Shared reference data: fictional places with approximate Bangkok coordinates.
PLACES = [
    ("loc-park-1", "Riverside Community Park (synthetic)", "park", 13.7310, 100.5160, False, "06:00", "20:00"),
    ("loc-park-2", "Northern Green Park (synthetic)", "park", 13.8050, 100.5560, False, "05:00", "21:00"),
    ("loc-temple-1", "Wat Demo Walking Courtyard (synthetic)", "temple", 13.7540, 100.4950, False, "06:00", "18:00"),
    ("loc-mall-1", "Cool Air Mall walking loop (synthetic)", "indoor-mall", 13.7640, 100.5700, True, "10:00", "22:00"),
    ("loc-mall-2", "Eastside Mall walking loop (synthetic)", "indoor-mall", 13.7700, 100.6400, True, "10:00", "22:00"),
    ("loc-gym-1", "Demo Hospital Cardiac Rehab Gym (synthetic)", "rehab-gym", 13.7590, 100.4860, True, "08:00", "16:00"),
    ("loc-track-1", "Community Sports Track (synthetic)", "track", 13.8170, 100.7250, False, "05:00", "20:00"),
    ("loc-temple-2", "Wat Lat Phrao Demo Grounds (synthetic)", "temple", 13.8140, 100.5900, False, "06:00", "18:00"),
]
SERVICES = [
    ("svc-walk-group-1", "Morning walking group, Riverside Park", "loc-park-1", "light", "Easy 20-minute group walk, talk-test pace, every weekday 06:30"),
    ("svc-walk-group-2", "Temple courtyard slow walk", "loc-temple-1", "light", "Quiet slow walk with older adults after morning prayers"),
    ("svc-mall-walk", "Air-conditioned mall walkers club", "loc-mall-1", "light", "Indoor walking loop before shops open, good on hot or smoky days"),
    ("svc-rehab-class", "Supervised cardiac rehab class", "loc-gym-1", "moderate", "Monitored exercise class with ECG telemetry, needs referral"),
    ("svc-tai-chi", "Tai chi for beginners, Northern Green Park", "loc-park-2", "light", "Gentle tai chi, 30 minutes, Saturday and Sunday 07:00"),
    ("svc-evening-walk", "Evening walking circle, Community Track", "loc-track-1", "light", "Easy evening walk after sunset, friendly for fasting days"),
    ("svc-cycle-class", "Stationary cycling, low resistance", "loc-mall-2", "moderate", "Instructor-led low-resistance cycling, 25 minutes"),
]


def iso(d: date, hh: int, mm: int = 0) -> str:
    return datetime(d.year, d.month, d.day, hh, mm, tzinfo=TZ).isoformat()


def meta():
    return {"tag": [SYNTH_TAG]}


def entry(resource: dict) -> dict:
    rtype, rid = resource["resourceType"], resource["id"]
    resource.setdefault("meta", meta())
    return {"fullUrl": f"{LOCAL}/{rtype}/{rid}", "resource": resource, "request": {"method": "PUT", "url": f"{rtype}/{rid}"}}


def cc(system, code, display):
    return {"coding": [{"system": system, "code": code, "display": display}], "text": display}


def local_cc(code, display):
    return cc(CS_LOCAL, code, display)


def qty(value, unit, code):
    return {"value": value, "unit": unit, "system": UCUM, "code": code}


def shared_bundle():
    entries = [
        entry({"resourceType": "Organization", "id": "org-demo-clinic", "active": True,
               "name": "Demo Cardiac Rehab Clinic (synthetic)"}),
        entry({"resourceType": "Practitioner", "id": "pr-cardio-1", "active": True,
               "name": [{"family": "Rattanakul", "given": ["Narin"], "prefix": ["Dr."]}],
               "qualification": [{"code": {"text": "Cardiologist (synthetic)"}}]}),
        entry({"resourceType": "Practitioner", "id": "pr-rehab-1", "active": True,
               "name": [{"family": "Saelim", "given": ["Pimchanok"]}],
               "qualification": [{"code": {"text": "Cardiac rehabilitation physiotherapist (synthetic)"}}]}),
        entry({"resourceType": "Device", "id": "dev-medgemma", "status": "active",
               "deviceName": [{"name": "MedGemma 27B mission picker (demo config)", "type": "model-name"}],
               "type": {"text": "AI model"}}),
        entry({"resourceType": "Questionnaire", "id": "symptom-check", "status": "active",
               "url": f"{LOCAL}/Questionnaire/symptom-check", "version": "1.0", "title": "Before/after mission symptom check",
               "item": [
                   {"linkId": "chest-pain", "text": "Chest pain, pressure or tightness?", "type": "boolean"},
                   {"linkId": "breathless", "text": "Unusually short of breath?", "type": "boolean"},
                   {"linkId": "dizzy", "text": "Dizzy or faint?", "type": "boolean"},
                   {"linkId": "palpitations", "text": "Racing or irregular heartbeat?", "type": "boolean"},
                   {"linkId": "rpe", "text": "How hard was it (Borg 6-20)?", "type": "integer"},
               ]}),
    ]
    for lid, name, kind, lat, lon, indoor, opens, closes in PLACES:
        entries.append(entry({
            "resourceType": "Location", "id": lid, "status": "active", "name": name, "mode": "instance",
            "type": [local_cc(kind, kind.replace("-", " "))],
            "position": {"latitude": lat, "longitude": lon},
            "hoursOfOperation": [{"daysOfWeek": ["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
                                  "openingTime": f"{opens}:00", "closingTime": f"{closes}:00"}],
            "extension": [{"url": f"{EXT}/indoor", "valueBoolean": indoor}],
        }))
    for sid, name, lid, intensity, comment in SERVICES:
        entries.append(entry({
            "resourceType": "HealthcareService", "id": sid, "active": True, "name": name, "comment": comment,
            "providedBy": {"reference": "Organization/org-demo-clinic"},
            "location": [{"reference": f"Location/{lid}"}],
            "category": [local_cc("exercise-activity", "Exercise activity")],
            "extension": [{"url": f"{EXT}/activity-intensity", "valueCode": intensity}],
        }))
    return {"resourceType": "Bundle", "type": "transaction", "entry": entries}


def discharge_note(p) -> str:
    conds = ", ".join(CONDITIONS[c][1] for c in p["conds"])
    meds = "; ".join(MEDS[m][1] for m in p["meds"])
    lvef = f"LVEF {p['lvef']}%" if p.get("lvef") else "LVEF not recorded"
    extra = []
    if p.get("icd"):
        extra.append("ICD implanted before discharge.")
    if p.get("cabg_weeks"):
        extra.append(f"CABG {p['cabg_weeks']} weeks ago; sternal precautions, no upper-body lifting.")
    return (f"SYNTHETIC DISCHARGE SUMMARY (demo only, not a real patient)\n"
            f"Patient: {p['given']} {p['family']}\nDiagnoses: {conds}\n{lvef}. Risk class: {p['risk']}.\n"
            f"Medications: {meds}\n{' '.join(extra)}\n"
            f"Plan: cardiac rehabilitation referral; follow-up in cardiology clinic in 4 weeks.")


def patient_bundle(p, rng: random.Random):
    pid = f"cmc-{p['id']}"
    pref = {"reference": f"Patient/{pid}"}
    out = []

    def add(res):
        out.append(entry(res))

    add({"resourceType": "Patient", "id": pid, "active": True, "gender": p["gender"], "birthDate": p["birth"],
         "name": [{"use": "official", "family": p["family"], "given": [p["given"]]}],
         "address": [{"district": p["district"], "city": "Bangkok", "country": "TH"}],
         "communication": [{"language": cc("urn:ietf:bcp:47", "th", "Thai"), "preferred": True}],
         "extension": [{"url": f"{EXT}/home-district-position",
                        "extension": [{"url": "latitude", "valueDecimal": p["lat"]},
                                      {"url": "longitude", "valueDecimal": p["lon"]}]}]})

    for i, c in enumerate(p["conds"], 1):
        code, disp = CONDITIONS[c]
        add({"resourceType": "Condition", "id": f"{pid}-cond-{i}", "subject": pref,
             "clinicalStatus": cc("http://terminology.hl7.org/CodeSystem/condition-clinical", "active", "Active"),
             "verificationStatus": cc("http://terminology.hl7.org/CodeSystem/condition-ver-status", "confirmed", "Confirmed"),
             "code": cc(SNOMED, code, disp), "onsetDateTime": iso(DAY0 - timedelta(days=30 + 7 * i), 9)})

    for i, m in enumerate(p["meds"], 1):
        code, text, is_bb = MEDS[m]
        res = {"resourceType": "MedicationStatement", "id": f"{pid}-med-{i}", "status": "active", "subject": pref,
               "medicationCodeableConcept": cc(ATC, code, m.capitalize()), "dosage": [{"text": text}],
               "effectivePeriod": {"start": iso(DAY0 - timedelta(days=28), 8)}}
        if is_bb:
            res["extension"] = [{"url": f"{EXT}/beta-blocker", "valueBoolean": True}]
        add(res)

    add({"resourceType": "DocumentReference", "id": f"{pid}-discharge", "status": "current", "subject": pref,
         "type": cc(LOINC, "18842-5", "Discharge summary"), "date": iso(DAY0 - timedelta(days=21), 15),
         "content": [{"attachment": {"contentType": "text/plain; charset=utf-8",
                                     "data": base64.b64encode(discharge_note(p).encode()).decode("ascii")}}]})

    add({"resourceType": "Device", "id": f"{pid}-watch", "status": "active", "patient": pref,
         "type": {"text": "Smartwatch"},
         "deviceName": [{"name": rng.choice(["Apple Watch", "Galaxy Watch", "Garmin Venu", "Huawei Watch"]), "type": "user-friendly-name"}]})

    if p.get("lvef") is not None:
        add({"resourceType": "Observation", "id": f"{pid}-lvef", "status": "final", "subject": pref,
             "category": [cc("http://terminology.hl7.org/CodeSystem/observation-category", "imaging", "Imaging")],
             "code": cc(LOINC, "10230-1", "Left ventricular Ejection fraction"),
             "effectiveDateTime": iso(DAY0 - timedelta(days=24), 10), "valueQuantity": qty(p["lvef"], "%", "%")})
    add({"resourceType": "Observation", "id": f"{pid}-risk", "status": "final", "subject": pref,
         "code": local_cc("aacvpr-risk-class", "Exercise risk class (AACVPR-style)"),
         "effectiveDateTime": iso(DAY0 - timedelta(days=20), 11), "valueCodeableConcept": local_cc(p["risk"], p["risk"])})

    vitals = cc("http://terminology.hl7.org/CodeSystem/observation-category", "vital-signs", "Vital Signs")
    activity = cc("http://terminology.hl7.org/CodeSystem/observation-category", "activity", "Activity")
    watch = {"reference": f"Device/{pid}-watch"}
    for d in range(DAYS):
        day = DAY0 + timedelta(days=d)
        add({"resourceType": "Observation", "id": f"{pid}-rhr-{d + 1}", "status": "final", "subject": pref, "device": watch,
             "category": [vitals], "code": cc(LOINC, "8867-4", "Heart rate"), "effectiveDateTime": iso(day, 6, 30),
             "valueQuantity": qty(p["rest_hr"] + rng.randint(-4, 4), "beats/minute", "/min")})
        steps = 0 if p["adherence"] == 0 and rng.random() < 0.3 else max(300, int(rng.gauss(p["steps"], p["steps"] * 0.2)))
        add({"resourceType": "Observation", "id": f"{pid}-steps-{d + 1}", "status": "final", "subject": pref, "device": watch,
             "category": [activity], "code": cc(LOINC, "41950-7", "Number of steps in 24 hour Measured"),
             "effectivePeriod": {"start": iso(day, 0), "end": iso(day, 23, 59)}, "valueQuantity": qty(steps, "steps", "{steps}")})
    for k in range(2):
        sbp, dbp = 128 + rng.randint(-10, 12), 78 + rng.randint(-6, 8)
        add({"resourceType": "Observation", "id": f"{pid}-bp-{k + 1}", "status": "final", "subject": pref,
             "category": [vitals], "code": cc(LOINC, "85354-9", "Blood pressure panel with all children optional"),
             "effectiveDateTime": iso(DAY0 + timedelta(days=2 + 3 * k), 7),
             "component": [{"code": cc(LOINC, "8480-6", "Systolic blood pressure"), "valueQuantity": qty(sbp, "mmHg", "mm[Hg]")},
                           {"code": cc(LOINC, "8462-4", "Diastolic blood pressure"), "valueQuantity": qty(dbp, "mmHg", "mm[Hg]")}]})

    add({"resourceType": "Consent", "id": f"{pid}-consent", "status": "active", "patient": pref,
         "scope": cc("http://terminology.hl7.org/CodeSystem/consentscope", "patient-privacy", "Privacy Consent"),
         "category": [cc(LOINC, "59284-0", "Patient Consent")],
         "dateTime": iso(DAY0 - timedelta(days=14), 10),
         "policyRule": cc("http://terminology.hl7.org/CodeSystem/v3-ActCode", "OPTIN", "opt-in"),
         "provision": {"type": "permit", "purpose": [{"system": "http://terminology.hl7.org/CodeSystem/v3-ActReason", "code": "TREAT"}],
                       "provision": [{"type": "deny", "actor": [{"role": cc("http://terminology.hl7.org/CodeSystem/v3-RoleClass", "PAYOR", "payor"),
                                                                  "reference": {"display": "Any insurer"}}]}]}})

    limit, careplan_id = p.get("limit"), f"{pid}-limits"
    if limit or p.get("draft_limit"):
        exts = []
        if limit:
            exts = [{"url": f"{EXT}/hr-ceiling", "valueQuantity": qty(limit["hr"], "beats/minute", "/min")},
                    {"url": f"{EXT}/rpe-target", "valueRange": {"low": {"value": limit["rpe"][0]}, "high": {"value": limit["rpe"][1]}}},
                    {"url": f"{EXT}/limit-source", "valueCode": limit["source"]}]
            exts += [{"url": f"{EXT}/allowed-activity", "valueCode": a} for a in limit["acts"]]
            if p.get("cabg_weeks"):
                exts.append({"url": f"{EXT}/restriction", "valueString": "No upper-body resistance until 12 weeks after CABG"})
        add({"resourceType": "Goal", "id": f"{pid}-goal", "lifecycleStatus": "active" if limit else "proposed", "subject": pref,
             "description": {"text": "Walk most days at an easy, can-still-talk effort"}})
        add({"resourceType": "CarePlan", "id": careplan_id, "status": "active" if limit else "draft", "intent": "plan",
             "subject": pref, "title": "Clinician-signed exercise limit record" if limit else "Exercise limit record awaiting clinician",
             "period": {"start": iso(DAY0 - timedelta(days=7), 9), "end": iso(DAY0 + timedelta(days=49), 9)},
             "author": {"reference": "Practitioner/pr-cardio-1"} if limit else None,
             "goal": [{"reference": f"Goal/{pid}-goal"}], "extension": exts or None})
        if limit:
            add({"resourceType": "Provenance", "id": f"{pid}-limits-prov", "target": [{"reference": f"CarePlan/{careplan_id}"}],
                 "recorded": iso(DAY0 - timedelta(days=7), 9, 15),
                 "agent": [{"type": cc("http://terminology.hl7.org/CodeSystem/provenance-participant-type", "attester", "Attester"),
                            "who": {"reference": "Practitioner/pr-cardio-1"}}]})

    if p.get("risk") == "high":
        add({"resourceType": "Flag", "id": f"{pid}-ineligible", "status": "active", "subject": pref,
             "code": local_cc("app-ineligible", "Not eligible for app-only exercise missions: refer to supervised rehab"),
             "period": {"start": iso(DAY0 - timedelta(days=7), 9)}, "author": {"reference": "Practitioner/pr-cardio-1"}})

    if limit:
        red_day = p.get("red_flag_day")
        for d in range(DAYS):
            day = DAY0 + timedelta(days=d)
            hour = 19 if p.get("fasting") else rng.choice([7, 8, 17, 18])
            code, desc = MISSIONS[3] if d == 3 else MISSIONS[rng.choice([0, 1, 2] if "stationary-cycling" in limit["acts"] else [0, 1])]
            if red_day is not None and d > red_day:
                status = "cancelled"
            elif red_day is not None and d == red_day:
                status = "failed"
            else:
                status = "completed" if rng.random() < p["adherence"] else "requested"
            tid = f"{pid}-task-{d + 1}"
            add({"resourceType": "Task", "id": tid, "status": status, "intent": "plan", "for": pref,
                 "basedOn": [{"reference": f"CarePlan/{careplan_id}"}], "code": local_cc(code, desc), "description": desc,
                 "executionPeriod": {"start": iso(day, hour), "end": iso(day, hour, 30)}, "authoredOn": iso(day, 5)})
            add({"resourceType": "Provenance", "id": f"{tid}-prov", "target": [{"reference": f"Task/{tid}"}], "recorded": iso(day, 5),
                 "agent": [{"type": cc("http://terminology.hl7.org/CodeSystem/provenance-participant-type", "assembler", "Assembler"),
                            "who": {"reference": "Device/dev-medgemma"}}],
                 "reason": [local_cc("picked-from-allowed-set", "Mission id chosen from the rules engine's allowed set")]})
            if status in ("completed", "failed"):
                red = status == "failed"
                add({"resourceType": "QuestionnaireResponse", "id": f"{tid}-check", "status": "completed",
                     "questionnaire": f"{LOCAL}/Questionnaire/symptom-check|1.0", "subject": pref,
                     "authored": iso(day, hour, 35),
                     "extension": [{"url": f"{EXT}/about-task", "valueReference": {"reference": f"Task/{tid}"}}],
                     "item": [{"linkId": "chest-pain", "answer": [{"valueBoolean": red}]},
                              {"linkId": "breathless", "answer": [{"valueBoolean": False}]},
                              {"linkId": "dizzy", "answer": [{"valueBoolean": False}]},
                              {"linkId": "palpitations", "answer": [{"valueBoolean": False}]},
                              {"linkId": "rpe", "answer": [{"valueInteger": 13 if red else rng.randint(limit['rpe'][0], limit['rpe'][1])}]}]})
                if red:
                    add({"resourceType": "Flag", "id": f"{pid}-redflag", "status": "active", "subject": pref,
                         "category": [cc("http://terminology.hl7.org/CodeSystem/flag-category", "clinical", "Clinical")],
                         "code": local_cc("red-flag-chest-symptom", "Red flag: chest tightness reported. Coaching paused."),
                         "period": {"start": iso(day, hour, 36)}})
                    add({"resourceType": "Communication", "id": f"{pid}-redflag-alert", "status": "completed", "subject": pref,
                         "category": [local_cc("clinician-alert", "Clinician alert")], "sent": iso(day, hour, 36),
                         "recipient": [{"reference": "Practitioner/pr-cardio-1"}],
                         "about": [{"reference": f"Flag/{pid}-redflag"}],
                         "payload": [{"contentString": "Patient tapped 'chest tightness' after a walk. Stop message and 1669 prompt shown. Please review before coaching resumes."}]})
    return {"resourceType": "Bundle", "type": "transaction", "entry": out}


def drop_nones(obj):
    if isinstance(obj, dict):
        return {k: drop_nones(v) for k, v in obj.items() if v is not None}
    if isinstance(obj, list):
        return [drop_nones(v) for v in obj]
    return obj


def main():
    rng = random.Random(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    bundles = {"00_shared_reference_data.json": shared_bundle()}
    for p in PROFILES:
        bundles[f"{p['id']}_{p['given']}_{p['family']}.json"] = patient_bundle(p, rng)
    counts = {}
    for name, b in bundles.items():
        b = drop_nones(b)
        Bundle.model_validate(b)  # raises on invalid FHIR (R4B models, as in the kit)
        (OUT / name).write_text(json.dumps(b, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        for e in b["entry"]:
            rt = e["resource"]["resourceType"]
            counts[rt] = counts.get(rt, 0) + 1
    (OUT.parent / "profiles.json").write_text(json.dumps(
        [{"id": f"cmc-{p['id']}", "name": f"{p['given']} {p['family']}", "risk": p["risk"], "story": p["story"]} for p in PROFILES],
        indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(bundles)} bundles to {OUT}")
    for rt, n in sorted(counts.items()):
        print(f"  {rt:22s} {n}")


if __name__ == "__main__":
    main()
