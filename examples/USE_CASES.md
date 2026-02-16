# Example Use Cases

## UnifySense Clinical Diagnosis Assistant - Real-World Scenarios

### Use Case 1: Primary Care Triage

**Scenario**: A patient calls a clinic with symptoms. The medical assistant uses UnifySense to perform initial triage.

**Input**:
- Age: 42
- Gender: Female
- Symptoms:
  - Fever (102°F) - Severe - 2 days
  - Dry cough - Moderate - 4 days
  - Body aches - Mild - 3 days
- Medical History: Asthma
- Current Medications: Albuterol inhaler

**Expected Output**:
- Triage Priority: High
- Severity: Moderate-Severe
- Possible Diagnoses: Influenza, COVID-19, Respiratory infection
- Recommended Action: Schedule urgent appointment within 24 hours
- Recommended Tests: COVID-19 test, Influenza rapid test, Chest X-ray if symptoms worsen

---

### Use Case 2: Emergency Department Pre-Assessment

**Scenario**: ER staff use UnifySense for quick pre-assessment before physician evaluation.

**Input**:
- Age: 65
- Gender: Male
- Symptoms:
  - Crushing chest pain - Critical - 30 minutes
  - Shortness of breath - Severe - 30 minutes
  - Sweating - Moderate - 30 minutes
- Medical History: Hypertension, High cholesterol
- Current Medications: Atorvastatin, Amlodipine

**Expected Output**:
- Triage Priority: EMERGENCY
- Severity: Critical
- Possible Diagnoses: Acute Myocardial Infarction (Heart Attack), Unstable Angina
- Recommended Action: IMMEDIATE medical attention, activate cardiac team
- Recommended Tests: ECG, Cardiac enzymes (Troponin), Chest X-ray

---

### Use Case 3: Chronic Condition Management

**Scenario**: Follow-up visit for chronic condition monitoring.

**Input**:
- Age: 58
- Gender: Female
- Symptoms:
  - Increased thirst - Moderate - 14 days
  - Frequent urination - Moderate - 14 days
  - Fatigue - Mild - 21 days
- Medical History: Type 2 Diabetes, Obesity
- Current Medications: Metformin 1000mg BID

**Expected Output**:
- Triage Priority: Medium
- Severity: Moderate
- Possible Diagnoses: Uncontrolled Diabetes, Medication adjustment needed
- Recommended Action: Schedule appointment with endocrinologist
- Recommended Tests: HbA1c, Fasting glucose, Comprehensive metabolic panel

---

### Use Case 4: Pediatric Assessment

**Scenario**: Parent brings child to clinic with concerning symptoms.

**Input**:
- Age: 8
- Gender: Male
- Symptoms:
  - Sore throat - Severe - 2 days
  - Fever (101°F) - Moderate - 2 days
  - Difficulty swallowing - Moderate - 2 days
  - Rash - Mild - 1 day
- Medical History: None
- Allergies: Penicillin

**Expected Output**:
- Triage Priority: High
- Severity: Moderate
- Possible Diagnoses: Streptococcal pharyngitis, Viral pharyngitis, Scarlet fever
- Recommended Action: Same-day appointment
- Recommended Tests: Rapid strep test, Throat culture
- Precautions: Note penicillin allergy - use alternative antibiotics if needed

---

### Use Case 5: Telemedicine Consultation

**Scenario**: Remote patient consultation via telehealth platform.

**Input**:
- Age: 35
- Gender: Female
- Symptoms:
  - Migraine headache - Severe - 1 day
  - Nausea - Moderate - 1 day
  - Sensitivity to light - Moderate - 1 day
- Medical History: Migraine disorder
- Current Medications: Sumatriptan PRN

**Expected Output**:
- Triage Priority: Medium
- Severity: Moderate
- Possible Diagnoses: Acute migraine episode, Tension headache
- Recommended Treatment: Sumatriptan dose, rest in dark room, hydration
- Follow-up: If no improvement in 24 hours, consider ER visit

---

### Use Case 6: Occupational Health Screening

**Scenario**: Employee reports work-related symptoms to occupational health.

**Input**:
- Age: 45
- Gender: Male
- Symptoms:
  - Lower back pain - Moderate - 7 days
  - Limited range of motion - Moderate - 7 days
  - Muscle spasms - Mild - 5 days
- Medical History: Previous back injury (2 years ago)
- Occupation: Warehouse worker (heavy lifting)

**Expected Output**:
- Triage Priority: Medium
- Severity: Moderate
- Possible Diagnoses: Musculoskeletal strain, Herniated disc, Sciatica
- Recommended Action: Physical therapy evaluation, ergonomic assessment
- Recommended Tests: X-ray of lumbar spine, MRI if symptoms persist
- Work Restrictions: Modified duty - avoid heavy lifting temporarily

---

## Integration Examples

### Example 1: Integration with EHR System

```python
# Pseudocode for EHR integration
patient = ehr_system.get_patient(patient_id)
symptoms = patient.get_current_symptoms()

# Send to UnifySense
analysis = unifysense.analyze(
    age=patient.age,
    gender=patient.gender,
    symptoms=symptoms,
    medical_history=patient.medical_history,
    medications=patient.current_medications
)

# Store results in EHR
ehr_system.add_assessment(
    patient_id=patient_id,
    assessment=analysis,
    provider="UnifySense AI Assistant"
)
```

### Example 2: Integration with Appointment Scheduling

```python
# Pseudocode for scheduling integration
analysis = unifysense.analyze(patient_data)

if analysis.triage_priority == "emergency":
    alert_service.send_emergency_alert(patient_data)
elif analysis.triage_priority == "high":
    scheduling.book_urgent_appointment(patient_id, within_hours=24)
elif analysis.triage_priority == "medium":
    scheduling.suggest_appointment(patient_id, within_days=3)
```

### Example 3: Integration with Lab Systems

```python
# Pseudocode for lab order integration
diagnosis = unifysense.generate_diagnosis(patient_data)
treatment = unifysense.recommend_treatment(patient_data, diagnosis)

# Auto-create lab orders
for test in treatment.recommended_tests:
    lab_system.create_order(
        patient_id=patient_id,
        test_name=test,
        priority=treatment.urgency_level,
        requesting_provider=current_provider
    )
```

---

## Performance Metrics

Expected system performance:
- **Symptom Analysis**: 2-5 seconds
- **Diagnosis Generation**: 5-15 seconds (using Nova Pro)
- **Treatment Recommendations**: 5-10 seconds
- **Total Workflow**: Under 30 seconds

---

## Medical Disclaimer

All examples are for demonstration purposes. UnifySense is designed to assist healthcare professionals and should not replace clinical judgment. All AI-generated suggestions must be reviewed and validated by qualified healthcare providers.
