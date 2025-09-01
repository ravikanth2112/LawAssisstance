"""
Billing model for case billing and financial tracking
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Numeric, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Billing(Base):
    __tablename__ = "billing"

    billing_id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"), nullable=False)
    lawyer_id = Column(Integer, ForeignKey("lawyers.lawyer_id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    
    # Invoice details
    invoice_number = Column(String(50), unique=True, index=True)
    invoice_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    
    # Financial details
    hours_worked = Column(Numeric(8, 2), default=0)
    hourly_rate = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(12, 2), nullable=False)
    tax_amount = Column(Numeric(12, 2), default=0)
    total_amount = Column(Numeric(12, 2), nullable=False)
    amount_paid = Column(Numeric(12, 2), default=0)
    
    # Status and payment tracking
    status = Column(String(20), nullable=False, default="pending")  # pending, sent, paid, overdue, cancelled
    payment_method = Column(String(50))  # check, credit_card, bank_transfer, etc.
    payment_date = Column(Date)
    payment_reference = Column(String(100))
    
    # Description and notes
    description = Column(Text)
    services_rendered = Column(Text)
    notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    case = relationship("Case", backref="billing_records")
    lawyer = relationship("Lawyer", backref="billing_records")
    client = relationship("Client", backref="billing_records")
    
    @property
    def id(self):
        return self.billing_id
    
    @property
    def balance_due(self):
        return float(self.total_amount - self.amount_paid)
    
    @property
    def is_paid(self):
        return self.amount_paid >= self.total_amount
    
    @property
    def is_overdue(self):
        from datetime import date
        return self.due_date < date.today() and not self.is_paid


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    billing_id = Column(Integer, ForeignKey("billing.billing_id"), nullable=False)
    
    # Payment details
    payment_amount = Column(Numeric(12, 2), nullable=False)
    payment_date = Column(Date, nullable=False)
    payment_method = Column(String(50), nullable=False)
    reference_number = Column(String(100))
    
    # Notes
    notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    recorded_by = Column(Integer, ForeignKey("users.user_id"))

    # Relationships
    billing_record = relationship("Billing", backref="payments")
    recorder = relationship("User", backref="recorded_payments")
    
    @property
    def id(self):
        return self.payment_id
