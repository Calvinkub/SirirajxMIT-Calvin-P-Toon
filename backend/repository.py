"""Single fictional patient, fixed illustrative week. Not a patient portal."""
import json
from datetime import date, datetime
from zoneinfo import ZoneInfo
from .db import transaction

PATIENT = "demo-somchai"
DEMO_DATE = "2026-10-17"


class RuleViolation(Exception):
    pass


def snapshot():
    with transaction() as cur:
        cur.execute("SELECT ProfileJson, Stopped FROM Heartstep.Patient WHERE PatientId = ?", [PATIENT])
        row = cur.fetchone()
        if row is None:
            raise RuntimeError("Run python -m backend.setup first")
        profile, stopped = json.loads(row[0]), bool(row[1])
        cur.execute("SELECT LimitJson FROM Heartstep.ClinicalLimit WHERE PatientId = ?", [PATIENT])
        limit = json.loads(cur.fetchone()[0])
        valid = limit["approved"] and date.fromisoformat(limit["reviewBy"]) >= datetime.now(ZoneInfo("Asia/Bangkok")).date()
        profile.update(clinicianApproved=valid, maxHR=limit["maxHR"], rpe=limit["rpe"],
                       allowedActivities=limit["allowedActivities"], source=limit["source"])
        cur.execute("SELECT Kind FROM Heartstep.Completion WHERE PatientId = ? AND MissionDate = ?", [PATIENT, DEMO_DATE])
        done = [row[0] for row in cur.fetchall()]
        cur.execute("SELECT COUNT(*) FROM Heartstep.Completion WHERE PatientId = ? AND Kind = ? AND MissionDate BETWEEN ? AND ?",
                    [PATIENT, "walk", "2026-10-12", "2026-10-18"])
        walks = int(cur.fetchone()[0])
        cur.execute("SELECT Steps, RestingHR FROM Heartstep.ActivitySummary WHERE PatientId = ? AND ReadingDate = ?", [PATIENT, DEMO_DATE])
        activity = tuple(cur.fetchone())
    return {"profile": profile, "done": done, "stopped": stopped, "weeklyWalks": walks,
            "activity": {"steps": int(activity[0]), "restingHR": int(activity[1])},
            "demoDate": DEMO_DATE, "storage": "iris"}


def completion(kind, completed):
    if kind not in ("walk", "medication"):
        raise RuleViolation("Unknown mission")
    # Lock the patient row so a concurrent stop and completion serialize.
    with transaction() as cur:
        cur.execute("UPDATE Heartstep.Patient SET Stopped = Stopped WHERE PatientId = ?", [PATIENT])
        cur.execute("SELECT Stopped FROM Heartstep.Patient WHERE PatientId = ?", [PATIENT])
        stopped = bool(cur.fetchone()[0])
        cur.execute("SELECT LimitJson FROM Heartstep.ClinicalLimit WHERE PatientId = ?", [PATIENT])
        limit = json.loads(cur.fetchone()[0])
        if completed and kind == "walk" and (stopped or not limit["approved"]
                or date.fromisoformat(limit["reviewBy"]) < datetime.now(ZoneInfo("Asia/Bangkok")).date()
                or not limit["maxHR"] or not limit["rpe"] or "walking" not in limit["allowedActivities"]):
            raise RuleViolation("Exercise is paused or clinician approval is missing/expired")
        cur.execute("DELETE FROM Heartstep.Completion WHERE PatientId = ? AND MissionDate = ? AND Kind = ?", [PATIENT, DEMO_DATE, kind])
        if completed:
            cur.execute("INSERT INTO Heartstep.Completion (PatientId, MissionDate, Kind) VALUES (?, ?, ?)", [PATIENT, DEMO_DATE, kind])
    return snapshot()


def stop():
    with transaction() as cur:
        cur.execute("UPDATE Heartstep.Patient SET Stopped = 1 WHERE PatientId = ?", [PATIENT])
    return snapshot()


def reset():
    # Explicitly demo-only. Never use this reset path for real patient data.
    with transaction() as cur:
        cur.execute("UPDATE Heartstep.Patient SET Stopped = 0 WHERE PatientId = ?", [PATIENT])
        cur.execute("DELETE FROM Heartstep.Completion WHERE PatientId = ? AND MissionDate = ?", [PATIENT, DEMO_DATE])
    return snapshot()
