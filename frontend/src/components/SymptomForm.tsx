/**
 * Symptom Input Component
 */
import React, { useState } from 'react';
import {
  Box,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  IconButton,
  Paper,
  Typography,
  Grid,
} from '@mui/material';
import { Delete as DeleteIcon, Add as AddIcon } from '@mui/icons-material';
import { SymptomInput } from '../services/api';

interface SymptomFormProps {
  symptoms: SymptomInput[];
  onChange: (symptoms: SymptomInput[]) => void;
}

const SymptomForm: React.FC<SymptomFormProps> = ({ symptoms, onChange }) => {
  const addSymptom = () => {
    onChange([
      ...symptoms,
      {
        symptom: '',
        severity: 'mild',
        duration_days: 1,
        additional_notes: '',
      },
    ]);
  };

  const removeSymptom = (index: number) => {
    onChange(symptoms.filter((_, i) => i !== index));
  };

  const updateSymptom = (index: number, field: keyof SymptomInput, value: any) => {
    const updated = [...symptoms];
    updated[index] = { ...updated[index], [field]: value };
    onChange(updated);
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">Symptoms</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={addSymptom}
        >
          Add Symptom
        </Button>
      </Box>

      {symptoms.map((symptom, index) => (
        <Paper key={index} elevation={2} sx={{ p: 2, mb: 2 }}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Symptom Description"
                value={symptom.symptom}
                onChange={(e) => updateSymptom(index, 'symptom', e.target.value)}
                required
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth required>
                <InputLabel>Severity</InputLabel>
                <Select
                  value={symptom.severity}
                  label="Severity"
                  onChange={(e) => updateSymptom(index, 'severity', e.target.value)}
                >
                  <MenuItem value="mild">Mild</MenuItem>
                  <MenuItem value="moderate">Moderate</MenuItem>
                  <MenuItem value="severe">Severe</MenuItem>
                  <MenuItem value="critical">Critical</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={2}>
              <TextField
                fullWidth
                type="number"
                label="Duration (days)"
                value={symptom.duration_days}
                onChange={(e) =>
                  updateSymptom(index, 'duration_days', parseInt(e.target.value))
                }
                inputProps={{ min: 0 }}
                required
              />
            </Grid>
            <Grid item xs={12} md={1}>
              <IconButton
                color="error"
                onClick={() => removeSymptom(index)}
                sx={{ mt: 1 }}
              >
                <DeleteIcon />
              </IconButton>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Additional Notes"
                value={symptom.additional_notes || ''}
                onChange={(e) => updateSymptom(index, 'additional_notes', e.target.value)}
                multiline
                rows={2}
              />
            </Grid>
          </Grid>
        </Paper>
      ))}

      {symptoms.length === 0 && (
        <Box textAlign="center" py={4}>
          <Typography color="text.secondary">
            No symptoms added yet. Click "Add Symptom" to begin.
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default SymptomForm;
