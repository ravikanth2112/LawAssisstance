"""
Immigration case model
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class CaseStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    WAITING_RESPONSE = "waiting_response"
    APPROVED = "approved"
    DENIED = "denied"
    COMPLETED = "completed"

class CasePriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    lawyer_id = Column(Integer, ForeignKey("lawyers.id"), nullable=False)
    
    # Case details
    case_number = Column(String(50), unique=True, index=True)
    case_type = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Status and priority
    status = Column(Enum(CaseStatus), default=CaseStatus.PENDING)
    priority = Column(Enum(CasePriority), default=CasePriority.MEDIUM)
    
    # Important dates
    filed_date = Column(DateTime(timezone=True))
    deadline = Column(DateTime(timezone=True))
    completed_date = Column(DateTime(timezone=True))
    
    # Financial
    estimated_cost = Column(Numeric(10, 2))
    actual_cost = Column(Numeric(10, 2))
    
    # Tracking
    progress_percentage = Column(Integer, default=0)
    notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    client = relationship("Client", backref="cases")
    lawyer = relationship("Lawyer", backref="assigned_cases")
