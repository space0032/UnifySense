"""
Medical knowledge and reasoning service
"""
from typing import Dict, List, Any
from app.services.bedrock import bedrock_service
from app.models.schemas import PatientSymptoms, DiagnosisResult, TreatmentRecommendation
from datetime import datetime
import uuid
import json

class MedicalReasoningService:
    """Service for medical reasoning using Amazon Nova"""
    
    async def analyze_symptoms(self, patient_data: PatientSymptoms) -> Dict[str, Any]:
        """
        Analyze patient symptoms using Nova Lite for quick triage
        
        Args:
            patient_data: Patient symptoms and information
            
        Returns:
            Analysis results
        """
        # Build comprehensive prompt
        symptoms_list = "\n".join([
            f"- {s.symptom} (Severity: {s.severity.value}, Duration: {s.duration_days} days)"
            for s in patient_data.symptoms
        ])
        
        prompt = f"""Analyze the following patient symptoms and provide a quick assessment:

Patient Information:
- Age: {patient_data.age}
- Gender: {patient_data.gender}

Symptoms:
{symptoms_list}

Medical History: {', '.join(patient_data.medical_history) if patient_data.medical_history else 'None reported'}
Current Medications: {', '.join(patient_data.current_medications) if patient_data.current_medications else 'None'}
Allergies: {', '.join(patient_data.allergies) if patient_data.allergies else 'None known'}

Provide:
1. A brief summary of the symptoms
2. Overall severity assessment (mild, moderate, severe, critical)
3. Recommended immediate action
4. Triage priority (low, medium, high, emergency)
5. Key insights and concerns

Format the response as JSON with keys: summary, severity_assessment, recommended_action, triage_priority, ai_insights"""

        response = await bedrock_service.invoke_nova_lite(prompt)
        response_text = bedrock_service.extract_text_from_response(response)
        
        # Parse response
        try:
            # Extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                analysis = json.loads(json_str)
            else:
                # Fallback if no JSON found
                analysis = {
                    "summary": response_text[:200],
                    "severity_assessment": "moderate",
                    "recommended_action": "Consult with healthcare provider",
                    "triage_priority": "medium",
                    "ai_insights": response_text
                }
        except json.JSONDecodeError:
            analysis = {
                "summary": response_text[:200],
                "severity_assessment": "moderate",
                "recommended_action": "Consult with healthcare provider",
                "triage_priority": "medium",
                "ai_insights": response_text
            }
        
        analysis["analysis_id"] = str(uuid.uuid4())
        return analysis
    
    async def generate_diagnosis(self, patient_data: PatientSymptoms) -> DiagnosisResult:
        """
        Generate diagnostic suggestions using Nova Pro for deep reasoning
        
        Args:
            patient_data: Patient symptoms and information
            
        Returns:
            Diagnosis results with possible conditions
        """
        symptoms_list = "\n".join([
            f"- {s.symptom} (Severity: {s.severity.value}, Duration: {s.duration_days} days, Notes: {s.additional_notes or 'None'})"
            for s in patient_data.symptoms
        ])
        
        system_prompt = """You are an expert medical AI assistant trained to help healthcare professionals analyze symptoms and suggest possible diagnoses. 
Your role is to:
1. Consider all symptoms comprehensively
2. Factor in patient demographics and history
3. Suggest evidence-based possible conditions
4. Provide confidence levels and reasoning
5. Include relevant ICD-10 codes
6. Always remind that final diagnosis must be made by licensed healthcare professionals

You must provide thorough, evidence-based analysis while acknowledging the limitations of AI in medical diagnosis."""

        prompt = f"""Based on the following patient information, suggest possible diagnoses:

Patient Information:
- Age: {patient_data.age}
- Gender: {patient_data.gender}

Presenting Symptoms:
{symptoms_list}

Medical History: {', '.join(patient_data.medical_history) if patient_data.medical_history else 'None reported'}
Current Medications: {', '.join(patient_data.current_medications) if patient_data.current_medications else 'None'}
Known Allergies: {', '.join(patient_data.allergies) if patient_data.allergies else 'None known'}

Please provide:
1. Top 3-5 possible conditions ranked by likelihood
2. Confidence score for each (0-1)
3. Detailed reasoning for each diagnosis
4. Relevant ICD-10 codes
5. Important differential diagnoses to rule out

Format response as JSON with structure:
{{
    "possible_conditions": [
        {{
            "name": "condition name",
            "confidence": 0.X,
            "reasoning": "explanation",
            "icd10_code": "code"
        }}
    ],
    "overall_confidence": 0.X,
    "clinical_reasoning": "detailed explanation",
    "differential_diagnoses": ["conditions to rule out"]
}}"""

        response = await bedrock_service.invoke_nova_pro(prompt, system_prompt)
        response_text = bedrock_service.extract_text_from_response(response)
        
        # Parse response
        try:
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                diagnosis_data = json.loads(json_str)
            else:
                diagnosis_data = self._create_fallback_diagnosis(response_text)
        except json.JSONDecodeError:
            diagnosis_data = self._create_fallback_diagnosis(response_text)
        
        # Build DiagnosisResult
        icd10_codes = [c.get("icd10_code", "Unknown") for c in diagnosis_data.get("possible_conditions", [])]
        
        return DiagnosisResult(
            diagnosis_id=str(uuid.uuid4()),
            possible_conditions=diagnosis_data.get("possible_conditions", []),
            confidence_score=diagnosis_data.get("overall_confidence", 0.5),
            reasoning=diagnosis_data.get("clinical_reasoning", response_text),
            icd10_codes=icd10_codes,
            created_at=datetime.utcnow()
        )
    
    async def recommend_treatment(self, diagnosis: DiagnosisResult, patient_data: PatientSymptoms) -> TreatmentRecommendation:
        """
        Generate treatment recommendations based on diagnosis
        
        Args:
            diagnosis: Diagnosis results
            patient_data: Patient information
            
        Returns:
            Treatment recommendations
        """
        conditions_text = "\n".join([
            f"- {c['name']} (Confidence: {c.get('confidence', 0)*100:.0f}%)"
            for c in diagnosis.possible_conditions
        ])
        
        system_prompt = """You are an expert medical AI assistant helping healthcare professionals plan diagnostic workup and treatment. 
Provide evidence-based recommendations for tests, treatments, and follow-up care.
Always prioritize patient safety and standard medical protocols."""

        prompt = f"""Based on the following diagnostic assessment, recommend next steps:

Patient Information:
- Age: {patient_data.age}
- Gender: {patient_data.gender}

Possible Diagnoses:
{conditions_text}

Medical History: {', '.join(patient_data.medical_history) if patient_data.medical_history else 'None'}
Current Medications: {', '.join(patient_data.current_medications) if patient_data.current_medications else 'None'}
Allergies: {', '.join(patient_data.allergies) if patient_data.allergies else 'None'}

Provide:
1. Recommended diagnostic tests to confirm diagnosis
2. Suggested treatment options
3. Urgency level (routine, urgent, emergency)
4. Follow-up requirements
5. Important precautions and contraindications

Format as JSON:
{{
    "recommended_tests": ["test1", "test2"],
    "recommended_treatments": ["treatment1", "treatment2"],
    "urgency_level": "level",
    "follow_up_required": true/false,
    "precautions": ["precaution1", "precaution2"],
    "detailed_reasoning": "explanation"
}}"""

        response = await bedrock_service.invoke_nova_pro(prompt, system_prompt)
        response_text = bedrock_service.extract_text_from_response(response)
        
        # Parse response
        try:
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                treatment_data = json.loads(json_str)
            else:
                treatment_data = self._create_fallback_treatment(response_text)
        except json.JSONDecodeError:
            treatment_data = self._create_fallback_treatment(response_text)
        
        return TreatmentRecommendation(
            recommended_tests=treatment_data.get("recommended_tests", []),
            recommended_treatments=treatment_data.get("recommended_treatments", []),
            urgency_level=treatment_data.get("urgency_level", "routine"),
            follow_up_required=treatment_data.get("follow_up_required", True),
            precautions=treatment_data.get("precautions", []),
            reasoning=treatment_data.get("detailed_reasoning", response_text)
        )
    
    def _create_fallback_diagnosis(self, text: str) -> Dict[str, Any]:
        """Create fallback diagnosis structure"""
        return {
            "possible_conditions": [
                {
                    "name": "Further evaluation required",
                    "confidence": 0.5,
                    "reasoning": text[:500],
                    "icd10_code": "R69"
                }
            ],
            "overall_confidence": 0.5,
            "clinical_reasoning": text,
            "differential_diagnoses": []
        }
    
    def _create_fallback_treatment(self, text: str) -> Dict[str, Any]:
        """Create fallback treatment structure"""
        return {
            "recommended_tests": ["Complete physical examination"],
            "recommended_treatments": ["Consult with specialist"],
            "urgency_level": "routine",
            "follow_up_required": True,
            "precautions": ["Monitor symptoms"],
            "detailed_reasoning": text
        }

# Global instance
medical_service = MedicalReasoningService()
