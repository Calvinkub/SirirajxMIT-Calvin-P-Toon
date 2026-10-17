"""Load the synthetic bundles into the IRIS for Health FHIR server from the FHIR-AI-Hackathon-Kit.

Start the server first (FHIR-AI-Hackathon-Kit/docker-iris-fhir), then:
    .venv/bin/python synthetic/load_to_iris.py

Bundles use PUT with fixed ids, so running this twice updates instead of duplicating.
Shared reference data (practitioners, places, services) loads first because patient bundles point at it.
"""

import json
from pathlib import Path

import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://localhost:52773/fhir/r4/"  # kit default
AUTH = HTTPBasicAuth("SuperUser", "SYS")       # kit default credentials, local demo only
HEADERS = {"Content-Type": "application/fhir+json", "Accept": "application/fhir+json"}

files = sorted((Path(__file__).parent / "fhir").glob("*.json"))  # 00_shared_* sorts first
for i, path in enumerate(files, 1):
    bundle = json.loads(path.read_text(encoding="utf-8"))
    res = requests.post(BASE_URL, json=bundle, headers=HEADERS, auth=AUTH, timeout=120)
    print(f"[{i}/{len(files)}] {path.name}: {res.status_code}")
    if res.status_code >= 400:
        for issue in res.json().get("issue", []):
            print("   ", issue.get("severity"), issue.get("diagnostics") or issue.get("details", {}).get("text"))
        raise SystemExit(1)
