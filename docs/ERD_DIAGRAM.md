# 🏗️ Immigration Law Dashboard - Entity Relationship Diagram (ERD)

## Database Schema Overview

This document contains the Entity Relationship Diagram and database schema for the Immigration Law Dashboard system.

---

## 📊 Core Entities & Relationships

### **Phase 1 Entities**

```mermaid
erDiagram
    USERS ||--o{ LAWYERS : "one-to-many"
    USERS ||--o{ CLIENTS : "one-to-many"
    LAWYERS ||--o{ CASES : "assigned_to"
    CLIENTS ||--o{ CASES : "belongs_to"
    
    USERS {
        int id PK
        string username
        string email
        string password_hash
        string first_name
        string last_name
        string phone
        enum role
        datetime created_at
        datetime updated_at
        boolean is_active
    }
    
    LAWYERS {
        int id PK
        int user_id FK
        string bar_number
        string specialization
        decimal hourly_rate
        text bio
        datetime created_at
        datetime updated_at
    }
    
    CLIENTS {
        int id PK
        int user_id FK
        string country_of_origin
        string immigration_status
        string preferred_language
        datetime created_at
        datetime updated_at
    }
    
    CASES {
        int id PK
        int client_id FK
        int lawyer_id FK
        string case_number
        string case_type
        string title
        text description
        enum status
        enum priority
        datetime created_at
        datetime updated_at
        datetime deadline_date
    }
```

### **Phase 2 Entities**

```mermaid
erDiagram
    CASES ||--o{ DEADLINES : "has"
    CASES ||--o{ DOCUMENTS : "contains"
    CASES ||--o{ BILLING : "generates"
    CASES ||--o{ ACTIVITIES : "tracks"
    LAWYERS ||--o{ ACTIVITIES : "performs"
    
    DEADLINES {
        int id PK
        int case_id FK
        string title
        text description
        datetime due_date
        enum priority
        enum status
        datetime created_at
        datetime updated_at
        boolean is_overdue
    }
    
    DOCUMENTS {
        int id PK
        int case_id FK
        string title
        string file_name
        string file_path
        string file_type
        int file_size
        enum confidentiality_level
        datetime uploaded_at
        datetime updated_at
    }
    
    BILLING {
        int id PK
        int case_id FK
        string invoice_number
        decimal amount
        text description
        enum status
        datetime due_date
        datetime created_at
        datetime updated_at
        boolean is_overdue
    }
    
    ACTIVITIES {
        int id PK
        int case_id FK
        int lawyer_id FK
        string activity_type
        text description
        decimal hours_worked
        decimal billable_rate
        boolean is_billable
        datetime activity_date
        datetime created_at
    }
```

---

## 🔗 Relationship Details

### **User Management**
- **Users** → **Lawyers**: One-to-Many (A user can be a lawyer)
- **Users** → **Clients**: One-to-Many (A user can be a client)

### **Case Management** 
- **Lawyers** → **Cases**: One-to-Many (A lawyer can handle multiple cases)
- **Clients** → **Cases**: One-to-Many (A client can have multiple cases)

### **Phase 2 Relationships**
- **Cases** → **Deadlines**: One-to-Many (A case can have multiple deadlines)
- **Cases** → **Documents**: One-to-Many (A case can have multiple documents)
- **Cases** → **Billing**: One-to-Many (A case can have multiple billing records)
- **Cases** → **Activities**: One-to-Many (A case can have multiple activities)
- **Lawyers** → **Activities**: One-to-Many (A lawyer can perform multiple activities)

---

## 📋 Field Specifications

### **Enums & Status Values**

#### User Roles
- `admin` - System administrator
- `lawyer` - Legal practitioner
- `client` - Client user

#### Case Status
- `open` - Active case
- `in_progress` - Case being worked on
- `closed` - Completed case
- `on_hold` - Temporarily paused

#### Case Priority
- `low` - Low priority
- `medium` - Medium priority
- `high` - High priority
- `urgent` - Urgent priority

#### Deadline Status
- `pending` - Not yet due
- `completed` - Finished
- `overdue` - Past due date

#### Billing Status
- `pending` - Invoice created
- `sent` - Invoice sent to client
- `paid` - Payment received
- `overdue` - Past due date
- `cancelled` - Invoice cancelled

#### Document Confidentiality
- `public` - No restrictions
- `confidential` - Restricted access
- `highly_confidential` - Highly restricted

---

## 🔧 Technical Implementation

### **Database Engine**
- **Primary**: SQL Server Express
- **ORM**: SQLAlchemy
- **Migration**: Alembic

### **Key Features**
- **Foreign Key Constraints**: Enforced referential integrity
- **Computed Properties**: Automatic status calculations
- **Timestamps**: Created/updated tracking
- **Soft Deletes**: Data preservation
- **Indexing**: Optimized query performance

---

## 📊 Data Flow

```
1. User Registration → User Table
2. Role Assignment → Lawyer/Client Table
3. Case Creation → Case Table
4. Case Activities → Deadlines, Documents, Billing, Activities Tables
5. Status Updates → Automatic computed properties
```

---

## 🔄 Database Migrations

All schema changes are version-controlled through:
- SQLAlchemy model definitions
- Automatic table creation on startup
- Foreign key relationship enforcement

---

**Last Updated**: September 2025  
**Version**: 2.0 (Phase 1 + Phase 2 Complete)  
**Total Tables**: 9 entities
