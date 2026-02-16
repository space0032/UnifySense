/**
 * API service for UnifySense backend
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface SymptomInput {
  symptom: string;
  severity: 'mild' | 'moderate' | 'severe' | 'critical';
  duration_days: number;
  additional_notes?: string;
}

export interface PatientSymptoms {
  patient_id?: string;
  age: number;
  gender: 'male' | 'female' | 'other';
  symptoms: SymptomInput[];
  medical_history?: string[];
  current_medications?: string[];
  allergies?: string[];
}

export interface AnalysisResponse {
  analysis_id: string;
  summary: string;
  severity_assessment: string;
  recommended_action: string;
  triage_priority: string;
  ai_insights: string;
}

export interface DiagnosisResult {
  diagnosis_id: string;
  possible_conditions: any[];
  confidence_score: number;
  reasoning: string;
  icd10_codes: string[];
  created_at: string;
}

export interface TreatmentRecommendation {
  recommended_tests: string[];
  recommended_treatments: string[];
  urgency_level: string;
  follow_up_required: boolean;
  precautions: string[];
  reasoning: string;
}

export const api = {
  // Symptom analysis
  analyzeSymptoms: async (data: PatientSymptoms): Promise<AnalysisResponse> => {
    const response = await apiClient.post('/api/symptoms/analyze', data);
    return response.data;
  },

  // Diagnosis generation
  generateDiagnosis: async (data: PatientSymptoms): Promise<DiagnosisResult> => {
    const response = await apiClient.post('/api/diagnosis/generate', data);
    return response.data;
  },

  // Treatment recommendations
  recommendTreatment: async (
    patient_data: PatientSymptoms,
    diagnosis: DiagnosisResult
  ): Promise<TreatmentRecommendation> => {
    const response = await apiClient.post('/api/treatment/recommend', {
      patient_data,
      diagnosis,
    });
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },
};

export default api;
