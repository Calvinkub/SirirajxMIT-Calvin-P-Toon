"""Username-only prototype access and structured, patient-scoped agent context."""
import hashlib
import json
import secrets
import time
from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException, Request
from .db import transaction
from .models import Registration
from .repository import PATIENT, RuleViolation, snapshot

COOKIE = "heartstep_session"
SESSION_SECONDS = 7 * 24 * 3600
UNITS = {"heart_rate": "bpm", "systolic_bp": "mmHg", "diastolic_bp": "mmHg",
         "weight": "kg", "height": "cm", "spo2": "%", "glucose": "mg/dL"}


def find_user(username):
    with transaction() as cur:
        cur.execute("SELECT PatientId FROM Heartstep.Account WHERE Username = ?", [username])
        row = cur.fetchone()
        return row[0] if row else None


def new_session(patient):
    token = secrets.token_urlsafe(32)
    with transaction() as cur:
        cur.execute("DELETE FROM Heartstep.UserSession WHERE ExpiresAt < ?", [int(time.time())])
        cur.execute("INSERT INTO Heartstep.UserSession (TokenHash, PatientId, ExpiresAt) VALUES (?, ?, ?)",
                    [hashlib.sha256(token.encode()).hexdigest(), patient, int(time.time()) + SESSION_SECONDS])
    return token


def current_patient(request: Request):
    token = request.cookies.get(COOKIE, "")
    if not token or len(token) > 128:
        raise HTTPException(401, "Enter your username to continue")
    with transaction() as cur:
        cur.execute("SELECT PatientId FROM Heartstep.UserSession WHERE TokenHash = ? AND ExpiresAt > ?",
                    [hashlib.sha256(token.encode()).hexdigest(), int(time.time())])
        row = cur.fetchone()
        if not row:
            raise HTTPException(401, "Your session has ended. Enter your username again")
        return row[0]


def logout(token):
    with transaction() as cur:
        cur.execute("DELETE FROM Heartstep.UserSession WHERE TokenHash = ?", [hashlib.sha256(token.encode()).hexdigest()])


def register(data: Registration):
    patient = "patient-" + uuid4().hex
    record = data.patient.model_dump(mode="json")
    # Lock a shared row to serialize username creation, including concurrent submits.
    with transaction() as cur:
        cur.execute("UPDATE Heartstep.Patient SET Stopped = Stopped WHERE PatientId = ?", [PATIENT])
        cur.execute("SELECT PatientId FROM Heartstep.Account WHERE Username = ?", [data.username])
        if cur.fetchone():
            raise RuleViolation("That username already exists. Sign in with it or choose another")
        profile = {"name": record["name"], "age": record["age"], "goal": record["goal"],
                   "diagnosis": (data.diagnoses[0].name + (f" (+{len(data.diagnoses)-1} more)" if len(data.diagnoses) > 1 else "")) if data.diagnoses else "Not provided"}
        cur.execute("INSERT INTO Heartstep.Patient (PatientId, ProfileJson, Stopped) VALUES (?, ?, 0)", [patient, json.dumps(profile, ensure_ascii=False)])
        cur.execute("INSERT INTO Heartstep.Account (Username, PatientId) VALUES (?, ?)", [data.username, patient])
        cur.execute("INSERT INTO Heartstep.PatientRecord (PatientId, RecordJson, MedicationStatus, CreatedAt) VALUES (?, ?, ?, ?)",
                    [patient, json.dumps(record, ensure_ascii=False), data.medicationStatus, datetime.now().astimezone().isoformat()])
        for table, entries in (("Diagnosis", data.diagnoses), ("Medication", data.medications), ("Measurement", data.measurements)):
            for entry in entries:
                payload = entry.model_dump(mode="json")
                if table == "Measurement":
                    payload["unit"] = UNITS[payload["kind"]]
                payload["source"] = "patient_entered"
                cur.execute(f"INSERT INTO Heartstep.{table} (RecordId, PatientId, DataJson) VALUES (?, ?, ?)",
                            [uuid4().hex, patient, json.dumps(payload, ensure_ascii=False)])
        if data.cpet:
            cpet = data.cpet.model_dump(mode="json")
            cpet.update(source="patient_entered_doctor_report", clinicianVerified=False)
            cur.execute("INSERT INTO Heartstep.CPET (PatientId, DataJson) VALUES (?, ?)", [patient, json.dumps(cpet, ensure_ascii=False)])
    return patient


def context(patient):
    with transaction() as cur:
        cur.execute("SELECT RecordJson, MedicationStatus, CreatedAt FROM Heartstep.PatientRecord WHERE PatientId = ?", [patient])
        row = cur.fetchone()
        record = {"patientRecord": json.loads(row[0]), "medicationStatus": row[1], "createdAt": row[2]} if row else {
            "patientRecord": None, "medicationStatus": "unknown", "createdAt": None}
        for table, key in (("Diagnosis", "diagnoses"), ("Medication", "medications"), ("Measurement", "measurements")):
            cur.execute(f"SELECT DataJson FROM Heartstep.{table} WHERE PatientId = ? ORDER BY RecordId", [patient])
            record[key] = [json.loads(r[0]) for r in cur.fetchall()]
        cur.execute("SELECT DataJson FROM Heartstep.CPET WHERE PatientId = ?", [patient])
        row = cur.fetchone()
        record["cpet"] = json.loads(row[0]) if row else None
        cur.execute("SELECT LimitJson FROM Heartstep.ClinicalLimit WHERE PatientId = ?", [patient])
        row = cur.fetchone()
        record["clinicianLimits"] = json.loads(row[0]) if row else None
        cur.execute("SELECT Username FROM Heartstep.Account WHERE PatientId = ?", [patient])
        record["username"] = cur.fetchone()[0]
    record.update(patientId=patient, schemaVersion=1, dataSource="patient_entered" if patient != PATIENT else "fictional_seed")
    state = snapshot(patient)
    record["safety"] = {"stopped": state["stopped"], "clinicianApproved": state["profile"]["clinicianApproved"]}
    return record
