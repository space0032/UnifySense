"""
Example usage of the UnifySense API
"""
import requests
import json

# API Base URL
BASE_URL = "http://localhost:8000"

def example_symptom_analysis():
    """Example: Analyze patient symptoms"""
    
    patient_data = {
        "age": 45,
        "gender": "male",
        "symptoms": [
            {
                "symptom": "Persistent headache",
                "severity": "moderate",
                "duration_days": 7,
                "additional_notes": "Worse in the morning, improves throughout the day"
            },
            {
                "symptom": "Fatigue",
                "severity": "mild",
                "duration_days": 10,
                "additional_notes": "Constant tiredness"
            }
        ],
        "medical_history": ["Hypertension", "Type 2 Diabetes"],
        "current_medications": ["Lisinopril 10mg", "Metformin 500mg"],
        "allergies": ["Penicillin"]
    }
    
    # Analyze symptoms
    print("Analyzing symptoms...")
    response = requests.post(f"{BASE_URL}/api/symptoms/analyze", json=patient_data)
    analysis = response.json()
    
    print("\n=== SYMPTOM ANALYSIS ===")
    print(f"Analysis ID: {analysis['analysis_id']}")
    print(f"Summary: {analysis['summary']}")
    print(f"Severity: {analysis['severity_assessment']}")
    print(f"Triage Priority: {analysis['triage_priority']}")
    print(f"Recommended Action: {analysis['recommended_action']}")
    
    return analysis

def example_diagnosis_generation():
    """Example: Generate diagnosis"""
    
    patient_data = {
        "age": 35,
        "gender": "female",
        "symptoms": [
            {
                "symptom": "Sharp chest pain",
                "severity": "severe",
                "duration_days": 1,
                "additional_notes": "Pain increases with deep breathing"
            },
            {
                "symptom": "Shortness of breath",
                "severity": "moderate",
                "duration_days": 1
            }
        ],
        "medical_history": [],
        "current_medications": [],
        "allergies": []
    }
    
    # Generate diagnosis
    print("\n\nGenerating diagnosis...")
    response = requests.post(f"{BASE_URL}/api/diagnosis/generate", json=patient_data)
    diagnosis = response.json()
    
    print("\n=== DIAGNOSIS RESULTS ===")
    print(f"Diagnosis ID: {diagnosis['diagnosis_id']}")
    print(f"Overall Confidence: {diagnosis['confidence_score']:.2%}")
    print(f"\nPossible Conditions:")
    for i, condition in enumerate(diagnosis['possible_conditions'], 1):
        print(f"\n{i}. {condition['name']}")
        print(f"   Confidence: {condition.get('confidence', 0):.2%}")
        print(f"   ICD-10: {condition.get('icd10_code', 'N/A')}")
        print(f"   Reasoning: {condition.get('reasoning', 'N/A')[:100]}...")
    
    print(f"\nClinical Reasoning: {diagnosis['reasoning'][:200]}...")
    
    return diagnosis

def example_treatment_recommendation():
    """Example: Get treatment recommendations"""
    
    patient_data = {
        "age": 60,
        "gender": "male",
        "symptoms": [
            {
                "symptom": "Joint pain",
                "severity": "moderate",
                "duration_days": 30,
                "additional_notes": "Mainly in knees and hands"
            }
        ],
        "medical_history": ["Osteoarthritis"],
        "current_medications": ["Ibuprofen PRN"],
        "allergies": []
    }
    
    # First generate diagnosis
    diagnosis_response = requests.post(f"{BASE_URL}/api/diagnosis/generate", json=patient_data)
    diagnosis = diagnosis_response.json()
    
    # Get treatment recommendations
    print("\n\nGetting treatment recommendations...")
    treatment_request = {
        "patient_data": patient_data,
        "diagnosis": diagnosis
    }
    
    response = requests.post(f"{BASE_URL}/api/treatment/recommend", json=treatment_request)
    treatment = response.json()
    
    print("\n=== TREATMENT RECOMMENDATIONS ===")
    print(f"Urgency Level: {treatment['urgency_level']}")
    print(f"Follow-up Required: {treatment['follow_up_required']}")
    
    print(f"\nRecommended Tests:")
    for test in treatment['recommended_tests']:
        print(f"  - {test}")
    
    print(f"\nRecommended Treatments:")
    for tx in treatment['recommended_treatments']:
        print(f"  - {tx}")
    
    print(f"\nPrecautions:")
    for precaution in treatment['precautions']:
        print(f"  - {precaution}")
    
    print(f"\nReasoning: {treatment['reasoning'][:200]}...")
    
    return treatment

def check_health():
    """Check API health"""
    response = requests.get(f"{BASE_URL}/health")
    health = response.json()
    print("=== HEALTH CHECK ===")
    print(json.dumps(health, indent=2))
    return health

if __name__ == "__main__":
    # Check if API is running
    try:
        check_health()
        
        # Run examples
        # Note: These will fail if AWS Bedrock is not properly configured
        # Uncomment to run when AWS credentials are set up
        
        # example_symptom_analysis()
        # example_diagnosis_generation()
        # example_treatment_recommendation()
        
        print("\n\nTo run the full examples, ensure:")
        print("1. Backend server is running (uvicorn main:app --reload)")
        print("2. AWS Bedrock credentials are configured")
        print("3. Amazon Nova models are accessible")
        print("4. Uncomment the example function calls above")
        
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API. Make sure the backend server is running.")
        print("Start the server with: uvicorn main:app --reload")
