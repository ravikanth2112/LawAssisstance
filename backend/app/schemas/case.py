"""
Case schemas for API requests and responses
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.case import CaseStatus, CasePriority

class CaseBase(BaseModel):
    case_type: str = Field(..., max_length=100)
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    priority: CasePriority = CasePriority.MEDIUM
    deadline: Optional[datetime] = None
    estimated_cost: Optional[Decimal] = Field(None, ge=0)

class CaseCreate(CaseBase):
    client_id: int
    lawyer_id: int
    case_number: Optional[str] = Field(None, max_length=50)

class CaseUpdate(BaseModel):
    case_type: Optional[str] = Field(None, max_length=100)
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[CaseStatus] = None
    priority: Optional[CasePriority] = None
    deadline: Optional[datetime] = None
    filed_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    estimated_cost: Optional[Decimal] = Field(None, ge=0)
    actual_cost: Optional[Decimal] = Field(None, ge=0)
    progress_percentage: Optional[int] = Field(None, ge=0, le=100)
    notes: Optional[str] = None

class CaseResponse(CaseBase):
    id: int
    client_id: int
    lawyer_id: int
    case_number: str
    status: CaseStatus
    filed_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    actual_cost: Optional[Decimal] = None
    progress_percentage: int
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CaseWithDetails(CaseResponse):
    client_name: str
    lawyer_name: str
