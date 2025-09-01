"""
Billing schemas for API requests and responses
"""

from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal

class BillingCreate(BaseModel):
    case_id: int
    lawyer_id: int
    client_id: int
    invoice_number: str
    invoice_date: date
    due_date: date
    hours_worked: Decimal = Decimal('0.00')
    hourly_rate: Decimal
    subtotal: Decimal
    tax_amount: Decimal = Decimal('0.00')
    total_amount: Decimal
    description: Optional[str] = None
    services_rendered: Optional[str] = None

class BillingUpdate(BaseModel):
    invoice_date: Optional[date] = None
    due_date: Optional[date] = None
    hours_worked: Optional[Decimal] = None
    hourly_rate: Optional[Decimal] = None
    subtotal: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    status: Optional[str] = None
    description: Optional[str] = None
    services_rendered: Optional[str] = None
    notes: Optional[str] = None

class BillingSend(BaseModel):
    email_address: Optional[str] = None
    send_copy_to_lawyer: bool = True
    include_detailed_breakdown: bool = True
    custom_message: Optional[str] = None

class BillingResponse(BaseModel):
    billing_id: int
    case_id: int
    lawyer_id: int
    client_id: int
    invoice_number: str
    invoice_date: date
    due_date: date
    hours_worked: Decimal
    hourly_rate: Decimal
    subtotal: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    amount_paid: Decimal
    status: str
    payment_method: Optional[str] = None
    payment_date: Optional[date] = None
    payment_reference: Optional[str] = None
    description: Optional[str] = None
    services_rendered: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Computed properties
    balance_due: Decimal = Decimal('0.00')
    is_paid: bool = False
    is_overdue: bool = False
    
    # Related objects (if populated)
    case: Optional['CaseResponse'] = None
    lawyer: Optional['LawyerResponse'] = None
    client: Optional['ClientResponse'] = None

    class Config:
        from_attributes = True
        
    @property
    def id(self):
        return self.billing_id


class PaymentCreate(BaseModel):
    billing_id: int
    payment_amount: Decimal
    payment_date: date
    payment_method: str
    reference_number: Optional[str] = None
    notes: Optional[str] = None

class PaymentResponse(BaseModel):
    payment_id: int
    billing_id: int
    payment_amount: Decimal
    payment_date: date
    payment_method: str
    reference_number: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    recorded_by: Optional[int] = None
    
    # Related objects (if populated)
    billing_record: Optional[BillingResponse] = None

    class Config:
        from_attributes = True
        
    @property
    def id(self):
        return self.payment_id

# Import here to avoid circular import
from app.schemas.case import CaseResponse
from app.schemas.lawyer import LawyerResponse
from app.schemas.client import ClientResponse
BillingResponse.model_rebuild()
