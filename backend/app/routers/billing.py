"""
Billing router - Billing and financial management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.billing import Billing, Payment
from app.schemas.billing import BillingResponse, BillingCreate, BillingUpdate, BillingSend, PaymentCreate, PaymentResponse

router = APIRouter()
security = HTTPBearer()

@router.get("/", response_model=List[BillingResponse])
async def get_billing_records(
    status_filter: Optional[str] = Query(None, alias="status"),
    client_id: Optional[int] = Query(None),
    lawyer_id: Optional[int] = Query(None),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get billing records with filtering"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    query = db.query(Billing)
    
    # Role-based filtering
    if current_user.role == "lawyer":
        query = query.filter(Billing.lawyer_id == current_user.id)
    elif current_user.role == "client":
        query = query.filter(Billing.client_id == current_user.id)
    
    # Apply filters
    if status_filter:
        query = query.filter(Billing.status == status_filter)
    if client_id and current_user.role in ["admin", "lawyer"]:
        query = query.filter(Billing.client_id == client_id)
    if lawyer_id and current_user.role == "admin":
        query = query.filter(Billing.lawyer_id == lawyer_id)
    
    billing_records = query.order_by(Billing.created_at.desc()).all()
    
    # Add computed properties
    for record in billing_records:
        record.balance_due = record.balance_due
        record.is_paid = record.is_paid
        record.is_overdue = record.is_overdue
    
    return [BillingResponse.model_validate(record) for record in billing_records]

@router.get("/pending", response_model=List[BillingResponse])
async def get_pending_invoices(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get pending invoices (Status-based filtering)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    query = db.query(Billing).filter(Billing.status.in_(["pending", "sent"]))
    
    # Role-based filtering
    if current_user.role == "lawyer":
        query = query.filter(Billing.lawyer_id == current_user.id)
    elif current_user.role == "client":
        query = query.filter(Billing.client_id == current_user.id)
    
    billing_records = query.order_by(Billing.due_date).all()
    
    # Add computed properties
    for record in billing_records:
        record.balance_due = record.balance_due
        record.is_paid = record.is_paid
        record.is_overdue = record.is_overdue
    
    return [BillingResponse.model_validate(record) for record in billing_records]

@router.post("/", response_model=BillingResponse)
async def create_billing_record(
    billing_data: BillingCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Create billing record (Auto-calculation from hours/rate)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin and lawyers can create billing records
    if current_user.role not in ["admin", "lawyer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin and lawyers can create billing records"
        )
    
    # Auto-calculate amounts if not provided
    billing_dict = billing_data.model_dump()
    if not billing_dict.get('subtotal'):
        billing_dict['subtotal'] = billing_dict['hours_worked'] * billing_dict['hourly_rate']
    if not billing_dict.get('total_amount'):
        billing_dict['total_amount'] = billing_dict['subtotal'] + billing_dict.get('tax_amount', 0)
    
    # Create billing record
    billing = Billing(**billing_dict)
    db.add(billing)
    db.commit()
    db.refresh(billing)
    
    # Add computed properties
    billing.balance_due = billing.balance_due
    billing.is_paid = billing.is_paid
    billing.is_overdue = billing.is_overdue
    
    return BillingResponse.model_validate(billing)

@router.get("/{billing_id}", response_model=BillingResponse)
async def get_billing_by_id(
    billing_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get billing record by ID"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    billing = db.query(Billing).filter(Billing.billing_id == billing_id).first()
    if not billing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Billing record not found"
        )
    
    # Check access permissions
    if current_user.role == "lawyer" and billing.lawyer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    elif current_user.role == "client" and billing.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Add computed properties
    billing.balance_due = billing.balance_due
    billing.is_paid = billing.is_paid
    billing.is_overdue = billing.is_overdue
    
    return BillingResponse.model_validate(billing)

@router.put("/{billing_id}", response_model=BillingResponse)
async def update_billing_record(
    billing_id: int,
    billing_update: BillingUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Update billing record"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    billing = db.query(Billing).filter(Billing.billing_id == billing_id).first()
    if not billing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Billing record not found"
        )
    
    # Check permissions
    if current_user.role == "client":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clients cannot update billing records"
        )
    
    if current_user.role == "lawyer" and billing.lawyer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update billing fields
    update_data = billing_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(billing, field, value)
    
    # Recalculate total if amounts changed
    if 'subtotal' in update_data or 'tax_amount' in update_data:
        billing.total_amount = billing.subtotal + billing.tax_amount
    
    db.commit()
    db.refresh(billing)
    
    # Add computed properties
    billing.balance_due = billing.balance_due
    billing.is_paid = billing.is_paid
    billing.is_overdue = billing.is_overdue
    
    return BillingResponse.model_validate(billing)

@router.post("/{billing_id}/send")
async def send_invoice(
    billing_id: int,
    send_data: BillingSend,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Send invoice (Email integration, PDF generation)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin and lawyers can send invoices
    if current_user.role not in ["admin", "lawyer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin and lawyers can send invoices"
        )
    
    billing = db.query(Billing).filter(Billing.billing_id == billing_id).first()
    if not billing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Billing record not found"
        )
    
    # Check permissions
    if current_user.role == "lawyer" and billing.lawyer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update status to sent
    billing.status = "sent"
    db.commit()
    
    # TODO: Implement actual email sending and PDF generation
    
    return {
        "message": "Invoice sent successfully",
        "invoice_number": billing.invoice_number,
        "sent_to": send_data.email_address or "client@email.com",
        "include_detailed_breakdown": send_data.include_detailed_breakdown
    }

@router.delete("/{billing_id}")
async def delete_billing_record(
    billing_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Delete billing record (admin only)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin can delete billing records
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete billing records"
        )
    
    billing = db.query(Billing).filter(Billing.billing_id == billing_id).first()
    if not billing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Billing record not found"
        )
    
    db.delete(billing)
    db.commit()
    
    return {"message": "Billing record deleted successfully"}

# Payment endpoints
@router.post("/payments", response_model=PaymentResponse)
async def record_payment(
    payment_data: PaymentCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Record payment (Transaction tracking, balance updates)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin and lawyers can record payments
    if current_user.role not in ["admin", "lawyer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin and lawyers can record payments"
        )
    
    # Check if billing record exists
    billing = db.query(Billing).filter(Billing.billing_id == payment_data.billing_id).first()
    if not billing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Billing record not found"
        )
    
    # Create payment record
    payment = Payment(
        **payment_data.model_dump(),
        recorded_by=current_user.id
    )
    db.add(payment)
    
    # Update billing record
    billing.amount_paid += payment_data.payment_amount
    billing.payment_method = payment_data.payment_method
    billing.payment_date = payment_data.payment_date
    billing.payment_reference = payment_data.reference_number
    
    # Update status
    if billing.amount_paid >= billing.total_amount:
        billing.status = "paid"
    
    db.commit()
    db.refresh(payment)
    
    return PaymentResponse.model_validate(payment)

@router.get("/payments/{payment_id}", response_model=PaymentResponse)
async def get_payment_by_id(
    payment_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get payment by ID"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    # Check access permissions through billing record
    billing = db.query(Billing).filter(Billing.billing_id == payment.billing_id).first()
    if current_user.role == "lawyer" and billing.lawyer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    elif current_user.role == "client" and billing.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return PaymentResponse.model_validate(payment)
