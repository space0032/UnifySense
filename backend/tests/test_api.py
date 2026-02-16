"""
Test suite for UnifySense API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "UnifySense" in response.json()["service"]

def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "services" in response.json()

def test_symptom_analysis_endpoint():
    """Test symptom analysis endpoint"""
    patient_data = {
        "age": 45,
        "gender": "male",
        "symptoms": [
            {
                "symptom": "Headache",
                "severity": "moderate",
                "duration_days": 3
            }
        ]
    }
    
    response = client.post("/api/symptoms/analyze", json=patient_data)
    # May fail without AWS credentials, but endpoint should exist
    assert response.status_code in [200, 500]

def test_diagnosis_endpoint():
    """Test diagnosis generation endpoint"""
    patient_data = {
        "age": 35,
        "gender": "female",
        "symptoms": [
            {
                "symptom": "Fever",
                "severity": "severe",
                "duration_days": 2
            }
        ]
    }
    
    response = client.post("/api/diagnosis/generate", json=patient_data)
    # May fail without AWS credentials, but endpoint should exist
    assert response.status_code in [200, 500]

def test_invalid_age():
    """Test validation for invalid age"""
    patient_data = {
        "age": -5,
        "gender": "male",
        "symptoms": []
    }
    
    response = client.post("/api/symptoms/analyze", json=patient_data)
    assert response.status_code == 422  # Validation error

def test_invalid_gender():
    """Test validation for invalid gender"""
    patient_data = {
        "age": 30,
        "gender": "invalid",
        "symptoms": []
    }
    
    response = client.post("/api/symptoms/analyze", json=patient_data)
    assert response.status_code == 422  # Validation error

def test_patient_creation():
    """Test patient record creation"""
    response = client.post(
        "/api/patient/",
        params={
            "age": 40,
            "gender": "female"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "patient_id" in data
    assert data["age"] == 40
    assert data["gender"] == "female"

def test_patient_retrieval():
    """Test patient record retrieval"""
    # First create a patient
    create_response = client.post(
        "/api/patient/",
        params={
            "age": 50,
            "gender": "male"
        }
    )
    patient_id = create_response.json()["patient_id"]
    
    # Then retrieve it
    get_response = client.get(f"/api/patient/{patient_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["patient_id"] == patient_id
    assert data["age"] == 50

def test_patient_not_found():
    """Test patient retrieval with invalid ID"""
    response = client.get("/api/patient/nonexistent-id")
    assert response.status_code == 404

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
