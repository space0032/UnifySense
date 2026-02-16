"""
Symptoms analysis API endpoints
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import PatientSymptoms, AnalysisResponse
from app.services.medical_reasoning import medical_service

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_symptoms(patient_data: PatientSymptoms):
    """
    Analyze patient symptoms and provide quick triage assessment
    
    Args:
        patient_data: Patient symptoms and information
        
    Returns:
        Analysis results with triage recommendations
    """
    try:
        analysis = await medical_service.analyze_symptoms(patient_data)
        return AnalysisResponse(**analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing symptoms: {str(e)}")
