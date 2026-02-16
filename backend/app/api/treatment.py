"""
Treatment recommendations API endpoints
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import PatientSymptoms, DiagnosisResult, TreatmentRecommendation
from app.services.medical_reasoning import medical_service
from pydantic import BaseModel

router = APIRouter()

class TreatmentRequest(BaseModel):
    """Request model for treatment recommendations"""
    patient_data: PatientSymptoms
    diagnosis: DiagnosisResult

@router.post("/recommend", response_model=TreatmentRecommendation)
async def recommend_treatment(request: TreatmentRequest):
    """
    Generate treatment recommendations based on diagnosis
    
    Args:
        request: Patient data and diagnosis results
        
    Returns:
        Treatment recommendations including tests and follow-up
    """
    try:
        recommendations = await medical_service.recommend_treatment(
            request.diagnosis,
            request.patient_data
        )
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")
