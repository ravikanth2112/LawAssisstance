# 🏛️ Immigration Law Dashboard - Complete API Documentation

## 📋 Overview

This comprehensive API documentation covers all endpoints for the Immigration Law Dashboard system, designed for immigration law practice management with client tracking, deadlines, billing, and analytics features.

**Base URL**: `http://localhost:8000`  
**API Version**: 2.0  
**Authentication**: JWT Bearer Token  

---

## 🔐 Authentication System

### **Authentication Endpoints**

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/auth/register` | Register new user | ❌ |
| `POST` | `/api/auth/login` | User login | ❌ |
| `POST` | `/api/auth/logout` | User logout | ✅ |
| `GET` | `/api/auth/me` | Get current user | ✅ |

### **Sample Authentication Flow**

```json
// Registration
POST /api/auth/register
{
  "username": "john_lawyer",
  "email": "john@lawfirm.com",
  "password": "secure123",
  "first_name": "John",
  "last_name": "Smith",
  "role": "lawyer"
}

// Login Response
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "john_lawyer",
    "role": "lawyer"
  }
}
```

---

## 👥 Phase 1 APIs

### **User Management**

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| `GET` | `/api/users/` | List all users | ✅ | admin |
| `POST` | `/api/users/` | Create new user | ✅ | admin |
| `GET` | `/api/users/{id}` | Get user by ID | ✅ | admin/self |
| `PUT` | `/api/users/{id}` | Update user | ✅ | admin/self |
| `DELETE` | `/api/users/{id}` | Delete user | ✅ | admin |

### **Lawyer Management**

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| `GET` | `/api/lawyers/` | List all lawyers | ✅ | All |
| `POST` | `/api/lawyers/` | Create lawyer profile | ✅ | admin |
| `GET` | `/api/lawyers/{id}` | Get lawyer by ID | ✅ | All |
| `PUT` | `/api/lawyers/{id}` | Update lawyer | ✅ | admin/self |
| `DELETE` | `/api/lawyers/{id}` | Delete lawyer | ✅ | admin |
| `GET` | `/api/lawyers/me/profile` | Get my lawyer profile | ✅ | lawyer |

### **Client Management**

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| `GET` | `/api/clients/` | List clients | ✅ | admin/lawyer |
| `POST` | `/api/clients/` | Create new client | ✅ | admin/lawyer |
| `GET` | `/api/clients/{id}` | Get client by ID | ✅ | admin/lawyer/self |
| `PUT` | `/api/clients/{id}` | Update client | ✅ | admin/lawyer/self |
| `DELETE` | `/api/clients/{id}` | Delete client | ✅ | admin |

### **Case Management**

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| `GET` | `/api/cases/` | List cases (filtered) | ✅ | All |
| `POST` | `/api/cases/` | Create new case | ✅ | admin/lawyer |
| `GET` | `/api/cases/{id}` | Get case by ID | ✅ | All |
| `PUT` | `/api/cases/{id}` | Update case | ✅ | admin/lawyer |
| `DELETE` | `/api/cases/{id}` | Delete case | ✅ | admin |
| `GET` | `/api/cases/statistics` | Get case statistics | ✅ | admin/lawyer |
| `GET` | `/api/cases/search` | Search cases | ✅ | All |

### **Dashboard Analytics**

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| `GET` | `/api/dashboard/stats` | Get dashboard KPIs | ✅ | All |
| `GET` | `/api/dashboard/recent-activity` | Recent activities | ✅ | All |
| `GET` | `/api/dashboard/upcoming-deadlines` | Upcoming deadlines | ✅ | All |
| `GET` | `/api/dashboard/case-distribution` | Case distribution | ✅ | admin/lawyer |

---

## 🚀 Phase 2 APIs

### **Deadline Management**

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| `GET` | `/api/deadlines/` | List deadlines (filtered) | ✅ | All |
| `GET` | `/api/deadlines/upcoming` | Get upcoming deadlines | ✅ | All |
| `GET` | `/api/deadlines/overdue` | Get overdue deadlines | ✅ | All |
| `POST` | `/api/deadlines/` | Create new deadline | ✅ | admin/lawyer |
| `GET` | `/api/deadlines/{id}` | Get deadline by ID | ✅ | All |
| `PUT` | `/api/deadlines/{id}` | Update deadline | ✅ | admin/lawyer |
| `DELETE` | `/api/deadlines/{id}` | Delete deadline | ✅ | admin |
| `GET` | `/api/deadlines/pending` | Get pending deadlines | ✅ | All |

### **Document Management**

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| `GET` | `/api/documents/` | List documents (filtered) | ✅ | All |
| `POST` | `/api/documents/upload` | Upload document (10MB max) | ✅ | admin/lawyer |
| `GET` | `/api/documents/{id}` | Get document by ID | ✅ | All |
| `PUT` | `/api/documents/{id}` | Update document metadata | ✅ | admin/lawyer |
| `DELETE` | `/api/documents/{id}` | Delete document | ✅ | admin |
| `POST` | `/api/documents/{id}/download` | Download document | ✅ | All |
| `POST` | `/api/documents/search` | Search documents | ✅ | All |
| `POST` | `/api/documents/{id}/share` | Share document | ✅ | admin/lawyer |

### **Billing & Financial Management**

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| `GET` | `/api/billing/` | List billing records | ✅ | All |
| `GET` | `/api/billing/pending` | Get pending invoices | ✅ | All |
| `POST` | `/api/billing/` | Create invoice (auto-calc) | ✅ | admin/lawyer |
| `GET` | `/api/billing/{id}` | Get billing record | ✅ | All |
| `PUT` | `/api/billing/{id}` | Update billing record | ✅ | admin/lawyer |
| `DELETE` | `/api/billing/{id}` | Delete billing record | ✅ | admin |
| `POST` | `/api/billing/{id}/send` | Send invoice via email | ✅ | admin/lawyer |
| `POST` | `/api/billing/payments` | Record payment | ✅ | admin/lawyer |
| `GET` | `/api/billing/payments/{id}` | Get payment details | ✅ | All |

### **Activity Tracking & Time Management**

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| `GET` | `/api/activities/` | List activities (filtered) | ✅ | All |
| `GET` | `/api/activities/summary` | Hours & billing summary | ✅ | All |
| `POST` | `/api/activities/` | Log time/activity | ✅ | admin/lawyer |
| `GET` | `/api/activities/{id}` | Get activity by ID | ✅ | All |
| `PUT` | `/api/activities/{id}` | Update activity | ✅ | admin/lawyer |
| `DELETE` | `/api/activities/{id}` | Delete activity | ✅ | admin |
| `GET` | `/api/activities/billable/pending` | Pending billable hours | ✅ | admin/lawyer |

---

## 📊 API Summary

### **Total Endpoint Coverage**

| Module | Endpoints | Status |
|--------|-----------|--------|
| **Authentication** | 4 | ✅ Complete |
| **Users** | 5 | ✅ Complete |
| **Lawyers** | 6 | ✅ Complete |
| **Clients** | 5 | ✅ Complete |
| **Cases** | 7 | ✅ Complete |
| **Dashboard** | 4 | ✅ Complete |
| **Deadlines** | 8 | ✅ Complete |
| **Documents** | 8 | ✅ Complete |
| **Billing** | 9 | ✅ Complete |
| **Activities** | 7 | ✅ Complete |
| **TOTAL** | **63** | ✅ **Production Ready** |

---

## 🔒 Security Features

### **Authentication & Authorization**
- **JWT Token Authentication** on all protected endpoints
- **Role-Based Access Control** (admin/lawyer/client)
- **Data Isolation** by user role and ownership
- **Secure Password Hashing** with bcrypt

### **File Upload Security**
- **10MB Maximum** file size limit
- **File Type Validation** for documents
- **Secure File Storage** with access controls
- **Confidentiality Levels** for sensitive documents

### **Data Protection**
- **Input Validation** using Pydantic schemas
- **SQL Injection Prevention** via SQLAlchemy ORM
- **Error Handling** without sensitive data exposure
- **Rate Limiting** and request validation

---

## 🌐 Interactive Documentation

### **Swagger UI Documentation**
**URL**: `http://localhost:8000/docs`

- ✅ **Interactive API Testing** - Test all endpoints directly
- ✅ **Schema Exploration** - View request/response models
- ✅ **Authentication Testing** - JWT token integration
- ✅ **Real-time Validation** - Immediate feedback

### **ReDoc Documentation**
**URL**: `http://localhost:8000/redoc`

- ✅ **Clean Documentation** - Professional API docs
- ✅ **Detailed Schemas** - Complete data models
- ✅ **Code Examples** - Sample requests/responses

---

## 🚀 Quick Start

### **1. Start the Server**
```bash
cd backend
python run_server.py
```

### **2. Access Documentation**
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### **3. Authentication**
```bash
# Register a new user
curl -X POST "http://localhost:8000/api/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"username":"test","email":"test@example.com","password":"test123","role":"lawyer"}'

# Login to get token
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username":"test","password":"test123"}'
```

### **4. Use API with Token**
```bash
# Use the token from login response
curl -X GET "http://localhost:8000/api/cases/" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📈 Performance & Scalability

### **Database Optimization**
- **Indexed Queries** for fast searches
- **Relationship Loading** optimization
- **Connection Pooling** for concurrent users
- **Query Optimization** with SQLAlchemy

### **API Performance**
- **Async/Await** FastAPI implementation
- **Response Caching** for static data
- **Pagination** for large datasets
- **Efficient Serialization** with Pydantic

---

## 🔄 API Versioning

**Current Version**: 2.0  
**Versioning Strategy**: URL-based (/api/v2/)  
**Backward Compatibility**: Phase 1 APIs maintained  

---

## 📞 Support & Resources

### **Development Team**
- **Backend API**: FastAPI + SQLAlchemy
- **Database**: SQL Server Express
- **Authentication**: JWT + bcrypt
- **Documentation**: Auto-generated via FastAPI

### **Integration Ready**
- ✅ **React.js Frontend** integration prepared
- ✅ **Mobile App APIs** complete
- ✅ **Third-party Integration** endpoints available
- ✅ **Webhook Support** for external systems

---

**Last Updated**: September 2025  
**API Version**: 2.0  
**Total Endpoints**: 63  
**Status**: Production Ready ✅
