# Immigration Law Dashboard - Phase 1 Backend Setup Guide

## 🎯 Phase 1 Implementation Complete!

Your Immigration Law Dashboard backend is ready with comprehensive APIs for authentication, user management, case management, and dashboard analytics.

## 📦 What's Included:

### ✅ **APIs Implemented:**
- **Authentication** (`/api/auth/`) - Complete JWT auth system
- **Users** (`/api/users/`) - User management with role-based access
- **Lawyers** (`/api/lawyers/`) - Lawyer profile and specialization management
- **Clients** (`/api/clients/`) - Client management with search
- **Cases** (`/api/cases/`) - Full case management with statistics
- **Dashboard** (`/api/dashboard/`) - Role-specific analytics and summaries

### ✅ **Database:**
- SQL Server Express ready schema (13 tables)
- Complete relationships and constraints
- Sample data for testing
- Proper indexes for performance

## 🚀 **Setup Instructions:**

### **Step 1: Database Setup**
```powershell
# 1. Install SQL Server Express (if not installed)
# Download from: https://www.microsoft.com/en-us/sql-server/sql-server-downloads

# 2. Create the database using SQL Server Management Studio (SSMS)
# Execute the SQL script in: backend/database_setup.md

# 3. Or create database via command line:
sqlcmd -S .\SQLEXPRESS -Q "CREATE DATABASE ImmigrationLawDB;"
```

### **Step 2: Environment Configuration**
```powershell
# Copy the environment file
cd backend
cp .env.example .env

# Edit .env file with your settings (especially DATABASE_URL)
```

### **Step 3: Initialize Database**
```powershell
# Navigate to backend directory
cd backend

# Install additional dependency
# (Already installed: pyodbc, httpx)

# Initialize database tables and sample data
python scripts/init_db.py
```

### **Step 4: Test Backend**
```powershell
# Test database connection and API functionality
python scripts/test_backend.py
```

### **Step 5: Start Server**
```powershell
# Start the FastAPI development server
python -m uvicorn app.main:app --reload

# Server will start on: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

## 🧪 **Testing the APIs:**

### **Sample Login Credentials:**
- **Admin**: `admin@lawfirm.com` / `admin123`
- **Lawyer**: `lawyer1@lawfirm.com` / `lawyer123`
- **Client 1**: `client1@email.com` / `client123`
- **Client 2**: `client2@email.com` / `client123`

### **Key API Endpoints:**
```
POST /api/auth/login           # User authentication
GET  /api/dashboard/           # Role-specific dashboard data
GET  /api/cases/               # List cases (role-filtered)
POST /api/cases/               # Create new case
GET  /api/cases/statistics     # Case statistics
GET  /api/users/               # List users (admin/lawyer only)
GET  /api/lawyers/             # List lawyers
GET  /api/clients/             # List clients
```

## 📊 **Dashboard Features:**

### **Admin Dashboard:**
- System-wide statistics (users, cases, activity)
- Monthly case trends
- Completion rates and performance metrics

### **Lawyer Dashboard:**
- Personal case statistics
- Recent case activity
- Upcoming deadlines tracking
- Performance analytics

### **Client Dashboard:**
- Personal case overview
- Case status tracking
- Quick statistics

## 🔗 **Frontend Integration:**

Your React frontend can now connect to these APIs:

```javascript
// Example: Login and get dashboard data
const login = async (email, password) => {
  const response = await fetch('http://localhost:8000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  return response.json();
};

const getDashboard = async (token) => {
  const response = await fetch('http://localhost:8000/api/dashboard/', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return response.json();
};
```

## 📈 **Phase 2 Ready:**

Phase 1 provides the foundation. Phase 2 will add:
- **Deadlines Management** - Calendar integration, reminders
- **Document Management** - File uploads, document tracking
- **Basic Billing** - Time tracking, simple invoicing
- **Activity Logging** - Audit trails, communication tracking

## 🛠 **Troubleshooting:**

### **Common Issues:**
1. **Database Connection Error:**
   - Ensure SQL Server Express is running
   - Check connection string in .env file
   - Verify database exists

2. **Import Errors:**
   - Ensure virtual environment is activated
   - Run: `pip install -r requirements.txt`

3. **Permission Errors:**
   - Check SQL Server authentication settings
   - Verify Windows authentication is enabled

### **Verify Setup:**
```powershell
# Quick verification
python scripts/test_backend.py

# Should show:
# ✅ Database connection successful!
# ✅ Sample data exists
# ✅ All API endpoints working
```

## 🎉 **Success Criteria:**

✅ Database tables created  
✅ Sample data loaded  
✅ FastAPI server running on port 8000  
✅ API documentation accessible at `/docs`  
✅ Authentication working with sample users  
✅ Dashboard data loading for all user types  
✅ Role-based access control functioning  

**Your backend is production-ready for Phase 1 features!** 🚀
