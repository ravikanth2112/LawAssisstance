from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

# User-related schemas
class UserType(str, Enum):
    ADMIN = "admin"
    LAWYER = "lawyer"
    CLIENT = "client"

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    user_type: UserType

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(UserCreate):
    pass

# Lawyer-related schemas
class LawyerBase(BaseModel):
    bar_number: str
    specialization: Optional[str] = None
    years_of_experience: Optional[int] = None
    hourly_rate: Optional[float] = None
    bio: Optional[str] = None
    languages_spoken: Optional[str] = None

class LawyerCreate(LawyerBase):
    user_id: int

class LawyerUpdate(BaseModel):
    bar_number: Optional[str] = None
    specialization: Optional[str] = None
    years_of_experience: Optional[int] = None
    hourly_rate: Optional[float] = None
    bio: Optional[str] = None
    languages_spoken: Optional[str] = None

class LawyerResponse(LawyerBase):
    lawyer_id: int
    user_id: int
    user: UserResponse
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Client-related schemas
class ClientBase(BaseModel):
    client_number: Optional[str] = None
    country_of_origin: Optional[str] = None
    current_status: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None

class ClientCreate(ClientBase):
    user_id: int

class ClientUpdate(BaseModel):
    client_number: Optional[str] = None
    country_of_origin: Optional[str] = None
    current_status: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None

class ClientResponse(ClientBase):
    client_id: int
    user_id: int
    user: UserResponse
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Case-related schemas
class CaseStatus(str, Enum):
    ACTIVE = "active"
    PENDING = "pending"
    COMPLETED = "completed"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class CasePriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class CaseBase(BaseModel):
    client_id: int
    primary_lawyer_id: int
    case_number: Optional[str] = None
    case_type: str
    case_status: CaseStatus = CaseStatus.PENDING
    priority_level: CasePriority = CasePriority.MEDIUM
    filing_date: Optional[datetime] = None
    expected_completion: Optional[datetime] = None
    estimated_cost: Optional[float] = None
    case_summary: Optional[str] = None

class CaseCreate(CaseBase):
    pass

class CaseUpdate(BaseModel):
    client_id: Optional[int] = None
    primary_lawyer_id: Optional[int] = None
    case_type: Optional[str] = None
    case_status: Optional[CaseStatus] = None
    priority_level: Optional[CasePriority] = None
    filing_date: Optional[datetime] = None
    expected_completion: Optional[datetime] = None
    estimated_cost: Optional[float] = None
    case_summary: Optional[str] = None

class CaseResponse(CaseBase):
    case_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CaseWithDetails(CaseResponse):
    client: Optional[ClientResponse] = None
    primary_lawyer: Optional[LawyerResponse] = None

    class Config:
        from_attributes = True

# Deadline-related schemas
class DeadlineType(str, Enum):
    FILING = "filing"
    HEARING = "hearing"
    RESPONSE = "response"
    INTERVIEW = "interview"
    RENEWAL = "renewal"
    OTHER = "other"

class DeadlineBase(BaseModel):
    case_id: int
    deadline_type: DeadlineType
    deadline_date: datetime
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    reminder_days: int = 7

class DeadlineCreate(DeadlineBase):
    pass

class DeadlineUpdate(BaseModel):
    deadline_type: Optional[DeadlineType] = None
    deadline_date: Optional[datetime] = None
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    reminder_days: Optional[int] = None

class DeadlineResponse(DeadlineBase):
    deadline_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Activity log schemas
class ActivityType(str, Enum):
    CASE_CREATED = "case_created"
    CASE_UPDATED = "case_updated"
    DOCUMENT_UPLOADED = "document_uploaded"
    PAYMENT_RECEIVED = "payment_received"
    DEADLINE_ADDED = "deadline_added"
    DEADLINE_COMPLETED = "deadline_completed"
    NOTE_ADDED = "note_added"
    CLIENT_COMMUNICATION = "client_communication"
    OTHER = "other"

class ActivityLogBase(BaseModel):
    case_id: int
    user_id: int
    activity_type: ActivityType
    description: str
    details: Optional[str] = None

class ActivityLogCreate(ActivityLogBase):
    pass

class ActivityLogResponse(ActivityLogBase):
    activity_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Document schemas
class DocumentType(str, Enum):
    PASSPORT = "passport"
    VISA = "visa"
    BIRTH_CERTIFICATE = "birth_certificate"
    MARRIAGE_CERTIFICATE = "marriage_certificate"
    DIPLOMA = "diploma"
    EMPLOYMENT_LETTER = "employment_letter"
    BANK_STATEMENT = "bank_statement"
    CONTRACT = "contract"
    CORRESPONDENCE = "correspondence"
    GOVERNMENT_FORM = "government_form"
    OTHER = "other"

class DocumentBase(BaseModel):
    case_id: int
    document_type: DocumentType
    document_name: str
    description: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None

class DocumentCreate(DocumentBase):
    file_path: str  # This will be set by the upload handler

class DocumentUpdate(BaseModel):
    document_type: Optional[DocumentType] = None
    document_name: Optional[str] = None
    description: Optional[str] = None

class DocumentResponse(DocumentBase):
    document_id: int
    file_path: str
    uploaded_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Billing schemas
class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

class InvoiceBase(BaseModel):
    case_id: int
    invoice_number: Optional[str] = None
    invoice_date: datetime
    due_date: datetime
    subtotal: float
    tax_rate: float = 0.0
    tax_amount: float = 0.0
    total_amount: float
    status: InvoiceStatus = InvoiceStatus.DRAFT
    notes: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(BaseModel):
    invoice_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    subtotal: Optional[float] = None
    tax_rate: Optional[float] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    status: Optional[InvoiceStatus] = None
    notes: Optional[str] = None

class InvoiceResponse(InvoiceBase):
    invoice_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TimeEntryBase(BaseModel):
    case_id: int
    lawyer_id: int
    description: str
    hours_worked: float
    hourly_rate: Optional[float] = None
    date_worked: datetime
    is_billable: bool = True

class TimeEntryCreate(TimeEntryBase):
    pass

class TimeEntryUpdate(BaseModel):
    description: Optional[str] = None
    hours_worked: Optional[float] = None
    hourly_rate: Optional[float] = None
    date_worked: Optional[datetime] = None
    is_billable: Optional[bool] = None

class TimeEntryResponse(TimeEntryBase):
    entry_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Standard API response wrapper
class StandardResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    message: str
    timestamp: datetime
