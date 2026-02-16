"""
Main FastAPI application for UnifySense Clinical Diagnosis Assistant
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import symptoms, diagnosis, patient, treatment

app = FastAPI(
    title="UnifySense Clinical Diagnosis Assistant",
    description="AI-powered diagnostic assistance using Amazon Nova",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(symptoms.router, prefix="/api/symptoms", tags=["symptoms"])
app.include_router(diagnosis.router, prefix="/api/diagnosis", tags=["diagnosis"])
app.include_router(patient.router, prefix="/api/patient", tags=["patient"])
app.include_router(treatment.router, prefix="/api/treatment", tags=["treatment"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "UnifySense Clinical Diagnosis Assistant",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "api": "running",
            "aws_bedrock": "configured"
        }
    }
