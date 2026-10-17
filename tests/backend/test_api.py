import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.app import app


class ApiBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_static_server_does_not_expose_source_or_secrets(self):
        for path in ("/.env", "/backend/db.py", "/compose.yaml", "/.git/config"):
            self.assertEqual(self.client.get(path).status_code, 404)
        self.assertIn("HEARTSTEP_API = true", self.client.get("/runtime.js").text)

    def test_rejects_cross_origin_mutations(self):
        response = self.client.post("/api/demo/reset", headers={"Origin": "https://example.com"})
        self.assertEqual(response.status_code, 403)

    def test_does_not_accept_clinical_limits_from_browser(self):
        response = self.client.put("/api/demo/completions/walk", json={"completed": True, "maxHR": 200})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.client.put("/api/demo/completions/running", json={"completed": True}).status_code, 422)

    def test_database_failure_returns_service_unavailable(self):
        with patch("backend.repository.snapshot", side_effect=RuntimeError("private connection details")), patch("backend.app.logging.getLogger"):
            response = TestClient(app, raise_server_exceptions=False).get("/api/demo")
        self.assertEqual(response.status_code, 503)
        self.assertNotIn("private connection details", response.text)


if __name__ == "__main__":
    unittest.main()
