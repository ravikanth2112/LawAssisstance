from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.database import get_db
from app.models import User, Case, Client, Lawyer, UserType, CaseStatus, CasePriority
from app.schemas import CaseCreate, CaseUpdate, CaseResponse, CaseWithDetails
from app.routers.auth import get_current_user
from datetime import datetime
import uuid

router = APIRouter()

def generate_case_number():
    """Generate a unique case number."""
    return f"CS{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"

@router.get("/", response_model=dict)
async def get_cases(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    lawyer_id: Optional[int] = Query(None),
    client_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all cases with pagination and filtering (filtered by user role)."""
    query = db.query(Case).join(Client).join(User).filter(User.is_active == True)
    
    # Role-based filtering
    if current_user.user_type == UserType.CLIENT:
        # Clients can only see their own cases
        client = db.query(Client).filter(Client.user_id == current_user.user_id).first()
        if client:
            query = query.filter(Case.client_id == client.client_id)
        else:
            # No client profile, return empty
            return {
                "success": True,
                "data": [],
                "pagination": {"page": 1, "limit": limit, "total": 0, "pages": 0},
                "message": "No cases found",
                "timestamp": datetime.utcnow().isoformat()
            }
    elif current_user.user_type == UserType.LAWYER:
        # Lawyers can see cases they are assigned to
        lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.user_id).first()
        if lawyer:
            query = query.filter(Case.primary_lawyer_id == lawyer.lawyer_id)
        else:
            # No lawyer profile, return empty
            return {
                "success": True,
                "data": [],
                "pagination": {"page": 1, "limit": limit, "total": 0, "pages": 0},
                "message": "No cases found",
                "timestamp": datetime.utcnow().isoformat()
            }
    # Admin can see all cases (no additional filtering)
    
    # Apply filters
    if status:
        try:
            status_enum = CaseStatus(status)
            query = query.filter(Case.case_status == status_enum)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid case status"
            )
    
    if priority:
        try:
            priority_enum = CasePriority(priority)
            query = query.filter(Case.priority_level == priority_enum)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid case priority"
            )
    
    if lawyer_id:
        query = query.filter(Case.primary_lawyer_id == lawyer_id)
    
    if client_id:
        query = query.filter(Case.client_id == client_id)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    cases = query.offset(skip).limit(limit).all()
    
    return {
        "success": True,
        "data": [
            {
                "case_id": case.case_id,
                "client_id": case.client_id,
                "primary_lawyer_id": case.primary_lawyer_id,
                "case_number": case.case_number,
                "case_type": case.case_type,
                "case_status": case.case_status.value,
                "priority_level": case.priority_level.value,
                "filing_date": case.filing_date.isoformat() if case.filing_date else None,
                "expected_completion": case.expected_completion.isoformat() if case.expected_completion else None,
                "estimated_cost": float(case.estimated_cost) if case.estimated_cost else None,
                "case_summary": case.case_summary,
                "created_at": case.created_at.isoformat(),
                "updated_at": case.updated_at.isoformat(),
                "client": {
                    "client_number": case.client.client_number,
                    "full_name": f"{case.client.user.first_name} {case.client.user.last_name}",
                    "email": case.client.user.email
                } if case.client and case.client.user else None,
                "primary_lawyer": {
                    "bar_number": case.primary_lawyer.bar_number,
                    "full_name": f"{case.primary_lawyer.user.first_name} {case.primary_lawyer.user.last_name}",
                    "specialization": case.primary_lawyer.specialization
                } if case.primary_lawyer and case.primary_lawyer.user else None
            } for case in cases
        ],
        "pagination": {
            "page": (skip // limit) + 1,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        },
        "message": "Cases retrieved successfully",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/", response_model=dict)
async def create_case(
    case_data: CaseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new case."""
    # Only lawyers and admins can create cases
    if current_user.user_type not in [UserType.LAWYER, UserType.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Verify client exists
    client = db.query(Client).filter(Client.client_id == case_data.client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Verify lawyer exists
    lawyer = db.query(Lawyer).filter(Lawyer.lawyer_id == case_data.primary_lawyer_id).first()
    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lawyer not found"
        )
    
    # Generate unique case number
    case_number = case_data.case_number or generate_case_number()
    
    # Check if case number is unique
    existing_case = db.query(Case).filter(Case.case_number == case_number).first()
    if existing_case:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Case number already exists"
        )
    
    # Create case
    db_case = Case(
        client_id=case_data.client_id,
        primary_lawyer_id=case_data.primary_lawyer_id,
        case_number=case_number,
        case_type=case_data.case_type,
        case_status=case_data.case_status,
        priority_level=case_data.priority_level,
        filing_date=case_data.filing_date,
        expected_completion=case_data.expected_completion,
        estimated_cost=case_data.estimated_cost,
        case_summary=case_data.case_summary
    )
    
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    
    return {
        "success": True,
        "data": {
            "case_id": db_case.case_id,
            "client_id": db_case.client_id,
            "primary_lawyer_id": db_case.primary_lawyer_id,
            "case_number": db_case.case_number,
            "case_type": db_case.case_type,
            "case_status": db_case.case_status.value,
            "priority_level": db_case.priority_level.value,
            "filing_date": db_case.filing_date.isoformat() if db_case.filing_date else None,
            "expected_completion": db_case.expected_completion.isoformat() if db_case.expected_completion else None,
            "estimated_cost": float(db_case.estimated_cost) if db_case.estimated_cost else None,
            "case_summary": db_case.case_summary,
            "created_at": db_case.created_at.isoformat(),
            "updated_at": db_case.updated_at.isoformat()
        },
        "message": "Case created successfully",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/statistics", response_model=dict)
async def get_case_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get case statistics for dashboard."""
    query = db.query(Case)
    
    # Apply role-based filtering
    if current_user.user_type == UserType.CLIENT:
        client = db.query(Client).filter(Client.user_id == current_user.user_id).first()
        if client:
            query = query.filter(Case.client_id == client.client_id)
        else:
            query = query.filter(False)  # No results
    elif current_user.user_type == UserType.LAWYER:
        lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.user_id).first()
        if lawyer:
            query = query.filter(Case.primary_lawyer_id == lawyer.lawyer_id)
        else:
            query = query.filter(False)  # No results
    
    # Get statistics
    total_cases = query.count()
    active_cases = query.filter(Case.case_status == CaseStatus.ACTIVE).count()
    pending_cases = query.filter(Case.case_status == CaseStatus.PENDING).count()
    completed_cases = query.filter(Case.case_status == CaseStatus.COMPLETED).count()
    
    # Cases by priority
    high_priority = query.filter(Case.priority_level == CasePriority.HIGH).count()
    urgent_priority = query.filter(Case.priority_level == CasePriority.URGENT).count()
    
    # Cases by status
    status_breakdown = {}
    for status in CaseStatus:
        count = query.filter(Case.case_status == status).count()
        status_breakdown[status.value] = count
    
    return {
        "success": True,
        "data": {
            "total_cases": total_cases,
            "active_cases": active_cases,
            "pending_cases": pending_cases,
            "completed_cases": completed_cases,
            "high_priority_cases": high_priority,
            "urgent_cases": urgent_priority,
            "cases_by_status": status_breakdown
        },
        "message": "Case statistics retrieved successfully",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/{case_id}", response_model=dict)
async def get_case(
    case_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get case details with client and lawyer information."""
    case = db.query(Case).filter(Case.case_id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Check permissions
    has_access = False
    if current_user.user_type == UserType.ADMIN:
        has_access = True
    elif current_user.user_type == UserType.CLIENT:
        client = db.query(Client).filter(Client.user_id == current_user.user_id).first()
        if client and case.client_id == client.client_id:
            has_access = True
    elif current_user.user_type == UserType.LAWYER:
        lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.user_id).first()
        if lawyer and case.primary_lawyer_id == lawyer.lawyer_id:
            has_access = True
    
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return {
        "success": True,
        "data": {
            "case_id": case.case_id,
            "client_id": case.client_id,
            "primary_lawyer_id": case.primary_lawyer_id,
            "case_number": case.case_number,
            "case_type": case.case_type,
            "case_status": case.case_status.value,
            "priority_level": case.priority_level.value,
            "filing_date": case.filing_date.isoformat() if case.filing_date else None,
            "expected_completion": case.expected_completion.isoformat() if case.expected_completion else None,
            "estimated_cost": float(case.estimated_cost) if case.estimated_cost else None,
            "case_summary": case.case_summary,
            "created_at": case.created_at.isoformat(),
            "updated_at": case.updated_at.isoformat(),
            "client": {
                "client_id": case.client.client_id,
                "client_number": case.client.client_number,
                "country_of_origin": case.client.country_of_origin,
                "current_status": case.client.current_status,
                "user": {
                    "first_name": case.client.user.first_name,
                    "last_name": case.client.user.last_name,
                    "email": case.client.user.email,
                    "phone": case.client.user.phone
                }
            } if case.client and case.client.user else None,
            "primary_lawyer": {
                "lawyer_id": case.primary_lawyer.lawyer_id,
                "bar_number": case.primary_lawyer.bar_number,
                "specialization": case.primary_lawyer.specialization,
                "hourly_rate": float(case.primary_lawyer.hourly_rate) if case.primary_lawyer.hourly_rate else None,
                "user": {
                    "first_name": case.primary_lawyer.user.first_name,
                    "last_name": case.primary_lawyer.user.last_name,
                    "email": case.primary_lawyer.user.email,
                    "phone": case.primary_lawyer.user.phone
                }
            } if case.primary_lawyer and case.primary_lawyer.user else None
        },
        "message": "Case details retrieved successfully",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.put("/{case_id}", response_model=dict)
async def update_case(
    case_id: int,
    case_update: CaseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update case."""
    case = db.query(Case).filter(Case.case_id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Check permissions (admin or assigned lawyer)
    has_access = False
    if current_user.user_type == UserType.ADMIN:
        has_access = True
    elif current_user.user_type == UserType.LAWYER:
        lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.user_id).first()
        if lawyer and case.primary_lawyer_id == lawyer.lawyer_id:
            has_access = True
    
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update fields
    update_data = case_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(case, field, value)
    
    db.commit()
    db.refresh(case)
    
    return {
        "success": True,
        "data": {
            "case_id": case.case_id,
            "client_id": case.client_id,
            "primary_lawyer_id": case.primary_lawyer_id,
            "case_number": case.case_number,
            "case_type": case.case_type,
            "case_status": case.case_status.value,
            "priority_level": case.priority_level.value,
            "filing_date": case.filing_date.isoformat() if case.filing_date else None,
            "expected_completion": case.expected_completion.isoformat() if case.expected_completion else None,
            "estimated_cost": float(case.estimated_cost) if case.estimated_cost else None,
            "case_summary": case.case_summary,
            "created_at": case.created_at.isoformat(),
            "updated_at": case.updated_at.isoformat()
        },
        "message": "Case updated successfully",
        "timestamp": datetime.utcnow().isoformat()
    }
