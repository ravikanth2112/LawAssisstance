"""
Deadline model for immigration case deadlines
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Deadline(Base):
    __tablename__ = "deadlines"

    deadline_id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"), nullable=False)
    lawyer_id = Column(Integer, ForeignKey("lawyers.lawyer_id"), nullable=False)
    
    # Deadline details
    deadline_type = Column(String(100), nullable=False)  # Filing, Response, Court Date, etc.
    title = Column(String(200), nullable=False)
    description = Column(Text)
    due_date = Column(Date, nullable=False)
    priority_level = Column(String(10), nullable=False)  # urgent, high, medium, low
    
    # Status tracking
    status = Column(String(20), nullable=False, default="pending")  # pending, completed, overdue
    is_court_deadline = Column(Boolean, default=False)
    completed_date = Column(Date)
    completion_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.user_id"))

    # Relationships
    case = relationship("Case", backref="deadlines")
    lawyer = relationship("Lawyer", backref="deadlines")
    creator = relationship("User", backref="created_deadlines")
    
    @property
    def id(self):
        return self.deadline_id
    
    @property
    def is_overdue(self):
        from datetime import date
        return self.due_date < date.today() and self.status == "pending"
    
    @property
    def days_remaining(self):
        from datetime import date
        return (self.due_date - date.today()).days
