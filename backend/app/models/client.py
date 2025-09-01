"""
Client model
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class ClientStatus(str, enum.Enum):
    ACTIVE = "active"
    PENDING = "pending"
    COMPLETED = "completed"
    INACTIVE = "inactive"

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=True)  # Not all clients need user accounts
    lawyer_id = Column(Integer, ForeignKey("lawyers.id"), nullable=False)
    
    # Client information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), index=True)
    phone = Column(String(20))
    address = Column(Text)
    
    # Immigration specific
    country_of_birth = Column(String(100))
    current_status = Column(String(100))
    case_type = Column(String(100))
    
    # Status and tracking
    status = Column(Enum(ClientStatus), default=ClientStatus.ACTIVE)
    last_contact = Column(DateTime(timezone=True))
    notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", backref="client_profile")
    lawyer = relationship("Lawyer", backref="clients")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
