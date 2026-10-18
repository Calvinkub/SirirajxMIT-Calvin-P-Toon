"""Patient-scoped SQL state; the seeded Somchai profile keeps its sample week."""
import json
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from .db import transaction

PATIENT = "demo-somchai"
DEMO_DATE = "2026-10-17"


class RuleViolation(Exception):
    pass


def patient_day(patient):
    return DEMO_DATE if patient == PATIENT else datetime.now(ZoneInfo("Asia/Bangkok")).date().isoformat()


def snapshot(patient=PATIENT):
    day = patient_day(patient)
    week_start = date.fromisoformat(day) - timedelta(days=date.fromisoformat(day).weekday())
    week_end = week_start + timedelta(days=6)
    with transaction() as cur:
        cur.execute("SELECT ProfileJson, Stopped FROM Heartstep.Patient WHERE PatientId = ?", [patient])
        row = cur.fetchone()
        if row is None:
            raise RuntimeError("Run python -m backend.setup first")
        profile, stopped = json.loads(row[0]), bool(row[1])
        cur.execute("SELECT LimitJson FROM Heartstep.ClinicalLimit WHERE PatientId = ?", [patient])
        limit_row = cur.fetchone()
        limit = json.loads(limit_row[0]) if limit_row else {"approved": False, "reviewBy": "1970-01-01", "maxHR": None, "rpe": "", "allowedActivities": [], "source": ""}
        valid = limit["approved"] and date.fromisoformat(limit["reviewBy"]) >= datetime.now(ZoneInfo("Asia/Bangkok")).date()
        profile.update(clinicianApproved=valid, maxHR=limit["maxHR"], rpe=limit["rpe"],
                       allowedActivities=limit["allowedActivities"], source=limit["source"])
        cur.execute("SELECT Kind FROM Heartstep.Completion WHERE PatientId = ? AND MissionDate = ?", [patient, day])
        done = [row[0] for row in cur.fetchall()]
        cur.execute("SELECT COUNT(*) FROM Heartstep.Completion WHERE PatientId = ? AND Kind = ? AND MissionDate BETWEEN ? AND ?",
                    [patient, "walk", week_start.isoformat(), week_end.isoformat()])
        walks = int(cur.fetchone()[0])
        cur.execute("SELECT Steps, RestingHR FROM Heartstep.ActivitySummary WHERE PatientId = ? AND ReadingDate = ?", [patient, day])
        activity_row = cur.fetchone()
        activity = tuple(activity_row) if activity_row else None
    return {"profile": profile, "done": done, "stopped": stopped, "weeklyWalks": walks,
            "activity": {"steps": int(activity[0]), "restingHR": int(activity[1])} if activity else None,
            "demoDate": day, "storage": "iris", "patientId": patient, "isDemo": patient == PATIENT}


def completion(kind, completed, patient=PATIENT):
    day = patient_day(patient)
    if kind not in ("walk", "medication"):
        raise RuleViolation("Unknown mission")
    # Lock the patient row so a concurrent stop and completion serialize.
    with transaction() as cur:
        cur.execute("UPDATE Heartstep.Patient SET Stopped = Stopped WHERE PatientId = ?", [patient])
        cur.execute("SELECT Stopped FROM Heartstep.Patient WHERE PatientId = ?", [patient])
        stopped = bool(cur.fetchone()[0])
        cur.execute("SELECT LimitJson FROM Heartstep.ClinicalLimit WHERE PatientId = ?", [patient])
        limit_row = cur.fetchone()
        limit = json.loads(limit_row[0]) if limit_row else {"approved": False}
        if completed and kind == "walk" and (stopped or not limit["approved"]
                or date.fromisoformat(limit["reviewBy"]) < datetime.now(ZoneInfo("Asia/Bangkok")).date()
                or not limit["maxHR"] or not limit["rpe"] or "walking" not in limit["allowedActivities"]):
            raise RuleViolation("Exercise is paused or clinician approval is missing/expired")
        cur.execute("DELETE FROM Heartstep.Completion WHERE PatientId = ? AND MissionDate = ? AND Kind = ?", [patient, day, kind])
        if completed:
            cur.execute("INSERT INTO Heartstep.Completion (PatientId, MissionDate, Kind) VALUES (?, ?, ?)", [patient, day, kind])
    return snapshot(patient)


def stop(patient=PATIENT):
    with transaction() as cur:
        cur.execute("UPDATE Heartstep.Patient SET Stopped = 1 WHERE PatientId = ?", [patient])
    return snapshot(patient)


def reset():
    # Explicitly demo-only. Never use this reset path for real patient data.
    with transaction() as cur:
        cur.execute("UPDATE Heartstep.Patient SET Stopped = 0 WHERE PatientId = ?", [PATIENT])
        cur.execute("DELETE FROM Heartstep.Completion WHERE PatientId = ? AND MissionDate = ?", [PATIENT, DEMO_DATE])
    return snapshot()
