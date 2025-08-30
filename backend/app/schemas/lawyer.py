from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

# Lawyer schemas
class LawyerBase(BaseModel):
    bar_number: str
    license_state: str
    specialization: Optional[str] = None
    hourly_rate: Optional[Decimal] = None
    bio: Optional[str] = None
    admitted_date: Optional[date] = None
    is_partner: bool = False

class LawyerCreate(LawyerBase):
    user_id: int

class LawyerUpdate(BaseModel):
    bar_number: Optional[str] = None
    license_state: Optional[str] = None
    specialization: Optional[str] = None
    hourly_rate: Optional[Decimal] = None
    bio: Optional[str] = None
    admitted_date: Optional[date] = None
    is_partner: Optional[bool] = None

class LawyerResponse(LawyerBase):
    lawyer_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Lawyer with user details
class LawyerWithUser(LawyerResponse):
    user: Optional[dict] = None
