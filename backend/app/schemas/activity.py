"""
Activity schemas for API requests and responses
"""

from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class ActivityCreate(BaseModel):
    case_id: int
    lawyer_id: int
    activity_type: str
    title: str
    description: str
    activity_date: datetime
    hours_spent: Decimal
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_billable: bool = True
    hourly_rate: Optional[Decimal] = None

class ActivityUpdate(BaseModel):
    activity_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    activity_date: Optional[datetime] = None
    hours_spent: Optional[Decimal] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_billable: Optional[bool] = None
    hourly_rate: Optional[Decimal] = None
    status: Optional[str] = None

class ActivityResponse(BaseModel):
    activity_id: int
    case_id: int
    lawyer_id: int
    activity_type: str
    title: str
    description: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    hours_spent: Decimal
    is_billable: bool
    hourly_rate: Optional[Decimal] = None
    billed_amount: Optional[Decimal] = None
    billing_status: str
    status: str
    activity_date: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Computed properties
    duration_hours: float = 0
    
    # Related objects (if populated)
    case: Optional['CaseResponse'] = None
    lawyer: Optional['LawyerResponse'] = None

    class Config:
        from_attributes = True
        
    @property
    def id(self):
        return self.activity_id

# Import here to avoid circular import
from app.schemas.case import CaseResponse
from app.schemas.lawyer import LawyerResponse
ActivityResponse.model_rebuild()
