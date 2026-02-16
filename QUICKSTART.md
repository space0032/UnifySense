# Quick Start Guide

## UnifySense Clinical Diagnosis Assistant

Get started with UnifySense in 5 minutes!

### Prerequisites Check

Before you begin, ensure you have:
- [ ] Python 3.9 or higher installed
- [ ] Node.js 18 or higher installed
- [ ] AWS Account with Bedrock access
- [ ] AWS credentials configured

### Step 1: Clone the Repository

```bash
git clone https://github.com/space0032/UnifySense.git
cd UnifySense
```

### Step 2: Backend Setup (5 minutes)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env file with your AWS credentials
```

**Edit `.env` file:**
```
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_actual_access_key
AWS_SECRET_ACCESS_KEY=your_actual_secret_key
```

### Step 3: Start Backend Server

```bash
# Make sure you're in the backend directory with venv activated
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Test the backend:**
Open http://localhost:8000 in your browser. You should see:
```json
{
  "status": "healthy",
  "service": "UnifySense Clinical Diagnosis Assistant",
  "version": "1.0.0"
}
```

### Step 4: Frontend Setup (3 minutes)

Open a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (this may take a few minutes)
npm install

# Start development server
npm start
```

The application will automatically open in your browser at http://localhost:3000

### Step 5: Try Your First Diagnosis

1. **Patient Information**:
   - Age: 45
   - Gender: Male
   - Medical History: Hypertension
   - Click "Next"

2. **Add Symptoms**:
   - Click "Add Symptom"
   - Symptom: "Persistent headache"
   - Severity: Moderate
   - Duration: 7 days
   - Notes: "Worse in the morning"
   - Click "Next"

3. **Analyze**:
   - Click "Analyze"
   - Wait 10-20 seconds for AI processing

4. **View Results**:
   - See symptom analysis
   - Review possible diagnoses
   - Check treatment recommendations

### Troubleshooting

#### Backend Issues

**Issue**: "Error invoking Nova Pro"
**Solution**: 
- Check AWS credentials in `.env`
- Verify Bedrock access is enabled
- Confirm Nova models are available in your region

**Issue**: "ModuleNotFoundError"
**Solution**: 
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

#### Frontend Issues

**Issue**: "npm: command not found"
**Solution**: Install Node.js from https://nodejs.org/

**Issue**: "Failed to compile"
**Solution**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Issue**: "Cannot connect to backend"
**Solution**:
- Ensure backend is running on port 8000
- Check CORS settings in backend/main.py

### AWS Bedrock Setup

If you haven't set up AWS Bedrock:

1. **Enable Amazon Bedrock**:
   - Log in to AWS Console
   - Navigate to Amazon Bedrock
   - Select your region (us-east-1 recommended)

2. **Request Model Access**:
   - Go to "Model access" in Bedrock
   - Click "Manage model access"
   - Enable:
     - Amazon Nova Pro
     - Amazon Nova Lite
     - Amazon Nova Micro
   - Submit request (approval may take a few minutes)

3. **Create IAM User** (if needed):
   ```bash
   # Create IAM user with Bedrock permissions
   aws iam create-user --user-name unifysense-user
   
   # Attach policy
   aws iam attach-user-policy \
     --user-name unifysense-user \
     --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess
   
   # Create access key
   aws iam create-access-key --user-name unifysense-user
   ```

### Testing Without AWS

If you don't have AWS credentials yet, you can still:

1. Test the frontend UI:
   - The interface will load
   - You can enter patient data
   - Analysis will fail gracefully with error message

2. Test the backend endpoints:
   ```bash
   # Test health check
   curl http://localhost:8000/health
   
   # Test patient creation
   curl -X POST "http://localhost:8000/api/patient/?age=30&gender=male"
   ```

### Development Mode

Both backend and frontend run in development mode with auto-reload:

**Backend**: FastAPI auto-reloads on code changes
**Frontend**: React auto-reloads on code changes

Edit files and see changes immediately!

### Next Steps

Once you have the application running:

1. **Read the Documentation**:
   - README.md - Comprehensive guide
   - ARCHITECTURE.md - System design
   - API_DOCUMENTATION.md - API reference

2. **Explore Examples**:
   - examples/USE_CASES.md - Real-world scenarios
   - examples/api_usage.py - Python API examples

3. **Try Different Scenarios**:
   - Emergency cases (chest pain, severe symptoms)
   - Routine care (mild headaches, cold symptoms)
   - Chronic conditions (diabetes management)

4. **Customize**:
   - Modify prompts in `backend/app/services/medical_reasoning.py`
   - Adjust UI in `frontend/src/pages/DiagnosisPage.tsx`
   - Add new features!

### Production Deployment

For production deployment, see DEPLOYMENT.md for:
- AWS Elastic Beanstalk setup
- Docker containerization
- ECS/Fargate deployment
- Security hardening
- Monitoring setup

### Getting Help

- **Documentation**: Check the docs/ folder
- **Issues**: Open a GitHub issue
- **Examples**: See examples/ folder

### What's Next?

Now that you have UnifySense running, you can:
- Customize the medical prompts
- Add more Nova model integrations
- Integrate with your EHR system
- Deploy to production
- Contribute improvements!

---

**Important Medical Disclaimer**: UnifySense is designed to assist healthcare professionals and should not replace professional medical judgment. All AI-generated suggestions must be reviewed by qualified healthcare providers.

Happy diagnosing! 🏥🤖
