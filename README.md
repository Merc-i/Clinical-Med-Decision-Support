# Clinical Medication Decision Support System

A backend-focused **clinical medication decision-support prototype** built with Python and FastAPI.

The system evaluates proposed prescriptions against patient information and synthetic medication-safety rules, returning a decision, risk score, and explainable safety alerts.

 **Status: In active development**
This is an educational software prototype using synthetic clinical data. It is not intended for real-world clinical use.

## Features

- Patient and medication management using PostgreSQL
- Relational modelling of current medications and allergies
- Prescription request validation with Pydantic
- Database access using SQLAlchemy
- Database migrations using Alembic
- Rule-based medication safety engine
- Allergy checking
- Drug interaction checking
- Dosage checking
- Duplicate therapy checking
- Deterministic safety decisions
- Synthetic risk scoring
- Automated unit tests
- FastAPI Swagger documentation

## How It Works

Prescription Request
        ↓
Pydantic Validation
        ↓
Database Lookup
        ↓
Patient + Medication + Allergies + Current Medications
        ↓
Evaluation Context
        ↓
Safety Rules
        ↓
Decision Engine
        ↓
Decision and Risk Score and Alerts

The current decision logic is:


No alerts           → PASS
LOW / MODERATE      → WARNING
HIGH / CRITICAL     → REJECT


These rules and risk scores are synthetic prototype conventions and are not clinically validated.

## Technology Stack

- Python
- FastAPI
- Pydantic
- PostgreSQL
- SQLAlchemy
- Alembic
- asyncpg
- Docker Compose
- Pytest
- Redis

## API Example

### `POST /evaluate`

Example request:

```json
{
  "patient_id": 1,
  "medication_id": 1,
  "dosage": {
    "amount": 500,
    "unit": "mg"
  },
  "frequency": "twice daily"
}
```

Example response:

```json
{
  "decision": "PASS",
  "risk_score": 0,
  "alerts": []
}
```

The API is also available through FastAPI's interactive Swagger documentation at `/docs`.

## Running Locally

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start PostgreSQL and Redis

```bash
docker compose up -d
```

### Run migrations

```bash
alembic upgrade head
```

### Start the API

```bash
uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

### Run tests

```bash
python -m pytest -v
```

## Project Status

The core database, API validation, rule engine, and database-backed prescription evaluation are currently implemented.

The project is still being developed. Planned improvements include:

- More robust medication/allergy relationships
- Expanded clinical safety rules
- API and integration test coverage
- Prescription audit functionality
- Improved error handling
- Authentication and authorization
- Further infrastructure and deployment improvements

## Disclaimer

This project uses synthetic data and simplified clinical rules for educational and software-engineering purposes.

**It must not be used to make real clinical or medication decisions.**
