"""
Patient records API endpoints
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import PatientRecord
from typing import Optional
from datetime import datetime
import uuid

router = APIRouter()

# In-memory storage for demo (in production, use DynamoDB)
patient_records = {}

@router.post("/", response_model=PatientRecord)
async def create_patient(
    age: int,
    gender: str,
    medical_history: Optional[list[str]] = None,
    current_medications: Optional[list[str]] = None,
    allergies: Optional[list[str]] = None
):
    """
    Create a new patient record
    
    Args:
        age: Patient age
        gender: Patient gender
        medical_history: List of past medical conditions
        current_medications: List of current medications
        allergies: List of allergies
        
    Returns:
        Created patient record
    """
    try:
        patient_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        record = PatientRecord(
            patient_id=patient_id,
            age=age,
            gender=gender,
            medical_history=medical_history or [],
            current_medications=current_medications or [],
            allergies=allergies or [],
            created_at=now,
            updated_at=now
        )
        
        patient_records[patient_id] = record
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating patient record: {str(e)}")

@router.get("/{patient_id}", response_model=PatientRecord)
async def get_patient(patient_id: str):
    """
    Retrieve patient record by ID
    
    Args:
        patient_id: Patient ID
        
    Returns:
        Patient record
    """
    if patient_id not in patient_records:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return patient_records[patient_id]

@router.put("/{patient_id}", response_model=PatientRecord)
async def update_patient(
    patient_id: str,
    age: Optional[int] = None,
    medical_history: Optional[list[str]] = None,
    current_medications: Optional[list[str]] = None,
    allergies: Optional[list[str]] = None
):
    """
    Update patient record
    
    Args:
        patient_id: Patient ID
        age: Updated age
        medical_history: Updated medical history
        current_medications: Updated medications
        allergies: Updated allergies
        
    Returns:
        Updated patient record
    """
    if patient_id not in patient_records:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    record = patient_records[patient_id]
    
    if age is not None:
        record.age = age
    if medical_history is not None:
        record.medical_history = medical_history
    if current_medications is not None:
        record.current_medications = current_medications
    if allergies is not None:
        record.allergies = allergies
    
    record.updated_at = datetime.utcnow()
    patient_records[patient_id] = record
    
    return record
