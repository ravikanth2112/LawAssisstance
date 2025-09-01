"""
Lawyer schemas for API requests and responses
"""

from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class LawyerCreate(BaseModel):
    user_id: int
    bar_number: str
    license_state: str
    specialization: Optional[str] = None
    hourly_rate: Optional[Decimal] = None
    bio: Optional[str] = None
    admitted_date: Optional[datetime] = None
    is_partner: bool = False

class LawyerUpdate(BaseModel):
    bar_number: Optional[str] = None
    license_state: Optional[str] = None
    specialization: Optional[str] = None
    hourly_rate: Optional[Decimal] = None
    bio: Optional[str] = None
    admitted_date: Optional[datetime] = None
    is_partner: Optional[bool] = None

class LawyerResponse(BaseModel):
    lawyer_id: int
    user_id: int
    bar_number: Optional[str] = None
    license_state: Optional[str] = None
    specialization: Optional[str] = None
    hourly_rate: Optional[Decimal] = None
    bio: Optional[str] = None
    admitted_date: Optional[datetime] = None
    is_partner: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # User details (if populated via relationship)
    user: Optional['UserResponse'] = None

    class Config:
        from_attributes = True
        
    @property
    def id(self):
        return self.lawyer_id
    
    @property
    def full_name(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}"
        return "Unknown"

# Import here to avoid circular import
from app.schemas.user import UserResponse
LawyerResponse.model_rebuild()
