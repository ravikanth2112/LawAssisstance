"""
User model for authentication
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    LAWYER = "lawyer"
    CLIENT = "client"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    user_type = Column(String(6), nullable=False)  # Using String instead of Enum to match DB
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Add property for backward compatibility
    @property
    def id(self):
        return self.user_id
    
    @property
    def role(self):
        return self.user_type

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
