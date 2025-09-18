from flask import Blueprint, render_template, request
from ..services.salary_service import predict_salary, validate

bp = Blueprint("ui", __name__)
@bp.get("/")
def index():
    return render_template("index.html", prediction=None, error=None, **_form_options())

@bp.post("/predict")
def predict_from_form():
    form = request.form.to_dict()
    ok, payload = validate(form)
    if not ok:
        return render_template("index.html", prediction=None, error=payload["error"], **_form_options()), 400

    try:
        yhat = predict_salary(payload)
        return render_template("index.html", prediction=round(yhat, 2), error=None, **_form_options())
    except Exception as e:
        return render_template("index.html", prediction=None, error=f"Erreur : {e}", **_form_options()), 500

def _form_options():
    return dict(
        roles=[
            "Backend Developer", "BI Engineer", "Data Analyst", "Data Engineer",
            "Data Scientist", "DevOps Engineer", "Frontend Developer",
            "ML Engineer", "Product Manager", "QA Engineer"
        ],
        degrees=["No Degree", "Bachelors", "Masters", "PhD"],
        company_sizes=["Small", "Mid", "Large", "Enterprise"],
        locations=["Casablanca", "Rabat", "Fes", "Marrakech", "Tangier", "Agadir", "Remote"],
        levels=["Intern", "Junior", "Mid", "Senior", "Lead"]
    )
