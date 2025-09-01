"""
Client schemas for API requests and responses
"""

from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date

class ClientCreate(BaseModel):
    user_id: Optional[int] = None
    client_number: str
    country_of_origin: Optional[str] = None
    current_status: Optional[str] = None
    preferred_language: Optional[str] = None
    date_of_birth: Optional[date] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    notes: Optional[str] = None

class ClientUpdate(BaseModel):
    client_number: Optional[str] = None
    country_of_origin: Optional[str] = None
    current_status: Optional[str] = None
    preferred_language: Optional[str] = None
    date_of_birth: Optional[date] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    notes: Optional[str] = None

class ClientResponse(BaseModel):
    client_id: int
    user_id: Optional[int] = None
    client_number: str
    country_of_origin: Optional[str] = None
    current_status: Optional[str] = None
    preferred_language: Optional[str] = None
    date_of_birth: Optional[date] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # User details (if populated via relationship)
    user: Optional['UserResponse'] = None

    class Config:
        from_attributes = True
        
    @property
    def id(self):
        return self.client_id
    
    @property
    def full_name(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}"
        return "Unknown"

# Import here to avoid circular import
from app.schemas.user import UserResponse
ClientResponse.model_rebuild()
