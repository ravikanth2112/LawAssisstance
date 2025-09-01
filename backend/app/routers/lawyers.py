"""
Lawyers router - Lawyer management endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.lawyer import Lawyer
from app.schemas.lawyer import LawyerResponse, LawyerCreate, LawyerUpdate

router = APIRouter()
security = HTTPBearer()

@router.get("/", response_model=List[LawyerResponse])
async def get_lawyers(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get all lawyers"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Get all lawyers with their user information
    lawyers = db.query(Lawyer).join(User).filter(User.is_active == True).all()
    return [LawyerResponse.model_validate(lawyer) for lawyer in lawyers]

@router.get("/{lawyer_id}", response_model=LawyerResponse)
async def get_lawyer_by_id(
    lawyer_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get lawyer by ID"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    lawyer = db.query(Lawyer).filter(Lawyer.lawyer_id == lawyer_id).first()
    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lawyer not found"
        )
    
    return LawyerResponse.model_validate(lawyer)

@router.post("/", response_model=LawyerResponse)
async def create_lawyer(
    lawyer_data: LawyerCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Create lawyer profile"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin can create lawyer profiles
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create lawyer profiles"
        )
    
    # Check if user exists and is a lawyer
    user = db.query(User).filter(User.user_id == lawyer_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.user_type != "lawyer":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must be of type 'lawyer'"
        )
    
    # Check if lawyer profile already exists
    existing_lawyer = db.query(Lawyer).filter(Lawyer.user_id == lawyer_data.user_id).first()
    if existing_lawyer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lawyer profile already exists for this user"
        )
    
    # Create lawyer profile
    lawyer = Lawyer(**lawyer_data.model_dump())
    db.add(lawyer)
    db.commit()
    db.refresh(lawyer)
    
    return LawyerResponse.model_validate(lawyer)

@router.put("/{lawyer_id}", response_model=LawyerResponse)
async def update_lawyer(
    lawyer_id: int,
    lawyer_update: LawyerUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Update lawyer profile"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    lawyer = db.query(Lawyer).filter(Lawyer.lawyer_id == lawyer_id).first()
    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lawyer not found"
        )
    
    # Check if user can update this lawyer profile (admin or self)
    if current_user.role != "admin" and current_user.id != lawyer.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update lawyer fields
    update_data = lawyer_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(lawyer, field, value)
    
    db.commit()
    db.refresh(lawyer)
    
    return LawyerResponse.model_validate(lawyer)

@router.delete("/{lawyer_id}")
async def delete_lawyer(
    lawyer_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Delete lawyer profile (admin only)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin can delete lawyer profiles
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete lawyer profiles"
        )
    
    lawyer = db.query(Lawyer).filter(Lawyer.lawyer_id == lawyer_id).first()
    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lawyer not found"
        )
    
    db.delete(lawyer)
    db.commit()
    
    return {"message": "Lawyer profile deleted successfully"}

@router.get("/me/profile", response_model=LawyerResponse)
async def get_my_lawyer_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current user's lawyer profile"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    if current_user.role != "lawyer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only lawyers can access this endpoint"
        )
    
    lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.id).first()
    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lawyer profile not found"
        )
    
    return LawyerResponse.model_validate(lawyer)