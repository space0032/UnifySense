# Deployment Guide

## UnifySense - Clinical Diagnosis Assistant

### Prerequisites

1. **AWS Account** with Bedrock access enabled
2. **AWS Credentials** configured with appropriate permissions
3. **Python 3.9+** installed
4. **Node.js 18+** installed
5. **Docker** (optional, for containerized deployment)

### AWS Bedrock Setup

1. **Enable Amazon Bedrock** in your AWS account
2. **Request Model Access** for Nova models:
   - Amazon Nova Pro
   - Amazon Nova Lite
   - Amazon Nova Micro
3. **Configure IAM Permissions**:
   - bedrock:InvokeModel
   - bedrock:InvokeModelWithResponseStream

### Local Development Deployment

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
DYNAMODB_TABLE_NAME=unifysense-patients
S3_BUCKET_NAME=unifysense-documents
EOF

# Start the server
uvicorn main:app --reload --port 8000
```

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Access the application at `http://localhost:3000`

### Production Deployment

#### Option 1: AWS Elastic Beanstalk

**Backend:**
```bash
# Install EB CLI
pip install awsebcli

# Initialize Elastic Beanstalk
eb init -p python-3.9 unifysense-backend

# Create environment
eb create unifysense-prod

# Deploy
eb deploy
```

**Frontend:**
```bash
# Build production bundle
npm run build

# Deploy to S3 + CloudFront
aws s3 sync build/ s3://your-bucket-name
```

#### Option 2: Docker Containers

**Backend Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build and run:**
```bash
docker build -t unifysense-backend .
docker run -p 8000:8000 --env-file .env unifysense-backend
```

#### Option 3: AWS ECS/Fargate

1. Build Docker images
2. Push to Amazon ECR
3. Create ECS task definitions
4. Deploy services
5. Configure Application Load Balancer

### Environment Variables

**Backend:**
- `AWS_REGION`: AWS region for Bedrock (default: us-east-1)
- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `DYNAMODB_TABLE_NAME`: DynamoDB table name
- `S3_BUCKET_NAME`: S3 bucket for documents

**Frontend:**
- `REACT_APP_API_URL`: Backend API URL

### Database Setup (Production)

Create DynamoDB table:
```bash
aws dynamodb create-table \
  --table-name unifysense-patients \
  --attribute-definitions \
    AttributeName=patient_id,AttributeType=S \
  --key-schema \
    AttributeName=patient_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

### S3 Bucket Setup

```bash
aws s3 mb s3://unifysense-documents
aws s3api put-bucket-encryption \
  --bucket unifysense-documents \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'
```

### Security Considerations

1. **Enable HTTPS** for all endpoints
2. **Implement authentication** (AWS Cognito, Auth0, etc.)
3. **Enable CORS** only for trusted domains
4. **Use AWS Secrets Manager** for credentials
5. **Enable CloudWatch** logging and monitoring
6. **Implement rate limiting**
7. **Regular security audits**
8. **HIPAA compliance** measures if handling real patient data

### Monitoring

- **CloudWatch Logs**: Application logs
- **CloudWatch Metrics**: Custom metrics for API calls
- **AWS X-Ray**: Distributed tracing
- **Health checks**: Regular endpoint monitoring

### Backup and Recovery

- **DynamoDB**: Enable point-in-time recovery
- **S3**: Enable versioning and lifecycle policies
- **Regular backups**: Automated backup schedule

### Scaling

- **Auto Scaling**: Configure for backend services
- **CloudFront**: CDN for frontend
- **ElastiCache**: Redis for session management
- **Load Balancing**: Application Load Balancer

### Cost Optimization

- **Bedrock**: Monitor token usage
- **DynamoDB**: Use on-demand billing initially
- **S3**: Implement lifecycle policies
- **CloudWatch**: Set up billing alerts

### Support

For deployment issues, contact the development team or refer to AWS documentation.
