"""
Deadline schemas for API requests and responses
"""

from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date

class DeadlineCreate(BaseModel):
    case_id: int
    lawyer_id: int
    deadline_type: str
    title: str
    description: Optional[str] = None
    due_date: date
    priority_level: str  # urgent, high, medium, low
    is_court_deadline: bool = False

class DeadlineUpdate(BaseModel):
    deadline_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority_level: Optional[str] = None
    is_court_deadline: Optional[bool] = None
    status: Optional[str] = None
    completion_notes: Optional[str] = None

class DeadlineComplete(BaseModel):
    completion_notes: Optional[str] = None

class DeadlineResponse(BaseModel):
    deadline_id: int
    case_id: int
    lawyer_id: int
    deadline_type: str
    title: str
    description: Optional[str] = None
    due_date: date
    priority_level: str
    status: str
    is_court_deadline: bool
    completed_date: Optional[date] = None
    completion_notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    
    # Computed properties
    is_overdue: bool = False
    days_remaining: int = 0
    
    # Related objects (if populated)
    case: Optional['CaseResponse'] = None
    lawyer: Optional['LawyerResponse'] = None

    class Config:
        from_attributes = True
        
    @property
    def id(self):
        return self.deadline_id

# Import here to avoid circular import
from app.schemas.case import CaseResponse
from app.schemas.lawyer import LawyerResponse
DeadlineResponse.model_rebuild()
