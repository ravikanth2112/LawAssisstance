"""
Case schemas for API requests and responses
"""

from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal

class CaseCreate(BaseModel):
    client_id: int
    primary_lawyer_id: int
    case_number: str
    case_type: str
    case_status: str
    priority_level: str
    filing_date: Optional[date] = None
    expected_completion: Optional[date] = None
    estimated_cost: Optional[Decimal] = None
    case_summary: Optional[str] = None

class CaseUpdate(BaseModel):
    case_type: Optional[str] = None
    case_status: Optional[str] = None
    priority_level: Optional[str] = None
    filing_date: Optional[date] = None
    expected_completion: Optional[date] = None
    estimated_cost: Optional[Decimal] = None
    case_summary: Optional[str] = None

class CaseResponse(BaseModel):
    case_id: int
    client_id: int
    primary_lawyer_id: int
    case_number: str
    case_type: str
    case_status: str
    priority_level: str
    filing_date: Optional[date] = None
    expected_completion: Optional[date] = None
    estimated_cost: Optional[Decimal] = None
    case_summary: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Related objects (if populated via relationships)
    client: Optional['ClientResponse'] = None
    primary_lawyer: Optional['LawyerResponse'] = None

    class Config:
        from_attributes = True
        
    @property
    def id(self):
        return self.case_id
    
    @property
    def lawyer_id(self):
        return self.primary_lawyer_id
    
    @property
    def status(self):
        return self.case_status
    
    @property
    def priority(self):
        return self.priority_level

# Import here to avoid circular import
from app.schemas.client import ClientResponse
from app.schemas.lawyer import LawyerResponse
CaseResponse.model_rebuild()
