"""
User schemas for API requests and responses
"""

from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: 'UserResponse'

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    user_type: str  # "admin", "lawyer", "client"

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    user_type: Optional[str] = None

class UserResponse(BaseModel):
    user_id: int
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    user_type: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        
    @property
    def id(self):
        return self.user_id
        
    @property
    def role(self):
        return self.user_type
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

# Update forward references
LoginResponse.model_rebuild()
