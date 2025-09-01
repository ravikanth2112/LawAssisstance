"""
Lawyer model
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Numeric, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Lawyer(Base):
    __tablename__ = "lawyers"

    lawyer_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True, nullable=False)
    bar_number = Column(String(50), unique=True)
    license_state = Column(String(50))
    specialization = Column(String(200))
    hourly_rate = Column(Numeric(10, 2))
    bio = Column(Text)
    admitted_date = Column(DateTime)
    is_partner = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", backref="lawyer_profile")
    
    # Add property for backward compatibility
    @property
    def id(self):
        return self.lawyer_id
