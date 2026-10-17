"""Idempotent FHIR R4 installation and fictional Heartstep seed records."""
import json
import os
import time
import httpx
import iris
from .db import connect, transaction
from .repository import PATIENT


def install_fhir():
    conn = connect("HSLIB", native=True)
    try:
        native = iris.createIRIS(conn)
        if not native.classMethodBoolean("%SYS.Namespace", "Exists", "FHIRSERVER"):
            native.classMethodVoid("HS.Util.Installer.Foundation", "Install", "FHIRSERVER")
    finally:
        conn.close()
    conn = connect("FHIRSERVER", native=True)
    try:
        native = iris.createIRIS(conn)
        if not native.classMethodBoolean("HS.FHIRServer.ServiceInstance", "ExistsByUrl", "/fhir/r4"):
            native.classMethodVoid("HS.FHIRServer.Installer", "InstallNamespace")
            native.classMethodVoid("HS.FHIRServer.Installer", "InstallInstance", "/fhir/r4",
                                   "HS.FHIRServer.Storage.JsonAdvSQL.InteractionsStrategy", "hl7.fhir.r4.core@4.0.1")
    finally:
        conn.close()


TABLES = {
    "Patient": "PatientId VARCHAR(64) PRIMARY KEY, ProfileJson VARCHAR(4000), Stopped INTEGER DEFAULT 0",
    "ClinicalLimit": "PatientId VARCHAR(64) PRIMARY KEY, LimitJson VARCHAR(4000)",
    "Completion": "PatientId VARCHAR(64), MissionDate VARCHAR(10), Kind VARCHAR(20), PRIMARY KEY (PatientId, MissionDate, Kind)",
    "ActivitySummary": "PatientId VARCHAR(64), ReadingDate VARCHAR(10), Steps INTEGER, RestingHR INTEGER, PRIMARY KEY (PatientId, ReadingDate)",
}


def seed_sql():
    with transaction() as cur:
        for name, columns in TABLES.items():
            cur.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?", ["Heartstep", name])
            if not cur.fetchone()[0]:
                cur.execute(f"CREATE TABLE Heartstep.{name} ({columns})")
        cur.execute("SELECT COUNT(*) FROM Heartstep.Patient WHERE PatientId = ?", [PATIENT])
        if cur.fetchone()[0]:
            return  # Preserve saved completions and symptom stops across restarts.
        profile = {"name": "Somchai", "age": 62, "diagnosis": "Recovering after MI",
                   "goal": "Feel confident walking again", "fhirPatientId": PATIENT}
        limit = {"approved": True, "maxHR": 110, "rpe": "Easy · able to talk comfortably",
                 "allowedActivities": ["walking"], "source": "Fictional clinician-approved CPET plan",
                 "approvedBy": "Demo rehab team (fictional)", "approvedOn": "2026-10-17", "reviewBy": "2026-11-17"}
        cur.execute("INSERT INTO Heartstep.Patient (PatientId, ProfileJson, Stopped) VALUES (?, ?, 0)", [PATIENT, json.dumps(profile)])
        cur.execute("INSERT INTO Heartstep.ClinicalLimit (PatientId, LimitJson) VALUES (?, ?)", [PATIENT, json.dumps(limit)])
        for day in range(12, 16):
            cur.execute("INSERT INTO Heartstep.Completion (PatientId, MissionDate, Kind) VALUES (?, ?, ?)", [PATIENT, f"2026-10-{day}", "walk"])
        cur.execute("INSERT INTO Heartstep.ActivitySummary (PatientId, ReadingDate, Steps, RestingHR) VALUES (?, ?, ?, ?)", [PATIENT, "2026-10-17", 2480, 68])


def seed_fhir():
    base = os.getenv("FHIR_BASE_URL", "http://localhost:52773/fhir/r4")
    resources = [
        {"resourceType": "Patient", "id": PATIENT, "active": True,
         "name": [{"family": "Demo", "given": ["Somchai"]}],
         "identifier": [{"system": "urn:heartstep:demo", "value": PATIENT}]},
        {"resourceType": "Observation", "id": "demo-resting-hr", "status": "final",
         "code": {"coding": [{"system": "http://loinc.org", "code": "8867-4", "display": "Heart rate"}]},
         "subject": {"reference": f"Patient/{PATIENT}"}, "effectiveDateTime": "2026-10-17T08:00:00+07:00",
         "valueQuantity": {"value": 68, "unit": "beats/minute", "system": "http://unitsofmeasure.org", "code": "/min"}},
    ]
    with httpx.Client(auth=(os.getenv("IRIS_USERNAME", "SuperUser"), os.environ["IRIS_PASSWORD"]), timeout=60) as client:
        for resource in resources:
            url = f"{base}/{resource['resourceType']}/{resource['id']}"
            existing = client.get(url)
            if existing.status_code == 200:
                continue
            if existing.status_code != 404:
                existing.raise_for_status()
            response = client.put(url, json=resource, headers={"Content-Type": "application/fhir+json"})
            response.raise_for_status()


def main():
    for attempt in range(60):
        try:
            conn = connect("HSLIB", native=True)
            conn.close()
            break
        except Exception:
            if attempt == 59:
                raise
            time.sleep(2)
    install_fhir()
    seed_sql()
    seed_fhir()
    print("IRIS ready: FHIR R4 and fictional Heartstep records initialized.")


if __name__ == "__main__":
    main()
