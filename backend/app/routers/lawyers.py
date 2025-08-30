from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import User, Lawyer, UserType
from app.schemas import LawyerCreate, LawyerUpdate, LawyerResponse, LawyerWithUser
from app.routers.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=dict)
async def get_lawyers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    specialization: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all lawyers with pagination and filtering."""
    query = db.query(Lawyer).join(User).filter(User.is_active == True)
    
    # Apply filters
    if specialization:
        query = query.filter(Lawyer.specialization.ilike(f"%{specialization}%"))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    lawyers = query.offset(skip).limit(limit).all()
    
    return {
        "success": True,
        "data": [
            {
                "lawyer_id": lawyer.lawyer_id,
                "user_id": lawyer.user_id,
                "bar_number": lawyer.bar_number,
                "license_state": lawyer.license_state,
                "specialization": lawyer.specialization,
                "hourly_rate": float(lawyer.hourly_rate) if lawyer.hourly_rate else None,
                "bio": lawyer.bio,
                "admitted_date": lawyer.admitted_date.isoformat() if lawyer.admitted_date else None,
                "is_partner": lawyer.is_partner,
                "created_at": lawyer.created_at.isoformat(),
                "updated_at": lawyer.updated_at.isoformat(),
                "user": {
                    "email": lawyer.user.email,
                    "first_name": lawyer.user.first_name,
                    "last_name": lawyer.user.last_name,
                    "phone": lawyer.user.phone
                } if lawyer.user else None
            } for lawyer in lawyers
        ],
        "pagination": {
            "page": (skip // limit) + 1,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        },
        "message": "Lawyers retrieved successfully",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/", response_model=dict)
async def create_lawyer(
    lawyer_data: LawyerCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new lawyer profile."""
    # Check if user exists and is not already a lawyer
    user = db.query(User).filter(User.user_id == lawyer_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.user_type != UserType.LAWYER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have lawyer user type"
        )
    
    # Check if lawyer profile already exists
    existing_lawyer = db.query(Lawyer).filter(Lawyer.user_id == lawyer_data.user_id).first()
    if existing_lawyer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lawyer profile already exists for this user"
        )
    
    # Check if bar number is unique
    existing_bar = db.query(Lawyer).filter(Lawyer.bar_number == lawyer_data.bar_number).first()
    if existing_bar:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bar number already exists"
        )
    
    # Create lawyer profile
    db_lawyer = Lawyer(
        user_id=lawyer_data.user_id,
        bar_number=lawyer_data.bar_number,
        license_state=lawyer_data.license_state,
        specialization=lawyer_data.specialization,
        hourly_rate=lawyer_data.hourly_rate,
        bio=lawyer_data.bio,
        admitted_date=lawyer_data.admitted_date,
        is_partner=lawyer_data.is_partner
    )
    
    db.add(db_lawyer)
    db.commit()
    db.refresh(db_lawyer)
    
    return {
        "success": True,
        "data": {
            "lawyer_id": db_lawyer.lawyer_id,
            "user_id": db_lawyer.user_id,
            "bar_number": db_lawyer.bar_number,
            "license_state": db_lawyer.license_state,
            "specialization": db_lawyer.specialization,
            "hourly_rate": float(db_lawyer.hourly_rate) if db_lawyer.hourly_rate else None,
            "bio": db_lawyer.bio,
            "admitted_date": db_lawyer.admitted_date.isoformat() if db_lawyer.admitted_date else None,
            "is_partner": db_lawyer.is_partner,
            "created_at": db_lawyer.created_at.isoformat(),
            "updated_at": db_lawyer.updated_at.isoformat()
        },
        "message": "Lawyer profile created successfully",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/{lawyer_id}", response_model=dict)
async def get_lawyer(
    lawyer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get lawyer by ID."""
    lawyer = db.query(Lawyer).join(User).filter(
        Lawyer.lawyer_id == lawyer_id,
        User.is_active == True
    ).first()
    
    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lawyer not found"
        )
    
    return {
        "success": True,
        "data": {
            "lawyer_id": lawyer.lawyer_id,
            "user_id": lawyer.user_id,
            "bar_number": lawyer.bar_number,
            "license_state": lawyer.license_state,
            "specialization": lawyer.specialization,
            "hourly_rate": float(lawyer.hourly_rate) if lawyer.hourly_rate else None,
            "bio": lawyer.bio,
            "admitted_date": lawyer.admitted_date.isoformat() if lawyer.admitted_date else None,
            "is_partner": lawyer.is_partner,
            "created_at": lawyer.created_at.isoformat(),
            "updated_at": lawyer.updated_at.isoformat(),
            "user": {
                "email": lawyer.user.email,
                "first_name": lawyer.user.first_name,
                "last_name": lawyer.user.last_name,
                "phone": lawyer.user.phone
            } if lawyer.user else None
        },
        "message": "Lawyer retrieved successfully",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.put("/{lawyer_id}", response_model=dict)
async def update_lawyer(
    lawyer_id: int,
    lawyer_update: LawyerUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update lawyer profile."""
    lawyer = db.query(Lawyer).filter(Lawyer.lawyer_id == lawyer_id).first()
    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lawyer not found"
        )
    
    # Check permissions (admin or self)
    if current_user.user_type != UserType.ADMIN and current_user.user_id != lawyer.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if bar number is unique (if being updated)
    if lawyer_update.bar_number and lawyer_update.bar_number != lawyer.bar_number:
        existing_bar = db.query(Lawyer).filter(Lawyer.bar_number == lawyer_update.bar_number).first()
        if existing_bar:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bar number already exists"
            )
    
    # Update fields
    update_data = lawyer_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(lawyer, field, value)
    
    db.commit()
    db.refresh(lawyer)
    
    return {
        "success": True,
        "data": {
            "lawyer_id": lawyer.lawyer_id,
            "user_id": lawyer.user_id,
            "bar_number": lawyer.bar_number,
            "license_state": lawyer.license_state,
            "specialization": lawyer.specialization,
            "hourly_rate": float(lawyer.hourly_rate) if lawyer.hourly_rate else None,
            "bio": lawyer.bio,
            "admitted_date": lawyer.admitted_date.isoformat() if lawyer.admitted_date else None,
            "is_partner": lawyer.is_partner,
            "created_at": lawyer.created_at.isoformat(),
            "updated_at": lawyer.updated_at.isoformat()
        },
        "message": "Lawyer profile updated successfully",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/available", response_model=dict)
async def get_available_lawyers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get available lawyers for case assignment."""
    lawyers = db.query(Lawyer).join(User).filter(User.is_active == True).all()
    
    return {
        "success": True,
        "data": [
            {
                "lawyer_id": lawyer.lawyer_id,
                "user_id": lawyer.user_id,
                "bar_number": lawyer.bar_number,
                "specialization": lawyer.specialization,
                "hourly_rate": float(lawyer.hourly_rate) if lawyer.hourly_rate else None,
                "full_name": f"{lawyer.user.first_name} {lawyer.user.last_name}",
                "email": lawyer.user.email
            } for lawyer in lawyers
        ],
        "message": "Available lawyers retrieved successfully",
        "timestamp": datetime.utcnow().isoformat()
    }
