/**
 * Main Diagnosis Page Component
 */
import React, { useState } from 'react';
import {
  Container,
  Box,
  Typography,
  Paper,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Stepper,
  Step,
  StepLabel,
  Alert,
  CircularProgress,
  Chip,
  Divider,
  Grid,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';
import {
  Science as ScienceIcon,
  LocalHospital as HospitalIcon,
  Assessment as AssessmentIcon,
} from '@mui/icons-material';
import SymptomForm from '../components/SymptomForm';
import { api, PatientSymptoms, SymptomInput, AnalysisResponse, DiagnosisResult, TreatmentRecommendation } from '../services/api';

const steps = ['Patient Information', 'Symptoms', 'Analysis', 'Results'];

const DiagnosisPage: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Patient data
  const [age, setAge] = useState<number>(30);
  const [gender, setGender] = useState<'male' | 'female' | 'other'>('male');
  const [symptoms, setSymptoms] = useState<SymptomInput[]>([]);
  const [medicalHistory, setMedicalHistory] = useState<string>('');
  const [medications, setMedications] = useState<string>('');
  const [allergies, setAllergies] = useState<string>('');

  // Results
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null);
  const [diagnosis, setDiagnosis] = useState<DiagnosisResult | null>(null);
  const [treatment, setTreatment] = useState<TreatmentRecommendation | null>(null);

  const handleNext = async () => {
    if (activeStep === steps.length - 2) {
      // Perform analysis
      await performAnalysis();
    }
    setActiveStep((prev) => prev + 1);
  };

  const handleBack = () => {
    setActiveStep((prev) => prev - 1);
  };

  const handleReset = () => {
    setActiveStep(0);
    setSymptoms([]);
    setAnalysis(null);
    setDiagnosis(null);
    setTreatment(null);
    setError(null);
  };

  const performAnalysis = async () => {
    setLoading(true);
    setError(null);

    try {
      const patientData: PatientSymptoms = {
        age,
        gender,
        symptoms,
        medical_history: medicalHistory ? medicalHistory.split(',').map(s => s.trim()) : [],
        current_medications: medications ? medications.split(',').map(s => s.trim()) : [],
        allergies: allergies ? allergies.split(',').map(s => s.trim()) : [],
      };

      // Step 1: Analyze symptoms
      const analysisResult = await api.analyzeSymptoms(patientData);
      setAnalysis(analysisResult);

      // Step 2: Generate diagnosis
      const diagnosisResult = await api.generateDiagnosis(patientData);
      setDiagnosis(diagnosisResult);

      // Step 3: Get treatment recommendations
      const treatmentResult = await api.recommendTreatment(patientData, diagnosisResult);
      setTreatment(treatmentResult);

    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'An error occurred during analysis');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const canProceed = () => {
    switch (activeStep) {
      case 0:
        return age > 0 && gender;
      case 1:
        return symptoms.length > 0 && symptoms.every(s => s.symptom && s.duration_days >= 0);
      default:
        return true;
    }
  };

  const renderStepContent = () => {
    switch (activeStep) {
      case 0:
        return (
          <Box>
            <Typography variant="h5" gutterBottom>
              Patient Information
            </Typography>
            <Grid container spacing={3} sx={{ mt: 1 }}>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  type="number"
                  label="Age"
                  value={age}
                  onChange={(e) => setAge(parseInt(e.target.value))}
                  inputProps={{ min: 0, max: 150 }}
                  required
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth required>
                  <InputLabel>Gender</InputLabel>
                  <Select value={gender} label="Gender" onChange={(e) => setGender(e.target.value as any)}>
                    <MenuItem value="male">Male</MenuItem>
                    <MenuItem value="female">Female</MenuItem>
                    <MenuItem value="other">Other</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Medical History (comma-separated)"
                  value={medicalHistory}
                  onChange={(e) => setMedicalHistory(e.target.value)}
                  multiline
                  rows={2}
                  placeholder="e.g., Diabetes, Hypertension"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Current Medications (comma-separated)"
                  value={medications}
                  onChange={(e) => setMedications(e.target.value)}
                  multiline
                  rows={2}
                  placeholder="e.g., Metformin, Lisinopril"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Known Allergies (comma-separated)"
                  value={allergies}
                  onChange={(e) => setAllergies(e.target.value)}
                  multiline
                  rows={2}
                  placeholder="e.g., Penicillin, Peanuts"
                />
              </Grid>
            </Grid>
          </Box>
        );

      case 1:
        return (
          <Box>
            <Typography variant="h5" gutterBottom>
              Symptom Entry
            </Typography>
            <Box sx={{ mt: 2 }}>
              <SymptomForm symptoms={symptoms} onChange={setSymptoms} />
            </Box>
          </Box>
        );

      case 2:
        return (
          <Box textAlign="center" py={4}>
            {loading ? (
              <>
                <CircularProgress size={60} />
                <Typography variant="h6" sx={{ mt: 2 }}>
                  Analyzing symptoms with Amazon Nova AI...
                </Typography>
                <Typography color="text.secondary" sx={{ mt: 1 }}>
                  This may take a few moments
                </Typography>
              </>
            ) : (
              <>
                <AssessmentIcon sx={{ fontSize: 80, color: 'primary.main' }} />
                <Typography variant="h6" sx={{ mt: 2 }}>
                  Ready to analyze
                </Typography>
                <Typography color="text.secondary">
                  Click "Analyze" to begin AI-powered diagnostic assessment
                </Typography>
              </>
            )}
          </Box>
        );

      case 3:
        return (
          <Box>
            <Typography variant="h5" gutterBottom>
              Diagnostic Results
            </Typography>

            {error && (
              <Alert severity="error" sx={{ mb: 3 }}>
                {error}
              </Alert>
            )}

            {analysis && (
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Box display="flex" alignItems="center" mb={2}>
                    <AssessmentIcon sx={{ mr: 1, color: 'primary.main' }} />
                    <Typography variant="h6">Symptom Analysis</Typography>
                  </Box>
                  <Typography variant="body1" paragraph>
                    <strong>Summary:</strong> {analysis.summary}
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2">
                        <strong>Severity:</strong>{' '}
                        <Chip
                          label={analysis.severity_assessment}
                          color={
                            analysis.severity_assessment === 'critical'
                              ? 'error'
                              : analysis.severity_assessment === 'severe'
                              ? 'warning'
                              : 'info'
                          }
                          size="small"
                        />
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2">
                        <strong>Triage Priority:</strong>{' '}
                        <Chip label={analysis.triage_priority} color="primary" size="small" />
                      </Typography>
                    </Grid>
                  </Grid>
                  <Typography variant="body2" sx={{ mt: 2 }}>
                    <strong>Recommended Action:</strong> {analysis.recommended_action}
                  </Typography>
                </CardContent>
              </Card>
            )}

            {diagnosis && (
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Box display="flex" alignItems="center" mb={2}>
                    <ScienceIcon sx={{ mr: 1, color: 'secondary.main' }} />
                    <Typography variant="h6">Possible Diagnoses</Typography>
                  </Box>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Overall Confidence: {(diagnosis.confidence_score * 100).toFixed(0)}%
                  </Typography>
                  <List>
                    {diagnosis.possible_conditions.map((condition: any, index: number) => (
                      <ListItem key={index} divider>
                        <ListItemText
                          primary={
                            <Box display="flex" alignItems="center" justifyContent="space-between">
                              <Typography variant="subtitle1">{condition.name}</Typography>
                              <Chip
                                label={`${(condition.confidence * 100).toFixed(0)}% confidence`}
                                size="small"
                                color="primary"
                              />
                            </Box>
                          }
                          secondary={
                            <>
                              <Typography variant="body2" component="span">
                                {condition.reasoning}
                              </Typography>
                              {condition.icd10_code && (
                                <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                                  ICD-10: {condition.icd10_code}
                                </Typography>
                              )}
                            </>
                          }
                        />
                      </ListItem>
                    ))}
                  </List>
                  <Divider sx={{ my: 2 }} />
                  <Typography variant="body2">
                    <strong>Clinical Reasoning:</strong> {diagnosis.reasoning}
                  </Typography>
                </CardContent>
              </Card>
            )}

            {treatment && (
              <Card>
                <CardContent>
                  <Box display="flex" alignItems="center" mb={2}>
                    <HospitalIcon sx={{ mr: 1, color: 'success.main' }} />
                    <Typography variant="h6">Treatment Recommendations</Typography>
                  </Box>
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" gutterBottom>
                        Recommended Tests:
                      </Typography>
                      <List dense>
                        {treatment.recommended_tests.map((test, index) => (
                          <ListItem key={index}>
                            <ListItemText primary={test} />
                          </ListItem>
                        ))}
                      </List>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" gutterBottom>
                        Treatment Options:
                      </Typography>
                      <List dense>
                        {treatment.recommended_treatments.map((tx, index) => (
                          <ListItem key={index}>
                            <ListItemText primary={tx} />
                          </ListItem>
                        ))}
                      </List>
                    </Grid>
                    <Grid item xs={12}>
                      <Typography variant="subtitle2" gutterBottom>
                        Precautions:
                      </Typography>
                      <List dense>
                        {treatment.precautions.map((precaution, index) => (
                          <ListItem key={index}>
                            <ListItemText primary={precaution} />
                          </ListItem>
                        ))}
                      </List>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2">
                        <strong>Urgency:</strong>{' '}
                        <Chip
                          label={treatment.urgency_level}
                          color={treatment.urgency_level === 'emergency' ? 'error' : 'warning'}
                          size="small"
                        />
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2">
                        <strong>Follow-up Required:</strong>{' '}
                        {treatment.follow_up_required ? 'Yes' : 'No'}
                      </Typography>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            )}

            {!error && !analysis && (
              <Alert severity="info">
                Click "Analyze" on the previous step to generate results
              </Alert>
            )}

            <Alert severity="warning" sx={{ mt: 3 }}>
              <strong>Medical Disclaimer:</strong> These AI-generated suggestions are for
              informational purposes only and should be reviewed by qualified healthcare
              professionals. This tool does not replace professional medical judgment.
            </Alert>
          </Box>
        );

      default:
        return null;
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom align="center">
          Clinical Diagnosis Assistant
        </Typography>
        <Typography variant="subtitle1" align="center" color="text.secondary" gutterBottom>
          Powered by Amazon Nova AI
        </Typography>

        <Stepper activeStep={activeStep} sx={{ my: 4 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        <Box sx={{ minHeight: 400 }}>
          {renderStepContent()}
        </Box>

        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
          <Button
            disabled={activeStep === 0}
            onClick={handleBack}
          >
            Back
          </Button>
          <Box>
            {activeStep === steps.length - 1 ? (
              <Button variant="contained" onClick={handleReset}>
                New Analysis
              </Button>
            ) : (
              <Button
                variant="contained"
                onClick={handleNext}
                disabled={!canProceed() || loading}
              >
                {activeStep === steps.length - 2 ? 'Analyze' : 'Next'}
              </Button>
            )}
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default DiagnosisPage;
