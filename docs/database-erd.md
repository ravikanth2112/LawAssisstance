# Immigration Law Dashboard - Database ERD

## Entity Relationship Diagram

```mermaid
erDiagram
    USERS {
        int user_id PK
        string email UK
        string password_hash
        string first_name
        string last_name
        string phone
        enum user_type "lawyer, client, admin"
        datetime created_at
        datetime updated_at
        boolean is_active
    }

    LAWYERS {
        int lawyer_id PK
        int user_id FK
        string bar_number UK
        string license_state
        string specialization
        decimal hourly_rate
        text bio
        datetime admitted_date
        boolean is_partner
    }

    CLIENTS {
        int client_id PK
        int user_id FK
        string client_number UK
        string country_of_origin
        string current_status
        string preferred_language
        date date_of_birth
        string emergency_contact
        string emergency_phone
        text notes
    }

    CASES {
        int case_id PK
        int client_id FK
        int primary_lawyer_id FK
        string case_number UK
        string case_type
        string case_status
        string priority_level
        date filing_date
        date expected_completion
        decimal estimated_cost
        text case_summary
        datetime created_at
        datetime updated_at
    }

    CASE_LAWYERS {
        int case_lawyer_id PK
        int case_id FK
        int lawyer_id FK
        string role "primary, secondary, consultant"
        date assigned_date
        date removed_date
        boolean is_active
    }

    DEADLINES {
        int deadline_id PK
        int case_id FK
        int assigned_lawyer_id FK
        string title
        text description
        datetime due_date
        string priority "high, medium, low"
        string status "pending, completed, overdue"
        boolean is_court_deadline
        datetime created_at
        datetime completed_at
    }

    DOCUMENTS {
        int document_id PK
        int case_id FK
        int uploaded_by FK
        string document_name
        string document_type
        string file_path
        string file_extension
        int file_size
        string status "draft, final, submitted"
        boolean is_confidential
        datetime uploaded_at
        datetime modified_at
    }

    BILLING {
        int billing_id PK
        int case_id FK
        int lawyer_id FK
        string invoice_number UK
        decimal hours_worked
        decimal hourly_rate
        decimal total_amount
        decimal tax_amount
        string billing_period
        string status "draft, sent, paid, overdue"
        date invoice_date
        date due_date
        date paid_date
        text description
    }

    PAYMENTS {
        int payment_id PK
        int billing_id FK
        decimal amount_paid
        string payment_method
        string transaction_id
        date payment_date
        string payment_status
        text notes
    }

    ACTIVITIES {
        int activity_id PK
        int case_id FK
        int lawyer_id FK
        string activity_type
        text description
        decimal hours_spent
        date activity_date
        datetime logged_at
        boolean is_billable
    }

    COURT_HEARINGS {
        int hearing_id PK
        int case_id FK
        int lawyer_id FK
        string hearing_type
        datetime scheduled_date
        string court_name
        string judge_name
        string status "scheduled, completed, postponed, cancelled"
        text outcome
        text notes
    }

    COMMUNICATIONS {
        int communication_id PK
        int case_id FK
        int from_user_id FK
        int to_user_id FK
        string communication_type "email, call, meeting, letter"
        string subject
        text content
        datetime sent_at
        boolean is_read
        string priority
    }

    FIRM_SETTINGS {
        int setting_id PK
        string setting_key UK
        string setting_value
        string setting_type
        text description
        datetime updated_at
        int updated_by FK
    }

    %% Relationships
    USERS ||--o{ LAWYERS : "is_a"
    USERS ||--o{ CLIENTS : "is_a"
    USERS ||--o{ COMMUNICATIONS : "sends"
    USERS ||--o{ COMMUNICATIONS : "receives"
    USERS ||--o{ DOCUMENTS : "uploads"
    USERS ||--o{ FIRM_SETTINGS : "updates"

    LAWYERS ||--o{ CASES : "primary_lawyer"
    LAWYERS ||--o{ CASE_LAWYERS : "assigned_to"
    LAWYERS ||--o{ DEADLINES : "assigned_to"
    LAWYERS ||--o{ BILLING : "bills_for"
    LAWYERS ||--o{ ACTIVITIES : "performs"
    LAWYERS ||--o{ COURT_HEARINGS : "represents"

    CLIENTS ||--o{ CASES : "owns"

    CASES ||--o{ CASE_LAWYERS : "has_lawyers"
    CASES ||--o{ DEADLINES : "has_deadlines"
    CASES ||--o{ DOCUMENTS : "contains"
    CASES ||--o{ BILLING : "generates_billing"
    CASES ||--o{ ACTIVITIES : "has_activities"
    CASES ||--o{ COURT_HEARINGS : "has_hearings"
    CASES ||--o{ COMMUNICATIONS : "relates_to"

    BILLING ||--o{ PAYMENTS : "receives_payments"
```

## Table Descriptions

### Core User Management
- **USERS**: Base authentication and user profile information
- **LAWYERS**: Legal professionals with credentials and specializations
- **CLIENTS**: Immigration clients with country of origin and status tracking

### Case Management
- **CASES**: Central case tracking with status, priority, and financial estimates
- **CASE_LAWYERS**: Junction table for multiple lawyers assigned to cases
- **DEADLINES**: Court deadlines and internal milestones with priority tracking

### Document Management
- **DOCUMENTS**: File storage with metadata, confidentiality, and version control
- **COMMUNICATIONS**: Multi-channel communication tracking between users

### Financial Management
- **BILLING**: Time-based billing with invoice generation and status tracking
- **PAYMENTS**: Payment processing and transaction management
- **ACTIVITIES**: Billable hour tracking and detailed case activity logging

### Legal Process Management
- **COURT_HEARINGS**: Court appearance scheduling and outcome tracking

### System Configuration
- **FIRM_SETTINGS**: Configurable system settings and firm branding options

## Key Relationships

1. **User Inheritance**: LAWYERS and CLIENTS inherit from USERS (1:1)
2. **Case Ownership**: Each CASE belongs to one CLIENT but can have multiple LAWYERS
3. **Document Security**: DOCUMENTS are linked to CASES with confidentiality controls
4. **Financial Tracking**: BILLING links to CASES and LAWYERS, with PAYMENTS tracking settlements
5. **Activity Logging**: All ACTIVITIES are tracked per CASE and LAWYER for billing accuracy
6. **Communication History**: All COMMUNICATIONS are preserved with case context

## Data Integrity Features

- Primary Keys (PK) ensure unique record identification
- Foreign Keys (FK) maintain referential integrity
- Unique Keys (UK) prevent duplicate critical data
- Enum constraints on status fields ensure data consistency
- Timestamp tracking for audit trails
