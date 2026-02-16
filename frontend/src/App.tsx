/**
 * Main App Component
 */
import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box, AppBar, Toolbar, Typography } from '@mui/material';
import { LocalHospital as HospitalIcon } from '@mui/icons-material';
import DiagnosisPage from './pages/DiagnosisPage';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <HospitalIcon sx={{ mr: 2 }} />
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              UnifySense - Clinical Diagnosis Assistant
            </Typography>
          </Toolbar>
        </AppBar>
        <DiagnosisPage />
      </Box>
    </ThemeProvider>
  );
}

export default App;
