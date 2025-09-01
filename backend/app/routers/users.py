"""
Users router - User management endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_token, get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserCreate

router = APIRouter()
security = HTTPBearer()

@router.get("/", response_model=List[UserResponse])
async def get_users(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin can get all users
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can access all users"
        )
    
    users = db.query(User).all()
    return [UserResponse.model_validate(user) for user in users]

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get user by ID (admin or self only)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Check if user can access this user data (admin or self)
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.model_validate(user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Update user (admin or self only)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Check if user can update this user data (admin or self)
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update user fields
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return UserResponse.model_validate(user)

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Delete user - soft delete (admin only)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin can delete users
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete users"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Soft delete - mark as inactive
    user.is_active = False
    db.commit()
    
    return {"message": "User deleted successfully"}

@router.get("/search/", response_model=List[UserResponse])
async def search_users(
    q: str = "",
    role: str = None,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Search users by criteria (admin only)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin can search users
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can search users"
        )
    
    query = db.query(User)
    
    if q:
        query = query.filter(
            User.first_name.contains(q) | 
            User.last_name.contains(q) | 
            User.email.contains(q)
        )
    
    if role:
        query = query.filter(User.role == role)
    
    users = query.all()
    return [UserResponse.model_validate(user) for user in users]