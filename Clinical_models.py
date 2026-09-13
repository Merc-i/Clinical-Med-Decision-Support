from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, Float,  DateTime, ForeignKey,  Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class PatientModel(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50),  nullable=False)
    last_name = Column(String(50), nullable = False)
    date_of_birth = Column(String(10), nullable=False)
    created_at = Column(DateTime, default = lambda: datetime.now(timezone.utc), nullable=False)

    #Relationships
    prescriptions = relationship("PrescriptionRecord", back_populates="patient")
    audits = relationship("PrescriptionAuditModel", back_populates="patient")
    patient_medications = relationship("PatientMedication", back_populates="patient")
    allergies = relationship("PatientAllergyModel", back_populates="patient")


class MedicationRecord(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key = True, index=True)
    name = Column(String(100), unique = True, nullable=False)
    generic_name = Column(String(100), nullable=False)
    drug_class = Column(String(100), nullable = True)

    #Relationship to PrescriptionRecord
    prescriptions = relationship("PrescriptionRecord", back_populates = "medication")
    patient_medications = relationship("PatientMedication", back_populates="medication")



class PatientMedication(Base):
    __tablename__ = "patient_medications"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    medication_id = Column(Integer, ForeignKey("medications.id"), nullable=False, index=True)
    dosage = Column(String(50), nullable=False)
    frequency = Column(String(50), nullable=False)
    start_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    end_date = Column(DateTime, nullable=True)

    #Relationships
    patient = relationship("PatientModel", back_populates="patient_medications")
    medication = relationship("MedicationRecord", back_populates="patient_medications")


class PatientAllergyModel(Base):
    __tablename__ = "patient_allergies"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    allergy_substance = Column(String(100), nullable=False)
    severity = Column(String(50), nullable=False)
    reaction = Column(Text, nullable=True)

    patient = relationship("PatientModel", back_populates="allergies")


class PrescriptionRecord(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key = True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable = False)
    medication_id = Column(Integer, ForeignKey("medications.id"), nullable=False)
    dosage = Column(String(50), nullable=False)
    frequency = Column(String(50), nullable=False)
    prescribed_at = Column(DateTime, default = lambda: datetime.now(timezone.utc), nullable=False)

    #Relationships
    patient = relationship("PatientModel", back_populates="prescriptions")
    medication = relationship("MedicationRecord", back_populates="prescriptions")
    audits = relationship("PrescriptionAuditModel", back_populates="prescription")


class PrescriptionAuditModel(Base):

    __tablename__ = "prescription_audits"

    id = Column(Integer, primary_key = True, index = True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    decision = Column(String(20), nullable=False) # PASS, WARNING, REJECT
    risk_score = Column(Float, nullable=False)
    rule_version = Column(String(50), nullable =  False)
    evaluated_at = Column(DateTime, default = lambda: datetime.now(timezone.utc), nullable=False)

    #Relationships
    prescription = relationship("PrescriptionRecord", back_populates="audits")
    patient = relationship("PatientModel", back_populates="audits")


class ClinicalRuleModel(Base):
    __tablename__ = "clinical_rules"

    id = Column(Integer, primary_key=True, index=True)
    rule_identifier = Column(String(100), unique= True, nullable=False)
    rule_type = Column(String(50), nullable=False) # e.g., Drug-Drug Interaction, Allergy, etc.
    version = Column(String(20), nullable=False) 
    is_enabled = Column(Boolean, default=True, nullable=False)
    configuration = Column(Text, nullable=True)  # JSON or any other format for rule configuration
    
    





