from flask import Blueprint, request, jsonify
from ..schemas.salary import SalaryReq, SalaryResp
from ..services.salary_service import predict_salary

bp = Blueprint("salary", __name__)

@bp.post("/predict")
def predict():
    try:
        req = SalaryReq(**(request.get_json(silent=True) or {}))
    except Exception as e:
        # erreurs de validation Pydantic
        return jsonify({"error": str(e)}), 400

    try:
        yhat = predict_salary(req.model_dump())
        resp = SalaryResp(predicted_salary=round(yhat, 2))
        return jsonify(resp.model_dump()), 200
    except Exception as e:
        return jsonify({"error": f"Inference error: {e}"}), 500
