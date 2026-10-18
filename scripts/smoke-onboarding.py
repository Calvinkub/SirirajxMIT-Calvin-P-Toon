"""Run inside the API container. Creates and removes only its own synthetic users."""
import sys
import uuid
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import httpx
from backend.db import transaction

created = []
base = "http://127.0.0.1:8000"


def request(client, method, path, data=None, status=200):
    r = client.request(method, path, json=data)
    assert r.status_code == status, f"{path}: {r.status_code} {r.text}"
    return r.json()


try:
    with httpx.Client(base_url=base) as first, httpx.Client(base_url=base) as second:
        request(first, "GET", "/api/me", status=401)
        known = request(first, "POST", "/api/login", {"username": "SOMCHAI"})
        assert known["exists"]
        assert request(first, "GET", "/api/me")["patientId"] == "demo-somchai"
        username = "test-" + uuid.uuid4().hex[:16]
        assert not request(first, "POST", "/api/login", {"username": username})["exists"]
        request(first, "GET", "/api/me", status=401)
        body = {"username": username, "patient": {"name": "Synthetic Test Patient", "age": 60, "goal": "Build a routine", "history": "Fictional history", "allergies": "None reported"},
                "diagnoses": [{"name": "Sample diagnosis", "code": "TEST", "diagnosedOn": "2026-10-17"}],
                "medications": [{"name": "Fictional medication", "dose": "Sample dose", "frequency": "As prescribed"}], "medicationStatus": "listed",
                "measurements": [{"kind": "heart_rate", "value": 68, "measuredAt": "2026-10-18T08:00:00+07:00"}], "cpet": None}
        result = request(first, "POST", "/api/register", body, 201)
        created.append((username, result["patientId"]))
        state = request(first, "GET", "/api/me")
        assert state["profile"]["name"] == body["patient"]["name"]
        assert not state["profile"]["clinicianApproved"] and state["profile"]["maxHR"] is None
        assert state["activity"] is None and state["weeklyWalks"] == 0
        record = request(first, "GET", "/api/me/context")
        assert record["cpet"] is None and record["clinicianLimits"] is None
        assert record["medications"][0]["name"] == "Fictional medication"
        assert record["measurements"][0]["unit"] == "bpm"
        assert record["patientRecord"]["history"] == "Fictional history"
        request(first, "PUT", "/api/me/completions/walk", {"completed": True}, 409)
        request(first, "POST", "/api/register", body, 409)
        request(first, "POST", "/api/logout", {})
        request(first, "GET", "/api/me", status=401)
        assert request(first, "POST", "/api/login", {"username": username})["exists"]
        assert request(first, "GET", "/api/me/context")["patientRecord"]["history"] == "Fictional history"
        other = "test-" + uuid.uuid4().hex[:16]
        body2 = {"username": other, "patient": {"name": "Second Test Patient", "age": 55, "goal": "Gentle routine"}, "medicationStatus": "none",
                 "cpet": {"testDate": "2026-10-17", "doctorName": "Fictional Doctor", "heartRateVT1": 100, "vo2Peak": 20}}
        result = request(second, "POST", "/api/register", body2, 201)
        created.append((other, result["patientId"]))
        context = request(second, "GET", "/api/me/context")
        assert context["cpet"]["heartRateVT1"] == 100 and context["cpet"]["clinicianVerified"] is False
        assert context["medications"] == [] and context["diagnoses"] == [] and context["measurements"] == []
        assert not context["safety"]["clinicianApproved"]
        request(second, "POST", "/api/me/stop", {})
        assert request(second, "GET", "/api/me")["stopped"]
        assert not request(first, "GET", "/api/me")["stopped"]
        assert request(first, "GET", "/api/me/context")["username"] == username
        print("Onboarding smoke passed: existing login, no-CPET registration, CPET registration, persistent records, account isolation, and exercise lock.")
finally:
    # Remove only users created by this run; preserve all existing data.
    with transaction() as cur:
        for username, patient in created:
            for table in ("UserSession", "PatientRecord", "Diagnosis", "Medication", "Measurement", "CPET", "Completion", "ActivitySummary", "ClinicalLimit"):
                cur.execute(f"DELETE FROM Heartstep.{table} WHERE PatientId = ?", [patient])
            cur.execute("DELETE FROM Heartstep.Account WHERE Username = ? AND PatientId = ?", [username, patient])
            cur.execute("DELETE FROM Heartstep.Patient WHERE PatientId = ?", [patient])
