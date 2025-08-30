# SQL Server Database Creation Script for Immigration Law Dashboard

## 1. Database Creation
```sql
-- Create the database
CREATE DATABASE ImmigrationLawDB;
GO

-- Use the database
USE ImmigrationLawDB;
GO
```

## 2. Table Creation

### Users Table
```sql
CREATE TABLE users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    email NVARCHAR(255) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,
    first_name NVARCHAR(100) NOT NULL,
    last_name NVARCHAR(100) NOT NULL,
    phone NVARCHAR(20),
    address NVARCHAR(500),
    city NVARCHAR(100),
    state NVARCHAR(100),
    zip_code NVARCHAR(20),
    country NVARCHAR(100),
    user_type NVARCHAR(20) NOT NULL CHECK (user_type IN ('admin', 'lawyer', 'client')),
    is_active BIT DEFAULT 1,
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    updated_at DATETIME2 DEFAULT GETUTCDATE()
);
GO
```

### Lawyers Table
```sql
CREATE TABLE lawyers (
    lawyer_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    bar_number NVARCHAR(50) NOT NULL UNIQUE,
    specialization NVARCHAR(200),
    years_of_experience INT,
    hourly_rate DECIMAL(10,2),
    bio NVARCHAR(MAX),
    languages_spoken NVARCHAR(500),
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    updated_at DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
GO
```

### Clients Table
```sql
CREATE TABLE clients (
    client_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    client_number NVARCHAR(50) UNIQUE,
    country_of_origin NVARCHAR(100),
    current_status NVARCHAR(100),
    emergency_contact_name NVARCHAR(200),
    emergency_contact_phone NVARCHAR(20),
    emergency_contact_relationship NVARCHAR(100),
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    updated_at DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
GO
```

### Cases Table
```sql
CREATE TABLE cases (
    case_id INT IDENTITY(1,1) PRIMARY KEY,
    client_id INT NOT NULL,
    primary_lawyer_id INT NOT NULL,
    case_number NVARCHAR(50) NOT NULL UNIQUE,
    case_type NVARCHAR(200) NOT NULL,
    case_status NVARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (case_status IN ('active', 'pending', 'completed', 'closed', 'cancelled')),
    priority_level NVARCHAR(20) NOT NULL DEFAULT 'medium' CHECK (priority_level IN ('low', 'medium', 'high', 'urgent')),
    filing_date DATE,
    expected_completion DATE,
    estimated_cost DECIMAL(12,2),
    case_summary NVARCHAR(MAX),
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    updated_at DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (primary_lawyer_id) REFERENCES lawyers(lawyer_id)
);
GO
```

### Deadlines Table
```sql
CREATE TABLE deadlines (
    deadline_id INT IDENTITY(1,1) PRIMARY KEY,
    case_id INT NOT NULL,
    deadline_type NVARCHAR(20) NOT NULL CHECK (deadline_type IN ('filing', 'hearing', 'response', 'interview', 'renewal', 'other')),
    deadline_date DATETIME2 NOT NULL,
    title NVARCHAR(200) NOT NULL,
    description NVARCHAR(MAX),
    is_completed BIT DEFAULT 0,
    reminder_days INT DEFAULT 7,
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    updated_at DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
);
GO
```

### Documents Table
```sql
CREATE TABLE documents (
    document_id INT IDENTITY(1,1) PRIMARY KEY,
    case_id INT NOT NULL,
    document_type NVARCHAR(50) NOT NULL CHECK (document_type IN ('passport', 'visa', 'birth_certificate', 'marriage_certificate', 'diploma', 'employment_letter', 'bank_statement', 'contract', 'correspondence', 'government_form', 'other')),
    document_name NVARCHAR(255) NOT NULL,
    file_path NVARCHAR(500) NOT NULL,
    description NVARCHAR(MAX),
    file_size BIGINT,
    mime_type NVARCHAR(100),
    uploaded_by INT NOT NULL,
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    updated_at DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(user_id)
);
GO
```

### Invoices Table
```sql
CREATE TABLE invoices (
    invoice_id INT IDENTITY(1,1) PRIMARY KEY,
    case_id INT NOT NULL,
    invoice_number NVARCHAR(50) UNIQUE,
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    tax_rate DECIMAL(5,4) DEFAULT 0.0000,
    tax_amount DECIMAL(12,2) DEFAULT 0.00,
    total_amount DECIMAL(12,2) NOT NULL,
    status NVARCHAR(20) NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'sent', 'paid', 'overdue', 'cancelled')),
    notes NVARCHAR(MAX),
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    updated_at DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY (case_id) REFERENCES cases(case_id)
);
GO
```

### Time Entries Table
```sql
CREATE TABLE time_entries (
    entry_id INT IDENTITY(1,1) PRIMARY KEY,
    case_id INT NOT NULL,
    lawyer_id INT NOT NULL,
    description NVARCHAR(MAX) NOT NULL,
    hours_worked DECIMAL(5,2) NOT NULL,
    hourly_rate DECIMAL(10,2),
    date_worked DATE NOT NULL,
    is_billable BIT DEFAULT 1,
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    updated_at DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY (case_id) REFERENCES cases(case_id),
    FOREIGN KEY (lawyer_id) REFERENCES lawyers(lawyer_id)
);
GO
```

### Activity Logs Table
```sql
CREATE TABLE activity_logs (
    activity_id INT IDENTITY(1,1) PRIMARY KEY,
    case_id INT NOT NULL,
    user_id INT NOT NULL,
    activity_type NVARCHAR(50) NOT NULL CHECK (activity_type IN ('case_created', 'case_updated', 'document_uploaded', 'payment_received', 'deadline_added', 'deadline_completed', 'note_added', 'client_communication', 'other')),
    description NVARCHAR(500) NOT NULL,
    details NVARCHAR(MAX),
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY (case_id) REFERENCES cases(case_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
GO
```

### Payments Table
```sql
CREATE TABLE payments (
    payment_id INT IDENTITY(1,1) PRIMARY KEY,
    invoice_id INT NOT NULL,
    payment_amount DECIMAL(12,2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_method NVARCHAR(50),
    transaction_id NVARCHAR(200),
    notes NVARCHAR(MAX),
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id)
);
GO
```

### Communications Table
```sql
CREATE TABLE communications (
    communication_id INT IDENTITY(1,1) PRIMARY KEY,
    case_id INT NOT NULL,
    sender_id INT NOT NULL,
    recipient_id INT,
    subject NVARCHAR(255),
    message NVARCHAR(MAX) NOT NULL,
    communication_type NVARCHAR(20) NOT NULL CHECK (communication_type IN ('email', 'phone', 'meeting', 'note')),
    is_internal BIT DEFAULT 0,
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY (case_id) REFERENCES cases(case_id),
    FOREIGN KEY (sender_id) REFERENCES users(user_id),
    FOREIGN KEY (recipient_id) REFERENCES users(user_id)
);
GO
```

### Case Assignments Table (Many-to-Many for multiple lawyers per case)
```sql
CREATE TABLE case_assignments (
    assignment_id INT IDENTITY(1,1) PRIMARY KEY,
    case_id INT NOT NULL,
    lawyer_id INT NOT NULL,
    role NVARCHAR(50) NOT NULL DEFAULT 'associate',
    assigned_date DATE DEFAULT CAST(GETUTCDATE() AS DATE),
    is_active BIT DEFAULT 1,
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE,
    FOREIGN KEY (lawyer_id) REFERENCES lawyers(lawyer_id),
    UNIQUE(case_id, lawyer_id)
);
GO
```

## 3. Indexes for Performance

```sql
-- User indexes
CREATE INDEX IX_users_email ON users(email);
CREATE INDEX IX_users_user_type ON users(user_type);
CREATE INDEX IX_users_is_active ON users(is_active);

-- Case indexes
CREATE INDEX IX_cases_client_id ON cases(client_id);
CREATE INDEX IX_cases_primary_lawyer_id ON cases(primary_lawyer_id);
CREATE INDEX IX_cases_case_status ON cases(case_status);
CREATE INDEX IX_cases_priority_level ON cases(priority_level);
CREATE INDEX IX_cases_case_number ON cases(case_number);
CREATE INDEX IX_cases_created_at ON cases(created_at);

-- Deadline indexes
CREATE INDEX IX_deadlines_case_id ON deadlines(case_id);
CREATE INDEX IX_deadlines_deadline_date ON deadlines(deadline_date);
CREATE INDEX IX_deadlines_is_completed ON deadlines(is_completed);

-- Document indexes
CREATE INDEX IX_documents_case_id ON documents(case_id);
CREATE INDEX IX_documents_uploaded_by ON documents(uploaded_by);

-- Invoice indexes
CREATE INDEX IX_invoices_case_id ON invoices(case_id);
CREATE INDEX IX_invoices_status ON invoices(status);
CREATE INDEX IX_invoices_invoice_date ON invoices(invoice_date);

-- Activity log indexes
CREATE INDEX IX_activity_logs_case_id ON activity_logs(case_id);
CREATE INDEX IX_activity_logs_user_id ON activity_logs(user_id);
CREATE INDEX IX_activity_logs_created_at ON activity_logs(created_at);
```

## 4. Triggers for Automatic Updates

```sql
-- Trigger to update updated_at timestamp on users table
CREATE TRIGGER TR_users_updated_at ON users
AFTER UPDATE
AS
BEGIN
    UPDATE users 
    SET updated_at = GETUTCDATE()
    FROM users u
    INNER JOIN inserted i ON u.user_id = i.user_id;
END;
GO

-- Trigger to update updated_at timestamp on lawyers table
CREATE TRIGGER TR_lawyers_updated_at ON lawyers
AFTER UPDATE
AS
BEGIN
    UPDATE lawyers 
    SET updated_at = GETUTCDATE()
    FROM lawyers l
    INNER JOIN inserted i ON l.lawyer_id = i.lawyer_id;
END;
GO

-- Trigger to update updated_at timestamp on clients table
CREATE TRIGGER TR_clients_updated_at ON clients
AFTER UPDATE
AS
BEGIN
    UPDATE clients 
    SET updated_at = GETUTCDATE()
    FROM clients c
    INNER JOIN inserted i ON c.client_id = i.client_id;
END;
GO

-- Trigger to update updated_at timestamp on cases table
CREATE TRIGGER TR_cases_updated_at ON cases
AFTER UPDATE
AS
BEGIN
    UPDATE cases 
    SET updated_at = GETUTCDATE()
    FROM cases c
    INNER JOIN inserted i ON c.case_id = i.case_id;
END;
GO
```

## 5. Sample Data for Testing

```sql
-- Insert sample admin user
INSERT INTO users (email, password_hash, first_name, last_name, user_type) 
VALUES ('admin@lawfirm.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4wGD3MQZ7K', 'System', 'Admin', 'admin');

-- Insert sample lawyer
INSERT INTO users (email, password_hash, first_name, last_name, phone, user_type) 
VALUES ('lawyer1@lawfirm.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4wGD3MQZ7K', 'John', 'Smith', '555-0123', 'lawyer');

INSERT INTO lawyers (user_id, bar_number, specialization, years_of_experience, hourly_rate) 
VALUES (2, 'BAR123456', 'Immigration Law', 10, 350.00);

-- Insert sample client
INSERT INTO users (email, password_hash, first_name, last_name, phone, user_type) 
VALUES ('client1@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4wGD3MQZ7K', 'Maria', 'Garcia', '555-0456', 'client');

INSERT INTO clients (user_id, client_number, country_of_origin, current_status) 
VALUES (3, 'CL001', 'Mexico', 'Pending Green Card');

-- Insert sample case
INSERT INTO cases (client_id, primary_lawyer_id, case_number, case_type, case_status, priority_level, estimated_cost, case_summary) 
VALUES (1, 1, 'CS20241201ABCD1234', 'Family-based Green Card', 'active', 'high', 5000.00, 'Green card application for spouse of US citizen');
```

## 6. Connection String for FastAPI

Add this to your `.env` file:

```
DATABASE_URL=mssql+pyodbc://username:password@server_name/ImmigrationLawDB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes
```

For local SQL Server Express:
```
DATABASE_URL=mssql+pyodbc://./SQLEXPRESS/ImmigrationLawDB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes
```

## 7. Required Python Packages

Add to requirements.txt:
```
pyodbc==4.0.35
```

This script creates a comprehensive database structure that supports all the features in your immigration law dashboard. The database includes proper relationships, constraints, indexes for performance, and triggers for automatic timestamp updates.
