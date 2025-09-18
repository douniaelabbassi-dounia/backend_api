from pydantic import BaseModel, field_validator

class SalaryReq(BaseModel):
    years_experience: float
    role: str
    degree: str
    company_size: str
    location: str
    level: str

    @field_validator("role","degree","company_size","location","level")
    @classmethod
    def strip_str(cls, v: str) -> str:
        return v.strip()

class SalaryResp(BaseModel):
    predicted_salary: float
