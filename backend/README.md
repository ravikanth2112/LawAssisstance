# Immigration Law Dashboard - Phase 1 API Documentation

## 🚀 Quick Start

### 1. Installation
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start Server
```bash
python run_server.py
```

### 3. Create Sample Data
```bash
python create_sample_data.py
```

### 4. Access API
- **API Server**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs
- **ReDoc Documentation**: http://127.0.0.1:8000/redoc

## 📋 Test Accounts

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@lawfirm.com | admin123 |
| Lawyer | john.smith@lawfirm.com | lawyer123 |
| Lawyer | sarah.johnson@lawfirm.com | lawyer123 |
| Client | maria.rodriguez@email.com | client123 |
| Client | john.chen@email.com | client123 |

## 🔗 API Endpoints

### Authentication (`/api/auth`)
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - User logout

### Users (`/api/users`)
- `GET /api/users/` - Get all users (admin only)
- `GET /api/users/{user_id}` - Get user by ID
- `PUT /api/users/{user_id}` - Update user
- `DELETE /api/users/{user_id}` - Delete user (admin only)

### Lawyers (`/api/lawyers`)
- `GET /api/lawyers/` - Get all lawyers
- `GET /api/lawyers/{lawyer_id}` - Get lawyer by ID
- `POST /api/lawyers/` - Create lawyer profile
- `PUT /api/lawyers/{lawyer_id}` - Update lawyer profile
- `DELETE /api/lawyers/{lawyer_id}` - Delete lawyer profile
- `GET /api/lawyers/me/profile` - Get current user's lawyer profile

### Clients (`/api/clients`)
- `GET /api/clients/` - Get clients (filtered by role)
- `GET /api/clients/{client_id}` - Get client by ID
- `POST /api/clients/` - Create new client
- `PUT /api/clients/{client_id}` - Update client
- `DELETE /api/clients/{client_id}` - Delete client

### Cases (`/api/cases`)
- `GET /api/cases/` - Get cases (filtered by role)
- `GET /api/cases/{case_id}` - Get case by ID
- `POST /api/cases/` - Create new case
- `PUT /api/cases/{case_id}` - Update case
- `DELETE /api/cases/{case_id}` - Delete case

### Dashboard (`/api/dashboard`)
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/recent-activity` - Get recent activity
- `GET /api/dashboard/upcoming-deadlines` - Get upcoming deadlines
- `GET /api/dashboard/case-distribution` - Get case distribution

## 🔐 Authentication

All protected endpoints require a Bearer token in the Authorization header:

```bash
Authorization: Bearer <your_access_token>
```

### Login Example
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.smith@lawfirm.com",
    "password": "lawyer123"
  }'
```

## 🏗️ Database Schema

### Users Table
- `id` (Primary Key)
- `email` (Unique)
- `password_hash`
- `first_name`
- `last_name`
- `role` (lawyer, client, admin)
- `is_active`
- `is_verified`
- `created_at`
- `updated_at`

### Lawyers Table
- `id` (Primary Key)
- `user_id` (Foreign Key → Users)
- `bar_number`
- `practice_areas`
- `experience_years`
- `phone`
- `office_address`
- `bio`

### Clients Table
- `id` (Primary Key)
- `user_id` (Foreign Key → Users, Optional)
- `lawyer_id` (Foreign Key → Lawyers)
- `first_name`
- `last_name`
- `email`
- `phone`
- `address`
- `country_of_birth`
- `current_status`
- `case_type`
- `status` (active, pending, completed, inactive)
- `last_contact`
- `notes`

### Cases Table
- `id` (Primary Key)
- `client_id` (Foreign Key → Clients)
- `lawyer_id` (Foreign Key → Lawyers)
- `case_number` (Unique)
- `case_type`
- `title`
- `description`
- `status` (pending, in_progress, waiting_response, approved, denied, completed)
- `priority` (low, medium, high, urgent)
- `filed_date`
- `deadline`
- `completed_date`
- `estimated_cost`
- `actual_cost`
- `progress_percentage`
- `notes`

## 🎯 Role-Based Access Control

### Admin
- Full access to all endpoints
- Can manage users, lawyers, clients, and cases
- System-wide dashboard statistics

### Lawyer
- Can manage their own profile
- Can create and manage their assigned clients
- Can create and manage their assigned cases
- Dashboard shows their statistics only

### Client
- Can view their own profile
- Can view their assigned cases
- Can view their lawyer information
- Dashboard shows their case information only

## 📊 Dashboard Data

### Statistics API Response Example
```json
{
  "clients": {
    "total": 25,
    "active": 18,
    "pending": 5,
    "completed": 2
  },
  "cases": {
    "total": 45,
    "active": 32,
    "completed": 13,
    "pending": 0
  },
  "deadlines": {
    "this_week": 8
  }
}
```

### Recent Activity API Response Example
```json
[
  {
    "type": "case_update",
    "message": "Case CASE-2024-0001 updated",
    "client": "Maria Rodriguez",
    "time": "2024-09-01T10:30:00Z",
    "case_id": 1
  }
]
```

## 🔧 Configuration

Environment variables can be set in `.env` file:

```env
DEBUG=true
HOST=127.0.0.1
PORT=8000
DATABASE_URL=sqlite:///./immigration_law.db
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🚦 Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

## 🧪 Testing

Use the interactive API documentation at http://127.0.0.1:8000/docs to test all endpoints.

## 📈 Next Steps

This Phase 1 API provides the foundation for:
- User authentication and authorization
- Client and case management
- Dashboard analytics
- Role-based access control

Future phases will include:
- Document management
- File uploads
- Email notifications
- Advanced reporting
- Payment processing
- Calendar integration
