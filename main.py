from fastapi import FastAPI

from schemas import EvaluationResponse, PrescriptionCreate
from rules import DecisionEngine, EvaluationContext


app = FastAPI(title="Clinical Med Decision Support")


@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "message": "Clinical Med Decision Support is running.",
    }


@app.post("/evaluate", response_model=EvaluationResponse)
def evaluate_prescription(prescription: PrescriptionCreate):
    return {
        "decision": "PASS",
        "risk_score": 0,
        "alerts": [],
    }

