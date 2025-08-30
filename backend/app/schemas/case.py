from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from decimal import Decimal
from enum import Enum

class CaseStatus(str, Enum):
    ACTIVE = "active"
    PENDING = "pending"
    COMPLETED = "completed"
    CLOSED = "closed"
    ON_HOLD = "on_hold"

class CasePriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

# Case schemas
class CaseBase(BaseModel):
    case_number: str
    case_type: str
    case_status: CaseStatus = CaseStatus.ACTIVE
    priority_level: CasePriority = CasePriority.MEDIUM
    filing_date: Optional[date] = None
    expected_completion: Optional[date] = None
    estimated_cost: Optional[Decimal] = None
    case_summary: Optional[str] = None

class CaseCreate(CaseBase):
    client_id: int
    primary_lawyer_id: int

class CaseUpdate(BaseModel):
    case_status: Optional[CaseStatus] = None
    priority_level: Optional[CasePriority] = None
    filing_date: Optional[date] = None
    expected_completion: Optional[date] = None
    estimated_cost: Optional[Decimal] = None
    case_summary: Optional[str] = None

class CaseResponse(CaseBase):
    case_id: int
    client_id: int
    primary_lawyer_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Case with related data
class CaseWithDetails(CaseResponse):
    client: Optional[dict] = None
    primary_lawyer: Optional[dict] = None
