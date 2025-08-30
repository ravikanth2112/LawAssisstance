# Immigration Law Dashboard - API Documentation

## Project Overview
**Technology Stack:** SQL Server Express, SSMS, Python FastAPI, React.js  
**Database:** SQL Server Express Edition  
**Backend:** Python FastAPI  
**Frontend:** React.js with Vite  

---

## 🔐 Authentication & Authorization APIs

### User Authentication
| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `POST` | `/api/auth/register` | User registration | `{email, password, first_name, last_name, user_type}` | `{user_id, token, user_info}` |
| `POST` | `/api/auth/login` | User login | `{email, password}` | `{token, refresh_token, user_info}` |
| `POST` | `/api/auth/logout` | User logout | `{refresh_token}` | `{message}` |
| `POST` | `/api/auth/refresh-token` | Refresh JWT token | `{refresh_token}` | `{token, refresh_token}` |
| `POST` | `/api/auth/forgot-password` | Password reset request | `{email}` | `{message}` |
| `POST` | `/api/auth/reset-password` | Reset password with token | `{token, new_password}` | `{message}` |
| `GET` | `/api/auth/me` | Get current user profile | - | `{user_info}` |
| `PUT` | `/api/auth/me` | Update current user profile | `{first_name, last_name, phone}` | `{user_info}` |

---

## 👥 User Management APIs

### Users
| Method | Endpoint | Description | Access Level | Parameters |
|--------|----------|-------------|--------------|------------|
| `GET` | `/api/users` | Get all users | Admin only | `?page=1&limit=10&search=""` |
| `GET` | `/api/users/{user_id}` | Get user by ID | Admin/Self | - |
| `PUT` | `/api/users/{user_id}` | Update user | Admin/Self | `{first_name, last_name, phone, is_active}` |
| `DELETE` | `/api/users/{user_id}` | Delete user (soft delete) | Admin only | - |
| `GET` | `/api/users/search` | Search users by criteria | Admin only | `?query=""&user_type=""` |

### Lawyers
| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/api/lawyers` | Get all lawyers | - | `[{lawyer_info}]` |
| `POST` | `/api/lawyers` | Create lawyer profile | `{user_id, bar_number, license_state, specialization, hourly_rate}` | `{lawyer_id, lawyer_info}` |
| `GET` | `/api/lawyers/{lawyer_id}` | Get lawyer by ID | - | `{lawyer_info}` |
| `PUT` | `/api/lawyers/{lawyer_id}` | Update lawyer profile | `{bar_number, specialization, hourly_rate, bio}` | `{lawyer_info}` |
| `DELETE` | `/api/lawyers/{lawyer_id}` | Delete lawyer | - | `{message}` |
| `GET` | `/api/lawyers/available` | Get available lawyers for assignment | - | `[{lawyer_info}]` |

### Clients
| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/api/clients` | Get all clients | - | `[{client_info}]` |
| `POST` | `/api/clients` | Create client profile | `{user_id, country_of_origin, current_status, preferred_language}` | `{client_id, client_info}` |
| `GET` | `/api/clients/{client_id}` | Get client by ID | - | `{client_info}` |
| `PUT` | `/api/clients/{client_id}` | Update client profile | `{country_of_origin, current_status, emergency_contact}` | `{client_info}` |
| `DELETE` | `/api/clients/{client_id}` | Delete client | - | `{message}` |
| `GET` | `/api/clients/search` | Search clients | `?query=""&country=""&status=""` | `[{client_info}]` |

---

## 📋 Case Management APIs

### Cases
| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/api/cases` | Get all cases (filtered by user role) | - | `[{case_info}]` |
| `POST` | `/api/cases` | Create new case | `{client_id, primary_lawyer_id, case_type, case_status, priority_level}` | `{case_id, case_info}` |
| `GET` | `/api/cases/{case_id}` | Get case details | - | `{case_info, client_info, lawyers, deadlines}` |
| `PUT` | `/api/cases/{case_id}` | Update case | `{case_status, priority_level, expected_completion}` | `{case_info}` |
| `DELETE` | `/api/cases/{case_id}` | Delete case | - | `{message}` |
| `GET` | `/api/cases/statistics` | Case statistics for dashboard | - | `{total_cases, active_cases, completed_cases, by_status}` |
| `GET` | `/api/cases/search` | Search cases | `?query=""&status=""&priority=""&lawyer_id=""` | `[{case_info}]` |
| `GET` | `/api/cases/by-status` | Get cases by status | `?status=""` | `[{case_info}]` |
| `GET` | `/api/cases/by-priority` | Get cases by priority | `?priority=""` | `[{case_info}]` |

### Case Lawyers Assignment
| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/api/cases/{case_id}/lawyers` | Get lawyers assigned to case | - | `[{lawyer_info, role, assigned_date}]` |
| `POST` | `/api/cases/{case_id}/lawyers` | Assign lawyer to case | `{lawyer_id, role}` | `{assignment_info}` |
| `DELETE` | `/api/cases/{case_id}/lawyers/{lawyer_id}` | Remove lawyer from case | - | `{message}` |
| `PUT` | `/api/cases/{case_id}/lawyers/{lawyer_id}` | Update lawyer role in case | `{role}` | `{assignment_info}` |

---

## ⏰ Deadline Management APIs

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/api/deadlines` | Get all deadlines | `?lawyer_id=""&status=""&priority=""` | `[{deadline_info}]` |
| `POST` | `/api/deadlines` | Create deadline | `{case_id, assigned_lawyer_id, title, description, due_date, priority}` | `{deadline_id, deadline_info}` |
| `GET` | `/api/deadlines/{deadline_id}` | Get deadline by ID | - | `{deadline_info}` |
| `PUT` | `/api/deadlines/{deadline_id}` | Update deadline | `{title, description, due_date, priority, status}` | `{deadline_info}` |
| `DELETE` | `/api/deadlines/{deadline_id}` | Delete deadline | - | `{message}` |
| `GET` | `/api/deadlines/upcoming` | Get upcoming deadlines | `?days=7&lawyer_id=""` | `[{deadline_info}]` |
| `GET` | `/api/deadlines/overdue` | Get overdue deadlines | `?lawyer_id=""` | `[{deadline_info}]` |
| `GET` | `/api/deadlines/by-case/{case_id}` | Get deadlines for specific case | - | `[{deadline_info}]` |
| `PUT` | `/api/deadlines/{deadline_id}/complete` | Mark deadline as completed | - | `{deadline_info}` |

---

## 📄 Document Management APIs

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/api/documents` | Get all documents | `?case_id=""&document_type=""&is_confidential=""` | `[{document_info}]` |
| `POST` | `/api/documents` | Upload document | `{case_id, document_name, document_type, file, is_confidential}` | `{document_id, document_info}` |
| `GET` | `/api/documents/{document_id}` | Get document metadata | - | `{document_info}` |
| `PUT` | `/api/documents/{document_id}` | Update document metadata | `{document_name, document_type, status, is_confidential}` | `{document_info}` |
| `DELETE` | `/api/documents/{document_id}` | Delete document | - | `{message}` |
| `GET` | `/api/documents/{document_id}/download` | Download document file | - | `File Stream` |
| `GET` | `/api/documents/by-case/{case_id}` | Get documents for case | - | `[{document_info}]` |
| `POST` | `/api/documents/{document_id}/share` | Share document with users | `{user_ids: []}` | `{message}` |
| `GET` | `/api/documents/search` | Search documents | `?query=""&document_type=""&date_from=""&date_to=""` | `[{document_info}]` |

---

## 💰 Billing & Financial APIs

### Billing
| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/api/billing` | Get all billing records | `?status=""&lawyer_id=""&date_from=""&date_to=""` | `[{billing_info}]` |
| `POST` | `/api/billing` | Create billing record | `{case_id, lawyer_id, hours_worked, hourly_rate, billing_period, description}` | `{billing_id, billing_info}` |
| `GET` | `/api/billing/{billing_id}` | Get billing by ID | - | `{billing_info, case_info, lawyer_info}` |
| `PUT` | `/api/billing/{billing_id}` | Update billing | `{hours_worked, hourly_rate, total_amount, status}` | `{billing_info}` |
| `DELETE` | `/api/billing/{billing_id}` | Delete billing | - | `{message}` |
| `GET` | `/api/billing/by-case/{case_id}` | Get billing for case | - | `[{billing_info}]` |
| `GET` | `/api/billing/by-lawyer/{lawyer_id}` | Get billing by lawyer | `?date_from=""&date_to=""` | `[{billing_info}]` |
| `GET` | `/api/billing/pending` | Get pending invoices | - | `[{billing_info}]` |
| `POST` | `/api/billing/{billing_id}/send` | Send invoice | `{email_template}` | `{message}` |

### Payments
| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/api/payments` | Get all payments | `?billing_id=""&payment_status=""&date_from=""&date_to=""` | `[{payment_info}]` |
| `POST` | `/api/payments` | Record payment | `{billing_id, amount_paid, payment_method, transaction_id, payment_date}` | `{payment_id, payment_info}` |
| `GET` | `/api/payments/{payment_id}` | Get payment by ID | - | `{payment_info}` |
| `PUT` | `/api/payments/{payment_id}` | Update payment | `{amount_paid, payment_status, notes}` | `{payment_info}` |
| `GET` | `/api/payments/by-billing/{billing_id}` | Get payments for invoice | - | `[{payment_info}]` |

### Financial Reports
| Method | Endpoint | Description | Parameters | Response |
|--------|----------|-------------|------------|----------|
| `GET` | `/api/reports/revenue` | Revenue reports | `?period=""&lawyer_id=""&date_from=""&date_to=""` | `{total_revenue, revenue_by_period, revenue_by_lawyer}` |
| `GET` | `/api/reports/outstanding` | Outstanding payments | `?overdue_only=false` | `{total_outstanding, overdue_amount, outstanding_invoices}` |
| `GET` | `/api/reports/lawyer-billing` | Billing by lawyer | `?date_from=""&date_to=""` | `[{lawyer_info, total_billed, total_hours}]` |

---

## 📊 Activity Tracking APIs

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/api/activities` | Get all activities | `?case_id=""&lawyer_id=""&date_from=""&date_to=""&is_billable=""` | `[{activity_info}]` |
| `POST` | `/api/activities` | Log new activity | `{case_id, lawyer_id, activity_type, description, hours_spent, activity_date, is_billable}` | `{activity_id, activity_info}` |
| `GET` | `/api/activities/{activity_id}` | Get activity by ID | - | `{activity_info}` |
| `PUT` | `/api/activities/{activity_id}` | Update activity | `{activity_type, description, hours_spent, is_billable}` | `{activity_info}` |
| `DELETE` | `/api/activities/{activity_id}` | Delete activity | - | `{message}` |
| `GET` | `/api/activities/by-case/{case_id}` | Get activities for case | - | `[{activity_info}]` |
| `GET` | `/api/activities/by-lawyer/{lawyer_id}` | Get activities by lawyer | `?date_from=""&date_to=""` | `[{activity_info}]` |
| `GET` | `/api/activities/billable` | Get billable activities | `?lawyer_id=""&date_from=""&date_to=""&billed=false` | `[{activity_info}]` |
| `GET` | `/api/activities/timesheet` | Generate timesheet | `?lawyer_id=""&date_from=""&date_to=""` | `{timesheet_data}` |

---

## ⚖️ Court Hearing APIs

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/api/hearings` | Get all court hearings | `?case_id=""&lawyer_id=""&status=""&date_from=""&date_to=""` | `[{hearing_info}]` |
| `POST` | `/api/hearings` | Schedule hearing | `{case_id, lawyer_id, hearing_type, scheduled_date, court_name, judge_name}` | `{hearing_id, hearing_info}` |
| `GET` | `/api/hearings/{hearing_id}` | Get hearing by ID | - | `{hearing_info}` |
| `PUT` | `/api/hearings/{hearing_id}` | Update hearing | `{scheduled_date, court_name, judge_name, status}` | `{hearing_info}` |
| `DELETE` | `/api/hearings/{hearing_id}` | Cancel hearing | - | `{message}` |
| `GET` | `/api/hearings/upcoming` | Get upcoming hearings | `?days=30&lawyer_id=""` | `[{hearing_info}]` |
| `GET` | `/api/hearings/by-case/{case_id}` | Get hearings for case | - | `[{hearing_info}]` |
| `GET` | `/api/hearings/by-lawyer/{lawyer_id}` | Get hearings for lawyer | `?date_from=""&date_to=""` | `[{hearing_info}]` |
| `PUT` | `/api/hearings/{hearing_id}/outcome` | Record hearing outcome | `{outcome, notes, status}` | `{hearing_info}` |

---

## 💬 Communication APIs

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/api/communications` | Get all communications | `?case_id=""&from_user_id=""&to_user_id=""&communication_type=""` | `[{communication_info}]` |
| `POST` | `/api/communications` | Send communication | `{case_id, to_user_id, communication_type, subject, content, priority}` | `{communication_id, communication_info}` |
| `GET` | `/api/communications/{comm_id}` | Get communication by ID | - | `{communication_info}` |
| `PUT` | `/api/communications/{comm_id}` | Update communication | `{subject, content, priority}` | `{communication_info}` |
| `DELETE` | `/api/communications/{comm_id}` | Delete communication | - | `{message}` |
| `GET` | `/api/communications/by-case/{case_id}` | Get case communications | - | `[{communication_info}]` |
| `GET` | `/api/communications/unread` | Get unread communications | - | `[{communication_info}]` |
| `PUT` | `/api/communications/{comm_id}/read` | Mark as read | - | `{communication_info}` |

---

## 🏢 Firm Settings & Configuration APIs

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/api/settings` | Get all firm settings | - | `{settings_object}` |
| `PUT` | `/api/settings` | Update firm settings | `{setting_key: value}` | `{settings_object}` |
| `GET` | `/api/settings/{key}` | Get specific setting | - | `{setting_value}` |
| `PUT` | `/api/settings/{key}` | Update specific setting | `{value}` | `{setting_info}` |
| `GET` | `/api/settings/branding` | Get firm branding settings | - | `{branding_info}` |
| `PUT` | `/api/settings/branding` | Update firm branding | `{firm_name, logo_url, color_scheme, address}` | `{branding_info}` |

---

## 📈 Dashboard & Analytics APIs

| Method | Endpoint | Description | Parameters | Response |
|--------|----------|-------------|------------|----------|
| `GET` | `/api/dashboard/stats` | Dashboard statistics | - | `{total_cases, active_deadlines, recent_activities, revenue_this_month}` |
| `GET` | `/api/dashboard/recent-activities` | Recent activities | `?limit=10` | `[{activity_info}]` |
| `GET` | `/api/dashboard/upcoming-deadlines` | Upcoming deadlines | `?limit=5` | `[{deadline_info}]` |
| `GET` | `/api/dashboard/case-overview` | Case overview stats | - | `{cases_by_status, cases_by_priority, cases_by_type}` |
| `GET` | `/api/analytics/cases` | Case analytics | `?period=""&lawyer_id=""` | `{case_trends, completion_rates, case_types_distribution}` |
| `GET` | `/api/analytics/revenue` | Revenue analytics | `?period=""&lawyer_id=""` | `{revenue_trends, revenue_by_case_type, revenue_by_lawyer}` |
| `GET` | `/api/analytics/lawyer-performance` | Lawyer performance metrics | `?lawyer_id=""&period=""` | `{cases_handled, hours_billed, success_rate}` |
| `GET` | `/api/analytics/client-satisfaction` | Client satisfaction metrics | `?period=""` | `{satisfaction_scores, feedback_summary}` |

---

## 🔍 Search & Filter APIs

| Method | Endpoint | Description | Parameters | Response |
|--------|----------|-------------|------------|----------|
| `GET` | `/api/search/global` | Global search across all entities | `?query=""&entity_types=["cases","clients","documents"]` | `{cases, clients, documents, lawyers}` |
| `GET` | `/api/search/cases` | Advanced case search | `?query=""&status=""&priority=""&case_type=""&lawyer_id=""&client_id=""` | `[{case_info}]` |
| `GET` | `/api/search/clients` | Advanced client search | `?query=""&country=""&status=""&lawyer_id=""` | `[{client_info}]` |
| `GET` | `/api/search/documents` | Advanced document search | `?query=""&document_type=""&case_id=""&date_from=""&date_to=""` | `[{document_info}]` |
| `GET` | `/api/filters/cases` | Get case filter options | - | `{statuses, priorities, case_types, lawyers}` |
| `GET` | `/api/filters/clients` | Get client filter options | - | `{countries, statuses, lawyers}` |

---

## 🔔 Notification APIs

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/api/notifications` | Get user notifications | `?is_read=false&type=""&limit=20` | `[{notification_info}]` |
| `POST` | `/api/notifications` | Create notification | `{user_id, type, title, message, related_entity_id}` | `{notification_id, notification_info}` |
| `PUT` | `/api/notifications/{notif_id}/read` | Mark notification as read | - | `{notification_info}` |
| `DELETE` | `/api/notifications/{notif_id}` | Delete notification | - | `{message}` |
| `GET` | `/api/notifications/unread` | Get unread notifications count | - | `{unread_count}` |

---

## 📤 Export & Import APIs

| Method | Endpoint | Description | Parameters | Response |
|--------|----------|-------------|------------|----------|
| `GET` | `/api/export/cases` | Export cases to CSV/Excel | `?format=csv&date_from=""&date_to=""&status=""` | `File Download` |
| `GET` | `/api/export/clients` | Export clients to CSV/Excel | `?format=excel&lawyer_id=""` | `File Download` |
| `GET` | `/api/export/billing` | Export billing data | `?format=csv&date_from=""&date_to=""&lawyer_id=""` | `File Download` |
| `POST` | `/api/import/clients` | Import clients from CSV/Excel | `{file, mapping_config}` | `{imported_count, errors}` |
| `POST` | `/api/import/cases` | Import cases from CSV/Excel | `{file, mapping_config}` | `{imported_count, errors}` |

---

## 🔧 System & Health APIs

| Method | Endpoint | Description | Access Level | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/api/health` | Health check | Public | `{status, database_status, version}` |
| `GET` | `/api/version` | API version info | Public | `{version, build_date, environment}` |
| `GET` | `/api/backup` | Trigger database backup | Admin only | `{backup_file, backup_date}` |
| `GET` | `/api/logs` | System logs | Admin only | `[{log_entry}]` |

---

## 📋 API Implementation Priority

### **Phase 1 (Core MVP) - Weeks 1-2**
1. ✅ Authentication & Authorization APIs
2. ✅ User Management (Users, Lawyers, Clients)
3. ✅ Basic Case Management
4. ✅ Dashboard Stats API

### **Phase 2 (Essential Features) - Weeks 3-4**
1. ✅ Deadline Management APIs
2. ✅ Document Management APIs
3. ✅ Basic Billing APIs
4. ✅ Activity Tracking APIs

### **Phase 3 (Advanced Features) - Weeks 5-6**
1. ✅ Court Hearings APIs
2. ✅ Communications APIs
3. ✅ Advanced Analytics APIs
4. ✅ Export/Import APIs

### **Phase 4 (Enterprise Features) - Weeks 7-8**
1. ✅ Advanced Reporting APIs
2. ✅ Notifications APIs
3. ✅ Firm Settings APIs
4. ✅ System Administration APIs

---

## 🔐 Security Considerations

### Authentication
- **JWT Tokens** with refresh token rotation
- **Password hashing** using bcrypt
- **Role-based access control** (RBAC)
- **API rate limiting** to prevent abuse

### Data Protection
- **Input validation** on all endpoints
- **SQL injection** prevention using parameterized queries
- **File upload security** with type and size validation
- **Confidential document** access controls

### Database Security
- **Connection string encryption**
- **Database user permissions** (least privilege)
- **Audit logging** for sensitive operations
- **Regular backups** with encryption

---

## 📊 Response Format Standards

### Success Response
```json
{
  "success": true,
  "data": {...},
  "message": "Operation completed successfully",
  "timestamp": "2025-08-29T10:30:00Z"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {...}
  },
  "timestamp": "2025-08-29T10:30:00Z"
}
```

### Pagination Response
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 150,
    "pages": 15
  }
}
```

---

**Document Version:** 1.0  
**Last Updated:** August 29, 2025  
**Technology Stack:** SQL Server Express + FastAPI + React.js
