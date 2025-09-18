import pandas as pd
from .base import load_model

# chargé une seule fois au premier import du module
_model = load_model("salary_model.pkl")

REQUIRED = ["years_experience","role","degree","company_size","location","level"]

def validate(payload: dict) -> tuple[bool, dict | None | dict]:
    missing = [k for k in REQUIRED if k not in payload]
    if missing: return False, {"error": f"Missing fields: {', '.join(missing)}"}
    try:
        payload["years_experience"] = float(payload["years_experience"])
    except Exception:
        return False, {"error": "years_experience must be numeric"}
    for s in ["role","degree","company_size","location","level"]:
        if not isinstance(payload[s], str):
            return False, {"error": f"{s} must be string"}
        payload[s] = payload[s].strip()
    return True, payload

def predict_salary(payload: dict) -> float:
    ok, data = validate(payload)
    if not ok:
        raise ValueError(data["error"])
    df = pd.DataFrame([data])
    yhat = _model.predict(df)[0]
    return float(yhat)
