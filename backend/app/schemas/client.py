"""
Client schemas for API requests and responses
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.client import ClientStatus

class ClientBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    country_of_birth: Optional[str] = Field(None, max_length=100)
    current_status: Optional[str] = Field(None, max_length=100)
    case_type: Optional[str] = Field(None, max_length=100)

class ClientCreate(ClientBase):
    lawyer_id: int
    user_id: Optional[int] = None

class ClientUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    country_of_birth: Optional[str] = Field(None, max_length=100)
    current_status: Optional[str] = Field(None, max_length=100)
    case_type: Optional[str] = Field(None, max_length=100)
    status: Optional[ClientStatus] = None
    notes: Optional[str] = None

class ClientResponse(ClientBase):
    id: int
    lawyer_id: int
    user_id: Optional[int] = None
    status: ClientStatus
    last_contact: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    full_name: str

    class Config:
        from_attributes = True

class ClientWithLawyer(ClientResponse):
    lawyer_name: str
