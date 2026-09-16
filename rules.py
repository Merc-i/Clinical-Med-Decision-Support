from enum import Enum
from typing import Any, Protocol

from schemas import PrescriptionCreate, SafetyAlert
from synthetic_rules import (
    find_drug_interaction,
    get_dosage_limit,
    get_therapeutic_category,
)


class Severity(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class BaseRule(Protocol):
    rule_id: str
    rule_type: str

    def evaluate(self, context):
        raise NotImplementedError


class EvaluationContext:
    def __init__(
        self,
        patient: Any,
        prescription: PrescriptionCreate,
        medication: Any,
        current_medications: list[Any],
        allergies: list[Any],
    ):
        self.patient = patient
        self.prescription = prescription
        self.medication = medication
        self.current_medications = current_medications
        self.allergies = allergies


class AllergyRule:
    rule_id = "allergy_check"
    rule_type = "allergy"

    def evaluate(self, context):
        for allergy in context.allergies:
           medication_name = context.medication.name.lower()
           drug_class = getattr(context.medication, "drug_class", None)

           if allergy.allergy_substance.lower() in medication_name or (
                drug_class and allergy.allergy_substance.lower() in drug_class.lower()
            ):
                return SafetyAlert(
                    rule_id=self.rule_id,
                    rule_type=self.rule_type,
                    severity="critical",
                    message=(
                        f"Proposed medication conflicts with documented allergy: "
                        f"{allergy.allergy_substance}."
                    ),
                )
        return None


class DrugInteractionRule:
    rule_id = "drug_interaction_check"
    rule_type = "drug_interaction"

    def evaluate(self, context):
        interaction = find_drug_interaction(
            context.medication,
            context.current_medications,
        )

        if interaction is None:
            return None

        return SafetyAlert(
            rule_id=self.rule_id,
            rule_type=self.rule_type,
            severity=interaction["severity"],
            message=interaction["message"],
        )


class DosageRule:
    rule_id = "dosage_check"
    rule_type = "dosage"

    def evaluate(self, context):
        limit = get_dosage_limit(context.medication.name)

        if limit is None:
            return None

        dosage = context.prescription.dosage

        if dosage.unit != limit["unit"]:
            return None

        if dosage.amount > limit["max_amount"]:
            return SafetyAlert(
                rule_id=self.rule_id,
                rule_type=self.rule_type,
                severity="high",
                message=(
                    "Proposed dosage exceeds the documented limit of "
                    f"{limit['max_amount']} {limit['unit']}"
                ),
            )
        return None


class DuplicateTherapyRule:
    rule_id = "duplicate_therapy_check"
    rule_type = "duplicate_therapy"

    def evaluate(self, context):
        proposed_category = get_therapeutic_category(context.medication.name)

        if proposed_category is None:
            return None

        for medication in context.current_medications:
            current_category = get_therapeutic_category(medication.name)

            if current_category == proposed_category:
                return SafetyAlert(
                    rule_id=self.rule_id,
                    rule_type=self.rule_type,
                    severity="moderate",
                    message=(
                        "Proposed medication belongs to the same therapeutic category as an "
                        f"existing medication: {proposed_category}."
                    ),
                )

        return None


RISK_SCORES = {
    "low": 1,
    "moderate": 3,
    "high": 7,
    "critical": 10,
}


class DecisionEngine:
    def __init__(self, rules):
        self.rules = rules

    def evaluate(self, context):
        alerts = []

        for rule in self.rules:
            result = rule.evaluate(context)
            if result is not None:
                alerts.append(result)

        decision = self.aggregate_decision(alerts)
        risk_score = self.calculate_risk_score(alerts)

        return decision, risk_score, alerts

    def aggregate_decision(self, alerts):
        if not alerts:
            return "PASS"

        severities = {alert.severity for alert in alerts}

        if "critical" in severities or "high" in severities:
            return "REJECT"

        return "WARNING"

    def calculate_risk_score(self, alerts):
        return sum(RISK_SCORES.get(alert.severity, 0) for alert in alerts)

