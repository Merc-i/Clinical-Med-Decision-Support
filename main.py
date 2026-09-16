from fastapi import FastAPI
from sqlalchemy import select

from Clinical_models import MedicationRecord, PatientAllergyModel, PatientModel, PatientMedication
from database import AsyncSessionLocal
from rules import (
    AllergyRule,
    DecisionEngine,
    DosageRule,
    DrugInteractionRule,
    DuplicateTherapyRule,
    EvaluationContext,
)
from schemas import EvaluationResponse, PrescriptionCreate

app = FastAPI(title="Clinical Med Decision Support")


@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "message": "Clinical Med Decision Support is running.",
    }


@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_prescription(prescription: PrescriptionCreate):
    async with AsyncSessionLocal() as session:
        patient_result = await session.execute(
            select(PatientModel).where(PatientModel.id == prescription.patient_id)
        )
        patient = patient_result.scalar_one_or_none()

        if patient is None:
            return {"decision": "REJECT", "risk_score": 0, "alerts": []}

        medication_result = await session.execute(
            select(MedicationRecord).where(MedicationRecord.id == prescription.medication_id)
        )
        medication = medication_result.scalar_one_or_none()

        if medication is None:
            return {"decision": "REJECT", "risk_score": 0, "alerts": []}

        current_medications_result = await session.execute(
            select(MedicationRecord)
            .join(PatientMedication, PatientMedication.medication_id == MedicationRecord.id)
            .where(
                PatientMedication.patient_id == patient.id,
                PatientMedication.active.is_(True),
            )
        )
        current_medications = current_medications_result.scalars().all()

        allergies_result = await session.execute(
            select(PatientAllergyModel).where(PatientAllergyModel.patient_id == patient.id)
        )
        allergies = allergies_result.scalars().all()

        context = EvaluationContext(
            patient=patient,
            prescription=prescription,
            medication=medication,
            current_medications=current_medications,
            allergies=allergies,
        )

        engine = DecisionEngine(
            rules=[
                AllergyRule(),
                DrugInteractionRule(),
                DosageRule(),
                DuplicateTherapyRule(),
            ]
        )

        decision, risk_score, alerts = engine.evaluate(context)
        return {"decision": decision, "risk_score": risk_score, "alerts": alerts}
 