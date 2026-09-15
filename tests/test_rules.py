from types import SimpleNamespace

from rules import AllergyRule, DosageRule, DrugInteractionRule, EvaluationContext, DuplicateTherapyRule,  DecisionEngine
from schemas import PrescriptionCreate


def test_allergy_rule_detects_conflict():
    medication = SimpleNamespace(name="warfarin")

    allergy = SimpleNamespace(
        allergy_substance="warfarin",
    )

    prescription = PrescriptionCreate(
        patient_id=1,
        medication_id=1,
        dosage={
            "amount": 5,
            "unit": "mg",
        },
        frequency="once daily",
    )

    context = EvaluationContext(
        patient=SimpleNamespace(id=1),
        prescription=prescription,
        medication=medication,
        current_medications=[],
        allergies=[allergy],
    )

    result = AllergyRule().evaluate(context)

    assert result is not None
    assert result.rule_id == "allergy_check"
    assert result.severity == "critical"

def test_allergy_rule_returns_none_when_no_conflict():
    medication = SimpleNamespace(name="warfarin")

    allergy = SimpleNamespace(
        allergy_substance="ibuprofen",
    )

    prescription = PrescriptionCreate(
        patient_id=1,
        medication_id=1,
        dosage={
            "amount": 5,
            "unit": "mg",
        },
        frequency="once daily",
    )

    context = EvaluationContext(
        patient=SimpleNamespace(id=1),
        prescription=prescription,
        medication=medication,
        current_medications=[],
        allergies=[allergy],
    )

    result = AllergyRule().evaluate(context)

    assert result is None


def test_drug_interaction_rule_detects_interaction():
    medication = SimpleNamespace(name="warfarin")

    current_medication = SimpleNamespace(name="ibuprofen")

    prescription = PrescriptionCreate(
        patient_id=1,
        medication_id=1,
        dosage={
            "amount": 5,
            "unit": "mg",
        },
        frequency="once daily",
    )

    context = EvaluationContext(
        patient=SimpleNamespace(id=1),
        prescription=prescription,
        medication=medication,
        current_medications=[current_medication],
        allergies=[],
    )

    result = DrugInteractionRule().evaluate(context)

    assert result is not None
    assert result.rule_id == "drug_interaction_check"
    assert result.severity == "high"

def test_drug_interaction_rule_returns_none_when_no_interaction():
    medication = SimpleNamespace(name="warfarin")

    current_medication = SimpleNamespace(name="simvastatin")

    prescription = PrescriptionCreate(
        patient_id=1,
        medication_id=1,
        dosage={
            "amount": 5,
            "unit": "mg",
        },
        frequency="once daily",
    )

    context = EvaluationContext(
        patient=SimpleNamespace(id=1),
        prescription=prescription,
        medication=medication,
        current_medications=[current_medication],
        allergies=[],
    )

    result = DrugInteractionRule().evaluate(context)

    assert result is None


def test_dosage_rule_detects_excessive_dosage():
    medication = SimpleNamespace(name="warfarin")

    prescription = PrescriptionCreate(
        patient_id=1,
        medication_id=1,
        dosage={
            "amount": 15,
            "unit": "mg",
        },
        frequency="once daily",
    )

    context = EvaluationContext(
        patient=SimpleNamespace(id=1),
        prescription=prescription,
        medication=medication,
        current_medications=[],
        allergies=[],
    )

    result = DosageRule().evaluate(context)

    assert result is not None
    assert result.rule_id == "dosage_check"
    assert result.severity == "high"


def test_dosage_rule_returns_none_when_dosage_is_within_limit():
    medication = SimpleNamespace(name="warfarin")

    prescription = PrescriptionCreate(
        patient_id=1,
        medication_id=1,
        dosage={
            "amount": 5,
            "unit": "mg",
        },
        frequency="once daily",
    )

    context = EvaluationContext(
        patient=SimpleNamespace(id=1),
        prescription=prescription,
        medication=medication,
        current_medications=[],
        allergies=[],
    )

    result = DosageRule().evaluate(context)

    assert result is None


def test_duplicate_therapy_rule_detects_same_category():
    medication = SimpleNamespace(name="warfarin")

    current_medication = SimpleNamespace(name="warfarin")

    prescription = PrescriptionCreate(
        patient_id=1,
        medication_id=1,
        dosage={
            "amount": 5,
            "unit": "mg",
        },
        frequency="once daily",
    )

    context = EvaluationContext(
        patient=SimpleNamespace(id=1),
        prescription=prescription,
        medication=medication,
        current_medications=[current_medication],
        allergies=[],
    )

    result = DuplicateTherapyRule().evaluate(context)

    assert result is not None
    assert result.rule_id == "duplicate_therapy_check"
    assert result.severity == "moderate"


def test_duplicate_therapy_rule_returns_none_for_different_category():
    medication = SimpleNamespace(name="warfarin")

    current_medication = SimpleNamespace(name="ibuprofen")

    prescription = PrescriptionCreate(
        patient_id=1,
        medication_id=1,
        dosage={
            "amount": 5,
            "unit": "mg",
        },
        frequency="once daily",
    )

    context = EvaluationContext(
        patient=SimpleNamespace(id=1),
        prescription=prescription,
        medication=medication,
        current_medications=[current_medication],
        allergies=[],
    )

    result = DuplicateTherapyRule().evaluate(context)

    assert result is None


def test_decision_engine_rejects_critical_alert():
    medication = SimpleNamespace(name="warfarin")

    allergy = SimpleNamespace(
        allergy_substance="warfarin",
    )

    prescription = PrescriptionCreate(
        patient_id=1,
        medication_id=1,
        dosage={
            "amount": 5,
            "unit": "mg",
        },
        frequency="once daily",
    )

    context = EvaluationContext(
        patient=SimpleNamespace(id=1),
        prescription=prescription,
        medication=medication,
        current_medications=[],
        allergies=[allergy],
    )

    engine = DecisionEngine(
        rules=[AllergyRule()]
    )

    decision, risk_score, alerts = engine.evaluate(context)

    assert decision == "REJECT"
    assert len(alerts) == 1
    assert alerts[0].severity == "critical"


def test_decision_engine_returns_warning_for_moderate_alert():
    medication = SimpleNamespace(name="warfarin")

    current_medication = SimpleNamespace(name="warfarin")

    prescription = PrescriptionCreate(
        patient_id=1,
        medication_id=1,
        dosage={
            "amount": 5,
            "unit": "mg",
        },
        frequency="once daily",
    )

    context = EvaluationContext(
        patient=SimpleNamespace(id=1),
        prescription=prescription,
        medication=medication,
        current_medications=[current_medication],
        allergies=[],
    )

    engine = DecisionEngine(
        rules=[DuplicateTherapyRule()]
    )

    decision, risk_score, alerts = engine.evaluate(context)

    assert decision == "WARNING"
    assert len(alerts) == 1
    assert alerts[0].severity == "moderate"


def test_decision_engine_returns_pass_when_no_alerts():
    medication = SimpleNamespace(name="warfarin")

    prescription = PrescriptionCreate(
        patient_id=1,
        medication_id=1,
        dosage={
            "amount": 5,
            "unit": "mg",
        },
        frequency="once daily",
    )

    context = EvaluationContext(
        patient=SimpleNamespace(id=1),
        prescription=prescription,
        medication=medication,
        current_medications=[],
        allergies=[],
    )

    engine = DecisionEngine(
        rules=[AllergyRule()]
    )

    decision, risk_score, alerts = engine.evaluate(context)

    assert decision == "PASS"
    assert alerts == []

def test_decision_engine_calculates_risk_score():
    medication = SimpleNamespace(name="warfarin")

    allergy = SimpleNamespace(
        allergy_substance="warfarin",
    )

    prescription = PrescriptionCreate(
        patient_id=1,
        medication_id=1,
        dosage={
            "amount": 5,
            "unit": "mg",
        },
        frequency="once daily",
    )

    context = EvaluationContext(
        patient=SimpleNamespace(id=1),
        prescription=prescription,
        medication=medication,
        current_medications=[],
        allergies=[allergy],
    )

    engine = DecisionEngine(
        rules=[AllergyRule()]
    )

    decision, risk_score, alerts = engine.evaluate(context)

    risk_score = engine.calculate_risk_score(alerts)

    assert decision == "REJECT"
    assert risk_score == 10