"""
Immigration case model
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Numeric, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Case(Base):
    __tablename__ = "cases"

    case_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    primary_lawyer_id = Column(Integer, ForeignKey("lawyers.lawyer_id"), nullable=False)
    
    # Case details
    case_number = Column(String(50), unique=True, index=True)
    case_type = Column(String(100), nullable=False)
    case_status = Column(String(9), nullable=False)  # Using String to match DB
    priority_level = Column(String(6), nullable=False)  # Using String to match DB
    
    # Important dates
    filing_date = Column(Date)
    expected_completion = Column(Date)
    
    # Financial
    estimated_cost = Column(Numeric(12, 2))
    
    # Summary
    case_summary = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    client = relationship("Client", backref="cases")
    primary_lawyer = relationship("Lawyer", backref="assigned_cases")
    
    # Add property for backward compatibility
    @property
    def id(self):
        return self.case_id
    
    @property
    def lawyer_id(self):
        return self.primary_lawyer_id
