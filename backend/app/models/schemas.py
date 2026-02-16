"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class SeverityLevel(str, Enum):
    """Symptom severity levels"""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"

class SymptomInput(BaseModel):
    """Model for symptom input"""
    symptom: str = Field(..., description="Description of the symptom")
    severity: SeverityLevel = Field(..., description="Severity level")
    duration_days: int = Field(..., ge=0, description="Duration in days")
    additional_notes: Optional[str] = None

class PatientSymptoms(BaseModel):
    """Model for patient symptoms submission"""
    patient_id: Optional[str] = None
    age: int = Field(..., ge=0, le=150)
    gender: str = Field(..., pattern="^(male|female|other)$")
    symptoms: List[SymptomInput]
    medical_history: Optional[List[str]] = []
    current_medications: Optional[List[str]] = []
    allergies: Optional[List[str]] = []

class DiagnosisResult(BaseModel):
    """Model for diagnosis result"""
    diagnosis_id: str
    possible_conditions: List[Dict[str, any]]
    confidence_score: float = Field(..., ge=0, le=1)
    reasoning: str
    icd10_codes: List[str]
    created_at: datetime

class TreatmentRecommendation(BaseModel):
    """Model for treatment recommendations"""
    recommended_tests: List[str]
    recommended_treatments: List[str]
    urgency_level: str
    follow_up_required: bool
    precautions: List[str]
    reasoning: str

class PatientRecord(BaseModel):
    """Model for patient record"""
    patient_id: str
    age: int
    gender: str
    medical_history: List[str]
    current_medications: List[str]
    allergies: List[str]
    created_at: datetime
    updated_at: datetime

class AnalysisResponse(BaseModel):
    """Model for symptom analysis response"""
    analysis_id: str
    summary: str
    severity_assessment: str
    recommended_action: str
    triage_priority: str
    ai_insights: str
