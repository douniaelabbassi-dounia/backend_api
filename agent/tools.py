# agent/tools.py
import os
import requests
from typing import Any, Dict, List, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

# ---- Schémas "logiques" des 8 tools ----
# (le LLM les voit; nous, on appelle les endpoints derrière)

TOOLS_SPEC = [
    {
        "name": "predict_salary",
        "description": "Predicts competitive salary (MAD) for a role with given features.",
        "parameters": {
            "type": "object",
            "properties": {
                "years_experience": {"type": "number"},
                "role": {"type": "string"},
                "degree": {"type": "string"},
                "company_size": {"type": "string"},
                "location": {"type": "string"},
                "level": {"type": "string"}
            },
            "required": ["years_experience", "role", "degree", "company_size", "location", "level"]
        }
    },
    {
        "name": "check_job_fit",
        "description": "Analyzes candidate vs job using the job-fit ML model and returns probability + binary fit.",
        "parameters": {
            "type": "object",
            "properties": {
                "candidate_id": {"type": "string"},
                "job_id": {"type": "string"}
            },
            "required": ["candidate_id", "job_id"]
        }
    },
    {
        "name": "screen_resume",
        "description": "Screens a resume against a job description, returns advance probability and binary decision.",
        "parameters": {
            "type": "object",
            "properties": {
                "resume_text": {"type": "string"},
                "job_text": {"type": "string"}
            },
            "required": ["resume_text", "job_text"]
        }
    },
    {
        "name": "get_priority",
        "description": "Ranks candidate priority level with confidence.",
        "parameters": {
            "type": "object",
            "properties": {
                "experience_band": {"type": "string"},
                "skills_coverage": {"type": "number"},
                "referral_flag": {"type": "boolean"},
                "english_level": {"type": "string"},
                "location_match": {"type": "boolean"}
            },
            "required": ["experience_band","skills_coverage","referral_flag","english_level","location_match"]
        }
    },
    # Data/DB helpers (simples stubs HTTP; à brancher sur Mongo plus tard)
    {
        "name": "get_candidate",
        "description": "Returns candidate profile by candidate_id.",
        "parameters": {"type": "object","properties":{"candidate_id":{"type":"string"}},"required":["candidate_id"]}
    },
    {
        "name": "get_job",
        "description": "Returns job posting by job_id.",
        "parameters": {"type": "object","properties":{"job_id":{"type":"string"}},"required":["job_id"]}
    },
    {
        "name": "list_candidates",
        "description": "Lists all candidates (paginated in future).",
        "parameters": {"type":"object","properties":{}}
    },
    {
        "name": "list_jobs",
        "description": "Lists all jobs (paginated in future).",
        "parameters": {"type":"object","properties":{}}
    },
]

# ---- Implémentations qui appellent ton backend Flask ----

def _post_json(path: str, payload: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
    url = f"{API_BASE}{path}"
    r = requests.post(url, json=payload, timeout=20)
    try:
        data = r.json()
    except Exception:
        data = {"error": f"Non-JSON response: {r.text[:200]}"}
    return r.status_code, data

def tool_predict_salary(args: Dict[str, Any]) -> Dict[str, Any]:
    code, data = _post_json("/api/salary/predict", args)
    return {"status_code": code, "data": data}

def tool_check_job_fit(args: Dict[str, Any]) -> Dict[str, Any]:
    # TODO: brancher sur /api/job_fit/predict quand ton modèle sera prêt
    return {"status_code": 501, "data": {"error": "job_fit not implemented yet"}}

def tool_screen_resume(args: Dict[str, Any]) -> Dict[str, Any]:
    # TODO: brancher sur /api/resume_screen/predict
    return {"status_code": 501, "data": {"error": "resume_screen not implemented yet"}}

def tool_get_priority(args: Dict[str, Any]) -> Dict[str, Any]:
    # TODO: brancher sur /api/candidate_priority/predict
    return {"status_code": 501, "data": {"error": "candidate_priority not implemented yet"}}

# Stubs simples pour la data (brancher MongoDB plus tard)
_FAKE_CANDIDATES = [
    {"candidate_id":"CAND001","name":"Ahmed El Mansouri","current_role":"DevOps Engineer",
     "years_experience":6.5,"skills":"Docker, Kubernetes, AWS, Linux","degree":"Masters"}
]
_FAKE_JOBS = [
    {"job_id":"JOB001","title":"Senior DevOps Engineer","company":"TechCorp Morocco","location":"Casablanca",
     "required_skills":"Docker, Kubernetes, AWS, Linux"}
]

def tool_get_candidate(args: Dict[str, Any]) -> Dict[str, Any]:
    cid = args.get("candidate_id")
    for c in _FAKE_CANDIDATES:
        if c["candidate_id"] == cid:
            return {"status_code": 200, "data": c}
    return {"status_code": 404, "data": {"error":"candidate not found"}}

def tool_get_job(args: Dict[str, Any]) -> Dict[str, Any]:
    jid = args.get("job_id")
    for j in _FAKE_JOBS:
        if j["job_id"] == jid:
            return {"status_code": 200, "data": j}
    return {"status_code": 404, "data": {"error":"job not found"}}

def tool_list_candidates(_: Dict[str, Any]) -> Dict[str, Any]:
    return {"status_code": 200, "data": _FAKE_CANDIDATES}

def tool_list_jobs(_: Dict[str, Any]) -> Dict[str, Any]:
    return {"status_code": 200, "data": _FAKE_JOBS}

# ---- Registry nom -> fonction implémentation ----
TOOLS_IMPL = {
    "predict_salary": tool_predict_salary,
    "check_job_fit": tool_check_job_fit,
    "screen_resume": tool_screen_resume,
    "get_priority": tool_get_priority,
    "get_candidate": tool_get_candidate,
    "get_job": tool_get_job,
    "list_candidates": tool_list_candidates,
    "list_jobs": tool_list_jobs,
}
