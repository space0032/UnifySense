# API Documentation

## UnifySense Clinical Diagnosis Assistant API

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Health Check

**GET /** 
- Returns basic health status

**GET /health**
- Returns detailed health status including AWS Bedrock connection

#### Symptom Analysis

**POST /api/symptoms/analyze**

Analyze patient symptoms and provide quick triage assessment.

Request Body:
```json
{
  "age": 45,
  "gender": "male",
  "symptoms": [
    {
      "symptom": "Persistent headache",
      "severity": "moderate",
      "duration_days": 7,
      "additional_notes": "Worse in the morning"
    }
  ],
  "medical_history": ["Hypertension"],
  "current_medications": ["Lisinopril"],
  "allergies": []
}
```

Response:
```json
{
  "analysis_id": "uuid",
  "summary": "Patient presents with persistent headache...",
  "severity_assessment": "moderate",
  "recommended_action": "Schedule appointment with primary care physician",
  "triage_priority": "medium",
  "ai_insights": "Detailed AI analysis..."
}
```

#### Diagnosis Generation

**POST /api/diagnosis/generate**

Generate diagnostic suggestions using Amazon Nova Pro.

Request Body: Same as symptom analysis

Response:
```json
{
  "diagnosis_id": "uuid",
  "possible_conditions": [
    {
      "name": "Tension Headache",
      "confidence": 0.75,
      "reasoning": "Symptoms consistent with...",
      "icd10_code": "G44.2"
    }
  ],
  "confidence_score": 0.75,
  "reasoning": "Comprehensive clinical reasoning...",
  "icd10_codes": ["G44.2"],
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Treatment Recommendations

**POST /api/treatment/recommend**

Get treatment recommendations based on diagnosis.

Request Body:
```json
{
  "patient_data": { /* PatientSymptoms object */ },
  "diagnosis": { /* DiagnosisResult object */ }
}
```

Response:
```json
{
  "recommended_tests": [
    "Complete blood count",
    "Blood pressure monitoring"
  ],
  "recommended_treatments": [
    "Stress management techniques",
    "Over-the-counter pain relief"
  ],
  "urgency_level": "routine",
  "follow_up_required": true,
  "precautions": [
    "Monitor blood pressure regularly",
    "Avoid triggers"
  ],
  "reasoning": "Based on diagnosis..."
}
```

#### Patient Records

**POST /api/patient/**
- Create new patient record

**GET /api/patient/{patient_id}**
- Retrieve patient record

**PUT /api/patient/{patient_id}**
- Update patient record

### Error Responses

All endpoints may return error responses in the format:
```json
{
  "detail": "Error message"
}
```

Common status codes:
- 200: Success
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

### Authentication

Currently, the API does not require authentication. In production, implement proper authentication and authorization mechanisms.

### Rate Limiting

No rate limiting is currently implemented. Consider adding rate limiting for production use.
