import unittest
from pydantic import ValidationError
from fastapi.testclient import TestClient
from backend.app import app
from backend.models import Registration, Username


def payload():
    return {"username": "test-user", "patient": {"name": "Test Patient", "age": 62, "goal": "Build a routine"}}


class OnboardingTests(unittest.TestCase):
    def test_username_normalized_and_rejects_unsafe_values(self):
        self.assertEqual(Username(username="  Somchai  ").username, "somchai")
        for username in ("a", "two words", "../../user", "x" * 33):
            with self.assertRaises(ValidationError):
                Username(username=username)

    def test_cpet_is_optional_and_never_accepts_approval(self):
        self.assertIsNone(Registration(**payload()).cpet)
        data = payload()
        data["cpet"] = {"testDate": "2026-10-17", "doctorName": "Demo Doctor", "heartRateVT1": 100}
        self.assertEqual(Registration(**data).cpet.heartRateVT1, 100)
        data["cpet"]["clinicianApproved"] = True
        with self.assertRaises(ValidationError):
            Registration(**data)

    def test_measurements_require_value_and_dated_timezone(self):
        data = payload()
        data["measurements"] = [{"kind": "heart_rate", "value": 68, "measuredAt": "2026-10-18T08:00:00+07:00"}]
        self.assertEqual(Registration(**data).measurements[0].value, 68)
        for bad in (float("nan"), -1):
            data["measurements"][0]["value"] = bad
            with self.assertRaises(ValidationError):
                Registration(**data)
        data["measurements"][0].update(value=68, measuredAt="2026-10-18T08:00:00")
        with self.assertRaises(ValidationError):
            Registration(**data)

    def test_medication_unknown_is_distinct_from_none(self):
        self.assertEqual(Registration(**payload()).medicationStatus, "unknown")
        data = payload()
        data["medicationStatus"] = "none"
        self.assertEqual(Registration(**data).medicationStatus, "none")
        data["medications"] = [{"name": "Sample medication"}]
        with self.assertRaises(ValidationError):
            Registration(**data)

    def test_patient_endpoints_require_session(self):
        client = TestClient(app)
        for path in ("/api/me", "/api/me/context"):
            self.assertEqual(client.get(path).status_code, 401)
        self.assertEqual(client.post("/api/me/stop").status_code, 401)
        self.assertEqual(client.put("/api/me/completions/walk", json={"completed": True}).status_code, 401)


if __name__ == "__main__":
    unittest.main()
