# 🚀 Immigration Law Dashboard - Quick Setup Guide

## 📋 Branch Organization

- **MAIN Branch**: Phase 1 APIs (FastAPI Backend)
- **DEV Branch**: UI Components (React Frontend)

## ⚡ Quick Start

### 1. For API Development (MAIN Branch)
```bash
# Switch to main branch
git checkout main

# Set up Python environment
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create sample data
python create_sample_data.py

# Start API server
python run_server.py
```

**API Available At:**
- Server: http://127.0.0.1:8000
- Documentation: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### 2. For UI Development (DEV Branch)
```bash
# Switch to dev branch
git checkout dev

# Install Node dependencies
npm install

# Start React development server
npm start
```

**React App Available At:**
- Frontend: http://localhost:3000

### 3. For Full-Stack Testing
```bash
# Terminal 1: API Server (MAIN branch)
git checkout main
cd backend
python run_server.py

# Terminal 2: React App (DEV branch)
git checkout dev
npm start
```

## 🔐 Test Accounts

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@lawfirm.com | admin123 |
| Lawyer | john.smith@lawfirm.com | lawyer123 |
| Client | maria.rodriguez@email.com | client123 |

## 📚 Documentation

- **API Docs**: `backend/README.md`
- **Frontend Docs**: `README.md`
- **Project Status**: `PROJECT_STATUS_REPORT.md`

## 🎯 Development Workflow

1. **UI Changes**: Work in DEV branch
2. **API Changes**: Work in MAIN branch
3. **Integration**: Test both branches together

You now have a perfectly organized Immigration Law Dashboard with complete separation between UI and APIs! 🎉
