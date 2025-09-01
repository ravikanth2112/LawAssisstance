"""
Activity model for tracking case activities and time logging
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Numeric, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Activity(Base):
    __tablename__ = "activities"

    activity_id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"), nullable=False)
    lawyer_id = Column(Integer, ForeignKey("lawyers.lawyer_id"), nullable=False)
    
    # Activity details
    activity_type = Column(String(100), nullable=False)  # meeting, call, research, filing, etc.
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    
    # Time tracking
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    hours_spent = Column(Numeric(8, 2), nullable=False)
    
    # Billing information
    is_billable = Column(Boolean, default=True)
    hourly_rate = Column(Numeric(10, 2))
    billed_amount = Column(Numeric(12, 2))
    billing_status = Column(String(20), default="unbilled")  # unbilled, billed, paid
    
    # Status
    status = Column(String(20), nullable=False, default="completed")  # in_progress, completed, cancelled
    
    # Timestamps
    activity_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    case = relationship("Case", backref="activities")
    lawyer = relationship("Lawyer", backref="activities")
    
    @property
    def id(self):
        return self.activity_id
    
    @property
    def duration_hours(self):
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            return round(delta.total_seconds() / 3600, 2)
        return float(self.hours_spent)
