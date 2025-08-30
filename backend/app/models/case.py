from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Date, Numeric, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class CaseStatus(enum.Enum):
    ACTIVE = "active"
    PENDING = "pending"
    COMPLETED = "completed"
    CLOSED = "closed"
    ON_HOLD = "on_hold"

class CasePriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Case(Base):
    __tablename__ = "cases"
    
    case_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    primary_lawyer_id = Column(Integer, ForeignKey("lawyers.lawyer_id"), nullable=False)
    case_number = Column(String(50), unique=True, nullable=False)
    case_type = Column(String(100), nullable=False)
    case_status = Column(SQLEnum(CaseStatus), default=CaseStatus.ACTIVE)
    priority_level = Column(SQLEnum(CasePriority), default=CasePriority.MEDIUM)
    filing_date = Column(Date)
    expected_completion = Column(Date)
    estimated_cost = Column(Numeric(12, 2))
    case_summary = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    client = relationship("Client", back_populates="cases")
    primary_lawyer = relationship("Lawyer", back_populates="primary_cases")
