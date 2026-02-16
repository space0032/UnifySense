"""
Diagnosis API endpoints
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import PatientSymptoms, DiagnosisResult
from app.services.medical_reasoning import medical_service

router = APIRouter()

@router.post("/generate", response_model=DiagnosisResult)
async def generate_diagnosis(patient_data: PatientSymptoms):
    """
    Generate diagnostic suggestions based on patient symptoms
    
    Args:
        patient_data: Patient symptoms and information
        
    Returns:
        Diagnosis results with possible conditions and ICD-10 codes
    """
    try:
        diagnosis = await medical_service.generate_diagnosis(patient_data)
        return diagnosis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating diagnosis: {str(e)}")
