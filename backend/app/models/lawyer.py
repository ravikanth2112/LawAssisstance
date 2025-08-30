from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Lawyer(Base):
    __tablename__ = "lawyers"
    
    lawyer_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True, nullable=False)
    bar_number = Column(String(50), unique=True, nullable=False)
    license_state = Column(String(50), nullable=False)
    specialization = Column(String(200))
    hourly_rate = Column(Numeric(10, 2))
    bio = Column(Text)
    admitted_date = Column(DateTime)
    is_partner = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship
    user = relationship("User", back_populates="lawyer")
