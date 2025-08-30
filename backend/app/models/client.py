from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Client(Base):
    __tablename__ = "clients"
    
    client_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True, nullable=False)
    client_number = Column(String(50), unique=True, nullable=False)
    country_of_origin = Column(String(100))
    current_status = Column(String(100))
    preferred_language = Column(String(50))
    date_of_birth = Column(Date)
    emergency_contact = Column(String(200))
    emergency_phone = Column(String(20))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship
    user = relationship("User", back_populates="client")
