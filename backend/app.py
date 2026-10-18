"""Loopback-only prototype with username identification and patient-scoped sessions."""
import logging
from pathlib import Path
from typing import Literal
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, Response
from pydantic import BaseModel, ConfigDict
from . import repository
from .db import transaction
from . import accounts
from .models import Registration, Username

app = FastAPI(title="ReVibe IRIS demo", version="0.1.0")
ROOT = Path(__file__).resolve().parent.parent


@app.middleware("http")
async def local_demo_boundary(request: Request, call_next):
    # Reject browser requests from other sites, including cross-origin writes.
    origin = request.headers.get("origin")
    if origin and origin != str(request.base_url).rstrip("/"):
        return JSONResponse({"detail": "Cross-origin requests are disabled"}, status_code=403)
    if request.headers.get("sec-fetch-site") == "cross-site":
        return JSONResponse({"detail": "Cross-site requests are disabled"}, status_code=403)
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store"
    return response


@app.exception_handler(repository.RuleViolation)
async def rule_error(request, exc):
    return JSONResponse({"detail": str(exc)}, status_code=409)


@app.exception_handler(Exception)
async def database_error(request, exc):
    logging.getLogger(__name__).error("IRIS request failed", exc_info=exc)
    return JSONResponse({"detail": "IRIS is unavailable. Check the API container logs."}, status_code=503)


class CompletionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    completed: bool


@app.get("/api/health")
def health():
    with transaction() as cur:
        cur.execute("SELECT 1")
        cur.fetchone()
    return {"status": "ok", "database": "iris"}


@app.get("/api/demo")
def demo():
    return repository.snapshot()


@app.put("/api/demo/completions/{kind}")
def complete(kind: Literal["walk", "medication"], body: CompletionRequest):
    return repository.completion(kind, body.completed)


@app.post("/api/demo/stop")
def stop():
    return repository.stop()


@app.post("/api/demo/reset")
def reset():
    return repository.reset()


def session_cookie(response, patient):
    response.set_cookie(accounts.COOKIE, accounts.new_session(patient), httponly=True,
                        samesite="strict", max_age=accounts.SESSION_SECONDS, path="/")


@app.post("/api/login")
def login(body: Username, response: Response):
    patient = accounts.find_user(body.username)
    if not patient:
        # Clear any previous user's session before starting a new registration.
        response.delete_cookie(accounts.COOKIE, path="/")
        return {"exists": False, "username": body.username}
    session_cookie(response, patient)
    return {"exists": True, "username": body.username}


@app.post("/api/register", status_code=201)
def register(body: Registration, response: Response):
    patient = accounts.register(body)
    session_cookie(response, patient)
    return {"username": body.username, "patientId": patient}


@app.post("/api/logout")
def logout(request: Request, response: Response):
    accounts.logout(request.cookies.get(accounts.COOKIE, ""))
    response.delete_cookie(accounts.COOKIE, path="/")
    return {"ok": True}


@app.get("/api/me")
def me(patient=Depends(accounts.current_patient)):
    data = repository.snapshot(patient)
    data["record"] = accounts.context(patient)
    return data


@app.get("/api/me/context")
def agent_context(patient=Depends(accounts.current_patient)):
    return accounts.context(patient)


@app.put("/api/me/completions/{kind}")
def user_complete(kind: Literal["walk", "medication"], body: CompletionRequest,
                  patient=Depends(accounts.current_patient)):
    return repository.completion(kind, body.completed, patient)


@app.post("/api/me/stop")
def user_stop(patient=Depends(accounts.current_patient)):
    return repository.stop(patient)


@app.get("/runtime.js")
def runtime():
    return Response("window.HEARTSTEP_API = true;", media_type="text/javascript")


@app.get("/{filename:path}")
def static(filename: str):
    filename = filename or "index.html"
    if filename not in {"index.html", "app.js", "safety.js", "styles.css", "access.js", "demo/agent-flow-demo.html"}:
        raise HTTPException(404)
    return FileResponse(ROOT / filename)
