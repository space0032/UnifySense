# UnifySense - Clinical Diagnosis Assistant

A generative AI application powered by Amazon Nova foundation models for medical diagnostic assistance.

## Overview

UnifySense is an AI-powered Clinical Diagnosis Assistant that helps medical practitioners analyze symptoms and patient history to generate diagnostic suggestions and recommended next steps. The application leverages Amazon Nova's reasoning capabilities to process medical data and provide evidence-based recommendations.

## Features

- **Intelligent Symptom Analysis**: Uses Amazon Nova models to reason through patient symptoms
- **Multimodal Understanding**: Processes both structured (patient histories) and unstructured medical data
- **Diagnostic Reasoning**: Generates possible diagnoses with confidence levels
- **Treatment Recommendations**: Suggests next steps including tests and treatments
- **Medical Database Integration**: Integrates with ICD-10 codes and medical knowledge bases
- **Patient History Management**: Securely stores and analyzes patient records
- **Interactive Web Interface**: User-friendly dashboard for medical practitioners

## Architecture

### Backend
- **Framework**: FastAPI (Python)
- **AI Engine**: Amazon Bedrock with Nova models
- **Database**: AWS DynamoDB for patient records
- **Storage**: AWS S3 for medical documents

### Frontend
- **Framework**: React with TypeScript
- **UI Library**: Material-UI
- **State Management**: React Context API

### AI Models
- **Amazon Nova Pro**: For complex medical reasoning and diagnosis
- **Amazon Nova Lite**: For quick symptom triage
- **Amazon Nova Micro**: For embeddings and semantic search

## Prerequisites

- Python 3.9+
- Node.js 18+
- AWS Account with Bedrock access
- AWS CLI configured with appropriate credentials

## Installation

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

## Configuration

Create a `.env` file in the backend directory:

```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
DYNAMODB_TABLE_NAME=unifysense-patients
S3_BUCKET_NAME=unifysense-documents
```

## Usage

### Start Backend Server

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### Start Frontend Development Server

```bash
cd frontend
npm start
```

Access the application at `http://localhost:3000`

## API Endpoints

- `POST /api/analyze-symptoms` - Analyze patient symptoms
- `POST /api/generate-diagnosis` - Generate diagnostic suggestions
- `POST /api/recommend-treatment` - Get treatment recommendations
- `GET /api/patient/{id}` - Retrieve patient history
- `POST /api/patient` - Create/update patient record

## Use Cases

1. **Symptom Analysis**: Input patient symptoms and receive AI-powered analysis
2. **Diagnostic Support**: Get evidence-based diagnostic suggestions
3. **Treatment Planning**: Receive recommended next steps and treatment options
4. **Medical Records**: Manage and analyze patient histories
5. **Knowledge Search**: Semantic search across medical literature

## Security & Compliance

- HIPAA-compliant data handling
- Encrypted data storage and transmission
- Audit logging for all medical decisions
- Role-based access control

## Disclaimer

This application is designed to assist medical practitioners and should not be used as a replacement for professional medical judgment. All AI-generated suggestions should be reviewed and validated by qualified healthcare professionals.

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## Support

For issues and questions, please open a GitHub issue.
