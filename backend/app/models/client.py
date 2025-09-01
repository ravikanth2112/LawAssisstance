"""
Client model
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Client(Base):
    __tablename__ = "clients"

    client_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True, nullable=True)
    client_number = Column(String(50), unique=True)
    country_of_origin = Column(String(100))
    current_status = Column(String(100))
    preferred_language = Column(String(50))
    date_of_birth = Column(Date)
    emergency_contact = Column(String(200))
    emergency_phone = Column(String(20))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", backref="client_profile")
    
    # Add property for backward compatibility
    @property
    def id(self):
        return self.client_id

    @property
    def full_name(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}"
        return "N/A"
