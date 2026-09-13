from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, Float, column, DateTime, ForeignKey,  Integer, String, false, Text
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class PatientModel(Base):
    __tablenname__ = "patients"

    id = column(Integer, Primary_key=True, index=True)
    first_name = Column(String(50),  nullable=False)
    last_name = column(String(50), nullable = False)
    date_of_birth = column(String(10), nullable=False)
    created_at = Column(DateTime, default = lambda: datetime.now(timezone.utc), nullable=False)


    class MedicationRecord(Base):
        __tablemame__ = "medications"

        id = column(Integer, primary_key = True, Index=True)
        name = Column(String(100), unique = True, nullable=False)
        generic_name = Column(String(100), nullable=False)
        drug_class = Column(String(100), nullable = False)

        #Relationship to PrescriptionRecord
        prescriptions = relationship("PrescriptionRecord", back_populates = "medication")


    class PrescriptionRecord(Base):
        __tablename__ = "prescriptions"

        id = Column(Integer, Primary_key = True, Index=True)
        patient_id = Column(Integer, ForeignKey("patients.id"), nullable = False)
        medication_id = Column(Integer, ForeignKey("medications.id"), nullable=False)
        dosage = Column(String(50), nullable=False)
        frequency = Column(String(50), nullable=False)
        prescribed_at = Column(DateTime, default = lambda: datetime.now(timezone.utc), nullable=False)

        #Relationships
        patient = relationship("PatientModel", back_populates="prescriptions")
        medication = relationship("MedicationRecord", back_populates="prescriptions")


    class PrescriptionAuditModel(Base):

        __tablename__ = "prescription_audit"

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
        
        





