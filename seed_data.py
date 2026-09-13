from datetime import datetime, timezone, date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



from Clinical_models import(
    Base,
    PatientModel,
    MedicationRecord,
    PatientMedication,
    PatientAllergyModel,
)

DATABASE_URL = "postgresql+psycopg2://postgres:summerwinterrain@localhost:5433/ClinicalMed_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

patients = [
    PatientModel(
        first_name="Joseph",
        last_name="Peters",
        date_of_birth=date(1985, 4, 12),
    ),
    PatientModel(
        first_name="Daniel",
        last_name="Johnson",
        date_of_birth=date(1972, 9, 28),
    ),
    PatientModel(
        first_name="Sophie",
        last_name="Harris",
        date_of_birth=date(1994, 1, 17),
    ),
]

medications = [
    MedicationRecord(
        name="Amoxicillin",
        generic_name="Amoxicillin",
        drug_class="Penicillin antibiotic",
    ),
    MedicationRecord(
        name="Metformin",
        generic_name="Metformin",
        drug_class="Biguanide",
    ),
    MedicationRecord(
        name="Lisinopril",
        generic_name="Lisinopril",
        drug_class="ACE inhibitor",
    ),
]

allergies = [
    PatientAllergyModel(
        patient=patients[0],
        allergy_substance="Penicillin",
        severity="Severe",
        reaction="Skin rash",
    ),
    PatientAllergyModel(
        patient=patients[1],
        allergy_substance="Sulfonamides",
        severity="Moderate",
        reaction="Hives",
    ),
    PatientAllergyModel(
        patient=patients[2],
        allergy_substance="Aspirin",
        severity="Mild",
        reaction="Stomach irritation",
    ),
]

existing_medications = [
    PatientMedication(
        patient=patients[0],
        medication=medications[1],
        dosage="500 mg",
        frequency="Twice daily",
        start_date=datetime(2026, 1, 10, tzinfo=timezone.utc),
        active=True,
    ),
    PatientMedication(
        patient=patients[1],
        medication=medications[2],
        dosage="10 mg",
        frequency="Once daily",
        start_date=datetime(2026, 2, 15, tzinfo=timezone.utc),
        active=True,
    ),
    PatientMedication(
        patient=patients[2],
        medication=medications[1],
        dosage="500 mg",
        frequency="Once daily",
        start_date=datetime(2026, 3, 1, tzinfo=timezone.utc),
        active=True,
    ),
]


def seed_database():
    session = SessionLocal()

    try:
        session.add_all(patients)
        session.add_all(medications)
        session.flush()

        session.add_all(allergies)
        session.add_all(existing_medications)

        session.commit()
        print("Synthetic data seeded successfully.")

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    seed_database()
