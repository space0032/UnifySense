# Architecture Overview

## UnifySense Clinical Diagnosis Assistant

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              React Frontend (TypeScript)                  │  │
│  │  - Material-UI Components                                │  │
│  │  - Patient Input Forms                                    │  │
│  │  - Results Visualization                                  │  │
│  │  - Stepper Workflow                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                               │
                               │ HTTPS/REST
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                           │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            FastAPI Backend (Python)                       │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  API Endpoints:                                     │  │  │
│  │  │  - /api/symptoms/analyze                            │  │  │
│  │  │  - /api/diagnosis/generate                          │  │  │
│  │  │  - /api/treatment/recommend                         │  │  │
│  │  │  - /api/patient/*                                   │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Medical Reasoning Service                         │  │
│  │  - Symptom Analysis Logic                                │  │
│  │  - Diagnosis Generation Logic                            │  │
│  │  - Treatment Recommendation Logic                        │  │
│  │  - Medical Knowledge Integration                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AI Engine Layer                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            Amazon Bedrock Service                         │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Amazon Nova Models:                                │  │  │
│  │  │  - Nova Pro: Complex reasoning & diagnosis          │  │  │
│  │  │  - Nova Lite: Quick symptom triage                  │  │  │
│  │  │  - Nova Micro: Embeddings & search                  │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data Storage Layer                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐    ┌──────────────────────────────┐   │
│  │   Amazon DynamoDB   │    │        Amazon S3             │   │
│  │  - Patient Records  │    │  - Medical Documents         │   │
│  │  - Diagnosis History│    │  - Images/Reports            │   │
│  │  - Analysis Logs    │    │  - Encrypted Storage         │   │
│  └─────────────────────┘    └──────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Component Descriptions

#### 1. Frontend Layer (React + TypeScript)
- **Technology**: React 18, Material-UI, TypeScript
- **Responsibilities**:
  - User interface for symptom input
  - Patient information collection
  - Results visualization
  - Multi-step workflow management
- **Key Features**:
  - Responsive design
  - Real-time validation
  - Interactive forms
  - Progress tracking

#### 2. API Layer (FastAPI)
- **Technology**: FastAPI, Python 3.9+
- **Responsibilities**:
  - Request validation
  - API endpoint management
  - CORS handling
  - Error handling
- **Endpoints**:
  - Symptom analysis
  - Diagnosis generation
  - Treatment recommendations
  - Patient record management

#### 3. Business Logic Layer
- **Medical Reasoning Service**:
  - Processes patient data
  - Constructs prompts for AI models
  - Parses and structures AI responses
  - Applies medical knowledge rules
- **Key Functions**:
  - Symptom triage
  - Differential diagnosis
  - Treatment planning
  - Risk assessment

#### 4. AI Engine (Amazon Bedrock)
- **Amazon Nova Pro**:
  - Use case: Complex medical reasoning
  - Features: Deep analysis, differential diagnosis
  - Parameters: Higher token count, careful temperature
- **Amazon Nova Lite**:
  - Use case: Quick symptom triage
  - Features: Fast response, basic analysis
  - Parameters: Lower latency, efficient processing
- **Amazon Nova Micro**:
  - Use case: Embeddings and semantic search
  - Features: Medical literature search
  - Parameters: Vector generation

#### 5. Data Storage
- **Amazon DynamoDB**:
  - Patient records
  - Diagnosis history
  - Audit logs
  - Session data
- **Amazon S3**:
  - Medical documents
  - Images and scans
  - Reports and exports
  - Encrypted at rest

### Data Flow

1. **Input Phase**:
   - User enters patient information and symptoms
   - Frontend validates and structures data
   - API receives formatted request

2. **Analysis Phase**:
   - Quick triage using Nova Lite
   - Severity assessment
   - Priority determination

3. **Reasoning Phase**:
   - Nova Pro performs deep analysis
   - Generates possible diagnoses
   - Calculates confidence scores
   - Assigns ICD-10 codes

4. **Recommendation Phase**:
   - Treatment suggestions
   - Test recommendations
   - Follow-up planning
   - Risk mitigation

5. **Output Phase**:
   - Structured results returned
   - Frontend displays information
   - Optional: Save to patient record

### Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       Security Layers                            │
├─────────────────────────────────────────────────────────────────┤
│  1. Transport Security: HTTPS/TLS                                │
│  2. Authentication: AWS Cognito (future)                         │
│  3. Authorization: Role-based access control                     │
│  4. Data Encryption: At rest (S3, DynamoDB) and in transit       │
│  5. Audit Logging: CloudWatch Logs                               │
│  6. Compliance: HIPAA-ready architecture                         │
└─────────────────────────────────────────────────────────────────┘
```

### Scalability

- **Horizontal Scaling**: FastAPI instances behind load balancer
- **Serverless Options**: Lambda functions for API
- **Caching**: ElastiCache for frequent queries
- **CDN**: CloudFront for frontend distribution
- **Database**: DynamoDB auto-scaling

### Monitoring and Observability

- **CloudWatch Metrics**: API latency, error rates
- **CloudWatch Logs**: Application logs, audit trails
- **AWS X-Ray**: Distributed tracing
- **Custom Dashboards**: Business metrics

### Future Enhancements

1. **Multimodal Support**:
   - Medical image analysis
   - Lab result interpretation
   - ECG/vital signs processing

2. **Voice Interface**:
   - Voice-based symptom input
   - Amazon Nova Sonic integration
   - Real-time transcription

3. **Advanced Features**:
   - Clinical decision support
   - Drug interaction checking
   - Evidence-based guidelines
   - Medical literature integration

4. **Integration**:
   - EHR system integration
   - Laboratory systems
   - Radiology PACS
   - Pharmacy systems
