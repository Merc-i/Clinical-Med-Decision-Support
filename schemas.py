from typing import Literal
from pydantic import BaseModel, Field

class Dosage(BaseModel):

    amount: float = Field(gt = 0)
    unit: Literal["mg", "g", "mL", "mcg"]


class PrescriptionCreate(BaseModel):
    patient_id: int=Field(gt=0)
    medication_id: int=Field(gt=0)
    dosage : Dosage
    frequency: str = Field(min_length=1)

class SafetyAlert(BaseModel):
    rule_id: str
    rule_type : str
    severity : Literal["low", "moderate", "high", "critical"]
    message : str


class EvaluationResponse(BaseModel):
    decision: str
    risk_score: float = Field(ge=0)
    alerts: list[SafetyAlert] 


    





