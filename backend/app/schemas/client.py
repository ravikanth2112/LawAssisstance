from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

# Client schemas
class ClientBase(BaseModel):
    client_number: str
    country_of_origin: Optional[str] = None
    current_status: Optional[str] = None
    preferred_language: Optional[str] = None
    date_of_birth: Optional[date] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    notes: Optional[str] = None

class ClientCreate(ClientBase):
    user_id: int

class ClientUpdate(BaseModel):
    country_of_origin: Optional[str] = None
    current_status: Optional[str] = None
    preferred_language: Optional[str] = None
    date_of_birth: Optional[date] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    notes: Optional[str] = None

class ClientResponse(ClientBase):
    client_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Client with user details
class ClientWithUser(ClientResponse):
    user: Optional[dict] = None
