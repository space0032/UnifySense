#!/bin/bash

# UnifySense Demo Script
# This script demonstrates the UnifySense Clinical Diagnosis Assistant

echo "======================================"
echo "UnifySense Clinical Diagnosis Assistant"
echo "Amazon Nova-Powered Medical AI"
echo "======================================"
echo ""

# Check if backend is running
echo "🔍 Checking backend server..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend server is running"
else
    echo "❌ Backend server is not running"
    echo "   Start it with: cd backend && uvicorn main:app --reload"
    exit 1
fi

echo ""
echo "🏥 Running demonstration scenarios..."
echo ""

# Scenario 1: Emergency Case
echo "📋 Scenario 1: Emergency - Chest Pain"
echo "   Patient: 65-year-old male"
echo "   Symptoms: Severe chest pain, shortness of breath"
echo ""

curl -X POST "http://localhost:8000/api/symptoms/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 65,
    "gender": "male",
    "symptoms": [
      {
        "symptom": "Severe crushing chest pain",
        "severity": "critical",
        "duration_days": 0,
        "additional_notes": "Started 30 minutes ago"
      },
      {
        "symptom": "Shortness of breath",
        "severity": "severe",
        "duration_days": 0
      }
    ],
    "medical_history": ["Hypertension", "High cholesterol"],
    "current_medications": ["Atorvastatin", "Lisinopril"]
  }' 2>/dev/null | python3 -m json.tool

echo ""
echo "---"
echo ""

# Scenario 2: Routine Care
echo "📋 Scenario 2: Routine - Headache"
echo "   Patient: 35-year-old female"
echo "   Symptoms: Mild headache for 3 days"
echo ""

curl -X POST "http://localhost:8000/api/symptoms/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "gender": "female",
    "symptoms": [
      {
        "symptom": "Headache",
        "severity": "mild",
        "duration_days": 3,
        "additional_notes": "Improves with rest"
      }
    ],
    "medical_history": [],
    "current_medications": []
  }' 2>/dev/null | python3 -m json.tool

echo ""
echo "---"
echo ""

# Create a patient record
echo "📋 Creating patient record..."
PATIENT_ID=$(curl -X POST "http://localhost:8000/api/patient/?age=45&gender=male" \
  -H "Content-Type: application/json" \
  2>/dev/null | python3 -c "import sys, json; print(json.load(sys.stdin)['patient_id'])")

echo "✅ Created patient record: $PATIENT_ID"
echo ""

# Retrieve patient record
echo "📋 Retrieving patient record..."
curl -X GET "http://localhost:8000/api/patient/$PATIENT_ID" \
  2>/dev/null | python3 -m json.tool

echo ""
echo "======================================"
echo "Demo Complete!"
echo "======================================"
echo ""
echo "Next Steps:"
echo "1. Open http://localhost:3000 to use the web interface"
echo "2. Try entering different symptoms and see AI analysis"
echo "3. Review the documentation in README.md"
echo "4. Explore examples in examples/USE_CASES.md"
echo ""
echo "Note: Full AI analysis requires AWS Bedrock credentials"
echo "      configured in backend/.env"
